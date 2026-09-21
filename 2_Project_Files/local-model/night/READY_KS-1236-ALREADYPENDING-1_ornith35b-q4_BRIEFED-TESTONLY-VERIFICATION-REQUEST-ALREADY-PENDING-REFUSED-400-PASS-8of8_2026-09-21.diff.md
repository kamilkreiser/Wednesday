# READY — KS-1236-ALREADYPENDING-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1236-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 10:03 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1236-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_siblings-1236-1006-drafter/ALREADYPENDING/out.md.checker/patch.diff` rc 0, Wednesday (the 08:4x seat)).

**Held 10:03 2026-09-21 by Wednesday (the 08:4x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1236-ornith35b-night2/out.md.checker`, not typed).** Tip `7be81d5c9b109959b559e03652fb092c12de58e8`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` (modify). `+` lines 14 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 16/16 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `GUARDTOLOG` → red exactly ['RED KS-1236: a request for a DIFFERENT target while one is a', 'RED KS-1236: a second request while one is already PENDING i']
- `SAMETARGETONLY` → red exactly ['RED KS-1236: a request for a DIFFERENT target while one is a']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1236-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1236-ALREADYPENDING-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1236-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
@@ -172,4 +172,18 @@
     const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
     expect([r.status, (r.json.data as Row | undefined)?.status, dbQuery.mock.calls.length]).toEqual([200, 'PENDING', 0]);
   });
+  it('RED KS-1236: a second request while one is already PENDING is refused 400 with the exact body A verification request is already pending - one store read, no INSERT', async () => {
+    user('u-1236-pend');
+    pendingRow('vr-1236-pend', 'u-1236-pend');
+    state.caller = { userId: 'u-1236-pend', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    expect([r.status, r.json, state.rows.size, dbQuery.mock.calls.length]).toEqual([400, { success: false, error: { code: 'BAD_REQUEST', message: 'A verification request is already pending' } }, 1, 1]);
+  });
+  it('RED KS-1236: a request for a DIFFERENT target while one is already PENDING is refused the same way - the guard is on any pending request, not on a duplicate target', async () => {
+    user('u-1236-pend2');
+    pendingRow('vr-1236-pend2', 'u-1236-pend2');
+    state.caller = { userId: 'u-1236-pend2', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'HIGH' });
+    expect([r.status, r.json, state.rows.size, dbQuery.mock.calls.length]).toEqual([400, { success: false, error: { code: 'BAD_REQUEST', message: 'A verification request is already pending' } }, 1, 1]);
+  });
   it('RED KS-1236: a target level EQUAL to the current level is refused 400 BAD_REQUEST before any store read or INSERT', async () => {
```
