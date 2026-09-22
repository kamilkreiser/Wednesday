# READY — KS-851-R18-QUOTEDNAME-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks851-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 06:37 2026-09-23). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -219,3 +219,8 @@ declared old=3 new=8 actual old=3 new=9 ); every line byte-exact` — STRICT APPLY REFUSED: `error: corrupt patch at line 13` (apply with --recount or rewrite the header; the raise seat states which); golden not located — no byte-identity claim is made.

**Held 06:37 2026-09-23 by Wednesday 06:0x seat 2026-09-23 after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks851-ornith35b-night/out.md.checker`, not typed).** Tip `2bc5ccf63b8c40911afb568b03cace066238ffcf`. Touches ONE file: `Blockchain/Dev/services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts` (modify). `+` lines 6 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 10/10 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `QUOTEDWRITE` → red exactly ['KS-851 G-4 - a quoted or schema-qualified table name is a wr']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` WITH --recount (strict apply refuses: miscounted hunk header — every line byte-exact per the T3 line) — or rewrite the header and assert the blob equals the --recount result at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks851-ornith35b-night/input.json`. Brief: `night/briefs/KS-851-R18-QUOTEDNAME-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks851-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks386-no-image-payload-written.test.ts
@@ -219,3 +219,8 @@
     expect(deletes.length).toBe(2);
   });
+  it('KS-851 G-4 - a quoted or schema-qualified table name is a write path too', () => {
+    // The matcher in writeStatements requires the BARE name, so INSERT INTO "svc_kyc_images"
+    // and UPDATE public.svc_kyc_images are invisible to it (re-gate G-4: 0 failed / 26, twice).
+    const anySpelling = stripComments(SRC).match(/(INSERT[ ]+INTO|UPDATE)[ ]+(?:"?public"?[.])?"?svc_kyc_images"?/gi) ?? [];
+    expect(anySpelling.map((w) => w.toUpperCase())).toEqual(['INSERT INTO SVC_KYC_IMAGES']);
+  });
 });
```
