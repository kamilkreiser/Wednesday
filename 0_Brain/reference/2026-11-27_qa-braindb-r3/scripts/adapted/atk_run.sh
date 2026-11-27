#!/bin/bash
# attack run 1: the builder's own wednesday.scope (a byte copy) over the attack tree
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/chk
A="$S/atk/r$(date +%H%M%S)"; mkdir -p "$A/cwd" || exit 2
echo "run dir $A"; echo "$A" > "$S/atk/LAST"
python3 "$S/atk/build.py" "$A/tree" || exit 2
SOCK=/tmp/qa3c; [ -d "$SOCK" ] || mkdir -m 700 "$SOCK"
B() { BRAINDB_ROOT="$A/tree" BRAINDB_PGDATA="$A/pg" BRAINDB_SOCKDIR="$SOCK" BRAINDB_SCOPE="${T_SCOPE:-}" WED_AGENT=wednesday /bin/bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/braindb.sh "$@"; }
B init > "$A/init.out" 2>&1; echo "init rc=$?"
B start; echo "start rc=$?"
echo "---- rebuild over the attack tree (run from $A/cwd)"
python3 - "$A" <<'PY'
import subprocess, os, sys
A = sys.argv[1]
env = dict(os.environ, BRAINDB_ROOT=A+"/tree", BRAINDB_PGDATA=A+"/pg", BRAINDB_SOCKDIR="/tmp/qa3c", WED_AGENT="wednesday")
r = subprocess.run(["/bin/bash", "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-braindb-r3/lanecopy/WEDNESDAY/2_Project_Files/brain-db/braindb.sh", "rebuild"], cwd=A+"/cwd", env=env)
print("rebuild rc=%d" % r.returncode)
PY
