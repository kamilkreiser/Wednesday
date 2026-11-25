#!/bin/bash
# QA-AUDIT-HOST-NOTES item 9: the Windows type-check in one tree, own target, the xwin cache copied into the work dir.
W=/private/tmp/claude-501/qahn
TREE="$1"; TAG="$2"
export QA_CLONE="$TREE" CARGO_TARGET_DIR=$W/target/win-$TAG XWIN_CACHE_DIR=$W/xwin-cache
export PATH="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/tools/xwin-kit/bin:$PATH"
for what in --lib --all-targets; do
  python3 -B $W/bin/run.py cargo xwin check --locked --offline --target x86_64-pc-windows-msvc -p coagent-audit-host $what > $W/logs/win_${TAG}_${what#--}.log 2>&1
  echo "$TAG $what rc=$?"
done
