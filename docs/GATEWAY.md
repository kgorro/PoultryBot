# HTTPS gateway for all bots (cccbdai.tech)

The poultry bot is shown to users as JuanVet; the repository and containers keep the name poultrybot.

One Caddy server owns ports 80 and 443 and sends each request to the right bot. Every bot is reachable two ways:

| Bot | Subdomain | Path |
|---|---|---|
| Landing page | https://cccbdai.tech/ | |
| JuanVet, the poultry bot (port 8000) | https://juangpt.cccbdai.tech/ | https://cccbdai.tech/juangpt/ |
| Sugbo Guide (port 8001) | https://sugbo.cccbdai.tech/ | https://cccbdai.tech/sugbo/ |

Certificates come from Let's Encrypt and renew automatically.

## 1. DNS

At your domain registrar, add three A records pointing to the VPS IP:

| Type | Name | Value |
|---|---|---|
| A | @ | 189.31.32.165 |
| A | juangpt | 189.31.32.165 |
| A | sugbo | 189.31.32.165 |

(Or one wildcard record `*` instead of the last two, so future projects need no DNS change.) Check with `nslookup juangpt.cccbdai.tech` before step 2; it can take a few minutes to an hour.

## 2. Start the gateway

    cd ~/poultrybot && git pull
    cd deploy/gateway
    cp .env.example .env
    nano .env                      # DOMAIN=cccbdai.tech, ACME_EMAIL=your email
    bash setup.sh

setup.sh opens ports 80 and 443 in ufw, stops any bot's own Caddy, starts the gateway, and prints the URLs. Also allow 80 and 443 in your VPS provider's firewall if it has one.

## 3. Close the raw ports (after HTTPS works)

So the bots are only reachable through HTTPS:

    # in ~/poultrybot/.env   set BOT_PORT=127.0.0.1:8000
    # in ~/sugboguide/.env   set BOT_PORT=127.0.0.1:8001
    cd ~/poultrybot && bash deploy/update.sh
    cd ~/sugboguide && bash deploy/update.sh
    sudo ufw delete allow 8000/tcp; sudo ufw delete allow 8001/tcp

Keep DOMAIN empty in each bot's own .env; the gateway handles HTTPS for all of them.

## Adding a project

1. Run it on the next free port, for example 8002, bound to 127.0.0.1.
2. In deploy/gateway/Caddyfile add a path block inside the main site and a subdomain block:

        redir /newbot /newbot/ 308
        handle_path /newbot/* {
            reverse_proxy 127.0.0.1:8002
        }

        newbot.{$DOMAIN} {
            reverse_proxy 127.0.0.1:8002
        }

3. Add a card to deploy/gateway/site/index.html, add the DNS record (unless you use the wildcard), and run `docker compose restart` in deploy/gateway.

Path routing works when the app uses relative URLs (fetch("chat"), not fetch("/chat")); both bot pages already do. If a new app breaks under a path, use its subdomain.

## Facebook Messenger

Webhook URL: https://juangpt.cccbdai.tech/messenger (or https://sugbo.cccbdai.tech/messenger).

## Troubleshooting

    cd ~/poultrybot/deploy/gateway && docker compose logs --tail 50 caddy

"no such host" or "NXDOMAIN" in the log means DNS is not ready yet; Caddy retries on its own. "connection refused" for a bot means that bot is not running on its port.
