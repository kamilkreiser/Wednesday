# READY — KS-1264 (Ornith, briefed, code_patch, originate jest) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1264-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.opts`** (section_2 is the new test file; section_2.decl.diff / .tdz.diff are the checker's working files, not patches to apply).

**Held 07:03 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `59412d057`. Product `Blockchain/Dev/services/originate/src/routes/documents.ts` — /revoke now CHECKS on-behalf-of before the update and RECORDS the action_provenance row only after `updateDocument` succeeds (the KS-1228 split, applied to its last caller); `handleOnBehalfOf` DELETED (no caller left; noUnusedLocals). Brief `night/briefs/KS-1264.md` (morning search round 2026-09-19; the #1042-1045 batch gate's N43-3). **Runtime behaviour change on the provenance record: TIER 1 at the gate. Refs KS-1264, linkKind contributes; stays In Progress on merge (§5f).**

## Source read (Wednesday)
- At the tip: `handleOnBehalfOf` (the recorder) at documents.ts:2348 runs BEFORE `updateDocument` at :2351; :2348 is its only call site.
- The model's 18 product +/- lines are IDENTICAL to the brief's fenced lines (python compare, bare fences: 0 not-in-brief, 0 brief-not-in-model); crossed control against the KS-1261 brief = 18/18 missing, so the compare can fail. (A first compare demanding ```diff fences returned 18/18 missing on BOTH — the instrument, re-run.)
- Checker A1-A7: strict apply; A4 red-first at the tip (1 failed / 3, assertion red, controls green); A5 3/3 after; A6 originate 767 → 770, 0 new reds; A7 tsc rc 0.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
test after product hunk: rc=0 total=3 passed=3 failed=0 suites_failed=0 loaded=1 failed_names=[]
PASS A5 GREEN-AFTER: src/__tests__/ks1264-revoke-records-its-action-provenance-row.test.ts passes with the product hunk (3 passed / 3 run)
INFO control cell present: 2 cell(s) passed BEFORE and 3 AFTER (the harness reaches the code both times)
after suite rc=0 total=770 passed=770 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline: total=767 failed=0 | after: total=770 failed=0
develop's own reds (attributed, not counted): []
NEW reds: []
reds fixed by the patch: []
tests added: 3
PASS A6 whole services/originate suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone (--types node,jest): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +144/-14 test=src/__tests__/ks1264-revoke-records-its-action-provenance-row.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
