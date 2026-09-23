#!/usr/bin/env bash
# Hide/unhide local matrix (2026-09-22, Kam 14:27:09 "clean up your boards") — the app on loopback (transient port 47793) against
# the REAL storage account through the CLI credential, with a SIMULATED Easy Auth principal (Kam's object id) for the viewer
# reads. Every row this matrix hides is one it POSTS ITSELF first, born synthetic (--synthetic; the pages hide such rows anyway),
# and every hide is reversed before the end. NOTHING IS DELETED — hidden is a MERGE of clear columns; the ciphertext is
# asserted byte-identical before and after. Arms: gates (401/401) · other seat's row 403 · unknown 404 · malformed 400 ·
# ALL 400 · hide -> absent from the seat list AND the viewer list · ?hidden=1 reveals it with hidden_* · audit row via the API
# and the raw table · unhide -> back in both lists · idempotent re-hide changed=false · tuesday hides her own Datasec probe row ·
# the audit is partition-scoped per seat · migrate_rewrap/mark_synthetic dry-runs leave the AUDIT partition alone.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
SCRATCH=${SCRATCH:?set SCRATCH to a scratch dir}
. "$HERE/scripts/ids.conf"
V=$HERE/.venv/bin/python
export TENANT_ID SEAT_API_APPID=$API_APPID STORAGE_ACCOUNT=$STORAGE SEAT_APP_MAP="$wednesday_seat_APPID:wednesday,$tuesday_seat_APPID:tuesday" KAM_OBJECT_ID=$KAM_USER_OBJ
PORT=47793; BASE="http://127.0.0.1:$PORT"; FAIL=0
( "$V" -m uvicorn main:app --app-dir "$HERE/app" --host 127.0.0.1 --port $PORT --log-level warning > "$SCRATCH/wedcloud_local_hide.log" 2>&1 ) &
APP_PID=$!
for i in $(seq 1 120); do curl -s -o /dev/null "$BASE/api/seat/health" && break; sleep 1; done   # 120 s: a cold venv import from the external drive took > 60 s once (first run 14:4x)
curl -s -o /dev/null "$BASE/api/seat/health" || { echo "FAIL  loopback app did not come up in 120 s: $(tail -3 "$SCRATCH/wedcloud_local_hide.log" | tr "\n" " ")"; kill $APP_PID 2>/dev/null; exit 1; }
expect() { if [ "$2" = "$3" ]; then echo "PASS  $1: expected $2 got $3"; else echo "FAIL  $1: expected $2 got $3"; FAIL=1; fi; }
hdr() { curl -s -o "$SCRATCH/h_body.txt" -w '%{http_code}' --max-time 30 "$@"; }
pyarm() { python3 -c "$1" "${@:2}" || { echo "FAIL  (python arm, see traceback above)"; FAIL=1; }; }
KAM=(-H "x-ms-client-principal-id: $KAM_USER_OBJ" -H 'x-ms-client-principal-name: kreiser.org@me.com')
mktok() { "$V" - <<PY
import sys; sys.path.insert(0,"$HERE/seat"); import seat_common as sc, argparse
a=sc.common_args(argparse.ArgumentParser()).parse_args(["--seat","$1","--client","$2"]); print(sc.get_token(a, sc.load_ids()))
PY
}
TOK=$(mktok wednesday WED); TOKT=$(mktok tuesday Datasec)
TS=$(date -u +%H%M%S); FTS="2026-09-22T00:00:$(date -u +%S).000Z"
echo "### HL1 health carries hide_route"
c=$(hdr "$BASE/api/seat/health"); expect "health" 200 "$c"; pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d.get("hide_route") is True and d.get("usage_route") is True and d["phase"]=="3",d;print("PASS  health: phase 3 + usage_route + hide_route true")' "$SCRATCH/h_body.txt"
echo "### HL2 gates"
expect "POST /api/seat/hide NO token" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d '{"client":"WED","id":"x"}' "$BASE/api/seat/hide")"
expect "POST /api/seat/hide FORGED token" 401 "$(hdr -X POST -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Im5vcGUifQ.eyJhdWQiOiJ4In0.c2ln' -H 'Content-Type: application/json' -d '{"client":"WED","id":"x"}' "$BASE/api/seat/hide")"
expect "POST /api/seat/unhide NO token" 401 "$(hdr -X POST -H 'Content-Type: application/json' -d '{"client":"WED","id":"x"}' "$BASE/api/seat/unhide")"
expect "GET /api/seat/hide/audit NO token" 401 "$(hdr "$BASE/api/seat/hide/audit")"
expect "GET /api/messages?hidden=1 without a principal header (app-level refusal; live: Easy Auth)" 401 "$(hdr "$BASE/api/messages?hidden=1")"
echo "### HL3 the probe rows (born synthetic): wednesday -> WED, tuesday -> Datasec"
post() { "$V" "$HERE/seat/post_message.py" --seat "$1" --client "$2" --base "$BASE" --text "$3" --id "$4" --ts "$FTS" --synthetic 2>"$SCRATCH/h_err.txt" | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["status"])'; }
RW="hide-probe-$TS"; RT="hide-probe-tue-$TS"; RKW="${FTS}_$RW"; RKT="${FTS}_$RT"
expect "wednesday posts WED synthetic row $RW" 201 "$(post wednesday WED "SYNTHETIC hide probe $TS — wednesday's own row" "$RW")"
expect "tuesday posts Datasec synthetic row $RT" 201 "$(post tuesday Datasec "SYNTHETIC hide probe $TS — tuesday's own row" "$RT")"
raw() { az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq '$1' and RowKey eq '$2'" -o json 2>/dev/null; }
raw WED "$RKW" > "$SCRATCH/h_raw_before.json"
pyarm 'import json,sys;it=json.load(open(sys.argv[1]))["items"];assert len(it)==1,it;r=it[0];assert r.get("hidden") is None and r["synthetic"] is True;print("      raw row before: hidden absent, synthetic true, ciphertext %d chars, kids %d" % (len(r["ciphertext"]), len(json.loads(r.get("wrapped_keys","[]")))))' "$SCRATCH/h_raw_before.json"
echo "### HL4 refusals: another seat's row 403 · unknown 404 · malformed 400 · ALL 400 · id ambiguity handled"
expect "wednesday hides tuesday's Datasec row (MUST refuse, R0)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"Datasec","row_key":"'$RKT'"}' "$BASE/api/seat/hide")"; echo "      body: $(head -c 120 "$SCRATCH/h_body.txt")"
expect "tuesday hides wednesday's WED row (MUST refuse, R0)" 403 "$(hdr -X POST -H "Authorization: Bearer $TOKT" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKW'"}' "$BASE/api/seat/hide")"
expect "wednesday hides an UNKNOWN row_key in WED" 404 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"2026-09-22T00:00:00.000Z_no-such-row-'$TS'"}' "$BASE/api/seat/hide")"
expect "wednesday hides an UNKNOWN id in WED" 404 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","id":"no-such-id-'$TS'"}' "$BASE/api/seat/hide")"
expect "malformed row_key -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"../etc"}' "$BASE/api/seat/hide")"
expect "neither row_key nor id -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED"}' "$BASE/api/seat/hide")"
expect "client=ALL (nobody's to hide) -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"ALL","row_key":"'$RKW'"}' "$BASE/api/seat/hide")"
expect "reason with control chars -> 400" 400 "$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKW'","reason":"<script>"}' "$BASE/api/seat/hide")"
echo "### HL5 hide -> absent from the seat list and the viewer list; ?hidden=1 reveals; audit; ciphertext untouched"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$FTS&limit=1000"); expect "seat list BEFORE the hide" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] in ids,ids;print("PASS  before: %s PRESENT in the seat list (%d rows since the fixture ts)" % (sys.argv[2], len(ids)))' "$SCRATCH/h_body.txt" "$RW"
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKW'","reason":"local matrix hide arm"}' "$BASE/api/seat/hide"); expect "wednesday HIDES its own WED row" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["changed"] is True and d["row"]["hidden"] is True and d["by"]=="wednesday" and d["row"]["row_key"]==sys.argv[2],d;print("      hide echo:",{k:d[k] for k in ("changed","by","audit_row_key")});print("PASS  hide echo: changed=true, hidden=true, by=wednesday")' "$SCRATCH/h_body.txt" "$RKW"
AUD1=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["audit_row_key"])' "$SCRATCH/h_body.txt")
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$FTS&limit=1000"); expect "seat list AFTER the hide" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] not in ids,ids;assert d.get("hidden_included") is False;print("PASS  after: %s ABSENT from the seat list (hidden_included=false)" % sys.argv[2])' "$SCRATCH/h_body.txt" "$RW"
c=$(hdr "${KAM[@]}" "$BASE/api/messages?client=WED&since=$FTS&limit=1000"); expect "viewer list (as Kam) AFTER the hide" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] not in ids,ids;print("PASS  after: %s ABSENT from the viewer list /api/messages (what the pages poll)" % sys.argv[2])' "$SCRATCH/h_body.txt" "$RW"
c=$(hdr "${KAM[@]}" "$BASE/api/messages?client=WED&since=$FTS&limit=1000&hidden=1"); expect "viewer list ?hidden=1 (the reveal)" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));m=[x for x in d["messages"] if x["id"]==sys.argv[2]];assert len(m)==1 and m[0]["hidden"] is True and m[0]["hidden_seat"]=="wednesday" and m[0]["hidden_by"]==sys.argv[3] and m[0].get("hidden_at"),m;assert d["hidden_included"] is True;print("      revealed row:",{k:m[0].get(k) for k in ("id","hidden","hidden_seat","hidden_at")});print("PASS  ?hidden=1 reveals the row with hidden=true, hidden_seat=wednesday, hidden_by = wednesday app id, hidden_at set")' "$SCRATCH/h_body.txt" "$RW" "$wednesday_seat_APPID"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$FTS&limit=1000&hidden=1"); expect "seat list ?hidden=1" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));m=[x for x in d["messages"] if x["id"]==sys.argv[2]];assert len(m)==1 and m[0]["hidden"] is True;print("PASS  seat ?hidden=1 reveals it too")' "$SCRATCH/h_body.txt" "$RW"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/hide/audit?limit=1000"); expect "GET /api/seat/hide/audit (wednesday)" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));a=[x for x in d["audit"] if x["RowKey"]==sys.argv[2]];assert len(a)==1,(sys.argv[2],[x["RowKey"] for x in d["audit"]][-5:]);x=a[0];assert x["action"]=="hide" and x["target_client"]=="WED" and x["target_row_key"]==sys.argv[3] and x["seat"]=="wednesday" and x["by"]==sys.argv[4] and x["changed"] is True and x["reason"]=="local matrix hide arm",x;assert all(y["target_client"] in ("WED","Secuura","ALL") for y in d["audit"]);print("      audit row:",{k:x[k] for k in ("at","action","target_client","seat","changed","reason")});print("PASS  audit row via the API: action=hide, target = the row, seat=wednesday, by = app id, when, reason; no Datasec audit line reaches the wednesday seat")' "$SCRATCH/h_body.txt" "$AUD1" "$RKW" "$wednesday_seat_APPID"
raw WED "$RKW" > "$SCRATCH/h_raw_after.json"
pyarm 'import json,sys;b=json.load(open(sys.argv[1]))["items"][0];a=json.load(open(sys.argv[2]))["items"][0];same=all(a.get(k)==b.get(k) for k in ("ciphertext","iv","kid","wrapped_key","wrapped_keys","scheme","id","ts","view","role","seat","written_by","written_at","synthetic"));assert same and a["hidden"] is True and a["hidden_seat"]=="wednesday","ROW MUTATED BEYOND THE HIDE COLUMNS";new=sorted(set(a)-set(b));print("      raw row after: new columns only:",new);print("PASS  raw row: ciphertext/iv/keys/routing byte-identical; ONLY hidden/hidden_at/hidden_by/hidden_seat were added (MERGE)")' "$SCRATCH/h_raw_before.json" "$SCRATCH/h_raw_after.json"
az storage entity query --account-name "$STORAGE" --table-name messages --auth-mode login --filter "PartitionKey eq 'AUDIT' and RowKey eq '$AUD1'" -o json 2>/dev/null > "$SCRATCH/h_raw_audit.json"
pyarm 'import json,sys;it=json.load(open(sys.argv[1]))["items"];assert len(it)==1,it;x=it[0];assert x["kind"]=="hide_audit" and x["action"]=="hide" and x["target_row_key"]==sys.argv[2] and "ciphertext" not in x;print("PASS  raw AUDIT row exists in the messages table (PartitionKey AUDIT), carries no envelope, target = the row")' "$SCRATCH/h_raw_audit.json" "$RKW"
echo "### HL6 idempotent re-hide, unhide -> back in both lists, unhide echo + audit"
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","id":"'$RW'"}' "$BASE/api/seat/hide"); expect "hide AGAIN by id (already hidden)" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["changed"] is False and d["row"]["hidden"] is True,d;print("PASS  re-hide: changed=false (idempotent), still audited (audit_row_key %s)" % d["audit_row_key"][:23])' "$SCRATCH/h_body.txt"
c=$(hdr -X POST -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' -d '{"client":"WED","row_key":"'$RKW'","reason":"local matrix unhide arm"}' "$BASE/api/seat/unhide"); expect "wednesday UNHIDES the row" 200 "$c"
pyarm 'import json,sys;d=json.load(open(sys.argv[1]));assert d["changed"] is True and d["row"]["hidden"] is False,d;print("PASS  unhide echo: changed=true, hidden=false")' "$SCRATCH/h_body.txt"
AUD2=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["audit_row_key"])' "$SCRATCH/h_body.txt")
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/messages?client=WED&since=$FTS&limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] in ids;m=[x for x in d["messages"] if x["id"]==sys.argv[2]][0];assert m["hidden"] is False and m.get("unhidden_seat")=="wednesday" and m.get("hidden_at");print("PASS  after unhide: %s BACK in the seat list, hidden=false, hidden_at + unhidden_* kept (history on the row)" % sys.argv[2])' "$SCRATCH/h_body.txt" "$RW"
c=$(hdr "${KAM[@]}" "$BASE/api/messages?client=WED&since=$FTS&limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] in ids;print("PASS  after unhide: %s BACK in the viewer list" % sys.argv[2])' "$SCRATCH/h_body.txt" "$RW"
c=$(hdr -H "Authorization: Bearer $TOK" "$BASE/api/seat/hide/audit?limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ks=[x["RowKey"] for x in d["audit"]];assert sys.argv[2] in ks and sys.argv[3] in ks;x=[y for y in d["audit"] if y["RowKey"]==sys.argv[3]][0];assert x["action"]=="unhide" and x["changed"] is True;print("PASS  audit holds hide + re-hide + unhide lines for the row (unhide: action=unhide, changed=true)")' "$SCRATCH/h_body.txt" "$AUD1" "$AUD2"
echo "### HL7 tuesday hides HER OWN Datasec probe row (the six real rows are hers to hide); the CLI; audit scoped per seat"
"$V" "$HERE/seat/hide_message.py" --seat tuesday --client Datasec --base "$BASE" --row-key "$RKT" --reason "local matrix tuesday arm" > "$SCRATCH/h_cli1.txt" 2>&1; expect "hide_message.py --seat tuesday hides her Datasec row rc" "rc=0" "$(tail -1 "$SCRATCH/h_cli1.txt")"; echo "      $(tail -2 "$SCRATCH/h_cli1.txt" | head -1 | cut -c1-160)"
"$V" "$HERE/seat/hide_message.py" --seat tuesday --client Datasec --base "$BASE" --list-hidden --since "$FTS" > "$SCRATCH/h_cli2.txt" 2>&1; expect "hide_message.py --list-hidden rc" "rc=0" "$(tail -1 "$SCRATCH/h_cli2.txt")"
/usr/bin/grep -q -- "Datasec/$RKT " "$SCRATCH/h_cli2.txt" && echo "PASS  --list-hidden shows Datasec/$RKT (hidden_seat=tuesday)" || { echo "FAIL  --list-hidden does not show the hidden row: $(cat "$SCRATCH/h_cli2.txt" | tr '\n' ' ' | cut -c1-300)"; FAIL=1; }
c=$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/messages?client=Datasec&since=$FTS&limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] not in ids;print("PASS  tuesday seat list: her hidden row ABSENT")' "$SCRATCH/h_body.txt" "$RT"
c=$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/hide/audit?limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));a=d["audit"];assert a and all(x["target_client"] in ("Datasec","ALL") for x in a) and any(x["target_row_key"]==sys.argv[2] and x["seat"]=="tuesday" for x in a);assert not any(x["target_row_key"]==sys.argv[3] for x in a);print("PASS  tuesday audit: only Datasec/ALL targets (%d rows), her hide present, the WED hide absent (scoped per seat)" % len(a))' "$SCRATCH/h_body.txt" "$RKT" "$RKW"
"$V" "$HERE/seat/hide_message.py" --seat wednesday --client Datasec --base "$BASE" --row-key "$RKT" --unhide > "$SCRATCH/h_cli3.txt" 2>&1; expect "hide_message.py --seat wednesday --unhide tuesday's row (MUST refuse) rc" "rc=1" "$(tail -1 "$SCRATCH/h_cli3.txt")"; /usr/bin/grep -q '"status": 403' "$SCRATCH/h_cli3.txt" && echo "PASS  refused with HTTP 403" || { echo "FAIL  not a 403: $(head -c 200 "$SCRATCH/h_cli3.txt")"; FAIL=1; }
"$V" "$HERE/seat/hide_message.py" --seat tuesday --client Datasec --base "$BASE" --id "$RT" --unhide --reason "local matrix tuesday unhide" > "$SCRATCH/h_cli4.txt" 2>&1; expect "hide_message.py --seat tuesday --unhide by id rc" "rc=0" "$(tail -1 "$SCRATCH/h_cli4.txt")"
c=$(hdr -H "Authorization: Bearer $TOKT" "$BASE/api/seat/messages?client=Datasec&since=$FTS&limit=1000"); pyarm 'import json,sys;d=json.load(open(sys.argv[1]));ids=[m["id"] for m in d["messages"]];assert sys.argv[2] in ids;print("PASS  tuesday seat list: her row BACK after the unhide")' "$SCRATCH/h_body.txt" "$RT"
echo "### HL8 the whole-table scanners leave the AUDIT partition alone"
"$V" "$HERE/seat/migrate_rewrap.py" --dry-run > "$SCRATCH/h_migrate.txt" 2>&1; expect "migrate_rewrap.py --dry-run rc" 0 "$?"
pyarm 'import re,sys;s=open(sys.argv[1]).read();m=re.search(r"AUDIT\s+unknown partition \(left alone\)\s+(\d+)",s);assert m and int(m.group(1))>=1,s[-600:];assert "to_rewrap\": 0" in s or "to rewrap" not in s.split("== cards")[0].replace("to_rewrap",""),s[-400:];print("PASS  migrate_rewrap dry-run: AUDIT rows = unknown partition (left alone): %s; nothing to rewrap" % m.group(1))' "$SCRATCH/h_migrate.txt"
/usr/bin/grep -o 'to_rewrap": [0-9]*' "$SCRATCH/h_migrate.txt" | sed 's/^/      /'
"$V" "$HERE/seat/mark_synthetic.py" --dry-run --tables messages > "$SCRATCH/h_marksyn.txt" 2>&1; expect "mark_synthetic.py --dry-run rc" 0 "$?"
pyarm 'import re,sys;s=open(sys.argv[1]).read();m=re.search(r"AUDIT\s+left alone \(real\)\s+(\d+)",s);assert m,s[-600:];assert not re.search(r"AUDIT\s+to mark",s);print("PASS  mark_synthetic dry-run: AUDIT rows left alone (%s), none to mark" % m.group(1))' "$SCRATCH/h_marksyn.txt"
unset TOK TOKT
kill $APP_PID 2>/dev/null; wait $APP_PID 2>/dev/null
echo "### RESULT: $([ $FAIL = 0 ] && echo ALL PASS || echo SOME FAILED)"
exit $FAIL
