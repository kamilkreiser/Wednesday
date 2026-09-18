# READY — KS-864 R-1 row 17 (Ornith, briefed, test_only, api-gateway vitest) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks864-ornith35b-night/out.md.checker/patch.diff`** (strict apply; NEW file).

**Held 07:49 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `59412d057`. TEST ONLY: new file `Blockchain/Dev/services/api-gateway/src/__tests__/ks864d-empty-portal-env-var-falls-back.test.ts` (5 cells) pinning that an EMPTY portal env var falls back to its compose default (the #1009 gate's row-17 Q-nullish tampers: `||`→`??` at the three portal lines :228 / :237 / :246). A new file because ks864c is held. **Refs KS-864, linkKind contributes.** Tier 2 (test-only).

## Source read (Wednesday)
- The model's 55 lines are IDENTICAL to the brief (0 not-in-brief); crossed control against the KS-1101-N3 brief: 47/55 missing.
- Checker T1-T8: strict apply; each of 3 tampers reds exactly its own portal's cell; controls green under all 3; tamper files restored by bytes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T8[ADMINNULLISH] Blockchain/Dev/services/api-gateway/src/routes/system-status.ts restored by bytes: sha256 d01feb648979 == tip blob, git diff --quiet rc 0
PASS T6[ADMINNULLISH] red set == declared exactly: {KS-864 R-1: admin-portal reports http://admin-frontend:80 wh}, every red an assertion failure
PASS T7[ADMINNULLISH] every control green under the tamper
T6 summary: 3/3 tamper(s) red exactly their declared set
T7 summary: controls green under all 3 tamper(s)
T8 summary: all 3 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks864d-empty-portal-env-var-falls-back.test.ts mode=new runner=vitest cells=5 tampers=3 apply=strict
RESULT: PASS (8/8)
