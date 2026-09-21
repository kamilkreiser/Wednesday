#!/usr/bin/env bash
# Step 5 — PROVE IT LIVE against https://$WEBAPP.azurewebsites.net. Every line is a probe with expected vs actual; exit 1 if any mismatch.
# Synthetic text only. Then read the raw Table rows (RBAC, --auth-mode login) and decrypt offline with the pilot private key
# (positive control) and a WRONG key (negative control).
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
SCRATCH=${SCRATCH:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/bbb4a64c-5352-455e-b4e6-9f36320976aa/scratchpad}
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
  "$V" "$HERE/seat/post_message.py" --seat "$1" --client "$2" --base "$BASE" --text "$3" --id "$4" 2>"$SCRATCH/p_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["status"]); sys.stderr.write("      body: "+d["body"][:160]+"\n")'; [ -s "$SCRATCH/p_err.txt" ] && sed 's/^/      stderr: /' "$SCRATCH/p_err.txt" >&2; }
TS=$(date -u +%H%M%S)
echo "### C. The partition (R0) — token roles decide, body is refused"
expect "wednesday-seat -> client=Secuura" 201 "$(post wednesday Secuura "SYNTHETIC live alpha $TS — wednesday writes Secuura" live-alpha-$TS)"
expect "wednesday-seat -> client=WED" 201 "$(post wednesday WED "SYNTHETIC live wed $TS — wednesday writes WED" live-wed-$TS)"
expect "wednesday-seat -> client=Datasec (MUST refuse)" 403 "$(post wednesday Datasec "SYNTHETIC live beta $TS — must be refused" live-beta-$TS)"
expect "tuesday-seat -> client=Secuura (MUST refuse)" 403 "$(post tuesday Secuura "SYNTHETIC live gamma $TS — must be refused" live-gamma-$TS)"
expect "tuesday-seat -> client=WED (not granted to tuesday; MUST refuse)" 403 "$(post tuesday WED "SYNTHETIC live wed2 $TS — must be refused" live-wed2-$TS)"
expect "tuesday-seat -> client=Datasec" 201 "$(post tuesday Datasec "SYNTHETIC live delta $TS — tuesday writes Datasec" live-delta-$TS)"
echo "### D. Card + plaintext refusal"
CARD=$("$V" "$HERE/seat/post_card.py" --seat wednesday --client Secuura --base "$BASE" --title "SYNTHETIC card $TS: choose a synthetic option" --bluf "SYNTHETIC bluf — nothing real here" --option A "Option alpha (synthetic)" --option B "Option beta (synthetic)" --recommended A --id live-card-$TS | python3 -c 'import json,sys;print(json.load(sys.stdin)["status"])')
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
echo "### F. Rows per partition (counts only)"
for c in Secuura Datasec WED; do n=$(az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq '$c'" --select id -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))'); echo "      messages/$c: $n"; done
echo "      cards total: $(az storage entity query --account-name "$STORAGE" --table-name cards --auth-mode login --select id -o json 2>/dev/null | python3 -c 'import json,sys;print(len(json.load(sys.stdin)["items"]))')"
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL PROBES PASS || echo SOME PROBES FAILED)"
exit $FAIL
