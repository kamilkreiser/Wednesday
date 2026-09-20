# READY — KS-1232-MCPINFORAWECHO-1 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night3/out.md.checker/patch.diff`** (from `ls` at 05:36 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night3/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck-b/MCPINFORAWECHO/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 05:36 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night3/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-connector-info-relay.test.ts` (new). `+` lines 37 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 2/2 cells. Tampers (2), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `RELAYDROPPED` → red exactly ['RED KS-1232: a gateway answer with allowedDocumentTypes: [] ']
- `RELAYWRONGFIELD` → red exactly ['RED KS-1232: a gateway answer with allowedDocumentTypes: [] ']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night3/input.json`. Brief: `night/briefs/KS-1232-MCPINFORAWECHO-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1232-ornith35b-night3/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-connector-info-relay.test.ts
@@ -0,0 +1,37 @@
+/**
+ * KS-1232 - the MCP relay of the gateway's connector info. secuura_get_connector_info (tools/info.ts) answers a JSON
+ * text whose connector.allowedDocumentTypes is the GATEWAY's /api/connector/info answer relayed as it is - the tool
+ * has no default of its own. The #1106-#1111 gate found nothing pins the relay (mcp-server has one placeholder test).
+ * registerInfoTools is driven with a duck-typed server that captures the tool handlers, and api-client is stubbed.
+ * A characterisation pin of TODAY's relay: a changed gateway answer must be re-pinned here on purpose.
+ */
+import { describe, it, expect, vi } from 'vitest';
+const api = vi.hoisted(() => ({
+  getConnectorInfo: vi.fn(async () => ({ ok: true, status: 200, data: { id: 'conn-ks1232', name: 'ks1232', scopes: ['register'], allowedDocumentTypes: [], workflowPolicy: 'enforce', rateLimit: 100 } })),
+  getVerificationPolicy: vi.fn(async () => ({ ok: false, status: 404, data: {} })),
+  getApiUrl: () => 'http://gateway.ks1232.test',
+  hasApiKey: () => true,
+  listDocuments: vi.fn(),
+  getWorkflowInstance: vi.fn(),
+}));
+vi.mock('../api-client.js', () => api);
+import { registerInfoTools } from '../tools/info.js';
+type ToolResult = { content: Array<{ type: string; text: string }>; isError?: boolean };
+type Handler = () => Promise<ToolResult>;
+/** Register the info tools on a duck-typed server, run secuura_get_connector_info, return the parsed JSON text's connector */
+async function connectorOf(): Promise<unknown> {
+  const handlers: Record<string, Handler> = {};
+  const server = { tool: (name: string, _desc: string, _shape: unknown, handler: Handler) => { handlers[name] = handler; } };
+  registerInfoTools(server as never);
+  const result = await handlers['secuura_get_connector_info']();
+  return (JSON.parse(result.content[0].text) as { connector: unknown }).connector;
+}
+describe('KS-1232: secuura_get_connector_info relays the gateway connector info as it is', () => {
+  it('RED KS-1232: a gateway answer with allowedDocumentTypes: [] is relayed with allowedDocumentTypes: [] and every other field intact', async () => {
+    expect(await connectorOf()).toEqual({ id: 'conn-ks1232', name: 'ks1232', scopes: ['register'], allowedDocumentTypes: [], workflowPolicy: 'enforce', rateLimit: 100 });
+  });
+  it('CONTROL: when the gateway does not answer ok the tool relays the not-available note instead of a connector', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 401, data: {} } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info not available (endpoint may not exist yet or no API key set)' });
+  });
+});
```
