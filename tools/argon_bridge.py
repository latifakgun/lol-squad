"""argon-lol:// köprüsü: siteden gelen isteği tek bir Vertex API çağrısıyla Argon'a verir, sonra commit + push yapar.

CLI ajanı (gemini --yolo) kullanılmaz: her adımda bütün bağlamı yeniden gönderip milyonlarca token yakıyordu (27 Eki).

Kayıt: tools/register_protocol.ps1. Elle: python tools/argon_bridge.py "argon-lol://update?target=all"
URI: argon-lol://update?target=<all|l4cg|minte|swag|patrick|premade>&urls=<virgüllü>&raw=<kısa talimat>&clip=1
clip=1 ise ham metin panodan okunur (URI uzunluk sınırı yüzünden); kısa talimat raw= ile de gelebilir.
"""
import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data" / "squadData.js"
TARGETS = {"all", "l4cg", "minte", "swag", "patrick", "premade"}
MODEL = "gemini-4-argon"


def parse(uri):
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(uri).query)
    target = q.get("target", ["all"])[0]
    if target not in TARGETS:
        sys.exit(f"Bilinmeyen hedef: {target}")
    urls = [u.strip() for u in q.get("urls", [""])[0].replace("\n", ",").split(",")]
    urls = [u for u in urls if u.startswith(("https://", "http://"))]
    raw = q.get("raw", [""])[0]
    if q.get("clip"):
        import tkinter
        tk = tkinter.Tk()
        tk.withdraw()
        try:
            raw = tk.clipboard_get()
        except tkinter.TclError:
            pass
        tk.destroy()
    return target, urls, raw


def build_prompt(target, urls, raw):
    text = (ROOT / "tools" / "argon_prompt.md").read_text(encoding="utf-8")
    return (text.replace("__TARGET__", target)
                .replace("__URLS__", ", ".join(urls) or "(yok, Riot ID'lerden LeagueOfGraphs linkini kendin kur)")
                .replace("__DATE__", datetime.date.today().isoformat())
                .replace("__RAW__", raw or "(yok)")
                .replace("__CURRENT__", DATA.read_text(encoding="utf-8")))


def argon(prompt):
    # Kimlik: gcloud ADC (bot/.env'deki proje). URL/arama araçları sunucu tarafında, döngü yok.
    env = dict(l.split("=", 1) for l in (ROOT / "bot" / ".env").read_text(encoding="utf-8").splitlines() if "=" in l)
    gcloud = shutil.which("gcloud") or sys.exit("gcloud bulunamadı.")
    token = subprocess.run([gcloud, "auth", "application-default", "print-access-token"],
                           capture_output=True, text=True, check=True).stdout.strip()
    url = (f"https://aiplatform.googleapis.com/v1/projects/{env['GOOGLE_CLOUD_PROJECT'].strip()}"
           f"/locations/global/publishers/google/models/{MODEL}:generateContent")
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "tools": [{"urlContext": {}}, {"googleSearch": {}}],
            "generationConfig": {"maxOutputTokens": 65536}}
    req = urllib.request.Request(url, json.dumps(body).encode(), {
        "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
    text = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
    blocks = re.findall(r"```(?:js|javascript)?\n(.*?)```", text, re.S)
    return (max(blocks, key=len) if blocks else text).strip() + "\n", d.get("usageMetadata", {})


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True)


def main():
    uri = sys.argv[1] if len(sys.argv) > 1 else "argon-lol://update?target=all"
    target, urls, raw = parse(uri)

    # Her site argon-lol:// açabilir: neyin gönderildiğini görmeden başlatma.
    print(f"Hedef : {target}\nLinkler: {urls or '-'}\nHam metin: {len(raw)} karakter")
    if raw:
        print("--- ham metnin başı ---\n" + raw[:600] + "\n-----------------------")
    if input("Argon başlatılsın mı? [e/H] ").strip().lower() not in {"e", "evet", "y"}:
        sys.exit("İptal edildi.")

    old = DATA.read_text(encoding="utf-8")
    new, usage = argon(build_prompt(target, urls, raw))
    print(f"Token: girdi {usage.get('promptTokenCount')}, çıktı {usage.get('candidatesTokenCount')}")
    DATA.write_text(new, encoding="utf-8")
    # Bozuk dosya push'lanmasın: yüklenmezse eskisini geri koy.
    if subprocess.run(["node", "-e", "import('./src/data/squadData.js')"], cwd=ROOT).returncode:
        DATA.write_text(old, encoding="utf-8")
        sys.exit("Argon'un dosyası yüklenmedi, eski veri geri kondu.")

    if (ROOT / ".git").exists():
        git("add", "src/data/squadData.js")
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
            git("commit", "-m", f"data: Argon güncellemesi ({target}, {datetime.date.today()})")
            git("push")
            print("Push edildi; GitHub Pages 1-2 dakikada yenilenir.")
        else:
            print("Veride değişiklik yok.")
    else:
        print("Git deposu yok, yalnızca yerel dosya güncellendi.")


if __name__ == "__main__":
    try:
        main()
    finally:
        if sys.stdin.isatty():
            input("\nKapatmak için Enter...")
