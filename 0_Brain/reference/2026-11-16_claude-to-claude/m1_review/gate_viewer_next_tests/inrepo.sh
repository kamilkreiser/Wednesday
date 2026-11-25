#!/bin/bash
# usage: inrepo.sh <repo dir> <target dir> cmd... ; runs cmd with cwd=<repo dir> (via incwd.py, no cd) and the project's toolchain env (QA-VIEWER-NEXT).
R="$1"; T="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qvx/tools CARGO_TARGET_DIR="$T"
. "$R/scripts/env.sh"
exec python3 -B /private/tmp/claude-501/qvx/s/incwd.py "$R" "$@"
