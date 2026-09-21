#!/usr/bin/env bash
# Step 0 — measure the tenant state we inherit. READ-ONLY. No mutation here.
# Asserts the tenant/user/subscription before anything else runs.
set -u
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
EXP_TENANT=d500ebad-cf53-4f2a-a501-f831289e67fc
EXP_USER=kreiser.org@me.com
EXP_SUB=0c57ab37-349c-47ae-a10f-e284a380bbb9

echo "== az account show"
ACC=$(az account show -o json 2>&1) || { echo "az account show FAILED (login needed? STOP): $ACC"; exit 2; }
echo "$ACC" | python3 -c '
import json,sys
a=json.load(sys.stdin)
print(json.dumps({"tenantId":a.get("tenantId"),"id":a.get("id"),"name":a.get("name"),"user":a.get("user",{}).get("name")},indent=1))
ok = a.get("tenantId")=="'"$EXP_TENANT"'" and a.get("id")=="'"$EXP_SUB"'" and a.get("user",{}).get("name")=="'"$EXP_USER"'"
print("ASSERTION tenant/sub/user ==", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 3)
' || { echo "tenant assertion FAILED — STOP"; exit 3; }

echo "== signed-in user"
az ad signed-in-user show --query '{upn:userPrincipalName,id:id}' -o json 2>&1

echo "== Security Defaults (Graph)"
az rest --method GET --url https://graph.microsoft.com/v1.0/policies/identitySecurityDefaultsEnforcementPolicy 2>&1 | head -c 1500; echo

echo "== organization assignedPlans (licence tier)"
az rest --method GET --url 'https://graph.microsoft.com/v1.0/organization?$select=displayName,assignedPlans' 2>&1 | python3 -c '
import json,sys
raw=sys.stdin.read()
try:
    d=json.loads(raw)
    for o in d.get("value",[]):
        print("org:",o.get("displayName"))
        plans=[p for p in o.get("assignedPlans",[]) if p.get("capabilityStatus")=="Enabled"]
        print("enabled plans:",sorted(set(p.get("service") for p in plans)))
except Exception as e:
    print("UNMEASURED (could not parse):",raw[:800])
'

echo "== existing app registrations named wednesday*"
az ad app list --display-name wednesday --query '[].{name:displayName,appId:appId}' -o json 2>&1
echo "== existing app registrations named tuesday*"
az ad app list --display-name tuesday --query '[].{name:displayName,appId:appId}' -o json 2>&1

echo "== does wednesday-dashboard-rg already exist?"
az group exists -n wednesday-dashboard-rg --subscription "$EXP_SUB" 2>&1
echo "== resource groups in the subscription (names only, read-only)"
az group list --subscription "$EXP_SUB" --query '[].name' -o tsv 2>&1
