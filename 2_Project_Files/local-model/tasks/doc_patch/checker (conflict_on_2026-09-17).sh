#!/bin/bash
# checker.sh <input.json> <out.md> <clone-dir> — doc_patch
#   D1 output is exactly one ```diff block          D2 diff applies at the tip (strict; --recount named as an accommodation)
#   D3 touched-file set == { product_file }         D4 BEFORE: every required token ABSENT in its section (else nothing to prove)
#   D5 AFTER: every required token PRESENT in its section
#   D6 every hunk lies inside a required section (nothing outside the brief's sections changed)
# Sections = from a line matching `## …<section substring>` to the next `## ` heading, measured on the TIP file.
set -uo pipefail
INPUT="${1:-}"; OUT="${2:-}"; CLONE="${3:-}"
[ -f "$INPUT" ] && [ -f "$OUT" ] && [ -d "$CLONE/.git" ] || { echo "usage: checker.sh <input.json> <out.md> <clone-dir>" >&2; exit 1; }
REP="$OUT.checker"; mkdir -p "$REP"
PRODUCT="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["product_file"])' "$INPUT")"
FAILS=0; pass(){ echo "PASS $*"; }; fail(){ echo "FAIL $*"; FAILS=$((FAILS+1)); }
# D0 the SUBJECT exists: the clone sits at the input's tip and carries the product file (a verifier asserts its
# subject before anything about it — 2026-09-08). Without this, an empty tree reads as "patch does not apply".
TIP="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("tip") or d.get("repo",{}).get("tip",""))' "$INPUT")"
HEADC="$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)"
if [ -z "$TIP" ] || [ "$HEADC" != "$TIP" ] || [ ! -f "$CLONE/$PRODUCT" ]; then
  echo "FAIL D0 subject: clone HEAD=${HEADC:-none} input tip=${TIP:-none} file present=$([ -f "$CLONE/$PRODUCT" ] && echo yes || echo no)"; echo "RESULT: FAIL (1 failed) — stopped at D0 (the harness, not the model)"; exit 1
fi
pass "D0 subject: clone at $TIP, $PRODUCT present"
# D1
python3 - "$OUT" "$REP/patch.diff" <<'PY' || { echo "RESULT: FAIL (1 failed) — stopped at D1"; exit 1; }
import re,sys
t=open(sys.argv[1],encoding="utf-8").read()
blocks=re.findall(r"```diff\n(.*?)\n```", t, re.S)
# 2026-09-15 22:1x (KS-871 05:56, KS-1097 C r2 21:27 — twice today): a repetition loop (a <=6-line cycle repeated to the
# token budget) leaves NO closed fence, so D1 read "found 0" and the reader had to open the output to see why. Name it.
tail0=[l for l in t.split("\n") if l.strip()][-41:]
for tail in (tail0, tail0[:-1]):          # the last line is often the TRUNCATED one (the token cut mid-line)
    if len(tail)>=12:
        for k in (1,2,3,4,5,6):
            cyc=tail[-k:]; n=min(len(tail),8*k)
            if all(tail[-(i+1)]==cyc[-(i%k+1)] for i in range(n)):
                print(f"FAIL D1 REPETITION LOOP: the output's last {n} non-blank lines repeat a {k}-line cycle starting {cyc[0][:60]!r} — a sampler loop, not a diff (done_reason length)"); sys.exit(1)
if len(blocks)!=1: print(f"FAIL D1 expected exactly one ```diff block, found {len(blocks)}"); sys.exit(1)
open(sys.argv[2],"w",encoding="utf-8").write(blocks[0].rstrip("\n")+"\n"); print("PASS D1 output is exactly one fenced ```diff block")
PY
# D2
if git -C "$CLONE" apply --check -p1 "$REP/patch.diff" > "$REP/apply_check.out" 2>&1; then APPLY_OPTS=""; pass "D2 diff applies at the tip (strict)"
elif git -C "$CLONE" apply --check -p1 --recount --ignore-whitespace "$REP/patch.diff" > "$REP/apply_check_lenient.out" 2>&1; then APPLY_OPTS="--recount --ignore-whitespace"; pass "D2 diff applies at the tip — with an accommodation: --recount --ignore-whitespace (miscounted hunk headers)"
else
  # third mode (same as code_patch's A2 REANCHORED): hunks rebuilt from the model's -/+ lines at the file's real
  # location — the model's context lines come from memory (20:04: an invented ` Notes:` after the §2 fence).
  REAN="$REP/patch.reanchored.diff"; SRC_DIR="$(dirname "$0")/../code_patch"
  python3 -c 'import json,sys; [print(l) for l in json.load(open(sys.argv[1]))["defect_line"].get("must_remove",[])]' "$INPUT" > "$REP/must_remove.txt" 2>/dev/null
  if REANCHOR_REFLOW=1 REANCHOR_MUST_REMOVE="$REP/must_remove.txt" python3 "$SRC_DIR/reanchor.py" "$REP/patch.diff" "$CLONE/$PRODUCT" "$REAN" > "$REP/reanchor.out" 2>&1 && git -C "$CLONE" apply --check -p1 "$REAN" > "$REP/apply_check_rean.out" 2>&1; then
    cp "$REAN" "$REP/patch.diff"; APPLY_OPTS=""; pass "D2 diff applies at the tip — ONLY REANCHORED (an accommodation the verdict names): $(tr '\n' ';' < "$REP/reanchor.out" | cut -c1-200)"
  else fail "D2 diff does NOT apply at the tip: strict: $(head -2 "$REP/apply_check.out" | tr '\n' ' ') | reanchored: $(head -2 "$REP/reanchor.out" 2>/dev/null | tr '\n' ' ') $(head -1 "$REP/apply_check_rean.out" 2>/dev/null)"; echo "RESULT: FAIL ($FAILS failed) — stopped at D2"; exit 1; fi
fi
# D3
TOUCHED="$(git -C "$CLONE" apply --numstat -p1 $APPLY_OPTS "$REP/patch.diff" 2>/dev/null | awk '{print $3}' | sort -u)"
if [ "$TOUCHED" = "$PRODUCT" ]; then pass "D3 touched-file set == { $PRODUCT }"; else fail "D3 touched-file set is not { $PRODUCT }: $(echo "$TOUCHED" | tr '\n' ' ')"; echo "RESULT: FAIL ($FAILS failed) — stopped at D3"; exit 1; fi
# D4/D5/D6 (python over the tip file, the patched file, and the hunk headers)
git -C "$CLONE" show "HEAD:$PRODUCT" > "$REP/before.md"
git -C "$CLONE" apply -p1 $APPLY_OPTS "$REP/patch.diff" > "$REP/apply.out" 2>&1 || { fail "D5 apply failed: $(head -2 "$REP/apply.out")"; echo "RESULT: FAIL ($FAILS failed)"; exit 1; }
cp "$CLONE/$PRODUCT" "$REP/after.md"; git -C "$CLONE" checkout -q -- "$PRODUCT"
DOC_TASK_DIR="$(cd "$(dirname "$0")" && pwd)" python3 - "$INPUT" "$REP/before.md" "$REP/after.md" "$REP/patch.diff" <<'PY'
import json,re,sys
inp=json.load(open(sys.argv[1])); before=open(sys.argv[2],encoding="utf-8").read().split("\n"); after=open(sys.argv[3],encoding="utf-8").read().split("\n"); patch=open(sys.argv[4],encoding="utf-8").read()
req=inp["defect_line"]["required"]; fails=0
def section(lines, sub):
    # 2026-09-15 23:2x (KS-1045 Part B, row 93): a brief may name the document's `# ` TITLE as the section — the
    # preamble between the title and the first `## ` had no name, so an edit there could not be proved. A `sub`
    # beginning `# ` (one hash) matches a `# ` line and runs to the next heading of ANY level; `## ` names are unchanged.
    if sub.startswith("# "):
        start=next((i for i,l in enumerate(lines) if l.startswith("# ") and not l.startswith("## ") and sub in l), None)
        if start is None: return None
        end=next((i for i in range(start+1,len(lines)) if lines[i].startswith("#")), len(lines))
        return start,end
    # 2026-09-15 23:5x (KS-1035 Part D, row 97): a brief may name a `### ` sub-heading — DEV-PROCESS.md's rules
    # live under `### 1./2./3.` inside one `## `; the rule matched `## ` only, so D4 said "not found at the tip"
    # for a heading that exists at :174. A `### ` sub runs to the next heading of level 3 OR HIGHER (`## `, `# `).
    if sub.startswith("### "):
        start=next((i for i,l in enumerate(lines) if l.startswith("### ") and sub in l), None)
        if start is None: return None
        end=next((i for i in range(start+1,len(lines)) if re.match(r"^#{1,3} ", lines[i])), len(lines))
        return start,end
    start=next((i for i,l in enumerate(lines) if l.startswith("## ") and sub in l), None)
    if start is None: return None
    end=next((i for i in range(start+1,len(lines)) if lines[i].startswith("## ")), len(lines))
    return start,end
ranges=[]
for r in req:
    sb=section(before,r["section"]); sa=section(after,r["section"])
    if sb is None: print(f"FAIL D4 section '{r['section']}' not found at the tip"); fails+=1; continue
    ranges.append(sb)
    tb="\n".join(before[sb[0]:sb[1]]); ta="\n".join(after[sa[0]:sa[1]]) if sa else ""
    absent=[t for t in r["tokens"] if not re.search(r"(?<![\w-])"+re.escape(t)+r"(?![\w-])", tb)]
    if len(absent)!=len(r["tokens"]): print(f"FAIL D4 BEFORE: in '{r['section']}' already present at the tip: {[t for t in r['tokens'] if t not in absent]} — nothing to prove"); fails+=1
    else: print(f"PASS D4 BEFORE: '{r['section']}' lacks {r['tokens']} at the tip (control: section found, {sb[1]-sb[0]} lines)")
    present=[t for t in r["tokens"] if re.search(r"(?<![\w-])"+re.escape(t)+r"(?![\w-])", ta)]
    if len(present)==len(r["tokens"]): print(f"PASS D5 AFTER: '{r['section']}' carries {r['tokens']}")
    else: print(f"FAIL D5 AFTER: '{r['section']}' still lacks {[t for t in r['tokens'] if t not in present]}"); fails+=1
# D6: every CHANGED REGION (before.md vs after.md, located on the before file) inside some required section.
# 2026-09-15 23:1x (row 92): the `@@` header's declared range is a representation the model miscounts on most runs
# (D2 recounts it); a correct edit in the LAST section read as outside it. d6_ranges.py measures the artefact.
import os, subprocess
_d6 = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])) if False else os.environ.get("DOC_TASK_DIR",""), "d6_ranges.py"), sys.argv[2], sys.argv[3], ",".join(f"{a}-{b}" for a,b in ranges)], capture_output=True, text=True)
bad=[l for l in _d6.stdout.split("\n") if l.strip()]
if _d6.returncode not in (0,1): print(f"FAIL D6 instrument error rc={_d6.returncode}: {_d6.stderr.strip()[:200]}"); fails+=1
elif bad: print(f"FAIL D6 changed region(s) outside the required sections (old-file lines): {bad}"); fails+=1
else: print(f"PASS D6 every changed region lies inside the required sections ({len(ranges)} section(s), measured on before/after)")
# D7 (2026-09-15 21:4x, KS-1097 D r2 false green): every must-remove line (the brief's fenced '-' lines) is PRESENT in
# before and ABSENT in after — a dropped '-' line kept as context by the re-anchor is exactly the corruption this sees.
mr=inp["defect_line"].get("must_remove",[])
if mr:
    bl=[l.rstrip() for l in before]; al=[l.rstrip() for l in after]
    ctrl=[m for m in mr if m not in bl]
    still=[m for m in mr if m in al]
    if ctrl: print(f"FAIL D7 control: {len(ctrl)} must-remove line(s) not in the file BEFORE (the input is wrong): {ctrl[:2]}"); fails+=1
    elif still: print(f"FAIL D7 must-remove line(s) STILL PRESENT after the patch ({len(still)} of {len(mr)}): {[x[:80] for x in still[:3]]}"); fails+=1
    else: print(f"PASS D7 every must-remove line ({len(mr)}) present before and absent after (control: all found at the tip)")
else: print("INFO D7 no must-remove lines in the input (an insert-only brief, or one built before 21:4x)")
# D8 (2026-09-16 00:0x, KS-1049 A r1 false green — row 99): every '+' line the brief's fenced blocks add is present in
# AFTER exactly (rstrip only) — the doc twin of code_patch's A3c. Dropped backticks, a re-flowed clause or a paraphrase
# is a FAIL by name, before the PASS is believed.
ep=inp["defect_line"].get("expected_plus",[])
al_=[l.rstrip() for l in after]
if ep:
    miss=[e for e in ep if e.strip() and e not in al_]
    if miss: print(f"FAIL D8 ADDITION ALTERED — {len(miss)} of {len(ep)} brief '+' line(s) are not in the file AFTER, exactly: {[x[:70] for x in miss[:3]]}"); fails+=1
    else: print(f"PASS D8 every brief '+' line ({len(ep)}) is in the file AFTER, exactly")
else: print("INFO D8 no expected '+' lines in the input (built before 00:0x)")
# D9 (same case): an insert-only brief names the line the block must FOLLOW ("Insert AFTER line N", read at build time).
# The first added line must sit immediately after that tip line's position in AFTER — the model put the bullet under the
# paragraph instead of above it and every other gate was green.
ia=inp["defect_line"].get("insert_after")
if ia and ep:
    anchor=before[ia-1].rstrip() if 0 < ia <= len(before) else None
    first=next((e for e in ep if e.strip()), None)
    pos=[i for i,l in enumerate(al_) if l==first]
    if anchor is None: print(f"FAIL D9 instrument: insert_after={ia} outside the BEFORE file"); fails+=1
    elif not pos: print(f"FAIL D9 the first brief '+' line is not in AFTER (see D8)"); fails+=1
    else:
        ok=any(i>0 and al_[i-1]==anchor for i in pos)
        # a leading blank '+' line: the anchor sits one line further up
        if not ok and ep and ep[0].strip()=="" : ok=any(i>1 and al_[i-1]=="" and al_[i-2]==anchor for i in pos)
        if ok: print(f"PASS D9 the insert follows its named anchor (tip line {ia}: {anchor[:50]!r})")
        else: print(f"FAIL D9 INSERT MISPLACED — the brief says 'Insert AFTER line {ia}' ({anchor[:50]!r}) but the first '+' line sits elsewhere in AFTER (preceded by {al_[pos[0]-1][:50]!r})"); fails+=1
else: print("INFO D9 no insert_after anchor in the input (not an insert-only brief, or built before 00:0x)")
total=7 if mr else 6
total += (1 if ep else 0) + (1 if (ia and ep) else 0)
print(f"RESULT: {'PASS (%d/%d)' % (total,total) if fails==0 else f'FAIL ({fails} failed)'}")
sys.exit(1 if fails else 0)
PY
