# Deploying PoultryBot on a VPS with Docker

Two containers: the bot (FastAPI, DALAN router, knowledge dump) and Ollama (the local LLM). Caddy is optional and adds HTTPS when you have a domain.

## VPS size

| RAM | Model (LLM_MODEL) | Notes |
|---|---|---|
| 4 GB | qwen2.5:3b-instruct (default) | CPU only; LLM answers take several seconds, but most questions never reach the LLM |
| 8 GB or more | qwen2.5:7b-instruct | Better generated answers |
| 2 GB | none | The bot still runs; uncertain questions get the closest verified topic instead of an LLM answer |

Use about 15 GB of free disk for the images and one model. Ubuntu 22.04 or 24.04, or Debian 12.

## First install

SSH into the VPS and run:

    git clone https://github.com/kgorro/PoultryBot.git ~/poultrybot
    cd ~/poultrybot
    cp .env.example .env
    nano .env                      # pick LLM_MODEL; set DOMAIN if you have one
    bash deploy/install.sh

install.sh installs Docker if it is missing, builds and starts the containers, downloads the model, and prints the URL and the /health check. If Docker was just installed, log out and back in once so you can run docker without sudo.

If the repository is private, clone with a GitHub personal access token or a deploy key instead of the plain URL.

## Without a domain

The bot is at http://SERVER_IP:8000. Open the port:

    sudo ufw allow OpenSSH
    sudo ufw allow 8000/tcp
    sudo ufw enable

## With a domain (HTTPS)

1. Point a DNS A record (for example poultrybot.example.com) to the VPS IP.
2. In .env set DOMAIN=poultrybot.example.com and BOT_PORT=127.0.0.1:8000.
3. Open ports 80 and 443 (sudo ufw allow 80,443/tcp) and run bash deploy/install.sh again.

Caddy gets and renews the certificate automatically. Facebook Messenger needs HTTPS, so use this setup for the webhook: https://DOMAIN/messenger.

## Everyday commands

    bash deploy/update.sh                          # pull new code or knowledge packs, rebuild, restart
    docker compose logs -f poultrybot              # bot logs
    docker compose ps                              # status
    curl localhost:8000/health                     # dump loaded? how many cached answers?
    docker compose exec ollama ollama pull qwen2.5:7b-instruct    # switch model, then set LLM_MODEL and run update.sh

Saved LLM answers live in the botdata volume and survive rebuilds. Answers saved for an older knowledge base are ignored automatically.

## Security notes

- Log in with an SSH key and turn off password login (PasswordAuthentication no in /etc/ssh/sshd_config).
- Ollama is not published to the internet; only the bot container can reach it.
- Keep FB tokens in .env only. .env is not committed.
- Three of the four research packs are from accepted or in-press papers. Confirm with the authors before opening the bot to the public.
