#!/usr/bin/env bash
# Phase 2 local matrix — the app on loopback (transient port 47790) against the REAL storage account through the CLI
# credential, exercising the NEW routes: pages, Kam's write path (principal pinned), duplicate/updated semantics, the
# seat's author=kam read with its partition set, long option keys. Local proof only; 05_probe_live.sh repeats what it
# can live (Kam's authenticated path cannot be driven live without his MFA — that is why this matrix exists).
# SYNTHETIC text only. exit 1 on any mismatch.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
SCRATCH=${SCRATCH:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/bbb4a64c-5352-455e-b4e6-9f36320976aa/scratchpad}
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
T=$(az account show --query tenantId -o tsv); [ "$T" = "$TENANT_ID" ] || { echo "TENANT ASSERTION FAILED: $T"; exit 3; }
export TENANT_ID SEAT_API_APPID=$API_APPID STORAGE_ACCOUNT=$STORAGE SEAT_APP_MAP="$wednesday_seat_APPID:wednesday,$tuesday_seat_APPID:tuesday" KAM_OBJECT_ID=$KAM_USER_OBJ
PORT=47790; BASE="http://127.0.0.1:$PORT"; FAIL=0
( "$V" -m uvicorn main:app --app-dir "$HERE/app" --host 127.0.0.1 --port $PORT --log-level warning > "$SCRATCH/wedcloud_local2.log" 2>&1 ) &
UV=$!
for i in $(seq 1 40); do curl -s -o /dev/null "$BASE/api/seat/health" && break; sleep 0.5; done
expect() { if [ "$2" = "$3" ]; then echo "PASS  $1: expected $2 got $3"; else echo "FAIL  $1: expected $2 got $3"; FAIL=1; fi; }
hdr() { curl -s -o "$SCRATCH/l_body.txt" -D "$SCRATCH/l_hdr.txt" -w '%{http_code}' --max-time 40 "$@"; }
KAM=(-H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'x-ms-client-principal-name: kreiser.org@me.com')
OTHER=(-H 'x-ms-client-principal-id: 00000000-0000-0000-0000-00000000dead' -H 'x-ms-client-principal-name: someone@else')
TS=$(date -u +%H%M%S)
echo "### P. pages"
expect "GET / no principal" 401 "$(hdr "$BASE/")"
c=$(hdr "${KAM[@]}" "$BASE/"); expect "GET / as Kam" 200 "$c"; echo "      title: $(/usr/bin/grep -o '<title>[^<]*' "$SCRATCH/l_body.txt")  bytes=$(wc -c < "$SCRATCH/l_body.txt")"
c=$(hdr "${KAM[@]}" "$BASE/chat"); expect "GET /chat as Kam" 200 "$c"; echo "      title: $(/usr/bin/grep -o '<title>[^<]*' "$SCRATCH/l_body.txt")"
c=$(hdr "${KAM[@]}" "$BASE/static/common.js"); expect "GET /static/common.js as Kam" 200 "$c"; echo "      content-type: $(/usr/bin/grep -i '^content-type' "$SCRATCH/l_hdr.txt" | tr -d '\r')"
expect "GET /static/common.js no principal" 401 "$(hdr "$BASE/static/common.js")"
c=$(hdr "${KAM[@]}" "$BASE/api/me"); expect "GET /api/me as Kam" 200 "$c"; echo "      $(cat "$SCRATCH/l_body.txt")"
c=$(hdr "${OTHER[@]}" "$BASE/api/me"); echo "      /api/me as OTHER principal: $(cat "$SCRATCH/l_body.txt")"
echo "### K. Kam's write path (POST /api/kam/messages)"
mkbody() { # view client id text -> JSON body with a real envelope (browser twin), via envelope.py
  "$V" - "$@" <<'PY'
import sys, json; sys.path.insert(0, "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
view, client, rid, text = sys.argv[1:5]
import datetime; ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
clear = {"client": client, "kind": "message", "id": rid, "ts": ts}
pub = envelope.load_public("/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/app/keys/kam-pilot-public.pub")
print(json.dumps({**clear, "view": view, "envelope": envelope.encrypt_text(pub, text, clear)}))
PY
}
B1=$(mkbody wednesday WED "kam-local-$TS" "SYNTHETIC Kam reply $TS from the local matrix (view wednesday)")
expect "POST kam NO principal" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d "$B1" "$BASE/api/kam/messages")"
c=$(hdr -X POST "${OTHER[@]}" -H 'Content-Type: application/json' -d "$B1" "$BASE/api/kam/messages"); expect "POST kam as OTHER principal (MUST refuse)" 403 "$c"; echo "      body: $(cat "$SCRATCH/l_body.txt")"
c=$(hdr -X POST "${KAM[@]}" -H 'Content-Type: application/json' -d "$B1" "$BASE/api/kam/messages"); expect "POST kam as Kam, view=wednesday" 201 "$c"; echo "      body: $(head -c 200 "$SCRATCH/l_body.txt")"
c=$(hdr -X POST "${KAM[@]}" -H 'Content-Type: application/json' -d "$B1" "$BASE/api/kam/messages"); expect "POST kam SAME row again (idempotent)" 200 "$c"; echo "      body: $(head -c 200 "$SCRATCH/l_body.txt")"
B2=$(mkbody both ALL "kam-local-both-$TS" "SYNTHETIC Kam broadcast $TS (view both -> ALL)")
c=$(hdr -X POST "${KAM[@]}" -H 'Content-Type: application/json' -d "$B2" "$BASE/api/kam/messages"); expect "POST kam view=both -> ALL" 201 "$c"; echo "      body: $(head -c 200 "$SCRATCH/l_body.txt")"
B3=$(mkbody tuesday Datasec "kam-local-tue-$TS" "SYNTHETIC Kam to Tuesday $TS (view tuesday -> Datasec)")
c=$(hdr -X POST "${KAM[@]}" -H 'Content-Type: application/json' -d "$B3" "$BASE/api/kam/messages"); expect "POST kam view=tuesday -> Datasec" 201 "$c"
B4=$(mkbody wednesday Secuura "kam-local-mis-$TS" "SYNTHETIC mismatch")
c=$(hdr -X POST "${KAM[@]}" -H 'Content-Type: application/json' -d "$B4" "$BASE/api/kam/messages"); expect "POST kam body client disagrees with view (MUST refuse)" 400 "$c"; echo "      body: $(cat "$SCRATCH/l_body.txt")"
c=$(hdr -X POST "${KAM[@]}" -H 'Content-Type: application/json' -d "$(echo "$B1" | sed 's/"view": "wednesday"/"view": "nobody"/')" "$BASE/api/kam/messages"); expect "POST kam view=nobody (MUST refuse)" 400 "$c"
c=$(hdr -X POST "${KAM[@]}" -H 'Content-Type: application/json' -d "$(echo "$B1" | sed 's/^{/{"text": "SYNTHETIC plaintext", /')" "$BASE/api/kam/messages"); expect "POST kam with a plaintext field (MUST refuse)" 400 "$c"; echo "      body: $(cat "$SCRATCH/l_body.txt")"
echo "### R. viewer reads include ALL; seat reads author=kam with the seat's partition set"
c=$(hdr "${KAM[@]}" "$BASE/api/messages?client=ALL&limit=5"); expect "GET /api/messages?client=ALL as Kam" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=d["messages"];print("      ALL rows:",len(m),"clients:",sorted({r["client"] for r in m}),"roles:",sorted({r["role"] for r in m}))' "$SCRATCH/l_body.txt"
tok() { "$V" - "$1" <<'PY'
import sys; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat",sys.argv[1],"--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
}
TW=$(tok wednesday); TT=$(tok tuesday)
c=$(hdr -H "Authorization: Bearer $TW" "$BASE/api/seat/messages?author=kam&limit=50"); expect "wednesday seat GET author=kam" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=d["messages"];print("      partitions:",d["clients"],"rows:",len(m),"roles:",sorted({r["role"] for r in m}),"clients seen:",sorted({r["client"] for r in m})); assert set(d["clients"])=={"ALL","Secuura","WED"}, d["clients"]; assert all(r["role"]=="kam" for r in m); print("PASS  wednesday sees ONLY ALL+Secuura+WED and ONLY role=kam rows")' "$SCRATCH/l_body.txt" || FAIL=1
c=$(hdr -H "Authorization: Bearer $TT" "$BASE/api/seat/messages?author=kam&limit=50"); expect "tuesday seat GET author=kam" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=d["messages"];print("      partitions:",d["clients"],"rows:",len(m),"clients seen:",sorted({r["client"] for r in m})); assert set(d["clients"])=={"ALL","Datasec"}, d["clients"]; assert all(r["client"] in ("ALL","Datasec") for r in m); print("PASS  tuesday sees ONLY ALL+Datasec (never WED/Secuura)")' "$SCRATCH/l_body.txt" || FAIL=1
expect "wednesday seat GET client=Datasec (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TW" "$BASE/api/seat/messages?client=Datasec")"
expect "tuesday seat GET client=WED (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TT" "$BASE/api/seat/messages?client=WED")"
expect "tuesday seat GET client=ALL (broadcast readable by every seat)" 200 "$(hdr -H "Authorization: Bearer $TT" "$BASE/api/seat/messages?client=ALL&limit=2")"
echo "### S. seat duplicate + card update + long option keys + backfill flags"
post() { "$V" "$HERE/seat/post_message.py" --seat "$1" --client "$2" --base "$BASE" --text "$3" --id "$4" ${5:-} 2>"$SCRATCH/l_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["status"]); sys.stderr.write("      body: "+d["body"][:200]+"\n")'; [ -s "$SCRATCH/l_err.txt" ] && sed 's/^/      stderr: /' "$SCRATCH/l_err.txt" >&2; }
expect "seat message first post" 201 "$(post wednesday WED "SYNTHETIC dup test $TS" dup-$TS "--ts 2026-09-20T01:02:03.000Z --backfill --src-ts 2026-09-20T11:02:03.000000+10:00")"
expect "seat message SAME (client,ts,id) again -> 200 duplicate, nothing written" 200 "$(post wednesday WED "SYNTHETIC dup test $TS" dup-$TS "--ts 2026-09-20T01:02:03.000Z --backfill --src-ts 2026-09-20T11:02:03.000000+10:00")"
CARD1=$("$V" "$HERE/seat/post_card.py" --seat wednesday --client WED --base "$BASE" --title "SYNTHETIC card $TS" --bluf "SYNTHETIC bluf" --option measure-then-rule "Measure first (synthetic)" --option ship-now-with-guard "Ship (synthetic)" --recommended measure-then-rule --id card-local-$TS | python3 -c 'import json,sys;print(json.load(sys.stdin)["status"])')
expect "card with 17/19-char option keys, first post" 201 "$CARD1"
CARD2=$("$V" "$HERE/seat/post_card.py" --seat wednesday --client WED --base "$BASE" --title "SYNTHETIC card $TS" --bluf "SYNTHETIC bluf" --option measure-then-rule "Measure first (synthetic)" --option ship-now-with-guard "Ship (synthetic)" --recommended measure-then-rule --status ruled --ruled-choice measure-then-rule --id card-local-$TS | python3 -c 'import json,sys;print(json.load(sys.stdin)["status"])')
expect "same card id again with status=ruled -> 200 updated in place" 200 "$CARD2"
c=$(hdr "${KAM[@]}" "$BASE/api/cards?client=WED&limit=1000"); expect "GET /api/cards as Kam" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=[r for r in d["cards"] if r["id"]==sys.argv[2]];print("      card rows with that id:",len(m),"status:",m[0]["status"] if m else None,"ruled_choice:",m[0].get("ruled_choice") if m else None,"row_key:",m[0]["row_key"] if m else None); assert len(m)==1 and m[0]["status"]=="ruled"; print("PASS  one card row, updated to ruled (RowKey card_<id>)")' "$SCRATCH/l_body.txt" "card-local-$TS" || FAIL=1
echo "### O. offline decrypt of the Kam row written above (raw table read)"
ROW=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'WED' and id eq 'kam-local-$TS'" -o json 2>"$SCRATCH/l_q.txt"); echo "$ROW" > "$SCRATCH/l_row.json"
"$V" - "$SCRATCH/l_row.json" "$CRED/kam-pilot-private.pem" "$TS" <<'PY'
import json,sys; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
items=json.load(open(sys.argv[1]))["items"]; assert len(items)==1, len(items); r=items[0]; ts=sys.argv[3]
exp=f"SYNTHETIC Kam reply {ts} from the local matrix (view wednesday)"
print("      clear fields:", {k:r[k] for k in ("role","seat","view","written_by") if k in r})
print("PASS  Kam's plaintext NOT in raw row" if exp not in json.dumps(r) else "FAIL  PLAINTEXT IN RAW ROW")
pt=envelope.decrypt_text(envelope.load_private(sys.argv[2]), r, {"client":r["PartitionKey"],"kind":r["kind"],"id":r["id"],"ts":r["ts"]})
print("PASS  offline decrypt == expected" if pt==exp else f"FAIL  mismatch {pt!r}")
assert r["role"]=="kam" and r["seat"]=="kam" and r["written_by"].startswith("easyauth:")
PY
[ $? -eq 0 ] || FAIL=1
kill $UV 2>/dev/null; wait $UV 2>/dev/null
echo "== server log tail:"; tail -5 "$SCRATCH/wedcloud_local2.log"
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL LOCAL PROBES PASS || echo SOME LOCAL PROBES FAILED)"; exit $FAIL
