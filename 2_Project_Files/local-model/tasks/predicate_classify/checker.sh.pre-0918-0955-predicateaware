#!/bin/bash
# checker.sh <input.json> <out.md> — predicate_classify
# The real check: a python reimplementation of the SAME written predicate
# agrees with the model's class on every row ("the second read"). Any
# disagreement is printed and the checker FAILs — it does not judge which
# side is right, only that they must agree.
# exit 0 = PASS, 1 = FAIL. stderr never discarded.
set -uo pipefail

INPUT="${1:-}"
OUT="${2:-}"
if [ -z "$INPUT" ] || [ -z "$OUT" ] || [ ! -f "$INPUT" ] || [ ! -f "$OUT" ]; then
  echo "usage: checker.sh <input.json> <out.md>" >&2
  exit 1
fi

python3 - "$INPUT" "$OUT" <<'PYEOF'
import json, re, sys

input_path, out_path = sys.argv[1], sys.argv[2]
data = json.load(open(input_path, encoding="utf-8"))
issues = data["issues"]
out = open(out_path, encoding="utf-8").read()

# --- the second read: reimplement the SAME predicate stated in sample_input.json:
# "class A = state type is 'started' AND the issue has a PR number (a '#'
# followed by digits) somewhere in its title or description; class B =
# state type is not 'started', OR state type is 'started' but no PR number
# appears; UNKNOWN only if the issue has no state field at all."
def classify(issue):
    if "state" not in issue or issue["state"] is None:
        return "UNKNOWN"
    stype = issue["state"].get("type")
    text = (issue.get("title") or "") + " " + (issue.get("description") or "")
    has_pr = bool(re.search(r'#\d+', text))
    if stype == "started" and has_pr:
        return "A"
    return "B"

expected = {i["identifier"]: classify(i) for i in issues}
expected_ids_in_order = [i["identifier"] for i in issues]

lines = [l for l in out.splitlines() if l.strip()]
ok = True

if len(lines) != len(issues):
    print(f"FAIL: expected {len(issues)} output lines, got {len(lines)}")
    ok = False

parsed = []
for ln in lines:
    parts = [p.strip() for p in ln.split("|")]
    if len(parts) < 3:
        print(f"FAIL: malformed line (need 'identifier | CLASS | reason'): {ln!r}")
        ok = False
        continue
    parsed.append((parts[0], parts[1], "|".join(parts[2:])))

parsed_ids = [p[0] for p in parsed]
if parsed_ids != expected_ids_in_order[:len(parsed_ids)]:
    print(f"FAIL: output identifier order/content {parsed_ids} != input order {expected_ids_in_order}")
    ok = False
else:
    print("PASS: one line per input identifier, in input order")

bad_class = [ (pid, cls) for pid, cls, _ in parsed if cls not in ("A", "B", "UNKNOWN") ]
if bad_class:
    print(f"FAIL: class value(s) outside {{A,B,UNKNOWN}}: {bad_class}")
    ok = False
else:
    print("PASS: every class value is one of A/B/UNKNOWN")

disagreements = []
for pid, cls, reason in parsed:
    exp = expected.get(pid)
    if exp is not None and cls != exp:
        disagreements.append((pid, "model="+cls, "second-read="+exp))

if disagreements:
    print(f"FAIL: second-read disagreement on {len(disagreements)} row(s): {disagreements}")
    ok = False
else:
    print(f"PASS: second-read (python reimplementation of the predicate) agrees with the model on all {len(parsed)} rows")

sys.exit(0 if ok else 1)
PYEOF
