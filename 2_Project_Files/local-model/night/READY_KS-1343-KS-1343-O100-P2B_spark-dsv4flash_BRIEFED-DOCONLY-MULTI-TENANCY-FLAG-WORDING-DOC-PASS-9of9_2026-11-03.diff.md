# READY - KS-1343-KS-1343-O100-P2B (spark-dsv4flash, briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1343_o100_p2b_multitenancy_flag_wording/out.md.checker/patch.diff` (from `ls` at 22:43 2026-11-03; sha256[:16] 4a1847666f3a7bf0, 1165 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 22:43 2026-11-03 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1343_o100_p2b_multitenancy_flag_wording/out.md.checker`; the expectations were RE-MEASURED here.** Tip `1cbf260548e7fd534603725f9fc6b05c5cdd9907`. Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1343_o100_p2b_multitenancy_flag_wording/KS-1343.md`
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/docs/MULTI-TENANCY.md']; `+` lines 3 (ASCII), `-` lines 2.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/docs/MULTI-TENANCY.md)`
  - `PASS A4 RED AT BASE: all 4 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (0 comment line(s) changed in 0 code file(s); 1 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 4 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 4/4 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `a distinction the first version of this correction got wrong` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `and it is off everywhere.` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `and in the repository it is off everywhere; live app` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `settings were not checked.` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/docs/MULTI-TENANCY.md
+++ b/Blockchain/Dev/docs/MULTI-TENANCY.md
@@ -50,10 +50,11 @@
   `migrations/050_documents_id_namespaces_disjoint.sql` adds a SECURITY DEFINER function that reads `documents`
   across tenants.
 - **A per-tenant-database path exists in the code and is dormant.** It is gated by **two** flags, and
-  they are in **different** states — a distinction the first version of this correction got wrong:
+  they are in **different** states:
   - `PROVISION_PER_TENANT_DB` (`tenant-pool-manager.ts:152`,
     `tenant-provisioning/src/index.ts:245`) is set in **no** configuration file in the repository.
-    **This is the flag that actually gates per-tenant databases**, and it is off everywhere.
+    **This is the flag that actually gates per-tenant databases**, and in the repository it is off everywhere; live app
+    settings were not checked.
   - `MULTI_TENANCY_ENABLED` (`tenant-pool-manager.ts:151`) is **ON in dev and demo**:
     `deployment/azure/env.dev.json:7` and `deployment/azure/env.demo.json:7` both set it to `"true"`,
     as does `deployment/azure/services.bicep:798`. It enables tenant *routing*; with
```
