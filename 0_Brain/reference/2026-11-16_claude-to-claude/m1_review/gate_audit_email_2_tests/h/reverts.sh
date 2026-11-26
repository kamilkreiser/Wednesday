#!/bin/bash
# usage: reverts.sh <plant>...  : tree f_<plant> = git archive 5aa56e1 + ONE edit (plant.py), tests untouched; own empty target tf_<plant>;
# runs the redactor-asserting targets of the builder's tests: ae2_email ae_email redaction gate_attacks gate_r2
Q=/private/tmp/claude-501/qae2
for n in "$@"; do
  D=$Q/f_$n; T=$Q/tf_$n
  if [ ! -e $D ]; then mkdir -p $D && git -C $Q/c archive 5aa56e1 | tar -x -C $D && python3 -B $Q/h/plant.py $D $n > /dev/null; fi
  diff -u $Q/ph/crates/coagent-audit/src/redact.rs $D/crates/coagent-audit/src/redact.rs > $Q/logs/revert_$n.diff
  find $D/crates -name '*.rs' -exec touch {} +
  mkdir -p $T; L=$Q/logs/revert_$n.log
  echo "revert $n redact.rs $(shasum -a 256 $D/crates/coagent-audit/src/redact.rs | cut -c1-64) $(date +%T)" > $L
  bash $Q/r.sh $D $T cargo test --locked -p coagent-audit --no-fail-fast --test ae2_email --test ae_email --test redaction --test gate --test gate_r2 >> $L 2>&1; echo "exit=$? $(date +%T)" >> $L
  echo "$n compiled=$(grep -c 'Compiling coagent-audit ' $L) $(grep -c '^test result: FAILED' $L) failed-targets; $(tail -1 $L)"
done
