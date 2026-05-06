#!/usr/bin/env sh
set -e

cd "$(dirname "$0")"

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

if [ ! -d node_modules ]; then
  echo "node_modules not found — running npm install..."
  npm install
fi

exec node webhook-server.js
