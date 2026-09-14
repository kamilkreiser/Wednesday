#!/bin/bash
# checker.sh <input.json> <out.md> — state_census
# exit 0 = PASS, 1 = FAIL. Prints each assertion. stderr never discarded.
set -uo pipefail

INPUT="${1:-}"
OUT="${2:-}"
if [ -z "$INPUT" ] || [ -z "$OUT" ] || [ ! -f "$INPUT" ] || [ ! -f "$OUT" ]; then
  echo "usage: checker.sh <input.json> <out.md>" >&2
  exit 1
fi

python3 - "$INPUT" "$OUT" <<'PYEOF'
import json, re, sys, collections

input_path, out_path = sys.argv[1], sys.argv[2]
issues = json.load(open(input_path, encoding="utf-8"))
out = open(out_path, encoding="utf-8").read()

expected_ids = set(i["identifier"] for i in issues)
expected_counts = collections.Counter(i["state"]["type"] for i in issues)

# Find every identifier-shaped token that appears in a table row (first
# pipe-delimited cell) — this is deliberately loose about table formatting
# and strict about the two things that matter: every id present, no id
# invented.
row_ids = re.findall(r'^\s*\|?\s*([A-Z]{2,10}-\d+)\s*\|', out, flags=re.MULTILINE)
found_ids = set(row_ids)

ok = True

missing = expected_ids - found_ids
if missing:
    print(f"FAIL: identifiers missing from output: {sorted(missing)}")
    ok = False
else:
    print(f"PASS: all {len(expected_ids)} input identifiers appear in the output")

extra = found_ids - expected_ids
if extra:
    print(f"FAIL: identifiers in output NOT present in input: {sorted(extra)}")
    ok = False
else:
    print("PASS: no invented identifiers in output")

dupes = [k for k, v in collections.Counter(row_ids).items() if v > 1]
if dupes:
    print(f"FAIL: identifiers appearing more than once: {sorted(dupes)}")
    ok = False
else:
    print("PASS: every identifier appears exactly once")

# counts line: `counts: type=n, type=n, ...`
m = re.search(r'counts:\s*(.+)', out)
if not m:
    print("FAIL: no 'counts:' line found in output")
    ok = False
else:
    pairs = dict(re.findall(r'([a-zA-Z_]+)\s*=\s*(\d+)', m.group(1)))
    pairs = {k: int(v) for k, v in pairs.items()}
    expected = dict(expected_counts)
    if pairs == expected:
        print(f"PASS: counts line matches computed counts: {expected}")
    else:
        print(f"FAIL: counts line {pairs} != computed {expected}")
        ok = False

sys.exit(0 if ok else 1)
PYEOF
