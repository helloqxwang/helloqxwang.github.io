#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
if ! command -v node >/dev/null || ! command -v npm >/dev/null; then
  echo "Please install Node.js 24 or newer to preview this website."
  exit 1
fi
if [ ! -d node_modules ]; then npm ci; fi
exec npm run dev -- --host 127.0.0.1 --port 8080
