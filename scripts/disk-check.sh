#!/usr/bin/env bash
# Prints free space on / and exits 0 (fine), 1 (warn: under 6 GB), 2 (stop: under 3 GB).
# Used by the realestate session at start and before anything disk-heavy, and by vps-setup.sh.
set -u
WARN_GB=${WARN_GB:-6}
STOP_GB=${STOP_GB:-3}
read -r size used avail pct < <(df -BG --output=size,used,avail,pcent / | tail -1 | tr -d 'G%')
echo "Disk on /: ${avail} GB free of ${size} GB (${pct}% used)"
if [ "$avail" -lt "$STOP_GB" ]; then
  echo "STOP: under ${STOP_GB} GB free. Nothing disk-heavy should run. Biggest folders:"
  du -xsh /root/projects/* /srv/* /home/* /var/lib/docker /var/cache /var/log 2>/dev/null | sort -rh | head -12
  exit 2
elif [ "$avail" -lt "$WARN_GB" ]; then
  echo "WARN: under ${WARN_GB} GB free. Tell Joe before it gets worse. Biggest folders:"
  du -xsh /root/projects/* /srv/* /home/* /var/lib/docker /var/cache /var/log 2>/dev/null | sort -rh | head -12
  exit 1
fi
exit 0
