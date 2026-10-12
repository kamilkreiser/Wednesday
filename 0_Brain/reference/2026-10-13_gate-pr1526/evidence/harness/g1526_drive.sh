#!/bin/bash
G=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad
W=$G/w
# usage: g1526_drive.sh <slice-file-in-preflight-dir>
SL=${1:-slice_gate.sh}
U=(env -u SECUURA_STACK_SLOT -u STACK_SLOT -u GATEWAY_URL -u GATEWAY_PORT -u COMPOSE_PROJECT_NAME -u SECUURA_BASE_URL -u API_BASE_URL -u SECUURA_API_URL -u OVERRIDE_APP_URL)
hook() { # one hook-path run: real slot-target.sh then the preflight lines, as .githooks/pre-push:281-283 does
  "${U[@]}" "$@" bash -c 'cd "$0" || exit 1; . systemTest/slot-target.sh >/dev/null 2>&1 || true; cd Blockchain/Dev && bash scripts/preflight/'"$SL" "$W"
}
echo "## hook path (real slot-target.sh then real preflight lines)"
for v in X=1 SECUURA_STACK_SLOT=1 SECUURA_STACK_SLOT=2 SECUURA_STACK_SLOT=4 SECUURA_STACK_SLOT=abc SECUURA_STACK_SLOT=9 GATEWAY_URL=https://demo.invalid:1/x; do
  echo "--- $v"; hook "$v" 2>&1; echo "  rc=$?"; done
echo "## direct preflight lines, no slot-target"
for v in X=1 SECUURA_STACK_SLOT=1 SECUURA_STACK_SLOT=3 SECUURA_STACK_SLOT=0 SECUURA_STACK_SLOT=02 SECUURA_STACK_SLOT=-1 SECUURA_STACK_SLOT=2.5 SECUURA_STACK_SLOT=5 STACK_SLOT=2 "SECUURA_STACK_SLOT=;id" "SECUURA_STACK_SLOT=2;touch $G/PWN" "SECUURA_STACK_SLOT=\$(touch $G/PWN)"; do
  echo "--- $v"; "${U[@]}" "$v" bash $W/Blockchain/Dev/scripts/preflight/$SL 2>&1; echo "  rc=$?"; done
echo "--- SECUURA_STACK_SLOT=2 + explicit GATEWAY_URL"
"${U[@]}" SECUURA_STACK_SLOT=2 GATEWAY_URL=http://h:1 bash $W/Blockchain/Dev/scripts/preflight/$SL 2>&1; echo "  rc=$?"
