#!/bin/bash
W=/private/tmp/claude-501/qwt/rm_t; mkdir -p $W
python3 -B -I - <<'PY'
import json
W='/private/tmp/claude-501/qwt/rm_t/'
A=lambda tools,req=None:dict(type="assistant",message={"content":[{"type":"tool_use","name":t} for t in tools]},**({"serverClassifierRequest":req} if req else {}))
U=lambda req=None:{"type":"user","serverClassifierContext":({"request":req} if req else {"other":1})}
# T1: context record WITHOUT request, assistant WITHOUT request (N-f case)
# T2: matching request/context pair; T3: assistant with request, no context
for n,recs in {"t1":[A(["Bash"]),U()],"t2":[A(["Bash"],"R1"),U("R1")],"t3":[A(["Bash"],"R2"),A([],"R3"),U("R1")]}.items():
    open(W+n+".jsonl","w").write("\n".join(json.dumps(r) for r in recs)+"\n")
PY
for t in t1 t2 t3; do for v in base head; do echo "--- $t $v"; python3 -B -I /private/tmp/claude-501/qwt/review_map_$v.py $W/$t.jsonl; done; done
