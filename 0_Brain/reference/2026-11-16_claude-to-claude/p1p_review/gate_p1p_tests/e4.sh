. /private/tmp/claude-501/qp1/p/lib.sh
H=$W/p/lh; G=$W/p/lg; mkdir -p $W/p/wh $W/p/wg
startd $H --gate --workspace $W/p/wh || echo startfail-h
startd $G --gate --workspace $W/p/wg || echo startfail-g
LINE=$(ctl $H '{"v":1,"id":1,"cmd":"invite"}' | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["result"]["line"])')
ctl $G "{\"v\":1,\"id\":2,\"cmd\":\"join\",\"args\":{\"blob\":\"$LINE\"}}" >/dev/null
for i in $(seq 1 240); do
  a=$(ctl $H '{"v":1,"id":3,"cmd":"status"}' | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["result"]["session"]["connected"])')
  b=$(ctl $G '{"v":1,"id":3,"cmd":"status"}' | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["result"]["session"]["connected"])')
  [ "$a" = True ] && [ "$b" = True ] && break; sleep 0.25; done
echo "connected h=$a g=$b"
IR=mcp__plugin_coagent_link__inbox_read; WT=mcp__plugin_coagent_link__wait
unread() { ctl $H '{"v":1,"id":4,"cmd":"status"}' | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["result"]["session"]["unread"])'; }
send() { ctl $G "{\"v\":1,\"id\":5,\"cmd\":\"send\",\"args\":{\"kind\":\"chat\",\"text\":\"$1\"}}" >/dev/null; for i in $(seq 1 120); do [ "$(unread)" -ge "${2:-1}" ] && return 0; sleep 0.25; done; echo "not delivered"; }
read_() { ctl $H '{"v":1,"id":6,"cmd":"inbox_read"}' | python3 -I -c 'import json,sys; r=json.load(sys.stdin); print("ok" if r["ok"] else "err", r.get("error",{}).get("code",""), [m["text"] for m in r.get("result",{}).get("messages",[])], r.get("result",{}).get("ack",""))'; }
ack() { ctl $H "{\"v\":1,\"id\":7,\"cmd\":\"inbox_ack\",\"args\":{\"upto\":$1}}" >/dev/null; }
witness() { ev "$1" $W/p/wh "${3:-default}" "$2" '{}' | hk $H | python3 -I -c 'import json,sys; l=sys.stdin.read(); print(l[:120])'; }
send MK-1
echo "== (b) inbox_read PreToolUse in dontAsk mode (decided deny?) then read"; witness S-A $IR dontAsk; read_; echo "unread=$(unread)"
echo "== (d1) wait witness, then inbox_read"; witness S-A $WT; read_
echo "== (d2) consume stray wait witness with a wait (inbox non-empty -> immediate)"; r=$(ctl $H '{"v":1,"id":8,"cmd":"wait","args":{"timeout_s":1}}' | python3 -I -c 'import json,sys; r=json.load(sys.stdin); print(r["ok"], [m["text"] for m in r.get("result",{}).get("messages",[])], r.get("result",{}).get("ack",""))'); echo "$r"
A=$(echo "$r" | awk '{print $NF}'); ack $A; echo "unread=$(unread)"
send MK-2
echo "== (c) one witness, two concurrent reads"; witness S-A $IR; (read_ > $W/p/tmp/r1 &) ; read_ > $W/p/tmp/r2; sleep 1; cat $W/p/tmp/r1 $W/p/tmp/r2
A=$(grep '^ok' $W/p/tmp/r1 $W/p/tmp/r2 | awk '{print $NF}'); [ -n "$A" ] && ack $A
send MK-3
echo "== (a) witness from session S-OTHER releases a read (known limit) and taints S-OTHER"; witness S-OTHER $IR; read_ | tee $W/p/tmp/r3; A=$(awk '{print $NF}' $W/p/tmp/r3); ack $A
python3 -I -c 'import json; print("gate.json tainted:", json.load(open("'$H'/gate.json"))["tainted"])'
send MK-4
echo "== (f) wait witness; wait times out with empty inbox? (inbox has MK-4, so use timeout path first)"; 
echo "== (e) restart drops a live witness"; witness S-A $IR; stopd $H; startd $H --gate --workspace $W/p/wh || echo restartfail; for i in $(seq 1 120); do c=$(ctl $H '{"v":1,"id":3,"cmd":"status"}' | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["result"]["session"]["connected"])'); [ "$c" = True ] && break; sleep 0.25; done; echo "reconnected=$c"; read_
echo "== (g) witness older than 330 s TTL: NOT TESTED here (lane A test d uses an in-process 2 s TTL)"
echo "== (h) taint write fails (gate.json replaced by a directory) -> nothing released"; witness S-NEW $IR; mv $H/gate.json $H/gate.json.bak; mkdir $H/gate.json; read_; echo "unread=$(unread)"; rmdir $H/gate.json; mv $H/gate.json.bak $H/gate.json
echo "== (h2) after the failed taint write: is S-NEW tainted in memory? second witness + read"; witness S-NEW $IR; read_ | tee $W/p/tmp/r4; A=$(awk '{print $NF}' $W/p/tmp/r4); [ "${A:-x}" != "" ] && ack $A 2>/dev/null
python3 -I -c 'import json; print("gate.json tainted:", json.load(open("'$H'/gate.json"))["tainted"])'
echo "== (i) wait witness consumed by a wait that times out; then a message; a second wait without witness"
witness S-A $WT; r=$(ctl $H '{"v":1,"id":9,"cmd":"wait","args":{"timeout_s":2}}'); echo "${r:0:160}"
send MK-5; r=$(ctl $H '{"v":1,"id":10,"cmd":"wait","args":{"timeout_s":2}}'); echo "${r:0:160}"; read_
echo "== (j) two waits on one wait witness (empty inbox): second refused"
witness S-A $IR; read_ | tee $W/p/tmp/r5; A=$(awk '{print $NF}' $W/p/tmp/r5); ack $A; echo "unread=$(unread)"
witness S-A $WT; (ctl $H '{"v":1,"id":11,"cmd":"wait","args":{"timeout_s":20}}' > $W/p/tmp/w1 &); sleep 1; ctl $H '{"v":1,"id":12,"cmd":"wait","args":{"timeout_s":20}}' > $W/p/tmp/w2; head -c 160 $W/p/tmp/w2; echo; send MK-6; sleep 2; head -c 200 $W/p/tmp/w1; echo
stopd $H; stopd $G
