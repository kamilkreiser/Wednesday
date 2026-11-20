# A9 | The HPAM back end as sent on 2026-11-20: `hpam-api`, `hpam-marketplace`, `infra_hpam`

Commission B1763, lane G, reader 1. Written 2026-11-20. Read-only: nothing was run from the source trees, no network, no git write.
All `path:line` pointers are relative to `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1120b/extracted/`.
Short prefixes used below: `API/` is `hpam-api-main/hpam-api-main/`, `MKT/` is `hpam-marketplace-main/hpam-marketplace-main/`, `INF/` is `infra_hpam-main/infra_hpam-main/`.

STATUS OF THIS FILE: complete (sections 1 to 10). Written in sections as the reading went; the BLUF was written last.

## BLUF

1. **`hpam-api` IS the gateway the documents ask for, and it is far smaller than they assume.** It is three Azure Functions, 70 lines: a health check, `negotiate` (hands out an Azure SignalR connection) and `send` (broadcasts whatever JSON it is given to the hub `printerhub`). It holds no user, card, PIN, token, licence or tenant logic and stores nothing. There is no card flow in it at all. OQ-7's gateway half is answered.
2. **The gateway does not check who sends an unlock message.** All three routes are anonymous in code; the only gate is App Service authentication in front (a token from the customer's tenant for `api://<HPAM client id>`), which does not say which user. Whoever may send may also listen, and every message goes to every connection. That settles the PRECONDITION of question 10 (OQ-10) in its bad form; the decision is still the product owner's. Two links in the attack are inferred and need a test (section 6.3).
3. **`hpam-marketplace` is two Azure offers:** the customer-tenant deployment (Function App, SignalR, storage, and an optional Log Analytics reporting stack whose accepted columns are now known: 17 and 3) and a deployable LICENCE SERVER (a pre-built .NET portal on SQLite), which the documents assumed did not exist outside Datasec. **`infra_hpam` is Datasec's own legacy Keycloak back end** (four production regions) with the `cc-api` web app (`CypherConnectAPI`); under C-18 it is out of scope.
4. **The documents' design survives, with one piece understated:** the server can join SignalR as one subscriber per tenant exactly as planned, but the phone-redirect relay is not "one added endpoint": it needs an authentication exclusion, a function allow-list entry, a new package compiled into the offer, and a second update path for customers who deployed by script.
5. **Counts:** 82 inventory rows (gateway 14, flow 6, keys 6, offer resources 20, licence component 15, build 5, infrastructure 16) plus 9 secret-location rows; 17 document comparisons, of which 3 contradictions (D4, D11, D14), 1 open risk answered adversely (D8), 13 "source missing" statements superseded, 2 still unknown; 22 proposed corrections; 7 open questions. **One secret location needs an owner's attention: a committed Terraform state backup holding four App Configuration access keys (S1).** No secret value appears in this report.

## 1. What each repository is

### 1.1 `hpam-api`: a three-function SignalR relay, and nothing else

`hpam-api` is an Azure Functions v4 Node.js app whose whole source is three files, 70 lines in total (`wc -l`: `index.js` 11, `send.js` 34, `printerhub.js` 25; one runtime dependency, `@azure/functions`, `API/package.json:10-12`). Its own README calls it "A Node.js application to work with Azure SignalR service" (`API/README.md:3`).

It IS the Function App that the Marketplace offer puts in the customer's Azure and that the printer app and the phone app talk to: the Marketplace wizard describes it as "the secure authentication gateway for HP Authentication Manager printer application and for the HP Secure Authentication mobile application, this services is to receive a token before connecting to the SignalR service" (`MKT/artifact/createUiDefinition.json:189`), and the deploy script tells the installer to enter its URL in the printer configuration field "SignalR Endpoint" (`API/deploy/api.sh:219-221`).

It is NOT a sign-in service in the sense the project documents may assume. It holds no user, no card, no PIN, no token, no licence and no tenant logic. It does two things: hand a caller the connection details for an Azure SignalR hub, and broadcast whatever JSON body a caller posts to that hub. Everything that makes a sign-in a sign-in (who the user is, what the message carries, what the printer does on receipt) lives in the two clients: the Workpath printer app and the phone app. Neither client is in these three repositories.

### 1.2 `hpam-marketplace`: the two Azure Marketplace offers

Two independent Bicep templates with their compiled ARM templates and wizard definitions:
- `MKT/bicep/main.bicep` (522 lines) with `MKT/artifact/`: the customer-tenant offer. It deploys the `hpam-api` Function App with Azure SignalR ("QR Sign In feature", `MKT/artifact/createUiDefinition.json:106`) and, separately switchable, a Log Analytics reporting stack ("Enable HPAM Reporting", `MKT/artifact/createUiDefinition.json:259`).
- `MKT/license/main.bicep` (301 lines) with `MKT/license/artifact/`: a licence-server web app ("HPAM License App", `MKT/license/artifact/createUiDefinition.json:12`). The template deploys a pre-built .NET package fetched from a Datasec storage URL; the licence server's source is not in this repository.

### 1.3 `infra_hpam`: Datasec's own legacy back-end infrastructure

Terraform for the Datasec-hosted Keycloak servers, their databases and the `CypherConnectAPI` web app (`cc-api`) in seven environments, plus two container builds. It is not the customer-tenant gateway and has no SignalR in it. Detail in section 4.

## 2. `hpam-api` inventory

### 2.1 HTTP routes (all of them)

Route prefix is `api` (`API/host.json:4-6`). `host.json` also carries an allow-list of exactly three functions, `healthcheck`, `send`, `negotiate` (`API/host.json:12`), so no other function can load even if a file were added.

| # | Method and path | Code auth level | What it reads | What it writes | What it returns | Pointer |
|---|---|---|---|---|---|---|
| G1 | GET `/api/healthcheck` | `anonymous` | nothing (logs the URL) | nothing | body `Healthy!` | `API/src/functions/index.js:3-11` |
| G2 | POST `/api/negotiate` | `anonymous` | the SignalR connection-info input binding for hub `printerhub`, from app setting `SIGNALR_CONNECTION_STRING` | nothing | the binding's object as a JSON string (by the binding's contract: the SignalR client URL and a short-lived SignalR access token); 500 with the error on failure | `API/src/functions/printerhub.js:3-8`, `:10-26` |
| G3 | POST `/api/send` | `anonymous` | the request JSON body; its field `realm` | one SignalR message to hub `printerhub`: `target` (the client method name) is the value of `body.realm`, `arguments` is the whole body | 200 with no body; 500 with `{error}` if the body is not JSON or the binding fails | `API/src/functions/send.js:3-8`, `:10-34` |

Things to note about these three rows:

- G4. **The code-level auth is anonymous on all three, but the platform in front of it is not.** The Marketplace template turns on App Service authentication with `requireAuthentication: true` and `unauthenticatedClientAction: 'Return401'` (`MKT/bicep/main.bicep:250-253`), Microsoft Entra as the provider with the customer's own tenant as issuer (`MKT/bicep/main.bicep:258`), allowed audience `api://<HPAM app client id>` (`MKT/bicep/main.bicep:267-269`) and allowed calling application the same HPAM app client id (`MKT/bicep/main.bicep:272-274`). The script deployment does the same thing with `az webapp auth` (`API/deploy/api.sh:209-217`). So in a deployed system every route, health check included, needs a bearer token issued by the customer's tenant for the audience `api://<HPAM app registration client id>`. The function code never inspects the token or the caller.
- G5. **The message is addressed by SignalR method name, not by connection, user or group.** `send` sets only `target` and `arguments` (`API/src/functions/send.js:18-21`); there is no `userId`, `groupName` or `connectionId`. In the Azure SignalR output binding that means the message goes to every connection on the hub, and each client receives it only if it has a handler registered under the name carried in `realm`. `negotiate` passes no `userId` either (`API/src/functions/printerhub.js:3-8`). The "realm" is therefore the routing key, chosen by the sender. What the printer app registers as its handler name (a per-printer value, a per-session value shown in the QR code, or a per-tenant value) is NOT in this repository: it is in the Workpath app and the phone app.
- G6. **The body is opaque to the gateway.** `send` forwards the whole body unchanged (`API/src/functions/send.js:20`). The gateway neither validates nor reads any field except `realm`. The schema of the sign-in message (what the phone sends, whether it carries a user token, an identifier or a one-time code) cannot be learned from this repository.
- G7. **No persistence.** No table, blob, queue, Cosmos or SQL use in the function code. Search: `/usr/bin/grep -r -o -i -c` for `table|blob|cosmos|sql|redis|queue` over `API/src` gave 0 in each of the three files; positive control from the same tree, `signalr` (case-insensitive), gave `send.js` 7, `printerhub.js` 5, `index.js` 0. The storage account the Function App is given is the Functions host's own (`AzureWebJobsStorage`) and the deployment package container (`MKT/bicep/main.bicep:129-132`, `:334-335`).
- G8. **No Microsoft Graph call and no Entra call from code.** Search over `API/src` for `graph|msal|login\.microsoftonline|oauth|jwt|bearer|authorization|headers`: 0 in each of the three files (same positive control as G7). The only Graph permission anywhere in the repository is in the helper script that creates the app registration: delegated `User.Read` on Microsoft Graph, then admin consent (`API/deploy/app_registration.sh:47`, `:50`; the Graph application id on line 47 was confirmed by a count match on the well-known Graph id, 1 hit). The script also creates a client secret valid two years (`API/deploy/app_registration.sh:21`, `:31-37`) and sets the identifier URI `api://<app id>` (`API/deploy/app_registration.sh:53`) that G4's audience check relies on.
- G9. **No card enrolment, no PIN, no licence check, no tenant model in code.** Search over `API/src` for `card|enrol|enroll|pin|licen|tenant|badge`: 0 in each of the three files (same positive control). The tenant model is "one deployment per customer tenant": the issuer is fixed to the tenant the template is deployed in (`MKT/bicep/main.bicep:258`; `API/deploy/api.sh:215` takes the tenant id as typed input).
- G10. **Logging is switched down to nothing.** Default log level `None`, Application Insights sampling, live metrics and dependency tracking all off (`API/host.json:14-32`); the script deployment creates the app with `--disable-app-insights` (`API/deploy/api.sh:182`). There is no audit trail of who sent what to which realm.
- G11. **Function timeout five minutes** (`API/host.json:13`); SignalR serverless connection timeout 60 seconds (`MKT/bicep/main.bicep:309-311`).

### 2.2 The phone (QR) sign-in flow, as far as this source shows it

| Step | What happens | Pointer | Seen in source? |
|---|---|---|---|
| F1 | A client (printer app or phone app) obtains an Entra token for audience `api://<HPAM app client id>` in the customer's tenant | `MKT/bicep/main.bicep:254-277` (what the platform demands) | The demand is in source; HOW each client gets the token is not (client code absent) |
| F2 | The printer app calls POST `/api/negotiate` and receives the SignalR URL and access token | `API/src/functions/printerhub.js:10-26` | yes |
| F3 | The printer app opens the SignalR connection to hub `printerhub` and registers a handler under some name (the "realm") | hub name at `API/src/functions/printerhub.js:6`; handler name not in source | hub yes; handler name NO |
| F4 | The printer shows a QR code; the phone app scans it and signs the user in to Microsoft | wizard text only: "QR sign in authentication feature" `MKT/artifact/createUiDefinition.json:111`, "QR Code Authentication workflows" `:145` | NO (wizard wording only) |
| F5 | The phone app calls POST `/api/send` with a JSON body whose `realm` names the printer's handler | `API/src/functions/send.js:16-21` | yes (the gateway side) |
| F6 | SignalR delivers the body to every connection that has a handler of that name; the printer app acts on it and signs the user in on the panel | `API/src/functions/send.js:18-21` | delivery yes; what the printer does with it NO |

There is NO card flow in this repository at all: no card enrolment route, no card lookup, no storage of a card identifier (G7, G9). Card and PIN sign-in must live entirely in the Workpath app and whatever store it uses (the project's A1 and A5 reports are the place to look, not this source).

### 2.3 Token and key handling (LOCATIONS only)

| # | Item | Location | Note |
|---|---|---|---|
| K1 | SignalR primary connection string (contains the SignalR access key) | Function App setting NAME `SIGNALR_CONNECTION_STRING`: set at `API/deploy/api.sh:198` from `az signalr key list` (`:151-155`); set at `MKT/bicep/main.bicep:332` from `listKeys()` | A plain app setting, not a Key Vault reference. No value is in the repository. |
| K2 | HPAM app registration client secret | Function App setting NAME `MICROSOFT_PROVIDER_AUTHENTICATION_SECRET`: `API/deploy/api.sh:193`, `API/deploy/api_update_secret.sh:23`, `MKT/bicep/main.bicep:333`; referenced by name at `MKT/bicep/main.bicep:260` and `API/deploy/api.sh:217` | Typed by the installer at a prompt (`API/deploy/api.sh:72-74`, read without `-s`, so it echoes to the terminal) or into the wizard (`MKT/artifact/createUiDefinition.json:79-89`, a plain `TextBox`, not a `PasswordBox`). No value is in the repository. |
| K3 | Storage account key | settings NAMES `AzureWebJobsStorage` and `DEPLOYMENT_STORAGE_CONNECTION_STRING`: `MKT/bicep/main.bicep:334-335`, both built from `listKeys()` at deploy time | No value in the repository. Shared-key access is left on (`MKT/bicep/main.bicep:100`). |
| K4 | `local.settings.json` | `API/local.settings.json` (115 bytes), also inside `API/deploy/hpam-api.zip`, `MKT/bicep/api-hpam-v1.2.0.zip`, `MKT/bicep/api-hpam-v1.3.0.zip` | Read MASKED (key names and value lengths only). Keys: `IsEncrypted`, `Values/FUNCTIONS_WORKER_RUNTIME` (length 4), `Values/AzureWebJobsStorage` (length 0, EMPTY). It holds NO secret. The three zipped copies hash-match the loose one. |
| K5 | The SignalR access token the gateway hands out | returned in the body of `negotiate`, `API/src/functions/printerhub.js:15` | Minted by the binding from K1; lifetime is the binding's default (not set in source). |
| K6 | A sample secret-shaped string in a validation message | `MKT/artifact/createUiDefinition.json:86`, `MKT/license/artifact/createUiDefinition.json:99` | By its wording ("f.e.") a format example, not a credential. Not reproduced here. |

No secret VALUE was found in `hpam-api`. A gitleaks workflow runs on push and pull request in all three repositories (`API/.github/workflows/gitleaks.yml:1-26`).

### 2.4 Build, packaging, versions

- G12. The CI workflow only installs, runs a placeholder test and zips (`API/.github/workflows/build.yml:23-36`; the test script is `echo "No tests yet..."`, `API/package.json:8`). There are no tests.
- G13. Three packaged copies of the app exist and the three function files in each hash-match the loose source: `API/deploy/hpam-api.zip` (324 entries, it bundles `node_modules`), `MKT/bicep/api-hpam-v1.2.0.zip` (`@azure/functions` `^4.7.0`), `MKT/bicep/api-hpam-v1.3.0.zip` (`@azure/functions` `^4.16.2`). The Marketplace template deploys `v1.3.0` (`MKT/bicep/main.bicep:74`, `:180`). The loose source pins `^4.11.2` (`API/package.json:11`). So the function CODE has not changed between v1.2.0 and v1.3.0; only the dependency version and the Node runtime (script: Node 22, `API/deploy/api.sh:179`; Marketplace: Node 24, `MKT/bicep/main.bicep:227-229`).
- G14. Zip member dates run from July 2025 (function files) to July 2026 (the v1.3.0 package files), as listed by `unzip -l`.

## 3. `hpam-marketplace` inventory

### 3.1 Offer 1, the customer-tenant deployment (`MKT/bicep/main.bicep`, compiled to `MKT/artifact/mainTemplate.json`, Bicep 0.38.33)

Wizard inputs (`MKT/artifact/createUiDefinition.json:329-344`): HPAM app registration client id, client secret, the enterprise application (service principal) object id (`:66-101`); "QR sign in authentication feature" enable or disable, DEFAULT DISABLED (`:109-116`); service plan size Basic, Standard or Premium, default Basic (`:154-161`); optional custom resource names (`:198-254`); "Enable HPAM Reporting" enable or disable, DEFAULT DISABLED (`:280-287`). Note that the Bicep parameter defaults are the opposite, both `true` (`MKT/bicep/main.bicep:9`, `:42`); through the Marketplace wizard the wizard's value wins.

Resources (21 in the compiled template, counted by a `json` parse of `MKT/artifact/mainTemplate.json`; 19 of them conditional, the storage account and its blob service being the two that are always deployed):

| # | Resource | Condition | Detail | Pointer (`MKT/bicep/main.bicep`) |
|---|---|---|---|---|
| M1 | Storage account, Standard_LRS, StorageV2 | always | public network access on, TLS 1.2, no public blobs, shared key allowed | `:87-122` |
| M2 | Blob service `default` | always | | `:124-127` |
| M3 | Blob container `function-releases` | QR sign-in on | holds the Function App package | `:129-132` |
| M4 | User-assigned managed identity `app-functions-deploy-identity-<unique>` | QR sign-in on | used only by the deployment script M7 | `:134-137` |
| M5 | Role assignment: Reader on the App Service plan to M4 | QR sign-in on | | `:139-147` |
| M6 | Role assignment: Website Contributor on the Function App to M4 | QR sign-in on | | `:149-157` |
| M7 | Deployment script (Azure CLI 2.66.0) that decodes the embedded `api-hpam-v1.3.0.zip` and zip-deploys it with a remote build | QR sign-in on | the zip is compiled INTO the template as base64 (`MKT/artifact/mainTemplate.json:156`, one 5,865-character line) | `:159-184` |
| M8 | App Service plan, `FC1` Flex Consumption, Linux | QR sign-in on | | `:186-197` |
| M9 | Function App, system-assigned identity, HTTPS only, Node 24, max 40 instances, 512 MB | QR sign-in on | | `:199-240` |
| M10 | App Service authentication settings (see G4) | QR sign-in on | token store enabled | `:242-292` |
| M11 | Azure SignalR, Serverless mode; SKU Free_F1, Standard_S1 or Premium_P1 by plan size | QR sign-in on | upstream template pointing every hub and event at the Function App host with auth `None` | `:294-326`, SKU mapping `:66-70` |
| M12 | Function App `appsettings` (the four NAMES in 3.2) | QR sign-in on | | `:328-337` |
| M13 | Deployment script that sleeps 60 seconds | reporting on | waits for the workspace | `:76-85` |
| M14 | Log Analytics workspace, retention 120 days by default | reporting on | | `:340-352` |
| M15 | Two linked-storage-account links (`Alerts`, `Query`) to M1 | reporting on | | `:354-372` |
| M16 | Custom table `HpamPrinterLogs_StatisticsJobData_CL`, 17 columns, 370 days, 730 total | reporting on | job statistics per printer job | `:375-407` |
| M17 | Custom table `HpamPrinterLogs_Supply_CL`, 3 columns | reporting on | supplies | `:410-428` |
| M18 | Data collection endpoint, public | reporting on | | `:432-440` |
| M19 | Data collection rule with the two custom streams | reporting on | | `:443-505` |
| M20 | Role assignment: Monitoring Metrics Publisher on the rule to the HPAM app's service principal | reporting on | this is what lets the PRINTER APP, using the HPAM app registration, push logs straight to Azure Monitor | `:509-517` |

(Rows M1 to M20 cover the 21 template resources: M15 is two resources in one row.)

Role assignments, complete list: M5 (Reader, plan, deploy identity), M6 (Website Contributor, Function App, deploy identity), M20 (Monitoring Metrics Publisher, data collection rule, HPAM service principal). Three. The Function App's own system-assigned identity (`:206-208`) is given NO role.

Outputs (`MKT/bicep/main.bicep:520-522`): `ReportingConnectionString` in the form `<logs ingestion endpoint>@Custom-HpamPrinterLogs@<rule immutable id>`, `SignalREndpointURL` (the Function App's `https://` host), `TenantId`. These are the three values an installer carries to the printer configuration; the script route prints the same two strings (`API/deploy/api.sh:219-221`, `API/deploy/hpam_logs.sh:224-226`, the second naming the parameter `reporting_string` and saying it is configured "via HP Command Centre").

### 3.2 Every app setting NAME

Offer 1, Function App (`MKT/bicep/main.bicep:332-335`): `SIGNALR_CONNECTION_STRING`, `MICROSOFT_PROVIDER_AUTHENTICATION_SECRET`, `AzureWebJobsStorage`, `DEPLOYMENT_STORAGE_CONNECTION_STRING`. Four. The script route sets `WEBSITE_RUN_FROM_PACKAGE`, `MICROSOFT_PROVIDER_AUTHENTICATION_SECRET`, `SIGNALR_CONNECTION_STRING` (`API/deploy/api.sh:188`, `:193`, `:198`).

Offer 2, licence web app (`MKT/license/main.bicep:190-239`): `APPINSIGHTS_INSTRUMENTATIONKEY` and `APPLICATIONINSIGHTS_CONNECTION_STRING` (only with monitoring on), `DatabaseProvider`, `AzureAd__CallbackPath`, `AzureAd__ClientId`, `AzureAd__ClientSecret`, `AzureAd__Domain`, `AzureAd__Instance`, `AzureAd__TenantId`, `HomeTenantId`, `WEBSITE_HEALTHCHECK_MAXPINGFAILURES`; plus one connection string NAME `CUSTOMCONNSTR_DB` (`:183-189`).

### 3.3 Offer 2, the licence component (`MKT/license/main.bicep`, compiled to `MKT/license/artifact/mainTemplate.json`)

13 resources by parse of the compiled template:

| # | Resource | Detail | Pointer (`MKT/license/main.bicep`) |
|---|---|---|---|
| L1 | Virtual network `10.0.0.0/16` with one subnet `10.0.0.0/24`, delegated to App Service, storage service endpoint | | `:24-57` |
| L2 | Network security group allowing inbound TCP 443 from anywhere | | `:60-80` |
| L3 | Storage account, default action Deny, only the subnet allowed | | `:83-107` |
| L4 | File service and a 16 GB SMB file share `hpamlicensedbstorage` | | `:109-134` |
| L5 | Linux App Service plan, Basic tier (`B1` in Bicep default; the wizard offers `B2` and `P0V3`, `MKT/license/artifact/createUiDefinition.json:122-128`) | | `:137-148` |
| L6 | Application Insights (optional) | | `:150-157` |
| L7 | Web app, .NET 10 on Linux, start command `dotnet HPAM.License.Portal.dll`, health check path `/healthcheck`, the file share mounted at `/data` | | `:160-243` |
| L8 | VNet integration | | `:245-252` |
| L9 | User-assigned deploy identity with Reader on the plan and Website Contributor on the web app | two role assignments | `:254-277` |
| L10 | Deployment script: downloads `license-portal.zip` from a Datasec-named public storage URL and zip-deploys it | the package URL is at `:21`; the licence server's SOURCE is not in any of the three repositories | `:279-297` |

What the template shows about the licence server (it shows nothing about its logic):
- L11. It is a .NET web portal named `HPAM.License.Portal` (`MKT/license/main.bicep:172`).
- L12. Its database is SQLite, one file on the mounted Azure Files share (`DatabaseProvider` `Sqlite` at `:203-206`; the connection string NAME and the file path at `:183-188`).
- L13. It signs users in with Microsoft Entra as a MULTI-TENANT app (`AzureAd__TenantId` is `common`, `:227-230`) with the callback `/signin-oidc` (`:207-210`), and it carries a `HomeTenantId` setting (`:231-234`), which by its name separates the operator's own tenant from the customers'.
- L14. The wizard asks for "the License Server App Registration" (`MKT/license/artifact/createUiDefinition.json:20`), a SEPARATE app registration from the HPAM one.
- L15. Nothing in `hpam-api` or in offer 1 calls it. Search over all three trees for `license-portal|License.Portal|hpam-license`: hits only inside `MKT/license/` (counts in section 6.4). How a printer app checks a licence against this server (the endpoint, the request, the response) is NOT in these repositories.

### 3.4 Build scripts (read, not run)

- B1. `MKT/build.sh:4-27`: `bicep build main.bicep`, copy `main.json` to `artifact/mainTemplate.json`, find the highest `artifact/hpam-azure-x.y.z.zip`, add one to the patch number (or start at 1.0.0), zip `createUiDefinition.json` and `mainTemplate.json`. That zip is what is uploaded to Partner Center as the offer's package.
- B2. `MKT/build-license.sh:4-27`: the same for `license/`, zip name `hpam-azure-license-x.y.z.zip`.
- B3. The built zips and `main.json` are git-ignored (`MKT/.gitignore:1-4`), so the repository holds no record of which package version is live in the Marketplace.
- B4. `MKT/deploy/api.sh` and `MKT/deploy/hpam_logs.sh` are byte-identical to the `hpam-api` copies (`diff -q`, no difference). `MKT/deploy/app_registration.sh` differs from the `hpam-api` copy by one added step, registering the `Microsoft.ContainerInstance` provider (`MKT/deploy/app_registration.sh:4-6`), which deployment scripts need.
- B5. The wizard links the customer to a public help article for the onboarding steps (`MKT/artifact/createUiDefinition.json:21`). Not fetched (no network).

## 4. `infra_hpam` inventory

### 4.1 What it is

Terraform (plus two container builds and one page of notes) for the infrastructure DATASEC ITSELF runs: per region, a Keycloak identity server with its PostgreSQL database and a .NET web app called `CypherConnectAPI`. Its README says "HPAM to provision HP authorization manager solution" and "Keycloak solution in Azure cloud is managed by terraform" (`INF/README.md:4`, `:9`). By every sign in the code this is the LEGACY Datasec-hosted back end (the documents' P13, "Legacy Keycloak back end", ruled NOT USED for OXPd by C-18), not the customer-tenant gateway. It has no SignalR resource at all: `/usr/bin/grep -r -o -i -c signalr` over the whole tree gave 0 files with a hit; positive control `keycloak` in the same tree, 17 files with a hit for `signalr|keycloak`.

| # | Item | Detail | Pointer |
|---|---|---|---|
| I1 | Terraform set-up | `azurerm` 3.87.0; remote state in an Azure storage container in a resource group named for the Datasec platform; lock file also pins `azuread` 2.47.0, `random` 3.6.0, `time` 0.10.0 | `INF/hpam/main.tf:1-17`, `INF/hpam/.terraform.lock.hcl:4-5`, `:23-24`, `:43-44`, `:62-63`, `INF/hpam/config/datasecdev.tfbackend:1-4` |
| I2 | Environments | seven resource groups: `dev-hpam` (West Europe), `staging-hpam`, `demo-hpam` (Australia East), and production in four regions: `production-au-hpam` (Australia East), `production-eu-hpam` (West Europe), `production-sp-hpam` (Southeast Asia), `production-us-hpam` (East US) | `INF/hpam/resource-group.tf:5-50` |
| I3 | Per environment | one Linux App Service plan (dev `B2`, all others `P1v3`), one Keycloak module, one `cc-api` module: seven of each | `INF/hpam/hpam-service.tf:5-235` |
| I4 | Keycloak module | PostgreSQL Flexible Server 14, 7-day backups, geo-redundant, zone-redundant high availability in production only; a Linux web app running the container image `keycloak:v26.1` from a private registry, path `/auth`, health check `/auth/health`, session affinity on | `INF/hpam/modules/keycloak.V26/main.tf:67-95`, `:98-166` |
| I5 | Keycloak settings | every credential is read from Azure App Configuration by key NAME (`Keycloak:dbpassword`, `Keycloak:DbUser`, `Keycloak:Config:User`, `Keycloak:Config:Password`, `ContainerRegistry:Password`, `ContainerRegistry:Url`, `ContainerRegistry:Username`, `Keycloak:sku`, `Keycloak:dbstorage`, `Keycloak:hostname`), labelled by environment. The web app also sets `NODE_TLS_REJECT_UNAUTHORIZED` to `0` | `INF/hpam/modules/keycloak.V26/main.tf:8-63`, `:131-148` (the TLS setting at `:139`) |
| I6 | `cc-api` module | a Linux web app on .NET 8, start command `dotnet CypherConnectAPI.dll`, health check `/healthcheck`, system-assigned identity, named `<region>-hpam-api` in production and `<region>-hpam-<environment>-api` elsewhere; Application Insights attached to a workspace named for Keycloak production logs | `INF/hpam/modules/cc-api/main.tf:1-5`, `:44-50`, `:54-74` |
| I7 | `cc-api` app setting NAMES | `KEYCLOAK_URL`, `KEYCLOAK_USER`, `KEYCLOAK_PASSWORD`, `KEYCLOAK_OTPEXCEPTIONSGROUPNAME`, `KEYCLOAK_CLIENTID`, `APPINSIGHTS_INSTRUMENTATIONKEY`, `ASPNETCORE_ENVIRONMENT`, `APPCONFIGURATION_FILTERKEY`, `OTP_APP_INFO`, `OTP_APP_NAME`, `OTP_APP_PIN_LIFETIME_SECONDS` (30), `KEYCLOAK_REALM_ADMIN_NAME`, `REGION_CODE`, `SALT` (a 32-character random string generated by Terraform); connection string NAME `CUSTOMCONNSTR_APPCONFIGURATION` | `INF/hpam/modules/cc-api/main.tf:7-10`, `:76-97` |
| I8 | PDF API module | a Gotenberg container (`gotenberg --api-timeout=180s`) behind App Service authentication, described as "App registration to make secure connection between mailflow app and pdf api"; four app registrations are created, but every one of the seven module instances has `count = 0`, so NO PDF API web app is deployed by this code as it stands | `INF/hpam/modules/pdf-api/main.tf:62-140`, `INF/hpam/pdf-api-service.tf:5-9`, `:24`, `:63`, `:102`, `:144`, `:164`, `:179`, `:194` |
| I9 | A defect in the PDF API file | the production identifier URI is attached to the dev-staging registration, not the production one | `INF/hpam/pdf-api-service.tf:129-131` |
| I10 | Shared App Configuration store | standard tier with a UK replica; the deploying identity is made App Configuration Data Owner | `INF/hpam/app-configuration.tf:1-19` |
| I11 | Alerts (production only) | 13 metric-alert resources: one on App Configuration throttling; per region, plan CPU above 70 and memory above 90, Keycloak health check, 5xx and network, database connection failures, CPU, memory and storage above 70, and for the API health check, 5xx and network; all to one action group | `INF/hpam/alerts.tf:3-289`, action group at `INF/hpam/variables.tf:23-26` |
| I12 | Workbook | one Application Insights workbook per production region, `<region>-hpam-api`: request totals, failures, authentication failures (400 and 401), failed requests, Keycloak identity-provider login errors, Keycloak 5xx | `INF/hpam/workbook.tf:4-10`, queries at `:54`, `:73`, `:94`, `:132`, `:158`, `:179`, `:200` |
| I13 | Network module | a VNet with back-end and gateway subnets, NAT gateway and security groups exists as a module but its only use is commented out | `INF/hpam/modules/vnet/main.tf:5-92`, `INF/hpam/vnet.tf:5-12` |
| I14 | `docker/keycloak` | image built from Keycloak 26.0.2 with a Datasec theme, PostgreSQL, relative path `/auth`, feature `persistent-user-sessions`; a compose file for local development; a manually triggered workflow that tests and pushes the image to a Datasec container registry. The welcome page title reads "Welcome to CypherConnect admin panel" | `INF/docker/keycloak/Dockerfile:1-13`, `INF/docker/keycloak/docker-compose.yml:1-36`, `INF/.github/workflows/keycloak-build.yml:1-61`, `INF/docker/keycloak/themes/dsec-theme/welcome/index.ftl:5` |
| I15 | `docker/app-registration-secret-alert` | a container that signs in as a service principal, lists every app registration in the tenant and e-mails an alert when a client secret has expired or will within 14 days | `INF/docker/app-registration-secret-alert/app-registration-secrets-alert.sh:4-12`, `:15-16`, `:19`, `:22`, `:42-51` |
| I16 | `docs/keycloak.md` | deployment in three steps (run Terraform, allow the database connection, create the `keycloak` database by hand), then general prose on App Service plans, autoscale, monitoring by App Service metrics and alerting; one operational fact: non-production uses a low tier and no scaling | `INF/docs/keycloak.md:5-13`, `:29-35`, `:37-45` |

Version drift worth knowing: the image built in `docker/keycloak` is 26.0.2 (`INF/docker/keycloak/Dockerfile:1`), the module deploys the tag `v26.1` (`INF/hpam/modules/keycloak.V26/main.tf:117`), and the README says the tag is controlled by an App Configuration key (`INF/docker/keycloak/README.md:13`), which the module does not read.

### 4.2 What it says about deployment and operations

Deployment is `az login`, `terraform init`, `terraform apply` by a person (`INF/README.md:10-13`); there is no pipeline that applies Terraform (the only workflows are the gitleaks scan and the Keycloak image build). Operations are Azure-native: App Service health checks, metric alerts to one action group, one workbook, 180 days of HTTP logs on each web app (`INF/hpam/modules/cc-api/main.tf:99-109`). Nothing here describes the customer-tenant side.

### 4.3 What `cc-api` is, and what its absence leaves unknown

References to `cc-api`, `cc_api`, `ccapi` or `cypherconnect`, by `/usr/bin/grep -r -o -i -c` (zips and images excluded):
- `hpam-api`: 0 files with a hit (positive control `signalr|keycloak`: 4 files with a hit).
- `hpam-marketplace`: 0 files with a hit (same control: 5 files).
- `infra_hpam`: 4 files, 14 hits: `hpam/hpam-service.tf` 7, `hpam/modules/cc-api/main.tf` 4, `hpam/terraform.tfstate.backup` 2, `docker/keycloak/themes/dsec-theme/welcome/index.ftl` 1.

From those: `cc-api` is the repository that builds `CypherConnectAPI.dll`, the .NET 8 API that Datasec hosts beside each regional Keycloak (I6). Its settings show it administers Keycloak with an admin account, has one-time-code logic ("OTP", a 30-second PIN lifetime, an exceptions group) and is region-aware (I7). The four production regions (AU, EU, US, Singapore) match the "API/Keycloak Hosted Services" regions report A6 found in the manuals (report A6 line 316), and report A1 lists the legacy endpoints the Workpath app calls on such an API (`token/client-credentials`, `config/`, `users`, `cardless/secret`, hub `printerhub-secure`: report A1 line 425). So `cc-api` appears to be the legacy hosted API, the Keycloak-mode counterpart of what `hpam-api` plus Entra do in the current mode. This is an inference from its infrastructure; its source was not sent.

What its absence leaves unknown: the legacy routes and their behaviour (how `cardless/secret` is produced, the legacy hub `printerhub-secure`, the OTP logic). Under C-18 (no OXPd customer is on the legacy back end) none of that is needed. One naming trap: the Terraform calls the `cc-api` web app "hpam api" (`<region>-hpam-api`, alerts named `hpamapi`: `INF/hpam/modules/cc-api/main.tf:2`, `INF/hpam/alerts.tf:222-289`). It is a different thing from the `hpam-api` repository. If anyone says "the HPAM API", ask which.

## 5. Identity and secrets (LOCATIONS only; no value appears in this report)

| # | Location | What is there | Severity |
|---|---|---|---|
| S1 | `INF/hpam/terraform.tfstate.backup:24-52` | A committed Terraform state backup (Terraform 1.1.9, serial 4) holding the Azure App Configuration store's FOUR access keys: `primary_read_key` (`:24`), `primary_write_key` (`:31`), `secondary_read_key` (`:41`), `secondary_write_key` (`:48`), each with a `connection_string` and a `secret` field (`:26`, `:28`, `:33`, `:35`, `:43`, `:45`, `:50`, `:52`). Read as structure only (attribute names and lengths; each key attribute is 267 characters long). That store is where every Keycloak, database and registry credential of I5 and I7 is kept, so a live write key would be the key to all of them. The repository ignores only `.terraform/` (`INF/.gitignore:1`), so state files are tracked. Whether these keys are still valid is not knowable from the file | **HIGH until someone confirms the keys were rotated** |
| S2 | `INF/hpam/terraform.tfstate` | 0 bytes, empty | none |
| S3 | `INF/docker/keycloak/docker-compose.yml:11`, `:22`, `:24` | database and bootstrap-admin passwords for the LOCAL development compose stack; short default-style words | low (local only), but they must never be used in a deployed instance |
| S4 | `INF/docker/app-registration-secret-alert/Dockerfile:16-29` | a service-principal password and an e-mail service connection string are passed as build arguments and written into image environment variables, so they live in the image layers of whatever was pushed to the registry; the README shows the build command with placeholders (`INF/docker/app-registration-secret-alert/README.md:7`) | medium (design weakness; no value in the repository) |
| S5 | `INF/hpam/variables.tf:25` | a subscription identifier inside the alert action-group path | identifier, not a secret; not reproduced |
| S6 | `INF/.github/workflows/keycloak-build.yml:36-37`, `:55-56` | registry user and password referenced as GitHub secrets by NAME | none (names only) |
| S7 | `API/local.settings.json` and its three zipped copies | no secret (see K4) | none |
| S8 | `MKT/license/main.bicep:21` | the public storage URL the licence-server package is downloaded from at deploy time, unauthenticated, with no checksum (`:294`) | not a secret; a supply-chain point: whoever can write that blob controls what every licence-server deployment runs |
| S9 | K1 to K3 in section 2.3 | where the gateway's secrets live at run time (plain app settings) | as the documents' W27 |

Three values were shown to me by tool output and are NOT repeated anywhere: the short local-development default at `INF/docker/keycloak/docker-compose.yml:24` (my masking script skips values shorter than six characters), part of the sample string at `MKT/artifact/createUiDefinition.json:86`, and the subscription identifier of S5. None is a credential of a deployed system as far as the files show.

## 6. Comparison with the documents

Document pointers are `02` for `02_architecture.md`, `03` for `03_plan-of-attack-and-build.md`, `05` for `05_readiness-to-build.md`, by line number as the files stood on 2026-11-20 after B1760.

### 6.1 Statement by statement

| # | Document statement (pointer) | What the source shows | Verdict |
|---|---|---|---|
| D1 | The phone app "and its SignalR/Function App gateway are reused" (`02:16`) | The gateway is three functions with a stable, tiny contract (G1 to G3); nothing in it prevents a server from being one more client | CONFIRMED as feasible |
| D2 | "no source of the gateway in the library ... its location is still to be found" (`02:44`); "its source is in none of the library's repositories" (`03:42`); WP0.7 "locate the customer Function App gateway source" (`03:140`); "The gateway source, asked for on the same card, i[s not answered]" (`02:971`); "the gateway source (asked again)" (`02:985`); "nothing new was learned about it" (`03:448`); "the gateway source" still owed (`03:450`); "still needed" (`05:12`); "Nothing you sent is the gateway" (`05:70`); "The gateway source blocks the phone sign-in work" (`05:77`); "Still needed" (`05:140`); listed among sources not in the library (`05:172`) | The source arrived on 2026-11-20 (C-40): repository `hpam-api`, packaged and deployed by `hpam-marketplace` (`API/README.md:3`, `MKT/artifact/createUiDefinition.json:189`, `MKT/bicep/main.bicep:74`, `:180`) | SUPERSEDED: twelve statements, all true when written, none true now |
| D3 | "the server joins the existing SignalR as one subscriber per tenant" (`02:44`); "one SignalR connection per tenant" (`02:73`, `02:336`); "Same SignalR hub and Function App; server subscribes once per tenant" (`02:718`); D11 option (a) (`02:823`) | Possible exactly as the Workpath app does it: an app-only token for `api://<client id>/.default` (report A1 line 265) satisfies the platform check (G4), POST `/api/negotiate` returns the connection (G2), the hub is `printerhub` (`API/src/functions/printerhub.js:6`), and the handler name is the routing key (G5; report A1 line 266 says the Workpath app uses the tenant id) | CONFIRMED |
| D4 | "the Function App may gain the phone-redirect relay endpoint" (`02:44`); the relay as an "additive" change (`02:874`); WP3.2 "relay endpoint added to the customer's Function App ... and shipped through the existing Azure offer" (`03:174`); D11 (`02:823`) | Not additive in the sense of "one more function". Four things stand in the way, all in source: (1) the platform refuses every unauthenticated request with 401 (`MKT/bicep/main.bicep:250-253`) and a phone browser returning from Microsoft carries no bearer token, so the auth settings need an excluded path, which the template does not have today (`excludedPaths`: 0 hits in `MKT/bicep/main.bicep`; control `allowedAudiences`, 1 hit); (2) `host.json` allow-lists three function names (`API/host.json:12`); (3) the app has no state store, so the relay must pass the code on, and the only channel it has broadcasts to every listener (G5); (4) the package is compiled into the template (M7), so a new endpoint is a new offer version that each customer must redeploy | CONTRADICTED IN PART (the relay is possible; "additive" understates it) |
| D5 | "later changes (for example per-printer routing instead of broadcast, W5), each backward-compatible" (`02:44`, `02:650`, `02:823`) | The routing key is chosen by the SENDER (`API/src/functions/send.js:17-19`). Per-printer routing therefore needs either the phone app to send a different `realm`, or the gateway to derive a target from another body field. Which body fields exist is not in this source (G6) | STILL UNKNOWN (needs the phone app's message; see Q2) |
| D6 | The phone app "publishes `{printer name, email, secret}`" (`02:389`); "routes by printer name" (`02:73`, `02:336`) | The gateway reads one field, `realm`, and forwards the whole body (`API/src/functions/send.js:16-21`). `realm` is not mentioned in the documents. The other fields are known only from the receiving side (report A1 lines 118 and 149) | STILL UNKNOWN from this source; one new field name found |
| D7 | Entra app credential used for "SignalR scope; Monitor scope" (`02:580`) | SignalR: audience `api://<client id>` and the calling application restricted to the same client id (`MKT/bicep/main.bicep:267-274`). Monitor: the HPAM service principal holds Monitoring Metrics Publisher on the data collection rule (`MKT/bicep/main.bicep:509-517`; script route `API/deploy/hpam_logs.sh:203-207`) | CONFIRMED |
| D8 | "Whether the Function App binds the published e-mail to the caller's token is a WP0.7 finding" (`02:613`); R24 "Gateway publisher trust unknown ... nobody has read the gateway source" (`02:879`); WP0.7 definition of done (`03:140`); OQ-10 (`03:374`); question 10 "Nobody has read the gateway's code" (`05:91-95`) | It does NOT bind. `send` never looks at the caller or the token (`API/src/functions/send.js:14-21`; search for `authorization|bearer|jwt|headers` in `API/src`: 0 in each of the three files, control `signalr` 12 hits). The platform check admits ANY token with the right audience from the customer's tenant issued to the HPAM application, with no restriction on which user (`allowedPrincipals: {}`, `MKT/bicep/main.bicep:270-275`). `negotiate` has the same gate, so whoever may send may also listen (G2, G4). The script route does not even restrict the calling application (`API/deploy/api.sh:213-217`: audience only) | ANSWERED: the feared case is the real one |
| D9 | W5 "Unlock messages broadcast to every printer of a tenant, carrying e-mail and virtual card id" (`02:650`) | Confirmed from the sending side, and wider than stated: the message goes to every connection on the hub, not only printers (G5). Combined with D8, any admitted caller can hold a connection and read every unlock message | CONFIRMED, and wider |
| D10 | W27 "Function App secret in a plain environment variable" (`02:672`) | Confirmed in the template and both scripts (K2). The SignalR key and the storage key are held the same way (K1, K3). No Key Vault in the offer (`vault`: 0 hits in `hpam-api` and `hpam-marketplace`; control `listKeys`, 4 files) | CONFIRMED, two more secrets of the same kind |
| D11 | R19 "each change means every customer redeploys or updates the ... offer"; mitigation "ship gateway changes through the existing offer, never by hand" (`02:874`) | Redeploy: confirmed (M7; the package is inside the template). But there are TWO supported deployment routes: the Marketplace offer and a hand-run script that builds the same thing with different settings (`API/deploy/api.sh:143-217`: Consumption plan not Flex, Node 22 not 24, SignalR always Standard_S1, no calling-application restriction). Customers who used the script cannot be updated "through the offer" | CONFIRMED on redeploy; CONTRADICTED on the single channel |
| D12 | Job statistics and supplies go to `<base>_StatisticsJobData_CL` and `<base>_Supply_CL`, "same record shape (to be proven field by field: spike S11)" (`02:127`, `02:343`, `02:716`); "No device events" (`02:343`) | Table names, stream names and the accepted columns are now in hand: 17 columns for job statistics and 3 for supplies (`MKT/bicep/main.bicep:375-428`, `:474-503`). The reporting string is `<ingestion endpoint>@Custom-HpamPrinterLogs@<rule id>` (`MKT/bicep/main.bicep:520`). There is no device-event table (`deviceevent`: 0 files in `hpam-api` and `hpam-marketplace`; control `statisticsjobdata`, 4 files). The rule stamps every record with the arrival time, overwriting any time the sender set (`MKT/bicep/main.bicep:457`, `:463`) | CONFIRMED; S11 now has the accepted-column list to test against |
| D13 | "the customer's Log Analytics rule that decides which report columns are accepted" is not in the library (`05:172`) | It is in `MKT/bicep/main.bicep:443-505` and `API/deploy/hpam_logs.sh:108-167`. A given customer's live rule could still differ from the template | SUPERSEDED |
| D14 | "assumed the licence service stays Datasec-hosted" (`03:341`); question 13 "The licence check needs Datasec's licence service" with option (b) "a customer-hosted licence service" treated as new work (`05:110-112`); "the licence service" among what stays the same (`02:16`) | A second Marketplace offer already deploys the licence server into any Azure subscription, on SQLite, as a multi-tenant Entra app with a "home tenant" setting (L7, L12, L13). Report A5's unanswered question 7 ("Why does the licence portal support SQLite ...") has its answer here. WHO is meant to deploy this offer (Datasec only, HP, resellers, customers) is not in the source | CONTRADICTED as an assumption: a deployable licence server exists; who uses it is unknown |
| D15 | P13 "Legacy Keycloak back end ... NOT USED (ruled, C-18)" (`02:46`, `02:842`) | `infra_hpam` is that back end's infrastructure (section 4). Nothing in it is needed by the OXPd design | CONFIRMED as out of scope |
| D16 | First-run "test page checks Graph, CSA schema, SignalR, Log Analytics, licence" (`02:750`) | Both the QR gateway and reporting are OPTIONAL and DEFAULT OFF in the Marketplace wizard (`MKT/artifact/createUiDefinition.json:116`, `:287`). A healthy customer may have neither | CONFIRMED with a condition: the test page must treat both as "not configured", not as failures |
| D17 | Customer-hosted pieces are "SignalR, Function App, Storage, Log Analytics" (`02:44`) | Confirmed: M1 to M20. Also a user-assigned deploy identity and two deployment scripts | CONFIRMED |

Counts for this table: 17 rows. CONFIRMED 10 (D1, D3, D7, D9, D10, D12, D15, D16, D17, and D11 in part). CONTRADICTED 3 (D4 in part, D11 in part, D14). ANSWERED 1 (D8). SUPERSEDED 2 rows covering 13 statements (D2, D13). STILL UNKNOWN 2 (D5, D6).

### 6.2 Is OQ-7's gateway half answered?

YES. The gateway source is `hpam-api` (three functions), its deployment is `hpam-marketplace/bicep` and `hpam-api/deploy`. WP0.7's "locate" and "read its SignalR contract" are done by this report. What WP0.7 still owes is the part the gateway cannot answer: the message body, which only the phone app's source or a capture in a test tenant can give.

### 6.3 Is question 10 (OQ-10) answered?

Its PRECONDITION is answered; the decision is still the product owner's. Question 10 asks what to do "if the customer's sign-in gateway does not check who sends an unlock message". It does not (D8). The document's own recommendation for that case is option (b), switch QR sign-in without MFA off on OXPd until the gateway is fixed (`05:93-94`).

How bad it is, stated with its limits. From source: any caller the platform admits can send any body to any realm and can listen to every message on the hub. Inferred, NOT tested: (1) an ordinary user of the customer's tenant can obtain such a token, because the phone app obtains one on a user's behalf from the same app registration (report A6 lines 217-218 and 290 describe the phone getting a gateway token and a `SignalR.Access` scope; that scope is not created by any script in these trees: 0 hits for `SignalR.Access`, control `User.Read` 2 files); (2) the per-user `secret` is stable from one sign-in to the next (report A1 line 24 calls it "a per-user virtual card id"). If both hold, a tenant user could collect other users' e-mail and secret pairs by listening and replay them at a printer; in No-MFA mode that is a sign-in as the other user. Both points need a test in the phase-0 tenant before anyone states this as fact. In MFA mode the documents already require a second step (C-29), which bounds it.

### 6.4 Searches behind the absence claims in this section

All by `/usr/bin/grep -r -o -i -c`, zips and images excluded, counted as files with at least one hit unless a hit count is given:
- `license-portal|License\.Portal|hpam-license`: 3 files, all under `MKT/license/` (`main.bicep` 3 hits, `artifact/createUiDefinition.json` 2, `artifact/mainTemplate.json` 3); 0 in `hpam-api`, 0 in `infra_hpam`.
- `keycloak` in `hpam-api` and `hpam-marketplace`: 0 files. Control: same word in `infra_hpam`, present (17 files for `signalr|keycloak`, of which `signalr` alone is 0).
- `card|enrol|badge|otp|pin_` in `INF/hpam`, `INF/docs`, `INF/README.md`: 1 file, `INF/hpam/modules/cc-api/main.tf`, 4 hits (the `OTP_` setting names). No card logic in the infrastructure either.
- `groupname|userid|connectionid` in `API/src`: 0 in each of the three files; control `target`: 1 hit in `send.js`.

## 7. What the OXPd server must call or reproduce for full parity (C-16), and what the design would break

### 7.1 Must call or reproduce

1. **Get an app-only token** for `api://<HPAM client id>/.default` from the customer's tenant with the HPAM app credential (what G4 demands; report A1 line 265).
2. **POST `<SignalR endpoint>/api/negotiate`** with that bearer token, then connect to hub `printerhub` (G2). With the .NET SignalR client the hub URL is `<SignalR endpoint>/api`, as in the Workpath app (report A1 line 264).
3. **Register a handler under the same name the Workpath app uses** (the tenant id, per report A1 line 266) and filter by printer name on receipt, because the gateway does no filtering (G5).
4. **Send nothing.** Printers only listen (report A1 line 268); only the phone calls `send`. The server should never call `/api/send` in release 1 unless the relay design needs it.
5. **Reconnect and re-negotiate** on drop; the SignalR token from `negotiate` is short-lived and the serverless connection timeout is 60 seconds (G11).
6. **Post job statistics and supplies** to the two streams with only the 17 and 3 accepted column names, using a token for Azure Monitor from the same app registration (D12, M20). Records with other top-level names are not stored.
7. **Parse the reporting string** `<endpoint>@Custom-HpamPrinterLogs@<rule id>` exactly as issued (`MKT/bicep/main.bicep:520`, `API/deploy/hpam_logs.sh:224`).
8. **Treat an empty SignalR endpoint and an empty reporting string as valid configurations** (D16).
9. **Work against both deployment routes** (Marketplace and script), which differ in plan type, runtime version, SignalR tier, issuer string (`MKT/bicep/main.bicep:258` against `API/deploy/api.sh:215`) and caller restriction (D11).
10. **Licence:** nothing in these repositories changes the licence protocol (it is in report A5's source). The licence server can be someone else's deployment with its own host name (D14), which the licence's host binding already allows (report A5 line 80).

Nothing in `hpam-api` needs to be reproduced inside the server: it has no logic to reproduce.

### 7.2 What the documents' design would break or must not assume

- X1. **The relay (M2b) as designed cannot be a plain new route** (D4). It needs an authentication exclusion in the template, an entry in the `host.json` allow-list, a new package version, and a way to hand the result to the server that does not broadcast it in a usable form. The PKCE verifier staying on the server (`02:388`) is what makes a broadcast code harmless; that property must be kept and tested.
- X2. **A gateway change cannot reach script-deployed customers through the offer** (D11).
- X3. **SignalR Free tier is the default** (`MKT/bicep/main.bicep:64-70`, wizard default Basic at `MKT/artifact/createUiDefinition.json:161`). General knowledge, not from this source and to be checked against Microsoft's current limits: the Free tier allows a small fixed number of concurrent connections and a daily message cap. One server connection per tenant is kind to that limit (a Workpath fleet uses one connection per printer), so the OXPd design helps here; but a mixed fleet near the cap today would notice any extra listener.
- X4. **"Messages never forwarded to devices" (`02:650`) fixes the OXPd side only.** The hub still delivers every message to every other listener (D9).
- X5. **Do not rely on gateway logs for audit.** Logging is off (G10). Any audit of QR sign-ins must be the server's own.
- X6. **Do not assume the record time in Log Analytics is the job time** (D12, the `now()` transform).
- X7. **Do not add a Key Vault reference without a template change** (D10): the Function App has an identity but no role and the offer has no vault.

## 8. PROPOSED CORRECTIONS (not applied; one sentence each; the writer decides the wording)

| # | Document line to replace | Proposed sentence | Source support |
|---|---|---|---|
| PC1 | `05:70` ("Still open: the source of the sign-in gateway ... Nothing you sent is the gateway.") | "Received on 2026-11-20 (C-40) and read (report A9): the gateway is the repository `hpam-api`, a three-function relay in front of Azure SignalR, deployed by the `hpam-marketplace` offer." | `API/README.md:3`; `API/host.json:12`; `MKT/artifact/createUiDefinition.json:189` |
| PC2 | `05:12` ("The source of the sign-in gateway ... is still needed ...") | "Both pieces of source code in the kit line are now in hand: the SharePoint app and the sign-in gateway (`hpam-api`, C-40)." | as PC1 |
| PC3 | `05:77` (the bracketed sentence ending "The gateway source blocks the phone sign-in work of phase 3") | "The gateway source is in and read; what still gates the phone sign-in work is your answer to question 10 and a capture of the phone app's message." | `API/src/functions/send.js:16-21` |
| PC4 | `05:92` ("Nobody has read the gateway's code (it is not in the library). In No-MFA mode a QR message is a full credential.") | "The gateway's code has been read (report A9): it does not check who sends an unlock message or whose e-mail it names, and whoever may send may also listen; in No-MFA mode a QR message is a full credential." | `API/src/functions/send.js:14-21`; `MKT/bicep/main.bicep:250-253`, `:267-275` |
| PC5 | `05:94` ("Recommendation: decide once the gateway source has been read; if it does not check the sender, (b). Default: (a), as Workpath.") | "Recommendation: (b), because the gateway does not check the sender; default until you rule: (a), as Workpath, with the risk recorded." | as PC4 |
| PC6 | `05:140` (kit row 12, "Still needed") | "The source code of the customer gateway: received 2026-11-20 (`hpam-api`, with `hpam-marketplace`); still wanted: the phone app's source or a message capture." | as PC1 |
| PC7 | `05:172` (the list of sources not in the library) | Remove "the customer gateway (Function App)" and "the customer's Log Analytics rule that decides which report columns are accepted" from the list; keep "the phone app". | `MKT/bicep/main.bicep:443-505` |
| PC8 | `03:42` (phase-0 input, gateway source "in none of the library's repositories") | "The source of the customer gateway: received 2026-11-20 (C-40), repository `hpam-api`, deployed by `hpam-marketplace`; read in report A9." | as PC1 |
| PC9 | `03:140` (WP0.7 row) | "WP0.7: gateway source located and read (A9); remaining: capture the phone app's message body in the test tenant, test whether an ordinary tenant user can obtain a gateway token, and plan the relay as a template change (authentication exclusion, function allow-list, new package version), not as one added route." | `API/host.json:12`; `MKT/bicep/main.bicep:250-253`, `:159-184` |
| PC10 | `03:174` (WP3.2 row, "relay endpoint added to the customer's Function App ... shipped through the existing Azure offer") | "relay endpoint added to the customer's Function App with an authentication exclusion for that one path and a new offer version; customers who deployed by script need a separate update path." | `MKT/bicep/main.bicep:250-253`; `API/deploy/api.sh:143-217` |
| PC11 | `03:261` ("Gateway source not found → the M2 relay (WP3.2) cannot ship; ...") | "Gateway source found (A9): the M2 relay can be built, but it is a customer-side Azure release and is not automatic for script-deployed customers; the fallbacks in this line stay for tenants that have not taken the update." | as PC10 |
| PC12 | `03:371` (OQ-7 row, "Still open: the gateway source ...") and `03:374` (OQ-10 row) | OQ-7: "ANSWERED 2026-11-20: SharePoint source (C-33, A8) and gateway source (C-40, A9)." OQ-10: "The gateway does not check the sender (A9 D8); the decision is the product owner's; default as Workpath, risk recorded." | as PC1, PC4 |
| PC13 | `02:44` (P11 evidence cell, "no source of the gateway in the library ...: its location is still to be found before any change") | "gateway source received 2026-11-20 (`hpam-api`; offer in `hpam-marketplace`; report A9): three functions, all behind App Service authentication; a relay endpoint needs a template change, not only a new function." | `API/host.json:12`; `MKT/bicep/main.bicep:242-292` |
| PC14 | `02:613` (the two sentences from "That rule does not bound who may publish a message" to "... is open question OQ-10") | "That rule does not bound who may publish a message, and the gateway does not either: it forwards any body from any caller the platform admits and never reads the caller's identity (report A9 D8); what to do about No-MFA with QR is open question OQ-10." | `API/src/functions/send.js:14-21`; `MKT/bicep/main.bicep:267-275` |
| PC15 | `02:650` (W5 description, "Unlock messages broadcast to every printer of a tenant") | "Unlock messages broadcast to every connection on the customer's hub (every printer and any other admitted listener), carrying e-mail and virtual card id." | `API/src/functions/send.js:18-21`; `API/src/functions/printerhub.js:3-8` |
| PC16 | `02:672` (W27 description and evidence) | "Function App holds the app secret, the SignalR key and the storage key as plain app settings; the offer has no Key Vault (report A9 K1 to K3)." | `MKT/bicep/main.bicep:332-335` |
| PC17 | `02:874` (R19 text "the gateway source is not in the library" and mitigation "ship gateway changes through the existing offer, never by hand") | "the gateway source is in hand (A9); there are two deployment routes, the Marketplace offer and a hand-run script, so a gateway change needs an update path for each." | `MKT/bicep/main.bicep:159-184`; `API/deploy/api.sh:143-217` |
| PC18 | `02:879` (R24, "Gateway publisher trust unknown ... because nobody has read the gateway source") | "Gateway publisher trust is absent: the gateway neither authenticates the publisher beyond the platform's audience check nor binds the message to the caller (A9 D8); whether an ordinary tenant user can obtain that token is to be tested in phase 0." | as PC14 |
| PC19 | `02:718` (compatibility row "QR gateway") | Add to the contract cell: "hub `printerhub`; POST `/api/negotiate` and POST `/api/send`; bearer token for `api://<client id>`; routing key is the `realm` field of the sent body." | `API/src/functions/printerhub.js:6`, `:24`; `API/src/functions/send.js:11`, `:17-19` |
| PC20 | `03:341` and `05:110` (licence service assumed Datasec-hosted; customer-hosted as new work) | "A deployable licence server already exists as a second Marketplace offer (SQLite, multi-tenant sign-in; report A9 L7 to L13); who is meant to deploy it is a question for the product owner, and option (b) is cheaper than this line assumed." | `MKT/license/main.bicep:160-243` |
| PC21 | `02:716` (reporting compatibility row) | Add: "the accepted columns are fixed by the customer's data collection rule: 17 for job statistics, 3 for supplies; the rule replaces the record time with the arrival time." | `MKT/bicep/main.bicep:474-503`, `:457`, `:463` |
| PC22 | `02:750` (first-run test page) | "the test page reports SignalR and Log Analytics as 'not configured' when their settings are empty: both are optional and off by default in the Azure offer." | `MKT/artifact/createUiDefinition.json:116`, `:287` |

22 proposed corrections: 7 in `05` (PC1 to PC7), 5 in `03` (PC8 to PC12), 9 in `02` (PC13 to PC19, PC21, PC22), 1 spanning `03` and `05` (PC20).

## 9. Open questions for the product owner (each with the default taken if unanswered)

1. **Question 10, now with its fact:** the gateway does not check who sends an unlock message. Is QR sign-in without MFA offered on OXPd printers? Default: as Workpath, risk recorded (the documents' current default). Recommendation: switch it off on OXPd until the gateway is fixed.
2. **The phone app's source (HP Secure Authentication), or leave to capture a sign-in in the test tenant.** The gateway forwards the message without reading it, so the message shape is known only from the printer's side. Default: capture it in the phase-0 tenant.
3. **`cc-api`: is it the legacy Keycloak-mode API (`CypherConnectAPI`), and is it therefore out of scope under your ruling that no OXPd customer is on the legacy back end?** Default: yes, not needed, not asked for again.
4. **Who deploys the licence-server Marketplace offer: Datasec only, or partners and customers too?** It decides whether an OXPd server must expect a licence server at a host other than Datasec's. Default: Datasec-hosted only, as the documents assume.
5. **How many customers deployed the Azure side by the script and how many by the Marketplace offer?** It decides how a gateway change reaches them. Default: both exist; every gateway change ships with both an offer version and a script.
6. **Is `v1.3.0` the package live in the Marketplace today?** The built offer zips are not in the repository. Default: yes.
7. **Were the App Configuration access keys in the committed Terraform state backup rotated?** (S1.) This is a housekeeping question for whoever owns `infra_hpam`, not an OXPd design question. Default: treated as live; never opened, never copied.

## 10. What was NOT read

- **Not sent, so not read:** `cc-api`; the phone app; the licence server's source for the Marketplace offer (only its deployment template); the built offer packages (`hpam-azure-*.zip`).
- **`hpam-api`:** `deploy/hpam-api.zip` was listed (324 entries) but its `node_modules` content was not opened; its three function files, `host.json` and settings file were hash-compared with the loose source and match. `package-lock.json` integrity strings were masked, not read.
- **`hpam-marketplace`:** the two compiled `mainTemplate.json` files were parsed for parameters, variables, resource types and outputs and NOT read line by line or diffed against a fresh build of the Bicep (no build was run), so "the compiled template matches the Bicep" is checked only at the level of the resource list and the `apiVersion` variable. The base64 package embedded at `artifact/mainTemplate.json:156` was not decoded. The help article linked from the wizard was not fetched.
- **`infra_hpam`:** `hpam/terraform.tfstate.backup` was read as structure only (names and lengths), never its values; `hpam/workbook.tf` was read for its resource lines and query lines only (cut at 220 characters), not whole; `.terraform.lock.hcl` hashes not read; the Keycloak theme (`login/theme.properties`, the CSS, all images, `welcome/index.ftl` beyond its title line) not read; `hpam/modules/vnet/variables.tf` not read; lines longer than 400 characters in the Terraform files were dropped from my display (none of the lines cited above).
- **Project documents:** `02`, `03` and `05` were read by a keyword search (gateway, SignalR, negotiate, Keycloak, phone, QR, OQ-7, Function App, licence server, Log Analytics, Marketplace and variants) and by the specific lines cited, NOT whole; a statement about the gateway phrased without any of those words would have been missed. Reports A1, A2, A5 and A6 were consulted by the same kind of search, not re-read. `CLARIFICATIONS.md` was read for C-27, C-33 and C-40 only. `review/B1757_APPLIED.md` and `review/B1760_APPLIED.md` were not read. Reports A3, A4, A7, A8, B1 to B3, C1 and C2 were not opened.
- **Nothing was run or tested.** Every statement about run-time behaviour (what App Service authentication admits, how the SignalR binding addresses a message, token lifetimes) is a reading of configuration and code plus general knowledge of those Azure services; the items marked "inferred" in 6.3 and "general knowledge" in 7.2 need a test in the phase-0 tenant.
- **Lane O's tree (`OXPd1_solution-master`) was not touched.**
