# READY — KS-739-N66-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks739-ornith35b-night4/out.md.checker/section_N.diff`, each applied with its `section_N.diff.opts`.**

**Held 13:13 2026-09-19 by the 10:2x Wednesday seat after a source read.** Tip `51dbedd39` (develop after #1061-#1069). Source: the #1061-#1069 gate's NOT-PINNED rows (report `2026-09-19-batch1061-1069-tier1-r1`). **KS-739 is Done + ARCHIVED: no Refs, no magic word, never reopen** (the #1066 precedent). Cells in ks739: a non-JSON 401 and 429 from the recipient lookup still map to RECIPIENT_LOOKUP_FAILED (documents.ts:1695, NOJSONCATCH_NON403). Source read: 8/8 = the brief; crossed 7/8 absent. Test files only (`diff_file_headers`, read by Wednesday). Tier 2.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[NOJSONCATCH_NON403] every control green under the tamper
tamper NOJSONCATCH: planted NOJSONCATCH at Blockchain/Dev/services/originate/src/routes/documents.ts:1695 (146712 -> 146694 bytes; sha256 46a098288bc9)
PASS T8[NOJSONCATCH] Blockchain/Dev/services/originate/src/routes/documents.ts restored by bytes: sha256 38eb29a64372 == tip blob, git diff --quiet rc 0
PASS T6[NOJSONCATCH] red set == declared exactly: {KS-739 F1: a 403 whose body is not JSON (json() rejects) sti, RED KS-739 N66-1: a 401 and a 429 whose body is not JSON (js}, every red an assertion failure
PASS T7[NOJSONCATCH] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts mode=modify runner=jest cells=18 tampers=2 apply=strict
RESULT: PASS (8/8)
