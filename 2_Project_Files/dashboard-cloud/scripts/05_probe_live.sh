#!/usr/bin/env bash
# Step 5 — PROVE IT LIVE against https://$WEBAPP.azurewebsites.net. Every line is a probe with expected vs actual; exit 1 if any mismatch.
# Synthetic text only. Then read the raw Table rows (RBAC, --auth-mode login) and decrypt offline with the pilot private key
# (positive control) and a WRONG key (negative control).
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
SCRATCH=${SCRATCH:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a45299b-5e60-46f6-b7e7-e32507803323/scratchpad}
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
BASE="https://$WEBAPP.azurewebsites.net"
FAIL=0
expect() { # $1 label $2 expected $3 actual
  if [ "$2" = "$3" ]; then echo "PASS  $1: expected $2 got $3"; else echo "FAIL  $1: expected $2 got $3"; FAIL=1; fi; }
hdr() { curl -s -o "$SCRATCH/p_body.txt" -D "$SCRATCH/p_hdr.txt" -w '%{http_code}' --max-time 40 "$@"; }
loc() { /usr/bin/grep -i '^location:' "$SCRATCH/p_hdr.txt" | head -1 | tr -d '\r' | cut -c1-90; }
echo "### A. Easy Auth gate (viewer surface)"
# Easy Auth refuses two ways: API-style clients (no Accept: text/html) get 401 + WWW-Authenticate: Bearer (empty body);
# browsers get 302 to login.microsoftonline.com. BOTH are Easy Auth's — the app's own 401 carries a JSON {"detail":...} body.
BROWSER=(-H 'Accept: text/html,application/xhtml+xml' -H 'User-Agent: Mozilla/5.0 (iPhone) Safari')
ea_refused() { # $1 label, rest curl args: assert Easy Auth (not the app) refused
  local label=$1; shift; local c; c=$(hdr "$@"); local wa; wa=$(/usr/bin/grep -i -c '^www-authenticate: Bearer' "$SCRATCH/p_hdr.txt")
  local appbody; appbody=$(/usr/bin/grep -i -c '"detail"' "$SCRATCH/p_body.txt")
  if [ "$c" = "401" ] && [ "$wa" = "1" ] && [ "$appbody" = "0" ]; then echo "PASS  $label: 401 from Easy Auth (WWW-Authenticate Bearer, empty body — NOT the app's JSON 401)"; else echo "FAIL  $label: code=$c www-auth=$wa app-json-body=$appbody"; FAIL=1; fi; }
ea_redirect() { local label=$1; shift; local c; c=$(hdr "${BROWSER[@]}" "$@"); local l; l=$(loc)
  if [ "$c" = "302" ] && /usr/bin/grep -i '^location:' "$SCRATCH/p_hdr.txt" | /usr/bin/grep -q -i 'login.microsoftonline.com/d500ebad-cf53-4f2a-a501-f831289e67fc/oauth2/v2.0/authorize'; then echo "PASS  $label (browser Accept): 302 -> login.microsoftonline.com/<tenant>/oauth2/v2.0/authorize"; else echo "FAIL  $label (browser): code=$c loc=$l"; FAIL=1; fi; }
ea_refused  "GET / plain client" "$BASE/"
ea_redirect "GET /" "$BASE/"
echo "      $(loc)" | cut -c1-200
/usr/bin/grep -o 'client_id=[a-f0-9-]*' "$SCRATCH/p_hdr.txt" | head -1 | sed 's/^/      redirect carries /'; /usr/bin/grep -o 'redirect_uri=[^&]*' "$SCRATCH/p_hdr.txt" | head -1 | sed 's/^/      /'
ea_refused  "GET /api/messages plain" "$BASE/api/messages";      ea_redirect "GET /api/messages" "$BASE/api/messages"
ea_refused  "GET /<nonexistent> plain" "$BASE/does-not-exist-$(date +%s)"; ea_redirect "GET /<nonexistent>" "$BASE/does-not-exist-$(date +%s)"
ea_refused  "GET /api/pubkey plain" "$BASE/api/pubkey"
ea_refused  "GET /api/messages with FORGED x-ms-client-principal-* headers from outside" -H 'x-ms-client-principal-id: forged' -H 'x-ms-client-principal-name: forged' "$BASE/api/messages"
echo "### B. Seat API gate"
c=$(hdr "$BASE/api/seat/health"); expect "GET /api/seat/health (excluded path, anonymous)" 200 "$c"
c=$(hdr -X POST -H 'Content-Type: application/json' -d '{"client":"Secuura"}' "$BASE/api/seat/messages"); expect "POST /api/seat/messages NO token" 401 "$c"; echo "      body: $(head -c 120 "$SCRATCH/p_body.txt")"
c=$(hdr -X POST -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Im5vcGUifQ.eyJhdWQiOiJ4In0.c2ln' -H 'Content-Type: application/json' -d '{"client":"Secuura"}' "$BASE/api/seat/messages"); expect "POST forged token" 401 "$c"; echo "      body: $(head -c 120 "$SCRATCH/p_body.txt")"
c=$(hdr "$BASE/api/seat/messages"); expect "GET /api/seat/messages NO token" 401 "$c"
post() { # seat client text id -> prints status
  "$V" "$HERE/seat/post_message.py" --seat "$1" --client "$2" --base "$BASE" --text "$3" --id "$4" --synthetic 2>"$SCRATCH/p_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["status"]); sys.stderr.write("      body: "+d["body"][:160]+"\n")'; [ -s "$SCRATCH/p_err.txt" ] && sed 's/^/      stderr: /' "$SCRATCH/p_err.txt" >&2; }
TS=$(date -u +%H%M%S)
echo "### C. The partition (R0) — token roles decide, body is refused"
expect "wednesday-seat -> client=Secuura" 201 "$(post wednesday Secuura "SYNTHETIC live alpha $TS — wednesday writes Secuura" live-alpha-$TS)"
expect "wednesday-seat -> client=WED" 201 "$(post wednesday WED "SYNTHETIC live wed $TS — wednesday writes WED" live-wed-$TS)"
expect "wednesday-seat -> client=Datasec (MUST refuse)" 403 "$(post wednesday Datasec "SYNTHETIC live beta $TS — must be refused" live-beta-$TS)"
expect "tuesday-seat -> client=Secuura (MUST refuse)" 403 "$(post tuesday Secuura "SYNTHETIC live gamma $TS — must be refused" live-gamma-$TS)"
expect "tuesday-seat -> client=WED (not granted to tuesday; MUST refuse)" 403 "$(post tuesday WED "SYNTHETIC live wed2 $TS — must be refused" live-wed2-$TS)"
expect "tuesday-seat -> client=Datasec" 201 "$(post tuesday Datasec "SYNTHETIC live delta $TS — tuesday writes Datasec" live-delta-$TS)"
echo "### D. Card + plaintext refusal"
CARD=$("$V" "$HERE/seat/post_card.py" --seat wednesday --client Secuura --base "$BASE" --title "SYNTHETIC card $TS: choose a synthetic option" --bluf "SYNTHETIC bluf — nothing real here" --option A "Option alpha (synthetic)" --option B "Option beta (synthetic)" --recommended A --id live-card-$TS --synthetic | python3 -c 'import json,sys;print(json.load(sys.stdin)["status"])')
expect "wednesday-seat card -> Secuura" 201 "$CARD"
TOK=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","text":"SYNTHETIC plaintext must be refused","envelope":{"scheme":"x","kid":"x","iv":"x","wrapped_key":"x","ciphertext":"x"}}' "$BASE/api/seat/messages"); expect "POST with a plaintext 'text' field" 400 "$c"; echo "      body: $(head -c 120 "$SCRATCH/p_body.txt")"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=Datasec"); expect "GET /api/seat/messages?client=Datasec with wednesday token" 403 "$c"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?limit=3"); expect "GET /api/seat/messages (own partitions) with wednesday token" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print("      clients in response:",d["clients"],"rows:",len(d["messages"]),"fields:",sorted(d["messages"][0].keys()) if d["messages"] else None)' "$SCRATCH/p_body.txt"
ea_refused "GET viewer /api/messages with a SEAT bearer token (a seat is not Kam; Easy Auth allowedApplications=[web app] refuses it)" -H "Authorization: Bearer $TOK" "$BASE/api/messages?limit=1"
unset TOK
echo "### E. Raw row = ciphertext; offline decrypt positive + negative controls"
ROW=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'Secuura' and id eq 'live-alpha-$TS'" -o json 2>"$SCRATCH/q_err.txt")
[ -s "$SCRATCH/q_err.txt" ] && sed 's/^/      az stderr: /' "$SCRATCH/q_err.txt"
echo "$ROW" > "$SCRATCH/raw_row.json"
"$V" - "$SCRATCH/raw_row.json" "$CRED/kam-pilot-private.pem" "$TS" <<'PY'
import json,sys,os
sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
items=json.load(open(sys.argv[1]))["items"]; assert len(items)==1, f"expected 1 row, got {len(items)}"
r=items[0]; ts=sys.argv[3]
expected=f"SYNTHETIC live alpha {ts} — wednesday writes Secuura"
raw=json.dumps(r)
print("      raw row fields:", sorted(k for k in r if not k.startswith("odata") and not k.endswith("@odata.type")))
print("      ciphertext (first 48 b64 chars):", r["ciphertext"][:48], "...")
print("PASS  plaintext substring NOT in raw row" if expected not in raw and "wednesday writes" not in raw else "FAIL  PLAINTEXT FOUND IN RAW ROW")
clear={"client":r["PartitionKey"],"kind":r["kind"],"id":r["id"],"ts":r["ts"]}
pt=envelope.decrypt_text(envelope.load_private(sys.argv[2]),r,clear)
print("PASS  offline decrypt with the pilot private key ==", repr(pt) if pt==expected else f"FAIL mismatch {pt!r}")
from cryptography.hazmat.primitives.asymmetric import rsa
try:
    envelope.decrypt_text(rsa.generate_private_key(public_exponent=65537,key_size=4096),r,clear); print("FAIL  WRONG KEY DECRYPTED")
except Exception as e: print("PASS  wrong key refused:", type(e).__name__)
try:
    envelope.decrypt_text(envelope.load_private(sys.argv[2]),r,dict(clear,client="Datasec")); print("FAIL  RELABELLED ROW DECRYPTED")
except Exception as e: print("PASS  row relabelled to another client refused (AAD):", type(e).__name__)
PY
echo "### G. Phase 2 (2026-09-21) — pages, Kam's write path, seat author=kam partitions, idempotency"
ea_refused  "GET /chat plain client" "$BASE/chat";                       ea_redirect "GET /chat" "$BASE/chat"
ea_refused  "GET /static/common.js plain client" "$BASE/static/common.js"
KB='{"client":"WED","view":"wednesday","id":"probe-kam-'$TS'","ts":"2026-09-21T00:00:00.000Z","envelope":{"scheme":"x","kid":"x","iv":"x","wrapped_key":"x","ciphertext":"x"}}'
ea_refused  "POST /api/kam/messages NO principal (Easy Auth refuses before the app)" -X POST -H 'Content-Type: application/json' -d "$KB" "$BASE/api/kam/messages"
ea_refused  "POST /api/kam/messages with FORGED x-ms-client-principal-id = Kam's real object id, from outside" -X POST -H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'x-ms-client-principal-name: kreiser.org@me.com' -H 'Content-Type: application/json' -d "$KB" "$BASE/api/kam/messages"
ea_redirect "POST /api/kam/messages (browser Accept, no session)" -X POST -H 'Content-Type: application/json' -d "$KB" "$BASE/api/kam/messages"
TOK=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)
TOKT=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","tuesday","--client","Datasec"]); print(sc.get_token(a, sc.load_ids()))
PY
)
ea_refused  "POST /api/kam/messages with a SEAT bearer token (a seat is not Kam)" -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d "$KB" "$BASE/api/kam/messages"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?author=kam&limit=200"); expect "wednesday seat GET author=kam" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=d["messages"];bad=[r for r in m if r.get("role")!="kam" or r["client"] not in ("ALL","Secuura","WED")];print("      partitions:",d["clients"],"rows:",len(m),"clients seen:",sorted({r["client"] for r in m}),"non-kam or foreign rows:",len(bad)); assert set(d["clients"])=={"ALL","Secuura","WED"} and not bad; print("PASS  wednesday author=kam: only ALL+Secuura+WED, only role=kam")' "$SCRATCH/p_body.txt" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/messages?author=kam&limit=200"); expect "tuesday seat GET author=kam" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=d["messages"];bad=[r for r in m if r.get("role")!="kam" or r["client"] not in ("ALL","Datasec")];print("      partitions:",d["clients"],"rows:",len(m),"clients seen:",sorted({r["client"] for r in m}),"non-kam or foreign rows:",len(bad)); assert set(d["clients"])=={"ALL","Datasec"} and not bad; print("PASS  tuesday author=kam: only ALL+Datasec, only role=kam")' "$SCRATCH/p_body.txt" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
expect "tuesday seat GET client=WED (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/messages?client=WED")"
expect "tuesday seat GET client=ALL (broadcast, every seat)" 200 "$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/messages?client=ALL&limit=1")"
expect "wednesday seat GET client=ALL" 200 "$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=ALL&limit=1")"
unset TOK TOKT
# The message dedupe key is (client, ts, id) — the tools and the backfill always pass a FIXED ts (the local entry's), so a
# repeat is byte-identical in the key. The probe therefore fixes --ts too (first run of this probe omitted it and correctly got 201).
postts() { "$V" "$HERE/seat/post_message.py" --seat "$1" --client "$2" --base "$BASE" --text "$3" --id "$4" --ts "$5" --backfill --src-ts "$6" --synthetic 2>"$SCRATCH/p_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["status"]); sys.stderr.write("      body: "+d["body"][:200]+"\n")'; }
expect "seat message probe-dup-$TS first post (fixed ts, backfill flags)" 201 "$(postts wednesday WED "SYNTHETIC dup probe $TS" probe-dup-$TS 2026-09-21T00:00:01.000Z 2026-09-21T10:00:01.000000+10:00)"
expect "seat message probe-dup-$TS SAME (client,ts,id) again -> 200 duplicate, nothing written" 200 "$(postts wednesday WED "SYNTHETIC dup probe $TS" probe-dup-$TS 2026-09-21T00:00:01.000Z 2026-09-21T10:00:01.000000+10:00)"
CARDU=$("$V" "$HERE/seat/post_card.py" --seat wednesday --client Secuura --base "$BASE" --title "SYNTHETIC card $TS: choose a synthetic option" --bluf "SYNTHETIC bluf — nothing real here" --option A "Option alpha (synthetic)" --option B "Option beta (synthetic)" --recommended A --status ruled --ruled-choice A --id live-card-$TS --synthetic | python3 -c 'import json,sys;print(json.load(sys.stdin)["status"])')
expect "card live-card-$TS re-posted as ruled -> 200 updated in place" 200 "$CARDU"
echo "### H. Phase 3 (2026-09-21) — per-seat wrapped keys, device keys, migrated rows, live readers"
c=$(hdr "$BASE/api/seat/health"); expect "H1 health phase 3" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d["phase"]=="3" and d["kam_keys"]==3 and d["seat_keys"]==["tuesday","wednesday"],d;print("PASS  H1 health: phase 3, kam_keys 3, seat_keys [tuesday, wednesday]")' "$SCRATCH/p_body.txt" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
ea_refused "H2 GET /api/pubkeys plain client (viewer route, Easy Auth gated)" "$BASE/api/pubkeys"
# H3: a NEW seat row carries the full recipient set; each Kam key + the addressed seat opens it; the other seat cannot
expect "H3 wednesday-seat -> WED (Phase 3 writer)" 201 "$(post wednesday WED "SYNTHETIC phase3 wed $TS — ring + wednesday seat" p3-wed-$TS)"
ROW=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'WED' and id eq 'p3-wed-$TS'" -o json 2>"$SCRATCH/q_err.txt"); echo "$ROW" > "$SCRATCH/raw_p3_wed.json"
"$V" - "$SCRATCH/raw_p3_wed.json" "SYNTHETIC phase3 wed $TS — ring + wednesday seat" WED <<'PY' || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
import json,sys; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
CRED="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"; items=json.load(open(sys.argv[1]))["items"]; assert len(items)==1, len(items)
r=items[0]; expected=sys.argv[2]; part=sys.argv[3]; clear={"client":r["PartitionKey"],"kind":r["kind"],"id":r["id"],"ts":r["ts"]}
kids=envelope.kids_of(r); exp=[envelope.kid_of(k) for _,k in envelope.recipients_for(part)]
print("      raw row kids:", kids); assert expected not in json.dumps(r), "PLAINTEXT IN RAW ROW"
print("PASS  H3 raw row wrapped_keys kids == recipients_for(%s) (pilot, ipad, laptop, wednesday-seat)" % part if kids==exp else "FAIL  H3 kids %s != %s" % (kids, exp)); assert kids==exp
for k in ("kam-pilot-private.pem","kam-laptop-private.pem","kam-ipad-private.pem","wednesday-seat.pem"):
    pt=envelope.decrypt_text(envelope.load_private(f"{CRED}/{k}"), r, clear); print(("PASS  H3 %s decrypts the new WED row == expected" % k) if pt==expected else ("FAIL  H3 %s mismatch" % k)); assert pt==expected
try: envelope.decrypt_text(envelope.load_private(f"{CRED}/tuesday-seat.pem"), r, clear); print("FAIL  H3 TUESDAY SEAT KEY DECRYPTED A WED ROW"); sys.exit(1)
except KeyError as e: print("PASS  H3 tuesday-seat.pem REFUSED on the WED row (KeyError: not a recipient)")
PY
# H4: a tuesday row (Datasec, synthetic) is wrapped to the tuesday seat and NOT to wednesday — verified on the DATA KEY only (no text decrypt of a Datasec row)
expect "H4 tuesday-seat -> Datasec (Phase 3 writer)" 201 "$(post tuesday Datasec "SYNTHETIC phase3 delta $TS — ring + tuesday seat" p3-delta-$TS)"
ROW=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'Datasec' and id eq 'p3-delta-$TS'" -o json 2>"$SCRATCH/q_err.txt"); echo "$ROW" > "$SCRATCH/raw_p3_delta.json"
"$V" - "$SCRATCH/raw_p3_delta.json" <<'PY' || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
import json,sys; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
CRED="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"; items=json.load(open(sys.argv[1]))["items"]; assert len(items)==1, len(items); r=items[0]
kids=envelope.kids_of(r); exp=[envelope.kid_of(k) for _,k in envelope.recipients_for("Datasec")]
print("PASS  H4 Datasec row kids == recipients_for(Datasec) (pilot, ipad, laptop, tuesday-seat)" if kids==exp else "FAIL  H4 kids %s" % kids); assert kids==exp
ref=envelope.unwrap_data_key(envelope.load_private(f"{CRED}/kam-pilot-private.pem"), r)
for k in ("kam-laptop-private.pem","kam-ipad-private.pem","tuesday-seat.pem"):
    ok=envelope.unwrap_data_key(envelope.load_private(f"{CRED}/{k}"), r)==ref; print(("PASS  H4 %s unwraps the Datasec row's DATA KEY (bytes only, text untouched)" % k) if ok else "FAIL  H4 %s" % k); assert ok
try: envelope.unwrap_data_key(envelope.load_private(f"{CRED}/wednesday-seat.pem"), r); print("FAIL  H4 WEDNESDAY SEAT UNWRAPPED A DATASEC ROW"); sys.exit(1)
except KeyError: print("PASS  H4 wednesday-seat.pem REFUSED on the Datasec row (KeyError: not a recipient)")
PY
# H5: a MIGRATED (backfill) WED row opens with every device key and the pilot (texts compared, never printed)
ROW=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'WED' and backfill eq true and role eq 'wednesday'" --num-results 1 -o json 2>"$SCRATCH/q_err.txt"); echo "$ROW" > "$SCRATCH/raw_p3_migrated.json"
"$V" - "$SCRATCH/raw_p3_migrated.json" <<'PY' || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
import json,sys; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
CRED="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"; items=json.load(open(sys.argv[1]))["items"]; assert items, "no migrated row"; r=items[0]
clear={"client":r["PartitionKey"],"kind":r["kind"],"id":r["id"],"ts":r["ts"]}; print("      migrated row:", r["RowKey"], "kids:", envelope.kids_of(r))
ref=envelope.decrypt_text(envelope.load_private(f"{CRED}/kam-pilot-private.pem"), r, clear)
for k in ("kam-laptop-private.pem","kam-ipad-private.pem","wednesday-seat.pem"):
    ok=envelope.decrypt_text(envelope.load_private(f"{CRED}/{k}"), r, clear)==ref; print(("PASS  H5 %s decrypts the MIGRATED row == the pilot's decrypt (%d chars, not printed)" % (k, len(ref))) if ok else "FAIL  H5 %s" % k); assert ok
print("PASS  H5 pilot key still decrypts the migrated row")
PY
# H6: the LIVE READERS (2026-09-21 18:0x: synthetic probe rows are excluded — the 15:0x reader change skips their decryption by default, so counting them made H6 a false alarm) — each seat, through the API with its own token and --decrypt (tuesday's rows are piped, never written to disk)
"$V" "$HERE/seat/get_kam_messages.py" --seat wednesday --decrypt --json --since 2026-09-21T02:00 --limit 400 > "$SCRATCH/kam_wed.json" 2>"$SCRATCH/p_err.txt"; expect "H6 wednesday seat get_kam_messages --decrypt --json rc" 0 "$?"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=d["messages"];live=[r for r in m if str(r.get("written_by","")).startswith("easyauth:") and not r.get("synthetic")];dec=[r for r in live if "text" in r];err=[r for r in live if "decrypt_error" in r];bad=[r for r in m if r["client"] not in ("ALL","Secuura","WED")]
print("      partitions:",d["clients"],"kam rows:",len(m),"live (easyauth) rows:",len(live),"decrypted:",len(dec),"errors:",len(err),"foreign:",len(bad))
assert not bad and len(live)>=4 and len(dec)==len(live), "wednesday seat could not decrypt every live Kam row it may read (or fewer than the 4 known)"; print("PASS  H6 wednesday seat decrypts EVERY live Kam row in its partitions (WED+ALL, %d rows since 02:00Z, >=4 known); 0 foreign rows" % len(live))' "$SCRATCH/kam_wed.json" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
"$V" "$HERE/seat/get_kam_messages.py" --seat tuesday --decrypt --json --since 2026-09-21T02:00 --limit 400 2>"$SCRATCH/p_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);m=d["messages"];live=[r for r in m if str(r.get("written_by","")).startswith("easyauth:") and not r.get("synthetic")];dec=[r for r in live if "text" in r];bad=[r for r in m if r["client"] not in ("ALL","Datasec")]
print("      partitions:",d["clients"],"kam rows:",len(m),"live rows:",len(live),"decrypted:",len(dec),"foreign:",len(bad),"(Datasec text NOT printed, NOT written to disk)")
assert set(d["clients"])=={"ALL","Datasec"} and not bad and len(dec)==len(live); print("PASS  H6 tuesday seat sees only ALL+Datasec and decrypts its live Kam rows; no WED row reaches it (R0)")' || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }
# H7: synthetic rows — born marked by this run's own posts (clear flag synthetic=true), PRESENT in the seat API, counted per partition;
#     the pages hide them (proven by scripts/09b_page_checks_phase3.mjs on the pages' own ingestion code — run here too)
TOK=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)
# H7 floor is FIXED at the probe-dup row's fixed ts day (2026-09-21T00:00:01Z): a `today` floor lost that row once the UTC date rolled past 2026-09-21 (found 2026-09-22 15:0x, first run after 10:00 AEST)
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=2026-09-21T00:00&limit=1000"); expect "H7 wednesday seat GET WED rows since 2026-09-21T00:00Z" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=d["messages"];ts=sys.argv[2];syn=[r for r in m if r.get("synthetic") is True];mine=[r for r in syn if r["id"] in ("live-wed-"+ts,"p3-wed-"+ts,"probe-dup-"+ts)]
print("      WED rows today:",len(m),"synthetic=true among them:",len(syn),"this run'"'"'s own probe rows found marked:",[r["id"] for r in mine])
assert len(mine)==3, "the rows this run posted with --synthetic are not all marked"; print("PASS  H7 this run'"'"'s 3 synthetic WED rows are PRESENT in the seat API and carry synthetic=true (the pages hide them; nothing deleted)")' "$SCRATCH/p_body.txt" "$TS" || { echo "FAIL  H7 (python arm, see traceback above)"; FAIL=1; }
unset TOK
node "$HERE/scripts/09b_page_checks_phase3.mjs" > "$SCRATCH/p_09b.txt" 2>&1; expect "H7 page checks (DOM order Updates-below-Needs-you; synthetic filter in the pages' own ingestion code)" 0 "$?"
/usr/bin/grep -i -c '^pass' "$SCRATCH/p_09b.txt" | sed 's/^/      09b PASS lines: /'
echo "### I. Usage gauges (2026-09-22) — seat-published, token-attributed, spoof refused, stale renders 'no reading'"
c=$(hdr "$BASE/api/seat/health"); expect "I1 health" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("usage_route") is True and d["phase"]=="3",d;print("PASS  I1 health: phase 3 + usage_route true")' "$SCRATCH/p_body.txt" || { echo "FAIL  (section I python arm, see traceback above)"; FAIL=1; }
ea_refused "I2 GET /api/usage plain client (viewer route, Easy Auth gated)" "$BASE/api/usage"
NOWU=$(date -u +%Y-%m-%dT%H:%M:%SZ)
expect "I3 POST /api/seat/usage NO token" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d '{"pct":1,"ts":"'$NOWU'"}' "$BASE/api/seat/usage")"
expect "I3 POST /api/seat/usage forged token" 401 "$(hdr -X POST -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Im5vcGUifQ.eyJhdWQiOiJ4In0.c2ln' -H 'Content-Type: application/json' -d '{"pct":1,"ts":"'$NOWU'"}' "$BASE/api/seat/usage")"
TOK=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)
TOKT=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","tuesday","--client","Datasec"]); print(sc.get_token(a, sc.load_ids()))
PY
)
expect "I4 SPOOF: body seat=tuesday with the WEDNESDAY token (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"seat":"tuesday","pct":7,"resets_in":"1d 1h","ts":"'$NOWU'"}' "$BASE/api/seat/usage")"; echo "      body: $(head -c 120 "$SCRATCH/p_body.txt")"
expect "I4 SPOOF: body seat=wednesday with the TUESDAY token (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKT" -H 'Content-Type: application/json' -d '{"seat":"wednesday","pct":7,"resets_in":"1d 1h","ts":"'$NOWU'"}' "$BASE/api/seat/usage")"
expect "I4 pct=101 -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"pct":101,"ts":"'$NOWU'"}' "$BASE/api/seat/usage")"
expect "I4 ts not ISO -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"pct":10,"ts":"yesterday"}' "$BASE/api/seat/usage")"
# I5: the publisher itself, on a fresh fixture, as THIS seat -> read back through the seat API AND the raw table row, attributed to the wednesday app id
printf '{"agent":"wednesday","pct":42,"resets_in":"3d 4h","ts":"%s"}\n' "$NOWU" > "$SCRATCH/usage_fixture_fresh.json"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" --file "$SCRATCH/usage_fixture_fresh.json" > "$SCRATCH/p_usage_pub.txt" 2>&1; echo "      $(tail -2 "$SCRATCH/p_usage_pub.txt" | head -1 | cut -c1-160)"
expect "I5 seat/post_usage.py --seat wednesday (fresh fixture 42%) rc" "rc=0" "$(tail -1 "$SCRATCH/p_usage_pub.txt")"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/usage"); expect "I5 GET /api/seat/usage (seat read-back)" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));w=d["wednesday"];print("      wednesday row:",{k:w.get(k) for k in ("seat","pct","resets_in","reading_ts","age_seconds")},"written_by:",w.get("written_by","")[:8]+"…","tuesday:",None if d["tuesday"] is None else {k:d["tuesday"].get(k) for k in ("pct","age_seconds")})
assert w["pct"]==42 and w["seat"]=="wednesday" and w["written_by"]==sys.argv[2] and w["reading_ts"]==sys.argv[3] and 0<=w["age_seconds"]<300,w;print("PASS  I5 read-back: wednesday 42%, attributed to the WEDNESDAY app id by the token, reading_ts == fixture, age fresh")' "$SCRATCH/p_body.txt" "$wednesday_seat_APPID" "$NOWU" || { echo "FAIL  (section I python arm, see traceback above)"; FAIL=1; }
ROWU=$(az storage entity query --account-name "$STORAGE" --table-name usage --auth-mode login --filter "PartitionKey eq 'USAGE' and RowKey eq 'wednesday'" -o json 2>"$SCRATCH/q_err.txt"); [ -s "$SCRATCH/q_err.txt" ] && sed 's/^/      az stderr: /' "$SCRATCH/q_err.txt"
echo "$ROWU" | python3 -c 'import json,sys;it=json.load(sys.stdin)["items"];assert len(it)==1,it;r=it[0];assert r["pct"]==42 and r["written_by"]==sys.argv[1] and r["seat"]=="wednesday" and r["kind"]=="usage",r;print("      raw row fields:",sorted(k for k in r if not k.startswith("odata") and not k.endswith("@odata.type")));print("PASS  I5 raw table row USAGE/wednesday: pct 42, written_by = wednesday app id (clear row, no envelope — a percentage is not prose)")' "$wednesday_seat_APPID" || { echo "FAIL  (section I python arm, see traceback above)"; FAIL=1; }
# I6: an OLDER reading is ignored; a stale file publishes nothing; the stored row is untouched by both
OLDU=$(date -u -v-2H +%Y-%m-%dT%H:%M:%SZ)
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"pct":99,"resets_in":"1d","ts":"'$OLDU'"}' "$BASE/api/seat/usage"); expect "I6 POST a 2h-old reading (99%) -> 200 replaced (last write wins; the page will show its age)" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("updated") is True and d["stored"]["pct"]==99,d;print("PASS  I6 stored echo: 99%, updated (no older-reading guard: a fixture must never be able to block the real reading)")' "$SCRATCH/p_body.txt" || { echo "FAIL  (section I python arm, see traceback above)"; FAIL=1; }
printf '{"agent":"wednesday","pct":99,"resets_in":"1d","ts":"%s"}\n' "$OLDU" > "$SCRATCH/usage_fixture_stale.json"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" --file "$SCRATCH/usage_fixture_stale.json" > "$SCRATCH/p_usage_pub2.txt" 2>&1; echo "      $(tail -2 "$SCRATCH/p_usage_pub2.txt" | head -1 | cut -c1-160)"
expect "I6 post_usage.py on a STALE reading (2h) publishes nothing" "rc=3" "$(tail -1 "$SCRATCH/p_usage_pub2.txt")"
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" --file "$SCRATCH/usage_none_$$_$TS.json" > "$SCRATCH/p_usage_pub3.txt" 2>&1; expect "I6 post_usage.py on a MISSING file publishes nothing" "rc=3" "$(tail -1 "$SCRATCH/p_usage_pub3.txt")"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/usage"); python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));w=d["wednesday"];assert w["pct"]==99 and w["age_seconds"]>=7100,w;print("PASS  I6 after the stale/missing attempts (nothing published) the row is the 2h-old 99%% with age_seconds=%d -> the page renders it as no reading" % w["age_seconds"])' "$SCRATCH/p_body.txt" || { echo "FAIL  (section I python arm, see traceback above)"; FAIL=1; }
# I7: how the page renders it — the pages' OWN usageState in Node (fresh / ageing / >=30 min or absent -> "no reading")
node "$HERE/scripts/09d_usage_page_checks.mjs" > "$SCRATCH/p_09d.txt" 2>&1; expect "I7 page checks (usageState: fresh figure, ageing dimmed, stale >=30 min or absent -> 'no reading'; both pages identical)" 0 "$?"
/usr/bin/grep -i -c '^pass' "$SCRATCH/p_09d.txt" | sed 's/^/      09d PASS lines: /'
# I8: leave the board TRUE — republish this seat's REAL reading (rc 0 if fresh; rc 3 = this seat idle, the fixture row then ages into "no reading" within 30 min)
"$V" "$HERE/seat/post_usage.py" --seat wednesday --base "$BASE" > "$SCRATCH/p_usage_pub5.txt" 2>&1; RC8=$(tail -1 "$SCRATCH/p_usage_pub5.txt"); echo "      I8 real reading republished: $(tail -2 "$SCRATCH/p_usage_pub5.txt" | head -1 | cut -c1-140) $RC8"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/usage")
if [ "$RC8" = "rc=0" ]; then
  python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));w=d["wednesday"];f=json.load(open(sys.argv[2]));assert w["pct"]==f["pct"] and w["reading_ts"]==f["ts"],(w,f);print("PASS  I8 the board is left at THIS seat'"'"'s REAL reading: %d%% @ %s (== usage_wednesday.json)" % (w["pct"], w["reading_ts"]))' "$SCRATCH/p_body.txt" "/Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/usage_wednesday.json" || { echo "FAIL  (section I python arm, see traceback above)"; FAIL=1; }
else
  python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));w=d["wednesday"];assert w["age_seconds"]>=1800,w;print("PASS  I8 this seat has no fresh reading (rc %s); the board holds a row %ds old -> the page renders no reading (nothing faked)" % (sys.argv[2], w["age_seconds"]))' "$SCRATCH/p_body.txt" "$RC8" || { echo "FAIL  (section I python arm, see traceback above)"; FAIL=1; }
fi
unset TOK TOKT
echo "### J. Hide / unhide (2026-09-22, Kam 14:27 'clean up your boards') — reversible, seat-scoped, audited, never deletes"
c=$(hdr "$BASE/api/seat/health"); expect "J1 health" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("hide_route") is True and d["phase"]=="3",d;print("PASS  J1 health: phase 3 + hide_route true")' "$SCRATCH/p_body.txt" || { echo "FAIL  (section J python arm, see traceback above)"; FAIL=1; }
expect "J2 POST /api/seat/hide NO token" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d '{"client":"WED","id":"x"}' "$BASE/api/seat/hide")"
expect "J2 POST /api/seat/hide FORGED token" 401 "$(hdr -X POST -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Im5vcGUifQ.eyJhdWQiOiJ4In0.c2ln' -H 'Content-Type: application/json' -d '{"client":"WED","id":"x"}' "$BASE/api/seat/hide")"
ea_refused "J2 GET /api/messages?hidden=1 plain client (the viewer reveal is Easy Auth gated like every viewer route)" "$BASE/api/messages?hidden=1"
TOK=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)
TOKT=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","tuesday","--client","Datasec"]); print(sc.get_token(a, sc.load_ids()))
PY
)
# J3: this run's own synthetic WED row (live-wed-$TS, posted in section C) is the target — hidden, revealed, audited, unhidden
RKJ=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'WED' and id eq 'live-wed-$TS'" --select RowKey,ciphertext,wrapped_keys,iv -o json 2>/dev/null | python3 -c 'import json,sys;it=json.load(sys.stdin)["items"];json.dump(it,open(sys.argv[1],"w"));print(it[0]["RowKey"] if len(it)==1 else "")' "$SCRATCH/j_raw_before.json")
[ -n "$RKJ" ] && echo "PASS  J3 target row found: WED/$RKJ (this run's synthetic row)" || { echo "FAIL  J3 target row live-wed-$TS not found"; FAIL=1; }
expect "J3 TUESDAY token hides a WED row (another seat's tab; MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKT" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKJ'"}' "$BASE/api/seat/hide")"; echo "      body: $(head -c 120 "$SCRATCH/p_body.txt")"
expect "J3 WEDNESDAY token hides a Datasec row (MUST refuse)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"Datasec","id":"p3-delta-'$TS'"}' "$BASE/api/seat/hide")"
expect "J3 unknown row_key -> 404" 404 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"2026-09-22T00:00:00.000Z_no-such-'$TS'"}' "$BASE/api/seat/hide")"
expect "J3 client=ALL -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"ALL","row_key":"'$RKJ'"}' "$BASE/api/seat/hide")"
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKJ'","reason":"live probe J3"}' "$BASE/api/seat/hide"); expect "J3 wednesday HIDES its own row" 200 "$c"
AUDJ=$(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d["changed"] is True and d["row"]["hidden"] is True and d["by"]=="wednesday",d;print(d["audit_row_key"])' "$SCRATCH/p_body.txt") && echo "PASS  J3 hide echo: changed=true hidden=true by=wednesday (audit $AUDJ)" || { echo "FAIL  J3 hide echo"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$(date -u +%Y-%m-%dT00:00)&limit=1000"); expect "J3 seat list after the hide" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] not in ids and d["hidden_included"] is False;print("PASS  J3 hidden row ABSENT from the default seat list (%d WED rows today listed)" % len(ids))' "$SCRATCH/p_body.txt" "live-wed-$TS" || { echo "FAIL  (section J python arm, see traceback above)"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$(date -u +%Y-%m-%dT00:00)&limit=1000&hidden=1"); expect "J3 seat list ?hidden=1" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=[x for x in d["messages"] if x["id"]==sys.argv[2]];assert len(m)==1 and m[0]["hidden"] is True and m[0]["hidden_seat"]=="wednesday" and m[0]["hidden_by"]==sys.argv[3],m;print("PASS  J3 ?hidden=1 REVEALS it: hidden=true hidden_seat=wednesday hidden_by=wednesday app id hidden_at=%s" % m[0]["hidden_at"])' "$SCRATCH/p_body.txt" "live-wed-$TS" "$wednesday_seat_APPID" || { echo "FAIL  (section J python arm, see traceback above)"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/hide/audit?limit=1000"); expect "J3 GET /api/seat/hide/audit" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));a=[x for x in d["audit"] if x["RowKey"]==sys.argv[2]];assert len(a)==1 and a[0]["action"]=="hide" and a[0]["target_row_key"]==sys.argv[3] and a[0]["seat"]=="wednesday" and a[0]["reason"]=="live probe J3",a;assert all(x["target_client"] in ("WED","Secuura","ALL") for x in d["audit"]);print("PASS  J3 audit line via the API (who=wednesday, when=%s, row=%s); no foreign-partition audit line" % (a[0]["at"], a[0]["target_id"]))' "$SCRATCH/p_body.txt" "$AUDJ" "$RKJ" || { echo "FAIL  (section J python arm, see traceback above)"; FAIL=1; }
az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'WED' and RowKey eq '$RKJ'" --select RowKey,ciphertext,wrapped_keys,iv,hidden,hidden_seat -o json 2>/dev/null > "$SCRATCH/j_raw_after.json"
python3 -c 'import json,sys;b=json.load(open(sys.argv[1]))[0];a=json.load(open(sys.argv[2]))["items"][0];assert a["ciphertext"]==b["ciphertext"] and a["iv"]==b["iv"] and a["wrapped_keys"]==b["wrapped_keys"] and a["hidden"] is True and a["hidden_seat"]=="wednesday";print("PASS  J3 raw row: ciphertext/iv/wrapped_keys byte-identical after the hide; hidden=true merged (nothing deleted, nothing rewritten)")' "$SCRATCH/j_raw_before.json" "$SCRATCH/j_raw_after.json" || { echo "FAIL  (section J python arm, see traceback above)"; FAIL=1; }
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKJ'","reason":"live probe J3 undo"}' "$BASE/api/seat/unhide"); expect "J3 wednesday UNHIDES it" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d["changed"] is True and d["row"]["hidden"] is False,d;print("PASS  J3 unhide echo: changed=true hidden=false")' "$SCRATCH/p_body.txt" || { echo "FAIL  (section J python arm, see traceback above)"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$(date -u +%Y-%m-%dT00:00)&limit=1000"); python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] in ids;print("PASS  J3 row BACK in the default seat list after the unhide (reversible)")' "$SCRATCH/p_body.txt" "live-wed-$TS" || { echo "FAIL  (section J python arm, see traceback above)"; FAIL=1; }
unset TOK TOKT
echo "### K. File drawer (2026-09-22, Kam 15:26 download / 15:31 upload) — encrypted both ways, seat-scoped, bounded, audited, never deletes"
c=$(hdr "$BASE/api/seat/health"); expect "K1 health" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("file_route") is True and d.get("file_max_bytes")==33554432 and d["phase"]=="3",d;print("PASS  K1 health: phase 3 + file_route true + file_max_bytes 33554432 (32 MiB)")' "$SCRATCH/p_body.txt" || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
expect "K2 GET /api/seat/files NO token" 401 "$(hdr "$BASE/api/seat/files")"
expect "K2 POST /api/seat/files NO token" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d '{"client":"WED"}' "$BASE/api/seat/files")"
expect "K2 GET /api/seat/files/WED/<rk>/blob NO token" 401 "$(hdr "$BASE/api/seat/files/WED/2026-09-22T00:00:00.000Z_x/blob")"
expect "K2 GET /api/seat/files FORGED token" 401 "$(hdr -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Im5vcGUifQ.eyJhdWQiOiJ4In0.c2ln' "$BASE/api/seat/files")"
ea_refused "K2 GET /api/files plain client (viewer list, Easy Auth gated)" "$BASE/api/files"
ea_refused "K2 GET /api/files/WED/<rk>/blob plain client (viewer download, Easy Auth gated)" "$BASE/api/files/WED/2026-09-22T00:00:00.000Z_x/blob"
ea_refused "K2 PUT /api/files/WED/<rk>/blob plain client (Kam's upload bytes, Easy Auth gated)" -X PUT -H 'Content-Type: application/octet-stream' -d 'x' "$BASE/api/files/WED/2026-09-22T00:00:00.000Z_x/blob"
ea_refused "K2 POST /api/files with FORGED x-ms-client-principal-id = Kam's object id, from outside" -X POST -H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'Content-Type: application/json' -d '{"view":"wednesday"}' "$BASE/api/files"
ea_refused "K2 GET /api/static drawer.js plain client" "$BASE/static/drawer.js"
# K3: share -> list -> download round-trip as the WEDNESDAY seat with a REAL random file; sha256 equal after decrypt with the seat key and Kam's keys
head -c 3000 /dev/urandom > "$SCRATCH/k3_$TS.bin"; K3SHA=$(shasum -a 256 "$SCRATCH/k3_$TS.bin" | cut -c1-64)
"$V" "$HERE/seat/share_file.py" "$SCRATCH/k3_$TS.bin" --seat wednesday --client WED --base "$BASE" --note "live probe K3 $TS" --synthetic > "$SCRATCH/k3_share.txt" 2>&1
expect "K3 share_file.py --seat wednesday --client WED (3000 random bytes) rc" "rc=0" "$(tail -1 "$SCRATCH/k3_share.txt")"
K3ID=$(/usr/bin/grep -o 'file_id=[A-Za-z0-9._-]*' "$SCRATCH/k3_share.txt" | cut -d= -f2); K3RK=$(/usr/bin/grep -o 'row_key=[A-Za-z0-9._:-]*' "$SCRATCH/k3_share.txt" | cut -d= -f2); echo "      file_id=$K3ID row_key=$K3RK"
TOK=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","wednesday","--client","WED"]); print(sc.get_token(a, sc.load_ids()))
PY
)
TOKT=$("$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","tuesday","--client","Datasec"]); print(sc.get_token(a, sc.load_ids()))
PY
)
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/files?client=WED&since=$(date -u +%Y-%m-%dT00:00)&limit=1000"); expect "K3 wednesday GET /api/seat/files?client=WED" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=[x for x in d["files"] if x["id"]==sys.argv[2]];assert len(m)==1,m;r=m[0];assert r["status"]=="ready" and r["direction"]=="shared" and r["size"]==3016 and r["seat"]=="wednesday" and r["synthetic"] is True and len(r["wrapped_keys"])==4,r
raw=open(sys.argv[1]).read();assert "k3_" not in raw and "live probe K3" not in raw, "NAME/NOTE IN CLEAR";print("PASS  K3 listed: ready, direction=shared, size 3016 (=3000+16 tag), 4 wrapped keys; the name and note are NOT in the response (encrypted meta)")' "$SCRATCH/p_body.txt" "$K3ID" || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
cp "$SCRATCH/p_body.txt" "$SCRATCH/k3_list.json"
c=$(curl -s -o "$SCRATCH/k3_ct.bin" -D "$SCRATCH/p_hdr.txt" -w '%{http_code}' --max-time 60 -H "Authorization: Bearer $TOK" "$BASE/api/seat/files/WED/$K3RK/blob"); expect "K3 wednesday GET .../blob (download)" 200 "$c"
"$V" - "$SCRATCH/k3_list.json" "$K3ID" "$SCRATCH/k3_ct.bin" "$K3SHA" <<'PY' || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
import json,sys,hashlib; sys.path.insert(0,"/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/seat"); import envelope
CRED="/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud"; r=[x for x in json.load(open(sys.argv[1]))["files"] if x["id"]==sys.argv[2]][0]; ct=open(sys.argv[3],"rb").read(); want=sys.argv[4]
assert len(ct)==r["size"] and hashlib.sha256(ct).hexdigest()==r["sha256"], "stored bytes != row size/sha256"; print("PASS  K3 downloaded bytes: len == row size, sha256 == row sha256 (the API serves the stored ciphertext verbatim)")
assert hashlib.sha256(ct).hexdigest()!=want and ct[:3000]!=open("/dev/null","rb").read(), "ciphertext equals plaintext?!"; print("PASS  K3 the stored bytes are NOT the file (ciphertext sha256 != plaintext sha256)")
clear={"client":r["client"],"kind":"file","id":r["id"],"ts":r["ts"]}
for k in ("wednesday-seat.pem","kam-pilot-private.pem","kam-laptop-private.pem","kam-ipad-private.pem"):
    pt=envelope.decrypt_file(envelope.load_private(f"{CRED}/{k}"), r, clear, ct); m=json.loads(envelope.decrypt_text(envelope.load_private(f"{CRED}/{k}"), r, clear))
    ok=hashlib.sha256(pt).hexdigest()==want==m["sha256"] and m["name"].startswith("k3_"); print(("PASS  K3 %s decrypts meta (name %s) + bytes: sha256 == the file's %s…" % (k, m["name"], want[:12])) if ok else "FAIL  K3 %s" % k); assert ok
try: envelope.decrypt_file(envelope.load_private(f"{CRED}/tuesday-seat.pem"), r, clear, ct); print("FAIL  K3 TUESDAY KEY OPENED A WED FILE"); sys.exit(1)
except KeyError: print("PASS  K3 tuesday-seat.pem REFUSED on the WED file (KeyError: not a recipient)")
PY
mkdir -p "$SCRATCH/k3_fetch_$TS"; "$V" "$HERE/seat/get_files.py" --seat wednesday --base "$BASE" --ids "$K3ID" --include-synthetic --fetch "$SCRATCH/k3_fetch_$TS" > "$SCRATCH/k3_fetch.txt" 2>&1; expect "K3 get_files.py --fetch (seat-side download + decrypt) rc" "rc=0" "$(tail -1 "$SCRATCH/k3_fetch.txt")"
expect "K3 fetched file sha256 == original" "$K3SHA" "$(shasum -a 256 "$SCRATCH/k3_fetch_$TS/${K3ID}_k3_$TS.bin" 2>/dev/null | cut -c1-64)"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/files/audit?limit=1000"); expect "K3 GET /api/seat/files/audit" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));a=[x for x in d["audit"] if x["target_id"]==sys.argv[2]];acts=[x["action"] for x in a];assert acts.count("share")==1 and acts.count("download")>=2,acts;assert all(x["target_client"] in ("WED","Secuura","ALL") and x["kind"]=="file_audit" for x in d["audit"]);print("PASS  K3 audit lines for this file: %s (who=%s, at=%s); no foreign-partition line" % (acts, a[0]["seat"], a[0]["at"]))' "$SCRATCH/p_body.txt" "$K3ID" || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/hide/audit?limit=1000"); python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert all(x.get("kind","hide_audit")=="hide_audit" for x in d["audit"]);print("PASS  K3 the hide audit route still lists hide/unhide lines only (%d rows, no file_audit among them)" % len(d["audit"]))' "$SCRATCH/p_body.txt" || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
# K4: refusals — the Datasec client from the wednesday seat (403, exactly as post_message.py), R0 on reads/writes, unknown row, re-PUT of a ready row
"$V" "$HERE/seat/share_file.py" "$SCRATCH/k3_$TS.bin" --seat wednesday --client Datasec --base "$BASE" --note "must be refused" --synthetic > "$SCRATCH/k4_share.txt" 2>&1; expect "K4 share_file.py --seat wednesday --client Datasec (MUST refuse) rc" "rc=1" "$(tail -1 "$SCRATCH/k4_share.txt")"
expect "K4 ... the refusal is the API's 403" '"status": 403' "$(/usr/bin/grep -o '"status": [0-9]*' "$SCRATCH/k4_share.txt" | head -1)"
expect "K4 tuesday token GET the WED file's bytes (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/files/WED/$K3RK/blob")"
expect "K4 tuesday token PUT bytes onto the WED row (MUST refuse)" 403 "$(hdr -X PUT -H "Authorization: Bearer $TOKT" -H 'Content-Type: application/octet-stream' -d 'xxxxxxxxxxxxxxxxxxxxx' "$BASE/api/seat/files/WED/$K3RK/blob")"
expect "K4 tuesday GET /api/seat/files?client=WED (MUST refuse)" 403 "$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/files?client=WED")"
expect "K4 unknown row_key blob -> 404" 404 "$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/files/WED/2026-09-22T00:00:00.000Z_no-such-$TS/blob")"
c=$(hdr -X PUT -H "Authorization: Bearer $TOK" -H 'Content-Type: application/octet-stream' -d 'xxxxxxxxxxxxxxxxxxxxx' "$BASE/api/seat/files/WED/$K3RK/blob"); expect "K4 wednesday re-PUT bytes onto its READY row -> 200 duplicate (nothing overwritten)" 200 "$c"
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("duplicate") is True,d;print("PASS  K4 duplicate echo: the ready row keeps its bytes")' "$SCRATCH/p_body.txt" || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
c=$(curl -s -o "$SCRATCH/k4_ct.bin" -w '%{http_code}' --max-time 60 -H "Authorization: Bearer $TOK" "$BASE/api/seat/files/WED/$K3RK/blob"); expect "K4 bytes after the re-PUT are byte-identical to the first download" "$(shasum -a 256 "$SCRATCH/k3_ct.bin" | cut -c1-64)" "$(shasum -a 256 "$SCRATCH/k4_ct.bin" | cut -c1-64)"
# K5: the size bound — a row declaring more than FILE_MAX is refused 413 at the row; a PUT whose Content-Length exceeds the bound is refused 413 before the bytes are read
"$V" "$HERE/seat/share_file.py" "$SCRATCH/k3_$TS.bin" --seat wednesday --client WED --note "bound" --synthetic --dry-run > "$SCRATCH/k5_dry.txt" 2>&1
python3 -c 'import json,sys;t=open(sys.argv[1]).read();d=json.loads(t[:t.rindex("}")+1])["body"];d["size"]=33554433;d["id"]="k5big-"+sys.argv[2];json.dump(d,open(sys.argv[3],"w"));d2=dict(d);d2["size"]=33554432;d2["id"]="k5max-"+sys.argv[2];json.dump(d2,open(sys.argv[4],"w"));d3=dict(d);d3["size"]=16;d3["id"]="k5tiny-"+sys.argv[2];json.dump(d3,open(sys.argv[5],"w"))' "$SCRATCH/k5_dry.txt" "$TS" "$SCRATCH/k5_big.json" "$SCRATCH/k5_max.json" "$SCRATCH/k5_tiny.json"
expect "K5 POST /api/seat/files declaring size 33554433 (= bound + 1) -> 413" 413 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' --data-binary "@$SCRATCH/k5_big.json" "$BASE/api/seat/files")"; echo "      body: $(head -c 120 "$SCRATCH/p_body.txt")"
expect "K5 POST /api/seat/files declaring size 16 (< tag + 1 byte) -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' --data-binary "@$SCRATCH/k5_tiny.json" "$BASE/api/seat/files")"
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' --data-binary "@$SCRATCH/k5_max.json" "$BASE/api/seat/files"); expect "K5 POST a row declaring exactly the bound (33554432) -> 201 pending" 201 "$c"
K5RK=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["stored"]["row_key"])' "$SCRATCH/p_body.txt")
# a REAL 32 MiB + 1 body (a forged Content-Length with a short body never yields a status to curl — first run got 000, an instrument fault)
head -c 33554433 /dev/zero > "$SCRATCH/k5_big.bin"
expect "K5 PUT a real 33554433-byte body (bound + 1) onto it -> 413" 413 "$(curl -s -o "$SCRATCH/p_body.txt" -w '%{http_code}' --max-time 180 -X PUT -H "Authorization: Bearer $TOK" -H 'Content-Type: application/octet-stream' -H 'Expect:' --data-binary "@$SCRATCH/k5_big.bin" "$BASE/api/seat/files/WED/$K5RK/blob")"; echo "      body: $(head -c 120 "$SCRATCH/p_body.txt")"
# K3b: a file ABOVE Kam's 25 MB ask (30 MB of random bytes) makes the whole round trip — share, seat download, decrypt, sha256 equal
head -c 31457280 /dev/urandom > "$SCRATCH/k3b_$TS.bin"; K3BSHA=$(shasum -a 256 "$SCRATCH/k3b_$TS.bin" | cut -c1-64)
"$V" "$HERE/seat/share_file.py" "$SCRATCH/k3b_$TS.bin" --seat wednesday --client WED --base "$BASE" --note "live probe K3b 30 MB $TS" --synthetic > "$SCRATCH/k3b_share.txt" 2>&1
expect "K3b share_file.py 30 MB (31457280 random bytes) rc" "rc=0" "$(tail -1 "$SCRATCH/k3b_share.txt")"
K3BID=$(/usr/bin/grep -o 'file_id=[A-Za-z0-9._-]*' "$SCRATCH/k3b_share.txt" | cut -d= -f2); mkdir -p "$SCRATCH/k3b_fetch_$TS"
"$V" "$HERE/seat/get_files.py" --seat wednesday --base "$BASE" --ids "$K3BID" --include-synthetic --fetch "$SCRATCH/k3b_fetch_$TS" > "$SCRATCH/k3b_fetch.txt" 2>&1; expect "K3b get_files.py --fetch 30 MB rc" "rc=0" "$(tail -1 "$SCRATCH/k3b_fetch.txt")"
expect "K3b fetched 30 MB file sha256 == original" "$K3BSHA" "$(shasum -a 256 "$SCRATCH/k3b_fetch_$TS/${K3BID}_k3b_$TS.bin" 2>/dev/null | cut -c1-64)"
expect "K5 PUT bytes whose length != the declared size -> 400" 400 "$(hdr -X PUT -H "Authorization: Bearer $TOK" -H 'Content-Type: application/octet-stream' -d 'twenty-one bytes here' "$BASE/api/seat/files/WED/$K5RK/blob")"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/files?client=WED&since=$(date -u +%Y-%m-%dT00:00)&limit=1000"); python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));ids=[x["id"] for x in d["files"]];assert "k5max-"+sys.argv[2] not in ids and "k5big-"+sys.argv[2] not in ids;print("PASS  K5 the pending (never completed) row is NOT listed (%d ready WED files today)" % len(ids))' "$SCRATCH/p_body.txt" "$TS" || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
# K6: a message row carries attachments (clear file ids) — seat writer; 9 ids refused
"$V" "$HERE/seat/post_message.py" --seat wednesday --client WED --base "$BASE" --text "SYNTHETIC K6 $TS message with an attachment" --id k6-msg-$TS --synthetic --dry-run > "$SCRATCH/k6_dry.txt" 2>&1
python3 -c 'import json,sys;d=json.load(open(sys.argv[1]))["body"];d["attachments"]=[sys.argv[2]];json.dump(d,open(sys.argv[3],"w"));d2=dict(d);d2["id"]="k6-nine-"+sys.argv[4];d2["attachments"]=["f-%d"%i for i in range(9)];json.dump(d2,open(sys.argv[5],"w"))' "$SCRATCH/k6_dry.txt" "$K3ID" "$SCRATCH/k6_msg.json" "$TS" "$SCRATCH/k6_nine.json"
expect "K6 POST /api/seat/messages with attachments=[file id] -> 201" 201 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' --data-binary "@$SCRATCH/k6_msg.json" "$BASE/api/seat/messages")"
expect "K6 POST with 9 attachment ids -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' --data-binary "@$SCRATCH/k6_nine.json" "$BASE/api/seat/messages")"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$(date -u +%Y-%m-%dT00:00)&limit=1000"); python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));m=[x for x in d["messages"] if x["id"]=="k6-msg-"+sys.argv[2]];assert len(m)==1 and m[0].get("attachments")==[sys.argv[3]],m;print("PASS  K6 the message row lists attachments == [%s] (parsed list, clear ids only)" % sys.argv[3])' "$SCRATCH/p_body.txt" "$TS" "$K3ID" || { echo "FAIL  (section K python arm, see traceback above)"; FAIL=1; }
unset TOK TOKT
# K7: the page module — file envelope both directions between common.js (Node WebCrypto) and envelope.py
"$V" - > "$SCRATCH/pubkeys_k7.json" <<'PY'
import sys, os, glob, hashlib, base64, json
K="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud/app/keys"
def kid(pem): return hashlib.sha256(base64.b64decode("".join(l for l in pem.splitlines() if l and not l.startswith("-----")))).hexdigest()[:16]
files=sorted(glob.glob(K+"/kam-*-public.pub")); files.sort(key=lambda q:(0 if os.path.basename(q)=="kam-pilot-public.pub" else 1,q))
print(json.dumps({"kam":[{"name":os.path.basename(q)[4:-11],"kid":kid(open(q).read()),"pem":open(q).read()} for q in files],"seats":{s:{"kid":kid(open(f"{K}/{s}-seat-public.pub").read()),"pem":open(f"{K}/{s}-seat-public.pub").read()} for s in ("wednesday","tuesday")},"seat_of_client":{"WED":["wednesday"],"Secuura":["wednesday"],"Datasec":["tuesday"],"ALL":["wednesday","tuesday"]}}))
PY
node "$HERE/scripts/09e_file_webcrypto.mjs" "$SCRATCH/pubkeys_k7.json" "$SCRATCH" > "$SCRATCH/p_09e.txt" 2>&1; expect "K7 page file checks (encryptFile -> seat decrypts; seat encrypt_file -> page decrypts; tuesday refused; relabel refused)" 0 "$?"
/usr/bin/grep -i -c '^pass' "$SCRATCH/p_09e.txt" | sed 's/^/      09e PASS lines: /'
echo "### F. Rows per partition (counts only)"
for c in Secuura Datasec WED ALL; do n=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq '$c'" --select id -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))'); s=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq '$c' and synthetic eq true" --select id -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))'); h=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq '$c' and hidden eq true" --select id -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))'); echo "      messages/$c: $n (synthetic, hidden by the pages: $s; hidden by a seat, reversible: $h)"; done
echo "      messages/AUDIT (hide/unhide audit lines): $(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'AUDIT'" --select action -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))')"
echo "      files table (ready/pending, counts only): $(az storage entity query --account-name "$STORAGE" --table-name files --auth-mode login --select status -o json 2>/dev/null | python3 -c 'import json,sys,collections;c=collections.Counter(i.get("status") for i in json.load(sys.stdin)["items"]);print(dict(c))')  file AUDIT lines: $(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'AUDIT' and kind eq 'file_audit'" --select action -o json 2>/dev/null | python3 -c 'import json,sys,collections;c=collections.Counter(i.get("action") for i in json.load(sys.stdin)["items"]);print(dict(c))')"
echo "      cards total: $(az storage entity query --account-name "$STORAGE" --table-name cards --auth-mode login --select id -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))') (synthetic, hidden: $(az storage entity query --account-name "$STORAGE" --table-name cards --auth-mode login --filter "synthetic eq true" --select id -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))'))"
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL PROBES PASS || echo SOME PROBES FAILED)"
exit $FAIL
