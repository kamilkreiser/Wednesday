. /private/tmp/claude-501/qp1/p/lib.sh
MP=$W/m/preview/make-plugin.sh
X="$W/p/s p!c"; mkdir -p "$X/bin" "$X/ws"
cp $B/coagent-hook $B/coagent-mcp $B/coagentd $B/coagent "$X/bin/"
D="$X/d"
echo "== render with space and ! in bin, data, out"; bash $MP "$X/bin" "$D" "$X/plug" | san; echo "rc=${PIPESTATUS[0]}"
CMD=$(python3 -I -c 'import json,sys; h=json.load(open(sys.argv[1])); print(h["hooks"]["PreToolUse"][0]["hooks"][0]["command"]); print(h["hooks"]["ConfigChange"][0]["hooks"][0]["command"]==h["hooks"]["PreToolUse"][0]["hooks"][0]["command"]); print([e["hooks"][0]["onFailure"] for k in ("PreToolUse","ConfigChange") for e in h["hooks"][k]], h["hooks"]["PreToolUse"][0]["matcher"], "ConfigChange matcher:", h["hooks"]["ConfigChange"][0].get("matcher"))' "$X/plug/hooks/hooks.json" | head -1)
python3 -I -c 'import json,sys; h=json.load(open(sys.argv[1])); print([ (k, e["hooks"][0]["onFailure"], e["hooks"][0]["timeout"], e.get("matcher")) for k in h["hooks"] for e in h["hooks"][k]])' "$X/plug/hooks/hooks.json"
echo "command: $CMD" | san
echo "== daemon DOWN: run the command through sh, zsh, bash"
for sh in /bin/sh /bin/zsh /bin/bash; do ev s1 "$X/ws" default Read '{}' | env -i PATH=/usr/bin:/bin $sh -c "$CMD" >/dev/null 2>$W/p/tmp/err; echo "$sh rc=$? err=$(cat $W/p/tmp/err)"; done
echo "== daemon UP (gate): the same three"
startd "$D" --gate --workspace "$X/ws" || echo startfail
for sh in /bin/sh /bin/zsh /bin/bash; do o=$(ev s1 "$X/ws" default Read "{\"file_path\":\"$X/ws/a\"}" | env -i PATH=/usr/bin:/bin $sh -c "$CMD" 2>&1); echo "$sh rc=$? out=${o:0:110}" | san; done
echo "== interactive-style zsh/bash with history expansion on"; o=$(ev s1 "$X/ws" default Read "{\"file_path\":\"$X/ws/a\"}" | env -i PATH=/usr/bin:/bin /bin/bash -H -c "set -H; $CMD" 2>&1); echo "bash -H rc=$? out=${o:0:80}"
stopd "$D"
echo "== .mcp.json"; cat "$X/plug/.mcp.json" | san
echo "== refusals (scratch HOME only)"
SH=$W/p/fakehome; mkdir -p $SH/.claude $W/p/fakeccd
env -i PATH=/usr/bin:/bin HOME=$SH bash $MP "$X/bin" "$D" $SH/.claude/plug 2>&1 | san; echo "rc=${PIPESTATUS[0]} exists=$([ -e $SH/.claude/plug ] && echo yes || echo no)"
env -i PATH=/usr/bin:/bin HOME=$SH bash $MP "$X/bin" "$D" $SH/.CLAUDE/plug2 2>&1 | san; echo "rc=${PIPESTATUS[0]}"
ln -sfn $SH/.claude $W/p/lnk; env -i PATH=/usr/bin:/bin HOME=$SH bash $MP "$X/bin" "$D" $W/p/lnk/plug3 2>&1 | san; echo "symlink-into rc=${PIPESTATUS[0]}"
env -i PATH=/usr/bin:/bin HOME=$SH CLAUDE_CONFIG_DIR=$W/p/fakeccd bash $MP "$X/bin" "$D" $W/p/fakeccd/plug 2>&1 | san; echo "rc=${PIPESTATUS[0]}"
env -i PATH=/usr/bin:/bin HOME=$SH bash $MP "$X/bin" "$D" "$X/plug" 2>&1 | san; echo "existing rc=${PIPESTATUS[0]}"
env -i PATH=/usr/bin:/bin HOME=$SH bash $MP "$X/bin" "$W/p/q'x" "$X/plugq" 2>&1 | san; echo "quote rc=${PIPESTATUS[0]}"
