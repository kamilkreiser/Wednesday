#!/bin/bash
# checker.sh <input.json> <out.md> — facts_comment
# exit 0 = PASS, 1 = FAIL. Prints each assertion. stderr never discarded.
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
input_text = open(input_path, encoding="utf-8").read()
out = open(out_path, encoding="utf-8").read()

ok = True

# 0 @ characters
at_count = out.count("@")
if at_count == 0:
    print("PASS: 0 '@' characters in output")
else:
    print(f"FAIL: {at_count} '@' character(s) found in output (mentions forbidden)")
    ok = False

# id extraction: KS-\d+, #\d+, 7-40 hex chars
ID_RE = re.compile(r'\bKS-\d+\b|#\d+\b|\b[0-9a-f]{7,40}\b')
input_ids = set(m.group(0) for m in ID_RE.finditer(input_text))
output_ids = set(m.group(0) for m in ID_RE.finditer(out))
invented = output_ids - input_ids
if invented:
    print(f"FAIL: id(s) in output not present in input: {sorted(invented)}")
    ok = False
else:
    print(f"PASS: every id in output ({sorted(output_ids)}) is present in input")

# first line starts with '## BLUF'
first_line = out.splitlines()[0] if out.splitlines() else ""
if first_line.startswith("## BLUF"):
    print("PASS: first line starts with '## BLUF'")
else:
    print(f"FAIL: first line does not start with '## BLUF' (got: {first_line!r})")
    ok = False

# length under 1500 chars
if len(out) < 1500:
    print(f"PASS: output length {len(out)} < 1500 chars")
else:
    print(f"FAIL: output length {len(out)} >= 1500 chars")
    ok = False

sys.exit(0 if ok else 1)
PYEOF
