# READY — KS-1624-BANNERBASE-2 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p2/out.md.checker/patch.diff`** (from `ls` at 01:35 2026-10-19; sha256[:16] 6c3c155b5fe53eb1, 2058 B; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p2/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p2-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1): change lines (`+`/`-`, ordered) IDENTICAL in every section; APPLIED PRODUCT(S): the two checkers' own `after_index.ts` IDENTICAL (`cmp` rc 0). Run's own golden_cmp.out [verbatim]: `golden tree 2bb2160c0a4c2df6731c1e2ffad0e0984572e9ec · patch tree 2bb2160c0a4c2df6731c1e2ffad0e0984572e9ec -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1624_p2_013052/*_cmp.index.out)`.

**Held 01:35 2026-10-19 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p2/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `8a9970511f22661d92f634058fae8c08c656124f`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8a9970511f22661d92f634058fae8c08c656124f, Blockchain/Dev/connectors/whatsapp-bot/src/index.ts and Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/connectors/whatsapp-bot/src/index.ts', 'Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/connectors/whatsapp-bot/src/index.ts } + { Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 1 must_change site(s) of index.ts are '-' lines, no stays-site removed; all 2 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 2 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 1/1 of `Blockchain/Dev/connectors/whatsapp-bot/src/index.ts` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/connectors/whatsapp-bot/src/index.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh 9 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1624_p2/KS-1624.md`]: `File:` lines == product_files ['Blockchain/Dev/connectors/whatsapp-bot/src/index.ts']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/connectors/whatsapp-bot/src/index.ts` (+2/-1 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` (+9/-3 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks812_whatsapp_bot_default_api_target.test.sh=RED(rc 1, 1 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks812_whatsapp_bot_default_api_target.test.sh(8 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` (modified) — B4 [verbatim]: `B4 ks812_whatsapp_bot_default_api_target.test.sh (RED) with the test edits alone: rc=1 fail_lines=1 pass_lines=7 load_error=0 timeout=0` [red FAIL lines: ['FAIL index.ts prints the exported, slash-stripped API base as the API target']] · B5 [verbatim]: `B5 ks812_whatsapp_bot_default_api_target.test.sh after every product section: rc=0 fail_lines=0 pass_lines=8 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (16 suite(s): check_shared_relink_tooling_tokens.test.sh 6p/0f->6p/0f; check_shared_relink.test.sh 0p/0f->0p/0f; check_stack_safety_latest_slot_symlink.test.sh 6p/0f->6p/0f; docker_build_empty_table.test.sh 5p/0f->5p/0f; ks1054_deploy_all_rc1_message.test.sh 4p/0f->4p/0f; ks1054_deploy_scripts_read_startup_migrations.test.sh 40p/0f->40p/0f; ks1054_deploy_sh_rc1_message.test.sh 4p/0f->4p/0f; ks1252_1253_e7_prefix_guard.test.sh 8p/0f->8p/0f; ks1355_dev_reload_slot_container.test.sh 7p/0f->7p/0f; ks949_main_seed_idempotence.test.sh 0p/1f->0p/1f; no_tracked_credentials_root.test.sh 16p/0f->16p/0f; preflight_failure_verdict_keeps_ratio.test.sh 8p/0f->8p/0f; preflight_leg4_sweep_not_run.test.sh 5p/0f->5p/0f; preflight_ratio_excludes_leg1_no_install.test.sh 6p/0f->6p/0f; preflight_state_is_initialised.test.sh 5p/0f->5p/0f; start_secuura_slot_names.test.sh 23p/0f->23p/0f;)` [16 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=3 ok=3 bad=0 skipped_newfile=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/connectors/whatsapp-bot/src/index.ts` (+2/-1) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` (MODIFIED, RED, +9/-3); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8a9970511f22661d92f634058fae8c08c656124f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1624_p2/KS-1624.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p2/checker.out`.

```diff
--- a/Blockchain/Dev/connectors/whatsapp-bot/src/index.ts
+++ b/Blockchain/Dev/connectors/whatsapp-bot/src/index.ts
@@ -2,4 +2,5 @@ import express from 'express';
 import { rejectNulBytes } from '@secuura/shared';
 import { verifyWebhook, handleWebhook } from './webhook';
+import { SECUURA_API_URL } from './verify';
 
 const app = express();
@@ -24,4 +25,4 @@ app.listen(PORT, () => {
   console.log(`Secuura WhatsApp Bot listening on port ${PORT}`);
   console.log(`Webhook URL: https://your-domain/webhook`);
-  console.log(`API target: ${process.env.SECUURA_API_URL || 'https://demo-pk.secuura.net'}`);
+  console.log(`API target: ${SECUURA_API_URL}`);
 });
--- a/Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh
@@ -56,8 +56,14 @@ else
   ok "no source file under src names the dead Container Apps host"
 fi
-if grep -qF "API target: \${process.env.SECUURA_API_URL || '$VM_HOST'}" "$SRC/index.ts"; then
-  ok "index.ts prints the VM ingress as the default API target"
+# KS-1624: the banner prints the value verify.ts exports (slash-stripped, default included), not the raw env var.
+if [ "$(grep -c 'API target' "$SRC/index.ts")" = "1" ]; then
+  ok "CONTROL KS-1624 index.ts has exactly one API target banner line"
 else
-  bad "index.ts prints the VM ingress as the default API target" "$(grep -n 'API target' "$SRC/index.ts" | cut -c1-200)"
+  bad "CONTROL KS-1624 index.ts has exactly one API target banner line" "$(grep -n 'API target' "$SRC/index.ts" | cut -c1-200)"
+fi
+if grep -qF 'API target: ${SECUURA_API_URL}' "$SRC/index.ts" && grep -qF "import { SECUURA_API_URL } from './verify';" "$SRC/index.ts"; then
+  ok "index.ts prints the exported, slash-stripped API base as the API target"
+else
+  bad "index.ts prints the exported, slash-stripped API base as the API target" "$(grep -n 'API target\|from ./verify.' "$SRC/index.ts" | cut -c1-200)"
 fi
 if [ "$URL_SET" = "https://example.test/api/verification/verify" ]; then
```
