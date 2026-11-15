export GIT_OPTIONAL_LOCKS=0 GIT_TERMINAL_PROMPT=0 GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-15_drafter-seatB178
C=$D/clone_work/clone
args=()
for n in 2220 2221 2222 2098 2079 2223 2224 2081 2230 2089 2228; do args+=("+refs/pull/$n/head:refs/remotes/pr/$n"); done
git -C $C -c credential.helper= -c 'credential.helper=!gh auth git-credential' fetch --quiet --no-tags origin +refs/heads/develop:refs/remotes/origin/develop "${args[@]}"
echo fetch rc=$?
git -C $C rev-parse origin/develop
