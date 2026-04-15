#!/bin/bash
set -e

# ── Usage ─────────────────────────────────────────────────────────────────────
# ./reset.sh
# Destroys all project data: containers, volumes, secrets, SSL, nginx patches.
# The project will be left in its original cloned state.
# Options:
#   -y    Skip confirmation prompt
# ──────────────────────────────────────────────────────────────────────────────
 
FORCE=false
 
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y)
      FORCE=true
      shift
      ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: ./reset.sh [-y]"
      exit 1
      ;;
  esac
done
 
if [ "$FORCE" = false ]; then
  read -p "This will destroy all project data. Are you sure? [y/N] " CONFIRM
  if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Aborted."
    exit 0
  fi
fi

# ── Stop and remove containers ────────────────────────────────────────────────
docker compose down -v

# ── Keycloak database ─────────────────────────────────────────────────────────
docker run --rm -v "$(pwd)/keycloak/data:/data" postgres:latest bash -c "rm -rf /data/*"

# ── SSL certificates ──────────────────────────────────────────────────────────
rm -f nginx/ssl/ssl.key nginx/ssl/ssl.crt

# ── Secrets ───────────────────────────────────────────────────────────────────
rm -f .env

# ── Restore nginx.conf ────────────────────────────────────────────────────────
git checkout nginx/nginx.conf

echo "Reset complete"
