#!/bin/bash
# =============================================================================
# SECUURA AZURE STAGING DEPLOYMENT
# =============================================================================
# This script deploys the complete Secuura staging environment to Azure.
# 
# ISOLATION: This deployment creates a completely self-contained environment
# that will NOT interfere with any other Azure resources or VMs.
#
# Prerequisites:
#   - Azure CLI installed and logged in
#   - Docker installed
#
# Usage:
#   ./deploy.sh                    # Full deployment
#   ./deploy.sh setup              # Setup infrastructure only
#   ./deploy.sh build              # Build and push images only
#   ./deploy.sh deploy             # Deploy apps only
#   ./deploy.sh services           # Deploy microservices only
#   ./deploy.sh status             # Check deployment status
#   ./deploy.sh destroy            # Remove all Secuura resources
# =============================================================================

# Pen-test H8: strict mode. `-u` unsets-as-error catches typos in
# variable expansions; `pipefail` makes piped commands fail if any
# stage fails (not just the last). Without these, the script silently
# tolerated unset KV refs and pipe failures during deploy.
set -euo pipefail

# Pen-test M20: secret hygiene
#   - NEVER `echo $POSTGRES_PASSWORD` / `echo $JWT_SECRET` / `echo $JWT_PRIVATE_KEY` / `echo $ACR_PASSWORD`.
#     Use `[ -n "$VAR" ] && echo "<set>" || echo "<missing>"` for verification.
#   - NEVER enable `set -x` in this script — it'll dump secret-bearing
#     `--parameters foo="$SECRET"` lines to the build log.
#   - Every `az keyvault secret set --value "$VAR"` already redirects to
#     /dev/null; do not change that.
#   - On error, bash prints the failing line. We accept this trade-off:
#     the alternative (custom ERR trap with line blanking) was tried and
#     was finicky; instead the lint scans CI for any new `set -x` or
#     `echo $.*PASSWORD|SECRET|KEY` regression.
trap 'echo "[deploy.sh] aborted at line $LINENO" >&2' ERR

# =============================================================================
# CONFIGURATION - Unique identifiers for isolation
# =============================================================================
DEPLOYMENT_ID="${SECUURA_DEPLOYMENT_ID:-secuura02}"   # Unique ID; defaults to the live Founders Hub tenant (secuura02). The OLD Secuura tenant (secuura01) is decommissioning — set SECUURA_DEPLOYMENT_ID=secuura01 only for decommission/rollback. A bare default of secuura01 silently targeted the dead env's resource names (KS-309).
LOCATION="${SECUURA_LOCATION:-southeastasia}"      # Azure region — Singapore (Southeast Asia). Override via SECUURA_LOCATION. Was uksouth until the 2026-06-17 region move.

# Environment selection: pass -e dev|demo or SECUURA_ENV=dev|demo
# Default: demo (production/demo environment)
ENVIRONMENT="${SECUURA_ENV:-demo}"

# Parse -e flag if provided (must come before the command)
while getopts "e:" opt 2>/dev/null; do
    case $opt in
        e) ENVIRONMENT="$OPTARG" ;;
        *)
            echo "Unknown option: -$OPTARG (allowed: -e dev|demo)" >&2
            exit 64
            ;;
    esac
done
shift $((OPTIND - 1))

# Validate environment
case "$ENVIRONMENT" in
    dev|demo)
        ;;
    *)
        echo "ERROR: Invalid environment '$ENVIRONMENT'. Must be 'dev' or 'demo'."
        echo "Usage: $0 [-e dev|demo] {build|deploy|services|setup|status|verify|destroy|full}"
        exit 1
        ;;
esac

# Derived names (all prefixed for isolation)
RESOURCE_GROUP="secuura-${ENVIRONMENT}-rg"
# KS Azure migration: the legacy old-tenant deploy (secuura01) keeps the
# original "secuura-<env>-*" names; the new Founders Hub tenant (secuura02+)
# derives names from DEPLOYMENT_ID so its globally-unique resources (KV, PG,
# Redis, etc.) don't collide with the still-live old prod.
if [ "$DEPLOYMENT_ID" = "secuura01" ]; then
    PROJECT_PREFIX="secuura-${ENVIRONMENT}"
else
    PROJECT_PREFIX="${DEPLOYMENT_ID}-${ENVIRONMENT}"
fi
KEY_VAULT_NAME="${PROJECT_PREFIX}-kv"

# ACR is shared between environments to avoid duplicate image storage
# Both dev and demo pull from the same registry
SHARED_ACR_NAME="${DEPLOYMENT_ID}demoacr"

# Project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Image-tag persistence (KS-34 bug 1).
# build_images writes the computed IMAGE_TAG to this file so subsequent
# `services` / `verify` invocations from the same build pick up the same
# tag — no longer broken by date rollover between build and services
# steps. Gitignored.
LAST_BUILD_TAG_FILE="$SCRIPT_DIR/.last-build.tag"

# Canonical list of deployable units — the single source of truth shared by
# build_images (what to build) and assert_images_present (what must exist at
# the tag before a `services` deploy). Keeping one list prevents the two from
# drifting (a service built but not verified, or verified but not built).
ALL_SERVICES=(
    api-gateway auth wallet-connector prism timestamping anchoring security analytics
    m365-integration transfer tokenisation tenant-provisioning mcp-server
    originate billing kyc vc-issuer staking referral governance nft-certificate
)
# Each entry is "<dir>:<image-name>". For most frontends dir == image-name,
# but the Outlook add-in's folder is `outlook-addin` while its image is
# `frontend-outlook` (matching the Container App resource in services.bicep).
FRONTENDS=("issuer:issuer" "verifier:verifier" "admin:admin" "outlook-addin:outlook")

# Environment-specific image tags.
# AUDIT D-6: stop using mutable `:latest` for dev. Date+sha tags make every
# deployment reproducible, and they prevent an attacker who can push to ACR
# from silently overwriting an in-flight image. Demo was already date-pinned;
# dev now matches with the same shape (YYYYMMDD_<sha8>) plus a fallback to
# date-only when not in a git checkout.
#
# Resolution order depends on the subcommand:
#
# `build` — always computes a FRESH tag from current git+date state, then
# overwrites .last-build.tag at the end. Reading .last-build.tag here
# would pin an in-progress build to whatever the previous build pushed,
# defeating AUDIT D-6 (immutable tags) and silently overwriting a tag
# that ops may already be referencing. SECUURA_IMAGE_TAG override still
# wins for cases like rebuilding under an existing tag during incident
# response.
#
# Anything else (`services`, `verify`, `setup`, etc.) — reads the tag
# the latest build wrote, so chained invocations stay pinned to it
# regardless of a midnight UTC rollover. Falls back to current date+sha
# when no prior build exists (genuinely fresh checkout, redeploy of
# unchanged code, etc.).
#
# In all cases SECUURA_IMAGE_TAG remains the explicit override.
GIT_SHA=$(git rev-parse --short=8 HEAD 2>/dev/null || echo "nogit")
SUBCOMMAND="${1:-full}"

if [ -n "${SECUURA_IMAGE_TAG:-}" ]; then
    IMAGE_TAG="$SECUURA_IMAGE_TAG"
elif [ "$SUBCOMMAND" = "build" ] || [ "$SUBCOMMAND" = "full" ]; then
    # Fresh tag for any flow that builds images.
    IMAGE_TAG="$(date +%Y%m%d)_${GIT_SHA}"
elif [ -f "$LAST_BUILD_TAG_FILE" ] && [ -s "$LAST_BUILD_TAG_FILE" ]; then
    IMAGE_TAG="$(cat "$LAST_BUILD_TAG_FILE")"
else
    IMAGE_TAG="$(date +%Y%m%d)_${GIT_SHA}"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════════════╗"
echo "║                 SECUURA AZURE DEPLOYMENT                               ║"
echo "║                                                                        ║"
echo "║  Environment:    ${ENVIRONMENT}                                              ║"
echo "║  Deployment ID:  ${DEPLOYMENT_ID}                                            ║"
echo "║  Resource Group: ${RESOURCE_GROUP}                                    ║"
echo "║  Location:       ${LOCATION}                                          ║"
echo "║  Image Tag:      ${IMAGE_TAG}                                          ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# =============================================================================
# AZURE CLI CHECK
# =============================================================================
check_azure() {
    log_info "Checking Azure CLI..."
    
    if ! command -v az &> /dev/null; then
        log_error "Azure CLI not found. Please install it first."
        echo "  macOS: brew install azure-cli"
        echo "  Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
        exit 1
    fi
    
    # Check login
    if ! az account show &> /dev/null; then
        log_warn "Not logged in to Azure. Running az login..."
        az login
    fi
    
    SUBSCRIPTION=$(az account show --query name -o tsv)
    SUBSCRIPTION_ID=$(az account show --query id -o tsv)
    log_success "Logged in to: $SUBSCRIPTION"
    log_info "Subscription ID: $SUBSCRIPTION_ID"
}

# =============================================================================
# KEY VAULT FIREWALL PRE-FLIGHT
# =============================================================================
# The KV firewall on dev / demo allowlists static IPs. When the operator's
# residential / mobile / VPN IP rotates, the next `az keyvault secret show`
# returns Forbidden and `deploy.sh` halts in the middle of provisioning.
# Detect that BEFORE we try to deploy and add the current IP to the
# allowlist if needed. Set SKIP_KV_PREFLIGHT=1 to bypass (CI runs are
# typically already whitelisted via service-principal scope).
ensure_kv_access() {
    if [ "${SKIP_KV_PREFLIGHT:-0}" = "1" ]; then return 0; fi
    log_info "Checking Key Vault firewall access..."
    if az keyvault secret list --vault-name "$KEY_VAULT_NAME" --query 'length(@)' -o tsv >/dev/null 2>&1; then
        log_success "Key Vault accessible from this network."
        return 0
    fi
    local MYIP
    MYIP=$(curl -fsS https://api.ipify.org 2>/dev/null || curl -fsS https://ifconfig.me 2>/dev/null || true)
    if [ -z "$MYIP" ]; then
        log_warn "Could not determine current public IP — set SKIP_KV_PREFLIGHT=1 if you've already whitelisted it manually."
        return 0
    fi
    log_warn "Key Vault denied access. Adding $MYIP/32 to network rules..."
    az keyvault network-rule add --name "$KEY_VAULT_NAME" --resource-group "$RESOURCE_GROUP" --ip-address "$MYIP/32" >/dev/null 2>&1 || {
        log_warn "Could not auto-add IP. Run manually: az keyvault network-rule add --name $KEY_VAULT_NAME -g $RESOURCE_GROUP --ip-address $MYIP/32"
        return 0
    }
    # KV firewall takes a few seconds to propagate.
    sleep 8
    if az keyvault secret list --vault-name "$KEY_VAULT_NAME" --query 'length(@)' -o tsv >/dev/null 2>&1; then
        log_success "Key Vault access restored ($MYIP/32 allow-listed)."
    else
        log_warn "KV still inaccessible after rule add — may need a longer propagation wait."
    fi
}

# =============================================================================
# RESOURCE GROUP (Isolated)
# =============================================================================
create_resource_group() {
    log_info "Creating isolated resource group: $RESOURCE_GROUP..."
    
    if az group exists --name $RESOURCE_GROUP | grep -q true; then
        log_success "Resource group already exists."
    else
        az group create \
            --name $RESOURCE_GROUP \
            --location $LOCATION \
            --tags project=secuura environment=$ENVIRONMENT deploymentId=$DEPLOYMENT_ID
        log_success "Resource group created."
    fi
}

# =============================================================================
# KEY VAULT (Secrets Management)
# =============================================================================
setup_keyvault() {
    log_info "Setting up Key Vault: $KEY_VAULT_NAME..."
    
    # Create Key Vault if it doesn't exist
    if ! az keyvault show --name $KEY_VAULT_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
        az keyvault create \
            --name $KEY_VAULT_NAME \
            --resource-group $RESOURCE_GROUP \
            --location $LOCATION \
            --enable-rbac-authorization false \
            --tags project=secuura environment=$ENVIRONMENT deploymentId=$DEPLOYMENT_ID
        
        log_success "Key Vault created."
    else
        log_success "Key Vault already exists."
    fi
    
    # Generate PostgreSQL password if it doesn't exist
    if ! az keyvault secret show --vault-name $KEY_VAULT_NAME --name postgres-admin-password &> /dev/null; then
        POSTGRES_PASSWORD=$(openssl rand -base64 24 | tr -d '/+=')
        az keyvault secret set --vault-name $KEY_VAULT_NAME --name postgres-admin-password --value "$POSTGRES_PASSWORD" > /dev/null
        log_success "PostgreSQL password generated and stored."
    else
        log_info "PostgreSQL password already exists."
    fi
    
    # Generate the RS256 JWT signing keypair if it doesn't exist (KS-180).
    # The private key signs (auth only); the public key is published via the
    # JWKS endpoint (KS-182). Stored base64-encoded because PEM is multi-line
    # and would otherwise break bicep `--parameters` passing / Container Apps
    # env values.
    if ! az keyvault secret show --vault-name $KEY_VAULT_NAME --name jwt-private-key &> /dev/null; then
        JWT_PRIVATE_PEM=$(openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048)
        JWT_PUBLIC_PEM=$(printf '%s' "$JWT_PRIVATE_PEM" | openssl pkey -pubout)
        JWT_KID="k$(date +%Y%m%d%H%M%S)"
        az keyvault secret set --vault-name $KEY_VAULT_NAME --name jwt-private-key --value "$(printf '%s' "$JWT_PRIVATE_PEM" | base64 | tr -d '\n')" > /dev/null
        az keyvault secret set --vault-name $KEY_VAULT_NAME --name jwt-public-key  --value "$(printf '%s' "$JWT_PUBLIC_PEM"  | base64 | tr -d '\n')" > /dev/null
        az keyvault secret set --vault-name $KEY_VAULT_NAME --name jwt-key-id      --value "$JWT_KID" > /dev/null
        log_success "RS256 JWT signing keypair generated and stored (kid=$JWT_KID)."
    else
        log_info "JWT signing keypair already exists."
    fi

    # Store Deployment ID for reference
    if ! az keyvault secret show --vault-name $KEY_VAULT_NAME --name deployment-id &> /dev/null; then
        az keyvault secret set --vault-name $KEY_VAULT_NAME --name deployment-id --value "$DEPLOYMENT_ID" > /dev/null
    fi
}

# =============================================================================
# INFRASTRUCTURE DEPLOYMENT (Bicep)
# =============================================================================
deploy_infrastructure() {
    log_info "Deploying infrastructure with Bicep..."
    
    # Get secrets from Key Vault
    POSTGRES_PASSWORD=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name postgres-admin-password --query value -o tsv)

    log_info "Starting Bicep deployment (this may take 10-15 minutes)..."
    
    # For non-demo environments, pass the shared ACR password so the API gateway can pull images
    local ACR_PASS_PARAM=""
    if [ "$ENVIRONMENT" != "demo" ]; then
        local SHARED_ACR_PASS=$(az acr credential show --name $SHARED_ACR_NAME --query passwords[0].value -o tsv 2>/dev/null || echo "")
        if [ -n "$SHARED_ACR_PASS" ]; then
            ACR_PASS_PARAM="--parameters acrPassword=$SHARED_ACR_PASS"
        fi
    fi

    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --template-file "$SCRIPT_DIR/main.bicep" \
        --parameters environment=$ENVIRONMENT \
        --parameters location=$LOCATION \
        --parameters postgresAdminPassword="$POSTGRES_PASSWORD" \
        --parameters deploymentId="$DEPLOYMENT_ID" \
        --parameters imageTag="$IMAGE_TAG" \
        $ACR_PASS_PARAM \
        --name "secuura-infra-$(date +%Y%m%d%H%M%S)"
    
    log_success "Infrastructure deployed."
    
    # Show outputs
    echo ""
    log_info "Deployment outputs:"
    az deployment group show \
        --resource-group $RESOURCE_GROUP \
        --name "$(az deployment group list --resource-group $RESOURCE_GROUP --query '[0].name' -o tsv)" \
        --query properties.outputs -o table
}

# =============================================================================
# BUILD AND PUSH DOCKER IMAGES
# =============================================================================
build_images() {
    log_info "Building and pushing Docker images..."

    # ACR is shared between environments — always use the shared registry
    ACTUAL_ACR_NAME="$SHARED_ACR_NAME"

    log_info "Logging into shared ACR: $ACTUAL_ACR_NAME..."
    az acr login --name $ACTUAL_ACR_NAME

    # KS-102: track per-image build failures so a partial build is loud, not
    # masked. ALL_SERVICES / FRONTENDS are module-scoped (single source of
    # truth, shared with assert_images_present). All services build from the
    # monorepo root context (packages/shared dependency).
    BUILD_FAILURES=()

    DATE_TAG=$(date +%Y%m%d)

    echo ""
    log_info "Building ${#ALL_SERVICES[@]} services (monorepo context → az acr build)..."

    for SERVICE in "${ALL_SERVICES[@]}"; do
        DOCKERFILE="$PROJECT_ROOT/services/$SERVICE/Dockerfile"

        if [ -f "$DOCKERFILE" ]; then
            echo -e "${YELLOW}Building $SERVICE...${NC}"
            # AUDIT D-6: only push the immutable date+sha tag. Dropping the
            # `:latest` tag means an attacker who can push to ACR cannot
            # silently overwrite a tag a container app is configured to
            # follow — every container app is pinned to a specific
            # date+sha tag at deploy time.
            # KS-102: gate log_success on the real build result. Previously
            # `|| log_error` swallowed failures and "Pushed" ran regardless,
            # so a rate-limited build still reported success and exited 0.
            # KS-102 pt2: REGISTRY_PREFIX makes the Dockerfile pull its base
            # image (node/nginx) from the shared-ACR copy instead of Docker
            # Hub, so cloud builds never hit the anonymous pull-rate limit.
            # Base tags are mirrored into ACR once via `az acr import`; local
            # builds default REGISTRY_PREFIX to "" (Docker Hub), unchanged.
            if (cd "$PROJECT_ROOT" && az acr build --registry $ACTUAL_ACR_NAME \
                --image "secuura/$SERVICE:$IMAGE_TAG" \
                --file "services/$SERVICE/Dockerfile" \
                --platform linux/amd64 \
                --build-arg "REGISTRY_PREFIX=${ACTUAL_ACR_NAME}.azurecr.io/" \
                .); then
                log_success "Pushed $SERVICE:$IMAGE_TAG"
            else
                log_error "Failed to build $SERVICE — continuing with remaining services"
                BUILD_FAILURES+=("$SERVICE")
            fi
        else
            log_warn "Skipping $SERVICE (no Dockerfile at $DOCKERFILE)"
        fi
    done

    # KS-207: pgbouncer — its own Dockerfile + build context (docker/pgbouncer/),
    # not the monorepo root, so it can't be a plain ALL_SERVICES entry.
    # KS-363 follow-up: its base (edoburu/pgbouncer) now ALSO comes from the ACR
    # mirror via REGISTRY_PREFIX — the old "one small pull; no rate-limit concern"
    # assumption cost us the pgbouncer image on two cloud builds (missing tags
    # 20260627_34e63cd7 / 20260701_5f2c8cd2). Mirror import (KS-366 bumped the
    # pin to v1.25.2-p0 — upstream moved to v-prefixed tags after 1.22.x):
    #   az acr import --name <acr> --source docker.io/edoburu/pgbouncer:v1.25.2-p0 \
    #     --image edoburu/pgbouncer:v1.25.2-p0
    # (re-import when the pinned tag changes; refresh-base-images.sh acr does this).
    echo ""
    log_info "Building pgbouncer..."
    if (cd "$PROJECT_ROOT/docker/pgbouncer" && az acr build --registry $ACTUAL_ACR_NAME \
        --image "secuura/pgbouncer:$IMAGE_TAG" \
        --file Dockerfile \
        --platform linux/amd64 \
        --build-arg "REGISTRY_PREFIX=${ACTUAL_ACR_NAME}.azurecr.io/" \
        .); then
        log_success "Pushed pgbouncer:$IMAGE_TAG"
    else
        log_error "Failed to build pgbouncer"
        BUILD_FAILURES+=("pgbouncer")
    fi

    # Build frontends (monorepo context — they use COPY frontend/xxx/ and COPY packages/shared/)
    echo ""
    log_info "Building frontend applications..."

    for ENTRY in "${FRONTENDS[@]}"; do
        FRONTEND_DIR_NAME="${ENTRY%%:*}"
        FRONTEND_IMG_NAME="${ENTRY##*:}"
        FRONTEND_DIR="$PROJECT_ROOT/frontend/$FRONTEND_DIR_NAME"
        DOCKERFILE="$FRONTEND_DIR/Dockerfile"

        if [ -d "$FRONTEND_DIR" ] && [ -f "$DOCKERFILE" ]; then
            echo -e "${YELLOW}Building frontend-$FRONTEND_IMG_NAME (from frontend/$FRONTEND_DIR_NAME)...${NC}"
            # AUDIT D-6: see above — immutable tag only, no :latest.
            # KS-102: gate log_success on the real build result (see above).
            # KS-102 pt2: REGISTRY_PREFIX → base images from ACR, not Docker Hub.
            if (cd "$PROJECT_ROOT" && az acr build --registry $ACTUAL_ACR_NAME \
                --image "secuura/frontend-$FRONTEND_IMG_NAME:$IMAGE_TAG" \
                --file "frontend/$FRONTEND_DIR_NAME/Dockerfile" \
                --platform linux/amd64 \
                --build-arg "REGISTRY_PREFIX=${ACTUAL_ACR_NAME}.azurecr.io/" \
                .); then
                log_success "Pushed frontend-$FRONTEND_IMG_NAME"
            else
                log_error "Failed to build frontend-$FRONTEND_IMG_NAME — continuing"
                BUILD_FAILURES+=("frontend-$FRONTEND_IMG_NAME")
            fi
        else
            log_warn "Skipping frontend-$FRONTEND_IMG_NAME (no Dockerfile at $DOCKERFILE)"
        fi
    done

    # KS-102: a partial build must not silently advance the pipeline. If any
    # image failed, report the set, do NOT persist the tag (so a later
    # `services` won't adopt an incomplete tag), and exit non-zero.
    if [ ${#BUILD_FAILURES[@]} -gt 0 ]; then
        log_error "${#BUILD_FAILURES[@]} image(s) failed to build at tag '$IMAGE_TAG':"
        for FAILED in "${BUILD_FAILURES[@]}"; do log_error "  - $FAILED"; done
        log_error "Tag NOT persisted. Fix the failures (see KS-102 for the Docker Hub"
        log_error "pull-rate-limit root cause) and rebuild before deploying."
        return 1
    fi

    log_success "All images built and pushed."

    # KS-34 bug 1: persist the just-built tag so subsequent `services` /
    # `verify` invocations pick it up automatically. Removes the
    # date-rollover foot-gun where a long build straddling midnight UTC
    # would push e.g. 20260509_<sha> images, then `services` would look
    # for 20260510_<sha> and fail with MANIFEST_UNKNOWN.
    echo "$IMAGE_TAG" > "$LAST_BUILD_TAG_FILE"
    log_info "Wrote tag to $(basename "$LAST_BUILD_TAG_FILE"): $IMAGE_TAG"
}

# =============================================================================
# IMAGE PRESENCE GUARD (KS-102)
# =============================================================================
# Refuse to deploy if any expected image is missing at $IMAGE_TAG. A partial
# or failed build (e.g. the Docker Hub pull-rate limit blocking some services)
# must not silently roll a Container App to a non-existent image, which
# Container Apps reports as MANIFEST_UNKNOWN. Checks every service + frontend
# repo for the tag in the shared ACR.
assert_images_present() {
    local acr="$1" tag="$2"
    local missing=()
    log_info "Verifying all images exist at tag '$tag' in $acr before deploy..."

    local svc
    for svc in "${ALL_SERVICES[@]}"; do
        if ! az acr repository show-tags --name "$acr" --repository "secuura/$svc" -o tsv 2>/dev/null | grep -qx "$tag"; then
            missing+=("secuura/$svc:$tag")
        fi
    done

    # KS-207: pgbouncer is built separately but is now part of the stack — guard it too.
    if ! az acr repository show-tags --name "$acr" --repository "secuura/pgbouncer" -o tsv 2>/dev/null | grep -qx "$tag"; then
        missing+=("secuura/pgbouncer:$tag")
    fi

    local entry img
    for entry in "${FRONTENDS[@]}"; do
        img="${entry##*:}"
        if ! az acr repository show-tags --name "$acr" --repository "secuura/frontend-$img" -o tsv 2>/dev/null | grep -qx "$tag"; then
            missing+=("secuura/frontend-$img:$tag")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Refusing to deploy — ${#missing[@]} image(s) missing at tag '$tag':"
        local m
        for m in "${missing[@]}"; do log_error "  - $m"; done
        log_error "Run './deploy.sh -e $ENVIRONMENT build' (or rebuild the missing services) first."
        exit 1
    fi
    log_success "All ${#ALL_SERVICES[@]} services + ${#FRONTENDS[@]} frontends present at '$tag'."
}

# =============================================================================
# DEPLOY MICROSERVICES
# =============================================================================
deploy_services() {
    log_info "Deploying microservices to '$ENVIRONMENT' environment..."

    # Get infrastructure outputs (from main.bicep infra deployment)
    INFRA_DEPLOYMENT=$(az deployment group list --resource-group $RESOURCE_GROUP \
        --query "[?starts_with(name, 'secuura-infra') && properties.provisioningState=='Succeeded'] | [0].name" -o tsv)

    if [ -z "$INFRA_DEPLOYMENT" ]; then
        log_error "No infrastructure deployment found in $RESOURCE_GROUP. Run './deploy.sh -e $ENVIRONMENT setup' first."
        exit 1
    fi

    # ACR is shared — always use the shared registry
    ACTUAL_ACR_NAME="$SHARED_ACR_NAME"

    # KS-102: fail fast if a prior build left images missing at this tag,
    # rather than rolling Container Apps to a non-existent image.
    assert_images_present "$ACTUAL_ACR_NAME" "$IMAGE_TAG"

    ENV_ID=$(az deployment group show --resource-group $RESOURCE_GROUP --name "$INFRA_DEPLOYMENT" --query properties.outputs.containerAppsEnvironmentId.value -o tsv)
    
    # Get secrets
    POSTGRES_PASSWORD=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name postgres-admin-password --query value -o tsv)

    # RS256 JWT signing key (KS-180). base64-encoded PEM in Key Vault, injected
    # on the auth service only. Optional until provisioned (`./deploy.sh -e
    # <env> setup` generates it); when empty, bicep falls back to a sentinel and
    # auth keeps signing HS256 until KS-181 flips it to RS256.
    JWT_PRIVATE_KEY=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name jwt-private-key --query value -o tsv 2>/dev/null || echo "")
    JWT_KEY_ID=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name jwt-key-id --query value -o tsv 2>/dev/null || echo "")
    # KS-167/184: the PUBLIC key goes to EVERY service so verifiers can verify
    # RS256 (HS256 was dropped — verifiers fail CLOSED without it). Retry the
    # read: a transient KV blip here once silently emptied the key, leaving auth
    # signing RS256 while every verifier 401'd (a demo outage). Not a secret.
    JWT_PUBLIC_KEY=""
    for _try in 1 2 3; do
        JWT_PUBLIC_KEY=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name jwt-public-key --query value -o tsv 2>/dev/null || echo "")
        [ -n "$JWT_PUBLIC_KEY" ] && break
        sleep 2
    done
    if [ -z "$JWT_PRIVATE_KEY" ]; then
        log_warn "JWT signing keypair not yet in $KEY_VAULT_NAME (run 'setup')."
    fi
    # KS-184: RS256-only. If the signer's private key is present, the verifiers'
    # public key MUST be too — otherwise auth signs tokens no verifier can check
    # and every authed request 401s. Fail loud rather than ship a broken state.
    if [ -n "$JWT_PRIVATE_KEY" ] && [ -z "$JWT_PUBLIC_KEY" ]; then
        log_error "jwt-private-key present but jwt-public-key read EMPTY from $KEY_VAULT_NAME after 3 tries."
        log_error "Deploying would leave verifiers unable to verify any RS256 token (401 on every authed request). Aborting."
        exit 1
    fi
    if [ -n "$JWT_PRIVATE_KEY" ]; then
        log_info "JWT RS256 keypair loaded (kid=$JWT_KEY_ID); auth signs RS256, verifiers verify with the public key (KS-184 — HS256 removed)."
    fi

    # PII keys (required by auth/kyc/security/originate/tokenisation).
    # If missing, fail loud — running without them means login is broken
    # and the deploy is incomplete. Generate them via ./sync-secrets.sh.
    PII_ENCRYPTION_KEY=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name pii-encryption-key --query value -o tsv 2>/dev/null || echo "")
    PII_LOOKUP_HMAC_KEY=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name pii-lookup-hmac-key --query value -o tsv 2>/dev/null || echo "")
    if [ -z "$PII_ENCRYPTION_KEY" ] || [ -z "$PII_LOOKUP_HMAC_KEY" ]; then
        log_error "PII keys missing in $KEY_VAULT_NAME (pii-encryption-key, pii-lookup-hmac-key)."
        log_error "Run: ./sync-secrets.sh --non-interactive"
        exit 1
    fi
    PII_ENCRYPTION_KEY_VERSION=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name pii-encryption-key-version --query value -o tsv 2>/dev/null || echo "1")

    # M365 / Entra credentials for the m365-integration service. Optional —
    # if missing, the m365 container will start but Entra-backed features
    # (SharePoint/Outlook/Teams) are no-ops.
    ENTRA_TENANT_ID=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name entra-tenant-id --query value -o tsv 2>/dev/null || echo "")
    ENTRA_CLIENT_ID=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name entra-client-id --query value -o tsv 2>/dev/null || echo "")
    ENTRA_CLIENT_SECRET=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name entra-client-secret --query value -o tsv 2>/dev/null || echo "")
    SHAREPOINT_SITE_URL=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name sharepoint-site-url --query value -o tsv 2>/dev/null || echo "https://anupambaidyasecuura.sharepoint.com")
    API_PUBLIC_URL="https://${PROJECT_PREFIX}-api.${LOCATION}.azurecontainerapps.io"  # placeholder; bicep also wires from FQDN

    # Cardano anchoring credentials. Required on demo (SIMULATE_ANCHORING=false).
    # On dev these are still passed but the anchoring service ignores them
    # because originate runs SIMULATE_ANCHORING=true and never invokes the
    # real chain path.
    BLOCKFROST_API_KEY=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name blockfrost-api-key --query value -o tsv 2>/dev/null || echo "")
    PLATFORM_WALLET_MNEMONIC=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name platform-wallet-mnemonic --query value -o tsv 2>/dev/null || echo "")
    # H11 backup-storage secrets — optional (empty in dev where backups
    # aren't wired). When present, the originate service gets them as
    # env vars and the in-container backup.sh starts uploading nightly.
    BACKUP_STORAGE_ACCOUNT=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name backup-storage-account --query value -o tsv 2>/dev/null || echo "")
    BACKUP_STORAGE_CONTAINER=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name backup-storage-container --query value -o tsv 2>/dev/null || echo "db-backups")
    BACKUP_STORAGE_SAS_TOKEN=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name backup-storage-sas-token --query value -o tsv 2>/dev/null || echo "")
    if [ -n "$BACKUP_STORAGE_ACCOUNT" ] && [ -n "$BACKUP_STORAGE_SAS_TOKEN" ]; then
        log_info "Backup storage configured: $BACKUP_STORAGE_ACCOUNT/$BACKUP_STORAGE_CONTAINER"
    else
        log_warn "Backup storage NOT configured (no backup-storage-* secrets in $KEY_VAULT_NAME) — backups will be skipped at runtime"
    fi

    # ACS Email — optional. Provisioned 2026-04-29 in dev. Auto-detect by
    # presence of the ACS resource in this RG. The bicep listKeys() call
    # will fetch the connection string at deploy time, so we only need to
    # pass the resource name + sender address as params.
    ACS_RESOURCE_NAME=$(az resource list --resource-group $RESOURCE_GROUP --resource-type Microsoft.Communication/communicationServices --query "[0].name" -o tsv 2>/dev/null || echo "")
    ACS_SENDER_ADDRESS=""
    if [ -n "$ACS_RESOURCE_NAME" ]; then
        # Find the linked email-service domain and construct donotreply@...
        ACS_DOMAIN=$(az resource list --resource-group $RESOURCE_GROUP --resource-type Microsoft.Communication/emailServices --query "[0].name" -o tsv 2>/dev/null || echo "")
        if [ -n "$ACS_DOMAIN" ]; then
            ACS_FROM_DOMAIN=$(az communication email domain list --resource-group $RESOURCE_GROUP --email-service-name "$ACS_DOMAIN" --query "[0].properties.fromSenderDomain" -o tsv 2>/dev/null || echo "")
            if [ -n "$ACS_FROM_DOMAIN" ]; then
                ACS_SENDER_ADDRESS="donotreply@${ACS_FROM_DOMAIN}"
            fi
        fi
    fi
    if [ -n "$ACS_RESOURCE_NAME" ] && [ -n "$ACS_SENDER_ADDRESS" ]; then
        log_info "ACS Email configured: $ACS_RESOURCE_NAME (sender=$ACS_SENDER_ADDRESS)"
    else
        log_info "ACS Email NOT configured in $RESOURCE_GROUP — services will fall back to SMTP / no-op"
    fi
    
    # Get ACR password (from shared registry)
    ACR_PASSWORD=$(az acr credential show --name $ACTUAL_ACR_NAME --query passwords[0].value -o tsv)
    
    # Get PostgreSQL FQDN
    PG_FQDN=$(az deployment group show --resource-group $RESOURCE_GROUP --name "$INFRA_DEPLOYMENT" --query properties.outputs.postgresServerFqdn.value -o tsv)
    
    # Redis is now an in-env Redis Container App (services.bicep
    # `${PROJECT_PREFIX}-redis`), NOT managed "Azure Cache for Redis (classic)"
    # — Azure globally retired Microsoft.Cache/redis for new creates (KS Azure
    # migration). Reach it by SHORT NAME over plain redis:// (no TLS, no key):
    # internal-only TCP within the Container Apps environment. No bicep output /
    # az redis call to read.
    REDIS_URL="redis://${PROJECT_PREFIX}-redis:6379"

    # Build connection strings.
    # KS-109 (cutover DONE on dev + demo 2026-05-22): the runtime services connect
    # as the least-privilege secuura_app role (NOSUPERUSER, NOBYPASSRLS) so RLS
    # binds; the gateway keeps the admin/owner connection for migrations + the
    # secuura_app role provisioning via MIGRATION_* below. See RLS_ROLE_CUTOVER.md.

    ADMIN_DATABASE_URL="postgresql://secuuraadmin:${POSTGRES_PASSWORD}@${PG_FQDN}:5432/secuura?sslmode=require"
    # secuura_app role password (read first — the runtime URL below uses it). The
    # gateway's provisionAppRole sets the role to this same value.
    APP_DB_PASSWORD=$(az keyvault secret show --vault-name $KEY_VAULT_NAME --name secuura-app-db-password --query value -o tsv 2>/dev/null || echo "")
    # KS-207: route the runtime DATABASE_URL through the bounded pgbouncer Container
    # App (transaction pooling) so the ~22 services multiplex onto <=45 server
    # connections instead of exhausting max_connections=50 (pg 53300). pgbouncer is
    # reached by SHORT NAME (resolves in-env over TCP; no "azure" substring so the
    # app pools' pgSslConfig keeps the in-VNet app->pgbouncer leg plaintext) on 6432
    # and carries NO sslmode. pgbouncer->PG uses TLS. Migration + platform URLs stay
    # DIRECT on :5432 (transaction pooling breaks DDL/advisory-locks/session features).
    PGBOUNCER_HOST="${PROJECT_PREFIX}-pgbouncer"
    if [ -n "$APP_DB_PASSWORD" ]; then
        DATABASE_URL="postgresql://secuura_app:${APP_DB_PASSWORD}@${PGBOUNCER_HOST}:6432/secuura"
    else
        # Fallback (no KV secret yet): stay on admin-DIRECT so a first-time deploy
        # still works. The gateway then provisions the role; a re-run picks up
        # secuura_app + pgbouncer.
        DATABASE_URL="$ADMIN_DATABASE_URL"
    fi

    # Platform DB stays DIRECT. Pass it explicitly so bicep's replace()-derivation
    # off DATABASE_URL (now pgbouncer) doesn't route platform through pgbouncer.
    if [ -n "$APP_DB_PASSWORD" ]; then
        PLATFORM_DATABASE_URL="postgresql://secuura_app:${APP_DB_PASSWORD}@${PG_FQDN}:5432/secuura_platform?sslmode=require"
    else
        PLATFORM_DATABASE_URL="postgresql://secuuraadmin:${POSTGRES_PASSWORD}@${PG_FQDN}:5432/secuura_platform?sslmode=require"
    fi

    # Gateway-only admin/owner connection for migrations + secuura_app provisioning (DIRECT).
    MIGRATION_DATABASE_URL="$ADMIN_DATABASE_URL"
    MIGRATION_PLATFORM_DATABASE_URL="postgresql://secuuraadmin:${POSTGRES_PASSWORD}@${PG_FQDN}:5432/secuura_platform?sslmode=require"
    
    log_info "Deploying services Bicep template..."
    
    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --template-file "$SCRIPT_DIR/services.bicep" \
        --parameters environment=$ENVIRONMENT \
        --parameters location=$LOCATION \
        --parameters containerAppsEnvironmentId="$ENV_ID" \
        --parameters containerRegistryName="$ACTUAL_ACR_NAME" \
        --parameters acrPassword="$ACR_PASSWORD" \
        --parameters databaseUrl="$DATABASE_URL" \
        --parameters platformDatabaseUrl="$PLATFORM_DATABASE_URL" \
        --parameters migrationDatabaseUrl="$MIGRATION_DATABASE_URL" \
        --parameters migrationPlatformDatabaseUrl="$MIGRATION_PLATFORM_DATABASE_URL" \
        --parameters appDbPassword="$APP_DB_PASSWORD" \
        --parameters postgresHost="$PG_FQDN" \
        --parameters postgresAdminPassword="$POSTGRES_PASSWORD" \
        --parameters redisUrl="$REDIS_URL" \
        --parameters jwtPrivateKey="$JWT_PRIVATE_KEY" \
        --parameters jwtKeyId="$JWT_KEY_ID" \
        --parameters jwtPublicKey="$JWT_PUBLIC_KEY" \
        --parameters piiEncryptionKey="$PII_ENCRYPTION_KEY" \
        --parameters piiEncryptionKeyVersion="$PII_ENCRYPTION_KEY_VERSION" \
        --parameters piiLookupHmacKey="$PII_LOOKUP_HMAC_KEY" \
        --parameters entraTenantId="$ENTRA_TENANT_ID" \
        --parameters entraClientId="$ENTRA_CLIENT_ID" \
        --parameters entraClientSecret="$ENTRA_CLIENT_SECRET" \
        --parameters sharepointSiteUrl="$SHAREPOINT_SITE_URL" \
        --parameters apiPublicUrl="$API_PUBLIC_URL" \
        --parameters blockfrostApiKey="$BLOCKFROST_API_KEY" \
        --parameters platformWalletMnemonic="$PLATFORM_WALLET_MNEMONIC" \
        --parameters deploymentId="$DEPLOYMENT_ID" \
        --parameters imageTag="$IMAGE_TAG" \
        --parameters backupStorageAccount="$BACKUP_STORAGE_ACCOUNT" \
        --parameters backupStorageContainer="$BACKUP_STORAGE_CONTAINER" \
        --parameters backupStorageSasToken="$BACKUP_STORAGE_SAS_TOKEN" \
        --parameters acsResourceName="$ACS_RESOURCE_NAME" \
        --parameters acsSenderAddress="$ACS_SENDER_ADDRESS" \
        --parameters deployOutlookAddin=true \
        --parameters keyVaultName="$KEY_VAULT_NAME" \
        --name "secuura-services-$(date +%Y%m%d%H%M%S)"
    
    log_success "Microservices deployed."

    # Run post-deploy verification
    verify_deployment
}

# =============================================================================
# POST-DEPLOY VERIFICATION
# =============================================================================
verify_deployment() {
    log_info "Running post-deploy verification..."
    local ERRORS=0
    # KS-1054 / gate44 N-1346-2/-3/-4: a THIRD counter, because a check that did not RUN is neither a
    # pass nor a failure. ERRORS fails the deploy; SKIPS does not, but it stops the summary claiming a
    # clean run. See check-startup-migrations.sh's header for why the two must not be merged.
    local SKIPS=0

    # ── 1. Verify REDIS_URL is set on all backend services ──────────────────
    log_info "Checking REDIS_URL on all backend services..."
    local BACKEND_APPS=$(az containerapp list --resource-group $RESOURCE_GROUP \
        --query "[?!contains(name,'issuer') && !contains(name,'verifier') && !contains(name,'admin')].name" -o tsv 2>/dev/null)

    for APP in $BACKEND_APPS; do
        # Container Apps env vars are wired via either `value` (plaintext) or
        # `secretRef` (KV-style reference). Inspecting only `.value` false-
        # positives on secretRef-wired vars (services.bicep wires REDIS_URL
        # via secretRef), and the auto-fix below would then overwrite the
        # secretRef with a plaintext URL, downgrading secret hygiene every
        # deploy. Treat the env var as set if EITHER field is non-empty.
        REDIS_ENTRY=$(az containerapp show --name "$APP" --resource-group $RESOURCE_GROUP \
            --query "properties.template.containers[0].env[?name=='REDIS_URL'] | [0]" -o json 2>/dev/null)
        if [ -z "$REDIS_ENTRY" ] || [ "$REDIS_ENTRY" = "null" ] \
           || ! echo "$REDIS_ENTRY" | grep -qE '"value":[[:space:]]*"[^"]+"|"secretRef":[[:space:]]*"[^"]+"'; then
            log_warn "REDIS_URL is empty on $APP — fixing..."
            # Redis is the in-env Redis Container App (KS Azure migration) —
            # reached by short name over plain redis://, no managed-Redis host/key
            # to look up. The fallback URL is the same one the bicep deploy wires.
            local FIX_REDIS_URL="redis://${PROJECT_PREFIX}-redis:6379"
            az containerapp update --name "$APP" --resource-group $RESOURCE_GROUP \
                --set-env-vars "REDIS_URL=$FIX_REDIS_URL" --output none 2>/dev/null
            log_success "  Fixed REDIS_URL on $APP"
        fi
    done

    # ── 2. Verify frontend portals respond correctly ────────────────────────
    log_info "Checking frontend portals..."
    local PORTALS=("${PROJECT_PREFIX}-issuer" "${PROJECT_PREFIX}-admin" "${PROJECT_PREFIX}-verifier")

    for i in "${!PORTALS[@]}"; do
        local FQDN=$(az containerapp show --name "${PORTALS[$i]}" --resource-group $RESOURCE_GROUP \
            --query "properties.configuration.ingress.fqdn" -o tsv 2>/dev/null)
        if [ -n "$FQDN" ]; then
            local HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -L "https://${FQDN}" 2>/dev/null)
            local BODY=$(curl -s -L "https://${FQDN}" 2>/dev/null | head -5)
            if echo "$BODY" | grep -q "Welcome to nginx"; then
                log_error "  ${PORTALS[$i]}: serving default nginx page — image rebuild required"
                ERRORS=$((ERRORS + 1))
            else
                log_success "  ${PORTALS[$i]}: OK (HTTP $HTTP_CODE)"
            fi
        fi
    done

    # ── 3. Verify API health ────────────────────────────────────────────────
    log_info "Checking API gateway health..."
    local API_FQDN=$(az containerapp show --name "${PROJECT_PREFIX}-api" --resource-group $RESOURCE_GROUP \
        --query "properties.configuration.ingress.fqdn" -o tsv 2>/dev/null)
    if [ -n "$API_FQDN" ]; then
        local API_HEALTH=$(curl -s "https://${API_FQDN}/health" 2>/dev/null)
        if echo "$API_HEALTH" | grep -q '"healthy"'; then
            log_success "  API Gateway: healthy"
        else
            log_error "  API Gateway: unhealthy — $API_HEALTH"
            ERRORS=$((ERRORS + 1))
        fi

        # KS-1054 / N-1332-5 — startup migrations. A grep for "healthy" cannot see them:
        # /health deliberately stays 200 and healthy when a startup migration failed (Kam's
        # option (a)), so the count in the payload is the only signal. The shared predicate
        # keys on `failed`, never on `error` — a CORE statement failure is served as
        # `failed: N` with no `error` at all.
        # THREE-WAY, not a boolean. The predicate returns 0 = ran clean, 1 = FAILED, 2 = did not run
        # (an older image with no such field, an empty or non-JSON body, or ran:false). rc 2 must NOT
        # count an ERROR: failing closed there would block a ROLLBACK to an older image, which is
        # exactly the operation you need when a deploy has gone wrong. It must not count as a pass
        # either, which is what SKIPS is for.
        # `|| MIG_RC=$?` is load-bearing under `set -e` (:28): a bare non-zero call would abort the
        # script before this case could read the value.
        local MIG_RC=0
        "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/check-startup-migrations.sh" "$API_HEALTH" || MIG_RC=$?
        case "$MIG_RC" in
            0)
                ;;
            2)
                log_warn "  API Gateway: startup migration check SKIPPED — see above (not a clean run)"
                SKIPS=$((SKIPS + 1))
                ;;
            *)
                # rc 1 is a failed count OR a count that could not be read (python3 missing, a non-integer
                # `failed`), so this line must not claim the migrations were read (gate47 N-1350-7).
                log_error "  API Gateway: startup migrations FAILED or could not be verified — see above"
                ERRORS=$((ERRORS + 1))
                ;;
        esac
    fi

    # ── 4. Verify login works ───────────────────────────────────────────────
    log_info "Checking login ($ENVIRONMENT)..."
    if [ -n "$API_FQDN" ]; then
        # Both dev and demo use the seeded default passwords now that demo
        # explicitly opts in via ALLOW_DEFAULT_SEED_PASSWORDS=true (services.bicep).
        # Per-tenant overrides via DEMO_<TENANT>_PASSWORD env vars.
        local LOGIN_EMAIL="demo@secuura.io"
        local LOGIN_PASS="demo123"
        local LOGIN_RESP=$(curl -s "https://${API_FQDN}/api/auth/login" -X POST \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"${LOGIN_EMAIL}\",\"password\":\"${LOGIN_PASS}\"}" 2>/dev/null)
        if echo "$LOGIN_RESP" | grep -q '"success":true'; then
            log_success "  Demo login: working"
        else
            local LOGIN_ERR=$(echo "$LOGIN_RESP" | grep -o '"error":"[^"]*"' | head -1)
            log_error "  Demo login failed: $LOGIN_ERR"
            ERRORS=$((ERRORS + 1))
        fi
    fi

    # ── Summary ─────────────────────────────────────────────────────────────
    echo ""
    if [ $ERRORS -eq 0 ] && [ $SKIPS -eq 0 ]; then
        log_success "Post-deploy verification passed — all checks OK"
    elif [ $ERRORS -eq 0 ]; then
        # PASS-WITH-SKIP. The deploy step PASSES — that is the rollback rule — but it must not report
        # a clean run, because gate44 N-1346-3 measured exactly that: an ABSENT startupMigrations
        # field yielded "all checks OK" over a check that never ran. No `return`, so rc stays 0.
        log_warn "Post-deploy verification passed with $SKIPS check(s) SKIPPED — NOT a clean run"
    else
        log_error "Post-deploy verification found $ERRORS issue(s) — see above"
        # KS-1054 / gate44 N-1346-1. WITHOUT this return, the function's last command was
        # `log_error` — an echo — so verify_deployment exited 0 over failed startup migrations and
        # the deploy read as SUCCESSFUL. Kam's ruling (a) is explicit that "the deploy scripts'
        # existing /health checks … see it and THE DEPLOY READS AS FAILED"; deploy-all.sh already
        # does that (`exit 1` on a failed smoke test), and this script did not.
        # One `return` is the whole fix: this file runs under `set -euo pipefail` (:28), and
        # verify_deployment is called UNCHECKED at both call sites — as deploy_services' last
        # command, and directly in the `verify)` branch — so a non-zero return aborts the script
        # with that status at either. No call site needs editing, and adding `|| exit 1` at them
        # would be a second, redundant path to the same outcome.
        return 1
    fi
}

# =============================================================================
# SHOW STATUS
# =============================================================================
show_status() {
    log_info "Checking deployment status for $RESOURCE_GROUP..."
    
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}                         DEPLOYMENT STATUS                              ${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${BLUE}Resource Group:${NC} $RESOURCE_GROUP"
    echo -e "${BLUE}Deployment ID:${NC} $DEPLOYMENT_ID"
    echo ""
    
    echo -e "${YELLOW}Virtual Network:${NC}"
    az network vnet show --resource-group $RESOURCE_GROUP --name "${PROJECT_PREFIX}-vnet" --query "{Name:name,AddressSpace:addressSpace.addressPrefixes[0],Subnets:subnets[].name}" -o table 2>/dev/null || echo "  Not deployed"
    echo ""
    
    echo -e "${YELLOW}Container Apps:${NC}"
    az containerapp list --resource-group $RESOURCE_GROUP --query "[].{Name:name,Status:properties.runningStatus,URL:properties.configuration.ingress.fqdn}" -o table 2>/dev/null || echo "  No container apps found"
    echo ""
    
    echo -e "${YELLOW}PostgreSQL Server:${NC}"
    az postgres flexible-server show --resource-group $RESOURCE_GROUP --name "${PROJECT_PREFIX}-pg" --query "{Name:name,State:state,FQDN:fullyQualifiedDomainName}" -o table 2>/dev/null || echo "  Not deployed"
    echo ""
    
    echo -e "${YELLOW}Redis (in-env Container App):${NC}"
    # Redis is now a Container App (KS Azure migration), not managed "Azure Cache
    # for Redis (classic)" — show the container app, not `az redis show`.
    az containerapp show --resource-group $RESOURCE_GROUP --name "${PROJECT_PREFIX}-redis" --query "{Name:name,Status:properties.runningStatus,Host:properties.configuration.ingress.fqdn}" -o table 2>/dev/null || echo "  Not deployed"
    echo ""
    
    echo -e "${YELLOW}Storage Account:${NC}"
    az storage account list --resource-group $RESOURCE_GROUP --query "[].{Name:name,Status:provisioningState}" -o table 2>/dev/null || echo "  Not deployed"
    echo ""
    
    echo -e "${YELLOW}Container Registry (shared):${NC}"
    az acr show --name "$SHARED_ACR_NAME" --query "{Name:name,LoginServer:loginServer}" -o table 2>/dev/null || echo "  Not deployed"
    echo ""
    
    # Show API Gateway URL if available
    API_URL=$(az containerapp show --name "${PROJECT_PREFIX}-api" --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv 2>/dev/null || echo "")
    if [ -n "$API_URL" ]; then
        echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  API Gateway: https://$API_URL${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════${NC}"
    fi
}

# =============================================================================
# DESTROY ALL RESOURCES
# =============================================================================
destroy_resources() {
    log_warn "This will DELETE ALL Secuura '$ENVIRONMENT' resources!"
    echo ""
    echo "  Environment:    $ENVIRONMENT"
    echo "  Resource Group: $RESOURCE_GROUP"
    echo "  Deployment ID:  $DEPLOYMENT_ID"
    echo ""

    if [ "$ENVIRONMENT" = "demo" ]; then
        log_warn "⚠  You are about to destroy the DEMO/PRODUCTION environment!"
        log_warn "   This contains live demo data. Are you absolutely sure?"
        echo ""
        read -p "Type 'destroy demo' to confirm: " CONFIRM
        [ "$CONFIRM" != "destroy demo" ] && { log_info "Cancelled."; return; }
    else
        read -p "Are you sure? Type 'yes' to confirm: " CONFIRM
        [ "$CONFIRM" != "yes" ] && { log_info "Cancelled."; return; }
    fi

    log_info "Deleting resource group $RESOURCE_GROUP..."
    # Note: shared ACR lives in secuura-demo-rg and is NOT deleted when destroying dev
    az group delete --name $RESOURCE_GROUP --yes --no-wait
    log_success "Deletion initiated. Resources will be removed in the background."
}

# =============================================================================
# MAIN
# =============================================================================
case "${1:-full}" in
    setup)
        check_azure
        create_resource_group
        ensure_kv_access
        setup_keyvault
        deploy_infrastructure
        ;;
    build)
        check_azure
        build_images
        ;;
    deploy)
        check_azure
        ensure_kv_access
        deploy_services
        ;;
    services)
        check_azure
        ensure_kv_access
        deploy_services
        ;;
    status)
        check_azure
        show_status
        ;;
    destroy)
        check_azure
        destroy_resources
        ;;
    verify)
        check_azure
        verify_deployment
        ;;
    full)
        check_azure
        create_resource_group
        ensure_kv_access
        setup_keyvault
        deploy_infrastructure
        build_images
        ensure_kv_access
        deploy_services
        show_status
        ;;
    *)
        echo "Usage: $0 [-e dev|demo] {setup|build|deploy|services|status|verify|destroy|full}"
        echo ""
        echo "Environments:"
        echo "  -e dev    - Development environment (secuura-dev-rg, :latest tags)"
        echo "  -e demo   - Demo/production environment (secuura-demo-rg, date-pinned tags)"
        echo "  Default: demo"
        echo ""
        echo "Commands:"
        echo "  setup     - Create resource group, Key Vault, and infrastructure"
        echo "  build     - Build and push Docker images to ACR (shared between environments)"
        echo "  deploy    - Deploy microservices to Container Apps"
        echo "  services  - Same as deploy"
        echo "  status    - Show current deployment status"
        echo "  verify    - Run post-deploy verification checks"
        echo "  destroy   - Delete all resources for the selected environment"
        echo "  full      - Run complete deployment (setup + build + deploy)"
        echo ""
        echo "Examples:"
        echo "  $0 build                  # Build images (shared ACR)"
        echo "  $0 -e dev setup           # Create dev infrastructure"
        echo "  $0 -e dev services        # Deploy services to dev environment"
        echo "  $0 -e demo services       # Deploy services to demo/production"
        echo "  SECUURA_ENV=dev $0 status  # Check dev status via env var"
        exit 1
        ;;
esac
