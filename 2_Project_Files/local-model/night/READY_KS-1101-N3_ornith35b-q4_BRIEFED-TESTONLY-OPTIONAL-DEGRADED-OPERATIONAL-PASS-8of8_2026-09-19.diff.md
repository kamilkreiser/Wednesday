# READY — KS-1101 N-3 (Ornith, briefed, test_only, api-gateway vitest) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1101-ornith35b-night/out.md.checker/patch.diff`** (strict apply).

**Held 07:46 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `59412d057`. TEST ONLY: one describe/one cell in `Blockchain/Dev/services/api-gateway/src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts` pinning that a degraded OPTIONAL service (billing) leaves /system/status operational and is not counted as required-degraded (the #1037 gate's unpinned tampers at system-status.ts:425 / :418). No product file changes. **Refs KS-1101, linkKind contributes.** Tier 2 at the gate (test-only).

## Source read (Wednesday)
- The model's 11 +/- lines are IDENTICAL to the brief (0 not-in-brief); crossed control against the KS-864-R1 brief: 9/11 missing (the 2 shared are generic closers), so the compare discriminates.
- Checker T1-T8: strict apply; each of the 2 tampers reds exactly its declared cell by assertion; controls green under both; tamper files restored by bytes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T8[REQUIREDCOUNTSALL] Blockchain/Dev/services/api-gateway/src/routes/system-status.ts restored by bytes: sha256 d01feb648979 == tip blob, git diff --quiet rc 0
PASS T6[REQUIREDCOUNTSALL] red set == declared exactly: {KS-1101 N-3: /api/system/status shows billing degraded, coun}, every red an assertion failure
PASS T7[REQUIREDCOUNTSALL] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts mode=modify runner=vitest cells=12 tampers=2 apply=strict
RESULT: PASS (8/8)
