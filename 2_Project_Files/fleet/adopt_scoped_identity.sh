#!/bin/bash
# adopt_scoped_identity.sh — move a project's `az` session onto its OWN scoped
# service principal, instead of Kam's Owner account.
#
# WHY THIS EXISTS: the two-command version required copy-pasting a client secret
# between terminal and chat, and embedded a path containing "!" which zsh expands
# as history when typed interactively ("zsh: event not found: CODING/..."). Both
# hazards were mine to remove, not Kam's to work around. This script:
#   - generates the secret and CONSUMES it in the same process (never displayed,
#     never pasted, never in a transcript or a shell history line);
#   - hard-codes the paths, so nothing with a "!" is ever typed at a prompt;
#   - verifies the result and prints only the identity, never the credential.
#
# Kam runs this. It writes into the target project's own 4_Credentials/.azure —
# his credential, his folder.
#
# Usage:  ./adopt_scoped_identity.sh vision
#         ./adopt_scoped_identity.sh cypherkey
set -u

WED_AZ="/Volumes/KK_T9_External_HDD/WEDNESDAY/4_Credentials/.azure"
TENANT="d500ebad-cf53-4f2a-a501-f831289e67fc"

case "${1:-}" in
  vision)
    APP_ID="bc1e3581-a76e-4df1-a807-58b4386c6f8d"
    TARGET="/Volumes/DevMASTER/!CODING/Datasec/Vision_Sales_Portal/4_Credentials/.azure"
    LABEL="Datasec / Vision Sales Portal"
    EXPECT_RG="datasec-sales-portal-rg"
    ;;
  cypherkey)
    APP_ID="d2efb3de-9cda-42f3-9203-19bf401b3b25"
    TARGET="/Volumes/DevMASTER/!CODING/Datasec/CypherKey/4_Credentials/.azure"
    LABEL="Datasec / CypherKey (OneTimePad)"
    EXPECT_RG="rg-otp-demo"
    ;;
  *)
    echo "usage: $0 vision|cypherkey" >&2; exit 2 ;;
esac

command -v az >/dev/null || { echo "az not on PATH" >&2; exit 2; }
[ -d "$WED_AZ" ] || { echo "Wednesday az config missing: $WED_AZ" >&2; exit 2; }
mkdir -p "$TARGET" || { echo "cannot create $TARGET" >&2; exit 2; }

echo "==> $LABEL"
echo "    app: $APP_ID"
echo "    target config: $TARGET"

# 1. Rotate/generate the secret. --query password -o tsv keeps it a bare value on
#    stdout; it goes straight into a variable and is never echoed.
echo "==> generating a fresh client secret (replaces any existing one)…"
PW="$(AZURE_CONFIG_DIR="$WED_AZ" az ad app credential reset \
        --id "$APP_ID" --years 1 --query password -o tsv 2>/dev/null)"
[ -n "$PW" ] || { echo "FAILED to generate a secret (are you logged in as an owner?)" >&2; exit 1; }

# 2. Consume it in the target project's isolated config dir.
#    RETRY IS REQUIRED, not defensive padding: a freshly-created Azure AD client
#    secret is not immediately usable. Measured 2026-08-06 against this very app —
#    attempts at 0s and 5s both returned AADSTS7000215 "Invalid client secret",
#    and the same secret authenticated fine at 10s. The first version of this
#    script tried once and reported LOGIN FAILED, which was pure propagation lag.
#    Errors are PRINTED, never discarded — the first version swallowed the
#    AADSTS code and left nothing to diagnose.
echo "==> logging the project session in as the scoped identity…"
RC=1
for attempt in 1 2 3 4 5 6 7 8; do
  ERR="$(AZURE_CONFIG_DIR="$TARGET" az login --service-principal \
          -u "$APP_ID" -p "$PW" --tenant "$TENANT" -o none 2>&1)"
  RC=$?
  [ $RC -eq 0 ] && { echo "    authenticated on attempt $attempt (~$(( (attempt-1)*5 ))s)"; break; }
  case "$ERR" in
    *AADSTS7000215*) echo "    attempt $attempt: secret not propagated yet, waiting 5s…" ;;
    *)               echo "    attempt $attempt failed: $(echo "$ERR" | head -1)" ;;
  esac
  sleep 5
done
PW=""; unset PW   # gone from this process either way

if [ $RC -ne 0 ]; then
  echo "LOGIN FAILED after 8 attempts (~40s). Last error:" >&2
  echo "$ERR" | head -3 >&2
  echo "The secret was rotated, so simply re-run this script — nothing is left in a bad state." >&2
  exit 1
fi

# 2b. PURGE any other identity from this project's config.
#     Found 2026-08-06 on Vision: after adopting the scoped SP, Kam's
#     kreiser.org@me.com (Owner) was STILL in the same profile as a non-default
#     account — so the agent could `az account set` straight back to Owner and
#     reach every project. Scoping an identity is worthless if a broader one is
#     still sitting beside it. The config must hold exactly ONE identity.
echo "==> purging any other identity from this project's config…"
OTHERS="$(AZURE_CONFIG_DIR="$TARGET" az account list --all \
           --query "[?user.name!='$APP_ID'].user.name" -o tsv 2>/dev/null | sort -u)"
if [ -n "$OTHERS" ]; then
  while IFS= read -r who; do
    [ -n "$who" ] || continue
    AZURE_CONFIG_DIR="$TARGET" az logout --username "$who" 2>/dev/null \
      && echo "    removed: $who" \
      || echo "    WARNING: could not remove $who — check manually" >&2
  done <<< "$OTHERS"
else
  echo "    none present (config holds only the scoped identity)"
fi

# 3. Verify: who is it, and can it see only what it should?
echo "==> verifying…"
echo "==> identities remaining in this config (must be exactly one):"
AZURE_CONFIG_DIR="$TARGET" az account list --all \
  --query "[].{identity:user.name,type:user.type}" -o tsv 2>/dev/null | sed 's/^/    /'
AZURE_CONFIG_DIR="$TARGET" az account show \
  --query "{identity:user.name, type:user.type, subscription:name}" -o json 2>/dev/null

echo "==> resource groups visible to this identity:"
AZURE_CONFIG_DIR="$TARGET" az group list --query "[].name" -o tsv 2>/dev/null | sed 's/^/    /'

echo
echo "Expected: the identity is the app id above (type servicePrincipal), and the"
echo "visible groups are that project's own only (e.g. $EXPECT_RG)."
echo "If you can see another project's resource groups, tell Wednesday — the scoping is wrong."
