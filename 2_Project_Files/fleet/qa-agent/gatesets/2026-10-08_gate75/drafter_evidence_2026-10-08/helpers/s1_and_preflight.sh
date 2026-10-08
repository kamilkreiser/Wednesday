#!/bin/bash
set -u
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ba10491f-d904-4eb7-a83b-e46c1bc8cc8e/scratchpad/gate75
K=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-08_gate75
E=$K/drafter_evidence_2026-10-08/runs
W=$S/wtHead
export TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1
unset GIT_SSH_COMMAND
echo "S-1 start $(date -u +%FT%TZ)"
(builtin cd "$W/Blockchain/Dev" && npm ci --ignore-scripts > $E/s1_dev_npmci.out 2> $E/s1_dev_npmci.err); echo "Blockchain/Dev npm ci rc=$?"
(builtin cd "$W/Blockchain/Dev" && npm run build --workspace=packages/shared > $E/s1_shared_build.out 2> $E/s1_shared_build.err); echo "shared build rc=$?"
ls -la "$W/Blockchain/Dev/packages/shared/dist/index.js"
for p in akto api-explorer performance playwright; do (builtin cd "$W/systemTest/$p" && npm ci --ignore-scripts > $E/s1_st_${p}.out 2> $E/s1_st_${p}.err); echo "systemTest/$p npm ci rc=$?"; done
echo "porcelain lines after S-1 (tracked only): $(git -C $W status --porcelain --untracked-files=no | wc -l)"
echo "preflight start $(date -u +%FT%TZ)"
python3 $K/c3_preflight_gate75.py preflight --wt $W --expect-tree 5f456a0128feee7dd4e2f164f08f923f6a136742 --out $E/preflight_head.json > $E/preflight_head.console 2> $E/preflight_head.err
echo "preflight tool rc=$? end $(date -u +%FT%TZ)"
python3 $K/c3_preflight_gate75.py format --wt $W --expect-tree 5f456a0128feee7dd4e2f164f08f923f6a136742 --paths "systemTest/__tests__/no_hardcoded_slot_literals.test.sh,systemTest/schemathesis/config/schemathesis-baseline.json,Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html,Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html" > $E/format_head.console 2> $E/format_head.err
echo "format tool rc=$?"
df -h /Volumes/DevMASTER /System/Volumes/Data
