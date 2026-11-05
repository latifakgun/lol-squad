"""LoL maç sonu ses botu.

/bitti → Riot API'den ekibin son maçı → Argon konuşma metni yazar → Gemini TTS (Pro, Fenrir) seslendirir
→ bot komutu yazanın ses kanalına girer, okur, çıkar.

Çalıştır:  python bot.py
Discord'suz deneme:  python bot.py --test ornek_mac.json   (Argon + TTS → out/test.wav)
Kurulum: README.md
"""
import asyncio
import json
import os
import pathlib
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import wave

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
STATE = HERE / "state.json"
BUSY = HERE / ".mesgul"  # /bitti sürerken var; güncelleme okunan sesi kesmesin (4 Kas: push 6. maçın TTS'ini kesti)
HISTORY = HERE / "gecmis.json"  # okunan metinler: akşamın hafızası + tekrar etmeme
SESSION_GAP = 4 * 3600 * 1000  # son maçtan 4 saat geçtiyse yeni akşam (gece yarısını geçen maçlar aynı akşama sayılır)

# key: (oyun adı, etiket, konuşmada söylenen ad)
SQUAD = {
    "l4cg": ("l4cg", "TR1", "Latif"),
    "minte": ("minte", "000", "Minte"),
    "swag": ("swagisback", "333", "Swag"),
    "patrick": ("Patrick Cem", "OMEN", "Patrick"),
    "yilmaz": ("ÖLÜYARAK31", "TR1", "Yılmaz"),
    "gorkem": ("Misty Minstrel", "1895", "Görkem"),
    "taner": ("hTune", "SF90", "Taner"),
    "eda": ("ibo kaypakkaya", "111", "Eda"),
    "malatya": ("MalatyaJigolosu", "AYIII", "Malatya Jigolosu"),
    "domalango": ("DOMALANGO", "chu", "Domalango"),
    "ateck": ("ateck28", "2828", "Ateck"),
}
KONUSMA = HERE.parent / "kulak" / "konusmalar"  # kulak'ın /git sonrası yazdığı konuşma dökümleri (konusma.py)
RIOT = "https://europe.api.riotgames.com"
ARGON_MODEL = "gemini-4-argon"
TTS_MODEL, TTS_VOICE = "gemini-2.5-pro-tts", "Fenrir"
# Ton tarifi metnin başına "<tarif> oku:" diye gider. Uzun, emir kipli talimat sesli okundu (26 Eki); kısa bir ses tarifi olarak kalsın.
TTS_STYLE = "Samimi, enerjik, gülerek laf sokan bir Türk Twitch yayıncısı sesiyle"
# Tekrarı model tarafında "tekrar etme" demek kırmıyor: açı, açılış ve Patrick lafları burada rastgele seçilir.
ANGLES = [
    "maçı belirleyen tek an: o anı kim, nasıl yaşattı",
    "en iyi oynayan: maçı onun gözünden anlat",
    "en kötü oynayan: maçı nasıl kendi eliyle sattı ya da az kalsın satıyordu",
    "maçın en saçma istatistiği: o sayıdan yola çıkıp herkese bağla",
    "koridor savaşları: ekipten herkes kendi rakibine karşı nasıl gitti",
    "şampiyon ve eşya seçimleri: kim neyi aldı, mantıklı mıydı",
    "altın farkı hikâyesi: maç nerede kırıldı, nasıl döndü ya da elden kaçtı",
    "takım oyunu: birlikte mi oynandı, herkes kendi kafasına mı",
]
TALIMAT = {
    "iyi": "SADECE küfürlü, coşkulu öv. Hiçbir eleştiri, 'ama', kusur, rün ya da eşya lafı yok.",
    "orta": "İyi yaptığını küfürlü öv, kötü yaptığını küfürlü göm; ikisi de kısa.",
    "kötü": "Sayılarıyla küfürlü göm.",
}
# Kimse kötü oynamadıysa bu açılar elenir: kusur aramaya zorluyorlar.
NEGATIVE_ANGLES = {ANGLES[2], ANGLES[3], ANGLES[7]}
OPENINGS = [
    "doğrudan en çarpıcı olayla, sanki biri az önce sormuş gibi",
    "sahte sakin bir başlangıç, sonra patlama",
    "bir soru sorup cevabını kendin vererek",
    "maçı tek kelimeyle özetleyip sonra açarak",
    "birisi hakkında kısa, kesin bir hüküm cümlesiyle",
    "maç spikeri gibi, anons eder gibi",
    "fısıldar gibi bir sır vererek",
]
PATRICK_LINES = ["Yarma ya, yarma!", "Ölüsünü sikicem onun!", "Ya kanka hadi ya!", "Ya yok amına koyayım ya!"]
# Kötü oynayan iki kişiye heceye bölünmüş ikili adı: ikisi yan yana gelince küfür çıkar.
DUO_NAMES = [("Yar", "Rak"), ("Am", "Cık"), ("Sa", "Lak"), ("Ga", "Vat"), ("Beyin", "Siz"), ("E", "Zik"), ("Dan", "Galak"), ("Ap", "Tal")]
DUO_TOP, DUO_TOP_CHANCE = DUO_NAMES[:2], 0.8  # Latif 3 Kas: ikili adı çoğunlukla Yar-Rak ya da Am-Cık
PATRICK_LINE_CHANCE, DUO_CHANCE = 0.4, 0.35  # ponytail: elle seçilmiş sıklık; hâlâ sık/seyrek gelirse buradan ayarla
QUEUES = {400: "Normal", 420: "Dereceli Tek/Çift", 430: "Normal", 440: "Esnek", 450: "ARAM", 490: "Hızlı Oyun"}


def load_env():
    env = HERE / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


# ---------- Riot ----------

UA = {"User-Agent": "lol-squad-bot/1.0 (+https://github.com/latifakgun/lol-squad)"}  # Cloudflare Python-urllib'i 1010 ile reddediyor
BOOTS = set()  # item_names doldurur
RUNES = {}  # item_names doldurur: rün kimliği → Türkçe ad (eşya kimlikleriyle çakışabildiği için ayrı)


def get_json(url, headers=None):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=15) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            # 429: Riot servis yoğunluğu ya da hız sınırı; Retry-After kadar bekleyip tekrar dene.
            if e.code != 429 or attempt == 3:
                raise
            time.sleep(int(e.headers.get("Retry-After") or 2 * (attempt + 1)))
        except (urllib.error.URLError, TimeoutError, ConnectionError):  # laptopta DNS/bağlantı ara sıra kopuyor
            if attempt == 3:
                raise
            time.sleep(3)


def riot_get(path):
    return get_json(RIOT + path, {"X-Riot-Token": os.environ["RIOT_API_KEY"]})


def puuids():
    # Biri Riot ID'sini değiştirince 404 bütün /bitti'yi düşürüyordu (5 Kas, DOMALANGO#chu): o kişi atlanır.
    q, out = urllib.parse.quote, {}
    for k, (n, t, _) in SQUAD.items():
        try:
            out[k] = riot_get(f"/riot/account/v1/accounts/by-riot-id/{q(n)}/{q(t)}")["puuid"]
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
            print(f"Riot ID bulunamadı, atlandı: {n}#{t}", flush=True)
    return out


def item_names():
    ver = get_json("https://ddragon.leagueoflegends.com/api/versions.json")[0]
    data = get_json(f"https://ddragon.leagueoflegends.com/cdn/{ver}/data/tr_TR/item.json")
    BOOTS.update(int(i) for i, v in data["data"].items() if "Boots" in v.get("tags", []))  # 3. kademe çizmeler de (Zincirli Eziciler): adından anlaşılmıyor
    for style in get_json(f"https://ddragon.leagueoflegends.com/cdn/{ver}/data/tr_TR/runesReforged.json"):
        RUNES[style["id"]] = style["name"]
        RUNES.update((r["id"], r["name"]) for slot in style["slots"] for r in slot["runes"])
    return {int(i): v["name"] for i, v in data["data"].items()}


def latest_match_id(ids_by_key, done):
    """Ekipten en az ikisinin birlikte oynadığı, en yeni, henüz analiz edilmemiş maç (tek kişinin solo maçı sayılmaz)."""
    seen = {}
    for p in ids_by_key.values():
        for i in riot_get(f"/lol/match/v5/matches/by-puuid/{p}/ids?count=5"):
            seen[i] = seen.get(i, 0) + 1
    fresh = sorted((i for i, n in seen.items() if n >= 2 and i not in done), key=lambda i: int(i.split("_")[1]))
    return fresh[-1] if fresh else None


def summarize(match, ids_by_key, items):
    info = match["info"]
    key_of = {p: k for k, p in ids_by_key.items()}
    mins = info["gameDuration"] / 60

    def row(p):
        cs = p["totalMinionsKilled"] + p["neutralMinionsKilled"]
        slots = [p.get(k) for k in [*(f"item{i}" for i in range(6)), "roleBoundItem"]]
        return {
            "boots": next((items.get(i) for i in slots if i in BOOTS), None),
            "champ": p["championName"], "role": p.get("teamPosition") or "-", "win": p["win"],
            "kills": p["kills"], "deaths": p["deaths"], "assists": p["assists"],
            "cs": cs, "cs_per_min": round(cs / mins, 1), "gold": p["goldEarned"],
            "damage": p["totalDamageDealtToChampions"], "vision": p["visionScore"],
            "magic_damage": p.get("magicDamageDealtToChampions"), "physical_damage": p.get("physicalDamageDealtToChampions"),
            "kill_participation": round(p.get("challenges", {}).get("killParticipation", 0) * 100),
            "items": [items.get(p[k], "") for k in [*(f"item{i}" for i in range(6)), "roleBoundItem"] if p.get(k)],
            "level": p.get("summonerLevel"),
        }

    squad, others = {}, []
    for p in info["participants"]:
        k = key_of.get(p["puuid"])
        if k:
            ch = p.get("challenges", {})
            squad[SQUAD[k][2]] = {**row(p), "skillshots_hit": ch.get("skillshotsHit"), "skillshots_dodged": ch.get("skillshotsDodged"),
                                  "q_w_e_r_casts": [p.get(f"spell{i}Casts") for i in range(1, 5)],
                                  "solo_kills": ch.get("soloKills"), "control_wards": ch.get("controlWardsPlaced"),
                                  # ana ağaç (ilk ad = temel rün), sonra ikincil ağaç
                                  "runes": [RUNES.get(x) for s in p.get("perks", {}).get("styles", [])
                                            for x in [s["style"], *(sel["perk"] for sel in s["selections"])]]}
        else:
            others.append({"name": p.get("riotIdGameName"), "team_win": p["win"], **row(p)})
    # Veri maç SONUNDAKİ envanter: geç oyunda çizme satılıp yerine eşya alınır (4 Kas: "çizme almamışsın" yanlış alarmı).
    for v in squad.values():
        if not v["boots"] and mins >= 25:
            v["boots"] = "yok, büyük ihtimalle slot için satıldı (hata değil)"
    return {"queue": QUEUES.get(info["queueId"], str(info["queueId"])), "minutes": round(mins),
            "squad": squad, "others": others}


def region(x, y, our_team):
    """Harita koordinatından kaba bölge. ponytail: köşegen/şerit eşikleri elle; yanlış etiket görülürse eşikleri daralt."""
    blue_side = x + y < 14800
    side = "bizim" if blue_side == (our_team == 100) else "rakip"
    if x < 3600 and y < 3600 or x > 11200 and y > 11200:
        return f"{side} üs"
    if abs(y - x) < 1800:
        return f"orta koridor ({side} taraf)"
    if x < 2200 or y > 12700:
        return "üst koridor"
    if y < 2200 or x > 12700:
        return "alt koridor"
    if abs(x + y - 14800) < 1600:
        return "nehir"
    return f"{side} orman"


def moments(match, timeline, ids_by_key):
    """Ekipten birinin karıştığı kill/ölümler + objektifler, zaman sırasıyla."""
    info = match["info"]
    key_of = {p: k for k, p in ids_by_key.items()}
    our_team = next(p["teamId"] for p in info["participants"] if p["puuid"] in key_of)
    who = {}  # participantId → (ad, ekipten mi)
    for p in info["participants"]:
        k = key_of.get(p["puuid"])
        tag = SQUAD[k][2] if k else ("takım arkadaşı" if p["teamId"] == our_team else "rakip")
        who[p["participantId"]] = (f"{p['championName']} ({tag})", k is not None)

    out = []
    for fr in timeline["info"]["frames"]:
        for e in fr["events"]:
            t = f"{e['timestamp'] // 60000}:{e['timestamp'] // 1000 % 60:02d}"
            if e["type"] == "CHAMPION_KILL":
                ids = [e.get("killerId", 0), e["victimId"], *e.get("assistingParticipantIds", [])]
                if not any(who.get(i, ("", False))[1] for i in ids):
                    continue
                out.append({"t": t, "where": region(e["position"]["x"], e["position"]["y"], our_team),
                            "killer": who.get(e.get("killerId"), ("kule/minyon",))[0], "victim": who[e["victimId"]][0],
                            "assists": [who[i][0] for i in e.get("assistingParticipantIds", [])],
                            "shutdown_gold": e.get("shutdownBounty") or None})
            elif e["type"] == "ELITE_MONSTER_KILL":
                out.append({"t": t, "objective": e.get("monsterSubType") or e["monsterType"],
                            "taken_by": "biz" if e.get("killerTeamId") == our_team else "rakip"})
            elif e["type"] == "BUILDING_KILL" and e.get("buildingType") == "INHIBITOR_BUILDING":
                out.append({"t": t, "objective": "inhibitör", "lost_by": "biz" if e.get("teamId") == our_team else "rakip"})
    return out


def gold_curve(match, timeline, ids_by_key):
    """Takım altın farkı (biz eksi rakip): beş dakikada bir, en önde, en geride, son."""
    info = match["info"]
    team = {p["participantId"]: p["teamId"] for p in info["participants"]}
    our = next(p["teamId"] for p in info["participants"] if p["puuid"] in ids_by_key.values())
    diff = [sum(f["totalGold"] * (1 if team[int(pid)] == our else -1) for pid, f in fr["participantFrames"].items())
            for fr in timeline["info"]["frames"]]
    return {"dakika_basina": {i: d for i, d in enumerate(diff) if i and i % 5 == 0},
            "en_onde": {"dakika": diff.index(max(diff)), "fark": max(diff)},
            "en_geride": {"dakika": diff.index(min(diff)), "fark": min(diff)}, "son": diff[-1]}


def talk(match):
    """Kulak dökümlerinden bu maçın konuşmaları (oyun saatiyle; maç sonrası üç dakika dahil) ve Argon'un notları."""
    start, end = match["info"]["gameStartTimestamp"], match_end(match)
    lines, notes = [], []
    for f in sorted(KONUSMA.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if d["end"] < start or d["start"] > end + 180_000:
            continue
        notes.append(d["analiz"])
        for l in d["satirlar"]:
            if start <= l["ms"] <= end + 180_000:
                s = (l["ms"] - start) // 1000
                lines.append({"t": "maç sonu" if l["ms"] > end else f"{s // 60}:{s % 60:02d}", "kim": l["kim"], "soz": l["soz"]})
    return lines, notes


def match_end(match):
    info = match["info"]
    return info.get("gameEndTimestamp") or info["gameCreation"] + info["gameDuration"] * 1000


def load_history():
    return json.loads(HISTORY.read_text(encoding="utf-8")) if HISTORY.exists() else []


def direct(summary, history, match_id, end):
    """Akşamın hafızasını ve bu konuşmanın açısını özete ekler."""
    past = [h for h in history if h["end"] < end and h["id"] != match_id]
    tonight, t = [], end
    for h in reversed(past):  # geriye doğru, aralar 4 saati geçmeyene kadar
        if t - h["end"] > SESSION_GAP:
            break
        tonight.insert(0, h)
        t = h["end"]
    older = past[:len(past) - len(tonight)]
    recent = {h.get("aci") for h in past[-3:]}
    ratio = lambda p: (p["kills"] + p["assists"]) / max(p["deaths"], 1)
    # Hüküm kodda verilir, model karar vermez (4 Kas: 20/5/1 taşıyan Patrick'e "asistin az" dendi).
    # ponytail: eşikler elle, 4 Kas'ın beş maçına göre; yanlış hüküm görülürse buradan ayarla.
    win = any(p["win"] for p in summary["squad"].values())
    team = list(summary["squad"].values()) + [o for o in summary["others"] if o["team_win"] == win]
    team_dmg, team_kills = sum(p["damage"] for p in team) or 1, sum(p["kills"] for p in team) or 1
    aram = summary["queue"] == "ARAM"
    for p in summary["squad"].values():
        r = ratio(p)
        p["hasar_payi"] = round(100 * p["damage"] / team_dmg)  # takım hasarının yüzdesi
        p["kill_payi"] = round(100 * p["kills"] / team_kills)
        # 20 dakikalık eşdeğer ölüm: 41 dk'da 12 ölüm, 20 dk'da 6 ölümdür; ARAM'da ölüm bol, yarısı sayılır
        d20 = p["deaths"] * 20 / max(summary["minutes"], 15) / (2 if aram else 1)
        # maçı sırtlayan: kill ve hasarda pay büyük, ya da takım hasarının üçte birinden fazlası tek başına
        carry = (p["hasar_payi"] >= 28 and p["kill_payi"] >= 30 and r >= 1.5) or (p["hasar_payi"] >= 35 and r >= 1.2)
        p["performans"] = ("iyi" if carry or r >= 2.5 or (r >= 2 and d20 <= 6)
                           else "kötü" if r < 1 or (d20 >= 8 and r < 2) or (p["hasar_payi"] < 12 and r < 1.6) else "orta")
        p["talimat"] = TALIMAT[p["performans"]]
        if p["performans"] == "iyi":
            # Prompttaki "iyi oynayana eleştiri yok" kuralı tek başına tutmadı (4 Kas 6. maç: çizme "satıldı" yazıyordu,
            # yine de "çizmen yok" dendi). Eleştiri cephanesi veriden silinir: görmediği şeye laf sokamaz.
            for k in ("boots", "q_w_e_r_casts", "control_wards", "runes"):
                p.pop(k, None)
    anyone_bad = any(p["performans"] == "kötü" for p in summary["squad"].values())
    angles = [a for a in ANGLES if a not in recent and (anyone_bad or a not in NEGATIVE_ANGLES)]
    summary["oturum"] = {"mac_no": len(tonight) + 1, "onceki_sonuclar": ["G" if h["win"] else "M" for h in tonight],
                         "bu_aksam_okunanlar": [h["text"] for h in tonight],
                         "onceki_gunlerin_acilislari": [h["text"].split(".")[0] for h in older[-10:]],
                         "onceki_gunlerin_dersleri": [h["text"] for h in older[-6:]]}
    summary["yonlendirme"] = {"aci": random.choice(angles), "acilis": random.choice(OPENINGS)}
    if "Patrick" in summary["squad"]:
        p = summary["squad"]["Patrick"]
        # ponytail: "kötü" = skor oranı 1,5 altı ya da 8+ ölüm; "çok kötü" = oran 1 altı ya da 10+ ölüm. Eşikler elle.
        if (ratio(p) < 1.5 or p["deaths"] >= 8) and random.random() < PATRICK_LINE_CHANCE:
            used = {h.get("patrick_lafi") for h in tonight}
            summary["yonlendirme"]["patrick_lafi"] = random.choice([l for l in PATRICK_LINES if l not in used] or PATRICK_LINES)
    # Kötü ikili şakası: gerçekten iki kişi batırdıysa ve bu akşam yapılmadıysa, arada bir.
    bad = sorted((n for n, p in summary["squad"].items() if n != "Eda" and ratio(p) < 1 and p["deaths"] >= 6),
                 key=lambda n: ratio(summary["squad"][n]))
    if len(bad) >= 2 and not any(h.get("ikili") for h in tonight) and random.random() < DUO_CHANCE:
        used = {tuple(h["ikili"]) for h in older[-10:] if h.get("ikili")}
        summary["yonlendirme"]["kotu_ikili"] = {"oyuncular": bad[:2],
                                                "ad": random.choice(DUO_TOP) if random.random() < DUO_TOP_CHANCE
                                                else random.choice([d for d in DUO_NAMES[2:] if d not in used] or DUO_NAMES[2:])}
    return summary


def remember(history, match_id, end, summary, text):
    win = any(p["win"] for p in summary["squad"].values())
    y = summary["yonlendirme"]
    entry = {"id": match_id, "end": end, "win": win, "aci": y["aci"], "text": text,
             "patrick_lafi": y.get("patrick_lafi"), "ikili": y.get("kotu_ikili", {}).get("ad")}
    keep = sorted([h for h in history if h["id"] != match_id] + [entry], key=lambda h: h["end"])[-30:]
    HISTORY.write_text(json.dumps(keep, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- Argon + TTS ----------

async def argon_script(summary):
    return await argon((HERE / "script_prompt.md").read_text(encoding="utf-8").replace(
        "__MATCH__", json.dumps(summary, ensure_ascii=False, indent=1)), think=True)


async def argon(prompt, think=False):
    # CLI değil doğrudan Vertex API: sunucuda tarayıcı girişi gerekmiyor, kimlik google.auth.default() (VM servis hesabı).
    from google import genai
    from google.genai import types

    # Argon ara sıra birkaç dakika 429 veriyor (1 Kas): istemci 429/503'te kendi bekleyip dener, bekleme toplamı ~4 dk.
    client = genai.Client(vertexai=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location="global",
                          http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=6, initial_delay=15, max_delay=60)))
    r = await asyncio.wait_for(client.aio.models.generate_content(
        model=ARGON_MODEL, contents=prompt,
        # Varsayılanda Argon hiç düşünmüyor (5 Kas ölçümü: düşünme tokeni yok); maç metni yüksek düşünmeyle yazılır.
        config=types.GenerateContentConfig(system_instruction="Verilen görevi uygula. Yalnızca okunacak metni yaz.",
                                           thinking_config=types.ThinkingConfig(thinking_level="high") if think else None)), timeout=480)
    if not (r.text or "").strip():
        raise RuntimeError("Argon boş döndü")
    return r.text.strip()


def tts(text, path):
    # Cloud TTS 4000 baytta bölüyordu, ikinci parçada ses incelip değişiyordu (3 Kas, ~3:10).
    # Vertex generateContent tek istekte bütün metni okur: tek ses, ek yeri yok.
    from google import genai
    from google.genai import types

    client = genai.Client(vertexai=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location="global",
                          http_options=types.HttpOptions(timeout=300_000))
    r = client.models.generate_content(model=TTS_MODEL, contents=f"{TTS_STYLE} oku: {text}",
        config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=types.SpeechConfig(
            language_code="tr-TR", voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=TTS_VOICE)))))
    pcm = r.candidates[0].content.parts[0].inline_data.data  # audio/L16, 24 kHz, mono
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)


async def analysis_text(summary, name):
    txt = OUT / f"{name}.txt"
    cached = name != "test"  # bir adım patlayıp tekrar /bitti denenirse hazır metni/sesi kullan, Argon'a baştan yazdırma
    text = txt.read_text(encoding="utf-8") if cached and txt.exists() else await argon_script(summary)
    OUT.mkdir(exist_ok=True)
    txt.write_text(text, encoding="utf-8")
    return text


async def analysis_audio(summary, name):
    path = OUT / f"{name}.wav"
    text = await analysis_text(summary, name)
    if name != "test" and path.exists():
        return text, path
    for attempt in range(5):  # TTS bağlantısı ara sıra kopuyor (yanıtsız kesme, laptopta TLS INVALID_SESSION_ID)
        try:
            await asyncio.to_thread(tts, text, path)
            break
        except Exception:
            if attempt == 4:
                raise
            await asyncio.sleep(5)
    return text, path


# ---------- Discord ----------

def run_bot():
    import discord
    from discord import app_commands

    client = discord.Client(intents=discord.Intents.default())  # voice_states varsayılanda açık
    tree = app_commands.CommandTree(client)
    lock = asyncio.Lock()
    cache = {}

    @tree.command(name="bitti", description="Maç bitti: son maçı analiz edip ses kanalında oku")
    @app_commands.describe(mac="İsteğe bağlı: belirli bir maç kimliği (TR1_... ya da sadece numara)")
    async def bitti(interaction: discord.Interaction, mac: str | None = None):
        voice = interaction.user.voice
        if not voice or not voice.channel:
            return await interaction.response.send_message("Önce bir ses kanalına gir, oraya geleyim.", ephemeral=True)
        if lock.locked():
            return await interaction.response.send_message("Bir önceki maçı okuyorum, bitince tekrar dene.", ephemeral=True)
        await interaction.response.defer(thinking=True)
        async with lock:
            BUSY.touch()  # sunucu/guncelle.sh bu dosya varken botu yeniden başlatmaz
            try:
                if "puuids" not in cache:
                    cache["puuids"] = await asyncio.to_thread(puuids)
                    cache["items"] = await asyncio.to_thread(item_names)
                done = set(json.loads(STATE.read_text())) if STATE.exists() else set()

                # Maç verisi Riot'a 1-2 dk gecikmeyle düşebilir: 3 dk boyunca 20 sn arayla dene.
                mac = mac or os.environ.get("BITTI_MAC")  # tek seferlik: botu BITTI_MAC=<id> ile başlatınca ilk başarılı /bitti o maçı okur
                match_id = (mac if mac.upper().startswith("TR1_") else f"TR1_{mac}").upper() if mac else None
                for _ in range(0 if match_id else 10):
                    match_id = await asyncio.to_thread(latest_match_id, cache["puuids"], done)
                    if match_id:
                        break
                    await asyncio.sleep(20)
                if not match_id:
                    return await interaction.followup.send("Yeni maç Riot'a düşmedi. Bir dakika sonra tekrar /bitti yaz.")

                # Kimlik listeye maç verisinden önce düşebiliyor: veri gelene kadar 404 döner (27 Eki).
                for _ in range(10):
                    try:
                        match = await asyncio.to_thread(riot_get, f"/lol/match/v5/matches/{match_id}")
                        timeline = await asyncio.to_thread(riot_get, f"/lol/match/v5/matches/{match_id}/timeline")
                        break
                    except urllib.error.HTTPError as e:
                        if e.code != 404:
                            raise
                        await asyncio.sleep(20)
                else:
                    return await interaction.followup.send(f"{match_id} verisi Riot'ta hâlâ hazır değil. Bir dakika sonra tekrar /bitti yaz.")
                summary = summarize(match, cache["puuids"], cache["items"])
                if match["info"]["gameDuration"] < 300:  # remake: 2 dk'lık maçta "sıfır hasar" diye gömüyordu (4 Kas)
                    STATE.write_text(json.dumps(sorted(done | {match_id})))
                    return await interaction.followup.send(f"{match_id} remake, {summary['minutes']} dk sürmüş. Konuşacak bir şey yok, yeni maça basın.")
                summary["moments"] = moments(match, timeline, cache["puuids"])
                summary["altin_farki"] = gold_curve(match, timeline, cache["puuids"])
                for _ in range(40):  # /git sonrası döküm hâlâ işleniyorsa bekle (en fazla 2 dk)
                    if not list(KONUSMA.glob("*.isleniyor")):
                        break
                    await asyncio.sleep(3)
                summary["konusmalar"], summary["konusma_notlari"] = talk(match)
                history, end = load_history(), match_end(match)
                direct(summary, history, match_id, end)
                import atisma
                if os.environ.get("KLON_URL"):
                    asyncio.create_task(asyncio.to_thread(atisma.isit))  # konteyner uyansın, metin yazılırken ısınır
                text = await analysis_text(summary, match_id)
                (_, path), ek = await asyncio.gather(analysis_audio(summary, match_id), atisma.guvenli(summary, match_id, text))
                path = atisma.ekle(path, ek, match_id)

                vc = await voice.channel.connect()
                try:
                    finished = asyncio.Event()
                    vc.play(discord.FFmpegPCMAudio(str(path)), after=lambda e: client.loop.call_soon_threadsafe(finished.set))
                    await interaction.followup.send(f"🎙️ **{summary['queue']} · {summary['minutes']} dk**\n{text}"[:2000])
                    await finished.wait()
                    await asyncio.sleep(20)  # okuma bitince hemen kaçmasın, ekip tepki versin
                finally:
                    await vc.disconnect()
                STATE.write_text(json.dumps(sorted(done | {match_id})))
                remember(history, match_id, end, summary, text)
                os.environ.pop("BITTI_MAC", None)
            except urllib.error.HTTPError as e:
                if e.code != 401:
                    await interaction.followup.send(f"Bir şey patladı: `HTTPError: {str(e)[:300]}`")
                    raise
                # Geliştirici anahtarı 24 saatte ölüyor; traceback'e gerek yok.
                await interaction.followup.send("Riot API anahtarının süresi dolmuş. Latif yenisini girene kadar /bitti çalışmaz.")
            except Exception as e:
                await interaction.followup.send(f"Bir şey patladı: `{type(e).__name__}: {str(e)[:300]}`")
                raise
            finally:
                BUSY.unlink(missing_ok=True)

    @client.event
    async def on_ready():
        guild = discord.Object(int(os.environ["DISCORD_GUILD_ID"]))
        tree.copy_global_to(guild=guild)
        await tree.sync(guild=guild)  # sunucuya senkron: /bitti anında görünür
        print(f"Hazır: {client.user} · /bitti bekleniyor")

    client.run(os.environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    load_env()
    if len(sys.argv) == 3 and sys.argv[1] == "--test":
        summary = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
        t = time.time()
        text, path = asyncio.run(analysis_audio(summary, "test"))
        print(text, f"\n\n→ {path} ({time.time() - t:.0f} sn)")
    else:
        run_bot()
