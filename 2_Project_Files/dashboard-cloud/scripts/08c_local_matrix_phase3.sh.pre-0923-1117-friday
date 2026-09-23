#!/usr/bin/env bash
# Phase 3 local matrix — the app on loopback (transient port 47791) against the REAL storage account through the CLI credential,
# with a SIMULATED Easy Auth principal (Kam's object id), exercising what Easy Auth stops the builder from driving live:
#   Kam's reply route with the Phase-3 envelope: wrapped to the addressed seat -> 201; NOT wrapped to it -> 400 (server guard);
#   wrapped_keys malformed -> 400; then the WEDNESDAY seat reads the reply back through the seat API with --decrypt (== text),
#   and the TUESDAY seat cannot (partition) / cannot open it offline (kid). GET /api/pubkeys as Kam -> ring + seats.
# The reply envelope is produced by the page's OWN common.js in Node (scripts/09 pattern) — the real shape a browser sends.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
SCRATCH=${SCRATCH:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a45299b-5e60-46f6-b7e7-e32507803323/scratchpad}
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
export TENANT_ID SEAT_API_APPID=$API_APPID STORAGE_ACCOUNT=$STORAGE SEAT_APP_MAP="$wednesday_seat_APPID:wednesday,$tuesday_seat_APPID:tuesday" KAM_OBJECT_ID=$KAM_USER_OBJ
PORT=47791; BASE="http://127.0.0.1:$PORT"; FAIL=0
( "$V" -m uvicorn main:app --app-dir "$HERE/app" --host 127.0.0.1 --port $PORT --log-level warning > "$SCRATCH/wedcloud_local3.log" 2>&1 ) &
APP_PID=$!
for i in $(seq 1 40); do curl -s -o /dev/null "$BASE/api/seat/health" && break; sleep 0.5; done
expect() { if [ "$2" = "$3" ]; then echo "PASS  $1: expected $2 got $3"; else echo "FAIL  $1: expected $2 got $3"; FAIL=1; fi; }
hdr() { curl -s -o "$SCRATCH/l_body.txt" -w '%{http_code}' --max-time 30 "$@"; }
KAM=(-H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'x-ms-client-principal-name: kreiser.org@me.com')
TS=$(date -u +%H%M%S)
echo "### P3-L1 /api/pubkeys as Kam"
expect "GET /api/pubkeys as Kam" 200 "$(hdr "${KAM[@]}" "$BASE/api/pubkeys")"
cp "$SCRATCH/l_body.txt" "$SCRATCH/pubkeys_local.json"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print("      kam ring:",[(k["name"],k["kid"]) for k in d["kam"]],"seats:",{s:v["kid"] for s,v in d["seats"].items()});assert len(d["kam"])==3 and set(d["seats"])=={"wednesday","tuesday"} and all("BEGIN PUBLIC KEY" in k["pem"] and "PRIVATE" not in k["pem"] for k in d["kam"]);print("PASS  ring = 3 Kam PUBLIC keys + 2 seat PUBLIC keys, no private material")' "$SCRATCH/pubkeys_local.json" || FAIL=1
echo "### P3-L2 Kam's reply made by the page's own module (Node WebCrypto), three shapes"
node - "$HERE" "$SCRATCH/pubkeys_local.json" "$TS" > "$SCRATCH/kam_bodies.json" <<'EOF2'
import fs from "node:fs"; import vm from "node:vm";
const [HERE, pk, TS] = process.argv.slice(2); const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8"); const pubkeys = JSON.parse(fs.readFileSync(pk, "utf8"));
const sb = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, console, localStorage: undefined, indexedDB: undefined,
  fetch: async (url) => { if (url === "/api/pubkeys") return { ok: true, status: 200, json: async () => pubkeys }; throw new Error("unexpected " + url); } };
sb.globalThis = sb; vm.createContext(sb); vm.runInContext(src, sb); const WED = sb.window.WED;
const text = `SYNTHETIC Kam reply from the loopback matrix ${TS} (page module, ring + seat)`;
const mk = async (view, client, id) => { const clear = { client, kind: "message", id, ts: new Date().toISOString(), view }; return { client, view, id, ts: clear.ts, envelope: await WED.encryptText(text, clear) }; };
const good = await mk("wednesday", "WED", `p3l-good-${TS}`);
const noseat = JSON.parse(JSON.stringify(await mk("wednesday", "WED", `p3l-noseat-${TS}`))); noseat.envelope.wrapped_keys = noseat.envelope.wrapped_keys.filter(e => e.kid !== pubkeys.seats.wednesday.kid);
const bad = JSON.parse(JSON.stringify(await mk("wednesday", "WED", `p3l-bad-${TS}`))); bad.envelope.wrapped_keys = [{ kid: "zz", wrapped_key: "!!" }];
const both = await mk("both", "ALL", `p3l-both-${TS}`);
console.log(JSON.stringify({ text, good, noseat, bad, both }));
EOF2
body() { python3 -c 'import json,sys;print(json.dumps(json.load(open(sys.argv[1]))[sys.argv[2]]))' "$SCRATCH/kam_bodies.json" "$1"; }
EXPECTED=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["text"])' "$SCRATCH/kam_bodies.json")
c=$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' -d "$(body noseat)" "$BASE/api/kam/messages"); expect "POST reply NOT wrapped to the wednesday seat (server guard)" 400 "$c"; echo "      body: $(head -c 160 "$SCRATCH/l_body.txt")"
c=$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' -d "$(body bad)" "$BASE/api/kam/messages"); expect "POST reply with malformed wrapped_keys" 400 "$c"; echo "      body: $(head -c 120 "$SCRATCH/l_body.txt")"
c=$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' -d "$(body good)" "$BASE/api/kam/messages"); expect "POST reply wrapped to ring + wednesday seat (view=wednesday -> WED)" 201 "$c"; echo "      body: $(head -c 160 "$SCRATCH/l_body.txt")"
c=$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' -d "$(body both)" "$BASE/api/kam/messages"); expect "POST reply view=both -> ALL wrapped to both seats" 201 "$c"
echo "### P3-L3 the seats read it back through the API"
"$V" "$HERE/seat/get_kam_messages.py" --seat wednesday --decrypt --json --since "$(date -u +%Y-%m-%dT%H:%M -v-2M 2>/dev/null || date -u +%Y-%m-%dT00:00)" > "$SCRATCH/l_wed.json" 2>"$SCRATCH/l_err.txt"; expect "wednesday seat get_kam_messages --decrypt rc" 0 "$?"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m={r["id"]:r for r in d["messages"]};g=m.get("p3l-good-"+sys.argv[3]);b=m.get("p3l-both-"+sys.argv[3]);exp=sys.argv[2]
assert g and g.get("text")==exp, ("good row missing/undecrypted", g and {k:g.get(k) for k in ("text","decrypt_error")}); print("PASS  wednesday seat decrypts Kam'"'"'s view=wednesday reply == the text the page encrypted")
assert b and b.get("text")==exp and b["client"]=="ALL"; print("PASS  wednesday seat decrypts Kam'"'"'s view=both (ALL) reply")
assert "p3l-noseat-"+sys.argv[3] not in m and "p3l-bad-"+sys.argv[3] not in m; print("PASS  the two refused replies were NOT stored")' "$SCRATCH/l_wed.json" "$EXPECTED" "$TS" || FAIL=1
"$V" "$HERE/seat/get_kam_messages.py" --seat tuesday --decrypt --json --since "$(date -u +%Y-%m-%dT%H:%M -v-2M 2>/dev/null || date -u +%Y-%m-%dT00:00)" 2>"$SCRATCH/l_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);m={r["id"]:r for r in d["messages"]};exp=sys.argv[1];t=sys.argv[2]
assert "p3l-good-"+t not in m, "R0 BROKEN: WED row reached the tuesday seat"; print("PASS  tuesday seat does NOT receive the WED-partition reply (R0, partition from the token)")
b=m.get("p3l-both-"+t); assert b and b.get("text")==exp; print("PASS  tuesday seat decrypts the view=both (ALL) reply with her own key")' "$EXPECTED" "$TS" || FAIL=1
echo "### P3-L4 offline: the raw WED reply row cannot be opened with the tuesday seat key"
az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'WED' and id eq 'p3l-good-$TS'" -o json > "$SCRATCH/l_raw.json" 2>/dev/null
"$V" - "$SCRATCH/l_raw.json" "$EXPECTED" <<'PY' || FAIL=1
import json,sys; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
CRED="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"; r=json.load(open(sys.argv[1]))["items"][0]; clear={"client":r["PartitionKey"],"kind":r["kind"],"id":r["id"],"ts":r["ts"]}
assert sys.argv[2] not in json.dumps(r); print("      raw row kids:", envelope.kids_of(r), "written_by:", r["written_by"][:12], "plaintext absent")
for k in ("kam-pilot-private.pem","kam-laptop-private.pem","kam-ipad-private.pem","wednesday-seat.pem"):
    assert envelope.decrypt_text(envelope.load_private(f"{CRED}/{k}"), r, clear)==sys.argv[2]; print(f"PASS  {k} opens Kam's reply row")
try: envelope.decrypt_text(envelope.load_private(f"{CRED}/tuesday-seat.pem"), r, clear); print("FAIL  tuesday key opened a WED reply"); sys.exit(1)
except KeyError: print("PASS  tuesday-seat.pem refused (KeyError)")
PY
kill $APP_PID 2>/dev/null; wait $APP_PID 2>/dev/null
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL LOCAL PHASE 3 PROBES PASS || echo SOME FAILED)"; exit $FAIL
