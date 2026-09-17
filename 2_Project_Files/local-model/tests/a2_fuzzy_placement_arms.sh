#!/bin/bash
# a2_fuzzy_placement_arms.sh — red-proof for code_patch A2 CONTEXT-WS REANCHOR + the FUZZY offset guard (2026-09-18, KS-1229;
# IMPROVEMENTS row "01:26 2026-09-18 — code_patch A2 accepts a FUZZY placement 30 lines from the hunk header").
#
# The defect: KS-1229 r1 + retry (runs/2026-09-18_ks1229-ornith35b-night) wrote 43 byte-exact '+' lines but re-indented ONE
# trailing context line (`});` at column 0 as `  });`). Strict and --recount --ignore-whitespace refuse; FUZZY -C1 matched the
# first `  });` of nine — "apply fragment at 174" for `@@ -204` — and the verdict read PASS A2 "with an accommodation". The cells
# landed in a scope without `issue` (a load error, FAIL 3). Into a scope that compiles it would have been a false green.
# The fix (tasks/code_patch/checker.sh + a2_placement.py): strict → lenient → CONTEXT-WS REANCHORED at the header line (the
# old side equal to the tip's lines with whitespace stripped, within 3 lines; rebuilt with the tip's exact text, applied
# strictly, '+' lines untouched) → FUZZY only when the measured fragment lands inside [B-3, B+D+3] (B header line in the
# patched image, D leading lines git dropped), else FAIL A2 FUZZY-MISPLACED → reanchor.py → fail.
#
# Every checker arm runs the REAL checker end to end (sandbox-exec, off-host outbound denied) in ONE scratch clone at the KS-1229
# tip 3961c2add, against the run's own input.json, and reads its PASS/FAIL/RESULT lines; nothing is re-implemented.
#   ARM1   NEW, the REAL r1 out.md                          → A2 CONTEXT-WS REANCHORED at 205, RESULT: PASS (7/7); the rebuilt
#          section's '+' lines byte-identical to the model's, and applied to a tip copy they sit between tip :206 `  });` and
#          tip :207 `});` (the describe.each closer), i.e. where `@@ -204` puts them
#   ARM1o  OLD (.pre-0918-fuzzyguard), the same             → PASS/FAIL/RESULT lines IDENTICAL to the recorded night checker.out
#          (FUZZY at 174, RESULT: FAIL (3 failed))
#   ARM1r  NEW, the REAL retry out.md                       → A2 CONTEXT-WS REANCHORED at 204, RESULT: PASS (7/7)
#   ARM2   NEW, r1 with its header moved to `@@ -120,6 +120,49 @@` (only -C1 resolves it, at 174)
#                                                          → FAIL A2 FUZZY-MISPLACED naming 174 and old-start 120, stopped at A2
#   ARM2o  OLD, the same                                    → PASS A2 … FUZZY … fragment at 174 (the false accept)
#   ARM2b  NEW, r1 at `@@ -204` with a WORD changed in its trailing context (so CONTEXT-WS cannot fire)
#                                                          → FAIL A2 FUZZY-MISPLACED naming 174 and old-start 204
#   ARM2bo OLD, the same                                    → PASS A2 … FUZZY … fragment at 174
#   ARM3   NEW, retry with `});` at column 0 (the model's slip fixed) and ONE word changed in the FIRST context line (the
#          header line) — the case fuzzy mode was built for (2026-09-15) → PASS A2 FUZZY with "placement guard: PLACED hunk 1
#          at 205", RESULT: PASS (7/7)
#   ARM3o  OLD, the same                                    → RESULT: PASS (7/7) (the verdict is unchanged)
#   ARM4   NEW, retry with `});` at column 0 (a clean hunk) → PASS A2 (strict …), apply_mode=strict, no accommodation text,
#          RESULT: PASS (7/7)
#   ARM5a  NEW, r1 with ONE '+' line's text changed (ks1229 → ks1230 in R1's holderEmail) → A2 CONTEXT-WS applies, then
#          FAIL A3c INCOMPLETE — 1 of 43, stopped at A3c ·  ARM5ao OLD → the same FAIL A3c (no over-accommodation)
#   ARM5b  NEW, r1 with ONE unique '+' line indented +2      → FAIL A3i INDENT SHIFT (apply mode context-ws), stopped at A3i ·
#          ARM5bo OLD → FAIL A3i INDENT SHIFT (apply mode fuzzy)
#   ARM6   census (no jest): the NEW A2 chain replayed offline over EVERY runs/**/checker.out that says "applies ONLY FUZZY"
#          → every recorded RESULT: PASS (7/7) stays FUZZY-PLACED (>= 9 of them), both KS-1229 samples become CONTEXT-WS,
#          and every FUZZY-MISPLACED row is a run whose recorded RESULT was already FAIL
#   ARM7   helper units (no jest): ctxws refuses a whitespace-stripped tie at ±1 · ctxws never alters a '+' line (a '+' line
#          carrying trailing spaces and a tab survives byte for byte) · fuzzy ties a "Context reduced" line with no preceding
#          "Hunk #n succeeded" line to its hunk (rc 0), and an untieable one fails closed (rc 2)
#
# Usage: A2F_CLONE=<clone at 3961c2add, services/originate prepared by tasks/code_patch/prepare_clone.sh> bash a2_fuzzy_placement_arms.sh
#   (make the clone as night/night_run.sh does: `git clone --shared --no-checkout <source_checkout> <clone>` +
#    `git -C <clone> checkout --detach <tip>` + prepare_clone.sh — all in a scratch dir, never in the source)
# env: A2F_CHECKER (default the installed checker.sh), A2F_OLD_CHECKER (default checker.sh.pre-0918-fuzzyguard), A2F_SCRATCH
# (default a mktemp -d). rc 0 only when every arm holds. Never reads an rc through a pipe. No rm. bash 3.2.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CK="${A2F_CHECKER:-$LM/tasks/code_patch/checker.sh}"
OLD="${A2F_OLD_CHECKER:-$LM/tasks/code_patch/checker.sh.pre-0918-fuzzyguard}"
PY="$(dirname "$CK")/a2_placement.py"
SB=$LM/tests/fixtures/a3b_line/nonet.sb
CLONE="${A2F_CLONE:-}"
TIP=3961c2add8e1637b32e638f8f0952c328c00833e
R=$LM/runs/2026-09-18_ks1229-ornith35b-night
TF=Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
SP="${A2F_SCRATCH:-$(mktemp -d "${TMPDIR:-/tmp}/a2f_arms.XXXXXX")}"
[ -d "$SP" ] && [ -n "$(ls -A "$SP" 2>/dev/null)" ] && { mv "$SP" "$SP.prev-$(date +%Y%m%d-%H%M%S)"; }
mkdir -p "$SP"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
for f in "$CK" "$OLD" "$PY" "$SB" "$R/out.md" "$R/input.json" "$R/checker.out" "$R/retry/out.md" "$R/retry/checker.out"; do
  [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }
done
[ -n "$CLONE" ] && [ "$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)" = "$TIP" ] || { echo "FATAL: A2F_CLONE ($CLONE) is not a clone at $TIP"; exit 2; }
echo "a2 fuzzy placement arms $(date '+%F %H:%M:%S') · checker $CK ($(shasum -a 256 "$CK" | cut -c1-12)) · old $OLD ($(shasum -a 256 "$OLD" | cut -c1-12)) · helper ($(shasum -a 256 "$PY" | cut -c1-12)) · scratch $SP"

# ---- fixtures (from the immutable out.md files; each asserts its one edit landed)
python3 - "$R" "$SP" <<'PYFX'
import sys
r, sp = sys.argv[1:3]
r1 = open(f"{r}/out.md", encoding="utf-8").read(); rt = open(f"{r}/retry/out.md", encoding="utf-8").read()
def one(text, old, new, what):
    assert text.count(old) == 1, (what, text.count(old)); return text.replace(old, new)
def write(name, text): open(f"{sp}/{name}", "w", encoding="utf-8").write(text)
H = "@@ -204,6 +204,49 @@"
write("a2_far.md", one(r1, H, "@@ -120,6 +120,49 @@", "far header"))
write("a2b_word.md", one(r1, "\n describe('KS-1202 create guard - ", "\n describe('KS-1202 create gate - ", "trailing word"))
closer_bad = "\n+  }); // KS-1229 control\n   });\n"; closer_ok = "\n+  }); // KS-1229 control\n });\n"
fixed = one(rt, closer_bad, closer_ok, "retry closer")
write("a4_strict.md", fixed)
write("a3_word.md", one(fixed, "\n     expect([r.status, r.saved]).toEqual([201, 0]);\n", "\n     expect([r.status, r.count]).toEqual([201, 0]);\n", "header-line word"))
write("a5a_plus_text.md", one(r1, "holderEmail: 'holder-ks1229@example.test', parentDocumentId: SOURCE_ID });\n+      expect([r.status, r.code, upstreamUrls])",
      "holderEmail: 'holder-ks1230@example.test', parentDocumentId: SOURCE_ID });\n+      expect([r.status, r.code, upstreamUrls])", "plus text"))
write("a5b_plus_indent.md", one(r1, "\n+    // KS-1229 (X-ISSUE-AFTER-HOLDER)", "\n+      // KS-1229 (X-ISSUE-AFTER-HOLDER)", "plus indent"))
print("fixtures written")
PYFX
[ -f "$SP/a5b_plus_indent.md" ] || { echo "FATAL: fixture generation failed"; exit 2; }

run_ck(){ # run_ck <label> <checker> <out.md> — runs into $SP/<label>/, sets RC and CO
  local d="$SP/$1"; mkdir -p "$d"; cp "$3" "$d/out.md"
  echo "  .. $1 start $(date +%H:%M:%S)"
  nice -n 5 sandbox-exec -f "$SB" bash "$2" "$R/input.json" "$d/out.md" "$CLONE" > "$d/checker.out" 2>&1
  RC=$?; CO="$d/checker.out"
  echo "  .. $1 end $(date +%H:%M:%S) rc=$RC :: $(/usr/bin/grep -E '^(FAIL|RESULT|SUMMARY)' "$CO" | cut -c1-260 | tr '\n' '|')"
}
has(){ /usr/bin/grep -q -E "$2" "$1"; }
lines(){ /usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$1"; }

echo "--- ARM1 the real KS-1229 samples"
run_ck ARM1_new_r1 "$CK" "$R/out.md"
PLACE="$(python3 - "$SP/ARM1_new_r1/out.md.checker" "$CLONE" "$TIP" "$TF" <<'PYP'
import os, subprocess, sys, tempfile
rep, clone, tip, tf = sys.argv[1:5]
sec = open(f"{rep}/section_1.diff", encoding="utf-8").read().split("\n"); cw = open(f"{rep}/section_1.ctxws.diff", encoding="utf-8").read().split("\n")
p_model = [l for l in sec if l.startswith("+") and not l.startswith("+++")]; p_cw = [l for l in cw if l.startswith("+") and not l.startswith("+++")]
if p_model != p_cw: print(f"PLUS DIFFER model={len(p_model)} rebuilt={len(p_cw)}"); sys.exit()
tipb = subprocess.run(["git", "-C", clone, "show", f"{tip}:{tf}"], capture_output=True, check=True).stdout
tmp = tempfile.mkdtemp(prefix="a2f_place.", dir=os.path.dirname(rep)); tree = os.path.join(tmp, "tree"); dst = os.path.join(tree, tf)
os.makedirs(os.path.dirname(dst)); open(dst, "wb").write(tipb)
env = dict(os.environ, GIT_CEILING_DIRECTORIES=tmp)
a = subprocess.run(["git", "apply", "-p1", f"{rep}/section_1.ctxws.diff"], cwd=tree, capture_output=True, text=True, env=env)
if a.returncode: print("APPLY FAILED " + a.stderr[:200]); sys.exit()
t = tipb.decode().split("\n"); n = open(dst, encoding="utf-8").read().split("\n")
added = [l[1:] for l in p_model]
ok = n[:206] == t[:206] and n[206:206 + len(added)] == added and n[206 + len(added):] == t[206:] and t[205] == "  });" and t[206] == "});"
print(f"{'PLACED' if ok else 'WRONG'} plus={len(added)} identical; tip :206={t[205]!r} :207={t[206]!r}; applied lines 207..{206 + len(added)} are the '+' lines, :{207 + len(added)}={n[206 + len(added)]!r}")
PYP
)"
if [ "$RC" -eq 0 ] && has "$CO" '^RESULT: PASS \(7/7\)$' && has "$CO" '^PASS A2 diff applies at the tip — with an accommodation: \[Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts: A2 CONTEXT-WS REANCHORED at 205 — ' && has "$CO" 'apply_mode=context-ws$' && ! has "$CO" '^PASS A2 .*FUZZY' && echo "$PLACE" | /usr/bin/grep -q '^PLACED plus=43 identical'; then ok "ARM1  NEW, real r1 out.md → A2 CONTEXT-WS REANCHORED at 205, RESULT: PASS (7/7); $PLACE"; else bad "ARM1" "rc=$RC place=[$PLACE] $(lines "$CO" | cut -c1-220 | tr '\n' '|')"; fi
run_ck ARM1o_old_r1 "$OLD" "$R/out.md"
lines "$R/checker.out" > "$SP/ARM1o.expected"; lines "$CO" > "$SP/ARM1o.got"
if [ "$RC" -ne 0 ] && cmp -s "$SP/ARM1o.expected" "$SP/ARM1o.got" && [ -s "$SP/ARM1o.got" ] && has "$CO" '^PASS A2 .*FUZZY — applies only with -C1 .*apply fragment at 174' && has "$CO" '^RESULT: FAIL \(3 failed\)$'; then ok "ARM1o OLD, same → $(wc -l < "$SP/ARM1o.got" | tr -d ' ') PASS/FAIL/RESULT lines identical to the recorded night run (FUZZY at 174, RESULT: FAIL (3 failed))"; else bad "ARM1o" "rc=$RC $(diff "$SP/ARM1o.expected" "$SP/ARM1o.got" | cut -c1-160 | head -4 | tr '\n' '|')"; fi
run_ck ARM1r_new_retry "$CK" "$R/retry/out.md"
if [ "$RC" -eq 0 ] && has "$CO" '^RESULT: PASS \(7/7\)$' && has "$CO" '^PASS A2 .*A2 CONTEXT-WS REANCHORED at 204 — ' && has "$CO" 'apply_mode=context-ws$'; then ok "ARM1r NEW, real retry out.md → A2 CONTEXT-WS REANCHORED at 204, RESULT: PASS (7/7)"; else bad "ARM1r" "rc=$RC $(lines "$CO" | cut -c1-220 | tr '\n' '|')"; fi

echo "--- ARM2 a fuzzy placement the header contradicts"
run_ck ARM2_new_far "$CK" "$SP/a2_far.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A2 FUZZY-MISPLACED — .*hunk 1: -C1 applied it at line 174 but its header says old-start 120 \(expected 120\.\.121, off by \+53 — more than 3 lines\)' && has "$CO" '^RESULT: FAIL \(1 failed\) — stopped at A2 \(a fuzzy placement the hunk header contradicts\)$' && ! has "$CO" '^(PASS|FAIL) A3'; then ok "ARM2  NEW, header moved to -120 → FAIL A2 FUZZY-MISPLACED (applied at 174, old-start 120), stopped at A2, no A3 line"; else bad "ARM2" "rc=$RC $(lines "$CO" | cut -c1-300 | tr '\n' '|')"; fi
run_ck ARM2o_old_far "$OLD" "$SP/a2_far.md"
if has "$CO" '^PASS A2 diff applies at the tip — with an accommodation: .*FUZZY — applies only with -C1 \(one context line\): Context reduced to \(1/1\) to apply fragment at 174'; then ok "ARM2o OLD, same → PASS A2 FUZZY at 174 (the false accept; $(/usr/bin/grep '^RESULT' "$CO"))"; else bad "ARM2o" "rc=$RC $(lines "$CO" | cut -c1-200 | tr '\n' '|')"; fi
run_ck ARM2b_new_word "$CK" "$SP/a2b_word.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A2 FUZZY-MISPLACED — .*hunk 1: -C1 applied it at line 174 but its header says old-start 204 \(expected 204\.\.205, off by -30 — more than 3 lines\)' && has "$CO" 'context-ws: ctxws refused: hunk 1 \(header old-start 204\)' && has "$CO" 'stopped at A2 \(a fuzzy placement'; then ok "ARM2b NEW, trailing-context word changed at -204 → CONTEXT-WS refused, FAIL A2 FUZZY-MISPLACED (174 vs 204..205, off by -30)"; else bad "ARM2b" "rc=$RC $(lines "$CO" | cut -c1-300 | tr '\n' '|')"; fi
run_ck ARM2bo_old_word "$OLD" "$SP/a2b_word.md"
if has "$CO" '^PASS A2 diff applies at the tip — with an accommodation: .*FUZZY — .*apply fragment at 174'; then ok "ARM2bo OLD, same → PASS A2 FUZZY at 174 ($(/usr/bin/grep '^RESULT' "$CO"))"; else bad "ARM2bo" "rc=$RC $(lines "$CO" | cut -c1-200 | tr '\n' '|')"; fi

echo "--- ARM3 a genuine one-word outer-context difference at the header line"
run_ck ARM3_new_word "$CK" "$SP/a3_word.md"
A3CO="$CO"
if [ "$RC" -eq 0 ] && has "$CO" '^RESULT: PASS \(7/7\)$' && has "$CO" '^PASS A2 .*FUZZY — applies only with -C1 ' && has "$CO" '^section 1 .*: applies ONLY FUZZY \(-C1\): .* — placement guard: PLACED hunk 1 at 205 \(header old-start 204, expected 204\.\.205, off by \+0' && has "$CO" 'apply_mode=fuzzy$' && ! has "$CO" 'CONTEXT-WS REANCHORED'; then ok "ARM3  NEW, one word changed at the header line → PASS A2 FUZZY, placement guard PLACED at 205 (204..205), RESULT: PASS (7/7)"; else bad "ARM3" "rc=$RC $(/usr/bin/grep -E '^(PASS|FAIL|RESULT|section)' "$CO" | cut -c1-300 | tr '\n' '|')"; fi
run_ck ARM3o_old_word "$OLD" "$SP/a3_word.md"
lines "$A3CO" | /usr/bin/grep -v '^PASS A6 ' > "$SP/ARM3.new"; lines "$CO" | /usr/bin/grep -v '^PASS A6 ' > "$SP/ARM3.old"
if [ "$RC" -eq 0 ] && has "$CO" '^RESULT: PASS \(7/7\)$' && has "$CO" '^PASS A2 .*FUZZY' && cmp -s "$SP/ARM3.new" "$SP/ARM3.old"; then ok "ARM3o OLD, same → RESULT: PASS (7/7); NEW's PASS/FAIL/RESULT lines byte-identical to OLD's (the accepted-fuzzy PASS A2 text unchanged)"; else bad "ARM3o" "rc=$RC $(diff "$SP/ARM3.new" "$SP/ARM3.old" | cut -c1-200 | head -4 | tr '\n' '|')"; fi

echo "--- ARM4 a clean strict hunk"
run_ck ARM4_new_strict "$CK" "$SP/a4_strict.md"
if [ "$RC" -eq 0 ] && has "$CO" '^RESULT: PASS \(7/7\)$' && has "$CO" '^PASS A2 diff applies at the tip \(strict git apply --check, every section, hunk headers consistent\)$' && has "$CO" 'apply_mode=strict$' && ! has "$CO" 'accommodation|CONTEXT-WS|FUZZY|REANCHORED'; then ok "ARM4  NEW, clean hunk → PASS A2 strict, apply_mode=strict, no accommodation text, RESULT: PASS (7/7)"; else bad "ARM4" "rc=$RC $(lines "$CO" | cut -c1-200 | tr '\n' '|')"; fi

echo "--- ARM5 '+' lines that differ from the brief are still refused"
run_ck ARM5a_new_plustext "$CK" "$SP/a5a_plus_text.md"
if [ "$RC" -ne 0 ] && has "$CO" '^PASS A2 .*A2 CONTEXT-WS REANCHORED at 205' && has "$CO" '^FAIL A3c INCOMPLETE — 1 of 43 line\(s\) the brief adds are ABSENT' && has "$CO" 'stopped at A3c'; then ok "ARM5a NEW, one '+' text changed → A2 CONTEXT-WS at 205, then FAIL A3c INCOMPLETE — 1 of 43, stopped at A3c"; else bad "ARM5a" "rc=$RC $(lines "$CO" | cut -c1-200 | tr '\n' '|')"; fi
run_ck ARM5ao_old_plustext "$OLD" "$SP/a5a_plus_text.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3c INCOMPLETE — 1 of 43 line\(s\)' && has "$CO" 'stopped at A3c'; then ok "ARM5ao OLD, same → FAIL A3c INCOMPLETE — 1 of 43 (as before)"; else bad "ARM5ao" "rc=$RC $(lines "$CO" | cut -c1-200 | tr '\n' '|')"; fi
run_ck ARM5b_new_plusindent "$CK" "$SP/a5b_plus_indent.md"
if [ "$RC" -ne 0 ] && has "$CO" '^PASS A2 .*A2 CONTEXT-WS REANCHORED at 205' && has "$CO" '^FAIL A3i INDENT SHIFT — 1 of 43 line\(s\) .*shifted \+2.*\(apply mode context-ws\)$' && has "$CO" 'stopped at A3i'; then ok "ARM5b NEW, one '+' line indented +2 → A2 CONTEXT-WS at 205, FAIL A3i INDENT SHIFT 1 of 43 (apply mode context-ws)"; else bad "ARM5b" "rc=$RC $(lines "$CO" | cut -c1-240 | tr '\n' '|')"; fi
run_ck ARM5bo_old_plusindent "$OLD" "$SP/a5b_plus_indent.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3i INDENT SHIFT — 1 of 43 line\(s\) .*\(apply mode fuzzy\)$'; then ok "ARM5bo OLD, same → FAIL A3i INDENT SHIFT 1 of 43 (apply mode fuzzy) (as before)"; else bad "ARM5bo" "rc=$RC $(lines "$CO" | cut -c1-240 | tr '\n' '|')"; fi

echo "--- ARM6 census: the NEW A2 chain over every historical fuzzy section (offline, no jest)"
python3 - "$LM" "$PY" "$CLONE" "$SP/census" > "$SP/ARM6.out" 2>&1 <<'PYC'
import glob, json, os, re, subprocess, sys, tempfile
LM, HELPER, OBJ, SCR = sys.argv[1:5]
os.makedirs(SCR, exist_ok=True); rows = []; summary = {}
for co in sorted(glob.glob(f"{LM}/runs/**/checker.out", recursive=True)):
    c = open(co, encoding="utf-8", errors="replace").read()
    fz = re.findall(r"^section (\d+) (\S+): applies ONLY FUZZY \(-C1\): (.*)$", c, re.M)
    if not fz: continue
    d0 = os.path.dirname(co); inp = f"{d0}/input.json"
    if not os.path.exists(inp): inp = f"{os.path.dirname(d0)}/input.json"
    d = json.load(open(inp, encoding="utf-8")); tip = d.get("tip") or d["repo"]["tip"]; sub = d.get("repo_subdir", "")
    res = re.search(r"^RESULT: .*$", c, re.M); res = res.group(0) if res else "?"
    name = os.path.relpath(d0, LM + "/runs")
    for k, path, rec in fz:
        sec = f"{d0}/out.md.checker/section_{k}.diff"
        rp = path if path.startswith(sub + "/") else f"{sub}/{path}"
        g = subprocess.run(["git", "-C", OBJ, "show", f"{tip}:{rp}"], capture_output=True)
        if g.returncode != 0 or not os.path.exists(sec):
            rows.append((name, k, res, "CENSUS-SKIP", "")); summary["CENSUS-SKIP"] = summary.get("CENSUS-SKIP", 0) + 1; continue
        tmp = tempfile.mkdtemp(prefix="census.", dir=SCR); tree = os.path.join(tmp, "tree"); dst = os.path.join(tree, path)
        os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, "wb").write(g.stdout)
        tipf = os.path.join(tmp, "tip_file"); open(tipf, "wb").write(g.stdout)
        env = dict(os.environ, GIT_CEILING_DIRECTORIES=tmp)
        for x in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"): env.pop(x, None)
        cw = os.path.join(tmp, "ctxws.diff"); word = None; detail = ""
        r1 = subprocess.run(["python3", HELPER, "ctxws", sec, tipf, cw], capture_output=True, text=True)
        if r1.returncode == 0 and subprocess.run(["git", "apply", "--check", "-p1", cw], cwd=tree, capture_output=True, env=env).returncode == 0:
            word = "CONTEXT-WS"; detail = " ".join(re.findall(r"CONTEXT-WS at \d+ \(header old-start \d+, offset [-+]\d+\)", r1.stdout))
        else:
            v = subprocess.run(["git", "apply", "--check", "-v", "-p1", "--recount", "--ignore-whitespace", "-C1", sec], cwd=tree, capture_output=True, text=True, env=env)
            vo = os.path.join(tmp, "v.out"); open(vo, "w").write(v.stdout + v.stderr)
            if v.returncode != 0:
                word = "FUZZY-NOT-APPLIED-OFFLINE"
            else:
                gd = subprocess.run(["python3", HELPER, "fuzzy", sec, vo], capture_output=True, text=True)
                word = {0: "FUZZY-PLACED", 1: "FUZZY-MISPLACED", 2: "FUZZY-UNMEASURED"}.get(gd.returncode, "GUARD-ERROR"); detail = " ; ".join(gd.stdout.strip().splitlines())
        summary[word] = summary.get(word, 0) + 1
        rows.append((name, k, res, word, detail))
for n, k, res, w, det in rows:
    print(f"ROW {n} s{k} | recorded {res[:44]} | NEW {w} {det[:230]}")
bad = [r for r in rows if r[2].startswith("RESULT: PASS") and r[3] != "FUZZY-PLACED"]
mis_on_pass = [r for r in rows if r[3] in ("FUZZY-MISPLACED", "FUZZY-UNMEASURED") and not r[2].startswith("RESULT: FAIL")]
k1229 = sorted(r[0] for r in rows if "ks1229" in r[0] and r[3] == "CONTEXT-WS")
n_pass = sum(1 for r in rows if r[2].startswith("RESULT: PASS"))
print(f"SUMMARY {json.dumps(summary, sort_keys=True)} sections={len(rows)} recorded_pass={n_pass} pass_not_placed={len(bad)} misplaced_on_non_fail={len(mis_on_pass)} ks1229_ctxws={k1229}")
PYC
A6L="$(tail -1 "$SP/ARM6.out")"
NP="$(echo "$A6L" | sed -E 's/.*recorded_pass=([0-9]+).*/\1/')"
if echo "$A6L" | /usr/bin/grep -q -E "pass_not_placed=0 misplaced_on_non_fail=0 ks1229_ctxws=\['2026-09-18_ks1229-ornith35b-night', '2026-09-18_ks1229-ornith35b-night/retry'\]$" && [ "${NP:-0}" -ge 9 ] && ! /usr/bin/grep -q -E 'CENSUS-SKIP|NOT-APPLIED-OFFLINE|GUARD-ERROR' "$SP/ARM6.out"; then ok "ARM6  census: $(echo "$A6L" | sed 's/^SUMMARY //') — every recorded PASS stays FUZZY-PLACED; misplaced rows: $(/usr/bin/grep -c 'NEW FUZZY-MISPLACED' "$SP/ARM6.out") (all on recorded FAILs)"; else bad "ARM6" "$A6L :: $(/usr/bin/grep -E 'SKIP|NOT-APPLIED|ERROR' "$SP/ARM6.out" | head -3 | tr '\n' '|')"; fi

echo "--- ARM7 helper units (no jest)"
python3 - "$PY" "$SP/units" > "$SP/ARM7.out" 2>&1 <<'PYU'
import os, subprocess, sys
PY, d = sys.argv[1:3]; os.makedirs(d, exist_ok=True)
res = []
def run(*a): return subprocess.run(["python3", PY, *a], capture_output=True, text=True)
# U1 tie: the old side matches whitespace-stripped at BOTH -1 and +1 → refused
open(f"{d}/tie.txt", "w").write("a\nx\n  y\nx\n  y\nx\nb\n")
open(f"{d}/tie.diff", "w").write("--- a/tie.txt\n+++ b/tie.txt\n@@ -4,2 +4,3 @@\n y\n+new\n x\n")
r = run("ctxws", f"{d}/tie.diff", f"{d}/tie.txt", f"{d}/tie.out.diff")
res.append(("U1 ctxws tie refused", r.returncode == 1 and "BOTH offsets [-1, 1]" in r.stdout, r.stdout.strip()))
# U2 '+' lines never altered: trailing spaces + a tab survive; context re-indented back to the tip's text
open(f"{d}/keep.txt", "w").write("one\n\tfunc() {\n}\nlast\n")
plus = "+  added  \t \n+\tsecond\n"
open(f"{d}/keep.diff", "w").write("--- a/keep.txt\n+++ b/keep.txt\n@@ -1,4 +1,6 @@\n one\n     func() {\n" + plus + "   }\n last\n")
r = run("ctxws", f"{d}/keep.diff", f"{d}/keep.txt", f"{d}/keep.out.diff")
out = open(f"{d}/keep.out.diff").read() if r.returncode == 0 else ""
res.append(("U2 ctxws '+' bytes kept, context = tip text", r.returncode == 0 and plus in out and " \tfunc() {\n" in out and "\n }\n" in out and "@@ -1,4 +1,6 @@" in out, r.stdout.strip()))
# U3 a "Context reduced" line with no preceding "Hunk #n succeeded" line: tied to the hunk whose new-start - dropped == N
open(f"{d}/two.diff", "w").write("--- a/f\n+++ b/f\n@@ -10,3 +10,4 @@\n l10\n+A\n l11\n l12\n@@ -50,5 +51,6 @@\n l49\n l50\n+B\n l51\n l52\n")
open(f"{d}/two.v", "w").write("Checking patch f...\nContext reduced to (1/1) to apply fragment at 50\n")
r = run("fuzzy", f"{d}/two.diff", f"{d}/two.v")
res.append(("U3 fuzzy unnumbered reduced line tied to hunk 2", r.returncode == 0 and r.stdout.startswith("PLACED hunk 2 at 50 (header old-start 50, expected 51..52, off by -1"), r.stdout.strip()))
# U4 an untieable reduced fragment fails closed
open(f"{d}/bad.v", "w").write("Checking patch f...\nContext reduced to (1/1) to apply fragment at 77\n")
r = run("fuzzy", f"{d}/two.diff", f"{d}/bad.v")
res.append(("U4 fuzzy untieable fragment → rc 2", r.returncode == 2 and "UNMEASURED" in r.stdout, r.stdout.strip()))
for name, good, detail in res:
    print(("OK " if good else "BAD ") + name + " :: " + detail.replace("\n", " | ")[:220])
PYU
if [ "$(/usr/bin/grep -c '^OK ' "$SP/ARM7.out")" = 4 ] && ! /usr/bin/grep -q '^BAD ' "$SP/ARM7.out"; then ok "ARM7  helper units 4/4: $(/usr/bin/grep '^OK ' "$SP/ARM7.out" | sed -E 's/ :: .*//; s/^OK //' | tr '\n' ';')"; else bad "ARM7" "$(cat "$SP/ARM7.out" | tr '\n' '|' | cut -c1-600)"; fi

echo "a2 fuzzy placement arms: $pass passed, $fail failed ($(date +%H:%M:%S)) · scratch $SP"
[ "$fail" -eq 0 ]
