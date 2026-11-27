#!/bin/bash
# (f) source mutants: tree = git archive 6274318 (fetch-only repo) + ONE edit to src/redact.rs (tests untouched, every .rs touched),
# own EMPTY target dir; run the six redactor-asserting targets; log kept. Usage: mutants_f.sh <name>... (env RED=<cfg name> optional)
Q=/private/tmp/claude-501/qae3
for N in "$@"; do
  D=$Q/f_$N; T=$Q/tf_$N
  [ -e "$D" ] || [ -e "$T" ] && { echo "exists $D or $T"; exit 5; }
  mkdir -p $D && git -C $Q/gho archive 627431877d5fa3b86f91ec23d0dc2879c800eb33 | tar -x -C $D || exit 3
  python3 -B $Q/h/plant.py $D $N > /dev/null || exit 4
  diff -u <(git -C $Q/gho show 6274318:crates/coagent-audit/src/redact.rs) $D/crates/coagent-audit/src/redact.rs > $Q/logs/mut_$N.diff
  L=$Q/logs/mut_$N.log
  echo "mutant $N redact.rs $(shasum -a 256 $D/crates/coagent-audit/src/redact.rs | cut -c1-64) red=${RED:-none} start $(date +%T)" > $L
  if [ -n "$RED" ]; then export COAGENT_AUDIT_RED=$RED; else unset COAGENT_AUDIT_RED; fi
  bash $Q/r.sh $D $T cargo test --locked -p coagent-audit --no-fail-fast --test ae3_email --test ae2_email --test ae_email --test redaction --test gate --test gate_r2 >> $L 2>&1
  echo "exit=$? end $(date +%T)" >> $L
  echo "$N: compiling-audit=$(grep -c 'Compiling coagent-audit ' $L) failed-tests=$(grep -E '^test .* FAILED$' $L | sed 's/^test //; s/ \.\.\. FAILED//' | tr '\n' ' ') $(tail -1 $L)"
done
