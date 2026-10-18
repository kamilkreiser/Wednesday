# READY — KS-1377-APIKEYUSAGEATOMIC-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1/out.md.checker/patch.diff`** (from `ls` at 10:44 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:44 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `78cb3c3939e319332e387ffecb075a169edd4a39`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/security/src/index.ts , Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/security/src/index.ts
19	0	Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 2 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/security/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)` [a3i_indent.out: `OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts` (hunks=4, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1370-validate-reads-stored-revoke.test.ts fails at the untouched tip (1 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=1 of total=10; red cell(s): ['KS-1370: validate answers on the STORED revoke, and its usage write cannot revive one RED KS-1377 W3 N-1338-3: the usage write counts IN the database and does not write the process-local count back']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1370-validate-reads-stored-revoke.test.ts passes with the product hunk (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=343 failed=0 | after: total=344 failed=0` · `NEW reds: []` [baseline_suite.json total=343 failed=0; after_suite.json total=344 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +21/-2 test=src/__tests__/ks1370-validate-reads-stored-revoke.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts` (+19/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `78cb3c3939e319332e387ffecb075a169edd4a39` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1377_p1/KS-1377.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1377_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/index.ts b/Blockchain/Dev/services/security/src/index.ts
index c945b2f2d..07ac412a4 100644
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -498,4 +498,4 @@
     await runWithTenantId(k.tenantId, () => query(
-      `UPDATE svc_api_keys SET last_used_at = $2, usage_count = $3 WHERE id = $1`,
-      [k.id, k.lastUsedAt || null, k.usageCount]
+      `UPDATE svc_api_keys SET last_used_at = GREATEST(last_used_at, $2), usage_count = usage_count + 1 WHERE id = $1`,
+      [k.id, k.lastUsedAt || null]
     ));
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts
index 81f5ed5b9..b356aa2de 100644
--- a/Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1370-validate-reads-stored-revoke.test.ts
@@ -33,2 +33,4 @@
 
+const usageParams = vi.hoisted(() => [] as unknown[][]);
+
 vi.mock('../db', () => ({
@@ -47,2 +49,3 @@
       state.usageSql.push(sql);
+      usageParams.push(params ?? []);
       return { rows: [], rowCount: 1 };
@@ -135,2 +138,17 @@
 
+  it('RED KS-1377 W3 N-1338-3: the usage write counts IN the database and does not write the process-local count back', async () => {
+    state.stored.set(HASH, storedRow(true));
+    cacheKey(true);
+    usageParams.length = 0;
+    await validate();
+    const sql = state.usageSql.join('\n');
+    expect({
+      writes: state.usageSql.length,
+      incrementsInSql: /usage_count\s*=\s*usage_count\s*\+\s*1/.test(sql),
+      lastUsedNeverMovesBack: /last_used_at\s*=\s*GREATEST\(\s*last_used_at\s*,\s*\$2\s*\)/.test(sql),
+      writesOwnCopy: /\$3/.test(sql),
+      paramCount: usageParams.length === 1 ? usageParams[0].length : -1,
+    }).toEqual({ writes: 1, incrementsInSql: true, lastUsedNeverMovesBack: true, writesOwnCopy: false, paramCount: 2 });
+  });
+
   it('V1 half (ii): a STALE cache saying active cannot honour a key the store has revoked', async () => {
@@ -165,2 +183,3 @@
       .toEqual({ valid: false, reason: 'Key not found', evicted: true });
+    expect(state.usageSql.length, 'a vanished row is answered, not written: no INSERT and no UPDATE was issued').toBe(0);
   });
```
