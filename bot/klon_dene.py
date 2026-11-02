"""klon_modal üretimini deploy etmeden T4'te dener: profil, LoRA, ayar.json ve son işlem servisteki kodla aynı.
Çalıştır: modal run klon_dene.py --isler isler.json --klasor cikti   (isler.json: [["Swag", "metin"], ...])"""
import json
import pathlib

import modal

import klon_modal as k

app = modal.App("lol-klon-dene")


@app.function(image=k.image.add_local_python_source("klon_modal"), gpu="T4", volumes={"/veri": k.hacim}, timeout=900)  # imajdaki kopya eski kalıyor
def dene(isler):
    k.fren_yama()
    import torch
    m = k.Motor()
    ana = dict(m.m.t3.tfmr.named_parameters())
    ilk = next(iter(m.lora.values()))
    ad = next(iter(ilk)) + ".weight"
    temiz = ana[ad].data.clone()
    wavlar = []
    for kim, metin in isler:
        y, a = m.sentez(kim, metin, 11)
        print(kim, round(len(y) / m.m.sr, 2), "sn", "lora" if kim in m.lora else "taban", flush=True)
        wavlar.append(m.wav(y, a))
    m.lora_tak(None)
    assert torch.allclose(ana[ad].data, temiz, atol=1e-4), "LoRA çıkarılınca ağırlık geri dönmedi"
    return wavlar


@app.local_entrypoint()
def main(isler="isler.json", klasor="klon_dene"):
    I = json.load(open(isler, encoding="utf8"))
    d = pathlib.Path(klasor)
    d.mkdir(exist_ok=True)
    for i, ((kim, _), w) in enumerate(zip(I, dene.remote(I))):
        (d / f"{kim}_{i:02d}.wav").write_bytes(w)
    print(d, len(I))
