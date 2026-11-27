#!/bin/bash
# tests/mutants.sh — proof that tests/run.sh CAN FAIL (2026-08-07_a-check-that-cannot-fail).
# For each named safety property it makes a scratch COPY of this lane, breaks that one property in the copy's
# nb_core.py, runs the copy's tests/run.sh, and requires (a) a non-zero exit and (b) a FAIL line carrying the
# test id that owns the property. A mutant the suite does not catch is printed as SURVIVED and fails this script.
# The real lane is never edited. Everything lives under the base (/private/tmp only). No rm.
#
#   tests/mutants.sh [base dir under /private/tmp]
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANE="$(cd -P "$HERE/.." && pwd)"
TREE="$(cd -P "$LANE/../.." && pwd)"
BASE="${1:-/private/tmp/nas-backup-tests}"
case "$BASE" in /private/tmp/*) ;; *) echo "mutants: REFUSED — the base must be under /private/tmp" >&2; exit 2 ;; esac
RUN="$BASE/mutants_$(date +%Y%m%d-%H%M%S)_$$"
mkdir -p "$RUN" || exit 2
PY=/opt/homebrew/bin/python3; [ -x "$PY" ] || PY=/usr/bin/python3
CAUGHT=0; SURVIVED=0

mutant() { # name  expected-test-id  old-text  new-text  [old-text new-text ...]
  # More than one pair when a property is held by more than one guard: a mutant that removes only one of two
  # independent guards is (rightly) not caught, and proves nothing about the tests.
  local name="$1" want="$2"; shift 2
  local copy="$RUN/$name/WEDNESDAY/2_Project_Files/nas-backup"
  mkdir -p "$copy/tests" "$RUN/$name/WEDNESDAY/2_Project_Files/fleet/cockpit" "$RUN/$name/base"
  cp "$LANE/nb_core.py" "$LANE/nb_common.sh" "$LANE/nas_backup.sh" "$LANE/nas_backup_nightly.sh" "$LANE/nas_backup_watch.sh" "$copy/"
  cp "$LANE/tests/run.sh" "$copy/tests/"
  cp "$TREE/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$RUN/$name/WEDNESDAY/2_Project_Files/fleet/cockpit/"
  if ! "$PY" -c 'import sys
p, pairs = sys.argv[1], sys.argv[2:]
s = open(p, encoding="utf-8").read()
for i in range(0, len(pairs), 2):
    old, new = pairs[i], pairs[i + 1]
    n = s.count(old)
    if n != 1:
        sys.stderr.write("mutation target found %d times (need exactly 1): %r\n" % (n, old)); sys.exit(1)
    s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)' "$copy/nb_core.py" "$@"; then
    SURVIVED=$((SURVIVED+1)); printf '  BROKEN    %-28s the mutation could not be applied (the code moved): fix this script\n' "$name"; return
  fi
  bash "$copy/tests/run.sh" "$RUN/$name/base" > "$RUN/$name/out.txt" 2>&1; local rc=$?
  local nfail; nfail="$(/usr/bin/grep -c -F '  FAIL  ' "$RUN/$name/out.txt")"
  if [ "$rc" -ne 0 ] && /usr/bin/grep -F '  FAIL  ' "$RUN/$name/out.txt" | /usr/bin/grep -q -F "$want"; then
    CAUGHT=$((CAUGHT+1)); printf '  CAUGHT    %-28s %2s FAIL line(s), including %s: %s\n' "$name" "$nfail" "$want" "$(/usr/bin/grep -F '  FAIL  ' "$RUN/$name/out.txt" | /usr/bin/grep -F "$want" | head -1 | cut -c9-110)"
  else
    SURVIVED=$((SURVIVED+1)); printf '  SURVIVED  %-28s exit %s, %s FAIL line(s), none for %s (output: %s)\n' "$name" "$rc" "$nfail" "$want" "$RUN/$name/out.txt"
  fi
}

echo "=== mutants — scratch copies under $RUN ==="
# control: the UNMUTATED copy must pass, or a CAUGHT below proves nothing
ctl="$RUN/control/WEDNESDAY/2_Project_Files/nas-backup"
mkdir -p "$ctl/tests" "$RUN/control/WEDNESDAY/2_Project_Files/fleet/cockpit" "$RUN/control/base"
cp "$LANE/nb_core.py" "$LANE/nb_common.sh" "$LANE/nas_backup.sh" "$LANE/nas_backup_nightly.sh" "$LANE/nas_backup_watch.sh" "$ctl/"
cp "$LANE/tests/run.sh" "$ctl/tests/"; cp "$TREE/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$RUN/control/WEDNESDAY/2_Project_Files/fleet/cockpit/"
bash "$ctl/tests/run.sh" "$RUN/control/base" > "$RUN/control/out.txt" 2>&1; CRC=$?
echo "  CONTROL   the unmutated copy: exit $CRC — $(tail -1 "$RUN/control/out.txt" | cut -c1-40)"
[ "$CRC" -eq 0 ] || { echo "mutants: the CONTROL failed; nothing below would mean anything" >&2; exit 1; }

# (rsync 3 treats --backup-dir as implying --backup, so removing --backup alone changes nothing: both go.)
mutant keeps-no-previous-version "T3 the PREVIOUS a.txt" \
  '"--backup",' '' \
  '"--backup-dir=" + bdir, ' ''
mutant secrets-folder-allowed "T4 no secret" \
  '("secret", ["4_Credentials", "3_Access_Keys", ".env",' '("secret", ["3_Access_Keys",'
mutant git-and-node-modules-allowed "T4 no secret" \
  '("git", [".git"]),' '("git", []),'
mutant other-seat-folders-allowed "T4 no secret" \
  '"other_seat_names": ["*[Tt]uesday*", "*TUESDAY*", "*[Ff]riday*", "*FRIDAY*"],
        "other_client_names": ["*[Dd]atasec*", "*DATASEC*"],' '"other_seat_names": ["*[Ff]riday*", "*FRIDAY*"],
        "other_client_names": ["*[Dd]atasec*", "*DATASEC*"],'
mutant mount-check-off "T5a NAS not in the mount table" \
  'return any(needle in ln for ln in mount_lines(ctx))' 'return True'
mutant case-check-off "T5c " \
  '    if name in names:
        return "exact"' '    if True:
        return "exact"'
mutant free-space-floor-off "T5d free space under the floor" \
  'if free < c["min_free_gib"]:' 'if False:'
mutant lock-ignored "T5e live lock" \
  '    except FileExistsError:
        ls = lock_status(ctx) or {}' '    except FileExistsError:
        return
        ls = lock_status(ctx) or {}'
mutant foreign-source-allowed "T5f'"' a source outside' \
  'if not under(s["src"], c["source_volume"]) or os.stat(s["src"]).st_dev != tree_dev:' 'if False:'
# (the allow-list is checked twice on purpose: when the conf is loaded and again when a destination is built.)
mutant allow-list-off "T5g destination in another client" \
  '            if s["client"] not in self.info["clients"]:' '            if False:' \
  '        if client not in self.info["clients"]:' '        if False:'
mutant window-check-off "T5i a real run at 14:00" \
  'if not inw and not out_of_sequence:' 'if False:'
mutant hold-ignored "T5j HOLD file present" \
  'if mode == "run" and os.path.exists(ctx.hold_file):' 'if False:'
mutant deletion-flag-allowed "T5k every deletion-capable" \
  'if a == bad or a.startswith(bad + "=") or a.startswith("--delete") or a.startswith("--del"):' 'if False:'
mutant file-ceiling-off "T5m a set above max_files" \
  'if len(src["files"]) > ctx.conf["max_files"]:' 'if False:'
mutant deleting-line-ignored "T6 exit 9" \
  'if low.startswith("*deleting") or low.startswith("deleting "):' 'if False:'
mutant catches-nothing-up "T7 a second fire the same night" \
  'if lg and lg["time"] >= o:' 'if False:'
mutant runs-outside-window "T7 day 3, 14:00" \
  '    if not inw:
        if c["late_fire"] == "run":' '    if False:
        if c["late_fire"] == "run":'
mutant flag-every-boot "T8 across five more checks" \
  'same_gap = flag.get("gap_key") == gap_key' 'same_gap = False'
mutant flag-never "T8 night 3" \
  'overdue = hours >= FLAG_AFTER_HOURS' 'overdue = False'
mutant size-check-off "T3 same-size change" \
  '            if ix is None or tuple(ix) != tuple(sv):' '            if False:'

echo
echo "=== $CAUGHT mutants caught, $SURVIVED survived or broken — outputs kept under $RUN ==="
[ "$SURVIVED" -eq 0 ]
