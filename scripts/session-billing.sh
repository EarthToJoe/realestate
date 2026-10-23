#!/usr/bin/env bash
# Switches what the interactive realestate chat session bills.
#   off  (default, recommended): session on the claude.ai login, so it appears in the Claude app (Remote Control);
#        heavy work goes through scripts/api-run.sh, which bills the API credit.
#   on : session itself bills the API key. Claude Code then disables Remote Control, so the session is
#        reachable only via tmux on the VPS. Use only if Joe prefers that.
set -euo pipefail
UNIT=claude-remote@realestate
DROPIN=/etc/systemd/system/${UNIT}.service.d/billing.conf
SEC=/srv/realestate/secrets
[ "$(id -u)" = 0 ] || { echo "Run as root on the VPS." >&2; exit 1; }
case "${1:-}" in
  on)  [ -f "$SEC/claude-code.env" ] || { echo "No key stored; run scripts/secret-set.sh ANTHROPIC_API_KEY first." >&2; exit 1; }
       install -d -m 755 "$(dirname "$DROPIN")"
       printf '# Written by scripts/session-billing.sh. Only the realestate session reads this file.\n[Service]\nEnvironmentFile=-%s/claude-code.env\n' "$SEC" > "$DROPIN" ;;
  off) rm -f -- "${DROPIN:?}" ;;
  *)   echo "usage: $0 on|off" >&2; exit 1 ;;
esac
systemctl daemon-reload
systemctl restart "$UNIT"
echo "Interactive session billing: $1. Session restarted; give it 20 seconds."
