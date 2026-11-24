#!/bin/bash
# usage: t_rustenv.sh <file-under-test> <label>   (own fixture; reads the real tools folder only through a symlink)
F="$1"; L="$2"; W=/private/tmp/claude-501/qwt/fx_$L; REAL="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools"
rm -rf "$W" 2>/dev/null; mkdir -p "$W"
mk() { # $1 = proj dir
  mkdir -p "$1/2_Project_Files/spikes/lib" "$1/worktrees/x/spikes/lib"; ln -s "$REAL" "$1/tools"
  cp "$F" "$1/2_Project_Files/spikes/lib/rustenv.sh"; cp "$F" "$1/worktrees/x/spikes/lib/rustenv.sh"; }
mk "$W/proj"; mk "$W/sp ace/proj"
ln -s "$W/proj/worktrees/x/spikes/lib" "$W/linkdir"
ln -s "$W/proj/worktrees/x/spikes/lib/rustenv.sh" "$W/linkfile.sh"
ln -s "$W/proj" "$W/projlink"   # a symlink to the PROJECT folder (logical path stays inside the project)
run() {
  env -i HOME=/nonexistent PATH=/usr/bin:/bin "$1" -c "$2; . \"$3\"; echo rc=\$?; echo C=\$CARGO_HOME; echo R=\$RUSTUP_HOME; echo T=\$CARGO_TARGET_DIR; cargo --version 2>&1 | head -1" 2>&1; }
for sh in bash zsh; do for pre in ":" "set -u" "set -e" "set -eu"; do for p in \
  "$W/proj/2_Project_Files/spikes/lib/rustenv.sh" "$W/proj/worktrees/x/spikes/lib/rustenv.sh" \
  "$W/sp ace/proj/worktrees/x/spikes/lib/rustenv.sh" "$W/linkdir/rustenv.sh" "$W/linkfile.sh" "$W/projlink/worktrees/x/spikes/lib/rustenv.sh"; do
  echo "### $L $sh [$pre] ${p#$W/}"; run $sh "$pre" "$p"; done; done; done
echo "##### NO TOOLCHAIN"; mkdir -p "$W/neg/a/spikes/lib"; cp "$F" "$W/neg/a/spikes/lib/rustenv.sh"
for sh in bash zsh; do echo "### neg $sh"; env -i HOME=/nonexistent PATH=/usr/bin:/bin $sh -c ". '$W/neg/a/spikes/lib/rustenv.sh'; echo rc=\$?; printf 'C=<%s> R=<%s> T=<%s> PATH=%s\\n' \"\$CARGO_HOME\" \"\$RUSTUP_HOME\" \"\$CARGO_TARGET_DIR\" \"\$PATH\"; env | grep -c '^_coagent' " 2>&1; done
