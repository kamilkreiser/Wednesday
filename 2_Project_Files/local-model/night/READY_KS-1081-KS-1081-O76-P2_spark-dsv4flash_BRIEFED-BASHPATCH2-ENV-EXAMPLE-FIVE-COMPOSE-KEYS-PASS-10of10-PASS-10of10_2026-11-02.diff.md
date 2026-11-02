# READY — KS-1081-KS-1081-O76-P2 (spark-dsv4flash, briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2/out.md.checker/patch.diff`** (from `ls` at 14:48 2026-11-02; sha256[:16] 88cc1c86011c07b0, 3917 B; NOTE — `cat section_*.diff | cmp patch.diff` rc 1: the SECTION FILES are the applied units: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2-control/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT(S): the two checkers' own `after_env.example` IDENTICAL (`cmp` rc 0).

**Held 14:48 2026-11-02 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `86e12156d4e0435587d179084ca525693f716bd8`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 86e12156d4e0435587d179084ca525693f716bd8, Blockchain/Dev/env.example and Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/env.example', 'Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/env.example } + { Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of env.example are '-' lines, no stays-site removed; all 11 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 11 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 0/0 of `Blockchain/Dev/env.example` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/env.example 12 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh 55 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1081_o76_p2_env_example_five_compose_keys_r2/KS-1081.md`]: `File:` lines == product_files ['Blockchain/Dev/env.example']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/env.example` (+12/-0 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh` (+55/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks1081_env_example_declares_compose_keys.test.sh=RED(rc 1, 5 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks1081_env_example_declares_compose_keys.test.sh(7 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh` (new) — B4 [verbatim]: `B4 ks1081_env_example_declares_compose_keys.test.sh (RED) with the test edits alone: rc=1 fail_lines=5 pass_lines=2 load_error=0 timeout=0` [red FAIL lines: ['FAIL env.example declares ADMIN_USER_PASSWORD empty', 'FAIL env.example declares ENABLE_DEMO_SEED empty', 'FAIL env.example declares ALLOW_DEFAULT_SEED_PASSWORDS empty', 'FAIL env.example declares TSA_URL empty', 'FAIL env.example declares TSA_AUTH_KEY empty']] · B5 [verbatim]: `B5 ks1081_env_example_declares_compose_keys.test.sh after every product section: rc=0 fail_lines=0 pass_lines=7 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (88 suite(s): aggregate_report_trivy_artefact.test.sh 5p/0f->5p/0f; blockchain_testing_target_base_follows_the_slot.test.sh 161p/0f->161p/0f; bootstrap_env_canonical_template.test.sh 7p/0f->7p/0f; bootstrap_env_gateway_vouch.test.sh 7p/0f->7p/0f; bootstrap_env_slot_ports.test.sh 51p/0f->51p/0f; check_akto_container_names_flags.test.sh 6p/0f->6p/0f; check_akto_container_names.test.sh 17p/0f->17p/0f; check_connector_xss_skips_node_modules.test.sh 4p/0f->4p/0f; check_container_isolation.test.sh 0p/0f->0p/0f; check_dockerfile_non_root_reports_root.test.sh 11p/0f->11p/0f; check_no_demo_mutation_base.test.sh 5p/0f->5p/0f; check_no_demo_mutation_missing_base.test.sh 5p/0f->5p/0f; check_no_latest_tags.test.sh 9p/0f->9p/0f; check_no_pii_store_untracked_leg.test.sh 5p/0f->5p/0f; check_no_sql_injection_allow_list.test.sh 15p/0f->15p/0f; check_no_sql_injection_multiline.test.sh 22p/0f->22p/0f; check_no_sql_injection_path_filter_and_scan_errors.test.sh 25p/0f->25p/0f; check_no_sql_injection_reports_the_hit.test.sh 4p/0f->4p/0f; check_no_sql_injection_skips_node_modules.test.sh 5p/0f->5p/0f; check_no_strictness_patches_skips_node_modules.test.sh 4p/0f->4p/0f; check_script_portability.test.sh 0p/0f->0p/0f; check_shared_relink_case.test.sh 0p/0f->0p/0f; check_shared_relink_tooling_tokens.test.sh 6p/0f->6p/0f; check_shared_relink.test.sh 0p/0f->0p/0f; check_slot_credentials.test.sh 32p/0f->32p/0f; check_stack_safety_hook_env.test.sh 5p/0f->5p/0f; check_stack_safety_latest_slot_symlink.test.sh 6p/0f->6p/0f; container_trivy_exit_code_env_keeps_findings.test.sh 7p/0f->7p/0f; container_trivy_failed_scan_is_loud.test.sh 6p/0f->6p/0f; container_trivy_image_filter.test.sh 6p/0f->6p/0f; docker_build_empty_table.test.sh 5p/0f->5p/0f; docs_fragments.test.sh 81p/0f->81p/0f; ks1054_deploy_all_rc1_message.test.sh 4p/0f->4p/0f; ks1054_deploy_scripts_read_startup_migrations.test.sh 40p/0f->40p/0f; ks1054_deploy_sh_rc1_message.test.sh 4p/0f->4p/0f; ks1136_aggregate_report_unreadable_artefacts.test.sh 6p/0f->6p/0f; ks1252_1253_e7_prefix_guard.test.sh 8p/0f->8p/0f; ks1317_shared_test_runner_guard.test.sh 8p/0f->8p/0f; ks1347_proxy_out_dir_spaced_checkout.test.sh 20p/0f->20p/0f; ks1355_dev_reload_slot_container.test.sh 7p/0f->7p/0f; ks1355_slot_blind_launchers.test.sh 36p/0f->36p/0f; ks1405_run_schemathesis_default_findings_dir.test.sh 5p/0f->5p/0f; ks1417_env_example_no_dead_gateway_port.test.sh 10p/0f->10p/0f; ks1426_lockfile_cleanroom_names_its_surface.test.sh 14p/0f->14p/0f; ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh 4p/0f->4p/0f; ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh 7p/0f->7p/0f; ks1513_ratchet_leg_suite_skips_real_checker_cells_without_install.test.sh 5p/0f->5p/0f; ks1527_ratchet_leg_stub_cells_catch_a_mutated_leg.test.sh 4p/0f->4p/0f; ks1547_preflight_step_header_denominator.test.sh 12p/0f->12p/0f; ks1560_private_path_suites_link_jq.test.sh 3p/0f->3p/0f; ks808_run_migrations_counts_skips_apart.test.sh 5p/0f->5p/0f; ks812_whatsapp_bot_default_api_target.test.sh 11p/0f->11p/0f; ks884_pre_push_tag_named_develop.test.sh 10p/0f->10p/0f; ks949_main_seed_idempotence.test.sh 0p/0f->0p/0f; ks998_pre_push_judges_the_push.test.sh 80p/0f->80p/0f; ks998_pre_push_stale_base_hint.test.sh 21p/0f->21p/0f; no_tracked_credentials_root.test.sh 16p/0f->16p/0f; orchestrate_jobs.test.sh 18p/0f->18p/0f; pre_push_hook_base_fixture_guard.test.sh 12p/0f->12p/0f; pre_push_hook_base_leg_comment.test.sh 4p/0f->4p/0f; pre_push_hook_base.test.sh 36p/0f->36p/0f; pre_push_hook_current_develop.test.sh 4p/0f->4p/0f; pre_push_stack_legs_comment.test.sh 4p/0f->4p/0f; preflight_deps.test.sh 82p/0f->82p/0f; preflight_failure_verdict_keeps_ratio.test.sh 8p/0f->8p/0f; preflight_gateway_slot.test.sh 15p/0f->15p/0f; preflight_leg4_sweep_not_run.test.sh 5p/0f->5p/0f; preflight_ratio_excludes_leg1_no_install.test.sh 6p/0f->6p/0f; preflight_state_is_initialised.test.sh 5p/0f->5p/0f; preflight_test_types_ratchet_leg.test.sh 27p/0f->27p/0f; preflight_verdict_names_real_failures.test.sh 5p/0f->5p/0f; prometheus_targets.test.sh 6p/0f->6p/0f; run_code_guards.test.sh 17p/0f->17p/0f; run_migrations_failure_exit_code.test.sh 7p/0f->7p/0f; run_shell_suites.test.sh 79p/0f->79p/0f; slot_is_local_host_only.test.sh 4p/0f->4p/0f; smoke_test_counters_survive_errexit.test.sh 6p/0f->6p/0f; smoke_test_degraded_warns.test.sh 5p/0f->5p/0f; smoke_test_honours_smoke_base_url.test.sh 5p/0f->5p/0f; stack_env.test.sh 25p/0f->25p/0f; stack_guard.test.sh 27p/0f->27p/0f; start_secuura_banner.test.sh 4p/0f->4p/0f; start_secuura_expected_services.test.sh 5p/0f->5p/0f; start_secuura_marker_unknown_warning.test.sh 5p/0f->5p/0f; start_secuura_slot_names.test.sh 23p/0f->23p/0f; stop_secuura.test.sh 11p/0f->11p/0f; tenant_isolation_stderr_own_file.test.sh 5p/0f->5p/0f; validate_lint_errexit.test.sh 4p/0f->4p/0f;)` [88 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/env.example` (+12/-0) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh` (NEW, RED, +55/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `86e12156d4e0435587d179084ca525693f716bd8` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2/input.json`. Brief (given by --brief): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1081_o76_p2_env_example_five_compose_keys_r2/KS-1081.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1081_o76_p2_env_example_five_compose_keys_r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/env.example b/Blockchain/Dev/env.example
--- a/Blockchain/Dev/env.example
+++ b/Blockchain/Dev/env.example
@@ -510,2 +510,14 @@
 #     openssl rand -hex 32
 EMITTER_SIGNING_SECRET=
+
+# KS-1081: five keys that docker-compose.yml reads but this template did not declare. Each is
+# declared here at compose's own default (empty), so a .env bootstrapped from this file behaves
+# exactly as before. Set real values in your own .env, never here.
+# Bootstrap SYSTEM_ADMIN password (KS-966): empty means the account is not seeded.
+ADMIN_USER_PASSWORD=
+# Demo-seed gate, with the flag below it: read by the seeder in originate.
+ENABLE_DEMO_SEED=
+ALLOW_DEFAULT_SEED_PASSWORDS=
+# RFC-3161 timestamp authority; an EMPTY TSA_URL means the code default.
+TSA_URL=
+TSA_AUTH_KEY=
diff --git a/Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh b/Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh
@@ -0,0 +1,55 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/env.example - KS-1081: the canonical env template must declare the
+# five keys that docker-compose.yml reads with an empty default, so a .env bootstrapped from it
+# carries them forward.
+# =============================================================================
+# Reads the two files with grep only; nothing is started, no network, no docker.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1081_env_example_declares_compose_keys.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+DEV_DIR="$(cd "$HERE/../.." && pwd)"
+TEMPLATE="$DEV_DIR/env.example"
+COMPOSE="$DEV_DIR/docker-compose.yml"
+PASS=0; FAIL=0
+
+check() {
+    local desc="$1" want="$2" got="$3"
+    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\n' "$desc"
+    else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
+}
+
+# declared_empty <key>: prints 1 when env.example has a line that is exactly KEY= (an empty value), else 0
+declared_empty() {
+    if grep -qxF "$1=" "$TEMPLATE"; then echo 1; else echo 0; fi
+}
+
+# compose_default_empty <key>: prints 1 when docker-compose.yml interpolates ${KEY:-} (empty default), else 0
+compose_default_empty() {
+    if grep -qF "\${$1:-}" "$COMPOSE"; then echo 1; else echo 0; fi
+}
+
+# --- CELL 0 (CONTROL, tip AND after): a key the template already declares is seen by the matcher ---
+check "CONTROL the matcher sees GATEWAY_VOUCH_SECRET declared empty in env.example" "1" "$(declared_empty GATEWAY_VOUCH_SECRET)"
+
+# --- CELL 1 (CONTROL, tip AND after): compose reads the five keys with an empty default ---
+BOTH=""
+for k in ADMIN_USER_PASSWORD ENABLE_DEMO_SEED ALLOW_DEFAULT_SEED_PASSWORDS TSA_URL TSA_AUTH_KEY; do
+    [[ "$(compose_default_empty "$k")" == "1" ]] || BOTH="${BOTH}${k} "
+done
+check "CONTROL docker-compose.yml reads all five keys with an empty default" "" "${BOTH% }"
+
+# --- CELLS 2-6 (RED at the tip): each key is declared empty in env.example ---
+check "env.example declares ADMIN_USER_PASSWORD empty" "1" "$(declared_empty ADMIN_USER_PASSWORD)"
+check "env.example declares ENABLE_DEMO_SEED empty" "1" "$(declared_empty ENABLE_DEMO_SEED)"
+check "env.example declares ALLOW_DEFAULT_SEED_PASSWORDS empty" "1" "$(declared_empty ALLOW_DEFAULT_SEED_PASSWORDS)"
+check "env.example declares TSA_URL empty" "1" "$(declared_empty TSA_URL)"
+check "env.example declares TSA_AUTH_KEY empty" "1" "$(declared_empty TSA_AUTH_KEY)"
+
+echo ""
+echo "ks1081_env_example_declares_compose_keys: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
```
