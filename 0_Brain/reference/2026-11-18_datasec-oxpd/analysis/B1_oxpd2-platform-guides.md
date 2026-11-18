# B1 — OXPd2 platform model, from the SDK guides and portal pages

Lane B1, Datasec / OXPd, 2026-11-18. Source set: `OXPd2/Docs/SDK-Documentation/guides/` and `OXPd2/Docs/*.md`.

Citation shorthand used throughout (paths are relative to the library root `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`):
- `G/x.md:N` means `OXPd2/Docs/SDK-Documentation/guides/x.md`, line N.
- `P/x.md:N` means `OXPd2/Docs/x.md`, line N (the developer-portal pages).
- "(inferred)" marks a conclusion of mine that no document states.

## 1. BLUF

This lane holds HP's own description of the OXPd2 platform: 46 guides (SDK Beta 10 documentation app) and 7 portal pages. The five facts that most shape the port:

1. **An OXPd2 "solution" is server code plus a signed bundle of declarations.** No partner code runs on the printer. The bundle (`solution.bdl`) holds a manifest of registration records that tell the device which URLs on the solution server to call and which tiles and agents to show; the panel UI is a web page served by the solution server and rendered in the device's embedded browser (`P/how-it-works.md:13,30,32`, `G/applicationServiceOverview.md:19`).
2. **The network is two-way.** The device must reach the server (browser page loads and every callback "target"), and the server must reach the device (OAuth token grants, install, login, launch, HID open, every REST call) (`G/architectureModel.md:580,598`, `G/securityModel.md:136`). Nothing in the guides offers a device-initiated-only mode; WebSocket and TCP targets are "not currently supported" (`G/architectureModel.md:620,629-632`).
3. **A production bundle must be signed by HP after "VAV"**, with self-certified testing on one device from each of seven device groups for an authentication solution; an unsigned bundle installs only on a device in LaserJet Debug Bridge (developer) mode, and switching that mode wipes all solutions (`P/publish.md:11,97-99`, `G/securityModel.md:34`, `G/debugBridge.md:52`).
4. **Sign-in is a first-class agent model** that fits the hub: the device calls the server's pre-prompt, prompt page, post-prompt and sign-out endpoints; a card swipe arrives at the server as raw HID reports and the server answers with `login(succeeded, user details)`; the user's attributes then live in the device's Security Context (`G/authenticationServiceOverview.md:66-74,147-164`, `G/usbAccessoriesOverview.md:304-334`).
5. **The embedded browser is Chromium 87 (QtWebEngine 5.15) with file input, downloads, pop-ups and tabs disabled, and its cookie, cache, memory and "hooks" behaviour are all declared "still under development"** (`G/applicationServiceBrowserUseModel.md:11,68,89-98,108,115,195,205`). Every Microsoft sign-in page and every document picker the suite shows must work inside that.

Also decisive: OXPd2 devices do not run OXPd1 and OXPd1 devices do not run OXPd2 (`P/how-it-works.md:28`), so "OXPd 1 and 2" means two device-facing adapters behind one server; and the platform is still labelled Beta, with the compatible-device list "to be defined" (`P/oxpd2.md:17`, `P/compatible-devices.md:9`).

## 2. Coverage

| Set | Count | How read |
|---|---|---|
| Library orientation (`START-HERE.md`, `README.md`, `README-INDEX.md`) | 3 | Whole, by me |
| Portal pages `OXPd2/Docs/*.md` | 7 of 7 | Whole, by me |
| Guides read whole by me | 23 | Every line: introduction, architectureModel, securityModel, sdkUserGuide, securityServiceOverview, securityServiceRegistration, solutionManagerOverview, solutionManagerRegistration, authenticationServiceOverview, authenticationServiceRegistration, applicationServiceOverview, applicationServiceBrowserUseModel, applicationServiceRegistration, usbAccessoriesOverview, usbAccessoriesRegistration, pullPrintDemoGuide, printJobServiceOverview, printJobServiceRegistration, ews, solutionPackagingUtility, solutionPackagingUtilityCli, kioskAndBrowserDemoGuide, debugBridge |
| Guides read whole by a sub-reader (A: scan, copy, stored jobs, IPP) | 8 | scanJobServiceOverview, scanJobServiceRegistration, copyServiceOverview, copyServiceRegistration, simpleScanDemoGuide, simpleCopyDemoGuide, storedJobsDemoGuide, printJobIppExtensions. Their findings are in section 4.13 and are marked "(sub-reader A)"; I did not re-read these files line by line |
| Guides read whole by a sub-reader (B: examples, statistics, device, tools) | 16 | exampleOverviewGuide, jobStatisticsServiceOverview/Registration, jobStatsDemoGuide, suppliesServiceOverview/Registration, deviceUsageServiceOverview/Registration, deviceServiceOverview/Registration, sdkSupportServiceOverview/Registration, solutionDiagnosticsOverview/Registration, postmanOXPd2Collection, debugBridge (also read by me). Findings in sections 4.14 to 4.16, marked "(sub-reader B)" |
| Guides total | 46 | 23 + 8 + 16 − 1 (debugBridge read twice) = 46. The lane message says 48 and `START-HERE.md:65` says 47; the folder holds 46 `.md` files (counted with `ls`) |
| Sequence diagrams | 7 PNG in `sequence-diagrams/`, 283 PNG in `md-img/` | All are bitmap images, there is no text source. I viewed 7 that carry mechanism: `md-img/service/authentication/sequence/Authentication_With_PrePrompt.png`, `Authentication_With_No_PrePrompt.png`, `Authentication_Initiated_by_Agent.png`, `md-img/service/solutionManager/sequence/Solution_Install.png`, `md-img/service/application/sequence/Application_Session.png`, `md-img/securityModel/securityModel-deploymentMechanisms.png`. The other images (mostly screenshots) were not opened |
| Not opened | `openapi/` (16 specs), `code-samples/` (448 files) | Outside this lane. One exception: I listed the title, version and paths of `userPolicy.openapi.json` and `webHook.openapi.json` because the guides are silent on both (section 4.12) |

Searches behind every "not found" in this report were run over the untruncated text of all 46 guides plus the 7 portal pages, counting matches, with a positive control (`solutionManager`: 91 matches). Zero matches for: `userPolicy`, `user policy`, `webHook`, `web hook`, `mTLS`, `client certificate`.

## 3. Inventory

| Item | What it is | Source |
|---|---|---|
| Platform status | "OXPd2 (Currently in Beta)" | `P/oxpd2.md:17` |
| SDK contents | demos, documentation app, examples, libraries (.NET, Java, JavaScript), specifications, tools | `G/sdkUserGuide.md:130-137,218-222` |
| Demos (each in .NET, Java, JS, with a prebuilt bundle and an admin web view) | Kiosk and Browser Examples, Pull Print with Authentication, Simple Scan, Simple Copy, Statistics, Stored Jobs | `G/sdkUserGuide.md:143-158` |
| Tools | Solution Packaging Utility (GUI and CLI), Postman collection with a "multipart-packager", development certificates and a certificate script | `G/sdkUserGuide.md:247-252`, `G/sdkUserGuide.md:45-55` |
| Build prerequisites (SDK guide) | Visual Studio 2022; OpenJDK 21.0.4 and Gradle 8.10; NodeJS 22.11 and Yarn 1.22.22; SPU needs .NET Desktop Runtime 8, Windows 10 with WSL 1 (Ubuntu 22.04 default) or Ubuntu 22.04+ | `G/sdkUserGuide.md:17-39` |
| Services with guides | application, authentication, copy, device, deviceUsage, jobStatistics, printJob (plus IPP extensions), scanJob, sdkSupport, security, solutionDiagnostics, solutionManager, supplies, usbAccessories | file list of `G/` |
| Services with an OpenAPI spec but no guide | userPolicy ("1.0 (Alpha 2)"), webHook ("1.0 (Beta 3)") | `OXPd2/Docs/SDK-Documentation/openapi/userPolicy.openapi.json`, `webHook.openapi.json` (info block only) |
| Demo ports named in my guides | Pull Print 5050, Kiosk 5450; example host 5000 (5001 also appears in its context file) | `G/pullPrintDemoGuide.md:65`, `G/kioskAndBrowserDemoGuide.md:65`, `G/exampleOverviewGuide.md:63,106` |
| Device-side fixed points | Service discovery at `/cdm/servicesDiscovery`; OAuth2 token resource `/cdm/oauth2/v1/token`; OXPd2 services under `/ext/<service>/v1/...`; remote browser debugger on port 9211 in developer mode | `G/architectureModel.md:508,537,553`, `G/debugBridge.md:73` |

## 4. Findings

### 4.1 What a solution is and where its code runs

- HP's definition: OXPd "centralizes the 3rd party code (called a Solution) on a Solution Server connected to the same network"; the device administrator configures devices to work with that server (`P/how-it-works.md:13`).
- The platform is "a set of Web Services for device management and control plus an embedded Web Browser used for all front panel walkup user interactions" (`P/how-it-works.md:30`).
- Two kinds of extension: **Agents** extend core device functions (authentication, authorisation, statistics, quota); **Applications** are walk-up workflows. One solution may hold any combination (`P/how-it-works.md:30`).
- A **Solution Bundle** defining those agents and applications is installed on the device by a device administrator; an optional **Solution Context** carries installation-specific values "such as the hostname of the customer's Solution Server" (`P/how-it-works.md:32`).
- An OXPd2 Application "is fundamentally a web application that is hosted by a solution on an external server/platform"; installing the bundle puts a tile (icon and title) on the home screen; touching it loads the web application in the embedded browser (`G/applicationServiceOverview.md:19`).
- The SDK introduction names the server languages: "Host your Java or .NET solution on an external server" (`G/introduction.md:4`); a JavaScript (NodeJS) library and demos also ship (`G/sdkUserGuide.md:25-27,158`).
- The API is REST-like with JSON, a set of independently versioned services, replacing the WS-* and REST-XML models of earlier OXPd (`G/architectureModel.md:4-11`). Service URLs are not fixed; a client discovers them per device at run time from `/cdm/servicesDiscovery`, and binds to a service by major version (`G/architectureModel.md:15,504-508`).
- Multi-part requests: JSON "content" part first, then named parts (used for install, context, start intent, certificates) (`G/architectureModel.md:210-212`). No URL may exceed 2018 bytes (`G/architectureModel.md:175`). Duplicate HTTP headers "may cause errors" (`G/architectureModel.md:101`).

### 4.2 The callback ("target") model: how the device calls the server

- "Most OXPd2 API communication is client-initiated"; when the device must start a conversation it uses a callback target (`G/architectureModel.md:580`).
- Registration is **persistent** (in the manifest, lives as long as the solution is installed) or **transient** (created at run time, for example the I/O target of an opened HID accessory) (`G/architectureModel.md:594-596`).
- HP's guidance for server solutions: use client targets "which allow the device to establish the communication channel only when a callback is needed" (`G/architectureModel.md:598`).
- Only HTTP and bundle target patterns are implemented. `webSocketClientTarget`, `webSocketDeviceTarget`, `tcpSocketClientTarget`, `tcpSocketDeviceTarget` are "Not currently supported" (`G/architectureModel.md:620,627-635`).
- Every HTTP client target has: `scheme` (http or https), `host` (authority, may include a port), `path`, optional `authorization` (HTTP Basic username and password, or a bearer token), optional custom `headers`, optional `retry` (`timeoutSeconds`, `maxRetries`, default 0) (`G/architectureModel.md:645-662`).
- A **payload** target receives a POST of JSON holding `payloads[]` and a `sequence` number that starts at 0, increments per POST and "resets on device reboot"; payloads are delivered in order and the sequence lets the server detect loss (`G/architectureModel.md:703-711`).
- A **service** target is a small REST surface the server must implement to HP's definition (the authentication agent is the worked case); the solution must define custom headers to receive any session or UI token (`G/architectureModel.md:692-696`).
- **Bindable fields and macros.** A bindable field is either an explicit value or an expression the device expands at run time (`G/architectureModel.md:742-763`). Macro families: `$DEVICE(ID|MODEL_NAME|IPV4_ADDRESS|IPV6_ADDRESS|HOST_NAME)$` (`G/architectureModel.md:889-893`), `$SOLUTION(ID|NAME)$`, `$SOLUTION_SESSION(UI_CONTEXT_TOKEN|AUTHENTICATION_CONTEXT_ID|AUTHENTICATION_CONTEXT_TOKEN)$` (`G/architectureModel.md:933-937`), `$SOLUTION_CONTEXT(key)$` (`G/architectureModel.md:942`), `$SECURITY_CONTEXT(...)$` (section 4.7), date and time, string, encode and decode (Base64, percent, JSON), `$GUID_GENERATE()$` (`G/architectureModel.md:864-988`).
- So the standard way for a server to know which printer is calling is a custom header carrying `$DEVICE(ID)$` on each target (`G/solutionManagerRegistration.md:80-91`).

### 4.3 Security model: trust between device and solution server

**Who authenticates whom.**

| Direction | Mechanism in the guides | Source |
|---|---|---|
| Server calling device | OAuth2 bearer token issued by the device. The device is identity manager, authorisation service and resource service; the device administrator is the resource owner; the solution is the client; one grant per device | `G/securityModel.md:124-136` |
| Device calling server | TLS to the server, validated only against Certificate Authorities in the solution's own store ("The device uses these solution-provided Certificate Authorities exclusively when establishing outbound TLS connections with external solution endpoints"), plus optional HTTP Basic or bearer credentials and custom headers declared in the target | `G/solutionPackagingUtility.md:162`, `G/architectureModel.md:650-658` |
| Device identity presented to the server | No client certificate. Zero matches for "client certificate" or "mTLS" in the guides. The device is identified by macro headers (`$DEVICE(ID)$`) and by whatever shared secret the target's `authorization` carries | search in section 2; `G/authenticationServiceRegistration.md:151-152` |
| Server validating the device's TLS certificate | Not addressed. The EWS guide says a browser "Not Secure" warning is expected until a certificate is installed on the device | `G/ews.md:37,231-246` |

**Three grants on the device's token resource** (`<deviceRoot>/cdm/oauth2/v1/token`, form-encoded POST) (`G/securityModel.md:149-156`):

| Grant | Who uses it | Result | Source |
|---|---|---|---|
| `password` | An installer that holds the device administrator's user name and password | Access token scoped `com.hp.cdm.auth.alias.deviceRole.deviceAdmin`, lifetime 3600 s, no refresh token. Needed for install through the Installer resource | `G/securityModel.md:161-195` |
| `authorization_code` | The solution server, after the device delivers a one-time install code to the solution's notification target (`ntAuthCode`) | Access token (3600 s) and, when `refresh_token_requested=true`, a refresh token; scope `...deviceRole.solutionProvider ...`. `client_id` is the well-known `com.hp.cdm.client.hpE2Solution`. The code must be exchanged within 5 minutes; `reissueInstallCode` on the solution resource sends a new one | `G/securityModel.md:205-250` |
| `refresh_token` | The solution server | New access token (3600 s) | `G/securityModel.md:260-292` |

- The solution token gives access to (1) resources public to all solution providers and (2) resources private to this solution, "which allows a certain level of solution self-configuration that does not depend on device administrator credentials" (`G/securityModel.md:207-212`).
- Solutions on one device are isolated: they "do not share or expose their configurations to each other" (`G/securityModel.md:19`); each solution has its own certificate store (`G/solutionManagerOverview.md:496`); agent collections are "selection collections" in which an owner sees its own records fully and others only by id (`G/authenticationServiceOverview.md:131`).
- The device tracks delivery of the install code: `installCodeState` is `icsPending`, `icsDeliveryFailed` or `icsDelivered` (`G/solutionManagerOverview.md:477`).

**Token types a server ends up holding, per device** (assembled from the guides):

| Token | Obtained how | Lifetime | Grants |
|---|---|---|---|
| Admin access token | password grant | 1 hour, no refresh | Install and uninstall, Application Runtime `reset`, home-screen modify, access to any solution's resources (`G/securityModel.md:103`, `G/applicationServiceOverview.md:395,667`) |
| Solution (provider) access token and refresh token | install-code exchange | 1 hour, refreshable | Own solution resources and context, Application Runtime read, `initiateLaunch`, own agents' `login`, owned USB accessories (`G/applicationServiceOverview.md:34,180`, `G/usbAccessoriesOverview.md:225-227`) |
| UI Context Session Token | Created by the device when an application claims the UI; delivered to the server in a header declared with `$SOLUTION_SESSION(UI_CONTEXT_TOKEN)$`; also readable in the page as `window.oxpd2.uiContextToken` | The life of that UI session | Current Context operations (exit, exec, beep, reset inactivity timer), runtime chrome, start intent, shared USB accessories, priority print (`G/applicationServiceOverview.md:30-34,535`, `G/applicationServiceBrowserUseModel.md:120`, `G/printJobServiceRegistration.md:9-12`) |
| Authentication session id and session token | Created by the device per sign-in attempt; delivered in the pre-prompt and post-prompt bodies and in headers declared with `$SOLUTION_SESSION(AUTHENTICATION_CONTEXT_ID|TOKEN)$` | The life of the authentication session | Secured features and `forceLogout` (`G/authenticationServiceOverview.md:31,78-88,228`) |

**"Access" a solution must be granted.** There are no user-consented scopes. Access is declared, not requested at run time: each service the solution uses needs its registration record (agent) in the signed manifest, and the install-code exchange yields a token whose scope reflects the solution-provider role. Examples: no Security Agent record, no `$SECURITY_CONTEXT` expansion ("Access Denied") (`G/securityServiceOverview.md:166-168`); no Print Job Agent, no priority print (`G/printJobServiceRegistration.md:9-12`); no Message Center Agent, no message API (`G/applicationServiceRegistration.md:434`); no Runtime Registration Agent, no run-time registration (`G/solutionManagerOverview.md:612`). Who may install is decided by the bundle's HP asset classification and by possession of device-administrator credentials (section 4.4).

**Development certificates.** The SDK ships a root CA `ExtSDKRootCA.pem` already bundled in the demo solutions, and a script that issues a server certificate for a given common name and host IP. HP warns that its private key "is distributed to all approved solution developers" and it must not be used in production (`G/sdkUserGuide.md:45-55,68-78`). The location of those key files is listed in section 8.

### 4.4 Bundles, manifest, signing, the Solution Packaging Utility

**Bundle and manifest.**
- A bundle is an "HP Bundle-wrapped" file of MIME type BDL holding the manifest `solution.json` and the solution's assets (`G/solutionManagerOverview.md:22,32,37`).
- Manifest content: `archiveVersion`, `solutionId` (vendor-defined), `description` (name, description, version, vendor, support contacts), `packages`, `registrations` (the registration records), `contextProfile`, `trustedSites`, `certificateAuthorities`, `configuration` (a solution-defined blob with a MIME type) (`G/solutionManagerOverview.md:43-59`). `hostSets` (device-managed fail-over between server hosts), `installActions` and `uninstallActions` are "not supported in this release" (`G/solutionManagerOverview.md:60-62`).
- **Context profile**: named keys with `isSensitive`, optional `defaultValue`, description, optional JSON schema. Sensitive values are never returned by GET and may not have a default (`G/solutionManagerOverview.md:94-106`).
- **Trusted sites**: the external addresses the device may reach on the solution's behalf, per solution: empty (none), `"*"` (all), or `host;host` with a one-level wildcard (`*.host.com` covers `foo.host.com`, not `foo.bar.host.com`). The value is bindable, so it can be driven from the context after deployment (`G/solutionManagerOverview.md:135-144`).
- **Certificate authorities** may be pre-packaged in the bundle (PEM) (`G/solutionManagerOverview.md:509`, `G/solutionPackagingUtility.md:166`). Certificate and private-key pairs for the solution are specified but "not supported in this release" and can never ship inside a bundle (`G/solutionManagerOverview.md:422,523-525`).
- Registration records "are not intended to be hand-crafted"; the SPU writes them (`G/solutionManagerRegistration.md:24`).

**Asset classification and signing.**

| Classification | Signed by | Installable where | Source |
|---|---|---|---|
| Unverified Aftermarket Solution | Unsigned or developer self-signed (the SPU's output) | Only devices with LaserJet Debug Bridge mode on | `G/securityModel.md:30,34`, `G/solutionManagerOverview.md:153` |
| Restricted Aftermarket Solution | HP, with deployment restrictions | The diagram ties it to the HP cloud deployment platform; OXPd2 solutions do not use it | `G/securityModel.md:31,38`, `G/md-img/securityModel/securityModel-deploymentMechanisms.png` |
| Unrestricted Aftermarket Solution | HP, after V&V | "any FIM installation route" | `G/securityModel.md:32,34`, `G/solutionManagerOverview.md:154` |

- Classification "is not something that can be determined by the solution developer" (`G/securityModel.md:38`).
- V&V asserts bundle integrity, compliance with HP security policy and the JetAdvantage partner agreement, and vulnerability screening (`G/securityModel.md:54-62`).

**Publishing (the portal's process).**
- A production bundle must be "submitted to HP for verification and validation (VAV), and finally signed by HP"; this is done in the HP App Center, which needs a company enrolment and a Master Admin account (during the beta, a new HP.io account) (`P/publish.md:11,48,61`).
- HP's stated VAV focus is security and data protection: HTTPS for all communication, good encryption, no credentials stored in the solution, no sensitive data in logs, no insecure permissions; "enforced by the Solution Packaging Utility" (`P/publish.md:83-91`).
- **Device qualification**: a solution must be tested on at least one device from each MFP group A to E, and a solution with printing-related functionality "(such as printing, authentication, statistics, etc.)" also on one from each printer group F and G, on the latest firmware at submission (`P/publish.md:97-113`).

| Group | Type | Panel resolution | Models named |
|---|---|---|---|
| A | LaserJet A3 MFP | 1280x800 | Enterprise MFP 8601, Managed MFP E826, Color Enterprise MFP 8801, Color Managed MFP E877, E786, Managed MFP E731 |
| B | LaserJet A4 MFP | 1280x800 | Color Enterprise MFP X677, X58045, X57945 |
| C | LaserJet A3 MFP | 1024x768 | Color Managed MFP E785, Managed MFP E730 |
| D | LaserJet A4 MFP | 1024x768 | Color Enterprise MFP 6800/6801, 5800 |
| E | LaserJet A4 MFP | 480x272 | Enterprise MFP M430/M431, Color Enterprise MFP M480, Color Managed MFP E47528 |
| F | LaserJet A4 Printer | 480x272 | Color 6700/6701, X654, Enterprise 5700, X557 |
| G | LaserJet A4 Printer | 320x240 | Color M455, M400, Enterprise M407 |

(`P/publish.md:101-109`)

- Registration: upload the self-signed bundle (maximum 100 MB), declare languages, self-certify the tested devices, upload an app guide, declare the data collected; then a catalogue listing (62x62 icon, categories, description, 1 to 5 screenshots of at most 1024x768, EULA and privacy-statement URLs, support contact) (`P/publish.md:204-298`).
- VAV "is completely automated and generally completes quickly"; HP may review more deeply at any time (`P/publish.md:306-310`).
- On approval the uploaded bundle is replaced by an HP-signed bundle of the same name, downloaded from the App Center. OXPd2 solutions "are not publicly listed"; status reads "Unpublished" (`P/publish.md:326,336-338`).
- An approved app can have "client credentials" added "for use with the HP Token Proxy" (`P/publish.md:345`). No guide or portal page explains the HP Token Proxy (one match for the phrase in the whole source set).
- Platform targeting: "specify the minimum OXPd2 platform version still supported by VAV and required to run the app when packaging"; an app targeting a platform version past its VAV end-of-support date fails VAV (`P/platform-versions.md:21-23`).

**Solution Packaging Utility (SPU).**
- GUI for Windows and Linux; a project is saved as `spu_project.json`; the build writes `solution.bdl` to a `build` folder and, by default, a `context.json` holding the context defaults (`G/solutionPackagingUtility.md:20,48,664,679,683`).
- Tabs follow the services: general settings (basic details, context profile, notification agents, certificates and trusted sites, configuration), then application, authentication, copy, device usage, job statistics, print job, scan job, security, solution diagnostics, supplies and USB accessories assets (`G/solutionPackagingUtility.md:62-73`).
- Self-signing: generate an RSA key of at least 2048 bits in PEM, tick "Sign Tarball" and "Sign Bundle"; the SPU creates detached signatures inside the bundle. Self-signing is required before V&V and optional in development; it "does not replace the HP V&V signature" (`G/solutionPackagingUtility.md:740-758`).
- CLI for build pipelines: actions `squashfs`, `verity`, `tar`, `signtar`, `fimpak`, `fimbdl`, `signbdl`, `fimdump`, `validate`, `batch` (`G/solutionPackagingUtilityCli.md:47-61`). The pipeline is: stage folder to SquashFS, DM-Verity hash image and root hash, gzip tarball `solution.tar.gz`, detached signature `solution.tar.gz.sig`, HP "FIM" package (PAK), then bundle (BDL) (`G/solutionPackagingUtilityCli.md:143-147,215,233,250`). Only `--type unverified` produces a valid developer bundle (`G/solutionPackagingUtilityCli.md:299`).
- `validate` at production level requires HTTPS, disallows the SDK's development CA, and warns if no notification agent subscribes to the install-code notification (`G/solutionPackagingUtilityCli.md:344-350`).
- On Windows the CLI and GUI need WSL 1 for SquashFS and DM-Verity (`P/how-it-works.md:86`, `G/solutionPackagingUtilityCli.md:199-200`).

### 4.5 Solution Manager: install, update, remove

**Install paths HP defines** (`G/securityModel.md:69-78`):

| # | Mechanism | Status in the guides |
|---|---|---|
| 1 | Indirect install through an HP cloud solution deployment platform | "Not supported for OXPd2 solutions"; reserved for HP Workpath solutions |
| 2 | Walk-up install from a USB drive at the panel | "Currently not supported" |
| 3 | Remote install through the device's Embedded Web Server | "Currently not supported" |
| 4 | Remote install through the Solution Manager Installer REST API | Supported; the only working route in this SDK |

**Installer API** (admin token):
- `installSolution`: a push; multipart POST with `content` (JSON), `solution` (the bundle, content type `application/vnd.hp.solution-bundle`) and optional `context` (JSON) (`G/solutionManagerOverview.md:261-272`).
- `installRemote`: a device pull; the caller gives an `archiveTarget` and optional `contextTarget` (both HTTP service client targets on a server) and the device fetches the bundle and context itself. If the context cannot be fetched the solution installs with a null context and the operation ends `iosPartialSuccess` (`G/solutionManagerOverview.md:284-303`). Added at platform Beta 8 (`P/platform-versions.md:18`).
- `uninstallSolution` with the `solutionId` (`G/solutionManagerOverview.md:313-317`).
- `installModification` and `uninstallModification` are "not supported in this release"; scheduled operations and `requestCancel` are "Currently not supported"; `install` and `uninstall` are deprecated names (`G/solutionManagerOverview.md:223-232,308,326`).
- The installer is a singleton with `status` `isIdle`, `isInstalling` or `isUninstalling`; an install attempted while not idle fails (`G/solutionManagerOverview.md:249-254`).
- Each call returns an Installer Operation (`iosInProgress`, `iosSucceeded`, `iosFailed`, `iosPartialSuccess`); the device keeps the last 32 (`G/solutionManagerOverview.md:331,349-354`).
- What the device does on install: verify signatures and permissions against device settings, unpack, process the manifest, register the services, mark installed (`G/solutionManagerOverview.md:171-175`).

**Install sequence as drawn** (`G/md-img/service/solutionManager/sequence/Solution_Install.png`): a "Trusted Client" ("an application/interface that the device administrator trusts with their credentials") holding an admin token GETs the installer (idle), POSTs `installSolution`, receives 201 with an operation in progress; when the device finishes it POSTs `ntAuthCode` and then `ntSolutionInstalled` to the solution's notification endpoint; the solution exchanges the code for its own tokens.

**Notification agent** (zero or more per solution). Target is an HTTP payload client target. Types: `ntAll`, `ntDeviceBoot`, `ntShuttingDown`, `ntSolutionInstalled`, `ntSolutionUninstalled`, `ntAuthCode`, `ntWalkupSignIn`, `ntWalkupSignOut`, `ntContextModified`, `ntCertificateAuthorityAdded`, `ntCertificateAuthorityDeleted`, `ntInstallerOperation`. Boot, shutdown, walk-up sign-in and sign-out and installer-operation notifications go to every solution that subscribed; the others only to the solution concerned. The list itself is bindable (`G/solutionManagerRegistration.md:8,154-168`).

**After install** (solution token or admin token):
- **Context**: GET, PUT (replace) or PATCH the solution's context at any time; this is how the server host name, paths, credentials, trusted sites and tile visibility change without a new bundle (`G/solutionManagerOverview.md:410-413,483-487`, `G/securityModel.md:105-109`).
- **Certificate authorities**: list, import (one per call), export, delete in the solution's own store (`G/solutionManagerOverview.md:414-421,496-507`).
- **Configuration**: a solution-defined blob with a MIME type, GET or PATCH the metadata and GET or PUT the data (`G/solutionManagerOverview.md:531-553`).
- **Runtime registrations**: with a Runtime Registration Agent declared in the manifest, the solution owner or a device administrator may add and delete, per device, registration records of two types only: application agents (new tiles) and i18n assets (`G/solutionManagerOverview.md:569-573,612`, `G/solutionManagerRegistration.md:292-298`). Added at platform Beta 9 (`P/platform-versions.md:19`).
- Solution state: `ssInstalled`, `ssInstalling`, `ssUninstalled`, `ssUninstalling`; `initializedState` is evaluated per boot (`G/solutionManagerOverview.md:475-476`).

**Update.** The guides describe no in-place upgrade of an installed solution. "Modifications" are the specified mechanism and are not supported. The manifest of an installed solution "cannot be modified" (`G/solutionManagerOverview.md:467`). An upgrade is therefore, as far as these guides go, uninstall followed by install of a new signed bundle (inferred); whether installing a bundle with the same `solutionId` over an existing one replaces it is not stated.

**EWS view.** The device's web interface has a Solution Management page that lists the supported solution platforms and versions and the installed solutions with their registration records, and offers a download of the solution's logs. It is described as a viewer; no install control is described (`G/ews.md:253-265`).

### 4.6 Who deploys to a fleet, and what "LDB" is

- Deployment is by "the device administrator" using the Solution Manager service (`G/solutionManagerOverview.md:169`). In every demo this is the solution's own admin web application: the operator types the device address, the device admin user name and password, the solution host address and port, picks the bundle (and context file), and presses Install (`G/pullPrintDemoGuide.md:237-244`, `G/kioskAndBrowserDemoGuide.md:303-311`). That is the pattern HP models: **the vendor's server is the installer**, holding admin credentials briefly to get a one-hour admin token.
- No HP fleet tool is named for OXPd2 bundle deployment in the guides or portal pages. HP's cloud route is excluded (`G/securityModel.md:71,78`). Zero matches for "Web Jetadmin" in this source set (searched with the method of section 2). Bulk deployment to many devices is therefore the solution vendor's job, one REST conversation per device (inferred).
- The Device service has "Device Deployment" information (nickname, location, asset number, company, contact) that an administrator sets in EWS and a solution can read (`G/ews.md:113-125`).

**LDB = LaserJet Debug Bridge**, the device's developer mode (`G/debugBridge.md:4`).
- It allows the SDK Support service, advanced debug tools and "Installation of unsigned bundles on the device" (`G/debugBridge.md:6-9`). It "should only be enabled during development" and is required for every SDK example and demo (`G/debugBridge.md:11`).
- Enabling needs: an LDB Service Key requested from the HP developer portal, device administrator access, the device on a network with internet access (with proxy set if needed), and presence at the physical control panel ("Remote connections are not allowed"); the operator signs in on the panel with an HP.io user name and the service key (`G/debugBridge.md:22-27,34-50`).
- "When LDB is enabled or disabled, the device will remove all solutions and associated data, then reboot" (`G/debugBridge.md:52`).
- In LDB mode the embedded browser can be inspected remotely with browser developer tools at `<device IP>:9211` (`G/debugBridge.md:67-74`).

### 4.7 Authentication service and agent model

**Registration (the Authentication Agent record)** (`G/authenticationServiceRegistration.md:13-18`):
- Identity: `name`, `agentId`, localised name and description.
- `authenticationTarget`: an HTTP service target (host, path, optional Basic or bearer authorisation, headers, retry). To receive the session id and token the record must declare headers using `$SOLUTION_SESSION(AUTHENTICATION_CONTEXT_ID)$` and `$SOLUTION_SESSION(AUTHENTICATION_CONTEXT_TOKEN)$` (`G/authenticationServiceRegistration.md:50-86`).
- `modifiedUserAttributes` (required): the standard attribute names and the custom attribute keys the agent intends to set on a successful sign-in. Custom keys should be reverse-domain; keys starting `com.hp` are refused. The worked example sets `userName`, `fullyQualifiedUserName`, `emailAddress` and two custom keys (`G/authenticationServiceRegistration.md:91-113`).
- `enablePrePromptCheck` and `enableSignoutNotification` (`G/authenticationServiceRegistration.md:121-122`).
- The SPU allows several authentication agents in one solution (`G/solutionPackagingUtility.md:372`); the registration guide's opening sentence says "a single registration record" (`G/authenticationServiceRegistration.md:4`). See section 6.

**The four endpoints the server hosts** under the agent's target (`G/authenticationServiceOverview.md:68-74`):

| Endpoint | Called when | Body the device sends | What the server returns |
|---|---|---|---|
| `POST .../prePromptResult` | Before the browser opens, only if `enablePrePromptCheck` is true | `sessionId`, `sessionAccessToken`, `languageCode` | A result that decides what the device does next: `succeeded` (with user details), `failed`, `continue` (go on to the prompt), `canceled` (values as listed for the equivalent `login` call, `G/authenticationServiceOverview.md:151-155`) |
| `GET .../prompt` | To show the sign-in UI | No parameters; session id and token arrive in the declared headers | "an HTML page to display in the embedded browser" |
| `POST .../postPromptResult` | After the prompt page closes | `sessionId`, `sessionAccessToken`, `languageCode` | The authentication outcome: succeeded with the user's attributes (the diagram shows "displayName, emailAddress, etc."), or canceled or failed with an optional failure message |
| `POST .../signoutNotification` | Just after a user who signed in with this agent is signed out, if enabled | `sessionId` | Nothing stated |

(`G/authenticationServiceOverview.md:76-88`, `G/md-img/service/authentication/sequence/Authentication_With_PrePrompt.png`.) The `languageCode` is there so the server can build localised failure messages (`G/authenticationServiceOverview.md:82`).

**Flow with a prompt, as drawn** (`Authentication_With_PrePrompt.png`, `Authentication_With_No_PrePrompt.png`): the user touches a protected function or Sign In; the device allocates a `sessionId` and an Auth Context Session Token; (pre-prompt POST, answer `continue`); the device GETs the prompt page and displays it; the page "interacts with solution" directly (the page talks to its own server); the page closes; the device POSTs post-prompt; on `succeeded` the device shows success and updates the logged-in user; otherwise it shows failure and invalidates the authentication context.

**What starts a sign-in** (`G/authenticationServiceOverview.md:21-29`):
- At the panel: pressing Sign In and choosing the agent, or pressing a secured element such as Home or a secured feature.
- By program: `POST authenticationAgents/{agentId}/login`, allowed only for the solution that owns the agent; or `POST authenticationAccessPoints/{accessPointId}/initiateLogin`, allowed for solution providers and local device administrators.
- By the agent on an outside event such as a card presented.

**The `login` call (how a server signs a user in on the device)** (`G/authenticationServiceOverview.md:147-166`):
- Body: `result` (`succeeded` with a `details` object for the user, `failed`, `continue`, `canceled`) and optional `action`: `none` or `initiateAppLaunch` with an `applicationAccessPointId` (the `startIntent` property of that action is "not currently supported").
- It is the pre-prompt answer supplied up front: "The `prePromptTarget` will not be called", and the prompt and post-prompt may be bypassed depending on the result.
- It works when the panel is idle ("no user is logged in and the home screen is being displayed"); a sleeping device is woken. It returns at once, before sign-in completes, with the session id and a token for the session.
- "Authentication (Autolaunch Application)" arrived at platform Beta 9 (`P/platform-versions.md:19`).

**Card-initiated flow, as drawn** (`Authentication_Initiated_by_Agent.png`): card tap, the open USB accessory resource POSTs a read-report notification to the server's USB I/O endpoint, the server verifies the card, then calls `login(succeeded)` (no PIN), or `login(continue)` (PIN required, the prompt page follows), or `login(canceled or failed, message)` (card not registered); the device returns the `sessionId`, which the server associates with the validated user.

**Authentication access points**: the collection lists every sign-in method on the device, native and solution-provided, each with an `accessPointId`, a `kind` from an enumeration and, for kind `akCustom`, a `customName` set by the solution (`G/authenticationServiceOverview.md:177,188-195`). `initiateLogin` "will succeed even if the access point is inaccessible or the prompt page fails to load" (`G/authenticationServiceOverview.md:206`). On the panel the user picks the agent in a "Sign-In Method" drop-down of the native sign-in dialog (`G/pullPrintDemoGuide.md:391-393`).

**Session.**
- A successful sign-in starts an authentication session with a `sessionId` and linked session token; "secured features are only authorized to those requests that bear the Authentication Session Token linked to the current authentication session" (`G/authenticationServiceOverview.md:31`).
- It lasts "until explicitly logged out or until the device inactivity timeout is reached"; while it is active no new session can start (`G/authenticationServiceOverview.md:31`).
- Inactivity timeout: factory default 60 seconds, settable from 10 to 300 seconds, reset by any touch, and resettable by the solution (`resetInactivityTimer`), which "must not override the UI inactivity timeout indefinitely" (`G/applicationServiceOverview.md:446-452`).

**Sign-out.**
- `POST session/forceLogout`: asynchronous, "equivalent to a reset button press", effective only if the token used is associated with the current login session; the UI returns to the home screen (`G/authenticationServiceOverview.md:222-230`).
- Application Runtime `reset` (admin token): exits any active application and logs out any user (`G/applicationServiceOverview.md:389-398`).
- A USB callback response may carry the action `forceLogout` (`G/usbAccessoriesOverview.md:334`).
- The server learns of sign-out from `signoutNotification` (its own agent's users) and from `ntWalkupSignOut` (any walk-up user) (`G/authenticationServiceOverview.md:74`, `G/solutionManagerRegistration.md:162`).

**What identity the device then holds: the Security Context.**
- It "establishes the group memberships and privileges associated with a signed-in user" (`G/securityServiceOverview.md:20`).
- Readable attributes (macros): `DISPLAY_NAME`, `EMAIL_ADDRESS`, `EXCHANGE_MAILBOX`, `FQ_USER_NAME`, `HOME_FOLDER`, `LDAP_BIND_USER`, `USER_NAME`, `USER_DOMAIN`, `USER_PRINCIPAL`, `AUTH_TYPE`, `AUTH_AGENT_ID`, `SAM_ACCOUNT`, `SID`, and `CUSTOM_<key>` for custom attributes (`G/architectureModel.md:954-967`).
- To read them a solution registers one Security Agent listing each attribute in `declaredExpressionOperators`; an undeclared one resolves to "Access Denied" (`G/securityServiceRegistration.md:9,51-53`).
- Two ways to read: put the macro in a target header or in scan metadata (`G/securityServiceOverview.md:31-57,62-80`), or `POST securityAgents/{agentId}/resolveSecurityExpression` with an expression (`G/securityServiceOverview.md:173-184`).
- The Security Agent record can enable CORS in the SPU (`G/solutionPackagingUtility.md:538`), and the kiosk demo resolves these macros from JavaScript in the page (`G/kioskAndBrowserDemoGuide.md:511-524`).
- Because the attributes are set by whichever agent signed the user in, a solution reading the Security Context sees users signed in by native methods and by other vendors' agents too; `AUTH_AGENT_ID` tells which (`G/architectureModel.md:964`) (the cross-agent reading is inferred from the macro's definition).

### 4.8 Application service: tiles, UI contexts, the browser

**Application Agent record** (one per tile; several per manifest) (`G/applicationServiceRegistration.md:17-21`):
- Identity and labels; `category` `acStandardWalkup` (a home-screen tile) or `acKiosk` (may replace the home screen); `platform` `apOXPd2`; `enabled`, a bindable boolean that shows or hides the tile; `icon` or an `iconSet` keyed `[width]X[height]` (`G/applicationServiceRegistration.md:38-52`).
- Icon formats: PNG, JPEG, or a single-frame Lottie JSON as a vector (animations not supported); an icon over 50 KB as Base64 (about 30 to 32 KB raw) installs but the tile does not appear (`G/applicationServiceRegistration.md:93-96,113`).
- `target.webApplicationTarget`: scheme, host, path, optional Basic or bearer authorisation, headers, retry, and an optional default start intent. A header with `$SOLUTION_SESSION(UI_CONTEXT_TOKEN)$` is how the server receives the UI token on the page request (`G/applicationServiceRegistration.md:125-148`).
- `chrome.webApplicationChrome` defaults, all bindable: header and footer colours, footer visibility (default false), header title, Home button available, Start button visible and enabled, soft keyboard available (`G/applicationServiceRegistration.md:218-229`).
- `failureBehavior`: a custom localised message and title, colours, and whether the failure dialog can be dismissed, shown when the page fails to load (`G/applicationServiceRegistration.md:284-290`).
- `intentProfile`: a JSON schema for a start intent; result intents are "not currently supported" (`G/applicationServiceRegistration.md:296-304`).
- i18n assets: string tables per language tag, inline or as a JSON file in the bundle; the first language is the fallback (`G/applicationServiceRegistration.md:331-355`).
- One Message Center Agent per solution lets it post info, warning or error messages to the device's Status Center; the text must reference i18n strings (inline text and images are "Not currently supported") (`G/applicationServiceRegistration.md:434`, `G/applicationServiceOverview.md:761-784`).

**UI session and context** (`G/applicationServiceOverview.md:30-39`, `Application_Session.png`):
- From load to teardown is a UI Session, tracked by an Application Context linked to a UI Context Session Token. One application holds the context at a time.
- Start: the user touches the tile, or a client calls `applicationAccessPoints/{id}/initiateLaunch` (solution token or admin). The call does not return the UI token; the launched application gets it through the header macro (`G/applicationServiceOverview.md:178-197`). A start intent can be passed as a multipart part (`G/applicationServiceOverview.md:204-229`).
- End: the user leaves, the page calls `window.close()`, or the `exit` operation, or `reset` (`G/applicationServiceOverview.md:39,469-471`).
- `applicationAccessPoints` lists every application on the device, native and third-party, with id, localised title and optional icon (`G/applicationServiceOverview.md:120-124`).
- `applicationRuntime` gives `currentLanguage` and `activityState` (`asAsleep`, `asInactive`, `asAwakeIdle`, `asAwakeActive`) (`G/applicationServiceOverview.md:363-368`).
- `currentContext` shows the active application (id, name, solution id) to any solution; its operations are for the holder of the UI token: `resetInactivityTimer`, `exit`, `exec`, `beep` (`G/applicationServiceOverview.md:405-439`).
- `exec` launches a child application (mainly a native one) and returns to the launcher when it exits; "only supported when an OXPd2 application is in kiosk-mode" (`G/applicationServiceOverview.md:486`).
- `runtimeChrome` (GET, PATCH, PUT with the UI token) changes the header and footer during the session; values are lost when the context is released (`G/applicationServiceOverview.md:510-535,565`).
- `applicationAgents/{id}/refresh` re-evaluates a tile after its context-driven properties change, for example `enabled` (`G/applicationServiceOverview.md:317`).
- The Current Context is "available to both the application running in the embedded browser (via localhost access) as well as to the remote solution running on an external server" (`G/applicationServiceOverview.md:403`). The kiosk demo calls the Device, Application, Copy, USB Accessories, Scan and Security services from page JavaScript "using CORS ... instead of through the solution host server" (`G/kioskAndBrowserDemoGuide.md:372-383`).

**Home-screen button.** The tile is the Application Agent (title and icon). The guide compares it to OXPd1's TopLevelButton and stresses the difference: in OXPd2 the tile must be declared in the signed manifest and appears only on install (`G/applicationServiceRegistration.md:17`), with the two escape hatches above: the bindable `enabled` flag, and run-time registration of extra application agents.

**Kiosk mode.** A device administrator PATCHes the `homescreen` resource to set `defaultApplicationId` to an application registered as `acKiosk`; it then loads in place of the native home screen; the all-zero UUID restores the native one (`G/applicationServiceOverview.md:655,690-708`). Custom home-screen messages are "not currently supported" (`G/applicationServiceOverview.md:659`). Two other guides say kiosk is not available in this release (section 6).

**The embedded browser** (`G/applicationServiceBrowserUseModel.md`):

| Topic | Statement | Line |
|---|---|---|
| Engine | Qt QtWebEngine using Chromium 87.0.4280.144 | 9-11 |
| User agent | `Mozilla/5.0 (X11; Linux aarch64) ... QtWebEngine/5.15.16 Chrome/87.0.4280.144 Safari/537.36`; "will be updated in future releases" | 128-132 |
| Shown when | Only while an OXPd2 application holds the UI context | 20 |
| Enabled features named | HTML5, CSS, WebAssembly, SVG, WebGL and Canvas, Storage API, WebRTC (subset), PWA (subset) | 77-84 |
| Disabled | File input control, file download links, pop-up windows, browser tabs, notifications, fullscreen, screen capture, plugins | 89-98 |
| Feature set | "still under development"; not the final production behaviour | 68 |
| Memory and CPU | Constrained to protect device functions; allocations still being tuned; no numbers given | 106-108 |
| Hooks | "still under development"; features described "may not be currently enabled in this SDK release" | 115 |
| UI token in page | `window.oxpd2.uiContextToken` | 120 |
| Hard keys | Digits, `*`, `#` as a keyboard; Clear keyCode 12; Home, Start and Help delivered to the page as keyCodes 112, 113, 114 on `onkeydown`; Sleep, Reset, Stop not delivered | 140-160 |
| Soft keyboard | Native keyboard appears on text inputs; per-input style through a custom `textbox-mode` attribute (`latin-only`, `fax`, `fraction`, `hex`, `pin`) | 170-188 |
| Cookies | "still under development"; no behaviour described at all | 195 |
| Cache | In device RAM, cleared only by a power cycle; honours cache-control headers; the application's primary target "is never cached"; behaviour not final | 201-205 |
| Not controllable | Header icon; style of browser dialogs (prompt, confirm) | 47,53 |

- Panel variation is read from the Application service capabilities `User Interface Attributes`: resolution, diagonal size, header and footer pixel heights, icon sizes and formats, hard keys, keyboard types, native theme (`G/applicationServiceOverview.md:67-81`). The portal recommends adjusting layouts per model (`P/how-it-works.md:204-206`).

### 4.9 USB accessories: card readers

- One USB Accessories registration record per solution lists accessories by `vendorId` and `productId` (integers, required) and optional `serialNumber` (omitted matches any; empty string matches only readers with none), each `rkOwned` or `rkShared`, plus an optional `registrationTarget` (an HTTP payload client target, "considered a critical target") (`G/usbAccessoriesRegistration.md:53-62,88-113`). The alternative record type `usbAccessoriesAgentRegistrationRecord` in the specification "is not currently supported" (`G/usbAccessoriesRegistration.md:6`).
- **Owned**: only the registering solution may use it, at any time, with its solution token. "Once a solution has registered a particular accessory as owned, no other solution may register that accessory as owned, or redefine the accessory as shared"; a later solution that tries fails to install (`G/usbAccessoriesOverview.md:22,41,104`).
- **Shared**: several solutions, each only while it holds the UI context (solution token plus UI token) (`G/usbAccessoriesOverview.md:23,228-231`).
- Associations are rebuilt at every boot (they "are not persistent"). After boot evaluation the device sends an attachment notification for owned accessories to the registration target; a later attach does the same; detach destroys the resource and force-closes it, and "No notifications of the resource removal occur" beyond the closure (`G/usbAccessoriesOverview.md:68-93`).
- An accessory that matches no registration makes the panel show an "unsupported USB accessory" message (`G/usbAccessoriesOverview.md:74`).
- **HID access**: `POST accessories/{id}/hid/open` with an optional `operationContext` cookie and `reportReadingActive`; with it true, input reports from the interrupt-in pipe are delivered asynchronously to the registration target (`G/usbAccessoriesOverview.md:273-281,351`). Synchronous or asynchronous `readReport` (GET_REPORT) and `writeReport` (SET_REPORT) work on the control pipe (`G/usbAccessoriesOverview.md:397-425`). Low-level "generic" USB access is "not supported this release" (`G/usbAccessoriesOverview.md:202-203`).
- Reports pass "in raw form (i.e., it does not parse, format, or interpret the data)"; the solution parses them to the manufacturer's specification (`G/usbAccessoriesOverview.md:266`).
- **Events to the server**: each POST wraps `usbCallbackEnvelope` items with the `operationContext` and one of `hidRead` (`data`, `hidReadSequence`), `usbRead`, `usbWrite`, `usbClosed` (`G/usbAccessoriesOverview.md:308-322`).
- **Response actions**: the server's HTTP response to a callback may carry `action`: `none`, `initiateLogin` (start a sign-in at the authentication access point) or `forceLogout` (`G/usbAccessoriesOverview.md:328-334`).
- If the solution loses access (no longer active at the panel, or uninstalled) the accessory is closed; re-opening an already open accessory closes and reopens it with possible data loss (`G/usbAccessoriesOverview.md:292-293`).
- USB accessories support (proximity card and barcode readers) arrived at platform Beta 3 (`P/platform-versions.md:13`).

### 4.10 Solution-server requirements and where the server may live

Every statement found about location and reachability:

| Statement | Source |
|---|---|
| The solution server is "connected to the same network" as the devices | `P/how-it-works.md:13` |
| Target market: "print-to-digital integration with on-premises and legacy systems"; scan to and print from "any on premises or private-cloud based middleware, directly from the device" | `P/oxpd2.md:23,28-29` |
| "Host your Java or .NET solution on an external server" | `G/introduction.md:4` |
| The solution context exists to hold "the hostname of the customer's Solution Server" | `P/how-it-works.md:32` |
| A target `host` is "typically a server DNS host name or IP address" with optional port, no user info | `G/solutionPackagingUtility.md:145` |
| Server host and credentials are expected to change after install and are changed through the context | `G/securityModel.md:94-97` |
| Device-managed fail-over between server hosts (`hostSets`) is not supported in this release | `G/solutionManagerOverview.md:60` |
| The device has web-proxy settings in EWS, "may be required for private or corporate network configurations" | `G/ews.md:171-178` |
| Device and server clocks must agree, or TLS and IPP fail | `G/ews.md:54,72` |
| HP's cloud is not in the path for OXPd2 solution install | `G/securityModel.md:71,78` |
| Enabling developer mode (LDB) needs the device to have internet access; nothing says a production device needs it | `G/debugBridge.md:40-42` |

What follows for a localised server:

1. **Device to server is mandatory.** The browser loads the tile's page from the server; the authentication agent, notification agent, USB registration target and every other agent target are HTTP requests the device opens to the server (`G/architectureModel.md:598`, section 4.2).
2. **Server to device is mandatory in the documented model.** The install-code exchange and token refresh, `login`, `initiateLaunch`, HID `open`, context and certificate changes, and install itself are requests the server opens to the device (`G/securityModel.md:136,205`, `G/authenticationServiceOverview.md:149`, `G/usbAccessoriesOverview.md:273`).
3. Some device APIs can be called from the page itself over localhost with CORS (section 4.8), which moves part of the traffic onto the device; but the page needs tokens, and the solution token is obtained by the server calling the device. The guides do not describe a pattern that removes the server-to-device leg (inferred from the absence; see section 6).
4. **TLS.** Production manifests must use HTTPS (`G/solutionPackagingUtilityCli.md:346`, `P/publish.md:85`). The device trusts only CAs in the solution's own store for its outbound calls to solution endpoints (`G/solutionPackagingUtility.md:162`). A customer whose local server uses a private CA therefore needs that CA imported into the solution's store on each device after install (`certificateAuthorities/import`), because the CAs inside an HP-signed bundle are fixed at signing (inferred from `G/solutionManagerOverview.md:417,509`).
5. **Ports.** None is mandated for the server; the authority may carry any port (`G/architectureModel.md:648`). The device's REST and EWS endpoint is reached at `https://<device IP>` (`G/ews.md:35`). Demo ports are developer defaults only.
6. **DNS.** Host names or IP addresses are both accepted; the demos use IP addresses and issue the server certificate for an IP (`G/sdkUserGuide.md:68-72`, `G/kioskAndBrowserDemoGuide.md:37`).
7. **Outbound internet from the panel.** The embedded browser may reach only the solution's `trustedSites` (`G/solutionManagerOverview.md:135-141`). A Microsoft sign-in page shown in the panel browser needs the Microsoft sign-in hosts in that list (or `*`), and needs the device to route to the internet, through the EWS proxy if the site requires one (inferred).

### 4.11 Print Job service and pull print (my files)

- The Print Job service's "only functionality" at present is registering a Print Job Agent, which enables **priority printing** through IPP extensions; it lists capabilities and agents and nothing else (`G/printJobServiceOverview.md:4-10`).
- Priority print needs: a Print Job Agent in the manifest, the solution installed, and a valid, active UI context token (`G/printJobServiceRegistration.md:9-12`). It "pauses external IPP print jobs while the walk-up mode is active" (`G/solutionPackagingUtility.md:476`) and lets the walk-up application reserve the device for its print jobs until it exits the mode or the inactivity timeout fires (`G/pullPrintDemoGuide.md:422`).
- Printing itself is IPP from the server to the device. From firmware 6.25.0.730 the device setting "Verify Certificate for IPP/IPPS Pull Printing" is on by default and makes the device process only IPP jobs "from servers with a verified security certificate"; the demo requires an administrator to switch it off in EWS (`G/ews.md:185-195`, `G/pullPrintDemoGuide.md:36`). The detail of the IPP extensions is in section 4.13.

**Pull Print with Authentication demo, as a worked pattern** (`G/pullPrintDemoGuide.md`):
- One solution combines four services: Print Job (priority print), Authentication (a user pool and their documents), USB Accessories (card swipe sign-in), Security (read the signed-in user) (lines 4-8).
- Two faces: an **admin web application** on the server (deploy to a device, manage users, documents and user-to-document permissions, view authentication and USB logs) and a **walk-up application** on the panel (lines 10-17).
- Deployment page: device address, admin user and password, "Solution Host Address:Port", the bundle; install, uninstall, operation status, a notifications tab, and "reissue the install code" (lines 223-244).
- Sign-in at the panel: Sign-in icon, choose the agent in "Sign-In Method", the agent's web page loads, the user submits; on success a welcome message appears "and the Pull Print Application will automatically launch" (lines 391-398).
- Card sign-in: swipe on an attached HP card reader; sign-in completes for a fixed "Card User" and the application launches. The bundle registers only the HP reader; another reader needs another bundle. The demo "will consider any data read into the attached accessory to be valid authentication information" (lines 403-415).
- The walk-up page lists the user's documents; Start prints the selected ones with status updates; Delete removes them; buttons enter and exit priority print mode (lines 420-441).
- Requires HTTPS on the server with a certificate issued from the SDK's development CA, port 5050 (lines 43, 65, 174).
- Its context file shows the shape of a real one: keys for the host, the application path, the notification-agent path and the authentication-agent path (`G/solutionPackagingUtility.md:705-735`).

### 4.12 User policy, authorisation, quota and web hooks

- The portal promises: "Control walkup users' access to device functions with custom authorization logic" and "Impose usage quotas for individual users across a fleet of devices" (`P/oxpd2.md:31,34`).
- **No guide describes either.** Zero matches for `userPolicy`, `user policy`, `webHook`, `web hook` in the 46 guides and 7 portal pages; "quota" appears only in the two portal sentences. The platform-versions table lists no user-policy or web-hook feature in any beta (`P/platform-versions.md:11-19`).
- Both exist only as OpenAPI specifications (outside this lane; headline facts only): `userPolicy` is "1.0 (Alpha 2)", "APIs for implementing a custom userPolicy agent", with paths for agents, configuration, `permissionSets`, `permissions` and bulk updates; `webHook` is "1.0 (Beta 3)", "registering HTTP web hooks in the device which will be forwarded on to the hosted solution", with paths only for capabilities and agents (`OXPd2/Docs/SDK-Documentation/openapi/userPolicy.openapi.json`, `webHook.openapi.json`, info and path keys).
- What the guides do offer for authorisation: the device checks permissions of secured elements against the current authentication session (`G/authenticationServiceOverview.md:31`), and EWS has an "Access Control" page for sign-in permissions (`G/ews.md:207`). How a custom agent's user is mapped to device permission sets is not explained.
- "Events" in the guides are: Solution Manager notifications (section 4.5), authentication sign-out notification, USB callbacks, and per-job notifications of the scan, copy and job-statistics agents.

### 4.13 Scan, copy, stored jobs, IPP extensions (sub-reader A)

Read whole by sub-reader A, who reported no truncated lines. I re-read the lines marked † myself; the rest carry the sub-reader's line numbers.

**Scan Job service.**
- A REST API for scans sent to "file-like destinations"; three phases: scan, process into a file, transmit (`G/scanJobServiceOverview.md:4,26-29`). Fax is excluded (`:21`).
- One Scan Job Agent per solution, declared in the manifest (`scanJobAgentRegistrationRecord`), with a `scanNotificationTarget` (`G/scanJobServiceRegistration.md:4,48`, `G/scanJobServiceOverview.md:588`).
- **Creating a scan job needs "an active and valid UI Context Session token"** † (`G/scanJobServiceOverview.md:636`). A scan cannot be started without the solution's application open on the panel (inferred). Which token the other calls need is not stated in the guides.
- Start: `POST scanJobAgents/{agentId}/scanJob` with a scan ticket and an optional `solutionContext` that is echoed in every status and notification (`G/scanJobServiceOverview.md:578,641-656`). The ticket has `destinationOptions`, `scanOptions`, optional `metadataOptions`, optional `retryOptions` (0 to 5 attempts, 1 to 300 s apart) (`:72-77,276-277`).
- Destinations:

| Destination | Status | How the bytes move | Source |
|---|---|---|---|
| `http` | Supported | The **device POSTs** multipart/mixed to an HTTP or HTTPS endpoint the solution hosts: a JSON `content` part (`scanJobId`, files in this segment, files delivered so far, `transmittingState`), one or more `scanFile` parts, an optional metadata part. Optional Basic or bearer authorisation, custom headers, retry | `G/scanJobServiceOverview.md:86,97-137` |
| `networkFolder` | Supported | Device writes by SMB (UNC path) or FTP; credentials "provided" or taken from the security context (`cstSecurityContext`) | `:87,184-198` |
| `jobStorage` | Supported | Raw scanned image kept in the device's native job storage, with job name, folder and optional write-only password | `:88,203-213` |
| `localFolder`, `email` | Not currently supported | | `:89-90` |

- There is no server-pull of scan data in the guides; delivery is device push only. No size limit is stated. Whether the device validates the scan target's TLS certificate against the solution CA store is not stated in these guides.
- 31 scan options (image processing, original, output file, capture and progress modes); per-device values and constraints come from `GET profile` (rules such as valid values, ranges, conditions) and defaults from `GET defaultOptions`. A non-conforming ticket is not rejected: "the default options will be used instead" (`G/scanJobServiceOverview.md:224-256,446-483`). Only PDF is named as an output format in the examples (`:415`); JPEG and TIFF are implied by macro examples (`:349`).
- Metadata: a solution-defined file (content, MIME type, name) built from macros: `$JOB(...)$`, `$SCAN(...)$`, `$ATTACHMENT(...)$`, and security-context macros such as the signed-in user name (`G/scanJobServiceOverview.md:264-268,302-349`, `G/securityServiceOverview.md:62-80`).
- Status: `jobDoneStatus` `jdsActive`, `jdsSucceeded`, `jdsPartiallySucceeded`, `jdsFailed`, `jdsCanceled`; counters for images scanned, processed, transmitted; activity timelines (`G/scanJobServiceOverview.md:696-736`). Notifications of every state change go to the notification target as a payload wrapper (`G/scanJobServiceRegistration.md:73,126-135`). Cancel by POST (`:678-680`). The device keeps active jobs plus at most 256 completed ones, not across reboot (`:617-619`).
- Prompt-for-more-pages, job build and preview behaviour are not described beyond the existence of `scanCaptureMode` and `scanProgressMode` enums (`G/scanJobServiceOverview.md:252-253`).

**Copy service.** Same shape: one Copy Agent per solution, optional notification target, `POST copyAgents/{agentId}/copyJobs` with a ticket, UI Context token required to create, profile and defaults, status and cancel (`G/copyServiceRegistration.md:4,16`, `G/copyServiceOverview.md:335,402-419,444-490`). The option list (scan side, print side, finishing, stamps and watermark) is "for this beta release" (`G/copyServiceOverview.md:81-135`). Not needed by the suite.

**Stored jobs.** In these guides a stored job is a **scan** kept on the device and later released as a **copy**: created by a scan job with destination `jobStorage`, listed with `GET copyAgents/{agentId}/storedJobs` (fields include `jobUserName`, `jobName`, `folderName`, `totalPages`), released with `.../release` (password if set; the job stays and can be released again) and deleted with `.../remove` (`G/copyServiceOverview.md:340-344,495-571`, `G/storedJobsDemoGuide.md:328`). The list also shows jobs stored by other agents and by walk-up users (`G/copyServiceOverview.md:497`). **Stored print jobs (driver job storage, PIN print, hold and release of print jobs) are not covered by any guide.**

**IPP extensions (how a server prints to the device).**
- IPP is offered at `http://<device>:631/`, `http://<device>:80/` and `https://<device>:443/`, resource normally `/ipp/print`, discoverable † (`G/printJobIppExtensions.md:28-36`). Authentication of ordinary IPP submission is not described.
- Vendor operations Priority-Print-Enter and Priority-Print-Exit take a `priority-print-auth-cookie` that must equal the valid UI Context Session Token (`G/printJobIppExtensions.md:45-46,64-76,197`).
- While reserved, the device answers other IPP clients `server-error-busy`, and holds jobs arriving on port 9100 or LPD until the mode ends; the mode ends on exit, on the UI inactivity timeout, or when the cookie becomes invalid † (`G/printJobIppExtensions.md:80-86`).
- The extensions that would submit a job to a **reserved** device, by value (Print-Job) and by reference (Print-URI), are both marked "currently not supported" † (`G/printJobIppExtensions.md:47,49`), although the pull-print demo is described as printing in that mode. See section 6.
- **Print-URI**: the server hands the device a URL and the **device fetches the document itself**, optionally with Basic credentials (`print-uri-user-name`, `print-uri-password`) and up to four cookie sets (`print-uri-cookie`) supplied in the request †. The job is aborted on an HTTP error "from the server or the proxy" or when the HTTPS server certificate fails validation against "the OXPd2 CA Certificate store" † (`G/printJobIppExtensions.md:92-134`). Failures surface as `document-access-error` (`:136-146`).
- `job-uuid` gives each print job a UUID through Get-Job-Attributes (all zeros until processing starts) (`G/printJobIppExtensions.md:151-159`).
- No accounting, PIN or user-identity attribute beyond the standard `requesting-user-name` is described.

**Demo ports and pattern.** Simple Scan 5150, Simple Copy 5250, Stored Jobs 5650; each is an admin web app plus a walk-up tile, installed by pushing the bundle with the device admin password and a "Solution Host Address:Port"; each needs LDB mode and HTTPS (`G/simpleScanDemoGuide.md:15,27,49,221-227`, `G/simpleCopyDemoGuide.md:48`, `G/storedJobsDemoGuide.md:50`). The scan demo's server writes received files into a folder per scan job id (`G/simpleScanDemoGuide.md:294-296`).

### 4.14 Example host, tokens per call (sub-reader B)

Read whole by sub-reader B (16 guides, no truncation reported). Lines marked † I re-read.

- The example host is a web application (.NET, Java, JavaScript) on port 5000 that exercises 13 services against a device the operator "binds" by typing its IP address; it is a development solution needing LDB mode and runs over plain HTTP, with the remark that only HTTPS solutions will be approved for production (`G/exampleOverviewGuide.md:4,6,34,63,143`).
- Its context file has one authority key per callback family (notification, application, authentication, USB, scan job), which the developer changes from `localhost` to the server's IP (`G/exampleOverviewGuide.md:87-115`). This is the model for making the server address a deployment setting.
- Token behaviour as the example guide tells it:

| Token | Statement | Source |
|---|---|---|
| Device administrator | Expires 60 minutes after issue, "or on device reboot or crash" | `G/exampleOverviewGuide.md:145-151` |
| Solution owner | Provided on a successful install, only to the host that installed. "This token will not expire, but if the Examples host has been restarted, or the device has been rebooted/crashed, it may need to be reissued", by reinstalling or by reissuing the install code † | `G/exampleOverviewGuide.md:152-157` |
| UI context | Issued when an application reserves the UI (panel or programmatic launch); gone when the application closes | `G/exampleOverviewGuide.md:158-160` |
| Authentication session | Issued at sign-in; expires on inactivity or logout | `G/exampleOverviewGuide.md:161-163` |

- A per-operation table of required tokens does not exist in any guide (`G/exampleOverviewGuide.md:165` defers to each API reference).
- `login` with result Succeeded: the server passes "a list of authenticated user properties"; `userName` and `fullyQualifiedUsername` are required; an application can be auto-launched by its access point id † (`G/exampleOverviewGuide.md:664-666`). Continue raises the prompt on the panel; Failed can carry a message for the panel (`:667-669`).
- Pull install is demonstrated with the example host itself serving the bundle and context to the device (`G/exampleOverviewGuide.md:237-268`).
- Kiosk: after setting the home-screen application a Reset is needed to load it; `homescreenCustomMessage` is not supported (`G/exampleOverviewGuide.md:573-575`).
- USB: with `reportReadingActive` true, reports go to "the `asyncIOTarget` defined at Open HID" (`G/exampleOverviewGuide.md:1574`), whereas the USB overview says they go to the `registrationTarget` of the registration record (section 4.9). See section 6.
- Solutions "Certificates" and "Modifications" tabs "will be added in a future release" (`G/exampleOverviewGuide.md:294-295`).
- User Policy, Web Hook and SDK Support do not appear in the example guide (confirmed by the sub-reader's full read and by my counts in section 2).

### 4.15 Job statistics, device usage, supplies, device service (sub-reader B)

**Job Statistics** (platform Beta 9).
- One Job Statistics Agent per solution; optional HTTP notification target; optional content filters per job category, fixed at install; a `criticalSolution` flag (`G/jobStatisticsServiceOverview.md:6,248`, `G/jobStatisticsServiceRegistration.md:4,48-69,207-215,297-302`).
- Each completed job gets a device-wide, monotonically increasing sequence number in a ring buffer of at least 256 entries † (`G/jobStatisticsServiceOverview.md:55,66`). A record has `jobInfo` (category, source, destinations, application name, times, status), `userInfo` "only if a user was signed in", and per-type blocks: `printInfo`, `scanInfo`, `emailInfo`, `folderInfo`, `ftpInfo`, `httpInfo`, `driverInfo`, fax blocks (`:31-42`). The fields inside `userInfo` are left to the API reference.
- Per solution the device tracks the last sequence notified and the last sequence processed; the solution must advance "processed" for every job, wanted or not, and what is processed disappears from its view for good (`G/jobStatisticsServiceOverview.md:10-12,109`, `G/jobStatisticsServiceRegistration.md:205`).
- Four delivery patterns: synchronous push (persist, then acknowledge in the HTTP response), deferred push, pull (GET or PATCH on `jobs`), and notification-triggered pull (`G/jobStatisticsServiceOverview.md:87-154`).
- Server unreachable: the device retries as registered, then includes the undelivered data in the next notification that succeeds; a lost acknowledgment causes duplicates the solution must ignore; a non-critical solution that stays away loses the oldest entries; a critical solution's unprocessed entries are never overwritten and the device "will lock and stop accepting new job submissions" † (`G/jobStatisticsServiceOverview.md:62-74,168-183`). The SPU says the critical flag is not supported in this release (`G/solutionPackagingUtility.md:442,454`).

**Device Usage and Supplies** (platform Beta 7). Pull only, no events; one identity-only agent each. Device Usage returns lifetime counters by group (print, scan, fax, job) with no per-user breakdown; Supplies returns configuration (low thresholds, behaviour at low, anti-theft), per-supply information (type, serial, percent remaining, pages remaining, state) and usage (`G/deviceUsageServiceOverview.md:4-8,70-74,139-155`, `G/suppliesServiceOverview.md:4-6,45-50,89-135`).

**Device service.** Needs no registration record and "can be used by any client" (`G/deviceServiceRegistration.md:4`).

| Resource | Content | Source |
|---|---|---|
| `identity` | `deviceUuid`, `serialNumber`, `formatterSerialNumber`, `productNumber`, `firmwareVersion`, make and model (`base`, `family`, `model`) | `G/deviceServiceOverview.md:51-59` |
| `deploymentInformation` | Per adapter: fully qualified `hostName`, IPv4, IPv6, MAC; owner information set by the administrator (asset number, company, contact, location, device name) | `:80-93` |
| `status` | One of initialising, shutting down, in power save, in error, ready, other operable, other inoperable | `:111-120` |
| `scanner` | Paper in feeder, paper on flatbed, busy, online; absent without a scanner | `:128-145` |
| `email` | Whether the device's own email sending is configured | `:153-164` |

Print-engine status and device alerts are "not supported this release" (`G/deviceServiceOverview.md:14-15`). Service and version discovery is per-service `capabilities` plus the CDM services-discovery resource (section 4.1).

### 4.16 Diagnostics, SDK support, Postman (sub-reader B)

- **Solution Diagnostics** (Beta 5): one identity-only agent; `GET solutionDiagnosticsAgents/{agentId}/log` returns "the latest available" trace log as one gzip (tar) or plain-text part. The device logs on the solution's behalf into a common system log; there is no API for a solution to write log entries; the server keeps its own logs by its own means; `crashReport` does not apply to OXPd2 (`G/solutionDiagnosticsOverview.md:15-17,48-54,92-107`). The same logs can be downloaded from EWS (`G/ews.md:265`).
- **SDK Support** (LDB devices only, no registration): simulated USB HID devices with a `tap` that injects Base64 card data; panel screen capture as PNG; simulated hard-key presses; an echo resource. Touch simulation (`pressScreen`) and "Functions" are not supported. Simulated devices vanish on reset or on leaving developer mode (`G/sdkSupportServiceOverview.md:4,18-30,124-126,145,158-203,268-270`). This allows automated tests of card sign-in without a reader, on developer-mode devices only.
- **Postman collection**: an environment (`HOST`, `ADMIN_AUTH_TOKEN`, `UI_CONTEXT_TOKEN`, `SOLUTION_SERVER_AUTHORITY`) and two collections ("CDM", "OXPd2"). The guide tells the developer to switch off TLS certificate verification because the device may present a self-signed certificate. A "Multipart-Packer" command-line tool builds the install request body from a solution id, bundle and context (`G/postmanOXPd2Collection.md:40-43,60-63,72-111`).

### 4.17 Platform versions, firmware, device families

| Firmware (FutureSmart) | Platform version | Features introduced |
|---|---|---|
| 6.3 | Beta 1 | Solution Manager, Application, Print services, SPU |
| 6.7 | Beta 2 | Authentication, Device services |
| 6.10 | Beta 3 | USB Accessories (proximity card and barcode readers) |
| 6.12 | Beta 4 | Scan Job (default options, profiles), Security |
| 6.16 | Beta 5 | Scan jobs, Solution Diagnostics |
| 6.19 | Beta 6 | Copy |
| 6.23 | Beta 7 | Device Usage, Supplies, SDK Support |
| 6.26 | Beta 8 | Device deployment info, SDK Support (screen capture, echo, remote key press), Solution Manager remote install |
| 6.34 | Beta 9 | Job Statistics, Solution Manager runtime registrations, Authentication autolaunch application |

(`P/platform-versions.md:9-19`.) Every row is "(pre-release)" and its "VAV End of Support" cell reads "Not Supported". Beta 10 is absent from the table although it is the SDK on the download page with simulator firmware 6.38.0.793 (`P/oxpd2-download.md:18,22`).

- OXPd2 is "available on only the newest devices running FutureSmart 6 and later"; "Those devices will not support OXPd1" (`P/how-it-works.md:28`). OXPd1 has been in every firmware "up to and including FutureSmart 5" (`P/how-it-works.md:36`).
- HP's claim on dual support: OXPd2 "does support all the same features as OXPd1 (but using different protocols) making it is easy to support both ... within the same Solution Server implementation" (`P/how-it-works.md:28`).
- Compatible devices: "devices supporting Next Generation LaserJet FW. The Model Numbers supported will be defined prior to production release" (`P/compatible-devices.md:9`). The only model list is the test-group table on the publish page (section 4.4).
- A simulator VM runs "the same firmware installed on OXPd2 compatible print devices" (`P/oxpd2.md:50`).
- Beta firmware "is for internal testing only and may not be distributed to customers"; at the time of capture no beta or early-access firmware images were offered for download (`P/oxpd2-download.md:36,42,66`).

### 4.18 Every stated limitation, "not supported" and roadmap note (my files)

| # | Limitation | Source |
|---|---|---|
| 1 | WebSocket and TCP callback targets not supported; only HTTP and bundle targets | `G/architectureModel.md:620,629-635` |
| 2 | Not all target types in the specification are implemented | `G/architectureModel.md:687` |
| 3 | Install through HP cloud: not for OXPd2. Install from USB at the panel and through EWS: currently not supported | `G/securityModel.md:71-73` |
| 4 | `hostSets` (server fail-over), `installActions`, `uninstallActions`: not supported | `G/solutionManagerOverview.md:60-62` |
| 5 | Solution modifications (install, uninstall, collection, registration record): not supported | `G/solutionManagerOverview.md:223,225,308,326,372,429`, `G/solutionManagerRegistration.md:13` |
| 6 | Scheduled installs and cancelling an installer operation: not supported | `G/solutionManagerOverview.md:232,350,368,385` |
| 7 | Solution certificates with private keys: not supported; "will be supported in a future release" | `G/solutionManagerOverview.md:422,525`, `G/solutionPackagingUtility.md:90` |
| 8 | CA import takes only the first certificate per call | `G/solutionManagerOverview.md:500` |
| 9 | Remote-install targets do not expand `$SOLUTION` or `$OP_SOLUTION` macros | `G/solutionManagerOverview.md:299` |
| 10 | Runtime registration limited to application agents and i18n assets | `G/solutionManagerOverview.md:571-573` |
| 11 | Password-grant token: one hour, no refresh | `G/securityModel.md:163` |
| 12 | Install code valid 5 minutes | `G/securityModel.md:218` |
| 13 | `login` action `initiateAppLaunch.startIntent`: not supported | `G/authenticationServiceOverview.md:160` |
| 14 | Result intents: not supported anywhere (access point, runtime, registration, SPU) | `G/applicationServiceOverview.md:152,206,353-355,619`, `G/applicationServiceRegistration.md:142,303`, `G/solutionPackagingUtility.md:340` |
| 15 | Custom home-screen messages: not supported, "in future releases" | `G/applicationServiceOverview.md:659` |
| 16 | Message Center inline messages, inline titles and images: not supported | `G/applicationServiceOverview.md:765,773,777` |
| 17 | `exec` only in kiosk mode; one child at a time | `G/applicationServiceOverview.md:486` |
| 18 | Kiosk applications "currently not supported" (SPU); "homescreen feature is not supported this release" (kiosk demo); more kiosk chrome options "being considered for future SDK releases" | `G/solutionPackagingUtility.md:288,326`, `G/kioskAndBrowserDemoGuide.md:8` |
| 19 | Kiosk demo: Application page, run-time context editing and "Other Operations" not supported in this release | `G/kioskAndBrowserDemoGuide.md:279,290,340,356,414` |
| 20 | Browser: file input, downloads, pop-ups, tabs, notifications, fullscreen, screen capture, plugins disabled | `G/applicationServiceBrowserUseModel.md:89-98` |
| 21 | Browser feature set, constraints, hooks, user agent, cookies and cache: all "under development", subject to change before production | `G/applicationServiceBrowserUseModel.md:68,108,115,132,195,205` |
| 22 | Lottie animations not supported as icons; icon over 50 KB Base64 hides the tile | `G/applicationServiceRegistration.md:96,113` |
| 23 | USB: `generic` low-level access not supported; `usbAccessoriesAgentRegistrationRecord` not supported; `ttWorkpath` I/O target not for OXPd2 | `G/usbAccessoriesOverview.md:137,202-203`, `G/usbAccessoriesRegistration.md:6` |
| 24 | Print Job service: registration for priority print is its only function | `G/printJobServiceOverview.md:4` |
| 25 | Job statistics "critical solution" flag: not supported | `G/solutionPackagingUtility.md:442,454` |
| 26 | LDB toggling wipes all solutions; needs physical presence, internet and an HP service key | `G/debugBridge.md:34,40-42,52` |
| 27 | SPU: Windows (with WSL 1) and Linux only; `fimbdl` type must be `unverified` | `G/solutionPackagingUtility.md:20-29`, `G/solutionPackagingUtilityCli.md:299` |
| 28 | All SDK demos and examples are development solutions that "cannot be installed on production devices" | `G/pullPrintDemoGuide.md:28`, `G/kioskAndBrowserDemoGuide.md:22` |
| 29 | Bundle upload limit 100 MB | `P/publish.md:210` |
| 30 | URL length limit 2018 bytes; content filters support no advanced wildcards | `G/architectureModel.md:175,437` |
| 31 | Compatible model numbers not yet defined; platform in Beta | `P/compatible-devices.md:9`, `P/oxpd2.md:17` |
| 32 | Scan: fax, `localFolder` and `email` destinations not supported; scan and copy job creation need a UI Context token; invalid ticket options silently fall back to defaults; job lists hold 256 completed jobs and do not survive reboot (sub-reader A) | `G/scanJobServiceOverview.md:21,89-90,446,617-619,636`, `G/copyServiceOverview.md:402` |
| 33 | IPP: Print-Job by value and Print-URI by reference to a reserved (priority print) device "currently not supported"; one reservation at a time | `G/printJobIppExtensions.md:47,49,80-81` |
| 34 | Device service: print-engine status and alerts not supported this release (sub-reader B) | `G/deviceServiceOverview.md:14-15` |
| 35 | SDK Support: `pressScreen` and Functions not supported; whole service absent on production devices (sub-reader B) | `G/sdkSupportServiceOverview.md:4,203,270` |
| 36 | Solution Diagnostics: read-only, "latest available" log only, no crash report on OXPd2 (sub-reader B) | `G/solutionDiagnosticsOverview.md:52-54` |
| 37 | Job Statistics: notification filters fixed at install; ring buffer may overwrite unprocessed entries of a non-critical solution (sub-reader B) | `G/jobStatisticsServiceRegistration.md:215`, `G/jobStatisticsServiceOverview.md:62` |
| 38 | Admin token is lost on device reboot; the solution token "may need to be reissued" after a device reboot or crash (sub-reader B, re-read by me) | `G/exampleOverviewGuide.md:148-157` |

The sub-readers' full lists (32 and 70 items, mostly per-option limits) are not reproduced; the rows above are the ones that bear on the suite. No guide states a firmware minimum; the only firmware number in the guides is 6.25.0.730 for the IPP certificate default (`G/ews.md:185`).

## 5. What this means for the port

### 5.1 Mapping the suite to OXPd2 concepts

| Need of the suite | OXPd2 concept that carries it | Notes and limits |
|---|---|---|
| **Sign-in hub**: appear as a sign-in method on the panel | One Authentication Agent record; it shows in the native "Sign-In Method" list; kind `akCustom` (4.7) | The agent's target host should be `$SOLUTION_CONTEXT(...)` so each customer's local server is set at install |
| Sign-in UI (QR code, Microsoft sign-in, PIN) | The agent's `GET prompt` page in the embedded browser; the page talks to the Datasec server; closing the page triggers post-prompt (4.7) | Microsoft's pages must render in Chromium 87 with no pop-ups; redirect-style flows only (4.8). `trustedSites` must admit the Microsoft sign-in hosts |
| Card sign-in (HID keyboard-wedge readers) | USB Accessories record with each reader's vendor and product id as `rkOwned`; server opens the HID at boot and attach; `hidRead` payloads to the server; server calls `login(succeeded, details)` or `login(continue)` for enrolment (4.9, 4.7) | The server must decode raw HID keyboard reports into the card number. Reader ids are fixed in the signed bundle: a new reader model means a new HP-signed bundle |
| QR and phone (BLE) sign-in completed away from the panel | Server-side event, then `login(succeeded)` on that device; or, with the prompt page open, the page polls its server and closes | `login` works only when the panel is idle with no user signed in (4.7). BLE through the reader is a HID question, not covered by the guides |
| Share the signed-in user with the six apps | Not a device feature. All apps live on one server, so the Entra token cache is server-side, keyed by device id and authentication session id; the device carries only identity attributes (Security Context) | This is a simplification against Workpath's app-to-app token sharing. Declare `modifiedUserAttributes` (`userName`, `emailAddress`, display name, a custom key for the Entra object id) and a Security Agent listing them |
| Know which user is at the panel when a tile is opened | Header macros on the application target: `$DEVICE(ID)$`, `$SOLUTION_SESSION(UI_CONTEXT_TOKEN)$`, `$SECURITY_CONTEXT(...)$`; or `resolveSecurityExpression`; and `ntWalkupSignIn` / `ntWalkupSignOut` (4.2, 4.5, 4.7) | Check `AUTH_AGENT_ID` so a user signed in by another method is not mistaken for an Entra user |
| Sign-out clears the user's tokens | `signoutNotification` and `ntWalkupSignOut` to the server; server drops the session's tokens; `forceLogout` from the server when it must end a session (4.7) | The device timeout (default 60 s) drives this; the server must treat a missed notification as possible and expire sessions itself |
| **Six tiles** (Mailflow, Teams, OneDrive, SharePoint, Universal Print, others) | Six Application Agent records in one manifest, each with icon set, localised title and a web target on the server (4.8) | Per-customer licensing of tiles: bindable `enabled` plus `refresh`, or run-time registration of application agents (4.5) |
| Launch an app straight after sign-in | `login` with `action.initiateAppLaunch`, or `initiateLaunch` from the server (4.7, 4.8) | Start intent on the login action is not supported; it is on `initiateLaunch` |
| Panel UI of each app | Server-rendered web pages sized from `User Interface Attributes`; chrome through `runtimeChrome`; hard keys as key events (4.8) | Seven test groups down to 320x240 for a solution with authentication (4.4) |
| Scan to mail, Teams, OneDrive, SharePoint | Scan Job Agent; scan job with destination `http`: the device POSTs the file (multipart) to a receiver on the server; then Microsoft Graph from the server. `solutionContext` on the job carries the server's own session key; status by notifications (4.13) | Needs the app open on the panel (UI Context token). The server receiver must be reachable from the device and should require the target's bearer credential. No file picker exists in the browser; files only enter through the scanner. Output formats beyond PDF need the profile |
| Print from mail, OneDrive, SharePoint; Universal Print release | Server fetches or renders the document and prints by IPP: either Print-Job (server pushes bytes to the device's IPP port) or Print-URI (device pulls from a server URL with one-time credentials or cookie). Print Job Agent for priority print while the user is at the panel (4.11, 4.13) | The device's IPP certificate check is on by default from 6.25.0.730: the server's certificate must verify, or an administrator must switch the check off. Printing into a priority-print reservation is flagged "currently not supported" (section 6, row 17). The document must be in a language the printer accepts; conversion is the server's job (inferred) |
| Universal Print "secure" release with a hold on the device | No documented equivalent. Stored jobs in the guides are scans, not print jobs (4.13) | Hold the job on the server (or in Universal Print) and release on sign-in; this is the pull-print demo's pattern |
| Browse and pick documents | A web UI on the server; the browser cannot download or open files itself (4.8) | Previews must be server-rendered images |
| Device and usage logs (today in Log Analytics) | Job Statistics agent (per job, with user information when a user was signed in), Device Usage and Supplies agents (polled) (4.15) | The server must acknowledge every job record or lose them when the ring buffer wraps; it then forwards to Log Analytics |
| Deployment to a fleet | The server's own installer: admin credentials, password grant, `installSolution` or `installRemote`, context with the customer's server host, CA import, then install-code exchange (4.5, 4.6) | No HP fleet tool or cloud route is documented |
| Configuration per customer (tenant id, server host, feature flags) | Solution Context (sensitive keys for secrets) and the solution Configuration blob (4.4, 4.5) | Tenant secrets are better kept on the server than pushed to devices (inferred) |
| Diagnostics | Solution Diagnostics agent; EWS log download; remote browser debugger in developer mode only (4.6, 4.16) | |

### 5.2 Requirements and constraints, each tied to a finding

1. **One server, two device adapters.** A device speaks OXPd2 or OXPd1, never both (4.17). The application logic (Entra, Graph, Universal Print, token store) should sit behind a device-abstraction layer with an OXPd2 REST adapter and an OXPd1 SOAP adapter. HP itself says the same server can serve both (`P/how-it-works.md:28`).
2. **The server needs a route to every printer and every printer a route to the server** (4.10). A localised server on the customer's LAN satisfies both directly. A cloud-hosted server would need an inbound path to each device (VPN or an on-site relay); nothing in the guides provides one. This is the strongest documentary support for the "localised server" design.
3. **The server holds device credentials.** Per device: a refresh token (long-lived) and, at install time, the administrator password. The token store is a high-value secret store (4.3).
4. **A one-time, time-boxed handshake at install.** The server must be listening on the notification target at install time and exchange the install code within 5 minutes; an installer that deploys while the server is down must call `reissueInstallCode` later (4.3, 4.5).
5. **Everything customer-specific must be a context key**, because the manifest is frozen by HP's signature: server authority, every path, credentials for targets, trusted sites, tile visibility, notification list (4.4).
6. **Reboot handling.** After `ntDeviceBoot` the server must re-open owned card readers, and treat payload sequence numbers as reset (4.2, 4.9).
7. **Lead time and cost of HP signing.** HP App Center enrolment, a VAV submission per bundle version, and access to seven device classes for self-certification (4.4). The design should minimise how often the bundle changes: keep logic on the server, keep the manifest generic.
8. **Developer mode is destructive**, so development devices and customer pilot devices cannot be the same units without wiping (4.6).
9. **Reusable from the SDK** (as patterns, to be confirmed by the lanes that read the code): the pull-print demo is nearly the hub's skeleton (authentication agent, owned card reader, security agent, admin deployment page); the Java and .NET client libraries cover token grants and service clients (4.11, section 3).

### 5.3 Traps

- **Microsoft sign-in in Chromium 87.** The engine dates from late 2020 and the page cannot open pop-ups. Whether current Microsoft sign-in pages, Conditional Access prompts and passkey or FIDO flows work there is not answerable from the guides (inferred risk). A fallback that keeps the Microsoft page off the panel (device code or QR to the user's phone) is already in the product's character.
- **Cookie behaviour is undefined** (4.8). If the browser keeps Microsoft session cookies between walk-up users, user B could inherit user A's Microsoft session; if it drops them, every sign-in is a full sign-in. The cache lives in RAM until power cycle. This must be tested on firmware, and the server should force a fresh prompt (`prompt=login`) regardless (inferred).
- **Owned readers collide.** If another vendor's solution on the same device already owns the same reader model, the Datasec bundle fails to install (4.9). A customer running a third-party pull-print product with card sign-in on OXPd2 devices cannot simply add this suite.
- **Only one authentication session at a time, and `login` needs an idle panel** (4.7). A card tap while someone is signed in must be handled as "sign out, then sign in" using the `forceLogout` response action.
- **The device does not present a client certificate.** Anyone on the LAN who can reach the server's agent endpoints can imitate a device unless the target carries a secret. The bearer or Basic credential in the target, set per device through a sensitive context key, is the available control (4.3).
- **Short session timeout.** Default 60 seconds of inactivity ends the session and the UI; long Graph operations need `resetInactivityTimer`, used sparingly (4.7).
- **IPP certificate verification** defaults on; a private-CA server certificate must be trusted by the device's own certificate store (EWS Certificate Management), which is separate from the solution's CA store (4.11; the separation is inferred from `G/ews.md:231-246` and `G/solutionPackagingUtility.md:162`).
- **Tokens after a device reboot.** The example guide says the solution token "may need to be reissued" after a device reboot or crash (4.14). If a reboot does invalidate it, the server must detect 401 responses and call `reissueInstallCode`, which itself needs a valid token: an admin token if the solution's own is dead (inferred). An unattended recovery path may therefore need stored admin credentials. To be settled by test.
- **Scan and print both need the user's app session alive.** Scan creation and priority print are tied to the UI Context token, which dies with the 60-second inactivity timeout (4.7, 4.13).
- **What the guides leave unanswered** (collected): the HP Token Proxy; User Policy and Web Hook services; cookie and storage persistence between users; which CA store the browser uses for third-party sites; whether a same-id install upgrades in place; whether tokens survive reboot; the fields of `userInfo` and of the `login` details object; authentication of plain IPP submission; print languages accepted; how a custom agent's users map to device permissions; fleet deployment tooling; production firmware minimum and model list; a production release date.
- **Beta status.** Browser behaviour, kiosk, cookies and device list are explicitly unfinished; a production commitment date for customers depends on HP's production release, which no page dates.

## 6. Contradictions and doubts

| # | Disagreement or doubt | Sources | My reading |
|---|---|---|---|
| 1 | "for production use the scheme must be `http`" versus production validation "requires HTTPS" and VAV "Use HTTPS for all network communication" | `G/applicationServiceRegistration.md:126`, `G/solutionManagerRegistration.md:59` vs `G/solutionPackagingUtilityCli.md:346`, `P/publish.md:85` | A typo for `https`, repeated in two guides. Design for HTTPS only |
| 2 | Token URL written as `<deviceRoot>/cdm/oauth2/v1/token` in the table and `<deviceRoot>/oauth2/v1/token` in the three request examples | `G/securityModel.md:149` vs `:179,233,274` | The service-discovery sample gives `/cdm/oauth2/v1/token` (`G/architectureModel.md:537`); use discovery |
| 3 | Kiosk mode is documented as a working Homescreen API, but the SPU says "Kiosk applications are currently not supported" and the kiosk demo says the homescreen feature "is not supported this release" | `G/applicationServiceOverview.md:655-708` vs `G/solutionPackagingUtility.md:288`, `G/kioskAndBrowserDemoGuide.md:8` | Treat kiosk as unavailable in Beta 10 |
| 4 | An HP-signed bundle "can be installed using any FIM installation route", but two of the routes are "Currently not supported" and the diagram shows an EWS installer and a walk-up USB installer | `G/solutionManagerOverview.md:154` vs `G/securityModel.md:72-73`, `G/md-img/securityModel/securityModel-deploymentMechanisms.png` | Only the REST installer can be relied on today; EWS and USB install look like roadmap |
| 5 | Bundle described as "a simple ZIP archive", while the SPU builds SquashFS, DM-Verity hashes, a signed tarball, a PAK and a BDL, and the zip action is deprecated | `G/solutionManagerOverview.md:32` vs `G/solutionPackagingUtilityCli.md:143-147,339` | The overview text is stale |
| 6 | One authentication agent record or many | `G/authenticationServiceRegistration.md:4` vs `G/solutionPackagingUtility.md:372` | The SPU text is more specific; confirm in the OpenAPI spec |
| 7 | The platform-versions page stops at Beta 9 (firmware 6.34) and marks every version "Not Supported" for VAV, while the publish page describes a working VAV and the current SDK is Beta 10 | `P/platform-versions.md:9-21`, `P/publish.md:306-312`, `P/oxpd2-download.md:18` | Unclear whether any bundle can pass VAV today for customer use. A question for HP (section 7) |
| 8 | Portal prerequisites (OpenJDK 17, Gradle 7.5, NodeJS 18.14.2, SPU on macOS, two demos) versus the SDK guide (OpenJDK 21.0.4, Gradle 8.10, NodeJS 22.11, SPU on Windows and Linux only, six demos) | `P/how-it-works.md:67-72,90-92,157-160` vs `G/sdkUserGuide.md:23-27,34-39,143-149` | The portal page is older; the SDK guide governs |
| 9 | SPU locations: GUI at `tools/spu/spu-gui/net8.0/Debug` versus `tools\dotnet\spu\spu-gui\net8\Release`; CLI at `spu-cli/net6.0/Release` while the library index lists `spu-cli/net8.0/Release` | `G/solutionPackagingUtility.md:39`, `P/how-it-works.md:178`, `G/solutionPackagingUtilityCli.md:28`, `README-INDEX.md:7` | Trust the extracted SDK tree |
| 10 | Content type of a bundle: `application/vnd.hp.solution-bundle` for push, `application/vnd.hp.package-archive` or `application/vnd.hp.mod-archive` from a remote archive target | `G/solutionManagerOverview.md:271,294` | May be two real types; confirm in the spec |
| 11 | Macros `$OP_SOLUTION`, `SOLUTION_ACTIVE_HOST()`, `JOB()`, `SCAN()`, `ATTACHMENT()` are referenced but absent from the architecture guide's macro list | `G/solutionManagerOverview.md:299`, `G/securityServiceOverview.md:199-202` vs `G/architectureModel.md:848-859` | The macro list is incomplete; `SOLUTION_ACTIVE_HOST` hints at the unsupported host-set fail-over |
| 12 | Header values written as plain strings in the authentication example, as bindable objects everywhere else | `G/authenticationServiceRegistration.md:76-85` vs `G/applicationServiceRegistration.md:166-173` | Use the SPU's output |
| 13 | HELP key listed as keyCode 114 "(F4)"; 114 is F3 | `G/applicationServiceBrowserUseModel.md:160` | Test on a device |
| 14 | The browser guide links to an Application Runtime "reserve context" section that the overview does not contain | `G/applicationServiceBrowserUseModel.md:20` | Left over from an earlier design |
| 15 | "The device uses these solution-provided Certificate Authorities exclusively" for outbound TLS to "external solution endpoints": it is not said whether the embedded browser's connections to third-party trusted sites (Microsoft) use the same store or a public root store | `G/solutionPackagingUtility.md:162` | Open; decisive for showing Microsoft pages on the panel (section 7) |
| 16 | The publish page lists compatible model families for testing while the compatible-devices page says models are not yet defined | `P/publish.md:101-109` vs `P/compatible-devices.md:9` | The publish page (dated assets 2025-11) is newer |
| 17 | Submitting a print job to a device in priority print mode is "currently not supported" (by value and by reference), yet the pull-print demo prints documents and offers Enter and Exit Priority Print | `G/printJobIppExtensions.md:47,49` vs `G/pullPrintDemoGuide.md:420-441` | Either the note is stale or the demo prints outside the reservation. Must be tested on firmware; it decides how Universal Print release behaves |
| 18 | The scan guide says the Job Statistics Service is "not currently supported", while that service has full guides and is listed as introduced at Beta 9 | `G/scanJobServiceOverview.md:292` vs `P/platform-versions.md:19` | The scan guide note is stale |
| 19 | Where HID reports are delivered: the `registrationTarget` of the manifest record, or an `asyncIOTarget` given when the accessory is opened | `G/usbAccessoriesOverview.md:268,304` vs `G/exampleOverviewGuide.md:1574,1588`, and `G/architectureModel.md:596` (which calls the HID I/O target a transient registration) | The overview and registration guides agree with each other and are newer in wording; confirm in the OpenAPI spec |
| 20 | The solution token "will not expire" (example guide) versus an access token of 3600 seconds plus refresh token (security model); and it "may need to be reissued" after a device reboot | `G/exampleOverviewGuide.md:155` vs `G/securityModel.md:247-248` | The example guide speaks loosely of the refreshable pair. Whether a device reboot invalidates the refresh token is not settled by the guides and matters for unattended operation (section 7) |
| 21 | The scan create path is written `scanJob` (singular) for create and get and `scanJobs` (plural) for the collection and cancel (sub-reader A) | `G/scanJobServiceOverview.md:576-581` | Use the OpenAPI spec |
| 22 | Scheme lists for HTTP targets include `wss` although WebSocket targets are not supported (sub-readers A and B) | `G/scanJobServiceOverview.md:115`, `G/jobStatisticsServiceRegistration.md:69` vs `G/architectureModel.md:620` | Ignore `wss` |
| 23 | Rules for resetting the "last sequence notified" counter differ between three places (sub-reader B) | `G/exampleOverviewGuide.md:1088-1089`, `G/jobStatisticsServiceRegistration.md:196`, `G/jobStatisticsServiceOverview.md:109,200` | Use the registration guide's rule and test |
| 24 | Simple Scan and Simple Copy demos print the same solution id (sub-reader A) | `G/simpleScanDemoGuide.md:237`, `G/simpleCopyDemoGuide.md:235` | Likely a copy-paste error in one guide |

The sub-readers also listed about fifty editorial slips (field-name casing, copy-pasted sentences naming the wrong service, malformed examples). They do not change the model and are not repeated here; they are a reminder that the guides are beta documentation and the OpenAPI specifications are the contract.

## 7. Questions for Kam or his team

1. **Does Datasec have an HP App Center account for OXPd2 and has any OXPd2 bundle of any vendor passed VAV for customer installation yet?** Why: every production install needs an HP-signed bundle, and the platform-versions page marks all platform versions "Not Supported" for VAV. If unanswered I assume signing is available but adds weeks, and that pilots run on developer-mode devices.
2. **Where does the server live for the first customers: on the customer's LAN, or Datasec-hosted with a path into the customer network?** Why: the platform needs server-to-device calls as well as device-to-server. If unanswered I assume a customer-premises server (VM or container) with outbound internet to Microsoft, which is what "localised" suggests.
3. **Which OXPd2 devices can the team test on, and are all seven groups A to G reachable (including 480x272 and 320x240 panels and print-only models)?** Why: HP requires self-certified testing on each group for an authentication solution. If unanswered I assume only one or two MFP models plus the simulator, which blocks VAV until more are borrowed.
4. **What is the "HP Token Proxy" for which the App Center issues client credentials?** Why: it may be HP's answer to cloud-hosted solutions reaching devices, which would change the network design. The library's guides do not explain it. If unanswered I ignore it.
5. **Must Microsoft's sign-in page be shown on the panel, or is phone-based sign-in (QR or device code) plus card acceptable as the only interactive methods on OXPd2?** Why: the panel browser is Chromium 87 with unfinished cookie handling. If unanswered I design phone and card first and treat on-panel Microsoft sign-in as a tested option.
6. **Which card reader models (USB vendor and product ids) must the first signed bundle list?** Why: the list is frozen by HP's signature. If unanswered I take the six models in the earlier OXPd1 attempt plus the HP readers named in the HPAM material.
7. **Do target customers already run another vendor's card-authentication or pull-print solution on the same OXPd2 devices?** Why: only one solution can own a reader model on a device. If unanswered I assume the suite is the only authentication solution on the device.
8. **Who at the customer supplies device administrator credentials, and may the server store them?** Why: install needs them once per device; ongoing operation does not. If unanswered I assume they are entered at deployment and never stored.
9. **Is the customer's server certificate issued by a private CA?** Why: the CA must be imported per device into the solution's store, and separately trusted for IPP. If unanswered I build CA import into the deployment tool.
10. **Is kiosk mode (suite replaces the home screen) wanted?** Why: it is not available in Beta 10. If unanswered: no.
11. **Is there an HP contact (partner engineer or the OXPd2 beta forum) who can answer four platform questions the guides leave open:** tokens after device reboot, printing during priority print, browser cookie persistence between users, and the CA store used for third-party sites? Why: each changes a design decision. If unanswered I plan a test spike on a developer-mode device for each before the architecture is frozen.
12. **Does the suite need per-user device permissions or quotas on OXPd2 (block copy for some users, for example)?** Why: the only carrier is the undocumented User Policy service (Alpha 2). If unanswered I assume no: the suite authenticates and leaves device permissions to the device's own access control.

## 8. Secrets and sensitive items seen

No secret value appears in the guides I read; examples use placeholders (`<secret>`, `<access-token>`). Items worth knowing, locations only:

- The SDK ships a development root CA whose private key HP says is distributed to every approved developer; the guides place it at `tools/certificates/ExtSDKRootCA.pem` inside the SDK with a generation script beside it (`G/sdkUserGuide.md:53-55`). It must never reach a production bundle; the SPU's production validation rejects it (`G/solutionPackagingUtilityCli.md:347`).
- The demos tell the developer to write a certificate password into `appsettings.json` or `application.properties` in the demo folders (`G/pullPrintDemoGuide.md:63-74,116-120`). Any such file in the extracted SDK or in Datasec's own trees may hold a real password; that is for the code lanes to check.
- The LDB Service Key is a personal developer credential managed on the HP portal (`G/debugBridge.md:22-29`).
- Two solution ids of SDK demos are printed in the guides (`G/pullPrintDemoGuide.md:259`, `G/kioskAndBrowserDemoGuide.md:321`); they are identifiers, not secrets.

Weaknesses in the demo pattern that the port must not copy:

- The pull-print demo accepts any card data as a valid user (`G/pullPrintDemoGuide.md:415`).
- The demo's authentication log page displays the session access token (`G/pullPrintDemoGuide.md:341`).
- Demo context files use `TRUSTED_SITES` = `*` and plain `http` schemes with no target authorisation (`G/kioskAndBrowserDemoGuide.md:60-61`, `G/solutionManagerRegistration.md:264`).
- The demo admin page takes the device administrator password in a web form (`G/pullPrintDemoGuide.md:239-240`); a real installer needs TLS, no logging of it, and no storage.
