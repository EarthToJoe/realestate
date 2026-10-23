"""Logs one headless job's cost from its JSON output to /srv/realestate/spend.jsonl and prints its answer.

    python3 scripts/api_log.py LOG_JSON TAG TS EXIT_CODE

Called by scripts/api-run.sh after each job; run by hand to log a job whose runner failed after the job
itself finished (the JSON in /srv/realestate/logs/ is written by claude -p, not by the runner).
"""
import json
import sys

p, tag, ts, rc = sys.argv[1:5]
try:
    d = json.load(open(p))
except Exception as e:
    print(f"[api-run] exit={rc}; output was not JSON ({e}); see {p}")
    sys.exit(0)
cost = d.get("total_cost_usd"); u = d.get("usage", {})
rec = {"ts": ts, "tag": tag, "cost_usd": cost, "input": u.get("input_tokens"), "output": u.get("output_tokens"),
       "cache_read": u.get("cache_read_input_tokens"), "cache_write": u.get("cache_creation_input_tokens"),
       "turns": d.get("num_turns"), "duration_ms": d.get("duration_ms"), "exit": int(rc),
       "session": d.get("session_id")}
with open("/srv/realestate/spend.jsonl", "a") as f:
    f.write(json.dumps(rec) + "\n")
print(str(d.get("result", ""))[:6000])
print(f"\n[api-run] tag={tag} cost=${cost} turns={d.get('num_turns')} exit={rc} session={d.get('session_id')} log={p}")
