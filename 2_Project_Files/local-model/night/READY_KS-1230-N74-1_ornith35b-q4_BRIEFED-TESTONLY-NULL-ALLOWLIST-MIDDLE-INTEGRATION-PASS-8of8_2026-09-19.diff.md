# READY — KS-1230-N74-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1230-ornith35b-night3/out.md.checker/patch.diff`** (from `ls`, 16:09).

**Held 16:09 2026-09-19 by the 10:2x Wednesday seat after a source read.** Tip `f9c28a8b8`. One cell: a null allow-list in the MIDDLE of three integrations is stored as null (MIDDLENULL, admin.ts ~:1132; 0 of 633 red without the cell, exactly 1 of 634 with it). Source: the #1070-#1076 gate's N74-1. Source read: 5/5 + lines = the brief; crossed controls 3/5 and 4/5 absent (the sibling N69-1 shares its scaffolding). **Refs KS-1230.** Test files only. Tier 2. **Same file as the held READY_KS-1230-N69-1? NO:** N69-1 merged in #1074, so this builds on it at f9c28a8b8.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[NULLREFUSED] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts mode=modify runner=vitest cells=9 tampers=2 apply=strict
RESULT: PASS (8/8)
