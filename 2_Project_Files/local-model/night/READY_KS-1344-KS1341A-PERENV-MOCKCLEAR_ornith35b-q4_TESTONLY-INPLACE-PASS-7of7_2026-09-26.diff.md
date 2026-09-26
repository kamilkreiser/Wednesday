# READY — KS-1344 ks1341a per-environment mockClear (Ornith, briefed, TEST-ONLY in place, jest) — PASS 7/7 (round 2 = the ONE rebrief) — HELD for QA

> ⚠ **CANONICAL PATCH = the GOLDEN `2_Project_Files/local-model/night/briefs/KS-1344.golden/KS-1344.golden.diff`** (reproduced below). **Ornith's patch** (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1344-ornith35b-night2/out.md.checker/patch.diff`, also below) differs from it only in (a) a function-name suffix on the hunk header and (b) one extra trailing context line `  });` beyond the header's 7-line count; it applied at the checker with an accommodation. **Proof of equivalence (Wednesday, 19:53 2026-09-26):** both diffs applied with `patch -F0` (rc 0 each) to `git show 179a4f32ec06:<file>` in a scratch dir give BYTE-IDENTICAL files (sha256 prefix d999b07834ad163f each; the original is fe5e989ff9c19d04). Raise the golden; state in the PR body that the resulting file equals Ornith's output byte for byte.

**Held 19:53 2026-09-26 by Wednesday BY HAND** — `hold_ready.py` REFUSED (rc 2: "checker.out has no 'mode: code_patch' line"): this input is code_patch-shaped (no `test_file` key; `suggested_test_file` = the existing test) while the checker ran it `mode: test_only`. Tooling gap owned on Wednesday's side (IMPROVEMENTS row). Every verdict line below is COPIED from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-26_ks1344-ornith35b-night2/checker.out`.

## Checker verdict (verbatim)
```
mode: test_only (tamper at Blockchain/Dev/services/originate/src/routes/webhooks.ts:563)
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=0]
PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts } — the product file is untouched, as the ticket requires
PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)
PASS A4 RED-FIRST: src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts fails at the untouched tip (2 failed / 8 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts passes with the product hunk (8 passed / 8 run)
PASS A6 whole services/originate suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)
RESULT: PASS (7/7)
SUMMARY files=1 +3/-1 test=src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts red_first=yes apply_mode=lenient
```

## PR NOTES for the raise seat
- TEST-ONLY. ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (+3/-1). No product byte changes.
- Closes the N-1288-2 weakness (gate28): A1's REACHED check now clears the logger per environment and asserts the WHOLE call list, so a `fail500` that logged only under production reds both A1 rows (tamper at webhooks.ts:563, brief `## Tamper`).
- Refs KS-1344 (closes it). Tier by its diff at the gate (test-only on a security surface's test: T2 recommended). Run the originate package's lint on the file before pushing (the KS-1337 lesson).
- Base: develop 179a4f32ec06 at hold; re-check that the file is unchanged at the raise tip (part B #1290 does not touch it).

## Canonical patch (golden)
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
@@ -112,7 +112,9 @@
     for (const nodeEnv of NODE_ENVS) {
+      // KS-1344: cleared per environment, so each iteration must reach fail500 and log for itself.
+      mockLoggerError.mockClear();
       const reply = await call(route, nodeEnv);
       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
       // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
-      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
+      expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
     }
```

## Ornith's patch (for the record)
```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts
@@ -112,7 +112,9 @@ describe('KS-1341 part A: GET / and POST / never answer a 500 with the thrown te
     for (const nodeEnv of NODE_ENVS) {
+      // KS-1344: cleared per environment, so each iteration must reach fail500 and log for itself.
+      mockLoggerError.mockClear();
       const reply = await call(route, nodeEnv);
       expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
       expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
       // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
-      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
+      expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
     }
   });
```
