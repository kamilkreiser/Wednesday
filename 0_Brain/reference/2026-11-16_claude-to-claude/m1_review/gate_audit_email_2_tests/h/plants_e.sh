#!/bin/bash
# usage: plants_e.sh <name>...   name = a source plant of plant.py (copy e_<name> = head + probe + ONE edit) or cfg:<red> (xh built red)
Q=/private/tmp/claude-501/qae2
for n in "$@"; do
  case "$n" in
    cfg:*) red=${n#cfg:}; dir=xh; tag=$red; export COAGENT_AUDIT_RED=$red ;;
    *) dir=e_$n; tag=$n; unset COAGENT_AUDIT_RED
       [ -e $Q/$dir ] || { bash $Q/h/mkcopy.sh $dir 5aa56e1 >/dev/null && python3 -B $Q/h/plant.py $Q/$dir $n >/dev/null && diff -u $Q/xh/crates/coagent-audit/src/redact.rs $Q/$dir/crates/coagent-audit/src/redact.rs > $Q/logs/plant_$n.diff; } ;;
  esac
  tgt=$Q/te_$tag; mkdir -p $tgt
  for c in c1 own lit; do bash $Q/h/probe.sh $dir te_$tag $c $tag > $Q/logs/probe_${tag}_$c.log 2>&1; done
  echo "$tag $(date +%T) compiled=$(grep -c 'Compiling coagent-audit ' $Q/logs/probe_${tag}_c1.log) red-build=$(grep -c 'RED CONTROL BUILD' $Q/logs/probe_${tag}_c1.log) exits=$(grep -h '^exit=' $Q/logs/probe_${tag}_*.log | tr '\n' ' ')"
  for c in c1 own lit; do python3 -I -B $Q/h/qa2_diff.py $Q/corp/$c $Q/corp/$c.base.out $Q/corp/$c.$tag.out ${tag}_$c > $Q/logs/diff_${tag}_$c.txt 2>&1; done
done
