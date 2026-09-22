# KS-1081 R16B-CANONENV - re-brief at develop 8c2f7b3fd of READY_KS-1081_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 10:26:40 AEST by Wednesday's feed9 drafter under the FEED 8 ruling; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip (KS-1081: one hunk corrected to the old brief's intent - see the drafter's note), every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
`Blockchain/Dev/` carries **two tracked env templates** — `env.example` (444 lines, 102 distinct
variables) and `.env.example` (327 lines, 65 variables) — and the two consumers read different ones.
`scripts/bootstrap-env.sh:26` sets `ENV_EXAMPLE="$DEV_DIR/.env.example"`, while the documentation
documents the other file: `Blockchain/Dev/README.md:25` and `Blockchain/Dev/CONTRIBUTING.md:26` both
say `cp env.example .env`, `docs/DEPLOYMENT.md:130` and `docs/DEVELOPER-GUIDE.md:53` say the same, and
`docs/ENVIRONMENT-VARIABLES.md:13-15` names `env.example` as *the* core infrastructure template. So a
developer who follows the docs and a developer who runs the script get environments that differ by
**64 variables** (measured: the generated `.env` from the tip is missing 64 of the 102 that
`env.example` declares, including `ENABLE_TEST_TOKENS`, every `AUTH0_*`, every `AZURE_AD_*`, every
`STRIPE_*`, `SIMULATE_ANCHORING` and `VITE_ENABLE_DEMO`). **Kam ruled it: "env.example (the larger,
the one CLAUDE.md documents) is canonical."** This task points the script at the canonical template,
names it in the operator-visible message, and keeps the legacy name alive only as a fallback for a
tree that carries no `env.example` — because two existing harnesses build exactly such a tree
(`scripts/__tests__/bootstrap_env_slot_ports.test.sh:91` and
`scripts/verify-slot-credential-isolation.sh:59` each write only `.env.example` into a scratch clone
and then run this script), and breaking them is not part of the ruling. NOT in this task: editing
either template file, deleting `.env.example`, or reconciling the 30 variables that `.env.example`
declares and `env.example` does not — that is the separate reconciliation half of the KS-1077 shape.
## Drafter's note (feed9, read before the hunk)
CORRECTION vs the old READY (feed9 drafter): the old READY's hunk 2 removed `  exit 1` and kept the old `print_error ".env.example not found at: ..."` line - the reverse of what the old brief asked (KS-1081.md: replace the message line, keep `exit 1`), and a real defect (a missing template would no longer stop the script by that guard). Hunk 2 below is the BRIEF's shape: the `-` line is the old `print_error` message, the `+` line is the new message, `  exit 1` stays as context. Nothing else differs from the old READY. The suite has no cell on the missing-template path, so B4/B5 read the same lines either way. Scope note from the old READY: the NAMED legacy fallback (`ENV_EXAMPLE_LEGACY`) is deliberate and must stay until the two templates are reconciled.

## The exact change - 3 hunk(s) in `Blockchain/Dev/scripts/bootstrap-env.sh` (3 '-' line(s), 16 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
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
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:26` - **must change**: `ENV_EXAMPLE="$DEV_DIR/.env.example"`
* `:56` - **must change**: `  print_error ".env.example not found at: $ENV_EXAMPLE"`
* `:67` - **must change**: `  print_success "Created .env from .env.example"`
* `:23` - (correct) `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"` - stays
* `:24` - (correct) `DEV_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh`

File: `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/bootstrap_env_slot_ports.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (90 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh`, ONE hunk header `@@ -0,0 +1,90 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TEST: bootstrap-env.sh copies the CANONICAL template env.example (KS-1081)
# =============================================================================
# Usage: bash Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEV_DIR="$(cd "$HERE/../.." && pwd)"
BOOTSTRAP="${BOOTSTRAP_SH:-$HERE/../bootstrap-env.sh}"
ENV_SH="$HERE/../stack_env.sh"
CANONICAL="$DEV_DIR/env.example"
LEGACY="$DEV_DIR/.env.example"
[[ -f "$BOOTSTRAP" ]] || { echo "FATAL: bootstrap-env.sh not found at $BOOTSTRAP" >&2; exit 2; }
[[ -f "$ENV_SH" ]]    || { echo "FATAL: stack_env.sh not found at $ENV_SH" >&2; exit 2; }
[[ -f "$CANONICAL" ]] || { echo "FATAL: canonical template not found at $CANONICAL" >&2; exit 2; }
[[ -f "$LEGACY" ]]    || { echo "FATAL: legacy template not found at $LEGACY" >&2; exit 2; }
command -v openssl >/dev/null 2>&1 || { echo "FATAL: openssl required (bootstrap-env.sh needs it)" >&2; exit 2; }
PASS=0
FAIL=0

var_names() { grep -E '^[A-Z][A-Z0-9_]*=' "$1" | cut -d= -f1 | sort -u; }
GENERATED='^(POSTGRES_PASSWORD|DATABASE_URL|REDIS_PASSWORD|REDIS_URL|PII_ENCRYPTION_KEY|PII_ENCRYPTION_KEY_VERSION|PII_LOOKUP_HMAC_KEY|DEMO_SERVICE_ENABLED|DEMO_SERVICE_KEY|JWT_PRIVATE_KEY|JWT_PUBLIC_KEY|JWT_KEY_ID)$'
CANON_ONLY="$(comm -23 <(var_names "$CANONICAL") <(var_names "$LEGACY") | grep -vE "$GENERATED" | head -n1)"
[[ -n "$CANON_ONLY" ]] || { echo "FATAL: the two templates no longer differ outside the script-generated keys - premise of this suite changed" >&2; exit 2; }

SCRATCH_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/ks1081.XXXXXX")"
trap 'rm -rf "$SCRATCH_ROOT"' EXIT
BOTH="$SCRATCH_ROOT/both/Blockchain/Dev"
mkdir -p "$BOTH/scripts"
cp "$BOOTSTRAP" "$BOTH/scripts/bootstrap-env.sh"
cp "$ENV_SH" "$BOTH/scripts/stack_env.sh"
cp "$CANONICAL" "$BOTH/env.example"
cp "$LEGACY" "$BOTH/.env.example"
env -u SECUURA_STACK_SLOT -u STACK_SLOT -u POSTGRES_EXTERNAL_PORT -u REDIS_EXTERNAL_PORT HOME="$HOME" PATH="$PATH" bash "$BOTH/scripts/bootstrap-env.sh" >"$BOTH/bootstrap.log" 2>&1
BOTH_RC=$?

ONLY_LEGACY="$SCRATCH_ROOT/legacyonly/Blockchain/Dev"
mkdir -p "$ONLY_LEGACY/scripts"
cp "$BOOTSTRAP" "$ONLY_LEGACY/scripts/bootstrap-env.sh"
cp "$ENV_SH" "$ONLY_LEGACY/scripts/stack_env.sh"
cp "$LEGACY" "$ONLY_LEGACY/.env.example"
env -u SECUURA_STACK_SLOT -u STACK_SLOT -u POSTGRES_EXTERNAL_PORT -u REDIS_EXTERNAL_PORT HOME="$HOME" PATH="$PATH" bash "$ONLY_LEGACY/scripts/bootstrap-env.sh" >"$ONLY_LEGACY/bootstrap.log" 2>&1
LEGACY_RC=$?

MISSING_N="$(comm -23 <(var_names "$CANONICAL") <(var_names "$BOTH/.env") | grep -c .)"
MISSING="$(comm -23 <(var_names "$CANONICAL") <(var_names "$BOTH/.env") | head -n 6 | xargs)"
DB_PORT="$(grep -E '^DATABASE_URL=' "$BOTH/.env" | head -n1 | sed -E 's#^.*@localhost:##; s#/.*$##')"

if [[ "$MISSING_N" -eq 0 ]]; then
  echo "PASS: every variable in env.example reached the generated .env"; PASS=$((PASS+1))
else
  echo "FAIL: the generated .env is missing $MISSING_N variables that env.example declares (first 6: $MISSING)"; FAIL=$((FAIL+1))
fi

if grep -qE "^${CANON_ONLY}=" "$BOTH/.env"; then
  echo "PASS: the canonical-only variable $CANON_ONLY is in the generated .env"; PASS=$((PASS+1))
else
  echo "FAIL: $CANON_ONLY is declared in env.example and absent from the generated .env - .env.example was copied"; FAIL=$((FAIL+1))
fi

if grep -qF 'Created .env from env.example' "$BOTH/bootstrap.log"; then
  echo "PASS: the script reports the canonical template by name"; PASS=$((PASS+1))
else
  echo "FAIL: the bootstrap log does not say 'Created .env from env.example'"; FAIL=$((FAIL+1))
fi

if grep -qF '$DEV_DIR/env.example' "$BOOTSTRAP"; then
  echo "PASS: the script resolves the canonical template path under DEV_DIR"; PASS=$((PASS+1))
else
  echo "FAIL: $BOOTSTRAP never names the canonical env.example path under DEV_DIR"; FAIL=$((FAIL+1))
fi

if [[ "$BOTH_RC" -eq 0 && "$DB_PORT" == "6432" ]]; then
  echo "PASS: CONTROL bootstrap exits 0 and DATABASE_URL still carries the slot-1 port 6432"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL bootstrap rc=$BOTH_RC, DATABASE_URL port '$DB_PORT' (want rc 0 and 6432)"; FAIL=$((FAIL+1))
fi

if [[ "$LEGACY_RC" -eq 0 && -f "$ONLY_LEGACY/.env" ]]; then
  echo "PASS: CONTROL a tree carrying only .env.example still bootstraps (the fallback)"; PASS=$((PASS+1))
else
  echo "FAIL: CONTROL a tree carrying only .env.example no longer bootstraps (rc=$LEGACY_RC)"; FAIL=$((FAIL+1))
fi

echo ""
echo "bootstrap_env_canonical_template: $PASS passed, $FAIL failed"
[[ $FAIL -eq 0 ]]
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `echo "PASS: every variable in env.example reached the generated .env"; PASS=$((PASS+1))`
- `echo "PASS: the canonical-only variable $CANON_ONLY is in the generated .env"; PASS=$((PASS+1))`
- `echo "PASS: the script reports the canonical template by name"; PASS=$((PASS+1))`
- `echo "PASS: the script resolves the canonical template path under DEV_DIR"; PASS=$((PASS+1))`
- `echo "PASS: CONTROL bootstrap exits 0 and DATABASE_URL still carries the slot-1 port 6432"; PASS=$((PASS+1))`
- `echo "PASS: CONTROL a tree carrying only .env.example still bootstraps (the fallback)"; PASS=$((PASS+1))`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/bootstrap-env.sh` / `+++ b/Blockchain/Dev/scripts/bootstrap-env.sh` (3 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` (one hunk, `@@ -0,0 +1,90 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed9 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 10:26:40 AEST)
- `Blockchain/Dev/scripts/bootstrap-env.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Blockchain/Dev/scripts/bootstrap-env.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/bootstrap_env_slot_ports.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x; FEED 9 inherits it) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed9-drafter-precheck/CANONENV/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1081 on the Secuura board at 2026-09-22 10:26:40 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
