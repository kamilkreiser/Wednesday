#!/bin/bash
# xwin.sh <tree> <target name> cargo-xwin args... : the kit method (no install, offline, own target dir).
T="$1"; N="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qwf/tools
export CARGO_TARGET_DIR=/private/tmp/claude-501/qwf/t/$N
. "$T/scripts/env.sh"
export XWIN_CACHE_DIR=/Volumes/Laptop-DEV/coagent-xwin-cache CARGO_NET_OFFLINE=true
export PATH="$COAGENT_TOOLS/xwin-kit/bin:$PATH"
exec env -C "$T" cargo xwin "$@"
