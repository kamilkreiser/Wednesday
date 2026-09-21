#!/usr/bin/env bash
# Step 2 — resource group + storage account + tables. Every command names RG + subscription. Idempotent.
set -eu
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
. "$HERE/scripts/ids.conf"
T=$(az account show --query tenantId -o tsv); U=$(az account show --query user.name -o tsv); S=$(az account show --query id -o tsv)
[ "$T" = "$TENANT_ID" ] && [ "$U" = "kreiser.org@me.com" ] && [ "$S" = "$SUB_ID" ] || { echo "TENANT ASSERTION FAILED: $T $U $S"; exit 3; }
echo "tenant assertion PASS"

if [ "$(az group exists -n "$RG" --subscription "$SUB_ID")" = "false" ]; then
  az group create -n "$RG" -l "$LOCATION" --subscription "$SUB_ID" --tags project=wednesday-dashboard phase=pilot owner=kreiser.org@me.com created=2026-09-21 -o table
else echo "RG $RG exists"; fi

if ! az storage account show -n "$STORAGE" -g "$RG" --subscription "$SUB_ID" -o none 2>/tmp/sa_err.txt; then
  echo "creating storage account $STORAGE (show said: $(head -c 200 /tmp/sa_err.txt))"
  az storage account create -n "$STORAGE" -g "$RG" -l "$LOCATION" --subscription "$SUB_ID" \
    --sku Standard_LRS --kind StorageV2 --min-tls-version TLS1_2 --allow-blob-public-access false \
    --https-only true --allow-shared-key-access true --tags project=wednesday-dashboard phase=pilot -o none
fi
az storage account show -n "$STORAGE" -g "$RG" --subscription "$SUB_ID" \
  --query '{name:name,sku:sku.name,tls:minimumTlsVersion,blobPublic:allowBlobPublicAccess,httpsOnly:enableHttpsTrafficOnly,location:location,id:id}' -o json

# My own RBAC on the account so the tables can be created + probed with --auth-mode login (no account key used anywhere)
SA_ID=$(az storage account show -n "$STORAGE" -g "$RG" --subscription "$SUB_ID" --query id -o tsv)
for role in "Storage Table Data Contributor"; do
  if [ -z "$(az role assignment list --assignee "$KAM_USER_OBJ" --scope "$SA_ID" --role "$role" --subscription "$SUB_ID" --query '[0].id' -o tsv)" ]; then
    az role assignment create --assignee-object-id "$KAM_USER_OBJ" --assignee-principal-type User --role "$role" --scope "$SA_ID" --subscription "$SUB_ID" -o none
    echo "granted '$role' to Kam's user on $STORAGE (scope = the storage account only)"
  else echo "Kam already has '$role' on $STORAGE"; fi
done
echo "waiting up to 90s for RBAC propagation before creating tables (eventual consistency, never 'failed')"
for i in $(seq 1 18); do
  if az storage table create -n messages --account-name "$STORAGE" --auth-mode login -o none 2>/tmp/tbl_err.txt; then echo "table messages ok"; break; fi
  echo "  attempt $i: $(head -c 160 /tmp/tbl_err.txt | tr '\n' ' ')"; sleep 5
done
az storage table create -n cards --account-name "$STORAGE" --auth-mode login -o json
az storage table list --account-name "$STORAGE" --auth-mode login -o json
echo "SA_ID=$SA_ID"
sed -i '' '/^SA_ID=/d' "$HERE/scripts/ids.conf"; echo "SA_ID=$SA_ID" >> "$HERE/scripts/ids.conf"
