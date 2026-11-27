#!/bin/bash
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb
D="$S/prop/r$(date +%H%M%S)"; T="$D/WEDNESDAY"; mkdir -p "$D"
SRC=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files
sh() { awk -v n="${1:-190}" '{print substr($0,1,n)}' | sed "s|$D/||g"; }
echo "/bin/bash is: $(/bin/bash --version | head -1)"
for f in doctor_block.sh launcher_block.sh; do /bin/bash -n "$S/prop/$f"; echo "bash -n $f rc=$?"; done
/bin/bash -n "$SRC/brain-db/braindb.sh"; echo "bash -n braindb.sh rc=$?"; /bin/bash -n "$SRC/brain-db/tests/run.sh"; echo "bash -n tests/run.sh rc=$?"
echo "bash-4-only constructs in braindb.sh / run.sh / the two blocks (want 0; control: 'local ' count in braindb.sh = $(/usr/bin/grep -i -c 'local ' "$SRC/brain-db/braindb.sh")):"
/usr/bin/grep -n -i -E 'declare -A|mapfile|readarray|\$\{[A-Za-z_]+(,,|\^\^)\}|&>>|\|&|coproc|timeout ' "$SRC/brain-db/braindb.sh" "$SRC/brain-db/tests/run.sh" "$S/prop/doctor_block.sh" "$S/prop/launcher_block.sh" | sh; echo "(grep rc=$?; 1 means none)"
python3 "$SRC/brain-db/tests/make_fixtures.py" "$T" > "$D/fx.out" 2>&1
mkdir -p "$T/2_Project_Files/brain-db" "$T/2_Project_Files/fleet/cockpit"
cp "$SRC/brain-db/braindb.sh" "$SRC/brain-db/braindb_index.py" "$T/2_Project_Files/brain-db/"; cp -R "$SRC/brain-db/scope" "$T/2_Project_Files/brain-db/"
cp "$SRC/fleet/cockpit/seat_resolve.sh" "$T/2_Project_Files/fleet/cockpit/"
export BRAINDB_SOCKDIR=/tmp/qa-bdb-501
launcher() { ( set -u; PROJECT_DIR="$T"; AGENT="wednesday"; . "$S/prop/launcher_block.sh"; echo "[launcher continues after the block: yes]" ) 2>&1 | sh; }
doctor() { ( set -uo pipefail; QUIET=""; WARNS=0; PROJECT_DIR="$T"; _DOC_AGENT="wednesday"; ok() { printf "  OK   %s\n" "$1"; }; warn() { printf "  WARN %-34s %s\n" "$1" "${2:-}"; }; . "$S/prop/doctor_block.sh"; echo "[doctor continues: yes]" ) 2>&1 | sh; }
np() { local snap; snap="$(ps -axww -o pid=,command=)"; printf '%s\n' "$snap" | /usr/bin/grep -i -F -c -- "-D $D"; }
echo; echo "---- D1 doctor, no cluster yet"; doctor; echo "processes: $(np)"
echo "---- L1 launcher block, first boot (no cluster): creates, starts, builds"; t0=$(date +%s); launcher; echo "took $(( $(date +%s) - t0 )) s ; processes: $(np)"
echo "---- D2 doctor, server running, index current"; doctor
echo "---- D3 doctor, a file changed"; echo "x" >> "$T/0_Brain/skills/ritual.md"; doctor
echo "---- L2 launcher block, second boot, a file changed: rebuild"; launcher
echo "---- stop (the proposed wrap line), then D4 doctor with the server stopped"; /bin/bash "$T/2_Project_Files/brain-db/braindb.sh" stop | tail -1 | sh 60; doctor; echo "processes after doctor: $(np)"
echo "---- L3 launcher block with a cluster from another major version (marker 14)"
mv -n "$T/2_Project_Files/brain-db/pgdata-wednesday/PG_VERSION" "$D/PG_VERSION.real"; echo 14 > "$T/2_Project_Files/brain-db/pgdata-wednesday/PG_VERSION"
launcher; echo "processes: $(np)"; echo "-- D5 doctor in the same state"; doctor
mv -n "$T/2_Project_Files/brain-db/pgdata-wednesday/PG_VERSION" "$D/PG_VERSION.fake"; mv -n "$D/PG_VERSION.real" "$T/2_Project_Files/brain-db/pgdata-wednesday/PG_VERSION"
echo "---- L4 launcher block with Postgres ABSENT (a copy of the tool whose two keg paths do not exist, PATH=/usr/bin:/bin)"
sed -e 's|/opt/homebrew/opt/postgresql@15/bin|/nonexistent/pg15/bin|; s|/usr/local/opt/postgresql@15/bin|/nonexistent/pg15b/bin|' "$T/2_Project_Files/brain-db/braindb.sh" > "$D/braindb_nopg.sh"
mv -n "$T/2_Project_Files/brain-db/braindb.sh" "$D/braindb_orig.sh"; cp "$D/braindb_nopg.sh" "$T/2_Project_Files/brain-db/braindb.sh"; chmod +x "$T/2_Project_Files/brain-db/braindb.sh"
( PATH=/usr/bin:/bin; launcher ); echo "processes: $(np)"
echo "---- L5 launcher block with python3 ABSENT from PATH (PATH=/nonexistent)"
( set -u; PROJECT_DIR="$T"; AGENT="wednesday"; PATH=/nonexistent; . "$S/prop/launcher_block.sh"; echo "[launcher continues after the block: yes]" ) 2>&1 | sh
mv -n "$T/2_Project_Files/brain-db/braindb.sh" "$D/braindb_nopg_used.sh"; mv -n "$D/braindb_orig.sh" "$T/2_Project_Files/brain-db/braindb.sh"
echo "---- L6 launcher block when the lane or the scope file is missing (another seat that has not adopted)"
( set -u; PROJECT_DIR="$T"; AGENT="friday"; . "$S/prop/launcher_block.sh"; echo "[silent skip, launcher continues: yes]" ) 2>&1 | sh
/bin/bash "$T/2_Project_Files/brain-db/braindb.sh" stop | tail -1 | sh 60; echo "processes with -D under $D: $(np)"
