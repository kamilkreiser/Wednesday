# READY — KS-1928-KS-1928-O130-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text/out.md.checker/patch.diff`** (from `ls` at 09:20 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:20 2026-11-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `07d4218e9776a5eced016f16330983c900e94fb3`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/mcp-server/src/tools/info.ts } + { Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (product) and `Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	6	Blockchain/Dev/services/mcp-server/src/tools/info.ts
105	0	Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (9 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: info.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/mcp-server/src/tools/info.ts`; test(s): `Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/mcp-server/src/tools/info.ts 9 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts 105 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1928 the info tools answer a constant and log the real error RED ks1928 R1 secuura_list_documents: a thrown Error answers the constant with no leak; the log has the text', 'KS-1928 the info tools answer a constant and log the real error RED ks1928 R2 secuura_check_workflow: a thrown Error answers the constant with no leak; the log has the text', 'KS-1928 the info tools answer a constant and log the real error RED ks1928 R3 secuura_get_connector_info: a throw outside the guarded calls answers the constant with no leak; the log has the text', 'KS-1928 the info tools answer a constant and log the real error RED ks1928 R4 a thrown non-Error string is never echoed and is logged by its type only']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=131 failed=0 | after: total=137 failed=0` · `NEW reds: []` [baseline_suite.json total=131 failed=0; after_suite.json total=137 failed=0]
- A6 [verbatim]: `PASS A6 whole services/mcp-server suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/mcp-server: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/mcp-server/src/tools/info.ts` (+9/-6 per numstat.out) and the test file `Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts` (+105/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/mcp-server/src/tools/info.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `07d4218e9776a5eced016f16330983c900e94fb3` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1928_o130_p1_mcp_info_tools_never_return_the_thrown_text/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/mcp-server/src/tools/info.ts b/Blockchain/Dev/services/mcp-server/src/tools/info.ts
--- a/Blockchain/Dev/services/mcp-server/src/tools/info.ts
+++ b/Blockchain/Dev/services/mcp-server/src/tools/info.ts
@@ -55,9 +55,10 @@ export function registerInfoTools(server: McpServer) {
           ],
         };
       } catch (err: unknown) {
-        const message = err instanceof Error ? err.message : String(err);
+        // KS-1928: the thrown text must not reach the MCP client; it goes to stderr (stdout is the stdio JSON-RPC channel), a non-Error by its type only.
+        console.error('[mcp-server] secuura_list_documents failed:', err instanceof Error ? err.message : typeof err);
         return {
-          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],
+          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: 'An unexpected error occurred' }) }],
           isError: true,
         };
       }
@@ -105,9 +106,10 @@ export function registerInfoTools(server: McpServer) {
           ],
         };
       } catch (err: unknown) {
-        const message = err instanceof Error ? err.message : String(err);
+        // KS-1928: the thrown text must not reach the MCP client; it goes to stderr (stdout is the stdio JSON-RPC channel), a non-Error by its type only.
+        console.error('[mcp-server] secuura_check_workflow failed:', err instanceof Error ? err.message : typeof err);
         return {
-          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],
+          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: 'An unexpected error occurred' }) }],
           isError: true,
         };
       }
@@ -163,9 +165,10 @@ export function registerInfoTools(server: McpServer) {
           ],
         };
       } catch (err: unknown) {
-        const message = err instanceof Error ? err.message : String(err);
+        // KS-1928: the thrown text must not reach the MCP client; it goes to stderr (stdout is the stdio JSON-RPC channel), a non-Error by its type only.
+        console.error('[mcp-server] secuura_get_connector_info failed:', err instanceof Error ? err.message : typeof err);
         return {
-          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],
+          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: 'An unexpected error occurred' }) }],
           isError: true,
         };
       }
diff --git a/Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1928-info-tools-never-return-the-thrown-text.test.ts
@@ -0,0 +1,105 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+import type { MockInstance } from 'vitest';
+
+// KS-1928 (piece 1 of 3: tools/info.ts): three MCP info tools returned the thrown error's own message to the client inside an isError result.
+// The text is whatever the platform call threw (a network error naming a host and port, a file-system error naming a path). Each catch now
+// logs the real text with console.error (stderr: stdout is the stdio JSON-RPC channel) and answers the constant `An unexpected error occurred`.
+// A thrown non-Error is logged by its TYPE only. Harness: the real registerInfoTools on a duck-typed server, api-client stubbed.
+const api = vi.hoisted(() => ({
+  listDocuments: vi.fn(),
+  getWorkflowInstance: vi.fn(),
+  getConnectorInfo: vi.fn(async () => ({ ok: false, status: 404, data: {} })),
+  getVerificationPolicy: vi.fn(async () => ({ ok: false, status: 404, data: {} })),
+  getApiUrl: vi.fn(() => 'http://gateway.ks1928.test'),
+  hasApiKey: () => true,
+}));
+vi.mock('../api-client.js', () => api);
+import { registerInfoTools } from '../tools/info.js';
+
+type ToolResult = { content: Array<{ type: string; text: string }>; isError?: boolean };
+type Handler = (args: Record<string, unknown>) => Promise<ToolResult>;
+
+const CONSTANT = 'An unexpected error occurred';
+const LEAK = 'connect ECONNREFUSED 10.1.2.3:5432 while reading /srv/secuura/keys/platform.pem';
+let errSpy: MockInstance<typeof console.error>;
+
+async function run(tool: string, args: Record<string, unknown> = {}): Promise<ToolResult> {
+  const handlers: Record<string, Handler> = {};
+  const server = { tool: (name: string, _desc: string, _shape: unknown, handler: Handler) => { handlers[name] = handler; } };
+  registerInfoTools(server as never);
+  return handlers[tool](args);
+}
+
+function logged(): string {
+  return errSpy.mock.calls.map((a) => a.map((x) => (typeof x === 'string' ? x : '<<non-string:' + typeof x + '>>')).join(' ')).join('\n');
+}
+
+beforeEach(() => {
+  api.listDocuments.mockReset();
+  api.getWorkflowInstance.mockReset();
+  api.getApiUrl.mockReset();
+  api.getApiUrl.mockImplementation(() => 'http://gateway.ks1928.test');
+  errSpy = vi.spyOn(console, 'error').mockImplementation(() => undefined);
+});
+
+afterEach(() => {
+  errSpy.mockRestore();
+});
+
+describe('KS-1928 the info tools answer a constant and log the real error', () => {
+  it('RED ks1928 R1 secuura_list_documents: a thrown Error answers the constant with no leak; the log has the text', async () => {
+    api.listDocuments.mockRejectedValueOnce(new Error(LEAK));
+    const r = await run('secuura_list_documents', {});
+    expect(r.isError).toBe(true);
+    expect(JSON.parse(r.content[0].text)).toEqual({ success: false, error: CONSTANT });
+    expect(r.content[0].text).not.toContain('ECONNREFUSED');
+    expect(r.content[0].text).not.toContain('platform.pem');
+    expect(logged()).toContain(LEAK);
+  });
+
+  it('RED ks1928 R2 secuura_check_workflow: a thrown Error answers the constant with no leak; the log has the text', async () => {
+    api.getWorkflowInstance.mockRejectedValueOnce(new Error(LEAK));
+    const r = await run('secuura_check_workflow', { workflowInstanceId: 'wf-1' });
+    expect(r.isError).toBe(true);
+    expect(JSON.parse(r.content[0].text)).toEqual({ success: false, error: CONSTANT });
+    expect(r.content[0].text).not.toContain('ECONNREFUSED');
+    expect(logged()).toContain(LEAK);
+  });
+
+  it('RED ks1928 R3 secuura_get_connector_info: a throw outside the guarded calls answers the constant with no leak; the log has the text', async () => {
+    api.getApiUrl.mockImplementation(() => {
+      throw new Error(LEAK);
+    });
+    const r = await run('secuura_get_connector_info', {});
+    expect(r.isError).toBe(true);
+    expect(JSON.parse(r.content[0].text)).toEqual({ success: false, error: CONSTANT });
+    expect(r.content[0].text).not.toContain('ECONNREFUSED');
+    expect(logged()).toContain(LEAK);
+  });
+
+  it('RED ks1928 R4 a thrown non-Error string is never echoed and is logged by its type only', async () => {
+    api.listDocuments.mockRejectedValueOnce('S3CR3T-STRING-MARKER');
+    const r = await run('secuura_list_documents', {});
+    expect(r.isError).toBe(true);
+    expect(JSON.parse(r.content[0].text)).toEqual({ success: false, error: CONSTANT });
+    expect(r.content[0].text).not.toContain('S3CR3T-STRING-MARKER');
+    expect(logged()).not.toContain('S3CR3T-STRING-MARKER');
+    expect(logged()).toContain('string');
+  });
+
+  it('control ks1928 C1 a non-2xx reply from the platform keeps its own HTTP-status answer and logs nothing', async () => {
+    api.listDocuments.mockResolvedValueOnce({ ok: false, status: 500, data: { error: 'upstream' } });
+    const r = await run('secuura_list_documents', {});
+    expect(r.isError).toBe(true);
+    expect(JSON.parse(r.content[0].text)).toEqual({ success: false, error: 'HTTP 500', data: { error: 'upstream' } });
+    expect(errSpy).not.toHaveBeenCalled();
+  });
+
+  it('control ks1928 C2 a successful list still answers its documents and logs nothing', async () => {
+    api.listDocuments.mockResolvedValueOnce({ ok: true, status: 200, data: { documents: [{ id: 'd1', title: 'T', status: 'signed' }], total: 1, page: 1, limit: 20 } });
+    const r = await run('secuura_list_documents', {});
+    expect(r.isError).toBeUndefined();
+    expect(JSON.parse(r.content[0].text)).toMatchObject({ total: 1, count: 1, documents: [{ id: 'd1', title: 'T', status: 'signed' }] });
+    expect(errSpy).not.toHaveBeenCalled();
+  });
+});
```
