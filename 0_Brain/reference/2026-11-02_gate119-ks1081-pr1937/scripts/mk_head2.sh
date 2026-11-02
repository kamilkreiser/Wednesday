W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937
[ -e $W/head2_tree ] && { echo exists; exit 9; }
git -C $W/repo worktree add --detach $W/head2_tree pr1937 2>&1 | tail -1
npm --prefix $W/head2_tree/Blockchain/Dev/services/auth ci --ignore-scripts > $W/logs/npm_ci_auth.log 2>&1; echo "npm ci rc=$?"
tail -3 $W/logs/npm_ci_auth.log
