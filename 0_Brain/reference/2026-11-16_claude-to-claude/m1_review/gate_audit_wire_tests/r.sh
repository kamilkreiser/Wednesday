#!/bin/bash
# usage: r.sh <clone dir> <target dir> <cmd...>   (cd inside, env from scripts/env.sh, own tools)
D="$1"; T="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qaw/tools CARGO_TARGET_DIR="$T"
cd "$D" || exit 99
. scripts/env.sh
exec "$@"
