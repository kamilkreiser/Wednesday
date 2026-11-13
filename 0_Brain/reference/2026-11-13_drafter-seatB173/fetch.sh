export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB173
args=""
for n in 2098 2097 2096 2095 2090 2089 2079 2220 2221 2222 2223 2224 2225 2099 2160; do args="$args +refs/pull/$n/head:refs/remotes/pr/$n"; done
git -C $D/clone fetch --quiet --no-tags origin +refs/heads/develop:refs/remotes/origin/develop $args
echo fetch rc=$?
git -C $D/clone rev-parse origin/develop
git -C $D/clone fetch --quiet --no-tags /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172/clone +refs/remotes/pr/r118:refs/remotes/pr/r118; echo r118 fetch rc=$?
