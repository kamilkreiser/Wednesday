# READY — KS-1206 item 1 (Ornith, briefed, code_patch, originate jest) — PASS 7/7 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1206-ornith35b-night/out.md.checker/section_N.diff`, each applied with its `section_N.opts`** (section_1 product; section_2 the new test `src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts`).

**Held 07:30 2026-09-19 by the 06:0x Wednesday seat after a source read.** Tip `59412d057`. Product `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+4 at ~:904): the admin API-key mint answers 400 BAD_REQUEST when `rateLimit` is present and not an integer 1..10000, BEFORE the INSERT. Bound = the ticket's own recommendation (the security service clamp, `services/security/src/index.ts:569-570`). Item 2 (`connectorId`) NOT included: the ticket leaves it to the owner. **Refs KS-1206, linkKind contributes; runtime → stays In Progress on merge (§5f).**

## Source read (Wednesday)
- The model's 4 product lines are IDENTICAL to the brief's (bare-fence compare: 0 not-in-brief); crossed control against the KS-1264 brief: 4/4 missing.
- Checker: strict apply; A4 red-first (3 red cells by assertion, 3 controls green); A5 6/6; A6 originate 767 → 773, 0 new reds; A7 tsc 0.

## For the GATE to measure (Wednesday's question, not a conclusion)
- The guard skips ONLY `undefined`. At the tip `d.rateLimit || 1000` turned `null` and `0` into 1000; after this change `null` and `0` answer **400**. Is any caller (admin UI, scripts, S's key-mint flow) sending `null` or `0` today? If yes, that is a compatibility break to rule on before merge.
- This does not choose the value S connector keys should get (Peter's KS-1195 question to Kam, still open), and does not repair keys already minted with a bad value.

## SEQUENCING
- Held `READY_KS-730-B*` edits the same file at :184-235 (net +3). Raise one at a time; the second rebases.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
INFO control cell present: 3 cell(s) passed BEFORE and 6 AFTER (the harness reaches the code both times)
after suite rc=0 total=773 passed=773 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline: total=767 failed=0 | after: total=773 failed=0
develop's own reds (attributed, not counted): []
NEW reds: []
reds fixed by the patch: []
tests added: 6
PASS A6 whole services/originate suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone (--types node,jest): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +111/-0 test=src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
