# READY — KS-1062 F-1 (Ornith, briefed, test_only, NEW api-gateway vitest file) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1062-ornith35b-night/out.md.checker/patch.diff`** (strict apply; NEW file).

**Held 08:24 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `59412d057`. TEST ONLY: new file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts` (3 cells) pinning the #932 gate's three unpinned startup-migrations tampers: the tenant summary logs at WARN when a tenant failed (:1209), the INCOMPLETE headline (:1210), the FIRST error kept (:836). New file because the ks1125 test file is held. **Refs KS-1062, linkKind contributes.** Tier 2 (test-only).

## Source read (Wednesday)
- All model +/- lines IDENTICAL to the brief (compare 0 not-in-brief); crossed control against the KS-991-R1 brief (see note).
- Checker T1-T8: strict apply; each of 3 tampers reds exactly its cell; controls green under all 3; tamper files restored by bytes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T8[SUMMARYCOMPLETE] Blockchain/Dev/services/api-gateway/src/startup-migrations.ts restored by bytes: sha256 623a99b9531e == tip blob, git diff --quiet rc 0
PASS T6[SUMMARYCOMPLETE] red set == declared exactly: {a failed tenant makes the tenant summary a WARN that says IN}, every red an assertion failure
PASS T7[SUMMARYCOMPLETE] every control green under the tamper
T6 summary: 3/3 tamper(s) red exactly their declared set
T7 summary: controls green under all 3 tamper(s)
T8 summary: all 3 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts mode=new runner=vitest cells=3 tampers=3 apply=strict
RESULT: PASS (8/8)
