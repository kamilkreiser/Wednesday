# READY — KS-1104-O151-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label/out.md.checker/patch.diff`** (from `ls` at 03:51 2026-11-12; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 03:51 2026-11-12 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `16a5c67e676eefa3e620c663fee3162941a22fa0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx } + { Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx
94	0	Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: VerifyPage.tsx`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts 94 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1104 the verifier mode tabs carry an accessible name RED ks1104 R1 every mode tab carries a non-empty aria-label', 'KS-1104 the verifier mode tabs carry an accessible name RED ks1104 R2 the labels are the three names the tabs show at desktop width']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1623 failed=1 | after: total=1628 failed=1` · `NEW reds: []` [baseline_suite.json total=1623 failed=1; after_suite.json total=1628 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts` (+94/-0); 2 files in all (code_patch2: products Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `16a5c67e676eefa3e620c663fee3162941a22fa0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label/input.json`. Brief (given by --brief; its `# ` heading names KS-1104): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1104_o151_p1_verifier_mode_tabs_aria_label/KS-1104.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1104_o151_p1_verifier_mode_tabs_aria_label/checker.out`.

```diff
diff --git a/Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx b/Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx
--- a/Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx
+++ b/Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx
@@ -264,5 +264,5 @@
                       <Tooltip>
                         <TooltipTrigger asChild>
-                          <TabsTrigger value="upload" data-testid="tab-upload" className="gap-2">
+                          <TabsTrigger value="upload" data-testid="tab-upload" aria-label="Upload File" className="gap-2">
                             <Upload className="w-4 h-4" />
                             <span className="hidden sm:inline">Upload File</span>
@@ -275,5 +275,5 @@
                       <Tooltip>
                         <TooltipTrigger asChild>
-                          <TabsTrigger value="id" data-testid="tab-id" className="gap-2">
+                          <TabsTrigger value="id" data-testid="tab-id" aria-label="Enter ID" className="gap-2">
                             <Search className="w-4 h-4" />
                             <span className="hidden sm:inline">Enter ID</span>
@@ -286,5 +286,5 @@
                       <Tooltip>
                         <TooltipTrigger asChild>
-                          <TabsTrigger value="qr" data-testid="tab-qr" className="gap-2">
+                          <TabsTrigger value="qr" data-testid="tab-qr" aria-label="Scan QR" className="gap-2">
                             <ScanLine className="w-4 h-4" />
                             <span className="hidden sm:inline">Scan QR</span>
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1104-verifier-mode-tabs-carry-an-accessible-name.test.ts
@@ -0,0 +1,94 @@
+import { describe, it, expect } from 'vitest';
+import { existsSync, readFileSync } from 'node:fs';
+import { dirname, join, resolve } from 'node:path';
+import { fileURLToPath } from 'node:url';
+import ts from 'typescript';
+
+// KS-1104: at phone width the verifier's three mode tabs (Upload File, Enter ID, Scan QR) render icon-only, because their text spans
+// are `hidden sm:inline`, and each tab has no aria-label, so a screen reader hears three unnamed tabs (WCAG 2.1 SC 4.1.2).
+// SOURCE GUARD, stated as such: frontend/verifier has no test runner, so this cell reads the page's source text (the TypeScript
+// syntax tree, so a commented-out attribute does not count) and pins the wiring, not the browser behaviour. It is hosted here
+// because this package has a runner and a test may read a file under frontend/ by a path relative to the Dev root (ks1564 does).
+
+function findDevRoot(start: string): string {
+  let dir = start;
+  for (let i = 0; i < 12; i++) {
+    if (existsSync(join(dir, 'services')) && existsSync(join(dir, 'packages')) && existsSync(join(dir, 'frontend'))) return dir;
+    const parent = resolve(dir, '..');
+    if (parent === dir) break;
+    dir = parent;
+  }
+  throw new Error(`[ks1104 guard] could not locate the Dev root from ${start}`);
+}
+
+const TREE_TOP = findDevRoot(dirname(fileURLToPath(import.meta.url)));
+const VERIFY_PAGE = join(TREE_TOP, 'frontend', 'verifier', 'src', 'components', 'VerifyPage.tsx');
+
+interface Trigger {
+  testId: string | null;
+  label: string | null;
+  labelled: boolean;
+}
+
+/** Every `<TabsTrigger ...>` element in the source, with its data-testid and its STATIC aria-label (a string literal), if any. */
+function scanTabTriggers(source: string): Trigger[] {
+  const sf = ts.createSourceFile('VerifyPage.tsx', source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
+  const found: Trigger[] = [];
+  const visit = (node: ts.Node): void => {
+    if ((ts.isJsxOpeningElement(node) || ts.isJsxSelfClosingElement(node)) && node.tagName.getText(sf) === 'TabsTrigger') {
+      const literal = (name: string): string | null => {
+        for (const prop of node.attributes.properties) {
+          if (ts.isJsxAttribute(prop) && prop.name.getText(sf) === name) {
+            return prop.initializer && ts.isStringLiteral(prop.initializer) ? prop.initializer.text : null;
+          }
+        }
+        return null;
+      };
+      const label = literal('aria-label');
+      found.push({ testId: literal('data-testid'), label, labelled: label !== null && label.trim().length > 0 });
+    }
+    ts.forEachChild(node, visit);
+  };
+  visit(sf);
+  return found;
+}
+
+const source = readFileSync(VERIFY_PAGE, 'utf8');
+const triggers = scanTabTriggers(source);
+
+describe('KS-1104 the verifier mode tabs carry an accessible name', () => {
+  it('control ks1104 C0 the scan reaches the three mode tabs of the real page', () => {
+    expect(triggers.map((t) => t.testId)).toEqual(['tab-upload', 'tab-id', 'tab-qr']);
+  });
+
+  it('RED ks1104 R1 every mode tab carries a non-empty aria-label', () => {
+    expect(triggers.filter((t) => !t.labelled).map((t) => t.testId)).toEqual([]);
+  });
+
+  it('RED ks1104 R2 the labels are the three names the tabs show at desktop width', () => {
+    expect(Object.fromEntries(triggers.map((t) => [t.testId, t.label]))).toEqual({
+      'tab-upload': 'Upload File',
+      'tab-id': 'Enter ID',
+      'tab-qr': 'Scan QR',
+    });
+  });
+
+  it('control ks1104 C1 the scan tells a labelled tab from an unlabelled one', () => {
+    const labelled = scanTabTriggers('const a = <TabsTrigger value="x" data-testid="t" aria-label="Name" />;');
+    expect(labelled.map((t) => t.labelled)).toEqual([true]);
+    const bare = scanTabTriggers('const a = <TabsTrigger value="x" data-testid="t"><span>Name</span></TabsTrigger>;');
+    expect(bare.map((t) => t.labelled)).toEqual([false]);
+    const commented = scanTabTriggers('const a = <TabsTrigger value="x" /* aria-label="Name" */ data-testid="t" />;');
+    expect(commented.map((t) => t.labelled)).toEqual([false]);
+    const empty = scanTabTriggers('const a = <TabsTrigger value="x" aria-label="" data-testid="t" />;');
+    expect(empty.map((t) => t.labelled)).toEqual([false]);
+    const dynamic = scanTabTriggers('const a = <TabsTrigger value="x" aria-label={name} data-testid="t" />;');
+    expect(dynamic.map((t) => t.labelled)).toEqual([false]);
+  });
+
+  it('control ks1104 C2 the visible tab text is still there', () => {
+    for (const text of ['Upload File', 'Enter ID', 'Scan QR']) {
+      expect(source).toContain(`>${text}</span>`);
+    }
+  });
+});
```
