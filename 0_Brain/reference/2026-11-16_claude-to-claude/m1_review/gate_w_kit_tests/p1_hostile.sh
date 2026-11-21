#!/bin/bash
# QA-W-KIT probes 4b and 5 (no build is started by any of these; every case must exit before the per-program loop)
W=/private/tmp/claude-501/qwk
SRC=$W/clone
B=$SRC/scripts/windows/build.sh
mkdir -p $W/hostile && cd_unused=1
# fresh tools root with only the links, so any write is visible
T2=$W/hostile/tools2; mkdir -p $T2/cargo; ln -sfn "$W/tools/cargo/bin" $T2/cargo/bin; ln -sfn "$W/tools/rustup" $T2/rustup; ln -sfn "$W/tools/xwin-kit" $T2/xwin-kit
snap() { find $T2 $W/hostile/empty_cache "$W/hostile/sp ace" 2>/dev/null | grep -v '/cargo/bin$\|/rustup$\|/xwin-kit$' | sort; }
mkdir -p $W/hostile/empty_cache
echo "== P4b: empty cache + --offline"; snap > $W/hostile/s0.txt
COAGENT_TOOLS=$T2 XWIN_CACHE_DIR=$W/hostile/empty_cache bash $B --offline </dev/null; echo "exit=$?"; snap | diff $W/hostile/s0.txt - && echo "NOTHING WRITTEN (tools2 + empty cache unchanged)"
echo "== P5a: cache path with a space"
COAGENT_TOOLS=$T2 XWIN_CACHE_DIR="$W/hostile/sp ace/c" bash $B </dev/null; echo "exit=$?"; ls -d "$W/hostile/sp ace" 2>&1; snap | diff $W/hostile/s0.txt - && echo "NOTHING WRITTEN"
echo "== P5a2: space + --offline"
COAGENT_TOOLS=$T2 XWIN_CACHE_DIR="$W/hostile/sp ace/c" bash $B --offline </dev/null; echo "exit=$?"
