#!/bin/bash
# a3c_testonly_arms.sh — red-proof for the TEST-ONLY twin of A3c/A3d (2026-09-16 00:3x, KS-887: the first test-only
# brief with fenced '+' edits). Before this, checker.sh measured the brief's '+' lines against the PRODUCT section in
# every mode — in test-only mode there is none, so every line read "absent": a false FAIL with no subject.
# Arms on REAL run artefacts (09-08 rule 12 — controls from things the author did not write):
#   1 the checker's section-select one-liner, want = the TEST file, on KS-1120 night2's sections.json → a path (non-empty)
#   2 the same one-liner, want = the PRODUCT file (the old routing) on the same sections.json          → EMPTY (the cause)
#   3 a3c_plus.py with argv[3] = the test path, expected_plus = the section's own real '+' lines         → rc 0, quiet
#   4 as 3 with one expected line the section does NOT carry                                            → rc 1, prints it
#   5 A3d in test-only: KS-1172 night9's PINNED test section + one real tip line of that test marked '+',
#     argv[3] = the test path (its tip is in `files`)                                                    → rc 2, 1 A3D line
#   6 as 5 WITHOUT argv[3] (A3d reads the product tip — the line is not there)                          → rc 0 (blind = old behaviour)
#   7 as 5 on the OLD script (.pre-0916-a3ctestonly, ignores argv[3])                                   → rc 0 (the control: the new script discriminates, the old could not)
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
A3C=${A3C:-$LM/tasks/code_patch/a3c_plus.py}
OLD=$LM/tasks/code_patch/a3c_plus.py.pre-0916-a3ctestonly
R1=$LM/runs/2026-09-15_ks1120-ornith35b-night2
R5=$LM/runs/2026-09-15_ks1172-ornith35b-night9
SUB=Blockchain/Dev
sel() { python3 -c 'import json,sys; sub=sys.argv[3]; want=sys.argv[2]
for o in json.load(open(sys.argv[1])):
    if o["path"]==want or sub+"/"+o["path"]==want: print(o["file"]); break' "$1" "$2" "$SUB"; }
fail=0
T1=$SUB/services/vc-issuer/src/__tests__/ks1120-f2-db-miss-falls-through-to-memory.test.ts
P1=$SUB/services/vc-issuer/src/routes/presentations.ts
s=$(sel $R1/out.md.checker/sections.json "$T1"); [ -n "$s" ] && [ -s "$s" ] && echo "ARM1 PASS (test-file section found: ${s##*/})" || { echo "ARM1 FAIL (no section for the test file)"; fail=1; }
s=$(sel $R1/out.md.checker/sections.json "$P1"); [ -z "$s" ] && echo "ARM2 PASS (product section EMPTY in test-only — the old routing had no subject)" || { echo "ARM2 FAIL (unexpected product section $s)"; fail=1; }
SEC1=$(sel $R1/out.md.checker/sections.json "$T1")
TMPD=$(mktemp -d)
python3 - "$R1/input.json" "$SEC1" "$TMPD/in3.json" "$TMPD/in4.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); sec=open(sys.argv[2]).read().split("\n")
plus=[l[1:] for l in sec if l.startswith("+") and not l.startswith("+++") and len(l[1:].strip())>=8][:3]
assert len(plus)>=2, "the real section carries fewer than 2 long + lines"
d.setdefault("defect_line",{})["expected_plus"]=plus; json.dump(d,open(sys.argv[3],"w"))
d["defect_line"]["expected_plus"]=plus+["  expect(nothingTheModelWrote).toBe('absent'); // ARM4"]; json.dump(d,open(sys.argv[4],"w"))
PY
out=$(python3 "$A3C" "$TMPD/in3.json" "$SEC1" "$T1"); rc=$?
[ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ARM3 PASS (rc=0, quiet — the section's own + lines read as present)" || { echo "ARM3 FAIL (rc=$rc: $out)"; fail=1; }
out=$(python3 "$A3C" "$TMPD/in4.json" "$SEC1" "$T1"); rc=$?
[ "$rc" -eq 1 ] && printf '%s' "$out" | /usr/bin/grep -qi 'ARM4' && echo "ARM4 PASS (rc=1, the absent line named)" || { echo "ARM4 FAIL (rc=$rc: $out)"; fail=1; }
T5=$SUB/services/originate/src/__tests__/lifecycleEventRepo.test.ts
SEC5=$(sel $R5/out.md.checker/sections.json "$T5")
python3 - "$R5/input.json" "$SEC5" "$T5" "$TMPD/in5.json" "$TMPD/sec5.diff" <<'PY'
import json,sys
d=json.load(open(sys.argv[1])); sec=open(sys.argv[2]).read().split("\n"); tpath=sys.argv[3]
plus=[l[1:] for l in sec if l.startswith("+") and not l.startswith("+++")]
d.setdefault("defect_line",{})["expected_plus"]=[p for p in plus if p.strip()]
tip=d["files"][tpath].split("\n")
ctx=[l for l in tip if len(l.strip())>=12 and l.strip() not in {p.strip() for p in plus}][5]
json.dump(d,open(sys.argv[4],"w")); open(sys.argv[5],"w").write("\n".join(sec)+"\n+"+ctx+"\n")
print("planted tip line as +:", ctx.strip()[:70])
PY
out=$(python3 "$A3C" "$TMPD/in5.json" "$TMPD/sec5.diff" "$T5"); rc=$?; n=$(printf '%s\n' "$out" | /usr/bin/grep -ci '^A3D ')
[ "$rc" -eq 2 ] && [ "$n" -eq 1 ] && echo "ARM5 PASS (rc=2, 1 A3D line — the pinned test's tip line marked + is refused)" || { echo "ARM5 FAIL (rc=$rc, $n A3D lines: $out)"; fail=1; }
out=$(python3 "$A3C" "$TMPD/in5.json" "$TMPD/sec5.diff"); rc=$?
[ "$rc" -eq 0 ] && echo "ARM6 PASS (rc=0 without argv[3] — A3d reads the PRODUCT tip and is blind to the test line, the old routing)" || { echo "ARM6 FAIL (rc=$rc: $out)"; fail=1; }
out=$(python3 "$OLD" "$TMPD/in5.json" "$TMPD/sec5.diff" "$T5"); rc=$?
[ "$rc" -eq 0 ] && echo "ARM7 PASS (rc=0 on the OLD script with argv[3] — the control: it ignores the path)" || { echo "ARM7 FAIL (rc=$rc: $out)"; fail=1; }
exit $fail
