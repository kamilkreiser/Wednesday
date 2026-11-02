#!/usr/bin/env bash
# =============================================================================
# TESTS for the startup banners - KS-1413: start-secuura.sh and start-local.sh must not
# echo the demo issuer password value in their closing credentials banner.
# =============================================================================
# Reads the two scripts with grep only; nothing is started, no network, no docker.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
START_SECUURA="$REPO_ROOT/Start_Up/start-secuura.sh"
START_LOCAL="$REPO_ROOT/Blockchain/Dev/scripts/start-local.sh"
PASS=0; FAIL=0

check() {
    local desc="$1" want="$2" got="$3"
    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\n' "$desc"
    else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
}

# echoed_secret <file>: prints the number of echo lines in the file that contain the demo password value
echoed_secret() {
    grep -cE '^[[:space:]]*echo[^|]*demo123' "$1" || true
}

# --- CELL 0 (CONTROL): the instrument matches an echo line that carries the value ---
PLANT="$(printf '%s\n' '    echo "    Issuer:  demo@secuura.io  / demo123"' | grep -cE '^[[:space:]]*echo[^|]*demo123' || true)"
check "CONTROL the echo matcher sees a planted banner line with the value" "1" "$PLANT"

# --- CELL 1 (CONTROL, tip AND after): both banners still name the issuer account ---
NAMED=0
for f in "$START_SECUURA" "$START_LOCAL"; do
    if grep -qE '^[[:space:]]*echo.*Issuer:.*demo@secuura\.io' "$f"; then NAMED=$((NAMED+1)); fi
done
check "CONTROL both banners still name the demo issuer account" "2" "$NAMED"

# --- CELL 2 (RED at the tip): start-secuura.sh banner prints no password value ---
check "start-secuura.sh echoes no demo password value" "0" "$(echoed_secret "$START_SECUURA")"

# --- CELL 3 (RED at the tip): start-local.sh banner prints no password value ---
check "start-local.sh echoes no demo password value" "0" "$(echoed_secret "$START_LOCAL")"

echo ""
echo "ks1413_start_banners_print_no_demo_password: ${PASS} passed, ${FAIL} failed"
(( FAIL == 0 ))
