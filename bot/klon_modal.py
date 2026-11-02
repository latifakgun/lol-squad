"""Klon sesi üretimi: Modal'da T4 + Chatterbox, /bitti'deki atışma için. VM yalnız HTTP ile çağırır.

Profil ve LoRA ağırlıkları `lol-klon` Volume'unda durur, repoya girmez:
  /veri/profil/<Kişi>.pt   /veri/lora/<Kişi>.pt   /veri/ayar.json
ayar.json kişi başına: {"tempo": 1.0, "perde": 1.0, "fren": "gevsek", "uzat": false, "hece": 5.0}. Yeniden deploy gerektirmez.

Deploy:  modal deploy klon_modal.py      Anahtar: modal secret create lol-klon-anahtar KLON_ANAHTAR=...
"""
import hmac
import json
import os
import pathlib
import subprocess
import tempfile

import modal

app = modal.App("lol-klon")
hacim = modal.Volume.from_name("lol-klon", create_if_missing=True)
VERI = pathlib.Path("/veri")
EX, CFG, TOP_DB = 0.8, 0.5, 38
FRENLER = {"siki": ({"kuyruk": 5, "tekrar": True}, 2.0), "gevsek": ({"kuyruk": 25, "tekrar": False}, 1.2)}  # kuyruk: son jetonlar için izin (25 = 1 sn)


def kur():
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    ChatterboxMultilingualTTS.from_pretrained(device="cpu")  # ağırlıklar imaja girsin, soğuk başlangıç kısalsın


def fren_yama():
    """Hizalama denetçisi son jetonları 200 ms'de ve üst üste iki aynı jetonda kesiyor. Eşiği ayarlanabilir yap: Yılmaz gevsek kullanıyor, LoRA'lılarda fren devreye girmiyor (2 Kas).
    Konteyner açılışında, chatterbox yüklenmeden çalışır: imaj aşamasındaki yama çalışma anına ulaşmadı (2 Kas)."""
    import importlib.metadata
    f = pathlib.Path(importlib.metadata.distribution("chatterbox-tts").locate_file("chatterbox/models/t3/inference/alignment_stream_analyzer.py"))
    s = f.read_text(encoding="utf8")
    if s.startswith("FREN ="):
        return
    for eski, yeni in [("A[self.completed_at:, -3:].sum(dim=0).max() >= 5)", 'A[self.completed_at:, -3:].sum(dim=0).max() >= FREN["kuyruk"])'),
                       ("if long_tail or alignment_repetition or token_repetition:", 'if long_tail or alignment_repetition or (token_repetition and FREN["tekrar"]):')]:
        assert eski in s, eski
        s = s.replace(eski, yeni)
    f.write_text('FREN = {"kuyruk": 5, "tekrar": True}\n' + s, encoding="utf8")
    for c in f.parent.glob("__pycache__/alignment_stream_analyzer*"):
        c.unlink()


image = (modal.Image.debian_slim(python_version="3.11").apt_install("ffmpeg")
         .pip_install("numpy==1.26.4", "cython", "setuptools<70", "wheel")
         .pip_install("chatterbox-tts", "soundfile", "fastapi[standard]")
         .run_function(kur)
         .add_local_python_source("okunus", "duzelt")
         .add_local_file("okunus.json", "/root/okunus.json"))


def uygun(sn, hedef):
    """Süre koruması: model ara sıra sona anlamsız ses ekliyor ya da erken kesiyor."""
    return 0.4 * hedef <= sn <= 1.6 * hedef + 1


class Motor:
    """Model, profiller ve LoRA'lar bellekte. Hem servis hem klon_dene bunu çalıştırır."""

    def __init__(self):
        import torch
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS, Conditionals
        self.m = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
        self.kosul = {p.stem: Conditionals.load(p).to("cuda") for p in (VERI / "profil").glob("*.pt")}
        self.lora = {p.stem: torch.load(p, map_location="cuda")["agirlik"] for p in (VERI / "lora").glob("*.pt")}
        self.ayar = json.loads((VERI / "ayar.json").read_text(encoding="utf8"))
        self.takili = None

    def lora_tak(self, kim):
        """Ağırlıklara ekler, kişi değişince çıkarır: katman sarmaya gerek kalmaz."""
        if kim == self.takili:
            return
        mod = dict(self.m.t3.tfmr.named_modules())
        for k, isaret in ((self.takili, -1), (kim, 1)):
            for ad, (A, B) in self.lora.get(k, {}).items():
                mod[ad].weight.data += isaret * (B.float() @ A.float())
        self.takili = kim

    def sentez(self, kim, metin, ton):
        import librosa
        import torch
        from chatterbox.models.t3.inference import alignment_stream_analyzer as asa
        from okunus import okut
        a = self.ayar.get(kim, {})
        fren, rp = FRENLER[a.get("fren", "siki")]
        asa.FREN.update(fren)
        self.lora_tak(kim)
        t = okut(metin, uzat=a.get("uzat", True))
        hedef = sum(c in "aeıioöuüAEIİOÖUÜ" for c in t) / a.get("hece", 5.0)
        en_iyi = None
        for d in range(3):
            torch.manual_seed(ton + d)
            self.m.conds = self.kosul[kim]
            y = self.m.generate(t, language_id="tr", exaggeration=EX, cfg_weight=CFG, repetition_penalty=rp).squeeze().cpu().numpy()
            y = librosa.effects.trim(y, top_db=TOP_DB)[0]
            sn = len(y) / self.m.sr
            if en_iyi is None or abs(sn - hedef) < abs(len(en_iyi) / self.m.sr - hedef):
                en_iyi = y
            if uygun(sn, hedef):
                break
        return en_iyi, a

    def wav(self, y, a):
        import soundfile as sf
        with tempfile.TemporaryDirectory() as d:
            g, c = f"{d}/g.wav", f"{d}/c.wav"
            sf.write(g, y, self.m.sr)
            tempo, perde = a.get("tempo", 1.0), a.get("perde", 1.0)
            sr = self.m.sr
            filtre = f"asetrate={sr * perde:.0f},aresample={sr},atempo={tempo / perde:.3f},loudnorm=I=-15:TP=-1.5:LRA=11"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", g, "-af", filtre, "-ar", str(sr), "-ac", "1", "-c:a", "pcm_s16le", c], check=True)
            return pathlib.Path(c).read_bytes()


@app.cls(image=image, gpu="T4", volumes={"/veri": hacim}, secrets=[modal.Secret.from_name("lol-klon-anahtar")],
         scaledown_window=120, timeout=280, max_containers=1)
class Klon:
    @modal.enter()
    def yukle(self):
        fren_yama()
        self.motor = Motor()

    @modal.fastapi_endpoint(method="POST")
    def uret(self, istek: dict):
        from fastapi import HTTPException, Response
        if not hmac.compare_digest(str(istek.get("anahtar")), os.environ["KLON_ANAHTAR"]):
            raise HTTPException(401)
        if istek.get("isit"):  # /bitti başında konteyneri uyandırır
            return {"hazir": sorted(self.motor.kosul)}
        kim = istek["kim"]
        if kim not in self.motor.kosul:
            raise HTTPException(404, f"profil yok: {kim}")
        y, a = self.motor.sentez(kim, istek["metin"], int(istek.get("ton", 1)))
        return Response(self.motor.wav(y, a), media_type="audio/wav")
