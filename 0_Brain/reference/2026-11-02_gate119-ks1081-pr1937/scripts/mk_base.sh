W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937
[ -e $W/base_tree ] && { echo exists; exit 9; }
git -C $W/repo worktree add --detach $W/base_tree 8f313815f415 2>&1 | tail -2
git -C $W/base_tree rev-parse HEAD
ls $W/repo/Blockchain/Dev/scripts/__tests__/*.test.sh | wc -l
ls $W/base_tree/Blockchain/Dev/scripts/__tests__/*.test.sh | wc -l
