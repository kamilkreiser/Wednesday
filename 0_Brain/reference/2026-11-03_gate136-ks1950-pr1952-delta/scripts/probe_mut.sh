#!/bin/bash
# usage: probe_mut.sh K2|K6 -- the real-PG probe on a gate-made MUTANT of the head product; head restored after (sha asserted by swap.sh)
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta
R=$G/repo; A=$R/Blockchain/Dev/services/governance; SVC=$A/src/services/governanceService.ts; Q=$G/logs/_quarantine; mkdir -p $Q $G/logs/prod/mut
bash $G/scripts/swap.sh head > /dev/null
python3 - "$1" "$SVC" "$G/logs/prod/mut/$1_governanceService.ts" <<'PY'
import sys
k, svc, out = sys.argv[1:]
s = open(svc).read()
E = {'K2': ("      if (own && own.walletAddress === p.walletAddress) return own;", "      if (own) return own;"),
     'K6': ("    proposer = holder ?? (await dbInsertParticipantIfAbsent(unstakedParticipant(proposerId, linked)));", "    void holder; proposer = await dbInsertParticipantIfAbsent(unstakedParticipant(proposerId, linked));")}
a, b = E[k]; assert s.count(a) == 1; open(out, 'w').write(s.replace(a, b)); print('mutant written', k)
PY
cp $G/logs/prod/mut/$1_governanceService.ts $SVC
cp $G/scripts/probe.test.ts $A/src/__tests__/zz-gate136-probe.test.ts
: > $G/logs/probe_mut$1.jsonl
PROBE_OUT=$G/logs/probe_mut$1.jsonl RACE_N=${RACE_N:-50} bash $G/scripts/jt.sh $G/logs/probe_mut$1_jest.log zz-gate136-probe; echo "probe mut $1 rc=$?"
mv $A/src/__tests__/zz-gate136-probe.test.ts $Q/probe_mut$1_$(date +%H%M%S).test.ts
bash $G/scripts/swap.sh head
git -C $R status --short
