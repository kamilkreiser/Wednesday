#!/bin/bash
# checker.sh <input.json> <out.md> <clone-dir> — comment_patch (2026-09-17 19:4x, HARNESS_WIDEN_PROPOSAL_2026-09-17b §3)
#
# A comment/docblock edit to ONE .ts/.tsx/.js/.mjs/.cjs file. No test cell can go red for it, so nothing runs: the proof
# is that the PROGRAM did not change (C4) while the brief's words did (C6/C7), inside the brief's lines only (C5).
#   C0 subject   the clone sits at the input's tip, carries the product file, and its node_modules/typescript loads
#   C1 one block exactly one fenced ```diff block, nothing outside it; a sampler repetition loop is named (D1 copy)
#   C2 applies   strict; then --recount (named); then the reanchor chain (code_patch/reanchor.py, named) — no NEWFILE
#                synthesis, no --ignore-whitespace, no fuzz: a comment edit never creates a file, and a whitespace
#                accommodation would let an indent change through unnamed
#   C3 touched   the touched-file set == { product_file }
#   C4 tokens    the code-token stream (every syntax leaf: kind + text, literals included) is IDENTICAL before and after,
#                measured by tasks/comment_patch/token_equiv.cjs under the CLONE's own node_modules/typescript; the
#                first difference is named; an instrument error FAILS (closed)
#   C4b directives the multiset of directive comment lines is identical
#   C5 region    every changed line lies inside the brief's named ranges
#   C6 removed   every brief '-' line is the tip's line at its number before, and gone after
#   C7 adds      every brief '+' line is in the file after, byte-exact
# No A4/A6/A7 equivalent: C4 proves the token stream is unchanged, so the suites and tsc cannot change.
# C4-C7 all run (not stop-at-first) so a verdict names every broken gate. Every write verb runs inside <clone-dir>;
# the patched file is copied out and the clone restored. Reports in <out.md>.checker/. rc 0 only when all pass.
set -uo pipefail
INPUT="${1:-}"; OUT="${2:-}"; CLONE="${3:-}"
[ -f "$INPUT" ] && [ -f "$OUT" ] && [ -d "$CLONE/.git" ] || { echo "usage: checker.sh <input.json> <out.md> <clone-dir>" >&2; exit 1; }
HERE="$(cd -P "$(dirname "$0")" && pwd)"
REP="$OUT.checker"; mkdir -p "$REP"
PRODUCT="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["product_file"])' "$INPUT")"
SUBDIR="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("repo_subdir","Blockchain/Dev"))' "$INPUT")"
FAILS=0; pass(){ echo "PASS $*"; }; fail(){ echo "FAIL $*"; FAILS=$((FAILS+1)); }
python3 -c 'import json,sys; c=json.load(open(sys.argv[1])).get("comment"); sys.exit(0 if c and c.get("ranges") else 1)' "$INPUT" || { echo "FAIL C0 subject: the input carries no comment.ranges (not a comment_patch input)"; echo "RESULT: FAIL (1 failed) — stopped at C0 (the harness, not the model)"; exit 1; }
# ---- C0
TIP="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("tip") or d.get("repo",{}).get("tip",""))' "$INPUT")"
HEADC="$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)"
TSDIR="$CLONE/$SUBDIR/node_modules/typescript"
if [ -z "$TIP" ] || [ "$HEADC" != "$TIP" ] || [ ! -f "$CLONE/$PRODUCT" ]; then
  echo "FAIL C0 subject: clone HEAD=${HEADC:-none} input tip=${TIP:-none} file present=$([ -f "$CLONE/$PRODUCT" ] && echo yes || echo no)"; echo "RESULT: FAIL (1 failed) — stopped at C0 (the harness, not the model)"; exit 1
fi
TSV="$(/opt/homebrew/bin/node -e 'process.stdout.write(require(process.argv[1]).version)' "$TSDIR" 2>"$REP/ts_load.err")"
if [ -z "$TSV" ]; then
  echo "FAIL C0 subject: the clone's typescript does not load from $TSDIR ($(head -1 "$REP/ts_load.err" | cut -c1-160)) — run tasks/comment_patch/prepare_clone.sh"; echo "RESULT: FAIL (1 failed) — stopped at C0 (the harness, not the model)"; exit 1
fi
if [ -n "$(git -C "$CLONE" status --porcelain -- "$PRODUCT")" ]; then
  echo "FAIL C0 subject: $PRODUCT is modified in the clone before the check"; echo "RESULT: FAIL (1 failed) — stopped at C0 (the harness, not the model)"; exit 1
fi
pass "C0 subject: clone at $TIP, $PRODUCT present and clean, typescript $TSV loads from the clone"
# ---- C1 (doc_patch D1, copied)
python3 - "$OUT" "$REP/patch.diff" <<'PY' || { echo "RESULT: FAIL (1 failed) — stopped at C1"; exit 1; }
import re,sys
t=open(sys.argv[1],encoding="utf-8").read()
tail0=[l for l in t.split("\n") if l.strip()][-41:]
for tail in (tail0, tail0[:-1]):
    if len(tail)>=12:
        for k in (1,2,3,4,5,6):
            cyc=tail[-k:]; n=min(len(tail),8*k)
            if all(tail[-(i+1)]==cyc[-(i%k+1)] for i in range(n)):
                print(f"FAIL C1 REPETITION LOOP: the output's last {n} non-blank lines repeat a {k}-line cycle starting {cyc[0][:60]!r} — a sampler loop, not a diff"); sys.exit(1)
blocks=re.findall(r"```diff[^\n]*\n(.*?)\n?```", t, re.S)
allb=re.findall(r"```[^\n]*\n.*?```", t, re.S)
outside=re.sub(r"```[^\n]*\n.*?```", "", t, flags=re.S).strip()
if len(blocks)!=1 or len(allb)!=1 or outside:
    print(f"FAIL C1 expected exactly one ```diff block and nothing else: diff blocks {len(blocks)}, fenced blocks {len(allb)}, prose outside {len(outside)} chars{(' ('+repr(outside[:60])+')') if outside else ''}"); sys.exit(1)
body=blocks[0].split("\n")
while body and body[-1]=="": body.pop()
open(sys.argv[2],"w",encoding="utf-8").write("\n".join(body)+"\n"); print("PASS C1 output is exactly one fenced ```diff block, nothing outside it")
PY
# ---- C2 (strict → --recount → reanchored)
APPLY_OPTS=""; APPLY_MODE=strict
if git -C "$CLONE" apply --check -p1 "$REP/patch.diff" > "$REP/apply_check.out" 2>&1; then pass "C2 diff applies at the tip (strict)"
elif git -C "$CLONE" apply --check -p1 --recount "$REP/patch.diff" > "$REP/apply_check_recount.out" 2>&1; then APPLY_OPTS="--recount"; APPLY_MODE=recount; pass "C2 diff applies at the tip — with an accommodation: --recount (miscounted hunk headers)"
else
  REAN="$REP/patch.reanchored.diff"
  python3 -c 'import json,sys; [print(m["text"]) for m in json.load(open(sys.argv[1]))["comment"]["must_remove"]]' "$INPUT" > "$REP/must_remove.txt"
  if REANCHOR_MUST_REMOVE="$REP/must_remove.txt" python3 "$HERE/../code_patch/reanchor.py" "$REP/patch.diff" "$CLONE/$PRODUCT" "$REAN" > "$REP/reanchor.out" 2>&1 && git -C "$CLONE" apply --check -p1 "$REAN" > "$REP/apply_check_rean.out" 2>&1; then
    cp "$REP/patch.diff" "$REP/patch.as-written.diff"; cp "$REAN" "$REP/patch.diff"; APPLY_OPTS=""; APPLY_MODE=reanchored
    pass "C2 diff applies at the tip — ONLY REANCHORED (an accommodation the verdict names): $(tr '\n' ';' < "$REP/reanchor.out" | cut -c1-200)"
  else
    fail "C2 diff does NOT apply at the tip: strict: $(head -2 "$REP/apply_check.out" | tr '\n' ' ') | recount: $(head -1 "$REP/apply_check_recount.out" | tr '\n' ' ') | reanchored: $(head -2 "$REP/reanchor.out" 2>/dev/null | tr '\n' ' ') $(head -1 "$REP/apply_check_rean.out" 2>/dev/null)"
    echo "RESULT: FAIL ($FAILS failed) — stopped at C2"; exit 1
  fi
fi
# ---- C3
git -C "$CLONE" apply --numstat -p1 $APPLY_OPTS "$REP/patch.diff" > "$REP/numstat.out" 2>&1
TOUCHED="$(awk -F'\t' '{print $3}' "$REP/numstat.out" | sort -u)"
if [ "$TOUCHED" = "$PRODUCT" ] && /usr/bin/grep -q . "$REP/numstat.out"; then pass "C3 touched-file set == { $PRODUCT }"
else fail "C3 touched-file set is not { $PRODUCT }: $(echo "$TOUCHED" | tr '\n' ' ')"; echo "RESULT: FAIL ($FAILS failed) — stopped at C3"; exit 1; fi
# ---- apply, copy out, restore
git -C "$CLONE" show "HEAD:$PRODUCT" > "$REP/before.src"
git -C "$CLONE" apply -p1 $APPLY_OPTS "$REP/patch.diff" > "$REP/apply.out" 2>&1 || { fail "C2 apply failed after --check passed: $(head -2 "$REP/apply.out")"; echo "RESULT: FAIL ($FAILS failed)"; exit 1; }
cp "$CLONE/$PRODUCT" "$REP/after.src"; git -C "$CLONE" checkout -q -- "$PRODUCT"
[ -z "$(git -C "$CLONE" status --porcelain -- "$PRODUCT")" ] || echo "WARNING the clone's $PRODUCT is not clean after restore"
# ---- C4 C4b C5 C6 C7
python3 "$HERE/cp_gates.py" check "$INPUT" "$REP/before.src" "$REP/after.src" "$TSDIR" > "$REP/gates.out" 2>&1
GRC=$?
cat "$REP/gates.out"
NG="$(/usr/bin/grep -c '^FAIL ' "$REP/gates.out")"
if [ "$GRC" -ne "$NG" ]; then fail "C4 gate instrument rc=$GRC does not match its $NG FAIL line(s): $(tail -2 "$REP/gates.out" | tr '\n' ' ' | cut -c1-200)"; fi
FAILS=$((FAILS + NG))
FIRST="$(/usr/bin/grep -m1 '^FAIL ' "$REP/gates.out" | awk '{print $2}')"
TOTAL=$((4 + $(/usr/bin/grep -c -E '^(PASS|FAIL) ' "$REP/gates.out")))
if [ "$FAILS" -eq 0 ]; then echo "RESULT: PASS ($TOTAL/$TOTAL) apply_mode=$APPLY_MODE"; exit 0; fi
echo "RESULT: FAIL ($FAILS failed) — stopped at ${FIRST:-C4} ($(/usr/bin/grep '^FAIL ' "$REP/gates.out" | awk '{print $2}' | tr '\n' ' ' | sed 's/ $//'))"
exit 1
