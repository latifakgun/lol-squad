#!/bin/bash
# lol-guncelle.timer her 5 dk çalıştırır (root). GitHub'da yeni commit varsa çeker.
# Yalnızca .md değiştiyse (promptlar) yeniden başlatmaz: bot promptu her /bitti'de dosyadan okur, okunan sesi kesmeyelim.
set -euo pipefail
U=$1; R=$2
as() { runuser -u "$U" -- "$@"; }
cd "$R"
as git fetch -q origin
old=$(as git rev-parse HEAD); new=$(as git rev-parse '@{u}')
[ "$old" = "$new" ] && exit 0
as git merge -q --ff-only '@{u}'
changed=$(as git diff --name-only "$old" "$new")
echo "$changed" | grep -q '^bot/requirements.txt$' && as bot/.venv/bin/pip install -q -r bot/requirements.txt
echo "$changed" | grep -q '^kulak/package-lock.json$' && (cd kulak && as npm ci --silent)
echo "$changed" | grep '^bot/' | grep -qv '\.md$' && systemctl restart lolbot
echo "$changed" | grep '^kulak/' | grep -qv '\.md$' && systemctl restart kulak
echo "güncellendi: $old → $new"
