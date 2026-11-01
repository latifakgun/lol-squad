"""klon_modal imajını ve üretimi deploy etmeden T4'te dener. Çalıştır: modal run klon_dene.py --kim Swag --metin "..." """
import pathlib

import modal

import klon_modal as k

app = modal.App("lol-klon-dene")


@app.function(image=k.image, gpu="T4", volumes={"/veri": k.hacim}, timeout=280)
def dene(kim, metin, fren, uzat):
    import io
    import librosa
    import soundfile as sf
    import torch
    from chatterbox.models.t3.inference import alignment_stream_analyzer as asa
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS, Conditionals
    from okunus import okut
    m = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
    f, rp = k.FRENLER[fren]
    asa.FREN.update(f)
    m.conds = Conditionals.load(k.VERI / "profil" / f"{kim}.pt").to("cuda")
    torch.manual_seed(11)
    y = m.generate(okut(metin, uzat=uzat), language_id="tr", exaggeration=k.EX, cfg_weight=k.CFG, repetition_penalty=rp).squeeze().cpu().numpy()
    y = librosa.effects.trim(y, top_db=k.TOP_DB)[0]
    b = io.BytesIO()
    sf.write(b, y, m.sr, format="WAV")
    return b.getvalue()


@app.local_entrypoint()
def main(kim="Swag", metin="Ya hadi ya yarma ya.", fren="gevsek", uzat=False, cikti="klon_dene.wav"):
    w = dene.remote(kim, metin, fren, uzat)
    pathlib.Path(cikti).write_bytes(w)
    print(cikti, len(w))
