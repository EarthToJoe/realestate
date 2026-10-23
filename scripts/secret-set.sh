#!/usr/bin/env bash
# Stores one secret for the realestate project with hidden input (never paste secrets into chat).
#   sudo bash scripts/secret-set.sh ANTHROPIC_API_KEY
# Files land in /srv/realestate/secrets/ (root, 0600). ANTHROPIC_API_KEY additionally switches the
# realestate Claude Code session to API billing through a systemd drop-in that only that session reads.
# To switch back to Max: sudo bash scripts/secret-set.sh --remove ANTHROPIC_API_KEY
set -euo pipefail
SEC=/srv/realestate/secrets
UNIT=claude-remote@realestate
DROPIN=/etc/systemd/system/${UNIT}.service.d/billing.conf
[ "$(id -u)" = 0 ] || { echo "Run as root on the VPS (ssh -t vps sudo bash $0 NAME)." >&2; exit 1; }

remove=0
if [ "${1:-}" = "--remove" ]; then remove=1; shift; fi
NAME=${1:-}
[ -n "$NAME" ] || { echo "Usage: $0 [--remove] NAME" >&2; exit 1; }
[[ "$NAME" =~ ^[A-Z][A-Z0-9_]+$ ]] || { echo "NAME must look like ANTHROPIC_API_KEY" >&2; exit 1; }

install -d -m 700 "$SEC"

if [ $remove = 1 ]; then
  rm -f -- "${SEC:?}/${NAME:?}"
  if [ "$NAME" = ANTHROPIC_API_KEY ]; then
    rm -f -- "${SEC:?}/claude-code.env" "${DROPIN:?}"; systemctl daemon-reload
    systemctl is-active --quiet "$UNIT" && systemctl restart "$UNIT"
    echo "API billing off for the realestate session (back to the logged-in account)."
  fi
  echo "Removed $NAME."; exit 0
fi

[ -t 0 ] || { echo "Needs an interactive terminal for hidden input: ssh -t vps sudo bash $0 $NAME" >&2; exit 1; }
read -r -s -p "Paste the value for $NAME (hidden), then Enter: " VALUE; echo
[ -n "$VALUE" ] || { echo "Nothing entered; nothing changed." >&2; exit 1; }
umask 077
printf '%s' "$VALUE" > "$SEC/$NAME"
echo "Stored $SEC/$NAME (root only)."

if [ "$NAME" = ANTHROPIC_API_KEY ]; then
  printf 'ANTHROPIC_API_KEY=%s\n' "$VALUE" > "$SEC/claude-code.env"
  install -d -m 755 "$(dirname "$DROPIN")"
  cat > "$DROPIN" <<CONF
# Written by scripts/secret-set.sh. Only the realestate session reads this file.
[Service]
EnvironmentFile=-$SEC/claude-code.env
CONF
  # Pre-approve the key so Claude Code does not park on "Do you want to use this API key?" at every start.
  # Claude Code records approvals as the key's last 20 characters in /root/.claude.json.
  python3 - "$VALUE" <<'APPROVE'
import json, os, sys, tempfile
key = sys.argv[1][-20:]
p = '/root/.claude.json'
d = json.load(open(p)) if os.path.exists(p) else {}
r = d.setdefault('customApiKeyResponses', {}); a = r.setdefault('approved', [])
if key not in a: a.append(key)
r.setdefault('rejected', [])
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(p))
with os.fdopen(fd, 'w') as f: json.dump(d, f, indent=2)
os.chmod(tmp, 0o600); os.replace(tmp, p)
print("API key pre-approved in /root/.claude.json")
APPROVE
  systemctl daemon-reload
  if systemctl is-active --quiet "$UNIT"; then systemctl restart "$UNIT"; fi
  echo "The realestate session now bills the API key (check with /status inside the session: it should say API key)."
  echo "Other sessions are untouched."
fi
