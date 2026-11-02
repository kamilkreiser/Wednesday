#!/bin/bash
# =============================================================================
# SECUURA LOCAL DEVELOPMENT STARTUP SCRIPT
# =============================================================================
# This script starts the complete local development environment.
#
# Usage:
#   ./scripts/start-local.sh           # Start all services
#   ./scripts/start-local.sh infra     # Start only infrastructure
#   ./scripts/start-local.sh services  # Start only application services
#   ./scripts/start-local.sh stop      # Stop all services
#   ./scripts/start-local.sh logs      # Follow all logs
#   ./scripts/start-local.sh status    # Show service status
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║            SECUURA LOCAL DEVELOPMENT ENVIRONMENT              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check for .env file
# KS-731: `cp .env.local .env` copies whatever passwords that file carries --
# which, for a clone that took .env.local from the example, are the committed
# shared literals. bootstrap-env.sh is the path that generates PER-CLONE
# credentials, so it is preferred; the copy remains as the fallback for a
# developer who keeps a hand-maintained .env.local.
SCRIPT_DIR_KS731="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -f .env ]; then
    if [ -x "$SCRIPT_DIR_KS731/bootstrap-env.sh" ]; then
        echo -e "${YELLOW}No .env file found. Running bootstrap-env.sh so this clone gets"
        echo -e "its OWN datastore credentials rather than the shared committed ones.${NC}"
        "$SCRIPT_DIR_KS731/bootstrap-env.sh"
    elif [ -f .env.local ]; then
        echo -e "${YELLOW}No .env file found. Creating from .env.local...${NC}"
        cp .env.local .env
        echo -e "${GREEN}Created .env from .env.local${NC}"
    else
        echo -e "${RED}Error: No .env.local file found!${NC}"
        exit 1
    fi
fi

# KS-731: an EXISTING clone still carries the shared literal, because bootstrap
# only fills a blank value -- deliberately, so a pull never breaks a running
# stack. Non-blocking for the same reason Kam ruled the compose fallbacks stay
# (KS-762): blocking would stop exactly the stacks that ruling protects.
# SECUURA_STRICT_CREDENTIAL_CHECK=1 makes it refuse.
if ! "$SCRIPT_DIR_KS731/check-slot-credentials.sh"; then
    if [ "${SECUURA_STRICT_CREDENTIAL_CHECK:-}" = "1" ]; then
        echo -e "${RED}Refusing to start: SECUURA_STRICT_CREDENTIAL_CHECK=1 and this clone"
        echo -e "shares its datastore credentials (see above).${NC}"
        exit 1
    fi
    echo -e "${YELLOW}Continuing anyway — the stack starts, but it is reachable from other"
    echo -e "slots on this machine. The remedy is printed above.${NC}"
    echo ""
fi

# KS-762 (QA F-800-01): the APP_DB_PASSWORD sibling, wired the SAME way.
#
# It shipped 164 lines and was invoked by NOTHING — a whole-tree grep found two
# hits, both prose in .env.example and env.example — while the credential
# checker above was wired into both start scripts in the same commit. So the
# non-blocking pattern was available and simply unused.
#
# That is F-731-01 recurring INSIDE the PR that closes F-731-01: a fix that does
# not reach is a fix nobody has. Wiring it is the whole remedy.
#
# It exits 0 in today's HELD state, so this is normally silent. It fails only on
# an INCOHERENT tree — both `:-` and `:?` forms present (a half-applied switch,
# where some services demand the variable and others fall back, so the stack
# half-starts on two different passwords), or neither form anywhere. Those are
# real defects rather than "this clone shares a password", which is why the
# message below says something different from its sibling's.
if ! "$SCRIPT_DIR_KS731/check-app-db-password-default.sh"; then
    if [ "${SECUURA_STRICT_CREDENTIAL_CHECK:-}" = "1" ]; then
        echo -e "${RED}Refusing to start: SECUURA_STRICT_CREDENTIAL_CHECK=1 and the"
        echo -e "APP_DB_PASSWORD configuration is incoherent (see above).${NC}"
        exit 1
    fi
    echo -e "${YELLOW}Continuing anyway — but the APP_DB_PASSWORD configuration above is"
    echo -e "INCOHERENT, not merely permissive. A half-applied switch starts some"
    echo -e "services on the variable and others on the committed literal.${NC}"
    echo ""
fi

# Load environment
source .env

# -----------------------------------------------------------------------------
# KS-1355 spot 2b: derive this slot's ports, project and container prefix
# -----------------------------------------------------------------------------
# This script brings the PLATFORM stack up and did not source stack_env.sh, so from a
# slot-N worktree it drove slot 1's compose project, stamped `unknown` ownership markers
# on anything it created (the KS-1011 mechanism), and printed slot 1's URLs whatever the
# slot. start-secuura.sh and stop-secuura.sh have shared this derivation since KS-666;
# nothing made this one comply, because check-stack-safety.sh enforced the source for
# those two only. It now covers every platform launcher.
#
# Sourced AFTER `source .env` deliberately. stack_env.sh assigns the ports
# unconditionally, so sourcing it second makes the SLOT authoritative over a value a
# clone happens to carry in .env — and the exported value is also what Compose itself
# resolves first (it prefers the shell over .env; see KS-785). Sourcing it before .env
# would let a stale literal in .env silently win, which is the defect, not the fix.
#
# stack_env.sh's contract is PROJECT_ROOT = the REPO root, while this script's own
# PROJECT_ROOT is Blockchain/Dev (it cd's there at the top and uses it for sibling
# paths). Set it for the source only and restore it, so neither contract is bent.
# A malformed or out-of-range slot makes stack_env.sh print the reason and exit 2 —
# refusing, rather than falling back to slot 1 and tearing into another ticket's stack.
_sl_dev_dir="$PROJECT_ROOT"
PROJECT_ROOT="$(cd "$_sl_dev_dir/../.." && pwd)"
export PROJECT_ROOT
# shellcheck source=stack_env.sh
source "$_sl_dev_dir/scripts/stack_env.sh"
PROJECT_ROOT="$_sl_dev_dir"

# Functions
start_infrastructure() {
    echo -e "${BLUE}Starting infrastructure services...${NC}"
    docker compose up -d postgres redis
    
    echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
    until docker compose exec -T postgres pg_isready -U $POSTGRES_USER > /dev/null 2>&1; do
        sleep 1
    done
    echo -e "${GREEN}PostgreSQL is ready!${NC}"
    
    echo -e "${YELLOW}Waiting for Redis to be ready...${NC}"
    until docker compose exec -T redis redis-cli ping > /dev/null 2>&1; do
        sleep 1
    done
    echo -e "${GREEN}Redis is ready!${NC}"
}

start_cardano() {
    echo -e "${BLUE}Starting Cardano local devnet...${NC}"
    docker compose --profile devnet up -d cardano-devnet
    echo -e "${YELLOW}Cardano devnet starting (may take 60s)...${NC}"
}

start_services() {
    echo -e "${BLUE}Starting application services...${NC}"
    docker compose up -d \
        api-gateway \
        originate \
        wallet-connector \
        auth \
        prism \
        timestamping \
        anchoring \
        security \
        m365-integration \
        vc-issuer \
        staking \
        referral \
        transfer \
        kyc \
        analytics \
        billing \
        governance \
        nft-certificate \
        tokenisation \
        tenant-provisioning \
        mcp-server

    echo -e "${YELLOW}Waiting for new services to become healthy...${NC}"
    local MAX_WAIT=60
    local WAITED=0
    while [ $WAITED -lt $MAX_WAIT ]; do
        local ALL_UP=true
        for svc in tokenisation tenant-provisioning mcp-server; do
            if ! docker compose ps "$svc" 2>/dev/null | grep -q "Up"; then
                ALL_UP=false
                break
            fi
        done
        if [ "$ALL_UP" = true ]; then
            echo -e "${GREEN}All services are up!${NC}"
            break
        fi
        sleep 3
        WAITED=$((WAITED + 3))
    done
    if [ $WAITED -ge $MAX_WAIT ]; then
        echo -e "${YELLOW}Warning: Some services may still be starting...${NC}"
    fi
}

start_frontends() {
    echo -e "${BLUE}Starting frontend applications...${NC}"
    docker compose up -d \
        issuer-frontend \
        verifier-frontend \
        admin-frontend \
        status-frontend \
        website-frontend \
        nginx-gateway
}

start_monitoring() {
    # Observability is a standalone stack (KS-200) — started only from
    # observability/, by nothing else. This platform script does not start it.
    echo -e "${BLUE}Observability is a standalone stack — start it with:${NC}"
    echo -e "  cd observability && npm run start"
}

stop_all() {
    echo -e "${YELLOW}Stopping all services...${NC}"
    docker compose --profile devnet down
    echo -e "${GREEN}All services stopped.${NC}"
}

show_status() {
    echo -e "${BLUE}Service Status:${NC}"
    docker compose ps
}

show_logs() {
    docker compose logs -f
}

show_urls() {
    # KS-1355: from stack_env.sh's exports. The ${VAR:-historic} fallback keeps this
    # function correct if it is ever reached without the source above.
    local GW="${GATEWAY_PORT:-6882}"
    local WEB="${WEBSITE_PORT:-6881}"
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}                    SERVICE URLs                               ${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    # KS-1355: the slot's own gateway, not slot 1's. GW/WEB are set just below.
    echo -e "  ${BLUE}Platform Gateway (port ${GW}):${NC}"
    echo "    Issuer Portal:     http://localhost:${GW}/"
    echo "    Verifier Portal:   http://localhost:${GW}/verify/"
    echo "    Admin Dashboard:   http://localhost:${GW}/admin/"
    echo "    Status Page:       http://localhost:${GW}/status/"
    echo "    Website:           http://localhost:${GW}/website/"
    echo "    API Gateway:       http://localhost:${GW}/api/"
    echo "    API Docs:          http://localhost:${GW}/api/docs"
    echo "    Health Check:      http://localhost:${GW}/health"
    echo ""
    echo -e "  ${BLUE}Direct Access:${NC}"
    echo "    Marketing Website: http://localhost:${WEB}"
    echo ""
    echo -e "  ${BLUE}Vite Dev Servers (for hot-reload development):${NC}"
    echo "    Issuer Portal:     http://localhost:6100"
    echo "    Verifier Portal:   http://localhost:6101"
    echo "    Admin Dashboard:   http://localhost:6102"
    echo "    Website:           http://localhost:6103"
    echo ""
    echo -e "  ${BLUE}Multi-Tenancy & AI Services:${NC}"
    echo "    Tokenisation:      http://localhost:6021"
    echo "    Tenant Prov.:      http://localhost:6022"
    echo "    MCP Server:        http://localhost:6023"
    echo ""
    echo -e "  ${BLUE}Infrastructure:${NC}"
    # KS-731: the slot's own ports, not slot 1's. See start-environment.sh.
    echo "    PostgreSQL:        localhost:${POSTGRES_EXTERNAL_PORT:-6432}"
    echo "    Redis:             localhost:${REDIS_EXTERNAL_PORT:-6379}"
    echo "    Cardano Devnet:    http://localhost:6092"
    echo ""
    echo -e "  ${BLUE}Monitoring:${NC}"
    echo "    Grafana:           http://localhost:6300 (admin/secuura_grafana)"
    echo "    Prometheus:        http://localhost:6301"
    echo ""
    echo -e "  ${BLUE}Demo Credentials:${NC}"
    echo "    Issuer:  demo@secuura.io  / demo123"
    echo "    Admin:   admin@secuura.com / admin123"
    echo ""
}

# Main command handler
case "${1:-all}" in
    infra|infrastructure)
        start_infrastructure
        ;;
    cardano)
        start_cardano
        ;;
    services)
        start_services
        ;;
    frontends)
        start_frontends
        ;;
    monitoring)
        start_monitoring
        ;;
    all)
        start_infrastructure
        start_services
        start_frontends
        show_urls
        ;;
    full)
        start_infrastructure
        start_cardano
        start_services
        start_frontends
        show_urls
        ;;
    stop)
        stop_all
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    urls)
        show_urls
        ;;
    *)
        echo "Usage: $0 {all|full|infra|cardano|services|frontends|monitoring|stop|status|logs|urls}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Done!${NC}"
