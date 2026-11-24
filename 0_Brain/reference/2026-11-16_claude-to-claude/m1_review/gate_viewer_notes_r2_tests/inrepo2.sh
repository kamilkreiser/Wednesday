#!/bin/bash
# usage: inrepo2.sh <repo dir> <target dir> cmd... ; runs cmd with cwd=<repo dir> (via incwd.py, no cd) and the project's toolchain env.
R="$1"; T="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qvn2/tools CARGO_TARGET_DIR="$T"
. "$R/scripts/env.sh"
exec python3 -B /private/tmp/claude-501/qvn2/s/incwd.py "$R" "$@"
