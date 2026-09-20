# READY — KS-1275-ORDER-1 (Ornith, briefed, test_only, jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1275-ornith35b-night4/out.md.checker/patch.diff`** (from `ls` of that dir at 16:37).

**Held 16:37 2026-09-20 by the 16:0x Wednesday seat after a source read.** Tip `e470198783bcb1ef0eac94780f87579974051423`. ONE file, test-only, **zero product bytes**: adds one cell to `Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts` pinning the DECLARED ORDER of `LIFECYCLE_EVENT_ACTIONS`.

**Why it is worth having.** The suite's existing vocabulary pin asserts `[...LIFECYCLE_EVENT_ACTIONS].sort()` against a sorted literal, so it is **order-blind by construction** — any permutation of the sixteen verbs leaves it green. That order is published three ways (`z.enum` into `secuura-api.yaml`, the 400 body's `Accepted: …join(', ')`, and `docs/VOCABULARY.md`) and **nothing in the repo asserted it**. The new cell closes that.

**Source read (Wednesday, in the same action as this file):** the model's 4 `+` lines are **byte-identical** to the brief's; exactly one file touched; no product file.

**Wednesday's independent check before the brief was ever queued:** the fence's one context line `});` at `:82` was verified byte-equal at the tip **with a shifted control** (`:81` is `  });`, which does not match), and the asserted sixteen-verb string was **re-derived from `lifecycleActions.ts:38-63` independently** and matched the brief exactly.

⚠ **WEDNESDAY'S RULING FOR THE RAISE: raise as `Refs KS-1275`, NEVER a closing word.** This cell PINS today's declaration order; it does **not** do KS-1275's own fix (replacing the hand-written verb list in the `POST /lifecycle-events` description at `originate.openapi.ts:1847-1861` with a pointer to the enum, plus a spec regeneration — a two-file change). A close would be a false completion.

**Round history, stated so the record is honest:** two rounds were lost to WEDNESDAY'S OWN harness errors (the wrong input builder), not to the model or the brief — they do **not** consume Kam's one-rebrief allowance. Round 1 proper FAILED T5 on a real brief defect (two controls declared as prefixes; a jest suite matches the FULL title). **This is rebrief 1**, and the model's output was byte-identical to the brief in every one of the four rounds.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T5 GREEN AT THE TIP: src/__tests__/lifecycleEventRepo.test.ts passes with no tamper (8/8 cells; every declared cell present) — the cells pin EXISTING behaviour
tamper SWAPNOTECERT: planted SWAPNOTECERT (block 2 -> 2 lines) at Blockchain/Dev/services/originate/src/lifecycleActions.ts:60-61 (3423 -> 3423 bytes; sha256 4e71783c696b)
PASS T8[SWAPNOTECERT] Blockchain/Dev/services/originate/src/lifecycleActions.ts restored by bytes: sha256 1fabaf50e7a7 == tip blob, git diff --quiet rc 0
PASS T6[SWAPNOTECERT] red set == declared exactly: {RED KS-1275 ORDER-1: LIFECYCLE_EVENT_ACTIONS is declared in }, every red an assertion failure
PASS T7[SWAPNOTECERT] every control green under the tamper
tamper SWAPFIRSTTWO: planted SWAPFIRSTTWO (block 2 -> 2 lines) at Blockchain/Dev/services/originate/src/lifecycleActions.ts:39-40 (3423 -> 3423 bytes; sha256 cd92897c0ec0)
PASS T8[SWAPFIRSTTWO] Blockchain/Dev/services/originate/src/lifecycleActions.ts restored by bytes: sha256 1fabaf50e7a7 == tip blob, git diff --quiet rc 0
PASS T6[SWAPFIRSTTWO] red set == declared exactly: {RED KS-1275 ORDER-1: LIFECYCLE_EVENT_ACTIONS is declared in }, every red an assertion failure
PASS T7[SWAPFIRSTTWO] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts mode=modify runner=jest cells=8 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/lifecycleEventRepo.test.ts
@@ -82,1 +82,5 @@
+  it('RED KS-1275 ORDER-1: LIFECYCLE_EVENT_ACTIONS is declared in ONE order, the order z.enum publishes and the 400 message joins', () => {
+    const declaredOrder = [...LIFECYCLE_EVENT_ACTIONS].join(',');
+    expect(declaredOrder).toEqual('rights-unassign,share-revoke,share-permission-change,rename,delete,restore,share-recipient-change,share-expiry-change,share-token-rotate,share-resend,share-attach-consent,protect,unprotect,note,certified,verified');
+  });
 });
```
