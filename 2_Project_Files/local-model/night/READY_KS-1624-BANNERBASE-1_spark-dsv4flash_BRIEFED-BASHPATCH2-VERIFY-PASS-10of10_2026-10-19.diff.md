# READY — KS-1624-BANNERBASE-1 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p1/out.md.checker/patch.diff`** (from `ls` at 01:35 2026-10-19; sha256[:16] 76cca308b15992ad, 2597 B; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p1-control-r2/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1): change lines (`+`/`-`, ordered) IDENTICAL in every section; APPLIED PRODUCT(S): the two checkers' own `after_verify.ts` IDENTICAL (`cmp` rc 0). Run's own golden_cmp.out [verbatim]: `golden tree 54e1aee3e775d289c322c79c699faf1fa550f309 · patch tree 54e1aee3e775d289c322c79c699faf1fa550f309 -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1624_p1_012730/*_cmp.index.out)`.

**Held 01:35 2026-10-19 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p1/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `8a9970511f22661d92f634058fae8c08c656124f`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8a9970511f22661d92f634058fae8c08c656124f, Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts and Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts', 'Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts } + { Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 1 must_change site(s) of verify.ts are '-' lines, no stays-site removed; all 1 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 1 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 1/1 of `Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh 29 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1624_p1/KS-1624.md`]: `File:` lines == product_files ['Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts` (+1/-1 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` (+29/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks812_whatsapp_bot_default_api_target.test.sh=RED(rc 1, 2 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks812_whatsapp_bot_default_api_target.test.sh(10 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` (modified) — B4 [verbatim]: `B4 ks812_whatsapp_bot_default_api_target.test.sh (RED) with the test edits alone: rc=1 fail_lines=2 pass_lines=8 load_error=0 timeout=0` [red FAIL lines: ['FAIL KS-1624 verify.ts exports the base with its trailing slashes stripped', 'FAIL KS-1624 verify.ts exports the default base when SECUURA_API_URL is unset']] · B5 [verbatim]: `B5 ks812_whatsapp_bot_default_api_target.test.sh after every product section: rc=0 fail_lines=0 pass_lines=10 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (6 suite(s): check_shared_relink.test.sh 0p/0f->0p/0f; ks1054_deploy_scripts_read_startup_migrations.test.sh 40p/0f->40p/0f; ks884_pre_push_tag_named_develop.test.sh 10p/0f->10p/0f; ks998_pre_push_judges_the_push.test.sh 74p/0f->74p/0f; pre_push_hook_base_fixture_guard.test.sh 6p/0f->6p/0f; pre_push_hook_base.test.sh 33p/0f->33p/0f;)` [6 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts` (+1/-1) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh` (MODIFIED, RED, +29/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8a9970511f22661d92f634058fae8c08c656124f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1624_p1/KS-1624.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1624_p1/checker.out`.

```diff
--- a/Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts
+++ b/Blockchain/Dev/connectors/whatsapp-bot/src/verify.ts
@@ -3,5 +3,5 @@ import { VerifyResult } from './messages';
 
 // KS-1490: an override written with a trailing slash (https://host/) must not build https://host//api/verification/verify.
-const SECUURA_API_URL = (process.env.SECUURA_API_URL || 'https://demo-pk.secuura.net').replace(/\/+$/, '');
+export const SECUURA_API_URL = (process.env.SECUURA_API_URL || 'https://demo-pk.secuura.net').replace(/\/+$/, '');
 
 export function hashBuffer(buffer: Buffer): string {
--- a/Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/ks812_whatsapp_bot_default_api_target.test.sh
@@ -79,4 +79,33 @@ else
   bad "KS-1490 a SECUURA_API_URL with a path and two trailing slashes keeps the path and builds a single slash" "requested: $URL_SLASHES"
 fi
+# KS-1624: verify.ts EXPORTS the slash-stripped base it builds the request URL from, so index.ts can print the very value the bot uses.
+exported_base() {
+  VERIFY_TS="$SRC/verify.ts" TMP_DIR="$WORK" ENVVAL="$1" node -e '
+    const fs = require("fs");
+    const m = require("module");
+    const src = fs.readFileSync(process.env.VERIFY_TS, "utf8").replace(/^import .* from .\.\/messages.;\s*$/m, "");
+    const file = process.env.TMP_DIR + "/base-" + Date.now() + ".mjs";
+    fs.writeFileSync(file, m.stripTypeScriptTypes(src));
+    if (process.env.ENVVAL === "UNSET") delete process.env.SECUURA_API_URL; else process.env.SECUURA_API_URL = process.env.ENVVAL;
+    import(file).then((mod) => console.log(String(mod.SECUURA_API_URL)));
+  ' 2>/dev/null
+}
+if [ -n "$(exported_base UNSET)" ]; then
+  ok "CONTROL KS-1624 the instrument imports verify.ts and prints what it exports"
+else
+  bad "CONTROL KS-1624 the instrument imports verify.ts and prints what it exports" "printed nothing"
+fi
+BASE_SLASHES="$(exported_base "https://example.test/base//")"
+if [ "$BASE_SLASHES" = "https://example.test/base" ]; then
+  ok "KS-1624 verify.ts exports the base with its trailing slashes stripped"
+else
+  bad "KS-1624 verify.ts exports the base with its trailing slashes stripped" "exported: $BASE_SLASHES"
+fi
+BASE_UNSET="$(exported_base UNSET)"
+if [ "$BASE_UNSET" = "$VM_HOST" ]; then
+  ok "KS-1624 verify.ts exports the default base when SECUURA_API_URL is unset"
+else
+  bad "KS-1624 verify.ts exports the default base when SECUURA_API_URL is unset" "exported: $BASE_UNSET"
+fi
 printf '\n  %d passed, %d failed\n' "$pass" "$fail"
 [ "$fail" -eq 0 ] || exit 1
```
