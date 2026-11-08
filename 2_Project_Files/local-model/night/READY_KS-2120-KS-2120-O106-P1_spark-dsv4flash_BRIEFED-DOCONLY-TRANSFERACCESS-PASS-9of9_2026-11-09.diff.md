# READY - KS-2120-KS-2120-O106-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2120_o106_p1_transfer_access_comment_names_the_platform_admin_login/out.md.checker/patch.diff` (from `ls` at 02:23 2026-11-09; sha256[:16] d45563b8fbb60ae3, 1598 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:23 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2120_o106_p1_transfer_access_comment_names_the_platform_admin_login/out.md.checker`; the expectations were RE-MEASURED here.** Tip `c0e6e744b7b21f3e1aa28105766764775b50ce6d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/transfer/src/services/transferAccess.ts']; `+` lines 3 (ASCII), `-` lines 1.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/transfer/src/services/transferAccess.ts)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (4 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `A person cannot gain them, because the login mints read role and level through closed tables that hold neither.` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `The platform-admin login does not read those tables: it mints` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `declares it with no CHECK.` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/transfer/src/services/transferAccess.ts
+++ b/Blockchain/Dev/services/transfer/src/services/transferAccess.ts
@@ -109,7 +109,9 @@
  * KS-2081: true when the verified token is not a person. Kam ruled that keys are never a party on these doors: card
  * secuura-ks2038-connector-principals-on-transfer-doors-1106 = a, "Keys are never a party on these doors (recommended)". Any one signal decides:
  *   - type, role or verificationLevel as auth's generateConnectorToken stamps them. A key cannot shed them, because they are constants in that mint.
- *     A person cannot gain them, because the login mints read role and level through closed tables that hold neither.
+ *     A person cannot gain them through the closed users tables, which hold neither. The platform-admin login does not read those tables: it mints
+ *     platform_admins.role as stored, so a person there could carry a connector role only if someone wrote one into that row (KS-2120). The docker
+ *     schema (docker/init-platform/01-platform-schema.sql) CHECKs that column to three values; the Azure migrate script (deployment/azure/migrate/run-platform.sh) declares it with no CHECK.
  *   - a user id that cannot be a users row. This also refuses a machine principal nobody has minted yet, which then comes back to Kam, as his card says.
  * So "no person's answer changes" rests on the schema and the mint, not on the shape of this test.
  * A missing, empty or non-string user id is NOT decided here: such a token keeps its answers, 401 at the id doors and the body fallback at the open door.
```
