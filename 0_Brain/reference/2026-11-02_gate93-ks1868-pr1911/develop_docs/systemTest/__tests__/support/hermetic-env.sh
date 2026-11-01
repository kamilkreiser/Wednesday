# hermetic-env.sh — strip every slot-carrying variable before a cell launches a step (KS-1286).
#
# WHY (measured 2026-09-28): run from a shell that had sourced slot-target.sh for slot 2,
#   pre_suite.test.sh           9 of 31 red — its "offline" cells (closed port 127.0.0.1:1, a remote
#                               host) PROVISIONED AGAINST SLOT 2'S LIVE GATEWAY, because the exported
#                               SECUURA_GATEWAY_URL outranks the API_BASE_URL each cell sets;
#   quarantine_call_sites.test.sh 2 red — the same leak, plus cells that named SECUURA_STACK_SLOT=1;
#   manifest_path.test.sh       2 red under the STACK_SLOT alias alone.
# A cell must state every input it needs; nothing may arrive from the operator's shell.
#
# The strip set is MEASURED, not typed (the KS-786 lesson in slot_target.test.sh): source the real wrapper
# under `env -i`, and take every variable it adds to the SAME bare bash environment, plus the inputs it
# reads. A wrapper that grows a new export is stripped here without anyone editing a list.
#
# Requires: $HERMETIC_SLOT_TARGET_SH (absolute path to systemTest/slot-target.sh).
# Provides: HERMETIC_SLOT_VARS (array of names) and HERMETIC_STRIP (array of `-u NAME` for `env`).

# Variables the wrapper READS (so it adds none of them) but which steer slot behaviour.
HERMETIC_SLOT_INPUTS=(SECUURA_STACK_SLOT SECUURA_SLOT_TARGET_QUIET STACK_SLOT CI SECUURA_TICKET SECUURA_ARTIFACT_LABEL AKTO_RUN_NAME)

hermetic_measure_slot_vars() { # $1 = wrapper; prints one name per line
  local wrapper="$1"
  # The baseline goes through the SAME bash, with the SAME inputs, so bash's own variables (PWD, SHLVL, _)
  # and the two we pass in cancel out instead of being counted as slot variables.
  comm -13 \
    <(env -i HOME="$HOME" PATH="$PATH" SECUURA_STACK_SLOT=2 SECUURA_SLOT_TARGET_QUIET=1 bash -c 'env' \
        | cut -d= -f1 | grep -E '^[A-Za-z_][A-Za-z0-9_]*$' | sort -u) \
    <(env -i HOME="$HOME" PATH="$PATH" SECUURA_STACK_SLOT=2 SECUURA_SLOT_TARGET_QUIET=1 \
        bash -c 'source "$1" >/dev/null 2>&1; env' _ "$wrapper" \
        | cut -d= -f1 | grep -E '^[A-Za-z_][A-Za-z0-9_]*$' | sort -u)
}

HERMETIC_SLOT_VARS=()
while IFS= read -r _hermetic_v; do [[ -n "$_hermetic_v" ]] && HERMETIC_SLOT_VARS+=("$_hermetic_v"); done \
  < <(hermetic_measure_slot_vars "$HERMETIC_SLOT_TARGET_SH")
if (( ${#HERMETIC_SLOT_VARS[@]} < 20 )); then
  echo "FATAL hermetic-env: measured only ${#HERMETIC_SLOT_VARS[@]} slot variables from $HERMETIC_SLOT_TARGET_SH — nothing would be stripped" >&2
  exit 2
fi
HERMETIC_SLOT_VARS+=("${HERMETIC_SLOT_INPUTS[@]}")
HERMETIC_STRIP=()
for _hermetic_v in "${HERMETIC_SLOT_VARS[@]}"; do HERMETIC_STRIP+=(-u "$_hermetic_v"); done
unset _hermetic_v

# The strip set minus the variables a cell passes in deliberately (e.g. `API_BASE_URL=… run_step x`,
# where the value reaches the function through its environment). Prints `-u NAME` words, one per line.
hermetic_strip_except() { # $@ = names to keep
  local v keep k
  for v in "${HERMETIC_SLOT_VARS[@]}"; do
    keep=""; for k in "$@"; do [[ "$v" == "$k" ]] && keep=1; done
    [[ -z "$keep" ]] && printf -- '-u\n%s\n' "$v"
  done
  return 0
}
