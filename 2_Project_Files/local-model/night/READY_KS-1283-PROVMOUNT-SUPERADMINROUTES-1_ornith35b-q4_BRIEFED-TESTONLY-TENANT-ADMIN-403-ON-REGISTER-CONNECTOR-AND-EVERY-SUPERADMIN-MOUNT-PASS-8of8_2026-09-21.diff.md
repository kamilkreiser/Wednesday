# READY — KS-1283-PROVMOUNT-SUPERADMINROUTES-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1283-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 09:28 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1283-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1112rows-drafter-precheck/PROVMOUNT-SUPERADMINROUTES/out.md.checker/patch.diff` rc 0, Wednesday (the 08:4x seat)).

**Held 09:28 2026-09-21 by Wednesday (the 08:4x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1283-ornith35b-night2/out.md.checker`, not typed).** Tip `7be81d5c9b109959b559e03652fb092c12de58e8`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts` (modify). `+` lines 26 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 41/41 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `PROVMOUNTUNGUARDED` → red exactly ['RED KS-1283: POST /api/platform/organizations/register-conne']
- `WIDENROLES` → red exactly ['RED KS-1283: POST /api/platform/organizations/register-conne', 'RED KS-1283: a tenant ADMIN JWT is refused 403 on every requ', 'RED: a tenant ADMIN JWT is refused 403 on GET /api/platform/']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1283-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1283-PROVMOUNT-SUPERADMINROUTES-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1283-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts
@@ -455,4 +455,30 @@
     const r = await post(gateway!.url, PATH, { 'x-api-key': OK_KEY }, registerBody());
     expect(JSON.stringify([r.status, registerBearers(r)])).toBe(JSON.stringify([201, allThree('connector-jwt')]));
   });
+  function tenantAdminJwt(): string {
+    return 'Bearer ' + jwt.sign({ userId: 'u-ks1283-admin', email: 'ks1283-admin@secuura.io', role: 'ADMIN', verificationLevel: 'email', authMethod: 'email', tenantId: TENANT, sessionId: 'ks1215-live' }, PRIV, { algorithm: 'RS256', expiresIn: '10m' });
+  }
+  it('RED KS-1283: POST /api/platform/organizations/register-connector with a tenant ADMIN bearer answers 403 FORBIDDEN and forwards nothing', async () => {
+    const r = await post(gateway!.url, PATH, { authorization: tenantAdminJwt() }, registerBody());
+    expect([r.status, r.code, r.forwarded.map((h) => h.url)]).toEqual([403, 'FORBIDDEN', []]);
+  });
+  it('RED KS-1283: a tenant ADMIN JWT is refused 403 on every requireSuperAdmin mount and nothing is forwarded', async () => {
+    vi.stubEnv('PLATFORM_DATABASE_URL', 'postgres://ks1283:ks1283@127.0.0.1:1/ks1283');
+    const pairs: Array<[string, string]> = [
+      ['POST', '/api/platform/tenants'], ['GET', '/api/platform/tenants/ks1283-t1'], ['PATCH', '/api/platform/tenants/ks1283-t1'],
+      ['PATCH', '/api/platform/tenants/ks1283-t1/status'], ['DELETE', '/api/platform/tenants/ks1283-t1'], ['GET', '/api/platform/audit-log'],
+      ['POST', '/api/platform/tenant-key'], ['DELETE', '/api/platform/tenant-key/ks1283-t1'], ['GET', '/api/platform/tenant-key/ks1283-t1/status'],
+      ['GET', '/api/platform/templates/document-types'], ['GET', '/api/platform/templates/workflows'], ['POST', '/api/platform/templates/clone-to-tenant'],
+    ];
+    const outcomes: unknown[] = [];
+    for (const [method, path] of pairs) {
+      const n = hits.length;
+      const body = method === 'GET' || method === 'DELETE' ? undefined : JSON.stringify({ name: 'ks1283' });
+      const r = await fetch(gateway!.url + path, { method, headers: body ? { 'content-type': 'application/json', authorization: tenantAdminJwt() } : { authorization: tenantAdminJwt() }, body });
+      const code = ((await r.json().catch(() => ({}))) as any)?.error?.code ?? null;
+      await new Promise((w) => setTimeout(w, 50));
+      outcomes.push([method + ' ' + path, r.status, code, hits.slice(n).map((h) => h.url)]);
+    }
+    expect(outcomes).toEqual(pairs.map(([method, path]) => [method + ' ' + path, 403, 'FORBIDDEN', []]));
+  });
 });
```
