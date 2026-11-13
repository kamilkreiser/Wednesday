export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172
git -C $D/clone fetch --quiet --no-tags "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-r118-ks1699" +HEAD:refs/remotes/pr/r118
echo rc=$?
git -C $D/clone rev-parse refs/remotes/pr/r118
