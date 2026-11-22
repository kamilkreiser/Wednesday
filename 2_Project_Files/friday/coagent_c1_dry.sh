#!/bin/bash
# c1_dry.sh — Friday's LOOPBACK dry run of the C1/C2 command shapes at merged main 3337192.
# Nothing listens beyond 127.0.0.1. Root: /private/tmp/c2c-dry (must not exist). The invitation
# line is never printed: only its length. bash 3.2 safe.
set -u
W=/private/tmp/claude-501/mcwd1
PROJ="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent"
ROOT=/private/tmp/c2c-dry
BIN="$W/target/debug"
[ -e "$ROOT" ] && { echo "dry: $ROOT exists; move it aside first" >&2; exit 2; }
[ "$(git -C "$W/clone" rev-parse HEAD)" = "33371921670acfcb6fc7634d0c4eacafa9800a8d" ] || { echo "dry: clone not at 3337192" >&2; exit 2; }
[ -z "$(git -C "$W/clone" status --porcelain)" ] || { echo "dry: clone dirty" >&2; exit 2; }
export COAGENT_TOOLS="$W/tools" CARGO_TARGET_DIR="$W/target"
( cd "$W/clone" && . scripts/env.sh && cargo build --locked -p coagent-daemon --bins && cargo build --locked -p coagent-cli --bin coagent ) > "$W/c1_build.log" 2>&1
RC=$?; echo "BUILD rc=$RC"; [ $RC -eq 0 ] || { tail -n 20 "$W/c1_build.log"; exit 3; }
ls -la "$BIN/coagentd" "$BIN/coagent"; shasum -a 256 "$BIN/coagentd" "$BIN/coagent"
if lsof -nP -iTCP:7443 -sTCP:LISTEN -t >/dev/null 2>"$W/lsof.err"; then echo "dry: port 7443 already has a listener" >&2; exit 4; fi
mkdir -m 700 "$ROOT" || exit 2
ctl() { "$BIN/coagentd" ctl --data-dir "$ROOT/$1" "$2"; }
PIDS=""
stop_all() { for p in $PIDS; do kill -INT "$p" 2>>"$ROOT/stop.err"; done; sleep 3; for p in $PIDS; do if kill -0 "$p" 2>/dev/null; then echo "STILL ALIVE pid $p"; fi; done; }
echo "== M2 relay (loopback)"
nohup "$BIN/coagent" relay --listen 127.0.0.1:7443 --status-secs 60 --identity-file "$ROOT/relay.id" > "$ROOT/r.log" 2>&1 < /dev/null &
RP=$!; PIDS="$RP"
i=0; while [ $i -lt 20 ]; do grep -q 'fingerprint' "$ROOT/r.log" && break; sleep 0.5; i=$((i+1)); done
echo "-- r.log:"; cat "$ROOT/r.log"
URL="$(sed -n 's/^.*url: *//p' "$ROOT/r.log" | head -n 1)"
PIN="$(sed -n 's/^.*fingerprint: *//p' "$ROOT/r.log" | head -n 1)"
echo "URL=[$URL] PIN length ${#PIN}"
[ -n "$URL" ] && [ -n "$PIN" ] || { echo "dry: no url or fingerprint"; stop_all; exit 5; }
echo "== M3 host daemon"
nohup "$BIN/coagentd" --data-dir "$ROOT/h" --relay-url "$URL" --relay-pin "$PIN" --idle-exit-secs 86400 > "$ROOT/h.out" 2> "$ROOT/h.log" < /dev/null &
HP=$!; PIDS="$PIDS $HP"
echo "== guest daemon (no relay flags)"
nohup "$BIN/coagentd" --data-dir "$ROOT/g" --idle-exit-secs 86400 > "$ROOT/g.out" 2> "$ROOT/g.log" < /dev/null &
GP=$!; PIDS="$PIDS $GP"
sleep 3
echo "-- h.log:"; cat "$ROOT/h.log"; echo "-- g.log:"; cat "$ROOT/g.log"
echo "== status before (h, g)"
ctl h '{"v":1,"id":1,"cmd":"status"}'; echo " rc=$?"
ctl g '{"v":1,"id":1,"cmd":"status"}'; echo " rc=$?"
echo "== M4 invite (line NOT printed)"
ctl h '{"v":1,"id":2,"cmd":"invite"}' > "$ROOT/invite.json" 2> "$ROOT/invite.err"; echo "invite rc=$?"
python3 - "$ROOT/invite.json" "$ROOT/line.txt" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
r = d.get("result", {})
line = r.get("line", "")
open(sys.argv[2], "w").write(line)
print("invite keys:", sorted(d.keys()), "result keys:", sorted(r.keys()))
print("ok:", d.get("ok"), "expires_in_s:", r.get("expires_in_s"))
print("line length:", len(line), "starts with 'coagent join ':", line.startswith("coagent join "))
blob = line.split(" ")[-1]
print("blob length:", len(blob), "charset ok for cmd (A-Za-z0-9_-=):", all(c.isalnum() or c in "-_=" for c in blob))
PY
chmod 600 "$ROOT/invite.json" "$ROOT/line.txt"
echo "== P6 join on g (whole line as the blob)"
python3 - "$ROOT/line.txt" > "$ROOT/join_arg.json" <<'PY'
import json, sys
print(json.dumps({"v":1,"id":2,"cmd":"join","args":{"blob":open(sys.argv[1]).read()}}))
PY
chmod 600 "$ROOT/join_arg.json"
ctl g "$(cat "$ROOT/join_arg.json")"; echo " join rc=$?"
echo "== P7/M5 status poll"
T0=$(date +%s); OK=0; i=0
while [ $i -lt 30 ]; do
  ctl h '{"v":1,"id":3,"cmd":"status"}' > "$ROOT/sh.json" 2>&1; ctl g '{"v":1,"id":3,"cmd":"status"}' > "$ROOT/sg.json" 2>&1
  if grep -q '"connected":true' "$ROOT/sh.json" && grep -q '"connected":true' "$ROOT/sg.json"; then OK=1; break; fi
  sleep 2; i=$((i+1))
done
echo "connected both=$OK after $(( $(date +%s) - T0 )) s"; echo "-- h status:"; cat "$ROOT/sh.json"; echo; echo "-- g status:"; cat "$ROOT/sg.json"; echo
if [ $OK -eq 1 ]; then
  echo "== C2-1 g sends request"
  ctl g '{"v":1,"id":4,"cmd":"send","args":{"kind":"request","text":"C2X-1 request from the guest: please reply"}}'; echo " rc=$?"
  sleep 3
  echo "== C2-2 h inbox_read"
  ctl h '{"v":1,"id":5,"cmd":"inbox_read"}' | tee "$ROOT/h_read.json"; echo
  ACK="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["result"].get("ack",""))' "$ROOT/h_read.json" 2>>"$ROOT/py.err")"
  MID="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); m=d["result"].get("messages",[]); print(m[0].get("id","") if m else "")' "$ROOT/h_read.json" 2>>"$ROOT/py.err")"
  echo "ack=[$ACK] id=[$MID]"
  echo "== C2-3 h inbox_ack"
  ctl h "{\"v\":1,\"id\":6,\"cmd\":\"inbox_ack\",\"args\":{\"upto\":$ACK}}"; echo " rc=$?"
  echo "== C2-4 h reply WITH re"
  ctl h "{\"v\":1,\"id\":7,\"cmd\":\"send\",\"args\":{\"kind\":\"reply\",\"re\":\"$MID\",\"text\":\"C2X-2 reply from the host\"}}"; echo " rc=$?"
  echo "== extra: h reply WITHOUT re (is re required?)"
  ctl h '{"v":1,"id":8,"cmd":"send","args":{"kind":"reply","text":"C2X-5 reply without re"}}'; echo " rc=$?"
  sleep 3
  echo "== C2-5 g inbox_read"
  ctl g '{"v":1,"id":9,"cmd":"inbox_read"}'; echo
  echo "== C2-9 marker counts (must be 0) and a positive control"
  grep -c 'C2X-' "$ROOT/h.log" "$ROOT/g.log" "$ROOT/r.log"
  echo "control (h_read.json holds the text): $(grep -c 'C2X-1' "$ROOT/h_read.json")"
fi
echo "== stop (SIGINT each)"
stop_all
echo "-- h.log tail:"; tail -n 4 "$ROOT/h.log"; echo "-- g.log tail:"; tail -n 4 "$ROOT/g.log"; echo "-- r.log tail:"; tail -n 4 "$ROOT/r.log"
echo "listeners on 7443 after: $(lsof -nP -iTCP:7443 -sTCP:LISTEN -t 2>/dev/null | wc -l | tr -d ' ')"
: > "$ROOT/line.txt"; : > "$ROOT/join_arg.json"; : > "$ROOT/invite.json"
echo "DRY RUN END"
