export GIT_OPTIONAL_LOCKS=0 GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config" GIT_TERMINAL_PROMPT=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatB176
C=$D/clone_work/clone
args=""
for n in 2095 2090 2098 2089 2079 2220 2221 2222 2223 2224 2225 2228 2099 2160 2227; do args="$args +refs/pull/$n/head:refs/remotes/pr/$n"; done
git -C $C -c credential.helper= -c 'credential.helper=!gh auth git-credential' fetch --quiet --no-tags origin +refs/heads/develop:refs/remotes/origin/develop $args
echo fetch rc=$?
git -C $C rev-parse origin/develop
