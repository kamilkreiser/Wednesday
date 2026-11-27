#!/bin/bash
# attack run 1: the builder's own wednesday.scope (a byte copy) over the attack tree
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb
A="$S/atk/r$(date +%H%M%S)"; mkdir -p "$A/cwd" || exit 2
echo "run dir $A"; echo "$A" > "$S/atk/LAST"
python3 "$S/atk/build.py" "$A/tree" || exit 2
SOCK=/tmp/qa-bdb-501; [ -d "$SOCK" ] || mkdir -m 700 "$SOCK"
B() { BRAINDB_ROOT="$A/tree" BRAINDB_PGDATA="$A/pg" BRAINDB_SOCKDIR="$SOCK" BRAINDB_SCOPE="${T_SCOPE:-}" WED_AGENT=wednesday /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/braindb.sh "$@"; }
B init > "$A/init.out" 2>&1; echo "init rc=$?"
B start; echo "start rc=$?"
echo "---- rebuild over the attack tree (run from $A/cwd)"
python3 - "$A" <<'PY'
import subprocess, os, sys
A = sys.argv[1]
env = dict(os.environ, BRAINDB_ROOT=A+"/tree", BRAINDB_PGDATA=A+"/pg", BRAINDB_SOCKDIR="/tmp/qa-bdb-501", WED_AGENT="wednesday")
r = subprocess.run(["/bin/bash", "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/braindb.sh", "rebuild"], cwd=A+"/cwd", env=env)
print("rebuild rc=%d" % r.returncode)
PY
