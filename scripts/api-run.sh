#!/usr/bin/env bash
# Runs one headless Claude Code job in this project, billed to the API credit, and logs its cost.
#   bash scripts/api-run.sh [--tag WS2] [--model MODEL] [--resume SESSION_ID] "prompt text"
# --resume continues an earlier job's session (its id is in spend.jsonl), keeping everything it already read.
# The job reads CLAUDE.md like any session, may edit files, run git and the project's scripts, and search the web.
# Output: the job's final answer on stdout; full JSON in /srv/realestate/logs/; one line per run appended to
# /srv/realestate/spend.jsonl (tag, cost, tokens), which scripts/spend-summary.sh rolls into docs/SPEND-LOG.md.
# Bash reads a script while running it, so editing this file in place breaks every job running it (it did,
# 2026-10-23). The body is one function, parsed whole before it runs; still, replace the file by atomic rename.
main() {
  set -euo pipefail
  PROJ=/root/projects/realestate; SEC=/srv/realestate/secrets; LOG=/srv/realestate/logs
  TAG=general; MODEL=""; RESUME=""
  while [ $# -gt 1 ]; do
    case "$1" in --tag) TAG=$2; shift 2 ;; --model) MODEL=$2; shift 2 ;; --resume) RESUME=$2; shift 2 ;; *) break ;; esac
  done
  PROMPT=${1:?usage: api-run.sh [--tag TAG] [--model MODEL] "prompt"}
  [ -f "$SEC/ANTHROPIC_API_KEY" ] || { echo "No key stored; run scripts/secret-set.sh ANTHROPIC_API_KEY" >&2; exit 1; }
  install -d -m 700 "$LOG"
  ts=$(date +%Y%m%d-%H%M%S); out="$LOG/$ts-$TAG.json"
  cd "$PROJ"
  set +e
  # A job's background helpers are stopped 10 minutes after its last turn unless the ceiling is lifted (lost
  # WS5's first run, 2026-10-23); lift it, and tell jobs to keep helpers in the foreground anyway.
  ANTHROPIC_API_KEY=$(cat "$SEC/ANTHROPIC_API_KEY") CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0 claude -p "$PROMPT" \
    --output-format json --permission-mode acceptEdits \
    --allowedTools "Bash(git *) Bash(bash scripts/*) Bash(python3 *) Bash(uv *) Bash(ls *) Bash(cat *) Bash(wc *) Bash(grep *) Bash(find *) Bash(mkdir *) Bash(curl *) WebFetch WebSearch" \
    --append-system-prompt "You are a headless job launched by the realestate chat session. Do the task completely, write results to files in the repo, commit the files you changed with a meaningful message, and never wait for a human answer: note questions in docs/QUESTIONS-FOR-JOE.md with a provisional choice and continue. A headless job ends the moment you end your turn: never end it while waiting for anything. Run subagents in the foreground (Agent without run_in_background; several in one message run in parallel and you wait for all of them) and never start background agents or background commands." \
    ${MODEL:+--model "$MODEL"} ${RESUME:+--resume "$RESUME"} > "$out"
  rc=$?
  set -e
  python3 "$PROJ/scripts/api_log.py" "$out" "$TAG" "$ts" "$rc"
}
main "$@"; exit
