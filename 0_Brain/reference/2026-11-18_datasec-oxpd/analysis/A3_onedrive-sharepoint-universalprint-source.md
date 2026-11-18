# A3: OneDrive / SharePoint and Universal Print: source analysis

Lane A3, Datasec OXPd project, 2026-11-18. Source of truth: the code in `HPAM - Docs and Notes/Source Code/CypherOneDrive-main` and `.../UniversalPrint-main` (library root `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`).

Path shorthand used in every citation (all relative to the library root):

| Short | Stands for |
|---|---|
| `UP/` | `HPAM - Docs and Notes/Source Code/UniversalPrint-main/` |
| `UPJ/` | `UP/app/src/main/java/com/hp/print/mup/agentas/` |
| `OD/` | `HPAM - Docs and Notes/Source Code/CypherOneDrive-main/` |
| `ODJ/` | `OD/app/src/com/hp/print/cypher/` |
| `HPAMsrc/` | `HPAM - Docs and Notes/Source Code/HPAuthenticationManager-main/` (another lane's tree; read only where Universal Print calls into it) |
| `CVLsrc/` | `HPAM - Docs and Notes/Source Code/CommonValueLibraryCypher-master/commonvaluablelibrary/src/main/java/com/hp/print/commonvaluablelibrary/` (another lane's tree; two files sampled) |

No secret value appears in this report. Section 8 lists locations only.

---

## 1. BLUF

This lane holds two Android (HP Workpath) apps: the OneDrive/SharePoint file app and the Universal Print agent ("HP for Universal Print", package `com.hp.print.mup.agentas`, version 4.4.1).

1. **Universal Print never uses the Graph print API.** Every job operation is IPP INFRA over HTTPS against `print.print.microsoft.com/printers/{id}`; registration is the Microsoft printer-registration REST service at `register.print.microsoft.com/api/v1.0/register`. The Graph print methods are declared and never called (4.2.9).
2. **One physical device becomes up to three separate Universal Print printers** (`_Direct`, `_Secure`, `_Pull`), each with its own RSA-2048 key, Microsoft-issued device certificate, cloud device id and device token. All of it sits in the app's encrypted preferences on the device; there is no export, no renewal and no deregistration code (4.2.2, 4.2.3).
3. **Direct and Pull already print over the network path a server would use**: an IPP `Print-Job` to `https://<printer-ip>:631/ipp/print`, streamed from the cloud with HTTP Range resume. Only Secure prints through the Workpath SDK, from a file downloaded to the device, after a panel preview (4.2.5 to 4.2.7).
4. **Registration needs a human-grade Entra credential**: a device-code sign-in with scope `<print resource>/.default` by a Printer Administrator (or Global Administrator). For unattended fleet roll-out the app receives that account's username and password through HP Command Center and drives the Microsoft sign-in page with injected JavaScript; it cannot pass MFA (4.2.1).
5. **Pull release is not in this app's UI**: HP Authentication Manager calls an AIDL service in the Universal Print app at sign-in (`fetchJobs`, `releasePullPrintJobs`, `cancelPullPrint`), and the per-user auto-release switch is a HPAM user property named `UPAR` (4.2.6).

OneDrive / SharePoint facts are in 4.1 (merged from the second half of this lane).

---

## 2. Coverage

### Universal Print (`UP/`, 389 files)

| Class of file | Count | Treatment |
|---|---|---|
| Kotlin/Java under `UPJ/` | 202 | **128 read whole**; 17 sampled by targeted grep and partial read; 57 not opened |
| OnGuardLib (Java 13, C++/headers 14) | 27 | 1 header sampled for symbol names only (`secrets.h`); rest not opened |
| Unit / instrumented tests | 9 | names listed, not opened |
| Build, packaging, manifests | 9 | read whole (`settings.gradle.kts`, both `build.gradle.kts`, `gradle.properties` keys only, 2 manifests, 2 `hpk.xml`, `packaging_release/readme`, `notes`) |
| GitHub workflows | 4 | sampled (step names, triggers) |
| `app/moc/*.cfg`, `*.moc` | 4 | structure only (keys and ids extracted by script; values not read into this session, see section 8) |
| `app/ipp_stuff/*` developer captures | 12 | 5 sampled through a masking filter (emails, GUIDs, IPs, long blobs replaced) |
| `app/diagrams/UP_Init_Phase.drawio` | 1 | box labels extracted |
| Resources (`res/`, 67 xml, 17 png) | 84 | `values/uris.xml` and the error strings of `values/strings.xml` read; rest not opened |
| `.aar` / `.jar` binaries | 7 | class names listed with `unzip -l` / `bsdtar -t` (not unpacked); no decompilation |
| EULA `.htm`, PDFs, fonts, images | about 30 | not opened |

Read whole (128): everything in `conn/`, `auth/`, `remoteconfig/`, `directprint/` except `WebViewAutomatedLogin.kt` and `JSCodes.kt`, `directprint/spooler/`, `core/` (except `core/api/error/mtl/`), `delegate/`, `crypto/`, `io/`, `hilt/`, `app/`, `common/Constants.kt`, `common/DataHolder.kt`, `common/SecuredPreferences.kt`, `common/file/FilePath.kt`, `common/net/Port.kt`, `storage/`, `util/Utils.kt`, `util/IPP.kt`, `util/PrinterHttpClient.kt`, `util/PrinterNetworkHelper.kt`, `util/PrinterIpAddressProvider.kt`, `util/AppConfigHelper.kt`, `util/DirectoryHelper.kt`, the `model/microsoft/gup/`, `model/graph/` and `model/ippinfra/` models, `ui/splash/`, `ui/jobs/GetJobsActivity.kt`, `ui/print/` (4 files), `ui/registration/presenter/` (2 of 4).

Sampled (17), chosen because they carry flow but are mostly view plumbing: `directprint/WebViewAutomatedLogin.kt` (every function signature, every network call, every timeout and page-state branch), `directprint/JSCodes.kt` (constants and function names), `ui/registration/RegisterPrinterActivity.kt` (lines 96 to 258 and 532 to 740 read), `ui/registration/RegisterPrinterAuthActivity.kt`, `ui/tenant/AdminConsentActivity.kt`, `ui/settings/SettingsAppFragment.kt`, two `ui/settings/signin/` fragments, `ui/sio/RememberMeFragment.kt`, `ui/BaseActivity.kt`, `ui/adapter/JobsAdapter.kt`, `ui/logout/presenter/LogoutPresenter.kt`, `util/webkit/AuthWebViewHardening.kt`, `util/FallbackDns.kt`, `util/okhttp/OkHttpUtils.kt`, `conn/factory/tls/TLSV12SocketFactory.java`, `util/Loggable.kt`.

Not opened (57): small constant holders under `common/net/`, `common/token|time|intent|thread|media`, `model/base/`, `model/oidc/`, `model/token/`, `model/microsoft/devicecode/`, `model/graph/user|operation|printer/share`, `db/` (Room settings table), `ui/settings/urlbar|domainhint`, `ui/information/`, `ui/view/`, `ui/mvvm/`, `logger/`, `util/DebugConsole|DateUtils|StreamWriter|FileUtils|Extensions|webkit/WebkitUtils|base64|content`, `core/api/error/mtl/`, remaining contracts.

Outside the lane, read because Universal Print's behaviour is split across apps: `HPAMsrc/usermanagement/src/main/aidl/com/hp/print/asprintservice/*.aidl` (whole), `HPAMsrc/usermanagement/.../UserManagementProxyKt.kt` (whole), `.../UserManagement.kt` and `.../AsPrintServiceProvider.kt` (sampled), `HPAMsrc/app/.../ui/printservice/CheckPullPrintJobsFragment.kt` and `.../model/ReaderOutputProcessor.kt` (grep for the pull-print calls only), `CVLsrc/utils/CommonSDKUtil.java:188-198`, `CVLsrc/print/service/PrintSupportService.java:436-452`.

### OneDrive / SharePoint (`OD/`, 532 files)

See 4.1.0 (coverage table supplied by the OneDrive half of the lane).

---

## 3. Inventory

### 3.1 Universal Print

| Item | Value | Source |
|---|---|---|
| Gradle root name | "HP for Universal Print" | `UP/settings.gradle.kts:48` |
| Modules | `:app`, `:usermanagement`, `:MTL`, `:CVL`, `:OnGuardLib` | `UP/settings.gradle.kts:49` |
| Package / namespace | `com.hp.print.mup.agentas` | `UP/app/build.gradle.kts:27,43` |
| Version | 4.4.1 (versionCode 4040101) | `UP/app/build.gradle.kts:46-47` |
| SDK levels | min 31, target/compile 35 | `UP/build.gradle.kts` (extra properties) |
| Language | Kotlin 1.9.10 (201 kt) with 22 Java; Hilt 2.48; Room; RxJava2 and coroutines side by side | `UP/settings.gradle.kts:27-32`, `UP/app/build.gradle.kts:102-175` |
| HP Workpath package descriptor | name "Universal Print for Authentication Suite", vendor "HP Inc", platform `LinkForDevice` 31.7, fixed app UUID | `UP/packaging_release/hpk.xml` |
| Packaging | `.hpk` = zip of the release APK plus `hpk.xml` | `UP/packaging_release/readme`, `UP/.github/workflows/release.yml:168-190` |
| IPP library | `com.hp.jipp:jipp-core:0.7.16` (HP's JIPP) | `UP/app/build.gradle.kts:151` |
| HTTP | Retrofit 2.5 / OkHttp 3.10 | `UP/app/build.gradle.kts:126-136` |
| Crypto | SpongyCastle 1.51 (PKCS#10), jjwt 0.11.2 (RS256), androidx security-crypto 1.0.0 | `UP/app/build.gradle.kts:123,139-144` |
| PDF | PdfiumAndroid 1.9.8, pdfbox-android 2.0.27 (preview side, via CVL) | `UP/app/build.gradle.kts:146-147` |
| Bundled binaries | `WorkpathLib-1.6.3.aar`, `commonvaluablelibrary-1.09.20.aar` (719 classes), `usermanagement-release.aar` v1.0.5 (62 classes, holds the HPAM token proxy and the `IPrintService` AIDL stubs), `MTL-1.00.010.aar` (thread pool) | `UP/app/libs/`, `UP/CVL/`, `UP/usermanagement/`, `UP/MTL/`; class lists by `bsdtar -t` |
| Entry points | `SplashActivity` (launcher); `PrintService` (exported foreground service, also the AIDL endpoint); `WorkPathReadyReceiver` (boot trigger); debug-only `DefaultConfigRegistrationReceiver` | `UP/app/src/main/AndroidManifest.xml:45-89`, `UP/app/src/debug/AndroidManifest.xml` |
| Permissions | INTERNET, FOREGROUND_SERVICE, SCHEDULE_EXACT_ALARM; declares `...hpauthenticationmanager.permissions.TokenLibraryPermission` | `UP/app/src/main/AndroidManifest.xml:5-8` |
| CI | build, CodeQL, gitleaks, release (tag, test, assemble, zip HPK, checksum, GitHub release) | `UP/.github/workflows/*.yml` |
| Tests | 5 unit tests of substance (`SessionAccessPolicy`, `EntraEndpointResolver`, `BuildConfigRegistrationDefaults`, `JSCodes`, `AuthenticationRace`) | `UP/app/src/test/` |

Screens: Splash, Register Printer (admin form or "ask your admin" message), Register Printer Auth (device-code web view), Admin Consent (declared, never launched: 4.2.1), Get Jobs (the Secure release list), Print Preview, Settings, Information, Open Source (`UP/app/src/main/AndroidManifest.xml:21-75`).

### 3.2 OneDrive / SharePoint

See 4.1.1.

---

## 4. Findings

## 4.1 OneDrive / SharePoint

<!-- ONEDRIVE-SECTION-PLACEHOLDER -->

## 4.2 Universal Print

### 4.2.0 The shape of the app in one paragraph

A sticky foreground service (`PrintService`) starts when Workpath broadcasts `WORKPATH_READY` and whenever the app is opened. It reads its configuration (from HP Command Center through the Workpath `ConfigService`, or from the admin form on the panel), registers up to three cloud printers, then runs three loops: an attribute-sync loop (every 120 s), a Direct loop (every 10 s) that fetches every pending cloud job and pushes it to the printer's own IPP port, and a Pull loop (every 5 s) that only tracks jobs already released. Pull release itself is triggered by HP Authentication Manager over AIDL when a user signs in. Secure is interactive: the signed-in user opens the app, sees only their jobs, selects, previews, and the file is printed through the Workpath SDK. Sources: `UPJ/directprint/PrintService.kt:83-137,253-283`, `UPJ/directprint/WorkPathReadyReceiver.kt:15-45`, `UPJ/directprint/DirectPrintProcessor.kt:71-93`, `UPJ/directprint/PullPrintProcessor.kt:80-92`, `UPJ/ui/jobs/GetJobsActivity.kt:197-256`.

### 4.2.1 Registration: who signs in, with what

**Token used to register.** OAuth 2.0 device authorization grant against Entra:

- device code: `POST {entraId}/{tenant or "organizations"}/oauth2/v2.0/devicecode` with `client_id` = configured app client id and `scope` = `{resourceUri}/.default`, where `resourceUri` is the Universal Print resource (`https://print.print.microsoft.com` for Commercial) (`UPJ/core/api/devicecode/DeviceCodeTask.kt:31-39`, `UPJ/remoteconfig/EntraEndpointResolver.kt:6-13`, `UPJ/remoteconfig/PrintCloudConfig.kt:13-21`);
- token: OIDC discovery at `{authority}/v2.0/.well-known/openid-configuration`, then `POST token_endpoint` with `grant_type=device_code`, polled at the server-given interval until 90% of the code lifetime has passed (`UPJ/ui/registration/presenter/RegistrationTokenPresenter.kt:65-87,89-104,220-244`);
- it is a **public client**: no client secret is sent in this flow (`RegistrationTokenPresenter.kt:94-97`). A field map with `client_secret` exists (`UPJ/conn/factory/field/FieldMapFactory.kt:11-26`) but its only consumer, `OIDCApi.getOIDCTokenBundle`, has no caller (search: `/usr/bin/grep -rn "getOIDCTokenBundle" UPJ` returns only the interface declaration; control: `oidcApi.loadOIDCConfig` is found twice).

**Default application id.** A fixed client id is compiled in as `CLIENT_ID_UP` (`UP/app/build.gradle.kts:52`) and used when the cloud is Commercial and no id is configured (`UPJ/remoteconfig/WorkpathConfigProvider.kt:450-452`). A customer-managed app id, or any non-Commercial cloud, makes the tenant id mandatory (`UPJ/remoteconfig/Config.kt:29-47`).

**Checks on the token after sign-in.** The access token's `tid` must equal the configured tenant if one is configured, then is stored as the tenant (`RegistrationTokenPresenter.kt:115-120,155`). The code also computes whether the token has the `Printers.Create` scope, whether the audience equals the print resource, and whether the `wids` claim contains the Global Administrator or Printer Administrator role template, but **only logs these four booleans; none of them blocks registration** (`RegistrationTokenPresenter.kt:121-154`). The real authorisation decision is Microsoft's, at the register call.

**Two ways to produce that sign-in.**

| Path | Trigger | What happens | Source |
|---|---|---|---|
| Interactive (panel) | A Workpath **device admin** opens the app; `SplashViewModel` routes any admin principal to the registration form | Admin ticks Direct / Secure / Pull, composes names, sets the pull sign-out timeout, presses Register. A hardened WebView loads Microsoft's `verification_uri`; the admin types the code flow credentials (and MFA) by hand | `UPJ/ui/splash/SplashViewModel.kt:115-120,225-249`, `UPJ/ui/registration/RegisterPrinterActivity.kt:112-210,532-615`, `UPJ/ui/registration/RegisterPrinterAuthActivity.kt:283-350` |
| Unattended (fleet) | HP Command Center pushes a config whose state becomes `HPCC.RequireUpdate` | `PrintService` runs a 10-minute registration chain. `RegisterPrinter` asks for a device code, then an **off-screen WebView loads the verification page and JavaScript fills the user code, the admin username and the admin password, and presses Next** | `UPJ/directprint/PrintService.kt:158-232`, `UPJ/directprint/RegisterPrinter.kt:61-79`, `UPJ/directprint/WebViewAutomatedLogin.kt:88-131,302-345,580-618` (sampled), `UPJ/directprint/JSCodes.kt:5-14,168-191` (sampled) |

The unattended path is where "the Entra Printer Administrator account the notes mention" lives: fidgets `azure_admin_username` and `azure_admin_password` in the HPCC frame `com.hp.print.mup.agentas.printer_registration` (`UPJ/remoteconfig/WorkpathConfigProvider.kt:277,326-337`). After reading them the app writes the config back to HPCC with both values blanked and `isConsumed=true` (`WorkpathConfigProvider.kt:489-518`), but keeps them in its own encrypted preferences as part of the saved `Config` JSON (`WorkpathConfigProvider.kt:80-88`, `UPJ/remoteconfig/Config.kt:7-9`). The login automation recognises MFA pages: for an approval page it presses the approval button, for a code page it only waits; a "security enrollment" page is terminal; an `AADSTS` code seen in the page console aborts (`WebViewAutomatedLogin.kt:404-470,494-509,143-151`). In practice the account must be able to sign in with a password alone (inferred from those branches).

**Admin consent.** An `AdminConsentActivity` loading `{authority}/adminconsent` exists (`UPJ/ui/tenant/AdminConsentActivity.kt:298-323`, `UPJ/remoteconfig/EntraEndpointResolver.kt:18-19`) but is unreachable: `callAdminConsentActivity()` in `UPJ/ui/splash/SplashActivity.kt:169` has no caller (search `callAdminConsentActivity\(|AdminConsentActivity::class` over `UPJ` returns only that definition).

**Who may see what** is decided by the Workpath principal: an admin principal always lands on registration and never sees cloud jobs; a non-admin with no HPAM token is sent to HPAM to sign in (`SplashViewModel.kt:115-176`, `UPJ/ui/splash/SplashActivity.kt:94-106`, `UPJ/ui/jobs/GetJobsActivity.kt:199-202`, `UPJ/auth/SessionAccessPolicy.kt:4-11`).

### 4.2.2 Registration: the protocol with Microsoft

Run once per enabled flavour, in the order Direct, Pull, Secure for the unattended chain (`PrintService.kt:162-207`) and Direct, Secure, Pull for the panel form (`RegisterPrinterActivity.kt:669-711`). Class: `UPJ/directprint/RegisterPrinter.kt`.

| Step | Call | Detail | Source |
|---|---|---|---|
| 1 | local | Clear this flavour's stored registration. Generate an **RSA-2048** key pair; store the private key (PKCS#8, Base64) in encrypted preferences under a per-flavour key | `RegisterPrinter.kt:50-54,269-293` |
| 2 | local | Build a PKCS#10 CSR, `SHA256withRSA`, with a fixed subject (CN "Microsoft", O "Microsoft Corp", L "Redmond", ST "Washington", C "US"). The subject carries nothing about the device | `UPJ/delegate/helper/CsrHelper_2.kt:19-32,57-88` |
| 3 | `POST {registration}/api/v1.0/register` | Headers: `Authorization: Bearer <admin registration token>`, `client-request-id`. JSON body: `name` (printer display name), `manufacturer` "HP", `model` (from the Workpath device attribute), `device_id` = **a fresh random UUID**, `device_type` "printer", `certificate_request` {`type` "pkcs10", `data` = CSR, `transport_key` = public key}. 3 attempts, retry on 500/502/503/504 and transport errors with 1 s then 2 s pause | `RegisterPrinter.kt:136-230`, `UPJ/model/microsoft/gup/register/GUPRegisterPrinterRequest.kt`, `UPJ/model/microsoft/gup/pkcs10/DeviceCertRequest.kt`, `UPJ/conn/api/GUPRegServiceApi.kt:13-17` |
| 4 | response | `registration_id`, `interval` | `UPJ/model/microsoft/gup/register/GUPRegisterPrinterResponse.kt` |
| 5 | `GET {registration}/api/v1.0/register?registration_id=...` | Same bearer. 202 = pending (sleep `interval`, default 5 s), 200 = done. No upper bound in this class; the unattended chain bounds it at 10 minutes | `RegisterPrinter.kt:84-92,295-361`, `PrintService.kt:161` |
| 6 | 200 body | `cloud_device_id`, `certificate` (**issued by Microsoft: Microsoft is the signer**), `print_svc_url`, `notification_url`, `mcp_svc_resource_id`, `device_token_url`. Stored per flavour, except `notification_url`, which is never stored or used | `UPJ/model/microsoft/gup/register/GUPRegistrationComplete.kt`, `RegisterPrinter.kt:321-358` |
| 7 | device token | See 4.2.3 (forced) | `RegisterPrinter.kt:99-105` |
| 8 | IPP `Update-Output-Device-Attributes` to `{print_svc_url}/printers/{cloud_device_id}` | Full capability set (4.2.4) | `RegisterPrinter.kt:107-114`, `UPJ/util/Utils.kt:286-373` |
| 9 | local | In-memory key pair dropped. On any failure the flavour's `cloudDeviceId` is cleared | `RegisterPrinter.kt:117-131` |

After registration the admin must **share the printer in the Azure portal by hand**: the completion dialog says so (`UP/app/src/main/res/values/strings.xml:58`). The app declares `POST print/shares` on Graph (`UPJ/conn/api/GraphApi.kt:22-28`) and never calls it.

**No deregistration.** Unticking a flavour or a failed chain only deletes local state (`RegisterPrinterActivity.kt:260-303,540-553`, `UPJ/common/SecuredPreferences.kt:62-74`); the cloud printer object stays until an admin removes it. Search `deregister|unregister|DELETE\(` over `UPJ`: only AIDL-callback and file hits (control: `expires_in` found 3 times in `DeviceTokenManager.kt`).

**Re-registration triggers.** (a) HPCC pushes a new config: state goes to `RequireUpdate` and the chain registers any enabled flavour that is not "configured" (`PrintService.kt:158-207`). (b) "Configured" is tested live: an IPP `Get-Jobs` with the stored device token; IPP status `client-error-gone`, HTTP 401, HTTP 403, or an HTTP 400 whose body mentions device authentication or `AADSTS` mean "not registered any more" and the local state is wiped (`UPJ/util/IPP.kt:60-156`, `UPJ/core/exception/CommonException.kt:29-42`). Any other failure is treated as "still registered". (c) A change of the tuple (app client id, tenant id, Entra host, resource URI, registration endpoint) wipes all three registrations (`WorkpathConfigProvider.kt:577-594`, `Config.kt:70-84`). (d) A change of cloud endpoints restarts the app process (`WorkpathConfigProvider.kt:236-246,596-607`).

### 4.2.3 Device identity at run time: the device token

Class: `UPJ/auth/DeviceTokenManager.kt` (one cached token per flavour, in memory and in encrypted preferences).

1. `POST {device_token_url}` form `grant_type=srv_challenge`, `windows_api_version=2.0` → `{ "Nonce": ... }` (`DeviceTokenManager.kt:86-118`).
2. Build a JWT, **RS256, signed with the flavour's private key**, header `x5c` = the Microsoft-issued certificate, claims: `request_nonce`, `grant_type` "device_token", `resource` = `mcp_svc_resource_id`, `client_id` = app client id, `redirect_uri` = `https://localhost`, `iss` = `cloud_device_id` (`DeviceTokenManager.kt:120-184`, `UP/app/src/main/res/values/uris.xml:2`).
3. `POST {device_token_url}` form `grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer`, `request=<jwt>`, on a cookie-stripping client → `access_token`, `token_type`, `expires_in`, `expires_on`, `not_before`, `resource`, `device_info` (`DeviceTokenManager.kt:186-271`, `UPJ/model/microsoft/gup/DeviceAccessTokenResponse.kt`, `UPJ/conn/interceptor/ClearCookies.kt`).
4. Refresh when more than 90% of `expires_in` has elapsed since the token was fetched (`elapsed_ms > expires_in * 900`) (`DeviceTokenManager.kt:273-360`). The Secure status path also forces a refresh on a 401 and retries up to twice (`UPJ/ui/print/presenter/PrintPresenter.kt:54-76`).

This device token is the only credential on every IPP INFRA call. The signed-in user's Entra token is **never** sent to Universal Print: the user is conveyed as an IPP attribute, `requesting-user-uri = mailto:<upn or email>` (4.2.5 to 4.2.7).

**Where credentials live.** `EncryptedSharedPreferences` file `SecuredPreferences2`, AES256-SIV keys / AES256-GCM values, master key from the Android keystore (`UPJ/common/SecuredPreferences.kt:17-27`). Per flavour: `cloud_device_id`, private key, device token JSON and fetch time, certificate, `device_token_url`, `mcp_svc_resource_id`, `print_svc_url` (`SecuredPreferences.kt:60-260`). Also there: tenant id, the user's HPAM access token (`access_token`), the whole `Config` JSON including admin username and password (`config_key`), and one IPP attribute snapshot per cloud device (`IPP_SNAPSHOT_<id>`) (`SecuredPreferences.kt:29-39`, `WorkpathConfigProvider.kt:31,84`, `UPJ/util/IPP.kt:476-491`). The private key is software-generated and stored as data, not as a non-exportable keystore key (`RegisterPrinter.kt:275-293`).

**Certificate renewal: none.** Search `renew|notAfter|certificate.*expir|checkValidity` over `UPJ` finds one line, in a WebView SSL-error description helper (`UPJ/util/webkit/AuthWebViewHardening.kt:121`). When the certificate stops working the device token request fails, the flavour is judged unregistered (4.2.2 b) and, under HPCC, re-registered from scratch as a **new** cloud printer.

### 4.2.4 The three flavours

`enum PrinterType { DIRECT, PULL, SECURE }` (`UPJ/core/api/registerprinter/RegisterPrinterRequest.kt:13-17`). The name is `<parts joined by "_">` + `_Direct` / `_Secure` / `_Pull`, parts being any of product name, hostname (first label), product number, serial number and free text (`UPJ/directprint/PrinterNameBuilder.kt:32-68`, HPCC keys `product_name`, `productHostname`, `productNumber`, `serialNumber`, `free_text` at `WorkpathConfigProvider.kt:338-366`).

| | `_Direct` | `_Pull` | `_Secure` |
|---|---|---|---|
| What the user experiences | Prints come out without anyone at the device (unless the job carries a PIN) | User prints to one shared queue, then signs in at any device; HPAM offers or auto-releases their jobs | User signs in, opens the Universal Print app, picks jobs, can preview and change options, prints |
| Who starts the work | Background loop, every 10 s | HPAM over AIDL at sign-in | The user in the app's job list |
| Jobs fetched | All fetchable jobs of the printer (`Get-Jobs` with no user) | Only the user's: `requesting-user-uri` + `my-jobs=true`, then a second client-side check | Only the user's: same two attributes |
| Hold mechanism | None in the app. If the job has `job-password`, it is forwarded and the **printer's own firmware** holds it | Microsoft holds the job until a device acknowledges it for that user (printer advertises owner-authorised release, see below) | Same advertisement; the job stays in the cloud until the user picks it |
| Document transport | Cloud → app memory stream → printer `https://<ip>:631/ipp/print` (IPP `Print-Job`) | Same as Direct | Cloud → file in app storage → Workpath SDK `PrinterService.submit` |
| Status source | Poll printer `Get-Job-Attributes` every 10 s, mirror upward | Poll printer every 5 s, mirror upward | Workpath print-job broadcasts (start, complete with sheet and impression counts) |
| Extra attributes advertised | none | `smi311-universal-print-anywhere-enabled=true`; `release-action-supported/default = owner-authorized`; `job-release-action-default = workflow-app`; `job-release-action-supported` = none, workflow-app, owner-authorized-badge, owner-authorized-biometrics, owner-authorized-username-password, owner-authorized | (same as Pull) |
| Sources | `UPJ/directprint/DirectPrintProcessor.kt` | `UPJ/directprint/PullPrintProcessor.kt`, `UPJ/directprint/PrintService.kt:285-327` | `UPJ/ui/jobs/GetJobsActivity.kt`, `UPJ/core/api/getjobs/GetJobsIPPTask.kt`, `UPJ/core/api/downloadjob/DownloadJobIPPTask.kt`, `UPJ/ui/print/presenter/PrintPresenter.kt` |

Extra-attribute source: `UPJ/util/IPP.kt:364-391`. This confirms the old port brief (`OLD BUILD/OXPd1_solution-master/todo.txt`, as summarised in `START-HERE.md:29`): Secure prints through the Workpath SDK, the other two through the printer's IPP port.

### 4.2.5 Direct: exactly as coded

Loop (`DirectPrintProcessor.kt:71-93`): every 10 s, if enabled, `checkKnownJobs` then `fetchAndSubmit`. Enabled means the flavour is switched on and has a cloud device id (`PrintService.kt:234-248`).

1. IPP `Get-Jobs` → `POST {print}/printers/{id}`, body `application/ipp`, operation attributes `printer-uri = {print}/printers/{id}`, `output-device-uuid = urn:uuid:{id}` (`UPJ/util/IPP.kt:158-199`, `UPJ/conn/api/IPPInfraApi.kt:17-22`).
2. For each job id: IPP `Fetch-Job` with `job-uri = ipps://<print host>:443/printers/{id}/jobs/{n}` (`DirectPrintProcessor.kt:588-614`). States aborted / completed / canceled / processing are skipped; pending and pending-held continue (`DirectPrintProcessor.kt:167-181`).
3. IPP `Acknowledge-Job` (sent twice in this path: once without and once with `requesting-user-uri`), carrying `printer-uri-supported` = the device's `ipp://`, `ipps://` and `https://` URIs on port 631 (`DirectPrintProcessor.kt:172,219-221,715-777`, `UPJ/util/IPP.kt:221-270`).
4. Queue a spool request (`DirectPrintProcessor.kt:226-412`). The spooler runs one submission at a time, Pull before Direct, retry delay `2^attempt` seconds capped at 64 s, duplicate request ids ignored (`UPJ/directprint/spooler/PrintSpoolerImpl.kt:36-77,150-175,304-307`, `UPJ/directprint/spooler/SpoolerClasses.kt:61-65`). The request id is `"pull-$jobId"` in both processors (`DirectPrintProcessor.kt:227`, `PullPrintProcessor.kt:259`).
5. Submission: probe size with `Fetch-Document` and `Range: bytes=0-0` (expects HTTP 206 and `Content-Range`), then open a resumable stream that re-issues `Fetch-Document` with `Range: bytes=<offset>-<end>`, strips the IPP response header from each HTTP body and yields only document bytes; 3 retries at the same offset with 0.5 to 10 s back-off plus jitter, counter reset on progress (`DirectPrintProcessor.kt:249-285,415-423`, `UPJ/io/ResumableIppDocumentInputStream.kt:21-34,131-178,194-239`).
6. Build a local `Print-Job` for `ipp://<ip>:631/ipp/print`: `job-name`, `requesting-user-name` = originating user name, `requesting-user-uri` = `mailto:` address, `job-password` and `job-password-encryption` copied if present, and only these job attributes copied: copies, finishings, sides, orientation-requested, media, print-quality, printer-resolution, output-bin, media-col, output-mode, ipp-attribute-fidelity, multiple-document-handling, page-ranges, print-color-mode, minus any attribute this printer previously rejected (`DirectPrintProcessor.kt:425-494`, `UPJ/util/IPP.kt:201-218`).
7. Send it: `POST https://<ip>:631` (the `ipp` scheme is rewritten to `https`), `Content-type: application/ipp`, chunked 8 KiB, connect 6 s, read 15 s (`UPJ/util/PrinterHttpClient.kt:25-58,101-118`).
8. Result handling: success codes → record remote-to-local job id, remember any `unsupported-attributes` names for next time (in memory only), report job state upward; `server-error-busy` → retry in 10 s; anything else → report `aborted` (`DirectPrintProcessor.kt:313-383`, `UPJ/directprint/spooler/InMemoryUnsupportedAttrStore.kt`).
9. Status mirror: each cycle, `Get-Job-Attributes` on the printer for every mapped local job, then `Update-Job-Status` upward with `output-device-job-state` and `output-device-job-state-reasons`; mapping dropped when the local job is terminal or not found (`DirectPrintProcessor.kt:500-562,616-702`).

The remote-to-local job map is a `ConcurrentHashMap` in memory (`DirectPrintProcessor.kt:106`): a service restart loses it and those cloud jobs never get a final state from this device.

### 4.2.6 Pull: hold, release, cancel

**The AIDL contract** (defined in HPAM's `usermanagement` module, shipped inside this app as a binary):

```
interface IPrintService {
    void registerPullPrintCallback(IPullPrintServiceCallback callback);
    void unregisterPullPrintCallback(IPullPrintServiceCallback callback);
    void fetchJobs(String userEmail);
    void releasePullPrintJobs(String userEmail);
    int  pullPrintTimeoutDuration();
    void cancelPullPrint();
}
interface IPullPrintServiceCallback { void onStatusChanged(int documentsInQueue); }
```

Source: `HPAMsrc/usermanagement/src/main/aidl/com/hp/print/asprintservice/IPrintService.aidl:5-12`, `.../IPullPrintServiceCallback.aidl:3-5`. Implemented in `UPJ/directprint/PrintService.kt:285-327`; every method first checks that the caller's package is signed with the same certificate as this app (`PrintService.kt:328-342`). HPAM binds to component `com.hp.print.mup.agentas/.directprint.PrintService` with a 10 s call timeout (`HPAMsrc/usermanagement/src/main/java/com/hp/print/asprinterservice/AsPrintServiceProvider.kt:31-49`).

**Sequence.**

1. User signs in at the panel (HPAM). HPAM registers a callback and calls `fetchJobs(email)` (`HPAMsrc/app/src/main/java/com/hp/print/hpauthenticationmanager/model/ReaderOutputProcessor.kt:1306-1346`).
2. The app runs `Get-Jobs` on the **Pull** printer with `requesting-user-uri = mailto:<email>` and `my-jobs = true`, counts job groups and calls back `onStatusChanged(count)`; 0 if Pull is disabled (`PullPrintProcessor.kt:607-637`, `UPJ/util/IPP.kt:176-183`).
3. HPAM shows a dialog on the panel: release now, or auto-release with a countdown; the timeout comes from `pullPrintTimeoutDuration()`, which is the admin-set "pull print sign-out timeout" (default 10 s, HPCC fidget `pull_print_timeout`) (`HPAMsrc/app/.../ui/printservice/CheckPullPrintJobsFragment.kt:79-135,228-405` (sampled), `PrintService.kt:314-317`, `UPJ/remoteconfig/Config.kt:16`, `WorkpathConfigProvider.kt:368-374`). The per-user "auto-release" preference is the HPAM user property `UPAR`, which this app reads and writes through the HPAM binder and shows as a switch in its own drawer (`UPJ/ui/splash/SplashViewModel.kt:179-193`, `UPJ/ui/jobs/GetJobsActivity.kt:269-278,995-1007`).
4. HPAM calls `releasePullPrintJobs(email)` (`CheckPullPrintJobsFragment.kt:96-99,329-330`). The app, for each of the user's jobs: `Fetch-Job`; client-side check that `job-originating-user-uri` **contains** the email, case-insensitive (`PullPrintProcessor.kt:825-840`); `Acknowledge-Job` with `requesting-user-uri` (non-cancellable); poll `Fetch-Job` once a second up to 10 times until the state leaves pending / pending-held; if still pending, give up on that job (`PullPrintProcessor.kt:231-253,585-605`).
5. Then the same streamed `Print-Job` to the printer's port 631 as Direct, through the same spooler at higher priority (`PullPrintProcessor.kt:258-441`).
6. `cancelPullPrint()`: cancels the fetch coroutine, removes the last user's queued spool entries, sends IPP `Cancel-Job` to the printer for each non-terminal local job, and reports `canceled` / `job-canceled-at-device` upward (`PullPrintProcessor.kt:876-949`). The user is "the last email passed to release": a comment says the contract should carry the email in a later release (`PullPrintProcessor.kt:858-861,880-885`).

So a held Pull job is held **by Microsoft**, and is released to whichever registered `_Pull` printer acknowledges it for that user. The "print anywhere" behaviour comes from the `smi311-universal-print-anywhere-enabled` attribute and from users printing to one shared queue (inferred from the attribute name and the flow; the code does not explain the cloud-side routing).

### 4.2.7 Secure: the panel release UI

1. Splash obtains the user token from HPAM: the `usermanagement` library binds to HPAM's `ITokenManagementService` and emits sign-in, new-token and sign-out events (`HPAMsrc/usermanagement/.../UserManagementProxyKt.kt:16-64`, `.../UserManagement.kt:18-66` (sampled), `SplashViewModel.kt:135-176`). The app decodes the JWT payload locally, without verifying it, to get `given_name`, `family_name`, `unique_name`, `upn`, `tid` (`UPJ/util/Utils.kt:617-641`). It also requires an authenticated Workpath principal (`SplashViewModel.kt:152-157,201-223`).
2. Job list (`GetJobsActivity`): `Get-Jobs` on the **Secure** printer with `requesting-user-uri = mailto:<upn>` and `my-jobs = true`; then `Fetch-Job` per job to read name, sides, copies, colour mode, output bin, media size and type, orientation, finishings, collation, size in kilo-octets and creation time (`UPJ/core/api/getjobs/GetJobsIPPTask.kt:77-155,274-367`). No paging: one request, all groups.
3. UI: list with per-row select, select-all, a Print button, refresh, a drawer with the user's name, the Pull auto-release switch and Sign out, and an overflow menu (Settings for admins or when SIO is enabled, Information, Sign out, Exit) (`GetJobsActivity.kt:269-351,531-551,965-984`).
4. Print: each selected job is downloaded to `files/MUP_AppData_<timestamp>/Print_<timestamp>/<timestamp>.<ext>` with a resumable ranged `Fetch-Document` (3 retries per offset; a 416 restarts from zero) (`UPJ/core/api/downloadjob/DownloadJobIPPTask.kt:62-263`, `UPJ/util/DirectoryHelper.kt:12-61`). A free-space check exists but is commented out (`DownloadJobIPPTask.kt:66-70`).
5. The files and a `TaskConfiguration` per job (the options from step 2) go to the CVL print-preview screen, where the user can change options; CVL submits to the Workpath SDK as a print-from-storage job (`GetJobsActivity.kt:664-681`, `UPJ/ui/print/PrintPreviewAppActivity.kt:105-121`, `UPJ/ui/print/PrintPreviewAppFragment.kt:42-48`, `CVLsrc/print/service/PrintSupportService.java:344,439-452`).
6. Status: on the CVL "job start" broadcast the app sends `Acknowledge-Job`; on "job complete" it sends `Acknowledge-Job` then `Update-Job-Status` with `job-impressions-completed`, `job-pages-completed` (both set to the impression count), `job-media-sheets-completed` and state `completed`; if the user cancels during download it sends state `canceled` / `job-canceled-by-user` (`GetJobsActivity.kt:910-963,720-731`, `UPJ/ui/print/presenter/PrintPresenter.kt:54-76,174-264,266-353`).
7. Session end: leaving the activity deletes the temp folders, clears the cached user token and the in-memory device tokens, but keeps the registrations (`GetJobsActivity.kt:553-562`, `UPJ/util/Utils.kt:163-177`).

Formats: the cloud printer advertises `application/pdf` only (4.2.8), and the list hard-codes the content type as PDF (`GetJobsIPPTask.kt:133`). The print check accepts pdf, jpg, jpeg, tiff, tif, txt by extension (`CVLsrc/utils/CommonSDKUtil.java:190-196`). **There is no conversion code in this app**: Microsoft renders to PDF because PDF is what the printer says it accepts (inferred), and the device prints the PDF natively.

### 4.2.8 Printer attributes and capabilities reported

Sent with IPP `Update-Output-Device-Attributes` to `POST {print}/printers/{id}`, operation attributes `output-device-uuid` and `printer-uri-supported` (the device's three port-631 URIs) (`UPJ/util/Utils.kt:316-354`).

At registration (`UPJ/util/Utils.kt:304-314`, `UPJ/util/IPP.kt:285-392`):

- From the Workpath SDK's capability model (via CVL option groups, mapped by `UPJ/core/api/registerprinter/mapper/IPPMappingTable.kt:6-119`): `multiple-document-handling` default and supported, `media-col-supported`, `sides` default and supported, `print-color-mode` default and supported, `media-type-supported`, `media-source-supported`, `copies` default and supported.
- Fixed: `printer-state = idle`, `printer-is-accepting-jobs = true`, `printer-state-reasons = none`, `ipp-versions-supported` 1.0 / 1.1 / 2.0, `printer-up-time = 1000`, `printer-make-and-model` = Workpath model name, `document-format-default` and `-supported` = `application/pdf`.
- From the device itself: a full IPP `Get-Printer-Attributes` (`requested-attributes = all`) against `https://<ip>:631`, every attribute appended, then a block list removed (PCLm / URF / JPEG specifics, PDF size constraints, firmware strings, `printer-device-id`, marker and supply telemetry, strings URIs, `printer-name`); plus `job-password-encryption` taken from the device or defaulting to sha2-256.
- `printer-name` = the configured flavour name; the release attributes of 4.2.4 for Secure and Pull.

Every 120 s while configured (20 s poll otherwise): re-read the device's attributes, compute a canonical snapshot of a **watch list** (defaults, supported sets, `media-ready`, `media-col-ready`, `printer-state`, `printer-state-reasons`, the release and job-password attributes; `media-col-database`, `printer-input-tray`, `printer-output-tray` by SHA-256 digest), compare with the stored snapshot, and send only the changed attributes (`PrintService.kt:109-120`, `UPJ/util/Utils.kt:219-284,451-498`, `UPJ/util/IPP.kt:494-601`). This is how out-of-paper or a tray change reaches Universal Print.

### 4.2.9 What is not used

| Declared | Status | Evidence |
|---|---|---|
| Graph `print/shares`, `print/printers/{id}/jobs`, `.../jobs/{id}/cancel`, job paging, document download, printer existence check | never called | `UPJ/conn/api/GraphApi.kt:22-60`; search `graphApi\.|sharePrinter|cancelJobGraphAPI|verifyPrinterExists|getJobsPaging|downloadFileGraphAPI` over `UPJ` outside `conn/` returns one hit, `graphApi.getMyPhoto` |
| Graph `me/photos/360x360/$value` | called only from a private function whose single call site is commented out ("Disabled for now") | `UPJ/ui/splash/SplashViewModel.kt:147-151,253-272` |
| Notification service (`notification.print.microsoft.com`, `notification_url`) | URL builder exists, no caller; no IPP `Get-Notifications`, no subscription. **Job discovery is polling only** | `UPJ/delegate/URLStore.kt:35-37`; search `notification_url|getIPPInfraApiNotificationBaseURI|Get-Notifications|getNotifications|webhook` over `UPJ` returns only the model field and that builder |
| Discovery service host | config field only | `UPJ/remoteconfig/PrintCloudConfig.kt:8` |
| HP token proxy (`core.api.hp.com`, `stage.api.hp.com`, `/tokenProxy/v1/token`) | URL builders exist, no caller | `UPJ/delegate/URLStore.kt:19-21,59-81`, `UP/app/src/main/res/values/uris.xml:3-4` |
| Graph-style printer registration model (`displayName`, `physicalDeviceId`, `hasPhysicalDevice`, `certificateSigningRequest`, `connectorId`) | model only | `UPJ/model/graph/printer/register/RegisterPrinterRequest.kt:7-36` |
| `LocalJobsManager` ("saved jobs") | the list is always set to empty; the read is commented out | `UPJ/core/LocalJobsManager.kt`, `GetJobsActivity.kt:366,431` |
| Licensing | no licence check in this app's own code | search `licen` (case-insensitive) over `UPJ`: one file, the open-source notice screen; control: `DeviceTokenManager` found in 12 files. A check inside the CVL binary's `initialize` is not excluded (not decompiled) |

### 4.2.10 Background service, start-up, failure handling

- Start: `WORKPATH_READY` broadcast (protected by HP's services permission) or app launch schedules an exact alarm that starts the foreground service; `START_STICKY` (`UPJ/directprint/WorkPathReadyReceiver.kt:15-45`, `UP/app/src/main/AndroidManifest.xml:76-83`, `SplashViewModel.kt:86-98`, `PrintService.kt:253-283`).
- Init: Workpath SDK and CVL initialised with a 20 s cap, then config processing (`PrintService.kt:89-107`).
- Printer address: Workpath `DA_NETWORK_IPADDRESS`, falling back to every local IPv4 address; the first that accepts TCP on 631 within 1.5 s wins; cached 10 minutes (`UPJ/util/PrinterNetworkHelper.kt:84-118`, `UPJ/util/PrinterIpAddressProvider.kt:17-25`).
- TLS to the printer: before each request the app opens a TLS socket with a trust-everything manager to read the printer's certificate, then builds a context that trusts exactly that certificate (`PrinterNetworkHelper.kt:33-81`, `UPJ/util/PrinterHttpClient.kt:101-138`). See 8.
- Cloud HTTP: connect 10 s, read and write 90 s, redirects off, a DNS wrapper that caches resolved addresses in preferences and falls back to them when system DNS fails (`UPJ/conn/factory/okhttp/HTTPClientFactory.kt:13-31`, `UPJ/util/FallbackDns.kt:22-41` (sampled)).
- Throttling: HTTP 429 and 503 map to `TooManyRequestsException` and a "Too many requests" dialog in the interactive path (`UPJ/core/exception/CommonException.kt:42`, `UPJ/core/exception/ExceptionAlertMessageUtil.kt:48-50`). **`Retry-After` is not read anywhere**; the background loops simply log and try again on the next tick (`DirectPrintProcessor.kt:114-122`).
- Error surface for users: strings `error_*` in `UP/app/src/main/res/values/strings.xml:17-30` (download failed, file not found, insufficient storage, session expired, server access lost, no permission, device not registered, unsupported format, device unavailable, firmware update required, tenant required, too many requests, unable to retrieve data).
- Nothing is persisted about in-flight jobs (4.2.5 last paragraph); unsupported-attribute memory is also in memory only.

### 4.2.11 Configuration

| Source | Keys | Code |
|---|---|---|
| HP Command Center frame `com.hp.print.mup.agentas.printer_registration` | `print_type` {`secure_print`, `direct_print`, `pull_print`}, `azure_admin_username`, `azure_admin_password`, `registration_names` {`product_name`, `productHostname`, `productNumber`, `serialNumber`, `free_text`}, `pull_print_timeout` | `WorkpathConfigProvider.kt:277,307-376` |
| HP Command Center frame `com.hp.print.mup.agentas.cloud_config` | `cloudConfig` (Commercial, GCC, GCC_High, DoD, Custom), `appClientId`, `tenantId`, and for Custom: `entraId`, `print`, `registration`, `discovery`, `notification`, `graphApi`, `resourceUri` | `WorkpathConfigProvider.kt:280,389-448`, `UPJ/remoteconfig/PrintCloudEnvironment.kt` |
| CVL app config frame | `adminOptIn` (EULA), `msDomainHint`, `urlAddressBar` | `UPJ/util/AppConfigHelper.kt:100-105` |
| HPAM user properties | `UPAR`; `universalprint.remember_me_save`, `universalprint.remember_me_do_not_show_again` | `SplashViewModel.kt:184`, `UPJ/storage/UserPreferencesStore.kt:7-9` |
| Panel form | flavour ticks, three names, pull timeout | `RegisterPrinterActivity.kt:112-210,575-590` |

Config states: `NotConfigured`, `HPCC.RequireUpdate`, `HPCC.Configured`, `ConfiguredUI` (`UPJ/remoteconfig/Config.kt:86-93`). Live HPCC changes arrive through `ConfigService.AbstractConfigChangeObserver` (`WorkpathConfigProvider.kt:55-67,609-618`).

Endpoints per cloud (host names are public Microsoft service names, from `UPJ/remoteconfig/PrintCloudConfig.kt:13-51`):

| Cloud | Entra | Print (IPP INFRA) | Registration | Graph | Resource |
|---|---|---|---|---|---|
| Commercial | login.microsoftonline.com | print.print.microsoft.com | register.print.microsoft.com | graph.microsoft.com | print.print.microsoft.com |
| GCC | login.microsoftonline.com | gcc-print.print.azure.us | gcc-register.print.azure.us | graph.microsoft.com | print.print.microsoft.com |
| GCC High | login.microsoftonline.us | print.print.azure.us | register.print.azure.us | graph.microsoft.us | print.print.azure.us |
| DoD | login.microsoftonline.us | print.print-dod.azure.us | register.print-dod.azure.us | dod-graph.microsoft.us | print.print-dod.azure.us |

### 4.2.12 Every outbound endpoint actually used

| # | Destination | Protocol | Auth | Purpose | Source |
|---|---|---|---|---|---|
| 1 | `{entraId}/{tenant}/oauth2/v2.0/devicecode` | HTTPS form | public client id | start admin sign-in | `DeviceCodeTask.kt:36-39` |
| 2 | `{entraId}/{tenant}/v2.0/.well-known/openid-configuration` | HTTPS GET | none | find token endpoint | `RegistrationTokenPresenter.kt:68` |
| 3 | Entra token endpoint | HTTPS form | device code | admin registration token | `RegistrationTokenPresenter.kt:94-102` |
| 4 | Microsoft sign-in pages (WebView; allow-list of host suffixes) | HTTPS | interactive or scripted | admin sign-in | `RegisterPrinterAuthActivity.kt:317-350`, `AuthWebViewHardening.kt:17-35,74-96` (sampled) |
| 5 | `{registration}/api/v1.0/register` POST and GET | HTTPS JSON | admin bearer | register, poll | `GUPRegServiceApi.kt:13-29` |
| 6 | `{device_token_url}` (returned by 5) | HTTPS form | nonce, then signed JWT | device token | `DeviceTokenManager.kt:105,217` |
| 7 | `{print}/printers/{cloud_device_id}` | IPP over HTTPS POST | device bearer | Update-Output-Device-Attributes, Get-Jobs, Fetch-Job, Fetch-Document (with `Range`), Acknowledge-Job, Update-Job-Status, Get-Job-Attributes | `IPPInfraApi.kt:10-53` |
| 8 | `https://<printer ip>:631` and `/ipp/print` | IPP over HTTPS | none | Get-Printer-Attributes, Print-Job, Get-Job-Attributes, Cancel-Job | `PrinterHttpClient.kt:31-118` |
| 9 | HPAM (same device) | Android binder | signature / permission | user token, user properties, start sign-in | `UserManagementProxyKt.kt`, `SplashActivity.kt:94-106` |
| 10 | Workpath SDK (same device) | SDK | n/a | device attributes, principal, sign-out, config, print submit, job events | `Utils.kt:202-217`, `SplashViewModel.kt:201-249`, `GetJobsActivity.kt:771`, `WorkpathConfigProviderHelper.kt:14-46` |

`print_svc_url` returned at registration overrides the configured print host for the Retrofit base URL, but only the **Secure** flavour's value is consulted, for all three flavours (`UPJ/delegate/URLStore.kt:27-33`).

### 4.2.13 Multi-device and fleet aspects

- Each device registers itself; there is no central registry in this app. Fleet roll-out = the same HPCC config pushed to many devices, each running the scripted admin sign-in on its own (4.2.1).
- Name uniqueness depends on the admin choosing hostname or serial in the name parts; the register body's `device_id` is random, so nothing ties the cloud object to the hardware (4.2.2 step 3).
- A device that re-registers creates a **new** cloud printer and must be shared again by hand; the developers' own notes record exactly this kind of orphaning during testing (`UP/app/ipp_stuff/INvestigate_list_reg`, `UP/app/ipp_stuff/Investigate_missing_registration_part2`).
- Load on Microsoft: per device, one `Get-Jobs` on the Direct printer every 10 s (plus one `Fetch-Job` per listed job, every cycle, for jobs not yet terminal), one attribute read from the device every 120 s, and device-token refreshes per flavour.

---

## 5. What this means for the port

<!-- ONEDRIVE-PORT-PLACEHOLDER -->

### 5.2 Universal Print

**What depends on running on the device, and what does not.**

| Behaviour | Needs from the device today | On a server |
|---|---|---|
| Registration protocol (4.2.2), device token (4.2.3), all IPP INFRA traffic (4.2.5 to 4.2.8) | Nothing: outbound HTTPS only | Portable as is. `jipp-core` is a plain JVM library; a .NET port needs an IPP encoder with the INFRA operations |
| Direct and Pull printing | Reaches its own IPP port; uses the address as seen from itself | Server must reach **each printer on TCP 631 with IPPS enabled**, and must tell Universal Print the printer's real URIs (`printer-uri-supported`). Finding 4.2.5 steps 6 to 7 |
| PIN-held Direct jobs | Printer firmware holds a `Print-Job` carrying `job-password` | Unchanged, as long as the server forwards the two attributes (4.2.5 step 6) |
| Capability report | Workpath print capabilities + IPP `Get-Printer-Attributes` | IPP `Get-Printer-Attributes` works remotely. The Workpath-derived half must come from OXPd device / print services instead, or be dropped in favour of the IPP answer (4.2.8) |
| Model, hostname, serial, product number, IP | Workpath `DeviceService` | OXPd device service, or the same IPP query (4.2.4, 4.2.10) |
| Secure job list, selection, preview, option change | Android screens on the panel | An OXPd browser/app UI served by the server; preview pages rendered server-side (4.2.7) |
| Secure print submit and page counts | Workpath `PrinterService.submit` from a local file; Workpath job broadcasts | Either OXPd print-job submission or, simpler, the **same IPP `Print-Job` path as Pull** with the user's chosen options. Sheet and impression counts then come from IPP job attributes or OXPd job statistics (4.2.7 steps 5 to 6) |
| Pull release at sign-in | HPAM calls the app over AIDL; dialog drawn by HPAM | An in-process call inside the server at the OXPd sign-in event; dialog becomes an OXPd UI page (4.2.6) |
| "Who is signed in" | HPAM token over binder + Workpath principal | The server's own session for that device (4.2.7 step 1) |
| Admin gate for registration | Workpath principal `isAdmin` | A server admin console; no panel step needed (4.2.1) |
| Config | HP Command Center through Workpath `ConfigService` | Server configuration store; HPCC does not exist for OXPd (4.2.11) |
| Secrets | Android keystore-backed encrypted preferences | Server secret store, now holding **every** printer's keys (below) |
| Always-on loops | Foreground service started at `WORKPATH_READY` | A server daemon; devices no longer need to be awake to be polled for, but must be awake to print |

**What a server-side connector must hold.** It stands in for many printers, so the unit of state is (physical printer, flavour).

Per tenant / environment:

- cloud environment (five endpoint URLs, 4.2.11), app client id, tenant id;
- a way to obtain a registration token with `Printers.Create` for a Printer Administrator. On a server this can be **one interactive device-code sign-in by an admin in a web console, reused for a batch of registrations**, instead of a stored password and a scripted login per device (4.2.1). The token is needed only at registration time (4.2.2 steps 3 and 5).

Per (printer, flavour), all required to keep an existing registration alive:

| State | Why | Finding |
|---|---|---|
| RSA-2048 private key | signs every device-token request | 4.2.3 step 2 |
| Microsoft-issued device certificate | `x5c` header | 4.2.3 step 2 |
| `cloud_device_id` | JWT issuer, URL path, `output-device-uuid` | 4.2.3, 4.2.5 |
| `device_token_url`, `mcp_svc_resource_id`, `print_svc_url` | token and job endpoints (store per flavour; do not copy the Secure-only shortcut of 4.2.12) | 4.2.2 step 6 |
| cached device token + fetch time | avoid a token round-trip per call | 4.2.3 step 4 |
| printer name and enabled flag | attribute updates | 4.2.4 |
| last attribute snapshot | diff-only updates | 4.2.8 |
| remote-to-local job map, **persisted** | final job status after a restart | 4.2.5 |
| set of attributes this printer rejects | cleaner `Print-Job` | 4.2.5 step 8 |

Per physical printer: network address or hostname, a **stored** TLS trust anchor for its IPPS certificate, model / serial / product number, the OXPd identity the server uses to drive it.

Per signed-in user (transient): UPN and email as they appear in Universal Print's `job-originating-user-uri`, the auto-release preference (`UPAR` today lives in HPAM user properties).

**Constraints and traps.**

1. *Three cloud printers per device, three keys.* A fleet of N devices is up to 3N registrations and 3N private keys in one place. The server's key store becomes the single most valuable target in the product (4.2.3).
2. *No migration path between Workpath and the server.* Keys never leave the device app. Moving a device from the Workpath app to the server means a new registration, a new cloud printer id, and re-sharing and re-assigning in the Azure portal (4.2.2, 4.2.13). For mixed fleets this is fine (a device is served by one or the other), but a device must **not** be registered by both for the same flavour name.
3. *Pull works across both worlds for free.* Release is "any registered `_Pull` printer acknowledges for this user", so a user can release at a Workpath device or an OXPd device as long as the cloud-side sharing treats them as one pool (4.2.6; the cloud-side rule is not in this code: question 3).
4. *Polling does not scale linearly without care.* Today each device polls for itself every 10 s. One server polling for N Direct printers makes N `Get-Jobs` per cycle from one address, with no `Retry-After` handling in the code being ported (4.2.10). The unused `notification_url` returned at registration (4.2.2 step 6) is the obvious lead for an event-driven design; it needs verification against Microsoft's documentation, which is not in this library.
5. *Identity matching is by string.* The user is whatever `mailto:` value the server sends; Microsoft filters with `my-jobs`, and the app's second check is a substring match (4.2.6 step 4). Secure uses the token's `upn`, Pull uses the HPAM user's email (4.2.6 step 1, 4.2.7 step 2): tenants where UPN and mail differ behave differently per flavour. The port should use one rule and an exact match.
6. *The server becomes the party that can fetch anyone's held documents.* The device token is not user-bound; with it the holder can list and fetch any user's job on that printer by naming them (4.2.3). On a device that power is confined to one device's queue; on a server it spans the fleet. The release decision must be bound to a verified panel sign-in event inside the server.
7. *Direct is the easy first target*, Pull second (needs the sign-in hook), Secure last (needs UI, preview and option mapping). Direct and Pull share one code path after the release decision (4.2.5, 4.2.6).
8. *Reusable as specification, almost line for line:* `RegisterPrinter.kt`, `DeviceTokenManager.kt`, `CsrHelper_2.kt`, `IPP.kt` (attribute filter, watch list, creatable-attribute list), `ResumableIppDocumentInputStream.kt`, `PrintSpoolerImpl.kt`, `PrintCloudConfig.kt`, `EntraEndpointResolver.kt`, `Config.kt` validation rules. Not reusable: everything under `ui/`, `WebViewAutomatedLogin.kt` (and it should not be reproduced), `WorkpathConfigProvider.kt` parsing.
9. *OXPd 1.x and 2 both suffice for Direct and Pull printing as coded*, because the print leg is plain IPPS to the printer and does not go through an extensibility API at all (4.2.5 step 7). What OXPd must supply is the sign-in event, the panel UI, and device identity. Whether the customer's printers allow IPPS job submission from a server address, and whether an OXPd print-job service is preferable, is for the platform lanes.

---

## 6. Contradictions and doubts

<!-- ONEDRIVE-DOUBTS-PLACEHOLDER -->

Universal Print:

1. **Port brief versus code on Graph.** The lane brief lists "Graph print APIs" among the possible mechanisms; the code uses none (4.2.9). Any document that describes job handling through Graph is describing an earlier design. The developer note `UP/app/ipp_stuff/secure_ipp_attempts` shows the same job once through "graph" and once through "ipp", and `UP/app/ipp_stuff/INvestigate_list_reg` records a Graph job URL as "not working anymore": the switch from Graph to IPP INFRA happened during development.
2. **Job-state report after a successful local submit looks inverted.** When the cloud job carries both `job-password` and `job-password-encryption`, the app reports `processing` / `none`; when it carries neither, it reports `pending-held` / `job-password-wait` (`DirectPrintProcessor.kt:314-331`, same in `PullPrintProcessor.kt:327-344`). One would expect the opposite. The following status poll overwrites it within 5 to 10 s, so the effect is brief. Not verified on a device.
3. **`media-col-default` normalisation writes x for both dimensions** (`UPJ/util/IPP.kt:697-700`); the function has no caller that I found in the read set (its sibling `enrichReadyWithNamesSafely` is commented out at `Utils.kt:457`). Probably dead; do not port it.
4. **`IPPMediaSource.default()` returns a `media-default` attribute built from a paper source** (`UPJ/core/api/registerprinter/mapper/IPPMediaSource.kt:12-16`); it is not called by `fillDefaultAttributes` (`IPP.kt:333-343`), so harmless today.
5. **Spool request ids are `"pull-…"` for Direct jobs too** (`DirectPrintProcessor.kt:227`). Job ids are per cloud printer, so a Direct job and a Pull job with the same number on one device would be treated as duplicates by the spooler (`PrintSpoolerImpl.kt:49-57`). Low probability, real.
6. **`notes` at the tree root** contains a fragment with `isAdmin || true` (`UP/notes:1`). It is a scratch note, not compiled code; the shipped check is `SplashViewModel.kt:115`.
7. **Emulator scaffolding in production code**: a hard-coded emulator address, dummy jobs, a built-in default config with build-time admin credentials for debug builds (`UPJ/common/Constants.kt:12-19`, `GetJobsIPPTask.kt:157-272`, `UPJ/remoteconfig/DefaultConfigProvider.kt:14-27`, `UP/app/build.gradle.kts:59-80`). Release builds set those three build fields to empty strings.
8. **`START-HERE.md:52-53` describes one Entra app registration ("HP Authentication Manager") and its Graph scopes.** Universal Print registration uses a *different* client id (`CLIENT_ID_UP`) and a different resource (the print service), so the suite needs at least two app registrations or one registration with both API permissions. The library's summary does not say this.
9. **Licensing**: none found in the app's code (4.2.9). If the suite licenses Universal Print, it is enforced in CVL, HPAM or the back end, outside this lane.

---

## 7. Questions for Kam or his team

<!-- ONEDRIVE-QUESTIONS-PLACEHOLDER -->

Universal Print:

| # | Question | Why it matters | Assumed if unanswered |
|---|---|---|---|
| 1 | For the server product, may registration use **one interactive admin sign-in in a web console** (device code or auth code) instead of a stored Printer Administrator username and password with a scripted login? | Removes the weakest part of the current design and the MFA limitation (4.2.1) | Yes: interactive admin sign-in, token used for a batch, nothing stored |
| 2 | Is the fixed default client id (`CLIENT_ID_UP`) a Datasec multi-tenant app registration that the OXPd server may also use, or must each customer register their own app for the server? | Decides tenant onboarding steps and whether the server needs a secret or certificate | Reuse the same multi-tenant public client for registration |
| 3 | In customer tenants, how are the `_Pull` printers shared: one share per device, or does "print anywhere" make all of them one pool? What exactly must the customer configure in the Universal Print portal? | Decides whether Workpath and OXPd devices can release each other's jobs in a mixed fleet (5.2 item 3) | One share per device, plus the print-anywhere setting; mixed release works |
| 4 | Must an OXPd device keep the **same** three-printer model and the same naming (`…_Direct`, `…_Secure`, `…_Pull`), or may the server collapse Secure into Pull (one held queue, release at sign-in or from a list)? | Secure is the only flavour that needs a full panel UI, preview and the Workpath print path | Keep all three for parity; build Direct, then Pull, then Secure |
| 5 | Are customers' OXPd printers allowed to accept IPPS (TCP 631) from the server, or is that port usually closed by policy? | The whole Direct/Pull path depends on it (5.2 table) | Open between server and printers on the print VLAN |
| 6 | Who holds the Universal Print licence position per registered printer or per job, and does three printers per device affect cost? | Up to 3N registrations (5.2 item 1) | No cost effect (Universal Print is metered by job volume): to be confirmed |
| 7 | Is certificate expiry of registered printers a known field problem? There is no renewal code (4.2.3) | Decides whether the server needs a renewal or scheduled re-registration job | Treat "gone / unauthorised" as "re-register and alert an admin to re-share" |
| 8 | Should the server report job statistics (sheets, impressions) to Universal Print for Direct and Pull as it does for Secure? Today only Secure sends counts (4.2.7 step 6) | Customer reporting parity | Yes, from IPP job attributes |

---

## 8. Secrets and sensitive items seen (locations only), and weaknesses not to carry over

<!-- ONEDRIVE-SECRETS-PLACEHOLDER -->

### Universal Print: locations

| Item | Location | Note |
|---|---|---|
| Android signing keystore, committed | `UP/app/datasec_printer_keystore` | binary, not opened |
| Keystore store password, key alias and key password, hard-coded | `UP/app/build.gradle.kts:36-38` | the same keystore file name appears in the OneDrive tree |
| Default Entra application (client) id, hard-coded | `UP/app/build.gradle.kts:52` | an identifier, not a secret; listed because the brief names tenant and app ids |
| HP Workpath app UUID, hard-coded | `UP/packaging_release/hpk.xml`, `UPJ/common/Constants.kt:35` | identifier |
| What look like a real admin user principal name and a password (values not read into this session; a script reported "contains @", "no placeholder wording", lengths only) | `UP/app/moc/config_for_printer.cfg` and `UP/app/moc/config_from_moc_tool.cfg`, fidgets `azure_admin_username` / `azure_admin_password` | **should be checked by Kam and rotated if real** |
| Workpath MOC definitions that mention the admin password field 7 times each | `UP/app/moc/UniversalPrint.moc`, `UP/app/moc/UniversalPrint_test_nondefaultappidwithcommercial.moc` | not opened; may carry defaults |
| Native "locker" constants: authorised package, UUID, vault client id, client id, tenant id, cipher key, IV, transformation | `UP/OnGuardLib/src/main/cpp/hdr/locker/secret/secrets.h:4-12` | symbol names read, values not |
| Developer IPP captures with a real person's name and email address, printer ids, share ids, tenant-specific printer names, and a hashed job password | `UP/app/ipp_stuff/` (notably `pin protected job`, `INvestigate_list_reg`, `Investigate_missing_registration_part2`, `ipp_output`, `ipp_output_up`) | personal data in a source repo |
| Entra directory-role template ids (Global Administrator, Printer Administrator) | `UPJ/ui/registration/presenter/RegistrationTokenPresenter.kt:136,142` | public constants |
| Build-time debug admin username / password / tenant, read from an untracked `config.properties` | `UP/app/build.gradle.kts:14-20,59-73`; file is git-ignored (`UP/.gitignore`) | not present in the tree |

### Universal Print: weaknesses the port should not carry over

1. **A privileged Entra account's password travels through device management and is stored on every printer** (4.2.1). Blanking it in HPCC after consumption does not remove it from the device's own store, nor from HPCC's history.
2. **Scripted sign-in by injecting the password into Microsoft's page** (`WebViewAutomatedLogin.kt`, `JSCodes.kt`). It depends on Microsoft's DOM ids, defeats the purpose of interactive sign-in, forces an MFA-less privileged account, and saves WebView screenshots in some branch (`WebViewAutomatedLogin.kt:822-863`, sampled: destination not verified).
3. **TLS to the printer is trust-on-every-use.** The certificate is fetched with all checks off and then "pinned" for the request that follows, so any host answering on that address is trusted (`PrinterNetworkHelper.kt:33-81`, `PrinterHttpClient.kt:121-138`). On-device the address is the device itself; from a server across a network this would be a real interception risk. Store the printer's certificate or CA once and verify against it.
4. **Device private keys are exportable data** in encrypted preferences (4.2.3). On a server use an HSM or a key vault with non-exportable keys and sign there.
5. **All suite apps trust each other by APK signature, and the signing keystore with its passwords is in the repository** (`PrintService.kt:328-342`, row 1 and 2 above). Anyone with the repo can sign an app that the pull-print service will obey.
6. **User matching by substring** for Pull (`PullPrintProcessor.kt:835-836`): `a@x.com` matches `aa@x.com`.
7. **Unverified local JWT parsing** decides the user identity sent to Microsoft (`Utils.kt:617-641`). Acceptable only because the token comes from HPAM over a signature-checked binder; a server must take identity from its own verified session.
8. **Verbose logging of job packets** at info level: job names, user names and email addresses (`DirectPrintProcessor.kt:152`, `PullPrintProcessor.kt:130,162`), plus full error bodies from Microsoft (`RegisterPrinter.kt:240-246`).
9. **Authorisation checks that only log** (4.2.1): role and scope are computed and ignored. Harmless here because Microsoft enforces them, but it reads as a check.
10. **Exported service guarded by a normal-level Android permission** (`UP/app/src/main/AndroidManifest.xml:84-89`); the real guard is the signature check in code (item 5).
11. **Debug hooks**: a debug-manifest broadcast receiver that triggers registration with built-in credentials (`UP/app/src/debug/AndroidManifest.xml`, `UPJ/directprint/DefaultConfigRegistrationReceiver.kt`), an `X-Mode: debug` header factory (`UPJ/conn/factory/header/HeaderMapFactory.kt:8-17`, no caller found in the read set), and a TLS helper that adds a clear-text connection spec (`UPJ/util/okhttp/OkHttpUtils.kt:54-62`; its only wrapper, `BaseClientFactory.enableTLSV12`, is not called by `HTTPClientFactory`).
12. **No clean-up in the cloud** (4.2.2): orphaned printer objects accumulate in the customer's tenant on every re-registration.
