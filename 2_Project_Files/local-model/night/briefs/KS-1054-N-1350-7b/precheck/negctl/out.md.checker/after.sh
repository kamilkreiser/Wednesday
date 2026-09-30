#!/usr/bin/env bash
# =============================================================================
# SECUURA PLATFORM — UNIFIED DEPLOYMENT SCRIPT
# =============================================================================
# Builds ALL services with a single git-hash tag and deploys them atomically
# to the target environment. Ensures all services run the same version.
#
# Usage:
#   ./deploy-all.sh dev              # Deploy to Azure Dev
#   ./deploy-all.sh demo             # Deploy to Azure Demo
#   ./deploy-all.sh dev --skip-build # Deploy using existing :latest images
#   ./deploy-all.sh dev --services "originate auth api-gateway"  # Subset only
#   ./deploy-all.sh dev --dry-run    # Show what would be deployed
#
# Requirements:
#   - Azure CLI logged in (az login)
#   - ACR access (secuura02demoacr)
#   - Run from repo root (Blockchain/Dev/)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# KS-359: single source of truth for the deployment id, matching deploy.sh.
# The demo container apps are named "${DEPLOYMENT_ID}-demo-*" (e.g.
# secuura02-demo-api); deriving the prefix from here (instead of a hardcoded
# "secuura-demo") keeps deploy-all.sh in step after the secuura02 rename.
DEPLOYMENT_ID="secuura02"
ACR="${DEPLOYMENT_ID}demoacr"
ACR_URL="${ACR}.azurecr.io/secuura"

# Environment configuration (bash 3 compatible)
get_env_config() {
  local env="$1" key="$2"
  case "${env}_${key}" in
    dev_rg)     echo "secuura-dev-rg" ;;
    dev_prefix) echo "secuura-dev" ;;
    dev_domain) echo "kindtree-935b2ded.southeastasia.azurecontainerapps.io" ;;
    demo_rg)     echo "secuura-demo-rg" ;;
    demo_prefix) echo "${DEPLOYMENT_ID}-demo" ;;
    demo_domain) echo "kindtree-935b2ded.southeastasia.azurecontainerapps.io" ;;
  esac
}

# Service → Dockerfile mapping
# Format: "container-app-suffix:image-name:dockerfile-path"
BACKEND_SERVICES=(
  "api:api-gateway:services/api-gateway/Dockerfile"
  "originate:originate:services/originate/Dockerfile"
  "auth:auth:services/auth/Dockerfile"
  "anchoring:anchoring:services/anchoring/Dockerfile"
  "wallet:wallet-connector:services/wallet-connector/Dockerfile"
  "prism:prism:services/prism/Dockerfile"
  "security:security:services/security/Dockerfile"
  "analytics:analytics:services/analytics/Dockerfile"
  "timestamp:timestamping:services/timestamping/Dockerfile"
  "billing:billing:services/billing/Dockerfile"
  "tokenisation:tokenisation:services/tokenisation/Dockerfile"
  "tenant-prov:tenant-provisioning:services/tenant-provisioning/Dockerfile"
)

# Frontend services (only deployed when --include-frontend is passed)
FRONTEND_SERVICES=(
  "admin:frontend-admin:frontend/admin/Dockerfile"
  "issuer:frontend-issuer:frontend/issuer/Dockerfile"
  "verifier:frontend-verifier:frontend/verifier/Dockerfile"
)

# Optional services (only exist in some environments)
OPTIONAL_SERVICES=(
  "m365:m365-integration:services/m365-integration/Dockerfile"
  "outlook:outlook-addin:frontend/outlook-addin/Dockerfile"
)

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------

TARGET_ENV="${1:-}"
SKIP_BUILD=false
DRY_RUN=false
INCLUDE_FRONTEND=false
SPECIFIC_SERVICES=""
SKIP_SMOKE=false

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-build) SKIP_BUILD=true ;;
    --dry-run) DRY_RUN=true ;;
    --include-frontend) INCLUDE_FRONTEND=true ;;
    --skip-smoke) SKIP_SMOKE=true ;;
    --services) SPECIFIC_SERVICES="$2"; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

if [[ -z "$TARGET_ENV" ]] || [[ "$TARGET_ENV" != "dev" && "$TARGET_ENV" != "demo" ]]; then
  echo "Usage: $0 <dev|demo> [--skip-build] [--dry-run] [--include-frontend] [--services 'svc1 svc2']"
  exit 1
fi

RG="$(get_env_config "$TARGET_ENV" rg)"
PREFIX="$(get_env_config "$TARGET_ENV" prefix)"
DOMAIN="$(get_env_config "$TARGET_ENV" domain)"
TAG="$(git rev-parse --short HEAD)-$(date +%Y%m%d%H%M)"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  SECUURA UNIFIED DEPLOYMENT                              ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║  Environment:  ${TARGET_ENV}                                       ║"
echo "║  Resource Group: ${RG}                       ║"
echo "║  Image Tag:   ${TAG}                          ║"
echo "║  Skip Build:  ${SKIP_BUILD}                                    ║"
echo "║  Dry Run:     ${DRY_RUN}                                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# ---------------------------------------------------------------------------
# Determine which services to deploy
# ---------------------------------------------------------------------------

SERVICES_TO_DEPLOY=()

if [[ -n "$SPECIFIC_SERVICES" ]]; then
  # User specified a subset
  for svc in $SPECIFIC_SERVICES; do
    for entry in "${BACKEND_SERVICES[@]}" "${FRONTEND_SERVICES[@]}" "${OPTIONAL_SERVICES[@]}"; do
      app_suffix=$(echo "$entry" | cut -d: -f1)
      if [[ "$svc" == "$app_suffix" ]] || [[ "$svc" == "$(echo "$entry" | cut -d: -f2)" ]]; then
        SERVICES_TO_DEPLOY+=("$entry")
      fi
    done
  done
else
  # All backend services
  SERVICES_TO_DEPLOY=("${BACKEND_SERVICES[@]}")
  # Frontend if requested
  if [[ "$INCLUDE_FRONTEND" == "true" ]]; then
    SERVICES_TO_DEPLOY+=("${FRONTEND_SERVICES[@]}")
  fi
  # Optional services only if they exist in the target environment
  for entry in "${OPTIONAL_SERVICES[@]}"; do
    app_suffix=$(echo "$entry" | cut -d: -f1)
    app_name="${PREFIX}-${app_suffix}"
    if az containerapp show --name "$app_name" --resource-group "$RG" &>/dev/null; then
      SERVICES_TO_DEPLOY+=("$entry")
    fi
  done
fi

echo "Services to deploy (${#SERVICES_TO_DEPLOY[@]}):"
for entry in "${SERVICES_TO_DEPLOY[@]}"; do
  echo "  - $(echo "$entry" | cut -d: -f2)"
done
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
  echo "[DRY RUN] Would build and deploy ${#SERVICES_TO_DEPLOY[@]} services with tag ${TAG}"
  exit 0
fi

# ---------------------------------------------------------------------------
# Build phase — parallel ACR builds
# ---------------------------------------------------------------------------

if [[ "$SKIP_BUILD" == "false" ]]; then
  echo "═══ BUILD PHASE ═══"
  PIDS=()
  BUILD_LOGS=()

  for entry in "${SERVICES_TO_DEPLOY[@]}"; do
    image_name=$(echo "$entry" | cut -d: -f2)
    dockerfile=$(echo "$entry" | cut -d: -f3)

    if [[ ! -f "$dockerfile" ]]; then
      echo "  ⚠ Skipping $image_name — Dockerfile not found: $dockerfile"
      continue
    fi

    LOG="/tmp/secuura-build-${image_name}.log"
    BUILD_LOGS+=("$image_name:$LOG")

    echo "  Building $image_name..."
    az acr build --registry "$ACR" \
      --image "secuura/${image_name}:${TAG}" \
      --file "$dockerfile" . \
      > "$LOG" 2>&1 &
    PIDS+=($!)
  done

  # Wait for all builds
  FAILED=0
  for i in "${!PIDS[@]}"; do
    if ! wait "${PIDS[$i]}"; then
      entry="${BUILD_LOGS[$i]}"
      name=$(echo "$entry" | cut -d: -f1)
      log=$(echo "$entry" | cut -d: -f2-)
      echo "  ✗ FAILED: $name"
      tail -5 "$log"
      FAILED=$((FAILED + 1))
    fi
  done

  if [[ $FAILED -gt 0 ]]; then
    echo ""
    echo "ERROR: $FAILED build(s) failed. Aborting deployment."
    exit 1
  fi

  echo "  All ${#SERVICES_TO_DEPLOY[@]} builds succeeded."
  echo ""
fi

# ---------------------------------------------------------------------------
# Deploy phase — update all container apps
# ---------------------------------------------------------------------------

echo "═══ DEPLOY PHASE ═══"
DEPLOY_FAILED=0

for entry in "${SERVICES_TO_DEPLOY[@]}"; do
  app_suffix=$(echo "$entry" | cut -d: -f1)
  image_name=$(echo "$entry" | cut -d: -f2)
  app_name="${PREFIX}-${app_suffix}"
  image="${ACR_URL}/${image_name}:${TAG}"

  echo -n "  Deploying ${app_name}... "
  if az containerapp update --name "$app_name" --resource-group "$RG" \
    --image "$image" &>/dev/null; then
    echo "done"
  else
    echo "FAILED"
    DEPLOY_FAILED=$((DEPLOY_FAILED + 1))
  fi
done

if [[ $DEPLOY_FAILED -gt 0 ]]; then
  echo ""
  echo "WARNING: $DEPLOY_FAILED deployment(s) failed."
fi

echo ""
echo "Deployment complete. Tag: ${TAG}"
echo ""

# ---------------------------------------------------------------------------
# Smoke test phase
# ---------------------------------------------------------------------------

if [[ "$SKIP_SMOKE" == "true" ]]; then
  echo "Skipping smoke tests (--skip-smoke)"
  exit 0
fi

echo "═══ SMOKE TEST PHASE (waiting 30s for containers to start) ═══"
sleep 30

API="https://${PREFIX}-api.${DOMAIN}"
PASS=0
FAIL=0
# KS-1054 / gate44 N-1346-3: a third counter. A check that did not RUN was landing in PASS and
# inflating "7 passed, 0 failed". It must not land in FAIL either — that would fail a deploy over a
# rollback to an older image whose /health has no such field.
SKIP=0

smoke_skip() { # a check that did NOT run: neither a pass nor a failure
  local name="$1"
  local why="$2"
  echo "  ⚠ $name — SKIPPED: $why (not a pass)"
  SKIP=$((SKIP + 1))
}

smoke_test() {
  local name="$1"
  local expected="$2"
  local actual="$3"
  if [[ "$actual" == "$expected" ]]; then
    echo "  ✓ $name"
    PASS=$((PASS + 1))
  else
    echo "  ✗ $name (expected $expected, got $actual)"
    FAIL=$((FAIL + 1))
  fi
}

# 1. Health
CODE=$(curl -s --max-time 10 -o /dev/null -w "%{http_code}" "$API/health")
smoke_test "Health check" "200" "$CODE"

# 1b. KS-1054 / N-1332-5 — startup migrations. The check above discards the BODY
# (`-o /dev/null`), so it cannot see a failed startup migration: /health answers 200 and stays
# healthy by design (Kam's option (a)), and the failure is reported in the payload. Fetch the
# body and let the shared predicate decide; it keys on `failed`, never on `error`.
HEALTH_BODY=$(curl -s --max-time 10 "$API/health")
# THREE-WAY, matching the predicate's three exit codes. `|| MIG_RC=$?` is load-bearing under
# `set -e` (:21). rc 2 is rendered as a named SKIP: it neither counts as a pass nor fails the deploy.
MIG_RC=0
"$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/check-startup-migrations.sh" "$HEALTH_BODY" || MIG_RC=$?
case "$MIG_RC" in
  0)
    smoke_test "Startup migrations" "0 failed" "0 failed"
    ;;
  2)
    smoke_skip "Startup migrations" "the check did not run — see above"
    ;;
  *)
    # rc 1 is a failed count OR a count that could not be read (python3 missing, a non-integer
    # `failed`), so the reported value must not claim the migrations were read (gate47 N-1350-7).
    smoke_test "Startup migrations" "0 failed" "failed or could not be verified — see above"
    ;;
esac

# 2. Login
LOGIN_RESP=$(curl -s --max-time 10 -X POST "$API/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@secuura.com","password":"admin123"}')
TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('accessToken',''))" 2>/dev/null || echo "")
if [[ -n "$TOKEN" && "$TOKEN" != "None" ]]; then
  smoke_test "Admin login" "200" "200"
else
  smoke_test "Admin login" "200" "FAIL"
fi

# 3. Platform tenants (admin only)
if [[ -n "$TOKEN" && "$TOKEN" != "None" ]]; then
  CODE=$(curl -s --max-time 10 -o /dev/null -w "%{http_code}" "$API/api/platform/tenants" \
    -H "Authorization: Bearer $TOKEN")
  smoke_test "Platform tenants" "200" "$CODE"
fi

# 4. Certification
if [[ -n "$TOKEN" && "$TOKEN" != "None" ]]; then
  CERT_CODE=$(curl -s --max-time 10 -o /dev/null -w "%{http_code}" -X POST "$API/api/certifications/issue" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
    -d '{"type":"certificate","data":{"title":"Smoke Test","issuedBy":"Deploy Script"}}')
  smoke_test "Certification issue" "201" "$CERT_CODE"
fi

# 5. Verification
VERIFY_CODE=$(curl -s --max-time 10 -o /dev/null -w "%{http_code}" -X POST "$API/api/verification/verify" \
  -H 'Content-Type: application/json' \
  -d '{"contentHash":"sha256:smoketest"}')
smoke_test "Verification endpoint" "200" "$VERIFY_CODE"

# 6. RBAC — non-admin should get 403 on platform
NON_ADMIN_RESP=$(curl -s --max-time 10 -X POST "$API/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d '{"email":"registrar@ox.ac.uk","password":"OxRegistrar123!@#"}')
NON_ADMIN_TOKEN=$(echo "$NON_ADMIN_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('accessToken',''))" 2>/dev/null || echo "")
if [[ -n "$NON_ADMIN_TOKEN" && "$NON_ADMIN_TOKEN" != "None" ]]; then
  CODE=$(curl -s --max-time 10 -o /dev/null -w "%{http_code}" "$API/api/platform/tenants" \
    -H "Authorization: Bearer $NON_ADMIN_TOKEN")
  smoke_test "RBAC: OWNER blocked from platform" "403" "$CODE"
fi

echo ""
echo "═══ SMOKE TEST RESULTS: $PASS passed, $FAIL failed, $SKIP skipped ═══"

if [[ $FAIL -gt 0 ]]; then
  echo ""
  echo "⚠ WARNING: Some smoke tests failed. Review the deployment."
  exit 1
fi

echo ""
echo "✓ Deployment and smoke tests passed for ${TARGET_ENV}."
echo "  Tag: ${TAG}"
echo "  API: ${API}"
