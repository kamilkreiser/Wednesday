#!/bin/bash
# a3c_multiset_arm_2026-10-01.sh — the red arm for A3c-as-MULTISET (a3c_plus.py, 2026-10-01).
# Subject: KS-1364 nft-verify, whose brief adds `      required: true,` TWICE.
#   ARM 1 (golden section)                          -> exit 0 (both copies present)
#   ARM 2 (one copy mutated to `required: !0,`)     -> exit 1 (one expected copy MISSING)  <- PASSED under the old set-based A3c
#   ARM 3 (one copy dropped entirely)               -> exit 1
#   CONTROLS: the three real Spark outputs held today (runs/spark_secuura_2026-10-01_KS-1364-*) -> exit 0 each
set -u
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
A=$L/tasks/code_patch/a3c_plus.py
B=$L/night/briefs/KS-1364-nft-verify/precheck
IN=$B/input.json
TMP=$(mktemp -d)
G=$B/out.md.checker/section_1.diff
python3 $A $IN $G >/dev/null; echo "ARM 1 golden: exit $? (want 0)"
python3 - "$G" "$TMP/mut.diff" "$TMP/drop.diff" <<'EOF'
import sys
s = open(sys.argv[1]).read()
i = s.index('+      required: true,')
open(sys.argv[2], 'w').write(s[:i] + '+      required: !0,' + s[i + len('+      required: true,'):])
open(sys.argv[3], 'w').write(s[:i] + s[i + len('+      required: true,\n'):])
EOF
python3 $A $IN $TMP/mut.diff >/dev/null; echo "ARM 2 one of two identical lines mutated: exit $? (want 1)"
python3 $A $IN $TMP/drop.diff >/dev/null; echo "ARM 3 one of two identical lines dropped: exit $? (want 1)"
for t in nft-record-estimate nft-verify analytics-reports; do
  R=$L/runs/spark_secuura_2026-10-01_KS-1364-$t
  python3 $A $R/input.json $R/out.md.checker/section_1.diff >/dev/null; echo "CONTROL today's held run $t: exit $? (want 0)"
done
