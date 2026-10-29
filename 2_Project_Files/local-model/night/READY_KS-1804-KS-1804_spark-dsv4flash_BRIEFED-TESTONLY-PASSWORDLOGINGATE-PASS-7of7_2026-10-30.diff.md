# READY — KS-1804-KS-1804 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1804_p1_burn_exactly_once/out.md.checker/patch.diff`** (from `ls` at 08:58 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1804_p1_burn_exactly_once/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 08:58 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1804_p1_burn_exactly_once/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `593cd90c3131f200f4adaf242c1a406a5b66fbb0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	0	Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (11 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 14 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 11 line(s) byte-exact incl. leading whitespace (of 11; 14 line(s) added by the apply)` [a3i_indent.out: `OK 11 line(s) byte-exact incl. leading whitespace (of 11; 14 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `b11d690dc858e92b` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts:281)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1804_p1_burn_exactly_once_075953/clone/Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts:281: '          await userRepo.updateUserOrThrow(' -> "          await userRepo.updateUserOrThrow(user.id, { mfaBackupCodes: user.mfaBackupCodes }, 'tamper').catch(() => undefined); await userRepo.updateUserOrThrow("` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 281. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts fails at the untouched tip (2 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=2 of total=8; red cell(s): ['KS-1188 F3 - the 503 around a backup-code burn says the code may already be spent RED KS-1804 N2 a healthy backup-code sign-in burns the code with exactly one UPDATE users', 'KS-1188 F3 - the 503 around a backup-code burn says the code may already be spent RED KS-1804 N2 the faulted case (the read-back fails after the burn landed) still issued exactly one UPDATE users']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1326 failed=1 | after: total=1328 failed=0` · `NEW reds: []` [baseline_suite.json total=1326 failed=1; after_suite.json total=1328 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +14/-0 test=src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts` (+14/-0 per numstat.out); the product `Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts` is the tamper target and is byte-unchanged (sha256 b11d690dc858e92b, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `593cd90c3131f200f4adaf242c1a406a5b66fbb0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1804_p1_burn_exactly_once/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1804_p1_burn_exactly_once/checker.out`.

```diff
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1188-f3-a-spent-backup-code-503-says-so.test.ts
@@ -156,4 +156,18 @@
     await expect(assertAccountMayReceiveCredential(mfaUser(), input(BACKUP_CODE))).resolves.toEqual({ ok: true });
     expect(state.recordSuccess).toBe(1);
   });
+
+  // KS-1804 note 2 (KS-1188 F3 gate note carried on KS-1467): the two cells that look at `state.queries` only ask whether SOME `UPDATE users` ran (or none). Nothing counted them, so a burn that runs twice stayed green.
+  const burns = () => state.queries.filter((q) => /^\s*UPDATE\s+users/i.test(q.sql));
+
+  it('RED KS-1804 N2 a healthy backup-code sign-in burns the code with exactly one UPDATE users', async () => {
+    await expect(assertAccountMayReceiveCredential(mfaUser(), input(BACKUP_CODE))).resolves.toEqual({ ok: true });
+    expect(burns()).toHaveLength(1);
+  });
+
+  it('RED KS-1804 N2 the faulted case (the read-back fails after the burn landed) still issued exactly one UPDATE users', async () => {
+    state.readBackFails = CONNECTION_LOST;
+    await rejection(BACKUP_CODE);
+    expect(burns()).toHaveLength(1);
+  });
 });
```
