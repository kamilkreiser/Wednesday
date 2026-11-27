#!/bin/bash
# G — destination-escape attempts, odd names, every engine invocation and destructive verb in the lane (read-only
# greps of the REAL lane), real-branch mount-table parsing (pure functions only; nothing is run against the NAS),
# the seat's STATUS figures against its own evidence files.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
RL=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }

say "### G1 set= lines that try to land OUTSIDE <client>/<Seat>/nightly-backup/current/"
fixture G1; b="$(find "$T/nas" | sort | shasum | cut -c1-12)"
for line in "set=General|../../escape|$T/vol/WEDNESDAY/sub" "set=General|a/../../../b|$T/vol/WEDNESDAY/sub" "set=General|/abs|$T/vol/WEDNESDAY/sub" "set=General|.|$T/vol/WEDNESDAY/sub" "set=General/../Datasec|x|$T/vol/WEDNESDAY/sub" "set=Datasec|x|$T/vol/WEDNESDAY/sub" "set=general|x|$T/vol/WEDNESDAY/sub" "set=General|wednesday|$T/vol/WEDNESDAY/sub" "set=|x|$T/vol/WEDNESDAY/sub" "set=General|x|relative/path"; do
  write_conf "$line"; rc=$(run "$(at 0 1 0)" e$RANDOM); printf 'rc=%s  nas tree changed: %s  [%s]\n' "$rc" "$([ "$(find "$T/nas" | sort | shasum | cut -c1-12)" = "$b" ] && echo no || echo YES)" "$(echo "$line" | sed "s|$T/||")"
done
write_conf "set=General|ok/nested|$T/vol/WEDNESDAY/sub"; rc=$(run "$(at 0 1 0)" ok); say "CONTROL a legal extra set: rc=$rc ; arrived: $(find "$T/nas" -path '*current/ok/nested/b.txt' | wc -l | tr -d ' ')"

say; say "### G2 odd file names (newline, leading dash, glob characters, trailing space, quotes, emoji, 240-char name, deep path)"
fixture G2
"$PY" - "$T/vol/WEDNESDAY" <<'PYEOF'
import os, sys
d = sys.argv[1]
names = ["line\nbreak.txt", "-rf", "--delete", "star*.txt", "q?.txt", "[b]racket.txt", "trail space ", "quote'\".txt", "back\\slash.txt", "tab\there.txt", "\U0001F600 emoji.txt", "n" * 240, "semi;colon &amp.txt", "$(echo x).txt", "#recycle-not/x.txt", "._not-appledouble-dir/x.txt"]
for n in names:
    p = os.path.join(d, "odd", n); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write("ODD " + repr(n) + "\n")
deep = os.path.join(d, "odd", *(["d" * 40] * 18)); os.makedirs(deep); open(os.path.join(deep, "deep.txt"), "w").write("deep\n")
print("planted %d odd names + 1 deep path (%d chars)" % (len(names), len(deep)))
PYEOF
rc=$(run "$(at 0 1 0)" r1); say "rc=$rc ; $(/usr/bin/grep -c 'GOOD:' "$T/out/r1.txt") GOOD ; source files under odd/: $(find "$T/vol/WEDNESDAY/odd" -type f | wc -l | tr -d ' ') ; destination files under odd/: $(find "$(CUR)/odd" -type f | wc -l | tr -d ' ')"
say "names at the source that did NOT arrive: $("$PY" -c 'import os,sys
s=set(); d=set()
for r,_,f in os.walk(sys.argv[1]):
    for x in f: s.add(os.path.relpath(os.path.join(r,x), sys.argv[1]))
for r,_,f in os.walk(sys.argv[2]):
    for x in f: d.add(os.path.relpath(os.path.join(r,x), sys.argv[2]))
print(sorted(repr(x)[:60] for x in s-d))' "$T/vol/WEDNESDAY/odd" "$(CUR)/odd")"
/usr/bin/grep -E 'excluded at the source' "$T/out/r1.txt" | head -1
snap a; "$PY" -c 'import os,sys
for r,_,f in os.walk(sys.argv[1]):
    for x in f: open(os.path.join(r,x),"a").write("changed\n")' "$T/vol/WEDNESDAY/odd"
rc=$(run "$(at 1 1 0)" r2); say "after changing every odd file: rc=$rc ; versions kept: $(find "$(VER)" -type f | wc -l | tr -d ' ')"; lost a | tail -1

say; say "### G3 every engine invocation and every destructive verb in the REAL lane's code (read-only grep)"
say "subprocess calls in nb_core.py:"; /usr/bin/grep -n -E 'subprocess\.(run|Popen)' "$RL/nb_core.py" | cut -c1-150
say "the one argv built for the engine (nb_core.py):"; /usr/bin/grep -n -A1 'argv = \[c\["rsync"\]' "$RL/nb_core.py" | cut -c1-200; /usr/bin/grep -n -E 'argv\.(insert|append)|argv \+=' "$RL/nb_core.py" | cut -c1-160
say "rsync / rm / unlink / rmtree / remove / truncate / mv in the lane's five code files (comments included):"
for f in nb_core.py nb_common.sh nas_backup.sh nas_backup_nightly.sh nas_backup_watch.sh; do printf '  %-24s os.remove|unlink|rmtree|shutil: %s ; os.rename|os.replace: %s ; lines with " rm ": %s ; --delete/--inplace/--remove-source outside the FORBIDDEN list and comments: %s\n' "$f" "$(/usr/bin/grep -c -E 'os\.remove|os\.unlink|rmtree|shutil|\.unlink\(' "$RL/$f")" "$(/usr/bin/grep -c -E 'os\.rename|os\.replace' "$RL/$f")" "$(/usr/bin/grep -c -E '(^|[;&| ])rm ' "$RL/$f")" "$(/usr/bin/grep -v -E '^\s*#|FORBIDDEN_RSYNC|"--del", "--delete"|a.startswith' "$RL/$f" | /usr/bin/grep -c -E -- '--delete|--inplace|--remove-source')"; done
say "(positive control for the grep) os.rename|os.replace lines found in nb_core.py:"; /usr/bin/grep -n -E 'os\.rename|os\.replace' "$RL/nb_core.py" | cut -c1-120
say "open(..., \"w\"/\"wb\") targets in nb_core.py:"; /usr/bin/grep -n -E 'open\(.*"(w|wb|a)"' "$RL/nb_core.py" | cut -c1-170

say; say "### G4 the REAL (non-test) mount-table branch, pure functions only: nothing is opened on the NAS"
"$PY" - "$LANE" <<'PYEOF'
import sys; sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1]); import nb_core
class C: pass
def chk(nas, vol):
    c = C(); c.troot = None; c.conf = {"nas_root": nas, "source_volume": vol}
    return nb_core.nas_is_smb_mounted(c), nb_core.source_is_local_volume(c)
print("  /Volumes/DEV-Working as nas_root, /Volumes/DevMASTER as source ->", chk("/Volumes/DEV-Working", "/Volumes/DevMASTER"))
print("  /Volumes/DEV-Workin (prefix of a real mount) ->", chk("/Volumes/DEV-Workin", "/Volumes/DevMAS"))
print("  /Volumes/DevMASTER (a LOCAL drive) offered as the NAS ->", chk("/Volumes/DevMASTER", "/Volumes/DEV-Working"))
print("  /Volumes/NotThere ->", chk("/Volumes/NotThere", "/Volumes/NotThere"))
PYEOF

say; say "### G5 the seat's STATUS figures against its own evidence files"
EV="$RL/evidence"
say "tests_run_final.txt: PASS lines $(/usr/bin/grep -c '  PASS  ' "$EV/tests_run_final.txt"), FAIL lines $(/usr/bin/grep -c '  FAIL  ' "$EV/tests_run_final.txt") ; last line: $(tail -1 "$EV/tests_run_final.txt" | cut -c1-40)"
say "mutants_final.txt: CAUGHT lines $(/usr/bin/grep -c '  CAUGHT  ' "$EV/mutants_final.txt"), SURVIVED $(/usr/bin/grep -c 'SURVIVED  ' "$EV/mutants_final.txt") ; first pass file: CAUGHT $(/usr/bin/grep -c '  CAUGHT  ' "$EV/mutants_first_pass_2_survivors.txt"), SURVIVED $(/usr/bin/grep -c '  SURVIVED  ' "$EV/mutants_first_pass_2_survivors.txt")"
say "real dry run: $(/usr/bin/grep -E '^--- totals' "$EV/real_dry_run_2026-11-27.out" | cut -c1-230)"
say "real dry run: PROBLEM lines $(/usr/bin/grep -c 'PROBLEM' "$EV/real_dry_run_2026-11-27.out") ; 'NOT BACKED UP' lines $(/usr/bin/grep -c 'NOT BACKED UP' "$EV/real_dry_run_2026-11-27.out") ; 'NOT LISTED' lines $(/usr/bin/grep -c 'NOT LISTED' "$EV/real_dry_run_2026-11-27.out") ; estimate line: $(/usr/bin/grep -c '^estimate (not a measurement' "$EV/real_dry_run_2026-11-27.out") ; stderr file bytes: $(stat -f %z "$EV/real_dry_run_2026-11-27.err")"
/usr/bin/grep -E 'NOT LISTED|not this seat' "$EV/real_dry_run_2026-11-27.out" | cut -c1-160
say "engine lines in the real dry run handed a path on the NAS: $(/usr/bin/grep -E '^ +engine: ' "$EV/real_dry_run_2026-11-27.out" | /usr/bin/grep -c '/Volumes/DEV-Working') of $(/usr/bin/grep -c -E '^ +engine: ' "$EV/real_dry_run_2026-11-27.out") ; with -n: $(/usr/bin/grep -E '^ +engine: ' "$EV/real_dry_run_2026-11-27.out" | /usr/bin/grep -c -- ' -n ')"
say "nas_before_and_after_dry_run.txt:"; sed 's/^/   /' "$EV/nas_before_and_after_dry_run.txt" | cut -c1-200
say "not armed (read-only): nasbackup templates in scheduler/jobs: $(ls /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/scheduler/jobs | /usr/bin/grep -i -c nasbackup) ; nasbackup plists in ~/Library/LaunchAgents: $(ls "$HOME/Library/LaunchAgents" | /usr/bin/grep -i -c nasbackup) (control: naspush plists there: $(ls "$HOME/Library/LaunchAgents" | /usr/bin/grep -i -c naspush)) ; HOLD files in the real lane: $(ls "$RL" | /usr/bin/grep -c '^HOLD_')"
say "real state file (the seat's one hold-proof record): $(/opt/homebrew/bin/python3 -c 'import json; d=json.load(open("/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup/state/wednesday.json")); print("armed_at=%s last_good=%s attempts=%d last=%s" % (d.get("armed_at"), d.get("last_good"), len(d.get("recent_attempts", [])), (d.get("last_attempt") or {}).get("status")))')"
