#!/usr/bin/env bash
# Hosting helper for the realestate hughesnode project. Touches nothing outside /srv/hughesnode/apps/realestate.
#   bash scripts/hosting.sh info     what hn has for realestate (README excerpt, app dir, compose file)
#   bash scripts/hosting.sh docker   switch the project to the docker type (copies deploy/hughesnode/* in, hn deploy)
#   bash scripts/hosting.sh static   switch back to the static type (keeps public/ as it is)
#   bash scripts/hosting.sh check    curl the live URL with the house login: app home, review home, a review page
set -euo pipefail
PROJ=/root/projects/realestate
APP=/srv/hughesnode/apps/realestate
cmd=${1:-info}

case "$cmd" in
  info)
    echo "== /srv/hughesnode/README.md"; cat /srv/hughesnode/README.md
    echo; echo "== $APP"; ls -la "$APP"
    for f in "$APP"/*; do [ -f "$f" ] && { echo "== $f"; sed -n '1,80p' "$f"; }; done
    ;;
  render)
    # How hn renders a docker-type project (read-only look at the hn command).
    sed -n "${2:-140,230p}" /srv/hughesnode/hn
    ;;
  docker)
    bash "$PROJ/scripts/disk-check.sh"
    install -m 644 "$PROJ/deploy/hughesnode/docker-compose.yml" "$APP/docker-compose.yml"
    # hn reads the project type from its own env file in the app dir; set it, keeping a backup.
    if [ -f "$APP/hn.env" ]; then
      cp "$APP/hn.env" "$APP/hn.env.static.bak"
      sed -i 's/^TYPE=.*/TYPE=docker/' "$APP/hn.env"
      grep -q '^PORT=' "$APP/hn.env" && sed -i 's/^PORT=.*/PORT=8000/' "$APP/hn.env" || echo 'PORT=8000' >> "$APP/hn.env"
    fi
    hn deploy realestate
    ;;
  static)
    [ -f "$APP/hn.env.static.bak" ] && cp "$APP/hn.env.static.bak" "$APP/hn.env"
    hn deploy realestate
    ;;
  check)
    PW='Fibonacci0!'
    for p in / /review/ /index.html /docs-success-criteria.html /healthz; do
      printf '%-32s ' "$p"; curl -s -o /dev/null -w '%{http_code}\n' -u ":$PW" "https://realestate.hughesnode.com$p"
    done
    printf '%-32s ' "(no login) /"; curl -s -o /dev/null -w '%{http_code}\n' "https://realestate.hughesnode.com/"
    ;;
  *) echo "usage: $0 info|docker|static|check" >&2; exit 2 ;;
esac
