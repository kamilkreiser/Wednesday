# READY — KS-1229-SIGNWALLET-R15 (Ornith, briefed, test_only, modify · jest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night3/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night3/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/1229SIGNWALLET-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 12/12 in the diff; reds matched 1/1; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 12/12 in the diff; reds matched 1/1; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night3/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` (modify). `+` lines 12 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 87/87 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `SIGNWALLET` → red exactly ['RED KS-1229 SW1 - a legacy source served as DEGREE still ref']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night3/input.json`. Brief: `night/briefs/KS-1229-SIGNWALLET-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1229-ornith35b-night3/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts
@@ -141,3 +141,15 @@
 const REFUSED = { status: 400, code: 'BAD_REQUEST', saved: 0, stored: null, served: null };
+describe('KS-1229 X-SIGNWALLET-SERVED - sign-wallet compares with the STORED type, not the served label', () => {
+  const signWallet = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata });
+  it('RED KS-1229 SW1 - a legacy source served as DEGREE still refuses metadata.documentType DEGREE', async () => {
+    // KS-1229 (X-SIGNWALLET-SERVED): the new row would be STORED CERTIFICATE and SERVED DEGREE - the relabel KS-1213 closed.
+    seed('CERTIFICATE', { documentType: 'DEGREE' });
+    expect(await signWallet({ documentType: 'DEGREE' })).toEqual(REFUSED);
+  }); // KS-1229 SW1
+  it('control - KS-1229 an ordinary source accepts a metadata.documentType equal to its stored type', async () => {
+    seed('DOCUMENT');
+    expect(await signWallet({ documentType: 'DOCUMENT' })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
+  }); // KS-1229 SW control
+});
 const PRINCIPALS: Array<[string, Record<string, unknown>]> = [['ISSUER_ADMIN', ISSUER], ['SYSTEM_ADMIN', SYSADMIN], ['connector with documents:write', CONNECTOR]];
 const WRITERS: Array<[string, string, (metadata?: Record<string, unknown>) => Record<string, unknown>]> = [
```
