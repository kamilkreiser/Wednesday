#!/bin/bash
# Arms for friday/name_addendum.sh. The refuse arms are the REAL names that the tap gate refused
# on 2026-09-27..09-30 (Friday ledger, tap-verb rows w=2..w=6); the pass arms are the names they
# were renamed to, which the gate delivered.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$HERE/../friday/name_addendum.sh"
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT   # a scratch briefs dir this test created itself
pass=0; fail=0
arm() { # name expected-rc args...
  local name="$1" want="$2"; shift 2
  bash "$T" "$@" >/dev/null 2>"$D/err"; local rc=$?
  if [ "$rc" = "$want" ]; then pass=$((pass+1)); echo "PASS $name (rc $rc)"; else fail=$((fail+1)); echo "FAIL $name (rc $rc, want $want): $(head -2 "$D/err")"; fi
}
# refused by the real gate (real history)
arm "w2 accepted"          6 "$D" 2026-09-27_B47 1 accepted
arm "w3 start-H4"          6 "$D" 2026-09-29_B60 2 start-H4
arm "w5 deploy-checks"     6 "$D" 2026-09-30_B72 1 deploy-checks-ticket
arm "w6 resume-after"      6 "$D" 2026-09-30_B88 0 resume-after-account-switch
arm "merge in slug"        6 "$D" 2026-10-02_B06 1 merge-order
# renamed forms that the gate delivered
arm "w3 renamed base sha"  0 "$D" 2026-09-29_B60 2 H4-base-99a5ac6
arm "w5 renamed hosted"    0 "$D" 2026-09-30_B72 1 hosted-measurements-ticket
arm "w6 renamed state"     0 "$D" 2026-09-30_B88 0 account-switch-state
arm "check mode clean"     0 --check "$D/2026-10-02_B06_ADDENDUM-1_records.md"
arm "check mode dirty"     6 --check "$D/2026-10-02_B06_ADDENDUM-1_proceed.md"
# never clobber
touch "$D/2026-10-02_B06_ADDENDUM-1_findings.md"
arm "exists"               3 "$D" 2026-10-02_B06 1 findings
# fail closed when the gate's regex cannot be read
printf '#!/bin/bash\necho no gate here\n' > "$D/fake_cockpit.sh"
NAME_ADDENDUM_COCKPIT="$D/fake_cockpit.sh" arm "gate regex missing" 5 "$D" 2026-10-02_B06 2 records
NAME_ADDENDUM_COCKPIT="$D/nope.sh"         arm "gate unreadable"    5 "$D" 2026-10-02_B06 2 records
# usage
arm "bad slug"             2 "$D" 2026-10-02_B06 1 'two words'
echo "name_addendum arms: $pass PASS, $fail FAIL"
[ "$fail" -eq 0 ]
