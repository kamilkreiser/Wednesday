#!/bin/bash
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb
D="$S/sim-$(date +%H%M%S)"; T="$D/TUESDAY"; mkdir -p "$D/scr"
SRC=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files
python3 "$SRC/brain-db/tests/make_fixtures.py" "$T" > "$D/fx.out" 2>&1
mkdir -p "$T/2_Project_Files/brain-db" "$T/2_Project_Files/fleet/cockpit"
cp "$SRC/brain-db/braindb.sh" "$SRC/brain-db/braindb_index.py" "$SRC/brain-db/.gitignore" "$T/2_Project_Files/brain-db/"
cp -R "$SRC/brain-db/scope" "$SRC/brain-db/tests" "$SRC/brain-db/proposed" "$T/2_Project_Files/brain-db/"
cp "$SRC/fleet/cockpit/seat_resolve.sh" "$T/2_Project_Files/fleet/cockpit/"
B="$T/2_Project_Files/brain-db/braindb.sh"
sh() { awk -v n="${1:-200}" '{print substr($0,1,n)}' | sed "s|$D/||g"; }
echo "sim dir $D"
echo "---- requirement 4: status prints the seat (WED_AGENT unset, tree named TUESDAY)"
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" status | sh; 
echo "---- before step 1: every command refuses"
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" check 2>&1 | sh; echo "rc=${PIPESTATUS[0]} ; cluster dir created by the refused command? $([ -d "$T/2_Project_Files/brain-db/pgdata-tuesday" ] && echo YES || echo no) ; processes: $(ps -axww -o command= | /usr/bin/grep -i -F -c -- "-D $T")"
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" stop 2>&1 | tail -1 | sh 80
echo "---- step 1: cp -n the proposal into place"
cp -n "$T/2_Project_Files/brain-db/proposed/scope/tuesday.scope" "$T/2_Project_Files/brain-db/scope/tuesday.scope"; echo "cp rc=$?"
echo "---- step 2: the suite on this tree (instructions say: 295 passed, or two failures in section 12 once scope/tuesday.scope exists)"
env -u WED_AGENT /bin/bash "$T/2_Project_Files/brain-db/tests/run.sh" "$D/scr" > "$D/suite.log" 2>&1; echo "suite rc=$? : $(tail -1 "$D/suite.log" | sh 40)"; /usr/bin/grep -i '  FAIL  ' "$D/suite.log" | sh 160
echo "---- step 3: up, rebuild, check"
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" up > "$D/up.out" 2>&1; echo "up rc=$? : $(tail -1 "$D/up.out" | sh 100)"
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" rebuild 2>&1 | sh 170
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" check | sh 100
echo "---- what the Tuesday index holds (kind, path)"
/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h /tmp/qa-bdb-501 -d braindb -c "select kind, path from brain.files order by 1,2"
echo "---- step 6"
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" search xcanary23 --limit 1 | sh 120
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" at pane | sh 140
echo "---- a WEDNESDAY-seat env var on the TUESDAY tree (WED_AGENT=wednesday): which seat's index is built from this tree?"
WED_AGENT=wednesday BRAINDB_SOCKDIR=/tmp/qa-bdb-501-b /bin/bash "$B" status 2>&1 | head -2 | sh
env -u WED_AGENT BRAINDB_SOCKDIR=/tmp/qa-bdb-501 /bin/bash "$B" stop | tail -1 | sh 60
echo "processes with -D under $D: $(ps -axww -o command= | /usr/bin/grep -i -F -c -- "-D $D")"
echo "default socket dir for tuesday on this Mac touched by me? $(ls -ld /tmp/wed-braindb-501-tuesday 2>&1 | sh 90)"
