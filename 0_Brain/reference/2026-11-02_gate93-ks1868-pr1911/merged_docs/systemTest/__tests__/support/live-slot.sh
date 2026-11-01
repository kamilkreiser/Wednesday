# live-slot.sh — the ONE way a shell test finds a live stack: the slot its caller NAMED.
#
# WHY (KS-1286, Peter 2026-09-28): the live arms of pre_suite.test.sh defaulted to
# `http://localhost:6882` and forced `SECUURA_STACK_SLOT=1` when nothing was named, so every
# pre-push run from ANY worktree logged in to — and tried to create accounts on — slot 1's stack
# while slot 1 was running another ticket's k6 load test (measured in slot 1's gateway log,
# 2026-09-28 12:49–12:55Z: failed and successful logins plus `POST /api/users/admin/create`).
# Slots are dynamic: no test may assume slot 1 exists, is free, or is ours. A live arm now runs
# only against the slot its caller named, and otherwise says NOT RUN.
#
# The gateway is DERIVED by slot-target.sh (itself derived from slot 1's bases in stack_env.sh),
# never typed. An explicit SYSTEMTEST_BASE_URL still wins — that is the caller naming a target.
#
# Requires: $LIVE_SLOT_TARGET_SH (absolute path to systemTest/slot-target.sh).
# Provides: live_slot_named, live_slot_gateway.

# Prints the slot the caller named (SECUURA_STACK_SLOT, or platform-s's STACK_SLOT); returns 1,
# printing nothing, when neither is set. Never a default.
live_slot_named() {
  local slot="${SECUURA_STACK_SLOT:-${STACK_SLOT:-}}"
  [[ -n "$slot" ]] || return 1
  printf '%s' "$slot"
}

# Prints the live gateway root to test against, or returns 1 when the caller named no target.
live_slot_gateway() {
  if [[ -n "${SYSTEMTEST_BASE_URL:-}" ]]; then printf '%s' "$SYSTEMTEST_BASE_URL"; return 0; fi
  local slot
  slot="$(live_slot_named)" || return 1
  # A subshell, so sourcing the wrapper cannot leak its exports into the calling suite. A slot the
  # wrapper rejects makes stack_env.sh `exit 2` inside it; any failure is reported as 1, printing nothing.
  local gw
  gw="$( export SECUURA_STACK_SLOT="$slot" SECUURA_SLOT_TARGET_QUIET=1
    # shellcheck source=../../slot-target.sh
    source "$LIVE_SLOT_TARGET_SH" >/dev/null 2>&1 || exit 1
    printf '%s' "${SECUURA_GATEWAY_URL:-}" )" || return 1
  [[ -n "$gw" ]] || return 1
  printf '%s' "$gw"
}
