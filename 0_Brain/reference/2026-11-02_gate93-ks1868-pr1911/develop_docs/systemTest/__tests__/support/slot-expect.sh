# slot-expect.sh — what a shell test EXPECTS for slot N, derived from slot 1's bases (KS-1386).
#
# WHY (Peter, 2026-09-29, KS-1386): the shell suites typed every slot's values by hand — `6982`,
# `akto-s2`, `actors-slot3.json`, `-slot4` — so a test could only ever agree with a literal, and a
# wrong literal in the code passed against an equally wrong literal in the test. The platform rule
# (root CLAUDE.md, "Every slot value is CALCULATED from slot 1", 2026-09-14) is that slot N is
# derived: port = base + 100*(N-1), and every name follows the slot-1 name by one fixed shape.
#
# This file states each slot-1 base ONCE and derives everything else. It holds NO slot 2..MAX
# value, and it is the one file the no-hardcoded-slot-literal guard skips (for the bases alone).
# Shape follows Blockchain/Dev/scripts/__tests__/start_secuura_slot_names.test.sh.
#
# It is an INDEPENDENT oracle: it does not source slot-target.sh or stack_env.sh to compute a
# value (KS-786 — a test that asks the code what the code should say compares the code with
# itself). The only thing it reads from stack_env.sh is the slot CEILING, so a fifth slot needs no
# edit here; it greps the declaration rather than sourcing the file.
#
# bash 3.2 (macOS /bin/bash) compatible: no associative arrays, no ${var,,}.
#
# Provides: SE_BASE_* constants, SE_PORT_BASES, SE_UNSLOTTED_TAG, and the se_* functions below.

# --- slot-1 bases, stated once -------------------------------------------------------------------
readonly SE_BASE_GATEWAY=6882
readonly SE_BASE_WEBSITE=6881
readonly SE_BASE_TOKENOMICS=8881
readonly SE_BASE_POSTGRES=6432
readonly SE_BASE_PGBOUNCER=6433
readonly SE_BASE_REDIS=6379
readonly SE_BASE_AKTO_DASHBOARD=9091
readonly SE_BASE_AKTO_MONGO=27017
readonly SE_BASE_MONGO_EXPRESS=9490
readonly SE_BASE_PW_REPORT=9324
readonly SE_BASE_K6_DASHBOARD=5665
readonly SE_PORT_STRIDE=100
# Every port family, so a guard or a loop can cover a new family by adding it here, once.
SE_PORT_BASES=("$SE_BASE_GATEWAY" "$SE_BASE_WEBSITE" "$SE_BASE_TOKENOMICS" "$SE_BASE_POSTGRES"
  "$SE_BASE_PGBOUNCER" "$SE_BASE_REDIS" "$SE_BASE_AKTO_DASHBOARD" "$SE_BASE_AKTO_MONGO"
  "$SE_BASE_MONGO_EXPRESS" "$SE_BASE_PW_REPORT" "$SE_BASE_K6_DASHBOARD")

# KS-1386: an exempt run that named no slot is labelled this — never `slot1`.
readonly SE_UNSLOTTED_TAG=unslotted

# --- the ceiling, read (not typed) from stack_env.sh ---------------------------------------------
_se_here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SE_STACK_ENV_SH="${SE_STACK_ENV_SH:-$_se_here/../../../Blockchain/Dev/scripts/stack_env.sh}"
SE_MAX_SLOT="$(sed -nE 's/^[[:space:]]*(readonly[[:space:]]+)?SECUURA_MAX_STACK_SLOT=([0-9]+).*/\2/p' "$SE_STACK_ENV_SH" 2>/dev/null | head -1)"
if [[ -z "$SE_MAX_SLOT" ]]; then
  echo "FATAL slot-expect: could not read SECUURA_MAX_STACK_SLOT from $SE_STACK_ENV_SH" >&2
  exit 2
fi
readonly SE_MAX_SLOT
unset _se_here

# --- derivations -----------------------------------------------------------------------------------
se_port()         { echo $(( $1 + SE_PORT_STRIDE * ($2 - 1) )); }                    # BASE N
se_gw()           { echo "http://localhost:$(se_port "$SE_BASE_GATEWAY" "$1")"; }       # N
se_gw_docker()    { echo "http://host.docker.internal:$(se_port "$SE_BASE_GATEWAY" "$1")"; }
se_prefix()       { if (( $1 > 1 )); then echo "secuura-s$1"; else echo "secuura"; fi; }
se_project()      { if (( $1 > 1 )); then echo "secuura_slot$1"; else echo ""; fi; }   # "" = Compose's default
se_akto_prefix()  { if (( $1 > 1 )); then echo "akto-s$1"; else echo "akto"; fi; }
se_akto_project() { if (( $1 > 1 )); then echo "akto_s$1"; else echo "akto"; fi; }
se_akto_vol()     { if (( $2 > 1 )); then echo "$1_s$2"; else echo "$1"; fi; }        # NAME N
# se_tag / se_manifest with NO argument (or an empty one) give the UNSLOTTED form (KS-1386).
se_tag()          { if [[ -n "${1:-}" ]]; then echo "slot$1"; else echo "$SE_UNSLOTTED_TAG"; fi; }
se_suffix()       { echo "-$(se_tag "$1")"; }
se_manifest()     { echo "actors-$(se_tag "${1:-}").json"; }
se_slots()        { local n=1; while (( n <= SE_MAX_SLOT )); do echo "$n"; n=$((n + 1)); done; }
# Slots other than slot 1 — the ones whose values no source or test may type.
se_slots_above_1() { se_slots | sed '1d'; }
