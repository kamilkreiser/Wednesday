# READY — KS-1117 (systemTest/performance `utils/yaml.ts:108`: one leading U+FEFF stripped before `loadYaml` — a BOM-then-comment file now reads 'it contains no YAML document', not 'line 1, column 2') — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (run 20:17; A2 FUZZY -C1 on the product section — its outer context line drifted by a word; the -/+ lines are exact — the Sunday seat re-applies from the -/+ lines at :108)
# Source read by me (Wednesday): E1 exactly as briefed (two-line comment + `source.replace(/^﻿/, '')`); standalone temp-file test with `YamlParseError` asserted by class and the full KS-1109 message; 🔴 red at the tip / green after; control (no BOM) green both; whole performance suite green; tsc green.

```diff
--- a/systemTest/performance/utils/yaml.ts
+++ b/systemTest/performance/utils/yaml.ts
@@ -105,7 +105,9 @@ export function readYaml(filepath: string): unknown {
     // Read outside the try: a missing or unreadable file is not a parse failure and keeps its own error.
     const source = fs.readFileSync(filepath, 'utf-8');
     try {
-        return loadYaml(source);
+        // KS-1117: strip leading BOM so a comments-only config does not report "line 1, column 2".
+        // (QA-963-2)
+        return loadYaml(source.replace(/^\ufeff/, ''));
     } catch (err: unknown) {
         // KS-1109 (QA-960-1): the read sits above this try, so anything caught here came from parsing, and all of it is
         // wrapped. PRIOR BEHAVIOUR: only a YAMLException was wrapped and anything else rethrown, so js-yaml's URIError
 
--- /dev/null
+++ b/systemTest/performance/tests/unit/utils/ks1117-k6-yaml-loader-a-bom-immediately.test.ts
@@ -0,0 +1,52 @@
+import * as fs from 'node:fs';
+import * as os from 'node:os';
+import * as path from 'node:path';
+
+import { afterEach, beforeEach, describe, expect, it } from 'vitest';
+
+import { readYaml, YamlParseError } from '../../../utils/yaml.ts';
+
+let dir: string;
+
+/** Whatever `fn` throws, or undefined. */
+function thrownBy(fn: () => unknown): unknown {
+    try {
+        fn();
+        return undefined;
+    } catch (_err: unknown) {
+        return undefined;
+    }
+}
+
+beforeEach(() => {
+    dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ks1117-bom-'));
+});
+afterEach(() => {
+    fs.rmSync(dir, { recursive: true, force: true });
+});
+
+describe('KS-1117 — k6 YAML loader', () => {
+    it('🔴 KS-1117 — a BOM immediately followed by a comment reads "it contains no YAML document", not "line 1, column 2"', () => {
+        const file = path.join(dir, 'comments-only-bom.yml');
+        fs.writeFileSync(file, '\ufeff# only a comment\n');
+        let err: unknown;
+        try {
+            readYaml(file);
+        } catch (caught) {
+            err = caught;
+        }
+        expect(err).toBeInstanceOf(YamlParseError);
+        expect((err as Error).message).toBe(
+            `Could not parse YAML in ${file}: it contains no YAML document (the file's content is not shown).`,
+        );
+    });
+
+    it('KS-1117 control — the same comments-only file WITHOUT a BOM already reads "it contains no YAML document"', () => {
+        const file = path.join(dir, 'comments-only.yml');
+        fs.writeFileSync(file, '# only a comment\n');
+        let err: unknown;
+        try {
+            readYaml(file);
+        } catch (caught) {
+            err = caught;
+        }
+        expect(err).toBeInstanceOf(YamlParseError);
+        expect((err as Error).message).toBe(
+            `Could not parse YAML in ${file}: it contains no YAML document (the file's content is not shown).`,
+        );
+    });
+});
```
