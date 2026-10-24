"""argon-lol:// köprüsü: siteden gelen isteği Argon CLI'a verir, sonra commit + push yapar.

Kayıt: tools/register_protocol.ps1. Elle: python tools/argon_bridge.py "argon-lol://update?target=all"
URI: argon-lol://update?target=<all|l4cg|minte|swag|patrick|premade>&urls=<virgüllü>&clip=1
clip=1 ise ham metin panodan okunur (URI uzunluk sınırı yüzünden).
"""
import datetime
import pathlib
import shutil
import subprocess
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
ARSENAL = ROOT.parent.parent / "🛠️ 600-Arsenal"
TARGETS = {"all", "l4cg", "minte", "swag", "patrick", "premade"}
MODEL = "gemini-4-argon"


def parse(uri):
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(uri).query)
    target = q.get("target", ["all"])[0]
    if target not in TARGETS:
        sys.exit(f"Bilinmeyen hedef: {target}")
    urls = [u.strip() for u in q.get("urls", [""])[0].replace("\n", ",").split(",")]
    urls = [u for u in urls if u.startswith(("https://", "http://"))]
    raw = ""
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
                .replace("__RAW__", raw or "(yok)"))


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True)


def main():
    uri = sys.argv[1] if len(sys.argv) > 1 else "argon-lol://update?target=all"
    target, urls, raw = parse(uri)

    # Her site argon-lol:// açabilir ve Argon --yolo çalışıyor: neyin gönderildiğini görmeden başlatma.
    print(f"Hedef : {target}\nLinkler: {urls or '-'}\nHam metin: {len(raw)} karakter")
    if raw:
        print("--- ham metnin başı ---\n" + raw[:600] + "\n-----------------------")
    if input("Argon başlatılsın mı? [e/H] ").strip().lower() not in {"e", "evet", "y"}:
        sys.exit("İptal edildi.")

    gemini = shutil.which("gemini") or sys.exit("gemini CLI bulunamadı (npm i -g @google/gemini-cli).")
    cmd = [gemini, "--model", MODEL, "--yolo", "-p", "Stdin'deki görevi uygula."]
    if ARSENAL.exists():
        cmd[1:1] = ["--include-directories", str(ARSENAL)]
    subprocess.run(cmd, cwd=ROOT, input=build_prompt(target, urls, raw), text=True,
                   encoding="utf-8", check=True)

    # Argon kendi doğruluyor ama bozuk dosya push'lanmasın diye bir kez de biz bakalım.
    subprocess.run(["node", "-e", "import('./src/data/squadData.js')"], cwd=ROOT, check=True)

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
