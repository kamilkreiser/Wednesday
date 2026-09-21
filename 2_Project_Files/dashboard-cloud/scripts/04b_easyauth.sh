#!/usr/bin/env bash
# Step 4b — Easy Auth v2 on the web app (idempotent PUT). Microsoft provider only; unauthenticated -> redirect to login;
# /api/seat/* excluded (the app validates seat JWTs itself). Separate from 04_deploy.sh so it can be re-applied alone.
set -eu
export AZURE_CONFIG_DIR=/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.azure
HERE=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud
SCRATCH=${SCRATCH:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/bbb4a64c-5352-455e-b4e6-9f36320976aa/scratchpad}
. "$HERE/scripts/ids.conf"
T=$(az account show --query tenantId -o tsv); U=$(az account show --query user.name -o tsv); S=$(az account show --query id -o tsv)
[ "$T" = "$TENANT_ID" ] && [ "$U" = "kreiser.org@me.com" ] && [ "$S" = "$SUB_ID" ] || { echo "TENANT ASSERTION FAILED: $T $U $S"; exit 3; }
echo "tenant assertion PASS"
APP_RES=$(az webapp show -n "$WEBAPP" -g "$RG" --subscription "$SUB_ID" --query id -o tsv)
cat > "$SCRATCH/authv2.json" <<JSON
{"properties":{
 "platform":{"enabled":true,"runtimeVersion":"~1"},
 "globalValidation":{"requireAuthentication":true,"unauthenticatedClientAction":"RedirectToLoginPage","redirectToProvider":"azureactivedirectory",
                     "excludedPaths":["/api/seat/*"]},
 "identityProviders":{"azureActiveDirectory":{"enabled":true,
   "registration":{"openIdIssuer":"https://login.microsoftonline.com/$TENANT_ID/v2.0","clientId":"$WEB_APPID","clientSecretSettingName":"MICROSOFT_PROVIDER_AUTHENTICATION_SECRET"},
   "validation":{"allowedAudiences":["api://$WEB_APPID","$WEB_APPID"],"defaultAuthorizationPolicy":{"allowedApplications":["$WEB_APPID"]}},
   "login":{"disableWWWAuthenticate":false}}},
 "login":{"tokenStore":{"enabled":true},"preserveUrlFragmentsForLogins":false,"cookieExpiration":{"convention":"FixedTime","timeToExpiration":"08:00:00"}},
 "httpSettings":{"requireHttps":true,"routes":{"apiPrefix":"/.auth"},"forwardProxy":{"convention":"NoProxy"}}
}}
JSON
az rest --method PUT --url "https://management.azure.com${APP_RES}/config/authsettingsV2?api-version=2022-03-01" --body @"$SCRATCH/authv2.json" \
  --query '{enabled:properties.platform.enabled,require:properties.globalValidation.requireAuthentication,action:properties.globalValidation.unauthenticatedClientAction,excluded:properties.globalValidation.excludedPaths,aad:properties.identityProviders.azureActiveDirectory.registration.clientId,issuer:properties.identityProviders.azureActiveDirectory.registration.openIdIssuer,secretSetting:properties.identityProviders.azureActiveDirectory.registration.clientSecretSettingName}' -o json
echo "== read back:"
az rest --method GET --url "https://management.azure.com${APP_RES}/config/authsettingsV2/list?api-version=2022-03-01" --query '{require:properties.globalValidation.requireAuthentication,action:properties.globalValidation.unauthenticatedClientAction,excluded:properties.globalValidation.excludedPaths}' -o json
echo "== web app config:"
az webapp config show -n "$WEBAPP" -g "$RG" --subscription "$SUB_ID" --query '{ftps:ftpsState,minTls:minTlsVersion,http20:http20Enabled,alwaysOn:alwaysOn,linuxFx:linuxFxVersion,startup:appCommandLine}' -o json
az webapp show -n "$WEBAPP" -g "$RG" --subscription "$SUB_ID" --query '{httpsOnly:httpsOnly,host:defaultHostName,state:state,identity:identity.type,mi:identity.principalId}' -o json
for p in ftp scm; do echo "basicPublishingCredentialsPolicies/$p allow=$(az resource show --ids "$APP_RES/basicPublishingCredentialsPolicies/$p" --query properties.allow -o tsv)"; done
