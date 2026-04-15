#!/bin/bash
set -e

# ── Usage ─────────────────────────────────────────────────────────────────────
# ./setup.sh -ip <IP>
#
# Examples:
#   ./setup.sh -ip localhost        # local setup
#   ./setup.sh -ip 127.0.0.1        # local setup
#   ./setup.sh -ip [::1]            # local setup (IPv6)
#   ./setup.sh -ip 11.22.33.44      # public server
#   ./setup.sh -ip [1:2:3:4:5:6]    # public server (IPv6)
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

# ── Fresh install ───────────────────────────────────────────────────────────

bash reset.sh -y

# ── Patch nginx.conf 1/2 ──────────────────────────────────────────────────────────
sed -i "/resolver/!s/127\.0\.0\.1/$IP/g" nginx/nginx.conf
echo "Nginx configured with IP: $IP"

# ── SSL certificate ───────────────────────────────────────────────────────────
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/ssl.key \
  -out    nginx/ssl/ssl.crt \
  -subj   "/CN=$IP"
chmod 644 nginx/ssl/ssl.key nginx/ssl/ssl.crt

# ── Secrets ───────────────────────────────────────────────────────────────────
echo "KEYCLOAK_ADMIN_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)" > .env
echo "KEYCLOAK_DB_PASSWORD=$(cat /dev/urandom | tr -dc 'A-Za-z0-9' | fold -w 32 | head -n 1)"   >> .env

source .env

echo "All secrets set up"

# ── Docker compose up ─────────────────────────────────────────────────────────
docker compose build
docker compose pull
docker compose up -d

# ── Wait for Keycloak & get token ─────────────────────────────────────────────────────────
echo "Waiting for Keycloak..."
until TOKEN=$(
  curl -sk -X POST \
    "https://$IP/keycloak/realms/master/protocol/openid-connect/token" \
    -d "client_id=admin-cli" \
    -d "username=admin" \
    -d "password=$KEYCLOAK_ADMIN_PASSWORD" \
    -d "grant_type=password" |
    jq -r '.access_token' 2>/dev/null
  ) &&
  [ -n "$TOKEN" ] &&
  [ "$TOKEN" != "null" ];
  do
    sleep 5
done

echo "Configuring Keycloak..."

# ── Retrieve client secret ────────────────────────────────────────────────────
# UUID du client
CLIENT_UUID=$(curl -sk \
  "https://$IP/keycloak/admin/realms/game/clients?clientId=game_client" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.[0].id')

# Secret
SECRET=$(curl -sk \
  "https://$IP/keycloak/admin/realms/game/clients/$CLIENT_UUID/client-secret" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.value')

# ── Update redirect URIs ──────────────────────────────────────────────────────
curl -sk -X PUT \
  "https://$IP/keycloak/admin/realms/game/clients/$CLIENT_UUID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"redirectUris\":[\"https://$IP/*\"],\"webOrigins\":[\"https://$IP\"]}"

echo "Keycloak configured"

# ── Patch nginx.conf 2/2 ──────────────────────────────────────────────────────────
sed -i "s/your_client_secret/$SECRET/g"  nginx/nginx.conf
echo "Nginx configured with Keycloak client secret"

echo "KEYCLOAK_CLIENT_SECRET=$SECRET" >> .env

echo "Restarting nginx..."

# ── Restart webserver ─────────────────────────────────────────────────────────
docker compose restart webserver

echo "Setup complete. App available at: https://$IP"
echo "Create your users at: https://$IP/keycloak/"
echo "Username: admin"
echo "Password: $KEYCLOAK_ADMIN_PASSWORD"
echo "Realm: Game"
echo "Don't forget to provide the users with credentials"
echo "The app runs at: https://$IP/"
