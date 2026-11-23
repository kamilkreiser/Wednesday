#!/bin/bash
# usage: inrepo.sh <repo dir> <target dir> cmd... ; runs cmd in a subshell inside the repo with the project's toolchain env.
R="$1"; T="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qla2/tools CARGO_TARGET_DIR="$T"
( cd "$R" && . scripts/env.sh && "$@" )
