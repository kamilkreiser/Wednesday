#!/bin/bash
# Strict apply of each held O74 diff at base cd9c4a7, alone and combined, in temp indexes (read-tree resets them); compare blobs to PR head.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930
R=$W/repo; H=$W/evidence/held; T=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a974be12-1abe-4d9a-9532-9c46296d28fc/scratchpad
for s in p1 p2 p3 p4 p5; do
  export GIT_INDEX_FILE=$T/idx_$s
  git -C $R read-tree cd9c4a7dd3b87f4810d16b40352a63330d1d6793
  git -C $R apply --cached --verbose $H/o74_$s.diff > $W/logs/held_alone_$s.log 2>&1; echo "alone $s rc=$?"
  grep -i "offset\|fuzz\|error" $W/logs/held_alone_$s.log
done
export GIT_INDEX_FILE=$T/idx_all
git -C $R read-tree cd9c4a7dd3b87f4810d16b40352a63330d1d6793
for s in p1 p2 p3 p4 p5; do git -C $R apply --cached --verbose $H/o74_$s.diff > $W/logs/held_comb_$s.log 2>&1; echo "combined $s rc=$?"; grep -i "offset\|fuzz" $W/logs/held_comb_$s.log; done
echo "-- blobs: combined-held vs PR head"
git -C $R ls-files -s Blockchain/Dev/services/security/src | awk '{print $2, $4}' | sort -k2 > $T/held_blobs
unset GIT_INDEX_FILE
git -C $R ls-tree -r pr1930 Blockchain/Dev/services/security/src | awk '{print $3, $4}' | sort -k2 > $T/pr_blobs
diff $T/held_blobs $T/pr_blobs > $W/logs/held_vs_pr_diff.log; echo "blob diff rc=$? (0 = identical over all services/security/src files)"
wc -l < $T/pr_blobs
for f in index.ts db.ts; do echo "$(grep " Blockchain/Dev/services/security/src/$f\$" $T/held_blobs) | PR $(grep " Blockchain/Dev/services/security/src/$f\$" $T/pr_blobs)"; done
grep ks1868 $T/held_blobs
echo "-- control: corrupt one context line of p2"
export GIT_INDEX_FILE=$T/idx_ctl
git -C $R read-tree cd9c4a7dd3b87f4810d16b40352a63330d1d6793
sed '0,/^ .*rethrow/s/rethrow/rethroW/' $H/o74_p2.diff > $T/o74_p2_bad.diff
cmp -s $T/o74_p2_bad.diff $H/o74_p2.diff && echo "CONTROL NOT CORRUPTED"
git -C $R apply --cached $T/o74_p2_bad.diff > $W/logs/held_control.log 2>&1; echo "corrupted p2 rc=$?"
