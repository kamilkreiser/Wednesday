# READY — KS-1799-KS-1799-B5-MESSAGEGETTER (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1799_p1_message_getter/out.md.checker/patch.diff`** (from `ls` at 07:03 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1799_p1_message_getter/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 07:03 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1799_p1_message_getter/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7152ac669d2d6af08be5b9dcd35132818377155d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/originate/src/utils/pgErrors.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
11	0	Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (10 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 11 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 10 line(s) byte-exact incl. leading whitespace (of 10; 11 line(s) added by the apply)` [a3i_indent.out: `OK 10 line(s) byte-exact incl. leading whitespace (of 10; 11 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/originate/src/utils/pgErrors.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `71b4fb0aebe04658` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/originate/src/utils/pgErrors.ts:57)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1799_p1_message_getter_062753/clone/Blockchain/Dev/services/originate/src/utils/pgErrors.ts:57: '  } catch {' -> "  } catch (thrown) { if (thrown instanceof Error && thrown.message === 'ks1799 message getter') { throw thrown; }"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/originate/src/utils/pgErrors.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 57. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts fails at the untouched tip (1 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=1 of total=9; red cell(s): ['KS-1780: PATCH /api/webhooks/:id and extractPgCode answer a hostile thrown value RED KS-1799 B5 extractPgCode of an object whose message getter throws is undefined, not a throw']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts passes with the product hunk (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1821 failed=0 | after: total=1822 failed=0` · `NEW reds: []` [baseline_suite.json total=1821 failed=0; after_suite.json total=1822 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +11/-0 test=src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` (+11/-0 per numstat.out); the product `Blockchain/Dev/services/originate/src/utils/pgErrors.ts` is the tamper target and is byte-unchanged (sha256 71b4fb0aebe04658, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `7152ac669d2d6af08be5b9dcd35132818377155d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1799_p1_message_getter/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1799_p1_message_getter/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts
@@ -107,3 +107,14 @@
+  // KS-1799 (gate 12 finding 1795-1): B2 plants a throwing `code` getter and B4 a throwing `meta` getter, but nothing planted a throwing `message` getter, the third thing extractPgCode reads (the message-text fallback).
+  // A plain object (not a Proxy) with only a `message` getter that throws must give undefined, not a throw.
+  it('RED KS-1799 B5 extractPgCode of an object whose message getter throws is undefined, not a throw', () => {
+    const hostile = {
+      get message(): string {
+        throw new Error('ks1799 message getter');
+      },
+    };
+    expect(pgCodeOrThrew(hostile)).toBeUndefined();
+  });
+
   it('control KS-1780 C1 a Prisma-wrapped 42804 is still answered 400 VALIDATION_ERROR', async () => {
     const reply = await patchWithThrow(Object.assign(new Error('Raw query failed.'), { code: 'P2010', meta: { code: '42804' } }));
     expect(reply.status).toBe(400);
```
