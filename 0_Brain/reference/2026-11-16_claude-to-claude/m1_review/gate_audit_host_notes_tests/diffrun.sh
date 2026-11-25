#!/bin/bash
# QA-AUDIT-HOST-NOTES item 4: the previous check's three schedule sets, same seed, one tree after the other.
W=/private/tmp/claude-501/qahn
for T in "$@"; do
  echo "== $T start $(date '+%F %T'); heavy jobs of others: $(ps -axo command | grep -E '^bash .*(check\.sh|red-controls[^ ]*\.sh|test-p1p\.sh|test-daemon\.sh)' | sort -u | wc -l)"
  ONLY=""; [ "$T" = abl ] && ONLY=Seal
  mkdir -p $W/scratch/$T
  QAHN_ONLY=$ONLY COAGENT_AUDIT_HOST_SCRATCH=$W/scratch/$T QA_CLONE=$W/$T CARGO_TARGET_DIR=$W/target/$T \
    python3 -B $W/bin/run.py cargo test --release --locked -p coagent-audit-host --lib -- \
    tests::qahn::qahf_exhaustive_singles_and_pairs tests::qahn::qahf_persistent_rules tests::qahn::qahf_generated \
    --exact --nocapture --test-threads 1 > $W/logs/diff_$T.log 2>&1
  echo "== $T rc=$? end $(date '+%F %T')"
done
