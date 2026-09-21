#!/usr/bin/env bash
# Step 1b — Entra app registrations for the pilot. Idempotent (looks up by exact display name first).
# Creates ONLY: wednesday-dashboard-web, wednesday-seat-api, wednesday-seat, tuesday-seat.
# The Easy Auth client secret goes ONLY to 4_Credentials/dashboard-cloud/easyauth-client-secret.json (600).
set -eu
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
. "$HERE/scripts/ids.conf"

# --- tenant assertion (fails loud) ---
T=$(az account show --query tenantId -o tsv); U=$(az account show --query user.name -o tsv); S=$(az account show --query id -o tsv)
[ "$T" = "$TENANT_ID" ] && [ "$U" = "kreiser.org@me.com" ] && [ "$S" = "$SUB_ID" ] || { echo "TENANT ASSERTION FAILED: $T $U $S"; exit 3; }
echo "tenant assertion PASS ($T / $U / $S)"

find_app() { az ad app list --display-name "$1" --query "[?displayName=='$1'].appId" -o tsv; }
ensure_sp() { # $1 appId -> prints sp objectId
  local sp; sp=$(az ad sp list --filter "appId eq '$1'" --query '[0].id' -o tsv)
  if [ -z "$sp" ]; then sp=$(az ad sp create --id "$1" --query id -o tsv); fi
  echo "$sp"
}
graph_post() { az rest --method POST --url "$1" --headers Content-Type=application/json --body "$2"; }

# ---------- 1. wednesday-dashboard-web (Easy Auth relying party) ----------
REDIRECT="https://$WEBAPP.azurewebsites.net/.auth/login/aad/callback"
WEB_APPID=$(find_app wednesday-dashboard-web)
if [ -z "$WEB_APPID" ]; then
  WEB_APPID=$(az ad app create --display-name wednesday-dashboard-web --sign-in-audience AzureADMyOrg \
     --web-redirect-uris "$REDIRECT" --enable-id-token-issuance true --query appId -o tsv)
  echo "created wednesday-dashboard-web appId=$WEB_APPID"
else echo "exists wednesday-dashboard-web appId=$WEB_APPID"; fi
WEB_OBJ=$(az ad app show --id "$WEB_APPID" --query id -o tsv)
WEB_SP=$(ensure_sp "$WEB_APPID")
az ad sp update --id "$WEB_SP" --set appRoleAssignmentRequired=true
echo "wednesday-dashboard-web: objectId=$WEB_OBJ spId=$WEB_SP appRoleAssignmentRequired=$(az ad sp show --id "$WEB_SP" --query appRoleAssignmentRequired -o tsv)"
# Assign Kam (and only Kam) the default role on the SP
EXISTING=$(az rest --method GET --url "https://graph.microsoft.com/v1.0/servicePrincipals/$WEB_SP/appRoleAssignedTo" --query "value[?principalId=='$KAM_USER_OBJ'].id" -o tsv)
if [ -z "$EXISTING" ]; then
  graph_post "https://graph.microsoft.com/v1.0/servicePrincipals/$WEB_SP/appRoleAssignedTo" \
    "{\"principalId\":\"$KAM_USER_OBJ\",\"resourceId\":\"$WEB_SP\",\"appRoleId\":\"00000000-0000-0000-0000-000000000000\"}" >/tmp/x.json 2>&1 || { cat /tmp/x.json; exit 4; }
  echo "assigned Kam ($KAM_USER_OBJ) to wednesday-dashboard-web"
else echo "Kam already assigned"; fi
echo "assignments on web SP: $(az rest --method GET --url "https://graph.microsoft.com/v1.0/servicePrincipals/$WEB_SP/appRoleAssignedTo" --query 'value[].principalDisplayName' -o tsv | tr '\n' ',')"
# Client secret for Easy Auth (6 months) — written ONLY to 4_Credentials, never printed
if [ ! -f "$CRED/easyauth-client-secret.json" ]; then
  umask 077
  az ad app credential reset --id "$WEB_APPID" --append --display-name easyauth-2026-09-21 --end-date 2027-03-21 -o json > "$CRED/easyauth-client-secret.json"
  echo "easy-auth client secret written to $CRED/easyauth-client-secret.json (keys: $(python3 -c "import json;print(list(json.load(open('$CRED/easyauth-client-secret.json')).keys()))"))"
fi
echo "easyauth secret expiry: $(az ad app show --id "$WEB_APPID" --query "passwordCredentials[?displayName=='easyauth-2026-09-21'].endDateTime" -o tsv)"

# ---------- 2. wednesday-seat-api (audience with app roles) ----------
API_APPID=$(find_app wednesday-seat-api)
ROLES_FILE=/tmp/wed_api_roles.json
python3 - "$ROLES_FILE" <<'PY'
import json,sys,uuid
# Fixed UUIDs so re-runs are idempotent
roles=[("Seat.Write","Seat may append messages/cards","11111111-0000-4000-8000-000000000001"),
       ("Seat.Read","Seat may read its partitions","11111111-0000-4000-8000-000000000002"),
       ("Client.Secuura","Partition Secuura","11111111-0000-4000-8000-000000000011"),
       ("Client.Datasec","Partition Datasec","11111111-0000-4000-8000-000000000012"),
       ("Client.WED","Partition WED (shared)","11111111-0000-4000-8000-000000000013")]
json.dump([{"allowedMemberTypes":["Application"],"description":d,"displayName":v,"id":i,"isEnabled":True,"value":v} for v,d,i in roles],open(sys.argv[1],"w"),indent=1)
PY
if [ -z "$API_APPID" ]; then
  API_APPID=$(az ad app create --display-name wednesday-seat-api --sign-in-audience AzureADMyOrg --app-roles "@$ROLES_FILE" --query appId -o tsv)
  echo "created wednesday-seat-api appId=$API_APPID"
else echo "exists wednesday-seat-api appId=$API_APPID"; fi
az ad app update --id "$API_APPID" --identifier-uris "api://$API_APPID"
API_OBJ=$(az ad app show --id "$API_APPID" --query id -o tsv)
# v2 access tokens (aud = appId, iss = login.microsoftonline.com/<tenant>/v2.0) — Graph PATCH; az --set cannot address nested api.*
az rest --method PATCH --url "https://graph.microsoft.com/v1.0/applications/$API_OBJ" --headers Content-Type=application/json --body '{"api":{"requestedAccessTokenVersion":2}}'
API_SP=$(ensure_sp "$API_APPID")
echo "wednesday-seat-api: objectId=$API_OBJ spId=$API_SP roles=$(az ad app show --id "$API_APPID" --query 'appRoles[].value' -o tsv | tr '\n' ',') tokenVersion=$(az ad app show --id "$API_APPID" --query api.requestedAccessTokenVersion -o tsv)"

# ---------- 3. seat client apps with certificate credentials + role grants ----------
role_id() { az ad app show --id "$API_APPID" --query "appRoles[?value=='$1'].id" -o tsv; }
make_seat() { # $1 name, then roles...
  local name=$1; shift
  local appid; appid=$(find_app "$name")
  if [ -z "$appid" ]; then
    appid=$(az ad app create --display-name "$name" --sign-in-audience AzureADMyOrg --query appId -o tsv)
    echo "created $name appId=$appid"
  else echo "exists $name appId=$appid"; fi
  local obj sp; obj=$(az ad app show --id "$appid" --query id -o tsv); sp=$(ensure_sp "$appid")
  # certificate credential (public cert only)
  local have; have=$(az ad app show --id "$appid" --query 'length(keyCredentials)' -o tsv)
  if [ "$have" = "0" ]; then
    az ad app credential reset --id "$appid" --cert "@$CRED/$name.crt" --append --display-name "$name-2026-09-21" -o json | python3 -c 'import json,sys;d=json.load(sys.stdin);print("cert credential uploaded; keys returned:",list(d.keys()))'
  fi
  echo "$name: objectId=$obj spId=$sp keyCredentials=$(az ad app show --id "$appid" --query 'keyCredentials[].{thumb:customKeyIdentifier,end:endDateTime}' -o tsv | tr '\n' ' ')"
  for role in "$@"; do
    local rid; rid=$(role_id "$role")
    local has; has=$(az rest --method GET --url "https://graph.microsoft.com/v1.0/servicePrincipals/$sp/appRoleAssignments" --query "value[?appRoleId=='$rid' && resourceId=='$API_SP'].id" -o tsv)
    if [ -z "$has" ]; then
      graph_post "https://graph.microsoft.com/v1.0/servicePrincipals/$sp/appRoleAssignments" \
        "{\"principalId\":\"$sp\",\"resourceId\":\"$API_SP\",\"appRoleId\":\"$rid\"}" > /tmp/x.json 2>&1 || { cat /tmp/x.json; exit 5; }
      echo "  granted $role to $name"
    else echo "  $role already granted to $name"; fi
  done
  echo "  $name roles now: $(az rest --method GET --url "https://graph.microsoft.com/v1.0/servicePrincipals/$sp/appRoleAssignments" --query 'value[].appRoleId' -o tsv | while read -r r; do az ad app show --id "$API_APPID" --query "appRoles[?id=='$r'].value" -o tsv; done | tr '\n' ',')"
  echo "${name//-/_}_APPID=$appid" >> "$HERE/scripts/ids.conf"
}
make_seat wednesday-seat Seat.Write Seat.Read Client.Secuura Client.WED
make_seat tuesday-seat   Seat.Write Seat.Read Client.Datasec

# record non-secret ids
sed -i '' '/^WEB_APPID=\|^WEB_SP=\|^API_APPID=\|^API_SP=/d' "$HERE/scripts/ids.conf"
{ echo "WEB_APPID=$WEB_APPID"; echo "WEB_SP=$WEB_SP"; echo "API_APPID=$API_APPID"; echo "API_SP=$API_SP"; } >> "$HERE/scripts/ids.conf"
echo "== ids.conf now:"; cat "$HERE/scripts/ids.conf"
