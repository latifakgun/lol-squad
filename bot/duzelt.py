import re
# Kisaltma ve kufur tek bicime iner; Argon kuralina guvenilmez, TTS'ten once kod garanti eder.
KUFUR = [(r"\b(amk|amq|aq|amınakoyim|amınakoyayım|amına koyayım|amına koyim|amına koyim)\b", "amına koyim"),
         (r"\bmk\b", "amına koyim"), (r"\bsg\b", "siktir git"), (r"\byk\b", "yarrak kafalı"), (r"\bsikeyim\b", "sikim")]
KELIME = {"değil": "diil", "değildim": "diildim", "değilim": "diilim", "nasıl": "nası", "nereden": "nerden", "oradan": "ordan",
          "buradan": "burdan", "orada": "orda", "burada": "burda", "şurada": "şurda", "bir": "bi", "şey": "şey",
          "ne yapayım": "napayım", "ne yapıyorsun": "napıyon", "yapacak": "yapıcak", "gelecek": "gelcek", "gelecekler": "gelcekler",
          "Fizz'e": "Fize", "Fizz": "Fiz", "Veigar": "Veygar", "Illaoi": "İlaoy", "Tahm Kench": "Tam Kenç"}
def duzelt(t):
    for a, b in KUFUR:
        t = re.sub(a, b, t, flags=re.I)
    for a, b in sorted(KELIME.items(), key=lambda x: -len(x[0])):
        t = re.sub(rf"\b{a}\b", lambda m: b[0].upper() + b[1:] if m[0][0].isupper() else b, t, flags=re.I)
    t = re.sub(r"(?<=[a-zçğıöşü])yorlar\b", "yolar", t)
    t = re.sub(r"(?<=[a-zçğıöşü])yorduk\b", "yoduk", t)
    t = re.sub(r"(?<=[a-zçğıöşü])yorum\b", "yom", t)
    t = re.sub(r"(?<=[a-zçğıöşü])yorsun\b", "yon", t)
    t = re.sub(r"(?<=[a-zçğıöşü])yordum\b", "yodum", t)
    t = re.sub(r"(?<=[a-zçğıöşü])yor\b", "yo", t)
    return t
if __name__ == "__main__":
    for a, b in [("Ne yaptın amk", "Ne yaptın amına koyim"), ("AQ oğlum", "amına koyim oğlum"), ("bu amına koyayım ya", "bu amına koyim ya"),
                 ("geliyorum görmüyor musun", "geliyom görmüyo musun"), ("nereden çıktı", "nerden çıktı"), ("bir de ne yapayım", "bi de napayım"),
                 ("biliyorsun yani yiyordum", "biliyon yani yiyodum"), ("Bir de Fizz'e Veigar", "Bi de Fize Veygar"), ("mkm", "mkm"), ("yorum", "yorum")]:
        assert duzelt(a) == b, (a, duzelt(a), b)
    print("duzelt ok")
