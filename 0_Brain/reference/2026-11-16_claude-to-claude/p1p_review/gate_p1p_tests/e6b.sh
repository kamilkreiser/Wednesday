. /private/tmp/claude-501/qp1/p/lib.sh
mkdir -p $W/p/w8; n=0
for c in '{"v":1,"tainted":[]}' '{"v":2,"tainted":[]}' '{"v":1,"tainted":[],"extra":1}' 'garbage' 'MODE000'; do n=$((n+1)); X=$W/p/y$n; mkdir -m 700 $X
  if [ "$c" = MODE000 ]; then printf '{"v":1,"tainted":[]}' > $X/gate.json; chmod 000 $X/gate.json; else printf '%s' "$c" > $X/gate.json; chmod 600 $X/gate.json; fi
  "${RUNENV[@]}" $B/coagentd --data-dir $X --coagent $B/coagent --gate --workspace $W/p/w8 </dev/null >/dev/null 2>$W/p/tmp/x9.err & P=$!; sleep 3
  if kill -0 $P 2>/dev/null; then echo "[$c] RUNNING (started)"; kill $P; wait $P; else wait $P; echo "[$c] exit=$? $(tail -1 $W/p/tmp/x9.err)"; fi
  chmod 600 $X/gate.json
done
