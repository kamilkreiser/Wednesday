#!/bin/bash
# lib2.sh — round-2 re-check harness (fresh checker, 2026-11-27). Sources the ADAPTED copy of the first checker's lib
# (fixtures sealed with the END marker), adds stub and marker helpers. Everything runs on a scratch COPY of the lane
# against fake trees under the session scratchpad. Never a real NAS path.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/r1_adapted/lib.sh"
mkstub() { # name body   (body runs after the --version passthrough; "$@" = rsync's args; T2 = fixture root)
  local f="$T/stub/$1"
  { echo '#!/bin/bash'; echo "REAL=$REAL_RSYNC"; echo 'T2="$(cd "$(dirname "$0")/.." && pwd)"'
    echo 'for a in "$@"; do if [ "$a" = "--version" ]; then exec "$REAL" --version; fi; done'
    echo 'DEST="${@: -1}"; N=$(cat "$T2/stub/calls" 2>/dev/null || echo 0); N=$((N+1)); echo $N > "$T2/stub/calls"'
    echo "$2"; } > "$f"; chmod +x "$f"; echo "$f"; }
run() { nb --run --now "$1" > "$T/out/$2.txt" 2>&1; echo $?; }
good() { /usr/bin/grep -c -F 'GOOD: every in-scope' "$T/out/$1.txt"; }
line() { /usr/bin/grep -F -- "$2" "$T/out/$1.txt" | head -${3:-1} | cut -c1-${4:-260}; }
onnas() { /usr/bin/grep -r -l -F -- "$1" "$T/nas" 2>&1 | wc -l | tr -d ' '; }
oncur() { /usr/bin/grep -r -l -F -- "$1" "$T/nas"/*/Wednesday/nightly-backup/current 2>&1 | wc -l | tr -d ' '; }
idxrows() { /opt/homebrew/bin/python3 -c 'import sqlite3,sys
try:
    print(sqlite3.connect(sys.argv[1]).execute("select count(*) from files").fetchone()[0])
except Exception as e: print("ERR", e)' "$T/lane/state/wednesday.index.sqlite"; }
