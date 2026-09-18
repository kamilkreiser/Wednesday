# READY — KS-1258 N53-1 (Ornith, briefed, test_only, api-gateway vitest) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1258-ornith35b-night/out.md.checker/patch.diff`** (strict apply).

**Held 09:43 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `3c447abc7` (all of #1050-#1060 merged). TEST ONLY: the N44-1 cell in `Blockchain/Dev/services/api-gateway/src/__tests__/ks1258-degraded-optional-service-advice.test.ts` widens its start-command pattern with `yarn start|yarn dev|yarn run|node services` — the #1050-#1060 gate's NOT-PINNED tampers YARN / YARNDEV / NODE at system-status.ts:592 (the degraded-OPTIONAL block; the same `from` at :576 is the REQUIRED block — the plant is proven to land in the optional one). NPMSTART / COMPOSE still red it (no regression). **Refs KS-1258, linkKind contributes.** Tier 2 (test-only). The first live brief built with the `diff_file_headers` field: the model's diff carries both headers.

## Source read (Wednesday)
- The model's 2 +/- lines are IDENTICAL to the brief (0 not-in-brief); crossed control against the KS-1230-N54-1 brief: 2/2 missing.
- Checker T1-T8: strict apply; 5 tampers each red exactly the declared cell; controls green; tamper files restored by bytes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T8[COMPOSE] Blockchain/Dev/services/api-gateway/src/routes/system-status.ts restored by bytes: sha256 d01feb648979 == tip blob, git diff --quiet rc 0
PASS T6[COMPOSE] red set == declared exactly: {KS-1258 N44-1: the degraded optional advice carries no start}, every red an assertion failure
PASS T7[COMPOSE] every control green under the tamper
T6 summary: 5/5 tamper(s) red exactly their declared set
T7 summary: controls green under all 5 tamper(s)
T8 summary: all 5 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1258-degraded-optional-service-advice.test.ts mode=modify runner=vitest cells=4 tampers=5 apply=strict
RESULT: PASS (8/8)
