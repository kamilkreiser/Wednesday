#!/bin/bash
# friday_as.sh — run ONE command under ONE client's identity, and nothing else's.
#
# WHY (Kam, 2026-09-23 10:49: "Friday will work on both Secura and Dataset projects from this laptop").
# Hard rule 2 (no cross-client contamination) and hard rules 4/5 (never mix Azure tenants or GitHub
# accounts) were enforced until today by giving each client its OWN seat. Friday serves both, so the
# isolation has to live INSIDE her: each client's gh / az state sits in its own folder under
# 4_Credentials/clients/<client>/, and this wrapper is the only thing that points a command at one.
# Friday's own shell exports NEITHER client's GH_CONFIG_DIR / AZURE_CONFIG_DIR, so a bare `gh` or `az`
# in her session reaches her own (Wednesday-repo) identity, never a client's by accident.
#
# Usage:
#   friday_as.sh secuura gh auth status
#   friday_as.sh datasec gh issue list -R <org>/<repo>
#   friday_as.sh secuura --which          # prints the identity it WOULD use, runs nothing
# The client's optional .env (4_Credentials/clients/<client>/.env) is exported for the command only.
set -u
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"; SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
TREE="$(cd -P "$(dirname "$SOURCE")/../.." && pwd)"

C="${1:-}"
case "$C" in
  secuura|datasec) shift ;;
  *) echo "friday_as: first argument must be 'secuura' or 'datasec' (got '${C}') — REFUSING rather than guessing a client" >&2; exit 2 ;;
esac
[ $# -gt 0 ] || { echo "friday_as: no command given" >&2; exit 2; }
CD="$TREE/4_Credentials/clients/$C"
[ -d "$CD" ] || { echo "friday_as: $CD does not exist — run Launch_Friday.command setup (step 6) first" >&2; exit 3; }

# Clear anything a parent shell may have exported for the OTHER client (or for Friday herself),
# then point at this client's folders only.
unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN AZURE_CLIENT_ID AZURE_CLIENT_SECRET AZURE_TENANT_ID
export GH_CONFIG_DIR="$CD/.gh-config"
export AZURE_CONFIG_DIR="$CD/.azure"
export FRIDAY_CLIENT="$C"

if [ "$1" = "--which" ]; then
  echo "client:           $C"
  echo "GH_CONFIG_DIR:    $GH_CONFIG_DIR"
  echo "AZURE_CONFIG_DIR: $AZURE_CONFIG_DIR"
  if command -v gh >/dev/null 2>&1; then echo "github login:     $(gh api user -q .login 2>&1)"; fi
  exit 0
fi
if [ -f "$CD/.env" ]; then set -a; . "$CD/.env"; set +a; fi
exec "$@"
