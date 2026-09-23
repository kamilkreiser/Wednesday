#!/usr/bin/env bash
# Step 3 local check — run the app on loopback (transient, port 47789 from Wednesday's block, NOT a registered service)
# against the REAL storage account via the CLI credential, and run the seat matrix. Local proof only; Step 5 repeats it live.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
export TENANT_ID SEAT_API_APPID=$API_APPID STORAGE_ACCOUNT=$STORAGE SEAT_APP_MAP="$wednesday_seat_APPID:wednesday,$tuesday_seat_APPID:tuesday"
PORT=47789
( "$V" -m uvicorn main:app --app-dir "$HERE/app" --host 127.0.0.1 --port $PORT --log-level warning > /tmp/wedcloud_local.log 2>&1 ) &
UV=$!
for i in $(seq 1 30); do curl -s -o /dev/null "http://127.0.0.1:$PORT/api/seat/health" && break; sleep 0.5; done
BASE="http://127.0.0.1:$PORT"
code() { curl -s -o /tmp/body.txt -w '%{http_code}' "$@"; echo -n "  body=$(head -c 160 /tmp/body.txt | tr '\n' ' ')"; echo; }
echo "health:            $(code $BASE/api/seat/health)"
echo "viewer / no hdr:   $(code $BASE/)"
echo "viewer /api/messages no hdr: $(code $BASE/api/messages)"
echo "viewer /api/messages WITH Easy-Auth header (simulated locally): $(code -H 'x-ms-client-principal-id: test' "$BASE/api/messages?limit=5")"
echo "POST no token:     $(code -X POST -H 'Content-Type: application/json' -d '{"client":"Secuura"}' $BASE/api/seat/messages)"
echo "POST garbage token:$(code -X POST -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiJ9.e30.abc' -H 'Content-Type: application/json' -d '{"client":"Secuura"}' $BASE/api/seat/messages)"
echo "wednesday -> Secuura (expect 201):"; "$V" "$HERE/seat/post_message.py" --seat wednesday --client Secuura --base $BASE --text "SYNTHETIC local alpha — wednesday to Secuura" --id local-alpha
echo "wednesday -> Datasec (expect 403):"; "$V" "$HERE/seat/post_message.py" --seat wednesday --client Datasec --base $BASE --text "SYNTHETIC local beta — must be refused" --id local-beta
echo "tuesday -> Secuura (expect 403):";  "$V" "$HERE/seat/post_message.py" --seat tuesday --client Secuura --base $BASE --text "SYNTHETIC local gamma — must be refused" --id local-gamma
echo "tuesday -> Datasec (expect 201):";  "$V" "$HERE/seat/post_message.py" --seat tuesday --client Datasec --base $BASE --text "SYNTHETIC local delta — tuesday to Datasec" --id local-delta
echo "plaintext field refused (expect 400):"; curl -s -o /tmp/body.txt -w '%{http_code}\n' -X POST -H "Authorization: Bearer $("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)" -H 'Content-Type: application/json' -d '{"client":"WED","text":"SYNTHETIC plaintext must be refused","envelope":{"scheme":"x","kid":"x","iv":"x","wrapped_key":"x","ciphertext":"x"}}' $BASE/api/seat/messages; head -c 200 /tmp/body.txt; echo
echo "card (expect 201):"; "$V" "$HERE/seat/post_card.py" --seat wednesday --client WED --base $BASE --title "SYNTHETIC card: pick a colour" --bluf "SYNTHETIC bluf text" --option A "Blue" --option B "Green" --recommended A --id local-card1
kill $UV 2>/dev/null; wait $UV 2>/dev/null
echo "== server log tail:"; tail -20 /tmp/wedcloud_local.log
