#!/usr/bin/env bash
# =============================================================================
# package_format_gate_dead_pid.test.sh — package_format_gate.test.sh picks its "dead" pid the way the gate does (KS-1926)
# =============================================================================
# Cases 20 and 32 of package_format_gate.test.sh plant a stage directory for a "dead" pid and expect the gate
# (check-package-format.sh, _sweep_dead_stages) to sweep it. The gate decides with `ps -p`. The test used to pick
# the pid with `kill -0`, which reports failure (EPERM) for a LIVE process owned by another user on macOS, so
# the test could call such a process dead and then fail on the gate's correct refusal to sweep it.
#
# This suite pins the PICKER, not the gate: it takes each picker line out of package_format_gate.test.sh, forces
# its starting pid to a live process owned by someone else (kill -0 fails, ps -p succeeds), runs the line, and
# requires that the pid it returns is one `ps -p` does not see. Nothing here touches the real tree.
# =============================================================================
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBJ="$HERE/package_format_gate.test.sh"
PASS=0; FAIL=0; EXPECT=5
ok()  { PASS=$((PASS + 1)); echo "PASS: $1"; }
bad() { FAIL=$((FAIL + 1)); echo "FAIL: $1 ($2)"; }

# The seam: the picker's random start expression, replaced by a chosen start pid in a COPY of the line.
START_EXPR='50000 + RANDOM % 9000'
PICKERS=()
while IFS= read -r l; do PICKERS+=("$l"); done < <(grep -F 'dead=$((50000 + RANDOM % 9000));' "$SUBJ")

# A live process this user cannot signal: kill -0 fails, ps -p sees it.
LIVE=""
# the range the test draws from (50000-58999) first, then any pid
for p in $(ps -axo pid= | awk '$1 >= 50000 && $1 <= 58999' | sort -rn) $(ps -axo pid= | sort -rn); do
  kill -0 "$p" 2>/dev/null && continue
  ps -p "$p" >/dev/null 2>&1 || continue
  LIVE="$p"; break
done
# A free pid: neither tool sees it.
FREE=50000
while kill -0 "$FREE" 2>/dev/null || ps -p "$FREE" >/dev/null 2>&1; do FREE=$((FREE + 1)); done

run_picker() {   # <picker line> <start pid> -> the pid the line settles on
  local line="${1/"$START_EXPR"/$2}"
  ( eval "$line"; echo "$dead" )
}

if [[ "${#PICKERS[@]}" -eq 2 ]]; then ok "CONTROL the suite holds exactly two picker lines (cases 20 and 32)"
else bad "CONTROL the suite holds exactly two picker lines (cases 20 and 32)" "found ${#PICKERS[@]}"; fi

if [[ -z "$LIVE" ]]; then
  EXPECT=3
  echo "SKIP: no live process owned by another user is visible to this account (running as root?)"
else
  n=0
  for line in "${PICKERS[@]}"; do
    n=$((n + 1))
    got="$(run_picker "$line" "$LIVE")"
    if [[ "$got" =~ ^[0-9]+$ ]] && ! ps -p "$got" >/dev/null 2>&1; then
      ok "picker $n skips a live pid owned by another user (start $LIVE -> $got)"
    else
      bad "picker $n skips a live pid owned by another user" "start $LIVE, picked '$got', which ps -p sees"
    fi
  done
fi

n=0
for line in "${PICKERS[@]}"; do
  n=$((n + 1))
  got="$(run_picker "$line" "$FREE")"
  if [[ "$got" == "$FREE" ]]; then ok "CONTROL picker $n keeps a free start pid ($FREE)"
  else bad "CONTROL picker $n keeps a free start pid" "start $FREE, picked '$got'"; fi
done

echo "$PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 && "$PASS" -eq "$EXPECT" ]]
