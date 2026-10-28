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
}
KONUSMA = HERE.parent / "kulak" / "konusmalar"  # kulak'ın /git sonrası yazdığı konuşma dökümleri (konusma.py)
RIOT = "https://europe.api.riotgames.com"
ARGON_MODEL = "gemini-4-argon"
TTS_MODEL, TTS_VOICE, TTS_RATE = "gemini-2.5-pro-tts", "Fenrir", 0.9
# Cloud TTS'te prompt ve text ayrı alan: ton talimatı asla seslendirilmez.
# Uzun, emir kipli talimat metin uzayınca sesli okundu (26 Eki); kısa bir ses tarifi olarak kalsın.
TTS_STYLE = "Samimi, enerjik, gülerek laf sokan bir Türk Twitch yayıncısı sesiyle"
# Tekrarı model tarafında "tekrar etme" demek kırmıyor: açı, açılış ve Patrick lafları burada rastgele seçilir.
ANGLES = [
    "maçı belirleyen tek an: o anı kim, nasıl yaşattı",
    "en iyi oynayan: maçı onun gözünden anlat, diğerleri ona nasıl yük oldu",
    "en kötü oynayan: maçı nasıl kendi eliyle sattı ya da az kalsın satıyordu",
    "maçın en saçma istatistiği: o sayıdan yola çıkıp herkese bağla",
    "koridor savaşları: ekipten herkes kendi rakibine karşı nasıl gitti",
    "şampiyon ve eşya seçimleri: kim neyi aldı, mantıklı mıydı",
    "altın farkı hikâyesi: maç nerede kırıldı, nasıl döndü ya da elden kaçtı",
    "takım oyunu: birlikte mi oynandı, herkes kendi kafasına mı",
]
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
    q = urllib.parse.quote
    return {k: riot_get(f"/riot/account/v1/accounts/by-riot-id/{q(n)}/{q(t)}")["puuid"] for k, (n, t, _) in SQUAD.items()}


def item_names():
    ver = get_json("https://ddragon.leagueoflegends.com/api/versions.json")[0]
    data = get_json(f"https://ddragon.leagueoflegends.com/cdn/{ver}/data/tr_TR/item.json")
    return {int(i): v["name"] for i, v in data["data"].items()}


def latest_match_id(ids_by_key, done):
    """Ekipten herhangi birinin en yeni, henüz analiz edilmemiş maçı."""
    ids = {riot_get(f"/lol/match/v5/matches/by-puuid/{p}/ids?count=1")[0] for p in ids_by_key.values()}
    fresh = sorted((i for i in ids if i not in done), key=lambda i: int(i.split("_")[1]))
    return fresh[-1] if fresh else None


def summarize(match, ids_by_key, items):
    info = match["info"]
    key_of = {p: k for k, p in ids_by_key.items()}
    mins = info["gameDuration"] / 60

    def row(p):
        cs = p["totalMinionsKilled"] + p["neutralMinionsKilled"]
        return {
            "champ": p["championName"], "role": p.get("teamPosition") or "-", "win": p["win"],
            "kills": p["kills"], "deaths": p["deaths"], "assists": p["assists"],
            "cs": cs, "cs_per_min": round(cs / mins, 1), "gold": p["goldEarned"],
            "damage": p["totalDamageDealtToChampions"], "vision": p["visionScore"],
            "kill_participation": round(p.get("challenges", {}).get("killParticipation", 0) * 100),
            "items": [items.get(p[f"item{i}"], "") for i in range(6) if p[f"item{i}"]],
            "level": p.get("summonerLevel"),
        }

    squad, others = {}, []
    for p in info["participants"]:
        k = key_of.get(p["puuid"])
        if k:
            ch = p.get("challenges", {})
            squad[SQUAD[k][2]] = {**row(p), "skillshots_hit": ch.get("skillshotsHit"), "skillshots_dodged": ch.get("skillshotsDodged"),
                                  "q_w_e_r_casts": [p.get(f"spell{i}Casts") for i in range(1, 5)],
                                  "solo_kills": ch.get("soloKills"), "control_wards": ch.get("controlWardsPlaced")}
        else:
            others.append({"name": p.get("riotIdGameName"), "team_win": p["win"], **row(p)})
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
    summary["oturum"] = {"mac_no": len(tonight) + 1, "onceki_sonuclar": ["G" if h["win"] else "M" for h in tonight],
                         "bu_aksam_okunanlar": [h["text"] for h in tonight],
                         "onceki_gunlerin_acilislari": [h["text"].split(".")[0] for h in older[-10:]]}
    summary["yonlendirme"] = {"aci": random.choice([a for a in ANGLES if a not in recent]), "acilis": random.choice(OPENINGS)}
    if "Patrick" in summary["squad"]:
        summary["yonlendirme"]["patrick_laflari"] = random.sample(PATRICK_LINES, 2)
        p = summary["squad"]["Patrick"]
        # ponytail: "çok kötü" = skor oranı 1'in altı ya da 10+ ölüm; fazla/az tetiklerse eşiği buradan ayarla.
        if (p["kills"] + p["assists"]) / max(p["deaths"], 1) < 1 or p["deaths"] >= 10:
            summary["yonlendirme"]["patrick_can_gelsin"] = True
    return summary


def remember(history, match_id, end, summary, text):
    win = any(p["win"] for p in summary["squad"].values())
    entry = {"id": match_id, "end": end, "win": win, "aci": summary["yonlendirme"]["aci"], "text": text}
    keep = sorted([h for h in history if h["id"] != match_id] + [entry], key=lambda h: h["end"])[-30:]
    HISTORY.write_text(json.dumps(keep, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------- Argon + TTS ----------

async def argon_script(summary):
    return await argon((HERE / "script_prompt.md").read_text(encoding="utf-8").replace(
        "__MATCH__", json.dumps(summary, ensure_ascii=False, indent=1)))


async def argon(prompt):
    # CLI değil doğrudan Vertex API: sunucuda tarayıcı girişi gerekmiyor, kimlik google.auth.default() (VM servis hesabı).
    from google import genai
    from google.genai import types

    client = genai.Client(vertexai=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location="global")
    r = await asyncio.wait_for(client.aio.models.generate_content(
        model=ARGON_MODEL, contents=prompt,
        config=types.GenerateContentConfig(system_instruction="Verilen görevi uygula. Yalnızca okunacak metni yaz.")), timeout=240)
    if not (r.text or "").strip():
        raise RuntimeError("Argon boş döndü")
    return r.text.strip()


def chunks(text, limit=3500):
    """Cloud TTS metin alanı 4000 baytla sınırlı: cümle sınırından böl."""
    out, cur = [], ""
    for s in text.replace("! ", "!\n").replace("? ", "?\n").replace(". ", ".\n").splitlines():
        if cur and len((cur + " " + s).encode()) > limit:
            out.append(cur); cur = s
        else:
            cur = f"{cur} {s}".strip()
    return out + [cur] if cur else out


def tts(text, path):
    import base64, io
    import google.auth
    from google.auth.transport.requests import AuthorizedSession

    project = os.environ["GOOGLE_CLOUD_PROJECT"]
    cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"], quota_project_id=project)
    session = AuthorizedSession(cred)
    pcm = b""
    for part in chunks(text):
        r = session.post("https://texttospeech.googleapis.com/v1/text:synthesize", timeout=180, json={
            "input": {"prompt": TTS_STYLE, "text": part},
            "voice": {"languageCode": "tr-TR", "name": TTS_VOICE, "modelName": TTS_MODEL},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000, "speakingRate": TTS_RATE}})
        r.raise_for_status()
        with wave.open(io.BytesIO(base64.b64decode(r.json()["audioContent"]))) as w:
            pcm += w.readframes(w.getnframes())
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)


async def analysis_audio(summary, name):
    path, txt = OUT / f"{name}.wav", OUT / f"{name}.txt"
    cached = name != "test"  # bir adım patlayıp tekrar /bitti denenirse hazır metni/sesi kullan, Argon'a baştan yazdırma
    if cached and path.exists():
        return txt.read_text(encoding="utf-8"), path
    text = txt.read_text(encoding="utf-8") if cached and txt.exists() else await argon_script(summary)
    OUT.mkdir(exist_ok=True)
    txt.write_text(text, encoding="utf-8")
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
                summary["moments"] = moments(match, timeline, cache["puuids"])
                summary["altin_farki"] = gold_curve(match, timeline, cache["puuids"])
                for _ in range(40):  # /git sonrası döküm hâlâ işleniyorsa bekle (en fazla 2 dk)
                    if not list(KONUSMA.glob("*.isleniyor")):
                        break
                    await asyncio.sleep(3)
                summary["konusmalar"], summary["konusma_notlari"] = talk(match)
                history, end = load_history(), match_end(match)
                direct(summary, history, match_id, end)
                text, path = await analysis_audio(summary, match_id)

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
