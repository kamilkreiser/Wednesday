#!/bin/bash
# Q1c: do the .env shapes / URL forms the script ACCEPTS actually resolve to the remote host
# in the real consumers? Test files hold only crafted test lines (no generated values).
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate165-ks915-pr1982
NM="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules"
D=$W/runs/q1c; mkdir -p "$D"
M=gate165rmt
CASES=(
  "export DATABASE_URL=postgres://u:p@$M.host/x"
  "  DATABASE_URL=postgres://u:p@$M.host/x"
  "DATABASE_URL = postgres://u:p@$M.host/x"
  "DATABASE_URL: postgres://u:p@$M.host/x"
  "DATABASE_URL=postgres://u:p@localhost:6432/x"$'\n'"DATABASE_URL=postgres://u:p@$M.host/x"
  "NODE_ENV=production # live"
  "export NODE_ENV=production"
  "NODE_ENV= production"
  "NODE_ENV=development"$'\n'"NODE_ENV=production"
  "  NODE_ENV=production"
)
printf '%-4s %-22s %-22s %-22s | %s\n' id dotenv-16.6.1 bash-set-a compose-v5-config case
i=0
for c in "${CASES[@]}"; do
  i=$((i+1)); f="$D/c$i.env"; printf '%s\n' "$c" > "$f"
  dn=$(node -e '
    const d=require(process.argv[1]+"/dotenv"); const fs=require("fs");
    const o=d.parse(fs.readFileSync(process.argv[2]));
    const u=o.DATABASE_URL||""; const n=o.NODE_ENV;
    console.log(u ? (u.includes(process.argv[3])?"DB=remote":"DB=local") : (n!==undefined ? "NODE_ENV="+JSON.stringify(n) : "unset"));' "$NM" "$f" "$M" 2>&1 | tail -1)
  bs=$(env -i PATH=/usr/bin:/bin bash -c 'set -a; . "$1" 2>/dev/null; if [[ -n "${DATABASE_URL:-}" ]]; then [[ "$DATABASE_URL" == *"$2"* ]] && echo DB=remote || echo DB=local; elif [[ -n "${NODE_ENV+x}" ]]; then echo "NODE_ENV=\"$NODE_ENV\""; else echo unset-or-error; fi' _ "$f" "$M")
  printf 'services:\n  probe:\n    image: busybox\n    environment:\n      - DATABASE_URL=${DATABASE_URL:-}\n      - NODE_ENV=${NODE_ENV:-}\n' > "$D/compose.yml"
  cf=$(env -i PATH=/Users/kamilkreiser/.docker/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home DOCKER_CONFIG=/Users/kamilkreiser/.docker docker compose -p gate165probe --env-file "$f" -f "$D/compose.yml" config 2>&1)
  if grep -q "DATABASE_URL: postgres" <<<"$cf"; then
    cs=$(grep -q "$M" <<<"$cf" && echo DB=remote || echo DB=local)
  elif grep -q 'NODE_ENV: ' <<<"$cf"; then cs="NODE_ENV=$(grep 'NODE_ENV: ' <<<"$cf" | head -1 | sed 's/.*NODE_ENV: //')"
  else cs="unset/err:$(head -c 40 <<<"$cf" | tr '\n' ' ')"; fi
  printf '%-4s %-22s %-22s %-22s | %q\n' "c$i" "$dn" "$bs" "$cs" "$c"
done

echo
echo "== pg-connection-string 2.12.0 / pg 8.20.0 on the URL forms the script accepted =="
for u in "postgres://u:p@localhost:5432,$M.host:5432/x" "postgres://u:p@[::1],$M.host/x" "postgres://u:p@[::1]$M.com/x" \
         "postgres://u:p@localhost/x?h%6Fst=$M.host" "postgres://u:p@localhost/x?host%3D$M.host"; do
  node -e '
    const {parse}=require(process.argv[1]+"/pg-connection-string");
    let r; try { const c=parse(process.argv[2]); r="host="+JSON.stringify(c.host)+" remote="+String(JSON.stringify(c).includes(process.argv[3])) } catch(e) { r="THROWS "+e.code+" "+e.message.slice(0,50) }
    console.log(r.padEnd(60)+" | "+process.argv[2]);' "$NM" "$u" "$M"
done
