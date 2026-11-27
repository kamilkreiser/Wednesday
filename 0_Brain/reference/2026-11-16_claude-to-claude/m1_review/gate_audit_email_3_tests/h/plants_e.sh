#!/bin/bash
# (e) planted loosenings: each in its own copy (git archive 6274318 + probe + ONE edit, or a cfg red name) and its own EMPTY target dir; probe over the five corpora
Q=/private/tmp/claude-501/qae3
for P in "$@"; do
  case $P in
    cfg:*) N=${P#cfg:}; D=xh; T=$Q/tp_$N; export COAGENT_AUDIT_RED=$N;;
    *) N=$P; D=e_$N; T=$Q/tp_$N; unset COAGENT_AUDIT_RED
       if [ "$PLANTED" != 1 ]; then bash $Q/h/mkcopy.sh $D 627431877d5fa3b86f91ec23d0dc2879c800eb33 || exit 3; python3 -B $Q/h/plant.py $Q/$D $N || exit 4; fi
       diff -u <(git -C $Q/gho show 6274318:crates/coagent-audit/src/redact.rs) $Q/$D/crates/coagent-audit/src/redact.rs > $Q/logs/plant_$N.diff;;
  esac
  [ -e "$T" ] && { echo "target exists $T"; exit 5; }
  for c in own c2 c1 c3 lit; do
    bash $Q/h/probe.sh $D tp_$N $c pl_$N > $Q/logs/plprobe_${N}_$c.log 2>&1
  done
  echo "$N: Compiling coagent-audit lines $(grep -c 'Compiling coagent-audit ' $Q/logs/plprobe_${N}_own.log); RED CONTROL BUILD lines $(grep -c 'RED CONTROL BUILD' $Q/logs/plprobe_${N}_own.log); probe exits $(grep -h '^exit=' $Q/logs/plprobe_${N}_*.log | cut -d' ' -f1 | sort | uniq -c | tr '\n' ' ')"
done
