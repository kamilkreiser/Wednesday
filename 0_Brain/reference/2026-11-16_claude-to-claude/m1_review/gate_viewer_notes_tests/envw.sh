# usage: . envw.sh <tree> <target-subdir>
export COAGENT_TOOLS=/private/tmp/claude-501/qvn/tools CARGO_TARGET_DIR=/private/tmp/claude-501/qvn/$2
. "$1/scripts/env.sh"
