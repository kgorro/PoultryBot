#!/usr/bin/env bash
# Starts the HTTPS gateway for all bots. Run from anywhere:  bash ~/poultrybot/deploy/gateway/setup.sh
set -euo pipefail
cd "$(dirname "$0")"
SUDO=""; docker info >/dev/null 2>&1 || SUDO="sudo"
if [ ! -f .env ]; then cp .env.example .env; echo "Edit $(pwd)/.env (DOMAIN and ACME_EMAIL), then run this again."; exit 1; fi
set -a; . ./.env; set +a
if [ -z "${DOMAIN:-}" ] || [ "$DOMAIN" = "example.com" ]; then echo "Set DOMAIN in $(pwd)/.env first."; exit 1; fi

# Only the gateway may use 80 and 443: stop a bot's own Caddy if one was started with the https profile
for c in $($SUDO docker ps --format '{{.Names}}' | grep -E '^(poultrybot|sugboguide)-caddy-' || true); do
  echo "Stopping $c (the gateway replaces it)"; $SUDO docker stop "$c" >/dev/null; $SUDO docker rm "$c" >/dev/null
done

if command -v ufw >/dev/null && $SUDO ufw status | grep -q "Status: active"; then
  $SUDO ufw allow 80/tcp >/dev/null; $SUDO ufw allow 443/tcp >/dev/null
fi

$SUDO docker compose up -d
echo "Waiting for certificates..."; sleep 8
$SUDO docker compose logs --tail 15 caddy | grep -iE "certificate obtained|error|failed" || true
echo
echo "Main page:   https://$DOMAIN/"
echo "JuanVet:     https://juanvet.$DOMAIN/   or  https://$DOMAIN/juanvet/"
echo "Sugbo Guide: https://sugbo.$DOMAIN/     or  https://$DOMAIN/sugbo/"
