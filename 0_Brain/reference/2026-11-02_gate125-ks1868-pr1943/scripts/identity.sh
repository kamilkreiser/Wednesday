#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate125-ks1868-pr1943
R=$W/repo
RUN=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_a6_originate_certification_repo_list_and_shares_catches_unreadable_throw/out.md.checker
S=$W/scratch_base
test -e $S && { echo scratch exists; exit 1; }
mkdir -p $S
git -C $R archive e2a2426d221d -- Blockchain/Dev/services/originate/src | tar -x -C $S
for k in 1 2; do ( patch -p1 -d $S --dry-run < $RUN/section_$k.diff; echo dry$k rc=$? ) ; done
for k in 1 2; do ( patch -p1 -d $S < $RUN/section_$k.diff; echo apply$k rc=$? ) ; done
P=Blockchain/Dev/services/originate/src/repositories/certificationRepo.ts
T=Blockchain/Dev/services/originate/src/__tests__/ks1868-certification-repo-list-and-shares-catches-o79p6-unreadable-throw.test.ts
echo "held product    $(shasum -a 256 < $S/$P)"
echo "commit1 product $(git -C $R show db76eec6:$P | shasum -a 256)"
echo "head   product  $(git -C $R show pr1943:$P | shasum -a 256)"
echo "held test       $(shasum -a 256 < $S/$T)"
echo "commit1 test    $(git -C $R show db76eec6:$T | shasum -a 256)"
echo "head test       $(git -C $R show pr1943:$T | shasum -a 256)"
echo "patch.diff == cat sections:"; cat $RUN/section_1.diff $RUN/section_2.diff | cmp - $RUN/patch.diff; echo cmp rc=$?
echo "commit2 diff:"; git -C $R diff db76eec6 pr1943 --numstat; git -C $R diff db76eec6 pr1943 -U0 | /usr/bin/grep '^[+-]' 
echo "commit1 vs held on non-code files:"; git -C $R diff --stat e2a2426d221d db76eec6 | tail -6
