# A1 — HP Authentication Manager: source code of the sign-in hub

Lane A1, Datasec / OXPd, 2026-11-18. Read-only analysis. No value of any secret is reproduced here; section 8 gives locations only.

Path shorthand used in every citation (all relative to the library root `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`):

| Short | Full relative path |
|---|---|
| `HPAM-A/` | `HPAM - Docs and Notes/Source Code/HPAuthenticationManager-main/` |
| `J/` | `HPAM-A/app/src/main/java/com/hp/print/hpauthenticationmanager/` |
| `UM/` | `HPAM-A/usermanagement/src/main/` |
| `ASM/` | `HPAM - Docs and Notes/Source Code/HP-AuthSuite-Manager-main/` |

---

## 1. BLUF

This lane holds two unrelated code bases that both carry the product name. `HPAuthenticationManager-main` is the Android/Kotlin Workpath app (v4.4.1) that runs on the printer and IS the sign-in hub. `HP-AuthSuite-Manager-main` is a Windows desktop tool (.NET 10, WinUI 3 + Windows service) that pushes the suite's HPK packages and their configuration to printers over the printer's HTTPS admin API; it contains no sign-in logic.

The five facts that most shape the port:

1. **The hub already keeps almost no state on the device.** Card-to-user mappings and (in no-MFA mode) the user's Microsoft refresh token live in Entra Custom Security Attributes (attribute set `HPAuthenticationSuite`), read and written with an app-only Graph token from a client secret held on each printer. A server can do exactly the same calls.
2. **Token sharing is an Android bound service (AIDL)**, `TokenManagementService`, gated by APK signing-certificate match. It has no network form. On OXPd the "other apps" are server components, so this becomes an in-server token broker; a mixed fleet needs no bridge because CSA is the shared store.
3. **Every sign-in method collapses to one function, `acceptInput(cardId, email?)`.** Card swipe, BLE badge and QR/mobile all deliver a string; the QR path delivers a per-user virtual card id over SignalR. Only the passkey (device-code) path differs.
4. **Interactive Microsoft sign-in is an embedded WebView on the panel** with a custom-scheme redirect, PKCE, `prompt=login`, a script that auto-clicks on the Microsoft page, and a spoofed user agent. This is the part with no direct server equivalent; the device-code flow already in the code (QR + user code on the panel, polling) is the one that ports cleanly.
5. **Device identity is weak and local**: a random UUID per printer for QR routing, the serial number for licensing. Tenant identity is one configured tenant id per printer.

---

## 2. Coverage

Git history: **not available**. Neither tree has a `.git` folder (searched to depth 4 for `.git*`; only `.github`, `.gitignore`, `.gitattributes`, `.gitleaks.toml` exist; positive control: those were found).

### HPAuthenticationManager-main (331 files; 118 main Kotlin + 4 Java in `app`, 12 main Kotlin + 10 AIDL in `usermanagement`)

| Class | Count | What |
|---|---|---|
| Read whole | 90 of 118 app main `.kt` | `App`; all of `auth/`, `config/`, `di/`, `signalr/`, `sdk/` (except the mock), `tokenmanagement/`, `storage/`, `security/`, `reporting/` (except dummy data), `repository/`; `model/` except `ShowToast`; `license/` except the 3-line enum; `network/` except `KeycloakApiProvider`; `util/` all; UI: `MainActivity`, `AuthActivity`, `LoadingFragment`, `OnManualSignInFragment` + view model, `MicrosoftSsoFragment`, `DeviceCodeSignInFragment`, `AuthPhase`, QR models, `WebViewUserAgent` |
| Read whole | 9 of 12 usermanagement `.kt`, 5 of 10 AIDL | `UserManagement`, both proxies, `CloudConfig`, `CloudEnvironment`, `CloudConfigProxy`, `AsPrintServiceProvider`; `ITokenManagementService`, `IUserListener`, `ICloudConfigService`, `IPrintService`, `IPullPrintServiceCallback` (imports and blank lines stripped on display) |
| Read whole | 14 other | `README.md`, `settings.gradle.kts`, both `build.gradle(.kts)`, `gradle.properties`, both manifests, release `hpk.xml`, `app/notes`, two readmes, `UserManagementHowTo.txt`, `usermanagement/build.gradle.kts`, `.gitleaks.toml`, all 5 PlantUML flow files |
| Sampled | 8 | `CheckPullPrintJobsFragment.kt` (grep for service calls and timers); `HPAuthenticationManager.moc` (grep of every frame, fidget, set, item and label line); `strings.xml` (grep for sign-in wording); 3 workflow files (grep of step names and build commands); `auto_click_send_notification.js` (first 25 of 234 lines); `config.properties` (key names only, values masked by the command); 4 `.cfg` samples (a script printed only the length of each sensitive field) |
| Not opened | 28 app main `.kt` | `KeycloakApiProvider`, `SDKBridgeMockImpl`, `DummyDataFactory`, `ShowToast`, `LicenseStatus`, 6 of 8 `network/model/*`, `exceptions/*` (3), `extensions/Activity.kt`, `extensions/Fragment.kt`, `ui/config/*` (2), `ui/externallinks/*`, `ui/main/HomeMockActivity`, `MainActivityViewModel`, `TooManyCardsFragment`, `WebPageActivity`, `ui/microsoftsso/…ViewModel`, `ui/mvvm/BaseViewModel`, `ui/views/*` (2), `cloudconfig` adapter/utils/DTO in usermanagement (3) |
| Not opened | all else | 4 Gson converter `.java`; 13 unit tests + 1 instrumented test; 54 of 57 resource XML (layouts, drawables, nav graph); debug and simulator `hpk.xml`; `how_omni_team_parses_the_config_from_hpcc/*` except its readme; the 3 `.aar`, 2 `.jar`, keystore, fonts, images |

### HP-AuthSuite-Manager-main (344 files; 266 `.cs`, 29 `.xaml`)

| Class | Count | What |
|---|---|---|
| Read whole | 14 | `README.md`, `installer/README.md`, `ref-files/README.md`, `scripts/README.md`, `AuthSuiteApps.cs`, `JobAction.cs`, `JobScope.cs`, `IWorkpathDeviceClient.cs`, `WorkpathDeviceClient.cs`, `DeviceInfoClient.cs`, `DeviceDiscoveryClient.cs`, `DataProtector.cs`, `WorkerService/Program.cs`, `WorkpathDeviceClientFactory.cs` (using-lines and comments stripped on display, so a few statement lines that begin with `using var` are missing from what I saw) |
| Sampled | whole tree | two greps: files mentioning `oxpd` (3 hits, all in `Core/Workpath/DeviceInfo/`), files mentioning Graph / login.microsoftonline / entra (0 hits; positive control: the `oxpd` grep over the same tree returned 3) |
| Not opened | 252 `.cs`, all `.xaml` | job engine (`JobRunRunner`, `JobDispatcher`), repositories, SQLite migrations, view models, pages, dialogs (including the MOC-driven config editor `HpkConfigDialogContent.xaml.cs`, 1,150 lines), tests, installer scripts, the 3,593-line UI regression catalogue |

Sample choice for the .NET tree: I read the files that touch a printer over the network and the files that name the suite, because the lane question is what the tool is and how it relates to the hub. The job engine and UI were judged out of lane.

---

## 3. Inventory

### 3.1 HPAuthenticationManager-main — the on-device hub

| Item | Value | Source |
|---|---|---|
| Kind | Android application packaged as a Workpath HPK (zip of APK + `hpk.xml`) | `HPAM-A/app/notes:34-39`, `HPAM-A/.github/workflows/release.yml:48-67` |
| Package / version | `com.hp.print.hpauthenticationmanager`, versionName 4.4.1, minSdk 31, compileSdk 36 | `HPAM-A/app/build.gradle.kts:21-28` |
| Language / stack | Kotlin 2.2, Hilt DI, coroutines, Retrofit 2.9 + OkHttp 4.11, Microsoft SignalR Java client 10.0.3, ZXing, auth0 java-jwt, AndroidX security-crypto, App Center 4.3.1 | `HPAM-A/app/build.gradle.kts:125-171`, `HPAM-A/settings.gradle.kts:27-33` |
| Workpath SDK | `WorkpathLib163.aar` linked (162 also present) | `HPAM-A/app/build.gradle.kts:133` |
| Gradle modules | `:app`, `:usermanagement` (the client library other apps embed, v1.06.01, minSdk 26), `:CVL` (prebuilt `commonvaluablelibrary-1.09.00.aar`) | `HPAM-A/settings.gradle.kts:46`, `HPAM-A/usermanagement/build.gradle.kts:17-26` |
| Flavors | `printer` (config comes from the device) and `emulator` (config baked from `config.properties`) | `HPAM-A/app/build.gradle.kts:67-101` |
| HPK identity | HPK uuid `b749825e-…995c`, name "HP Authentication Manager", platform `LinkForDevice` 31.7 | `HPAM-A/app/packaging_contents_release/hpk.xml:3-9` |
| HPK providers | `STATISTICS` agent, `AUTHN` agent (points at `AuthActivity`, `enablePrePromptCheck=true`), six `ACCESSORIES` entries (`OWNED`) | `HPAM-A/app/packaging_contents_release/hpk.xml:12-80` |
| Entry points | `App` (process start), `MainActivity` (launcher), `AuthActivity` (called by the platform), services `PrinterAuthenticationService`, `PrinterAccessoryService`, `TokenManagementService`, `CloudConfigService`, `PrintReportingService`, receiver `AccessoryReceiver` (also `BOOT_COMPLETED`) | `HPAM-A/app/src/main/AndroidManifest.xml:55-125` |
| CI | unit tests, signed release APK build, HPK zip, CodeQL, gitleaks, release on merged PR with sha256 and the `.moc` attached | `HPAM-A/.github/workflows/ci.yml:28-31`, `release-merged-pr.yml:150-231` |

`CommonValueLibrary` is used in exactly one place in this app (a screen-size helper for WebView scale): `J/ui/microsoftsso/MicrosoftSsoFragment.kt:20`, `:361`. Its EULA activity is explicitly removed from the manifest (`HPAM-A/app/src/main/AndroidManifest.xml:44-48`).

### 3.2 HP-AuthSuite-Manager-main — the Windows deployment manager

| Item | Value | Source |
|---|---|---|
| Kind | Windows desktop app (WinUI 3) + Windows service "HP AuthSuite Service" + SQLite, .NET 10 | `ASM/README.md:2-4`, `ASM/src/WorkerService/Program.cs` (service name) |
| Purpose | deploy and manage the Workpath apps of the suite across networked HP printers | `ASM/README.md:2` |
| Actions | install + configure, install, set configuration, uninstall; scopes per device group | `ASM/src/Core/Enums/JobAction.cs`, `JobScope.cs` |
| Knows the suite as | six fixed HPK uuids (HPAM, SharePoint, OneDrive, Teams, Mailflow, Universal Print), with a TODO to fetch them from a server | `ASM/src/Core/Utilities/AuthSuiteApps.cs` |
| Packaging | Inno Setup installer, binaries signed with Azure Trusted Signing | `ASM/installer/README.md` |

### 3.3 How the two relate

They share nothing at source level. The relation is operational: the manager uploads the hub's `.hpk` to each printer and then PUTs the hub's configuration JSON (the same frames/fidgets structure the hub parses) to the printer's package-management endpoint; the hub reads that JSON through the Workpath `ConfigService`. The manager builds its configuration editor from each app's `.moc` file (`ASM/ref-files/README.md`), and the hub's release pipeline publishes the `.moc` next to the `.hpk` (`HPAM-A/.github/workflows/release-merged-pr.yml:227-231`). The same six uuids appear in the hub's reporting code (`J/reporting/ReportingClient.kt:178-185`) and in the manager (`ASM/src/Core/Utilities/AuthSuiteApps.cs`).

---

## 4. Findings

### 4.1 Two back ends in one binary

A single boolean, `enableCsa`, switches the whole app between the current back end ("MS Entra", Custom Security Attributes) and the legacy one (a Datasec-hosted API in front of Keycloak): `J/config/Config.kt:22-24`, `J/config/WorkpathConfigProvider.kt:254-256`. Almost every component has both branches. Microsoft is the identity provider for the user in both; the back end only decides where card mappings, the stored refresh token and the QR channel live.

### 4.2 Start-up and initialisation

1. `App.onCreate` loads debug flags and sign-in scopes, binds the Universal Print service, and (legacy only, once a logging secret has been fetched) starts App Center (`J/App.kt:78-99`).
2. `AppInitialization` polls connectivity every 200 ms and re-runs initialisation whenever the configuration changes, clearing cached app tokens and restarting SignalR (`J/model/AppInitialization.kt:125-179`).
3. Initialisation blocks until a tenant id is configured (status `NoConfig`), then requires a non-`Unlicensed` licence state, then runs the back-end check (`J/model/AppInitialization.kt:356-388`).
4. Entra check: GET `{graph}/v1.0/$metadata`, then GET `{graph}/v1.0/directory/customSecurityAttributeDefinitions?$top=1&$select=id` with the app-only token (`J/model/AppInitialization.kt:408-478`).
5. Legacy check: GET `version` (must start with `v0.`), POST `token/client-credentials`, GET `config/` which returns the mobile-app auth URL and the App Center secret (`J/model/AppInitialization.kt:508-616`, `J/network/KeycloakApi.kt:16-20`).

The whole initialisation has a 60-second timeout (`J/model/AppInitialization.kt:227`).

### 4.3 The sign-in state machine

State is `AuthPhase`: `WAITING_FOR_LICENSE`, `AUTH_NOT_STARTED`, `PROCESSING_CARD`, `DEVICE_CODE_SIGN_IN`, `MICROSOFT_SSO_SIGN_IN`, `MICROSOFT_SSO_VALIDATION`, `TOO_MANY_CARDS`, `PULL_PRINT_JOB_PROCESSING`, `SIGN_IN_COMPLETED`, `SIGNED_IN`, `AUTH_FAILED` (`J/ui/model/AuthPhase.kt:12-25`). The engine is `ReaderOutputProcessor` (1,524 lines). Each attempt is a `Session` whose id is the creation time in milliseconds; every asynchronous step re-checks that its session is still the current one and silently stops if not (`J/model/ReaderOutputProcessor.kt:343-348`, `:1495-1502`).

**Single entry point.** `acceptInput(sequence, email?)` lower-cases the string, starts a new session, cancels any pending waits and calls `startProcessingCard` (`J/model/ReaderOutputProcessor.kt:366-383`). It is called by:

| Caller | Source of the string | Source |
|---|---|---|
| Card reader, newer firmware (broadcast) | HID data decoded by `ReaderDataStore` | `J/sdk/AccessoryReceiver.kt:136-138` |
| Card reader, older firmware (observer) | per-reader decoders | `J/sdk/PrinterAccessoryService.kt:366-390` |
| QR / mobile app | `secret` (Entra) or `userName` (legacy) field of a SignalR event, plus `email` | `J/ui/main/OnManualSignInFragmentViewModel.kt:115-146` |
| Diagnostics menu | a 4 to 6 character typed id | `J/ui/main/MainActivity.kt:478-486` |
| Debug broadcast | intent action literally named `action`, extra `extra`, receiver registered with no permission | `J/sdk/PrinterAccessoryService.kt:127-134` |

**Card processing, Entra back end** (`J/model/ReaderOutputProcessor.kt:385-422`, `:628-680`):

1. Reject ids longer than 32 UTF-8 bytes with a toast (`:634-646`).
2. If nobody is signed in, ask the platform to start a sign-in (`initiateSignIn`, up to 5 tries 300 ms apart) (`:283-304`, `:401-403`).
3. Look the card up in CSA (4.6). Lookup failure aborts and resets; no match means "unknown card"; a match yields UPN, object id, the auto-release flag and the stored refresh token.

**Known card** (`continueWithKnownUser`, `:424-485`):

- Same user already signed in: the tap signs them **out** (`:435-438`).
- A different user signed in: sign the first out, wait 2 seconds, start a new platform sign-in (`:440-451`).
- Ask Universal Print whether the user has pull-print jobs waiting; if so show the release dialog and wait (`:458`, `:931-956`, 4.9).
- **MFA mode on** (`isMfaEnabled`, default true): open the Microsoft page in the WebView with `login_hint` set to the user's UPN; phase `MICROSOFT_SSO_VALIDATION` (`:460-475`, `:871-889`).
- **MFA mode off**: write the user's attributes back to CSA, then exchange the stored refresh token for an access token with no UI (`:476-483`, `:567-577`). If the exchange fails for any reason other than an Intune block, fall back to the interactive page (`:602-616`). If Entra answers with `AADSTS53009` (Intune app protection required), clear the stored refresh token in CSA, toast, and cancel (`:580-601`).

**Unknown card / first enrolment** (`continueWithUnknownCard`, `:487-518`): the Microsoft page is shown with no login hint (phase `MICROSOFT_SSO_SIGN_IN`, title "Registration"); the user types their own account there. The identity is then taken from the returned access token's claims (`oid`, `upn`/`unique_name`/`preferred_username`, `name`, `given_name`, `family_name`, `tid`) (`:1201-1230`), and the card is appended to that user's CSA `cardId` collection (`:761-785`). There is **no separate "enter your e-mail" screen in the app** on the Entra path; see 6.1.

**Completion** (`signIn`, `:1118-1159`): publish tokens to `TokenManagementService` first, then tell the platform the sign-in succeeded with the user's attributes, then phases `SIGN_IN_COMPLETED` (activity finishes) and `SIGNED_IN`.

**Legacy back end**: look up by card (`GET users?sequence=`), else by e-mail, else create the user; attributes and a chunked "OfflineToken" are stored on the Keycloak user (`J/model/ReaderOutputProcessor.kt:706-851`, `J/repository/KeyCloakApiRepositoryImpl.kt:145-192`).

### 4.4 Each sign-in method

| Method | What the code does | Source |
|---|---|---|
| Card swipe | HID reports from an owned USB accessory are decoded to a string, then 4.3 | `J/sdk/AccessoryReceiver.kt`, `J/sdk/PrinterAccessoryService.kt`, `J/model/ReaderDataStore.kt` |
| BLE mobile badge | **No Bluetooth code exists in the app.** The reader does the BLE exchange and emits the credential as keyboard input; a UUID-shaped string has its dashes removed. Search: case-insensitive `bluetooth` over both modules' main sources, 0 files; positive control `signalr`, 15 files | `J/model/ReaderDataStore.kt:25-30` |
| NFC / biometric card | No NFC or biometric API is used (case-insensitive `biometric|NfcAdapter`, 0 files). To the app these are ordinary card ids from the reader | same search |
| QR code + mobile app | The panel shows a QR holding five fields (printer name, tenant id, client id, SignalR endpoint, OAuth authority), each AES-GCM encrypted with a key compiled into the app. The phone app does its own Microsoft sign-in (not in this lane) and causes a SignalR event carrying the printer name, the user's e-mail and a per-user secret; the printer treats the secret as a card id and continues as 4.3 with the e-mail as login hint | `J/ui/main/OnManualSignInFragmentViewModel.kt:182-207`, `:115-146`, `J/ui/main/MSEntraQrCodeModel.kt` |
| Username entry | Not a separate method. The user types the account name on Microsoft's own page inside the WebView | `J/ui/microsoftsso/MicrosoftSsoFragment.kt:170-173` |
| Passkey (device code) | Button "Sign-in with Passkey", Entra back end only. Requests `…/oauth2/v2.0/devicecode`, shows the verification URL as a QR plus the user code, polls the token endpoint (minimum 5 s, `slow_down` adds 5 s). On success: no card, no CSA lookup, no CSA write; tokens are published and the platform sign-in completed | `J/ui/main/OnManualSignInFragment.kt:75-77`, `J/repository/DeviceCodeRepository.kt:34-98`, `J/ui/devicecode/DeviceCodeSignInFragment.kt:65-79`, `J/model/ReaderOutputProcessor.kt:1069-1116` |

### 4.5 Interactive Microsoft sign-in (the WebView)

- Authorize URL: `{authority}/{tenantId}/oauth2/v2.0/authorize` with `redirect_uri`, `client_id`, random `state` and `nonce` (16 bytes each), `code_challenge` + `code_challenge_method` (S256, 64 bytes of entropy), `prompt=login`, `scope`, `response_type=code`, and when a user is known `login_hint` plus `hsu=1` (`J/repository/MicrosoftSsoRepository.kt:246-281`, `J/repository/CodeVerifierUtil.kt:30`, `:115-128`).
- The returned `state` is never compared with the one sent; the code only looks for `error` or `code` on the redirect (`J/ui/microsoftsso/MicrosoftSsoFragment.kt:282-335`).
- Redirect capture: `shouldOverrideUrlLoading` intercepts any URL that starts with the redirect URI; nothing is actually listening on that URI (`:176-205`, `:286-288`).
- Token request: POST `{authority}/{tenantId}/oauth2/v2.0/token` with `code`, `grant_type=authorization_code`, `redirect_uri`, `code_verifier`, `client_id`, and `client_secret` only in confidential mode. Both an access token and a refresh token are required or the sign-in fails (`J/repository/MicrosoftSsoRepository.kt:43-58`, `:87-132`).
- All WebView cookies are deleted before every attempt, so there is no single sign-on between users (`J/ui/microsoftsso/MicrosoftSsoFragment.kt:163-164`).
- The WebView stays hidden behind a "please wait" layer until a Microsoft page has rendered, or until navigation leaves the Microsoft host (comment: possibly a federated IdP) (`:186-191`, `:210-216`).
- **Autoclicker**: after each Microsoft page load a bundled 234-line script is injected unless `disableAutoclicker` is set (`:216-221`). From its name and header it presses the "send notification" control on the Microsoft page (inferred; only the first 25 lines were read).
- **User agent**: the platform section of the UA string and the UA client hints are replaced with "HP Workpath" (`J/ui/web/WebViewUserAgent.kt:9-43`).
- A redirect to the `https-intunemam:` scheme, or `AADSTS53009` anywhere in an error, ends the attempt with an "Intune App Protection unavailable on this printer" message (`J/auth/MicrosoftSignInFailure.kt:24-85`, `HPAM-A/app/src/main/res/values/strings.xml:95`).
- Screenshots are blocked on real devices (`FLAG_SECURE`) (`J/ui/main/MainActivity.kt:131-136`).

### 4.6 The Entra app registration the code expects

| Aspect | What the code does | Source |
|---|---|---|
| One registration, two roles | the same client id is used for user sign-in and for app-only (client credentials) calls | `J/repository/MicrosoftSsoRepository.kt:219`, `J/network/MsEntraAndKeycloakSessionAuthenticator.kt:33-37` |
| Tenancy | every endpoint is `{authority}/{tenantId}/…`, never `common` or `organizations` | `J/repository/MicrosoftSsoRepository.kt:288-298` |
| Public client (default) | redirect `com.hp.hpauthenticationmanager://oauth2redirect`; auth code + PKCE with no secret; refresh grant with no secret; device-code grant (needs "allow public client flows") | `J/repository/MicrosoftSsoRepository.kt:33`, `:60-71`, `J/repository/DeviceCodeRepository.kt:19` |
| Confidential client (hidden option) | redirect `http://localhost`; the client secret is added to the code and refresh requests. Only honoured when CSA is on; hidden in the admin form | `J/repository/MicrosoftSsoRepository.kt:32`, `:96`, `:145-149`, `J/config/WorkpathConfigProvider.kt:258-261`, `HPAM-A/README.md:5-30`, `HPAM-A/app/moc_file/HPAuthenticationManager.moc:151-158` |
| Delegated scopes requested | always `openid profile offline_access`. Ten more are selectable **per device** from a password-gated diagnostics dialog, default all off: `Channel.ReadBasic.All`, `ChannelMessage.Send`, `email`, `Files.ReadWrite.All`, `Mail.ReadWrite`, `Mail.Send`, `People.Read`, `Sites.ReadWrite.All`, `Team.ReadBasic.All`, `User.Read`, plus a free-text custom list | `J/auth/SignInScopes.kt:7-59`, `J/ui/main/MainActivity.kt:512-540` |
| App-only Graph | client credentials, scope `{graph}/.default` | `J/network/MsEntraAndKeycloakSessionAuthenticator.kt:30-37` |
| App-only SignalR gateway | client credentials, scope `api://{clientId}/.default` (so the registration exposes an API with that URI) | `J/signalr/SignalRAuthHeaderProvider.kt:45-51` |
| App-only log ingestion | client credentials, scope `{monitor}/.default` | `J/reporting/PrintReportingTokenManager.kt:36-44` |

The Graph application permissions needed are not named anywhere in the code. From the calls made they must cover reading users with their custom security attributes, writing those attributes, and creating attribute sets and definitions (inferred). Error AI05 is raised precisely when the definitions read returns 403 (`J/model/AppInitialization.kt:450-461`).

Because the default scope set is only `openid profile offline_access`, the access token the hub hands to the other apps has whatever audience and scopes Entra grants for that request. How Mailflow, Teams, OneDrive and SharePoint get Graph permissions out of it is decided in those apps or in the tenant's consent set-up, not here; see 6.4.

### 4.7 Where things are stored

**Entra Custom Security Attributes** (current). Attribute set `HPAuthenticationSuite`, created on demand with `maxAttributesPerSet` 500; definitions created on demand as searchable strings (`J/repository/MSEntraApiRepositoryImpl.kt:44`, `:245-273`, `:312-395`).

| Attribute | Type | Content | Source |
|---|---|---|---|
| `cardId` | collection of string, max 15 per user | 64-character blob per card: 62 characters = base64url of (6-byte nonce derived by HMAC from the card id, AES-GCM ciphertext of the card id zero-padded to 32 bytes, 8-byte tag) + 2 characters derived by HMAC from the user's `mail`. Deterministic, so the same card always gives the same first 62 characters | `J/util/CardValidator.kt:27-94`, `MSEntraApiRepositoryImpl.kt:46`, `:456-459` |
| `refreshToken` | collection of string | the user's Microsoft refresh token cut into 60-character pieces, each prefixed `NNN_`. Written only when MFA mode is off. **Stored as plain text** (see 6.2) | `MSEntraApiRepositoryImpl.kt:81-92`, `:430-436` |
| `UPAR` | string `true`/`false` | Universal Print auto-release preference, default true | `J/extensions/SharedPrefs.kt:48-51`, `J/repository/CSAUserModel.kt` |
| any other key | string | written by other apps through `updateProperty` | `MSEntraApiRepositoryImpl.kt:693-777` |

A per-user budget of 50 attribute values (each collection element counts as one) is enforced before every write (`MSEntraApiRepositoryImpl.kt:45-78`).

Graph calls, all with the app-only token:

| Purpose | Call | Source |
|---|---|---|
| Find user by card | `GET /v1.0/users?$count=true&$select=id,displayName,userPrincipalName,customSecurityAttributes,mail&$filter=customSecurityAttributes/HPAuthenticationSuite/cardId/any(c:startswith(c,'<62 chars>'))` with header `ConsistencyLevel: eventual`; then the full 64-character blob is recomputed with the matched user's `mail` and compared. A mismatch shows "Card-user association is invalid." | `MSEntraApiRepositoryImpl.kt:100-161` |
| User detail | `GET /v1.0/users/{id}?$select=givenName,surname,userPrincipalName,mail,displayName,id` | `:164-176` |
| Attribute set | `GET` / `POST /v1.0/directory/attributeSets` | `:245-273` |
| Definitions | `GET` / `POST /v1.0/directory/customSecurityAttributeDefinitions` | `:278-395` |
| Read user attributes | `GET /v1.0/users/{id}?$select=customSecurityAttributes,displayName,userPrincipalName,mail` | `:400-414` |
| Write user attributes | `PATCH /v1.0/users/{id}` with `customSecurityAttributes.HPAuthenticationSuite` | `:480-496` |
| Clear stored refresh token | `PATCH` with an empty `refreshToken` collection | `:509-548` |

Only the first page of the card search is read (`value`, no `@odata.nextLink` handling), and a failed HTTP status on that search is treated as "no user" (`:126-131`), which sends an existing user down the enrolment path.

**Per-user preferences in OneDrive** (new, separate channel). `getUserProperty`/`updateUserProperty` read and write a JSON map at `{graph}/v1.0/me/drive/special/approot:/hpam-user-properties.v1.json:/content` using the **user's own** access token (`J/storage/OneDriveUserPropertiesStore.kt:27`, `:82-137`).

**On the device.** One `EncryptedSharedPreferences` file, `SecuredPreferences` (AES-256, Android keystore master key) (`J/di/LocalStorageModule.kt:20-29`):

| Key(s) | Content | Source |
|---|---|---|
| `config_key` | the whole configuration as JSON, **including the client secret and the legacy API key** | `J/config/WorkpathConfigProvider.kt:102-109` |
| `tokenKey`, `refreshTokenKey`, `setupTime`, `relaunchAppKey` | the signed-in user's access token and refresh token, and the app to launch after sign-in | `J/model/UsersTokensStorage.kt:8-81` |
| `access_token`, `refresh_token` | the app-only Graph token (Entra) or the legacy API tokens; both back ends share the same two keys | `J/extensions/SharedPrefs.kt:5-32` |
| `userId`, `tenantId`, `UPAR` and other attribute cache | current user's object id and cached attributes | `J/extensions/SharedPrefs.kt:17-46` |
| `hpam.persisted_session.*` | phase, user key, e-mail, SHA-256 of the last card, timestamp; restored after a process restart only if under 10 minutes old and the platform still reports a signed-in user | `J/model/ReaderOutputProcessor.kt:149-168`, `:1423-1483` |
| `printer_name` | the random UUID that identifies this printer on the QR channel | `J/ui/main/OnManualSignInFragmentViewModel.kt:55-61` |
| `dns_ip_cache*` | last resolved addresses per host, used when DNS fails | `J/network/FallbackDns.kt:17-41` |

Plain preference files: `hpam_prefs` (debug logging flag, selected scopes), `print_reporting` (last synced job time), DataStore `license_info` (`J/util/DebugFlags.kt:7-8`, `J/auth/SignInScopes.kt:75-77`, `J/reporting/PrintReportingService.kt:47-51`, `J/di/DataStoreModulesKt.kt:8-10`).

**Legacy Keycloak path.** Card id in user attribute `sequence`; refresh token in attributes `OfflineToken_01…` (1,200 characters each), with a fallback read of the older single `OfflineToken`; profile attributes `DisplayName`, `TenantId`, `AzureUserId`, `UserPrincipalName`, `UPAR` (`J/repository/KeyCloakApiRepositoryImpl.kt:41-44`, `:121-127`, `:150-175`, `:219-245`).

### 4.8 How the token is shared with the other Workpath apps

**Mechanism: an exported Android bound service with an AIDL interface, plus a small client library the other apps embed.** No content provider, no broadcast, no shared file.

| Element | Detail | Source |
|---|---|---|
| Service class | `com.hp.print.hpauthenticationmanager.tokenmanagement.TokenManagementService`, exported, intent action `com.hp.print.hpauthenticationmanager.usermanagement.BIND_SERVICE` | `HPAM-A/app/src/main/AndroidManifest.xml:80-87` |
| Manifest gate | requires `android.permission.GET_PACKAGE_SIZE`, a normal permission any app can hold; the manifest comment says it was chosen only so the permission survives an uninstall | `AndroidManifest.xml:18-22`, `:82` |
| Real gate | every AIDL method first calls `enforceSameSignature()`: the caller's package must be signed with the same certificate as the hub | `J/tokenmanagement/TokenManagementService.kt:95-109` |
| Interface | `ITokenManagementService`: `setTokens`, `setRefreshToken`, `getToken`, `getNewToken`, `onUserSignIn`, `onUserSignOut`, `registerListener`, `unregisterListener`, `setLaunchAppAfterAuthCompleteAndStartAuth`, `getProperty`, `updateProperty`, `getAccessForRefreshToken`, `getUserProperty`, `updateUserProperty` | `UM/aidl/com/hp/print/hpauthenticationmanager/tokenmanagement/ITokenManagementService.aidl` |
| Push callbacks | `IUserListener`: `onUserSignIn(token)`, `onNewAccessToken(token)`, `onUserSignOut()` | `UM/aidl/…/IUserListener.aidl` |
| Client library | `usermanagement.aar`: `UserManagementProxy(context).subscribeUserManagement(cb)` binds; `UserManagement` wraps the binder; `UserManagementProxyKt.listenForToken()` gives a flow of `Pending / Exists(token) / NotExists / AuthManagerMissing` | `UM/java/…/usermanagement/UserManagementProxy.kt`, `UserManagement.kt`, `UserManagementProxyKt.kt` |
| Expected consumers | manifest `queries` lists `com.hp.print.cypher.teams`, `com.hp.print.cypher.sharepoint`, `com.hp.print.cypher.onedriveforbusiness`, `com.hp.print.mailflowas`, `com.hp.print.mup.agentas` | `AndroidManifest.xml:10-16` |

Behaviour that consumers rely on:

- **What is shared is one bearer access token string.** The refresh token never leaves the hub through `getToken` or the callbacks (`TokenManagementService.kt:247-255`, `:447-463`).
- **Anti-mix-up check on every read**: the token's `unique_name`, `upn` or `preferred_username` must equal the e-mail of the user the platform reports as signed in; otherwise the hub wipes its tokens and signs the device out (`:123-154`).
- **Refresh loop**: 4 minutes after sign-in and every 4 minutes after, the hub redeems the refresh token and pushes `onNewAccessToken` to every listener (`:162-185`). The rotated refresh token returned by Entra is discarded in this loop (`:173-176`).
- **On-demand refresh**: `getNewToken(listener)` (`:257-270`).
- **"Launch me after sign-in"**: an app that finds no user calls `setLaunchAppAfterAuthCompleteAndStartAuth(uuid)`; the hub stores the uuid, starts a platform sign-in, and passes the uuid to the platform as the access point to auto-launch on success (`:299-328`, `J/sdk/SDKBridgeImpl.kt:222-229`).
- **Per-user properties** for other apps: `getProperty`/`updateProperty` (CSA or Keycloak, with a device cache) and `getUserProperty`/`updateUserProperty` (OneDrive file) (`TokenManagementService.kt:330-422`).

Two more inter-app links:

- `CloudConfigService` (AIDL `ICloudConfigService`, same signature check on register/unregister) pushes the cloud endpoints (authority, Graph, Monitor) to the other apps (`J/cloudconfig/CloudConfigService.kt:60-93`, `UM/java/…/cloudconfig/CloudConfigProxy.kt`). `getConfig()` itself is not signature-checked (`CloudConfigService.kt:76-78`).
- The hub is a **client** of the Universal Print app's service `com.hp.print.mup.agentas.directprint.PrintService` (AIDL `IPrintService`: `fetchJobs(email)`, `releasePullPrintJobs(email)`, `pullPrintTimeoutDuration()`, `cancelPullPrint()`, callback `onStatusChanged(documentsInQueue)`), bound by reflection with `bindServiceAsUser` (`UM/java/com/hp/print/asprinterservice/AsPrintServiceProvider.kt`, `UM/aidl/com/hp/print/asprintservice/IPrintService.aidl`).

### 4.9 Pull-print check during sign-in

Before finishing a sign-in the hub asks Universal Print how many documents wait for the user's e-mail. If the service is missing or does not answer in 10 seconds the step is skipped (`J/model/ReaderOutputProcessor.kt:1306-1393`). If documents wait, a dialog offers release / stay signed in / cancel with a countdown whose length comes from the Universal Print app (`pullPrintTimeoutDuration()`), default 10 seconds; auto-release is driven by the user's `UPAR` flag (`J/ui/printservice/CheckPullPrintJobsFragment.kt:58`, `:83`, `:98-99`, `:236`, `:306-307`, `:329-330`; sampled by grep, not read whole).

### 4.10 The SignalR gateway (QR and mobile app)

| Aspect | Entra back end | Legacy back end | Source |
|---|---|---|---|
| Hub URL | `{signalREndpoint}/api` | `{baseUrl}/printerhub-secure` | `J/signalr/SignalRHubFactory.kt:23-27` |
| Auth | header `Authorization: Bearer <app-only token for api://{clientId}/.default>` set once when the connection is built | bearer from `token/client-credentials` | `J/signalr/SignalRAuthHeaderProvider.kt:19-56`, `SignalRHubFactory.kt:39-41` |
| Event the printer subscribes to | the event **named after the tenant id** | `NotifyAll` | `SignalRHubFactory.kt:46-49`, `J/signalr/SignalRManager.kt:139-147` |
| Message shape | a flat string map; keys read: `id` (must equal this printer's stored name), `secret` (used as card id), `email` | keys `id`, `userName`, `email` | `J/ui/main/OnManualSignInFragmentViewModel.kt:115-146` |
| Printer-to-hub messages | **none**; the printer only listens | none | whole `signalr/` package |
| Reconnect | new connection and new token each time, backoff 1 s doubling to 60 s; state polled every second | same | `SignalRManager.kt:82-108`, `:160-169` |
| TLS | the hub connection uses a trust manager that accepts **any** certificate | same | `J/di/NetworkSecurityModule.kt:24-55`, `SignalRHubFactory.kt:34-36` |

QR content (Entra): JSON `{name, clientId, tenantId, signalREndpoint, oauthBaseUrl}`, each value AES-256-GCM encrypted with a random 12-byte IV under a key hardcoded in the app (`J/ui/main/OnManualSignInFragmentViewModel.kt:186-193`, `J/util/Encryptor.kt:26-50`). QR content (legacy): `{name, secret, baseUrl, authUrl}` in clear, with `secret` fetched from `GET cardless/secret?id=<printerName>` (`OnManualSignInFragmentViewModel.kt:196-206`, `J/network/KeycloakApi.kt:10-14`).

The Function App side of the gateway (negotiate, the method the phone calls, how `secret` is produced) is **not in this lane**: there is no server code in either tree. Because the event is addressed to a whole tenant and filtered on the printer, every printer in a tenant receives every unlock message, including each user's e-mail and virtual card id (inferred from the subscription and filter code).

There is no BLE-specific gateway traffic in this app. In the code the gateway serves the QR/mobile path only; "BLE" reaches the printer through the card reader (4.4).

### 4.11 Card readers

Readers are declared in the HPK as accessories the app **owns** and are opened through the Workpath HID accessory service; the app receives raw HID reports, not key events.

| USB vendor:product (decimal) | Hex | Probable make (inferred from the vendor id, not stated in code) | Decoder |
|---|---|---|---|
| 3111:15354 | 0C27:3BFA | RF IDeas | keyboard usage byte to A-Z / 0-9, Enter ends |
| 1008:69 | 03F0:0045 | HP | raw ASCII bytes, CR (13) ends; newer path: whole buffer as text |
| 2520:1040, 2520:784 | 09D8:0410, 09D8:0310 | Elatec TWN4 / TWN3 | byte arithmetic (+19 for digits, +61 after a shift marker), byte 40 (Enter) ends |
| 1899:21544 | 076B:5428 | HID OMNIKEY | no specific branch in the old path; generic keyboard decoder in the new path |
| 7590:272 | 1DA6:0110 | not known | same as above |

Sources: `HPAM-A/app/packaging_contents_release/hpk.xml:45-80`, `J/sdk/PrinterAccessoryService.kt:282-375`, `J/sdk/PrinterAccessoryService.kt:499-518`.

Two code paths exist, chosen by Android version:

- **Android 12 and later firmware**: accessory events arrive as broadcasts `com.hp.workpath.action.ACCESSORY_STATUS_ACTION` and `…ACCESSORY_REPORT_ACTION`. On context created or resent the receiver calls `AccessoryService.open` then `startReading`; a revoked context marks the reader disconnected. Reports are de-duplicated by ordinal (`J/sdk/AccessoryReceiver.kt:43-140`, `J/sdk/PrinterAccessoryService.kt:173-177`).
- **Older firmware**: observers registered in a foreground service; at start it waits for the accessory service and calls `resendOwnedAccessoryContext` for each owned reader (`J/sdk/PrinterAccessoryService.kt:142-215`, `:238-242`).

Generic keyboard decoder (`J/model/ReaderDataStore.kt:59-142`): 8-byte boot-keyboard reports (modifier, reserved, six key slots); a character is emitted only for a key that was not down in the previous report; shift is honoured; usage 0x28 (Enter) ends the card; full US-layout map for letters, digits and punctuation. The result is lower-cased; if it parses as a UUID the dashes are removed.

Format limits: at most 32 UTF-8 bytes (`J/util/CardValidator.kt:21`); no hex-only check, no length minimum, no checksum. The diagnostics emulator accepts 4 to 6 characters (`J/ui/main/MainActivity.kt:83-84`).

### 4.12 Every use of the Workpath SDK

| API | Used for | Source |
|---|---|---|
| `Workpath.getInstance().initialize` | SDK start, in five places | e.g. `J/sdk/SDKBridgeImpl.kt:47` |
| `AbstractAuthenticationService` callbacks `onPrePrompt`, `onSignIn(Principal)`, `onSignOut` | the platform telling the agent a sign-in prompt is due, a user is in, a user is out | `J/sdk/PrinterAuthenticationService.kt:81-122` |
| `AccessService.initiateSignIn` | start a device sign-in from the app side (card tap, or another app asking) | `J/sdk/SDKBridgeImpl.kt:104`, `J/tokenmanagement/TokenManagementService.kt:319` |
| `AccessService.signIn(SignInAction.CONTINUE)` | ask the platform to show the agent's UI (`AuthActivity`) | `SDKBridgeImpl.kt:113-131` |
| `AccessService.signIn(SignInAction.SUCCESS, AuthenticationAttributes)` | complete the sign-in. Attributes: display name (four admin-selectable forms), user name, e-mail, a constant placeholder password, domain, home folder, user properties, e-mail/fax override defaults from string resources, language, and `AutoLaunchAppAccessPointId` | `SDKBridgeImpl.kt:68-89`, `:183-257` |
| `AccessService.signIn(SignInAction.CANCEL)` | abandon | `SDKBridgeImpl.kt:134-151` |
| `AccessService.signOut` | sign the device out | `SDKBridgeImpl.kt:52-65` |
| `AccessService.getCurrentPrincipal` | is a user signed in, their e-mail, are they admin | `SDKBridgeImpl.kt:154-171` |
| `AttestationService.getAppToken` | wrapper `obtainCredentialsToken()` exists; I found no caller in the files read | `SDKBridgeImpl.kt:174-180` |
| `ConfigService.getDefaultConfig`, `setDefaultConfig`, `AbstractConfigChangeObserver` | read admin configuration, write it back with secrets blanked, be told of changes | `J/config/WorkpathConfigProviderHelper.kt:14-44`, `J/config/WorkpathConfigProvider.kt:48-51`, `:429-435` |
| `accessory.hid.AccessoryService` (`isSupported`, `isReady`, `getOwnedAccessories`, `resendOwnedAccessoryContext`, `open`, `startReading`, observers), `AbstractAccessoryService` | card readers | 4.11 |
| `DeviceService.getString(DeviceAttribute.*)` | serial number (licence, logs), vendor, model, firmware, device id, formatter serial, product number; for reporting, **every** string attribute | `J/model/AppInitialization.kt:110-123`, `J/model/PrinterInfo.kt:44-121`, `J/reporting/StatsRepository.kt:98-112` |
| `StatisticsService.getAllJobsList` | job accounting records | `StatsRepository.kt:37-51` |
| `SuppliesService.getSuppliesInfo` | consumables | `StatsRepository.kt:53-69` |
| `DeviceEventsService.getDeviceEvents` | read but the send is commented out | `StatsRepository.kt:120-135`, `J/reporting/PrintReportingService.kt:97` |
| Manifest permissions | `ACCESS_STATISTICS`, `ACCESS_DEVICE_USAGE`, `ACCESS_SUPPLIES`, `ACCESS_DEVICE_EVENTS`; components guarded by `com.hp.jetadvantage.link.permission.SERVICES_PERMISSION` | `HPAM-A/app/src/main/AndroidManifest.xml:26-30`, `:68-118` |

Panel UI and the platform handshake (`J/ui/main/MainActivity.kt:327-366`, `J/ui/main/AuthActivity.kt:30-55`, `J/model/ReaderOutputProcessor.kt:972-1036`, `:1405-1421`): the platform starts `AuthActivity`, which starts `MainActivity` with an `auth` extra; only an activity started that way may complete a sign-in. On `onPrePrompt` with no card in progress the UI is requested at once; with a card in progress the UI is requested only if the silent path has run for 8 seconds. If the activity does not appear within 10 seconds after `CONTINUE` the handshake is restarted. Pressing Home or Back before completion resets the session.

### 4.13 Sign-out and session timeout

- **Sign-out triggers**: the platform's `onSignOut` callback (panel sign-out button or the device's own inactivity timer); a tap of the signed-in user's own card; a tap of another card; a change of cloud environment; a failed token-owner check (`J/sdk/PrinterAuthenticationService.kt:99-116`, `J/model/ReaderOutputProcessor.kt:435-451`, `:261-267`, `J/tokenmanagement/TokenManagementService.kt:145-153`).
- **What sign-out does**: cancel the refresh loop, erase access token, refresh token and user id from device storage, clear the OneDrive property cache, call `onUserSignOut` on every listening app, stop the service, call `AccessService.signOut`, reset the session (`TokenManagementService.kt:465-490`, `ReaderOutputProcessor.kt:1269-1289`).
- **Session timeout**: the hub has **no inactivity timer of its own**. Search: whole-word, case-insensitive `inactivity|idle|autologout|sessiontimeout` over the main Kotlin of both modules (the random-word list file excluded) gave 0 lines; positive control `DEFAULT_LOGOUT_TIME` gave 3. That constant (10) is only the default pull-print dialog countdown (`ReaderOutputProcessor.kt:112`, `:1500`). The device's inactivity timeout is the session timeout, and the hub learns of it through `onSignOut` (inferred from the absence of any other timer). The only time limits in the hub are the 4-minute token refresh, the 10-minute window for restoring state after a process restart, and the 60-second initialisation timeout.

### 4.14 Device and tenant identity

| Identity | How obtained | Used for | Source |
|---|---|---|---|
| Tenant | `tenantId` in the configuration; one per printer; initialisation waits until it is set | all OAuth URLs, SignalR event name, licence request, QR | `J/model/AppInitialization.kt:359-366` |
| Printer on the QR channel | random UUID generated on first run, kept in device storage | SignalR message filter, QR `name` | `J/ui/main/OnManualSignInFragmentViewModel.kt:55-61`, `:119` |
| Printer for licensing and logs | `DA_SYSTEM_SERIALNUMBER`; `"NoSerial"` if unreadable; `Build.DEVICE` on an emulator | licence request body, App Center event property | `J/model/AppInitialization.kt:110-123`, `J/util/Loggable.kt:108` |
| Printer in reports | all string device attributes (host name, IP, MAC, model, serial, firmware, device id and so on) attached to every record | Log Analytics | `J/reporting/StatsRepository.kt:71-115` |

Nothing authenticates the printer as a device to Entra; all printers of a customer share one client id and one client secret.

### 4.15 Configuration

**Channel.** On a real device the configuration is the app's Workpath "default config": a JSON document of frames, fidgets, sets and items, optionally wrapped as `{schema, uuid, data}` (`J/config/WorkpathConfigProvider.kt:439-449`). It reaches the device from HP Command Center or from the Windows manager's PUT to `/hp/device/webservices/ext/pkgmgt/packages/{uuid}/defaultConfig` with schema `com.hp.jetadvantage.link.config.default` (`ASM/src/Core/Workpath/PackageManagement/WorkpathDeviceClient.cs` `SetConfigurationAsync`). The form the admin fills is generated from `HPAuthenticationManager.moc`. There is **no admin screen on the panel** for these values: a settings fragment exists but its menu entry is compiled out (`J/ui/main/MainActivity.kt:403`).

On arrival the app validates, stores the full configuration encrypted on the device, then writes the configuration **back** to the platform with `apikey`, `appcenterkey` and `serviceEndpointSecret` blanked, so the secret cannot be read back from the management side (`WorkpathConfigProvider.kt:53-66`, `:111-155`). A debug broadcast `com.hp.print.hpauthenticationmanager.readconfig` forces a re-read (`:39`, `:79-93`).

| Frame (admin label) | Field id | Meaning | Default | Source (`.moc` line / parser line) |
|---|---|---|---|---|
| Connection Options | `tenantId` | Entra tenant | none, required | moc 15 / `:250-252` |
| | `serviceEndpointClientId` | app registration client id | required when CSA on | moc 32 / `:269-271` |
| | `enableCsa` | Entra back end on/off | false | moc 49 / `:254-256` |
| | `serviceEndpointSecret` | app registration secret (masked type) | required when CSA on | moc 108 / `:272-274` |
| | `signalREndpoint` | gateway URL; empty means QR off | empty | moc 129 / `:275-277` |
| | `confidentialClientAuthentication` | hidden; confidential user sign-in | false | moc 151-158 / `:258-261` |
| | `baseUrl`, `apikey` | legacy API URL (must be https) and key | required when CSA off | moc 66, 87 / `:263-267` |
| Microsoft Cloud Sovereignty | `cloudConfig` | Commercial, GCC, GCC High, DoD, or Custom with authority / Graph / Monitor URLs | Commercial if absent | moc 177-270 / `:310-326`, `:361-376` |
| Device Options | `console_user_name` | name shown on the panel: first+last, UPN, display name, e-mail | display name if the field is absent | moc 486-519 / `:281-285` |
| Security Options | `mfa` | "Enable Microsoft MFA/2FA/Passwordless Mode" | true | moc 540 / `:289-291` |
| | `disableAutoclicker` | hidden | false | moc 557-564 / `:293-295` |
| Reporting Options | `reporting_string` | `DCE-URL@stream-base-name@DCR-id` | empty = off | moc 587 / `:299-301` |
| License Options | `licenseEndpoint` | licence server base URL | empty | moc 618 / `:305-307` |

Cloud endpoint presets are in `UM/java/…/cloudconfig/model/CloudConfig.kt`: Commercial and GCC use `login.microsoftonline.com`, `graph.microsoft.com`, `monitor.azure.com`; GCC High uses `login.microsoftonline.us`, `graph.microsoft.us`, `monitor.azure.us`; DoD uses `dod-graph.microsoft.us`.

Device-local settings outside that channel: debug logging and the delegated scope selection, both behind a diagnostics menu opened by a tap gesture on the version label and a fixed password compiled into the app (`J/ui/main/MainActivity.kt:85`, `:421-438`, `:492-540`).

### 4.16 Licensing

- Call: POST `{licenseEndpoint}/api/validate` with JSON `{tenantId, serial, nonce}` (`J/model/AppInitialization.kt:84-86`, `J/license/LicenseCheckRunner.kt:52-65`).
- Response: `{token}` where token is an RS256 JWT carrying its certificate chain in the `x5c` header. The chain is validated to a root certificate bundled in the app (`assets/hpauthsuite_root.pem`), revocation checking off; the signature is verified with the leaf key; the `nonce` claim must match; claim `valid` decides (`LicenseCheckRunner.kt:86-135`).
- The HTTP client for this call accepts any TLS certificate and any host name; the trust is in the signed token, not the channel (`LicenseCheckRunner.kt:145-181`).
- States: `Licensed` ("License OK"), `Unlicensed` ("Reached license limit", "License has expired", "Temporary license expired"), `TempLicense` (any error or a non-JSON reply). A device with no stored state starts in `TempLicense`. `TempLicense` older than 20 days becomes `Unlicensed`; `Unlicensed` can never go back to `TempLicense` (`LicenseCheckRunner.kt:71-82`, `:129-141`, `J/license/LicenseInfoStore.kt:36-38`, `:60-87`).
- Re-check cadence: daily when licensed, hourly when temporary, every 15 minutes when unlicensed; also on every configuration change and network return (`J/model/AppInitialization.kt:309-313`, `:368-373`).
- Effect: `Unlicensed` with at least one completed check blocks initialisation with the "no licence" screen and phase `WAITING_FOR_LICENSE` (`AppInitialization.kt:374-382`, `J/model/ReaderOutputProcessor.kt:206-208`).
- Licence status and message are added to every reporting record (`J/reporting/StatsRepository.kt:113-114`).

### 4.17 Error codes

All codes link to one help article (`J/App.kt:63-64`). "AI" is stated to mean "App Initialization" (`J/model/AppInitialization.kt:65`).

| Code | Entra back end trigger | Legacy back end trigger | Source |
|---|---|---|---|
| AI01 | not used | version check or token call threw (network or wrong base URL) | `AppInitialization.kt:538-570` |
| AI02 | not used | token call returned an HTTP error (bad key or server error) | `:572-585` |
| AI03 | initialisation exceeded 60 s; TLS error during the Graph check ("check time and date"); any other exception during the Graph check | TLS handshake failure on the version check | `:235-243`, `:485-504`, `:527-536` |
| AI04 | not used | token call succeeded with an empty body | `:617-627` |
| AI05 | Graph returned 403 on the attribute-definitions read (missing CSA permission or role) | `config/` call failed | `:450-461`, `:600-611` |
| AI06 | `$metadata` not successful; attribute-definitions read failed with a status other than 403 | API version does not start with `v0.` | `:419-431`, `:464-474`, `:513-524` |
| AI07 | no SignalR endpoint configured **and** no reader detected | n/a (needs Entra back end) | `J/ui/main/OnManualSignInFragmentViewModel.kt:152-159` |
| AI08 | SignalR unreachable **and** no reader detected | same | `:165-168` |
| AI09 | SignalR unreachable but a reader is present (shown in place of the QR; card sign-in still works) | same | `:161-164` |

The same code therefore means different things on the two back ends (AI05, AI06), and AI03 covers three unrelated causes.

Other user-visible failures, none with an AI code: no connection, no configuration, no licence screens (`J/ui/main/LoadingFragment.kt:120-134`); toasts "Card-user association is invalid.", "Cannot accept card number longer than 32 1-byte chars", "Please launch Universal Print application."; the too-many-cards screen at 15 cards; Microsoft sign-in failures, where a normalised diagnostic code is logged (`AADSTS53009`, `MICROSOFT_SIGN_IN_FAILED`, `CONFIDENTIAL_CLIENT_NOT_CONFIGURED`, or the raw OAuth `error`), and on the device-code screen the `AADSTS…` number is shown (`J/auth/MicrosoftSignInFailure.kt:24-25`, `J/repository/MicrosoftSsoRepository.kt:30-31`, `J/repository/DeviceCodeRepository.kt:114-124`).

### 4.18 Logging and telemetry

| Channel | Content | When | Source |
|---|---|---|---|
| Android logcat | tag prefix `HPAUTHM `; info and above normally, debug when the debug flag is on | always | `J/util/Loggable.kt:8`, `:71-97` |
| Microsoft App Center Analytics + Crashes | **every info-level log line is sent as an analytics event name**, with properties serial number and "realm" (last path segment of the legacy base URL) | only starts once a logging secret arrives, which only the legacy `config/` call supplies; so effectively legacy-only (inferred) | `J/App.kt:85-96`, `J/util/Loggable.kt:103-111`, `J/model/PrinterInfo.kt:20-23` |
| Azure Monitor Logs Ingestion | job statistics and supplies, each record with a `deviceInfo` object. POST `{DCE}/dataCollectionRules/{DCR}/streams/{base}_StatisticsJobData_CL?api-version=2021-11-01-preview` and `…/{base}_Supply_CL`; a `…_DeviceEvent_CL` sender exists but its call is commented out | Entra back end only, reporting string set; poll every minute; supplies sent only together with new jobs; high-water mark = latest job-done time | `J/reporting/ReportingClient.kt:51-64`, `:95-101`, `:165-171`, `J/reporting/PrintReportingService.kt:60-99`, `:204-210` |
| HTTP logging | method and status only (bodies deliberately excluded) | debug | `J/di/NetworkModule.kt:53-60` |

Before sending, the reporting client deletes the text `OXPd:` from the payload and replaces the six suite uuids with app names (`ReportingClient.kt:84-90`, `:178-185`). The stream suffix in code is `_StatisticsJobData_CL`; the library's START-HERE spells the table `…_StatisticJobData_CL` (see 6.6).

Some debug-level lines print whole tokens and card numbers (`J/tokenmanagement/TokenManagementService.kt:172`, `:194`; `J/model/ReaderOutputProcessor.kt:372`); these are suppressed unless debug logging is switched on.

### 4.19 Outbound network endpoints

| # | Endpoint | Purpose | Auth | Source |
|---|---|---|---|---|
| 1 | `{authority}/{tenant}/oauth2/v2.0/authorize` (WebView) | interactive user sign-in | user | `J/repository/MicrosoftSsoRepository.kt:294-298` |
| 2 | `{authority}/{tenant}/oauth2/v2.0/token` | code exchange; refresh; client credentials for Graph, gateway and Monitor; device-code polling | PKCE / secret | `MicrosoftSsoRepository.kt:288-292`, `J/network/AuthenticationApiMSEntra.kt:13` |
| 3 | `{authority}/{tenant}/oauth2/v2.0/devicecode` | passkey flow | none (public) | `J/repository/DeviceCodeRepository.kt:42-49` |
| 4 | any host the Microsoft page redirects to (federated IdP, Microsoft CDNs) | inside the WebView | user | `J/ui/microsoftsso/MicrosoftSsoFragment.kt:186-191` |
| 5 | `{graph}/v1.0/$metadata`, `/directory/attributeSets`, `/directory/customSecurityAttributeDefinitions`, `/users`, `/users/{id}` | health check and CSA store | app-only bearer | 4.2, 4.7 |
| 6 | `{graph}/v1.0/me/drive/special/approot:/hpam-user-properties.v1.json:/content` | per-user properties | user bearer | `J/storage/OneDriveUserPropertiesStore.kt:134-137` |
| 7 | `{signalREndpoint}/api` (SignalR negotiate + transport) | QR / mobile unlock | app-only bearer | 4.10 |
| 8 | `{DCE}/dataCollectionRules/{DCR}/streams/…` | job and supply logs | app-only bearer (Monitor) | 4.18 |
| 9 | `{licenseEndpoint}/api/validate` | licence | none; signed reply | 4.16 |
| 10 | `help.hpauthsuite.com/support/…` (six fixed article URLs) | help, error codes, supported readers, privacy, EULA, copyright, shown in a WebView | none | `J/App.kt:63-74` |
| 11 | App Center ingestion (SDK default host, not named in code) | analytics and crashes | App Center secret | `J/App.kt:88-95` |
| 12 | Legacy: `{baseUrl}/token/client-credentials`, `/token/refresh`, `/config/`, `/users`, `/users/{id}`, `/cardless/secret`; `/version` one path level up; `{baseUrl}/printerhub-secure` | legacy store and QR channel | client id + API key, then bearer; one "cluster cookie" captured from the first response is replayed and copied into the WebView | `J/network/AuthenticationApiKeycloak.kt`, `J/network/KeycloakApi.kt`, `J/network/VersionCheckApiKeycloakProvider.kt:71-73`, `J/di/NetworkModule.kt:149-185` |

Timeouts on all OkHttp clients: connect 15 s, read 30 s, write 30 s, whole call 60 s (`J/di/NetworkModule.kt:39-42`). All clients use a DNS wrapper that falls back to the last addresses that resolved (`J/network/FallbackDns.kt:24-41`).

### 4.20 The Windows manager's printer-side protocol (relevant because it is server-to-device today)

All calls are HTTPS to the printer with HTTP Basic `admin:<device admin password>`, certificate validation disabled, TLS 1.0 to 1.3 allowed (`ASM/src/Infrastructure/Workpath/WorkpathDeviceClientFactory.cs`).

| Call | Purpose |
|---|---|
| `GET /hp/device/webservices/ext/pkgmgt/installer` | installer idle? (`insIdle`) |
| `GET …/pkgmgt/packages` | installed apps |
| `POST …/pkgmgt/installer/install?clientId=Datasec-HP-AuthSuite-Manager&installSource=isStandardRepository` (multipart, the `.hpk`) | install |
| `GET` / `DELETE …/installer/install/{uuid}` | track (`psCompleted`, `psInProgress`, `psFailed`), clean up |
| `POST …/installer/uninstall?clientId=…&uuid=…`, `GET` / `DELETE …/installer/uninstall/{uuid}` | uninstall |
| `GET` / `PUT …/pkgmgt/packages/{uuid}/defaultConfig` | read / write app configuration |
| `POST https://{ip}:7627/hp/device/webservices/OXPd/DeviceInfoService` (SOAP 1.2, action `…/IDeviceInfoService/GetManufacturerInfo`) | model, host name, product number, serial |
| IPP `Get-Printer-Attributes` to `ipp://{ip}:631/ipp/print` | is this an HP device, colour? |
| `GET https://{ip}/hp/device/DeviceInformation/View`, `…/InternalPages/Index?id=ConfigurationPage` (HTML scrape) | name, location, firmware, Workpath status and version |

Source for the table: `ASM/src/Core/Workpath/PackageManagement/WorkpathDeviceClient.cs`, `ASM/src/Core/Workpath/DeviceInfo/DeviceInfoClient.cs`, `ASM/src/WinUI.Logic/Services/DeviceDiscovery/DeviceDiscoveryClient.cs`. Device admin passwords are stored with Windows DPAPI, machine scope (`ASM/src/Core/Utilities/DataProtector.cs`). **Datasec already calls an OXPd 1.x SOAP service on port 7627 in shipping code**, for device information only.

---

## 5. What this means for the port

### 5.1 Behaviour by where it must run

| Behaviour today | Needs the device for | Server-side equivalent needs | Finding |
|---|---|---|---|
| Register as the device's sign-in agent; be told pre-prompt, sign-in, sign-out | the platform's agent slot | an OXPd authentication agent registration whose callbacks reach the server; the server completes the device session with the same attribute set (display name in one of four forms, e-mail, user name, domain, language, app to auto-launch) | 4.12 |
| Start a sign-in from a card tap with nobody at the prompt | reader events arriving outside a prompt | reader events delivered to the server at any time, and a way for the server to start a device sign-in unprompted. The whole "tap to sign in, tap again to sign out, tap to switch user" behaviour depends on this | 4.3 |
| Read the card | USB HID reports from an owned reader | raw HID reports (or already-decoded text) forwarded by the device, per reader, with vendor and product id. The six decoders are plain byte logic and move to the server unchanged | 4.11 |
| Show sign-in screens (welcome + QR, wait, errors, too many cards, pull-print dialog, passkey code) | the panel | pages served by the server and shown in the device's browser | 4.3, 4.9 |
| Interactive Microsoft sign-in | an embedded browser the app controls: URL interception of a custom scheme, script injection, cookie wipe, UA override | either (a) the device browser doing a normal web redirect back to the server (confidential web client with an https redirect URI; no script injection, cookie isolation depends on the device browser), or (b) device-code flow, which needs nothing from the device but a page showing a QR and a code. The hidden confidential-client mode proves the token logic already works with a secret | 4.5, 4.4, 4.6 |
| Silent sign-in (no-MFA mode) | nothing | identical: read refresh token from CSA, redeem, complete device session | 4.3 |
| QR / mobile sign-in | panel to show the QR; a socket to the gateway | one server connection to the gateway per tenant instead of one per printer; the server routes each message to the right device by printer name. The server must give each device a stable name and render a per-device QR | 4.10 |
| Card mapping and token store | nothing | identical Graph calls with the same attribute set, blob format and key, so cards enrolled on Workpath work on OXPd and the reverse | 4.7 |
| Token sharing with other apps | Android binder, same-certificate check | an in-process (or internal API) token broker keyed by device session: get token, refresh every 4 minutes or on demand, sign-in / new-token / sign-out notifications, per-user property get and set, "launch me after sign-in" | 4.8 |
| Token-owner check against the device's signed-in user | `getCurrentPrincipal` | the server already owns the mapping device session → user; keep the check as "token subject equals session user" | 4.8 |
| Sign-out and timeout | platform callback | the device must notify the server of every sign-out, including its own inactivity timeout, or the server must poll session state; otherwise tokens outlive the session | 4.13 |
| Pull-print check at sign-in | binder to the Universal Print app | a call between two server components; the dialog becomes a served page | 4.9 |
| Configuration | Workpath config channel, device-encrypted store | server configuration per tenant; the client secret is held once on the server instead of on every printer | 4.15 |
| Licensing | device serial number | the device serial obtained remotely (Datasec already reads it over OXPd 1.x SOAP, 4.20); same `{tenantId, serial, nonce}` request, so the licence server needs no change if each OXPd device is to count as one seat | 4.16, 4.14 |
| Job, supply and device reporting | on-device statistics, supplies and device-attribute services | remote statistics / usage / supplies services, same Log Analytics streams and record shape so existing customer workbooks keep working | 4.18 |
| Screenshot blocking, encrypted device storage | Android | not applicable; replaced by server-side secret storage | 4.5, 4.7 |

### 5.2 Requirements and constraints

1. **Keep the CSA contract byte-for-byte** if mixed fleets must share enrolments: attribute set name, `cardId` blob algorithm and key, `refreshToken` chunk format (`NNN_` + 60 characters), `UPAR`, the 15-card and 50-value limits (4.7). This is the integration point with the existing Workpath product; no bridge between the two products is needed beyond it.
2. **Same app registration or a second one is a design choice the code constrains.** A stored refresh token can only be redeemed by the client it was issued to. If the server uses a different client id from the Workpath apps, a user enrolled on one platform in no-MFA mode will fall back to interactive sign-in on the other, and each platform will then overwrite the other's stored token (4.3, 4.7). Sharing one registration means adding a web redirect URI and running it as both public (Workpath) and confidential (server).
3. **The stored-token model is single-slot per user.** Two printers, or two platforms, signing the same user in keep overwriting one CSA value; today that is harmless because all devices use the same client and the rotated token is discarded anyway (4.8, 6.3).
4. **Session-scoped state must become per-device.** The Android app assumes exactly one device, one session, one signed-in user, one refresh loop. The server needs that whole state machine instantiated per device, with the same "stale session id" guard (4.3).
5. **Graph load concentrates.** Each sign-in costs 2 to 7 Graph calls, among them an eventually-consistent filtered search over all users, three directory-schema reads and a PATCH (4.7). From one server address for a whole fleet this needs caching of the schema checks and throttling handling, which the app does not have.
6. **Two clouds beyond commercial are in production code** (GCC High, DoD) plus a custom option; the server must carry authority, Graph and Monitor endpoints per tenant (4.15).
7. **The "launch app after sign-in" contract** (an access-point id passed at sign-in completion) needs an equivalent on OXPd or the "open OneDrive, get asked to sign in, land in OneDrive" behaviour is lost (4.8).
8. **The legacy Keycloak back end need not be ported** unless a customer still on it will run OXPd devices; it doubles every code path (4.1). Decision taken for this report: treat it as out of scope and ask (question 7.3).

### 5.3 Reusable parts

- The six reader decoders and the generic keyboard-report decoder (`ReaderDataStore`, `PrinterAccessoryService`): portable logic, with unit tests in the tree (`ReaderOutputProcessorTest`, `AccessoryReceiverTest`; not opened).
- `MSEntraApiRepositoryImpl` as the specification of the CSA store, and `CardValidator` as the specification of the blob.
- `DeviceCodeRepository`: a complete, UI-free device-code client.
- `MicrosoftSsoRepository`: authorize-URL construction, both client modes, error normalisation including the Intune case.
- `LicenseCheckRunner`: the full licence protocol and the bundled root certificate.
- `ReportingClient`: stream names and record shape.
- The `.moc`: the complete list of tenant-level settings an admin expects.
- From the Windows manager: device discovery (IPP), the OXPd 1.x DeviceInfoService SOAP call, the device-group and job model, DPAPI-protected admin passwords. It is the natural home, or at least the model, for registering an OXPd solution on a fleet.

### 5.4 Traps

- **The autoclicker and the UA spoof are compensations for running Microsoft's page in a small embedded WebView.** They will not exist in a device browser the server does not control; expect different Microsoft page behaviour, and expect Conditional Access to see a different client (4.5).
- **Intune app-protection tenants are already a dead end on the printer** (handled, not solved). The server model changes what Entra sees as the client and may change this outcome either way (4.3, 4.5).
- **`prompt=login` plus cookie wipe is how user isolation is achieved today.** On a shared device browser the cookie jar is not the server's to wipe (4.5).
- **AI codes are overloaded**; a server needs its own finer codes while still showing the documented ones on the panel (4.17).
- **An eventually-consistent search**: a card enrolled seconds ago may not be found, and a failed search looks like "unknown card" and triggers re-enrolment (4.7).
- **Do not copy the weaknesses listed in section 8.**

---

## 6. Contradictions and doubts

1. **Enrolment prompt.** The PlantUML flow says the app prompts for e-mail/UPN and writes the card mapping before Microsoft sign-in (`HPAM-A/app/plantuml/Card Tap — First-time or MFA mode (interactive sign-in)` lines 19-24). The code shows the Microsoft page first and writes the mapping after, using the identity in the token (`J/model/ReaderOutputProcessor.kt:487-518`, `:761-785`). Code wins.
2. **"Encrypted refresh token".** Both card-tap diagrams say the refresh token is encrypted with a tenant key before it is written to CSA and decrypted on read. The code chunks the raw token and writes it; `Encryptor` is referenced only by the QR builder (grep over both modules: `Encryptor.` appears in `OnManualSignInFragmentViewModel.kt:188-192` and nowhere else; positive control: `CardValidator.` found in 6 places). There is no tenant key anywhere; the only key is one compiled into every copy of the app.
3. **Rotation.** The no-MFA diagram says a rotated refresh token is re-encrypted and written back. In code the silent path returns only the access token to the caller (`J/tokenmanagement/TokenManagementService.kt:435-436`) and the refresh loop keeps the old refresh token (`:173-176`); CSA is rewritten with the token it already held. If the tenant rotates and revokes refresh tokens, the stored one eventually dies and the user is sent to interactive sign-in.
4. **Scopes.** START-HERE lists a broad delegated scope set as what the registration uses. The app requests only `openid profile offline_access` unless someone enables more per device in a hidden menu (`J/auth/SignInScopes.kt:7-29`). An older sample token in a source comment shows a broad `scp` including print scopes (`J/repository/AzureUserModel.kt:28-71`), so earlier versions probably requested more, or the tenant's consent makes Entra return more (doubt; not resolvable from this lane).
5. **MFA default.** The app flavor default for `isMfaEnabled` in `Config` is true and the parser defaults to true (`J/config/Config.kt:15`, `WorkpathConfigProvider.kt:289-291`); the emulator flavor defaults to false (`HPAM-A/app/build.gradle.kts:81`). Not a conflict for production, but tests on the emulator run the other mode.
6. **Table name.** START-HERE: `HpamPrinterLogs_StatisticJobData_CL`. Code: `<base>_StatisticsJobData_CL` (`J/reporting/ReportingClient.kt:52`). Code wins; the base name is whatever the admin put in the reporting string.
7. **Console user name default.** The data class default is first+last name (`Config.kt:14`), the parser's fallback when the field is missing is display name (`WorkpathConfigProvider.kt:281-285`).
8. **Redirect URI scheme vs package.** The redirect is `com.hp.hpauthenticationmanager://…` while the package is `com.hp.print.hpauthenticationmanager` (`MicrosoftSsoRepository.kt:33`, `build.gradle.kts:25`). Harmless (the URL is intercepted, never dispatched), but any document that derives one from the other will be wrong.
9. **`hpk.xml` date** is 20240101 and vendor "HP Inc" for a 2026 build (`hpk.xml:5-6`); looks like a fixed template value.
10. **Reader list.** START-HERE names three BLE-capable readers; the HPK owns six vendor/product pairs and the old-firmware code path decodes only four of them (4.11). Which path real fleets run depends on firmware.
11. **`README.md` of the Windows manager** names the installer `.msi`; the installer is built with Inno Setup, which produces an `.exe` (`ASM/README.md:11`, `ASM/installer/README.md`). Stale wording.

---

## 7. Questions for Kam or his team

1. **Will the OXPd server use the same Entra app registration as the Workpath apps, or its own?** Why it matters: it decides whether no-MFA users move between Workpath and OXPd printers without re-authenticating, and whether the two platforms fight over the single stored refresh token (5.2 items 2 and 3). Assumed if unanswered: same registration, with an added web redirect URI and the server acting as a confidential client.
2. **Must cards enrolled on Workpath work on OXPd printers and the reverse, in the same tenant?** Why: if yes, the server must reuse the CSA blob format including the compiled-in key, which then has to be treated as a long-lived shared secret; if no, the port can use a per-tenant key and fix the weakness. Assumed: yes, full interoperability, key reused, with a planned versioned migration.
3. **Is the legacy Keycloak back end still in use by any customer who will buy OXPd?** Why: it doubles the state machine and the storage layer. Assumed: no; Entra CSA only.
4. **Where is the source of the SignalR / Function App gateway and of the HP Secure Authentication mobile app?** Why: the printer side shows only the receiving half; the method the phone calls, how the per-user `secret` is generated, and who may publish to a tenant's event are unknown from this lane, and the server must either reuse or replace that contract. Assumed: gateway reused unchanged, the server subscribing once per tenant.
5. **Which interactive sign-in does the team want on OXPd panels: Microsoft's page in the device browser, or device code (QR + code) only?** Why: it is the largest behavioural difference from today, drives Conditional Access results, and decides whether a browser-capable panel is required for enrolment. Assumed: device code as the baseline that works everywhere, browser redirect where the device browser can do it.
6. **How do the other four apps obtain Graph permissions today, given the hub requests only `openid profile offline_access` by default?** Why: the server-side token broker must issue tokens those functions can use; if each app relies on tenant-wide admin consent making the default token broad, the server must request scopes the same way. Assumed: admin consent on the registration makes the token carry the full delegated set; to be confirmed in the app lanes.
7. **Is one licence seat per printer serial still the model for OXPd, or per server?** Why: the licence request carries a serial; a server speaking for many printers must either loop per device or change the protocol. Assumed: per device serial, unchanged licence server.
8. **Is the tenant-wide broadcast of unlock messages on the gateway accepted, or should the port fix it?** Why: with a central server the natural design is one subscriber per tenant, which removes the exposure for OXPd devices but not for Workpath ones. Assumed: accepted for Workpath, fixed by design for OXPd.

---

## 8. Secrets and sensitive items seen (locations only), and weaknesses not to carry over

### 8.1 Secrets and personal data in the tree

| Location | What is there |
|---|---|
| `HPAM-A/app/build.gradle.kts:35-38` | release keystore file name, store password, key alias and key password hardcoded |
| `HPAM-A/datasec_printer_keystore` | the release signing keystore itself is committed. This key is the trust anchor of the inter-app token service (4.8) |
| `HPAM-A/app/notes:15-31` | test account e-mail addresses of a real person and plaintext passwords; line 66 repeats the keystore password; lines 7-19 show internal device IP addresses; line 70-71 an Azure subscription path and an id |
| `HPAM-A/config.properties` | populated values for an API key, client id, tenant id, an app registration secret, SignalR endpoint, reporting string, licence endpoint (commented alternates included) |
| `J/util/CardValidator.kt:10`, `J/util/Encryptor.kt:12` | one 256-bit AES/HMAC key hardcoded, used both for the CSA card blob and for the QR payload |
| `J/ui/main/MainActivity.kt:85` | the diagnostics-menu password hardcoded |
| `HPAM-A/app/moc_file/config.cfg`, `config_kc.cfg` | sample configurations with non-empty tenant id, client id, a 40-character secret field (`config.cfg`) and a 32-character API key field (`config_kc.cfg`) |
| `HPAM-A/app/src/test/resources/*.cfg` (4 files) | dev-staging configurations with populated secret / API-key fields; `.gitleaks.toml:3-7` allow-lists this whole folder, so the scanner will never flag them |
| `J/repository/AzureUserModel.kt:28-71` | a decoded real access-token payload in a comment: tenant id, app id, object id, a person's name and UPN, an IP address |
| `ASM/installer/artifact-signing-metadata.json` | code-signing account metadata (not opened; described in `ASM/installer/README.md`) |
| `HPAM-A/app/src/main/assets/hpauthsuite_root.pem` | a root certificate (public material, listed for completeness) |

### 8.2 Weaknesses in the existing product the port should not carry over

1. **A tenant-wide client secret on every printer.** The secret grants app-only Graph access wide enough to read and write security attributes on any user and create directory schema (4.6, 4.7). On a server it is held once and can sit in a vault.
2. **User refresh tokens stored in plain text in a directory attribute**, readable by anyone with the attribute-reader role and by every printer holding the secret; the documentation in the tree says they are encrypted (6.2).
3. **One global hardcoded key for all customers** protects the card blob and the QR payload; the card "encryption" is deterministic by design (needed for the prefix search), so equal cards give equal blobs and anyone with the app binary can decrypt every customer's card numbers (4.7).
4. **TLS verification disabled** on the SignalR hub connection (bearer token and unlock messages exposed to a network attacker who can then inject an unlock) and on the licence call; in the Windows manager on every device call, with the device admin password sent by Basic auth and TLS 1.0/1.1 allowed (4.10, 4.16, 4.20).
5. **Unlock messages are broadcast per tenant and filtered on the device**; each carries a user's e-mail and virtual card id, which is itself a sign-in credential in no-MFA mode (4.10).
6. **In no-MFA mode a card number alone is a full credential** for the user's Microsoft data, with no second factor and no device binding; the passkey path performs no licence-independent check either. This is the product's intended trade-off, but the server should at least rate-limit and audit card lookups, which the app does not.
7. **OAuth `state` is generated but never verified** (4.5). Low risk inside a private WebView; a real risk once the redirect is an https endpoint on a server.
8. **Debug entry points left in release code**: a broadcast receiver with action `action`, registered with no permission, that injects a card id; receivers for `.signout` and `.signin` registered with no permission, and an explicitly exported one for `.readconfig`; a fixed diagnostics password that unlocks card emulation (4 to 6 characters) and scope changes (4.3, 4.15, `J/sdk/PrinterAuthenticationService.kt:61-65`).
9. **`CloudConfigService.getConfig()` skips the signature check** that its sibling methods enforce (4.8).
10. **Every info-level log line becomes a third-party analytics event name** on the legacy path, with the serial number attached; debug logging prints whole tokens (4.18).
11. **Silent failure modes that look like success or like "new user"**: a failed card search is treated as an unknown card; `updateUser` swallows all errors except too-many-cards, so a sign-in can complete without the mapping or token being saved (`J/repository/MSEntraApiRepositoryImpl.kt:126-127`, `:498-502`).
12. **Signing keystore and its password in the repository**: anyone with the repository can sign an app that the hub's signature check will accept and receive user tokens (8.1, 4.8).
