#!/bin/bash
# Re-run the AUTHOR's recorder (copied, unmodified) in this gate's clone at base and head, then the author's judge + its 6 tampers on MY recordings.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate122-ks1939-pr1940
R=$W/repo; D=$R/Blockchain/Dev; A=$D/services/originate; L=$W/logs; E=$W/evidence/author_recorder; sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
F=src/routes/verification.ts; MB=e2a2426d221d8bd672e97c43c6bbcd6c4027b350
mkdir -p $L/head_copy $L/_quarantine; cp $A/$F $L/head_copy/verification.ts; h0=$(sha $A/$F)
for v in base head; do
  [ $v = base ] && git -C $R show $MB:Blockchain/Dev/services/originate/$F > $A/$F
  [ $v = head ] && cp $L/head_copy/verification.ts $A/$F
  cp $E/rec_pr1_v16.test.ts $A/src/__tests__/zz-gate122-authrec.test.ts
  V16_REC_OUT=$L/authrec_$v.json nice -n 10 $D/node_modules/.bin/jest --config $A/jest.config.js --rootDir $A --forceExit zz-gate122-authrec > $L/authrec_${v}_jest.log 2>&1; echo "authrec $v rc=$?"
  mv $A/src/__tests__/zz-gate122-authrec.test.ts $L/_quarantine/authrec_$v.test.ts
  python3 -I -c "import json,sys; print('$v scenarios', len(json.load(open(sys.argv[1]))))" $L/authrec_$v.json
done
cp $L/head_copy/verification.ts $A/$F; [ "$(sha $A/$F)" = "$h0" ] && echo RESTORE_OK
python3 -I $E/judge_pr1_v16.py $L/authrec_base.json $L/authrec_head.json $L/authjudge_mine.txt > /dev/null; echo "judge on MY recordings rc=$? $(tail -1 $L/authjudge_mine.txt)"
python3 -I $E/judge_pr1_v16.py $E/author_rec_base_a.json $E/author_rec_head_a.json $L/authjudge_theirs.txt > /dev/null; echo "judge on THEIR recordings rc=$? $(tail -1 $L/authjudge_theirs.txt)"
for t in 1 2 3 4 5 6; do python3 -I $E/judge_pr1_v16.py $L/authrec_base.json $L/authrec_head.json $L/authjudge_t$t.txt --tamper $t; echo "tamper $t rc=$?"; done
python3 -I - $L/authrec_base.json $L/authrec_head.json $E/author_rec_base_a.json $E/author_rec_head_a.json <<'PY'
import json,sys,re
a,b,c,d=[json.load(open(p)) for p in sys.argv[1:5]]
n=lambda x: re.sub(r'"verifiedAt": ?"[^"]+"','T',json.dumps(x,sort_keys=True))
print('my base == their base (verifiedAt normalised):', n(a)==n(c), '; my head == their head:', n(b)==n(d))
PY
git -C $R status --short
