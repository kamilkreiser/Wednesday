# READY — KS-1670-KS-1670-ks_1670_p1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/out.md.checker/patch.diff`** (from `ls` at 14:15 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1-control/out.md.checker/patch.diff` rc 0, Spark operator for Wednesday).

**Held 14:15 2026-10-28 by Spark operator for Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/m365-integration/src/index.ts , Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/index.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/m365-integration/src/index.ts
55	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/m365-integration/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1670: the m365 success redirect encodes the connection id RED KS-1670 R1 every connectionId interpolation in a redirect query is wrapped in encodeURIComponent', 'KS-1670: the m365 success redirect encodes the connection id RED KS-1670 R2 the success redirect carries the encoded connection id and the encoded tenant, in that order']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=266 failed=0 | after: total=271 failed=0` · `NEW reds: []` [baseline_suite.json total=266 failed=0; after_suite.json total=271 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +56/-1 test=src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/index.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts` (+55/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1670): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1670_p1/KS-1670.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/m365-integration/src/index.ts b/Blockchain/Dev/services/m365-integration/src/index.ts
--- a/Blockchain/Dev/services/m365-integration/src/index.ts
+++ b/Blockchain/Dev/services/m365-integration/src/index.ts
@@ -677,4 +677,4 @@
-    res.redirect(`${process.env.FRONTEND_URL || 'http://localhost:6882'}/admin/integrations?m365=success&connectionId=${connectionId}&tenant=${encodeURIComponent(connection.tenantName || '')}`);
+    res.redirect(`${process.env.FRONTEND_URL || 'http://localhost:6882'}/admin/integrations?m365=success&connectionId=${encodeURIComponent(connectionId)}&tenant=${encodeURIComponent(connection.tenantName || '')}`);
   } catch (err: any) {
     connection.status = 'error';
     connection.errorMessage = err?.message || 'Token exchange failed';
diff --git a/Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts
@@ -0,0 +1,55 @@
+// KS-1670 site 1 (m365-integration src/index.ts, GET /api/callback success redirect): the redirect put `connectionId` into the query string unencoded, while `tenant` in the same template was
+// encoded with encodeURIComponent. The id only reaches that line after the server's own connection lookup hits, so it is not exploitable today, but an id format that ever admitted `&`, `#` or `%`
+// would change the shape of the query. This file reads the route's source text (no app boot, no database) and pins that every `connectionId=${...}` interpolation in the file is wrapped in
+// encodeURIComponent, and that the success redirect still encodes the tenant. C1 to C3 prove the instrument finds the route and the redirects it must not disturb.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+
+const SRC = readFileSync(join(__dirname, '..', 'index.ts'), 'utf8');
+const NEEDLE = 'connectionId=${';
+
+/** Every interpolation that follows `connectionId=${` in the source, as the text up to the closing `}` of the template expression. */
+function interpolations(): string[] {
+  const found: string[] = [];
+  let at = SRC.indexOf(NEEDLE);
+  while (at !== -1) {
+    const start = at + NEEDLE.length;
+    let depth = 1;
+    let i = start;
+    while (i < SRC.length && depth > 0) {
+      if (SRC[i] === '{') depth++;
+      else if (SRC[i] === '}') depth--;
+      i++;
+    }
+    found.push(SRC.slice(start, i - 1));
+    at = SRC.indexOf(NEEDLE, i);
+  }
+  return found;
+}
+
+describe('KS-1670: the m365 success redirect encodes the connection id', () => {
+  it('RED KS-1670 R1 every connectionId interpolation in a redirect query is wrapped in encodeURIComponent', () => {
+    const unwrapped = interpolations().filter((expr) => !/^encodeURIComponent\(.*\)$/.test(expr.trim()));
+    expect(unwrapped).toEqual([]);
+  });
+
+  it('RED KS-1670 R2 the success redirect carries the encoded connection id and the encoded tenant, in that order', () => {
+    expect(SRC).toContain('m365=success&connectionId=${encodeURIComponent(connectionId)}&tenant=${encodeURIComponent(connection.tenantName');
+  });
+
+  it('control KS-1670 C1 the instrument finds exactly one connectionId interpolation (the success redirect)', () => {
+    expect(interpolations()).toHaveLength(1);
+  });
+
+  it('control KS-1670 C2 the success redirect is still the one that follows the "connection completed" log line', () => {
+    const logAt = SRC.indexOf('OAuth callback: connection completed');
+    const redirectAt = SRC.indexOf('m365=success');
+    expect(logAt).toBeGreaterThan(-1);
+    expect(redirectAt).toBeGreaterThan(logAt);
+  });
+
+  it('control KS-1670 C3 the invalid_state refusal redirect is untouched', () => {
+    expect(SRC).toContain('/admin/integrations?m365=error&message=invalid_state');
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD
- Source-read: the one `res.redirect` template line at m365-integration src/index.ts (success branch, after "connection completed") changes only `connectionId=${connectionId}` to `connectionId=${encodeURIComponent(connectionId)}`; for every id the server issues the redirect is byte-for-byte the same. Site 1 ONLY: sites 2 and 3 of KS-1670 wait for the KS-1641 `:515` decision and are not here; the raise seat must NOT close-word KS-1670 on this PR (Refs).
- The test is a source-text pin (5 cells; reads index.ts, boots nothing): it proves the text, not the redirect on the wire. State that in the PR body.
- SEQUENCE: no shared file with any other held pass.
- Verdict: HOLD.
