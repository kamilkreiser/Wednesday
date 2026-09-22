# READY — KS-1081 (CONFIG DRIFT: two tracked env templates disagree — KAM RULED option a at 09:53: "env.example (the larger, the one CLAUDE.md documents) is canonical") — Ornith ornith:35b (Q4_K_M) PASS 7/7 **on its FIRST sample**, BASH_PATCH, NEW test file, tip develop M55 48e65c435, run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1081-ornith35b-night
# Source read by me (Wednesday): the applied `after.sh` carries the three replaced lines as briefed — :26 becomes a canonical-first block naming Kam's ruling, with `ENV_EXAMPLE_CANONICAL`/`ENV_EXAMPLE_LEGACY` and a NAMED fallback; :56 the pre-flight error; :67 the "Created .env from" line. B4 red-first genuine, B5 green-after 6/6, B6 two sibling suites with no new failure.
# ⚠ THREE THINGS THE TICKET GOT WRONG, measured at the tip by the brief's author and material to the ruling — **the ticket's two variable lists are INVERTED**. Making env.example canonical therefore DROPS about 30 variables a fresh clone used to get, including `ALLOW_DEFAULT_SEED_PASSWORDS`, `ENABLE_DEMO_SEED`, `ENCRYPTION_SALT`, `ADMIN_USER_*`, the PGBOUNCER trio, `FRONTEND_URL` and `VC_SIGNING_KEY`. **Kam's ruling still stands — he chose the larger, documented template — but the reconciliation of those 30 is a real follow-up and is NOT in this diff.** Second: the ticket says the project CLAUDE.md documents the `cp` line; it does not — the evidence is README.md:25, CONTRIBUTING.md:26, docs/DEPLOYMENT.md:130, docs/DEVELOPER-GUIDE.md:53 and docs/ENVIRONMENT-VARIABLES.md:13-15, and the PR should cite those. Third: the numbers have drifted since 2026-09-10 — .env.example is 327 lines / 65 vars, env.example has 102 DISTINCT vars (`KYC_PROVIDER` is declared twice), and the delta is 37 each way, not ~39.
# PR NOTES for the Sunday raising seat: (1) TWO files: `Blockchain/Dev/scripts/bootstrap-env.sh` (three one-line replacements) + the NEW suite `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh`. (2) **The named legacy fallback is deliberate and must stay until the reconciliation PR lands:** two harnesses (`bootstrap_env_slot_ports.test.sh:91` and `verify-slot-credential-isolation.sh:59`) build a scratch tree holding only `.env.example` and then run this script — a hard repoint with no fallback makes both exit non-zero at the pre-flight. Cell 6 pins that. (3) File the 30-variable reconciliation as its own ticket before `.env.example` is deleted.

```diff
--- a/Blockchain/Dev/scripts/bootstrap-env.sh
+++ b/Blockchain/Dev/scripts/bootstrap-env.sh
@@ -23,7 +23,21 @@ set -e
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
 
@@ -53,7 +67,7 @@ if ! command -v openssl >/dev/null 2>&1; then
 
 if [[ ! -f "$ENV_EXAMPLE" ]]; then
   print_error ".env.example not found at: $ENV_EXAMPLE"
-  exit 1
+  print_error "No env template found: neither $ENV_EXAMPLE_CANONICAL (canonical, KS-1081) nor $ENV_EXAMPLE_LEGACY"
 fi
 
 # -----------------------------------------------------------------------------
@@ -64,7 +78,7 @@ else
   print_info ".env already exists — leaving it untouched"
 else
   cp "$ENV_EXAMPLE" "$ENV_FILE"
-  print_success "Created .env from .env.example"
+  print_success "Created .env from $(basename "$ENV_EXAMPLE") (KS-1081: env.example is canonical)"
 fi
 
 # -----------------------------------------------------------------------------

--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh
@@ -0,0 +1,97 @@
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
