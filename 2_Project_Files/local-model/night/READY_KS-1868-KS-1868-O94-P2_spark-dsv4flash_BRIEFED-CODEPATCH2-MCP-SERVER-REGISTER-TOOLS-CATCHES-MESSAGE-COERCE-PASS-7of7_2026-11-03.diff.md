# READY — KS-1868-KS-1868-O94-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 11:55 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 11:55 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `c6f4cc2f17a3999bd568b91ec6b55eebe58aa603`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/mcp-server/src/tools/register.ts } + { Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/mcp-server/src/tools/register.ts` (product) and `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	2	Blockchain/Dev/services/mcp-server/src/tools/register.ts
108	0	Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (12 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: register.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/mcp-server/src/tools/register.ts`; test(s): `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/mcp-server/src/tools/register.ts 12 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts 108 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/mcp-server/src/tools/register.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 the register tools read the thrown value safely RED ks1868 R1 secuura_register_document answers a constant reason for a revoked Proxy thrown value', 'KS-1868 the register tools read the thrown value safely RED ks1868 R2 secuura_register_document answers a constant reason for an Error whose message getter throws', 'KS-1868 the register tools read the thrown value safely RED ks1868 R3 secuura_register_documents keeps its results when one document throws a revoked Proxy', 'KS-1868 the register tools read the thrown value safely RED ks1868 R4 secuura_register_documents keeps its results when one document throws an Error whose message getter throws']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=131 failed=0 | after: total=137 failed=0` · `NEW reds: []` [baseline_suite.json total=131 failed=0; after_suite.json total=137 failed=0]
- A6 [verbatim]: `PASS A6 whole services/mcp-server suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/mcp-server: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/mcp-server/src/tools/register.ts` (+12/-2 per numstat.out) and the test file `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts` (+108/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/mcp-server/src/tools/register.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `c6f4cc2f17a3999bd568b91ec6b55eebe58aa603` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p2_mcp_server_register_tools_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/mcp-server/src/tools/register.ts b/Blockchain/Dev/services/mcp-server/src/tools/register.ts
--- a/Blockchain/Dev/services/mcp-server/src/tools/register.ts
+++ b/Blockchain/Dev/services/mcp-server/src/tools/register.ts
@@ -61,7 +61,12 @@
           ],
         };
       } catch (err: unknown) {
-        const message = err instanceof Error ? err.message : String(err);
+        let message: string;
+        try {
+          message = err instanceof Error ? err.message : String(err);
+        } catch {
+          message = 'unreadable thrown value';
+        }
         return {
           content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],
           isError: true,
@@ -118,7 +123,12 @@
             });
           }
         } catch (err: unknown) {
-          const message = err instanceof Error ? err.message : String(err);
+          let message: string;
+          try {
+            message = err instanceof Error ? err.message : String(err);
+          } catch {
+            message = 'unreadable thrown value';
+          }
           results.push({ success: false, filePath: doc.filePath, error: message });
         }
       }
diff --git a/Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts
@@ -0,0 +1,108 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: the two catches of src/tools/register.ts (secuura_register_document, secuura_register_documents) read
+// `err instanceof Error ? err.message : String(err)` unguarded. When the thrown value itself cannot be read (a revoked Proxy throws on
+// `instanceof`; an Error whose `message` getter throws, throws on `.message`) the catch throws, so the tool call rejects: for the batch tool
+// the results of every other document are lost with it. Each tool must still answer with a success:false result carrying a constant reason.
+// The stand-ins are plain functions, not vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy first.
+const h = vi.hoisted(() => ({
+  registerThrows: undefined as unknown,
+}));
+
+vi.mock('../hashing.js', () => ({
+  hashFile: () => Promise.resolve('sha256:abc'),
+  extractFileName: (p: string) => p,
+}));
+
+vi.mock('../api-client.js', () => ({
+  registerDocument: () => Promise.reject(h.registerThrows),
+}));
+
+import { registerRegisterTools } from '../tools/register.js';
+
+type ToolResult = { content: Array<{ type: string; text: string }>; isError?: boolean };
+type Handler = (args: Record<string, unknown>) => Promise<ToolResult>;
+
+/** Register the register tools on a duck-typed server, run one, return its result (undefined when the handler rejects). */
+async function runTool(name: string, args: Record<string, unknown>): Promise<ToolResult | undefined> {
+  const handlers: Record<string, Handler> = {};
+  const server = {
+    tool: (n: string, _desc: string, _shape: unknown, handler: Handler) => {
+      handlers[n] = handler;
+    },
+  };
+  registerRegisterTools(server as never);
+  return handlers[name](args).catch(() => undefined);
+}
+
+function revokedProxy(): unknown {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function throwingMessageError(): unknown {
+  return Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+}
+
+const one = { title: 'T', documentType: 'certificate', contentHash: 'sha256:abc' };
+const batch = { documents: [{ filePath: '/x/doc.pdf', title: 'T', documentType: 'certificate' }] };
+
+describe('KS-1868 the register tools read the thrown value safely', () => {
+  beforeEach(() => {
+    h.registerThrows = undefined;
+  });
+
+  it('control ks1868 C1 secuura_register_document still returns its message for an ordinary Error', async () => {
+    h.registerThrows = new Error('api down');
+    const r = await runTool('secuura_register_document', one);
+    expect(r?.isError).toBe(true);
+    expect(JSON.parse(r!.content[0].text)).toEqual({ success: false, error: 'api down' });
+  });
+
+  it('control ks1868 C2 secuura_register_documents still lists an ordinary Error against its document', async () => {
+    h.registerThrows = new Error('api down');
+    const r = await runTool('secuura_register_documents', batch);
+    const body = JSON.parse(r!.content[0].text);
+    expect(body.failed).toBe(1);
+    expect(body.results[0].error).toBe('api down');
+  });
+
+  it('RED ks1868 R1 secuura_register_document answers a constant reason for a revoked Proxy thrown value', async () => {
+    h.registerThrows = revokedProxy();
+    const r = await runTool('secuura_register_document', one);
+    expect(r?.isError).toBe(true);
+    expect(JSON.parse(r!.content[0].text)).toEqual({ success: false, error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 secuura_register_document answers a constant reason for an Error whose message getter throws', async () => {
+    h.registerThrows = throwingMessageError();
+    const r = await runTool('secuura_register_document', one);
+    expect(r?.isError).toBe(true);
+    expect(JSON.parse(r!.content[0].text)).toEqual({ success: false, error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 secuura_register_documents keeps its results when one document throws a revoked Proxy', async () => {
+    h.registerThrows = revokedProxy();
+    const r = await runTool('secuura_register_documents', batch);
+    expect(r).toBeDefined();
+    const body = JSON.parse(r!.content[0].text);
+    expect(body.failed).toBe(1);
+    expect(body.results[0].error).toBe('unreadable thrown value');
+  });
+
+  it('RED ks1868 R4 secuura_register_documents keeps its results when one document throws an Error whose message getter throws', async () => {
+    h.registerThrows = throwingMessageError();
+    const r = await runTool('secuura_register_documents', batch);
+    expect(r).toBeDefined();
+    const body = JSON.parse(r!.content[0].text);
+    expect(body.failed).toBe(1);
+    expect(body.results[0].error).toBe('unreadable thrown value');
+  });
+});
```
