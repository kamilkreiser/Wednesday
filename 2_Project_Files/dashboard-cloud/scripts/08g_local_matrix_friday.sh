#!/usr/bin/env bash
# Friday seat + file-hide local matrix (2026-09-23; brief 2_Project_Files/fleet/briefs_staged/2026-09-23_friday_liveboard_builder.md).
# The app (app/main.py, unmodified) runs on loopback :47796 over the IN-MEMORY test double scripts/08g_double_app.py — NOTHING in
# this matrix can write the live storage account (Wednesday 11:16: "STOP posting to the LIVE board from any local matrix"); the
# last section PROVES it (0 rows with this run's ids on the live store, read-only query; the double's credential was never called).
# Seat tokens are REAL (the three seats' certificates against Entra). Kam's messages are made by the page's OWN common.js in Node
# WebCrypto (the 08c pattern) and posted with a simulated Easy Auth principal (the only unattended way past Easy Auth).
# Arms (each can fail): FR1 health/pubkeys · FR2 friday token roles · FR3 friday writes Friday 201, 403 on Secuura/Datasec/WED ·
# FR4 friday reads Friday + ALL, nothing of Secuura/Datasec/WED · FR5 wednesday/tuesday 403 writing Friday, cannot read Friday rows ·
# FR6 Kam view=friday -> Friday, wrapped to ring + friday ONLY; seat guard; the friday seat decrypts, the others cannot; view=both ->
# 3 seats · FR7 file hide (own row hidden -> absent from seat + viewer lists, ?hidden=1 reveals, other seat refused 403, audit
# row, unhide restores, row otherwise untouched) · FR8 message hide ownership for Friday rows · FR9 usage chip row for friday ·
# FR10 no-live-store proof.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
SCRATCH=${SCRATCH:?set SCRATCH to a scratch dir}
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
export TENANT_ID SEAT_API_APPID=$API_APPID SEAT_APP_MAP="$wednesday_seat_APPID:wednesday,$tuesday_seat_APPID:tuesday,$friday_seat_APPID:friday" KAM_OBJECT_ID=$KAM_USER_OBJ
unset STORAGE_ACCOUNT
PORT=47796; BASE="http://127.0.0.1:$PORT"; FAIL=0; NPASS=0
case "$BASE" in http://127.0.0.1:*|http://localhost:*) ;; *) echo "REFUSED: base $BASE is not loopback"; exit 2 ;; esac   # never the live host
( "$V" "$HERE/scripts/08g_double_app.py" --port $PORT > "$SCRATCH/g_app.log" 2>&1 ) &
APP_PID=$!
for i in $(seq 1 120); do curl -s -o /dev/null "$BASE/api/seat/health" && break; sleep 1; done
curl -s -o /dev/null "$BASE/api/seat/health" || { echo "FAIL  double app did not come up in 120 s: $(tail -5 "$SCRATCH/g_app.log" | tr "\n" " ")"; kill $APP_PID 2>/dev/null; exit 1; }
expect() { if [ "$2" = "$3" ]; then echo "PASS  $1: expected $2 got $3"; else echo "FAIL  $1: expected $2 got $3"; FAIL=1; fi; }
hdr() { curl -s -o "$SCRATCH/g_body.txt" -w '%{http_code}' --max-time 30 "$@"; }
pyarm() { python3 -c "$1" "${@:2}" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }; }
KAM=(-H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'x-ms-client-principal-name: kreiser.org@me.com')
mktok() { "$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","$1","--client","$2"]); print(sc.get_token(a, sc.load_ids()))
PY
}
TOKF=$(mktok friday Friday); TOKW=$(mktok wednesday WED); TOKT=$(mktok tuesday Datasec)
TS=$(date -u +%H%M%S); FTS="2026-09-23T00:00:$(date -u +%S).000Z"
dump() { curl -s --max-time 30 "$BASE/__double/dump" > "$SCRATCH/g_dump.json"; }

echo "### FR0 the double is the store (positive control) and the live store is unreachable from it"
c=$(hdr "$BASE/__double/proof"); expect "GET /__double/proof" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["storage_account"]=="nolivestore-double" and d["credential_calls"]==0,d;print("PASS  double: STORAGE_ACCOUNT=%s, credential_calls=0 before any arm" % d["storage_account"])' "$SCRATCH/g_body.txt"

echo "### FR1 health + pubkeys"
c=$(hdr "$BASE/api/seat/health"); expect "health" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["file_hide_route"] is True and d["seats"]==["wednesday","tuesday","friday"] and "Friday" in d["clients"] and d["seat_keys"]==["friday","tuesday","wednesday"] and d["hide_route"] and d["file_route"],d;print("PASS  health: file_hide_route, seats=%s, clients=%s, seat_keys=%s" % (d["seats"],d["clients"],d["seat_keys"]))' "$SCRATCH/g_body.txt"
c=$(hdr "${KAM[@]}" "$BASE/api/pubkeys"); expect "GET /api/pubkeys as Kam" 200 "$c"; cp "$SCRATCH/g_body.txt" "$SCRATCH/g_pubkeys.json"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));s=d["seat_of_client"];assert len(d["kam"])==3 and set(d["seats"])=={"wednesday","tuesday","friday"} and s["Friday"]==["friday"] and s["ALL"]==["wednesday","tuesday","friday"] and s["Datasec"]==["tuesday"] and s["WED"]==["wednesday"] and s["Secuura"]==["wednesday"];assert all("PRIVATE" not in v["pem"] for v in d["seats"].values());print("PASS  pubkeys: 3 Kam keys + 3 seat keys (friday kid %s); seat_of_client Friday->[friday], ALL->3 seats, others unchanged" % d["seats"]["friday"]["kid"])' "$SCRATCH/g_pubkeys.json"
FKID=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["seats"]["friday"]["kid"])' "$SCRATCH/g_pubkeys.json")
FILEKID=$(openssl pkey -pubin -in "$HERE/app/keys/friday-seat-public.pub" -outform DER | openssl dgst -sha256 | sed 's/^.*= //' | cut -c1-16)
expect "served friday kid == kid of app/keys/friday-seat-public.pub" "$FILEKID" "$FKID"
CERTKID=$(openssl x509 -in "$CRED/friday-seat.crt" -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256 | sed 's/^.*= //' | cut -c1-16)
expect "friday-seat.crt public key == the served friday key" "$FKID" "$CERTKID"

echo "### FR2 the friday token: roles exactly Seat.Write, Seat.Read, Client.Friday"
"$V" "$HERE/seat/post_message.py" --seat friday --client Friday --text x --token-only > "$SCRATCH/g_claims.json" 2>"$SCRATCH/g_claims.err"; expect "post_message.py --seat friday --token-only rc" 0 "$?"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));r=sorted(d["roles"]);assert r==["Client.Friday","Seat.Read","Seat.Write"] and d["azp"]==sys.argv[2],d;print("PASS  friday token roles=%s azp=friday-seat appId (no Client.Secuura/Datasec/WED)" % r)' "$SCRATCH/g_claims.json" "$friday_seat_APPID"

echo "### FR3 friday writes: Friday 201; Secuura / Datasec / WED 403"
post() { "$V" "$HERE/seat/post_message.py" --seat "$1" --client "$2" --base "$BASE" --text "$3" --id "$4" --ts "$FTS" --synthetic 2>"$SCRATCH/g_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["status"])'; }
RF="fri-l-$TS"; RW="fri-l-wed-$TS"; RT="fri-l-tue-$TS"; RKF="${FTS}_$RF"; RKW="${FTS}_$RW"
expect "friday posts to Friday" 201 "$(post friday Friday "SYNTHETIC friday matrix $TS — friday's own row" "$RF")"
for c in Secuura Datasec WED; do expect "friday posts to $c (MUST refuse, R0)" 403 "$(post friday $c "SYNTHETIC friday matrix $TS must be refused" "fri-l-x$c-$TS")"; done
expect "wednesday posts its WED fixture row" 201 "$(post wednesday WED "SYNTHETIC friday matrix $TS — wednesday fixture" "$RW")"
expect "tuesday posts her Datasec fixture row" 201 "$(post tuesday Datasec "SYNTHETIC friday matrix $TS — tuesday fixture" "$RT")"
dump; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));m=d["tables"]["messages"];ids=[(r["PartitionKey"],r["id"]) for r in m];assert ("Friday",sys.argv[2]) in ids;assert not any(i.startswith("fri-l-x") for _,i in ids),ids;r=[x for x in m if x["id"]==sys.argv[2]][0];assert r["seat"]=="friday" and r["written_by"]==sys.argv[3] and r["synthetic"] is True;print("PASS  raw (double): the Friday row is seat=friday, written_by=friday-seat appId, synthetic; the three refused rows were NOT stored")' "$SCRATCH/g_dump.json" "$RF" "$friday_seat_APPID"

echo "### FR4 friday reads: Friday + ALL; nothing of Secuura / Datasec / WED"
c=$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/messages?since=$FTS&limit=1000"); expect "friday default list" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["clients"]==["ALL","Friday"],d["clients"];cs={m["client"] for m in d["messages"]};ids=[m["id"] for m in d["messages"]];assert cs<={"ALL","Friday"} and sys.argv[2] in ids and sys.argv[3] not in ids and sys.argv[4] not in ids,(cs,ids);print("PASS  friday default list: partitions %s, its row present, the WED + Datasec fixtures absent" % d["clients"])' "$SCRATCH/g_body.txt" "$RF" "$RW" "$RT"
expect "friday reads client=Friday" 200 "$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/messages?client=Friday&since=$FTS")"
expect "friday reads client=ALL" 200 "$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/messages?client=ALL&since=$FTS")"
for c in Secuura Datasec WED; do expect "friday reads client=$c (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/messages?client=$c&since=$FTS")"; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert "messages" not in d,d;print("PASS  refusal body carries no rows")' "$SCRATCH/g_body.txt"; done
expect "friday lists files client=WED (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/files?client=WED")"

echo "### FR5 wednesday / tuesday: 403 writing Friday; cannot read Friday rows"
expect "wednesday posts to Friday (MUST refuse)" 403 "$(post wednesday Friday "SYNTHETIC must be refused" "fri-l-wx-$TS")"
expect "tuesday posts to Friday (MUST refuse)" 403 "$(post tuesday Friday "SYNTHETIC must be refused" "fri-l-tx-$TS")"
expect "wednesday reads client=Friday (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TOKW" "$BASE/api/seat/messages?client=Friday&since=$FTS")"
expect "tuesday reads client=Friday (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/messages?client=Friday&since=$FTS")"
c=$(hdr -H "Authorization: Bearer $TOKW" "$BASE/api/seat/messages?since=$FTS&limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert "Friday" not in d["clients"] and not any(m["client"]=="Friday" for m in d["messages"]) and sys.argv[2] not in [m["id"] for m in d["messages"]];print("PASS  wednesday default list %s: no Friday row" % d["clients"])' "$SCRATCH/g_body.txt" "$RF"
c=$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/messages?since=$FTS&limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert "Friday" not in d["clients"] and not any(m["client"]=="Friday" for m in d["messages"]);print("PASS  tuesday default list %s: no Friday row" % d["clients"])' "$SCRATCH/g_body.txt"
"$V" "$HERE/seat/get_kam_messages.py" --seat wednesday --base "$BASE" --client Friday --json > "$SCRATCH/g_gkm_wf.txt" 2>&1; expect "get_kam_messages.py --seat wednesday --client Friday (MUST fail)" 1 "$?"

echo "### FR6 Kam types on the FRIDAY tab: view=friday -> Friday, wrapped to ring + friday ONLY"
node - "$HERE" "$SCRATCH/g_pubkeys.json" "$TS" > "$SCRATCH/g_kam_bodies.json" <<'EOF2'
import fs from "node:fs"; import vm from "node:vm";
const [HERE, pk, TS] = process.argv.slice(2); const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8"); const pubkeys = JSON.parse(fs.readFileSync(pk, "utf8"));
const sb = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, console, localStorage: undefined, indexedDB: undefined,
  fetch: async (url) => { if (url === "/api/pubkeys") return { ok: true, status: 200, json: async () => pubkeys }; throw new Error("unexpected " + url); } };
sb.globalThis = sb; vm.createContext(sb); vm.runInContext(src, sb); const WED = sb.window.WED;
const text = `SYNTHETIC Kam to Friday from the 08g double ${TS} (page module)`;
if (WED.VIEW_TO_CLIENT.friday !== "Friday") throw new Error("page VIEW_TO_CLIENT.friday = " + WED.VIEW_TO_CLIENT.friday);
const mk = async (view, id) => { const client = WED.VIEW_TO_CLIENT[view]; const clear = { client, kind: "message", id, ts: new Date().toISOString(), view }; return { client, view, id, ts: clear.ts, envelope: await WED.encryptText(text, clear) }; };
const good = await mk("friday", `fri-kam-${TS}`);
const noseat = JSON.parse(JSON.stringify(await mk("friday", `fri-kam-noseat-${TS}`))); noseat.envelope.wrapped_keys = noseat.envelope.wrapped_keys.filter(e => e.kid !== pubkeys.seats.friday.kid);
const both = await mk("both", `fri-kam-both-${TS}`);
const agent = WED.agentOfRow({ role: "kam", view: "friday", client: "Friday" }) + "|" + WED.agentOfRow({ role: "friday", seat: "friday", client: "Friday" }) + "|" + WED.agentOfRow({ seat: "tuesday", client: "Datasec" }) + "|" + WED.agentOfRow({ seat: "wednesday", client: "WED" });
console.log(JSON.stringify({ text, good, noseat, both, agent }));
EOF2
expect "page module built the three bodies (node rc)" 0 "$?"
body() { python3 -c 'import json,sys;print(json.dumps(json.load(open(sys.argv[1]))[sys.argv[2]]))' "$SCRATCH/g_kam_bodies.json" "$1"; }
EXPECTED=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["text"])' "$SCRATCH/g_kam_bodies.json")
expect "page agentOfRow: kam/friday, friday seat, tuesday, wednesday" "friday|friday|tuesday|wednesday" "$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["agent"])' "$SCRATCH/g_kam_bodies.json")"
c=$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' -d "$(body noseat)" "$BASE/api/kam/messages"); expect "Kam view=friday NOT wrapped to the friday seat (server guard)" 400 "$c"; echo "      body: $(head -c 150 "$SCRATCH/g_body.txt")"
c=$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' -d "$(body good)" "$BASE/api/kam/messages"); expect "Kam view=friday wrapped to ring + friday" 201 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["stored"]["client"]=="Friday",d;print("PASS  stored in partition Friday")' "$SCRATCH/g_body.txt"
c=$(hdr "${KAM[@]}" -X POST -H 'Content-Type: application/json' -d "$(body both)" "$BASE/api/kam/messages"); expect "Kam view=both -> ALL" 201 "$c"
dump; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));p=json.load(open(sys.argv[2]));m={r["id"]:r for r in d["tables"]["messages"]};r=m["fri-kam-"+sys.argv[3]];b=m["fri-kam-both-"+sys.argv[3]]
ring={k["kid"] for k in p["kam"]};S={s:v["kid"] for s,v in p["seats"].items()}
kr={e["kid"] for e in json.loads(r["wrapped_keys"])};kb={e["kid"] for e in json.loads(b["wrapped_keys"])}
assert r["PartitionKey"]=="Friday" and r["view"]=="friday" and r["role"]=="kam",r
assert kr==ring|{S["friday"]},(kr,ring,S);assert S["wednesday"] not in kr and S["tuesday"] not in kr
assert kb==ring|set(S.values()),kb;assert "fri-kam-noseat-"+sys.argv[3] not in m
print("PASS  raw Friday row: kids == Kam ring (3) + friday; wednesday + tuesday kids ABSENT");print("PASS  raw ALL row: kids == ring + all THREE seats; the refused body was not stored")' "$SCRATCH/g_dump.json" "$SCRATCH/g_pubkeys.json" "$TS"
"$V" "$HERE/seat/get_kam_messages.py" --seat friday --base "$BASE" --decrypt --json --since "$FTS" > "$SCRATCH/g_gkm_f.json" 2>"$SCRATCH/g_gkm_f.err"; expect "get_kam_messages.py --seat friday --decrypt rc" 0 "$?"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));m={r["id"]:r for r in d["messages"]};t=sys.argv[3];assert m["fri-kam-"+t].get("text")==sys.argv[2],m.get("fri-kam-"+t);assert m["fri-kam-both-"+t].get("text")==sys.argv[2];assert d["clients"]==["ALL","Friday"];print("PASS  the friday seat reads + decrypts Kam'"'"'s view=friday row AND his view=both row with friday-seat.pem")' "$SCRATCH/g_gkm_f.json" "$EXPECTED" "$TS"
"$V" "$HERE/seat/get_kam_messages.py" --seat wednesday --base "$BASE" --json --since "$FTS" > "$SCRATCH/g_gkm_w.json" 2>"$SCRATCH/g_gkm_w.err"; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[r["id"] for r in d["messages"]];assert "fri-kam-"+sys.argv[2] not in ids and "fri-kam-both-"+sys.argv[2] in ids;print("PASS  the wednesday seat does NOT receive the Friday row (it does receive the ALL row)")' "$SCRATCH/g_gkm_w.json" "$TS"
"$V" - "$SCRATCH/g_dump.json" "$EXPECTED" "$TS" <<'PY' || FAIL=1
import json,sys; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
CRED="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"; d=json.load(open(sys.argv[1])); r=[x for x in d["tables"]["messages"] if x["id"]=="fri-kam-"+sys.argv[3]][0]
clear={"client":r["PartitionKey"],"kind":r["kind"],"id":r["id"],"ts":r["ts"]}
assert sys.argv[2] not in json.dumps(r)
for k in ("kam-pilot-private.pem","kam-laptop-private.pem","kam-ipad-private.pem","friday-seat.pem"):
    assert envelope.decrypt_text(envelope.load_private(f"{CRED}/{k}"), r, clear)==sys.argv[2]; print(f"PASS  {k} opens Kam's view=friday row")
for k in ("wednesday-seat.pem","tuesday-seat.pem"):
    try: envelope.decrypt_text(envelope.load_private(f"{CRED}/{k}"), r, clear); print(f"FAIL  {k} opened a Friday row"); sys.exit(1)
    except KeyError: print(f"PASS  {k} refused (KeyError: not a recipient)")
PY

echo "### FR7 file hide: the owner hides its own FILE row; others refused; audit; unhide restores"
printf 'SYNTHETIC friday file %s\n' "$TS" > "$SCRATCH/g_file_$TS.txt"
"$V" "$HERE/seat/share_file.py" "$SCRATCH/g_file_$TS.txt" --seat friday --base "$BASE" --synthetic --note "08g" > "$SCRATCH/g_share.txt" 2>&1; expect "share_file.py --seat friday (default client Friday) rc" "rc=0" "$(tail -1 "$SCRATCH/g_share.txt")"
FRK=$(sed -n 's/.*row_key=\([^ ]*\) client=Friday.*/\1/p' "$SCRATCH/g_share.txt"); FID=$(sed -n 's/^file_id=\([^ ]*\) .*/\1/p' "$SCRATCH/g_share.txt"); echo "      friday file: $FID row $FRK"
"$V" "$HERE/seat/share_file.py" "$SCRATCH/g_file_$TS.txt" --seat wednesday --base "$BASE" --synthetic --note "08g wed" > "$SCRATCH/g_share_w.txt" 2>&1; expect "share_file.py --seat wednesday (WED) rc" "rc=0" "$(tail -1 "$SCRATCH/g_share_w.txt")"
WRK=$(sed -n 's/.*row_key=\([^ ]*\) client=WED.*/\1/p' "$SCRATCH/g_share_w.txt")
dump; cp "$SCRATCH/g_dump.json" "$SCRATCH/g_dump_before_filehide.json"
c=$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/files"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));rk=[f["row_key"] for f in d["files"]];assert sys.argv[2] in rk and d["clients"]==["ALL","Friday"];print("PASS  before: the friday file is listed for the friday seat")' "$SCRATCH/g_body.txt" "$FRK"
c=$(hdr "${KAM[@]}" "$BASE/api/files"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));rk=[f["row_key"] for f in d["files"]];assert sys.argv[2] in rk and sys.argv[3] in rk;print("PASS  before: both files listed in the viewer drawer (/api/files)")' "$SCRATCH/g_body.txt" "$FRK" "$WRK"
expect "wednesday hides the FRIDAY file row (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKW" -H 'Content-Type: application/json' -d '{"client":"Friday","kind":"file","row_key":"'$FRK'"}' "$BASE/api/seat/hide")"
expect "tuesday hides the FRIDAY file row (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKT" -H 'Content-Type: application/json' -d '{"client":"Friday","kind":"file","row_key":"'$FRK'"}' "$BASE/api/seat/hide")"
expect "friday hides the WEDNESDAY file row (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"WED","kind":"file","row_key":"'$WRK'"}' "$BASE/api/seat/hide")"
expect "unknown kind -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"Friday","kind":"card","row_key":"'$FRK'"}' "$BASE/api/seat/hide")"
expect "kind=file, unknown row -> 404" 404 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"Friday","kind":"file","row_key":"2026-09-23T00:00:00.000Z_f-nosuch"}' "$BASE/api/seat/hide")"
expect "kind=message on the FILE row key -> 404 (the discriminator picks the table)" 404 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"Friday","row_key":"'$FRK'"}' "$BASE/api/seat/hide")"
"$V" "$HERE/seat/hide_message.py" --seat friday --client Friday --file --base "$BASE" --row-key "$FRK" --reason "08g friday hides its own file row" > "$SCRATCH/g_fh1.txt" 2>&1; expect "hide_message.py --seat friday --file hides its own file row rc" "rc=0" "$(tail -1 "$SCRATCH/g_fh1.txt")"; echo "      $(tail -2 "$SCRATCH/g_fh1.txt" | head -1 | cut -c1-170)"
c=$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/files"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));rk=[f["row_key"] for f in d["files"]];assert sys.argv[2] not in rk and d["hidden_included"] is False;print("PASS  after: the friday file is ABSENT from the seat list")' "$SCRATCH/g_body.txt" "$FRK"
c=$(hdr "${KAM[@]}" "$BASE/api/files"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));rk=[f["row_key"] for f in d["files"]];assert sys.argv[2] not in rk and sys.argv[3] in rk;print("PASS  after: ABSENT from the viewer drawer (file_query skips it); the wednesday file still listed")' "$SCRATCH/g_body.txt" "$FRK" "$WRK"
c=$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/files?hidden=1"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));f=[x for x in d["files"] if x["row_key"]==sys.argv[2]];assert len(f)==1 and f[0]["hidden"] is True and f[0]["hidden_seat"]=="friday" and d["hidden_included"] is True;print("PASS  ?hidden=1 reveals it: hidden=true, hidden_seat=friday")' "$SCRATCH/g_body.txt" "$FRK"
"$V" "$HERE/seat/hide_message.py" --seat friday --client Friday --file --base "$BASE" --list-hidden > "$SCRATCH/g_fh2.txt" 2>&1; expect "hide_message.py --list-hidden --file rc" "rc=0" "$(tail -1 "$SCRATCH/g_fh2.txt")"; /usr/bin/grep -q -- "Friday/$FRK " "$SCRATCH/g_fh2.txt" && { echo "PASS  --list-hidden --file shows Friday/$FRK"; } || { echo "FAIL  --list-hidden --file: $(tr '\n' ' ' < "$SCRATCH/g_fh2.txt" | cut -c1-300)"; FAIL=1; }
dump; pyarm 'import json,sys;b={(r["PartitionKey"],r["RowKey"]):r for r in json.load(open(sys.argv[1]))["tables"]["files"]};a={(r["PartitionKey"],r["RowKey"]):r for r in json.load(open(sys.argv[2]))["tables"]["files"]};k=("Friday",sys.argv[3]);x,y=b[k],a[k]
new=sorted(set(y)-set(x));assert new==["hidden","hidden_at","hidden_by","hidden_seat"],new;assert all(y[c]==x[c] for c in x),"ROW MUTATED BEYOND THE HIDE COLUMNS";assert b[("WED",sys.argv[4])]==a[("WED",sys.argv[4])]
aud=[r for r in json.load(open(sys.argv[2]))["tables"]["messages"] if r["PartitionKey"]=="AUDIT" and r.get("target_row_key")==sys.argv[3] and r.get("kind")=="hide_audit"];assert len(aud)==1,aud;z=aud[0];assert z["action"]=="hide" and z["target_kind"]=="file" and z["seat"]=="friday" and z["target_client"]=="Friday" and z["changed"] is True and z["reason"]=="08g friday hides its own file row",z
print("PASS  raw file row: ONLY hidden/hidden_at/hidden_by/hidden_seat added (envelope, blob, sha256, status byte-identical); the wednesday file row untouched");print("PASS  ONE audit row (messages/AUDIT, kind=hide_audit, target_kind=file, seat=friday, reason) for the hide; the 3 refused attempts wrote none")' "$SCRATCH/g_dump_before_filehide.json" "$SCRATCH/g_dump.json" "$FRK" "$WRK"
c=$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/hide/audit"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));a=[x for x in d["audit"] if x["target_row_key"]==sys.argv[2]];assert len(a)==1 and a[0]["target_kind"]=="file" and d["clients"]==["ALL","Friday"];print("PASS  GET /api/seat/hide/audit (friday) lists the file hide")' "$SCRATCH/g_body.txt" "$FRK"
c=$(hdr -H "Authorization: Bearer $TOKW" "$BASE/api/seat/hide/audit"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert not any(x["target_row_key"]==sys.argv[2] for x in d["audit"]);print("PASS  the wednesday seat does NOT see the Friday file hide in its audit")' "$SCRATCH/g_body.txt" "$FRK"
expect "wednesday UNHIDES the friday file (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKW" -H 'Content-Type: application/json' -d '{"client":"Friday","kind":"file","row_key":"'$FRK'"}' "$BASE/api/seat/unhide")"
"$V" "$HERE/seat/hide_message.py" --seat friday --client Friday --file --base "$BASE" --id "$FID" --unhide --reason "08g unhide" > "$SCRATCH/g_fh3.txt" 2>&1; expect "hide_message.py --seat friday --file --unhide by id rc" "rc=0" "$(tail -1 "$SCRATCH/g_fh3.txt")"
c=$(hdr "${KAM[@]}" "$BASE/api/files"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));rk=[f["row_key"] for f in d["files"]];assert sys.argv[2] in rk;print("PASS  after unhide: BACK in the viewer drawer")' "$SCRATCH/g_body.txt" "$FRK"
"$V" "$HERE/seat/get_files.py" --seat friday --base "$BASE" --include-synthetic --ids "$FID" --fetch "$SCRATCH/g_fetch_$TS" > "$SCRATCH/g_fetch.txt" 2>&1; expect "get_files.py --seat friday --fetch (decrypt with friday-seat.pem) rc" 0 "$?"
cmp -s "$SCRATCH/g_file_$TS.txt" "$SCRATCH/g_fetch_$TS/${FID}_g_file_$TS.txt" && echo "PASS  fetched file byte-identical to the original" || { echo "FAIL  fetched file differs / missing: $(tail -3 "$SCRATCH/g_fetch.txt" | tr '\n' ' ')"; FAIL=1; }

echo "### FR8 message hide ownership for Friday rows"
expect "wednesday hides the Friday MESSAGE row (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKW" -H 'Content-Type: application/json' -d '{"client":"Friday","row_key":"'$RKF'"}' "$BASE/api/seat/hide")"
expect "friday hides the WED message row (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKW'"}' "$BASE/api/seat/hide")"
expect "friday hides its OWN Friday message row" 200 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"Friday","row_key":"'$RKF'","reason":"08g"}' "$BASE/api/seat/hide")"
c=$(hdr -H "Authorization: Bearer $TOKF" "$BASE/api/seat/messages?client=Friday&since=$FTS"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert sys.argv[2] not in [m["id"] for m in d["messages"]];print("PASS  hidden Friday message absent from the friday list")' "$SCRATCH/g_body.txt" "$RF"
expect "friday unhides it" 200 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"Friday","row_key":"'$RKF'","reason":"08g"}' "$BASE/api/seat/unhide")"
expect "friday hides ALL (nobody's to hide)" 400 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"client":"ALL","row_key":"'$RKF'"}' "$BASE/api/seat/hide")"

echo "### FR9 usage chip: friday row null until published; token-attributed"
c=$(hdr "${KAM[@]}" "$BASE/api/usage"); expect "GET /api/usage as Kam" 200 "$c"; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert set(d)=={"wednesday","tuesday","friday"} and d["friday"] is None,d;print("PASS  /api/usage has three keys; friday = null (nothing published)")' "$SCRATCH/g_body.txt"
NOWZ=$(date -u +%Y-%m-%dT%H:%M:%SZ)
expect "friday POST usage" 201 "$(hdr -X POST -H "Authorization: Bearer $TOKF" -H 'Content-Type: application/json' -d '{"pct":7,"resets_in":"3d","ts":"'$NOWZ'"}' "$BASE/api/seat/usage")"
expect "wednesday POST usage claiming seat=friday (spoof)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKW" -H 'Content-Type: application/json' -d '{"seat":"friday","pct":99,"ts":"'$NOWZ'"}' "$BASE/api/seat/usage")"
c=$(hdr "${KAM[@]}" "$BASE/api/usage"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["friday"]["pct"]==7 and d["friday"]["seat"]=="friday" and d["friday"]["written_by"]==sys.argv[2];print("PASS  friday chip row: pct 7 written_by = friday-seat appId (the spoof wrote nothing)")' "$SCRATCH/g_body.txt" "$friday_seat_APPID"

echo "### FR10 proof: nothing reached the live store"
c=$(hdr "$BASE/__double/proof"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["credential_calls"]==0 and d["writes"]>=10,d;print("PASS  double: %d writes held in memory, credential_calls=0 (no path asked for a real Azure credential)" % d["writes"])' "$SCRATCH/g_body.txt"
az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "id eq '$RF' or id eq 'fri-kam-$TS' or id eq 'fri-kam-both-$TS' or id eq '$RW' or id eq '$RT'" --select PartitionKey RowKey -o json > "$SCRATCH/g_live_msgs.json" 2>"$SCRATCH/g_live_err.txt"; expect "read-only live query rc" 0 "$?"
az storage entity query --account-name "$STORAGE" --table-name files --auth-mode login --filter "id eq '$FID'" --select PartitionKey RowKey -o json > "$SCRATCH/g_live_files.json" 2>>"$SCRATCH/g_live_err.txt"
pyarm 'import json,sys;a=json.load(open(sys.argv[1]))["items"];b=json.load(open(sys.argv[2]))["items"];assert a==[] and b==[],(a,b);print("PASS  live store: 0 message rows and 0 file rows carry this run'"'"'s ids")' "$SCRATCH/g_live_msgs.json" "$SCRATCH/g_live_files.json"
az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "id eq 'p3l-good-011552'" --select PartitionKey RowKey -o json > "$SCRATCH/g_live_ctrl.json" 2>>"$SCRATCH/g_live_err.txt"
pyarm 'import json,sys;a=json.load(open(sys.argv[1]))["items"];assert len(a)==1;print("PASS  positive control: the same query shape finds a known live row (p3l-good-011552) -> the zero above is real")' "$SCRATCH/g_live_ctrl.json"
unset TOKF TOKW TOKT
kill $APP_PID 2>/dev/null; wait $APP_PID 2>/dev/null
echo "### TALLY"
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL PASS || echo SOME FAILED)"
exit $FAIL
