# READY — KS-1275-ORDERTHROUGHSPEC-1 (Ornith, briefed, test_only, JEST/originate) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1275-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 02:38 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp`, Wednesday).

**Held 02:38 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (develop at the hold). Adds ONE cell to `originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` (one hunk at the file's end, `@@ -143,1 +143,7 @@`) pinning TODAY's spec plumbing: the REGISTERED `LifecycleEventRequest`/`LifecycleEventResponse` schemas' `action.options` equal `[...LIFECYCLE_EVENT_ACTIONS]` in declared order (the #1102–#1104 gate's NOT-PINNED row ORDERTHROUGHSPEC — the complement of #1102's ORDER-1 pin: not only the constant's order, but that the order reaches the registered spec). Refs KS-1275; NEVER Closes.

**Source read (Wednesday, same action):** 6 `+` lines, all 6 byte-equal (ordered) to `night/briefs/KS-1275-ORDERTHROUGHSPEC-1.md`; 0 `-`; one test file (T2); the run's patch BYTE-IDENTICAL to the drafter's golden (`cmp`). First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** REQREGREVERSED `originate.openapi.ts:1740`, RESREGREVERSED `:1765` (each reds exactly the new cell; each From byte-matches the tip, count 1 by `grep -c -F -x`, control `LIFECYCLE_EVENT_ACTIONS` 3, checked by Wednesday); T8 restored by bytes. Controls: 2 full `it` titles. Whole originate suite (drafter): 807/807 at the tip → 808/808 with the cell; under each tamper 807/808, the red = the new cell only.

**Checker:** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 (`runs/2026-09-21_wave3-drafter-precheck/`).

**Collision:** no held READY touches this test file; `READY_KS-1133-A` / `READY_KS-794` (2026-09-15, unmerged) carry product hunks ELSEWHERE in `originate.openapi.ts` — line numbers may shift, the From lines stay unique (drafter's frame; Wednesday re-derived counts at the tip). No live seat owns originate.

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); originate JEST 808 expected; `Refs KS-1275`; tier 2. Partition: `originate/src/__tests__/` owned by no live seat.

---
--- a/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts
@@ -143,1 +143,7 @@
+  it('RED KS-1275 ORDERTHROUGHSPEC: the REGISTERED LifecycleEventRequest and LifecycleEventResponse schemas publish action in the declared order of LIFECYCLE_EVENT_ACTIONS', async () => {
+    const { LIFECYCLE_EVENT_ACTIONS } = await import('../lifecycleActions');
+    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
+    const published = (refId: string) => defs.filter((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === refId).map((d) => d.schema.shape.action.options);
+    expect([published('LifecycleEventRequest'), published('LifecycleEventResponse')]).toEqual([[[...LIFECYCLE_EVENT_ACTIONS]], [[...LIFECYCLE_EVENT_ACTIONS]]]);
+  });
 });
