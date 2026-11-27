#!/bin/bash
# N8 — the proposals against scratch COPIES of their real targets: the installer + plist template (as ONE change, in
# every order), doctor.sh (the sourced block), PORTABILITY. launchctl is a STUB that only logs; HOME is a scratch
# folder. No real launchctl verb is run and nothing is installed. Fresh checker.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib2.sh"
REAL=/Volumes/DevMASTER/WEDNESDAY
E="$S/proposals_$$"; mkdir -p "$E/bin" "$E/home"
cat > "$E/bin/launchctl" <<EOF
#!/bin/bash
echo "launchctl \$*" >> "$E/launchctl.calls"
case "\$1" in list) cat "$E/loaded.txt" 2>/dev/null; exit 0;; load) /usr/bin/plutil -lint "\$2" >/dev/null 2>&1 || { echo "STUB: launchd would refuse an invalid plist" >&2; exit 1; }; printf -- '-\t0\t%s\n' "\$(basename "\$2" .plist)" >> "$E/loaded.txt"; exit 0;; *) exit 0;; esac
EOF
chmod +x "$E/bin/launchctl"
mktree() { # seat-dir  variant(installer: orig|edited ; template: yes|no)
  local t="$E/$3/$1/2_Project_Files"; mkdir -p "$t/scheduler/jobs" "$t/nas-backup" "$t/fleet/cockpit" "$t/tools" "$E/home_$3/Library/LaunchAgents"
  cp "$REAL/2_Project_Files/scheduler/install_all_jobs.sh" "$t/scheduler/"; cp "$REAL/2_Project_Files/scheduler/jobs/naspush.plist.template" "$t/scheduler/jobs/"
  cp "$LANE"/nb_core.py "$LANE"/nb_common.sh "$LANE"/nas_backup*.sh "$t/nas-backup/"; cp -R "$LANE/seats" "$LANE/jobs" "$t/nas-backup/"; cp "$LANE"/HOLD_* "$t/nas-backup/"
  cp "$REAL/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$t/fleet/cockpit/"; cp "$REAL/2_Project_Files/tools/seat_note.sh" "$t/tools/"
  [ "$4" = yes ] && cp -n "$t/nas-backup/jobs/nasbackup.plist.template" "$t/scheduler/jobs/nasbackup.plist.template"
  if [ "$2" = edited ]; then /opt/homebrew/bin/python3 - "$t/scheduler/install_all_jobs.sh" <<'PYEOF'
import sys
p = sys.argv[1]; s = open(p).read()
anchor = '  label="com.$SEAT.$job"\n'
assert s.count(anchor) == 1
add = '''  # nasbackup (WED-170, Kam 2026-11-27): the copy-only nightly backup. Held per seat by nas-backup/HOLD_<seat>; only seats with a confirmed scope file get the job.
  if [ "$job" = "nasbackup" ] && [ -e "$PROJECT_DIR/2_Project_Files/nas-backup/HOLD_$SEAT" ]; then echo "skip $job — HELD (2_Project_Files/nas-backup/HOLD_$SEAT)"; continue; fi
  if [ "$job" = "nasbackup" ] && ! /usr/bin/grep -q '^status=confirmed$' "$PROJECT_DIR/2_Project_Files/nas-backup/seats/$SEAT.conf" 2>/dev/null; then echo "skip $job — no confirmed nas-backup/seats/$SEAT.conf"; continue; fi
'''
open(p, "w").write(s.replace(anchor, add + anchor))
PYEOF
  fi; echo "$t"; }
inst() { # tree-2pf  home  [args]
  local t="$1" h="$2"; shift 2; : > "$E/launchctl.calls"; env -u WED_AGENT HOME="$h" PATH="$E/bin:/usr/bin:/bin:/usr/sbin:/sbin" bash "$t/scheduler/install_all_jobs.sh" "$@" 2>&1 | /usr/bin/grep -i -E 'nasbackup|jobs for seat' | tr '\n' '~'; }

say "### E1 every ORDER of the one change, seat held (HOLD_wednesday present) — is anything loaded, is it valid, and does what it calls honour the hold?"
for v in "orig yes template-only(installer-not-yet-edited)" "edited no installer-lines-only(no-template)" "edited yes both"; do set -- $v; : > "$E/loaded.txt"
  t="$(mktree WEDNESDAY "$1" "o_$1_$2" "$2")"; h="$E/home_o_$1_$2"
  say "-- $3: $(inst "$t" "$h")"
  p="$h/Library/LaunchAgents/com.wednesday.nasbackup.plist"
  if [ -f "$p" ]; then say "   plist written: lint=[$(/usr/bin/plutil -lint "$p" 2>&1 | sed "s|$h||")] ; placeholders left: $(/usr/bin/grep -o -c '@[A-Z_0-9]*@' "$p") ; load calls: $(/usr/bin/grep -c 'launchctl load .*nasbackup' "$E/launchctl.calls")"
    prog="$(/usr/bin/plutil -extract ProgramArguments.1 raw "$p")"; out="$(env -u NB_TEST_ROOT WED_AGENT=wednesday bash -c 'echo "would run: $0"' "$prog")"
    say "   what launchd would call: ${prog#$E/} ; it exists: $([ -f "$prog" ] && echo yes || echo NO) ; fires per day: $(/usr/bin/grep -o -c '<key>Hour</key>' "$p") ; RunAtLoad: $(/usr/bin/plutil -extract RunAtLoad raw "$p")"
  else say "   no plist written for nasbackup"; fi; done
say "   (the hold itself, on the script launchd calls, under a HOLD: proven in test mode below, since outside test mode the copy would look at the real NAS path, which I never run)"
fixture E1h; echo held > "$T/lane/HOLD_wednesday"; nightly --now "$(at 0 0 31)" > "$T/out/n.txt" 2>&1; say "   nightly script under HOLD: rc=$? ; $(head -1 "$T/out/n.txt" | cut -c1-80) ; STARTED markers on the fake NAS: $(find "$T/nas" -name '*STARTED*' | wc -l | tr -d ' ')"
for hm in "0 31" "1 30" "2 30" "14 30"; do nb --run --now "$(at 0 $hm)" --out-of-sequence card-abcdef > "$T/out/h.txt" 2>&1; printf '   --run --out-of-sequence under HOLD at %s: rc=%s\n' "$hm" "$?"; done | sort | uniq -c
nb --run --now "$(at 0 1 0)" --accept-shrink card-abcdef > "$T/out/h.txt" 2>&1; say "   --run --accept-shrink under HOLD: rc=$?"
say "   HOLD spelled in another case (hold_wednesday / HOLD_WEDNESDAY) on this case-insensitive scratch volume: $(mv "$T/lane/HOLD_wednesday" "$T/lane/hold_tmp"; mv "$T/lane/hold_tmp" "$T/lane/HOLD_WEDNESDAY"; nb --run --now "$(at 0 1 0)" > "$T/out/h2.txt" 2>&1; echo "rc=$?") (the real drive is case-SENSITIVE: there a differently-cased hold file would NOT hold; not testable here)"

say; say "### E2 the same on a TUESDAY tree (no scope in the lane) with the template present"
for v in "orig yes" "edited yes"; do set -- $v; : > "$E/loaded.txt"; t="$(mktree TUESDAY "$1" "t_$1" "$2")"; h="$E/home_t_$1"
  say "-- installer $1: $(inst "$t" "$h") | plist: $([ -f "$h/Library/LaunchAgents/com.tuesday.nasbackup.plist" ] && echo WRITTEN || echo none)"; done
fixture E2t; mkdir -p "$T/vol/TUESDAY"; env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/TUESDAY" "$LANE/nas_backup_nightly.sh" > "$T/out/t.txt" 2>&1; say "   what that job would do each hour on her machine: rc=$? ($(head -1 "$T/out/t.txt" | cut -c1-100))"

say; say "### E3 hold lifted and conf confirmed, both parts in: installed, valid, re-run is idempotent, --check agrees"
: > "$E/loaded.txt"; t="$(mktree WEDNESDAY edited e3 yes)"; h="$E/home_e3"; mv "$t/nas-backup/HOLD_wednesday" "$t/nas-backup/HOLD_wednesday.lifted"
say "install: $(inst "$t" "$h")"; say "again:   $(inst "$t" "$h")"; say "--check: $(inst "$t" "$h" --check)"
p="$h/Library/LaunchAgents/com.wednesday.nasbackup.plist"; say "lint: $(/usr/bin/plutil -lint "$p" | sed "s|$h||") ; hours: $(/usr/bin/plutil -extract StartCalendarInterval json -o - "$p" | /opt/homebrew/bin/python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d), sorted(set(x["Minute"] for x in d)), sorted(x["Hour"] for x in d)[:3], "...")')"
say "naspush still renders beside it: $([ -f "$h/Library/LaunchAgents/com.wednesday.naspush.plist" ] && /usr/bin/plutil -lint "$h/Library/LaunchAgents/com.wednesday.naspush.plist" | sed "s|$h||")"

say; say "### E4 the schedule: 24 fires a day at minute 30; which fires can START a backup, per seat window (from the conf; Tuesday's and Friday's are proposals)"
fixture E4; for spec in "wednesday 00:30 5" "tuesday 02:30 3" "friday 04:30 5"; do set -- $spec; sed -i '' -e "s/^fire=.*/fire=$2/" -e "s/^window_hours=.*/window_hours=$3/" "$T/lane/seats/wednesday.conf"
  runs=""; for h in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23; do d="$(nightly --decide-only --now "$(at 0 $h 30)" 2>&1 | head -1)"; case "$d" in *": RUN:"*) runs="$runs $h:30";; esac; done
  say "   window of $1 ($2 for $3 h): fires that would start a backup when none is on record:$runs"; done
say "   after sleep: launchd runs ONE coalesced fire on wake. Decision for a wake at 07:10 with last night missed (Wednesday window): $(sed -i '' -e 's/^fire=.*/fire=00:30/' -e 's/^window_hours=.*/window_hours=5/' "$T/lane/seats/wednesday.conf"; nightly --decide-only --now "$(at 0 7 10)" 2>&1 | head -1 | cut -c1-150)"
say "   daylight saving, Australia/Sydney: spring forward 2027-10-03 (02:00 -> 03:00), fall back 2027-04-04 (03:00 -> 02:00), fire 00:30 for 5 h:"
for spec in "2027 10 3 2 30" "2027 10 3 5 29" "2027 10 3 5 31" "2027 4 4 2 30" "2027 4 4 5 29" "2027 4 4 5 31"; do set -- $spec; ep="$(TZ=Australia/Sydney /opt/homebrew/bin/python3 -c 'import datetime,sys; a=[int(x) for x in sys.argv[1:]]; print(int(datetime.datetime(*a).timestamp()))' "$@")"
  printf '      %s-%02d-%02d %02d:%02d wall -> %s\n' "$1" "$2" "$3" "$4" "$5" "$(TZ=Australia/Sydney env -u WED_AGENT NB_TEST_ROOT="$T" "$PY" "$LANE/nb_core.py" window --seat wednesday --tree "$T/vol/WEDNESDAY" --now "$ep" 2>&1 | cut -c1-110)"; done

say; say "### E5 doctor.sh: the proposed line applied to a scratch COPY of the real doctor.sh (not run whole: it probes this machine); syntax, placement, name clashes"
D="$E/doctor.sh"; cp "$REAL/2_Project_Files/doctor.sh" "$D"
/opt/homebrew/bin/python3 - "$D" <<'PYEOF'
import sys, re
p = sys.argv[1]; s = open(p).read().split("\n")
idx = [i for i, l in enumerate(s) if l.startswith("# --- NAS replica staleness")]
assert len(idx) == 1
j = idx[0] + 1
while not (s[j].startswith("# ---") or s[j].startswith("# ===")) : j += 1     # the next block header
ins = ['# --- Nightly copy-only NAS backup (WED-170, Kam 2026-11-27): the three-day flag\'s channel to a seat ---',
       '[ -f "$PROJECT_DIR/2_Project_Files/nas-backup/proposed/doctor_nasbackup_block.sh" ] && . "$PROJECT_DIR/2_Project_Files/nas-backup/proposed/doctor_nasbackup_block.sh"', '']
print("inserted before line %d: %s" % (j + 1, s[j][:70]))
open(p, "w").write("\n".join(s[:j] + ins + s[j:]))
PYEOF
say "bash -n on the patched copy: rc=$(bash -n "$D" 2>&1; echo $?)"
say "names the block and the two files it sources define, that doctor.sh ALSO uses (a clash would change doctor's behaviour after the block):"
for name in SEAT TREE_SEAT NB_DIR COORD_LEGACY_NAME SEAT_NOTE_SEAT SEAT_NOTE_REL SEAT_NOTE_DIR SEAT_NOTE_ERR _nb_seat _nb_lane _nb_now _nb_mark _nb_out _nb_rc _nb_line seat_resolve seat_from_tree_name coord_pane_id seat_note_dir; do printf '   %-22s uses in the real doctor.sh: %s\n' "$name" "$(/usr/bin/grep -c -E "(^|[^A-Za-z0-9_])\\\$?\{?$name([^A-Za-z0-9_]|\$)" "$REAL/2_Project_Files/doctor.sh")"; done
say "   control for that count: uses of HARD_FAIL in the real doctor.sh: $(/usr/bin/grep -c -E '(^|[^A-Za-z0-9_])\$?\{?HARD_FAIL([^A-Za-z0-9_]|$)' "$REAL/2_Project_Files/doctor.sh")"
say "the launcher: lines that make a HARD preflight failure NOT stop a rotation (read-only grep of the real launcher):"
/usr/bin/grep -n -E 'SEAT_ROTATION|PREFLIGHT_HARD=|_PF_RC=0' "$REAL/Launch_Wednesday.command" | cut -c1-150 | sed 's/^/   /'
say "   every unattended caller sets it: $(/usr/bin/grep -n 'SEAT_ROTATION=' "$REAL/2_Project_Files/fleet/cockpit/wednesday_rotate.sh" | cut -c1-140)"

say; say "### E6 PORTABILITY: the proposal says NN; the real file's last numbered sections"
/usr/bin/grep -n -E '^## [0-9]+[a-z]?\.' "$REAL/PORTABILITY.md" | tail -4 | cut -c1-110 | sed 's/^/   /'
say "   'NN' placeholders in the proposal: $(/usr/bin/grep -c -E '## NN\.' "$LANE/proposed/PORTABILITY.proposed.md") ; hard-coded section numbers proposed: $(/usr/bin/grep -c -E '^## [0-9]+\.' "$LANE/proposed/PORTABILITY.proposed.md")"
