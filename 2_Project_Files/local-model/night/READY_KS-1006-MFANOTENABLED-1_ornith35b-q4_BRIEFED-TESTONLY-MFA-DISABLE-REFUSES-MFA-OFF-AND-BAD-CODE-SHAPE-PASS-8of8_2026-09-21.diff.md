# READY — KS-1006-MFANOTENABLED-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1006-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 10:03 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1006-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_siblings-1236-1006-drafter/MFANOTENABLED/out.md.checker/patch.diff` rc 0, Wednesday (the 08:4x seat)).

**Held 10:03 2026-09-21 by Wednesday (the 08:4x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1006-ornith35b-night2/out.md.checker`, not typed).** Tip `7be81d5c9b109959b559e03652fb092c12de58e8`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` (modify). `+` lines 18 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 16/16 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `LENGTHDROPPED` → red exactly ['RED KS-1006: with MFA enabled and a secret stored, a code th']
- `MFAOFFIDEMPOTENT` → red exactly ['RED KS-1006: with MFA NOT enabled, a well-formed six-charact']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1006-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1006-MFANOTENABLED-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1006-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
@@ -126,4 +126,22 @@
     const r = await call('POST', '/me/mfa/disable', { code: 'abcdef' });
     expect([r.status, code(r.json), (r.json.error as Row | undefined)?.message]).toEqual([400, 'BAD_REQUEST', 'Invalid verification code']);
   });
+  it('RED KS-1006: with MFA NOT enabled, a well-formed six-character code is refused 400 with the exact body MFA is not enabled - the code is never looked at', async () => {
+    user('u-1006-off');
+    state.caller = { userId: 'u-1006-off', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/mfa/disable', { code: 'abcdef' });
+    expect([r.status, r.json]).toEqual([400, { success: false, error: { code: 'BAD_REQUEST', message: 'MFA is not enabled' } }]);
+  });
+  it('RED KS-1006: with MFA enabled and a secret stored, a code that is missing, not a string, five characters or seven characters is refused 400 with the exact body Valid 6-digit verification code required - before any TOTP check', async () => {
+    user('u-1006-shape');
+    Object.assign(state.users.get('u-1006-shape') as Record<string, unknown>, { mfaEnabled: true, mfaSecret: 'JBSWY3DPEHPK3PXP' });
+    state.caller = { userId: 'u-1006-shape', role: 'USER', tenantId: 'tenant-default' };
+    const outcomes: unknown[] = [];
+    for (const body of [{}, { code: 123456 }, { code: '12345' }, { code: '1234567' }]) {
+      const r = await call('POST', '/me/mfa/disable', body);
+      outcomes.push([r.status, r.json]);
+    }
+    const refused = [400, { success: false, error: { code: 'BAD_REQUEST', message: 'Valid 6-digit verification code required' } }];
+    expect(outcomes).toEqual([refused, refused, refused, refused]);
+  });
 });
```
