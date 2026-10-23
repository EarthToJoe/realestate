#!/usr/bin/env bash
# Hosting helper for the realestate hughesnode project. Changes nothing outside /srv/hughesnode/apps/realestate
# and /srv/realestate (hn itself, Traefik and other apps are untouched).
#   bash scripts/hosting.sh info       README, the app dir and its hn.conf
#   bash scripts/hosting.sh render [range]   read-only look at how hn renders a project (sed range of hn)
#   bash scripts/hosting.sh prepare    data dir, PII_KEY and DB_KEY secrets (created once, mode 600), src/ synced
#   bash scripts/hosting.sh trial      run the image on 127.0.0.1:8099 with the real mounts and check it
#   bash scripts/hosting.sh docker     switch the project to the docker type and deploy (backup: hn.conf.static.bak)
#   bash scripts/hosting.sh redeploy   sync src/ from the repo and rebuild (after code changes)
#   bash scripts/hosting.sh static     switch back to the static type (restores hn.conf.static.bak)
#   bash scripts/hosting.sh check      curl the live URL with the house login
set -euo pipefail
PROJ=/root/projects/realestate
APP=/srv/hughesnode/apps/realestate
SECRETS=/srv/realestate/secrets
DATA=/srv/realestate/data
cmd=${1:-info}

# The volumes the container gets (hn.conf VOLUMES, one per line). The model key and the PII/DB keys are mounted
# read-only; nothing secret goes into the image, app.env or a compose label.
VOLUMES="$SECRETS:/run/secrets/realestate:ro
$DATA:/data
./public:/review:ro"

sync_src() {
  mkdir -p "$APP/src"
  # Only what the image needs; the build context stays small and holds no docs, notes or secrets.
  tar -C "$PROJ" -cf - Dockerfile .dockerignore requirements.txt app config fixtures seed replays scripts/try \
    | tar -C "$APP/src" -xf -
  find "$APP/src" -name __pycache__ -type d -prune -exec rm -rf {} +
}

set_conf() { # set_conf KEY VALUE  (same quoting as hn's own set_kv)
  python3 - "$APP/hn.conf" "$1" "$2" <<'PY'
import sys
f, k, v = sys.argv[1:4]
v = v.replace("'", "'\\''")
out, skipping = [], False
for line in open(f):
    if skipping:  # inside an old multi-line value: drop lines up to its closing quote
        skipping = not line.rstrip("\n").endswith("'")
        continue
    if line.startswith(k + "="):
        body = line.rstrip("\n")[len(k) + 1:]
        skipping = not (len(body) >= 2 and body.endswith("'"))
        continue
    out.append(line)
out.append(f"{k}='{v}'\n")
open(f, "w").writelines(out)
PY
}

case "$cmd" in
  info)
    echo "== /srv/hughesnode/README.md"; cat /srv/hughesnode/README.md
    echo; echo "== $APP"; ls -la "$APP"
    echo "== $APP/hn.conf"; cat "$APP/hn.conf"
    ;;
  render)
    sed -n "${2:-140,230p}" /srv/hughesnode/hn
    ;;
  prepare)
    bash "$PROJ/scripts/disk-check.sh"
    mkdir -p "$DATA"; chmod 700 "$DATA"
    for k in PII_KEY DB_KEY; do
      if [ ! -s "$SECRETS/$k" ]; then
        ( umask 077; python3 -c "import base64,os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())" > "$SECRETS/$k" )
        echo "created $SECRETS/$k (mode 600)"
      fi
    done
    sync_src
    echo "src synced to $APP/src"
    ;;
  trial)
    docker build -q -t hn-realestate-trial "$APP/src" >/dev/null
    docker rm -f realestate-trial >/dev/null 2>&1 || true
    docker run -d --name realestate-trial -p 127.0.0.1:8099:8000 \
      -v "$SECRETS:/run/secrets/realestate:ro" -v "$DATA:/data" -v "$APP/public:/review:ro" \
      hn-realestate-trial >/dev/null
    for _ in $(seq 1 30); do curl -s -o /dev/null http://127.0.0.1:8099/healthz && break; sleep 1; done
    for p in /healthz / /intake?demo=1 /index.html /docs-success-criteria.html /docs-research-ws2-legal-licensing.html; do
      printf '%-44s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:8099$p")"
    done
    curl -s http://127.0.0.1:8099/healthz; echo
    docker logs realestate-trial 2>&1 | tail -5
    docker rm -f realestate-trial >/dev/null
    ;;
  docker)
    bash "$PROJ/scripts/disk-check.sh"
    [ -f "$APP/hn.conf.static.bak" ] || cp -p "$APP/hn.conf" "$APP/hn.conf.static.bak"
    sync_src
    set_conf TYPE docker
    set_conf PORT 8000
    set_conf VOLUMES "$VOLUMES"
    hn deploy realestate
    ;;
  redeploy)
    sync_src
    hn deploy realestate
    ;;
  static)
    cp -p "$APP/hn.conf.static.bak" "$APP/hn.conf"
    hn deploy realestate
    ;;
  check)
    PW='Fibonacci0!'  # the house login from /root/projects/CLAUDE.md (blank username)
    for p in / /intake /timeline /index.html /docs-success-criteria.html /docs-research-ws2-legal-licensing.html /healthz; do
      printf '%-44s %s\n' "$p" "$(curl -s -o /dev/null -w '%{http_code}' -u ":$PW" "https://realestate.hughesnode.com$p")"
    done
    printf '%-44s %s\n' "(no login) /" "$(curl -s -o /dev/null -w '%{http_code}' https://realestate.hughesnode.com/)"
    ;;
  *) echo "usage: $0 info|render|prepare|trial|docker|redeploy|static|check" >&2; exit 2 ;;
esac
