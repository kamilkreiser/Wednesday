# usage: bash /private/tmp/claude-501/qrr2/ev.sh <tree dir> <target name> <command...>
# Runs a command with the project's toolchain (links), COAGENT_TOOLS and a per-tree CARGO_TARGET_DIR inside the work dir.
set -u
TREE="$1"; TGT="$2"; shift 2
export COAGENT_TOOLS=/private/tmp/claude-501/qrr2/tools
export CARGO_TARGET_DIR=/private/tmp/claude-501/qrr2/t/$TGT
. "$TREE/scripts/env.sh"
exec "$@"
