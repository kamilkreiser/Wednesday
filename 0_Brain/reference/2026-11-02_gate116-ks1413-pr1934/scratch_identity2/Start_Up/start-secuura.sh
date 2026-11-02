#!/usr/bin/env bash
# =============================================================================
# SECUURA PLATFORM — AUTOMATED STARTUP SCRIPT
# =============================================================================
# Checks Docker, launches all containers, waits for health, and verifies
# that every service, portal, and API endpoint is operational.
#
# Usage:
#   ./Start_Up/start-secuura.sh          # Normal start
#   ./Start_Up/start-secuura.sh --rebuild # Force rebuild all containers
#   ./Start_Up/start-secuura.sh --quick   # Skip post-start verification
#   ./Start_Up/start-secuura.sh --stop    # Stop all containers (keeps volumes)
#   ./Start_Up/start-secuura.sh --fresh-db # Stop, DESTROY volumes, start clean
#   ./Start_Up/start-secuura.sh --status  # Show status only (no start)
#
# KS-666 — SHARED-STACK SAFETY:
# The VM hosts one shared, mutable stack. Every destructive path below now runs
# scripts/stack_guard.sh first, which refuses to proceed when the running stack
# belongs to someone else or the working tree has uncommitted tracked changes.
# Before KS-666 the fresh-DB recovery path was hand-typed (`docker compose
# down -v` + `git checkout develop`) and checked none of that; it destroyed
# other people's checkouts, volumes and uncommitted work silently, and reported
# success. `--fresh-db` exists so that path is a named, guarded operation
# instead of an unguarded reflex.
#
# KS-666 — STACK SLOTS (isolation):
# SECUURA_STACK_SLOT selects an isolated stack. Slot 1 (the default) is the
# primary stack and binds exactly the ports it always has, so nothing that
# hardcodes 6882 breaks. Slot N>1 offsets every published port by 100*(N-1)
# and uses its own compose project name, so its volumes and containers are
# namespaced and a `--fresh-db` of one slot cannot reach another's data.
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
COMPOSE_FILE="$PROJECT_ROOT/docker-compose.local.yml"
STACK_GUARD="$PROJECT_ROOT/Blockchain/Dev/scripts/stack_guard.sh"

# -----------------------------------------------------------------------------
# KS-666: stack slot, ports, project and ownership stamp
# -----------------------------------------------------------------------------
# Shared with stop-secuura.sh so both resolve the SAME compose project for a
# given slot. See Blockchain/Dev/scripts/stack_env.sh for why this is not
# duplicated.
# shellcheck source=../Blockchain/Dev/scripts/stack_env.sh
source "$PROJECT_ROOT/Blockchain/Dev/scripts/stack_env.sh"
MAX_HEALTH_WAIT=120  # seconds to wait for all containers to become healthy
HEALTH_POLL=5        # seconds between health polls

# Colours
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Expected services (27 total — secuura-midnight removed in the KS-312 cut)
# KS-1096: these are SUFFIXES, prefixed with STACK_PREFIX below. They used to be
# slot 1's bare names (`secuura-postgres`, ...), while docker-compose.local.yml
# names every container `${STACK_PREFIX}-<svc>` — `secuura-sN-<svc>` on slot N.
# So on slots 2-4 every `docker inspect` here missed, the health wait ran the
# full MAX_HEALTH_WAIT for nothing, `--status` reported 27 × "not found", and
# the DB/Redis probes below printed a healthy stack as down (exit 0 throughout).
EXPECTED_SUFFIXES=(
  postgres redis
  api-gateway nginx-gateway
  originate auth wallet-connector
  anchoring timestamping prism security
  kyc m365-integration
  analytics vc-issuer nft-certificate
  staking referral governance
  billing transfer
  issuer-frontend verifier-frontend
  admin-frontend status-frontend
  website-frontend tokenomics-website
)
# Derived once, after stack_env.sh (sourced above) has exported STACK_PREFIX —
# `secuura` on slot 1, so slot 1's names are byte-identical to before. Filled
# before it is ever expanded: bash 3.2 under `set -u` rejects "${arr[@]}" on an
# empty array (see the KS-321 note in the health-wait timeout diagnostic).
EXPECTED_SERVICES=()
for _suffix in "${EXPECTED_SUFFIXES[@]}"; do
  EXPECTED_SERVICES+=("${STACK_PREFIX}-${_suffix}")
done
unset _suffix

PORTALS=(
  "Issuer Portal|http://localhost:$GATEWAY_PORT/"
  "Verifier Portal|http://localhost:$GATEWAY_PORT/verify/"
  "Admin Portal|http://localhost:$GATEWAY_PORT/admin/"
  "Status Page|http://localhost:$GATEWAY_PORT/status/"
  "Website|http://localhost:$GATEWAY_PORT/website/"
  "Tokenomics|http://localhost:$TOKENOMICS_PORT/"
)

# Parse arguments
REBUILD=false
QUICK=false
STOP_ONLY=false
STATUS_ONLY=false
FRESH_DB=false
# KS-666: forwarded verbatim to stack_guard.sh. Deliberately verbose and
# logged — overriding another developer's stack should be uncomfortable to
# type and attributable afterwards.
GUARD_OVERRIDE=""

for arg in "$@"; do
  case "$arg" in
    --rebuild) REBUILD=true ;;
    --quick)   QUICK=true ;;
    --stop)    STOP_ONLY=true ;;
    --status)  STATUS_ONLY=true ;;
    --fresh-db) FRESH_DB=true ;;
    --i-have-confirmed-with-the-owner) GUARD_OVERRIDE="$arg" ;;
    --help|-h)
      echo "Usage: $0 [--rebuild] [--quick] [--stop] [--fresh-db] [--status]"
      echo ""
      echo "  --rebuild  Force rebuild all containers before starting"
      echo "  --quick    Skip post-start verification checks"
      echo "  --stop     Stop all containers and exit (volumes are KEPT)"
      echo "  --fresh-db Stop, DESTROY all volumes, then start clean"
      echo "  --status   Show current status without starting anything"
      echo ""
      echo "  --i-have-confirmed-with-the-owner"
      echo "             Override the KS-666 shared-stack guard. Only legitimate"
      echo "             when you have actually spoken to the owner named in the"
      echo "             refusal. Logged and attributable."
      echo ""
      echo "Environment:"
      echo "  SECUURA_STACK_SLOT  Isolated stack slot (default 1). Slot 1 keeps the"
      echo "                      historic ports; slot N offsets them by 100*(N-1)"
      echo "                      and namespaces its own project, volumes and names."
      exit 0
      ;;
  esac
done

# -----------------------------------------------------------------------------
# KS-666: shared-stack guard
# -----------------------------------------------------------------------------
# Called before anything that destroys state. Exit 1 means blocked; we stop
# rather than continue, because the whole point is that the destructive path
# should not proceed on momentum.
run_stack_guard() {
  local what="$1"
  if [[ ! -x "$STACK_GUARD" ]]; then
    echo "ERROR: stack guard not found or not executable: $STACK_GUARD" >&2
    echo "       Refusing to ${what} unguarded (KS-666)." >&2
    exit 2
  fi
  echo ""
  echo "[secuura] KS-666 stack guard — checking before: ${what}"
  if ! REPO_ROOT="$PROJECT_ROOT" "$STACK_GUARD" ${GUARD_OVERRIDE:+"$GUARD_OVERRIDE"}; then
    echo "" >&2
    echo "Refusing to ${what}." >&2
    exit 1
  fi
}

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
log()     { echo -e "${CYAN}[secuura]${NC} $1"; }
success() { echo -e "${GREEN}  ✓${NC} $1"; }
warn()    { echo -e "${YELLOW}  ⚠${NC} $1"; }
fail()    { echo -e "${RED}  ✗${NC} $1"; }
header()  { echo -e "\n${BOLD}━━━ $1 ━━━${NC}"; }

# -----------------------------------------------------------------------------
# KS-666 phase 4: lease visibility
# -----------------------------------------------------------------------------
# Announces who took or released the shared stack. Weaker than the label guard —
# it only fires when the scripts are used — but it covers the case the guard
# cannot see: someone about to start work who wants to know the stack is busy
# WITHOUT having to run a destructive command to find out.
#
# Deliberately NOT a lock service. A lock service adds a stale-lock failure mode
# of its own, and the container labels plus per-slot project namespacing already
# make one redundant (KS-666).
#
# Always best-effort: announcing must never be able to fail a stack start.
announce_lease() {
  local action="$1"
  local line
  line="$(printf '%s slot=%s owner=%s branch=%s commit=%s at=%s host=%s' \
    "$action" "$SECUURA_STACK_SLOT" "$STACK_OWNER" "$STACK_BRANCH" \
    "$STACK_COMMIT" "$STACK_STARTED_AT" "$(hostname -s 2>/dev/null || echo unknown)")"

  # Local ledger first — always available, and the thing you can actually read
  # over SSH when you are wondering who has the stack.
  {
    mkdir -p "$PROJECT_ROOT/.secuura" 2>/dev/null &&
      printf '%s\n' "$line" >>"$PROJECT_ROOT/.secuura/stack-lease.log"
  } 2>/dev/null || true

  # Optional team-channel notification. Unset by default so nothing is posted
  # anywhere until someone deliberately configures a webhook.
  if [[ -n "${SECUURA_LEASE_WEBHOOK_URL:-}" ]]; then
    curl -fsS -m 5 -X POST -H 'Content-Type: application/json' \
      --data "$(printf '{"text":"secuura stack %s"}' "$line")" \
      "$SECUURA_LEASE_WEBHOOK_URL" >/dev/null 2>&1 || true
  fi
}

check_http() {
  local url="$1"
  # KS-260: optional retry window. A container can report `healthy` a beat
  # before its HTTP server finishes binding, so a single probe races startup
  # (the Tokenomics false-negative). Callers that want a grace period pass a
  # retry count; default 1 keeps existing single-shot callers unchanged.
  local retries="${2:-1}"
  local delay="${3:-2}"
  local code attempt
  for ((attempt = 1; attempt <= retries; attempt++)); do
    code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "$url" 2>/dev/null || echo "000")
    if [[ "$code" =~ ^(200|301|302)$ ]]; then
      return 0
    fi
    [[ "$attempt" -lt "$retries" ]] && sleep "$delay"
  done
  return 1
}

# -----------------------------------------------------------------------------
# Phase 0: Pre-flight checks
# -----------------------------------------------------------------------------
header "Pre-flight Checks"

# Docker running?
if ! docker info >/dev/null 2>&1; then
  fail "Docker is not running. Please start Docker Desktop and try again."
  exit 1
fi
success "Docker is running"

# Compose file exists?
if [[ ! -f "$COMPOSE_FILE" ]]; then
  fail "Compose file not found: $COMPOSE_FILE"
  exit 1
fi
success "Compose file found"

# Check disk space (warn if < 5GB free)
FREE_GB=$(df -g "$PROJECT_ROOT" 2>/dev/null | tail -1 | awk '{print $4}' || echo "unknown")
if [[ "$FREE_GB" != "unknown" && "$FREE_GB" -lt 5 ]]; then
  warn "Low disk space: ${FREE_GB}GB free (recommend 5GB+)"
else
  success "Disk space OK (${FREE_GB}GB free)"
fi

# Check required ports are not blocked by non-Secuura processes
# KS-1096: Postgres/Redis were the slot-1 literals 6432/6379 while the other
# three were already slot-derived, so on slot N this checked ports the stack
# does not bind. stack_env.sh exports the per-slot values.
for port in $GATEWAY_PORT $TOKENOMICS_PORT $WEBSITE_PORT $POSTGRES_EXTERNAL_PORT $REDIS_EXTERNAL_PORT; do
  PID=$(lsof -ti :$port 2>/dev/null | head -1 || true)
  if [[ -n "$PID" ]]; then
    PROC=$(ps -p "$PID" -o comm= 2>/dev/null || echo "unknown")
    if [[ "$PROC" != *"com.docker"* && "$PROC" != "com.docke"* && "$PROC" != "docker"* && "$PROC" != "vpnkit"* && "$PROC" != *"Docker"* ]]; then
      warn "Port $port in use by $PROC (PID $PID) — may conflict"
    fi
  fi
done
success "Key ports available"

# -----------------------------------------------------------------------------
# Handle --stop
# -----------------------------------------------------------------------------
if $STOP_ONLY; then
  # KS-666: guarded even though `down` keeps volumes — stopping someone else's
  # stack mid-run still destroys their work in progress, just less permanently.
  run_stack_guard "stop the stack"
  header "Stopping All Services"
  # No `-v`. Volume destruction is only ever reached via the explicit
  # --fresh-db path below, so it can never be a reflex.
  docker compose -f "$COMPOSE_FILE" down 2>&1 | tail -5
  success "All containers stopped (volumes kept — use --fresh-db to destroy them)"
  announce_lease "stopped"
  exit 0
fi

# -----------------------------------------------------------------------------
# KS-666: Handle --fresh-db (the only path that destroys volumes)
# -----------------------------------------------------------------------------
if $FRESH_DB; then
  run_stack_guard "DESTROY all volumes for project '${COMPOSE_PROJECT_NAME:-<compose default>}'"
  header "Fresh Database — Destroying Volumes"
  warn "This destroys ALL database and seeded state for this stack slot."
  docker compose -f "$COMPOSE_FILE" down -v 2>&1 | tail -10
  success "Volumes destroyed — continuing with a clean start"
fi

# -----------------------------------------------------------------------------
# Handle --status (no start)
# -----------------------------------------------------------------------------
if $STATUS_ONLY; then
  header "Container Status"
  
  running=0
  healthy=0
  unhealthy=0
  stopped=0
  
  for svc in "${EXPECTED_SERVICES[@]}"; do
    status=$(docker inspect --format='{{.State.Status}}' "$svc" 2>/dev/null || echo "not_found")
    health=$(docker inspect --format='{{.State.Health.Status}}' "$svc" 2>/dev/null || echo "none")
    
    if [[ "$status" == "running" ]]; then
      running=$((running + 1))
      if [[ "$health" == "healthy" ]]; then
        healthy=$((healthy + 1))
        success "$svc — running (healthy)"
      elif [[ "$health" == "unhealthy" ]]; then
        unhealthy=$((unhealthy + 1))
        warn "$svc — running (unhealthy)"
      else
        success "$svc — running"
      fi
    elif [[ "$status" == "not_found" ]]; then
      stopped=$((stopped + 1))
      fail "$svc — not found"
    else
      stopped=$((stopped + 1))
      fail "$svc — $status"
    fi
  done
  
  header "Portal Accessibility"
  for entry in "${PORTALS[@]}"; do
    IFS='|' read -r name url <<< "$entry"
    if check_http "$url"; then
      success "$name ($url)"
    else
      fail "$name ($url) — not reachable"
    fi
  done
  
  echo ""
  log "Containers: ${running}/${#EXPECTED_SERVICES[@]} running, ${healthy} healthy, ${unhealthy} unhealthy, ${stopped} stopped"
  exit 0
fi

# -----------------------------------------------------------------------------
# Phase 0.5: Ensure environment (.env + required keys)
# -----------------------------------------------------------------------------
# KS-307: the RS256 JWT cutover (KS-167/184) made the signing keypair mandatory.
# auth fails fast without JWT_PRIVATE_KEY, which cascades — api-gateway's
# /health/ready probes auth, so the gateway reports unhealthy and every
# dependent container aborts. A .env that predates the cutover has no keypair,
# so a plain `--rebuild` breaks with exactly that symptom. bootstrap-env.sh is
# idempotent (only fills blanks: JWT keypair + PII keys, creating .env/.env.local
# from the examples if absent), so running it here self-heals a stale .env while
# leaving any values you've already set untouched.
header "Ensuring Environment"
BOOTSTRAP="$PROJECT_ROOT/Blockchain/Dev/scripts/bootstrap-env.sh"
if [[ -f "$BOOTSTRAP" ]]; then
  # KS-600: `mktemp -t PREFIX` is NOT portable. BSD/macOS appends the randomness
  # itself; GNU coreutils requires the template to end in at least six X's and
  # errors with "too few X's in template" otherwise. Under `set -euo pipefail`
  # (line 16) that aborts the whole script here — on Linux the entire rebuild
  # stops after the pre-flight checks with no error banner, 0 images built.
  # Invisible on a Mac, fatal on the Ubuntu VM the sweeps run on. Use an
  # explicit path + X's, which both platforms accept.
  BOOTSTRAP_LOG="$(mktemp "${TMPDIR:-/tmp}/secuura-bootstrap-env.XXXXXX")"
  if bash "$BOOTSTRAP" >"$BOOTSTRAP_LOG" 2>&1; then
    if grep -qi "Generated RS256 JWT" "$BOOTSTRAP_LOG"; then
      success "Generated missing RS256 JWT keypair in .env (mandatory since KS-184)"
    fi
    success "Environment ready (.env, RS256 keypair, PII keys)"
    rm -f "$BOOTSTRAP_LOG"
  else
    warn "bootstrap-env.sh failed — see $BOOTSTRAP_LOG"
    warn "Services that verify JWTs (auth, api-gateway) may be unhealthy without the keypair."
  fi
else
  warn "bootstrap-env.sh not found at $BOOTSTRAP — cannot guarantee the JWT keypair;"
  warn "auth/api-gateway may be unhealthy. Generate it with: bash Blockchain/Dev/scripts/bootstrap-env.sh"
fi

# -----------------------------------------------------------------------------
# Phase 0.6: Host workspace install freshness (KS-469)
# -----------------------------------------------------------------------------
# git pull updates package.json/package-lock.json but installs nothing, and
# image builds run npm ci INSIDE Docker — so the host node_modules silently
# rots while everything Docker-side stays green. A stale host install then
# fails host tooling (preflight's check:openapi, host test runs) with errors
# that masquerade as code/spec defects (the 2026-07-16 45-min hunt). npm
# stamps node_modules/.package-lock.json on every install; if the committed
# lock is newer than that stamp (or the stamp is missing), the install
# predates the lock. Warn with the actionable fix — don't auto-install: a
# root npm ci takes minutes and this script must stay fast for plain starts.
DEV_ROOT="$PROJECT_ROOT/Blockchain/Dev"
if [[ -f "$DEV_ROOT/package-lock.json" ]]; then
  NM_STAMP="$DEV_ROOT/node_modules/.package-lock.json"
  # Epoch mtimes (macOS stat -f, GNU stat -c fallback). A 5-minute tolerance
  # absorbs file-sync ordering skew (Unison copies the two files seconds
  # apart); the failure mode this catches is an install that is DAYS behind.
  # Same portability class as the KS-600 mktemp fix above, still unfixed here:
  # on GNU coreutils `-f` means --file-system, so `stat -f %m FILE` treats %m as
  # a FILE, fails on it, yet still prints "  File: ..." for FILE to stdout. That
  # text reaches the $(( )) below and aborts the script under `set -u` with
  # "File: unbound variable" — 0 images built on the Ubuntu VM, invisible on Mac.
  # macOS stat rejects -c cleanly, so trying -c first is safe on both.
  mtime_of() { stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0; }
  if [[ ! -f "$NM_STAMP" ]]; then
    warn "Host workspace has no install stamp (node_modules/.package-lock.json missing) — KS-469:"
    warn "host tooling (preflight check:openapi, host test runs) will fail confusingly."
    warn "Fix: (cd Blockchain/Dev && npm ci)"
  elif [[ $(( $(mtime_of "$DEV_ROOT/package-lock.json") - $(mtime_of "$NM_STAMP") )) -gt 300 ]]; then
    warn "Host workspace install is BEHIND package-lock.json (KS-469) — containers are unaffected,"
    warn "but host tooling (preflight check:openapi, host test runs) will fail confusingly."
    warn "Fix: (cd Blockchain/Dev && npm ci)"
  else
    success "Host workspace install is current (node_modules matches package-lock.json)"
  fi
fi

# -----------------------------------------------------------------------------
# Phase 1: Start containers
# -----------------------------------------------------------------------------
header "Starting Secuura Platform"

# Check if containers are already running
# KS-666: ask Compose about THIS project rather than prefix-matching container
# names. `--filter name=secuura-` is a substring match, so with a second stack
# slot running it also matched slot 1's `secuura-*` containers — slot 2 saw 33
# containers that were not its own, concluded it was already up, and skipped the
# serial build path (KS-345). Filtering by name cannot distinguish `secuura-` from
# `secuura-s2-`; the compose project can.
RUNNING_COUNT=$(docker compose -f "$COMPOSE_FILE" ps --status running -q 2>/dev/null | grep -c . || true)

if [[ "$RUNNING_COUNT" -ge 25 ]] && ! $REBUILD; then
  log "Most containers already running ($RUNNING_COUNT found). Ensuring all are up..."
  docker compose -f "$COMPOSE_FILE" up -d 2>&1 | grep -E "(Created|Started|Running)" | head -10
else
  if $REBUILD; then
    # KS-666: a rebuild recreates every container out from under whoever is
    # using the stack. Not volume-destroying, but it interrupts a run in
    # progress, so it goes through the same guard.
    run_stack_guard "rebuild all containers"
    log "Rebuilding all containers (--rebuild flag)..."
    # KS-259: build separately from up — 'up -d --build' deadlocks at BuildKit's
    # "resolving provenance" during the build->up handoff. Attestations off.
    # KS-345: a single `docker compose build` with no service args delegates to
    # ONE `buildx bake` with ~31 concurrent targets, which deadlocks on this
    # stack — the bake process wedges at 0% CPU after exporting one image and
    # never commits the rest (BUILDX_NO_DEFAULT_ATTESTATIONS alone does NOT fix
    # it). Build SERIALLY, one service per `docker compose build`, with
    # COMPOSE_BAKE=0 (classic builder, no bake delegation) and a streaming
    # --progress=plain so a slow build is visibly distinct from a hung one.
    # Image-only services (postgres/redis) are a clean no-op. Slower wall-clock
    # but it actually finishes; `tail -5` also buffered away all progress.
    # Note: macOS ships bash 3.2 — no `mapfile`/`readarray`, and `set -u` errors
    # on an empty array expansion. So iterate the newline list via word-splitting
    # (service names have no spaces) and collect failures in a plain string.
    _SVCS=$(docker compose -f "$COMPOSE_FILE" config --services | sort)
    _total=$(echo "$_SVCS" | wc -l | tr -d ' ')
    _i=0
    _failed=""
    for _svc in $_SVCS; do
      _i=$((_i + 1))
      log "Building [${_i}/${_total}] ${_svc} ..."
      if ! BUILDX_NO_DEFAULT_ATTESTATIONS=1 COMPOSE_BAKE=0 \
           docker compose --progress=plain -f "$COMPOSE_FILE" build "$_svc"; then
        log "  ✗ build FAILED: ${_svc}"
        _failed="${_failed} ${_svc}"
      fi
    done
    if [ -n "$_failed" ]; then
      log "Build FAILED for:${_failed} — not starting containers. Fix and re-run."
      exit 1
    fi
    log "Build complete (${_total} services). Starting containers..."
    docker compose -f "$COMPOSE_FILE" up -d 2>&1 | tail -10
  else
    log "Starting all containers..."
    docker compose -f "$COMPOSE_FILE" up -d 2>&1 | tail -10
  fi
fi

# -----------------------------------------------------------------------------
# Phase 2: Wait for health
# -----------------------------------------------------------------------------
header "Waiting for Services to Become Healthy"

elapsed=0
all_healthy=false

while [[ $elapsed -lt $MAX_HEALTH_WAIT ]]; do
  total=0
  healthy_count=0
  unhealthy_list=()
  
  for svc in "${EXPECTED_SERVICES[@]}"; do
    status=$(docker inspect --format='{{.State.Status}}' "$svc" 2>/dev/null || echo "not_found")
    health=$(docker inspect --format='{{.State.Health.Status}}' "$svc" 2>/dev/null || echo "none")
    
    if [[ "$status" == "running" ]]; then
      total=$((total + 1))
      if [[ "$health" == "healthy" || "$health" == "none" ]]; then
        healthy_count=$((healthy_count + 1))
      else
        unhealthy_list+=("$svc")
      fi
    else
      # Not running (exited / restarting / missing). Count it as "not healthy"
      # so the timeout diagnostic NAMES it — otherwise a removed/renamed service
      # left in EXPECTED_SERVICES sits invisibly at N-1/N forever (KS-321: the
      # cut secuura-midnight container did exactly this).
      unhealthy_list+=("$svc")
    fi
  done
  
  if [[ $healthy_count -ge ${#EXPECTED_SERVICES[@]} ]]; then
    all_healthy=true
    break
  fi
  
  # Progress indicator
  printf "\r  Healthy: %d/%d (waiting... %ds)" "$healthy_count" "${#EXPECTED_SERVICES[@]}" "$elapsed"
  
  sleep "$HEALTH_POLL"
  elapsed=$((elapsed + HEALTH_POLL))
done

echo ""  # clear the progress line

if $all_healthy; then
  success "All ${#EXPECTED_SERVICES[@]} containers are healthy"
else
  warn "Timeout after ${MAX_HEALTH_WAIT}s — ${#unhealthy_list[@]} container(s) not yet healthy:"
  # Guard the expansion: under `set -u`, bash 3.2 (the macOS default) throws
  # "unbound variable" on "${arr[@]}" when the array is empty (KS-321).
  if (( ${#unhealthy_list[@]} > 0 )); then
    for svc in "${unhealthy_list[@]}"; do
      status=$(docker inspect --format='{{.State.Status}}' "$svc" 2>/dev/null || echo "missing")
      health=$(docker inspect --format='{{.State.Health.Status}}' "$svc" 2>/dev/null || echo "none")
      warn "  $svc (status=$status health=$health)"
    done
  fi
fi

# Restart nginx-gateway to refresh DNS if frontends were just recreated
docker compose -f "$COMPOSE_FILE" restart nginx-gateway >/dev/null 2>&1 || true

# Brief pause for nginx to be ready
sleep 2

if $QUICK; then
  header "Startup Complete (quick mode — verification skipped)"
  log "Gateway: http://localhost:$GATEWAY_PORT"
  # KS-666: the lease must be recorded here as well. It was originally only in
  # the final summary, which --quick never reaches, so every quick start took
  # the stack without leaving any record that it had -- the exact invisibility
  # phase 4 exists to remove, and --quick is the common path.
  log "Stack lease: slot $SECUURA_STACK_SLOT, owner $STACK_OWNER, branch $STACK_BRANCH @ $STACK_COMMIT, $STACK_STARTED_AT (UTC)"
  announce_lease "started"
  exit 0
fi

# -----------------------------------------------------------------------------
# Phase 3: Verify portals
# -----------------------------------------------------------------------------
header "Verifying Portals"

portal_pass=0
portal_fail=0

for entry in "${PORTALS[@]}"; do
  IFS='|' read -r name url <<< "$entry"
  # KS-260: retry up to ~10s (5×2s) so a just-recreated portal that's still
  # binding doesn't read as a false ✗.
  if check_http "$url" 5 2; then
    success "$name — $url"
    portal_pass=$((portal_pass + 1))
  else
    fail "$name — $url (not reachable)"
    portal_fail=$((portal_fail + 1))
  fi
done

# -----------------------------------------------------------------------------
# Phase 4: Verify API
# -----------------------------------------------------------------------------
header "Verifying API"

# Gateway health
if check_http "http://localhost:$GATEWAY_PORT/health"; then
  success "Gateway health endpoint"
else
  fail "Gateway health endpoint not responding"
fi

# Auth - Issuer login
ISSUER_LOGIN=$(curl -s http://localhost:$GATEWAY_PORT/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@secuura.io","password":"demo123"}' 2>/dev/null)

if echo "$ISSUER_LOGIN" | grep -q '"success":true'; then
  success "Issuer login (demo@secuura.io)"
else
  fail "Issuer login failed"
fi

# Auth - Admin login
ADMIN_LOGIN=$(curl -s http://localhost:$GATEWAY_PORT/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@secuura.com","password":"admin123"}' 2>/dev/null)

if echo "$ADMIN_LOGIN" | grep -q '"success":true'; then
  success "Admin login (admin@secuura.com)"
else
  fail "Admin login failed"
fi

# Extract admin token for protected endpoint checks
ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('accessToken',''))" 2>/dev/null || echo "")

if [[ -n "$ADMIN_TOKEN" ]]; then
  # Admin endpoints
  for endpoint in "/api/admin/document-types" "/api/admin/workflows" "/api/admin/settings" "/api/admin/audit-logs"; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 \
      -H "Authorization: Bearer $ADMIN_TOKEN" \
      "http://localhost:$GATEWAY_PORT$endpoint" 2>/dev/null || echo "000")
    if [[ "$code" =~ ^(200|301)$ ]]; then
      success "Admin API: $endpoint ($code)"
    else
      fail "Admin API: $endpoint ($code)"
    fi
  done
fi

# Public verification endpoint
VERIFY_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 \
  -X POST -H 'Content-Type: application/json' \
  -d '{"documentId":"test-123"}' \
  "http://localhost:$GATEWAY_PORT/api/verification/verify" 2>/dev/null || echo "000")
if [[ "$VERIFY_CODE" != "000" ]]; then
  success "Public verification endpoint ($VERIFY_CODE)"
else
  fail "Public verification endpoint not responding"
fi

# Database connectivity
# KS-1096: was the bare `secuura-postgres` — slot 1's container. On slot N the
# exec targeted a container that does not exist and printed "PostgreSQL not
# accepting connections" under the Ready banner while the logins above had just
# round-tripped the database. Same for the Redis probe below.
DB_CHECK=$(docker exec "${STACK_PREFIX}-postgres" pg_isready -U secuura 2>/dev/null || echo "fail")
if echo "$DB_CHECK" | grep -q "accepting connections"; then
  success "PostgreSQL accepting connections"
else
  fail "PostgreSQL not accepting connections"
fi

# Redis connectivity. KS-260: redis is password-protected (correct posture), so
# a bare/wrong-credential `ping` answers `NOAUTH`/`WRONGPASS` — which is itself
# proof the server is up and serving (logins in the same run use it fine). Treat
# those as responding; only a genuine connection failure is "down". Capture
# stdout+stderr and `|| true` so an error reply isn't swallowed by `set -e`.
REDIS_PW="${REDIS_PASSWORD:-secuura_redis_dev}"
REDIS_CHECK="$(docker exec "${STACK_PREFIX}-redis" redis-cli --no-auth-warning -a "$REDIS_PW" ping 2>&1 || true)"
if [[ "$REDIS_CHECK" == *"PONG"* ]]; then
  success "Redis responding (PONG)"
elif [[ "$REDIS_CHECK" == *"NOAUTH"* || "$REDIS_CHECK" == *"WRONGPASS"* ]]; then
  success "Redis responding (auth-protected — server answered, probe credential not matched)"
else
  fail "Redis not responding"
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
header "Secuura Platform Ready"

# KS-666: count THIS slot's containers, not every Secuura container on the host.
# The old `name=secuura-` filter is a substring match, so with a second slot
# running it counted both stacks and reported a healthy total for a stack that
# was not fully up. Filtering on STACK_PREFIX does not fix it either — slot 1's
# `secuura-` is itself a prefix of slot 2's `secuura-s2-`. Ask Compose instead.
_SLOT_IDS=$(docker compose -f "$COMPOSE_FILE" ps --status running -q 2>/dev/null || true)
TOTAL_CONTAINERS=$(printf '%s' "$_SLOT_IDS" | grep -c . || true)
if [[ -n "$_SLOT_IDS" ]]; then
  HEALTHY_CONTAINERS=$(docker inspect \
    --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' \
    $_SLOT_IDS 2>/dev/null | grep -c '^healthy$' || true)
else
  HEALTHY_CONTAINERS=0
fi

echo ""
echo -e "  ${BOLD}Containers:${NC}  $TOTAL_CONTAINERS running, $HEALTHY_CONTAINERS healthy"
echo -e "  ${BOLD}Portals:${NC}     $portal_pass passed, $portal_fail failed"
echo ""
echo -e "  ${BOLD}URLs:${NC}"
echo -e "    Issuer Portal:    ${CYAN}http://localhost:$GATEWAY_PORT/${NC}"
echo -e "    Verifier Portal:  ${CYAN}http://localhost:$GATEWAY_PORT/verify/${NC}"
echo -e "    Admin Portal:     ${CYAN}http://localhost:$GATEWAY_PORT/admin/${NC}"
echo -e "    Status Page:      ${CYAN}http://localhost:$GATEWAY_PORT/status/${NC}"
echo -e "    Website:          ${CYAN}http://localhost:$GATEWAY_PORT/website/${NC}"
echo -e "    Tokenomics:       ${CYAN}http://localhost:$TOKENOMICS_PORT/${NC}"
echo -e "    API Docs:         ${CYAN}http://localhost:$GATEWAY_PORT/api/docs${NC}"
echo ""
echo -e "  ${BOLD}Credentials:${NC}"
# KS-1413: print the mechanism, not the demo password value.
echo -e "    Issuer:  demo@secuura.io (password: the published demo default - see CLAUDE.md)"
echo -e "    Admin:   provisioned per run - see systemTest/fixtures/provision-actors.ts (KS-966: no shared admin credential is published)"
echo ""
# KS-666: state, on screen, who now holds this stack — so the next person does
# not have to run a destructive command to discover it is occupied.
echo -e "  ${BOLD}Stack lease (KS-666):${NC}"
echo -e "    Slot:     $SECUURA_STACK_SLOT   Project: ${COMPOSE_PROJECT_NAME:-<compose default>}"
echo -e "    Owner:    $STACK_OWNER"
echo -e "    Branch:   $STACK_BRANCH @ $STACK_COMMIT"
echo -e "    Started:  $STACK_STARTED_AT (UTC)"
echo ""
# KS-1011 (Kam 2026-09-16, option b): marker labels are baked at container CREATE
# time, so a stack brought up any other way than this script - Docker Desktop
# restoring `restart: unless-stopped` containers after a reboot, or a plain
# `docker compose up -d` - carries "unknown" for the life of those containers, and
# a later run of this script cannot repair them. Warn loudly and name the remedy;
# never fail the start over it.
if [[ -n "$_SLOT_IDS" ]]; then
  _MARKER_UNKNOWN=$(docker inspect --format '{{index .Config.Labels "com.secuura.stack.owner"}}' $_SLOT_IDS 2>/dev/null | grep -c '^unknown$' || true)
  if [[ "$_MARKER_UNKNOWN" -gt 0 ]]; then
    echo -e "  ${BOLD}WARNING (KS-1011):${NC} $_MARKER_UNKNOWN of $TOTAL_CONTAINERS running containers report stack.owner=unknown."
    echo "    They were created outside this script, so their KS-666 marker labels cannot be repaired in place."
    echo "    Recreate them to restore the marker:  docker compose -f $COMPOSE_FILE up -d --force-recreate"
  fi
fi
announce_lease "started"
