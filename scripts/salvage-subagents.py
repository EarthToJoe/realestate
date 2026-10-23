"""Turns a headless job's subagent transcripts into compact markdown digests another job can read.

    python3 scripts/salvage-subagents.py SESSION_ID OUT_DIR

Used when a job's background helpers were stopped before reporting (the print-mode wait ceiling): the
searches and fetches they paid for are still in ~/.claude/projects/.../<session>/subagents/*.jsonl. Each digest
keeps the helper's brief, every search query and fetched URL with the tool's answer (trimmed), and the
helper's own text, in order.
"""
import json
import sys
from pathlib import Path

PROJ = Path("/root/.claude/projects/-root-projects-realestate")
RESULT_CAP = 4000  # characters kept from each tool result; WebFetch answers are already summaries


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    parts = []
    for c in content or []:
        if isinstance(c, dict) and c.get("type") == "text":
            parts.append(c.get("text", ""))
    return "\n".join(parts)


def digest(path: Path) -> str:
    meta = path.with_suffix(".meta.json")
    out = [f"# Salvaged helper transcript: {path.stem}"]
    if meta.exists():
        out.append(f"Meta: `{meta.read_text().strip()}`")
    first_user = True
    for line in path.open():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        msg = rec.get("message") or {}
        role, content = msg.get("role"), msg.get("content")
        if role == "user":
            if first_user:
                out.append("## Brief given to the helper\n\n" + text_of(content).strip())
                first_user = False
                continue
            for c in content if isinstance(content, list) else []:
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    body = text_of(c.get("content")) if not isinstance(c.get("content"), str) else c["content"]
                    body = body.strip()
                    if len(body) > RESULT_CAP:
                        body = body[:RESULT_CAP] + f"\n[... trimmed {len(body) - RESULT_CAP} chars]"
                    out.append("**Result:**\n\n" + body)
        elif role == "assistant":
            for c in content if isinstance(content, list) else []:
                if not isinstance(c, dict):
                    continue
                if c.get("type") == "text" and c.get("text", "").strip():
                    out.append("**Helper notes:**\n\n" + c["text"].strip())
                elif c.get("type") == "tool_use":
                    inp = c.get("input", {})
                    what = inp.get("query") or inp.get("url") or inp.get("file_path") or inp.get("command") or json.dumps(inp)[:300]
                    if inp.get("prompt") and inp.get("url"):
                        what += f"  (asked: {inp['prompt'][:300]})"
                    out.append(f"### {c.get('name')}: {what}")
    return "\n\n".join(out) + "\n"


def main() -> None:
    session, out_dir = sys.argv[1], Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in sorted((PROJ / session / "subagents").glob("*.jsonl")):
        d = digest(p)
        (out_dir / f"{p.stem}.md").write_text(d)
        print(f"{len(d):>9,} chars  {out_dir / (p.stem + '.md')}")


if __name__ == "__main__":
    main()
