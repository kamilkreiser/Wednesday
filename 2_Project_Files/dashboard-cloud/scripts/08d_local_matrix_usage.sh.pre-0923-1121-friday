#!/usr/bin/env bash
# Usage-gauge local matrix (2026-09-22) — the app on loopback (transient port 47792) against the REAL storage account through the
# CLI credential, with a SIMULATED Easy Auth principal (Kam's object id): the viewer read GET /api/usage, the seat write
# POST /api/seat/usage (token-attributed; body seat spoof -> 403; bounds -> 400; older reading ignored), the seat read-back,
# and the publisher seat/post_usage.py end to end (fresh fixture publishes; stale fixture publishes nothing, rc 3).
# Writes the WEDNESDAY usage row with fixture values; the last step republishes the REAL reading (if fresh) so the board is left true.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
SCRATCH=${SCRATCH:?set SCRATCH to a scratch dir}
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
export TENANT_ID SEAT_API_APPID=$API_APPID STORAGE_ACCOUNT=$STORAGE SEAT_APP_MAP="$wednesday_seat_APPID:wednesday,$tuesday_seat_APPID:tuesday" KAM_OBJECT_ID=$KAM_USER_OBJ
PORT=47792; BASE="http://127.0.0.1:$PORT"; FAIL=0
( "$V" -m uvicorn main:app --app-dir "$HERE/app" --host 127.0.0.1 --port $PORT --log-level warning > "$SCRATCH/wedcloud_local_usage.log" 2>&1 ) &
APP_PID=$!
for i in $(seq 1 60); do curl -s -o /dev/null "$BASE/api/seat/health" && break; sleep 1; done
curl -s -o /dev/null "$BASE/api/seat/health" || { echo "FAIL  loopback app did not come up in 60 s: $(tail -3 "$SCRATCH/wedcloud_local_usage.log" | tr "\n" " ")"; kill $APP_PID 2>/dev/null; exit 1; }
expect() { if [ "$2" = "$3" ]; then echo "PASS  $1: expected $2 got $3"; else echo "FAIL  $1: expected $2 got $3"; FAIL=1; fi; }
hdr() { curl -s -o "$SCRATCH/u_body.txt" -w '%{http_code}' --max-time 30 "$@"; }
KAM=(-H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'x-ms-client-principal-name: kreiser.org@me.com')
TOK=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "### U-L1 health carries usage_route"
c=$(hdr "$BASE/api/seat/health"); expect "health" 200 "$c"; python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("usage_route") is True and d["phase"]=="3",d;print("PASS  health: phase 3 + usage_route true")' "$SCRATCH/u_body.txt" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
echo "### U-L2 gates"
expect "POST /api/seat/usage NO token" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d '{"pct":1,"ts":"'$NOW'"}' "$BASE/api/seat/usage")"
expect "GET /api/usage without a principal header (app-level refusal; live: Easy Auth)" 401 "$(hdr "$BASE/api/usage")"
expect "POST body seat=tuesday with the WEDNESDAY token (SPOOF, must refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"seat":"tuesday","pct":7,"resets_in":"1d 1h","ts":"'$NOW'"}' "$BASE/api/seat/usage")"; echo "      body: $(head -c 140 "$SCRATCH/u_body.txt")"
expect "POST pct=101 -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"pct":101,"ts":"'$NOW'"}' "$BASE/api/seat/usage")"
expect "POST bad ts -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"pct":10,"ts":"yesterday"}' "$BASE/api/seat/usage")"
expect "POST resets_in with control chars -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"pct":10,"resets_in":"<b>x</b>","ts":"'$NOW'"}' "$BASE/api/seat/usage")"
echo "### U-L3 publisher end to end (fixture 42%)"
printf '{"agent":"wednesday","pct":42,"resets_in":"3d 4h","ts":"%s"}\n' "$NOW" > "$SCRATCH/usage_fixture_fresh.json"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" --file "$SCRATCH/usage_fixture_fresh.json" > "$SCRATCH/u_pub.txt" 2>&1; echo "      $(tail -2 "$SCRATCH/u_pub.txt" | head -1 | cut -c1-160)"
expect "post_usage.py fresh fixture rc" "rc=0" "$(tail -1 "$SCRATCH/u_pub.txt")"
c=$(hdr "${KAM[@]}" "$BASE/api/usage"); expect "GET /api/usage as Kam" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));w=d["wednesday"];print("      wednesday row:",{k:w.get(k) for k in ("seat","pct","resets_in","reading_ts","age_seconds")},"written_by:",w.get("written_by","")[:8]+"…","tuesday:",None if d["tuesday"] is None else d["tuesday"].get("pct"))
assert w["pct"]==42 and w["seat"]=="wednesday" and w["written_by"]==sys.argv[2] and w["reading_ts"]==sys.argv[3] and 0<=w["age_seconds"]<120,w;print("PASS  viewer read-back: wednesday 42%, seat attributed from the TOKEN (written_by = wednesday app id), reading_ts == fixture, age fresh")' "$SCRATCH/u_body.txt" "$wednesday_seat_APPID" "$NOW" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/usage"); expect "GET /api/seat/usage (seat read-back)" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d["wednesday"]["pct"]==42;print("PASS  seat read-back: wednesday 42%")' "$SCRATCH/u_body.txt" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
echo "### U-L4 last write wins; stale/missing/other-seat files publish nothing"
OLD=$(date -u -v-2H +%Y-%m-%dT%H:%M:%SZ)
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"pct":99,"resets_in":"1d","ts":"'$OLD'"}' "$BASE/api/seat/usage"); expect "POST a 2h-old reading (99%) -> 200 replaced (last write wins)" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("updated") is True and d["stored"]["pct"]==99,d;print("PASS  stored echo 99%, updated")' "$SCRATCH/u_body.txt" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
printf '{"agent":"wednesday","pct":99,"resets_in":"1d","ts":"%s"}\n' "$OLD" > "$SCRATCH/usage_fixture_stale.json"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" --file "$SCRATCH/usage_fixture_stale.json" > "$SCRATCH/u_pub2.txt" 2>&1; echo "      $(tail -2 "$SCRATCH/u_pub2.txt" | head -1 | cut -c1-160)"
expect "post_usage.py STALE fixture (2h) publishes nothing" "rc=3" "$(tail -1 "$SCRATCH/u_pub2.txt")"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" --file "$SCRATCH/usage_fixture_does_not_exist_$$.json" > "$SCRATCH/u_pub3.txt" 2>&1; expect "post_usage.py MISSING file rc" "rc=3" "$(tail -1 "$SCRATCH/u_pub3.txt")"
printf '{"agent":"tuesday","pct":5,"resets_in":"1d","ts":"%s"}\n' "$NOW" > "$SCRATCH/usage_fixture_tuesday_named.json"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" --file "$SCRATCH/usage_fixture_tuesday_named.json" > "$SCRATCH/u_pub4.txt" 2>&1; expect "post_usage.py file naming the OTHER seat refused locally" "rc=2" "$(tail -1 "$SCRATCH/u_pub4.txt")"
c=$(hdr "${KAM[@]}" "$BASE/api/usage"); python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));w=d["wednesday"];assert w["pct"]==99 and w["age_seconds"]>=7100,w;print("PASS  after the refused/stale/missing attempts (nothing published) the row is the 2h-old 99% (page: no reading)")' "$SCRATCH/u_body.txt" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
echo "### U-L5 leave the board TRUE: republish the real reading (rc 0 if fresh, 3 if this seat is idle)"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" > "$SCRATCH/u_pub5.txt" 2>&1; echo "      $(tail -2 "$SCRATCH/u_pub5.txt" | head -1 | cut -c1-160)"; echo "      $(tail -1 "$SCRATCH/u_pub5.txt")"
unset TOK
kill $APP_PID 2>/dev/null; wait $APP_PID 2>/dev/null
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL PASS || echo SOME FAILED)"
exit $FAIL
