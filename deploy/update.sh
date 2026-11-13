#!/usr/bin/env bash
# Pull the latest code and knowledge packs, rebuild, and restart. Saved LLM answers are kept; the bot ignores
# ones written for an older knowledge base.
set -euo pipefail
cd "$(dirname "$0")/.."
SUDO=""; docker info >/dev/null 2>&1 || SUDO="sudo"
git pull --ff-only
set -a; . ./.env; set +a
PROFILE=""; [ -n "${DOMAIN:-}" ] && PROFILE="--profile https"
$SUDO docker compose $PROFILE up -d --build
$SUDO docker image prune -f >/dev/null
