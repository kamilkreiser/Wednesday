#!/bin/bash
# QA-POLICY-B: one-command reproduction of the findings at both SHAs (needs the check's built trees); prints the four
# columns (no view, owner StillAsk, owner Allowed, both-agree) for the default list, `**/.env*` and `**/.env`.
W=/private/tmp/claude-501/qpb
for T in base head; do bash $W/h/run_diff.sh $T 0x9b17c4ec0001 $W/out/repro_$T.jsonl $([ $T = base ] && echo 1 || echo 0) QPB_N2=0 QPB_N3=0 QPB_ROWS=$W/rows/rows_repro.jsonl > /dev/null; done
python3 -B -I - <<'PY'
import json
W="/private/tmp/claude-501/qpb"
def rd(p):
    f=open(p); f.readline(); return [json.loads(l) for l in f]
for b,h in zip(rd(W+"/out/repro_base.jsonl"), rd(W+"/out/repro_head.jsonl")):
    sb={s["st"]:s for s in b["states"]}; sh={s["st"]:s for s in h["states"]}
    cols=lambda s:" ".join(s["cols"][j]["c"] for j in (0,8,9,3))
    print(f'{b["id"]}: ' + "; ".join(f'{st} {cols(sb[st])} -> {cols(sh[st])}' for st in ("default","**/.env*","**/.env")) + f'; head too large: {bool(h["oversize"])}')
PY
