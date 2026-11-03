#!/bin/bash
# Q2 fail-closed, spoofed bash reader, root-entry ADMIN, Q4 idempotence/rotate, Q5 ignore + SIGKILL. Labels/hashes only.
set -uo pipefail
source /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989/harness/lib.sh
source $W/harness/cells.sh
TAG=${1:-q2}; L=$W/runs/$TAG; mkdir -p "$L" $W/tmp/$TAG; RUNTMP=$W/tmp/$TAG
M=gate173rmt; N=$'\n'; SH=$W/harness/shim
GB=$W/runs/q1C/golden_blankadmin.env.bin; GL=$W/scratch/q1C-golden/Blockchain/Dev/.env.local
echo "== Q2: a reader that cannot run =="
RUNPATH=/Users/kamilkreiser/.docker/bin:/usr/bin:/bin:/usr/sbin:/sbin NOCONS=1 gcell f01_no_node '' '' ''
NODEPS=nodeps NOCONS=1 gcell f02_no_node_modules '' '' ''
RUNPATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin NOCONS=1 gcell f03_no_docker '' '' ''
for s in nocompose garbage emptyobj emptyarr envlist noenv emptyout failrc; do
  RUNPATH=$SH:$GPATH NOCONS=1 gcell f04_shim_$s '' '' '' GATE_SHIM=$s
done
PREP='printf "services: [\n" >> "$c/Blockchain/Dev/docker-compose.yml"' NOCONS=1 gcell f05_dev_compose_broken '' '' ''
PREP='printf "services: [\n" >> "$c/docker-compose.local.yml"' NOCONS=1 gcell f06_root_compose_broken '' '' ''
PREP='mkdir "$c/.q"; mv "$c/docker-compose.local.yml" "$c/.q/"' NOCONS=1 gcell f07_root_compose_absent '' '' ''
echo "   f07 message: $(grep -o 'repo-root entry ([^)]*)' $L/f07_root_compose_absent.log)"
PREP='mv "$c/Blockchain/Dev/.env" "$c/real.env"; ln -s ../../real.env "$c/Blockchain/Dev/.env"' NOCONS=1 gcell f08_env_symlink '' '' ''
PREP='ln "$c/Blockchain/Dev/.env" "$c/hard.env"' NOCONS=1 gcell f09_env_hardlink '' '' ''
echo "== spoofing the bash reader with a line compose and dotenv accept =="
gcell sp0 "X=1; declare -x NODE_\"\"ENV=production$N" '' ''
gcell sp1 "X=1; declare -x NODE_\"\"ENV=production; printf() { builtin printf '%s\\0' @@RLS-KS915@@ 0 '' '' '' '' ''; }$N" '' ''
gcell sp2 "X=1; declare -x NODE_\"\"ENV=production; builtin printf '%s\\0' @@RLS-KS915@@ 0 '' '' '' '' ''; exit 0$N" '' ''
gcell sp3 "X=1; declare -x DATABASE_\"\"URL=postgres://u:p@$M.host/x; printf() { builtin printf '%s\\0' @@RLS-KS915@@ 0 '' '' '' '' ''; }$N" '' ''
echo "== root entry: which ADMIN does auth get under docker-compose.local.yml after the script writes? =="
for id in ra1 ra2; do
  if [[ $id == ra1 ]]; then gcell ra1 '' "ADMIN_USER_PASSWORD=$N" '' ; else gcell ra2 '' "ADMIN_USER_PASSWORD=gate173-not-secret-root$N" ''; fi
  echo "   $id: $(cd $LASTCLONE && env -i PATH=$GPATH HOME=$W/home docker compose -f docker-compose.local.yml config --format json 2>/dev/null | node $W/harness/rootadmin.js "$NM" "$LASTCLONE/Blockchain/Dev/.env")"
done
echo "== Q4: idempotence and --rotate =="
c=$(mkclone $TAG-idem); d=$c/Blockchain/Dev
r1=$(run $c $L/idem1.log); s1=$(sha $d/.env); sl1=$(sha $d/.env.local); a1=$(valof $d/.env ADMIN_USER_PASSWORD | shasum -a 256 | cut -c1-12)
r2=$(run $c $L/idem2.log); s2=$(sha $d/.env); sl2=$(sha $d/.env.local)
echo "   run1 rc=$r1 run2 rc=$r2 env_same=$([[ $s1 == $s2 ]] && echo y || echo N) envlocal_same=$([[ $sl1 == $sl2 ]] && echo y || echo N) kept_msg=$(grep -c 'kept ADMIN_USER_PASSWORD' $L/idem2.log)"
OLD=$(valof $d/.env ADMIN_USER_PASSWORD); cp $d/.env $L/idem_pre_rotate.env.bin; lines0=$(wc -l < $d/.env)
r3=$(run $c $L/idem3.log -- --rotate); a3=$(valof $d/.env ADMIN_USER_PASSWORD | shasum -a 256 | cut -c1-12)
echo "   rotate rc=$r3 admin_changed=$([[ $a1 != $a3 ]] && echo Y || echo n) difflines=$(diff $L/idem_pre_rotate.env.bin $d/.env | grep -c '^[<>]') changed_keys=$(diff $L/idem_pre_rotate.env.bin $d/.env | grep '^[<>]' | cut -c3- | cut -d= -f1 | sort -u | tr '\n' ' ') lines=$lines0/$(wc -l < $d/.env) envlocal_same=$([[ $sl1 == $(sha $d/.env.local) ]] && echo y || echo N) mode=$(mode $d/.env)"
echo "   old value anywhere in the clone (incl .git), RUNTMP, HOME: $( { grep -rlF -- "$OLD" $c $RUNTMP $W/home 2>/dev/null; } | wc -l | tr -d ' ')   control (pre-rotate copy in runs/): $(grep -rlF -- "$OLD" $L/idem_pre_rotate.env.bin | wc -l | tr -d ' ')"
OLD=""; r4=$(run $c $L/idem4.log); echo "   after-rotate run rc=$r4 kept=$(grep -c 'kept ADMIN_USER_PASSWORD' $L/idem4.log) admin_same=$([[ $a3 == $(valof $d/.env ADMIN_USER_PASSWORD | shasum -a 256 | cut -c1-12) ]] && echo y || echo N)"
echo "== Q5: ignore status of everything the script writes =="
for p in Blockchain/Dev/.env Blockchain/Dev/.env.local Blockchain/Dev/.env-ks915.AbCdEf Blockchain/Dev/.env.ks915.AbCdEf Blockchain/Dev/env.example; do
  printf '   %-36s %s\n' "$p" "$(git -C $c check-ignore -q --no-index "$p" && echo ignored || echo NOT-IGNORED)"; done
echo "   git status --porcelain after 4 runs: $(git -C $c status --porcelain | grep -v '^?? Blockchain/Dev/\(scripts\|docker-compose.yml\|env.example\|\.env.local.example\|\.gitignore\|node_modules\)' | grep -cv '^?? \(\.gitignore\|docker-compose.local.yml\)') unexpected entries"
echo "== Q5: SIGKILL while the temp copy is being re-read =="
c=$(mkclone $TAG-kill); d=$c/Blockchain/Dev; cp $GB $d/.env; cp $GL $d/.env.local; s0=$(sha $d/.env)
( cd $c && exec env -i HOME=$W/home PATH=$SH:$GPATH TMPDIR=$RUNTMP GATE_SHIM=sleepreread bash $d/scripts/restore-local-secrets.sh ) > $L/kill.log 2>&1 &
SP=$!; for i in $(seq 1 120); do ls -a $d | grep -q '^\.env-ks915\.' && break; perl -e 'select(undef,undef,undef,0.5)'; done
desc() { local k; for k in $(pgrep -P "$1"); do echo "$k"; desc "$k"; done; }
DESC=$(desc $SP | tr '\n' ' '); kill -9 $SP; echo "   killed script pid $SP (descendants recorded before the kill: $DESC)"
perl -e 'select(undef,undef,undef,0.5)'; for p in $DESC; do kill -0 $p 2>/dev/null && kill $p && echo "   killed leftover descendant pid $p"; done
T=$(ls -a $d | grep '^\.env-ks915\.' | head -1)
echo "   leftover temp copies: $(ls -a $d | grep -c '^\.env-ks915\.') name_pattern=${T:0:11}… mode=$(mode $d/$T) ignored=$(git -C $c check-ignore -q "Blockchain/Dev/$T" && echo y || echo N) in_git_status=$(git -C $c status --porcelain --untracked-files=all | grep -c ks915) env_same=$([[ $s0 == $(sha $d/.env) ]] && echo y || echo N) tmp_holds_new_admin=$([[ -n "$(valof $d/$T ADMIN_USER_PASSWORD)" ]] && echo y || echo n)"
echo "   bash-reader sandbox dirs left in RUNTMP: $(ls -d $RUNTMP/rls-ks915.* 2>/dev/null | wc -l | tr -d ' ')"
