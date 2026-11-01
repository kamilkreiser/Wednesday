W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate76-ks1868-nft-1891
git -C $W/repo merge-tree --write-tree refs/gate/develop refs/gate/pr1891 > $W/logs/merge_tree.log 2>&1; echo rc $?; cat $W/logs/merge_tree.log
git -C $W/repo rev-parse refs/gate/develop^{tree} refs/gate/pr1891^{tree}
