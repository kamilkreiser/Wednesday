#!/bin/bash
# B7b — REDO of the B7 case variants. In B7 the variants (DataSec, DATAsec, TuesDay) were planted in the SAME parent
# as the listed spelling on a case-insensitive scratch volume, so they were the same folder: those "kept out" lines
# prove nothing. Here every variant has its own parent folder.
# B12 — the tuesday and friday seats' confinement, on fake TUESDAY / FRIDAY trees.
. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"
onnas() { /usr/bin/grep -r -l -a -F -- "$1" "$T/nas" 2>/dev/null | /usr/bin/grep -v '/manifests/' | wc -l | tr -d ' '; }
plant() { mkdir -p "$(dirname "$1")"; echo "MARK[$2]" > "$1"; }
report() { local n; n="$(onnas "MARK[$2]")"; if [ "$n" = 0 ]; then printf 'kept out   %-6s %s\n' "$2" "$1"; else printf 'LEAKED     %-6s %s -> %s\n' "$2" "$1" "$(/usr/bin/grep -r -l -a -F -- "MARK[$2]" "$T/nas" | /usr/bin/grep -v /manifests/ | head -1 | sed "s|$T/nas/||")"; fi; }

say "### B7b other-client and other-seat names, one parent folder per spelling (wednesday seat)"
fixture B7b; W="$T/vol/WEDNESDAY"; X="$T/vol/CODING/Secuura"
plant "$W/v1/Datasec/a.md" e1; plant "$W/v2/DATASEC/a.md" e2; plant "$W/v3/datasec/a.md" e3
plant "$W/v4/DataSec/a.md" e4; plant "$W/v5/DATAsec/a.md" e5; plant "$W/v6/dataSEC/a.md" e6; plant "$X/v7/DataSec/a.md" e7
plant "$W/w1/Tuesday/a.md" f1; plant "$W/w2/TUESDAY/a.md" f2; plant "$W/w3/TuesDay/a.md" f3; plant "$W/w4/tuesDAY/a.md" f4; plant "$W/w5/FriDay/a.md" f5
plant "$W/n1/NexusAI/a.md" g1; plant "$W/n2/Vision_Sales_Portal/a.md" g2; plant "$T/vol/CODING/Secuura/n3/nexusai/a.md" g3
nb --run --now "$(at 0 1 0)" > "$T/out/r.txt" 2>&1; say "run rc=$? ($(/usr/bin/grep -c 'GOOD:' "$T/out/r.txt") GOOD line)"
for m in e1 e2 e3; do report "Datasec, a spelling on the list" "$m"; done; for m in e4 e5 e6 e7; do report "Datasec, mixed case" "$m"; done
for m in f1 f2; do report "other seat, a spelling on the list" "$m"; done; for m in f3 f4 f5; do report "other seat, mixed case" "$m"; done
for m in g1 g2 g3; do report "a Datasec PROJECT by its own name (no 'datasec' in the name)" "$m"; done

seatfix() { # seat  CAP  -> fixture for another seat
  T="$S/fx/B12_$1_$$"; mkdir -p "$T/vol/$2" "$T/vol/CODING" "$T/nas/Secuura" "$T/nas/General" "$T/nas/Datasec" "$T/lane/seats" "$T/out"
  echo 5000 > "$T/free_gib.txt"; write_mounts; }
sconf() { # seat ; lines...
  local seat="$1"; shift
  { echo "status=confirmed"; echo "source_volume=$T/vol"; echo "nas_root=$T/nas"; echo "fire=02:30"; echo "window_hours=3"; echo "min_free_gib=200"; echo "max_seconds=600"; echo "hash_sample=5"
    for l in "$@"; do echo "$l"; done; } > "$T/lane/seats/$seat.conf"; }
srun() { env -u WED_AGENT NB_TEST_ROOT="$T" NB_TEST_TREE="$T/vol/$1" "$LANE/nas_backup.sh" --run --now "$(at 0 3 0)" > "$T/out/$2.txt" 2>&1; echo $?; }

say; say "### B12a TUESDAY seat (client Datasec): can it write to, or read from, Secuura / General?"
seatfix tuesday TUESDAY; TT="$T/vol/TUESDAY"
plant "$TT/own.md" u0; plant "$TT/x/Secuura/a.md" u1; plant "$TT/y/SecUura/a.md" u2; plant "$TT/z/secuura-notes.md" u3; plant "$TT/k/Blockchain/a.md" u4; plant "$TT/k2/Platform-K/a.md" u5
plant "$TT/2_Project_Files/wednesday/notes.md" u6; plant "$TT/0_Brain/daily_wednesday/d.md" u7; plant "$TT/4_Credentials/k" u8; plant "$TT/q/friday/a.md" u9
mkdir -p "$T/vol/CODING/Datasec/p" "$T/vol/CODING/Secuura/p"; plant "$T/vol/CODING/Datasec/p/a.md" u10; plant "$T/vol/CODING/Secuura/p/a.md" u11
sconf tuesday "set=Datasec|TUESDAY|$TT" "set=Datasec|Datasec|$T/vol/CODING/Datasec"
rc=$(srun TUESDAY r); say "run rc=$rc ; destination folders created: $(find "$T/nas" -maxdepth 2 -mindepth 2 | sed "s|$T/nas/||" | tr '\n' ' ')"
report "own file (POSITIVE CONTROL: must be LEAKED = arrived)" u0; report "own client project" u10
for m in u1 u3; do report "Secuura by a listed spelling" "$m"; done; report "Secuura mixed case" u2; report "Secuura's projects by their own names (Blockchain)" u4; report "Secuura's project (Platform-K)" u5
report "WEDNESDAY seat's folder inside the shared tree (2_Project_Files/wednesday)" u6; report "WEDNESDAY seat's daily notes (daily_wednesday)" u7; report "4_Credentials" u8; report "friday folder" u9
for bad in "set=Secuura|X|$TT" "set=General|X|$TT" "set=Datasec|X|$T/vol/CODING/Secuura/p"; do sconf tuesday "set=Datasec|TUESDAY|$TT" "$bad"; rc=$(srun TUESDAY b$RANDOM); say "rc=$rc for extra line [$(echo "$bad" | sed "s|$T/||")] ; u11 on NAS=$(onnas 'MARK[u11]') ; folders: $(find "$T/nas" -maxdepth 2 -mindepth 2 | sed "s|$T/nas/||" | tr '\n' ' ')"; done

say; say "### B12b FRIDAY seat as shipped in SEATS (clients General, forbid [], no other-client names): what does it carry?"
seatfix friday FRIDAY; FT="$T/vol/FRIDAY"
plant "$FT/own.md" v0; plant "$FT/x/Datasec/a.md" v1; plant "$FT/x/Secuura/a.md" v2; plant "$FT/x/tuesday/a.md" v3; plant "$FT/4_Credentials/k" v4
mkdir -p "$T/vol/CODING/Datasec/p" "$T/vol/CODING/Secuura/p"; plant "$T/vol/CODING/Datasec/p/a.md" v5; plant "$T/vol/CODING/Secuura/p/a.md" v6
sconf friday "set=General|FRIDAY|$FT" "set=General|CODING/Datasec|$T/vol/CODING/Datasec" "set=General|CODING/Secuura|$T/vol/CODING/Secuura"
rc=$(srun FRIDAY r); say "run rc=$rc ($(/usr/bin/grep -c 'GOOD:' "$T/out/r.txt") GOOD line)"
report "own file (control)" v0; report "Datasec folder inside the tree" v1; report "Secuura folder inside the tree" v2; report "tuesday folder inside the tree" v3; report "4_Credentials" v4
report "set= pointed at the Datasec client folder" v5; report "set= pointed at the Secuura client folder" v6
say "the shipped friday.conf says: $(/usr/bin/grep -c '^status=unconfirmed' "$LANE/seats/friday.conf") status=unconfirmed line (the tool refuses it until someone edits that line)"
