"""Maç sonu atışması: Keriz (Fenrir) ile maçtaki oyuncuların klon sesleri karşılıklı konuşur, monoloğun arkasına eklenir.

Klonlar yalnız sahiplerinin onayıyla ve yalnız KLONLU'daki kişiler için. KLON_URL yoksa ya da servis patlarsa
/bitti eskisi gibi yalnız Fenrir'le devam eder: bu dosyadaki hiçbir hata okumayı engellememeli.
"""
import asyncio
import json
import os
import random
import re
import subprocess
import traceback
import urllib.request
import wave

import bot

KLONLU = {"Latif": "Latif", "Minte": "Minte", "Swag": "Swag", "Patrick": "Patrick", "Yılmaz": "Yilmaz"}
ARA_SN, GIRIS_SN, SINIR_SN = 0.35, 0.9, 270  # Latif: en kötü 5 dk beklenir; Fenrir paralel gidiyor. Seviye monologla aynı: -15 LUFS
KERIZ = "Keriz"


def gercek_satirlar(ad, n=40):
    """Tarz için kişinin gerçek sözleri. Dökümler yalnız VM'de: repoya girmez, Argon'a her seferinde taze örnek gider."""
    s = [l["soz"] for f in sorted(bot.KONUSMA.glob("*.json")) for l in json.loads(f.read_text(encoding="utf-8"))["satirlar"]
         if l["kim"] == ad and len(l["soz"].split()) >= 3]
    return random.sample(s, min(n, len(s)))


def coz(ham, oynayan):
    """Argon'un JSON'u: kod bloğu sarılı gelebilir, listede olmayan konuşmacı atılır."""
    d = json.loads(re.sub(r"^```(?:json)?|```$", "", ham.strip()).strip())
    out = [{"kim": x["kim"], "metin": x["metin"].strip()} for x in d if x.get("kim") in {KERIZ, *oynayan} and (x.get("metin") or "").strip()]
    if not any(x["kim"] != KERIZ for x in out):
        raise ValueError("atışmada oyuncu repliği yok")
    return out


async def yazdir(summary, text):
    oynayan = [a for a in summary["squad"] if a in KLONLU]
    if not oynayan:
        return []
    ozet = {k: summary.get(k) for k in ("queue", "minutes", "squad", "moments", "konusmalar", "konusma_notlari")}
    tarz = "\n\n".join(f"{a} gerçekten şöyle konuşuyor:\n" + "\n".join("- " + s for s in gercek_satirlar(a)) for a in oynayan)
    istem = (bot.HERE / "atisma_prompt.md").read_text(encoding="utf-8")
    for k, v in (("__OYUNCULAR__", ", ".join(oynayan)), ("__TARZ__", tarz), ("__MONOLOG__", text), ("__MATCH__", json.dumps(ozet, ensure_ascii=False))):
        istem = istem.replace(k, v)
    return coz(await bot.argon(istem), oynayan)


def istek(govde, sure):
    r = urllib.request.Request(os.environ["KLON_URL"], json.dumps({"anahtar": os.environ["KLON_ANAHTAR"], **govde}).encode(),
                               {"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=sure) as c:
        return c.read()


def isit():
    try:
        istek({"isit": True}, 180)
    except Exception:
        traceback.print_exc()  # asıl üretim yine dener


def klon(ad, metin, ton, yol):
    for deneme in range(2):
        try:
            yol.write_bytes(istek({"kim": KLONLU[ad], "metin": metin, "ton": ton}, 170))
            return
        except Exception:
            if deneme:
                raise


def seviye(yol):
    """Fenrir repliği klonlarla aynı seviyeye gelsin (klon_modal.py aynı süzgeçten geçiriyor)."""
    g = yol.with_suffix(".ham.wav")
    yol.replace(g)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(g), "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", str(yol)], check=True)
    g.unlink()


def kerizle(metin, yol):
    bot.tts(metin, yol)
    seviye(yol)


def birlestir(parcalar, yol):
    """Aynı biçimde (24 kHz, mono, 16 bit) wav'lar arka arkaya; parça araları sessiz."""
    pcm = b""
    for p, sus in parcalar:
        with wave.open(str(p)) as w:
            assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (24000, 1, 2), p
            pcm += w.readframes(w.getnframes()) + b"\0\0" * int(sus * 24000)
    with wave.open(str(yol), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)


async def uret(summary, name, text):
    yol, jn = bot.OUT / f"{name}_atisma.wav", bot.OUT / f"{name}_atisma.json"
    if yol.exists():
        return yol
    satirlar = json.loads(jn.read_text(encoding="utf-8")) if jn.exists() else await yazdir(summary, text)
    if not satirlar:
        return None
    jn.write_text(json.dumps(satirlar, ensure_ascii=False, indent=0), encoding="utf-8")
    parca = [bot.OUT / f"{name}_a{i:02d}.wav" for i in range(len(satirlar))]
    await asyncio.gather(*(asyncio.to_thread(kerizle, s["metin"], p) for s, p in zip(satirlar, parca) if s["kim"] == KERIZ))
    for i, (s, p) in enumerate(zip(satirlar, parca)):  # tek GPU: paralel istek yine sıraya girer
        if s["kim"] != KERIZ:
            await asyncio.to_thread(klon, s["kim"], s["metin"], 1000 + i, p)
    birlestir([(p, ARA_SN) for p in parca], yol)
    for p in parca:
        p.unlink()
    return yol


async def guvenli(summary, name, text):
    """Hata ya da süre aşımı okumayı durdurmaz: atışma yoksa Fenrir tek başına okur."""
    if not os.environ.get("KLON_URL"):
        return None
    try:
        return await asyncio.wait_for(uret(summary, name, text), SINIR_SN)
    except Exception:
        traceback.print_exc()
        return None


def ekle(ana, ek, name):
    if not ek:
        return ana
    yol = bot.OUT / f"{name}_tam.wav"
    birlestir([(ana, GIRIS_SN), (ek, 0)], yol)
    return yol


if __name__ == "__main__":
    a = [{"kim": "Keriz", "metin": " Ne diyon "}, {"kim": "Swag", "metin": "Ya bak"}, {"kim": "Ateck", "metin": "x"}, {"kim": "Minte", "metin": ""}]
    assert coz(json.dumps(a), ["Swag"]) == [{"kim": "Keriz", "metin": "Ne diyon"}, {"kim": "Swag", "metin": "Ya bak"}]
    assert coz("```json\n" + json.dumps(a) + "\n```", ["Swag"])[1]["kim"] == "Swag"
    try:
        coz(json.dumps(a[:1]), ["Swag"]); raise SystemExit("yalnız Keriz'li atışma geçmemeli")
    except ValueError:
        pass
    import pathlib, tempfile
    with tempfile.TemporaryDirectory() as d:
        p, q = pathlib.Path(d) / "a.wav", pathlib.Path(d) / "b.wav"
        with wave.open(str(p), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(b"\1\0" * 24000)
        birlestir([(p, 0.5), (p, 0)], q)
        with wave.open(str(q)) as w:
            assert w.getnframes() == 60000, w.getnframes()
    print("atisma ok")
