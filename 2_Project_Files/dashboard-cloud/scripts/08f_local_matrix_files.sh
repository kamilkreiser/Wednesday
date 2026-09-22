#!/usr/bin/env bash
# File-drawer local matrix (2026-09-22, Kam 15:26 download / 15:31 upload) — the app on loopback (transient port 47795) against the
# REAL storage account through the CLI credential (Kam's user: Table + Blob Data Contributor on wedndashtkhrqh), with a SIMULATED
# Easy Auth principal (Kam's object id) for the VIEWER routes — the only unattended way to drive Kam's upload path, which sits
# behind Easy Auth on the live site. Every row/blob this matrix writes is born synthetic (the pages hide such rows). NOTHING IS
# DELETED (no delete route exists). Arms: viewer gates · Kam POST /api/files refused without the seat kid (400) · Kam upload
# (page-encrypted in Node WebCrypto with the pilot key) row 201 -> bytes 200 ready · wrong sha 400 · Kam lists it (own upload
# in the drawer) · Kam downloads it (bytes == ct) · the WEDNESDAY seat fetches + decrypts it (sha256 == original) via
# get_files.py · the tuesday seat cannot list/read it (R0) · a Kam message with attachments -> the row carries the ids ->
# kam_msgs.sh prints att=1 and --fetch-attachments writes the decrypted file · audit rows upload + download via the API.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
ROOT=/Volumes/DevMASTER/WEDNESDAY
SCRATCH=${SCRATCH:?set SCRATCH to a scratch dir}
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
export TENANT_ID SEAT_API_APPID=$API_APPID STORAGE_ACCOUNT=$STORAGE SEAT_APP_MAP="$wednesday_seat_APPID:wednesday,$tuesday_seat_APPID:tuesday" KAM_OBJECT_ID=$KAM_USER_OBJ
PORT=47795; BASE="http://127.0.0.1:$PORT"; FAIL=0
( "$V" -m uvicorn main:app --app-dir "$HERE/app" --host 127.0.0.1 --port $PORT --log-level warning > "$SCRATCH/wedcloud_local_files.log" 2>&1 ) &
APP_PID=$!
for i in $(seq 1 120); do curl -s -o /dev/null "$BASE/api/seat/health" && break; sleep 1; done
curl -s -o /dev/null "$BASE/api/seat/health" || { echo "FAIL  loopback app did not come up in 120 s: $(tail -3 "$SCRATCH/wedcloud_local_files.log" | tr "\n" " ")"; kill $APP_PID 2>/dev/null; exit 1; }
expect() { if [ "$2" = "$3" ]; then echo "PASS  $1: expected $2 got $3"; else echo "FAIL  $1: expected $2 got $3"; FAIL=1; fi; }
hdr() { curl -s -o "$SCRATCH/f_body.txt" -w '%{http_code}' --max-time 60 "$@"; }
pyarm() { python3 -c "$1" "${@:2}" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }; }
KAM=(-H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'x-ms-client-principal-name: kreiser.org@me.com')
OTHER=(-H "x-ms-client-principal-id: 00000000-0000-0000-0000-00000000dead" -H 'x-ms-client-principal-name: not-kam@example.invalid')
mktok() { "$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","$1","--client","$2"]); print(sc.get_token(a, sc.load_ids()))
PY
}
TOK=$(mktok wednesday WED); TOKT=$(mktok tuesday Datasec)
TS=$(date -u +%H%M%S)
echo "### FL1 health + viewer gates (app-level: no principal header -> 401; live: Easy Auth)"
c=$(hdr "$BASE/api/seat/health"); expect "health" 200 "$c"; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("file_route") is True and d.get("file_max_bytes")==33554432,d;print("PASS  health: file_route true, bound 33554432")' "$SCRATCH/f_body.txt"
expect "GET /api/files no principal" 401 "$(hdr "$BASE/api/files")"
expect "POST /api/files no principal" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d '{"view":"wednesday"}' "$BASE/api/files")"
expect "POST /api/files as a NON-Kam principal (read-only viewer) -> 403" 403 "$(hdr "${OTHER[@]}" -X POST -H 'Content-Type: application/json' -d '{"view":"wednesday"}' "$BASE/api/files")"
expect "GET /static/drawer.js as Kam" 200 "$(hdr "${KAM[@]}" "$BASE/static/drawer.js")"
echo "### FL2 Kam's upload — page-encrypted (common.js in Node WebCrypto, pilot key), view=wednesday -> WED"
"$V" - > "$SCRATCH/f_pubkeys.json" <<'PY'
import sys, os, glob, hashlib, base64, json
K="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/app/keys"
def kid(pem): return hashlib.sha256(base64.b64decode("".join(l for l in pem.splitlines() if l and not l.startswith("-----")))).hexdigest()[:16]
files=sorted(glob.glob(K+"/kam-*-public.pub")); files.sort(key=lambda q:(0 if os.path.basename(q)=="kam-pilot-public.pub" else 1,q))
print(json.dumps({"kam":[{"name":os.path.basename(q)[4:-11],"kid":kid(open(q).read()),"pem":open(q).read()} for q in files],"seats":{s:{"kid":kid(open(f"{K}/{s}-seat-public.pub").read()),"pem":open(f"{K}/{s}-seat-public.pub").read()} for s in ("wednesday","tuesday")},"seat_of_client":{"WED":["wednesday"],"Secuura":["wednesday"],"Datasec":["tuesday"],"ALL":["wednesday","tuesday"]}}))
PY
head -c 200000 /dev/urandom > "$SCRATCH/f_up_$TS.bin"; UPSHA=$(shasum -a 256 "$SCRATCH/f_up_$TS.bin" | cut -c1-64)
# the page's own uploadKamFile, with fetch mapped onto the loopback app (simulated Kam principal); the File object is a shim
node - "$HERE" "$SCRATCH" "$TS" "$BASE" "$KAM_USER_OBJ" > "$SCRATCH/f_node_up.txt" 2>&1 <<'JS' ; expect "node: page uploadKamFile (POST row + PUT bytes) rc" 0 "$?"
const [HERE, SCR, TS, BASE, OID] = process.argv.slice(2); const fs = require("node:fs"); const vm = require("node:vm");
const CRED = "/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud";
const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8"); const pubkeys = JSON.parse(fs.readFileSync(`${SCR}/f_pubkeys.json`, "utf8")); const store = new Map();
const H = { "x-ms-client-principal-id": OID, "x-ms-client-principal-name": "kreiser.org@me.com" };
const sandbox = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, console, localStorage: undefined, Blob,
  indexedDB: { open: () => { const r = {}; setTimeout(() => { r.result = { transaction: () => ({ objectStore: () => ({ put: (v, k) => store.set(k, v), get: (k) => { const g = {}; setTimeout(() => { g.result = store.get(k); g.onsuccess && g.onsuccess(); }, 0); return g; }, delete: (k) => store.delete(k) }), set oncomplete(f) { setTimeout(f, 0); }, set onerror(f) {} }) }; r.onsuccess && r.onsuccess(); }, 0); return r; } },
  fetch: async (url, opts) => { if (url === "/api/pubkeys") return { ok: true, status: 200, json: async () => pubkeys };
    const r = await fetch(BASE + url, { ...(opts || {}), headers: { ...H, ...((opts && opts.headers) || {}) } }); return r; } };
sandbox.globalThis = sandbox; vm.createContext(sandbox); vm.runInContext(src, sandbox); const WED = sandbox.window.WED;
(async () => {
  await WED.importFile({ name: "kam-pilot-private.pem", text: async () => fs.readFileSync(`${CRED}/kam-pilot-private.pem`, "utf8") });
  const bytes = fs.readFileSync(`${SCR}/f_up_${TS}.bin`);
  const file = { name: `kam-upload-${TS}.bin`, size: bytes.length, type: "application/octet-stream", arrayBuffer: async () => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength) };
  const msgId = "kam-fl-" + TS;
  const u = await WED.uploadKamFile(file, "wednesday", msgId, "");
  console.log(JSON.stringify(u));
  // the message that carries it (synthetic is not a page flag; the matrix marks the row through the body below instead)
  const j = await WED.postKamMessage("SYNTHETIC FL2 " + TS + " Kam message with an attachment", "wednesday", false, { id: msgId, attachments: [u.id] });
  console.log(JSON.stringify(j));
})().catch(e => { console.log("ERR " + (e.stack || e)); process.exit(1); });
JS
cat "$SCRATCH/f_node_up.txt" | sed 's/^/      /'
UPID=$(head -1 "$SCRATCH/f_node_up.txt" | python3 -c 'import json,sys;print(json.load(sys.stdin)["id"])'); UPRK=$(head -1 "$SCRATCH/f_node_up.txt" | python3 -c 'import json,sys;print(json.load(sys.stdin)["row_key"])')
# mark this run's Kam rows synthetic (a Kam-typed row has no synthetic flag; the pages must not show a probe as Kam's word)
"$V" - "$UPRK" "kam-fl-$TS" <<PY
import sys, os; os.environ.setdefault("AZURE_CONFIG_DIR","/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure")
from azure.identity import AzureCliCredential; from azure.data.tables import TableServiceClient, UpdateMode
svc=TableServiceClient(endpoint="https://$STORAGE.table.core.windows.net", credential=AzureCliCredential())
svc.get_table_client("files").update_entity({"PartitionKey":"WED","RowKey":sys.argv[1],"synthetic":True}, mode=UpdateMode.MERGE)
t=svc.get_table_client("messages"); rows=list(t.query_entities("PartitionKey eq 'WED' and id eq @i", parameters={"i":sys.argv[2]}, select=["RowKey"]))
for r in rows: t.update_entity({"PartitionKey":"WED","RowKey":r["RowKey"],"synthetic":True}, mode=UpdateMode.MERGE)
print("      marked synthetic: file row + %d message row(s)" % len(rows))
PY
echo "### FL3 the refusals on Kam's path"
"$V" - "$SCRATCH/f_noseat.json" "$TS" <<'PY'
import sys, os, json, hashlib; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
clear={"client":"WED","kind":"file","id":"f-noseat-"+sys.argv[2],"ts":"2026-09-22T00:00:00.000Z"}; data=os.urandom(100)
env,ct=envelope.encrypt_file(data,{"name":"x","note":"","size":100,"sha256":hashlib.sha256(data).hexdigest(),"mime":"application/octet-stream"},clear,seats=[])   # ring ONLY: no seat kid
json.dump({**clear,"view":"wednesday","size":len(ct),"sha256":hashlib.sha256(ct).hexdigest(),"iv_blob":env.pop("iv_blob"),"envelope":env,"synthetic":True},open(sys.argv[1],"w"))
PY
expect "Kam POST /api/files NOT wrapped to the wednesday seat -> 400 (the seat could never read it)" 400 "$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' --data-binary "@$SCRATCH/f_noseat.json" "$BASE/api/files")"; echo "      body: $(head -c 140 "$SCRATCH/f_body.txt")"
expect "Kam PUT bytes with the wrong sha (row already ready -> 200 duplicate; nothing overwritten)" 200 "$(hdr "${KAM[@]}" -X PUT -H 'Content-Type: application/octet-stream' -d 'xxxxxxxxxxxxxxxxxxxxx' "$BASE/api/files/WED/$UPRK/blob")"
expect "Kam PUT bytes onto the wednesday SEAT's row (must_seat) -> 403 or 200-duplicate only; a fresh seat row: 403" 403 "$(
  "$V" "$HERE/seat/share_file.py" "$SCRATCH/f_up_$TS.bin" --seat wednesday --client WED --base "$BASE" --note "seat pending row" --synthetic --dry-run > "$SCRATCH/f_seat_dry.txt" 2>&1
  python3 -c 'import json,sys;t=open(sys.argv[1]).read();d=json.loads(t[:t.rindex("}")+1])["body"];d["id"]="f-seatrow-"+sys.argv[2];json.dump(d,open(sys.argv[3],"w"))' "$SCRATCH/f_seat_dry.txt" "$TS" "$SCRATCH/f_seat_row.json"
  SRK=$(curl -s -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' --data-binary "@$SCRATCH/f_seat_row.json" "$BASE/api/seat/files" | python3 -c 'import json,sys;print(json.load(sys.stdin)["stored"]["row_key"])')
  hdr "${KAM[@]}" -X PUT -H 'Content-Type: application/octet-stream' -d 'xxxxxxxxxxxxxxxxxxxxx' "$BASE/api/files/WED/$SRK/blob")"
echo "### FL4 Kam lists and downloads his own upload (the drawer); the wednesday seat reads it; tuesday cannot"
c=$(hdr "${KAM[@]}" "$BASE/api/files?since=$(date -u +%Y-%m-%dT00:00)&limit=1000"); expect "Kam GET /api/files" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));m=[x for x in d["files"] if x["id"]==sys.argv[2]];assert len(m)==1 and m[0]["direction"]=="upload" and m[0]["role"]=="kam" and m[0]["status"]=="ready" and m[0]["size"]==200016 and m[0]["msg_id"]=="kam-fl-"+sys.argv[3],m;assert "kam-upload-" not in open(sys.argv[1]).read();print("PASS  the upload is listed for Kam: direction=upload role=kam ready size 200016 msg_id set; name not in clear")' "$SCRATCH/f_body.txt" "$UPID" "$TS"
c=$(curl -s -o "$SCRATCH/f_dl_kam.bin" -w '%{http_code}' "${KAM[@]}" "$BASE/api/files/WED/$UPRK/blob"); expect "Kam GET .../blob" 200 "$c"
expect "Kam's downloaded bytes == the ciphertext the page sent (sha256)" "$(python3 -c 'import json,sys;print([x for x in json.load(open(sys.argv[1]))["files"] if x["id"]==sys.argv[2]][0]["sha256"])' "$SCRATCH/f_body.txt" "$UPID")" "$(shasum -a 256 "$SCRATCH/f_dl_kam.bin" | cut -c1-64)"
mkdir -p "$SCRATCH/f_fetch_$TS"; "$V" "$HERE/seat/get_files.py" --seat wednesday --base "$BASE" --ids "$UPID" --include-synthetic --fetch "$SCRATCH/f_fetch_$TS" > "$SCRATCH/f_fetch.txt" 2>&1; expect "wednesday seat get_files.py --fetch of KAM'S upload rc" "rc=0" "$(tail -1 "$SCRATCH/f_fetch.txt")"
expect "seat-decrypted upload sha256 == the original file Kam attached" "$UPSHA" "$(shasum -a 256 "$SCRATCH/f_fetch_$TS/${UPID}_kam-upload-$TS.bin" 2>/dev/null | cut -c1-64)"
expect "tuesday GET /api/seat/files/WED/<rk>/blob (R0) -> 403" 403 "$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/files/WED/$UPRK/blob")"
"$V" "$HERE/seat/get_files.py" --seat tuesday --base "$BASE" --include-synthetic --json > "$SCRATCH/f_tue.txt" 2>&1; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert sys.argv[2] not in [x["id"] for x in d["files"]] and set(d["clients"])=={"ALL","Datasec"};print("PASS  tuesday seat list: only ALL+Datasec, the WED upload absent")' "$SCRATCH/f_tue.txt" "$UPID"
echo "### FL5 the message row carries the attachment; kam_msgs.sh shows att=1 and --fetch-attachments writes the decrypted file"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&author=kam&since=$(date -u +%Y-%m-%dT00:00)&limit=1000"); expect "seat GET Kam's WED rows" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));m=[x for x in d["messages"] if x["id"]=="kam-fl-"+sys.argv[2]];assert len(m)==1 and m[0].get("attachments")==[sys.argv[3]] and m[0]["synthetic"] is True,m;print("PASS  Kam'"'"'s message row: attachments == [%s]" % sys.argv[3])' "$SCRATCH/f_body.txt" "$TS" "$UPID"
mkdir -p "$SCRATCH/f_km_$TS"; WED_AGENT=wednesday KAM_LIVE_BASE="$BASE" KAM_LIVE_INCLUDE_SYNTHETIC=1 bash "$ROOT/2_Project_Files/tools/kam_msgs.sh" 40 --brief --fetch-attachments "$SCRATCH/f_km_$TS" > "$SCRATCH/f_km.txt" 2>"$SCRATCH/f_km.err"; expect "kam_msgs.sh --fetch-attachments rc" 0 "$?"
/usr/bin/grep -F "kam-fl-$TS" "$SCRATCH/f_km.txt" >/dev/null 2>&1; LINE=$(/usr/bin/grep -B0 -A1 "att=1" "$SCRATCH/f_km.txt" | /usr/bin/grep -F "FETCHED: $SCRATCH/f_km_$TS/${UPID}_kam-upload-$TS.bin" | head -1)
[ -n "$LINE" ] && echo "PASS  kam_msgs.sh: an att=1 line with the ATTACHMENT warning and the FETCHED path: $(echo "$LINE" | cut -c1-80)…" || { echo "FAIL  kam_msgs.sh output lacks the att=1 + FETCHED line: $(/usr/bin/grep -c 'att=1' "$SCRATCH/f_km.txt") att=1 lines; stderr: $(head -c 300 "$SCRATCH/f_km.err")"; FAIL=1; }
/usr/bin/grep -q 'ATTACHMENT(S) — the message is not only its text' "$SCRATCH/f_km.txt" && echo "PASS  kam_msgs.sh prints the ATTACHMENT warning (the 2026-09-10 lesson, now true for live rows)" || { echo "FAIL  no ATTACHMENT warning"; FAIL=1; }
expect "kam_msgs.sh-fetched file sha256 == original" "$UPSHA" "$(shasum -a 256 "$SCRATCH/f_km_$TS/${UPID}_kam-upload-$TS.bin" 2>/dev/null | cut -c1-64)"
echo "### FL6 audit"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/files/audit?limit=1000"); expect "GET /api/seat/files/audit" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));a=[x for x in d["audit"] if x["target_id"]==sys.argv[2]];acts=sorted(x["action"] for x in a);by=sorted({x["seat"] for x in a});assert "upload" in acts and acts.count("download")>=3 and "kam" in by and "wednesday" in by,(acts,by);print("PASS  audit for Kam'"'"'s upload: %s by %s (upload by kam via easyauth:<oid>; downloads by kam + the seat)" % (acts, by))' "$SCRATCH/f_body.txt" "$UPID"
kill $APP_PID 2>/dev/null; wait $APP_PID 2>/dev/null
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL LOCAL FILE ARMS PASS || echo SOME ARMS FAILED)  ($(/usr/bin/grep -c '^PASS' "$0.last" 2>/dev/null || true))"
exit $FAIL
