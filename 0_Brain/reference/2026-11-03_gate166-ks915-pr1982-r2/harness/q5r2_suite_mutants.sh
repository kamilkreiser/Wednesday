#!/bin/bash
# Q5: the PR's own suite at head, red-first without the script, and mutants on the refusal predicates.
set -uo pipefail
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate166-ks915-pr1982-r2
R=$W/repo
MUT=$W/mut/trees; mkdir -p "$MUT"
L=$W/runs/q5r2; mkdir -p "$L"
ORIG=$R/Blockchain/Dev/scripts/restore-local-secrets.sh
echo "script sha256 at head: $(shasum -a 256 "$ORIG" | cut -c1-12)"

mktree() {  # mktree NAME -> minimal tree the suite needs; script left out (caller adds)
  local t="$MUT/$1"; [[ -e "$t" ]] && { echo "EXISTS $t" >&2; return 1; }
  mkdir -p "$t/Blockchain/Dev/scripts/__tests__" "$t/Blockchain/Dev/services/auth/src/repositories"
  cp "$R/.gitignore" "$t/"
  cp "$R/Blockchain/Dev/env.example" "$R/Blockchain/Dev/.env.local.example" "$R/Blockchain/Dev/docker-compose.yml" "$t/Blockchain/Dev/"
  cp "$R/Blockchain/Dev/services/auth/src/repositories/userRepo.ts" "$t/Blockchain/Dev/services/auth/src/repositories/"
  cp "$R/Blockchain/Dev/scripts/bootstrap-env.sh" "$R/Blockchain/Dev/scripts/stack_env.sh" "$t/Blockchain/Dev/scripts/"
  cp "$R/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh" "$t/Blockchain/Dev/scripts/__tests__/"
  echo "$t"
}
suite() {  # suite TREE LOG -> "rc pass fail fatal"
  local t="$1" log="$2" rc
  ( cd "$W/tmp" && env -i HOME="$W/home" PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin TMPDIR="$W/tmp" \
      bash "$t/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh" ) > "$log" 2>&1; rc=$?
  echo "rc=$rc ok=$(grep -c '^ok ' "$log") FAIL=$(grep -c '^FAIL ' "$log") FATAL=$(grep -c FATAL "$log")"
}

echo "== suite at PR head, in the clone =="
( cd "$W/tmp" && env -i HOME="$W/home" PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin TMPDIR="$W/tmp" \
    bash "$R/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh" ) > "$L/head.log" 2>&1
echo "head: rc=$? ok=$(grep -c '^ok ' "$L/head.log") FAIL=$(grep -c '^FAIL ' "$L/head.log") $(tail -1 "$L/head.log")"

echo "== red-first: same suite, script absent =="
t=$(mktree redfirst) && echo "redfirst: $(suite "$t" "$L/redfirst.log")"


echo "== red on round 1: same head suite, script from 411f8e1e =="
t=$(mktree red411) && git -C "$R" show 411f8e1ea760dfc01048cd0d11519b8271b2a2aa:Blockchain/Dev/scripts/restore-local-secrets.sh > "$t/Blockchain/Dev/scripts/restore-local-secrets.sh" && echo "red411: $(suite "$t" "$L/red411.log")"
echo "== mutants (harness/mutants_r2.py) =="
for m in "$W"/mut/scripts/*.sh; do
  name=$(basename "$m" .sh)
  t=$(mktree "$name") || continue
  cp "$m" "$t/Blockchain/Dev/scripts/restore-local-secrets.sh"; chmod 755 "$t/Blockchain/Dev/scripts/restore-local-secrets.sh"
  res=$(suite "$t" "$L/$name.log")
  if [[ "$res" == rc=0* ]]; then verdict=SURVIVED; else verdict=killed; fi
  echo "$name: $verdict ($res) first-fail: $(grep -m1 '^FAIL ' "$L/$name.log" | cut -c1-110)"
done
