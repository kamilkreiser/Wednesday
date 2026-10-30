# READY (hand-written note: hold_ready.py REFUSED this loose code_patch2 PASS, A3x unmeasured=1) - KS-1410-P4

Spark operator 22, 2026-10-30. Rung 4 LOOSE (product lines written by the model, hunk headers dictated). **A PASS is a candidate, never a merge.** Raise as `Refs KS-1410` (never a close-word); the POST /api/tenants site (:361) is deliberately untouched (Kam open card secuura-ks1240-tenant-create-key-fail-answer-1028).

- What: tenant-provisioning index.ts: six 500 catch blocks log the thrown text and answer the constant message (POST /api/tenants untouched) (6 product hunks + 1 new vitest file)
- Tip: 40c06084919d5aff132e82693cd60d513cb40ba7 (origin/develop, ls-remote 2026-10-30 13:0x)
- Result: PASS 7/7; model 56 s, 18414+2220 tokens; A4 3 red of 6 (3 control cells green); A5 6/6; tenant-provisioning suite no new red; tsc rc 0; apply mode strict (no apply_check_strict error); A2a anchors ok
- Golden: patch.diff is cmp-IDENTICAL to the golden (the golden's product lines were NOT shown to the model); the control run dir /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1410_p4_tenantprov_500_no_echo-control is PASS
- Why no hold_ready READY: the loose allowance excludes code_patch2 (IMPROVEMENTS 2026-10-30 12:4x). The reviewer reads the product hunks below; the test file's + lines are byte-checked by A3x.
- Brief: night/briefs/ks_1410_p4_tenantprov_500_no_echo/KS-1410.md   Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1410_p4_tenantprov_500_no_echo
- Raise-seat notes: the 500 body loses its message text / details key (a response-shape change: say so in the PR). Test is a source-text guard (the module starts a server or needs pools on import).

```diff
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/index.ts b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
--- a/Blockchain/Dev/services/tenant-provisioning/src/index.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
@@ -382,6 +382,7 @@
       return;
     }
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[provisioning] GET /api/tenants failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -421,6 +422,7 @@
     });
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[provisioning] GET /api/tenants/:id failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -451,6 +453,7 @@
     res.json({ success: true, status });
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[provisioning] PATCH /api/tenants/:id/status failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -512,6 +515,7 @@
       return;
     }
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[provisioning] PATCH /api/tenants/:id failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -573,6 +577,7 @@
     res.json({ success: true, deleted: true });
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[provisioning] DELETE /api/tenants/:id failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -593,6 +598,7 @@
     res.json({ success: true, entries: result.rows, total: parseInt(countResult.rows[0].total) });
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[provisioning] GET /api/audit-log failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts
@@ -0,0 +1,78 @@
+/**
+ * KS-1410 (the tenant-provisioning file of the class): the catch blocks of tenant-provisioning/src/index.ts answered 500 with the thrown text
+ * as the response message (`message: message`), so a driver message or an internal host:port reached the caller. The six handlers other than
+ * POST /api/tenants now log the thrown text with console.error and answer the constant message below.
+ * POST /api/tenants (the key-generation path, whose 500 answer is Kam's open card secuura-ks1240-tenant-create-key-fail-answer-1028) is NOT
+ * changed here and must stay as it is. Source-text guard: the module starts a server and a pool on import, so the file is read, not imported.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { resolve } from 'node:path';
+
+const SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
+const CONSTANT = 'An unexpected error occurred';
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
+      const m = /^\s*(?:app|router)\.(get|post|put|patch|delete)\(\s*'([^']+)'/.exec(lines[j]);
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
+const EXEMPT = 'POST /api/tenants';
+const CHANGED = FIVE.filter((f) => f.handler !== EXEMPT);
+
+describe('tenant-provisioning index.ts: no 500 answer carries the thrown text', () => {
+  it('RED tp-500 P1 no 500 answer outside POST /api/tenants names a caught value', () => {
+    expect(CHANGED.filter((f) => leaks(f.stmt)).map((f) => f.handler)).toEqual([]);
+  });
+
+  it('RED tp-500 P2 each of the six answers the constant message', () => {
+    expect(CHANGED.map((f) => f.handler)).toHaveLength(6);
+    expect(CHANGED.filter((f) => !f.stmt.includes("message: '" + CONSTANT + "'")).map((f) => f.handler)).toEqual([]);
+  });
+
+  it('RED tp-500 P3 each of the six logs the thrown text with console.error just before it answers', () => {
+    expect(CHANGED.filter((f) => !/console\.error\(.*\b(message|err)\b/.test(f.context)).map((f) => f.handler)).toEqual([]);
+  });
+
+  it('control tp-500 C1 the scanner flags a leaking answer and passes the constant one', () => {
+    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });")).toBe(true);
+    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'x', details: { detail: msg } } });")).toBe(true);
+    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: '" + CONSTANT + "' } });")).toBe(false);
+  });
+
+  it('control tp-500 C2 the file has exactly seven 500 answers and POST /api/tenants is untouched', () => {
+    expect(FIVE).toHaveLength(7);
+    const post = FIVE.filter((f) => f.handler === EXEMPT);
+    expect(post).toHaveLength(1);
+    expect(post[0].stmt).toContain('message: message');
+  });
+
+  it('control tp-500 C3 the three 400 validation answers keep their details', () => {
+    expect(SRC.split("details: err.errors").length - 1).toBe(3);
+  });
+});
```
