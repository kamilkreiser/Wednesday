#!/bin/bash
# kam_awaiting_counts.sh — OPEN Datasec decision cards grouped by project, with age in hours.
# Read-only. Store: $DQ_FILE (same override decision_queue.sh uses) else 0_Brain/dashboard/data/decisions.json.
# Datasec rows only: filter is on the client_project FIELD (startswith "Datasec/"). Other clients are never printed.
# Usage: kam_awaiting_counts.sh [--json]
set -u
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export DQ_FILE="${DQ_FILE:-$DIR/../../../0_Brain/dashboard/data/decisions.json}"
MODE=text
for a in "$@"; do case "$a" in --json) MODE=json ;; *) echo "kam_awaiting_counts: unknown arg '$a' (only --json)" >&2; exit 2 ;; esac; done
export MODE
python3 - <<'PYEOF'
import datetime, json, os, sys
f = os.environ["DQ_FILE"]
try:
    data = json.load(open(f))
except Exception as e:
    print(f"kam_awaiting_counts: cannot read {f}: {e}", file=sys.stderr); sys.exit(2)
now = datetime.datetime.now().astimezone()
rows = []
for c in data:
    if not str(c.get("client_project", "")).startswith("Datasec/"): continue
    if c.get("status") != "open": continue
    age = None
    try: age = round((now - datetime.datetime.fromisoformat(c["ts"])).total_seconds() / 3600.0, 1)
    except Exception: print(f"kam_awaiting_counts: WARNING card {c.get('id')} has no parseable ts", file=sys.stderr)
    rows.append({"id": c["id"], "project": c["client_project"].split("/", 1)[1], "title": c.get("title", ""), "age_h": age})
by = {}
for r in rows: by.setdefault(r["project"], []).append(r)
if os.environ["MODE"] == "json":
    print(json.dumps({"total": len(rows), "projects": {p: {"count": len(v), "cards": v} for p, v in sorted(by.items())}}, indent=1)); sys.exit(0)
for p, v in sorted(by.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    print(f"awaiting {len(v)} for {p}")
    for r in sorted(v, key=lambda r: -(r["age_h"] or 0)):
        print(f"  {r['id']}  {'?' if r['age_h'] is None else r['age_h']}h")
print(f"total awaiting: {len(rows)}")
PYEOF
