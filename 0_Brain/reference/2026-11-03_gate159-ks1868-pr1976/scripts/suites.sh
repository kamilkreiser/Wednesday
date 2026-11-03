#!/bin/bash
# Whole anchoring unit suite at head, base, develop (sequential; the probe file is excluded where present).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
for side in head base dev; do
  echo "== $side start $(date +%T)"
  bash "$W/scripts/vt.sh" "$side" "suite_$side" --exclude '**/zz_gate159_probe.test.ts' --exclude '**/node_modules/**' --exclude '**/dist/**' --exclude 'src/__tests__/**/*.integration.test.ts'
  echo "== $side end $(date +%T)"
done
touch "$W/logs/suites.done"
