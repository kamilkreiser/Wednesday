#!/bin/bash
# reconcile_rulings_arms.sh — red-proof arms for tools/reconcile_rulings.py.
#
# WHY (2026-09-21, ledger w=2 measured 2026-09-20 19:4x): Kam ruled two cards in
# the form `Decision <id> note: <free text>`; the reconciler counted them in
# "taps found" and printed "to rule: 0" — a principal's ruling dropped without a
# line. These arms pin the fix: a note: tap is flagged LOUDLY and counted, a
# <key> tap still rules, an unknown id is named, and the other seat's card is
# skipped as out of scope (not flagged as this seat's). The NEGATIVE arm runs the
# pre-fix copy (reconcile_rulings.py.pre-0921-note) against the same fixtures and
# must FAIL the note check — that is the proof the arms discriminate.
#
# REPORT MODE ONLY. Fixtures live in a mktemp dir; the live store is never read
# (RECONCILE_DECISIONS / RECONCILE_CHAT point every run at the fixtures) and its
# sha is asserted unchanged at the end. bash 3.2: no declare -A, no timeout.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOL="$HERE/../tools/reconcile_rulings.py"
PREFIX="$HERE/../tools/reconcile_rulings.py.pre-0921-note"
LIVE="$HERE/../../0_Brain/dashboard/data/decisions.json"
LIVE_CHAT="$HERE/../../0_Brain/dashboard/data/chat_kam.json"
FX="$(mktemp -d "${TMPDIR:-/tmp}/reconcile_arms.XXXXXX")"
trap 'rm -rf "$FX"' EXIT

pass=0; fail=0
ok()   { pass=$((pass+1)); echo "PASS  $1"; }
bad()  { fail=$((fail+1)); echo "FAIL  $1"; echo "      expected: $2"; echo "      got:      $3"; }
# assert_has NAME FILE PATTERN — PASS when grep -F finds PATTERN in FILE
assert_has() { if grep -qF -- "$3" "$2"; then ok "$1"; else bad "$1" "line containing: $3" "$(cat "$2" | tr '\n' '|' | cut -c1-400)"; fi; }
# assert_not NAME FILE PATTERN — PASS when PATTERN is ABSENT from FILE
assert_not() { if grep -qF -- "$3" "$2"; then bad "$1" "NO line containing: $3" "$(grep -F -- "$3" "$2" | head -2 | tr '\n' '|')"; else ok "$1"; fi; }

# ---- fixtures ---------------------------------------------------------------
cat > "$FX/decisions.json" <<'EOF'
[
  {"id": "secuura-fx-note-card", "client_project": "Secuura/Blockchain", "status": "open",
   "title": "fixture secuura card", "bluf": "x",
   "options": [{"key": "a", "label": "A"}, {"key": "b", "label": "B"}],
   "recommended": "a", "default_action": "x"},
  {"id": "secuura-fx-key-card", "client_project": "Secuura/Blockchain", "status": "open",
   "title": "fixture secuura key card", "bluf": "x",
   "options": [{"key": "a", "label": "A"}, {"key": "b", "label": "B"}],
   "recommended": "a", "default_action": "x"},
  {"id": "nexusai-fx-datasec-card", "client_project": "Datasec/NexusAI", "status": "open",
   "title": "fixture datasec card", "bluf": "x",
   "options": [{"key": "a", "label": "A"}, {"key": "b", "label": "B"}],
   "recommended": "a", "default_action": "x"},
  {"id": "secuura-fx-closed-before", "client_project": "Secuura/Blockchain", "status": "withdrawn",
   "title": "closed AFTER the note (seat read it)", "bluf": "x", "options": [{"key": "a", "label": "A"}],
   "recommended": "a", "default_action": "x",
   "withdrawn_at": "2026-09-21T10:06:00.000000+10:00", "withdrawn_reason": "Kam, panel, verbatim: 'legacy'"},
  {"id": "secuura-fx-closed-after", "client_project": "Secuura/Blockchain", "status": "ruled",
   "title": "note arrived AFTER the close (nobody read it)", "bluf": "x", "options": [{"key": "a", "label": "A"}],
   "recommended": "a", "default_action": "x", "ruled_choice": "a", "ruled_ts": "2026-09-21T10:07:00.000000+10:00"}
]
EOF
cat > "$FX/chat_log.json" <<'EOF'
[
  {"role": "kam", "view": "wednesday", "ts": "2026-09-21T10:00:00+10:00",
   "text": "Decision secuura-fx-key-card: b — Option B (RECOMMENDED)"},
  {"role": "kam", "view": "wednesday", "ts": "2026-09-21T10:01:00+10:00",
   "text": "Decision secuura-fx-note-card note: remove the rule and make the fix"},
  {"role": "kam", "view": "tuesday", "ts": "2026-09-21T10:02:00+10:00",
   "text": "Decision nexusai-fx-datasec-card note: actioned.  remove card"},
  {"role": "kam", "view": "wednesday", "ts": "2026-09-21T10:03:00+10:00",
   "text": "Decision no-such-card-xyz: a — Option A"},
  {"role": "kam", "view": "wednesday", "ts": "2026-09-21T10:04:00+10:00",
   "text": "hello, not a tap"},
  {"role": "kam", "view": "wednesday", "ts": "2026-09-21T10:05:00+10:00",
   "text": "Decision secuura-fx-closed-before note: legacy"},
  {"role": "kam", "view": "wednesday", "ts": "2026-09-21T10:08:00+10:00",
   "text": "Decision secuura-fx-closed-after note: why not fix it completely now?"}
]
EOF
# note-only stream: the exact 09-20 shape (no <key> tap at all)
cat > "$FX/chat_note_only.json" <<'EOF'
[
  {"role": "kam", "view": "wednesday", "ts": "2026-09-20T19:42:44+10:00",
   "text": "Decision secuura-fx-note-card note: remove the rule and make the fix"}
]
EOF

sha_before="$(shasum "$LIVE" 2>/dev/null | cut -d' ' -f1)"
sha_chat_before="$(shasum "$LIVE_CHAT" 2>/dev/null | cut -d' ' -f1)"

run() { # run SEAT SCRIPT CHAT OUT — report mode, fixtures only
  WED_AGENT="$1" RECONCILE_DECISIONS="$FX/decisions.json" RECONCILE_CHAT="$3" \
    python3 "$2" > "$4" 2>&1; echo "$?" > "$4.rc"; }

# ---- arms: fixed script, Wednesday seat -------------------------------------
run wednesday "$TOOL" "$FX/chat_log.json" "$FX/wed.out"
assert_has "positive-control: script ran and printed a summary line"  "$FX/wed.out" "taps found: 6"
assert_has "regression: <key> tap still rules (WOULD RULE ... -> b)"    "$FX/wed.out" "WOULD RULE  secuura-fx-key-card -> b"
assert_has "note on KNOWN in-scope card is flagged LOUDLY, verbatim"     "$FX/wed.out" "UNPARSEABLE-KEY RULING — secuura-fx-note-card — remove the rule and make the fix"
assert_has "note is counted in the summary (notes: 1)"                  "$FX/wed.out" "notes: 1 (flagged, NOT applied)"
assert_has "note flag carries the ready withdraw command"               "$FX/wed.out" "withdraw secuura-fx-note-card \"remove the rule and make the fix\""
assert_has "note on the OTHER seat's card is SKIPPED as out of scope"   "$FX/wed.out" "SKIP  nexusai-fx-datasec-card -> note"
assert_not "... and NOT flagged as this seat's unparseable ruling"       "$FX/wed.out" "UNPARSEABLE-KEY RULING — nexusai-fx-datasec-card"
assert_has "unknown card id is reported (UNKNOWN CARD)"                 "$FX/wed.out" "UNKNOWN CARD"
assert_has "... naming the id"                                          "$FX/wed.out" "no-such-card-xyz"
assert_not "note OLDER than the card's close is silent (seat had it)"    "$FX/wed.out" "secuura-fx-closed-before"
assert_has "note NEWER than the card's close is reported, verbatim"      "$FX/wed.out" "secuura-fx-closed-after -> note"
assert_has "... with the wording that it was written after the close"   "$FX/wed.out" "this note is NEWER — 'why not fix it completely now?'"
assert_has "report mode changes nothing (trailer present)"              "$FX/wed.out" "report only — nothing was changed"
[ "$(cat "$FX/wed.out.rc")" = "0" ] && ok "exit 0 in report mode" || bad "exit 0 in report mode" "rc 0" "rc $(cat "$FX/wed.out.rc")"

# ---- arm: the exact 09-20 shape — note only, nothing else -------------------
run wednesday "$TOOL" "$FX/chat_note_only.json" "$FX/noteonly.out"
assert_not "note-only stream never reads 'to rule: 0 · notes: 0'"       "$FX/noteonly.out" "to rule: 0 · notes: 0"
assert_has "note-only stream: un-applied count visible in summary"      "$FX/noteonly.out" "to rule: 0 · notes: 1 (flagged, NOT applied)"
assert_has "note-only stream: trailer says a human is needed"           "$FX/noteonly.out" "nothing applied — 1 note ruling(s) above need a human"

# ---- arm: Tuesday seat sees the mirror image --------------------------------
run tuesday "$TOOL" "$FX/chat_log.json" "$FX/tue.out"
assert_has "tuesday seat: Datasec note is flagged, verbatim"            "$FX/tue.out" "UNPARSEABLE-KEY RULING — nexusai-fx-datasec-card — actioned. remove card"
assert_has "tuesday seat: Secuura note is out of scope"                 "$FX/tue.out" "SKIP  secuura-fx-note-card -> note"

# ---- NEGATIVE arm: the pre-fix copy must FAIL the note check ----------------
if [ ! -f "$PREFIX" ]; then
  bad "negative control: pre-fix copy present" "$PREFIX" "missing — the negative arm cannot run, so it cannot pass"
else
  # the pre-fix copy has no env override: point its two path constants at the
  # fixtures in a scratch COPY (the original is never edited)
  sed -e "s|^KAM_STREAM = .*|KAM_STREAM = Path('$FX/chat_log.json')|" \
      -e "s|^DECISIONS  = .*|DECISIONS  = Path('$FX/decisions.json')|" "$PREFIX" > "$FX/prefix.py"
  grep -q "^KAM_STREAM = Path('$FX" "$FX/prefix.py" && grep -q "^DECISIONS  = Path('$FX" "$FX/prefix.py" \
    || { bad "negative control: pre-fix copy rewired to fixtures" "both path lines rewritten" "$(grep -nE '^(KAM_STREAM|DECISIONS)' "$FX/prefix.py")"; }
  WED_AGENT=wednesday python3 "$FX/prefix.py" > "$FX/pre.out" 2>&1
  assert_has "negative control: pre-fix copy still parses the <key> tap"  "$FX/pre.out" "WOULD RULE  secuura-fx-key-card -> b"
  if grep -qF "UNPARSEABLE-KEY RULING" "$FX/pre.out"; then
    bad "negative: pre-fix copy DROPS the note (proves the arm discriminates)" "no UNPARSEABLE-KEY line from the old parser" "$(grep -F 'UNPARSEABLE-KEY' "$FX/pre.out" | head -1)"
  else
    ok "negative: pre-fix copy DROPS the note (proves the arm discriminates) — old summary: $(head -1 "$FX/pre.out")"
  fi
fi

# ---- guard: the live store was never touched --------------------------------
sha_after="$(shasum "$LIVE" 2>/dev/null | cut -d' ' -f1)"
sha_chat_after="$(shasum "$LIVE_CHAT" 2>/dev/null | cut -d' ' -f1)"
[ "$sha_before" = "$sha_after" ] && ok "guard: live decisions.json unchanged" || bad "guard: live decisions.json unchanged" "$sha_before" "$sha_after"
[ "$sha_chat_before" = "$sha_chat_after" ] && ok "guard: live chat_kam.json unchanged" || bad "guard: live chat_kam.json unchanged" "$sha_chat_before" "$sha_chat_after"

echo "----"
echo "reconcile_rulings_arms: $pass PASS, $fail FAIL"
[ "$fail" -eq 0 ]
