#!/bin/bash
# run.sh <tree dir> <target name> cmd... : the tree's env.sh environment, own target dir per tree.
T="$1"; N="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qwf/tools
export CARGO_TARGET_DIR=/private/tmp/claude-501/qwf/t/$N
. "$T/scripts/env.sh"
exec env -C "$T" "$@"
