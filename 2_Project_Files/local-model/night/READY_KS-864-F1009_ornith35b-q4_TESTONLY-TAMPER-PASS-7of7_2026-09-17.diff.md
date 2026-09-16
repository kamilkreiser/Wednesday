# READY — KS-864 F-1009-1 + F-1009-2 (TEST-ONLY, MODIFY-IN-PLACE ks864c-portal-env-vars.test.ts: per-block env values so vi.resetModules is pinned; a served environment.env == NODE_ENV cell + a control per block) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (03:59:39). Held by Wednesday at 04:14 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks864f1009-ornith35b-night
# Source read by me (Wednesday): the model's 13 `+` / 2 `-` lines IDENTICAL in sequence to the brief's two hunks (a mutated-copy control unequal); apply STRICT; A4 under the system-status.ts:437 tamper 1 red by assertion / 10 run, controls green; A6 api-gateway no new red; A7 tsc rc 0.
# NOT GRADED BY THE CHECKER: F-1009-1 (a test-side vi.resetModules property) — graded in the brief's premises (Q-reset: OLD 6/6 green → golden 3 red). The input was built with the builder's PR-attachment refusal bypassed (both KS-864 PRs merged; IMPROVEMENTS 03:52).
# PR NOTES: "Part of KS-864 (F-1009-1, F-1009-2)" — never Closes; test-only → tier 2; KS-864 stays open (Backlog).

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts
@@ -54,7 +54,8 @@ function describeUnder(nodeEnv: 'staging' | 'development') {
       vi.resetModules();
       vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('offline in test'); }));
       process.env.NODE_ENV = nodeEnv;
-      for (const p of PORTALS) process.env[p.envVar] = p.value;
+      // F-1009-1: each block sets its OWN values, so a development block that reads a staging-loaded module reds.
+      for (const p of PORTALS) process.env[p.envVar] = p.value + '/' + nodeEnv;
       const router = (await import('../routes/system-status')).default;
       const app = express();
       app.use('/api/system', router);
@@ -70,8 +71,18 @@ function describeUnder(nodeEnv: 'staging' | 'development') {
 
     for (const p of PORTALS) {
       it(`🔴 KS-864 — ${p.name} reports ${p.envVar} under NODE_ENV=${nodeEnv}`, async () => {
-        expect((await portalUrls(port))[p.name]).toBe(p.value);
+        expect((await portalUrls(port))[p.name]).toBe(p.value + '/' + nodeEnv);
       });
     }
+
+    it(`🔴 KS-864 F-1009-2 — the served environment.env equals NODE_ENV=${nodeEnv}`, async () => {
+      const envBody = await getJson(port, '/api/system/status');
+      expect(envBody.environment.env, 'F-1009-2: the block NODE_ENV reached the route').toBe(nodeEnv);
+    });
+
+    it(`🟢 KS-864 control — the status body under NODE_ENV=${nodeEnv} carries an environment block`, async () => {
+      const controlBody = await getJson(port, '/api/system/status');
+      expect(typeof controlBody.environment.env, 'control: environment.env is served').toBe('string');
+    });
   });
 }
```
