# READY — KS-864-F1009b-R15 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks864-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 00:14 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -48,2 +48,7 @@ function describeUnder(nodeEnv: 'staging' | 'development') { declared old=2 new=7 actual old=1 new=6 ); every line byte-exact` — STRICT APPLY REFUSED: `error: corrupt patch at line 10` (apply with --recount or rewrite the header; the raise seat states which); the run's patch DIFFERS from the drafter's golden at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/864F1009b-R15/out.md.checker/patch.diff` (`cmp` rc 1) — read the diff before raising.

**Held 00:14 2026-09-22 by Wednesday 00:05 seat, source-read: expected_plus 16/16 in the diff; golden DIFFERS by hunk-header form only (context line on the @@ line, --recount class); T3 by --recount after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks864-ornith35b-night2/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts` (modify). `+` lines 16 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 2 == `must_remove`. Green at the tip: 10/10 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F1009` → red exactly ['RED KS-864 F-1009-2 - the served environment.env equals NODE']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` WITH --recount (strict apply refuses: miscounted hunk header — every line byte-exact per the T3 line) — or rewrite the header and assert the blob equals the --recount result at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks864-ornith35b-night2/input.json`. Brief: `night/briefs/KS-864-F1009b-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks864-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts
@@ -48,2 +48,7 @@ function describeUnder(nodeEnv: 'staging' | 'development') {
+  // F-1009-2 titles are LITERAL per block (the checker matches the full rendered title). Under the tamper
+  // env: 'development' only the staging block can tell, so the development block's cell is a CONTROL.
+  const f1009Title = nodeEnv === 'staging'
+    ? 'RED KS-864 F-1009-2 - the served environment.env equals NODE_ENV=staging'
+    : 'KS-864 F-1009-2 control - the served environment.env equals NODE_ENV=development';
   describe(`KS-864 — portal env vars win under NODE_ENV=${nodeEnv}`, () => {
@@ -54,7 +59,8 @@
       vi.resetModules();
       vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('offline in test'); }));
       process.env.NODE_ENV = nodeEnv;
-      for (const p of PORTALS) process.env[p.envVar] = p.value;
+      // F-1009-1: each block sets its OWN values, so a development block that reads a staging-loaded module reds.
+      for (const p of PORTALS) process.env[p.envVar] = p.value + '/' + nodeEnv;
       const router = (await import('../routes/system-status')).default;
       const app = express();
       app.use('/api/system', router);
@@ -71,7 +77,15 @@
     for (const p of PORTALS) {
       it(`🔴 KS-864 — ${p.name} reports ${p.envVar} under NODE_ENV=${nodeEnv}`, async () => {
-        expect((await portalUrls(port))[p.name]).toBe(p.value);
+        expect((await portalUrls(port))[p.name]).toBe(p.value + '/' + nodeEnv);
       });
     }
+    it(f1009Title, async () => {
+      const envBody = await getJson(port, '/api/system/status');
+      expect(envBody.environment.env, 'F-1009-2: the block NODE_ENV reached the route').toBe(nodeEnv);
+    });
+    it(`GREEN KS-864 control - the status body under NODE_ENV=${nodeEnv} carries an environment block`, async () => {
+      const controlBody = await getJson(port, '/api/system/status');
+      expect(typeof controlBody.environment.env, 'control: environment.env is served').toBe('string');
+    });
   });
 }
```
