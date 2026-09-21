# READY — KS-1229-UNTYPEDSRCb-R15 (Ornith, briefed, test_only, modify · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1229-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 00:14 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1229-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1229UNTYPEDSRCb-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, source-read: expected_plus 13/13 in the diff, titles = U1 red + control; golden cmp IDENTICAL).

**Held 00:14 2026-09-22 by Wednesday 00:05 seat, source-read: expected_plus 13/13 in the diff, titles = U1 red + control; golden cmp IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1229-ornith35b-night2/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` (modify). `+` lines 13 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 1 == `must_remove`. Green at the tip: 87/87 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `UNTYPEDSRC` → red exactly ['RED KS-1229 U1 - an untyped source is refused a relabel, not']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1229-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1229-UNTYPEDSRCb-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1229-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -224,3 +224,15 @@
     expect(await create({ data: { title: 'nb', documentType: 'DOCUMENT' } })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
   });
-});
+}); // KS-1202 create guard
+describe('KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP - the sign-cert guard still refuses when the source has no type', () => {
+  const signCert = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-cert', { metadata });
+  it('RED KS-1229 U1 - an untyped source is refused a relabel, nothing saved', async () => {
+    // KS-1229 (Q-SIGNCERT-UNTYPED-SOURCE-SKIP): an untyped in-memory source must not skip the guard.
+    seed(undefined as unknown as string);
+    expect(await signCert({ documentType: 'DEGREE' })).toEqual(REFUSED);
+  }); // KS-1229 U1
+  it('control - KS-1229 a typed source is still refused a differing relabel', async () => {
+    seed('DOCUMENT');
+    expect(await signCert({ documentType: 'PROPERTY_DEED' })).toEqual(REFUSED);
+  }); // KS-1229 U control
+}); // KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP
```
