# READY — KS-1639-TEXTFALSEINACTIVE-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1/out.md.checker/patch.diff`** (from `ls` at 00:18 2026-10-20; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1-control/out.md.checker/patch.diff` rc 0, Wednesday (overnight 10-20)).

**Held 00:18 2026-10-20 by Wednesday (overnight 10-20) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `bc3e2e2460fff5e961cd26b70da3ab0050fccbcc`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/converters.ts , Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/converters.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	1	Blockchain/Dev/services/security/src/converters.ts
44	0	Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/converters.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/converters.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1639 - rowToApiKey reads the Postgres text forms of false as inactive RED KS-1639 F1: the text form "f" reads INACTIVE, never active', 'KS-1639 - rowToApiKey reads the Postgres text forms of false as inactive RED KS-1639 F2: "false", "F", "FALSE" and a padded " f " all read inactive', 'KS-1639 - rowToApiKey reads the Postgres text forms of false as inactive RED KS-1639 F3: an unrecognised text value reads inactive (fail closed), not active']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=347 failed=0 | after: total=353 failed=0` · `NEW reds: []` [baseline_suite.json total=347 failed=0; after_suite.json total=353 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +48/-1 test=src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/converters.ts` (+4/-1 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts` (+44/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `bc3e2e2460fff5e961cd26b70da3ab0050fccbcc` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1639_p1/KS-1639.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-20_ks_1639_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/converters.ts b/Blockchain/Dev/services/security/src/converters.ts
index edacb6a7d..2faf51a40 100644
--- a/Blockchain/Dev/services/security/src/converters.ts
+++ b/Blockchain/Dev/services/security/src/converters.ts
@@ -170,3 +170,6 @@
     usageCount: Number(r.usage_count),
-    isActive: Boolean(r.is_active),
+    // KS-1639: a text value is active only when it is a text form of true; 'f' / 'false' (and anything unrecognised) read inactive.
+    isActive: typeof r.is_active === 'string'
+      ? /^(t|true)$/i.test(r.is_active.trim())
+      : Boolean(r.is_active),
     expiresAt: r.expires_at ? new Date(r.expires_at as string) : undefined,
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts
new file mode 100644
index 000000000..529a3f262
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1639-rowtoapikey-reads-the-text-forms-of-false-as-inactive.test.ts
@@ -0,0 +1,44 @@
+/**
+ * KS-1639 (gate O2's probe on #1601, KS-1525) - rowToApiKey read `isActive: Boolean(r.is_active)`, and Boolean() of any
+ * non-empty string is true, so the Postgres TEXT forms of false ('f', 'false') read ACTIVE: a revoked key could be
+ * un-revoked by a row that arrives as text (a ::text cast, row_to_json, a hand-built fixture). The mapper already
+ * honoured 't' (cell G10 in row-converters.test.ts); after the fix a string is active ONLY when it is a text form of
+ * true ('t' / 'true', any case, surrounding spaces ignored) and every other string reads inactive (fail closed).
+ * The control cells keep what must not change: real booleans, null and an absent column, and the 't' forms.
+ */
+import { describe, it, expect } from 'vitest';
+import { rowToApiKey } from '../converters';
+
+const ROW = {
+  id: 'key_1639', organization_id: 'org_1', tenant_id: 'a0000000-0000-4000-8000-000000000002', connector_id: 'conn_1',
+  name: 'connector-1639', key_hash: 'h', key_prefix: 'sk_t_', scopes: '["read:docs"]',
+  rate_limit: '100', rate_limit_window: '60', last_used_at: null, usage_count: '0',
+  expires_at: null, created_at: '2026-04-01T00:00:00Z',
+};
+const active = (v: unknown) => rowToApiKey({ ...ROW, is_active: v }).isActive;
+
+describe('KS-1639 - rowToApiKey reads the Postgres text forms of false as inactive', () => {
+  it('RED KS-1639 F1: the text form "f" reads INACTIVE, never active', () => {
+    expect(active('f')).toBe(false);
+  });
+
+  it('RED KS-1639 F2: "false", "F", "FALSE" and a padded " f " all read inactive', () => {
+    expect(['false', 'F', 'FALSE', ' f '].map(active)).toEqual([false, false, false, false]);
+  });
+
+  it('RED KS-1639 F3: an unrecognised text value reads inactive (fail closed), not active', () => {
+    expect(active('maybe')).toBe(false);
+  });
+
+  it('CONTROL KS-1639 T1: the text forms of true still read active', () => {
+    expect(['t', 'true', 'T', 'TRUE', ' t '].map(active)).toEqual([true, true, true, true, true]);
+  });
+
+  it('CONTROL KS-1639 B1: real booleans are unchanged', () => {
+    expect([active(true), active(false)]).toEqual([true, false]);
+  });
+
+  it('CONTROL KS-1639 N1: null, an empty string and an absent column all read inactive', () => {
+    expect([active(null), active(''), rowToApiKey(ROW).isActive]).toEqual([false, false, false]);
+  });
+});
```
