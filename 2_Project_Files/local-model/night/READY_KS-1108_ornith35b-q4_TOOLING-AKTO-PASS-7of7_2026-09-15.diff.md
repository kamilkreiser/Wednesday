# READY — KS-1108 (systemTest/akto `src/config/secrets.ts:40`: the secrets parse is wrapped — a malformed secrets.yml throws a plain Error naming only the file and position, never js-yaml's reason/message/mark — the KS-1099 shape) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (run 20:20; the FIRST akto-package ticket, `tool=systemTest/akto vitest_config=vitest.unit.config.ts`; A2 --recount on the product hunk)
# Source read by me (Wednesday): E1 as briefed (try/catch, position from `mark.line/column` +1 or 'an unknown position', no reason/message/cause); the test writes the fixture under a temp repo root at SECRETS_FILE_RELATIVE, asserts `inspect(err, {depth: 6})` lacks the sentinel + the message names the file and 'at line 1, column ' (🔴 red at the tip: the raw YAMLException carries the sentinel); control parses a valid file (green both). Whole akto unit suite green; tsc green. The ticket's 'measure first' (akto's js-yaml 5.4.1 whole-file print) is answered by the red arm itself: inspect(err) at the tip DID carry the sentinel.

```diff
--- a/systemTest/akto/src/config/secrets.ts
+++ b/systemTest/akto/src/config/secrets.ts
@@ -36,7 +36,18 @@ export function loadSecretsYml(repoRoot: string): { data: SecretsYml; filePath:
         log.error('Then fill in your Akto dashboard and Secuura credentials.');
         process.exit(1);
     }
-    return { data: loadYaml(fs.readFileSync(filePath, 'utf-8')) as SecretsYml, filePath };
+    // KS-1108 (the KS-1099 shape): a js-yaml YAMLException carries the whole file in mark.buffer and, for a bare
+    // `!`/`*` value, the value itself in `reason`; an uncaught print would show every credential. Name only the
+    // file and the position — never the reason, the message, the mark or a cause.
+    const source = fs.readFileSync(filePath, 'utf-8');
+    try {
+        return { data: loadYaml(source) as SecretsYml, filePath };
+    } catch (err: unknown) {
+        const mark = (err as { mark?: { line?: number; column?: number } }).mark;
+        const where =
+            mark && typeof mark.line === 'number' && typeof mark.column === 'number'
+                ? ` at line ${String(mark.line + 1)}, column ${String(mark.column + 1)}`
+                : ' at an unknown position';
+        throw new Error(`Could not parse YAML in ${filePath}${where} (the file's content is not shown).`);
+    }
 }
--- /dev/null
+++ b/systemTest/akto/tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts
@@ -0,0 +1,82 @@
+import * as fs from 'fs';
+import * as os from 'os';
+import * as path from 'path';
+import { inspect } from 'util';
+
+import { afterEach, beforeEach, describe, expect, it } from 'vitest';
+
+import { loadSecretsYml } from '../../../src/config/secrets';
+import { SECRETS_FILE_RELATIVE } from '../../../src/core/constants';
+
+/** A value no real file holds, so a match can only come from the fixture. */
+const SENTINEL = 'ks1108-tag-Pw-4c2e91';
+
+let root: string;
+
+/** Whatever `fn` throws, or undefined. */
+function thrownBy(fn: () => unknown): unknown {
+    try {
+        fn();
+        return undefined;
+    } catch (err: unknown) {
+        return err;
+    }
+}
+
+/** Write `content` as the secrets file under a temporary repo root and return that root. */
+function writeSecrets(content: string): string {
+    const file = path.join(root, SECRETS_FILE_RELATIVE);
+    fs.mkdirSync(path.dirname(file), { recursive: true });
+    fs.writeFileSync(file, content);
+    return root;
+}
+
+beforeEach(() => {
+    root = fs.mkdtempSync(path.join(os.tmpdir(), 'ks1108-secrets-'));
+});
+afterEach(() => {
+    fs.rmSync(root, { recursive: true, force: true });
+});
+
+describe('loadSecretsYml', () => {
+    it('🔴 KS-1108 — a malformed secrets.yml throws an error that names the file and position and NOTHING of its content', () => {
+        const repoRoot = writeSecrets(`password: !${SENTINEL}\n`);
+        const err = thrownBy(() => loadSecretsYml(repoRoot));
+        expect(err).toBeInstanceOf(Error);
+        const rendered = inspect(err, { depth: 6 });
+        expect(rendered).not.toContain(SENTINEL);
+        expect((err as Error).message).toContain(`Could not parse YAML in ${path.join(repoRoot, SECRETS_FILE_RELATIVE)}`);
+        expect((err as Error).message).toContain(' at line 1, column ');
+    });
+
+    it('KS-1108 control — a well-formed secrets.yml still parses to its data', () => {
+        const repoRoot = writeSecrets('environments:\n  local:\n    dashboardUrl: http://127.0.0.1:9090\n');
+        const { data, filePath } = loadSecretsYml(repoRoot);
+        expect(filePath).toBe(path.join(repoRoot, SECRETS_FILE_RELATIVE));
+        expect((data as { environments?: unknown }).environments).toBeDefined();
+    });
+});
```
