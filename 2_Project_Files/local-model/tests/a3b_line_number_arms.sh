#!/bin/bash
# a3b_line_number_arms.sh — red-proof for code_patch checker A3b/A3e LINE-KEYED sites (2026-09-17, KS-1186) and the
# build_input.sh `## Where (line-keyed …)` opt-in that feeds them. Every checker arm runs the REAL checker.sh end to end
# (sandbox-exec, off-host outbound denied) in a scratch clone and reads its PASS/FAIL/RESULT lines; nothing is re-implemented.
#
# Fixture: KS-1186, `services/auth/src/repositories/userRepo.ts` at develop d7e95cd9f — :446 :512 :585 :627 are the SAME
# text (`if (result.rows.length > 0) return fromRow(result.rows[0]);`), :594 is unique. A TEXT match is satisfied by
# any one duplicate; the line-keyed grade is not.
#
#   A  (a) negative control: the OLD checker (.pre-0917-a3bline) on a WRONG-SITE diff (edits :512 + :585; the input's
#          must_change sites are :446 + :512)                                        → PASS A3b  (it cannot see it)
#   A2 (a) the OLD checker on the KS-1186 input with the :627 hunk dropped             → PASS A3b  (4 duplicates' text present)
#   B  (b) NEW checker, the KS-1186 line-keyed input + golden (5 hunks + test)         → PASS A3b (5 line-keyed) + RESULT PASS (7/7)
#   C  (c) NEW checker, the wrong-site diff of arm A                                   → FAIL A3b naming :446 (not :512), stopped at A3b
#   C2 (c) NEW checker, the KS-1186 input with the :627 hunk dropped                   → FAIL A3b naming :627 only
#   D1 (d) legacy text-keyed input KS-744 (code_744.json, 2 must_change) + its proven out.md → PASS/FAIL/RESULT lines
#          IDENTICAL to the 12:05 fin2 checker.out (made by the old checker)
#   D2 (d) legacy KS-1199 (code_1199.json, test-only, held) + its night run out.md at fa887f382 → lines IDENTICAL to that run's checker.out
#   D3 (d) census: the OLD and NEW PY3B/PY3E text predicates (extracted by marker) on every run under runs/ with an
#          input.json + a product section → identical output on every one (and >= 1 non-empty, so it is not vacuous)
#   E  (e) NEW checker, the KS-1186 input with site :512 renumbered :513 (the text kept) → FAIL A3b SITE TEXT MISMATCH naming
#          :513, no PASS A3b, and the RESULT line does NOT say "stopped at A3b" (RETRY-ONCE must not fire on a brief defect)
#   E0 (e) negative control: the OLD checker on the same input                        → PASS A3b (a silent pass)
#   F  A3e: sites :446 must_change + :512 (correct) stays — the SAME text; diff edits :446 only
#          NEW → PASS A3b and no FAIL A3e ·  F0 OLD → FAIL A3e (the row-411 defect: a stays line identical to a '-' line)
#   G  A3e: the same sites; diff edits :446 AND :512                                   → NEW FAIL A3e naming :512
#   I  NEW checker, hunk 1 header drifted to -500 + hunk 2 miscounted → A2 lenient (--recount); REMOVED_LINES still the five
#   J  NEW checker, one-site input, hunk 1 with context the file lacks → A2 REANCHORED; REMOVED_LINES 446, PASS A3b
#   H  builder (needs Linear read + git show on the source; skip with A3BL_SKIP_BUILDER=1):
#      H1 NEW builder + the line-keyed brief → 7 sites, all key=line+text, text_in_brief == text_at_tip
#      H2 NEW builder + the same brief with the :512 bullet renumbered :513 → rc 2, REFUSED naming :513
#      H3 NEW builder + the brief with `line-keyed` removed from the Where heading → 7 sites, NONE keyed (legacy shape)
#      H0 OLD builder + the line-keyed brief → NONE keyed (negative control: the opt-in did not exist)
#
# Usage: bash a3b_line_number_arms.sh   (env: A3BL_CHECKER, A3BL_OLD_CHECKER, A3BL_BUILDER, A3BL_OLD_BUILDER,
#        A3BL_CLONE (d7e95cd9f, prepared for services/auth + api-gateway), A3BL_CLONE_FA887, A3BL_SCRATCH, A3BL_SKIP_BUILDER)
# rc 0 only when every arm holds. Never reads an rc through a pipe. No rm: a previous scratch dir is MOVED aside.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CK="${A3BL_CHECKER:-$LM/tasks/code_patch/checker.sh}"
OLD="${A3BL_OLD_CHECKER:-$LM/tasks/code_patch/checker.sh.pre-0917-a3bline}"
BI="${A3BL_BUILDER:-$LM/night/build_input.sh}"
OLDBI="${A3BL_OLD_BUILDER:-$LM/night/build_input.sh.pre-0917-a3bline}"
FX=$LM/tests/fixtures/a3b_line
CLONE="${A3BL_CLONE:-/private/tmp/claude-501/night/a3bline_0917/clone}"
CLONE_FA="${A3BL_CLONE_FA887:-/private/tmp/claude-501/night/a3bline_0917/clone_fa887}"
SP="${A3BL_SCRATCH:-/private/tmp/claude-501/night/a3bline_0917/arms}"
[ -d "$SP" ] && mv "$SP" "$SP.prev-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SP"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
for f in "$CK" "$OLD" "$FX/ks1186_linekeyed_input.json" "$FX/ks1186_product_golden.diff" "$FX/ks1186_test_golden.diff" "$FX/nonet.sb"; do
  [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }
done
[ "$(git -C "$CLONE" rev-parse HEAD)" = d7e95cd9f153e9036ed77935a73c93504fa6e3dc ] || { echo "FATAL: $CLONE is not at d7e95cd9f"; exit 2; }
echo "a3b line-number arms $(date '+%F %H:%M:%S') · checker $CK ($(shasum -a 256 "$CK" | cut -c1-12)) · old $OLD ($(shasum -a 256 "$OLD" | cut -c1-12))"

# ---- fixtures: variant inputs and outs, generated from the KS-1186 golden (5 product hunks) + its test section
python3 - "$FX" "$SP" <<'PYFX'
import json, re, sys
fx, sp = sys.argv[1:3]
base = json.load(open(f"{fx}/ks1186_linekeyed_input.json", encoding="utf-8"))
prod = open(f"{fx}/ks1186_product_golden.diff").read().rstrip("\n").split("\n")
test = open(f"{fx}/ks1186_test_golden.diff").read()
head, hunks, cur = prod[:2], [], None
for l in prod[2:]:
    if l.startswith("@@ "): cur = [l]; hunks.append(cur)
    else: cur.append(l)
assert len(hunks) == 5 and [h[0] for h in hunks] == ["@@ -443,7 +443,7 @@", "@@ -509,7 +509,7 @@", "@@ -582,7 +582,7 @@", "@@ -591,7 +591,7 @@", "@@ -624,6 +624,6 @@"], [h[0] for h in hunks]
def out(name, idx):
    body = "\n".join(head + [l for i in idx for l in hunks[i]]) + "\n" + test
    open(f"{sp}/{name}.md", "w").write("```diff\n" + body + "```\n")
out("golden", [0, 1, 2, 3, 4]); out("wrongsite_512_585", [1, 2]); out("omit627", [0, 1, 2, 3]); out("only446", [0]); out("edit446_512", [0, 1])
def site(n):
    return next(dict(s) for s in base["defect_line"]["sites"] if s["line"] == n)
PLUS1 = "if (result.rows.length > 0) return await fromRow(result.rows[0]);"
def inp(name, sites, plus=None):
    d = json.loads(json.dumps(base)); d["defect_line"]["sites"] = sites
    if plus is not None: d["defect_line"]["expected_plus"] = plus
    json.dump(d, open(f"{sp}/{name}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
inp("golden", base["defect_line"]["sites"])
inp("c_446_512", [site(446), site(512)], [PLUS1])
s512 = site(512); s512["must_change"] = False; s512["note"] = "(correct) the same text as :446 - stays"
inp("f_446must_512stays", [site(446), s512], [PLUS1])
e = json.loads(json.dumps(base["defect_line"]["sites"]))
for s in e:
    if s["line"] == 512: s["line"] = 513
inp("e_512_renumbered_513", e)
# I: lenient opts — hunk 1's header start drifted (@@ -500) and hunk 2 miscounted (declares 8/8 for 7/7): A2 must go --recount
h1 = ["@@ -500,7 +500,7 @@"] + hunks[0][1:]; h2 = ["@@ -509,8 +509,8 @@"] + hunks[1][1:]
open(f"{sp}/i_lenient.md", "w").write("```diff\n" + "\n".join(head + h1 + h2 + hunks[2] + hunks[3] + hunks[4]) + "\n" + test + "```\n")
# J: reanchored — hunk 1's six context lines replaced by text the file does not have; only its -/+ pair is true
h1j = [hunks[0][0]] + ["     // ks1186 arm J: this context line is not in the file"] * 3 + hunks[0][4:6] + ["     // ks1186 arm J: nor this one"] * 3
open(f"{sp}/j_reanchor.md", "w").write("```diff\n" + "\n".join(head + h1j) + "\n" + test + "```\n")
inp("j_446", [site(446)], [PLUS1])
print("fixtures written")
PYFX
[ -f "$SP/golden.md" ] && [ -f "$SP/e_512_renumbered_513.json" ] || { echo "FATAL: fixture generation failed"; exit 2; }

run_ck(){ # run_ck <label> <checker> <input.json> <out.md> <clone> — runs into $SP/<label>/, sets RC and CO (checker.out path)
  local d="$SP/$1"; mkdir -p "$d"; cp "$4" "$d/out.md"
  echo "  .. $1 start $(date +%H:%M:%S)"
  sandbox-exec -f "$FX/nonet.sb" bash "$2" "$3" "$d/out.md" "$5" > "$d/checker.out" 2>&1
  RC=$?; CO="$d/checker.out"
  echo "  .. $1 end $(date +%H:%M:%S) rc=$RC :: $(/usr/bin/grep -E '^(PASS A3b|FAIL A3b|FAIL A3e|RESULT)' "$CO" | cut -c1-230 | tr '\n' '|')"
}
has(){ /usr/bin/grep -q -E "$2" "$1"; }

echo "--- (a) negative controls: the OLD checker"
run_ck A_old_wrongsite "$OLD" "$SP/c_446_512.json" "$SP/wrongsite_512_585.md" "$CLONE"
if has "$CO" '^PASS A3b' && ! has "$CO" '^FAIL A3b'; then ok "A  OLD checker PASSES A3b on the wrong-site diff (edits :512+:585, sites :446+:512) — it cannot tell the duplicates apart"; else bad "A" "the old checker did not pass A3b: $(/usr/bin/grep -E '^(PASS|FAIL) A3' "$CO" | head -3 | tr '\n' '|')"; fi
run_ck A2_old_omit627 "$OLD" "$SP/golden.json" "$SP/omit627.md" "$CLONE"
if has "$CO" '^PASS A3b' && ! has "$CO" '^FAIL A3b'; then ok "A2 OLD checker PASSES A3b on the KS-1186 diff with the :627 hunk dropped"; else bad "A2" "$(/usr/bin/grep -E '^(PASS|FAIL) A3' "$CO" | head -3 | tr '\n' '|')"; fi

echo "--- (b) golden"
run_ck B_new_golden "$CK" "$SP/golden.json" "$SP/golden.md" "$CLONE"
if [ "$RC" -eq 0 ] && has "$CO" '^PASS A3b every must_change site the ticket names is changed by the product hunk \(5 site\(s\); 7 line-keyed site\(s\), must_change and stays, matched by LINE NUMBER' && has "$CO" '^RESULT: PASS \(7/7\)' && has "$CO" '^A3b line-keyed: 7 site\(s\) .*REMOVED_LINES 446,512,585,594,627$'; then ok "B  NEW checker: golden → PASS A3b (5 must_change, 7 line-keyed, removed lines 446,512,585,594,627) and RESULT: PASS (7/7)"; else bad "B" "rc=$RC $(/usr/bin/grep -E '^(A3b line|PASS A3b|FAIL|RESULT)' "$CO" | head -4 | tr '\n' '|')"; fi

echo "--- (c) wrong site"
run_ck C_new_wrongsite "$CK" "$SP/c_446_512.json" "$SP/wrongsite_512_585.md" "$CLONE"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b PARTIAL FIX .*:446 `' && ! has "$CO" '^FAIL A3b PARTIAL FIX .*:512 `' && has "$CO" '^RESULT: FAIL .*stopped at A3b'; then ok "C  NEW checker: wrong-site diff → FAIL A3b naming :446 (and not :512), stopped at A3b"; else bad "C" "rc=$RC $(/usr/bin/grep -E '^(PASS A3b|FAIL|RESULT)' "$CO" | head -3 | tr '\n' '|')"; fi
run_ck C2_new_omit627 "$CK" "$SP/golden.json" "$SP/omit627.md" "$CLONE"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b PARTIAL FIX — the product hunk leaves 1 of 5 named site\(s\) untouched: :627 `' && has "$CO" '^RESULT: FAIL .*stopped at A3b'; then ok "C2 NEW checker: KS-1186 with the :627 hunk dropped → FAIL A3b naming :627 only"; else bad "C2" "rc=$RC $(/usr/bin/grep -E '^(PASS A3b|FAIL|RESULT)' "$CO" | head -3 | tr '\n' '|')"; fi

echo "--- (d) legacy text-keyed inputs: unchanged verdicts"
run_ck D1_new_ks744 "$CK" "$LM/night/inputs/code_744.json" "$FX/ks744_fin2/out.md" "$CLONE"
/usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$FX/ks744_fin2/checker.out" > "$SP/D1.expected"; /usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$CO" > "$SP/D1.got"
if cmp -s "$SP/D1.expected" "$SP/D1.got" && [ -s "$SP/D1.got" ] && ! has "$CO" '^A3b line-keyed'; then ok "D1 KS-744 (legacy, 2 must_change by text): $(wc -l < "$SP/D1.got" | tr -d ' ') PASS/FAIL/RESULT lines identical to the 12:05 fin2 run; the line-keyed path not entered"; else bad "D1" "$(diff "$SP/D1.expected" "$SP/D1.got" | head -6 | tr '\n' '|')"; fi
R1199=$LM/runs/2026-09-17_ks1199-ornith35b-night
run_ck D2_new_ks1199 "$CK" "$LM/night/inputs/code_1199.json" "$R1199/out.md" "$CLONE_FA"
/usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$R1199/checker.out" > "$SP/D2.expected"; /usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$CO" > "$SP/D2.got"
if cmp -s "$SP/D2.expected" "$SP/D2.got" && [ -s "$SP/D2.got" ] && ! has "$CO" '^A3b line-keyed'; then ok "D2 KS-1199 (legacy, test-only, held): $(wc -l < "$SP/D2.got" | tr -d ' ') PASS/FAIL/RESULT lines identical to its night run"; else bad "D2" "$(diff "$SP/D2.expected" "$SP/D2.got" | head -6 | tr '\n' '|')"; fi
extract(){ awk -v m="$2" -v e="$3" 'index($0,m)>0{f=1;next} f && $0==e{exit} f' "$1"; }
for pair in "PY3B|A3B_MISSED=\"\$(python3 - " "PY3E|A3E_REMOVED=\"\$(python3 - "; do
  tag="${pair%%|*}"; mk="${pair#*|}"
  extract "$OLD" "$mk" "$tag" > "$SP/old_$tag.py"; extract "$CK" "$mk" "$tag" > "$SP/new_$tag.py"
  [ -s "$SP/old_$tag.py" ] && [ -s "$SP/new_$tag.py" ] || { bad "D3" "could not extract $tag from a checker"; }
done
python3 - "$LM/runs" "$SP" > "$SP/D3.out" 2>&1 <<'PYD3'
import glob, json, os, subprocess, sys
runs, sp = sys.argv[1:3]
n = diff = nonempty = 0; skipped = 0; keyed = 0
for inp in sorted(glob.glob(f"{runs}/**/input.json", recursive=True)):
    d = os.path.dirname(inp); sj = f"{d}/out.md.checker/sections.json"
    if not os.path.exists(sj): continue
    try:
        j = json.load(open(inp, encoding="utf-8")); secs = json.load(open(sj))
    except Exception:
        skipped += 1; continue
    if any(s.get("key") for s in (j.get("defect_line") or {}).get("sites", [])): keyed += 1
    prod = j.get("product_file", ""); sub = j.get("repo_subdir", "")
    sec = next((o["file"] for o in secs if o.get("path") in (prod,) or f"{sub}/{o.get('path')}" == prod), None)
    if not sec or not os.path.exists(sec): skipped += 1; continue
    for tag in ("PY3B", "PY3E"):
        a = subprocess.run(["python3", f"{sp}/old_{tag}.py", inp, sec], capture_output=True, text=True)
        b = subprocess.run(["python3", f"{sp}/new_{tag}.py", inp, sec], capture_output=True, text=True)
        n += 1
        if (a.returncode, a.stdout, a.stderr) != (b.returncode, b.stdout, b.stderr):
            diff += 1; print(f"DIFF {tag} {d}: old={a.stdout.strip()[:80]!r} new={b.stdout.strip()[:80]!r}")
        if a.stdout.strip(): nonempty += 1
print(f"compared={n} differing={diff} nonempty_old_outputs={nonempty} skipped={skipped} inputs_with_key={keyed}")
PYD3
D3="$(tail -1 "$SP/D3.out")"
case "$D3" in
  *"differing=0 "*) nz="$(echo "$D3" | sed -E 's/.*nonempty_old_outputs=([0-9]+).*/\1/')"; nc="$(echo "$D3" | sed -E 's/.*compared=([0-9]+).*/\1/')"
     if [ "${nz:-0}" -ge 1 ] && [ "${nc:-0}" -ge 20 ]; then ok "D3 census over runs/: $D3"; else bad "D3" "vacuous comparison: $D3"; fi ;;
  *) bad "D3" "$D3 :: $(head -3 "$SP/D3.out" | tr '\n' '|')" ;;
esac

echo "--- (e) a line number whose tip text disagrees with the brief"
run_ck E_new_mismatch "$CK" "$SP/e_512_renumbered_513.json" "$SP/golden.md" "$CLONE"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3b SITE TEXT MISMATCH .*:513 must_change brief=`if \(result.rows.length > 0\) return fromRow\(result.rows\[0\]\);` tip=`return null;`' && ! has "$CO" '^PASS A3b' && has "$CO" '^RESULT: FAIL' && ! has "$CO" '^RESULT: .*stopped at A3b'; then ok "E  NEW checker: :512 renumbered :513 → FAIL A3b SITE TEXT MISMATCH naming :513 (tip \`return null;\`), no PASS A3b, RESULT does not trigger RETRY-ONCE"; else bad "E" "rc=$RC $(/usr/bin/grep -E '^(PASS A3b|FAIL|RESULT)' "$CO" | head -3 | tr '\n' '|')"; fi
run_ck E0_old_mismatch "$OLD" "$SP/e_512_renumbered_513.json" "$SP/golden.md" "$CLONE"
if has "$CO" '^PASS A3b'; then ok "E0 OLD checker on the same input → PASS A3b (the silent pass the new arm refuses)"; else bad "E0" "$(/usr/bin/grep -E '^(PASS|FAIL) A3' "$CO" | head -2 | tr '\n' '|')"; fi

echo "--- A3e line-keyed (the owed 'A3e line+text' fix, IMPROVEMENTS row 411 item 2)"
run_ck F_new_446only "$CK" "$SP/f_446must_512stays.json" "$SP/only446.md" "$CLONE"
if has "$CO" '^PASS A3b ' && ! has "$CO" '^FAIL A3e' && ! has "$CO" 'stopped at A3e'; then ok "F  NEW checker: stays :512 has the SAME text as must_change :446; diff edits :446 only → PASS A3b, no A3e refusal"; else bad "F" "$(/usr/bin/grep -E '^(PASS A3b|FAIL|RESULT)' "$CO" | head -3 | tr '\n' '|')"; fi
run_ck F0_old_446only "$OLD" "$SP/f_446must_512stays.json" "$SP/only446.md" "$CLONE"
if has "$CO" '^FAIL A3e .*:512 `'; then ok "F0 OLD checker on the same → FAIL A3e naming :512 (a false refusal: :512 was never touched)"; else bad "F0" "$(/usr/bin/grep -E '^(PASS A3b|FAIL|RESULT)' "$CO" | head -3 | tr '\n' '|')"; fi
run_ck G_new_446_512 "$CK" "$SP/f_446must_512stays.json" "$SP/edit446_512.md" "$CLONE"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3e .*:512 `' && ! has "$CO" '^FAIL A3e .*:446 `' && has "$CO" 'stopped at A3e'; then ok "G  NEW checker: diff edits :446 AND the stays :512 → FAIL A3e naming :512"; else bad "G" "rc=$RC $(/usr/bin/grep -E '^(PASS A3b|FAIL|RESULT)' "$CO" | head -3 | tr '\n' '|')"; fi

echo "--- the line measure under NON-strict apply opts (the section file / opts the checker recorded)"
run_ck I_new_lenient "$CK" "$SP/golden.json" "$SP/i_lenient.md" "$CLONE"
if has "$CO" '^PASS A2 diff applies at the tip — with an accommodation' && has "$CO" '^A3b line-keyed: 7 site\(s\) .*REMOVED_LINES 446,512,585,594,627$' && has "$CO" '^PASS A3b '; then ok "I  NEW checker: drifted header + miscounted hunk → A2 lenient, line measure still 446,512,585,594,627, PASS A3b"; else bad "I" "$(/usr/bin/grep -E '^(PASS A2|FAIL A2|A3b line|PASS A3b|FAIL A3b|RESULT)' "$CO" | head -4 | cut -c1-200 | tr '\n' '|')"; fi
run_ck J_new_reanchor "$CK" "$SP/j_446.json" "$SP/j_reanchor.md" "$CLONE"
if has "$CO" 'REANCHORED' && has "$CO" '^A3b line-keyed: 1 site\(s\) .*REMOVED_LINES 446$' && has "$CO" '^PASS A3b '; then ok "J  NEW checker: context the file lacks → A2 REANCHORED, the measure reads the reanchored file: REMOVED_LINES 446, PASS A3b"; else bad "J" "$(/usr/bin/grep -E '^(PASS A2|FAIL A2|A3b line|PASS A3b|FAIL A3b|RESULT)' "$CO" | head -4 | cut -c1-200 | tr '\n' '|')"; fi

if [ "${A3BL_SKIP_BUILDER:-0}" = 1 ]; then
  echo "--- (builder arms H skipped: A3BL_SKIP_BUILDER=1)"
else
  echo "--- builder: the brief opt-in (reads Linear + git show on the source checkout; no writes outside $SP)"
  PINS="ref=services/auth/src/__tests__/ks999-getuserbyid-awaits-fromrow.test.ts line=446 ctx=65536"
  mkdir -p "$SP/bH1" "$SP/bH2" "$SP/bH3"
  cp "$FX/briefs_linekeyed/KS-1186.md" "$SP/bH1/KS-1186.md"
  sed 's/^- `:512` — \*\*/- `:513` — **/' "$FX/briefs_linekeyed/KS-1186.md" > "$SP/bH2/KS-1186.md"
  sed 's/^## Where (line-keyed — /## Where (/' "$FX/briefs_linekeyed/KS-1186.md" > "$SP/bH3/KS-1186.md"
  [ "$(/usr/bin/grep -c '^- `:513` — ' "$SP/bH2/KS-1186.md")" = 1 ] && [ "$(/usr/bin/grep -c -i '^## Where (line-keyed' "$SP/bH3/KS-1186.md")" = 0 ] && [ "$(/usr/bin/grep -c -i '^## Where (line-keyed' "$SP/bH1/KS-1186.md")" = 1 ] || bad "H-fixture" "the sed edits did not land"
  sites(){ python3 -c 'import json,sys; s=json.load(open(sys.argv[1]))["defect_line"]["sites"]; print(len(s), sum(1 for x in s if x.get("key")=="line+text"), all(x.get("text_in_brief","").strip()==(x.get("text_at_tip") or "").strip() for x in s if x.get("key")))' "$1"; }
  # shellcheck disable=SC2086
  NIGHT_BRIEFS_DIR="$SP/bH1" bash "$BI" KS-1186 "$SP/bH1/input.json" $PINS > "$SP/bH1/build.out" 2>&1; rc=$?
  if [ "$rc" -eq 0 ] && [ "$(sites "$SP/bH1/input.json")" = "7 7 True" ]; then ok "H1 NEW builder + line-keyed brief → rc 0, 7 sites, 7 keyed line+text, every text_in_brief == text_at_tip"; else bad "H1" "rc=$rc $(sites "$SP/bH1/input.json" 2>&1) $(tail -2 "$SP/bH1/build.out" | tr '\n' '|')"; fi
  # shellcheck disable=SC2086
  NIGHT_BRIEFS_DIR="$SP/bH2" bash "$BI" KS-1186 "$SP/bH2/input.json" $PINS > "$SP/bH2/build.out" 2>&1; rc=$?
  if [ "$rc" -eq 2 ] && has "$SP/bH2/build.out" 'REFUSED KS-1186 — line-keyed `## Where`: :513 — the brief quotes' && [ ! -f "$SP/bH2/input.json" ]; then ok "H2 NEW builder + :512 renumbered :513 → rc 2 REFUSED naming :513, no input written"; else bad "H2" "rc=$rc $(tail -2 "$SP/bH2/build.out" | tr '\n' '|')"; fi
  # shellcheck disable=SC2086
  NIGHT_BRIEFS_DIR="$SP/bH3" bash "$BI" KS-1186 "$SP/bH3/input.json" $PINS > "$SP/bH3/build.out" 2>&1; rc=$?
  if [ "$rc" -eq 0 ] && [ "$(sites "$SP/bH3/input.json")" = "7 0 True" ]; then ok "H3 NEW builder + the brief WITHOUT 'line-keyed' in the heading → rc 0, 7 sites, 0 keyed (legacy shape)"; else bad "H3" "rc=$rc $(sites "$SP/bH3/input.json" 2>&1)"; fi
  mkdir -p "$SP/bH0"; cp "$FX/briefs_linekeyed/KS-1186.md" "$SP/bH0/KS-1186.md"
  # shellcheck disable=SC2086
  NIGHT_BRIEFS_DIR="$SP/bH0" bash "$OLDBI" KS-1186 "$SP/bH0/input.json" $PINS > "$SP/bH0/build.out" 2>&1; rc=$?
  if [ "$rc" -eq 0 ] && [ "$(sites "$SP/bH0/input.json")" = "7 0 True" ]; then ok "H0 OLD builder + the line-keyed brief → 7 sites, 0 keyed (negative control)"; else bad "H0" "rc=$rc $(sites "$SP/bH0/input.json" 2>&1)"; fi
fi

echo "a3b line-number arms: $pass passed, $fail failed ($(date +%H:%M:%S))"
[ "$fail" -eq 0 ]
