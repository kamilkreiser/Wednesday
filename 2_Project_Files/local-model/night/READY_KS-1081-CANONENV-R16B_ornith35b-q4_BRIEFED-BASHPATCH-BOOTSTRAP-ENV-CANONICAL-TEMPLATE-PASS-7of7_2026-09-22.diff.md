# READY — KS-1081-CANONENV-R16B (Ornith, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 11:14 2026-09-22; sha256[:16] 4087c62855fbb2d2, 7034 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed9-drafter-precheck/CANONENV/out.md.checker/patch.diff` rc 0, Wednesday); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 11:14 2026-09-22 by Wednesday after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (input `bash_patch_1081CANONENV-R16B.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 8c2f7b3fd4fde915b2a24542bc32259b24e092a0, Blockchain/Dev/scripts/bootstrap-env.sh and Blockchain/Dev/scripts/__tests__/bootstrap_env_slot_ports.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/bootstrap-env.sh', 'Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/bootstrap-env.sh , Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/bootstrap-env.sh` (script) and `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/bootstrap_env_slot_ports.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 16 brief `+` line(s) present; script `+` lines 16 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 3; must_change sites 3/3 each a `-` line; must_remove 3 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/bootstrap-env.sh` (+16/-3 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` (+90/-0 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh fails at the untouched tip (rc=1, 4 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=4 pass_lines=2 load_error=0 timeout=0` [red_first.out re-count: 4 FAIL line(s), 2 pass line(s); FAIL lines: ['FAIL: the generated .env is missing 64 variables that env.example declares (first 6: API_GATEWAY_PORT AUTH0_CLIENT_ID AUTH0_CLIENT_SECRET AUTH0_DOMAIN AZURE_AD_CLIENT_ID AZURE_AD_CLIENT_SECRET)', 'FAIL: API_GATEWAY_PORT is declared in env.example and absent from the generated .env - .env.example was copied', "FAIL: the bootstrap log does not say 'Created .env from env.example'", 'FAIL: /private/tmp/claude-501/night/clone_ks1081/Blockchain/Dev/scripts/__tests__/../bootstrap-env.sh never names the canonical env.example path under DEV_DIR']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 6 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=6 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 6 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive bootstrap-env.sh: no NEW failure after (2 suite(s))` [2 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/bootstrap-env.sh` (+16/-3 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` (+90/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night/input.json`. Brief (located by ticket + ROWID tokens ['CANONENV', 'R16B'] under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1081-R16B-CANONENV.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/bootstrap-env.sh
+++ b/Blockchain/Dev/scripts/bootstrap-env.sh
@@ -23,6 +23,19 @@ set -e
 SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
 DEV_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
 ENV_FILE="$DEV_DIR/.env"
-ENV_EXAMPLE="$DEV_DIR/.env.example"
+# KS-1081 (Kam 2026-09-16, option a): `env.example` is canonical - it is the larger
+# template (102 distinct vars at 48e65c435 against `.env.example`'s 65) and the one
+# the docs document (`README.md:25`, `CONTRIBUTING.md:26`, `docs/DEPLOYMENT.md:130`
+# all say `cp env.example .env`). This script read `.env.example`, so a developer
+# who followed the docs and a developer who ran this script got environments that
+# differed by dozens of variables. Canonical first. The legacy name survives ONLY
+# as a named fallback for a tree that carries no `env.example` - the scratch clones
+# built by `scripts/__tests__/bootstrap_env_slot_ports.test.sh` and
+# `scripts/verify-slot-credential-isolation.sh` are exactly that shape - so this
+# change cannot break them while the two templates are reconciled.
+ENV_EXAMPLE_CANONICAL="$DEV_DIR/env.example"
+ENV_EXAMPLE_LEGACY="$DEV_DIR/.env.example"
+ENV_EXAMPLE="$ENV_EXAMPLE_CANONICAL"
+[[ -f "$ENV_EXAMPLE" ]] || ENV_EXAMPLE="$ENV_EXAMPLE_LEGACY"
 ENV_LOCAL_FILE="$DEV_DIR/.env.local"
 ENV_LOCAL_EXAMPLE="$DEV_DIR/.env.local.example"
@@ -55,6 +68,6 @@ if ! command -v openssl >/dev/null 2>&1; then
 if [[ ! -f "$ENV_EXAMPLE" ]]; then
-  print_error ".env.example not found at: $ENV_EXAMPLE"
+  print_error "No env template found: neither $ENV_EXAMPLE_CANONICAL (canonical, KS-1081) nor $ENV_EXAMPLE_LEGACY"
   exit 1
 fi
 
 # -----------------------------------------------------------------------------
@@ -64,7 +77,7 @@ else
   print_info ".env already exists — leaving it untouched"
 else
   cp "$ENV_EXAMPLE" "$ENV_FILE"
-  print_success "Created .env from .env.example"
+  print_success "Created .env from $(basename "$ENV_EXAMPLE") (KS-1081: env.example is canonical)"
 fi
 
 # -----------------------------------------------------------------------------
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh
@@ -0,0 +1,90 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TEST: bootstrap-env.sh copies the CANONICAL template env.example (KS-1081)
+# =============================================================================
+# Usage: bash Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+DEV_DIR="$(cd "$HERE/../.." && pwd)"
+BOOTSTRAP="${BOOTSTRAP_SH:-$HERE/../bootstrap-env.sh}"
+ENV_SH="$HERE/../stack_env.sh"
+CANONICAL="$DEV_DIR/env.example"
+LEGACY="$DEV_DIR/.env.example"
+[[ -f "$BOOTSTRAP" ]] || { echo "FATAL: bootstrap-env.sh not found at $BOOTSTRAP" >&2; exit 2; }
+[[ -f "$ENV_SH" ]]    || { echo "FATAL: stack_env.sh not found at $ENV_SH" >&2; exit 2; }
+[[ -f "$CANONICAL" ]] || { echo "FATAL: canonical template not found at $CANONICAL" >&2; exit 2; }
+[[ -f "$LEGACY" ]]    || { echo "FATAL: legacy template not found at $LEGACY" >&2; exit 2; }
+command -v openssl >/dev/null 2>&1 || { echo "FATAL: openssl required (bootstrap-env.sh needs it)" >&2; exit 2; }
+PASS=0
+FAIL=0
+
+var_names() { grep -E '^[A-Z][A-Z0-9_]*=' "$1" | cut -d= -f1 | sort -u; }
+GENERATED='^(POSTGRES_PASSWORD|DATABASE_URL|REDIS_PASSWORD|REDIS_URL|PII_ENCRYPTION_KEY|PII_ENCRYPTION_KEY_VERSION|PII_LOOKUP_HMAC_KEY|DEMO_SERVICE_ENABLED|DEMO_SERVICE_KEY|JWT_PRIVATE_KEY|JWT_PUBLIC_KEY|JWT_KEY_ID)$'
+CANON_ONLY="$(comm -23 <(var_names "$CANONICAL") <(var_names "$LEGACY") | grep -vE "$GENERATED" | head -n1)"
+[[ -n "$CANON_ONLY" ]] || { echo "FATAL: the two templates no longer differ outside the script-generated keys - premise of this suite changed" >&2; exit 2; }
+
+SCRATCH_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/ks1081.XXXXXX")"
+trap 'rm -rf "$SCRATCH_ROOT"' EXIT
+BOTH="$SCRATCH_ROOT/both/Blockchain/Dev"
+mkdir -p "$BOTH/scripts"
+cp "$BOOTSTRAP" "$BOTH/scripts/bootstrap-env.sh"
+cp "$ENV_SH" "$BOTH/scripts/stack_env.sh"
+cp "$CANONICAL" "$BOTH/env.example"
+cp "$LEGACY" "$BOTH/.env.example"
+env -u SECUURA_STACK_SLOT -u STACK_SLOT -u POSTGRES_EXTERNAL_PORT -u REDIS_EXTERNAL_PORT HOME="$HOME" PATH="$PATH" bash "$BOTH/scripts/bootstrap-env.sh" >"$BOTH/bootstrap.log" 2>&1
+BOTH_RC=$?
+
+ONLY_LEGACY="$SCRATCH_ROOT/legacyonly/Blockchain/Dev"
+mkdir -p "$ONLY_LEGACY/scripts"
+cp "$BOOTSTRAP" "$ONLY_LEGACY/scripts/bootstrap-env.sh"
+cp "$ENV_SH" "$ONLY_LEGACY/scripts/stack_env.sh"
+cp "$LEGACY" "$ONLY_LEGACY/.env.example"
+env -u SECUURA_STACK_SLOT -u STACK_SLOT -u POSTGRES_EXTERNAL_PORT -u REDIS_EXTERNAL_PORT HOME="$HOME" PATH="$PATH" bash "$ONLY_LEGACY/scripts/bootstrap-env.sh" >"$ONLY_LEGACY/bootstrap.log" 2>&1
+LEGACY_RC=$?
+
+MISSING_N="$(comm -23 <(var_names "$CANONICAL") <(var_names "$BOTH/.env") | grep -c .)"
+MISSING="$(comm -23 <(var_names "$CANONICAL") <(var_names "$BOTH/.env") | head -n 6 | xargs)"
+DB_PORT="$(grep -E '^DATABASE_URL=' "$BOTH/.env" | head -n1 | sed -E 's#^.*@localhost:##; s#/.*$##')"
+
+if [[ "$MISSING_N" -eq 0 ]]; then
+  echo "PASS: every variable in env.example reached the generated .env"; PASS=$((PASS+1))
+else
+  echo "FAIL: the generated .env is missing $MISSING_N variables that env.example declares (first 6: $MISSING)"; FAIL=$((FAIL+1))
+fi
+
+if grep -qE "^${CANON_ONLY}=" "$BOTH/.env"; then
+  echo "PASS: the canonical-only variable $CANON_ONLY is in the generated .env"; PASS=$((PASS+1))
+else
+  echo "FAIL: $CANON_ONLY is declared in env.example and absent from the generated .env - .env.example was copied"; FAIL=$((FAIL+1))
+fi
+
+if grep -qF 'Created .env from env.example' "$BOTH/bootstrap.log"; then
+  echo "PASS: the script reports the canonical template by name"; PASS=$((PASS+1))
+else
+  echo "FAIL: the bootstrap log does not say 'Created .env from env.example'"; FAIL=$((FAIL+1))
+fi
+
+if grep -qF '$DEV_DIR/env.example' "$BOOTSTRAP"; then
+  echo "PASS: the script resolves the canonical template path under DEV_DIR"; PASS=$((PASS+1))
+else
+  echo "FAIL: $BOOTSTRAP never names the canonical env.example path under DEV_DIR"; FAIL=$((FAIL+1))
+fi
+
+if [[ "$BOTH_RC" -eq 0 && "$DB_PORT" == "6432" ]]; then
+  echo "PASS: CONTROL bootstrap exits 0 and DATABASE_URL still carries the slot-1 port 6432"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL bootstrap rc=$BOTH_RC, DATABASE_URL port '$DB_PORT' (want rc 0 and 6432)"; FAIL=$((FAIL+1))
+fi
+
+if [[ "$LEGACY_RC" -eq 0 && -f "$ONLY_LEGACY/.env" ]]; then
+  echo "PASS: CONTROL a tree carrying only .env.example still bootstraps (the fallback)"; PASS=$((PASS+1))
+else
+  echo "FAIL: CONTROL a tree carrying only .env.example no longer bootstraps (rc=$LEGACY_RC)"; FAIL=$((FAIL+1))
+fi
+
+echo ""
+echo "bootstrap_env_canonical_template: $PASS passed, $FAIL failed"
+[[ $FAIL -eq 0 ]]
```
