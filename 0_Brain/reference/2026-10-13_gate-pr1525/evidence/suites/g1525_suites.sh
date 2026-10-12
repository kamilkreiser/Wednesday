#!/bin/zsh
set -u
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad
WT=$S/g1525_head; O=$WT/Blockchain/Dev/services/originate; F=$O/src/routes/certifications.ts; REL=Blockchain/Dev/services/originate/src/routes/certifications.ts
L=$S/g1525_logs/suites; mkdir -p $L
source $S/g1525_pg/pg.env
trap 'git -C $WT checkout -q -- $REL' EXIT TERM
for src in base head; do
  if [ $src = base ]; then git -C $WT show 69878dc5d1ae4b717834c547c47d8bc036625d2e:$REL > $F; else git -C $WT checkout -q -- $REL; fi
  echo "== src=$src sha16=$(shasum -a 256 $F | cut -c1-16)"
  ( builtin cd $O && npx jest ks1538-legacy-certify-needs-document-access.test.ts > $L/${src}_unit.log 2>&1 ); echo "unit rc=$? $(grep -m1 'Tests:' $L/${src}_unit.log)"
  for mt in false true; do
    ( builtin cd $O && MULTI_TENANCY_ENABLED=$mt npx jest --config jest.integration.config.js ks1538-legacy-certify-needs-document-access > $L/${src}_integ_mt$mt.log 2>&1 ); echo "integ MT=$mt rc=$? $(grep -m1 'Tests:' $L/${src}_integ_mt$mt.log)"
  done
done
git -C $WT checkout -q -- $REL; echo "final sha16=$(shasum -a 256 $F | cut -c1-16)"
( builtin cd $O && npx jest > $L/head_originate_full.log 2>&1 ); echo "full originate unit jest rc=$? $(grep -E '^Test Suites:|^Tests:' $L/head_originate_full.log | tr '\n' ' ')"
