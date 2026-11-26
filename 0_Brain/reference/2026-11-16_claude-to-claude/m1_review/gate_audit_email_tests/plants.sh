#!/bin/bash
# usage: plants.sh <name>...   name = p1..p7 (scratch copies) or cfg:<red name> (head copy ph built red)
Q=/private/tmp/claude-501/qae
for n in "$@"; do
  case "$n" in
    cfg:*) red=${n#cfg:}; dir=ph; tgt=$Q/t_$red; export COAGENT_AUDIT_RED=$red; tag=$red ;;
    *) dir=$n; tgt=$Q/t$n; unset COAGENT_AUDIT_RED; tag=$n ;;
  esac
  mkdir -p $tgt; L=$Q/logs/plant_$tag
  find $Q/$dir/crates -name '*.rs' -exec touch {} +
  bash $Q/r.sh $Q/$dir $tgt cargo test --locked -p coagent-audit --test ae_email --no-fail-fast > $L.ae_email.log 2>&1; echo "exit=$?" >> $L.ae_email.log
  QAE_IN=$Q/corp/c1.hex QAE_OUT=$Q/corp/c1.$tag.out bash $Q/r.sh $Q/$dir $tgt cargo test --locked -p coagent-audit --test qae_probe -- --exact qae_dump --nocapture > $L.probe.log 2>&1; echo "exit=$?" >> $L.probe.log
  echo "$tag done $(date +%H:%M:%S) compiled-audit=$(grep -c 'Compiling coagent-audit ' $L.ae_email.log) red-build=$(grep -c 'RED CONTROL BUILD' $L.ae_email.log)"
done
