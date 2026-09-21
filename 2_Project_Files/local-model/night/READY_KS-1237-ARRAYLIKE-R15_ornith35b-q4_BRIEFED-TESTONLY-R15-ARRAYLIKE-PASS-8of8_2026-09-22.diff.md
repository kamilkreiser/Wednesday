# READY — KS-1237-ARRAYLIKE-R15 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1237-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch DIFFERS from the drafter's golden at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1237ARRAYLIKE-R15/out.md.checker/patch.diff` (`cmp` rc 1) — read the diff before raising.

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 8/8 in the diff; reds matched 1/1; golden DIFFERS (hunk-header form only; +/- body identical) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1237-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts` (modify). `+` lines 8 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 1 == `must_remove`. Green at the tip: 10/10 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `ARRAYLIKE` → red exactly ['RED KS-1237 AL1 - an array-like allow-list is not a list: 40']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1237-ornith35b-night/input.json`. Brief: `night/briefs/KS-1237-ARRAYLIKE-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1237-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts
@@ -243,3 +243,10 @@
+  it('RED KS-1237 AL1 - an array-like allow-list is not a list: 403 FORBIDDEN for a named type and an untyped body', async () => {
+    RAN.add('non-array an array-like');
+    connectorAllowedTypes = { 0: 'SSD_DOCUMENT', length: 1 };
+    const named = await createDocumentWithBody(CONNECTOR, { documentType: 'DOCUMENT' });
+    const untyped = await createDocumentWithBody(CONNECTOR, {});
+    expect([named.status, named.body?.error?.code, untyped.status, untyped.body?.error?.code]).toEqual([403, 'FORBIDDEN', 403, 'FORBIDDEN']);
+  }); // KS-1237 AL1
   it('control: an ARRAY allow-list ["SSD_DOCUMENT"] admits SSD_DOCUMENT and refuses DOCUMENT, as before', async () => {
     RAN.add('array control');
     connectorAllowedTypes = ['SSD_DOCUMENT'];
@@ -287,5 +294,5 @@
     expect([...RAN].sort()).toEqual([
       'string vs DOCUMENT', 'non-array the string "SSD_DOCUMENT"', 'non-array an object', 'non-array an empty string',
-      'array control', 'unrestricted control', 'precedence admits documentType', 'precedence refuses documentType',
+      'array control', 'unrestricted control', 'precedence admits documentType', 'precedence refuses documentType', 'non-array an array-like',
     ].sort());
   });
```
