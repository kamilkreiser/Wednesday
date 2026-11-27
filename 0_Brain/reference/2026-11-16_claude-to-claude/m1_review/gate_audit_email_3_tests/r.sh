#!/bin/bash
# usage: r.sh <dir> <target dir> <cmd...>  (the cd happens here; own tools; toolchain pinned from the copy's rust-toolchain.toml)
D="$1"; T="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qae3/tools CARGO_TARGET_DIR="$T"
cd "$D" || exit 99
. scripts/env.sh
export RUSTUP_TOOLCHAIN="$(sed -n 's/^channel *= *"\(.*\)"/\1/p' rust-toolchain.toml)"
exec "$@"
