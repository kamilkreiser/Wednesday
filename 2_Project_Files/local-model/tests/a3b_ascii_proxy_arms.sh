#!/bin/bash
# a3b_ascii_proxy_arms.sh — red-proof for the ASCII_PROXY line-keyed '-' site (2026-09-17 15:5x): night/build_input.sh parses
# `ascii_proxy U+XXXX=<ascii>` on a line-keyed must_change bullet; tasks/code_patch/checker.sh runs a3b_proxy.py BEFORE A2
# to restore the tip's real bytes where the model's '-' line equals the declared proxy text AND its hunk places it at the
# site's number; a3b_line.py compares the brief's quote in proxy form. Every checker arm runs the REAL checker end to end
# (sandbox-exec, off-host outbound denied) in a scratch clone at d7e95cd9f and reads its PASS/FAIL/RESULT lines.
#
# Fixture: KS-839, services/auth/src/services/oauth.ts:353 `  if (allowed.includes('*')) return requested; // Wildcard — all scopes`
# (one U+2014), proxy `... // Wildcard -- all scopes`. Input: night/inputs/code_839proxy.json (brief night/briefs/KS-839-proxy.md).
#
#   R1 NEW, KS-839's REAL r1 out.md (keeps :353 as context, deletes :354) + the proxy input   → FAIL A3b naming :353, stopped at A3b
#   R1b NEW, the same REAL out.md + its ORIGINAL (text-keyed) input                             → PASS/FAIL/RESULT lines IDENTICAL to the night run
#   R1c NEW, the REAL retry out.md + the proxy input                                            → FAIL A3b naming :353
#   R2 NEW, a proxy '-' line at the WRONG line (:353 kept as context, the proxy where :354 is)  → FAIL A3b ... ascii_proxy MISPLACED, no A2 line
#   R3 NEW, the golden with ONE other character changed in the proxy line (requested -> requestes) → FAIL A3b ... TEXTMISMATCH
#   R3b NEW, the golden with a single hyphen for the declared `--`                              → FAIL A3b ... TEXTMISMATCH
#   G  NEW, the golden (proxy at :353, the brief's test)                                        → A3b ascii_proxy SUBSTITUTED :353, strict, RESULT: PASS (7/7)
#   G0 OLD checker (.pre-0917-widen) on the golden                                              → FAIL A2 (negative control: the stand-in never applies)
#   G2 NEW, the golden with the REAL em dash in its '-' line (the model reproduced it)          → NOPROXYLINE, RESULT: PASS (7/7)
#   HX helper only (no vitest): header drifted to -300 with true context → SUBSTITUTED :353 · stale ascii_proxy.text → rc 2 ·
#      a legacy input → `PROXY none` rc 0 and the section file unchanged
#   B  builder (Linear read + git show on the source; skip with PROXY_SKIP_BUILDER=1):
#      B1 NEW + the proxy brief → rc 0, output byte-identical to night/inputs/code_839proxy.json
#      B2 the brief quoting the REAL em-dash line with ascii_proxy → rc 2 REFUSED (quote is not the proxy form)
#      B3 the quote one character off → rc 2 · B4 ascii_proxy under a NON-line-keyed Where → rc 2 · B5 ascii_proxy on a stays
#      site → rc 2 · B6 a declared character absent from the line (U+2013) → rc 2 · B7 `ascii_proxy` with no pair → rc 2
#      B8 a non-ASCII '+' line in the brief's fence → rc 2
#      B0 OLD builder (.pre-0917-widen2) + the proxy brief → rc 2 (negative control: the quote never matched the tip)
#
# Usage: bash a3b_ascii_proxy_arms.sh   (env: PROXY_CHECKER, PROXY_OLD_CHECKER, PROXY_BUILDER, PROXY_OLD_BUILDER, PROXY_INPUT,
#        PROXY_BRIEF, PROXY_CLONE, PROXY_SCRATCH, PROXY_SKIP_BUILDER). rc 0 only when every arm holds. No rm: a previous
#        scratch dir is MOVED aside. Never reads an rc through a pipe.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CK="${PROXY_CHECKER:-$LM/tasks/code_patch/checker.sh}"
OLD="${PROXY_OLD_CHECKER:-$LM/tasks/code_patch/checker.sh.pre-0917-widen}"
PXPY="$(dirname "$CK")/a3b_proxy.py"
BI="${PROXY_BUILDER:-$LM/night/build_input.sh}"
OLDBI="${PROXY_OLD_BUILDER:-$LM/night/build_input.sh.pre-0917-widen2}"
INP="${PROXY_INPUT:-$LM/night/inputs/code_839proxy.json}"
BRIEF="${PROXY_BRIEF:-$LM/night/briefs/KS-839-proxy.md}"
SB=$LM/tests/fixtures/a3b_line/nonet.sb
CLONE="${PROXY_CLONE:-/private/tmp/claude-501/night/a3bline_0917/clone}"
SP="${PROXY_SCRATCH:-/private/tmp/claude-501/night/widen_0917/proxy_arms}"
R839=$LM/runs/2026-09-17_ks839-ornith35b-night
PROD=Blockchain/Dev/services/auth/src/services/oauth.ts
[ -d "$SP" ] && mv "$SP" "$SP.prev-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SP"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
has(){ /usr/bin/grep -q -E "$2" "$1"; }
for f in "$CK" "$OLD" "$PXPY" "$INP" "$BRIEF" "$SB" "$R839/out.md" "$R839/input.json" "$R839/checker.out" "$R839/retry/out.md"; do
  [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }
done
[ "$(git -C "$CLONE" rev-parse HEAD)" = d7e95cd9f153e9036ed77935a73c93504fa6e3dc ] || { echo "FATAL: $CLONE is not at d7e95cd9f"; exit 2; }
echo "a3b ascii_proxy arms $(date '+%F %H:%M:%S') · checker $CK ($(shasum -a 256 "$CK" | cut -c1-12)) · old $OLD ($(shasum -a 256 "$OLD" | cut -c1-12)) · helper ($(shasum -a 256 "$PXPY" | cut -c1-12)) · input ($(shasum -a 256 "$INP" | cut -c1-12))"

# ---- fixtures: outs built from the brief's own fence + the tip's lines 350-356
python3 - "$BRIEF" "$CLONE" "$SP" "$INP" "$R839/input.json" <<'PYFX'
import json, re, subprocess, sys
brief, clone, sp, inp, legacy_inp = sys.argv[1:6]
b = open(brief, encoding="utf-8").read()
test = re.search(r"```ts\n(.*?)```", b, re.S).group(1).rstrip("\n").split("\n")
assert len(test) == 52, len(test)
tpath = json.load(open(inp, encoding="utf-8"))["suggested_test_file"]
tip = subprocess.run(["git", "-C", clone, "show", "d7e95cd9f:Blockchain/Dev/services/auth/src/services/oauth.ts"], capture_output=True, text=True).stdout.split("\n")
T = tip[352]; P = T.replace("—", "--"); PLUS = "  if (allowed.includes('*')) return []; // KS-839: a wildcard grants nothing"
assert "—" in T and P.isascii()
H = ["--- a/Blockchain/Dev/services/auth/src/services/oauth.ts", "+++ b/Blockchain/Dev/services/auth/src/services/oauth.ts"]
ctx = lambda n: " " + tip[n - 1]
TS = ["--- /dev/null", "+++ b/" + tpath, "@@ -0,0 +1,52 @@"] + ["+" + l for l in test]
def out(name, prod):
    open(f"{sp}/{name}.md", "w", encoding="utf-8").write("```diff\n" + "\n".join(H + prod + TS) + "\n```\n")
golden = ["@@ -350,7 +350,7 @@", ctx(350), ctx(351), ctx(352), "-" + P, "+" + PLUS, ctx(354), ctx(355), ctx(356)]
out("golden", golden)
out("wrongline", ["@@ -350,7 +350,7 @@", ctx(350), ctx(351), ctx(352), ctx(353), "-" + P, "+" + PLUS, ctx(355), ctx(356)])
assert "return requested;" in P
out("onechar", [l if not l.startswith("-") else "-" + P.replace("return requested;", "return requestes;") for l in golden])
out("hyphen", [l if not l.startswith("-") else "-" + P.replace("--", "-") for l in golden])
out("realdash", [l if not l.startswith("-") else "-" + T for l in golden])
out("drift300", ["@@ -300,7 +300,7 @@"] + golden[1:])
# helper-only inputs
d = json.load(open(inp, encoding="utf-8"))
st = json.loads(json.dumps(d))
for s in st["defect_line"]["sites"]:
    if s.get("ascii_proxy"): s["ascii_proxy"]["text"] = s["ascii_proxy"]["text"].replace("all scopes", "all scope")
json.dump(st, open(f"{sp}/stale_input.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for name, prod in (("drift300", ["@@ -300,7 +300,7 @@"] + golden[1:]), ("golden", golden)):
    open(f"{sp}/sec_{name}.diff", "w", encoding="utf-8").write("\n".join(H + prod) + "\n")
    json.dump([{"n": 1, "path": "Blockchain/Dev/services/auth/src/services/oauth.ts", "file": f"{sp}/sec_{name}.diff"}], open(f"{sp}/sec_{name}.json", "w"))
print("fixtures written")
PYFX
[ -f "$SP/golden.md" ] && [ -f "$SP/sec_golden.json" ] || { echo "FATAL: fixture generation failed"; exit 2; }

run_ck(){ # run_ck <label> <checker> <input.json> <out.md> — runs into $SP/<label>/, sets RC and CO
  local d="$SP/$1"; mkdir -p "$d"; cp "$4" "$d/out.md"
  echo "  .. $1 start $(date +%H:%M:%S)"
  sandbox-exec -f "$SB" bash "$2" "$3" "$d/out.md" "$CLONE" > "$d/checker.out" 2>&1
  RC=$?; CO="$d/checker.out"
  echo "  .. $1 end $(date +%H:%M:%S) rc=$RC :: $(/usr/bin/grep -E '^(A3b ascii_proxy|PASS A2|FAIL A2|PASS A3b|FAIL A3b|RESULT|SUMMARY)' "$CO" | cut -c1-260 | tr '\n' '|')"
}

echo "--- helper only (no vitest)"
cp "$SP/sec_drift300.diff" "$SP/sec_drift300.orig"
python3 "$PXPY" "$INP" "$CLONE" "$SP/sec_drift300.json" "$PROD" Blockchain/Dev > "$SP/hx_drift.out" 2>&1; rc=$?
if [ "$rc" -eq 0 ] && has "$SP/hx_drift.out" '^SUBSTITUTED :353 ' && cmp -s "$SP/sec_drift300.orig" "$SP/sec_drift300.diff.model.diff" && python3 -c 'import sys; t=open(sys.argv[1],encoding="utf-8").read(); sys.exit(0 if "-  if (allowed.includes(\x27*\x27)) return requested; // Wildcard — all scopes\n" in t and "-- all scopes" not in t else 1)' "$SP/sec_drift300.diff"; then
  ok "HX1 header drifted to -300, context true → SUBSTITUTED :353 (the header is not the placement); the section now carries the tip's em-dash line; model section kept as .model.diff"
else bad "HX1" "rc=$rc $(tr '\n' '|' < "$SP/hx_drift.out")"; fi
python3 "$PXPY" "$SP/stale_input.json" "$CLONE" "$SP/sec_golden.json" "$PROD" Blockchain/Dev > "$SP/hx_stale.out" 2>&1; rc=$?
if [ "$rc" -eq 2 ] && has "$SP/hx_stale.out" '^MEASURE ERROR: site :353: ascii_proxy.text is not the tip line'; then ok "HX2 stale ascii_proxy.text → rc 2 MEASURE ERROR (never substitutes on an input that disagrees with the tip)"; else bad "HX2" "rc=$rc $(tr '\n' '|' < "$SP/hx_stale.out")"; fi
cp "$SP/sec_golden.diff" "$SP/sec_golden.orig"
python3 "$PXPY" "$R839/input.json" "$CLONE" "$SP/sec_golden.json" "$PROD" Blockchain/Dev > "$SP/hx_legacy.out" 2>&1; rc=$?
if [ "$rc" -eq 0 ] && has "$SP/hx_legacy.out" '^PROXY none$' && cmp -s "$SP/sec_golden.orig" "$SP/sec_golden.diff" && [ ! -f "$SP/sec_golden.diff.model.diff" ]; then ok "HX3 legacy input (no ascii_proxy) → PROXY none, rc 0, section untouched"; else bad "HX3" "rc=$rc $(tr '\n' '|' < "$SP/hx_legacy.out")"; fi

echo "--- red arms (real checker)"
run_ck R1_new_real839 "$CK" "$INP" "$R839/out.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 1 named site\(s\) untouched: :353 `' && has "$CO" '^RESULT: FAIL .*stopped at A3b' && ! has "$CO" '^PASS A3b' && ! has "$CO" '^A3b ascii_proxy: .*SUBSTITUTED'; then
  ok "R1 KS-839's REAL r1 out.md (deletes :354) + proxy input → FAIL A3b naming :353, nothing substituted, stopped at A3b"
else bad "R1" "rc=$RC $(/usr/bin/grep -E '^(A3b|PASS A3b|FAIL|RESULT)' "$CO" | head -4 | tr '\n' '|')"; fi
run_ck R1b_new_real839_legacy "$CK" "$R839/input.json" "$R839/out.md"
/usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$R839/checker.out" > "$SP/R1b.expected"; /usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$CO" > "$SP/R1b.got"
if cmp -s "$SP/R1b.expected" "$SP/R1b.got" && [ -s "$SP/R1b.got" ] && ! has "$CO" 'ascii_proxy'; then ok "R1b the same REAL out.md + its ORIGINAL text-keyed input → $(wc -l < "$SP/R1b.got" | tr -d ' ') PASS/FAIL/RESULT lines identical to the 14:17 night run; no ascii_proxy line printed"; else bad "R1b" "$(diff "$SP/R1b.expected" "$SP/R1b.got" | head -6 | tr '\n' '|')"; fi
run_ck R1c_new_retry839 "$CK" "$INP" "$R839/retry/out.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b PARTIAL FIX .*:353 `' && has "$CO" '^RESULT: FAIL .*stopped at A3b' && ! has "$CO" 'SUBSTITUTED'; then ok "R1c KS-839's REAL retry out.md + proxy input → FAIL A3b naming :353"; else bad "R1c" "rc=$RC $(/usr/bin/grep -E '^(A3b|PASS A3b|FAIL|RESULT)' "$CO" | head -4 | tr '\n' '|')"; fi
run_ck R2_new_wrongline "$CK" "$INP" "$SP/wrongline.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 1 named site\(s\) untouched: :353 `if \(allowed.includes\(.\*.\)\) return requested; // Wildcard -- all scopes` ascii_proxy MISPLACED ' && has "$CO" '^RESULT: FAIL .*stopped at A3b' && ! has "$CO" '^(PASS|FAIL) A2'; then
  ok "R2 proxy '-' line at the WRONG line (:353 kept as context, the proxy where :354 is) → FAIL A3b … ascii_proxy MISPLACED, before A2"
else bad "R2" "rc=$RC $(/usr/bin/grep -E '^(A3b|PASS A2|FAIL A2|PASS A3b|FAIL|RESULT)' "$CO" | head -4 | tr '\n' '|')"; fi
run_ck R3_new_onechar "$CK" "$INP" "$SP/onechar.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b PARTIAL FIX .*:353 `.*` ascii_proxy TEXTMISMATCH .*return requestes; // Wildcard -- all scopes' && has "$CO" '^RESULT: FAIL .*stopped at A3b' && ! has "$CO" '^(PASS|FAIL) A2'; then
  ok "R3 proxy line with ONE other character changed (requested -> requestes) → FAIL A3b … ascii_proxy TEXTMISMATCH"
else bad "R3" "rc=$RC $(/usr/bin/grep -E '^(A3b|PASS A2|FAIL A2|FAIL|RESULT)' "$CO" | head -4 | tr '\n' '|')"; fi
run_ck R3b_new_hyphen "$CK" "$INP" "$SP/hyphen.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b PARTIAL FIX .*:353 `.*` ascii_proxy TEXTMISMATCH .*// Wildcard - all scopes' && has "$CO" '^RESULT: FAIL .*stopped at A3b'; then
  ok "R3b a single hyphen for the declared \`--\` → FAIL A3b … ascii_proxy TEXTMISMATCH"
else bad "R3b" "rc=$RC $(/usr/bin/grep -E '^(A3b|PASS A2|FAIL A2|FAIL|RESULT)' "$CO" | head -4 | tr '\n' '|')"; fi

echo "--- green arms"
run_ck G_new_golden "$CK" "$INP" "$SP/golden.md"
if [ "$RC" -eq 0 ] && has "$CO" '^A3b ascii_proxy: 1 site\(s\) declared \(rc=0\): SUBSTITUTED :353 ' && has "$CO" '^PASS A2 diff applies at the tip \(strict' && has "$CO" '^A3b line-keyed: 3 site\(s\) .*REMOVED_LINES 353$' && has "$CO" '^PASS A3b ' && has "$CO" '^A3i: ' && has "$CO" '^RESULT: PASS \(7/7\)' && has "$CO" 'apply_mode=strict'; then
  ok "G  golden (proxy '-' line at :353) → SUBSTITUTED :353, A2 strict, REMOVED_LINES 353, A3i byte-exact, RESULT: PASS (7/7)"
else bad "G" "rc=$RC $(/usr/bin/grep -E '^(A3b|PASS|FAIL|RESULT)' "$CO" | cut -c1-160 | head -12 | tr '\n' '|')"; fi
run_ck G0_old_golden "$OLD" "$INP" "$SP/golden.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A2 diff does NOT apply' && ! has "$CO" 'ascii_proxy'; then ok "G0 OLD checker on the same golden → FAIL A2 (negative control: without the restore the stand-in line applies nowhere)"; else bad "G0" "rc=$RC $(/usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$CO" | head -4 | cut -c1-160 | tr '\n' '|')"; fi
run_ck G2_new_realdash "$CK" "$INP" "$SP/realdash.md"
if [ "$RC" -eq 0 ] && has "$CO" '^A3b ascii_proxy: 1 site\(s\) declared \(rc=0\): NOPROXYLINE ' && has "$CO" '^RESULT: PASS \(7/7\)'; then ok "G2 the golden with the REAL em dash in its '-' line → NOPROXYLINE (nothing substituted), RESULT: PASS (7/7)"; else bad "G2" "rc=$RC $(/usr/bin/grep -E '^(A3b|PASS A2|FAIL|RESULT)' "$CO" | head -4 | cut -c1-160 | tr '\n' '|')"; fi

if [ "${PROXY_SKIP_BUILDER:-0}" = 1 ]; then
  echo "--- (builder arms B skipped: PROXY_SKIP_BUILDER=1)"
else
  echo "--- builder (Linear read + git show on the source; writes only under $SP)"
  PINS="product=Blockchain/Dev/services/auth/src/services/oauth.ts ref=services/auth/src/__tests__/ks466-oauth-tenant-guc.test.ts line=353 ctx=65536"
  mkb(){ # mkb <label> <python expr transforming t> — writes $SP/<label>/KS-839-proxy.md
    mkdir -p "$SP/$1"; python3 -c 'import sys; t=open(sys.argv[1],encoding="utf-8").read(); exec("t2="+sys.argv[2]); assert t2!=t or sys.argv[2]=="t", "variant did not change"; open(sys.argv[3],"w",encoding="utf-8").write(t2)' "$BRIEF" "$2" "$SP/$1/KS-839-proxy.md"
  }
  runbi(){ # runbi <label> <builder>
    # shellcheck disable=SC2086
    NIGHT_BRIEFS_DIR="$SP/$1" bash "$2" KS-839-proxy "$SP/$1/input.json" $PINS > "$SP/$1/build.out" 2>&1; RC=$?
    echo "  .. $1 rc=$RC :: $(/usr/bin/grep -E '^(build_input: REFUSED|wrote |  ascii_proxy site)' "$SP/$1/build.out" | cut -c1-260 | tr '\n' '|')"
  }
  refused(){ [ "$RC" -eq 2 ] && has "$SP/$1/build.out" "^build_input: REFUSED KS-839-proxy — $2" && [ ! -f "$SP/$1/input.json" ]; }
  # every variant edits the BULLET (the intro paragraph also names `ascii_proxy U+2014=--`); the fixture asserts it changed
  [ "$(/usr/bin/grep -c -F '(EDIT 1).** ascii_proxy U+2014=--' "$BRIEF")" = 1 ] || bad "B-fixture" "the proxy bullet is not exactly once in $BRIEF"
  mkb B1 't'; runbi B1 "$BI"
  if [ "$RC" -eq 0 ] && cmp -s "$SP/B1/input.json" "$INP"; then ok "B1 NEW builder + the proxy brief → rc 0, output byte-identical to $(basename "$INP")"; else bad "B1" "rc=$RC cmp=$(cmp "$SP/B1/input.json" "$INP" 2>&1 | head -1)"; fi
  mkb B2 't.replace("**`  if (allowed.includes(\x27*\x27)) return requested; // Wildcard -- all scopes`", "**`  if (allowed.includes(\x27*\x27)) return requested; // Wildcard — all scopes`", 1)'; runbi B2 "$BI"
  if refused B2 "line-keyed \`## Where\`: :353 — the brief quotes .* after its ascii_proxy substitution"; then ok "B2 the Where quote is the REAL em-dash line (not the proxy form) → rc 2 REFUSED"; else bad "B2" "rc=$RC $(tail -1 "$SP/B2/build.out")"; fi
  mkb B3 't.replace("**`  if (allowed.includes(\x27*\x27)) return requested; // Wildcard -- all scopes`", "**`  if (allowed.includes(\x27*\x27)) return requestes; // Wildcard -- all scopes`", 1)'; runbi B3 "$BI"
  if refused B3 "line-keyed \`## Where\`: :353 — the brief quotes .*requestes"; then ok "B3 the quote one character off → rc 2 REFUSED"; else bad "B3" "rc=$RC $(tail -1 "$SP/B3/build.out")"; fi
  mkb B4 't.replace("## Where (line-keyed - every", "## Where (every", 1)'; runbi B4 "$BI"
  if refused B4 '`## Where` :353 declares ascii_proxy but the Where heading is not line-keyed'; then ok "B4 ascii_proxy under a NON-line-keyed Where → rc 2 REFUSED"; else bad "B4" "rc=$RC $(tail -1 "$SP/B4/build.out")"; fi
  mkb B5 't.replace("- the named-scope filter. Stays.", "- the named-scope filter. Stays. ascii_proxy U+2014=--", 1)'; runbi B5 "$BI"
  if refused B5 "line-keyed \`## Where\` :354: ascii_proxy U\\+2014 does not occur|line-keyed \`## Where\` :354: ascii_proxy on a site that STAYS"; then ok "B5 ascii_proxy on the STAYS site :354 → rc 2 REFUSED ($(/usr/bin/grep -m1 'REFUSED' "$SP/B5/build.out" | cut -c38-150))"; else bad "B5" "rc=$RC $(tail -1 "$SP/B5/build.out")"; fi
  mkb B6 't.replace("(EDIT 1).** ascii_proxy U+2014=--", "(EDIT 1).** ascii_proxy U+2014=-- U+2013=-", 1)'; runbi B6 "$BI"
  if refused B6 "line-keyed \`## Where\` :353: ascii_proxy U\\+2013 does not occur in the tip's line 353"; then ok "B6 a declared character absent from the line (U+2013) → rc 2 REFUSED"; else bad "B6" "rc=$RC $(tail -1 "$SP/B6/build.out")"; fi
  mkb B7 't.replace("(EDIT 1).** ascii_proxy U+2014=--", "(EDIT 1).** ascii_proxy", 1)'; runbi B7 "$BI"
  if refused B7 '`## Where` :353: `ascii_proxy` must be followed by one or more'; then ok "B7 \`ascii_proxy\` with no U+XXXX pair → rc 2 REFUSED"; else bad "B7" "rc=$RC $(tail -1 "$SP/B7/build.out")"; fi
  mkb B8 't.replace("+  if (allowed.includes(\x27*\x27)) return []; // KS-839: a wildcard grants nothing", "+  if (allowed.includes(\x27*\x27)) return []; // KS-839: a wildcard grants nothing \u2014 ever", 1)'; runbi B8 "$BI"
  if refused B8 "an ascii_proxy brief's '\\+' lines must be ASCII"; then ok "B8 a NON-ASCII '+' line in an ascii_proxy brief → rc 2 REFUSED (nothing restores a '+' line; A3c/A3i see only ASCII)"; else bad "B8" "rc=$RC $(tail -1 "$SP/B8/build.out")"; fi
  mkb B0 't'; runbi B0 "$OLDBI"
  if refused B0 "line-keyed \`## Where\`: :353 — the brief quotes"; then ok "B0 OLD builder + the proxy brief → rc 2 REFUSED (negative control: the proxy quote is not the tip line)"; else bad "B0" "rc=$RC $(tail -1 "$SP/B0/build.out")"; fi
fi

echo "a3b ascii_proxy arms: $pass passed, $fail failed ($(date +%H:%M:%S))"
[ "$fail" -eq 0 ]
