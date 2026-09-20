# READY — KS-1234-SECURITYMIDDLEWARESKIP-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 05:36 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck-b/SECURITYMIDDLEWARESKIPUNPINNED/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 05:36 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night2/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts` (modify). `+` lines 7 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 5/5 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `SANITIZEEVERYWHERE` → red exactly ['RED KS-1234: POST /api/nft/upload as application/json - a pr']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1234-SECURITYMIDDLEWARESKIP-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts
@@ -92,3 +92,10 @@
     expect(await send('POST', '/api/v1/documents', BODY)).toEqual([200, ['POST /api/documents ks1234']]);
   }, 15000);
+  it('RED KS-1234: POST /api/nft/upload as application/json - a proxyPaths route whose body the gateway DOES parse, by the 10 MB upload parser - reaches the nft upstream with a title the sanitizer would rewrite arriving byte-equal, because sanitizeInput is skipped for proxyPaths', async () => {
+    expect(await send('POST', '/api/nft/upload', JSON.stringify({ title: '<b>ks1234</b>', contentHash: 'b'.repeat(64) }))).toEqual([200, ['POST /api/nft/upload <b>ks1234</b>']]);
+  }, 15000);
+  it('CONTROL KS-1234: the same title on the hand-parsed POST /api/documents and on its /api/v1 alias arrives byte-equal whether or not sanitizeInput is guarded - neither stream is ever parsed, so the sanitizer has nothing to rewrite', async () => {
+    const spicy = JSON.stringify({ title: '<b>ks1234</b>', contentHash: 'b'.repeat(64) });
+    expect([await send('POST', '/api/documents', spicy), await send('POST', '/api/v1/documents', spicy)]).toEqual([[200, ['POST /api/documents <b>ks1234</b>']], [200, ['POST /api/documents <b>ks1234</b>']]]);
+  }, 15000);
 });
```
