#!/bin/bash
# tests/attack_tree.sh <scratch directory> [path to the checker's atk_build.py]
# Re-runs the independent checker's attack tree (its own atk_build.py, unmodified and run from where it
# lies) against THIS lane's tool with a byte copy of scope/wednesday.scope, on a scratch cluster, and
# counts its expectations the way its atk_eval.sh does: a whole-index pg_dump searched for each token.
# The checker saw 26 unexpected of 69 on 2026-11-27; the target is 0.
# Reads the checker's directory, never writes it. Nothing is deleted. No `cd`.
set -u
SCR="${1:-}"; ATK="${2:-/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb/scripts/atk_build.py}"
[ -n "$SCR" ] && [ -d "$SCR" ] || { echo "usage: attack_tree.sh <scratch directory> [atk_build.py]" >&2; exit 2; }
[ -f "$ATK" ] || { echo "attack_tree.sh: not found: $ATK" >&2; exit 2; }
PY="${BRAINDB_PYTHON:-python3}"
SELF="${BASH_SOURCE[0]}"; case "$SELF" in /*) ;; *) SELF="$PWD/$SELF" ;; esac
LANE="$(dirname "$("$PY" -c 'import os,sys; print(os.path.dirname(os.path.realpath(sys.argv[1])))' "$SELF")")"
PF="$(dirname "$LANE")"
A="$SCR/atk-$(date +%Y%m%d-%H%M%S)-$$"; SOCK="/tmp/wed-bdb-a$$"
T="$A/sim/WEDNESDAY/2_Project_Files"
mkdir -p "$A/cwd" "$T/brain-db/scope" "$T/fleet/cockpit" "$T/tools" || exit 2
cp "$LANE/braindb.sh" "$LANE/braindb_index.py" "$LANE/braindb_lock.py" "$T/brain-db/" || exit 2
cp "$LANE/scope/wednesday.scope" "$T/brain-db/scope/" || exit 2
cp "$PF/fleet/cockpit/seat_resolve.sh" "$T/fleet/cockpit/" || exit 2
if [ -f "$PF/tools/seat_note.sh" ]; then cp "$PF/tools/seat_note.sh" "$T/tools/" || exit 2; fi
PGBIN="${BRAINDB_PGBIN:-/opt/homebrew/opt/postgresql@15/bin}"
B() { env -u WED_AGENT BRAINDB_ROOT="$A/tree" BRAINDB_PGDATA="$A/pg" BRAINDB_SOCKDIR="$SOCK" /bin/bash "$T/brain-db/braindb.sh" "$@"; }
echo "attack tree: run directory $A ; $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "builder: $ATK"
"$PY" "$ATK" "$A/tree" || { echo "the checker's builder failed" >&2; exit 2; }
"$PY" - "$A" "$T/brain-db/braindb.sh" "$SOCK" <<'PY'
import subprocess, os, sys
A, tool, sock = sys.argv[1], sys.argv[2], sys.argv[3]
env = dict(os.environ, BRAINDB_ROOT=A + "/tree", BRAINDB_PGDATA=A + "/pg", BRAINDB_SOCKDIR=sock)
env.pop("WED_AGENT", None)
r = subprocess.run(["/bin/bash", tool, "rebuild"], cwd=A + "/cwd", env=env)       # cwd as the checker ran it
print("rebuild rc=%d" % r.returncode)
PY
"$PGBIN/pg_dump" --data-only --schema=brain -h "$SOCK" -d braindb > "$A/dump.sql" || echo "pg_dump failed"
echo "dump lines: $(wc -l < "$A/dump.sql" | tr -d ' ')   (control) 'xneighbour01' count: $(/usr/bin/grep -i -F -c xneighbour01 "$A/dump.sql")   this lane's own canaries, 'xcanary' count: $(/usr/bin/grep -i -F -c xcanary "$A/dump.sql")"
"$PY" - "$A" <<'PY'
import json, sys
A = sys.argv[1]
d = open(A + "/dump.sql", encoding="utf-8", errors="replace").read()
bad = 0
exp = json.load(open(A + "/expect.json"))
for tok, want, what in exp:
    n = d.count(tok)
    got = "present" if n else "absent"
    v = "ok  " if got == want else "LEAK" if want == "absent" else "MISS"
    if got != want:
        bad += 1
    print("%s %-13s want %-7s got %-7s (%d)  %s" % (v, tok, want, got, n, what))
print("expectations: %d   unexpected: %d" % (len(exp), bad))
PY
echo "---- PWNED files under the run directory (want none); control: expect.json is found by the same find"
find "$A" -maxdepth 2 \( -iname 'PWNED*' -o -name expect.json \) -not -path '*/pg/*' | sed "s|$A/||"
B stop | tail -1
snap="$(ps -axww -o pid=,command=)"; echo "server processes left for this run: $(printf '%s\n' "$snap" | /usr/bin/grep -F -c -- "-D $A/pg")"
if [ -d "$SOCK" ]; then mv -n "$SOCK" "$A/sock-moved"; fi
date '+%Y-%m-%d %H:%M:%S %Z'
