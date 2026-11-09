# READY - KS-2150-KS-2150-O117-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 10/10 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2150_o117_p1_ks2109_fragments_state_the_pr_size_wrongly/out.md.checker/patch.diff` (from `ls` at 18:00 2026-11-09; sha256[:16] 317af8f0caf5776c, 4017 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 18:00 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2150_o117_p1_ks2109_fragments_state_the_pr_size_wrongly/out.md.checker`; the expectations were RE-MEASURED here.** Tip `e8d23ce366e292ed6ca13f296cc2cfb2a3796496`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Projects Documents/fragments/cheat/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html', 'Projects Documents/fragments/flow/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html']; `+` lines 2 (ASCII), `-` lines 2.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Projects Documents/fragments/cheat/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html, Projects Documents/fragments/flow/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html)`
  - `PASS A4 RED AT BASE: all 4 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (0 comment line(s) changed in 0 code file(s); 2 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 4 expectation(s) hold after the patch`
  - `PASS A6 DOC CHECK `node Blockchain/Dev/scripts/docs-fragments.mjs check` rc 0 after the patch (rc 0 at the tip)`
  - `PASS A7 REVERSION: with the patch reverse-applied, 4/4 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `<strong>2</strong> files against develop, <strong>+2 -2</strong>:` in `Projects Documents/fragments/cheat/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `<strong>4</strong> files against develop, <strong>+32 -2</strong>: the two edited files` in `Projects Documents/fragments/cheat/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_absent `Two lines of prose, in two files. PR 2060` in `Projects Documents/fragments/flow/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `in two files besides these fragments. PR 2060` in `Projects Documents/fragments/flow/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Projects Documents/fragments/cheat/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html
+++ b/Projects Documents/fragments/cheat/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html
@@ -13,7 +13,7 @@
 <h3>Figures</h3>
 <table>
 <tr><th>Figure</th><th>Value</th></tr>
-<tr><td>files, lines</td><td><strong>2</strong> files against develop, <strong>+2 -2</strong>: <code>trustHeaders.ts</code> (one comment line) and <code>AGENT-DOCUMENT-OPERATION-RULES.md</code> (one line)</td></tr>
+<tr><td>files, lines</td><td><strong>4</strong> files against develop, <strong>+32 -2</strong>: the two edited files, <strong>+2 -2</strong> (<code>trustHeaders.ts</code>, one comment line, and <code>AGENT-DOCUMENT-OPERATION-RULES.md</code>, one line), plus these two fragments</td></tr>
 <tr><td>code changed</td><td><strong>0</strong>: the TypeScript emit of <code>trustHeaders.ts</code> with comments removed is identical to develop's (790 bytes each); a planted code line makes it differ and a planted comment line does not</td></tr>
 <tr><td>suites, before then after</td><td>api-gateway 168 test files, 1880 tests, 0 failed on both sides; the 4 files that name <code>trustHeaders</code> 22 of 22; the shared <code>ks1536-one-role-vocabulary</code> guard 97 of 97; <code>eslint</code> 0 errors and 30 warnings and <code>tsc --noEmit</code> rc 0 with no output, both byte-identical before and after (measured 2026-11-09, Node v26.8.1)</td></tr>
 </table>
--- a/Projects Documents/fragments/flow/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html
+++ b/Projects Documents/fragments/flow/KS-2109-trustheaders-and-the-agent-rules-name-removed-role-lists.html
@@ -1,5 +1,5 @@
 <h2><!--n-->. Two pointers name role lists that PR 2060 removed (KS-2109, api-gateway)</h2>
-<table class="pmatrix"><tr><td class="pm-topic" rowspan="2"><strong>What this changes.</strong></td><td> Two lines of prose, in two files. PR 2060 (KS-1536 part 3a) removed the local role lists that the gateway checks used to carry, and two pointers still named them. In <code>services/api-gateway/src/utils/trustHeaders.ts</code>, a comment said the <code>x-tenant-override</code> header is gated on <code>SUPER_ADMIN_ROLES</code>; it now says the auth middleware gates on <code>isPlatformRole</code> (from <code>@secuura/shared</code>) before honouring it. In <code>docs/security/AGENT-DOCUMENT-OPERATION-RULES.md</code>, a line said <code>enforceAdminProxy</code> uses <code>PROXY_ADMIN_ROLES</code>, "which lists human roles only"; it now says <code>enforceAdminProxy</code> asks <code>isPlatformOrOrgAdminRole</code> and so admits <code>SYSTEM_ADMIN</code>, <code>SUPER_ADMIN</code> and <code>ORG_ADMIN</code> only: human roles.
+<table class="pmatrix"><tr><td class="pm-topic" rowspan="2"><strong>What this changes.</strong></td><td> Two lines of prose, in two files besides these fragments. PR 2060 (KS-1536 part 3a) removed the local role lists that the gateway checks used to carry, and two pointers still named them. In <code>services/api-gateway/src/utils/trustHeaders.ts</code>, a comment said the <code>x-tenant-override</code> header is gated on <code>SUPER_ADMIN_ROLES</code>; it now says the auth middleware gates on <code>isPlatformRole</code> (from <code>@secuura/shared</code>) before honouring it. In <code>docs/security/AGENT-DOCUMENT-OPERATION-RULES.md</code>, a line said <code>enforceAdminProxy</code> uses <code>PROXY_ADMIN_ROLES</code>, "which lists human roles only"; it now says <code>enforceAdminProxy</code> asks <code>isPlatformOrOrgAdminRole</code> and so admits <code>SYSTEM_ADMIN</code>, <code>SUPER_ADMIN</code> and <code>ORG_ADMIN</code> only: human roles.
     </td></tr><tr><td>One held Spark pass, applied strictly. The two files are independent, so the order does not matter. Nothing here is a runtime defect: gate 244 found that every gate it drove behaved as PR 2060 says, and the pointers were stale.
     </td></tr></table>
 <h3><!--n-->.1 What proves it</h3>
```
