"""Klon seslendirmesinden önceki son durak: sözlük + konuşma dili. Fenrir ve Discord metni bundan geçmez."""
import json
import pathlib
import re

from duzelt import duzelt

SOZLUK = json.loads((pathlib.Path(__file__).parent / "okunus.json").read_text(encoding="utf-8"))
HARF = {k for k in SOZLUK if len(k) <= 2}  # Q, W, R, Vi: küçük harfliyle (ve, vi, ar) karışmasın diye birebir eşleşir
KALIP = re.compile(r"\b(" + "|".join(sorted(map(re.escape, SOZLUK), key=len, reverse=True)) + r")\b(?:'([a-zçğıöşü]+))?", re.I)
_kucuk = {k.lower(): k for k in SOZLUK if k not in HARF}


def _cevir(m):
    k = m[1] if m[1] in HARF else _kucuk.get(m[1].lower())
    if k is None:
        return m[0]
    v = SOZLUK[k]
    if m[1][0].isupper():
        v = v[0].upper() + v[1:]
    return v + (m[2] or "")


def okut(t, uzat=True):
    t = re.sub(r"(?<=\w)'(?=\w)", "", duzelt(KALIP.sub(_cevir, t)))
    return re.sub(r"\b([Yy])a\b", r"\1aaaa", t) if uzat else t  # Latif: "ya" kısa söylenmez. ponytail: 3 denemenin 1-2'sinde tutuyor, kalıcı çözüm LoRA


def kalan(t):
    """Denetleyici: sözlükten sonra hâlâ okunamayacak kelimeler. Loglanır, sözlüğe eklenir."""
    return [w for w in re.findall(r"[^\W\d_]+", t) if re.search(r"[qwxQWX]", w)]


if __name__ == "__main__":
    for a, b in [("Vayne'e bak", "Veyne bak"), ("vayne geldi", "Veyn geldi"), ("Warwick'i kestim", "Vorviki kestim"), ("Kha'Zix geldi", "Kazik geldi"),
                 ("Q attı", "Kü attı"), ("Adam Vi aldı", "Adam Vay aldı"), ("ve vi", "ve vi"), ("Gank yedik amk", "Genk yedik amına koyim"),
                 ("R'si yok", "Arsi yok"), ("çar'ın", "çarın"), ("Ya hadi ya, yarma ya.", "Yaaaa hadi yaaaa, yarma yaaaa."), ("yani yarma", "yani yarma"), ("Lee Sin", "Li Sin"), ("Nereden geldi Lux", "Nerden geldi Laks")]:
        assert okut(a) == b, (a, okut(a), b)
    assert okut("Ya hadi ya", uzat=False) == "Ya hadi ya"
    assert kalan(okut("Bilinmez Xyz'e gitti")) == ["Xyze"]
    assert not [k for k, v in SOZLUK.items() if kalan(v)], [k for k, v in SOZLUK.items() if kalan(v)]
    print("okunus ok", len(SOZLUK))
