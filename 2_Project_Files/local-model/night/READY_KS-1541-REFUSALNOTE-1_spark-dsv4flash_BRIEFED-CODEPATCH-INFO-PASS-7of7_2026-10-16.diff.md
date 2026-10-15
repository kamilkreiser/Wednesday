# READY — KS-1541-REFUSALNOTE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1541_p1/out.md.checker/patch.diff`** (from `ls` at 08:46 2026-10-16; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1541_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1541_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1541_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in info.ts (run 12 vs golden 15 body lines — context, since the change lines are equal) (identical in ks1541-get-info-names-a-gateway-refusal.test.ts); hunk headers identical; APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 08:46 2026-10-16 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1541_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `76698952a75717bbcbc35ace85d08d6758d8844f`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/mcp-server/src/tools/info.ts , Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (product) and `Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/mcp-server/src/tools/info.ts
55	0	Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (7 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 7 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/mcp-server/src/tools/info.ts byte-exact incl. leading whitespace (apply mode strict): OK 7 line(s) byte-exact incl. leading whitespace (of 7; 7 line(s) added by the apply)` [a3i_indent.out: `OK 7 line(s) byte-exact incl. leading whitespace (of 7; 7 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1541: secuura_get_connector_info names a gateway refusal instead of calling it a missing endpoint RED KS-1541 C1: a 503 with an error object relays the status and the gateway message', 'KS-1541: secuura_get_connector_info names a gateway refusal instead of calling it a missing endpoint RED KS-1541 C2: a 403 with a string error relays the status and the string', 'KS-1541: secuura_get_connector_info names a gateway refusal instead of calling it a missing endpoint RED KS-1541 C3: a 500 with no error text relays the status alone']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=5 failed=0 | after: total=11 failed=0` · `NEW reds: []` [baseline_suite.json total=5 failed=0; after_suite.json total=11 failed=0]
- A6 [verbatim]: `PASS A6 whole services/mcp-server suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/mcp-server: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +62/-1 test=src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts` (+55/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `76698952a75717bbcbc35ace85d08d6758d8844f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1541_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1541_p1/KS-1541.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-16_ks_1541_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/mcp-server/src/tools/info.ts
+++ b/Blockchain/Dev/services/mcp-server/src/tools/info.ts
@@ -128,2 +128,8 @@ export function registerInfoTools(server: McpServer) {
         const connector = connectorResult?.ok ? connectorResult.data : null;
+        // KS-1541: any status but 401/404 is the gateway REFUSING on purpose (a 403/503 fail-closed), not a missing endpoint or key.
+        const gatewayError = (connectorResult?.data as unknown as { error?: unknown } | undefined)?.error;
+        const refusalText = typeof gatewayError === 'string' ? gatewayError : typeof (gatewayError as { message?: unknown } | undefined)?.message === 'string' ? (gatewayError as { message: string }).message : '';
+        const connectorNote = connectorResult && !connectorResult.ok && connectorResult.status !== 401 && connectorResult.status !== 404
+          ? `Connector info refused by the gateway (${connectorResult.status})${refusalText ? ': ' + refusalText : ''}`
+          : 'Connector info not available (endpoint may not exist yet or no API key set)';
         const policy = policyResult?.ok ? policyResult.data : null;
@@ -147,3 +153,3 @@ export function registerInfoTools(server: McpServer) {
                       }
-                    : { note: 'Connector info not available (endpoint may not exist yet or no API key set)' },
+                    : { note: connectorNote },
                   verificationPolicy: policy || { note: 'Policy not available' },
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts
@@ -0,0 +1,55 @@
+/**
+ * KS-1541 - secuura_get_connector_info (tools/info.ts) turned ANY non-2xx from the gateway's GET /api/connector/info into
+ * "Connector info not available (endpoint may not exist yet or no API key set)". A deliberate fail-closed refusal (403, 503)
+ * therefore read as a missing endpoint or key. The note now names the refusal with its status and the gateway's own error
+ * text; the old note stays for the cases it is true of (401, 404, a thrown request). Same duck-typed server and stubbed
+ * api-client as ks1232-connector-info-relay.test.ts.
+ */
+import { describe, it, expect, vi } from 'vitest';
+const api = vi.hoisted(() => ({
+  getConnectorInfo: vi.fn(async () => ({ ok: true, status: 200, data: {} })),
+  getVerificationPolicy: vi.fn(async () => ({ ok: false, status: 404, data: {} })),
+  getApiUrl: () => 'http://gateway.ks1541.test',
+  hasApiKey: () => true,
+  listDocuments: vi.fn(),
+  getWorkflowInstance: vi.fn(),
+}));
+vi.mock('../api-client.js', () => api);
+import { registerInfoTools } from '../tools/info.js';
+type ToolResult = { content: Array<{ type: string; text: string }>; isError?: boolean };
+type Handler = () => Promise<ToolResult>;
+const OLD_NOTE = 'Connector info not available (endpoint may not exist yet or no API key set)';
+/** Register the info tools on a duck-typed server, run secuura_get_connector_info, return the parsed JSON text's connector */
+async function connectorOf(): Promise<unknown> {
+  const handlers: Record<string, Handler> = {};
+  const server = { tool: (name: string, _desc: string, _shape: unknown, handler: Handler) => { handlers[name] = handler; } };
+  registerInfoTools(server as never);
+  const result = await handlers['secuura_get_connector_info']();
+  return (JSON.parse(result.content[0].text) as { connector: unknown }).connector;
+}
+describe('KS-1541: secuura_get_connector_info names a gateway refusal instead of calling it a missing endpoint', () => {
+  it('RED KS-1541 C1: a 503 with an error object relays the status and the gateway message', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 503, data: { success: false, error: { code: 'CONNECTOR_POLICY_UNREADABLE', message: 'Connector allow-list configuration could not be read; refusing until it can be read' } } } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info refused by the gateway (503): Connector allow-list configuration could not be read; refusing until it can be read' });
+  });
+  it('RED KS-1541 C2: a 403 with a string error relays the status and the string', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 403, data: { error: 'allow-list malformed' } } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info refused by the gateway (403): allow-list malformed' });
+  });
+  it('RED KS-1541 C3: a 500 with no error text relays the status alone', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 500, data: {} } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info refused by the gateway (500)' });
+  });
+  it('CONTROL KS-1541: a 401 keeps the not-available note', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 401, data: {} } as never);
+    expect(await connectorOf()).toEqual({ note: OLD_NOTE });
+  });
+  it('CONTROL KS-1541: a 404 keeps the not-available note', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 404, data: { error: 'not found' } } as never);
+    expect(await connectorOf()).toEqual({ note: OLD_NOTE });
+  });
+  it('CONTROL KS-1541: a thrown request keeps the not-available note', async () => {
+    api.getConnectorInfo.mockRejectedValueOnce(new Error('ECONNREFUSED'));
+    expect(await connectorOf()).toEqual({ note: OLD_NOTE });
+  });
+});
```
