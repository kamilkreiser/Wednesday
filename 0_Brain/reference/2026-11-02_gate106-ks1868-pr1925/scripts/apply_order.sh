#!/bin/bash
# Strict sequential apply of the held sections, both orders, at two bases, in throwaway worktrees inside my clone; compare with PR head.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate106-ks1868-pr1925
R=$W/repo; RUNS=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs
want(){ case $1 in o70_p1) echo f3d965f1683788f7c8abae89701701681959335f9c7cfa00453966845bed8a30;; o70_p2) echo 2376d93a963f57cbe829dba12a9e67e480e96d80aa06c48922a04df41695052b;; o66_p1) echo ab35ce3e838a5217e75a67118233c2a5e83aab955c31952fa06bfb26d896ffc0;; esac; }
dir(){ ls -d $RUNS/spark_secuura_2026-11-02_ks_1868_${1}_* | grep -v -- '-control$' | head -1; }
for p in o70_p2 o70_p1 o66_p1; do
  C=$(dir $p)/out.md.checker; s=$(shasum -a 256 $C/patch.diff | awk '{print $1}')
  echo "$p patchsha_ok=$([ "$s" = "$(want $p)" ] && echo yes || echo NO) sections_concat_equal=$(cat $C/section_1.diff $C/section_2.diff | cmp -s - $C/patch.diff && echo yes || echo NO) control_dir_patch_equal=$(cmp -s $C/patch.diff $(dir $p)-control/out.md.checker/patch.diff && echo yes || echo NO)"
done
HEADTREE=$(git -C $R rev-parse pr1925^{tree}); echo "PR head tree $HEADTREE"
for BASE in fcfa5dfdba9b5fe1b4a7c4619403ff3d0e2fe54c 04ff5262ad526a13c1a0df99480b76860a8d11d1; do
 for ORDER in "o70_p2 o70_p1 o66_p1" "o70_p1 o70_p2 o66_p1"; do
  WT=$W/apply_wt; test -e $WT && { echo "worktree path exists"; exit 2; }
  git -C $R worktree add -q --detach $WT $BASE
  echo "BASE ${BASE:0:12} ORDER [$ORDER]"
  for p in $ORDER; do C=$(dir $p)/out.md.checker
    for k in 1 2; do f=$C/section_$k.diff
      out=$(git -C $WT apply --check -p1 $f 2>&1); rc=$?; echo "  $p s$k check rc=$rc out=[$out]"
      out2=$(git -C $WT apply -v -p1 $f 2>&1 | /usr/bin/grep -i -E "offset|fuzz|error" ); git -C $WT apply -p1 $f 2>/dev/null; true
      [ -n "$out2" ] && echo "  $p s$k notes: $out2"
    done
  done
  git -C $WT add -A >/dev/null; T=$(git -C $WT write-tree); echo "  tree $T"
  git -C $WT diff --cached --quiet pr1925 -- Blockchain/Dev && echo "  SERVICE TREE EQUALS PR HEAD (Blockchain/Dev)" || echo "  SERVICE TREE DIFFERS"
  git -C $WT diff --cached --stat pr1925 | tail -2
  git -C $WT diff --cached --quiet $BASE -- Blockchain/Dev && echo "  control: equals base (instrument dead)" || echo "  control: differs from base (instrument fires)"
  git -C $R worktree remove --force $WT
 done
done
