#!/usr/bin/env bash
# Arms proving spark_gate.sh CAN FAIL. usage: test_spark_gate_arms.sh <repo-clone> <scratch-dir>
# Arm 1: wrong head sha -> exit 3 (refuse). Arm 2: nonexistent test file -> exit 4 (refuse, not "0 tests").
# Arm 3: the junit parser refuses a report with 0 tests (exit 4).
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; G="$HERE/../spark_gate.sh"
REPO="$1"; SCR="$2"; fail=0
# Refuse to run without its inputs (2026-10-26): with no args every arm failed on the
# invocation, not on spark_gate.sh, and read like a broken gate.
if [ -z "$REPO" ] || [ -z "$SCR" ] || [ ! -d "$REPO/.git" ] || [ ! -d "$SCR" ]; then
  echo "REFUSED: usage: test_spark_gate_arms.sh <repo-clone with .git> <existing scratch-dir>" >&2; exit 64
fi
if [ -z "$GIT_SSH_COMMAND" ] && [ -z "$(git -C "$REPO" config --get core.sshCommand)" ]; then
  echo "REFUSED: no GIT_SSH_COMMAND and no core.sshCommand in $REPO: the arms fetch the PR and need the deploy key" >&2; exit 64
fi
HEADOK=18e72727d94c81970952ea1d37b409d0b800bc76
TESTF=systemTest/schemathesis/tests/unit/support/test_precondition_probes_proposal_cap.py
bash "$G" "$REPO" 1687 0123456789abcdef0123456789abcdef01234567 develop "$TESTF" --work "$SCR/arm1_$$" < /dev/null; rc=$?
[ $rc -eq 3 ] && echo "ARM1 PASS: sha mismatch refused (exit 3)" || { echo "ARM1 FAIL: exit $rc"; fail=1; }
bash "$G" "$REPO" 1687 "$HEADOK" develop systemTest/schemathesis/tests/unit/support/test_does_not_exist.py --work "$SCR/arm2_$$" < /dev/null; rc=$?
[ $rc -eq 4 ] && echo "ARM2 PASS: missing test file refused (exit 4)" || { echo "ARM2 FAIL: exit $rc"; fail=1; }
printf '<testsuites><testsuite tests="0"></testsuite></testsuites>' > "$SCR/empty_$$.xml"
python3 "$HERE/../gate_facts.py" junit "$SCR/empty_$$.xml" "$SCR/empty_$$.json" < /dev/null; rc=$?
[ $rc -eq 4 ] && echo "ARM3 PASS: 0-test report refused (exit 4)" || { echo "ARM3 FAIL: exit $rc"; fail=1; }
exit $fail
