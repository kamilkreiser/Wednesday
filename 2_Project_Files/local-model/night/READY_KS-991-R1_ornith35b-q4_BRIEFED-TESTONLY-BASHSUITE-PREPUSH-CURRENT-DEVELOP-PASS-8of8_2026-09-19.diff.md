# READY — KS-991 R-1 (Ornith, briefed, test_only, NEW bash suite) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks991-ornith35b-night/out.md.checker/patch.diff`** (strict apply; NEW file).

**Held 08:06 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `59412d057`. TEST ONLY: new file `Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh` (4 cells, 81 lines) pinning the `!=` clause at `.githooks/pre-push:163` (the #903 gate's R-1 Tg-B tamper: a CURRENT local develop must NOT get the KS-991 BEHIND notice). A new file because `pre_push_hook_base.test.sh` is held by READY_KS-910. **Refs KS-991, linkKind contributes.** Tier 2 (test-only). **Note for the raise: it pins the pre-push hook every author runs.**

## Source read (Wednesday)
- The model's 81 lines are IDENTICAL to the brief (0 not-in-brief); crossed control against the KS-864-R1 brief: 81/81 missing.
- Checker T1-T8: strict apply; the tamper reds exactly the declared cell; controls green; tamper file restored by bytes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T8[NEQDROPPED] .githooks/pre-push restored by bytes: sha256 92abd8e9b30e == tip blob, git diff --quiet rc 0
PASS T6[NEQDROPPED] red set == declared exactly: {a CURRENT local develop is not called stale}, every red an assertion failure
PASS T7[NEQDROPPED] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh mode=new runner=bash cells=4 tampers=1 apply=strict
RESULT: PASS (8/8)
