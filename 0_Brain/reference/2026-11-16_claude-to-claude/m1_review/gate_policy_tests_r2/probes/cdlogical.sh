#!/bin/bash
# Probe: does the shell's `cd ..` after a symlinked directory go to the LOGICAL parent?
# Only creates and reads scratch files.
P=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy_r2/probe
mkdir -p "$P/root/ws/a/b/c" "$P/root/home/.aws"
echo FAKE-CRED > "$P/root/home/.aws/credentials"
ln -sfn "$P/root/ws/a/b/c" "$P/root/ws/l"
T='cd ./l && cd ../.. && pwd && cat home/.aws/credentials'
echo "== zsh: $T"; /bin/zsh -f -c "builtin cd $P/root/ws && $T"
echo "== zsh: cd ./l/.. && pwd"; /bin/zsh -f -c "builtin cd $P/root/ws && cd ./l/.. && pwd"
echo "== bash: $T"; /bin/bash -c "builtin cd $P/root/ws && $T"
echo "== physical: realpath of l/../.. ="; /usr/bin/python3 -I -c "import os;print(os.path.realpath('$P/root/ws/l/../..'))"
