#!/bin/bash
# tests/mutants.sh <scratch directory> [mutant name ...] - proof that the suite can fail.
# For each mutant: copy this lane into <scratch>/mut-.../WEDNESDAY/2_Project_Files/brain-db (with the seat
# resolver and seat_note.sh), BREAK ONE THING in the copy, run the copy's own tests/run.sh, and require
# at least one FAIL line that matches the assertion the broken thing is meant to trip. The lane itself is
# never modified. "none" is the control: the unmutated copy must pass with 0 failures.
# Runs up to 4 mutants at a time (each run has its own directories and socket directories).
set -u
SCR="${1:-}"; [ -n "$SCR" ] && [ -d "$SCR" ] || { echo "usage: mutants.sh <scratch directory> [mutant ...]" >&2; exit 2; }
shift
PY="${BRAINDB_PYTHON:-python3}"
SELF="${BASH_SOURCE[0]}"; case "$SELF" in /*) ;; *) SELF="$PWD/$SELF" ;; esac
TESTS="$("$PY" -c 'import os,sys; print(os.path.dirname(os.path.realpath(sys.argv[1])))' "$SELF")"
LANE="$(dirname "$TESTS")"; PF="$(dirname "$LANE")"
OUT="$SCR/mutants-$(date +%Y%m%d-%H%M%S)-$$"; mkdir -p "$OUT" || exit 2

cat > "$OUT/mutate.py" <<'PY'
import sys, os, shutil
name, lane, pf, dst = sys.argv[1:5]
# name: (file, old text that must occur exactly once, new text, regex one FAIL line must match, what was broken)
M = {
 "none": None,
 "F1i_key_not_folded": ("braindb_index.py", "                k = k.strip().strip(\"\\\"'\").strip().lower()\n", "                k = k.strip()\n",
     "xcanary601|xcanary609|xcanary611", "frontmatter keys are no longer folded (Tier:, \"tier\":, TIER:)"),
 "F1i_faults_ignored": ("braindb_index.py", "            if faults:\n", "            if False:\n",
     "xcanary605|xcanary607|xcanary608", "a head that is ambiguous about its tier no longer excludes the lesson"),
 "F1i_bom_kept": ("braindb_index.py", "    if text.startswith(\"\\ufeff\"):\n        text = text[1:]\n", "",
     "xneighbour831|a BOM", "the BOM is no longer stripped"),
 "F1ii_client_substring": ("braindb_index.py", "        if client in sc[\"own\"]:\n", "        if any(c in low for c in sc[\"own\"]):\n",
     "xcanary610|xcanary622", "own clients are matched as substrings of the whole tier again"),
 "F1iii_rejected_rows_ignored": ("braindb_index.py", "            if k in bad_names:\n", "            if False:\n",
     "xcanary660|xcanary663|xcanary668|xcanary675", "a damaged rules-index row no longer excludes the lesson it names"),
 "F1iii_keys_not_normalised": ("braindb_index.py", "    s = s.strip().split(\"#\", 1)[0].strip()\n    return s.replace(\"\\\\\", \"/\").rsplit(\"/\", 1)[-1].casefold()\n", "    return s.split(\"#\", 1)[0]\n",
     "xcanary662|xcanary664|xcanary670", "rules-index keys are no longer stripped, case-folded and path-stripped"),
 "F1iii_no_index_not_refused": ("braindb_index.py", "    if any(k == \"lesson\" for k, _ in sc[\"allow\"]) and good == 0:\n", "    if False:\n",
     "rules index missing is refused|no well-formed row is refused", "a missing rules index no longer refuses the rebuild"),
 "F1iv_marker_strict_spelling": ("braindb_index.py", "MARKER = re.compile(r\"(?i)^\\s*<!--\\s*tier\\s*:\\s*(.*?)\\s*-->\\s*$\")", "MARKER = re.compile(r\"^<!--\\s*tier:\\s*(P-.*?)\\s*-->\\s*$\")",
     "xcanary641|xcanary643|xcanary645|xcanary646", "section markers are matched in the old strict spelling only"),
 "F1iv_marker_blank_line": ("braindb_index.py", "        j = k + 1\n        while j < len(lines) and not lines[j].strip():\n            j += 1\n        if j in level:\n", "        j = k + 1\n        if j in level:\n",
     "xcanary640", "a blank line between a marker and its heading is no longer skipped"),
 "F1iv_subsection_kept": ("braindb_index.py", "level[h] <= level[j]", "True",
     "xcanary644sub", "a dropped section ends at the next heading of ANY level again"),
 "F3_hard_link_through": ("braindb_index.py", "            if st.st_nlink > 1:\n", "            if False:\n",
     "xcanary680|hard link", "hard links are indexed again"),
 "F11_seat_word_by_kind": ("braindb_index.py", "            name_exempt = kind in HOME and dlow in HOME[kind]\n", "            name_exempt = kind not in RECORD_KINDS\n",
     "xcanary700|xcanary701", "the seat-word test on file names depends on the declared kind again"),
 "daily_name_any": ("braindb_index.py", "            if kind == \"daily\" and not DAILY_NAME.fullmatch(name):\n", "            if False:\n",
     "xcanary691|xcanary692|xcanary693", "a daily note need no longer be named as a plain date"),
 "F2_any_server_will_do": ("braindb_index.py", "    if not got or os.path.realpath(got) != os.path.realpath(want):\n", "    if False:\n",
     "addressed to c2|untouched|GREEN line|ANOTHER cluster", "the server is no longer asked for its data directory"),
 "F4_scope_checked_late": ("braindb.sh", "           need_scope; find_pgbin; ensure_up || exit 1; indexer \"$@\" ;;\n", "           find_pgbin; ensure_up || exit 1; indexer \"$@\" ;;\n",
     "NOTHING was created|nothing created|no server was started", "the scope file is tested after the cluster is created and started"),
 "F5_no_lock": ("braindb.sh", "locked() { \"$PY\" \"$LANE/braindb_lock.py\" \"$LOCKFILE\" 150 /bin/bash \"$SELF\" \"$@\"; }\n", "locked() { /bin/bash \"$SELF\" \"$@\"; }\n",
     "double init|two starts|two self-starting|NO cluster at all", "init and start are no longer serialised by the lock"),
 "F6_stale_pid_unexplained": ("braindb.sh", "  foreign_pidfile_guard\n  check_sockdir\n", "  check_sockdir\n",
     "STALE PID FILE|recovery", "start no longer explains a pid file that names a live foreign process"),
 "F7_unreadable_aborts": ("braindb_index.py", "            except OSError as e:\n                loaded[rel] = None\n", "            except ZeroDivisionError as e:\n                loaded[rel] = None\n",
     "unreadable lesson|traceback|unreadable file is listed", "an unreadable file is no longer caught"),
 "F7_row_not_capped": ("braindb_index.py", "        if v is None or len(v) <= limit:\n", "        if True:\n",
     "3 MB section|truncated row", "an over-long row is no longer truncated"),
 "F8_separators_kept": ("braindb_index.py", "STRIP_BYTES = {0x00: None, 0x1e: None, 0x1f: None}", "STRIP_BYTES = {0x00: None}",
     "separator bytes", "the two separator bytes are no longer stripped on read"),
 "F9_stop_trusts_pidfile": ("braindb.sh", "  case \"$cmd \" in *\" -D $PGDATA \"*) return 0 ;; esac\n  return 1\n", "  return 0\n",
     "foreign process is still alive|foreign process was killed", "the checker's M2: stop signals whatever the pid file names"),
 "rules_row_always_first": ("braindb_index.py", "    first = [r for r in know if r[1] == \"rules\" and holds_all(r)]\n    rest = [r for r in know if not (r[1] == \"rules\" and holds_all(r))]\n", "    first = [r for r in know if r[1] == \"rules\"]\n    rest = [r for r in know if r[1] != \"rules\"]\n",
     "holds only ONE of the question", "a rules-file row is put first whatever it matched"),
 "lessons_first_off": ("braindb_index.py", "    if mode != \"default\":\n", "    if True:\n",
     "the lesson is result 1 although ledger rows score higher|incident rows follow", "the default order is the old mixed one"),
 "seat_follows_WED_AGENT": ("braindb.sh", "  seat_note_dir \"$CODE_ROOT\" braindb || exit 2\n  SEAT=\"$SEAT_NOTE_SEAT\"\n", "  . \"$RESOLVER\"; seat_resolve \"$CODE_ROOT\"\n",
     "WED_AGENT=tuesday on a tree named WEDNESDAY|not WEDNESDAY, TUESDAY or FRIDAY", "the seat follows WED_AGENT and an unknown tree defaults to wednesday, as before"),
}
if name == "--list":
    print(" ".join(M)); sys.exit(0)
t = os.path.join(dst, "WEDNESDAY", "2_Project_Files")
os.makedirs(os.path.join(t, "fleet", "cockpit")); os.makedirs(os.path.join(t, "tools"))
shutil.copytree(lane, os.path.join(t, "brain-db"),
                ignore=shutil.ignore_patterns("pgdata-*", "_quarantine_*", "_probe_*", "__pycache__", "evidence", "*.lock"))
shutil.copy2(os.path.join(pf, "fleet", "cockpit", "seat_resolve.sh"), os.path.join(t, "fleet", "cockpit"))
if os.path.isfile(os.path.join(pf, "tools", "seat_note.sh")):
    shutil.copy2(os.path.join(pf, "tools", "seat_note.sh"), os.path.join(t, "tools"))
if M[name] is None:
    open(os.path.join(dst, "EXPECT"), "w").write("\n"); open(os.path.join(dst, "WHAT"), "w").write("nothing (control)\n")
    sys.exit(0)
f, old, new, expect, what = M[name]
p = os.path.join(t, "brain-db", f)
s = open(p, encoding="utf-8").read()
if s.count(old) != 1:
    sys.exit("mutation anchor for %s found %d times in %s, need exactly 1" % (name, s.count(old), f))
open(p, "w", encoding="utf-8").write(s.replace(old, new))
open(os.path.join(dst, "EXPECT"), "w").write(expect + "\n"); open(os.path.join(dst, "WHAT"), "w").write(what + "\n")
PY

if [ "$#" -gt 0 ]; then NAMES="$*"; else NAMES="$("$PY" "$OUT/mutate.py" --list x x x)"; fi
one() { # run one mutant; writes $OUT/<name>/verdict
  local n="$1" d="$OUT/$1"
  mkdir -p "$d/scr" || return 1
  if ! "$PY" "$OUT/mutate.py" "$n" "$LANE" "$PF" "$d" > "$d/mutate.out" 2>&1; then echo "SETUP-ERROR $(tail -1 "$d/mutate.out")" > "$d/verdict"; return 0; fi
  /bin/bash "$d/WEDNESDAY/2_Project_Files/brain-db/tests/run.sh" "$d/scr" > "$d/suite.log" 2>&1
  local rc=$? nf np hit
  nf="$(/usr/bin/grep -i -F -c '  FAIL  ' "$d/suite.log")"; np="$(/usr/bin/grep -i -F -c '  PASS  ' "$d/suite.log")"
  if [ "$n" = "none" ]; then
    if [ "$rc" -eq 0 ] && [ "$nf" = "0" ]; then echo "CONTROL-OK  $np passed, 0 failed" > "$d/verdict"; else echo "CONTROL-BROKEN  $np passed, $nf failed (rc $rc)" > "$d/verdict"; fi
    return 0
  fi
  hit="$(/usr/bin/grep -i -F '  FAIL  ' "$d/suite.log" | /usr/bin/grep -i -E -c -- "$(cat "$d/EXPECT")")"
  if [ "$hit" != "0" ]; then echo "CAUGHT  $nf failing line(s), $hit on the expected assertion  [$(/usr/bin/grep -i -F '  FAIL  ' "$d/suite.log" | /usr/bin/grep -i -E -- "$(cat "$d/EXPECT")" | head -1 | cut -c9-150)]" > "$d/verdict"
  elif [ "$nf" != "0" ]; then echo "RED-ELSEWHERE  $nf failing line(s), none on the expected assertion /$(cat "$d/EXPECT")/" > "$d/verdict"
  else echo "SURVIVED  the suite passed ($np) with this broken" > "$d/verdict"; fi
}
echo "mutants: output $OUT ; $(date '+%Y-%m-%d %H:%M:%S %Z')"
running=0
for n in $NAMES; do
  one "$n" &
  running=$((running+1))
  if [ "$running" -ge 4 ]; then wait; running=0; fi
done
wait
caught=0; total=0; other=0
for n in $NAMES; do
  v="$(cat "$OUT/$n/verdict" 2>&1)"
  printf '%-30s %s\n' "$n" "$v"
  printf '%-30s   broke: %s\n' "" "$(cat "$OUT/$n/WHAT" 2>&1)"
  case "$n" in none) ;; *) total=$((total+1)); case "$v" in CAUGHT*) caught=$((caught+1)) ;; *) other=$((other+1)) ;; esac ;; esac
done
snap="$(ps -axww -o pid=,command=)"; echo "server processes left under $OUT: $(printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $OUT")"
echo "finished $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "MUTANTS: $caught of $total caught on the expected assertion; $other not"
[ "$other" -eq 0 ]
