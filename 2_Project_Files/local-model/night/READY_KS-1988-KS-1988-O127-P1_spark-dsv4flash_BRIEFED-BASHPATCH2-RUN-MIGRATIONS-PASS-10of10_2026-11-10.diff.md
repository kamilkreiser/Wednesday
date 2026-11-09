# READY — KS-1988-KS-1988-O127-P1 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/out.md.checker/patch.diff`** (from `ls` at 06:39 2026-11-10; sha256[:16] 9c9fcffdd7c2d9b1, 4131 B; NOTE — `cat section_*.diff | cmp patch.diff` rc 1: the SECTION FILES are the applied units: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host-control/out.md.checker/patch.diff` rc 0, Spark operator o127 (Wednesday 06:00 seat)); APPLIED PRODUCT(S): the two checkers' own `after_run-migrations.sh` IDENTICAL (`cmp` rc 0).

**Held 06:39 2026-11-10 by Spark operator o127 (Wednesday 06:00 seat) after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at d0b4825cc24493213f82b609670a4a0fa521a4b9, Blockchain/Dev/scripts/run-migrations.sh and Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/run-migrations.sh', 'Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/scripts/run-migrations.sh } + { Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of run-migrations.sh are '-' lines, no stays-site removed; all 2 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 2 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 0/0 of `Blockchain/Dev/scripts/run-migrations.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/scripts/run-migrations.sh 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh 67 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/KS-1988.md`]: `File:` lines == product_files ['Blockchain/Dev/scripts/run-migrations.sh']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/run-migrations.sh` (+2/-2 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh` (+67/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — run_migrations_readiness_probe_parses_the_url.test.sh=RED(rc 1, 2 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): run_migrations_readiness_probe_parses_the_url.test.sh(3 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh` (new) — B4 [verbatim]: `B4 run_migrations_readiness_probe_parses_the_url.test.sh (RED) with the test edits alone: rc=1 fail_lines=2 pass_lines=1 load_error=0 timeout=0` [red FAIL lines: ['FAIL a URL with no port probes the host on the default port 5432', 'FAIL a URL with no host and no port probes an empty host on the default port 5432']] · B5 [verbatim]: `B5 run_migrations_readiness_probe_parses_the_url.test.sh after every product section: rc=0 fail_lines=0 pass_lines=3 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (5 suite(s): ks1401_058_tenant_isolation_after_039.test.sh 0p/0f->0p/0f; ks1456_run_migrations_failed_run_names_no_closed_defect.test.sh 7p/0f->7p/0f; ks808_run_migrations_counts_skips_apart.test.sh 5p/0f->5p/0f; ks949_main_seed_idempotence.test.sh 0p/1f->0p/1f; run_migrations_failure_exit_code.test.sh 7p/0f->7p/0f;)` [5 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/run-migrations.sh` (+2/-2) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh` (NEW, RED, +67/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/input.json`. Brief (given by --title-from-brief): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/KS-1988.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1988_o127_p1_run_migrations_readiness_probe_parses_a_url_without_a_port_or_host/checker.out`.

```diff
diff --git a/Blockchain/Dev/scripts/run-migrations.sh b/Blockchain/Dev/scripts/run-migrations.sh
--- a/Blockchain/Dev/scripts/run-migrations.sh
+++ b/Blockchain/Dev/scripts/run-migrations.sh
@@ -68,8 +68,8 @@ echo "Waiting for PostgreSQL to be ready..."
 
 # Extract host and port from DATABASE_URL for pg_isready
 # Format: postgresql://user:pass@host:port/db
-PG_HOST=$(echo "$DATABASE_URL" | sed -E 's|.*@([^:/]+).*|\1|')
-PG_PORT=$(echo "$DATABASE_URL" | sed -E 's|.*:([0-9]+)/.*|\1|')
+PG_HOST=$(echo "$DATABASE_URL" | sed -nE 's|.*@([^:/]+).*|\1|p')
+PG_PORT=$(echo "$DATABASE_URL" | sed -nE 's|.*:([0-9]+)/.*|\1|p')
 PG_PORT=${PG_PORT:-5432}
 
 while [ "$RETRIES" -lt "$MAX_RETRIES" ]; do
diff --git a/Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh b/Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh
@@ -0,0 +1,67 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/run-migrations.sh - KS-1988: the readiness probe must hand
+# pg_isready a HOST and a PORT, never the whole DATABASE_URL.
+# =============================================================================
+# pg_isready and psql are stubs on a private PATH: no database is needed, no migration runs.
+# The pg_isready stub records its arguments, one bracketed word each, and always answers ready,
+# so the runner finishes at once and the cells read what the probe was CALLED with.
+# Usage: bash Blockchain/Dev/scripts/__tests__/run_migrations_readiness_probe_parses_the_url.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SUBJ="${RUN_MIGRATIONS_SH:-$HERE/../run-migrations.sh}"
+[[ -r "$SUBJ" ]] || { echo "FATAL: run-migrations.sh not readable at $SUBJ" >&2; exit 2; }
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1988.XXXXXX")"
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
+mkdir -p "$WORK/bin" "$WORK/fx/scripts" "$WORK/fx/migrations"
+cat > "$WORK/bin/pg_isready" <<'STUB'
+#!/bin/sh
+for a in "$@"; do printf '[%s]' "$a"; done > "$PROBE_LOG"
+exit 0
+STUB
+cat > "$WORK/bin/psql" <<'STUB'
+#!/bin/sh
+exit 0
+STUB
+chmod +x "$WORK/bin/pg_isready" "$WORK/bin/psql"
+cp "$SUBJ" "$WORK/fx/scripts/run-migrations.sh"
+echo "SELECT 1;" > "$WORK/fx/migrations/047_ok.sql"
+
+# probe_args <database url>: runs the runner and prints what pg_isready was called with
+probe_args() {
+    rm -f "$WORK/probe.log"
+    (
+        export PATH="$WORK/bin:/usr/bin:/bin" PROBE_LOG="$WORK/probe.log" DATABASE_URL="$1"
+        unset PLATFORM_DATABASE_URL
+        cd "$WORK/fx" && sh scripts/run-migrations.sh
+    ) >"$WORK/out.txt" 2>&1
+    cat "$WORK/probe.log" 2>/dev/null
+}
+
+# CELL 1 (CONTROL, tip AND after): a URL that names user, password, host and port is split correctly.
+check "CONTROL a URL with host and port probes that host and port" \
+    "[-h][db.example][-p][6432][-q]" "$(probe_args 'postgresql://u:pw@db.example:6432/secuura')"
+
+# CELL 2 (RED at the tip): a URL with no port probes the host on the default port 5432.
+check "a URL with no port probes the host on the default port 5432" \
+    "[-h][db.example][-p][5432][-q]" "$(probe_args 'postgresql://u:pw@db.example/secuura')"
+
+# CELL 3 (RED at the tip): a URL with no host (a socket directory in the query) never hands the URL to pg_isready.
+check "a URL with no host and no port probes an empty host on the default port 5432" \
+    "[-h][][-p][5432][-q]" "$(probe_args 'postgresql:///secuura?host=/var/run/postgresql')"
+
+echo ""
+echo "run_migrations_readiness_probe_parses_the_url: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
```
