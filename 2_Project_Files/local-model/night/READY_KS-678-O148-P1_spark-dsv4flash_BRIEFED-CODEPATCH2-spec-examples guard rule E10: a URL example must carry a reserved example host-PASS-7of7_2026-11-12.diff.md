# READY — KS-678-O148-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_678_o147_p3_spec_examples_guard_e10_url_host/out.md.checker/patch.diff`** (from `ls` at 02:21 2026-11-12; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_678_o147_p3_spec_examples_guard_e10_url_host/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_678_o147_p3_spec_examples_guard_e10_url_host/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_678_o147_p3_spec_examples_guard_e10_url_host/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_678_o147_p3_spec_examples_guard_e10_url_host/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 02:21 2026-11-12 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_678_o147_p3_spec_examples_guard_e10_url_host/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `dbde0ac763392432ac641d933b7a8bc9d3b78df7`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs , Blockchain/Dev/scripts/spec-examples/check/contract.mjs } + { Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
17	0	Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs
1	0	Blockchain/Dev/scripts/spec-examples/check/contract.mjs
89	0	Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (18 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: rules-example.mjs contract.mjs`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs`, `Blockchain/Dev/scripts/spec-examples/check/contract.mjs`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs 17 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/spec-examples/check/contract.mjs 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts 89 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/spec-examples/check/contract.mjs` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 88 run; controls green; assertion reds)` [red_first.json: failed=3 of total=88; red cell(s): ['KS-678 — rule E10: a URL example must carry a reserved example host RED ks678 R1 fires E10 on a URL whose host is not reserved, and names the field', 'KS-678 — rule E10: a URL example must carry a reserved example host RED ks678 R2 fires E10 on a URL inside an object example too', 'KS-678 — rule E10: a URL example must carry a reserved example host RED ks678 R3 does not treat a host that merely ends in the reserved name as reserved']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (88 passed / 88 run)` [green_after.json: failed=0 of total=88, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1623 failed=1 | after: total=1628 failed=1` · `NEW reds: []` [baseline_suite.json total=1623 failed=1; after_suite.json total=1628 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs` (+17/-0 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts` (+89/-0); 3 files in all (code_patch2: products Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs, Blockchain/Dev/scripts/spec-examples/check/contract.mjs). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `dbde0ac763392432ac641d933b7a8bc9d3b78df7` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_678_o147_p3_spec_examples_guard_e10_url_host/input.json`. Brief (given by --brief; its `# ` heading names KS-678): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_678_o147_p3_spec_examples_guard_e10_url_host/KS-678.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_678_o147_p3_spec_examples_guard_e10_url_host/checker.out`.

```diff
diff --git a/Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs b/Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs
--- a/Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs
+++ b/Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs
@@ -53,4 +53,21 @@
     checkAccountId(node, docPath, allow, findings, field);
     checkUsableCredential(node, docPath, allow, findings, field);
+    // E10 (KS-678): a value that parses as an http(s) URL must carry a host RFC 2606 / RFC 6761 reserves (or `localhost`), or a subdomain of
+    // one. E1 reads addresses only, so a URL on any domain used to pass every rule; an allowlist entry with a reason excuses one example.
+    if (/^https?:\/\//i.test(node)) {
+      let host = '';
+      try {
+        host = new URL(node).hostname.toLowerCase();
+      } catch {
+        host = '';
+      }
+      const reserved = ['example.com', 'example.org', 'example.net', 'localhost'];
+      if (host && !reserved.some((name) => host === name || host.endsWith(`.${name}`)) && !isAllowed(allow, 'E10', docPath)) {
+        record(findings, 'E10', docPath, node,
+          `URL host "${host}" is not a reserved example host (example.com, example.org, example.net, localhost) — ` +
+          'a published URL on any other domain names a place anyone may register',
+          field);
+      }
+    }
     return;
   }
diff --git a/Blockchain/Dev/scripts/spec-examples/check/contract.mjs b/Blockchain/Dev/scripts/spec-examples/check/contract.mjs
--- a/Blockchain/Dev/scripts/spec-examples/check/contract.mjs
+++ b/Blockchain/Dev/scripts/spec-examples/check/contract.mjs
@@ -305,2 +305,3 @@
   E9: 'usable-credential a request example pairing an email with a real password',
+  E10: 'url-host          a URL example whose host is not a reserved example host (KS-678)',
 };
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts
@@ -632,2 +632,91 @@
   });
 });
+
+describe('KS-678 — rule E10: a URL example must carry a reserved example host', () => {
+  /**
+   * E1 reads addresses only (it splits on `@`), so `https://example.secuura.io/resource` passed every rule while naming
+   * a domain that does not resolve and that anyone could register. E10 reads values that parse as an http(s) URL and
+   * accepts a host that is a reserved name (example.com, example.org, example.net, localhost) or a subdomain of one.
+   */
+  const guardPath = path.resolve(
+    path.dirname(fileURLToPath(import.meta.url)),
+    '../../../../scripts/spec-examples/check-spec-examples.mjs',
+  );
+
+  /** @returns the guard's JSON report for a spec written to a temp file. */
+  function runGuardOn(spec: string): { findings: { rule: string; field: string; value: string }[] } {
+    const specPath = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'ks678-')), 'spec.yaml');
+    fs.writeFileSync(specPath, spec);
+    try {
+      const stdout = execFileSync('node', [guardPath, '--spec', specPath, '--json'], {
+        encoding: 'utf8',
+      });
+      return JSON.parse(stdout);
+    } catch (err) {
+      return JSON.parse((err as { stdout: string }).stdout);
+    } finally {
+      fs.rmSync(path.dirname(specPath), { recursive: true, force: true });
+    }
+  }
+
+  /** A one-schema spec whose `webhookUrl` property carries `example`. */
+  function urlSpec(example: string): string {
+    return [
+      'openapi: 3.0.3',
+      'info:',
+      '  title: KS-678',
+      'components:',
+      '  schemas:',
+      '    Hook:',
+      '      type: object',
+      '      properties:',
+      '        webhookUrl:',
+      '          type: string',
+      `          example: ${example}`,
+    ].join('\n');
+  }
+
+  it('RED ks678 R1 fires E10 on a URL whose host is not reserved, and names the field', () => {
+    const findings = runGuardOn(urlSpec('https://example.secuura.io/resource')).findings;
+    expect(findings.map((f) => f.rule)).toContain('E10');
+    expect(findings.find((f) => f.rule === 'E10')?.field).toBe('webhookUrl');
+  });
+
+  it('RED ks678 R2 fires E10 on a URL inside an object example too', () => {
+    const findings = runGuardOn(
+      [
+        'openapi: 3.0.3',
+        'info:',
+        '  title: KS-678',
+        'components:',
+        '  schemas:',
+        '    Hook:',
+        '      type: object',
+        '      example:',
+        '        successUrl: https://checkout.secuura.io/done',
+      ].join('\n'),
+    ).findings;
+    expect(findings.map((f) => f.rule)).toContain('E10');
+  });
+
+  it('control ks678 C1 stays silent on the reserved hosts and their subdomains', () => {
+    for (const url of [
+      'https://example.com/resource',
+      'https://api.example.com/v1',
+      'https://example.org/x',
+      'http://example.net:8080/x',
+      'http://localhost:6882/x',
+    ]) {
+      expect(runGuardOn(urlSpec(url)).findings.filter((f) => f.rule === 'E10')).toHaveLength(0);
+    }
+  });
+
+  it('RED ks678 R3 does not treat a host that merely ends in the reserved name as reserved', () => {
+    const findings = runGuardOn(urlSpec('https://notexample.com/resource')).findings;
+    expect(findings.map((f) => f.rule)).toContain('E10');
+  });
+
+  it('control ks678 C3 stays silent on a value that is not a URL', () => {
+    expect(runGuardOn(urlSpec('not-a-url')).findings.filter((f) => f.rule === 'E10')).toHaveLength(0);
+  });
+});
```

> NOTE (operator o145, 2026-11-12): round passed at develop dbde0ac76339 (pin moved from 4f85ca04 at 02:09); real spec 422 blocks 0 findings after; planted webhookUrl https://example.secuura.io/resource rc 0 before, E10 1 finding rc 1 after; subdomains of a reserved name pass (design call); WHOLE-suite red (KS-278 signature test) is in the baseline.
