# READY — KS-1620-RELAYBOUND200-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1620_info/out.md.checker/patch.diff`** (from `ls` at 07:16 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1620_info/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1620_info/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1620_info/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 07:16 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1620_info/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/mcp-server/src/tools/info.ts , Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (product) and `Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/mcp-server/src/tools/info.ts
48	0	Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/mcp-server/src/tools/info.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1620: secuura_get_connector_info bounds the gateway text it relays RED KS-1620 B1: a 503 whose error message is 5000 characters relays only the first 200', 'KS-1620: secuura_get_connector_info bounds the gateway text it relays RED KS-1620 B2: a 403 whose string error is 500 characters relays only the first 200']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=11 failed=0 | after: total=15 failed=0` · `NEW reds: []` [baseline_suite.json total=11 failed=0; after_suite.json total=15 failed=0]
- A6 [verbatim]: `PASS A6 whole services/mcp-server suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/mcp-server: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +50/-1 test=src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts` (+48/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1620_info/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1620_info/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/mcp-server/src/tools/info.ts b/Blockchain/Dev/services/mcp-server/src/tools/info.ts
index d29df8194..1cd978016 100644
--- a/Blockchain/Dev/services/mcp-server/src/tools/info.ts
+++ b/Blockchain/Dev/services/mcp-server/src/tools/info.ts
@@ -131,4 +131,5 @@
         const refusalText = typeof gatewayError === 'string' ? gatewayError : typeof (gatewayError as { message?: unknown } | undefined)?.message === 'string' ? (gatewayError as { message: string }).message : '';
+        // KS-1620: bound the relayed gateway text to 200 characters (a non-gateway upstream, such as a proxy, can send any length).
         const connectorNote = connectorResult && !connectorResult.ok && connectorResult.status !== 401 && connectorResult.status !== 404
-          ? `Connector info refused by the gateway (${connectorResult.status})${refusalText ? ': ' + refusalText : ''}`
+          ? `Connector info refused by the gateway (${connectorResult.status})${refusalText ? ': ' + refusalText.slice(0, 200) : ''}`
           : 'Connector info not available (endpoint may not exist yet or no API key set)';
diff --git a/Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts
new file mode 100644
index 000000000..207ea84da
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts
@@ -0,0 +1,48 @@
+/**
+ * KS-1620 - secuura_get_connector_info (tools/info.ts) relays the gateway's own error text into the note when the gateway
+ * refuses (KS-1541). The text was copied as it came: a 503 carrying a 100,000-character message produced a 100,045-character
+ * note (gate D, finding LOW). The real gateway's texts on this route are short fixed literals, so the case needs an upstream
+ * that is not the gateway (a proxy, a misconfigured SECUURA_API_URL), but the note should not be unbounded. It is now cut to
+ * the first 200 characters of the text. Same duck-typed server and stubbed api-client as ks1541-get-info-names-a-gateway-refusal.test.ts.
+ */
+import { describe, it, expect, vi } from 'vitest';
+const api = vi.hoisted(() => ({
+  getConnectorInfo: vi.fn(async () => ({ ok: true, status: 200, data: {} })),
+  getVerificationPolicy: vi.fn(async () => ({ ok: false, status: 404, data: {} })),
+  getApiUrl: () => 'http://gateway.ks1620.test',
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
+describe('KS-1620: secuura_get_connector_info bounds the gateway text it relays', () => {
+  it('RED KS-1620 B1: a 503 whose error message is 5000 characters relays only the first 200', async () => {
+    const message = 'a'.repeat(200) + 'b'.repeat(4800);
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 503, data: { error: { code: 'X', message } } } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info refused by the gateway (503): ' + 'a'.repeat(200) });
+  });
+  it('RED KS-1620 B2: a 403 whose string error is 500 characters relays only the first 200', async () => {
+    const text = 'c'.repeat(200) + 'd'.repeat(300);
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 403, data: { error: text } } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info refused by the gateway (403): ' + 'c'.repeat(200) });
+  });
+  it('CONTROL KS-1620 B3: a text of exactly 200 characters is relayed whole', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 403, data: { error: 'e'.repeat(200) } } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info refused by the gateway (403): ' + 'e'.repeat(200) });
+  });
+  it('CONTROL KS-1620 B4: a short text is relayed whole', async () => {
+    api.getConnectorInfo.mockResolvedValueOnce({ ok: false, status: 503, data: { error: { message: 'allow-list unreadable' } } } as never);
+    expect(await connectorOf()).toEqual({ note: 'Connector info refused by the gateway (503): allow-list unreadable' });
+  });
+});
```
