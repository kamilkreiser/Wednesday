# READY (hand-written note: hold_ready.py REFUSED this loose code_patch2 PASS, A3x unmeasured=1) - KS-1410-P6

Spark operator 22, 2026-10-30. Rung 4 LOOSE (product lines written by the model, hunk headers dictated). **A PASS is a candidate, never a merge.** Raise as `Refs KS-1410` (never a close-word) ; a census found the platform.ts sites, KS-1410 does not name that file.

- What: api-gateway routes/platform.ts: the templates-read catch and the clone-to-tenant 500 stop putting the thrown text in the body (2 product hunks + 1 new vitest file)
- Tip: 40c06084919d5aff132e82693cd60d513cb40ba7 (origin/develop, ls-remote 2026-10-30 13:0x)
- Result: PASS 7/7; model 52 s, 25768+1624 tokens; A4 2 red of 5 (3 control cells green); A5 5/5; api-gateway suite 1321 -> 1326, no new red; tsc rc 0; apply mode strict (no apply_check_strict error); A2a anchors ok
- Golden: patch.diff is cmp-IDENTICAL to the golden (the golden's product lines were NOT shown to the model); the control run dir /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1410_p6_platform_templates_500_no_details-control-r3 is PASS
- Why no hold_ready READY: the loose allowance excludes code_patch2 (IMPROVEMENTS 2026-10-30 12:4x). The reviewer reads the product hunks below; the test file's + lines are byte-checked by A3x.
- Brief: night/briefs/ks_1410_p6_platform_templates_500_no_details/KS-1410.md   Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1410_p6_platform_templates_500_no_details
- Raise-seat notes: the 500 body loses its message text / details key (a response-shape change: say so in the PR). Test is a source-text guard (the module starts a server or needs pools on import).

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/platform.ts b/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/platform.ts
@@ -991,6 +991,9 @@
             })),
           });
         } finally { await pool.end(); }
-      } catch (err: any) { res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch templates', details: { detail: err?.message } } }); }
+      } catch (err: any) {
+        console.error('[Templates] Failed to fetch templates:', err?.message);
+        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch templates' } });
+      }
     },
   );
@@ -1088,7 +1091,7 @@
       } catch (err: unknown) {
         const msg = err instanceof Error ? err.message : String(err);
         console.error('[Clone] Failed:', msg);
-        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed', details: { detail: msg } } });
+        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed' } });
       }
     },
   );
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-platform-templates-500-never-echoes-the-thrown-text.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-platform-templates-500-never-echoes-the-thrown-text.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-platform-templates-500-never-echoes-the-thrown-text.test.ts
@@ -0,0 +1,70 @@
+/**
+ * KS-1410 class (api-gateway routes/platform.ts): two catch blocks answered 500 with the thrown text in `details.detail`: the platform
+ * templates read (`Failed to fetch templates`, `err?.message`) and the clone-to-tenant route (`Clone failed`, `msg`). The sibling 500s in
+ * the same file (a bare `catch` at the second templates read, and `Document lookup failed`) already answer a constant body with no details.
+ * The fix: the templates catch logs the thrown text with console.error and answers the constant body; the clone catch (which already logs
+ * `[Clone] Failed:`) just drops `details`. Source-text guard: createPlatformRoutes needs two pools and a wallet, so the file is read, not driven.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { resolve } from 'node:path';
+
+const SRC = readFileSync(resolve(__dirname, '..', 'routes/platform.ts'), 'utf8');
+
+type Five = { line: number; stmt: string; handler: string; context: string };
+
+/** Every statement that answers 500 through `.status(500).json(...)`, with the route it sits in and the 4 lines (plus the same line's prefix) before it. */
+function fiveHundreds(source: string): Five[] {
+  const lines = source.split('\n');
+  const out: Five[] = [];
+  lines.forEach((text, i) => {
+    const at = text.indexOf('.status(500).json(');
+    if (at < 0) return;
+    let handler = '';
+    for (let j = i; j >= 0; j--) {
+      const m = new RegExp('^\\s*(?:app|rout' + 'er)\\.(get|post|put|patch|delete)\\(\\s*\'([^\']+)\'').exec(lines[j]);
+      if (m) {
+        handler = m[1].toUpperCase() + ' ' + m[2];
+        break;
+      }
+    }
+    out.push({ line: i + 1, stmt: text.slice(at), handler, context: lines.slice(Math.max(0, i - 4), i).join('\n') + '\n' + text.slice(0, at) });
+  });
+  return out;
+}
+
+/** True when the response argument names a caught value: an identifier left once string literals and the envelope keys are removed. */
+function leaks(stmt: string): boolean {
+  const bare = stmt.replace(/'[^']*'/g, "''").replace(/\b(success|error|code|message|verified)\s*:/g, '');
+  return /\b(err|error|msg|message|detail|details|stack)\b/.test(bare);
+}
+
+const FIVE = fiveHundreds(SRC);
+
+describe('api-gateway platform.ts: no 500 answer carries the thrown text', () => {
+  it('RED plat-500 P1 no 500 answer in the file names a caught value or carries details', () => {
+    expect(FIVE.filter((f) => leaks(f.stmt)).map((f) => f.line > 0 && f.stmt.slice(0, 90))).toEqual([]);
+  });
+
+  it('RED plat-500 P2 the templates catch logs the thrown text with console.error just before it answers', () => {
+    const first = FIVE.filter((f) => f.stmt.includes("'Failed to fetch templates'"))[0];
+    expect(first).toBeDefined();
+    expect(first.context).toMatch(/console\.error\(.*err/);
+  });
+
+  it('control plat-500 C1 the scanner flags a details leak and passes the constant bodies', () => {
+    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed', details: { detail: msg } } });")).toBe(true);
+    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed' } });")).toBe(false);
+  });
+
+  it('control plat-500 C2 the file keeps its four 500 answers with their own messages', () => {
+    expect(FIVE).toHaveLength(4);
+    expect(FIVE.filter((f) => f.stmt.includes("message: 'Failed to fetch templates'"))).toHaveLength(2);
+    expect(FIVE.filter((f) => f.stmt.includes("message: 'Clone failed'"))).toHaveLength(1);
+    expect(FIVE.filter((f) => f.stmt.includes("message: 'Document lookup failed'"))).toHaveLength(1);
+  });
+
+  it('control plat-500 C3 the clone catch still logs the thrown text', () => {
+    expect(SRC).toContain("console.error('[Clone] Failed:', msg);");
+  });
+});
```
