export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB175
C=$D/clone_work/clone
export GIT_AUTHOR_NAME=drafter GIT_AUTHOR_EMAIL=d@example.invalid GIT_COMMITTER_NAME=drafter GIT_COMMITTER_EMAIL=d@example.invalid
export GIT_INDEX_FILE=$D/clone_work/idx_r118_$(date +%s)
DEV=$(git -C $C rev-parse origin/develop)
git -C $C read-tree $DEV
git -C $C apply --cached $D/r118new.patch; echo apply rc=$?
T=$(git -C $C write-tree); echo tree $T
CM=$(git -C $C commit-tree $T -p $DEV -m "scratch r118 analog")
unset GIT_INDEX_FILE
git -C $C update-ref refs/remotes/pr/r118an $CM; echo commit $CM
