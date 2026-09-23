#!/usr/bin/env bash
# 01d — the FRIDAY seat's identity (2026-09-23; Kam 10:49:26 on the live board, view=wednesday: "…add a Friday tab to the
# dashboard and give it the necessary keys etc. So create a new agent called Friday… Friday will work on both Secura and
# Dataset projects from this laptop."). Brief: 2_Project_Files/fleet/briefs_staged/2026-09-23_friday_liveboard_builder.md.
#
# Follows 01a (cert) + 01b (make_seat) + 01c (public key export) for ONE new seat. Idempotent: an existing key / app / role /
# grant is found and kept, never regenerated, never replaced, never deleted.
#   1. cert pair  -> 4_Credentials/dashboard-cloud/friday-seat.pem (0600, never printed) + friday-seat.crt (public)
#   2. public key -> app/keys/friday-seat-public.pub (SPKI PEM, the tuesday-seat-public.pub format)
#   3. app role `Client.Friday` ADDED to wednesday-seat-api (the existing five roles are read first and sent back unchanged)
#   4. app registration `friday-seat` + service principal + certificate credential
#   5. grants (admin-consented appRoleAssignments, as 01b): Seat.Write, Seat.Read, Client.Friday — and NOT Client.Secuura /
#      Client.Datasec / Client.WED (asserted after: the role set must be EXACTLY those three)
#   6. friday_seat_APPID=… appended to scripts/ids.conf (once)
# Touches Entra objects only (by id); no resource group, no subscription resource.
set -eu
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
CRED=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/dashboard-cloud
PUB=$HERE/app/keys
SCRATCH=${SCRATCH:?set SCRATCH to a scratch dir}
. "$HERE/scripts/ids.conf"
NAME=friday-seat
FRIDAY_ROLE_ID=11111111-0000-4000-8000-000000000014     # fixed, the 01b pattern (…011 Secuura, …012 Datasec, …013 WED)

# --- tenant assertion (fails loud) ---
T=$(az account show --query tenantId -o tsv); U=$(az account show --query user.name -o tsv); S=$(az account show --query id -o tsv)
[ "$T" = "$TENANT_ID" ] && [ "$U" = "kreiser.org@me.com" ] && [ "$S" = "$SUB_ID" ] || { echo "TENANT ASSERTION FAILED: $T $U $S"; exit 3; }
echo "tenant assertion PASS ($T / $U / $S)"

# ---------- 1. cert pair (01a pattern) ----------
chmod 700 "$CRED"
( umask 077
  if [ ! -f "$CRED/$NAME.pem" ]; then
    openssl req -x509 -newkey rsa:2048 -sha256 -days 365 -nodes -keyout "$CRED/$NAME.pem" -out "$CRED/$NAME.crt" \
      -subj "/CN=$NAME.wednesday-dashboard.pilot/O=Wednesday pilot" > "$SCRATCH/openssl_req.txt" 2>&1 || { cat "$SCRATCH/openssl_req.txt"; exit 4; }
    echo "generated $NAME.pem (private, never printed) + $NAME.crt (public cert)"
  else echo "$NAME.pem already exists — kept"; fi )
chmod 600 "$CRED/$NAME.pem"; chmod 644 "$CRED/$NAME.crt"
echo "mode: $(stat -f '%Sp %N' "$CRED/$NAME.pem")"
openssl x509 -in "$CRED/$NAME.crt" -noout -fingerprint -sha1 | sed 's/://g' | sed "s/^.*=/$NAME thumbprint=/"
openssl x509 -in "$CRED/$NAME.crt" -noout -enddate | sed "s/^/$NAME /"

# ---------- 2. public key (01c pattern) ----------
openssl x509 -in "$CRED/$NAME.crt" -pubkey -noout > "$PUB/$NAME-public.pub"
chmod 644 "$PUB/$NAME-public.pub"
kid=$(openssl pkey -pubin -in "$PUB/$NAME-public.pub" -outform DER | openssl dgst -sha256 | sed 's/^.*= //' | cut -c1-16)
echo "$NAME-public.pub kid=$kid ($(openssl pkey -pubin -in "$PUB/$NAME-public.pub" -text -noout | /usr/bin/grep -o 'Public-Key: ([0-9]* bit)'))"

find_app() { az ad app list --display-name "$1" --query "[?displayName=='$1'].appId" -o tsv; }
ensure_sp() { local sp; sp=$(az ad sp list --filter "appId eq '$1'" --query '[0].id' -o tsv)
  if [ -z "$sp" ]; then sp=$(az ad sp create --id "$1" --query id -o tsv); fi; echo "$sp"; }

# ---------- 3. Client.Friday on the API app (read the current roles, send them back unchanged + the new one) ----------
API_OBJ=$(az ad app show --id "$API_APPID" --query id -o tsv)
az ad app show --id "$API_APPID" --query appRoles -o json > "$SCRATCH/api_roles_current.json"
python3 - "$SCRATCH/api_roles_current.json" "$SCRATCH/api_roles_patch.json" "$FRIDAY_ROLE_ID" <<'PY'
import json, sys
cur = json.load(open(sys.argv[1])); rid = sys.argv[3]
vals = sorted(r["value"] for r in cur)
print("API roles before:", vals)
if any(r["value"] == "Client.Friday" for r in cur):
    print("Client.Friday already present — no patch"); json.dump(None, open(sys.argv[2], "w")); sys.exit(0)
assert len(cur) == 5 and set(vals) == {"Seat.Write", "Seat.Read", "Client.Secuura", "Client.Datasec", "Client.WED"}, vals
keep = [{k: r[k] for k in ("allowedMemberTypes", "description", "displayName", "id", "isEnabled", "value")} for r in cur]
keep.append({"allowedMemberTypes": ["Application"], "description": "Partition Friday (the laptop seat; Secuura + Datasec work)",
             "displayName": "Client.Friday", "id": rid, "isEnabled": True, "value": "Client.Friday"})
json.dump({"appRoles": keep}, open(sys.argv[2], "w"))
print("patch will carry", len(keep), "roles:", sorted(r["value"] for r in keep))
PY
if [ "$(cat "$SCRATCH/api_roles_patch.json")" != "null" ]; then
  az rest --method PATCH --url "https://graph.microsoft.com/v1.0/applications/$API_OBJ" --headers Content-Type=application/json --body "@$SCRATCH/api_roles_patch.json" > "$SCRATCH/api_roles_patch_out.txt" 2>&1 || { cat "$SCRATCH/api_roles_patch_out.txt"; exit 5; }
  echo "patched wednesday-seat-api appRoles"
fi
echo "API roles now: $(az ad app show --id "$API_APPID" --query 'appRoles[].value' -o tsv | sort | tr '\n' ',')"

# ---------- 4. friday-seat app + SP + certificate credential ----------
APPID=$(find_app "$NAME")
if [ -z "$APPID" ]; then
  APPID=$(az ad app create --display-name "$NAME" --sign-in-audience AzureADMyOrg --query appId -o tsv)
  echo "created $NAME appId=$APPID"
else echo "exists $NAME appId=$APPID"; fi
OBJ=$(az ad app show --id "$APPID" --query id -o tsv)
SP=""; for i in 1 2 3 4 5 6; do SP=$(ensure_sp "$APPID" 2>"$SCRATCH/sp_err.txt") && [ -n "$SP" ] && break; echo "SP not ready ($(head -c 200 "$SCRATCH/sp_err.txt")) — retry $i"; sleep 10; done
[ -n "$SP" ] || { echo "no service principal for $APPID"; exit 6; }
HAVE=$(az ad app show --id "$APPID" --query 'length(keyCredentials)' -o tsv)
if [ "$HAVE" = "0" ]; then
  az ad app credential reset --id "$APPID" --cert "@$CRED/$NAME.crt" --append --display-name "$NAME-2026-09-23" -o json > "$SCRATCH/cred_reset.json" 2>"$SCRATCH/cred_reset_err.txt" || { cat "$SCRATCH/cred_reset_err.txt"; exit 7; }
  python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print("cert credential uploaded; keys returned:",list(d.keys()), "password present:", bool(d.get("password")))' "$SCRATCH/cred_reset.json"
fi
echo "$NAME: objectId=$OBJ spId=$SP keyCredentials=$(az ad app show --id "$APPID" --query 'keyCredentials[].{thumb:customKeyIdentifier,end:endDateTime,name:displayName}' -o tsv | tr '\n' ' ')"

# ---------- 5. grants (admin-consented appRoleAssignments, 01b's way) ----------
role_id() { az ad app show --id "$API_APPID" --query "appRoles[?value=='$1'].id" -o tsv; }
for role in Seat.Write Seat.Read Client.Friday; do
  rid=$(role_id "$role"); [ -n "$rid" ] || { echo "role $role not found on the API"; exit 8; }
  has=$(az rest --method GET --url "https://graph.microsoft.com/v1.0/servicePrincipals/$SP/appRoleAssignments" --query "value[?appRoleId=='$rid' && resourceId=='$API_SP'].id" -o tsv)
  if [ -z "$has" ]; then
    ok=0; for i in 1 2 3 4 5 6; do
      if az rest --method POST --url "https://graph.microsoft.com/v1.0/servicePrincipals/$SP/appRoleAssignments" --headers Content-Type=application/json \
           --body "{\"principalId\":\"$SP\",\"resourceId\":\"$API_SP\",\"appRoleId\":\"$rid\"}" > "$SCRATCH/grant_$role.txt" 2>&1; then ok=1; break; fi
      echo "grant $role not yet accepted ($(head -c 200 "$SCRATCH/grant_$role.txt")) — retry $i"; sleep 10
    done
    [ "$ok" = 1 ] || { cat "$SCRATCH/grant_$role.txt"; exit 9; }
    echo "  granted $role ($rid) to $NAME"
  else echo "  $role already granted to $NAME"; fi
done
az rest --method GET --url "https://graph.microsoft.com/v1.0/servicePrincipals/$SP/appRoleAssignments" -o json > "$SCRATCH/friday_grants.json"
az ad app show --id "$API_APPID" --query appRoles -o json > "$SCRATCH/api_roles_after.json"
python3 - "$SCRATCH/friday_grants.json" "$SCRATCH/api_roles_after.json" "$API_SP" <<'PY'
import json, sys
g = json.load(open(sys.argv[1]))["value"]; roles = {r["id"]: r["value"] for r in json.load(open(sys.argv[2]))}
got = sorted(roles.get(a["appRoleId"], "?" + a["appRoleId"]) for a in g if a["resourceId"] == sys.argv[3])
other = [a for a in g if a["resourceId"] != sys.argv[3]]
print("friday-seat roles on wednesday-seat-api:", got, "| grants on other resources:", len(other))
ok = got == sorted(["Seat.Write", "Seat.Read", "Client.Friday"]) and not other
print("ASSERTION friday-seat roles == {Seat.Write, Seat.Read, Client.Friday} and nothing else:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 10)
PY

# ---------- 6. ids.conf ----------
if /usr/bin/grep -q '^friday_seat_APPID=' "$HERE/scripts/ids.conf"; then echo "ids.conf already has friday_seat_APPID"; else
  echo "friday_seat_APPID=$APPID" >> "$HERE/scripts/ids.conf"; echo "ids.conf += friday_seat_APPID=$APPID"; fi
echo "FRIDAY_APPID=$APPID FRIDAY_SP=$SP FRIDAY_OBJ=$OBJ CLIENT_FRIDAY_ROLE=$FRIDAY_ROLE_ID"
