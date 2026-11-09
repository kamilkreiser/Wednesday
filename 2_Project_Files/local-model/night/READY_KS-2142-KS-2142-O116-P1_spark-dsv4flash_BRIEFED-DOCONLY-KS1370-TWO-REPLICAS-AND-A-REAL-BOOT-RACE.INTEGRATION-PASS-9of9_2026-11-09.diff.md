# READY - KS-2142-KS-2142-O116-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2142_o116_p1_ks1370_b2_comment_marks_may_change_and_load_flake/out.md.checker/patch.diff` (from `ls` at 17:47 2026-11-09; sha256[:16] b9e648e7b3930f44, 1490 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 17:47 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2142_o116_p1_ks1370_b2_comment_marks_may_change_and_load_flake/out.md.checker`; the expectations were RE-MEASURED here.** Tip `e8d23ce366e292ed6ca13f296cc2cfb2a3796496`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/security/src/__tests__/ks1370-two-replicas-and-a-real-boot-race.integration.test.ts']; `+` lines 4 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/security/src/__tests__/ks1370-two-replicas-and-a-real-boot-race.integration.test.ts)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (5 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `// answers and the flag is still down.` in `Blockchain/Dev/services/security/src/__tests__/ks1370-two-replicas-and-a-real-boot-race.integration.test.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `fail pin B2 (F-2071-2): that is a load flake of the timing` in `Blockchain/Dev/services/security/src/__tests__/ks1370-two-replicas-and-a-real-boot-race.integration.test.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `A later fix under KS-1370 or KS-1377 may change it` in `Blockchain/Dev/services/security/src/__tests__/ks1370-two-replicas-and-a-real-boot-race.integration.test.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/security/src/__tests__/ks1370-two-replicas-and-a-real-boot-race.integration.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1370-two-replicas-and-a-real-boot-race.integration.test.ts
@@ -272,7 +272,8 @@
       seen.storedClosed = await validate(inst, K1);
 
       // db.ts backs off 1 s, 2 s, 4 s. After the second failed retry the next probe is 4 s away: that is the window where the database
-      // answers and the flag is still down.
+      // answers while the flag is still down. If the event loop stalls past that 4 s, the retry timer can fire first, flip the flag and
+      // fail pin B2 (F-2071-2): that is a load flake of the timing, not a regression of the boot probe.
       const failedRetries = () => logs.mock.calls.filter((c) => String(c[0]).includes('Database still unavailable')).length;
       await waitFor('two failed retries', () => failedRetries() >= 2, 20_000);
       await relay.open();
@@ -321,6 +322,8 @@
     expect(seen.storedClosed).toMatchObject({ status: 503, message: 'Unable to verify key' });
   });
 
+  // pin B2 (F-2071-1): pins what develop does today in that window. A later fix under KS-1370 or KS-1377 may change it; B2 going red
+  // then is that change being made, not a regression.
   it('pin B2: the database answers, the flag is still down, and a validate reads the stored row and warms memory', () => {
     expect(seen.flagAtWarm).toBe(false);
     expect(seen.flagAfterWarm).toBe(false);
```
