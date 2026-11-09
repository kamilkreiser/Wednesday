# READY - KS-716-KS-716-O120-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_716_o120_p1_akto_secrets_example_says_system_admin_absent_only_skips_one_role/out.md.checker/patch.diff` (from `ls` at 21:37 2026-11-09; sha256[:16] d625095d8f5331b6, 1451 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 21:37 2026-11-09 by Spark operator o120 (priority-triage seat for the 18:46 Wednesday) after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_716_o120_p1_akto_secrets_example_says_system_admin_absent_only_skips_one_role/out.md.checker`; the expectations were RE-MEASURED here.** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['systemTest/akto/config/secrets.example.yml']; `+` lines 6 (2 NON-ASCII chars), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (systemTest/akto/config/secrets.example.yml)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (7 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `# issuer/verifier/system_admin are optional` in `systemTest/akto/config/secrets.example.yml` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `It is ALSO the HAR replay's admin fallback` in `systemTest/akto/config/secrets.example.yml` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `but not for scan coverage` in `systemTest/akto/config/secrets.example.yml` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/systemTest/akto/config/secrets.example.yml
+++ b/systemTest/akto/config/secrets.example.yml
@@ -32,8 +32,13 @@
 #                the admin user-management API (which requires SYSTEM_ADMIN/ORG_ADMIN — the `admin`
 #                block above is ISSUER_ADMIN locally and cannot). Absent ⇒ that one role is skipped
 #                (best-effort), and AUTH_BYPASS_LOCKED_ACCOUNT_TOKEN_ROLE keeps skipping honestly.
+#                It is ALSO the HAR replay's admin fallback: harTraffic.ts sets adminToken to null unless both systemAdminEmail
+#                and systemAdminPassword are set. Absent ⇒ every endpoint the issuer token cannot get a 2xx from keeps no captured
+#                sample, stays a spec-imported placeholder that Akto's api_selection_filters exclude from the authz templates, and
+#                the scan reports green over it (KS-716 measured 0 of 16 super-admin-only endpoints scanned without this block).
 #
-# issuer/verifier/system_admin are optional — when absent, tests fall back to admin (KS-194) or skip (KS-357).
+# issuer/verifier are optional — when absent, tests fall back to admin (KS-194) or skip (KS-357). system_admin is optional for the setup
+# seed above but not for scan coverage (see the HAR replay note under system_admin).
 #
 # Default values below match the dev/local seed accounts created by
 # ALLOW_DEFAULT_SEED_PASSWORDS=true in Blockchain/Dev/.env (KS-955: NOT .env.local —
```
