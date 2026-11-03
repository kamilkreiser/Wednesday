#!/bin/bash
# D3 extra: whitespace / escape sequences inside the URL query that the WHATWG parser behind
# pg-connection-string strips, plus F9 (.env.local symlink), a hardlink, and ADMIN last-blank.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2/harness/lib.sh
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
TAG=d3e; L=$W/runs/$TAG; mkdir -p "$L" "$W/tmp/e" "$W/home/e"; M=gate166rmt
run() {  # same as lib.sh run, own HOME/TMPDIR so a concurrent suite is not disturbed
  local root="$1" log="$2"; shift 2
  ( cd "$root" && env -i HOME="$W/home/e" PATH="$GPATH" TMPDIR="$W/tmp/e" "$@" bash "$root/Blockchain/Dev/scripts/restore-local-secrets.sh" ) >"$log" 2>&1; echo $?
}
GB=$W/runs/d3C/golden_blankadmin.env.bin
consumers() {  # consumers FILE -> dotenv / bash / compose-probe pg host
  local f="$1" a b c
  a=$(node -e 'const d=require(process.argv[1]+"/dotenv");const {parse}=require(process.argv[1]+"/pg-connection-string");const u=d.parse(require("fs").readFileSync(process.argv[2])).DATABASE_URL;let h;try{h=String(parse(u).host)}catch(e){h="THROWS"};process.stdout.write(h.includes(process.argv[3])?"REMOTE":"local")' "$NM" "$f" "$M")
  b=$(env -i PATH=/usr/bin:/bin bash -c 'set -a; . "$1" >/dev/null 2>&1; printf %s "${DATABASE_URL:-}"' _ "$f")
  b=$(node -e 'const {parse}=require(process.argv[1]+"/pg-connection-string");let h;try{h=String(parse(process.argv[2]).host)}catch(e){h="THROWS"};process.stdout.write(h.includes(process.argv[3])?"REMOTE":"local")' "$NM" "$b" "$M")
  printf 'services:\n  probe:\n    image: busybox\n    environment:\n      - DATABASE_URL=${DATABASE_URL:-}\n' > "$L/probe.yml"
  c=$(env -i PATH=/Users/kamilkreiser/.docker/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/scratch/chome DOCKER_CONFIG=/Users/kamilkreiser/.docker docker compose -p gate166probe --env-file "$f" -f "$L/probe.yml" config --format json 2>/dev/null | python3 -I -c 'import json,sys
try: print(json.load(sys.stdin)["services"]["probe"]["environment"].get("DATABASE_URL") or "")
except Exception: print("")')
  c=$(node -e 'const {parse}=require(process.argv[1]+"/pg-connection-string");let h;try{h=String(parse(process.argv[2]).host)}catch(e){h="THROWS"};process.stdout.write(h.includes(process.argv[3])?"REMOTE":"local")' "$NM" "$c" "$M")
  echo "consumers: dotenv=$a bash=$b compose=$c"
}
shellcell() {  # shellcell ID URL
  local c rc t0 t1; c="$(mkclone $TAG-$1)" || return; cp "$GB" "$c/Blockchain/Dev/.env"; chmod 644 "$c/Blockchain/Dev/.env"
  t0=$(treesum "$c"); rc=$(run "$c" "$L/$1.log" "DATABASE_URL=$2"); t1=$(treesum "$c")
  local h; h=$(node -e 'const {parse}=require(process.argv[1]+"/pg-connection-string");let h;try{h=String(parse(process.argv[2]).host)}catch(e){h="THROWS"};process.stdout.write(h)' "$NM" "$2")
  printf '%-4s shell rc=%s tree_same=%s admin_now_set=%s pg_host_contains_marker=%s | %q\n' "$1" "$rc" "$([[ $t0 == $t1 ]] && echo y || echo N)" \
    "$([[ -n "$(valof "$c/Blockchain/Dev/.env" ADMIN_USER_PASSWORD)" ]] && echo y || echo n)" "$([[ $h == *$M* ]] && echo y || echo n)" "$2"
}
envcell() {  # envcell ID LINE
  local c e rc t0 t1; c="$(mkclone $TAG-$1)" || return; e="$c/Blockchain/Dev/.env"
  { cat "$GB"; printf '%s\n' "$2"; } > "$e"; chmod 644 "$e"; cp "$e" "$L/$1.pre.env.bin"
  t0=$(treesum "$c"); rc=$(run "$c" "$L/$1.log"); t1=$(treesum "$c")
  printf '%-4s .env  rc=%s tree_same=%s admin_now_set=%s %s | %q\n' "$1" "$rc" "$([[ $t0 == $t1 ]] && echo y || echo N)" \
    "$([[ -n "$(valof "$e" ADMIN_USER_PASSWORD)" ]] && echo y || echo n)" "$(consumers "$L/$1.pre.env.bin")" "$2"
}
echo "== query names with whitespace / escapes (WHATWG strips TAB, LF, CR) =="
shellcell e01 $'postgres://u:p@localhost/x?ho\tst='"$M.host"
shellcell e02 $'postgres://u:p@localhost/x?host\t='"$M.host"
shellcell e03 $'postgres://u:p@localhost/x?ho\rst='"$M.host"
envcell  e11 "DATABASE_URL=\"postgres://u:p@localhost/x?ho\\nst=$M.host\""
envcell  e12 "DATABASE_URL=\"postgres://u:p@localhost/x?ho\\tst=$M.host\""
envcell  e13 $'DATABASE_URL=postgres://u:p@localhost/x?ho\tst='"$M.host"
envcell  e14 "DATABASE_URL=\"postgres://u:p@localhost/x?ho\\rst=$M.host\""
echo "== control: plain ?host= in .env (instrument fires) =="
envcell  e19 "DATABASE_URL=postgres://u:p@localhost/x?host=$M.host"

echo "== F9: .env.local symlinked to a file outside Blockchain/Dev =="
c="$(mkclone $TAG-f9l)"; d="$c/Blockchain/Dev"; cp "$GB" "$d/.env"; chmod 644 "$d/.env"; tgt="$c/outside_local.env"
cp "$W/repo/Blockchain/Dev/.env.local.example" "$tgt"; chmod 644 "$tgt"; ln -s ../../outside_local.env "$d/.env.local"; s0=$(sha "$d/.env"); ts0=$(sha "$tgt")
rc=$(run "$c" "$L/f9l.log"); echo "f9l rc=$rc env_same=$([[ $s0 == $(sha "$d/.env") ]] && echo y || echo N) env_mode=$(mode "$d/.env") target_same=$([[ $ts0 == $(sha "$tgt") ]] && echo y || echo N) target_mode=$(mode "$tgt") still_link=$([[ -L $d/.env.local ]] && echo y || echo n) names_link=$(grep -c 'symbolic link' "$L/f9l.log")"
echo "== hardlinked .env (same inode as a file outside Blockchain/Dev), complete =="
c="$(mkclone $TAG-hl)"; d="$c/Blockchain/Dev"; tgt="$c/outside_hard.env"; cp "$W/runs/d3C/golden_blankadmin.env.bin" "$tgt"
printf 'ADMIN_USER_PASSWORD=gate166-not-secret-hl\nALLOW_DEFAULT_SEED_PASSWORDS=true\nNODE_ENV=development\n' >> "$tgt"; chmod 644 "$tgt"; ln "$tgt" "$d/.env"
rc=$(run "$c" "$L/hl.log"); echo "hardlink rc=$rc outside_target_mode=$(mode "$tgt") links=$(stat -f %l "$tgt")"
echo "== ADMIN set then blank (last wins in every consumer) =="
c="$(mkclone $TAG-ab)"; e="$c/Blockchain/Dev/.env"; grep -v '^ADMIN_USER_PASSWORD=' "$GB" > "$e"
printf 'ADMIN_USER_PASSWORD=gate166-not-secret-ab\nADMIN_USER_PASSWORD=\nALLOW_DEFAULT_SEED_PASSWORDS=true\n' >> "$e"; s0=$(sha "$e")
rc=$(run "$c" "$L/ab.log"); last=$(node -e 'const d=require(process.argv[1]+"/dotenv");process.stdout.write(d.parse(require("fs").readFileSync(process.argv[2])).ADMIN_USER_PASSWORD?"set":"blank")' "$NM" "$e")
echo "admin-last-blank rc=$rc file_same=$([[ $s0 == $(sha "$e") ]] && echo y || echo N) msg=$(grep -oE '(generated|kept|rotated) ADMIN_USER_PASSWORD' "$L/ab.log" | tr ' ' _) dotenv_reads_admin=$last"
