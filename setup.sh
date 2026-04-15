#!/bin/bash
set -e

# ── Usage ─────────────────────────────────────────────────────────────────────
# ./setup.sh -ip <IP>
#
# Examples:
#   ./setup.sh -ip 127.0.0.1        # local setup
#   ./setup.sh -ip 11.22.33.44      # public server
# ──────────────────────────────────────────────────────────────────────────────

IP=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -ip)
      IP="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: ./setup.sh -ip <IP>"
      exit 1
      ;;
  esac
done

if [ -z "$IP" ]; then
  echo "Missing required argument: -ip"
  echo "Usage: ./setup.sh -ip <IP>"
  exit 1
fi

echo "IP: $IP"

# ── SSL certificate ───────────────────────────────────────────────────────────
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/ssl.key \
  -out    nginx/ssl/ssl.crt \
  -subj   "/CN=$IP"

# ── Secrets ───────────────────────────────────────────────────────────────────
echo "KEYCLOAK_ADMIN_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)" > .env
echo "KEYCLOAK_DB_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)"   >> .env

source .env

# ── Docker compose up ─────────────────────────────────────────────────────────
docker compose build
docker compose pull
docker compose up -d

# ── Wait for Keycloak ─────────────────────────────────────────────────────────
echo "Waiting for Keycloak..."
until docker compose exec -T keycloak \
    /opt/keycloak/bin/kcadm.sh config credentials \
    --server http://localhost:8080 \
    --realm master \
    --user admin \
    --password "$KEYCLOAK_ADMIN_PASSWORD" \
    > /dev/null 2>&1; do
  sleep 5
done

# ── Retrieve client secret ────────────────────────────────────────────────────
CLIENT_UUID=$(docker compose exec -T keycloak \
    /opt/keycloak/bin/kcadm.sh get clients \
    --server http://localhost:8080 \
    -r game \
    --fields id,clientId \
    | jq -r '.[] | select(.clientId=="game_client") | .id')

if [ -z "$CLIENT_UUID" ] || [ "$CLIENT_UUID" = "null" ]; then
  echo "Client game_client not found in realm game."
  echo "Make sure realm-game.json was imported correctly."
  exit 1
fi

SECRET=$(docker compose exec -T keycloak \
    /opt/keycloak/bin/kcadm.sh get \
    "clients/$CLIENT_UUID/client-secret" \
    --server http://localhost:8080 \
    -r game \
    | jq -r '.value')

# ── Update redirect URIs ──────────────────────────────────────────────────────
docker compose exec -T keycloak \
    /opt/keycloak/bin/kcadm.sh update \
    "clients/$CLIENT_UUID" \
    --server http://localhost:8080 \
    -r game \
    -s "redirectUris=[\"https://$IP/*\"]" \
    -s "webOrigins=[\"https://$IP\"]"

# ── Patch nginx.conf ──────────────────────────────────────────────────────────
sed -i "s/your_client_secret/$SECRET/g" nginx/nginx.conf
sed -i "s/127\.0\.0\.1/$IP/g"           nginx/nginx.conf

echo "KEYCLOAK_CLIENT_SECRET=$SECRET" >> .env

# ── Restart webserver ─────────────────────────────────────────────────────────
docker compose restart webserver

echo "Setup complete. App available at: https://$IP"
echo "Create your users at: https://$IP/keycloak/admin/master/console/#/game/users"
