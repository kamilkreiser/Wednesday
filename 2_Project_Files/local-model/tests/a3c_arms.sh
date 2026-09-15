#!/bin/bash
# a3c_arms.sh — red-proof for tasks/code_patch/a3c_plus.py (2026-09-15, IMPROVEMENTS row 89).
# Arm 1 (PASS): the real KS-999 r1 product section — the brief's line + a trailing `// KS-999:` comment.
# Arm 2 (FAIL): the same section with the added line REMOVED (the KS-976 B r1 dropped-hunk shape).
# Arm 3 (FAIL): the same section with a TOKEN altered inside the line (`await` dropped) — a comment strip must not hide it.
# Arm 4 (PASS): exact match with no comment (the KS-794 shape).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; LM="$(cd "$HERE/.." && pwd)"; PY="$LM/tasks/code_patch/a3c_plus.py"
[ -n "${A3C_PY_OVERRIDE:-}" ] && PY="$A3C_PY_OVERRIDE"
S="$(mktemp -d /private/tmp/claude-501/a3c_arms.XXXXXX)"
cat > "$S/input.json" <<'J'
{"defect_line":{"expected_plus":["if (result.rows.length > 0) return await fromRow(result.rows[0]);"]}}
J
EXP='    if (result.rows.length > 0) return await fromRow(result.rows[0]);'
printf '%s\n' "+++ b/x.ts" " try {" "-    if (result.rows.length > 0) return fromRow(result.rows[0]);" "+$EXP // KS-999: await so the catch classifies infra failures" "     return null;" > "$S/arm1.sec"
printf '%s\n' "+++ b/x.ts" " try {" "-    if (result.rows.length > 0) return fromRow(result.rows[0]);" "     return null;" > "$S/arm2.sec"
printf '%s\n' "+++ b/x.ts" " try {" "-    if (result.rows.length > 0) return fromRow(result.rows[0]);" "+    if (result.rows.length > 0) return fromRow(result.rows[0]); // KS-999: await so the catch classifies" "     return null;" > "$S/arm3.sec"
printf '%s\n' "+++ b/x.ts" " try {" "-    if (result.rows.length > 0) return fromRow(result.rows[0]);" "+$EXP" "     return null;" > "$S/arm4.sec"
pass=0; fail=0
run() { local name="$1" sec="$2" want="$3"; python3 "$PY" "$S/input.json" "$sec" > "$S/out" 2>&1; rc=$?; if [ "$rc" -eq "$want" ]; then echo "PASS $name (rc=$rc)"; pass=$((pass+1)); else echo "FAIL $name (rc=$rc, wanted $want): $(cat "$S/out")"; fail=$((fail+1)); fi; }
run "arm1 trailing-comment line is PRESENT" "$S/arm1.sec" 0
run "arm2 dropped addition is ABSENT" "$S/arm2.sec" 1
run "arm3 altered token behind a comment is ABSENT" "$S/arm3.sec" 1
run "arm4 exact line is PRESENT" "$S/arm4.sec" 0
echo "a3c_arms: $pass passed, $fail failed"; [ "$fail" -eq 0 ]
