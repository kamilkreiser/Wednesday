# READY — KS-1229-VERSIONTRIM-R15 (Ornith, briefed, test_only, modify · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night4/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night4/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1229VERSIONTRIM-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 12/12 in the diff; reds matched 1/1; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 12/12 in the diff; reds matched 1/1; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night4/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` (modify). `+` lines 12 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 87/87 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `VERSIONTRIM` → red exactly ['RED KS-1229 VT1 - a trailing-space carrier is refused, never']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night4/input.json`. Brief: `night/briefs/KS-1229-VERSIONTRIM-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night4/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -123,3 +123,15 @@
 const SOURCE_ID = 'doc-src-1213';
+describe('KS-1229 X-VERSION-TRIM - the /version guard compares EXACTLY, so a padded carrier is refused', () => {
+  const version = (documentType: string) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/version', { action: 'watermark', newContentHash: HASH, metadata: { documentType } });
+  it('RED KS-1229 VT1 - a trailing-space carrier is refused, never trimmed into a match', async () => {
+    // KS-1229 (X-VERSION-TRIM): trimming would store DOCUMENT and serve the padded label - a relabel by invisible whitespace.
+    seed('DOCUMENT');
+    expect(await version('DOCUMENT ')).toEqual(REFUSED);
+  }); // KS-1229 VT1
+  it('control - KS-1229 the exact carrier is accepted and served as that type', async () => {
+    seed('DOCUMENT');
+    expect(await version('DOCUMENT')).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
+  }); // KS-1229 VT control
+});
 function seed(type: string, data: Record<string, unknown> = {}) {
   store.set(SOURCE_ID, { id: SOURCE_ID, type, status: 'draft', owner: { id: ISSUER.userId }, data: { title: 'src', ...data }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-09-17T00:00:00Z', updatedAt: '2026-09-17T00:00:00Z' });
```
