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
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import wave

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
STATE = HERE / "state.json"

# key: (oyun adı, etiket, konuşmada söylenen ad)
SQUAD = {
    "l4cg": ("l4cg", "TR1", "Latif"),
    "minte": ("minte", "000", "Minte"),
    "swag": ("swagisback", "333", "Swag"),
    "patrick": ("Patrick Cem", "OMEN", "Patrick"),
}
RIOT = "https://europe.api.riotgames.com"
ARGON_MODEL = "gemini-4-argon"
TTS_MODEL, TTS_VOICE, TTS_RATE = "gemini-2.5-pro-tts", "Fenrir", 0.9
# Cloud TTS'te prompt ve text ayrı alan: ton talimatı asla seslendirilmez.
TTS_STYLE = ("Türk bir Twitch yayıncısı gibi oku: samimi, enerjik, bol küfürlü, arkadaşlarına acımadan laf sokuyor, "
             "espri yerlerinde gülerek vurguluyor. Acele etmeden, rahat bir tempoda konuş. Patrick Cem'in lafları "
             "geçtiğinde onu taklit eder gibi sızlanan, abartılı bir sesle söyle.")
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
            others.append({"name": p.get("riotIdGameName"), "team_win": p["win"], **{x: row(p)[x] for x in ("champ", "role", "kills", "deaths", "assists")}})
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


# ---------- Argon + TTS ----------

async def argon_script(summary):
    prompt = (HERE / "script_prompt.md").read_text(encoding="utf-8").replace(
        "__MATCH__", json.dumps(summary, ensure_ascii=False, indent=1))
    gemini = shutil.which("gemini") or sys.exit("gemini CLI bulunamadı")
    # --yolo yok: metin yazmak için araç gerekmiyor, Argon'un komut çalıştırmasına izin vermiyoruz.
    proc = await asyncio.create_subprocess_exec(
        gemini, "--model", ARGON_MODEL, "-p", "Stdin'deki görevi uygula. Yalnızca okunacak metni yaz.",
        stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=HERE)
    out, err = await asyncio.wait_for(proc.communicate(prompt.encode("utf-8")), timeout=240)
    text = out.decode("utf-8", "ignore").strip()
    if proc.returncode or not text:
        raise RuntimeError(f"Argon hata verdi: {err.decode('utf-8', 'ignore')[-400:]}")
    return text


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
    text = await argon_script(summary)
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.txt").write_text(text, encoding="utf-8")
    path = OUT / f"{name}.wav"
    try:
        await asyncio.to_thread(tts, text, path)
    except Exception:  # Gemini TTS ara sıra bağlantıyı yanıtsız kesiyor; bir kez daha dene
        await asyncio.sleep(3)
        await asyncio.to_thread(tts, text, path)
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
    async def bitti(interaction: discord.Interaction):
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
                match_id = None
                for _ in range(10):
                    match_id = await asyncio.to_thread(latest_match_id, cache["puuids"], done)
                    if match_id:
                        break
                    await asyncio.sleep(20)
                if not match_id:
                    return await interaction.followup.send("Yeni maç Riot'a düşmedi. Bir dakika sonra tekrar /bitti yaz.")

                match = await asyncio.to_thread(riot_get, f"/lol/match/v5/matches/{match_id}")
                timeline = await asyncio.to_thread(riot_get, f"/lol/match/v5/matches/{match_id}/timeline")
                summary = summarize(match, cache["puuids"], cache["items"])
                summary["moments"] = moments(match, timeline, cache["puuids"])
                text, path = await analysis_audio(summary, match_id)

                vc = await voice.channel.connect()
                try:
                    finished = asyncio.Event()
                    vc.play(discord.FFmpegPCMAudio(str(path)), after=lambda e: client.loop.call_soon_threadsafe(finished.set))
                    await interaction.followup.send(f"🎙️ **{summary['queue']} · {summary['minutes']} dk**\n{text}"[:2000])
                    await finished.wait()
                finally:
                    await vc.disconnect()
                STATE.write_text(json.dumps(sorted(done | {match_id})))
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
