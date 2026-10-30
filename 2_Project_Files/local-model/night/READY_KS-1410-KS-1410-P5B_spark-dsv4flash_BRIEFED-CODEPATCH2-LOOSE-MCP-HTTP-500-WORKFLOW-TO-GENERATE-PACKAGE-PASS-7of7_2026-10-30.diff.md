# READY (hand-written note: hold_ready.py REFUSES a loose code_patch2 PASS, A3x unmeasured=1) - KS-1410-P5B

Spark operator 23, 2026-10-30. Rung 4 LOOSE (product lines written by the model, hunk headers dictated, plus a PER-HUNK line-by-line skeleton). **A PASS is a candidate, never a merge.** Raise as `Refs KS-1410` (never a close-word). POST /hash (:62, KS-1214) is deliberately untouched.

- What: mcp-server http-server.ts part B of 2: GET /workflow/:id, GET /connector, GET /policy, POST /generate-package: each logs the thrown text with console.error and answers the constant message (4 product hunks + 1 new vitest file).
- Origin of the split: ks_1410_p5 (9 hunks) FAILED twice at A2 (operator 22); Wednesday ruled SPLIT into two NEW briefs of <=5 hunks (a new brief, a new counter) with a hunk-specific instruction. This part passed on its ORIGINAL brief (counter unspent).
- Tip: 40c06084919d5aff132e82693cd60d513cb40ba7 (origin/develop, ls-remote 2026-10-30 13:2x)
- Result: PASS 7/7; 82 s round, model 50 s, 15227+2120 tokens; A4 3 red of 7 (4 control cells green); A5 7/7; mcp-server suite no new red; tsc rc 0; apply mode strict; A2a anchors 4/4 ok
- Golden: patch.diff is cmp-IDENTICAL to the golden (the golden's product lines were NOT shown to the model); control run PASS.
- Disjoint from ks_1530_p1 (`@@ -233,6 +233,13 @@`, the 400 guard at :233-239): p5a + p5b + the ks_1530_p1 http-server.ts hunk applied cleanly with `git apply` in all three orders tried (a b c / c b a / b c a) and gave the same final file (shasum 2efdce000c13). The other half of p5 (the sibling note) is the remaining five/four sites.
- Why no hold_ready READY: the loose allowance excludes code_patch2 (IMPROVEMENTS 2026-10-30 12:4x). The reviewer reads the product hunks below; the test file's + lines are byte-checked by A3x.
- Brief: night/briefs/ks_1410_p5b_mcp_http_500_no_echo_workflow_to_generate_package/KS-1410.md   Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1410_p5b_mcp_http_500_no_echo_workflow_to_generate_package
- Raise-seat notes: POST /verify's `error` string becomes a constant (a response-shape text change, say so in the PR; ChatGPT Actions clients not checked). The 500 body loses the thrown text on every site above. Test is a source-text guard (http-server.ts binds a port on import). Raise BOTH parts in one PR or two, reviewer's choice; they do not overlap.

```diff
diff --git a/Blockchain/Dev/services/mcp-server/src/http-server.ts b/Blockchain/Dev/services/mcp-server/src/http-server.ts
--- a/Blockchain/Dev/services/mcp-server/src/http-server.ts
+++ b/Blockchain/Dev/services/mcp-server/src/http-server.ts
@@ -190,6 +190,7 @@
     res.status(result.status).json(result.data);
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[mcp-http] GET /workflow/:id failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -200,6 +201,7 @@
     res.status(result.status).json(result.data);
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[mcp-http] GET /connector failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -210,6 +212,7 @@
     res.json(result.data);
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+    console.error('[mcp-http] GET /policy failed:', message);
+    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -263,8 +266,9 @@
     );
   } catch (err: unknown) {
     const message = err instanceof Error ? err.message : String(err);
+    console.error('[mcp-http] POST /generate-package failed:', message);
     if (!res.headersSent) {
-      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
+      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
     }
   }
 });
diff --git a/Blockchain/Dev/services/mcp-server/src/__tests__/ks1410-mcp-http-500-part-b-never-echoes-the-thrown-text.test.ts b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1410-mcp-http-500-part-b-never-echoes-the-thrown-text.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1410-mcp-http-500-part-b-never-echoes-the-thrown-text.test.ts
@@ -0,0 +1,86 @@
+/**
+ * KS-1410 (the mcp-server file of the class, part B of 2): the catch blocks of mcp-server/src/http-server.ts answered 500 with the thrown text in the
+ * response (`message: message`, and `error: message` on POST /verify), so a driver message, a file-system error naming a server path or an
+ * internal host:port reached the caller. The four handlers named in MINE below now log the thrown text with console.error and answer the
+ * constant message. The other handlers of the file are covered by the other part; POST /hash (KS-1214's route) is NOT changed and must stay as it is.
+ * Source-text guard: the module binds a port and runs a production guard on import, so the file is read, not imported.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { resolve } from 'node:path';
+
+const SRC = readFileSync(resolve(__dirname, '..', 'http-server.ts'), 'utf8');
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
+const EXEMPT = 'POST /hash';
+const MINE = ['GET /workflow/:id', 'GET /connector', 'GET /policy', 'POST /generate-package'];
+const CHANGED = FIVE.filter((f) => MINE.includes(f.handler));
+
+describe('mcp-server http-server.ts part B: no 500 answer of these handlers carries the thrown text', () => {
+  it('RED mcp-500b P1 no 500 answer of the four handlers names a caught value', () => {
+    expect(CHANGED).toHaveLength(MINE.length);
+    expect(CHANGED.filter((f) => leaks(f.stmt)).map((f) => f.handler)).toEqual([]);
+  });
+
+  it('RED mcp-500b P2 each of the four answers the constant message', () => {
+    expect(CHANGED.filter((f) => !f.stmt.includes("'" + CONSTANT + "'")).map((f) => f.handler)).toEqual([]);
+  });
+
+  it('RED mcp-500b P3 each of the four logs the thrown text with console.error just before it answers', () => {
+    expect(CHANGED.filter((f) => !/console\.error\(.*\b(message|err)\b/.test(f.context)).map((f) => f.handler)).toEqual([]);
+  });
+
+  it('control mcp-500b C1 the scanner flags a leaking answer and passes the constant one', () => {
+    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });")).toBe(true);
+    expect(leaks("res.status(500).json({ verified: false, error: message });")).toBe(true);
+    expect(leaks("res.status(500).json({ verified: false, error: '" + CONSTANT + "' });")).toBe(false);
+    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: '" + CONSTANT + "' } });")).toBe(false);
+  });
+
+  it('control mcp-500b C2 the file has exactly ten 500 answers and POST /hash is untouched', () => {
+    expect(FIVE).toHaveLength(10);
+    const hash = FIVE.filter((f) => f.handler === EXEMPT);
+    expect(hash).toHaveLength(1);
+    expect(hash[0].stmt).toContain('message: message');
+  });
+
+  it('control mcp-500b C3 the two per-item results of the batch routes are not touched', () => {
+    expect(SRC).toContain('results.push({ success: false, title: doc.title, error: message });');
+    expect(SRC).toContain('results.push({ verified: false, error: message });');
+  });
+
+  it('control mcp-500b C4 the 400 refusals keep their messages', () => {
+    expect(SRC).toContain("message: 'Provide documentId, contentHash, or filePath'");
+    expect(SRC).toContain("message: 'documents array is required'");
+  });
+});
```
