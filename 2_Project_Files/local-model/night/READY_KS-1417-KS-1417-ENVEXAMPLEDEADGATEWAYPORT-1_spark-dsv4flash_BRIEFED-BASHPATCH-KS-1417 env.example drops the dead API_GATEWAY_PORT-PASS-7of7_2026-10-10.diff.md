# READY — KS-1417-KS-1417-ENVEXAMPLEDEADGATEWAYPORT-1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/out.md.checker/patch.diff`** (from `ls` at 08:51 2026-10-10; sha256[:16] 5b38adb362b9a63c, 4823 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-control/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 08:51 2026-10-10 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7834fd8059da31025aba15a47c4b4d61447016ed`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 7834fd8059da31025aba15a47c4b4d61447016ed, Blockchain/Dev/env.example and Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/env.example', 'Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/env.example , Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/env.example` (script) and `Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 2 brief `+` line(s) present; script `+` lines 2 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/env.example` (+2/-1 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh` (+78/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh fails at the untouched tip (rc=1, 2 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=2 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 2 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL: env.example still sets API_GATEWAY_PORT (nothing reads it)', "FAIL: the generated slot-2 .env carries API_GATEWAY_PORT (a slot-1 literal in slot 2's .env)"]]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 4 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=4 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 4 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive env.example: no NEW failure after (3 suite(s))` [3 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/env.example` (+2/-1 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh` (+78/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7834fd8059da31025aba15a47c4b4d61447016ed` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-10_KS-1417-p1-env-example-dead-gateway-port-r2/checker.out`.

```diff
--- a/Blockchain/Dev/env.example
+++ b/Blockchain/Dev/env.example
@@ -358,7 +358,8 @@
 # -----------------------------------------------------------------------------
 # API GATEWAY
 # -----------------------------------------------------------------------------
-API_GATEWAY_PORT=6882
+# The gateway's host port is GATEWAY_PORT, which scripts/stack_env.sh derives per slot.
+# Nothing is set here on purpose: a port written in this file would be a slot-1 literal.
 
 # External port for Postgres (set to empty to disable in production)
 POSTGRES_EXTERNAL_PORT=6432
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh
@@ -0,0 +1,78 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TEST: env.example carries no API_GATEWAY_PORT, a key nothing reads (KS-1417)
+# =============================================================================
+# The gateway's host port comes from GATEWAY_PORT, which stack_env.sh derives per
+# slot. env.example also set API_GATEWAY_PORT=6882, read by nothing, and
+# bootstrap-env.sh copied that slot-1 literal into every clone's .env.
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1417_env_example_no_dead_gateway_port.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+DEV_DIR="$(cd "$HERE/../.." && pwd)"
+BOOTSTRAP="$HERE/../bootstrap-env.sh"
+ENV_SH="$HERE/../stack_env.sh"
+CANONICAL="${ENV_EXAMPLE_SH:-$DEV_DIR/env.example}"
+LEGACY="$DEV_DIR/.env.example"
+[[ -f "$BOOTSTRAP" ]] || { echo "FATAL: bootstrap-env.sh not found at $BOOTSTRAP" >&2; exit 2; }
+[[ -f "$ENV_SH" ]]    || { echo "FATAL: stack_env.sh not found at $ENV_SH" >&2; exit 2; }
+[[ -f "$CANONICAL" ]] || { echo "FATAL: env.example not found at $CANONICAL" >&2; exit 2; }
+[[ -f "$LEGACY" ]]    || { echo "FATAL: .env.example not found at $LEGACY" >&2; exit 2; }
+command -v openssl >/dev/null 2>&1 || { echo "FATAL: openssl required (bootstrap-env.sh needs it)" >&2; exit 2; }
+PASS=0
+FAIL=0
+
+SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/ks1417.XXXXXX")"
+trap 'rm -rf "$SCRATCH"' EXIT
+
+# The key is detected the same way in every cell: an assignment at the start of a line.
+has_dead_key() { grep -qE '^[[:space:]]*API_GATEWAY_PORT=' "$1"; }
+
+# Bootstrap a scratch tree for slot 2 from the real script and the real env.example.
+TREE="$SCRATCH/tree/Blockchain/Dev"
+mkdir -p "$TREE/scripts"
+cp "$BOOTSTRAP" "$TREE/scripts/bootstrap-env.sh"
+cp "$ENV_SH" "$TREE/scripts/stack_env.sh"
+cp "$CANONICAL" "$TREE/env.example"
+cp "$LEGACY" "$TREE/.env.example"
+env -u SECUURA_STACK_SLOT -u STACK_SLOT -u POSTGRES_EXTERNAL_PORT -u REDIS_EXTERNAL_PORT \
+  HOME="$HOME" PATH="$PATH" SECUURA_STACK_SLOT=2 bash "$TREE/scripts/bootstrap-env.sh" >"$TREE/bootstrap.log" 2>&1
+BOOT_RC=$?
+
+# CELL 1 (RED at the tip) - the canonical template no longer sets the dead key.
+if ! has_dead_key "$CANONICAL"; then
+  echo "PASS: env.example does not set API_GATEWAY_PORT"; PASS=$((PASS+1))
+else
+  echo "FAIL: env.example still sets API_GATEWAY_PORT (nothing reads it)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 2 (RED at the tip) - the slot-2 .env that bootstrap generates does not carry it either.
+if [[ -f "$TREE/.env" ]] && ! has_dead_key "$TREE/.env"; then
+  echo "PASS: the generated slot-2 .env does not carry API_GATEWAY_PORT"; PASS=$((PASS+1))
+else
+  echo "FAIL: the generated slot-2 .env carries API_GATEWAY_PORT (a slot-1 literal in slot 2's .env)"; FAIL=$((FAIL+1))
+fi
+
+# CELL 3 (GREEN CONTROL, tip AND after) - the detector can fire: a planted line is found.
+printf 'FOO=1\nAPI_GATEWAY_PORT=6882\n' > "$SCRATCH/planted.env"
+printf 'FOO=1\n# API_GATEWAY_PORT is not a key here\n' > "$SCRATCH/clean.env"
+if has_dead_key "$SCRATCH/planted.env" && ! has_dead_key "$SCRATCH/clean.env"; then
+  echo "PASS: CONTROL the detector finds a planted API_GATEWAY_PORT line and ignores a comment"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL the detector does not discriminate a planted line from a comment"; FAIL=$((FAIL+1))
+fi
+
+# CELL 4 (GREEN CONTROL, tip AND after) - bootstrap still works and the neighbouring keys survive.
+if [[ "$BOOT_RC" -eq 0 && -f "$TREE/.env" ]] \
+   && grep -qE '^POSTGRES_EXTERNAL_PORT=' "$TREE/.env" \
+   && grep -qF '# API GATEWAY' "$CANONICAL" \
+   && grep -qE '^POSTGRES_EXTERNAL_PORT=' "$CANONICAL"; then
+  echo "PASS: CONTROL bootstrap exits 0 and POSTGRES_EXTERNAL_PORT and the API GATEWAY heading survive"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL bootstrap rc=$BOOT_RC, .env present=$([[ -f "$TREE/.env" ]] && echo yes || echo NO)"; FAIL=$((FAIL+1))
+fi
+
+echo "ks1417_env_example_no_dead_gateway_port: $PASS passed, $FAIL failed"
+[[ $FAIL -eq 0 ]]
```
