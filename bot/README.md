# Maç sonu ses botu

Discord'da `/bitti` yazınca: Riot'un resmî API'sinden ekibin son maçını çeker → Argon (Gemini CLI) konuşma metnini yazar → Gemini Pro TTS (Fenrir sesi) seslendirir → bot komutu yazanın ses kanalına girer, okur, çıkar. Metin aynı anda kanala da yazılır.

LoL istemcisine, oyun belleğine ya da Vanguard'ın gördüğü hiçbir şeye dokunmaz; yalnızca Riot'un web API'sini kullanır.

## 1. Hesaplar (bir kez)

**Discord** — https://discord.com/developers/applications
1. *New Application* → isim ver → *Bot* sekmesi → *Reset Token* → token'ı kopyala (kimseyle paylaşma).
2. *Privileged Gateway Intents*: hiçbirini açmana gerek yok.
3. *OAuth2 → URL Generator*: scope `bot` + `applications.commands`; izinler **View Channels, Connect, Speak, Send Messages**. Çıkan linkle botu sunucuya davet et.
4. Discord'da *Ayarlar → Gelişmiş → Geliştirici Modu*'nu aç, sunucuya sağ tık → *Sunucu ID'sini Kopyala*.

**Riot** — https://developer.riotgames.com
1. Riot hesabınla gir. Ana sayfadaki *Development API Key* hemen çalışır ama 24 saatte bir yenilenmesi gerekir.
2. Kalıcı anahtar için *Register Product → Personal API Key*: "Arkadaş grubumuzun özel Discord sunucusu için maç sonu analiz botu" diye kısa bir açıklama yeter.

## 2. Masaüstü kurulumu

Gerekenler: Python 3.11+, Node.js, Git, ffmpeg.

```powershell
winget install Python.Python.3.12 OpenJS.NodeJS Git.Git Gyan.FFmpeg Google.CloudSDK
npm install -g @google/gemini-cli

git clone https://github.com/latifakgun/lol-squad
cd lol-squad\bot
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env      # sonra .env'i doldur
```

**Google (Argon + TTS) girişi:**
```powershell
gcloud auth application-default login
gcloud auth application-default set-quota-project <GOOGLE_CLOUD_PROJECT>
gemini     # bir kez aç, Vertex AI ile giriş yap, çık
```

## 3. Çalıştır

```powershell
.venv\Scripts\python bot.py --test ornek_mac.json   # Discord'suz deneme → out\test.wav
.venv\Scripts\python bot.py                          # bot açılır, "Hazır" yazınca /bitti kullanılabilir
```

Arkada açık bırakmak için PowerShell penceresini küçültmen yeterli. Bilgisayar açılınca otomatik başlasın istersen Görev Zamanlayıcı'ya `bot.py` eklenir.

## Ayarlar
- Ekip, Riot ID'ler, model ve ses: `bot.py` başındaki `SQUAD`, `TTS_MODEL`, `TTS_VOICE`.
- Argon'un ton ve yazım kuralları: `script_prompt.md`.
- Analiz edilen maçlar `state.json`'da tutulur; aynı maç iki kez okunmaz.
