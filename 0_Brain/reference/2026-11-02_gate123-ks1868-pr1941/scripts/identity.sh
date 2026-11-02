#!/bin/bash
# held-patch identity: sha, containment, section concat, strict apply at base e2a2426d in two orders, compare to PR head tree.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate123-ks1868-pr1941; R=$W/repo; L=$W/logs
RUNS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs; NIGHT=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night
MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
dir(){ case $1 in P3) echo spark_secuura_2026-11-02_ks_1868_o78_p3_originate_verification_v2_chain_fact_catch_unreadable_throw;; B1) echo spark_secuura_2026-11-02_ks_1868_o79_b1_originate_verification_verify_hash_status_guards_coerce_message;; B2) echo spark_secuura_2026-11-02_ks_1868_o79_b2_originate_verification_verify_file_guard_coerces_message;; B3) echo spark_secuura_2026-11-02_ks_1868_o79_b3_originate_verification_v2_guards_coerce_message;; esac; }
sha_(){ case $1 in P3) echo 5a79e4d9f1ee9c6cd1bd45b146666b96599a580fb7d2a91c4067bdbfc3dd507c;; B1) echo 65d01d25909528a2567e5c7fc43629ca48cdb86d5e9bc1001f8d0cf810ba191a;; B2) echo fdedc33d876274dc734b46d9ea2c7f63d6894d49b1b60b9a1e554a92756a3f1d;; B3) echo b2b221fa36249554952909d1d1db41a9a2217f2c201ef25730fd0917853979a0;; esac; }
held(){ case $1 in P3) echo READY_KS-1868-KS-1868-O78-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-VERIFICATION-V2-CHAIN-FACT-CATCH-PASS-7of7-PASS-7of7_2026-11-02.diff.md;; B1) echo READY_KS-1868-KS-1868-O79-B1_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFICATION-VERIFY-HASH-STATUS-COERCE-PASS-7of7_2026-11-02.diff.md;; B2) echo READY_KS-1868-KS-1868-O79-B2_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFICATION-VERIFY-FILE-COERCE-PASS-7of7_2026-11-02.diff.md;; B3) echo READY_KS-1868-KS-1868-O79-B3_spark-dsv4flash_BRIEFED-CODEPATCH2-VERIFICATION-V2-COERCE-PASS-7of7_2026-11-02.diff.md;; esac; }
for k in P3 B3 B1 B2; do
  P=$RUNS/$(dir $k)/out.md.checker
  s=$(shasum -a 256 $P/patch.diff | cut -d' ' -f1); [ "$s" = "$(sha_ $k)" ] && sm=SHA_OK || sm="SHA_MISMATCH $s"
  c=$(python3 -I -c 'import sys; print(open(sys.argv[1],"rb").read() in open(sys.argv[2],"rb").read())' $P/patch.diff $NIGHT/$(held $k))
  n=$(ls $P | /usr/bin/grep -c '^section_[0-9]*\.diff$')
  cat $P/section_1.diff $P/section_2.diff | cmp -s - $P/patch.diff && cc=CONCAT_EQ || cc=CONCAT_DIFF
  echo "$k $sm contained=$c sections=$n $cc"
done
apply_order(){ name=$1; shift; WT=$W/wt_$name; git -C $R worktree add -q --detach $WT $MB || return
  for k in "$@"; do P=$RUNS/$(dir $k)/out.md.checker
    for s in 1 2; do git -C $WT apply --check $P/section_$s.diff > $L/apply_${name}_${k}_$s.chk 2>&1; echo "$name $k s$s check rc=$? out=$(wc -c < $L/apply_${name}_${k}_$s.chk)"; git -C $WT apply -v $P/section_$s.diff > $L/apply_${name}_${k}_$s.out 2>&1; echo "  apply rc=$?; offsets: $(/usr/bin/grep -ic 'offset\|fuzz' $L/apply_${name}_${k}_$s.out)"; done
  done
  git -C $WT add -A; T=$(git -C $WT write-tree); echo "$name tree=$T"
  for p in Blockchain/Dev/services/originate/src/routes/verification.ts Blockchain/Dev/services/originate/src/routes/verificationV2.ts; do a=$(git -C $R rev-parse $T:$p); b=$(git -C $R rev-parse pr1941:$p); [ $a = $b ] && echo "  $p EQ $a" || echo "  $p DIFF $a vs head $b"; done
  for f in $(git -C $R diff --name-only $MB pr1941 -- 'Blockchain/Dev/services/originate/src/__tests__'); do a=$(git -C $R rev-parse $T:$f 2>/dev/null); b=$(git -C $R rev-parse pr1941:$f); [ "$a" = "$b" ] && echo "  test $(basename $f) EQ" || echo "  test $(basename $f) DIFF"; done
  git -C $R diff --stat $T pr1941 > $L/apply_${name}_vs_head.stat; echo "  tree vs head: $(tail -1 $L/apply_${name}_vs_head.stat)"; git -C $R diff --name-only $T pr1941 > $L/apply_${name}_vs_head.names
  git -C $R worktree remove --force $WT
}
apply_order fwd P3 B3 B1 B2
apply_order rev B2 B1 B3 P3
