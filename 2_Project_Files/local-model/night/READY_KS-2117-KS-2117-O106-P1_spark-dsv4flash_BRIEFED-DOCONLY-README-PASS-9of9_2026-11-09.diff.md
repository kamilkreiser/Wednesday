# READY - KS-2117-KS-2117-O106-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2117_o106_p1b_sdk_readme_transfer_calls_need_an_access_token/out.md.checker/patch.diff` (from `ls` at 02:23 2026-11-09; sha256[:16] 499789e89627591e, 495 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:23 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2117_o106_p1b_sdk_readme_transfer_calls_need_an_access_token/out.md.checker`; the expectations were RE-MEASURED here.** Tip `c0e6e744b7b21f3e1aa28105766764775b50ce6d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/sdk/javascript/README.md']; `+` lines 4 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/sdk/javascript/README.md)`
  - `PASS A4 RED AT BASE: all 4 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (0 comment line(s) changed in 0 code file(s); 1 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 4 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 4/4 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `// Approve a transfer` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `refuse every API key with 403 (KS-2081).` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `// Build the client with an accessToken for these calls` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `// Then approve it` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/sdk/javascript/README.md
+++ b/Blockchain/Dev/sdk/javascript/README.md
@@ -136,7 +136,10 @@
   requiresApproval: true,
 });
 
-// Approve a transfer
+// NOTE: the transfer write routes (initiate, approve and cancel) refuse every API key with 403 (KS-2081).
+// Build the client with an accessToken for these calls, not with the apiKey from Quick Start.
+
+// Then approve it
 await client.transfers.approve(transferId, 'approve', {
   comment: 'Approved for transfer',
 });
```
