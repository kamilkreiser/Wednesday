. /private/tmp/claude-501/qp1/p/lib.sh
X="$W/p/s p!c"; D="$X/d"
CMD=$(python3 -I -c 'import json,sys; h=json.load(open(sys.argv[1])); print(h["hooks"]["PreToolUse"][0]["hooks"][0]["command"])' "$X/plug/hooks/hooks.json")
"${RUNENV[@]}" "$X/bin/coagentd" --data-dir "$D" --coagent "$X/bin/coagent" --gate --workspace "$X/ws" --idle-exit-secs 600 </dev/null >/dev/null 2>"$W/p/sp.log" & PID=$!
for i in $(seq 1 100); do "${RUNENV[@]}" "$X/bin/coagentd" ctl --data-dir "$D" '{"v":1,"id":1,"cmd":"status"}' >/dev/null 2>&1 && break; sleep 0.1; done
for sh in /bin/sh /bin/zsh /bin/bash; do o=$(ev s1 "$X/ws" default Read "{\"file_path\":\"$X/ws/a\"}" | env -i PATH=/usr/bin:/bin $sh -c "$CMD" 2>&1); echo "$sh rc=$? out=${o:0:100}"; done
o=$(ev s1 "$X/ws" default Read "{\"file_path\":\"$X/ws/a\"}" | env -i PATH=/usr/bin:/bin /bin/bash -H -c "set -H; $CMD" 2>&1); echo "bash -H rc=$? out=${o:0:100}"
kill -TERM $PID; wait $PID
