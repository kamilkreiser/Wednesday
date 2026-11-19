#!/bin/bash
# The core red-control runner on the clean clone (old rows must stay RED).
export COAGENT_TOOLS=<work>/mc/tools CARGO_TARGET_DIR=<work>/mc/target
pushd <work>/mc/clone >/dev/null || exit 9
bash scripts/red-controls-core.sh > <work>/core.log 2>&1
echo "CORE exit $?" >> <work>/core.log
