#!/bin/bash
# a3i_indent_arms.sh — red-proof for code_patch checker gate A3i INDENT SHIFT (2026-09-17, KS-623 r1, IMPROVEMENTS row
# 2026-09-17 13:10). Every checker arm runs the REAL checker.sh end to end (sandbox-exec, off-host outbound denied) in a
# scratch clone at d7e95cd9f and reads its PASS/FAIL/RESULT lines; nothing is re-implemented.
#
#   A   (a) NEW checker, KS-623's REAL out.md + input (every product line shifted +2, applied FUZZY)
#           → FAIL A3i INDENT SHIFT naming :21 indent 4, brief 2; stopped at A3i; no A4 ran
#   A0  (a) negative control: the OLD checker (.pre-0917-a3i) on the same → RESULT: PASS (7/7), no A3i line
#   A1  (a) the measure is the real thing: line 21 of the file the night checker APPLIED in clone_ks623 (read only)
#           carries 4 leading spaces, and the tip's line 21 carries 2
#   B   (b) NEW checker, KS-1186's held run (its '+' lines carry a trailing `// KS-1186: …` comment the brief lacks; lenient)
#           → PASS/FAIL/RESULT lines IDENTICAL to the recorded run (PASS 7/7) and `A3i: … OK 5 line(s)`
#   B2  (b) NEW checker, the same out.md with ONE commented '+' line shifted +2 → FAIL A3i naming that line (the comment
#           tolerance never hides an indent)
#   C   (c) NEW checker, KS-1156 (test-only, no product hunk, no expected '+' lines) → lines IDENTICAL to its night run
#   D   (d) NEW checker, KS-623 hand-made with the brief's 2-space indent (its product hunk rebuilt from the TIP + the brief's '+' line)
#           → apply_mode=strict, `A3i: … OK 1`, RESULT: PASS (7/7)
#   D2  (d) NEW checker, the same with ONLY the '+' line at 4 spaces (context correct, so STRICT apply succeeds)
#           → FAIL A3i naming :21 (the gate is not tied to fuzzy mode)
#   E   (e) NEW checker, KS-623's shifted out.md + its input with expected_plus REMOVED (legacy shape)
#           → `INFO A3i skipped`, lines IDENTICAL to the recorded run minus its `PASS A3c` line (A3c skips too)
#   E2  (e) NEW checker, KS-623's input with expected_plus KEPT but the brief's `## The exact change` section removed from
#           ticket.description → `INFO A3i skipped` naming the description; lines IDENTICAL to the recorded run
#   F   census (no vitest): the helper over every run under runs/ whose checker.out has PASS A3c → exactly ONE flips
#           (KS-623), >= 10 measured, no measure error and no skip
#
# Usage: bash a3i_indent_arms.sh   (env: A3I_CHECKER, A3I_OLD_CHECKER, A3I_CLONE (d7e95cd9f, services/auth prepared),
#        A3I_SCRATCH). rc 0 only when every arm holds. Never reads an rc through a pipe. No rm: a previous scratch dir is
#        MOVED aside.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CK="${A3I_CHECKER:-$LM/tasks/code_patch/checker.sh}"
OLD="${A3I_OLD_CHECKER:-$LM/tasks/code_patch/checker.sh.pre-0917-a3i}"
PY="$(dirname "$CK")/a3i_indent.py"
SB=$LM/tests/fixtures/a3b_line/nonet.sb
CLONE="${A3I_CLONE:-/private/tmp/claude-501/night/a3bline_0917/clone}"
SP="${A3I_SCRATCH:-/private/tmp/claude-501/night/a3i_0917/arms}"
R623=$LM/runs/2026-09-17_ks623-ornith35b-night
R1186=$LM/runs/2026-09-17_ks1186-ornith35b-night
R1156=$LM/runs/2026-09-17_ks1156-ornith35b-night
NIGHT623=/private/tmp/claude-501/night/clone_ks623
AUTHN=Blockchain/Dev/services/auth/src/middleware/authenticate.ts
[ -d "$SP" ] && mv "$SP" "$SP.prev-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$SP"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
for f in "$CK" "$OLD" "$PY" "$SB" "$R623/out.md" "$R623/input.json" "$R623/checker.out" "$R1186/out.md" "$R1186/input.json" "$R1186/checker.out" "$R1156/out.md" "$R1156/input.json" "$R1156/checker.out"; do
  [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }
done
[ "$(git -C "$CLONE" rev-parse HEAD)" = d7e95cd9f153e9036ed77935a73c93504fa6e3dc ] || { echo "FATAL: $CLONE is not at d7e95cd9f"; exit 2; }
echo "a3i indent arms $(date '+%F %H:%M:%S') · checker $CK ($(shasum -a 256 "$CK" | cut -c1-12)) · old $OLD ($(shasum -a 256 "$OLD" | cut -c1-12)) · helper ($(shasum -a 256 "$PY" | cut -c1-12))"

# ---- fixtures
python3 - "$R623" "$R1186" "$SP" "$CLONE" <<'PYFX'
import json, re, subprocess, sys
r623, r1186, sp, clone = sys.argv[1:5]
out = open(f"{r623}/out.md", encoding="utf-8").read().split("\n")
# the product section = from its `--- a/` header to the next `--- ` header. Measured: the model's hunk is NOT a clean
# +2 shift of the golden (` */` is +1, and its last context line is a blank the file does not have), so D is built from
# the TIP: context 18-20 and 22-24 byte for byte, the tip's :21 as `-`, the brief's own '+' line (from the input's
# ticket.description, unstripped) as `+` — the brief's golden hunk (its P9 fin0 was strict PASS 7/7).
a = next(i for i, l in enumerate(out) if l.startswith("--- a/") and l.endswith("authenticate.ts"))
b = next(i for i in range(a + 1, len(out)) if out[i].startswith("--- "))
tip = subprocess.run(["git", "-C", clone, "show", "d7e95cd9f153e9036ed77935a73c93504fa6e3dc:Blockchain/Dev/services/auth/src/middleware/authenticate.ts"],
                     capture_output=True, text=True, check=True).stdout.split("\n")
d = json.load(open(f"{r623}/input.json", encoding="utf-8"))
bp = [l[1:] for l in d["ticket"]["description"].split("\n") if l.startswith("+  if (!['development'")]
assert len(bp) == 1 and bp[0].startswith("  if (") and not bp[0].startswith("   "), bp
hunk = out[a:a + 2] + ["@@ -18,7 +18,7 @@"] + [" " + tip[i - 1] for i in (18, 19, 20)] + ["-" + tip[20], "+" + bp[0]] + [" " + tip[i - 1] for i in (22, 23, 24)]
fixed = out[:a] + hunk + out[b:]
open(f"{sp}/d_ks623_indent_ok.md", "w", encoding="utf-8").write("\n".join(fixed))
d2h = list(hunk); d2h[7] = "+  " + bp[0]
assert d2h[7].startswith("+    if (") and hunk[6].startswith("-  if (")
d2 = out[:a] + d2h + out[b:]
open(f"{sp}/d2_ks623_plus_only_shifted.md", "w", encoding="utf-8").write("\n".join(d2))
print("D product hunk:\n" + "\n".join(hunk).replace(" ", "\u00b7"))
print("D2 '+' line:", d2h[7].replace(" ", "\u00b7"))
o86 = open(f"{r1186}/out.md", encoding="utf-8").read().split("\n")
k = next(i for i, l in enumerate(o86) if l.startswith("+    if (result.rows.length > 0) return await fromRow(result.rows[0]); // KS-1186"))
o86[k] = "+  " + o86[k][1:]
open(f"{sp}/b2_ks1186_one_shifted.md", "w", encoding="utf-8").write("\n".join(o86))
print(f"B2 shifted out.md line {k+1}:", o86[k][:40].replace(" ", "·"))
d = json.load(open(f"{r623}/input.json", encoding="utf-8"))
e = json.loads(json.dumps(d)); del e["defect_line"]["expected_plus"]
json.dump(e, open(f"{sp}/e_legacy_no_expected_plus.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
e2 = json.loads(json.dumps(d)); desc = e2["ticket"]["description"]
new = re.sub(r"^## The exact change\b.*?(?=^## )", "", desc, count=1, flags=re.M | re.S)
assert new != desc and not re.search(r"^##+\s*The exact change", new, re.M)  # the brief also names the heading in prose (THE MODE)
e2["ticket"]["description"] = new
json.dump(e2, open(f"{sp}/e2_no_exact_change_section.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("fixtures written")
PYFX
[ -f "$SP/d_ks623_indent_ok.md" ] && [ -f "$SP/e2_no_exact_change_section.json" ] || { echo "FATAL: fixture generation failed"; exit 2; }

run_ck(){ # run_ck <label> <checker> <input.json> <out.md> — runs into $SP/<label>/, sets RC and CO
  local d="$SP/$1"; mkdir -p "$d"; cp "$4" "$d/out.md"
  echo "  .. $1 start $(date +%H:%M:%S)"
  nice -n 5 sandbox-exec -f "$SB" bash "$2" "$3" "$d/out.md" "$CLONE" > "$d/checker.out" 2>&1
  RC=$?; CO="$d/checker.out"
  echo "  .. $1 end $(date +%H:%M:%S) rc=$RC :: $(/usr/bin/grep -E '^(FAIL|RESULT|A3i:|INFO A3i)' "$CO" | cut -c1-330 | tr '\n' '|')"
}
has(){ /usr/bin/grep -q -E "$2" "$1"; }
lines(){ /usr/bin/grep -E '^(PASS|FAIL|RESULT)' "$1"; }

echo "--- (a) KS-623 real run"
run_ck A_new_ks623 "$CK" "$R623/input.json" "$R623/out.md"
if [ "$RC" -ne 0 ] && has "$CO" "^FAIL A3i INDENT SHIFT — 1 of 1 line\(s\) the brief adds landed in the applied file with DIFFERENT leading whitespace: :21 indent 4, brief 2 \(shifted \+2\) \`if \(!\['development', 'test'\]" && has "$CO" 'indentation shifted by 2 space\(s\) right; copy the brief' && has "$CO" '^RESULT: FAIL \(1 failed\) — stopped at A3i' && has "$CO" '^PASS A3c ' && ! has "$CO" '^(PASS|FAIL) A4'; then ok "A  NEW checker: KS-623 real out.md → FAIL A3i INDENT SHIFT :21 indent 4, brief 2 (shifted +2), stopped at A3i, A4 never ran"; else bad "A" "rc=$RC $(lines "$CO" | tail -3 | tr '\n' '|')"; fi
run_ck A0_old_ks623 "$OLD" "$R623/input.json" "$R623/out.md"
if [ "$RC" -eq 0 ] && has "$CO" '^RESULT: PASS \(7/7\)' && ! has "$CO" 'A3i'; then ok "A0 OLD checker on the same → RESULT: PASS (7/7), no A3i (the silent pass)"; else bad "A0" "rc=$RC $(lines "$CO" | tail -2 | tr '\n' '|')"; fi
W_APPLIED="$(sed -n 21p "$NIGHT623/$AUTHN" 2>/dev/null | awk '{ match($0, /^ */); print RLENGTH }')"
W_TIP="$(git -C "$CLONE" show "d7e95cd9f153e9036ed77935a73c93504fa6e3dc:$AUTHN" | sed -n 21p | awk '{ match($0, /^ */); print RLENGTH }')"
T_APPLIED="$(sed -n 21p "$NIGHT623/$AUTHN" 2>/dev/null | sed -E 's/^[[:space:]]+//')"
if [ "$W_APPLIED" = 4 ] && [ "$W_TIP" = 2 ] && [ "$T_APPLIED" = "if (!['development', 'test'].includes(process.env.NODE_ENV || '')) {" ]; then ok "A1 the night clone's APPLIED authenticate.ts:21 = the fixed line at indent $W_APPLIED; the tip's :21 is at indent $W_TIP (the measure matches the real file)"; else bad "A1" "applied=$W_APPLIED tip=$W_TIP text=$T_APPLIED"; fi

echo "--- (b) KS-1186 held run: trailing comment beyond the brief"
run_ck B_new_ks1186 "$CK" "$R1186/input.json" "$R1186/out.md"
lines "$R1186/checker.out" > "$SP/B.expected"; lines "$CO" > "$SP/B.got"
if [ "$RC" -eq 0 ] && cmp -s "$SP/B.expected" "$SP/B.got" && [ -s "$SP/B.got" ] && has "$CO" "^A3i: every '\+' line the brief adds is in the applied .* \(apply mode lenient\): OK 5 line\(s\) byte-exact"; then ok "B  NEW checker: KS-1186 → $(wc -l < "$SP/B.got" | tr -d ' ') PASS/FAIL/RESULT lines identical to its night run (PASS 7/7); A3i OK 5 of 5 with the trailing comments"; else bad "B" "rc=$RC $(diff "$SP/B.expected" "$SP/B.got" | head -4 | tr '\n' '|') $(/usr/bin/grep -E '^A3i' "$CO")"; fi
run_ck B2_new_ks1186_shift "$CK" "$R1186/input.json" "$SP/b2_ks1186_one_shifted.md"
if [ "$RC" -ne 0 ] && has "$CO" '^FAIL A3i INDENT SHIFT — 1 of 5 line\(s\) .*:446 indent 6, brief 4 \(shifted \+2\) `if \(result.rows.length > 0\) return await fromRow\(result.rows\[0\]\);` — indentation shifted by 2 space' && has "$SP/B2_new_ks1186_shift/out.md" '^\+      if \(result.rows.length > 0\) return await fromRow\(result.rows\[0\]\); // KS-1186' && has "$CO" 'stopped at A3i'; then ok "B2 NEW checker: one commented '+' line shifted +2 → FAIL A3i naming :446 indent 6, brief 4 (the FAIL quotes the BRIEF's text; the applied line kept its comment, which A3c's tolerance accepts, and the indent is still caught)"; else bad "B2" "rc=$RC $(lines "$CO" | tail -2 | cut -c1-300 | tr '\n' '|')"; fi

echo "--- (c) KS-1156 test-only, no product hunk"
run_ck C_new_ks1156 "$CK" "$R1156/input.json" "$R1156/out.md"
lines "$R1156/checker.out" > "$SP/C.expected"; lines "$CO" > "$SP/C.got"
if cmp -s "$SP/C.expected" "$SP/C.got" && [ -s "$SP/C.got" ] && has "$CO" "^INFO A3i skipped — the input carries no expected '\+' lines"; then ok "C  NEW checker: KS-1156 → $(wc -l < "$SP/C.got" | tr -d ' ') PASS/FAIL/RESULT lines identical to its night run; INFO A3i skipped"; else bad "C" "rc=$RC $(diff "$SP/C.expected" "$SP/C.got" | head -4 | tr '\n' '|')"; fi

echo "--- (d) KS-623 with the brief's indent"
run_ck D_new_ks623_ok "$CK" "$R623/input.json" "$SP/d_ks623_indent_ok.md"
if [ "$RC" -eq 0 ] && has "$CO" '^RESULT: PASS \(7/7\)' && has "$CO" '^PASS A2 diff applies at the tip \(strict' && has "$CO" 'apply_mode=strict' && has "$CO" "^A3i: every '\+' line .*\(apply mode strict\): OK 1 line\(s\) byte-exact" && ! has "$CO" '^FAIL'; then ok "D  NEW checker: KS-623 at the brief's 2-space indent → strict apply, A3i OK 1, RESULT: PASS (7/7)"; else bad "D" "rc=$RC $(lines "$CO" | tail -3 | cut -c1-200 | tr '\n' '|')"; fi
run_ck D2_new_ks623_plusonly "$CK" "$R623/input.json" "$SP/d2_ks623_plus_only_shifted.md"
if [ "$RC" -ne 0 ] && has "$CO" '^PASS A2 diff applies at the tip \(strict' && has "$CO" '^FAIL A3i INDENT SHIFT — 1 of 1 .*:21 indent 4, brief 2 \(shifted \+2\).*\(apply mode strict\)$' && has "$CO" 'stopped at A3i'; then ok "D2 NEW checker: only the '+' line at 4 spaces → STRICT apply, FAIL A3i :21 indent 4, brief 2 (not a fuzzy-only gate)"; else bad "D2" "rc=$RC $(lines "$CO" | tail -3 | cut -c1-260 | tr '\n' '|')"; fi

echo "--- (e) legacy inputs: skipped with INFO, verdict unchanged"
run_ck E_new_legacy "$CK" "$SP/e_legacy_no_expected_plus.json" "$R623/out.md"
lines "$R623/checker.out" | /usr/bin/grep -v '^PASS A3c ' > "$SP/E.expected"; lines "$CO" > "$SP/E.got"
if [ "$RC" -eq 0 ] && cmp -s "$SP/E.expected" "$SP/E.got" && [ -s "$SP/E.got" ] && has "$CO" "^INFO A3i skipped — the input carries no expected '\+' lines" && [ "$(lines "$R623/checker.out" | /usr/bin/grep -c '^PASS A3c ')" = 1 ]; then ok "E  NEW checker: KS-623 input without expected_plus → INFO A3i skipped; $(wc -l < "$SP/E.got" | tr -d ' ') lines identical to the recorded run minus its one PASS A3c line (RESULT: PASS (7/7), the old blind spot kept)"; else bad "E" "rc=$RC $(diff "$SP/E.expected" "$SP/E.got" | head -4 | tr '\n' '|')"; fi
run_ck E2_new_nodesc "$CK" "$SP/e2_no_exact_change_section.json" "$R623/out.md"
lines "$R623/checker.out" > "$SP/E2.expected"; lines "$CO" > "$SP/E2.got"
if [ "$RC" -eq 0 ] && cmp -s "$SP/E2.expected" "$SP/E2.got" && [ -s "$SP/E2.got" ] && has "$CO" "^INFO A3i skipped — the input's ticket.description has no \`## The exact change\` section"; then ok "E2 NEW checker: expected_plus kept, the exact-change section gone from the description → INFO A3i skipped; $(wc -l < "$SP/E2.got" | tr -d ' ') lines identical to the recorded run"; else bad "E2" "rc=$RC $(diff "$SP/E2.expected" "$SP/E2.got" | head -4 | tr '\n' '|') $(/usr/bin/grep 'A3i' "$CO" | head -2)"; fi

echo "--- census: the helper over every historical run with PASS A3c (no vitest)"
python3 - "$LM" "$PY" "$CLONE" > "$SP/F.out" 2>&1 <<'PYF'
import glob, json, os, re, subprocess, sys
LM, PY, clone = sys.argv[1:4]
rc = {}; flips = []; skipped = {}
for inp in sorted(glob.glob(f"{LM}/runs/**/input.json", recursive=True)):
    d0 = os.path.dirname(inp); rep = f"{d0}/out.md.checker"; sj = f"{rep}/sections.json"; co = f"{d0}/checker.out"
    if not (os.path.exists(sj) and os.path.exists(co)): continue
    c = open(co, encoding="utf-8", errors="replace").read()
    if not re.search(r"^PASS A3c ", c, re.M): continue
    d = json.load(open(inp, encoding="utf-8")); secs = json.load(open(sj)); sub = d.get("repo_subdir", "")
    m = re.search(r"^PASS A3 \(test-only\) touched-file set == \{ (\S+) \}", c, re.M)
    target = m.group(1) if re.search(r"^mode: test_only", c, re.M) and m else d.get("product_file", "")
    k = next((i + 1 for i, o in enumerate(secs) if o.get("path") == target or f"{sub}/{o.get('path')}" == target), None)
    if not k:
        skipped["no_section"] = skipped.get("no_section", 0) + 1; continue
    f, o = (open(f"{rep}/section_{k}.opts").read().split("\n") + ["", ""])[:2]
    if subprocess.run(["git", "-C", clone, "cat-file", "-e", d["tip"] + "^{commit}"], capture_output=True).returncode:
        skipped["tip_absent"] = skipped.get("tip_absent", 0) + 1; continue
    r = subprocess.run(["python3", PY, inp, clone, f, target, o], capture_output=True, text=True)
    rc[r.returncode] = rc.get(r.returncode, 0) + 1
    if r.returncode != 0:
        flips.append(f"{os.path.relpath(d0, LM + '/runs')} rc={r.returncode} {r.stdout.strip().splitlines()[0][:120]}")
for x in flips: print("FLIP", x)
print(f"measured={sum(rc.values())} rc={dict(sorted(rc.items()))} skipped={skipped} flips={len(flips)}")
PYF
F="$(tail -1 "$SP/F.out")"
NM="$(echo "$F" | sed -E 's/^measured=([0-9]+).*/\1/')"
if [ "$(/usr/bin/grep -c '^FLIP ' "$SP/F.out")" = 1 ] && has "$SP/F.out" '^FLIP 2026-09-17_ks623-ornith35b-night rc=1 SHIFT :21 observed=4 expected=2' && [ "${NM:-0}" -ge 10 ] && echo "$F" | /usr/bin/grep -q -E "skipped=\{\} flips=1$"; then ok "F  census: $F — the one flip is KS-623"; else bad "F" "$F :: $(head -4 "$SP/F.out" | tr '\n' '|')"; fi

echo "a3i indent arms: $pass passed, $fail failed ($(date +%H:%M:%S))"
[ "$fail" -eq 0 ]
