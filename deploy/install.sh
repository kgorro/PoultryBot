#!/usr/bin/env bash
# One-time PoultryBot setup on a fresh Ubuntu or Debian VPS. Run as a sudo user:
#   curl -fsSL https://raw.githubusercontent.com/kgorro/PoultryBot/main/deploy/install.sh | bash
# or, after cloning:  bash deploy/install.sh
set -euo pipefail
REPO_URL=${REPO_URL:-https://github.com/kgorro/PoultryBot.git}
DIR=${DIR:-$HOME/poultrybot}

if ! command -v docker >/dev/null; then
  echo "Installing Docker"
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
fi
SUDO=""; docker info >/dev/null 2>&1 || SUDO="sudo"

if [ ! -d "$DIR/.git" ]; then git clone "$REPO_URL" "$DIR"; fi
cd "$DIR"
[ -f .env ] || cp .env.example .env
set -a; . ./.env; set +a

PROFILE=""; [ -n "${DOMAIN:-}" ] && PROFILE="--profile https"
$SUDO docker compose $PROFILE up -d --build

echo "Downloading the local model ${LLM_MODEL:-qwen2.5:3b-instruct} (a few GB, first run only)"
$SUDO docker compose exec -T ollama ollama pull "${LLM_MODEL:-qwen2.5:3b-instruct}"

sleep 3
$SUDO docker compose exec -T poultrybot python -c "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())"
if [ -n "${DOMAIN:-}" ]; then echo "PoultryBot: https://$DOMAIN"; else echo "PoultryBot: http://$(curl -fsS https://ifconfig.me || echo '<server-ip>'):${BOT_PORT:-8000}"; fi
