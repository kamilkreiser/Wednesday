#!/usr/bin/env bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937
R=$W/repo
S=$W/scratch_mut
[ -e "$S" ] && { echo "scratch exists"; exit 9; }
mkdir -p $S/base/Blockchain/Dev/scripts/__tests__ $S/head/Blockchain/Dev/scripts/__tests__
T=Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh
for side in base head; do
  ref=8f313815f415; [ $side = head ] && ref=pr1937
  git -C $R show $ref:Blockchain/Dev/env.example > $S/$side/Blockchain/Dev/env.example
  git -C $R show $ref:Blockchain/Dev/docker-compose.yml > $S/$side/Blockchain/Dev/docker-compose.yml
  git -C $R show pr1937:$T > $S/$side/$T
done
echo "== red-first: new suite vs BASE templates"; bash $S/base/$T; echo "rc=$?"
echo "== head"; bash $S/head/$T | tail -3; echo "rc=${PIPESTATUS[0]}"
echo "== mutants (remove one line from head env.example)"
E=$S/head/Blockchain/Dev/env.example
orig=$(shasum -a 256 $E | cut -d' ' -f1)
for k in ADMIN_USER_PASSWORD ENABLE_DEMO_SEED ALLOW_DEFAULT_SEED_PASSWORDS TSA_URL TSA_AUTH_KEY; do
  cp $E $E.orig
  grep -vxF "$k=" $E.orig > $E
  out=$(bash $S/head/$T 2>&1); rc=$?
  echo "-$k : rc=$rc  $(echo "$out" | grep -E 'passed' ) ; red cells: $(echo "$out" | grep '^FAIL' | sed 's/FAIL //' | tr '\n' '|')"
  cp $E.orig $E
  [ "$(shasum -a 256 $E | cut -d' ' -f1)" = "$orig" ] && echo "  restore OK" || echo "  RESTORE BAD"
done
echo "== extra mutants"
# M6 value made non-empty (placeholder) - should be red
cp $E $E.orig; sed -i.bak 's/^TSA_URL=$/TSA_URL=x/' $E; out=$(bash $S/head/$T 2>&1); echo "TSA_URL=x : rc=$? $(echo "$out"|grep passed)"; cp $E.orig $E
# M7 commented out
sed -i.bak 's/^ADMIN_USER_PASSWORD=$/# ADMIN_USER_PASSWORD=/' $E; out=$(bash $S/head/$T 2>&1); echo "ADMIN commented : $(echo "$out"|grep passed)"; cp $E.orig $E
# M8 blank password replaced by a non-empty value (the case that matters: seeded admin)
sed -i.bak 's/^ADMIN_USER_PASSWORD=$/ADMIN_USER_PASSWORD=changeme/' $E; out=$(bash $S/head/$T 2>&1); echo "ADMIN=nonempty : $(echo "$out"|grep passed)"; cp $E.orig $E
# M9 compose default dropped
C=$S/head/Blockchain/Dev/docker-compose.yml; cp $C $C.orig
sed -i.bak 's/\${TSA_AUTH_KEY:-}/${TSA_AUTH_KEY}/' $C; out=$(bash $S/head/$T 2>&1); echo "compose TSA_AUTH_KEY default dropped : $(echo "$out"|grep passed)"; cp $C.orig $C
[ "$(shasum -a 256 $E | cut -d' ' -f1)" = "$orig" ] && echo "final restore OK"
