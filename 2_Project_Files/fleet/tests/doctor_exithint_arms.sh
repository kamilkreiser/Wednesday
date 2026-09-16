#!/bin/bash
# doctor_exithint_arms.sh — red-proof for doctor.sh's launchd exit-code hints (2026-09-16).
# WHY: Tuesday's 2026-09-16 STATUS (disagreement 4) — doctor printed the 78/EX_CONFIG hint for a
# chat_sync that exited 126 (TCC), and the scheduler loop lumped 126 with 78. Two failures, two
# fixes. These arms drive doctor.sh with a FAKE launchctl on PATH so no real job is touched.
#   ARM 1  exit 126 -> chat_sync line names "not permitted" + Full Disk Access; scheduler names TCC
#   ARM 2  exit 78  -> chat_sync line names EX_CONFIG + ~/Library/Logs; scheduler names EX_CONFIG
#   ARM 3  exit 0   -> CONTROL: chat_sync "last launchd exit clean", no 126/78 hint printed
#   ARM 4  exit 126 against the PRE-FIX doctor -> it prints the 78 hint (the defect, reproduced),
#          proving arms 1-3 discriminate rather than pass on any doctor.
# Usage: bash 2_Project_Files/fleet/tests/doctor_exithint_arms.sh
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PF="$(cd -P "$HERE/../.." && pwd)"
NEW="$PF/doctor.sh"
OLD="$PF/doctor.sh.pre-0916-exithint"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/doctor_exithint.XXXXXX")"
PASS=0; FAIL=0

mkfake() { # $1 = exit code to report
  mkdir -p "$WORK/bin_$1"
  cat > "$WORK/bin_$1/launchctl" <<EOF
#!/bin/bash
case "\$1" in
  print) printf '\tstate = not running\n\tlast exit code = %s\n' "$1"; exit 0 ;;
  *) exit 1 ;;
esac
EOF
  chmod +x "$WORK/bin_$1/launchctl"
}

run_doctor() { # $1 = doctor path  $2 = code ; output file printed
  local out="$WORK/out_$(basename "$1")_$2.txt"
  PATH="$WORK/bin_$2:$PATH" bash "$1" > "$out" 2>&1
  echo "$out"
}

check() { # $1 name  $2 file  $3 grep -F pattern  $4 want (present|absent)
  if /usr/bin/grep -qiF -- "$3" "$2"; then got=present; else got=absent; fi
  if [ "$got" = "$4" ]; then echo "PASS: $1"; PASS=$((PASS+1)); else echo "FAIL: $1 (pattern '$3' $got, want $4) — see $2"; FAIL=$((FAIL+1)); fi
}

for c in 126 78 0; do mkfake "$c"; done

O=$(run_doctor "$NEW" 126)
check "ARM1 positive control: doctor output reached the chat_sync branch" "$O" "chat_sync loaded" present
check "ARM1 chat_sync 126 names not permitted" "$O" "last exit was: 126 (not permitted)" present
check "ARM1 chat_sync 126 names Full Disk Access" "$O" "Full Disk Access" present
check "ARM1 chat_sync 126 does NOT print the EX_CONFIG hint" "$O" "points its out/err somewhere" absent
check "ARM1 scheduler 126 names TCC (text only the fix prints)" "$O" "lacks Full Disk Access" present

O=$(run_doctor "$NEW" 78)
check "ARM2 chat_sync 78 names EX_CONFIG" "$O" "last exit was: 78 (EX_CONFIG)" present
check "ARM2 chat_sync 78 names the log path rule" "$O" "~/Library/Logs" present
check "ARM2 chat_sync 78 does NOT name Full Disk Access" "$O" "add /bin/bash" absent
check "ARM2 scheduler 78 names EX_CONFIG" "$O" "EX_CONFIG: launchd refused the plist" present

O=$(run_doctor "$NEW" 0)
check "ARM3 CONTROL exit 0 reads clean" "$O" "last launchd exit clean" present
check "ARM3 CONTROL exit 0 prints no 126 hint" "$O" "(not permitted)" absent

if [ -f "$OLD" ]; then
  O=$(run_doctor "$OLD" 126)
  check "ARM4 NEGATIVE: the pre-fix doctor prints the 78 hint for a 126" "$O" "78/EX_CONFIG means the plist points" present
  check "ARM4 NEGATIVE: the pre-fix scheduler line lacks the TCC-specific text" "$O" "lacks Full Disk Access" absent
else
  echo "FAIL: ARM4 needs $OLD"; FAIL=$((FAIL+1))
fi

echo "RESULT: $PASS passed, $FAIL failed (work dir kept: $WORK)"
[ "$FAIL" -eq 0 ]
