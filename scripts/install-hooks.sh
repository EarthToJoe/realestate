#!/usr/bin/env bash
# Installs the git hooks that republish https://realestate.hughesnode.com after every commit and pull.
# Hooks live in .git/hooks (not versioned), so run this once per clone.
set -euo pipefail
HOOKS=$(git -C /root/projects/realestate rev-parse --git-path hooks)
case "$HOOKS" in /*) ;; *) HOOKS=/root/projects/realestate/$HOOKS ;; esac
for h in post-commit post-merge; do
  cat > "$HOOKS/$h" <<'EOF'
#!/usr/bin/env bash
# Written by scripts/install-hooks.sh: republish the review site in the background.
( bash /root/projects/realestate/scripts/publish-review.sh >/srv/realestate/logs/publish-review.log 2>&1 & )
EOF
  chmod +x "$HOOKS/$h"
done
echo "hooks installed in $HOOKS"
