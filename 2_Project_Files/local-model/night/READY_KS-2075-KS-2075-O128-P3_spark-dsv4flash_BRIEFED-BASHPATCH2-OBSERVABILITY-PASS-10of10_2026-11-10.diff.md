# READY — KS-2075-KS-2075-O128-P3 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-r2/out.md.checker/patch.diff`** (from `ls` at 07:31 2026-11-10; sha256[:16] 5985955cf7124904, 3538 B; NOTE — `cat section_*.diff | cmp patch.diff` rc 1: the SECTION FILES are the applied units: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-r2/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-control/out.md.checker/patch.diff` rc 0, Spark operator o128); APPLIED PRODUCT(S): the two checkers' own `after_observability.sh` IDENTICAL (`cmp` rc 0).

**Held 07:31 2026-11-10 by Spark operator o128 after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-r2/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at d0b4825cc24493213f82b609670a4a0fa521a4b9, observability/scripts/observability.sh and Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['observability/scripts/observability.sh', 'Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { observability/scripts/observability.sh } + { Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of observability.sh are '-' lines, no stays-site removed; all 1 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 1 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 0/0 of `observability/scripts/observability.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK observability/scripts/observability.sh 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh 65 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2075_o128_p3_observability_down_survives_an_absent_redis_container/KS-2075.md`]: `File:` lines == product_files ['observability/scripts/observability.sh']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `observability/scripts/observability.sh` (+1/-1 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh` (+65/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — observability_down_survives_an_absent_redis_container.test.sh=RED(rc 1, 1 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): observability_down_survives_an_absent_redis_container.test.sh(2 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh` (new) — B4 [verbatim]: `B4 observability_down_survives_an_absent_redis_container.test.sh (RED) with the test edits alone: rc=1 fail_lines=1 pass_lines=1 load_error=0 timeout=0` [red FAIL lines: ['FAIL an absent redis container: down exits 0 and runs compose down once']] · B5 [verbatim]: `B5 observability_down_survives_an_absent_redis_container.test.sh after every product section: rc=0 fail_lines=0 pass_lines=2 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (3 suite(s): check_container_isolation.test.sh 0p/0f->0p/0f; ks1355_slot_blind_launchers.test.sh 78p/0f->78p/0f; prometheus_targets.test.sh 6p/0f->6p/0f;)` [3 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `observability/scripts/observability.sh` (+1/-1) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh` (NEW, RED, +65/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-r2/input.json`. Brief (given by --title-from-brief): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2075_o128_p3_observability_down_survives_an_absent_redis_container/KS-2075.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_2075_o128_p3_observability_down_survives_an_absent_redis_container-r2/checker.out`.

```diff
diff --git a/observability/scripts/observability.sh b/observability/scripts/observability.sh
--- a/observability/scripts/observability.sh
+++ b/observability/scripts/observability.sh
@@ -148,7 +148,7 @@
         sys.stdout.write(cmd[i + 1])' 2>/dev/null
 }
 
-_redis_pw="$(resolve_redis_password)"
+_redis_pw="$(resolve_redis_password || true)"
 if [[ -n "$_redis_pw" ]]; then
     export SECUURA_REDIS_PASSWORD="$_redis_pw"
 fi
diff --git a/Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh b/Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh
@@ -0,0 +1,65 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for observability/scripts/observability.sh - KS-2075: `down` must still stop the stack
+# when the platform's redis container is absent.
+# =============================================================================
+# docker is a stub on a private PATH: it records every call, answers `inspect` with a failure
+# when STUB_INSPECT_RC is non-zero (the container is absent), and answers everything else with 0.
+# No Docker, no network. The cells read the exit code and the recorded calls.
+# Usage: bash Blockchain/Dev/scripts/__tests__/observability_down_survives_an_absent_redis_container.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${OBSERVABILITY_SH:-$HERE/../../../../observability/scripts/observability.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: observability.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks2075.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+
+check() {
+    local desc="$1" want="$2" got="$3"
+    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\n' "$desc"
+    else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
+}
+
+mkdir -p "$WORK/bin"
+cat > "$WORK/bin/docker" <<'STUB'
+#!/bin/sh
+echo "docker $*" >> "$STUB_LOG"
+if [ "$1" = inspect ]; then
+    if [ "${STUB_INSPECT_RC:-0}" != 0 ]; then exit "$STUB_INSPECT_RC"; fi
+    echo '["redis-server"]'
+    exit 0
+fi
+if [ "$1" = exec ]; then exit 1; fi
+exit 0
+STUB
+chmod +x "$WORK/bin/docker"
+
+# run_down <inspect rc>: runs `observability.sh down` with the stub docker; prints "<exit code> <number of compose-down calls>"
+run_down() {
+    : > "$WORK/calls.log"
+    local rc
+    (
+        export PATH="$WORK/bin:/usr/bin:/bin" STUB_LOG="$WORK/calls.log" STUB_INSPECT_RC="$1"
+        unset SECUURA_REDIS_PASSWORD
+        bash "$SUBJ" down
+    ) >"$WORK/out.txt" 2>&1
+    rc=$?
+    printf '%s %s' "$rc" "$(grep -c 'docker compose .* down' "$WORK/calls.log")"
+}
+
+# CELL 1 (CONTROL, tip AND after): with the redis container present, down exits 0 and runs compose down once.
+check "CONTROL a present redis container: down exits 0 and runs compose down once" \
+    "0 1" "$(run_down 0)"
+
+# CELL 2 (RED at the tip): with the redis container absent, down exits 0 and runs compose down once.
+check "an absent redis container: down exits 0 and runs compose down once" \
+    "0 1" "$(run_down 1)"
+
+echo ""
+echo "observability_down_survives_an_absent_redis_container: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
```
