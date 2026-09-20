# READY — KS-1232-HTTPSERVERINFOEMPTY-1 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 05:36 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck-b/HTTPSERVERINFOEMPTY/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 05:36 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night2/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-generate-package-doctypes-default.test.ts` (new). `+` lines 50 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 2/2 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `RAWDOCTYPES` → red exactly ['RED KS-1232: allowedDocumentTypes "", 0 and false each reach']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1232-HTTPSERVERINFOEMPTY-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night2/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-generate-package-doctypes-default.test.ts
@@ -0,0 +1,50 @@
+/**
+ * KS-1232 - the SECOND site that shapes allowedDocumentTypes: the REST mirror's POST /generate-package (http-server.ts)
+ * hands the package generator allowedDocumentTypes || [] (http-server.ts:258), so a stored "", 0 or false becomes [] and a stored list
+ * passes through. The #1106-#1111 gate found nothing pins it (mcp-server has one placeholder test). The real
+ * http-server module is imported with MCP_HTTP_PORT=0 (its top-level listen then binds an ephemeral port, captured by
+ * wrapping http.createServer), the package generator is stubbed to RECORD its config, and the real express stack is
+ * driven over loopback. A characterisation pin of TODAY's default at this site.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import type { AddressInfo } from 'net';
+const rec = vi.hoisted(() => ({ configs: [] as Array<Record<string, unknown>> }));
+vi.mock('../package-generator.js', () => ({
+  generatePackage: vi.fn(async (config: Record<string, unknown>, output: { end: (s: string) => void }) => { rec.configs.push(config); output.end('zip'); }),
+}));
+vi.mock('../api-client.js', () => ({
+  registerDocument: vi.fn(), verifyDocument: vi.fn(), listDocuments: vi.fn(), getWorkflowInstance: vi.fn(), getConnectorInfo: vi.fn(), getVerificationPolicy: vi.fn(),
+}));
+const servers: http.Server[] = [];
+const realCreateServer = http.createServer;
+let baseUrl = '';
+beforeAll(async () => {
+  vi.stubEnv('MCP_HTTP_PORT', '0');
+  vi.stubEnv('NODE_ENV', 'test');
+  (http as unknown as { createServer: unknown }).createServer = (...args: unknown[]) => { const s = (realCreateServer as (...a: unknown[]) => http.Server)(...args); servers.push(s); return s; };
+  await import('../http-server.js');
+  const server = servers[0];
+  if (!server.listening) await new Promise<void>((r) => server.once('listening', () => r()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+}, 30000);
+afterAll(async () => {
+  (http as unknown as { createServer: unknown }).createServer = realCreateServer;
+  for (const s of servers) { s.closeAllConnections(); await new Promise<void>((r) => s.close(() => r())); }
+  vi.unstubAllEnvs();
+});
+/** POST /generate-package with the given allowedDocumentTypes; returns [status, the allowedDocumentTypes the generator received] */
+async function generate(allowedDocumentTypes: unknown): Promise<[number, unknown]> {
+  const before = rec.configs.length;
+  const res = await fetch(baseUrl + '/generate-package', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ agentType: 'generic_http', apiKey: 'sk_ks1232', allowedDocumentTypes }) });
+  await res.arrayBuffer();
+  return [res.status, rec.configs.length === before + 1 ? rec.configs[before].allowedDocumentTypes : 'generatePackage not called once'];
+}
+describe('KS-1232: POST /generate-package defaults a falsy allowedDocumentTypes to [] and passes a list through', () => {
+  it('RED KS-1232: allowedDocumentTypes "", 0 and false each reach the package generator as [] with status 200', async () => {
+    expect([await generate(''), await generate(0), await generate(false)]).toEqual([[200, []], [200, []], [200, []]]);
+  });
+  it('CONTROL: a stored list ["contract"] reaches the package generator unchanged with status 200', async () => {
+    expect(await generate(['contract'])).toEqual([200, ['contract']]);
+  });
+});
```
