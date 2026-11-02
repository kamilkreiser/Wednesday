#!/usr/bin/env bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937
R=$W/repo
S=$W/scratch_bootstrap
[ -e "$S" ] && { echo "scratch exists"; exit 9; }
mkdir -p "$S"
for side in base head; do
  ref=8f313815f415; [ $side = head ] && ref=pr1937
  D=$S/$side/Blockchain/Dev
  mkdir -p $D/scripts
  cp $R/Blockchain/Dev/scripts/bootstrap-env.sh $R/Blockchain/Dev/scripts/stack_env.sh $D/scripts/
  git -C $R show $ref:Blockchain/Dev/env.example > $D/env.example
  git -C $R show $ref:Blockchain/Dev/.env.example > $D/.env.example
  git -C $R show $ref:Blockchain/Dev/.env.local.example > $D/.env.local.example 2>/dev/null
  ( env -u SECUURA_STACK_SLOT -u STACK_SLOT bash $D/scripts/bootstrap-env.sh > $S/$side.out 2>&1 ); echo "$side bootstrap rc=$?"
  grep -E '^[A-Za-z_][A-Za-z0-9_]*=' $D/.env | cut -d= -f1 | sort > $S/$side.keys
  wc -l < $S/$side.keys
done
echo "--- key-set diff base vs head (names only)"
diff $S/base.keys $S/head.keys
echo "--- classification of the five keys (empty/nonempty/absent)"
for k in ADMIN_USER_PASSWORD ENABLE_DEMO_SEED ALLOW_DEFAULT_SEED_PASSWORDS TSA_URL TSA_AUTH_KEY; do
  for side in base head; do
    f=$S/$side/Blockchain/Dev/.env
    if grep -q "^$k=" $f; then v=$(grep "^$k=" $f | head -1 | cut -d= -f2-); [ -z "$v" ] && c=EMPTY || c=NONEMPTY; else c=ABSENT; fi
    echo "$k $side $c"
  done
done
