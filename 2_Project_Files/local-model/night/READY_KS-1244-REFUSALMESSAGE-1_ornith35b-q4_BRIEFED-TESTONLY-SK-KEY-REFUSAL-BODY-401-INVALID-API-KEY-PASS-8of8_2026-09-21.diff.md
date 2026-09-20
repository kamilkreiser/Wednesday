# READY — KS-1244-REFUSALMESSAGE-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1244-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 09:28 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1244-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1112rows-drafter-precheck/REFUSALMESSAGE/out.md.checker/patch.diff` rc 0, Wednesday (the 08:4x seat)).

**Held 09:28 2026-09-21 by Wednesday (the 08:4x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1244-ornith35b-night2/out.md.checker`, not typed).** Tip `7be81d5c9b109959b559e03652fb092c12de58e8`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts` (modify). `+` lines 13 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 19/19 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `REFUSALMESSAGECHANGED` → red exactly ['RED KS-1244: an sk_ key that fails validation on a required ']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1244-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1244-REFUSALMESSAGE-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1244-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts
@@ -232,4 +232,17 @@
       }
       expect(outcomes).toEqual([['sk_first, sk_second', 0, 401, false, 'UNAUTHORIZED', undefined], ['sk_second, sk_first', 0, 401, false, 'UNAUTHORIZED', undefined]]);
     });
+    it('RED KS-1244: an sk_ key that fails validation on a required mount is refused with the exact body 401 UNAUTHORIZED Invalid API key - a Node-joined pair and a single unknown key alike', async () => {
+      fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { valid: false } }) });
+      const outcomes: unknown[] = [];
+      for (const presented of ['sk_first, sk_second', 'sk_ks1244-unknown']) {
+        const req = makeReq({ headers: { 'x-api-key': presented, authorization: 'Bearer ' + buildTestToken({ sub: 'u-ks1244', role: 'user' }) } });
+        const res = makeRes();
+        const next = vi.fn();
+        await authenticateToken(true)(req, res as any, next);
+        outcomes.push([presented, next.mock.calls.length, res._status, res._json]);
+      }
+      const refused = { success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid API key' } };
+      expect(outcomes).toEqual([['sk_first, sk_second', 0, 401, refused], ['sk_ks1244-unknown', 0, 401, refused]]);
+    });
   });
```
