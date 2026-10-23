#!/usr/bin/env bash
# One-time setup of the always-on "realestate" Remote Control session on the VPS, next to the other
# projects' sessions. Joe runs it once from his Mac (after creating the GitHub repo):
#
#   ssh -t vps 'd=/root/projects/realestate; [ -f "$d/scripts/vps-setup.sh" ] || git clone -q -b realestate-lifeboat --single-branch "$(git -C /root/projects/shorts remote get-url origin)" "$d"; bash "$d/scripts/vps-setup.sh"'
#
# The clone uses the shorts checkout's own remote URL (same repo, different branch), so it reuses whatever
# key or token shorts already uses and never asks for a GitHub login.
#
# What it does (each file is backed up first; safe to re-run):
#   0. Checks free disk and stops under 3 GB (Joe: the VPS is near its limit).
#   1. /root/.claude.json      marks /root/projects/realestate as trusted (no trust prompt to park on)
#   2. /root/.local/bin/rc     adds "realestate" to the project list rc manages (if rc exists)
#   3. systemd                 enables and starts claude-remote@realestate (own tmux socket rc-realestate)
#   4. Optional                stores the Anthropic API key for THIS session only (hidden input), so the
#                              $200 credit is used before Max, as Joe asked. Skipped when not interactive.
# Modelled on /root/projects/shorts/scripts/add-phone-session.sh.
set -euo pipefail
PROJ=/root/projects/realestate
NAME=realestate
ts=$(date +%Y%m%d%H%M%S)
[ "$(id -u)" = 0 ] || { echo "Run this as root on the VPS." >&2; exit 1; }
cd "$PROJ"
# The folder may have been cloned from the temporary 'realestate-lifeboat' branch of the shorts repo
# (used until the real EarthToJoe/realestate repo exists). Work on a local 'main' either way.
cur=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
[ "$cur" = main ] || git checkout -q -B main
origin=$(git remote get-url origin 2>/dev/null || echo none)
echo "Repo: $PROJ (origin: $origin, branch: main)"

echo "== 0. Disk"
bash "$PROJ/scripts/disk-check.sh" || { rc=$?; if [ $rc -ge 2 ]; then
  echo "Stopping: too little disk. Free space or upgrade the plan, then re-run this script."; exit 1; fi; }

echo "== 1. Trust the folder"
trust() {
python3 - <<'PY'
import json, os, sys, tempfile
p = '/root/.claude.json'
d = json.load(open(p))
proj = d.setdefault('projects', {}).setdefault('/root/projects/realestate', {})
if proj.get('hasTrustDialogAccepted') is True:
    sys.exit(0)
proj['hasTrustDialogAccepted'] = True
fd, tmp = tempfile.mkstemp(dir='/root')
with os.fdopen(fd, 'w') as f:
    json.dump(d, f, indent=2)
os.chmod(tmp, 0o600)
os.replace(tmp, p)
print('trust flag written')
PY
}
trusted() {
  python3 -c "import json,sys; d=json.load(open('/root/.claude.json')); sys.exit(0 if d.get('projects',{}).get('/root/projects/realestate',{}).get('hasTrustDialogAccepted') is True else 1)"
}
cp -p /root/.claude.json "/root/.claude.json.bak-$ts-before-$NAME"
trust

echo "== 2. rc project list"
if [ -f /root/.local/bin/rc ]; then
  if ! grep -qE "^PROJECTS=\(.*\b$NAME\b.*\)$" /root/.local/bin/rc; then
    cp -p /root/.local/bin/rc "/root/.local/bin/rc.before-$NAME-$ts"
    sed -i -E "s/^PROJECTS=\((.*)\)$/PROJECTS=(\1 $NAME)/" /root/.local/bin/rc
    echo "added $NAME to rc"
  fi
else
  echo "rc not found at /root/.local/bin/rc; skipping (the session still runs via systemd)."
fi

echo "== 3. systemd session"
if ! systemctl cat claude-remote@.service >/dev/null 2>&1; then
  echo "The template unit claude-remote@.service is missing on this VPS. Installing a copy of the pattern used by shorts." >&2
  install -m 644 "$PROJ/deploy/claude-remote@.service" /etc/systemd/system/claude-remote@.service
  systemctl daemon-reload
fi
echo "Template working directory line:"; systemctl cat claude-remote@.service | grep -E "WorkingDirectory|ExecStart" | head -3
# Other running Claude processes rewrite /root/.claude.json; make sure the flag survived before the new session reads it.
sleep 5; trusted || trust
systemctl enable --now "claude-remote@$NAME"
echo "Waiting for the session to come up..."; sleep 20
trusted || { echo "Trust flag was lost; re-applying and restarting."; trust; systemctl restart "claude-remote@$NAME"; sleep 20; }

echo "== 4. API billing for this session (Joe, 2026-10-23: all of this project's work runs on the API credit)"
if [ -f /srv/realestate/secrets/claude-code.env ]; then
  echo "API key already stored; heavy work bills the credit via scripts/api-run.sh."
elif [ -t 0 ]; then
  echo "You need an API key from console.anthropic.com (API keys, Create key). Nothing is shown while you paste it."
  read -r -p "Store the Anthropic API key now so THIS session uses the \$200 credit? [Y/n] " yn
  [ -z "$yn" ] && yn=y
  case "$yn" in y|Y) bash "$PROJ/scripts/secret-set.sh" ANTHROPIC_API_KEY; bash "$PROJ/scripts/session-billing.sh" off ;; *) echo "Skipped. Later: ssh -t vps sudo bash $PROJ/scripts/secret-set.sh ANTHROPIC_API_KEY" ;; esac
else
  echo "Not interactive; skipped. Later: ssh -t vps sudo bash $PROJ/scripts/secret-set.sh ANTHROPIC_API_KEY"
fi

echo
[ -x /root/.local/bin/rc ] && /root/.local/bin/rc list || systemctl --no-pager status "claude-remote@$NAME" | head -5
echo
echo "Success = '$NAME' shows active/up here and a session named '$NAME' appears in your Claude app."
echo "Attach to its terminal if ever needed: tmux -L rc-$NAME attach"
case "$origin" in *shorts*) echo
  echo "NOTE: this clone came from the temporary lifeboat branch in the shorts repo. Once EarthToJoe/realestate"
  echo "exists (private, empty), run once:  bash $PROJ/scripts/repoint-origin.sh" ;; esac
