#!/bin/bash
# Round-2 env: named re-runs, tsc/eslint, probes base/head, mutants. Sequential (host load is high).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
echo "== RE-RUN threadTokenMint alone at head (suite2_head cell timed out at 60 s under load)"
bash "$W/scripts/vt3.sh" head rerun_threadTokenMint_head src/__tests__/threadTokenMint.test.ts
grep -m2 -E 'Unsupported type|timed out' "$W/logs/rerun_threadTokenMint_head.log"
echo "== pool-listener file alone, head and dev"
for s in head dev; do bash "$W/scripts/vt3.sh" $s rerun_poollistener_$s src/__tests__/ks1868-anchoring-db-pool-error-listener-unreadable-throw.test.ts; done
echo "== tsc / eslint (wt2)"
sed -e 's#/wt_\$side/#/wt2_$side/#g' -e 's#/wt_c1#/wt2_c1#g' -e 's#/wt_head/#/wt2_head/#g' -e 's#logs/tsc_#logs/tsc2_#g' -e 's#logs/eslint_#logs/eslint2_#g' "$W/scripts/tsc_eslint.sh" > "$W/scripts/tsc_eslint2.sh"
bash "$W/scripts/tsc_eslint2.sh" 2>&1 | grep -v 'error TS' | cut -c1-400
for s in base c1 head; do grep 'error TS' "$W/logs/tsc2_tests_$s.log" | sed -E "s#.*/wt2_$s/##" | sort > "$W/logs/tsc2_tests_$s.norm"; done
echo "tsc2 base-vs-head:"; diff "$W/logs/tsc2_tests_base.norm" "$W/logs/tsc2_tests_head.norm" && echo IDENTICAL
echo "tsc2 c1-vs-head:"; diff "$W/logs/tsc2_tests_c1.norm" "$W/logs/tsc2_tests_head.norm"
cat "$W/logs/tsc2_tests_head.norm"
echo "== probes (wt2)"
bash "$W/scripts/run_probe3.sh" head probe2_head
bash "$W/scripts/run_probe3.sh" base probe2_base
python3 -I "$W/scripts/analyse.py" "$W/logs/probe2_base.jsonl" "$W/logs/probe2_head.jsonl" > "$W/logs/analyse2_base_head.log" 2>&1
tail -1 "$W/logs/analyse2_base_head.log"; grep -E '^DIFF' "$W/logs/analyse2_base_head.log" | awk '{print $2,$3}'
echo "== mutants (wt2_mut)"
python3 -I "$W/scripts/mutants.py"
touch "$W/logs/round2_rest.done"
