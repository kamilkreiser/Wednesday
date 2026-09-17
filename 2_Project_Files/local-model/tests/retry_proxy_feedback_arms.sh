#!/bin/bash
# retry_proxy_feedback_arms.sh — red-proof for night_run.sh's RETRY-ONCE feedback on an ascii_proxy site (2026-09-17,
# HARNESS_WIDEN_REPORT_2026-09-17.md "OWED" item 1). The checker matches a proxy site on `ascii_proxy.text`
# (tasks/code_patch/a3b_proxy.py); the OLD builder fed back `text_at_tip` (the em-dash line the model will not reproduce).
# NO MODEL IS RUN. Like retry_a3i_routing_arms.sh this CUTS THE RUNNER'S OWN LINES out of the runner file it is given
# (the VERDICT line, the trigger `if`, and the python builder between `<<'PYR'` and `PYR`) — no test seam was added to
# night_run.sh, and nothing is re-implemented here.
#   ARM 0  extraction: each unit found exactly once in NEW and OLD
#   ARM 1  KS-839 REAL r1 out.md + proxy input, real checker output (FAIL A3b :353 with the em-dash text):
#          NEW retries; missed_sites == [{line 353, text_at_tip = ascii_proxy.text, match_by}]; the em-dash site text
#          appears NOWHERE in retry_feedback (verdict + instruction carry the proxy text); the match-by clause once
#   ARM 1b the real MISPLACED checker output (proxy '-' line at the wrong line): same missed_sites + clause
#   ARM 2  plain ASCII sites, KS-1121 real A3b PARTIAL (no ascii_proxy): NEW retry_feedback == OLD, no match_by, no clause
#   ARM 3  OLD runner (the backup) on ARM 1's and ARM 1b's fixtures → the ARM 1 predicate FAILS (negative control)
#   ARM 4  mixed: proxy :353 + plain ASCII :354 missed in one FAIL line → 353 proxied + tagged, 354 unchanged and
#          identical to OLD's 354 entry, em-dash text absent, clause once
#   ARM 4b the proxy input but the verdict names ONLY the plain :354 → NEW retry_feedback == OLD (no clause, no tag)
# Usage: bash retry_proxy_feedback_arms.sh [new night_run.sh] [old night_run.sh]
#        (defaults: night/night_run.sh and night/night_run.sh.pre-0917-proxyretry; env RPF_SCRATCH).
# No rm: a previous scratch dir is MOVED aside. rc 0 only when every arm holds. Never reads an rc through a pipe.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
NEW="${1:-$LM/night/night_run.sh}"; OLD="${2:-$LM/night/night_run.sh.pre-0917-proxyretry}"
FX=$LM/tests/fixtures/retry_proxy_feedback
PINP=$LM/night/inputs/code_839proxy.json
D_RUN=$LM/runs/2026-09-16_ks1121-ornith35b-night
W="${RPF_SCRATCH:-/private/tmp/claude-501/night/proxyfix/arms}"
[ -d "$W" ] && mv "$W" "$W.prev-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$W"
PASS=0; FAIL=0
ok()  { echo "PASS: $1"; PASS=$((PASS+1)); }
bad() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
CLAUSE="A missed site with match_by=ascii_proxy.text is matched by that ASCII text"

for f in "$NEW" "$OLD" "$PINP" "$FX/ks839_r1_proxyinput_checker.out" "$FX/ks839_wrongline_misplaced_checker.out" "$D_RUN/checker.out" "$D_RUN/input.json"; do
  [ -s "$f" ] || { echo "FATAL: missing $f"; exit 2; }
done
echo "retry proxy feedback arms $(date '+%F %H:%M:%S') · new $NEW ($(shasum -a 256 "$NEW" | cut -c1-12)) · old $OLD ($(shasum -a 256 "$OLD" | cut -c1-12)) · proxy input ($(shasum -a 256 "$PINP" | cut -c1-12))"

# ---------------------------------------------------------------- extraction (the runner's own lines)
extract() { # $1 runner  $2 outdir
  local r="$1" o="$2"; mkdir -p "$o"
  local nv nt nb
  nv="$(/usr/bin/grep -c -F "VERDICT=\"\$(/usr/bin/grep -m1 '^RESULT:' \"\$RUN/checker.out\"" "$r")"
  nt="$(/usr/bin/grep -c -F 'if [ "${NIGHT_RETRY_ON_PARTIAL:-1}" = "1" ]' "$r")"
  nb="$(/usr/bin/grep -c -x -F "PYR" "$r")"
  if [ "$nv" != 1 ] || [ "$nt" != 1 ] || [ "$nb" != 1 ]; then echo "extract $r: verdict=$nv trigger=$nt PYR-end=$nb (each must be 1)"; return 1; fi
  {
    echo '#!/bin/bash'
    echo 'set -uo pipefail'
    echo 'RUN="$1"; crc=1'
    /usr/bin/grep -F "VERDICT=\"\$(/usr/bin/grep -m1 '^RESULT:' \"\$RUN/checker.out\"" "$r"
    echo 'printf "VERDICT=%s\n" "$VERDICT"'
    awk 'index($0, "if [ \"${NIGHT_RETRY_ON_PARTIAL:-1}\" = \"1\" ]") {on=1} on {print} on && /; then$/ {exit}' "$r"
    echo '  echo DECISION=RETRY'
    echo 'else'
    echo '  echo DECISION=NORETRY'
    echo 'fi'
  } > "$o/decide.sh"
  awk '/<<'"'"'PYR'"'"'$/ {on=1; next} on && /^PYR$/ {exit} on {print} ' "$r" > "$o/builder.py"
  [ -s "$o/builder.py" ] && bash -n "$o/decide.sh"
}
decide() { # $1 new|old  $2 run dir (holding checker.out)  $3 tag
  bash "$W/x_$1/decide.sh" "$2" > "$W/dec_$1_$3.out" 2>&1
  /usr/bin/grep -o 'DECISION=[A-Z]*' "$W/dec_$1_$3.out" | head -1
}
build() { # $1 new|old  $2 input  $3 dir holding checker.out  $4 tag -> $W/fb_$1_$4.json ; prints the rc
  python3 "$W/x_$1/builder.py" "$2" "$3/checker.out" "$W/fb_$1_$4.json" > "$W/fb_$1_$4.out" 2>&1
  echo $?
}
stage() { # $1 tag  $2 source checker.out -> $W/run_$1/checker.out (so no out.md.checker/ sits beside it)
  mkdir -p "$W/run_$1"; cp "$2" "$W/run_$1/checker.out"
}
# the ARM 1 predicate, one definition used for NEW (must say OK) and OLD (must NOT): prints OK or the reason
pred1() { # $1 feedback json  $2 input json  $3 expected missed lines (comma list)  $4 proxy line
  python3 - "$1" "$2" "$3" "$4" "$CLAUSE" <<'PYP'
import json, sys
fbp, inp, want, pline, clause = sys.argv[1:6]
f = json.load(open(fbp, encoding="utf-8"))["retry_feedback"]
d = json.load(open(inp, encoding="utf-8"))
site = next(s for s in d["defect_line"]["sites"] if str(s["line"]) == pline)
tip, proxy = site["text_at_tip"], site["ascii_proxy"]["text"]
assert not tip.isascii() and proxy.isascii(), "fixture: the proxy site must be non-ASCII at the tip and ASCII in proxy"
blob = json.dumps(f, ensure_ascii=False)
lines = [str(m["line"]) for m in f["missed_sites"]]
pm = [m for m in f["missed_sites"] if str(m["line"]) == pline]
if lines != want.split(","): print(f"missed lines {lines} != {want}"); sys.exit()
if pm != [{"line": int(pline), "text_at_tip": proxy, "match_by": "ascii_proxy.text"}]: print(f"proxy entry {pm!r}"); sys.exit()
if tip.strip() in blob: print("the em-dash site text is still in retry_feedback"); sys.exit()
if proxy.strip() not in f["verdict"] or proxy.strip() not in f["instruction"]: print("proxy text missing from verdict/instruction"); sys.exit()
if f["instruction"].count(clause) != 1: print(f"clause count {f['instruction'].count(clause)}"); sys.exit()
print("OK")
PYP
}

extract "$NEW" "$W/x_new" > "$W/extract_new.out" 2>&1; xn=$?
extract "$OLD" "$W/x_old" > "$W/extract_old.out" 2>&1; xo=$?
if [ "$xn" -ne 0 ] || [ "$xo" -ne 0 ]; then
  bad "ARM0 EXTRACT new rc=$xn old rc=$xo: $(cat "$W/extract_new.out" "$W/extract_old.out" | tr '\n' ' ')"
  echo "RESULT: $PASS passed, $FAIL failed (work dir kept: $W)"; exit 1
fi
ok "ARM0 extract: VERDICT line, trigger if, PYR builder found exactly once in both (new builder $(wc -l < "$W/x_new/builder.py" | tr -d ' ') lines, old $(wc -l < "$W/x_old/builder.py" | tr -d ' '))"

# ---------------------------------------------------------------- ARM 1  (real KS-839 r1 + proxy input)
stage a1 "$FX/ks839_r1_proxyinput_checker.out"
if /usr/bin/grep -q '^FAIL A3b PARTIAL FIX .*:353 `' "$W/run_a1/checker.out"; then
  DN="$(decide new "$W/run_a1" a1)"
  if [ "$DN" = "DECISION=RETRY" ]; then ok "ARM1a NEW retries on the real FAIL A3b :353"; else bad "ARM1a decision '$DN'"; fi
  brc="$(build new "$PINP" "$W/run_a1" a1)"
  if [ "$brc" = 0 ]; then
    P="$(pred1 "$W/fb_new_a1.json" "$PINP" 353 353 2>&1)"
    if [ "$P" = "OK" ]; then ok "ARM1b NEW: missed_sites = [353 ascii_proxy.text, match_by]; em-dash text absent from retry_feedback; proxy text in verdict + instruction; clause once ($(tail -1 "$W/fb_new_a1.out"))"; else bad "ARM1b NEW predicate: $P"; fi
  else bad "ARM1b NEW builder rc=$brc: $(tail -3 "$W/fb_new_a1.out" | tr '\n' ' ')"; fi
else bad "ARM1 FIXTURE: no FAIL A3b :353 line in $FX/ks839_r1_proxyinput_checker.out"; fi

stage a1m "$FX/ks839_wrongline_misplaced_checker.out"
if /usr/bin/grep -q 'ascii_proxy MISPLACED' "$W/run_a1m/checker.out"; then
  DN="$(decide new "$W/run_a1m" a1m)"; brc="$(build new "$PINP" "$W/run_a1m" a1m)"
  P="$(pred1 "$W/fb_new_a1m.json" "$PINP" 353 353 2>&1)"
  if [ "$DN" = "DECISION=RETRY" ] && [ "$brc" = 0 ] && [ "$P" = "OK" ]; then ok "ARM1c NEW on the real MISPLACED output: retry, same proxy entry + clause"; else bad "ARM1c decision=$DN rc=$brc predicate=$P"; fi
else bad "ARM1c FIXTURE: no MISPLACED line"; fi

# ---------------------------------------------------------------- ARM 2  (plain ASCII sites, KS-1121 real)
stage a2 "$D_RUN/checker.out"
brc="$(build new "$D_RUN/input.json" "$W/run_a2" a2)"; orc="$(build old "$D_RUN/input.json" "$W/run_a2" a2)"
EQ="$(python3 -c "
import json,sys
a=json.load(open(sys.argv[1]))['retry_feedback']; b=json.load(open(sys.argv[2]))['retry_feedback']
print(a==b, len(a['missed_sites']), any('match_by' in m for m in a['missed_sites']), sys.argv[3] in a['instruction'], all(m['text_at_tip'].isascii() for m in a['missed_sites']))
" "$W/fb_new_a2.json" "$W/fb_old_a2.json" "$CLAUSE" 2>&1)"
case "$brc/$orc/$EQ" in "0/0/True "[1-9]*" False False True") ok "ARM2 KS-1121 plain ASCII A3b PARTIAL: NEW retry_feedback == OLD, no match_by, no clause ($EQ)";; *) bad "ARM2 rc new=$brc old=$orc got '$EQ' (want 'True N False False True')";; esac

# ---------------------------------------------------------------- ARM 3  (OLD runner = negative control)
orc="$(build old "$PINP" "$W/run_a1" a1)"
P="$(pred1 "$W/fb_old_a1.json" "$PINP" 353 353 2>&1)"
if [ "$orc" = 0 ] && [ "$P" != "OK" ]; then ok "ARM3a OLD on ARM1's fixture FAILS the predicate (control): $P"; else bad "ARM3a OLD rc=$orc predicate '$P' (must not be OK)"; fi
orc="$(build old "$PINP" "$W/run_a1m" a1m)"
P="$(pred1 "$W/fb_old_a1m.json" "$PINP" 353 353 2>&1)"
if [ "$orc" = 0 ] && [ "$P" != "OK" ]; then ok "ARM3b OLD on the MISPLACED fixture FAILS the predicate (control): $P"; else bad "ARM3b OLD rc=$orc predicate '$P' (must not be OK)"; fi

# ---------------------------------------------------------------- ARM 4  (mixed: proxy :353 + plain :354)
python3 - "$PINP" "$FX/ks839_r1_proxyinput_checker.out" "$W" > "$W/synth4.out" 2>&1 <<'PYS'
import json, sys
inp, chk, w = sys.argv[1:4]
d = json.load(open(inp, encoding="utf-8"))
s353 = next(s for s in d["defect_line"]["sites"] if s["line"] == 353)
s354 = next(s for s in d["defect_line"]["sites"] if s["line"] == 354)
assert s354["text_at_tip"].isascii()
s354["must_change"] = True
json.dump(d, open(f"{w}/mixed_input.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
out = []
for ln in open(chk, encoding="utf-8").read().split("\n"):
    if ln.startswith("FAIL A3b PARTIAL FIX"):
        ln = ("FAIL A3b PARTIAL FIX — the product hunk leaves 2 of 2 named site(s) untouched: :353 `" + s353["text_at_tip"].strip()
              + "` · :354 `" + s354["text_at_tip"].strip() + "`")
    out.append(ln)
import os
for tag, keep in (("a4", None), ("a4b", 354)):
    os.makedirs(f"{w}/run_{tag}", exist_ok=True)
    body = out if keep is None else [("FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 2 named site(s) untouched: :354 `" + s354["text_at_tip"].strip() + "`") if l.startswith("FAIL A3b PARTIAL FIX") else l for l in out]
    open(f"{w}/run_{tag}/checker.out", "w", encoding="utf-8").write("\n".join(body))
print("synth ok")
PYS
if /usr/bin/grep -q '^synth ok$' "$W/synth4.out"; then
  DN="$(decide new "$W/run_a4" a4)"
  brc="$(build new "$W/mixed_input.json" "$W/run_a4" a4)"; orc="$(build old "$W/mixed_input.json" "$W/run_a4" a4)"
  P="$(pred1 "$W/fb_new_a4.json" "$W/mixed_input.json" 353,354 353 2>&1)"
  Q="$(python3 -c "
import json,sys
a=json.load(open(sys.argv[1]))['retry_feedback']; b=json.load(open(sys.argv[2]))['retry_feedback']; d=json.load(open(sys.argv[3]))
t354=next(s for s in d['defect_line']['sites'] if s['line']==354)['text_at_tip']
na=[m for m in a['missed_sites'] if m['line']==354]; nb=[m for m in b['missed_sites'] if m['line']==354]
print(na==nb==[{'line':354,'text_at_tip':t354}], t354.strip() in a['verdict'])
" "$W/fb_new_a4.json" "$W/fb_old_a4.json" "$W/mixed_input.json" 2>&1)"
  if [ "$DN" = "DECISION=RETRY" ] && [ "$brc" = 0 ] && [ "$orc" = 0 ] && [ "$P" = "OK" ] && [ "$Q" = "True True" ]; then
    ok "ARM4 mixed :353 proxy + :354 ASCII: 353 carries ascii_proxy.text + match_by, 354 == {line, tip text} and identical to OLD's entry, em-dash text absent, clause once"
  else bad "ARM4 decision=$DN rc new=$brc old=$orc predicate='$P' plain-354='$Q' (want OK / 'True True')"; fi
  brc="$(build new "$W/mixed_input.json" "$W/run_a4b" a4b)"; orc="$(build old "$W/mixed_input.json" "$W/run_a4b" a4b)"
  E="$(python3 -c "
import json,sys
a=json.load(open(sys.argv[1]))['retry_feedback']; b=json.load(open(sys.argv[2]))['retry_feedback']
print(a==b, [m['line'] for m in a['missed_sites']], sys.argv[3] in a['instruction'])
" "$W/fb_new_a4b.json" "$W/fb_old_a4b.json" "$CLAUSE" 2>&1)"
  if [ "$brc" = 0 ] && [ "$orc" = 0 ] && [ "$E" = "True [354] False" ]; then ok "ARM4b proxy input but only plain :354 missed: NEW retry_feedback == OLD, no clause ($E)"; else bad "ARM4b rc new=$brc old=$orc got '$E' (want 'True [354] False')"; fi
else bad "ARM4 synthesis: $(cat "$W/synth4.out")"; fi

echo "RESULT: $PASS passed, $FAIL failed (work dir: $W)"
[ "$FAIL" -eq 0 ]
