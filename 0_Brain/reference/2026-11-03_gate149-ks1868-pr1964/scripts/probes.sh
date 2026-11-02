#!/bin/bash
# probe matrix: {base,head} x {development,production}, then {merged,devnow} (develop's two originate product changes swapped in), sha-restored.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate149-ks1868-pr1964
R=$W/repo; O=$R/Blockchain/Dev/services/originate; T=$R/Blockchain/Dev/node_modules/.bin/tsx; REL=Blockchain/Dev/services/originate
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
git -C $R show 4d1ab2cb6574:$REL/src/routes/documents.ts > $O/src/routes/documents.gate_base.ts
P1=src/services/errorTrackingService.ts; P2=src/utils/lifecyclePayloadCodec.ts; H1=$(sha $O/$P1); H2=$(sha $O/$P2); HD=$(sha $O/src/routes/documents.ts)
: > $W/logs/probe/probes.rc
run(){ nice -n 5 $T $W/scripts/probe.ts $1 $2 $W/logs/probe/$1_$2.jsonl > $W/logs/probe/$1_$2.out 2>&1; echo "rc=$? $1 $2" >> $W/logs/probe/probes.rc; }
for v in base head; do for e in development production; do run $v $e; done; done
for p in $P1 $P2; do git -C $R show 26955bf1b828:$REL/$p > $O/$p; done
for v in merged devnow; do for e in development production; do run $v $e; done; done
for p in $P1 $P2; do git -C $R show pr1964:$REL/$p > $O/$p; done
mv $O/src/routes/documents.gate_base.ts $W/logs/_quarantine/documents.gate_base.ts
{ [ "$(sha $O/$P1)" = "$H1" ] && [ "$(sha $O/$P2)" = "$H2" ] && [ "$(sha $O/src/routes/documents.ts)" = "$HD" ] && echo "probes restore OK" || echo "probes RESTORE FAIL"; git -C $R status --short; } > $W/logs/probe/probes_restore.log
date > $W/logs/probe/probes.done
