. /private/tmp/claude-501/qp1/p/lib.sh
mkdir -p $W/p/w8; D=$W/p/x8
startd $D --gate --workspace $W/p/w8 || echo startfail
echo "extra field in args:"; ctl $D '{"v":1,"id":1,"cmd":"gate","args":{"event":{"hook_event_name":"ConfigChange"},"x":1}}'
echo "event not an object:"; ctl $D '{"v":1,"id":2,"cmd":"gate","args":{"event":[1]}}'
echo "no args:"; ctl $D '{"v":1,"id":3,"cmd":"gate"}'
echo "unknown top-level field:"; ctl $D '{"v":1,"id":4,"cmd":"gate","args":{"event":{}},"y":2}'
echo "v=2:"; ctl $D '{"v":2,"id":5,"cmd":"gate","args":{"event":{}}}'
big=$(python3 -I -c 'print("{\"v\":1,\"id\":6,\"cmd\":\"gate\",\"args\":{\"event\":{\"hook_event_name\":\"ConfigChange\",\"pad\":\"" + "a"*(130*1024) + "\"}}}")')
echo "request > 128 KiB:"; ctl $D "$big" | head -c 200; echo
echo "ConfigChange (just under limit, 120 KiB pad):"; mid=$(python3 -I -c 'print("{\"v\":1,\"id\":7,\"cmd\":\"gate\",\"args\":{\"event\":{\"hook_event_name\":\"ConfigChange\",\"pad\":\"" + "a"*(120*1024) + "\"}}}")'); ctl $D "$mid" | head -c 200; echo
echo "daemon log lines mentioning the pad or tool input (expect 0):"; /usr/bin/grep -c 'aaaaaaaa' $D.log
stopd $D
echo "gate.json unreadable variants -> refuse start:"
for c in '{"v":2,"tainted":[]}' '{"v":1,"tainted":[],"extra":1}' 'garbage'; do mkdir -p $W/p/x9; printf '%s' "$c" > $W/p/x9/gate.json; chmod 600 $W/p/x9/gate.json; "${RUNENV[@]}" $B/coagentd --data-dir $W/p/x9 --coagent $B/coagent --gate --workspace $W/p/w8 </dev/null >/dev/null 2>$W/p/tmp/x9.err & P=$!; sleep 3; if kill -0 $P 2>/dev/null; then echo "[$c] STILL RUNNING"; kill $P; wait $P; else wait $P; echo "[$c] exit=$? $(tail -1 $W/p/tmp/x9.err)"; fi; done
echo "gate.json mode 000 (unreadable):"; printf '{"v":1,"tainted":[]}' > $W/p/x9/gate.json; chmod 000 $W/p/x9/gate.json; "${RUNENV[@]}" $B/coagentd --data-dir $W/p/x9 --coagent $B/coagent --gate --workspace $W/p/w8 </dev/null >/dev/null 2>$W/p/tmp/x9.err & P=$!; sleep 3; if kill -0 $P 2>/dev/null; then echo "STILL RUNNING"; kill $P; wait $P; else wait $P; echo "exit=$? $(tail -1 $W/p/tmp/x9.err)"; fi; chmod 600 $W/p/x9/gate.json
echo "--gate without --workspace:"; "${RUNENV[@]}" $B/coagentd --data-dir $W/p/xa --gate </dev/null >/dev/null 2>&1; echo "exit=$?"
echo "--gate with HOME unset:"; env -i PATH=/usr/bin:/bin $B/coagentd --data-dir $W/p/xa --gate --workspace $W/p/w8 </dev/null >/dev/null 2>&1; echo "exit=$?"
echo "--exclude without --gate:"; "${RUNENV[@]}" $B/coagentd --data-dir $W/p/xa --exclude 'x/**' </dev/null >/dev/null 2>&1; echo "exit=$?"
