#!/bin/bash
# Gate 70: everything after the probe chain, strictly one at a time (jest_run.sh waits while load1 > 8).
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884
D=$G/repo/Blockchain/Dev
O=$D/services/originate
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/g70
E=$G/evidence
waitload() { while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; sleep 20; done; }
echo "Q2 start $(date -u +%H:%M:%SZ)"
# 1. probe70 at the head (run 1 failed to compile: TS6133, own instrument; kept as probe70_head_app_run1_TS6133.log)
bash $G/scripts/probe_run.sh $E/probe/gate70-r2b-probe.integration.test.ts probe70_head_app.log 2>&1 | grep -v load1=
# 2. the author's six KS-1384 real-Postgres files, app role
bash $G/scripts/jest_run.sh integ app $E/w_integ_head_app.log 'src/__tests__/ks1384-.*integration' ; echo "w_integ rc=$?"; grep -E "Tests:|Test Suites:" $E/w_integ_head_app.log
# 3. originate unit suite
bash $G/scripts/jest_run.sh unitpar app $E/unit_head_full.log ; echo "unit rc=$?"; grep -E "Tests:|Test Suites:" $E/unit_head_full.log
# 4. anchoring unit and integration
bash $G/scripts/jest_run.sh avunit app $E/anchoring_unit_head.log ; echo "avunit rc=$?"; grep -E "Tests |Test Files" $E/anchoring_unit_head.log
bash $G/scripts/jest_run.sh avinteg app $E/anchoring_integ_head.log ; echo "avinteg rc=$?"; grep -E "Tests |Test Files" $E/anchoring_integ_head.log
# 5. tsc: product, all tests (probes excluded), positive control
waitload; nice -n 10 $D/node_modules/.bin/tsc --noEmit -p $O/tsconfig.json > $E/tsc_head.log 2>&1; echo "rc=$?" >> $E/tsc_head.log; echo "tsc product: $(tail -1 $E/tsc_head.log)"
waitload; nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.alltests.json > $E/tsc_head_with_tests.log 2>&1; echo "rc=$?" >> $E/tsc_head_with_tests.log; echo "tsc tests: $(tail -1 $E/tsc_head_with_tests.log)"
nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.alltests.json --listFilesOnly 2>/dev/null | grep -c "/services/originate/src/__tests__/" > $E/tsc_test_file_count.txt; echo "test files examined: $(cat $E/tsc_test_file_count.txt)"
waitload; nice -n 10 $D/node_modules/.bin/tsc -p $S/tsconfig.control.json > $E/tsc_control.log 2>&1; echo "rc=$?" >> $E/tsc_control.log; echo "tsc control: $(tail -2 $E/tsc_control.log | tr '\n' ' ')"
# 6. mutants (probe70 + W's r2a file, per cell)
nice -n 10 python3 $G/scripts/mutants.py > $E/mutants_run.log 2>&1; echo "mutants rc=$?"; grep -E '"mutant"|baseline' $E/mutants_run.log | cut -c1-400
git -C $G/repo status --short
echo "Q2 DONE $(date -u +%H:%M:%SZ)"
