# READY — KS-1349 ks730c per-environment mockClear (originate TEST file only) — Spark, rung 3, test-only in place — PASS 7/7 — HELD for QA

**Held 02:10 2026-09-27 by Wednesday BY HAND** (hold_ready.py cannot hold a code_patch-shaped input the checker ran `mode: test_only` — the KS-1344 gap, IMPROVEMENTS). Source read: `patch.diff` == `night/briefs/KS-1349/golden/*.diff` (`cmp` rc 0). The brief replaced the ticket's own tamper (production-only, which reds C1 either way) with a DEVELOPMENT-only tamper at adminConfig.ts:104: C1 is blind at the tip under it and red at the fix.

## Checker verdict (verbatim)
```
mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/adminConfig.ts:104)
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts } — the product file is untouched, as the ticket requires
PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)
PASS A4 RED-FIRST: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts fails at the untouched tip (6 failed / 19 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts passes with the product hunk (19 passed / 19 run)
INFO control cell present: 13 cell(s) passed BEFORE and 19 AFTER (the harness reaches the code both times)
PASS A6 whole services/originate suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone (--types node,jest): rc=0 (0 lines; not gated — the runner does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=1 +3/-1 test=src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)
SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)
```

## PR NOTES
- TEST FILE ONLY: `ks730c-adminconfig-500-never-answers-err-message.test.ts` in place. Refs KS-1349 (closes it). Tier 2. **Raise AFTER KS-1334-B** (both edit ks730c; the goldens compose to an identical file in either order, but B-first needs no re-anchor). Originate lint + a test-inclusive tsc.

## Canonical patch (== model == golden)
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts
@@ -112,9 +112,11 @@
     for (const nodeEnv of NODE_ENVS) {
+      // KS-1349: cleared per environment, so each iteration must reach fail500 and log for itself.
+      mockLoggerError.mockClear();
       const reply = await call(route, nodeEnv, true);
       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
       // REACHED, not merely clean: a body without the leak is also what the benign branch and any
       // mock-shaped crash produce. Only fail500 logs this route's context with the thrown text, so
       // this is the assertion that says the code under test actually ran for THIS nodeEnv.
-      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
+      expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
     }
```
