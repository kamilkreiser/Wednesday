# A5: Back end, licensing, administration and deployment source

Lane A5 of the Datasec OXPd analysis, 2026-11-18. Library root: `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`.

Path shorthand used in every citation: `SC/` means `HPAM - Docs and Notes/Source Code/` under the library root. So `SC/License-Services-main/src/License.Portal/Program.cs:25` is relative to the library root. No secret value appears in this report; section 8 lists locations only.

---

## 1. BLUF

This lane holds three .NET repositories that sit behind the Workpath suite (a licence service, an internal Datasec administration portal and a Windows fleet-deployment utility) plus two repositories that are not part of the printer suite.

1. **The licence is per Entra tenant with a device-count cap and an expiry date. It is not per app and not per platform.** A device is identified by its serial number alone, and the licence server registers serials first come, first served. A mixed fleet already fits under one licence with no schema change (finding 4.1.4, 4.1.6).
2. **Deployed Workpath devices never read the licence file.** They only check a short signed answer from `POST /api/validate` against a pinned root certificate. The licence format can therefore gain claims (platform, app set, server seats) without touching devices in the field (4.1.7).
3. **The licence core is a plain .NET library** (`License.Common`, net10.0) that a .NET OXPd server can reference directly. An OXPd server would call the same endpoint once per printer it drives (4.1.2, 5.1).
4. **The "Administration Portal" does not administer devices, licences or app configuration.** It automates legacy Keycloak onboarding and Azure Marketplace SaaS subscriptions. There is no single admin view today: tenants and devices live in the licence portal, deployment state lives in a local SQLite file on a technician's PC (4.2, 4.3.6).
5. **The deployment utility is a wrapper around HP's `HPKTool-cli.exe`** driven by a typed list of printer IP addresses and one shared device admin password. Nothing in it applies to OXPd except its job, task, retry and results model. The customer-hosted Azure pieces (SignalR, Function App, Log Analytics) have no code or templates in these five repositories (4.3, 4.5).

---

## 2. Coverage

| Repository | Files | Read whole | Sampled | Not opened |
|---|---|---|---|---|
| `License-Services-main` | 145 | 57 (all of `License.Common`, `License.Portal.Data`, portal services, controller, middlewares, page models, generator `MainForm.cs`, 3 workflows, both READMEs, certificates readme, LINQPad script, SQL Server migration, 1 of 6 test files) | `Devices.cshtml` lines 10 to 75, `DbMigration.cshtml` lines 1 to 12 | 8 `.pem` and 2 `.bin` files (deliberately: key material), SQLite migration, 5 test files, remaining `.cshtml` views, 4 page scripts, designer and `.resx` files, vendored jQuery, images |
| `HPK-Deployment-Utility-main` | 139 | 21 (`Worker.cs` all 1,070 lines, worker `Program.cs`, 6 utilities, `HpkServices`, `AppSettingsServices`, `DatabaseProvider`, initial migration, 6 models and enums, release workflow, build props, tools readme) | `DeploymentJobForm.cs` (keyword search plus lines 449 to 460 and 1262 to 1312), 4 other forms by keyword search, 2 migrations in part, HP's HPKTool user guide PDF (text extracted to scratch, 1,009 lines, read by section) | 9 repositories, 6 services, extensions, entities, designer and `.resx` files, 4 binaries |
| `Datasec-Administration-Portal-main` | 629 | 23 (`Program.cs`, `appsettings.json`, `Constants.cs`, `AppRoles.cs`, 4 controllers, 7 handlers, `IKeycloakClient`, `DataContext`, 2 DTOs, 2 filters and converters, workflow, README) | `ApplicationOnboardingExecuteCommandHandler.cs` lines 1 to 254 of 306, 3 pages in part, authorization attributes of all 27 pages by search, full file-name inventory of handlers, models, controllers and 63 migration names | 127 migration files (names only), about 70 handlers, all validators, mappers, view models, Vue components, scripts |
| `Datasec-Security-Composer-main` | 974 | 1 (`README.md`) | term counts across the tree | everything else, by decision (not the printer suite) |
| `attio-main` | 87 | 1 (`CLAUDE.md`) | term counts and the 8 matching lines | everything else, by decision (not the printer suite) |

Outside the lane, read because the lane asks how a device obtains and renews a licence: `SC/HPAuthenticationManager-main/app/src/main/java/com/hp/print/hpauthenticationmanager/license/` (4 files, whole), `.../model/AppInitialization.kt` lines 78 to 92 and 270 to 420 of 630, `SC/HPAuthenticationManager-main/config.properties` line 25, `.../app/moc_file/config.cfg` lines 349 to 359. The lane that owns that repository should be treated as authoritative for anything else in it.

Nothing was built, run or unpacked in the library. The one extraction (the HPKTool PDF to text) went to the session scratchpad.

---

## 3. Inventory

| Component | Language and framework | Version in source | Entry point | Packaging |
|---|---|---|---|---|
| License.Portal | C#, ASP.NET Core Razor Pages plus one API controller, EF Core, Tailwind, htmx-style partials | 2.3.0.0, `net10.0` (`SC/License-Services-main/src/License.Portal/License.Portal.csproj:4,8`) | `Program.cs` | `dotnet publish`, Azure App Service |
| License.Common | C# class library | 1.0.0.0, `net10.0` (`.../License.Common/License.Common.csproj:4,9`) | n/a | project reference |
| License.Generator | C# WinForms desktop app titled "HPAM License Manager" | 1.38.0, `net10.0-windows` (`.../License.Generator/License.Generator.csproj:4,10`; title at `Forms/MainForm.cs:82`) | `Program.cs` | self-contained single-file `win-x64` exe, zipped to a GitHub release |
| License.Portal.Data, two migration assemblies | EF Core, SQL Server and SQLite | one migration each, dated 2026-03-30 | n/a | project reference |
| License.Common.Tests | xUnit | n/a | n/a | not run by any workflow in the repo |
| HpkDeployment.ClientApp | C# WinForms | 3.0.0, `net10.0-windows` (`SC/HPK-Deployment-Utility-main/Directory.Build.props:3,7`) | `Program.cs` | self-contained single-file exe in a `.7z` GitHub release |
| HpkDeployment.Worker | C# generic host `BackgroundService`, started as a child process, not a Windows service | 3.0.0 | `Program.cs` | same archive |
| HpkDeployment.Infrastructure and Repository | SQLite, FluentMigrator, 7 migrations from 2025-05-23 to 2026-01-12 | n/a | n/a | n/a |
| `external_tools/` | HP `HPKTool-cli.exe`, Android `adb.exe` and two DLLs, HP's HPKTool User Guide v1.6.2 | tool 1.6.2 dated 2023-10-01 per the guide | n/a | copied to `tools/` in the release |
| DatasecAdministrationPortal | C# ASP.NET Core (Razor Pages, API controllers, MediatR, FluentValidation, Refit, EF Core SQL Server), Vue 3 front end | `net10` per README (`SC/Datasec-Administration-Portal-main/README.md:5`) | `Program.cs` | `dotnet publish`, Azure App Service |

---

## 4. Findings

### 4.1 Licensing

#### 4.1.1 Trust chain and key material

There are two key pairs and one per-licence key pair (`SC/License-Services-main/certificates/readme.md:19-63`):

| Asset | Held by | Use |
|---|---|---|
| Root private key | License.Generator only, embedded in the exe | signs every licence JWT and issues the per-licence tenant certificate |
| Root certificate | Generator, portal, and every device as `hpauthsuite_root.pem` in the Android app assets | verifies licences and tenant certificates |
| API certificate (public) | Generator | encrypts the tenant private key into the licence |
| API private key | Portal only, embedded resource | decrypts the tenant private key at validation time |
| Tenant key pair and certificate | generated per licence, RSA 2048, certificate signed by the root, valid until licence expiry | the portal signs each validation answer with it |

The readme says the root certificate file and the device's `hpauthsuite_root.pem` have the same content (`certificates/readme.md:27`). I did not open either file to confirm.

#### 4.1.2 What a licence is

A licence is a JWT, RS256, signed with the root key, gzip-compressed and saved as `<tenantId>.lic` (`.../License.Generator/Forms/MainForm.cs:187-188,262-282,299`; `.../License.Common/Utils/Compression.cs:8-17`).

| Claim | Meaning | Source |
|---|---|---|
| `iss` and `aud` | both the fixed string "Datasec Pty Ltd" | `License.Common/Utils/LicenseClaims.cs:8`, `LicenseValidator.cs:24-27` |
| `hpam:name` | company name | `LicenseClaims.cs:12` |
| `hpam:domain` | host name of the licence server this licence may be uploaded to | `LicenseClaims.cs:13`, check at `License.Portal/Services/LicenseUploadService.cs:40` |
| `hpam:tenantId` | customer's Entra tenant GUID | `LicenseClaims.cs:14` |
| `hpam:maxDevices` | device cap, must be above zero | `LicenseClaims.cs:15`, `MainForm.cs:160` |
| `hpam:licenseType` | Customer 1, Free 2, NFR 3, POC 4, Rental 5 | `License.Common/Enums/LicenseType.cs:4-11` |
| `hpam:tenantCert` | tenant certificate PEM | `MainForm.cs:274` |
| `hpam:metadata` | base64 JSON: `Key` is the tenant private key as a JWE (RSA-OAEP, A256GCM) for the API key; `Version` is the first 8 bytes of the SHA-256 of the API certificate | `MainForm.cs:252-259` |
| `exp` | last second of the month before the month picked in the UI | `MainForm.cs:172-174` |

The generator will not issue a licence that expires in less than about two months: the date picker's minimum is the first day of the month two months ahead (`MainForm.cs:43-44`).

What is licensed, then: **one Entra tenant, up to N devices, until a date.** There is no claim for an app, a feature, a device model, a platform or a version. The licence type is stored and shown but no code path in this repository branches on it (`TenantDeviceService.cs:10-56` uses only `ExpiresAt` and `MaxDevices`).

#### 4.1.3 Issuing and loading a licence

1. A Datasec employee runs the generator, types company, tenant id, licence server domain, device count, type and expiry month (`MainForm.cs:139-180`). The domain field defaults to `license.hpauthsuite.com` (`.../Forms/MainForm.Designer.cs:75`).
2. The file is saved locally and, if the box is ticked, posted as multipart form data to `https://{domain}/api/upload` with no credentials (`MainForm.cs:204-206,314-328`).
3. `POST /api/upload` is `[AllowAnonymous]` (`License.Portal/Controllers/LicensingController.cs:143-144`). The portal accepts the file if the signature and lifetime validate against the root certificate, the tenant id in the form matches the claim, **the `hpam:domain` claim equals the request's Host header**, and it has not expired (`LicenseUploadService.cs:28-43`).
4. The licence is upserted by tenant id. If the tenant now has more registered devices than the new cap, the devices seen least recently are deleted (`LicenseUploadService.cs:45-65`).
5. A customer can also upload a licence file for their own tenant through the portal page (`License.Portal/Pages/Devices/Devices.cshtml.cs:103-140`).

There is no link in code between a sale and a licence. The generator is a manual desktop tool, and the administration portal's Marketplace code never calls the licence service (search for "license" in the administration portal's `.cs`, `.cshtml`, `.vue` and `.js` files returns one hit, a UI label string in a seed migration; the same search for "keycloak" returns 807).

#### 4.1.4 How a device obtains, validates and renews

Server side (`LicensingController.cs:18-141`, `TenantDeviceService.cs:10-56`, `Utils/LicenseTokenUtils.cs:22-86`):

1. Device posts `{ serial, tenantId, nonce }` to `POST /api/validate`, anonymous.
2. Portal loads the tenant's licence, validates signature, issuer, audience and lifetime with 30 seconds of clock skew.
3. If `(tenantId, serial)` is already registered: update `LastSeen`, answer valid.
4. If not registered: answer invalid when the licence is expired or the tenant's device count has reached `maxDevices`; otherwise insert the device and answer valid. **Registration is automatic on first contact.**
5. Portal decrypts the tenant private key from the licence metadata with the API key, checks it matches the tenant certificate, and returns `{ token }`: a JWT signed RS256 by the tenant key, with the tenant certificate in the `x5c` header and three claims, `serial`, `nonce`, `valid`.

Device side (`SC/HPAuthenticationManager-main/.../license/LicenseCheckRunner.kt:40-143`):

1. Serial comes from the Workpath SDK device attribute `DA_SYSTEM_SERIALNUMBER`, with the literal fallback "NoSerial" if the read fails (`.../model/AppInitialization.kt:110-122`). Tenant id comes from the app configuration (`AppInitialization.kt:359-366`). The URL is the configured `licenseEndpoint` plus `/api/validate` (`AppInitialization.kt:84-86`); the shipped default is `https://license.hpauthsuite.com` (`SC/HPAuthenticationManager-main/config.properties:25`, `.../app/moc_file/config.cfg:352-359`).
2. The device validates the `x5c` chain to the pinned root with PKIX, revocation off, verifies the token signature with the leaf key, compares the nonce, and reads `valid` (`LicenseCheckRunner.kt:89-135`).
3. Outcome: valid gives `Licensed`; invalid gives `Unlicensed` with the message "Reached license limit"; any exception or any response without a token gives `TempLicense` (`LicenseCheckRunner.kt:71-83,129-142`).

Renewal is polling, not a renewal protocol (`AppInitialization.kt:309-313`):

| State | Recheck interval |
|---|---|
| Licensed | every 24 hours |
| TempLicense | every hour |
| Unlicensed | every 15 minutes |

A new licence takes effect on a device at its next poll; nothing is pushed.

#### 4.1.5 Offline behaviour

- A device that cannot reach the licence server, or gets any non-token answer, moves to `TempLicense` and keeps working (`LicenseCheckRunner.kt:138-142`).
- `TempLicense` lasts 20 days from the first failure, then becomes `Unlicensed` (`license/LicenseInfoStore.kt:60-80`).
- A device with no stored state at all reads as `TempLicense` (`LicenseInfoStore.kt:36-38`), so a fresh install works for up to 20 days without ever reaching the server.
- `Unlicensed` cannot fall back to `TempLicense` (`LicenseInfoStore.kt:82-87`), so an unlicensed device cannot regain service by going offline.
- `Unlicensed` with a recorded check blocks initialisation with a "no licence" failure state (`AppInitialization.kt:292-300,376-382`).
- The licence state is kept in an Android DataStore on the device (`LicenseInfoStore.kt:23-31`). Only HP Authentication Manager checks the licence: a search for "license" in the Kotlin and Java sources of MailFlow, Teams, OneDrive, Universal Print and the common library returned only open-source notice screens and a vendored photo-view library. The other apps are gated through their dependence on Authentication Manager (inferred).

#### 4.1.6 Data model and storage

Two tables (`License.Portal.Migrations.SqlServer/Migrations/20260330034002_InitialCreate.cs:14-54`):

| Table | Columns | Key |
|---|---|---|
| `TenantLicense` | `TenantId`, `LicenseKey` (the compressed licence bytes), `CreatedAt`, `UpdatedAt`, `CompanyName`, `Checksum` (the expiry in ticks, named for obscurity per `Entities/TenantLicense.cs:11`), `LicenseType` | `TenantId` |
| `TenantDevice` | `SerialNumber`, `TenantId`, `CreatedAt`, `LastSeen` | `(SerialNumber, TenantId)`, foreign key to `TenantLicense` with cascade delete |

A device row carries nothing but a serial and two timestamps: no model, no IP, no app version, no platform. Tenant ids are lower-cased on write (`License.Portal.Data/DataContext.cs:13-22`).

The provider is SQL Server by default or SQLite by configuration (`License.Portal/Program.cs:20,45-67`, `appsettings.json:10-14`), and a maintenance page copies all data from one to the other after wiping the destination (`Services/DbMigrationService.cs:39-106`). The schema is migrated at every start-up (`Program.cs:116-120`).

#### 4.1.7 What the device does and does not depend on

The device depends on four things only: the endpoint path, the request shape, the three token claims, and the pinned root certificate. It never parses the licence JWT. So the licence claims, the database schema and the portal can all change without a Workpath app release, as long as `/api/validate` keeps answering in the same shape.

#### 4.1.8 The licence portal as an administration surface

- Sign-in is Microsoft Entra, multi-tenant (`TenantId` is `common`, `appsettings.json:2-9`; `Program.cs:25-26`). All Razor pages require authentication (`Program.cs:111-112`).
- A Datasec operator is a user whose tenant equals the configured home tenant and whose username matches a pattern for Datasec mail domains (`Services/UserService.cs:18-26`, `Extensions/RegexExtnesions.cs:7`). Operators see every tenant: filter by type, name and expiry, export a CSV in a zip, delete licences, and drill into any tenant (`Pages/Tenants/Tenants.cshtml.cs:36-105`).
- Anyone else is scoped to their own tenant id from the token (`Middlewares/TenantContextMiddleware.cs:13-22`) and sees company name, expiry, days left, device cap, active device count, and the device list with serial and last-seen. They can delete devices to free seats and upload a licence file (`Pages/Devices/Devices.cshtml:26-45,62-70`; `Devices.cshtml.cs:82-140`).
- There are no app roles. Any user of the customer's tenant who can sign in gets that view (inferred from the absence of any role check in the page models read).

### 4.2 The administration portal

Its name suggests more than it does. Read from its controllers, handlers and data context, it has four jobs, none of which is device or licence management.

**Job 1: legacy Keycloak onboarding.** An operator enters customer name, a reference number, the customer's OpenID configuration URL, client id, client secret and secret expiry, for one or more "environments" (regions). The portal then runs eleven steps against a Datasec-hosted Keycloak through its admin REST API (`Constants.cs:265-278`; `Handlers/Onboardings/ApplicationOnboardingExecuteCommandHandler.cs:108-197`; `HttpClients/IKeycloakClient.cs:15-82`):

1. create a realm named after the reference number;
2. enable user events;
3. to 7. copy and edit the "first broker login" authentication flow so accounts merge automatically, and set the browser flow to redirect to the identity provider;
8. create two clients, `HP-Authentication-Manager` (confidential, service account, refresh tokens) and `HP-Secure-Authentication` (public, with the redirect URI `com.hp.hpauthenticationmanager://oauth2redirect`) (`Handlers/Onboardings/Steps/ClientsCreateCommandHandler.cs:35-62`);
9. switch off client host and IP claims on the first client and read back its secret;
10. create an OIDC identity provider pointing at the customer's Entra app registration;
11. enable the realm.

On success it emails a template containing the API base URL (environment API URL plus reference number), client id, the Keycloak client secret, an App Centre key, authorisation, token and redirect URLs (`ApplicationOnboardingExecuteCommandHandler.cs:204-236`). The library's own briefing says version 4 stores credentials in Entra Custom Security Attributes and that Keycloak is the legacy path (`START-HERE.md:53`), and the device app still carries both branches (`AppInitialization.kt:383-387` in the range read). So this onboarding tool serves the legacy back end.

**Job 2: Azure Marketplace SaaS subscriptions.** A landing page for the Marketplace purchase flow, a webhook receiver, activation, plan change, unsubscribe, a periodic refresh, and capture of the buyer's HP partner and account manager (`Controllers/Saas/SaasController.cs:14-91`, `Controllers/Saas/SaasPortalController.cs:17-189`, `Handlers/SaaS/SubscriptionActivateCommandHandler.cs:29-92`, `Pages/Saas/SaasApp.cshtml:23-75`). A `/rentals` page gives an HP partner the steps for a "Software Add-On for Rented HP Printers", and tells the partner they will receive details to configure "HP Command Centre Printer settings" (`Pages/Saas/Rentals.cshtml:22-70`). Activation calls the Marketplace fulfilment API and updates a local row; it does not create a licence (`SubscriptionActivateCommandHandler.cs:36-78`).

**Job 3: email.** Templates, sending through Azure Communication Services, delivery-report webhooks and a resend log (`Program.cs:147-153`; handler names under `Handlers/Emails`, `EmailDeliveries`, `EmailDeliveryReports`).

**Job 4: settings.** Environments (name, API URL, App Centre key, production flag, linked Keycloak), Keycloak instances (name, realm, URL, admin user; the password is held in Key Vault, inferred from the `KeyVaults` handlers and `Constants.cs:157`), UI resource strings and page templates (`Models/DTOs/EnvironmentDto.cs:15-23`, `Models/DTOs/KeycloakDto.cs:16-22`).

| Aspect | Finding | Source |
|---|---|---|
| Users | Datasec staff with app role `Admin`; a `Customer` role that may use the onboarding page and see its own onboarding log; Marketplace buyers through a separate sign-in | `Infrastructure/AppRoles.cs:5-7`, `Program.cs:127-145`, `Pages/Onboarding/Index.cshtml:4` |
| Auth | two Entra OIDC schemes: single-tenant for staff with role claims, multi-tenant for Marketplace buyers with forced consent on `/saas-app` | `Program.cs:61-119`, `appsettings.json:5-22` |
| Webhooks | five anonymous endpoints guarded by a shared code in the query string | `Controllers/WebhooksController.cs:14,30-117` |
| Data store | SQL Server through EF Core, soft delete on every entity, selected columns encrypted with a configured key, migrations applied at start-up outside development | `Program.cs:196-210,250-258`, `Repositories/DataContext.cs:22-67` |
| Azure dependencies | Key Vault, Communication Services email, Azure Resource Manager client, Application Insights, Microsoft Graph, Marketplace SaaS API | `Program.cs:34,82,147-153,238-246` |
| What it does not hold | no table or handler for devices, serials, licences, app configuration or printers | entity list at `DataContext.cs:47-65`; 63 migration names reviewed |

### 4.3 The HPK deployment utility

#### 4.3.1 What HPK is

An HPK is HP's package format for a Workpath app: a zip holding `hpk.xml` (with a UUID and name) and an Android APK, which HP must verify and sign before it installs on a device. HP's own tool for building, installing and configuring them is HPKTool (HP's HPKTool User Guide v1.6.2 in `SC/HPK-Deployment-Utility-main/external_tools/`, introduction and menu sections; HP confidential, described not quoted). The utility reads the UUID and name from `hpk.xml` and the version code from the APK manifest (`src/HpkDeployment.Common/Services/HpkServices.cs:33-70,83-95`).

#### 4.3.2 What the utility is

"HPK Deployment Utility" v3.0.0 is a Windows desktop app plus a background worker process that queue and run HPKTool command lines across a list of printers (`src/HpkDeployment.Common/Utilities/WorkerServiceUtils.cs:11-34`, `src/HpkDeployment.Worker/Worker.cs:16-69`). The desktop app starts and stops the worker by process name and by dropping `stop.signal` and `inprogress.signal` files beside the executable (`Utilities/ResourcesUtils.cs:16-19`). Everything is local to one PC: SQLite database `dsdm_wp.db` beside the exe (`src/HpkDeployment.Infrastructure/DatabaseProvider.cs:10-15`).

#### 4.3.3 Data model

| Entity | Content | Source |
|---|---|---|
| Job | name, one printer admin password (encrypted blob), a free-text list of printer IPs split on commas and line breaks | `Migrations/M2025052301_InitialDatabase.cs:10-14`, `Worker.cs:1040-1046` |
| Hpk | UUID, version, name, file name, the whole file as a blob | `Migrations/M2026011201_AddHpkVersion.cs:17-27` |
| JobApp | an HPK in a job, with an attestation JSON, a configuration JSON, and a sequence | `M2025052301_InitialDatabase.cs:22-30` |
| JobTask | what to run for a job: HPK option (ignore, install, uninstall), clear-config flag, install attestation, install configuration, status, sequence | `M2025052301_InitialDatabase.cs:32-41`, `Enums/HpkOption.cs:3-8` |
| Deployment, DeploymentApp, DeploymentResults, DeploymentLog | one run of a task, with per-IP, per-app attempt counts and success flags, and a log | `M2025052301_InitialDatabase.cs:43-78` |
| AppSettings | HP developer username, LDB service key (encrypted), concurrency (default 10), maximum retries (5), retry delay (1 minute), timeout (5 minutes) | `M2025052301_InitialDatabase.cs:81-88`, `M2025062601_UpdateAppSettings.cs` |

#### 4.3.4 How apps and configuration reach a printer

The worker polls every five minutes for pending tasks (`Worker.cs:25,46-52`). For each device, for each app in sequence, it runs up to three HPKTool commands (`Worker.cs:753,784,812,840`):

| Step | HPKTool command | Arguments supplied |
|---|---|---|
| Install | `--install` | HPK file path, `--host <ip>`, `--password <admin password>`, plus `--force` when "clear config" is set |
| Uninstall | `--uninstall` | `--uuid`, host, password |
| Attestation | `--attestation-update` | `--uuid`, host, password, `--username` and `--ldbkey` from settings, `--credentials "<JSON>"` |
| Configuration | `--config-update` | `--uuid`, host, password, `--data "<JSON>"` |

Other facts:

- **Protocol to the device:** not visible in this repository. The utility only launches `HPKTool-cli.exe`; the transport is inside HP's binary. HP's guide documents the same `--host` and `--password` parameters as device IP and device admin password. `adb.exe` is required to be present (`Worker.cs:71-87`) but the utility never invokes it; HP's guide says the attestation update uses `adb` in "Link Debug Mode" (guide section 10).
- **Device discovery:** none. IPs are typed or pasted. Online detection is a TCP connect to port 9100 or 631 with a two-second timeout (`Utilities/PrinterUtils.cs:11-28`).
- **Device admin credential:** one password per job, applied to every printer in the job, passed on the command line (`Worker.cs:176,753`).
- **Result parsing:** by substring of HPKTool's console output. "please check password" is fatal and stops the whole deployment for every device; "not found" skips the app on that device; "error", any stderr line or a non-zero exit code is a retryable failure (`Worker.cs:877-909,924-932`, `Worker.cs:590-593`).
- **Fleet behaviour:** up to N devices in parallel, per-device retry with delay, offline devices retried then abandoned after the retry limit (`Worker.cs:368-411,426-449`).
- **What is configured on each device:** per app, an "attestation" JSON and a "configuration" JSON chosen by the operator from `.cfg`, `.json` or `.txt` files (`DomainModels/FileFilter.cs:13`). HP's guide gives the attestation payload as a JSON array of client id and client secret pairs, and describes the command as updating client credentials for the "App Attestation Debug Flow". The configuration JSON is the app's own settings document; its keys belong to the app repositories, not this lane.
- **Portability of a job:** export to a `.dsjb` zip holding the HPK files and a `.dsmfst` manifest (job name, admin password, IPs, attestation and configuration data), encrypted with the utility's built-in key in release builds and written in clear in debug builds (`Forms/DeploymentJobForm.cs:452-454,1262-1278`).

#### 4.3.5 Relation to HP Command Center and other HP fleet tools

The utility has no integration with HP Command Center, Web Jetadmin or any HP cloud service: a search for "command cent" across this repository and the licence repository returns 0, against 51 hits for the control term "hpktool" in the same tree. It is a direct-to-device, on-LAN alternative to them. The only mention of HP Command Center in this lane is the rentals page in the administration portal, which tells HP partners they will be sent details to configure printer settings there (`SC/Datasec-Administration-Portal-main/src/DatasecAdministrationPortal/Pages/Saas/Rentals.cshtml:65`). So two deployment routes exist: Command Center for partners, this utility for direct LAN roll-outs (inferred; the documentation lanes should confirm).

#### 4.3.6 A note left by the developers

The database was renamed from `dsdm.db` to `dsdm_wp.db`, with a code comment saying the suffix avoids confusion with any future "deployment manager" applications, naming OXPd as the example (`src/HpkDeployment.Infrastructure/DatabaseProvider.cs:9-11`). The team already expects an OXPd sibling of this tool.

### 4.4 Hosted endpoints and environments named in this lane

| Name | What | Environment | Source |
|---|---|---|---|
| `https://license.hpauthsuite.com/` | licence portal and API | production, App Service `au-hpam-license` | `SC/License-Services-main/.github/workflows/build-test-deploy.yml:96-110` |
| `https://dev-hpam-license.azurewebsites.net/` | licence portal and API | dev, App Service `dev-hpam-license` | same file, lines 74-88 |
| App Service `hpam-admin-portal` | administration portal | production (URL not in source) | `SC/Datasec-Administration-Portal-main/.github/workflows/build-test-deploy.yml:92-97` |
| App Service `dev-hpam-admin-portal` | administration portal | dev | same file, lines 70-76 |
| `/api/validate`, `/api/upload`, `/healthcheck`, `/api-docs/errors`, `/errors/{category}/{type}` | licence portal routes | both | `LicensingController.cs:18,143`; `License.Portal/Constants.cs:28`; `Pages/ApiDocs/README.md:17-32` |
| `/api/onboarding`, `/api/saas`, `/api/saas-portal`, `/api/saas/webhook`, `/webhooks/email-delivery-event`, `/webhooks/email-delivery-job-execution`, `/webhooks/onboarding-cleanup`, `/webhooks/saas-refresh`, `/saas-app`, `/rentals`, `/healthcheck` | administration portal routes | both | controllers and pages cited in 4.2 |
| `https://login.microsoftonline.com/` | Entra authority | n/a | both `appsettings.json` files |
| Keycloak instances and per-region "environment" API URLs | legacy back end | stored in the portal database, not in source | `Models/DTOs/EnvironmentDto.cs`, `KeycloakDto.cs` |
| `*.hpauthsuite.com`, `*.datasec.com` | subject names used when the root and API certificates were generated | n/a | `SC/License-Services-main/certificates/Create Certificates.linq:15-16` |

The error `type` URIs in API responses use the placeholder host `license.portal`, not the real host (`LicensingController.cs:29`).

### 4.5 Customer-hosted Azure pieces

**Not found in this lane.** Search: case-insensitive, text files only, across `License-Services-main`, `Datasec-Administration-Portal-main` and `HPK-Deployment-Utility-main`, excluding `node_modules`.

| Term | Hits |
|---|---|
| `signalr` | 0 |
| `log analytics`, `loganalytics` | 0, 0 |
| `bicep`, `terraform`, `Microsoft.Web/sites` | 0, 0, 0 |
| `functionapp` | 0 (`function app` gave 1, a jQuery function named `appendModelPrefix`) |
| control: `keycloak` | 818 |
| control: `hpauthsuite.com` | 11 |

A file-name search for `*.bicep`, `*.tf`, `azuredeploy*`, `*.arm.json`, `Dockerfile*`, `*.ps1` and `*.sh` in the same three repositories returned only the two EF migration helper scripts. The SignalR and Function App gateway and the Log Analytics ingestion described in `START-HERE.md:54-55` must be sought in the app repositories and the help-portal documents, which belong to other lanes.

### 4.6 CI/CD

| Repository | Workflow | Trigger | What it does | Source |
|---|---|---|---|---|
| License-Services | License Portal Deploy | push or PR to `main` touching portal or common code, or manual | bumps the minor version and commits it, npm build, `dotnet build` and `publish`, deploys to dev, then to production on `main`, using publish-profile secrets | `.github/workflows/build-test-deploy.yml` |
| License-Services | Build license generator | push or PR to `main` touching generator or common code | builds on Windows, tags a release, patches the version, publishes a self-contained single-file exe, attaches a zip to the GitHub release | `.github/workflows/build-generator.yml` |
| HPK-Deployment-Utility | Release Build | every push to `main` | publishes client and worker as single-file `win-x64`, copies `external_tools` to `tools`, makes a `.7z`, creates a GitHub release tagged with the version in `Directory.Build.props` | `.github/workflows/release.yaml` |
| Administration Portal | Build, Test and Deploy | push or PR to `main`, or manual | tags a release, npm install, build, publish, writes `version.txt`, deploys to dev then production on `main` | `.github/workflows/build-test-deploy.yml` |
| all three | Gitleaks Scan, Dependabot for GitHub Actions with a five-day cooldown | push and PR | secret scan | `gitleaks.yml`, `dependabot.yml` |

No workflow in the licence repository runs the unit tests, despite the workflow file name. Production deploys follow dev automatically on a push to `main`; whether a GitHub environment approval gate sits in front of production is repository configuration and not visible here.

### 4.7 The two other repositories

**`Datasec-Security-Composer-main`** is "Policy Composer", a multi-tenant web application that turns an engagement's answers into an HP Security Manager policy and its documents (`SC/Datasec-Security-Composer-main/README.md:1-8`). It is TypeScript on Node 22 with React, PostgreSQL and a small .NET bridge, at an early harness phase, local-only by rule. It has 0 occurrences of "workpath", "oxpd" or "hpk". Its 33 occurrences of "authentication manager" are all in four policy-content JSON files, where printer security settings are named. It is a separate Datasec product about printer security policy and has nothing to do with the authentication suite's run time, licensing or deployment. No further time was spent.

**`attio-main`** is a Datasec internal sales-operations project: adopting the Attio CRM and migrating the Vision Sales Portal's flows into it (`SC/attio-main/CLAUDE.md:9-19`). Its eight "workpath" hits are sales email templates and CRM attribute names. It contains no product code. One thing is worth knowing from it: Datasec's sales scoping records fields named for Entra MFA, HP Command Center tenanting, Conditional Access, Universal Print and Workpath (`SC/attio-main/2_Project_Files/src/migration/attributes.js:212`), which is the pre-sales checklist an OXPd offer would extend. No further time was spent.

---

## 5. What this means for the port

### 5.1 Reusable as is

| Part | Why it carries over | Finding |
|---|---|---|
| Licence format, generator, root and tenant key design | nothing in it is Workpath-specific; the unit is tenant plus device count | 4.1.2 |
| `License.Common` (`LicenseValidator`, `LicenseClaims`, `Compression`) | plain .NET library; a .NET OXPd server can reference it to read a licence or verify a validation token | 4.1.2, 3 |
| `POST /api/validate` protocol | the caller needs only a tenant id, a serial and a nonce; an OXPd server can make the call for each printer it drives | 4.1.4 |
| Licence portal tenant and device pages | a device registered by an OXPd server appears in the same list and counts against the same cap | 4.1.6, 4.1.8 |
| Marketplace SaaS and email machinery in the administration portal | commercial plumbing, independent of device platform | 4.2 |
| Deployment utility's job, task, retry, per-device result and log model, and its UI | platform-neutral; only the command execution layer is HPKTool | 4.3.3, 4.3.4 |

### 5.2 Must change because the solution moves to a server

1. **Who performs the licence check.** Today each printer checks for itself daily and stores the result on the device (4.1.4, 4.1.5). On OXPd the server must check on behalf of each printer and hold the state. Requirement: the server obtains each device's serial through OXPd (the OXPd lanes say which call and what it costs on 1.x and 2), keys its licence cache by serial, and refuses sessions from an unlicensed device.
2. **Trust in the serial.** The endpoint is anonymous and takes any string as a serial (4.1.4). That is tolerable when the caller is the device. A server that registers many serials makes the weakness practical: anyone who knows a tenant id can consume its seats. The port should add caller authentication for server callers, at least a per-installation credential, and leave the anonymous path for existing Workpath devices.
3. **A batch call.** One request per device per day is fine for devices. A server with several hundred printers should validate in one call. This is an additive endpoint; the existing one must stay for the field.
4. **Offline grace moves to the server.** Kam's brief describes a localised server, which may sit on a network with restricted egress. The 20-day temporary-licence rule (4.1.5) needs a server-side equivalent, and it must survive a server restart or reinstall without resetting the clock. Decide whether a server that never reaches the licence service may run at all; today a fresh device runs for 20 days without contact.
5. **Is the server itself licensed?** Today nothing but printers is counted. A server product raises questions the current model has no field for: server instances per tenant, a hosted multi-tenant server, anti-cloning. The claims can be extended without touching fielded devices (4.1.7).
6. **Deployment.** Installing an Android package with a device admin password (4.3.4) has no OXPd equivalent in this lane's code. What replaces it is registration of the solution with each device: for OXPd 2 a signed solution bundle and for OXPd 1.x SOAP registration of the agent and buttons, per the OXPd lanes. The per-device unit of work still exists (reach the device, authenticate as admin, register, verify, retry), so the utility's engine is the right shape and its HPKTool layer is what gets replaced. The developers anticipated this (4.3.6).
7. **Per-device configuration collapses.** Today each app on each printer receives a configuration JSON and an attestation credential set (4.3.4). On a server, tenant configuration is held once on the server and the per-device part shrinks to "which server, which solution, which device group". The Entra client credentials no longer need to travel to printers at all, which removes the attestation step and the HP developer LDB key from the roll-out.
8. **Device admin credentials.** One shared password per job, stored with a built-in key and passed on a command line (4.3.4, section 8). An OXPd server holds device admin credentials for as long as it drives the fleet, so the port needs a proper secret store and per-device credentials from the start.
9. **Legacy Keycloak onboarding.** If the OXPd product is Entra-only, the administration portal's onboarding tool is not needed for it. If legacy Keycloak customers must be served on OXPd devices, the server needs the Keycloak branch as well. This is a scope decision (section 7).

### 5.3 What a mixed fleet under one licence and one admin view requires

The licence side is nearly free; the admin view is not.

| Requirement | Today | Change needed |
|---|---|---|
| One licence covers both kinds of device | already true: the cap is per tenant and a seat is a serial (4.1.6) | none, if one seat per printer regardless of platform is the commercial rule |
| No double counting | a printer is one row per `(serial, tenant)` | the OXPd server must send the same serial string the Workpath app would send for that model family. If a printer could run both (a Workpath-capable device driven by the OXPd server), it still counts once, which is correct |
| Tell the two kinds apart | `TenantDevice` has only serial and timestamps | add platform or source, reporting server id, model and app version columns; add an optional field to the validate request. Old devices that omit it are Workpath by default |
| Different price or entitlement per platform | no claim for it | add a claim (for example per-platform caps); safe for fielded devices (4.1.7); needs a rule for licences issued before the claim existed |
| One admin view of customer, licence, devices, deployment state and configuration | three unconnected stores: administration portal database, licence portal database, a SQLite file on a technician's PC (4.2, 4.3.2) | a decision on where the single view lives. The licence portal is the only place that already knows every tenant and every device and already has customer sign-in, so it is the natural base (my assumption); the OXPd server would report device and health data to it |
| Customer roles | any signed-in user of the tenant can delete devices and upload licences (4.1.8) | role checks before the portal grows into a fleet view |
| Seat release | customer deletes a device row; the device re-registers at its next poll if a seat is free | an OXPd server should release a seat when a printer is removed from it, or seats leak until someone deletes rows by hand |
| Reducing a cap | least recently seen devices are dropped (4.1.3) | with a server polling in batches, "last seen" must mean the device, not the server's last batch, or the cull picks arbitrary victims |

### 5.4 Traps

- **Expired licences are deleted when a Datasec operator opens the tenants page.** The grid validates every stored licence and deletes any that fails, including for expiry (`License.Portal/Services/TenantLicenseService.cs:49-56`), and the cascade removes that tenant's device list. An OXPd server that treats "licence not found" differently from "licence expired" will see the first where it expects the second.
- **The device's expiry branch looks dead.** The app marks itself unlicensed at once only if the response text contains "Lifetime validation failed" (`LicenseCheckRunner.kt:75-77`). The server's only failure reason is the fixed text "Invalid license signature or claims" (`License.Common/Utils/LicenseValidator.cs:35-36`). So an expired licence appears to give devices the 20-day temporary state rather than an immediate stop (inferred from the two files; not tested). The port must choose its expiry behaviour deliberately and not copy either side.
- **A registered device stays valid while the licence validates.** The cap is checked only when a new serial arrives (`TenantDeviceService.cs:14-33`). Lowering a cap takes effect through the cull at upload, not at validation.
- **The licence is bound to a licence-server host name** (4.1.3). A customer-hosted or regional licence server needs licences issued for that host, and a proxy that rewrites the Host header breaks upload.
- **The readme describes a stricter validation token than the code issues** (section 6). Build the server-side verifier from the code.
- **HPKTool output parsing by substring** (4.3.4) is brittle. Do not carry the pattern to OXPd, where the device APIs return structured results.

---

## 6. Contradictions and doubts

| # | Disagreement | Evidence | Which to trust |
|---|---|---|---|
| 1 | Validation token content | The readme says the token is valid for five minutes and that the client checks issuer, audience, lifetime and that the serial matches (`certificates/readme.md:126-141`). The code issues only `serial`, `nonce` and `valid`, with no expiry, issuer or audience (`Utils/LicenseTokenUtils.cs:77-82`), and the device checks only chain, signature, nonce and `valid` (`LicenseCheckRunner.kt:105-126`). | the code |
| 2 | .NET version in CI | Projects target `net10.0`; the licence and HPK workflows install .NET SDK `8.0.x` (`License-Services-main/.github/workflows/build-test-deploy.yml:51`, `build-generator.yml:35`, `HPK-Deployment-Utility-main/.github/workflows/release.yaml:15`). An 8.0 SDK cannot build a net10.0 target. Either the workflows are failing, or the copy in the library is mid-migration. The administration portal workflow uses `10.0.x`. | unknown; ask |
| 3 | Workflow named "build-test-deploy" runs no tests | `License-Services-main/.github/workflows/build-test-deploy.yml` has build, publish and deploy steps only | the file |
| 4 | "Attestation" in production roll-outs | HP's guide presents `--attestation-update` as a debug flow for testing, needing a developer-portal username and LDB key. The utility makes it a standard step of fleet deployment (`Worker.cs:812`). Whether production customers are deployed through a debug path, or this is used only for pilots and non-Marketplace installs, cannot be told from the code. | ask |
| 5 | Purpose of the SQLite option and the database migration page in the licence portal | The code supports running the licence portal on SQLite and moving data between providers (4.1.6). Nothing says why: cost reduction for the hosted service, or an intended customer-hosted licence server. The host-bound licence (4.1.3) fits the second reading. | ask |
| 6 | `image_cache.bin` | The readme says it is unused and is a disguised compressed copy of the API private key kept for possible future use (`certificates/readme.md:14,196-216`). The project file removes it from the build (`License.Portal.csproj:19-21`). It is still in the repository in two places. | treat as a live secret |
| 7 | Administration portal scope | START-HERE groups this repository under "back-end, licensing, admin, deployment" (`START-HERE.md:40`), which suggests fleet administration. The code is onboarding and subscription management only (4.2). | the code |
| 8 | Tenant id in two forms | The licence portal lower-cases tenant ids on write (`DataContext.cs:13-22`) but compares the upload form value to the claim as parsed GUIDs (`LicenseUploadService.cs:38-40`). Lookups by the raw request string (`LicensingController.cs:76`) rely on the database collation being case-insensitive. Fine on default SQL Server collation; on SQLite, string equality is case-sensitive by default, so an upper-case tenant id from a device could miss (inferred, not tested). | verify before any SQLite deployment |

---

## 7. Questions for Kam or his team

1. **Does one licence seat mean one printer, whatever the platform, or will OXPd devices be sold and counted separately?** It decides whether the licence needs a new claim and whether the generator and portal change. If unanswered I assume one seat per printer under one tenant cap, with a platform column added for reporting only.
2. **Is the OXPd server itself to be licensed (per installation, per tenant), and may one server serve more than one Entra tenant (a partner-hosted or Datasec-hosted server)?** The current model has no notion of a server. If unanswered I assume a customer-hosted, single-tenant server that needs no seat of its own and is identified by an installation id for audit.
3. **How long may an OXPd server run without reaching the licence service, and what should happen at licence expiry?** Devices get 20 days today and, as far as the code shows, also get them after expiry (5.4). If unanswered I assume the same 20-day grace on loss of contact and an immediate stop on a confirmed expiry.
4. **Where should the single admin view for a mixed fleet live?** Candidates: extend the licence portal, extend the administration portal, or build it into the OXPd server's own console. If unanswered I assume the licence portal, because it already holds every tenant and device and already signs customers in.
5. **Must the OXPd product support the legacy Keycloak back end, or Entra only?** It doubles the authentication work if yes. If unanswered I assume Entra only.
6. **How are production Workpath fleets deployed today: this utility, HP Command Center, or both, and is the attestation step used in production?** The answer says what partners and technicians will expect of an OXPd roll-out tool and whether HP Command Center must be part of the OXPd story. If unanswered I assume both routes exist and that an OXPd deployment tool replaces only the utility.
7. **Why does the licence portal support SQLite and host-bound licences: is a customer-hosted or sovereign licence server a real requirement?** A localised OXPd server on a closed network would need exactly that. If unanswered I assume the licence service stays Datasec-hosted and the server needs outbound HTTPS to it.
8. **Is the copy of the source in the library current?** The CI files of two repositories would not build the code beside them (section 6, item 2). If unanswered I treat the source as current and the workflows as stale.
9. **Who may issue licences, and is the generator the long-term tool?** It carries the root signing key inside a distributed executable (section 8). An OXPd launch that adds claims is the moment to move issuance to a service with the key in a vault. If unanswered I assume the generator stays and gains the new fields.
10. **Is "Rental" (licence type 5, and the `/rentals` flow) a billing arrangement only, or does it change product behaviour?** No code in this lane branches on licence type. If unanswered I assume billing only.

---

## 8. Secrets and sensitive items seen (locations only), and weaknesses not to carry over

### 8.1 Secret material in the library

| Location | What |
|---|---|
| `SC/License-Services-main/certificates/hpam_root_key.pem` and `SC/License-Services-main/src/License.Generator/Resources/hpam_root_key.pem` | files named and documented as the root RSA private key that signs every licence. Not opened. If they are the production key, anyone with this repository can issue valid licences for any tenant |
| `SC/License-Services-main/certificates/hpam_api_key.pem` and `SC/License-Services-main/src/License.Portal/Resources/hpam_api_key.pem` | files named and documented as the API RSA private key that unwraps tenant signing keys. Not opened |
| `SC/License-Services-main/certificates/image_cache.bin` and `SC/License-Services-main/src/License.Portal/Resources/image_cache.bin` | documented as a compressed private key under a disguised name. Not opened |
| `SC/HPK-Deployment-Utility-main/src/HpkDeployment.Common/Utilities/EncryptionUtils.cs:54-55` | a hardcoded AES key and a fixed initialisation vector. They protect the stored printer admin passwords, the HP developer LDB key and exported job files, on every installation of the utility |
| `SC/Datasec-Administration-Portal-main/src/DatasecAdministrationPortal/Pages/Saas/Rentals.cshtml:30,34` | two SharePoint sharing links with embedded share tokens to Datasec documents |
| `SC/Datasec-Administration-Portal-main/src/DatasecAdministrationPortal/Migrations/` (seed migrations, not opened beyond one matched line) | seed data for resources, templates and onboardings; the two "Seed_Onboardings" and "Seed_Customer_Info" migrations may hold real customer names and should be checked by whoever handles this repository |

Both `appsettings.json` files hold placeholders only (`<read_from_secret>`), and all three repositories run a Gitleaks workflow. The committed PEM files show the scan does not cover them or has an allow-list (inferred).

No personal data of named individuals was seen in the files read.

### 8.2 Weaknesses in the existing product that the port should not carry over

1. **TLS verification is switched off in the device's licence client.** It trusts every certificate and every host name, built through reflection on string fragments (`SC/HPAuthenticationManager-main/.../license/LicenseCheckRunner.kt:145-181`). The signed token limits the damage to denial or delay, but an OXPd server must validate TLS normally.
2. **Anonymous device registration.** Any caller can register any serial for any tenant id that has a licence, and so exhaust a customer's seats (`LicensingController.cs:18-19`, `TenantDeviceService.cs:28-44`). Tenant ids are not secret.
3. **Anonymous licence upload.** Bounded by the signature check, but an old still-valid licence for a tenant can be replayed to replace a newer one, and a lower cap then deletes devices (`LicensingController.cs:143-144`, `LicenseUploadService.cs:45-65`). There is no issue-date or serial ordering check.
4. **The database migration page is open to any signed-in user of any tenant.** It carries `[Authorize]` only, with no Datasec-operator check, on a multi-tenant sign-in, and it wipes the destination database (`Pages/Maintenance/DbMigration.cshtml.cs:9,30-38`, `Services/DbMigrationService.cs:71-73`). It is not linked from the layout but is reachable by URL. It needs both connection strings configured to do anything. It also displays the SQLite connection string unmasked (`DbMigrationService.cs:32-33`).
5. **Datasec operator status rests on a username pattern** as well as the home tenant id (`UserService.cs:23-25`). The tenant check carries the weight; the pattern adds nothing and would misfire if guest accounts are present in the home tenant.
6. **Root signing key distributed inside a desktop executable** and held in source control (8.1). The design document calls the root key offline; in practice it is on every PC that has the generator.
7. **Validation tokens never expire** (section 6, item 1). The nonce prevents replay to a correct client, so the exposure is small, but a server-side cache of tokens would make it matter.
8. **Device admin password on a process command line and under a shared static key** (`Worker.cs:753,784,812,840`; `EncryptionUtils.cs:51-58`). Visible to any local process listing and recoverable from any exported job file by anyone with the utility.
9. **Fixed IV with CBC** in the same routine: identical plaintexts give identical ciphertexts, and decryption failure silently returns an empty string, which the caller treats as an empty password (`EncryptionUtils.cs:34-48`, `Worker.cs:176`).
10. **Webhook authentication by a code in the query string** in the administration portal, logged on mismatch (`Controllers/WebhooksController.cs:108-114`). Query strings reach proxy and access logs. The Marketplace webhook should validate the bearer token Microsoft sends; `Program.cs:121-125` configures JWT validation parameters, but `WebhooksController` is `[AllowAnonymous]` and I did not read the webhook handler to see whether it validates the token itself.
11. **Client secrets sent by email** at the end of onboarding (`ApplicationOnboardingExecuteCommandHandler.cs:217-236`).
12. **Customer-side authorisation is all-or-nothing** in the licence portal (4.1.8).
