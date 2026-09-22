#!/bin/bash
# 04c — ZIP DEPLOY ONLY (2026-09-21 18:0x). Step 5 of 04_deploy.sh verbatim, for a static/app change when the plan, identity,
# settings and Easy Auth are already in place. Written because `az webapp update`/`config set` in 04_deploy.sh began failing
# with NoRegisteredProviderFound for api-version 2026-08-01 (azure-cli 2.81.0 vs the australiaeast provider) — those steps
# are idempotent and already applied; the zip deploy itself uses a different route. Same tenant assertion, same zip guards.
set -eu
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
SCRATCH=${SCRATCH:?set SCRATCH to a scratch dir}
. "$HERE/scripts/ids.conf"
T=$(az account show --query tenantId -o tsv); U=$(az account show --query user.name -o tsv); S=$(az account show --query id -o tsv)
[ "$T" = "$TENANT_ID" ] && [ "$U" = "kreiser.org@me.com" ] && [ "$S" = "$SUB_ID" ] || { echo "TENANT ASSERTION FAILED: $T $U $S"; exit 3; }
echo "tenant assertion PASS"
azs() { az "$@" --subscription "$SUB_ID"; }; AZ=azs
ZIP="$SCRATCH/wedcloud_deploy_$(date +%H%M%S).zip"
( builtin cd "$HERE" && zip -q -r "$ZIP" requirements.txt app seat -x 'app/__pycache__/*' 'seat/__pycache__/*' '*.pyc' '*.pre-*' )
echo "zip contents:"; unzip -Z1 "$ZIP"
PRIV_MARKERS=$(unzip -p "$ZIP" | /usr/bin/grep -i -c -- '-----BEGIN [A-Z ]*PRIVATE' || true)
PUB_MARKERS=$(unzip -p "$ZIP" app/keys/kam-pilot-public.pub | /usr/bin/grep -i -c -- '-----BEGIN PUBLIC' || true)
CTRL=$(/usr/bin/grep -i -c -- '-----BEGIN [A-Z ]*PRIVATE' "$CRED/kam-pilot-private.pem" || true)
echo "guard positive control on a real private key file: $CTRL (must be 1)"; [ "$CTRL" = "1" ] || { echo "GUARD CANNOT FAIL — ABORT"; exit 9; }
echo "zip private-key markers: $PRIV_MARKERS (must be 0); positive control: public-key markers in the public file: $PUB_MARKERS (must be 1)"
[ "$PRIV_MARKERS" = "0" ] && [ "$PUB_MARKERS" = "1" ] || { echo "ZIP CHECK FAILED — ABORT"; exit 9; }
# 2026-09-22 14:5x: EXPECT_MARKER=<string> asserts the zipped app/main.py carries the change being shipped. Added after a deploy
# shipped the PREVIOUS main.py: a `git pull --rebase --autostash` from another session had reverted the working tree 2 min
# before the zip was built (the edits sat in stash@{0}); the health check caught it, this guard catches it before the upload.
if [ -n "${EXPECT_MARKER:-}" ]; then
  MK=$(unzip -p "$ZIP" app/main.py | /usr/bin/grep -c -- "$EXPECT_MARKER" || true)
  echo "zipped app/main.py carries EXPECT_MARKER '$EXPECT_MARKER': $MK line(s) (must be >= 1)"
  [ "$MK" -ge 1 ] || { echo "ZIP DOES NOT CARRY THE CHANGE (working tree reverted?) — ABORT"; exit 9; }
fi
$AZ webapp deploy -n "$WEBAPP" -g "$RG" --src-path "$ZIP" --type zip --async false --timeout 900 -o json > "$SCRATCH/deploy_out.json" 2>"$SCRATCH/deploy_err.txt" || true
echo "deploy stderr: $(head -c 600 "$SCRATCH/deploy_err.txt")"
python3 -c 'import json,sys
try:
    d=json.load(open(sys.argv[1])); print("deploy:",{k:d.get(k) for k in ("status","status_text","complete","active","provisioningState","message","log_url") if k in d})
except Exception as e: print("deploy output not json:",open(sys.argv[1]).read()[-800:])' "$SCRATCH/deploy_out.json"
