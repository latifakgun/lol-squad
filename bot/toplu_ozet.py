"""Akşamın toplu özeti: birkaç maçı tek konuşmada, seçili oyuncular için (27 Eki'de Latif çok beğendi).

Sunucuda:  .venv/bin/python toplu_ozet.py "Latif,Patrick,Görkem,Swag" TR1_... TR1_... TR1_...
Ses son maçın önbelleğine yazılır (eskisi <id>.mac.* olarak saklanır). Sonra lolbot'u
BITTI_MAC=<son maç> ile yeniden başlat (README), bir sonraki /bitti bunu okur.
"""
import sys
import asyncio, json, re, shutil, bot
bot.load_env()
WHO = set(sys.argv[1].split(","))
MATCHES = sys.argv[2:]
ids, items = bot.puuids(), bot.item_names()
data = []
for m in MATCHES:
    match = bot.riot_get(f"/lol/match/v5/matches/{m}"); tl = bot.riot_get(f"/lol/match/v5/matches/{m}/timeline")
    s = bot.summarize(match, ids, items)
    mom = [x for x in bot.moments(match, tl, ids) if any(w in json.dumps(x, ensure_ascii=False) for w in WHO)]
    talk, notes = bot.talk(match)
    data.append({"mac": len(data) + 1, "queue": s["queue"], "dakika": s["minutes"],
                 "sonuc": "G" if any(p["win"] for p in s["squad"].values()) else "M",
                 "squad": {k: v for k, v in s["squad"].items() if k in WHO}, "moments": mom,
                 "konusmalar": [t for t in (talk or []) if t.get("kim") in WHO], "konusma_notlari": notes})
P = (bot.HERE / "script_prompt.md").read_text(encoding="utf-8")
blocks = {b.split("\n", 1)[0].split(" (")[0].strip(): b for b in P.split("\n\n")}
def sec(h):
    return next(b for k, b in blocks.items() if k.startswith(h))
prompt = f"""Sen Argon'sun, bu ekibin beşinci adamısın. Bu akşam {len(MATCHES)} maç oynandı ve hepsini onlarla izledin. Şimdi Discord ses kanalında AKŞAMIN TOPLU ÖZETİNİ yapacaksın. Metni bir TTS modeli okuyacak.

KAPSAM
- Yalnızca şu kişiler: {', '.join(sorted(WHO))}. Başka hiçbir oyuncudan bahsetme.
- Maç maç anlatma; her oyuncunun akşam boyunca gidişatını anlat: hangi maçta parladı, hangisinde battı, akşam boyunca tekrar eden hatası ne, toparladı mı.

ÇIKTI
- Yalnızca okunacak metni yaz. 650 ile 800 kelime arası (okununca dört beş dakika).
- İlk cümle ekibe seslenir: bu akşam kaç maç, kaç galibiyet kaç mağlubiyet.
- Sonra her oyuncuya ayrı bölüm. Her bölümde: akşamın en iyi anı, en kötü anı, tekrar eden hata. Yeni oyuncular için tekrar eden hatadan çıkan somut ders ve bir dahaki akşam tam olarak ne yapacağı.
- Konuşma kayıtlarından toplam iki dört sözü birebir alıntıla, kimin söylediğini adıyla söyle, maçta olanla karşılaştır.
- Kapanış: her birine bir sonraki akşam için tek cümlelik ödev.
- Bütün metinde dakika sayısı en fazla üç kere geçsin.

{sec("KİMİ GÖMECEKSİN")}

{sec("YENİ OYUNCULARA ÖĞRET")}

{sec("TON")}

{sec("TTS İÇİN YAZIM KURALLARI")}

{sec("EKİP")}

UYDURMA YOK: verinin söylemediği anı söyleme.

AKŞAMIN VERİSİ (JSON, maçlar sırayla)
{json.dumps(data, ensure_ascii=False, indent=1)}
"""
open("/tmp/toplu_prompt.txt", "w").write(prompt)
name = MATCHES[-1]
for ext in ("txt", "wav"):
    f = bot.OUT / f"{name}.{ext}"
    if f.exists():
        shutil.move(f, bot.OUT / f"{name}.mac.{ext}")
text = asyncio.run(bot.argon(prompt))
(bot.OUT / f"{name}.txt").write_text(text, encoding="utf-8")
bot.tts(text, bot.OUT / f"{name}.wav")
print(len(text.split()), "kelime")
print(text)
