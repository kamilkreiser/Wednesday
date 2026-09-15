#!/bin/bash
# reanchor_gap_arms.sh — red-proof for reanchor.py's insert-only BLANK-GAP rule (2026-09-15 23:5x, KS-1035 D, row 98):
# the blank context lines between a '+' block and its anchoring line are part of the placement.
# Arm on the REAL KS-1035 D r1 model diff against the tip DEV-PROCESS.md (git show, read-only):
#   new script → the applied file reads  merge. / blank / paragraph / blank / ### 3.   (one blank each side)
#   old script (.pre-0915-blankoffset) → merge. / blank / blank / paragraph / ### 3.  (the defect)
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
REAN=${REAN:-$LM/tasks/code_patch/reanchor.py}
RUN=$LM/runs/2026-09-15_ks1035-ornith35b-night
SRC="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
W=$(mktemp -d)
git -C "$SRC" show 48e65c435:Blockchain/Dev/docs/DEV-PROCESS.md > "$W/tip.md"
awk '/^```diff/{f=1;next} /^```$/{f=0} f' "$RUN/out.md" > "$W/raw.diff"
python3 "$REAN" "$W/raw.diff" "$W/tip.md" "$W/rean.diff" > "$W/rean.out" 2>&1 || { echo "ARM FAIL: reanchor rc"; exit 1; }
cp "$W/tip.md" "$W/applied.md"; patch -s -p3 "$W/applied.md" < "$W/rean.diff" || { echo "ARM FAIL: patch"; exit 1; }
# the property: exactly one blank line between 'merge.' and the paragraph, and exactly one before '### 3.'
python3 - "$W/applied.md" <<'PY'
import sys
L=open(sys.argv[1],encoding='utf-8').read().split("\n")
i=next(k for k,l in enumerate(L) if l=="merge."); j=next(k for k,l in enumerate(L) if l.startswith("### 3. Parked"))
above=[l for l in L[i+1:j]]
ok = above[0]=="" and above[1]!="" and above[-1]=="" and above[-2]!=""
print(("ARM PASS" if ok else "ARM FAIL")+f": between 'merge.' and '### 3.' → first={above[0]!r} second={above[1][:20]!r} last={above[-1]!r} penultimate={above[-2][:20]!r}")
sys.exit(0 if ok else 1)
PY
