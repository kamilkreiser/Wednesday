# READY — KS-1238-F1ii (Ornith, briefed, test_only, AUTH surface — TEST FILES ONLY) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1238-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.diff.opts`.**

**Held 12:53 2026-09-19 by the 10:2x Wednesday seat after a source read.** Brief pinned at `3c447abc7` (develop moved to 51dbedd39 with #1061-#1069, which touch neither this file nor the product lines it pins). NEW file pinning that `/api/signatories` and `/api/third-party-verifiers` (proxy.ts ~:677/:700) forward no caller Bearer on the connector branch. Source read: model + lines 109/109 = the brief; crossed controls F1i 102/109 and KS-1269-U 89/109 absent; 0 - lines. Tampers SIGRAW/TPVRAW: 0 of 615 at the tip; the new cells red by assertion. **Refs KS-1238, never Closes** (two of the ticket's four cells; (iii) has no cell that can red it, (iv) is already pinned). **Zero product bytes:** the diff's only file is under `__tests__/` (Wednesday, from `diff_file_headers`). Round 10 = auth surfaces opened to TEST-ONLY on Wednesday's reading of 'auth product EDITS stay out' (Monday list, item 10). Tier 2 at the gate (test-only), but auth-adjacent, so the gate should read the tamper at source.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[SIGRAW] every control green under the tamper
tamper TPVRAW: planted TPVRAW at Blockchain/Dev/services/api-gateway/src/routes/proxy.ts:700 (56355 -> 56389 bytes; sha256 00df13499ec0)
PASS T8[TPVRAW] Blockchain/Dev/services/api-gateway/src/routes/proxy.ts restored by bytes: sha256 0924495a9df6 == tip blob, git diff --quiet rc 0
PASS T6[TPVRAW] red set == declared exactly: {RED third-party-verifiers: a valid key + a LIVE user JWT, ex, RED third-party-verifiers: a valid key + a REVOKED session J}, every red an assertion failure
PASS T7[TPVRAW] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts mode=new runner=vitest cells=6 tampers=2 apply=strict
RESULT: PASS (8/8)
