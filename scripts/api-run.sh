#!/usr/bin/env bash
# Runs one headless Claude Code job in this project, billed to the API credit, and logs its cost.
#   bash scripts/api-run.sh [--tag WS2] [--model MODEL] "prompt text"
# The job reads CLAUDE.md like any session, may edit files, run git and the project's scripts, and search the web.
# Output: the job's final answer on stdout; full JSON in /srv/realestate/logs/; one line per run appended to
# /srv/realestate/spend.jsonl (tag, cost, tokens), which scripts/spend-summary.sh rolls into docs/SPEND-LOG.md.
set -euo pipefail
PROJ=/root/projects/realestate; SEC=/srv/realestate/secrets; LOG=/srv/realestate/logs
TAG=general; MODEL=""
while [ $# -gt 1 ]; do
  case "$1" in --tag) TAG=$2; shift 2 ;; --model) MODEL=$2; shift 2 ;; *) break ;; esac
done
PROMPT=${1:?usage: api-run.sh [--tag TAG] [--model MODEL] "prompt"}
[ -f "$SEC/ANTHROPIC_API_KEY" ] || { echo "No key stored; run scripts/secret-set.sh ANTHROPIC_API_KEY" >&2; exit 1; }
install -d -m 700 "$LOG"
ts=$(date +%Y%m%d-%H%M%S); out="$LOG/$ts-$TAG.json"
cd "$PROJ"
set +e
ANTHROPIC_API_KEY=$(cat "$SEC/ANTHROPIC_API_KEY") claude -p "$PROMPT" \
  --output-format json --permission-mode acceptEdits \
  --allowedTools "Bash(git *) Bash(bash scripts/*) Bash(python3 *) Bash(uv *) Bash(ls *) Bash(cat *) Bash(wc *) Bash(grep *) Bash(find *) Bash(mkdir *) Bash(curl *) WebFetch WebSearch" \
  --append-system-prompt "You are a headless job launched by the realestate chat session. Do the task completely, write results to files in the repo, commit the files you changed with a meaningful message, and never wait for a human answer: note questions in docs/QUESTIONS-FOR-JOE.md with a provisional choice and continue." \
  ${MODEL:+--model "$MODEL"} > "$out"
rc=$?
set -e
python3 - "$out" "$TAG" "$ts" "$rc" <<'PYEOF'
import json, sys
p, tag, ts, rc = sys.argv[1:]
try:
    d = json.load(open(p))
except Exception as e:
    print(f"[api-run] exit={rc}; output was not JSON ({e}); see {p}"); sys.exit(0)
cost = d.get("total_cost_usd"); u = d.get("usage", {})
rec = {"ts": ts, "tag": tag, "cost_usd": cost, "input": u.get("input_tokens"), "output": u.get("output_tokens"),
       "cache_read": u.get("cache_read_input_tokens"), "cache_write": u.get("cache_creation_input_tokens"),
       "turns": d.get("num_turns"), "duration_ms": d.get("duration_ms"), "exit": int(rc)}
with open("/srv/realestate/spend.jsonl", "a") as f: f.write(json.dumps(rec) + "\n")
print(str(d.get("result", ""))[:6000])
print(f"\n[api-run] tag={tag} cost=${cost} turns={d.get('num_turns')} exit={rc} log={p}")
PYEOF
