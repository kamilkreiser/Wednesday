#!/bin/bash
# env.sh (head) at main-tree and worktree positions, bash and zsh; fixture proj/tools -> real tools
F=$1; W=/private/tmp/claude-501/qwt/fx_env; REAL="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
rm -rf "$W"; for d in 2_Project_Files worktrees/x; do mkdir -p "$W/proj/$d/scripts"; cp "$F" "$W/proj/$d/scripts/env.sh"; done; ln -s "$REAL" "$W/proj/tools"
for sh in bash zsh; do for d in 2_Project_Files worktrees/x; do echo "### $sh $d"
 env -i HOME=/nonexistent PATH=/usr/bin:/bin $sh -c ". '$W/proj/$d/scripts/env.sh'; echo C=\$CARGO_HOME; echo T=\$CARGO_TARGET_DIR; cargo --version"; done; done
