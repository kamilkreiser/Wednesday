#!/bin/bash
# QA-W-DAEMON: the Windows type-check and clippy gate, kit method (W-0). Usage: wincheck.sh <tree> <target dir> <log prefix>
T="$1"; TD="$2"; L="$3"
W=/private/tmp/claude-501/qwd
export COAGENT_TOOLS=$W/tools CARGO_TARGET_DIR="$TD"
. "$T/scripts/env.sh"
export PATH="$W/tools/xwin-kit/bin:$PATH" XWIN_CACHE_DIR=/Volumes/Laptop-DEV/coagent-xwin-cache CARGO_NET_OFFLINE=true
M="--manifest-path $T/Cargo.toml"
env -C "$T" cargo xwin check --locked $M --target x86_64-pc-windows-msvc -p coagent-daemon > "$L.a.log" 2>&1; echo "(a) exit $?" | tee -a "$L.a.log"
env -C "$T" cargo xwin check --locked $M --target x86_64-pc-windows-msvc -p coagent-daemon --lib --bins --test win_rules --test win_datadir --test win_guest > "$L.b.log" 2>&1; echo "(b) exit $?" | tee -a "$L.b.log"
env -C "$T" cargo xwin clippy --locked $M --target x86_64-pc-windows-msvc -p coagent-daemon --lib --bins --test win_rules --test win_datadir --test win_guest -- -D warnings > "$L.c.log" 2>&1; echo "(clippy) exit $?" | tee -a "$L.c.log"
