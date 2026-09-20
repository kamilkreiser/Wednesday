# READY — KS-1234-ALIASUPLOAD-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night3/out.md.checker/patch.diff`** (from `ls` at 05:36 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night3/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck-b/ALIASUPLOADPARSERASYMMETRY/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 05:36 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night3/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts` (modify). `+` lines 7 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `NFTPARSERUNMOUNTED` → red exactly ['RED KS-1234: a non-JSON body on POST /api/nft/upload is refu']
- `PARSERONNFTALIAS` → red exactly ['RED KS-1234: a non-JSON body on POST /api/nft/upload is refu']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night3/input.json`. Brief: `night/briefs/KS-1234-ALIASUPLOAD-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1234-ornith35b-night3/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts
@@ -83,2 +83,9 @@
 }
+describe('KS-1234: the /api/v1/nft/upload alias is NOT parsed like its twin - a characterisation of the upload-parser asymmetry', () => {
+  it('RED KS-1234: a non-JSON body on POST /api/nft/upload is refused 400 by the 10 MB upload parser before any proxy, while the same body on POST /api/v1/nft/upload streams unparsed to the nft upstream and answers 200', async () => {
+    const twin = await send('POST', '/api/nft/upload', 'ks1234-not-json');
+    const alias = await send('POST', '/api/v1/nft/upload', 'ks1234-not-json');
+    expect([twin, [alias[0], alias[1].map((h) => h.split(' ')[2])]]).toEqual([[400, []], [200, ['-']]]);
+  }, 15000);
+});
 describe('KS-1234: a JSON create on the /api/v1/documents alias must answer', () => {
```
