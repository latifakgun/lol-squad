#!/bin/bash
# Google Cloud VM'de (Debian 12) lolbot + kulak kurulumu. Tekrar çalıştırmak güvenli.
# Önce: bot/.env bu makineye ~/lol-squad/bot/.env olarak kopyalanmış olmalı.
set -euo pipefail
U=$(whoami); R=$HOME/lol-squad

# e2-micro (ücretsiz katman) 1 GB RAM: kurulum ve ses işleme taşmasın diye 1 GB swap.
[ -f /swapfile ] || { sudo fallocate -l 1G /swapfile; sudo chmod 600 /swapfile; sudo mkswap -q /swapfile
  sudo swapon /swapfile; echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null; }

sudo apt-get update -q
sudo apt-get install -yq git python3-venv ffmpeg curl
command -v node >/dev/null && node -e 'process.exit(+process.versions.node.split(".")[0] < 22)' || {
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -   # Debian'ın node 18'inde process.loadEnvFile yok
  sudo apt-get install -yq nodejs; }

[ -d "$R/.git" ] || { tmp=$(mktemp -d); git clone -q https://github.com/latifakgun/lol-squad "$tmp"; cp -rn "$tmp/." "$R/"; rm -rf "$tmp"; }
cd "$R"
python3 -m venv bot/.venv
bot/.venv/bin/pip install -q -r bot/requirements.txt
(cd kulak && npm ci --silent)
sed -i "s|^KULAK_PYTHON=.*|KULAK_PYTHON=$R/bot/.venv/bin/python|" bot/.env

unit() {  # ad, çalışma klasörü, komut
  sudo tee /etc/systemd/system/$1.service >/dev/null <<EOF
[Unit]
Description=$1
After=network-online.target
Wants=network-online.target
[Service]
User=$U
WorkingDirectory=$R/$2
Environment=PYTHONUTF8=1
ExecStart=$3
Restart=always
RestartSec=5
[Install]
WantedBy=multi-user.target
EOF
}
unit lolbot bot "$R/bot/.venv/bin/python -u bot.py"
unit kulak kulak "/usr/bin/node kulak.js"

# GitHub'daki değişiklikleri 5 dakikada bir çek (sunucu/guncelle.sh).
sudo tee /etc/systemd/system/lol-guncelle.service >/dev/null <<EOF
[Service]
Type=oneshot
ExecStart=/bin/bash $R/sunucu/guncelle.sh $U $R
EOF
sudo tee /etc/systemd/system/lol-guncelle.timer >/dev/null <<EOF
[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
[Install]
WantedBy=timers.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable lolbot kulak lol-guncelle.timer
echo "kuruldu. başlat: sudo systemctl start lolbot kulak lol-guncelle.timer"
