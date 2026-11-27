#!/bin/bash
# E — the five proposals, applied ONLY to scratch copies. launchctl is never called: a stub named launchctl sits
# first on PATH and logs its arguments; HOME points into scratch so no real LaunchAgents folder is touched.
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-nasbackup
REAL=/Volumes/DevMASTER/WEDNESDAY
E="$S/e_$$"; PY=/opt/homebrew/bin/python3
say() { printf '%s\n' "$*"; }
mktree() { # NAME (WEDNESDAY|TUESDAY)
  local t="$E/$1"; mkdir -p "$t/2_Project_Files/scheduler/jobs" "$t/2_Project_Files/fleet/cockpit" "$E/home/Library/LaunchAgents" "$E/bin"
  cp -R "$S/copy/WEDNESDAY/2_Project_Files/nas-backup" "$t/2_Project_Files/nas-backup"
  cp "$REAL/2_Project_Files/fleet/cockpit/seat_resolve.sh" "$t/2_Project_Files/fleet/cockpit/"
  cp "$REAL/2_Project_Files/scheduler/install_all_jobs.sh" "$t/2_Project_Files/scheduler/install_all_jobs.sh"
  cp "$REAL/2_Project_Files/scheduler/jobs/naspush.plist.template" "$t/2_Project_Files/scheduler/jobs/"
  echo "$t"; }
mkdir -p "$E/bin"; cat > "$E/bin/launchctl" <<'STUB'
#!/bin/bash
echo "launchctl-STUB $*" >> "$LAUNCHCTL_LOG"
case "$1" in list) exit 0;; print) exit 1;; load) /usr/bin/plutil -lint "$2" >> "$LAUNCHCTL_LOG" 2>&1 || exit 1; exit 0;; *) exit 0;; esac
STUB
chmod +x "$E/bin/launchctl"; export LAUNCHCTL_LOG="$E/launchctl.log"; : > "$LAUNCHCTL_LOG"
inst() { ( export HOME="$E/home" PATH="$E/bin:/usr/bin:/bin:/usr/sbin:/sbin"; env -u WED_AGENT bash "$1/2_Project_Files/scheduler/install_all_jobs.sh" ${2:-} 2>&1 ); }
apply_step2() { "$PY" - "$1/2_Project_Files/scheduler/install_all_jobs.sh" <<'PYEOF'
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def once(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:60]); s = s.replace(old, new)
hold = '''  # nasbackup (WED-170, Kam 2026-11-27): the copy-only nightly backup. Held per seat by nas-backup/HOLD_<seat>; lifting it is the coordinator's word on Kam's instruction.
  if [ "$job" = "nasbackup" ] && [ -e "$PROJECT_DIR/2_Project_Files/nas-backup/HOLD_$SEAT" ]; then echo "skip $job — HELD (2_Project_Files/nas-backup/HOLD_$SEAT)"; continue; fi
  # ... and never for a seat whose configuration is not confirmed on its own machine.
  if [ "$job" = "nasbackup" ] && ! /usr/bin/grep -q '^status=confirmed$' "$PROJECT_DIR/2_Project_Files/nas-backup/seats/$SEAT.conf"; then echo "skip $job — seats/$SEAT.conf is not confirmed"; continue; fi
'''
once('  label="com.$SEAT.$job"\n', hold + '  label="com.$SEAT.$job"\n')
case = '''  case "$SEAT" in
    wednesday) NBH0=0; NBM0=30; NBH1=1; NBM1=40; NBH2=2; NBM2=50; NBH3=4; NBM3=0  ;;
    tuesday)   NBH0=2; NBM0=30; NBH1=3; NBM1=20; NBH2=4; NBM2=10; NBH3=5; NBM3=0  ;;
    friday)    NBH0=4; NBM0=30; NBH1=5; NBM1=40; NBH2=6; NBM2=50; NBH3=8; NBM3=10 ;;
  esac
'''
once('  rendered="$(sed ', case + '  rendered="$(sed ')
once('-e "s|@NASMIN@|$NASMIN|g" "$t")"', '-e "s|@NASMIN@|$NASMIN|g" -e "s|@NBH0@|$NBH0|g" -e "s|@NBM0@|$NBM0|g" -e "s|@NBH1@|$NBH1|g" -e "s|@NBM1@|$NBM1|g" -e "s|@NBH2@|$NBH2|g" -e "s|@NBM2@|$NBM2|g" -e "s|@NBH3@|$NBH3|g" -e "s|@NBM3@|$NBM3|g" "$t")"')
once('    printf "  installed %-16s (%s)\\n" "$job" "$label"; installed=$((installed+1))\n', '    printf "  installed %-16s (%s)\\n" "$job" "$label"; installed=$((installed+1))\n    [ "$job" = "nasbackup" ] && bash "$PROJECT_DIR/2_Project_Files/nas-backup/nas_backup_watch.sh" --mark-armed\n')
open(p, "w", encoding="utf-8").write(s); print("step 2 (a)(b)(c) applied: each anchor found exactly once")
PYEOF
}
show_plist() { local f="$E/home/Library/LaunchAgents/com.$1.nasbackup.plist"; if [ -f "$f" ]; then say "   plist written: yes ; plutil -lint: $(/usr/bin/plutil -lint "$f" 2>&1 | sed "s|$E/||") ; fire times: $(/usr/bin/grep -o -E '<integer>[^<]*</integer>' "$f" | sed -E 's/<[^>]*>//g' | paste -sd' ' -) ; unrendered placeholders: $(/usr/bin/grep -c '@' "$f")"; else say "   plist written: NO"; fi; }

say "### E1 install_all_jobs: Step 1 (copy the template) done BEFORE Step 2 (the edits), as the proposal orders them, HOLD still present"
W="$(mktree WEDNESDAY)"; cp -n "$W/2_Project_Files/nas-backup/jobs/nasbackup.plist.template" "$W/2_Project_Files/scheduler/jobs/"
inst "$W" | /usr/bin/grep -i -E 'nasbackup|jobs for' | sed 's/^/   /'; show_plist wednesday
say "   launchctl calls the UNMODIFIED installer made for nasbackup: $(/usr/bin/grep -c 'nasbackup' "$LAUNCHCTL_LOG") ; HOLD_wednesday present: $([ -e "$W/2_Project_Files/nas-backup/HOLD_wednesday" ] && echo yes)"
/usr/bin/grep -i 'nasbackup' "$LAUNCHCTL_LOG" | sed "s|$E/||g" | sed 's/^/   /'
inst "$W" --check | /usr/bin/grep -i -E 'nasbackup|jobs for' | sed 's/^/   --check: /'

say; say "### E2 Step 2 applied; HOLD present"
rm -rf "$E/home/Library/LaunchAgents"; mkdir -p "$E/home/Library/LaunchAgents"; : > "$LAUNCHCTL_LOG"
apply_step2 "$W"; bash -n "$W/2_Project_Files/scheduler/install_all_jobs.sh" && say "   bash -n: syntax ok"
inst "$W" | /usr/bin/grep -i -E 'nasbackup|naspush|jobs for' | sed 's/^/   /'; show_plist wednesday
inst "$W" --check | /usr/bin/grep -i -E 'nasbackup|jobs for' | sed 's/^/   --check: /'
say; say "### E3 HOLD moved aside, wednesday.conf confirmed"
mv -n "$W/2_Project_Files/nas-backup/HOLD_wednesday" "$W/2_Project_Files/nas-backup/HOLD_wednesday.lifted-test"
inst "$W" | /usr/bin/grep -i -E 'nasbackup|armed|jobs for' | sed 's/^/   /'; show_plist wednesday
say "   state after: armed_at=$($PY -c 'import json,sys; print(json.load(open(sys.argv[1])).get("armed_at"))' "$W/2_Project_Files/nas-backup/state/wednesday.json" 2>&1)"
say "   the naspush template still renders (regression check): $(/usr/bin/plutil -lint "$E/home/Library/LaunchAgents/com.wednesday.naspush.plist" 2>&1 | sed "s|$E/||")"
say; say "### E4 the same modified installer on a TUESDAY tree: (i) hold present (ii) hold lifted, conf still unconfirmed (iii) confirmed"
T2="$(mktree TUESDAY)"; cp "$W/2_Project_Files/scheduler/install_all_jobs.sh" "$T2/2_Project_Files/scheduler/"; cp -n "$T2/2_Project_Files/nas-backup/jobs/nasbackup.plist.template" "$T2/2_Project_Files/scheduler/jobs/"
inst "$T2" | /usr/bin/grep -i -E 'nasbackup' | sed 's/^/   (i)   /'
mv -n "$T2/2_Project_Files/nas-backup/HOLD_tuesday" "$T2/2_Project_Files/nas-backup/HOLD_tuesday.lifted-test"
inst "$T2" | /usr/bin/grep -i -E 'nasbackup' | sed 's/^/   (ii)  /'
sed -i '' 's/^status=unconfirmed/status=confirmed/' "$T2/2_Project_Files/nas-backup/seats/tuesday.conf"
inst "$T2" | /usr/bin/grep -i -E 'nasbackup|armed' | sed 's/^/   (iii) /'; show_plist tuesday
say "   wednesday and tuesday plists rendered on ONE machine/home: $(ls "$E/home/Library/LaunchAgents" | /usr/bin/grep -c nasbackup.plist\$) (labels differ: $(ls "$E/home/Library/LaunchAgents" | /usr/bin/grep 'nasbackup.plist$' | paste -sd' ' -))"

say; say "### E5 launcher proposal applied LITERALLY (the launcher runs under set -u; it has no PREFLIGHT_LOG variable)"
say "   occurrences of PREFLIGHT_LOG in the real launcher: $(/usr/bin/grep -c 'PREFLIGHT_LOG' "$REAL/Launch_Wednesday.command") ; (control) occurrences of _PF_OUT: $(/usr/bin/grep -c '_PF_OUT' "$REAL/Launch_Wednesday.command") ; set -u lines: $(/usr/bin/grep -c '^set -u' "$REAL/Launch_Wednesday.command")"
cat > "$E/launcher_harness.sh" <<HEOF
#!/bin/bash
set -u
PROJECT_DIR="$W"
echo "before the proposed block"
if [ -x "\$PROJECT_DIR/2_Project_Files/nas-backup/nas_backup_watch.sh" ]; then
  bash "\$PROJECT_DIR/2_Project_Files/nas-backup/nas_backup_watch.sh" --flag 2>&1 | tee -a "\$PREFLIGHT_LOG"
fi
echo "AFTER the proposed block: the boot continues"
HEOF
env -u WED_AGENT /bin/bash "$E/launcher_harness.sh" > "$E/launcher_harness.out" 2>&1; say "   harness exit=$? ; reached the line after the block: $(/usr/bin/grep -c 'AFTER the proposed block' "$E/launcher_harness.out")"; sed "s|$E/||g" "$E/launcher_harness.out" | cut -c1-200 | sed 's/^/   | /'
sed 's/"\$PREFLIGHT_LOG"/"$_PF_OUT2"/; s/^set -u$/set -u; _PF_OUT2="$(mktemp -t qa_pf.XXXXXX)"/' "$E/launcher_harness.sh" > "$E/launcher_harness2.sh"
env -u WED_AGENT /bin/bash "$E/launcher_harness2.sh" > "$E/launcher_harness2.out" 2>&1; say "   with a real file name substituted: exit=$? ; reached the line after: $(/usr/bin/grep -c 'AFTER the proposed block' "$E/launcher_harness2.out")"
say "   WED_AGENT=tuesday exported (Launch_Tuesday.command does this) but the tree is WEDNESDAY: $(WED_AGENT=tuesday /bin/bash "$E/launcher_harness2.sh" 2>&1 | sed -n 2p | cut -c1-150)"

say; say "### E6 doctor proposal: the block run in a harness with doctor's own shell options and helpers (launchctl stubbed)"
"$PY" - "$S/copy/WEDNESDAY/2_Project_Files/nas-backup/proposed/doctor.proposed.md" "$E/doctor_block.sh" <<'PYEOF'
import sys
t = open(sys.argv[1], encoding="utf-8").read(); a = t.index("```\n") + 4; b = t.index("\n```", a)
open(sys.argv[2], "w", encoding="utf-8").write(t[a:b] + "\n"); print("   block extracted: %d lines" % (t[a:b].count("\n") + 1))
PYEOF
dharness() { # PROJECT_DIR  _DOC_AGENT  launchctl-mode
  cat > "$E/doc_h.sh" <<HEOF
#!/bin/bash
set -uo pipefail
QUIET="--quiet"; HARD_FAIL=0; WARNS=0
ok()   { [ "\$QUIET" = "--quiet" ] || printf "  ✓ %s\n" "\$1"; }
warn() { printf "  ⚠ %-38s %s\n" "\$1" "\${2:-}"; WARNS=\$((WARNS+1)); }
launchctl() { case "$3" in notloaded) return 1;; exit7) echo "	last exit code = 7"; return 0;; esac; }
PROJECT_DIR="$1"; _DOC_AGENT="$2"
. "$E/doctor_block.sh"
echo "  [harness] reached the end; WARNS=\$WARNS"
HEOF
  env -u WED_AGENT /bin/bash "$E/doc_h.sh" 2>&1 | sed "s|$E/||g" | cut -c1-230; }
setstate() { "$PY" -c 'import json,sys,time
p, age = sys.argv[1], float(sys.argv[2]); t = time.time() - age*3600
json.dump({"schema":1,"seat":"wednesday","armed_at":None,"last_good":{"time":t,"time_local":time.strftime("%Y-%m-%d %H:%M:%S %Z",time.localtime(t)),"status":"good","reason":"x","counts":{}},"last_attempt":None,"last_fire":None,"recent_attempts":[],"flag":None}, open(p,"w"))' "$W/2_Project_Files/nas-backup/state/wednesday.json" "$1"; }
bash -n "$E/doctor_block.sh" && say "   bash -n: syntax ok"
"$PY" - "$REAL/2_Project_Files/doctor.sh" "$E/doctor_block.sh" "$E/doctor_patched.sh" <<'PYEOF'
import sys
d = open(sys.argv[1], encoding="utf-8").read(); b = open(sys.argv[2], encoding="utf-8").read()
anchor = "# --- Executable bits on on-drive scripts (added 2026-08-06) ---"
assert d.count(anchor) == 1; open(sys.argv[3], "w", encoding="utf-8").write(d.replace(anchor, b + "\n" + anchor)); print("   block inserted after the staleness block into a scratch copy of doctor.sh (anchor found once)")
PYEOF
bash -n "$E/doctor_patched.sh" && say "   bash -n on the patched scratch doctor.sh: syntax ok (the patched doctor itself was NOT run)"
mv -n "$W/2_Project_Files/nas-backup/HOLD_wednesday.lifted-test" "$W/2_Project_Files/nas-backup/HOLD_wednesday"
say "   (a) hold present:";                         dharness "$W" wednesday notloaded
mv -n "$W/2_Project_Files/nas-backup/HOLD_wednesday" "$W/2_Project_Files/nas-backup/HOLD_wednesday.lifted-test"
setstate 5;  say "   (b) hold lifted, last good 5 h ago, job not loaded:";  QUIETX=1 dharness "$W" wednesday notloaded
setstate 80; say "   (c) last good 80 h ago, job loaded with last exit 7:"; dharness "$W" wednesday exit7
echo "{broken" > "$W/2_Project_Files/nas-backup/state/wednesday.json"; say "   (d) corrupt state file:"; dharness "$W" wednesday notloaded
setstate 80; say "   (e) doctor's _DOC_AGENT=tuesday (WED_AGENT exported by Launch_Tuesday) on a WEDNESDAY tree:"; dharness "$W" tuesday notloaded
say "   (f) on a TUESDAY tree with WED_AGENT unset, doctor's own default gives _DOC_AGENT=wednesday (doctor.sh line 83): block looks for HOLD_wednesday"; dharness "$T2" wednesday notloaded

say; say "### E7 PORTABILITY proposal: 'the last one today is 30', proposed heading '## 31.'"
say "   headings '## 31.' already in the real PORTABILITY.md: $(/usr/bin/grep -c '^## 31\.' "$REAL/PORTABILITY.md") ; (control) '## 30.': $(/usr/bin/grep -c '^## 30\.' "$REAL/PORTABILITY.md") ; highest: $(/usr/bin/grep -o -E '^## [0-9]+' "$REAL/PORTABILITY.md" | sort -k2 -n | tail -1)"

say; say "### F the plist template rendered for all three seats (sed as the proposal gives it)"
for seat in wednesday tuesday friday; do
  case "$seat" in wednesday) NBH0=0; NBM0=30; NBH1=1; NBM1=40; NBH2=2; NBM2=50; NBH3=4; NBM3=0;; tuesday) NBH0=2; NBM0=30; NBH1=3; NBM1=20; NBH2=4; NBM2=10; NBH3=5; NBM3=0;; friday) NBH0=4; NBM0=30; NBH1=5; NBM1=40; NBH2=6; NBM2=50; NBH3=8; NBM3=10;; esac
  f="$E/render_$seat.plist"; sed -e "s|@PROJECT_DIR@|/Volumes/X/$seat|g" -e "s|@SEAT@|$seat|g" -e "s|@HOME@|/Users/x|g" -e "s|@NBH0@|$NBH0|g" -e "s|@NBM0@|$NBM0|g" -e "s|@NBH1@|$NBH1|g" -e "s|@NBM1@|$NBM1|g" -e "s|@NBH2@|$NBH2|g" -e "s|@NBM2@|$NBM2|g" -e "s|@NBH3@|$NBH3|g" -e "s|@NBM3@|$NBM3|g" "$S/copy/WEDNESDAY/2_Project_Files/nas-backup/jobs/nasbackup.plist.template" > "$f"
  conf_fire="$(/usr/bin/grep '^fire=' "$S/copy/WEDNESDAY/2_Project_Files/nas-backup/seats/$seat.conf")"; conf_win="$(/usr/bin/grep '^window_hours=' "$S/copy/WEDNESDAY/2_Project_Files/nas-backup/seats/$seat.conf")"
  say "   $seat: $(/usr/bin/plutil -lint "$f" | sed 's|.*: ||') ; fires $(/usr/bin/plutil -extract StartCalendarInterval json -o - "$f" | tr -d '\n') ; conf $conf_fire $conf_win ; '@' left: $(/usr/bin/grep -v '^ *@\|<!--' "$f" | sed -n '15,$p' | /usr/bin/grep -c '@') ; RunAtLoad: $(/usr/bin/plutil -extract RunAtLoad raw "$f") ; keys: $(/usr/bin/plutil -p "$f" | /usr/bin/grep -c -E 'KeepAlive|WakeSystem')"
done
