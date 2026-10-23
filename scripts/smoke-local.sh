#!/usr/bin/env bash
# Starts `make run` for a few seconds and checks the app home, the review pages and /healthz, then stops it.
#   bash scripts/smoke-local.sh [port]
set -uo pipefail
cd "$(dirname "$0")/.."
PORT=${1:-8000}
mkdir -p tmp
# GNU make is not installed on the VPS; then run the Makefile's own `run` recipe line, unchanged.
if command -v make >/dev/null; then RUN="make run"; else
  RUN=$(awk '/^run:/{getline; sub(/^\t/, ""); print; exit}' Makefile | sed 's/\$(UV)/uv/')
  echo "make not found; running the Makefile recipe: $RUN"
fi
REALESTATE_MODEL_MODE=${REALESTATE_MODEL_MODE:-replay} timeout 60 bash -c "$RUN" > tmp/run.log 2>&1 &
PID=$!
for _ in $(seq 1 40); do curl -s -o /dev/null "http://127.0.0.1:$PORT/healthz" && break; sleep 1; done
fail=0
for p in /healthz / /intake?demo=1 /index.html /docs-success-criteria.html; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$PORT$p")
  printf '%-32s %s\n' "$p" "$code"; [ "$code" = 200 ] || fail=1
done
kill "$PID" 2>/dev/null; pkill -f "uvicorn --factory app.main:create_app --host 127.0.0.1 --port $PORT" 2>/dev/null
wait 2>/dev/null
[ $fail = 0 ] && echo "make run: OK" || { echo "make run: FAILED"; tail -20 tmp/run.log; exit 1; }
