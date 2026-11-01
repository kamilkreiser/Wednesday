# READY — KS-1898-KS-1898-O49-P1 (spark-dsv4flash, briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger/out.md.checker/patch.diff`** (from `ls` at 00:04 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 00:04 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d7691f35312ea158f043e87a3227e477cccb183d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
31	4	Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (28 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 31 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 4.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 28 line(s) byte-exact incl. leading whitespace (of 28; 31 line(s) added by the apply)` [a3i_indent.out: `OK 28 line(s) byte-exact incl. leading whitespace (of 28; 31 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `ce478a5459d41dd2` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts:306)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger_000155/clone/Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts:306: "      throw new AppError('Credential not found', 404);" -> "      if (record && record.owner.userId === null) { logger.warn('revoke refused', { reason }); throw new AppError('Credential not found', 404, undefined, { ownerless: true }); } throw new AppError('Credential not found', 404);"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 306. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts fails at the untouched tip (13 failed / 36 run; controls green; assertion reds)` [red_first.json: failed=13 of total=36; red cell(s): ['KS-1851 memory path: only the principal that issued a credential may revoke it V14a an OWNER of tenant 1 revokes an owner-less memory row -> 404 byte-identical to an unknown id; unchanged; reason not logged', 'KS-1851 memory path: only the principal that issued a credential may revoke it V14b an ORG_ADMIN of tenant 1 revokes an owner-less memory row -> 404 byte-identical to an unknown id; unchanged; reason not logged', 'KS-1851 memory path: only the principal that issued a credential may revoke it V14c a SYSTEM_ADMIN of tenant 1 revokes an owner-less memory row -> 404 byte-identical to an unknown id; unchanged; reason not logged', 'KS-1851 memory path: only the principal that issued a credential may revoke it V14d a SUPER_ADMIN of tenant 1 revokes an owner-less memory row -> 404 byte-identical to an unknown id; unchanged; reason not logged', "KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V8b an OWNER of the row's tenant revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged", 'KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V8c an ORG_ADMIN of ANOTHER tenant revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged', "KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V8d an ORG_ADMIN of the row's tenant with NO userId revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged", "KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V8e an ORG_ADMIN of the row's tenant (KS 1116 ruling (a) admitted it; KS-1906 does not) revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged", "KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V8f a SUPER_ADMIN of ANOTHER tenant (KS-1906 is bound to the row's tenant) revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged", "KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V8g a SUPER_ADMIN of the row's tenant with NO userId revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged", 'KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V9 a SYSTEM_ADMIN revokes a pre-054 row with no owner and no tenant -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged', 'KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V9 an ORG_ADMIN revokes a pre-054 row with no owner and no tenant -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged', 'KS-1851 database path: the owner comes from the row, and a refused revoke writes nothing V9 a SUPER_ADMIN revokes a pre-054 row with no owner and no tenant -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts passes with the product hunk (36 passed / 36 run)` [green_after.json: failed=0 of total=36, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=710 failed=0 | after: total=714 failed=0` · `NEW reds: []` [baseline_suite.json total=710 failed=0; after_suite.json total=714 failed=0]
- A6 [verbatim]: `PASS A6 whole services/vc-issuer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/vc-issuer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +31/-4 test=src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts` (+31/-4 per numstat.out); the product `Blockchain/Dev/services/vc-issuer/src/routes/credentials.ts` is the tamper target and is byte-unchanged (sha256 ce478a5459d41dd2, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `d7691f35312ea158f043e87a3227e477cccb183d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger/input.json`. Brief (given by --brief; its `# ` heading names KS-1898): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger/KS-1898.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1898_o49_p1_vcissuer_revoke_byte_identical_logger/checker.out`.

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts
@@ -182,3 +182,24 @@
     expectNotFound(await revoke(mods, ALICE, UNKNOWN_ID));
   });
+
+  // KS-1898: an owner-less row in MEMORY (stored with the default OWNERLESS owner, as a caller that forgets the owner does).
+  it.each([
+    ['V14a an OWNER of tenant 1', BOB],
+    ['V14b an ORG_ADMIN of tenant 1', ORG_ADMIN],
+    ['V14c a SYSTEM_ADMIN of tenant 1', SYSTEM_ADMIN],
+    ['V14d a SUPER_ADMIN of tenant 1', SUPER_ADMIN],
+  ])('%s revokes an owner-less memory row -> 404 byte-identical to an unknown id; unchanged; reason not logged', async (_label, caller) => {
+    const id = 'https://secuura.io/credentials/1851d0b0-0000-4000-8000-000000000014';
+    await mods.repo.store(storedCredential(id));
+    const before = JSON.stringify(await mods.repo.getById(id));
+    Object.values(loggerMock).forEach((fn) => fn.mockClear());
+
+    const refused = await revoke(mods, caller, id);
+
+    expectNotFound(refused);
+    expectNothingLoggedForTheRefusal();
+    expect(JSON.stringify(await mods.repo.getById(id))).toBe(before);
+    expect((await mods.repo.getById(id))?.credentialStatus?.revoked).not.toBe(true);
+    expectByteIdentical(refused, await revoke(mods, caller, UNKNOWN_ID));
+  });
 });
@@ -250,6 +271,9 @@
     ['V8f a SUPER_ADMIN of ANOTHER tenant (KS-1906 is bound to the row\'s tenant)', { ...SUPER_ADMIN, tenantId: T2 }],
     ['V8g a SUPER_ADMIN of the row\'s tenant with NO userId', { tenantId: T1, role: 'SUPER_ADMIN', email: SUPER_ADMIN.email, verificationLevel: 'BASIC' }],
-  ])('%s revokes an owner-less row of tenant 1 -> 404 and NO UPDATE', async (_label, caller) => {
-    expectNotFound(await revoke(mods, caller, OWNERLESS_T1_ROW));
+  ])('%s revokes an owner-less row of tenant 1 -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged', async (_label, caller) => {
+    const refused = await revoke(mods, caller, OWNERLESS_T1_ROW);
+    expectNotFound(refused);
     expect(updates()).toEqual([]);
+    expectNothingLoggedForTheRefusal();
+    expectByteIdentical(refused, await revoke(mods, caller, UNKNOWN_ID));
   });
@@ -259,7 +283,10 @@
     ['V9 an ORG_ADMIN', ORG_ADMIN],
     ['V9 a SUPER_ADMIN', SUPER_ADMIN],
-  ])('%s revokes a pre-054 row with no owner and no tenant -> 404 and NO UPDATE', async (_label, caller) => {
-    expectNotFound(await revoke(mods, caller, LEGACY_ROW));
+  ])('%s revokes a pre-054 row with no owner and no tenant -> 404 byte-identical to an unknown id, NO UPDATE, reason not logged', async (_label, caller) => {
+    const refused = await revoke(mods, caller, LEGACY_ROW);
+    expectNotFound(refused);
     expect(updates()).toEqual([]);
+    expectNothingLoggedForTheRefusal();
+    expectByteIdentical(refused, await revoke(mods, caller, UNKNOWN_ID));
   });
 });
```
