#!/usr/bin/env bash
# Runs one headless Claude Code job in this project and logs its cost: on the API credit while it lasts, then on
# the Max login (Joe, 2026-10-23: "Do as much as you can with the api credit before moving to use the plan").
#   bash scripts/api-run.sh [--tag WS2] [--budget USD] [--effort LEVEL] [--model MODEL] [--resume SESSION_ID]
#                           [--billing auto|api|max] [--allow "Bash(docker *) Bash(hn *)"] "prompt"
# --budget is a hard cap for the job (claude --max-budget-usd; default 8). --effort defaults to high (the
# first runs used xhigh and spent about $125 in 35 minutes, 2026-10-23).
# --billing auto (default): the job runs on the credit if at least MIN_API dollars are left above the RESERVE kept
# for the POC's own calls at demo time (Max cannot pay for those), with its budget trimmed to what is left;
# otherwise, or once a job has hit "credit balance too low" (flag file), it runs on the Max login with no key in
# its environment. api forces the credit (refuses if it would cut into the reserve); max forces the plan.
# --allow adds tool permissions to the default set (research jobs need none; build jobs need docker, hn, make...).
# --resume continues an earlier job's session (its id is in spend.jsonl), keeping everything it already read.
# The job reads CLAUDE.md like any session, may edit files, run git and the project's scripts, and search the web.
# Output: the job's final answer on stdout; full JSON in /srv/realestate/logs/; one line per run appended to
# /srv/realestate/spend.jsonl (tag, billing, cost, tokens), which scripts/spend-summary.sh rolls into
# docs/SPEND-LOG.md. On Max the reported cost is notional (what the API would have charged).
# Bash reads a script while running it, so editing this file in place breaks every job running it (it did,
# 2026-10-23). The body is one function, parsed whole before it runs; still, replace the file by atomic rename.
main() {
  set -euo pipefail
  PROJ=/root/projects/realestate; SEC=/srv/realestate/secrets; LOG=/srv/realestate/logs
  TAG=general; MODEL=""; RESUME=""; BUDGET=8; EFFORT=high; BILLING=auto; ALLOW=""; CREDIT=200; RESERVE=15; MIN_API=2
  EXHAUSTED=/srv/realestate/credit-exhausted
  while [ $# -gt 1 ]; do
    case "$1" in --tag) TAG=$2; shift 2 ;; --model) MODEL=$2; shift 2 ;; --resume) RESUME=$2; shift 2 ;; --budget) BUDGET=$2; shift 2 ;; --effort) EFFORT=$2; shift 2 ;; --billing) BILLING=$2; shift 2 ;; --allow) ALLOW=$2; shift 2 ;; *) break ;; esac
  done
  PROMPT=${1:?usage: api-run.sh [--tag TAG] [--budget USD] [--billing auto|api|max] "prompt"}
  spent=$(python3 -c 'import json; print(round(sum(r.get("cost_usd") or 0 for r in map(json.loads, open("/srv/realestate/spend.jsonl")) if r.get("billing", "api") == "api"), 2))' 2>/dev/null || echo 0)
  left=$(python3 -c "print(round($CREDIT - $RESERVE - $spent, 2))")
  if [ "$BILLING" = auto ]; then
    if [ ! -e "$EXHAUSTED" ] && python3 -c "import sys; sys.exit(0 if $left >= $MIN_API else 1)"; then
      BILLING=api; BUDGET=$(python3 -c "print(min($BUDGET, $left))")
    else
      BILLING=max
    fi
  elif [ "$BILLING" = api ] && python3 -c "import sys; sys.exit(0 if $spent + $BUDGET > $CREDIT - $RESERVE else 1)"; then
    echo "[api-run] refused: logged credit spend \$$spent + budget \$$BUDGET would cut into the \$$RESERVE demo reserve of the \$$CREDIT credit" >&2; exit 3
  fi
  if [ "$BILLING" = api ]; then
    [ -f "$SEC/ANTHROPIC_API_KEY" ] || { echo "No key stored; run scripts/secret-set.sh ANTHROPIC_API_KEY" >&2; exit 1; }
  fi
  unset ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN ANTHROPIC_BASE_URL  # with no key, claude uses the Max login on this VPS
  # exported, not passed as an argument, so the key never shows in the process list; this script's process only
  [ "$BILLING" = api ] && export ANTHROPIC_API_KEY=$(cat "$SEC/ANTHROPIC_API_KEY")
  echo "[api-run] tag=$TAG billing=$BILLING budget=\$$BUDGET (credit left above reserve: \$$left)" >&2
  install -d -m 700 "$LOG"
  ts=$(date +%Y%m%d-%H%M%S); out="$LOG/$ts-$TAG.json"
  cd "$PROJ"
  set +e
  # A job's background helpers are stopped 10 minutes after its last turn unless the ceiling is lifted (lost
  # WS5's first run, 2026-10-23); lift it, and tell jobs to keep helpers in the foreground anyway.
  CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 claude -p "$PROMPT" \
    --output-format json --permission-mode acceptEdits --effort "$EFFORT" --max-budget-usd "$BUDGET" \
    --allowedTools "Bash(git *) Bash(bash scripts/*) Bash(python3 *) Bash(uv *) Bash(ls *) Bash(cat *) Bash(wc *) Bash(grep *) Bash(find *) Bash(mkdir *) Bash(curl *) WebFetch WebSearch${ALLOW:+ $ALLOW}" \
    --append-system-prompt "You are a headless job launched by the realestate chat session. Do the task completely, write results to files in the repo, commit the files you changed with a meaningful message, and never wait for a human answer: note questions in docs/QUESTIONS-FOR-JOE.md with a provisional choice and continue. A headless job ends the moment you end your turn: never end it while waiting for anything. Run subagents in the foreground (Agent without run_in_background; several in one message run in parallel and you wait for all of them) and never start background agents or background commands." \
    ${MODEL:+--model "$MODEL"} ${RESUME:+--resume "$RESUME"} > "$out"
  rc=$?
  set -e
  python3 "$PROJ/scripts/api_log.py" "$out" "$TAG" "$ts" "$rc" "$BILLING"
}
main "$@"; exit
