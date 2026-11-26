#!/bin/bash
Q=/private/tmp/claude-501/qana
date "+start %F %T"; echo "heavy counter: $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh)"
bash $Q/r.sh $Q/c $Q/t cargo build --workspace --bins --locked > $Q/logs/full_build.log 2>&1; echo "build rc=$?"
bash $Q/r.sh $Q/c $Q/t cargo test -p coagent-daemon -p coagent-mcp -p coagent-audit-host --locked --no-fail-fast > $Q/logs/full_test.log 2>&1; echo "test rc=$?"
date "+end %F %T"
