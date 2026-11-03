#!/bin/bash
# Independent bash consumer for the spoof cells (reads /usr/bin/env after set -a, so a printf override cannot fool it),
# root-entry ADMIN control with no repo-root .env, and the unexpected git-status entry. Counts/labels only.
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989/harness/lib.sh
M=gate173rmt
for id in sp0 sp1 sp2 sp3; do
  f=$SCR/q2-$id/Blockchain/Dev/.env
  out=$(cd $W/tmp && env -i PATH=/usr/bin:/bin bash -c 'set -a; . "$1" >/dev/null 2>&1; /usr/bin/env' _ "$f" 2>/dev/null)
  printf '%s: after the run, bash set -a + /usr/bin/env: NODE_ENV=production lines=%s, DATABASE_URL lines naming the remote marker=%s; file now has ADMIN set=%s\n' "$id" \
    "$(grep -c '^NODE_ENV=production$' <<<"$out")" "$(grep -c "^DATABASE_URL=.*$M" <<<"$out")" "$([[ -n "$(valof $f ADMIN_USER_PASSWORD)" ]] && echo y || echo n)"
done
c=$SCR/q2-idem
echo "ra0 control (no repo-root .env, clone q2-idem): $(cd $c && env -i PATH=$GPATH HOME=$W/home docker compose -f docker-compose.local.yml config --format json 2>/dev/null | node $W/harness/rootadmin.js "$NM" "$c/Blockchain/Dev/.env")"
echo "git status entries in q2-idem: $(git -C $c status --porcelain | tr '\n' ' ')"
