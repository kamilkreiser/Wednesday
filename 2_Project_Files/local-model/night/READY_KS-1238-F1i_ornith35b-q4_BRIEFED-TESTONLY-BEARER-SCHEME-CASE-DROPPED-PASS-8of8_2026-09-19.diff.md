# READY — KS-1238-F1i (Ornith, briefed, test_only, AUTH surface — TEST FILES ONLY) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1238-ornith35b-night2/out.md.checker/section_N.diff`, each applied with its `section_N.diff.opts`.**

**Held 12:53 2026-09-19 by the 10:2x Wednesday seat after a source read.** Brief pinned at `3c447abc7` (develop moved to 51dbedd39 with #1061-#1069, which touch neither this file nor the product lines it pins). ONE cell added to the ks1215 test pinning that a lower- or upper-case `bearer` scheme is also dropped on the connector branch (auth.ts:299). Source read: 6/6 + lines = the brief; crossed controls 5/6 absent; 0 - lines. **Polish, stated:** the new cell is outside the file's COMPLETENESS ledger (the gate's N63-1 shape on #1063); the raising seat may add it to `expected` and must then re-run the file. **Refs KS-1238, never Closes** (two of the ticket's four cells; (iii) has no cell that can red it, (iv) is already pinned). **Zero product bytes:** the diff's only file is under `__tests__/` (Wednesday, from `diff_file_headers`). Round 10 = auth surfaces opened to TEST-ONLY on Wednesday's reading of 'auth product EDITS stay out' (Monday list, item 10). Tier 2 at the gate (test-only), but auth-adjacent, so the gate should read the tamper at source.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T5 GREEN AT THE TIP: src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts passes with no tamper (21/21 cells; every declared cell present) — the cells pin EXISTING behaviour
tamper BEARERONLY: planted BEARERONLY at Blockchain/Dev/services/api-gateway/src/middleware/auth.ts:299 (19524 -> 19580 bytes; sha256 a05767342284)
PASS T8[BEARERONLY] Blockchain/Dev/services/api-gateway/src/middleware/auth.ts restored by bytes: sha256 9abef1c21164 == tip blob, git diff --quiet rc 0
PASS T6[BEARERONLY] red set == declared exactly: {RED KS-1238 (i): a valid key + a REVOKED session JWT under a}, every red an assertion failure
PASS T7[BEARERONLY] every control green under the tamper
T6 summary: 1/1 tamper(s) red exactly their declared set
T7 summary: controls green under all 1 tamper(s)
T8 summary: all 1 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts mode=modify runner=vitest cells=21 tampers=1 apply=strict
RESULT: PASS (8/8)
