#!/bin/bash
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934; R=$D/repo
RUN=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1413_o76_p1_start_banners_no_demo_password/out.md.checker
S=$D/scratch_identity; test ! -e $S || exit 1; mkdir -p $S
P="Start_Up/start-secuura.sh Blockchain/Dev/scripts/start-local.sh Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh"
git -C $R archive 8f313815f415 $P | tar -x -C $S
(cd $S
for k in 1 2 3 4; do git apply --check -p1 $RUN/section_$k.diff; echo "check $k rc=$?"; git apply -p1 $RUN/section_$k.diff; echo "apply $k rc=$?"; done
git apply -p1 --check $RUN/section_1.diff; echo "reapply control rc=$? (expect nonzero)")
for f in $P Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh; do
  a=$(shasum -a 256 $S/$f | cut -c1-16); b=$(git -C $R show pr1934:$f | shasum -a 256 | cut -c1-16)
  [ "$a" = "$b" ] && echo "EQUAL $f $a" || echo "DIFFER $f $a $b"
done
git -C $R ls-tree pr1934 Start_Up/start-secuura.sh Blockchain/Dev/scripts/start-local.sh
git -C $R ls-tree 8f313815f415 Start_Up/start-secuura.sh Blockchain/Dev/scripts/start-local.sh
