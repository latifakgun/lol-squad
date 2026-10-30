"""Kulak'ın kayıtlarını yazıya döker, Argon'a not çıkartır → kulak/konusmalar/<başlangıç>.json. /bitti bunu okur.

Kulak /git'te çağırır:  python konusma.py <başlangıç ms> <bitiş ms>
Ses dosyaları silinmez: ses klonu ve konuşma tarzı için lazım. ponytail: VM diski dolarsa eski günler elle temizlenir.
"""
import asyncio
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import bot

KAYIT = bot.HERE.parent / "kulak" / "kayit"
STT_MODEL = "gemini-3.1-flash-lite"  # 28 Eki A/B: 3-flash sessiz klibe cümle uydurdu ve kesik cümleleri tamamladı; lite birebir, 7 kat hızlı, ~5 kat ucuz
BATCH = 60  # istek başına klip; Vertex satır içi veri sınırının altında kalsın

NOTES_PROMPT = """Aşağıda bir League of Legends oturumunda ekibin Discord'daki sesli konuşmalarının dökümü var. Her satır: saat, kim, ne dedi.
Maç sonu analizini yapacak sesli bot için kısa notlar çıkar:
- akılda kalan ya da komik sözler (birebir alıntı ve saatiyle),
- kim kime laf attı, kim sızlandı ya da bahane buldu, kim iddialı konuştu,
- tekrar eden laflar, ekibin genel havası.
En fazla on beş madde, düz metin, madde başına bir satır. Dökümde olmayan hiçbir şeyi uydurma. Yalnızca notları yaz.

DÖKÜM:
"""


def transcribe(files):
    from google import genai
    from google.genai import types

    client = genai.Client(vertexai=True, project=os.environ["GOOGLE_CLOUD_PROJECT"], location="global")

    def batch(part):
        contents = []
        for i, f in enumerate(part, 1):
            contents += [f"Klip {i} ({f.stem.rsplit('_', 1)[0]}):", types.Part.from_bytes(data=f.read_bytes(), mime_type="audio/wav")]
        contents.append('Her klibi Türkçe birebir yazıya dök. Konuşanlar League of Legends oynuyor; şampiyon adları ve oyun argosu geçer. '
                        'JSON dizi döndür: [{"klip": numara, "metin": "..."}]. Sadece nefes, klavye, gülme ya da gürültü olan klipleri listeye koyma. Uydurma.')
        for attempt in range(12):  # laptopta TLS bağlantısı ara sıra kopuyor; 26 Eki'de 30 sn'lik deneme yetmedi
            try:
                r = client.models.generate_content(model=STT_MODEL, contents=contents,
                                                   config=types.GenerateContentConfig(response_mime_type="application/json"))
                break
            except Exception as e:
                if attempt == 11:
                    raise
                print("yeniden deneniyor:", type(e).__name__, flush=True)
                time.sleep(15)
        clip = lambda it: part[int(re.search(r"\d+", str(it["klip"]))[0]) - 1]  # lite bazen 4 yerine "Klip 4" döndürüyor
        return [{"ms": int(clip(it).stem.rsplit("_", 1)[1]), "kim": clip(it).stem.rsplit("_", 1)[0],
                 "soz": it["metin"].strip()} for it in json.loads(r.text) if it.get("metin", "").strip()]

    # 38 dakikalık kayıt sırayla 7,5 dk sürdü; partileri aynı anda gönder.
    with ThreadPoolExecutor(4) as ex:
        lines = [l for part in ex.map(batch, [files[b:b + BATCH] for b in range(0, len(files), BATCH)]) for l in part]
    return sorted(lines, key=lambda l: l["ms"])


def main(start, end):
    bot.load_env()
    files = sorted((f for f in KAYIT.glob("20*/*.wav") if start <= int(f.stem.rsplit("_", 1)[1]) <= end),
                   key=lambda f: int(f.stem.rsplit("_", 1)[1]))
    if not files:
        print("kayıt yok")
        return
    bot.KONUSMA.mkdir(parents=True, exist_ok=True)
    flag = bot.KONUSMA / f"{start}.isleniyor"
    flag.touch()
    try:
        lines = transcribe(files)
        dump = "\n".join(f"{time.strftime('%H:%M:%S', time.localtime(l['ms'] / 1000))} {l['kim']}: {l['soz']}" for l in lines)
        notes = asyncio.run(bot.argon(NOTES_PROMPT + dump)) if lines else ""
        out = {"start": start, "end": end, "satirlar": lines, "analiz": notes}
        (bot.KONUSMA / f"{start}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(files)} klip → {len(lines)} satır")
    finally:
        flag.unlink(missing_ok=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
