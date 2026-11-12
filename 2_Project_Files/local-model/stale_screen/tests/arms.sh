#!/bin/bash
# arms.sh - the red-proofs for the stale-ticket screen. Run BEFORE the nightly job is armed (and after any edit to screen.py).
#   bash arms.sh            deterministic arms (stub Spark / stub HTTP box / fixture board / scratch git repo): no Linear, no live Spark
#   ARMS_LIVE=1 bash arms.sh  adds ARM L: the deleted-file ticket against the REAL Spark (waits for the box; one request)
# Every arm prints PASS or FAIL with what it measured; exit 1 if any FAIL. Never touches a project checkout, Linear or the shared
# Spark state (a private SPARK_STATE_DIR is used for the lock arms). Scratch lives in stale_screen/scratch/arms_* (gitignored).
set -u
HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S="$(cd -P "$HERE/.." && pwd)"
PY=python3
SCRATCH="$S/scratch/arms_$(date +%Y%m%d_%H%M%S)_$$"
mkdir -p "$SCRATCH" || exit 2
FAILS=0; PASSES=0
pass() { echo "PASS  $1  [$2]"; PASSES=$((PASSES+1)); }
fail() { echo "FAIL  $1  [$2]"; FAILS=$((FAILS+1)); }
col() { awk -F'\t' -v k="$2" -v c="$3" '$1==k{print $c}' "$1/proposals.tsv"; }   # $1 outdir $2 key $3 column

# ---- scratch repo: develop with keep.ts, a DELETED gone.ts and a MOVED old/name.ts -> new/name.ts
R="$SCRATCH/repo"; mkdir -p "$R/src/old"
git -C "$R" init -q -b develop 2>/dev/null || { git -C "$R" init -q; git -C "$R" checkout -q -b develop; }
git -C "$R" config user.email a@b.c; git -C "$R" config user.name arms
printf 'export function keepFn() { return 1; }\nexport const KEEP_ME = 2;\n' > "$R/src/keep.ts"
printf 'export function goneFn() { return 3; }\n' > "$R/src/gone.ts"
printf 'export function nameFn() { return 4; }\n' > "$R/src/old/name.ts"
git -C "$R" add -A; GIT_COMMITTER_DATE="2020-01-01T00:00:00" git -C "$R" commit -q -m "initial" --date="2020-01-01T00:00:00"
git -C "$R" rm -q src/gone.ts; mkdir -p "$R/src/new"; git -C "$R" mv src/old/name.ts src/new/name.ts
git -C "$R" commit -q -m "remove gone.ts, move name.ts"
echo "// b" >> "$R/src/keep.ts"; git -C "$R" commit -q -am "KS-8: implement the thing the ticket asks for"
echo "// c" >> "$R/src/keep.ts"; git -C "$R" commit -q -am "Refs KS-9: a tangent that only points at the ticket"
git -C "$R" update-ref refs/remotes/origin/develop develop 2>/dev/null

# ---- fixture board (same shape the Linear query returns)
FIX="$SCRATCH/board.json"
$PY - "$FIX" <<'EOF'
import json, sys
def t(n, title, desc, who=None):
    return {"identifier": "KS-%d" % n, "number": n, "title": title, "description": desc, "priority": 3, "createdAt": "2020-06-01T00:00:00Z",
            "updatedAt": "2020-06-0%dT00:00:00Z" % n, "state": {"name": "Backlog"}, "assignee": who}
b = [t(1, "gone helper still referenced", "The helper in `src/gone.ts:1` throws on empty input and `goneFn` is wrong."),
     t(2, "make the onboarding flow nicer", "The onboarding copy is vague and the wizard feels long. No code is named here."),
     t(3, "name helper edge case", "See `src/old/name.ts` where `nameFn` mishandles null."),
     t(4, "keepFn returns a constant", "In `src/keep.ts:1` the function `keepFn` returns a constant instead of reading config."),
     t(5, "peter owns this", "`src/keep.ts` needs a lint pass.", {"name": "Peter", "email": "peter@obeden.com"}),
     t(6, "partitioned ticket", "`src/keep.ts:2` KEEP_ME should be a getter."),
     t(8, "ticket whose own commit landed", "Nothing code-like named here, just prose about the thing."),
     t(9, "ticket only referenced by a commit", "Nothing code-like named here either, just prose."),
     t(7, "keepFn is a constant", "`keepFn` in `src/keep.ts` ignores config and returns a constant.")]
json.dump(b, open(sys.argv[1], "w"))
EOF
echo "KS-6" > "$SCRATCH/partition.txt"
COMMON=(--fixture "$FIX" --repo "$R" --no-remote --scratch "$SCRATCH/clone" --partition-file "$SCRATCH/partition.txt")
NOSTATE=(--state-file "$SCRATCH/state.tsv")

# ---- facts for the candidate-id lookup (facts-only run: no Spark asked)
FO="$SCRATCH/out_facts"
$PY -I "$S/screen.py" --limit 20 --out "$FO" --facts-only "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/facts.log" 2>&1
fid() { $PY -I - "$FO/facts/$1.json" "$2" "$3" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
for f in d["facts"]:
    if f["kind"] == sys.argv[2] and sys.argv[3] in f["text"]:
        print(f["id"]); break
EOF
}
F_GONE="$(fid KS-1 PATH 'src/gone.ts')"; F_MOVED="$(fid KS-3 PATH 'src/old/name.ts')"; F_KEEP="$(fid KS-4 PATH 'src/keep.ts')"
F_CAND7="$(fid KS-7 CAND 'KS-4')"
[ -n "$F_GONE" ] && [ -n "$F_MOVED" ] && [ -n "$F_KEEP" ] && [ -n "$F_CAND7" ] || { echo "FAIL  setup: fact ids not found (gone=$F_GONE moved=$F_MOVED keep=$F_KEEP cand7=$F_CAND7); see $SCRATCH/facts.log"; exit 1; }

# ---- ARM 0 (the skips): Peter's ticket and the no-write partition never reach the Spark
if awk -F'\t' '$1=="KS-5"||$1=="KS-6"{f=1} END{exit !f}' "$FO/proposals.tsv"; then fail "ARM 0 skips" "KS-5 (Peter) or KS-6 (partition) was screened"; else
  /usr/bin/grep -q "assigned to Peter/Stuart 1" "$FO/report.md" && /usr/bin/grep -q "no-write partition 1" "$FO/report.md" && pass "ARM 0 skips: Peter-assigned and partition tickets are not screened and are counted" "KS-5, KS-6 absent from proposals.tsv; report.md counts 1 and 1" || fail "ARM 0 skips" "report.md does not count the skips"; fi

# ---- ARM 8: commit mentions are classified: the ticket's OWN commit (subject opens with the key) = MENTIONED; a "Refs KS-n" commit = REFERENCED only
st8="$($PY -I - "$FO/facts" <<'EOF2'
import json, sys
def st(k):
    d = json.load(open("%s/%s.json" % (sys.argv[1], k)))
    return [f["status"] for f in d["facts"] if f["kind"] == "COMMITS"]
print(st("KS-8"), st("KS-9"), st("KS-2"))
EOF2
)"
[ "$st8" = "['MENTIONED'] ['REFERENCED'] ['UNMENTIONED']" ] && pass "ARM 8 commit mentions classified: own-work -> MENTIONED, Refs-only -> REFERENCED, none -> UNMENTIONED" "KS-8/KS-9/KS-2 -> $st8" || fail "ARM 8" "got $st8"

# ---- ARM 1: the cited file was DELETED -> a Spark STILL-VALID is REFUSED; LIKELY-FIXED passes
cat > "$SCRATCH/stub1.json" <<EOF
{"KS-1": {"proposal":"STILL-VALID","duplicate_of":null,"fact_ids":["$F_GONE"],"reason":"[$F_GONE] \`src/gone.ts\` is still the code the ticket describes"},
 "KS-3": {"proposal":"CITATION-MOVED","duplicate_of":null,"fact_ids":["$F_MOVED"],"reason":"[$F_MOVED] \`src/old/name.ts\` no longer exists; \`src/new/name.ts\` has the same name"},
 "KS-4": {"proposal":"STILL-VALID","duplicate_of":null,"fact_ids":["$F_KEEP"],"reason":"[$F_KEEP] \`src/keep.ts\` exists at develop"},
 "KS-7": {"proposal":"POSSIBLE-DUPLICATE","duplicate_of":"KS-4","fact_ids":["$F_CAND7"],"reason":"[$F_CAND7] open ticket KS-4 shares \`src/keep.ts\` and the symbol \`keepFn\`"}}
EOF
O1="$SCRATCH/out1"; SCREEN_SPARK_STUB="$SCRATCH/stub1.json" $PY -I "$S/screen.py" --limit 20 --out "$O1" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/run1.log" 2>&1; rc=$?
p1="$(col "$O1" KS-1 2)"
if [ "$p1" = "REFUSED" ]; then pass "ARM 1a deleted cited file + Spark says STILL-VALID -> REFUSED, never STILL-VALID" "KS-1 -> $p1: $(col "$O1" KS-1 3 | cut -c1-110)"; else fail "ARM 1a" "KS-1 -> '$p1' (rc $rc)"; fi
cat > "$SCRATCH/stub1b.json" <<EOF
{"KS-1": {"proposal":"LIKELY-FIXED","duplicate_of":null,"fact_ids":["$F_GONE"],"reason":"[$F_GONE] \`src/gone.ts\` does NOT exist at develop and no file with that name exists"}}
EOF
O1B="$SCRATCH/out1b"; SCREEN_SPARK_STUB="$SCRATCH/stub1b.json" $PY -I "$S/screen.py" --keys KS-1 --out "$O1B" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/run1b.log" 2>&1
p="$(col "$O1B" KS-1 2)"; [ "$p" = "LIKELY-FIXED" ] && pass "ARM 1b deleted cited file + Spark says LIKELY-FIXED citing the MISSING fact -> accepted" "KS-1 -> $p, checker $(col "$O1B" KS-1 5)" || fail "ARM 1b" "KS-1 -> '$p'"
p="$(col "$O1" KS-3 2)"; [ "$p" = "CITATION-MOVED" ] && pass "ARM 1c moved file + CITATION-MOVED citing the MOVED fact -> accepted" "KS-3 -> $p" || fail "ARM 1c" "KS-3 -> '$p': $(col "$O1" KS-3 3)"
p="$(col "$O1" KS-4 2)"; [ "$p" = "STILL-VALID" ] && pass "ARM 1d control: present file + STILL-VALID citing the OK fact -> accepted (the checker is not a blanket refuser)" "KS-4 -> $p" || fail "ARM 1d" "KS-4 -> '$p': $(col "$O1" KS-4 3)"
p="$(col "$O1" KS-7 2)"; [ "$p" = "POSSIBLE-DUPLICATE KS-4" ] && pass "ARM 1e duplicate of an OPEN candidate citing its CANDIDATE fact -> accepted" "KS-7 -> $p" || fail "ARM 1e" "KS-7 -> '$p': $(col "$O1" KS-7 3)"

# ---- ARM 2: a ticket with no citations -> CANNOT-TELL, decided by the extractor (the stub has no reply for KS-2: a Spark call would error)
p="$(col "$O1" KS-2 2)"; s="$(col "$O1" KS-2 6)"
[ "$p" = "CANNOT-TELL" ] && [ "$s" = "rule" ] && pass "ARM 2 no citations -> CANNOT-TELL (source=rule, Spark not asked)" "KS-2 -> $p / $s" || fail "ARM 2" "KS-2 -> '$p' / '$s'"

# ---- ARM 3: planted Spark reason citing an INVENTED fact -> REFUSED; invented duplicate key -> REFUSED; invented fact id -> REFUSED
cat > "$SCRATCH/stub3.json" <<EOF
{"KS-1": {"proposal":"LIKELY-FIXED","duplicate_of":null,"fact_ids":["$F_GONE"],"reason":"[$F_GONE] \`src/invented.ts\` was removed in commit abcdef1234"},
 "KS-3": {"proposal":"CITATION-MOVED","duplicate_of":null,"fact_ids":["F99"],"reason":"[F99] \`src/old/name.ts\` moved"},
 "KS-4": {"proposal":"POSSIBLE-DUPLICATE","duplicate_of":"KS-9999","fact_ids":["$F_KEEP"],"reason":"[$F_KEEP] same as KS-9999"},
 "KS-7": {"proposal":"STILL-VALID","duplicate_of":null,"fact_ids":[],"reason":"looks fine"}}
EOF
O3="$SCRATCH/out3"; SCREEN_SPARK_STUB="$SCRATCH/stub3.json" $PY -I "$S/screen.py" --limit 20 --out "$O3" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/run3.log" 2>&1
r1="$(col "$O3" KS-1 3)"; [ "$(col "$O3" KS-1 2)" = "REFUSED" ] && echo "$r1" | /usr/bin/grep -q "src/invented.ts" && pass "ARM 3a planted reason citing an invented path/sha -> REFUSED, naming it" "$(echo "$r1" | cut -c1-150)" || fail "ARM 3a" "KS-1 -> $(col "$O3" KS-1 2): $r1"
[ "$(col "$O3" KS-3 2)" = "REFUSED" ] && col "$O3" KS-3 3 | /usr/bin/grep -q "F99" && pass "ARM 3b invented fact id F99 -> REFUSED" "$(col "$O3" KS-3 3 | cut -c1-120)" || fail "ARM 3b" "KS-3 -> $(col "$O3" KS-3 2)"
[ "$(col "$O3" KS-4 2)" = "REFUSED" ] && col "$O3" KS-4 3 | /usr/bin/grep -q "KS-9999" && pass "ARM 3c duplicate key that is not an open ticket (KS-9999) -> REFUSED" "$(col "$O3" KS-4 3 | cut -c1-120)" || fail "ARM 3c" "KS-4 -> $(col "$O3" KS-4 2)"
[ "$(col "$O3" KS-7 2)" = "REFUSED" ] && pass "ARM 3d class with no cited fact (STILL-VALID, fact_ids empty) -> REFUSED" "$(col "$O3" KS-7 3 | cut -c1-120)" || fail "ARM 3d" "KS-7 -> $(col "$O3" KS-7 2)"

# ---- ARM 4: Spark unreachable -> clean exit 0, says so, writes nothing
O4="$SCRATCH/out4"; SPARK_STATE_DIR="$SCRATCH/state4" SPARK_URL="http://127.0.0.1:1" $PY -I "$S/screen.py" --limit 20 --out "$O4" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/run4.log" 2>&1; rc=$?
if [ $rc -eq 0 ] && /usr/bin/grep -q "REFUSED (down)" "$SCRATCH/run4.log" && [ ! -e "$O4" ]; then pass "ARM 4a Spark unreachable (tunnel down) -> exit 0, 'REFUSED (down)' logged, nothing written" "rc=0; $(/usr/bin/grep -m1 REFUSED "$SCRATCH/run4.log" | cut -c1-120)"; else fail "ARM 4a" "rc=$rc out_exists=$([ -e "$O4" ] && echo yes || echo no): $(head -c 200 "$SCRATCH/run4.log")"; fi
# 4b: the box answers /v1/models but every completion fails (500): per-ticket ERROR, aborts after 3, exit 0
PORT=$((47900 + RANDOM % 80))
$PY -I - "$PORT" > "$SCRATCH/server.log" 2>&1 <<'EOF' &
import http.server, sys
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path == "/v1/models":
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"data":[]}')
        else:
            self.send_response(404); self.end_headers()
    def do_POST(self):
        self.send_response(500); self.end_headers(); self.wfile.write(b"boom")
http.server.HTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
EOF
SRV=$!; sleep 1
O4B="$SCRATCH/out4b"; SPARK_STATE_DIR="$SCRATCH/state4b" SPARK_URL="http://127.0.0.1:$PORT" $PY -I "$S/screen.py" --limit 20 --out "$O4B" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/run4b.log" 2>&1; rc=$?
nerr="$(awk -F'\t' '$2=="ERROR"' "$O4B/proposals.tsv" 2>/dev/null | wc -l | tr -d ' ')"
if [ $rc -eq 0 ] && [ "$nerr" = "3" ] && /usr/bin/grep -q "STOPPED" "$SCRATCH/run4b.log" && [ ! -d "$SCRATCH/state4b/round.lock" ]; then pass "ARM 4b box up but completions fail (HTTP 500) -> 3 ERROR rows, stops, exit 0, lock released" "rc=0 errors=$nerr; $(/usr/bin/grep -m1 STOPPED "$SCRATCH/run4b.log" | cut -c1-120)"; else fail "ARM 4b" "rc=$rc errors=$nerr lock_left=$([ -d "$SCRATCH/state4b/round.lock" ] && echo yes || echo no)"; fi

# ---- ARM 5: refuse-while-a-Spark-round-is-live (private state dir; the lock is held by a REAL live pid)
mkdir -p "$SCRATCH/state5/round.lock"; sleep 120 & HOLD=$!
echo "$HOLD" > "$SCRATCH/state5/round.lock/pid"; echo "arms: pretend round" > "$SCRATCH/state5/round.lock/what"
O5="$SCRATCH/out5"; SPARK_STATE_DIR="$SCRATCH/state5" SPARK_URL="http://127.0.0.1:$PORT" $PY -I "$S/screen.py" --limit 20 --out "$O5" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/run5.log" 2>&1; rc=$?
if [ $rc -eq 0 ] && /usr/bin/grep -q "REFUSED (busy).*round is live" "$SCRATCH/run5.log" && [ ! -e "$O5" ] && [ -d "$SCRATCH/state5/round.lock" ]; then pass "ARM 5a live round.lock holder (tunnel UP) -> refuses 'a Spark round is live', exit 0, no request, lock untouched" "rc=0; $(/usr/bin/grep -m1 REFUSED "$SCRATCH/run5.log" | cut -c1-130)"; else fail "ARM 5a" "rc=$rc: $(head -c 240 "$SCRATCH/run5.log")"; fi
kill "$HOLD" 2>/dev/null; wait "$HOLD" 2>/dev/null
# 5b control: the same lock but its holder is DEAD -> reclaimed (moved aside, never deleted) and the run proceeds to the box (500s here)
O5B="$SCRATCH/out5b"; SPARK_STATE_DIR="$SCRATCH/state5" SPARK_URL="http://127.0.0.1:$PORT" $PY -I "$S/screen.py" --limit 20 --out "$O5B" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/run5b.log" 2>&1; rc=$?
if [ $rc -eq 0 ] && /usr/bin/grep -q "reclaimed a stale round.lock" "$SCRATCH/run5b.log" && [ -d "$O5B" ] && [ -n "$(ls "$SCRATCH/state5/stale_locks" 2>/dev/null)" ]; then pass "ARM 5b control: dead-holder lock is reclaimed (moved to stale_locks), run proceeds -> the gate refuses for the RIGHT reason, not always" "rc=0; stale_locks kept"; else fail "ARM 5b" "rc=$rc: $(head -c 240 "$SCRATCH/run5b.log")"; fi
# 5c: a live round.lock arriving between tickets: (covered by wait_box before every request) - the lock is taken per request and released
[ ! -d "$SCRATCH/state5/round.lock" ] && pass "ARM 5c our own round.lock is released after every request and at exit (nothing left blocking the box)" "no round.lock in the private state dir" || fail "ARM 5c" "round.lock left behind"
kill "$SRV" 2>/dev/null; wait "$SRV" 2>/dev/null

# ---- ARM 9: the nightly entry point: outside 01:00-05:00 it refuses cleanly; inside the window with the Spark down it still exits 0 and says why
N1="$(STALE_HOUR=12 STALE_STATE="$SCRATCH/nstate" STALE_OUT="$SCRATCH/nout1" bash "$S/nightly.sh" 2>&1)"; rc=$?
if [ $rc -eq 0 ] && echo "$N1" | /usr/bin/grep -q "REFUSED - outside the 01:00-05:00 window" && [ ! -e "$SCRATCH/nout1" ]; then pass "ARM 9a nightly.sh at hour 12 -> REFUSED outside the window, exit 0, nothing run" "rc=0"; else fail "ARM 9a" "rc=$rc: $N1"; fi
N2="$(STALE_HOUR=2 STALE_STATE="$SCRATCH/nstate" STALE_OUT="$SCRATCH/nout2" SPARK_STATE_DIR="$SCRATCH/state9" SPARK_URL="http://127.0.0.1:1" bash "$S/nightly.sh" 2>&1)"; rc=$?
if [ $rc -eq 0 ] && echo "$N2" | /usr/bin/grep -q "REFUSED (down)" && echo "$N2" | /usr/bin/grep -q "finished .* rc=0" && [ ! -d "$SCRATCH/nstate/nightly.lock" ]; then pass "ARM 9b nightly.sh at hour 2 with the tunnel down -> logs 'REFUSED (down)', finishes rc=0, nightly.lock released" "rc=0"; else fail "ARM 9b" "rc=$rc: $N2"; fi

# ---- ARM 6: the checker as a pure function (red-proofs of the refusal rules), and the no-board-write guard
$PY -I - "$S/screen.py" > "$SCRATCH/arm6.out" 2>&1 <<'EOF'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("screen", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
F = lambda i, k, s, t: {"id": i, "kind": k, "status": s, "text": t}
facts = [F("F1", "PATH", "MISSING", "cited `a/b.ts` does NOT exist at develop"), F("F2", "PATH", "OK", "cited `c/d.ts` exists at develop"),
         F("F3", "CAND", "CANDIDATE", "open ticket KS-5 [Backlog] \"x\" shares paths ['c/d.ts']")]
ok = lambda raw, n=2, cands={"KS-5"}: m.check_proposal(raw, facts, "KS-1", {"KS-1", "KS-5"}, cands, n)[0]
res = []
res.append(("STILL-VALID refused while FACTS hold a MISSING path", not ok({"proposal": "STILL-VALID", "fact_ids": ["F2"], "reason": "[F2] `c/d.ts` exists"})))
res.append(("STILL-VALID refused with zero citations", not ok({"proposal": "STILL-VALID", "fact_ids": ["F2"], "reason": "[F2] `c/d.ts` exists"}, n=0)))
res.append(("LIKELY-FIXED citing only an OK fact refused", not ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F2"], "reason": "[F2] `c/d.ts` exists"})))
facts.append(F("F4", "CHANGES", "CHANGED", "5 commit(s) touched `c/d.ts` since the ticket was created")); facts.append(F("F5", "COMMITS", "MENTIONED", "2 commit(s) at develop since the ticket was created mention KS-1, newest: abc1234 2026-11-01 fix"))
res.append(("LIKELY-FIXED citing only a CHANGED (file edited) fact refused", not ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F4"], "reason": "[F4] 5 commit(s) touched `c/d.ts`"})))
facts.append(F("F6", "COMMITS", "REFERENCED", "2 commit(s) at develop since the ticket was created only REFER to KS-1"))
res.append(("LIKELY-FIXED citing only a REFERENCED (Refs/prose mention) fact refused", not ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F6"], "reason": "[F6] 2 commit(s) refer to KS-1"})))
res.append(("LIKELY-FIXED citing a MENTIONED commit fact accepted", ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F5"], "reason": "[F5] 2 commit(s) mention KS-1, newest abc1234"})))
res.append(("LIKELY-FIXED citing the MISSING fact accepted", ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F1"], "reason": "[F1] `a/b.ts` does NOT exist"})))
res.append(("reason number not in FACTS refused", not ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F1"], "reason": "[F1] `a/b.ts` was removed 47 commits ago"})))
res.append(("duplicate of an open KS key that is not a candidate refused", not ok({"proposal": "POSSIBLE-DUPLICATE", "duplicate_of": "KS-1", "fact_ids": ["F3"], "reason": "[F3] KS-5"}, cands=set())))
res.append(("slash-joined symbol list whose parts are all in FACTS accepted", ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F1"], "reason": "[F1] `a/b.ts` missing, see develop/exist"})))
res.append(("invented path made of real parts (extension) still refused", not ok({"proposal": "LIKELY-FIXED", "fact_ids": ["F1"], "reason": "[F1] `c/b.ts` missing"})))
res.append(("duplicate key that is not an open ticket refused (reason silent on the key)", not ok({"proposal": "POSSIBLE-DUPLICATE", "duplicate_of": "KS-9999", "fact_ids": ["F3"], "reason": "[F3] same problem"})))
res.append(("duplicate of the ticket itself refused", not ok({"proposal": "POSSIBLE-DUPLICATE", "duplicate_of": "KS-1", "fact_ids": ["F3"], "reason": "[F3] KS-1"})))
res.append(("duplicate of an open candidate citing its fact accepted", ok({"proposal": "POSSIBLE-DUPLICATE-OF KS-5", "fact_ids": ["F3"], "reason": "[F3] open ticket KS-5 shares `c/d.ts`"})))
res.append(("unknown class refused", not ok({"proposal": "CLOSE-IT", "fact_ids": ["F1"], "reason": "[F1]"})))
res.append(("non-object reply refused", not ok("STILL-VALID")))
res.append(("CANNOT-TELL with a clean reason accepted", ok({"proposal": "CANNOT-TELL", "fact_ids": [], "reason": "no fact decides it"})))
bad = [n for n, v in res if not v]
for n, v in res: print(("ok   " if v else "FAIL ") + n)
sys.exit(1 if bad else 0)
EOF
rc=$?; n6="$(/usr/bin/grep -c '^ok' "$SCRATCH/arm6.out")"
[ $rc -eq 0 ] && pass "ARM 6 checker rules (17 unit red-proofs, each with its control)" "$n6/17 ok" || { fail "ARM 6 checker rules" "see $SCRATCH/arm6.out"; /usr/bin/grep '^FAIL' "$SCRATCH/arm6.out"; }
nm="$(/usr/bin/grep -c -i 'mutation' "$S/screen.py")"; nq="$(/usr/bin/grep -c 'query' "$S/screen.py")"
[ "$nm" = "0" ] && [ "$nq" -gt 0 ] && pass "ARM 7 no board write: screen.py contains no GraphQL mutation (control: $nq 'query' hits) and gql() asserts query-only" "mutation hits=$nm" || fail "ARM 7" "mutation hits=$nm query hits=$nq"

# ---- ARM L (optional, live): the deleted-file ticket against the REAL Spark. Waits for the box (one request at a time).
if [ "${ARMS_LIVE:-0}" = "1" ]; then
  OL="$SCRATCH/outL"; $PY -I "$S/screen.py" --keys KS-1 --wait 3600 --out "$OL" "${COMMON[@]}" "${NOSTATE[@]}" > "$SCRATCH/runL.log" 2>&1; rc=$?
  pl="$(col "$OL" KS-1 2)"
  case "$pl" in
    LIKELY-FIXED|CITATION-MOVED|CANNOT-TELL|REFUSED) pass "ARM L real Spark on the deleted-file ticket never reads STILL-VALID" "KS-1 -> $pl ($(col "$OL" KS-1 7)s): $(col "$OL" KS-1 3 | cut -c1-120)";;
    *) fail "ARM L" "KS-1 -> '$pl' rc=$rc: $(tail -c 300 "$SCRATCH/runL.log")";;
  esac
fi
echo; echo "ARMS: $PASSES passed, $FAILS failed (scratch: $SCRATCH)"
[ "$FAILS" -eq 0 ]
