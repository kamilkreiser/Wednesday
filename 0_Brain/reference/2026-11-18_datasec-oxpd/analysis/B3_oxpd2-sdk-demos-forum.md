# B3 — OXPd2 SDK Beta 10 as shipped, its demos, and the field experience (forum + knowledge base)

Lane B3 of the Datasec / OXPd analysis, 18 Nov 2026. Library root: `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/` (read-only; nothing was run, built, unpacked or changed).

Path shorthand used in citations (all relative to the library root):

- `SDK/` = `OXPd2/SDK/OXPd2-SDK-Beta-10/`
- `PPA/` = `SDK/demos/pullPrintAuth/dotnet/PullPrintAuth/`
- `SF/<date>-<id>` = the thread file in `OXPd2/Support-Forum/` whose name starts with that date and Zendesk id (file names are long; the prefix is unique)
- "manifest" = a demo's `common/bundle/spu_project.json`; entries are cited by JSON path because the files were parsed, not read line by line.

---

## 1. BLUF

This lane holds the OXPd2 SDK Beta 10 (released 1 June 2026, build 20260416.1, minimum firmware 6.38.0.793), its three client libraries, six demos, the packaging and certificate tools, and all 29 partner forum threads plus the one knowledge-base article. Five facts shape the port:

1. **There is no working route to a customer device today.** A bundle installs without the developer mode (LDB) only if HP signs it through App Center "VNV". The one partner who went all the way through that in November 2026 got a signed bundle that the Beta 10 firmware and the simulator both reject; HP's last word (17 Nov 2026) is that they are still waiting on the signing team (`SF/2026-11-06-57213300079635:273-275, 301-340, 361, 378`). HP also says LDB is not supported for customer production (`SF/2026-11-06-57213365367443:110`).
2. **An OXPd2 solution is a plain HTTPS web server plus a signed manifest bundle.** The bundle carries no code: it declares agents whose targets point back at the server (`$SOLUTION_CONTEXT(HOST)$`), and the device calls those endpoints. The server calls the device's REST services with three kinds of token. Everything Datasec does on the panel today has to become pages served by that server.
3. **The pullPrintAuth demo is the right skeleton for a sign-in hub** (card swipe to pre-prompt result to device session to auto-launched app), but it is a single-device, in-memory, no-authentication toy that accepts any card and disables TLS validation. It proves the call sequence only.
4. **C# is the reference language.** Every API landed in the .NET library first (Beta 1 to 4), then Java, then JavaScript; all three are at parity since Beta 7, with the same holes. The .NET library is netstandard2.0 and the demos are ASP.NET Core on net8.0, which matches the existing Datasec back end.
5. **HP told a partner in 2023 that OXPd does not support direct integration with public cloud services such as SharePoint Online, and that Workpath is the SDK for that** (`SF/2023-06-15-17607595895827:98-100, 160`). The suite being ported is exactly that integration. Technically the server, not the device, would call Microsoft Graph, so this may be a statement about the device only, but it needs HP's confirmation before the plan is committed.

---

## 2. Coverage

Honest summary: the forum, the knowledge base and the release notes were read whole. The pullPrintAuth demo was read whole in C# except its IPP protocol classes. The other demos were read in their key service and controller files only. The example host, the Java and JavaScript sources and the statsDemo were **not** read; they were inventoried and probed with searches. This is less than the lane asked for (every demo whole in one language); the session's context budget ran out and an attempt to hand the remaining reading to helper agents was refused by the session's agent limit.

| Area | Read whole | Sampled (how) | Not opened |
|---|---|---|---|
| Library root | `START-HERE.md`, `README.md`, `README-INDEX.md` | | |
| Release notes | `OXPd2/SDK/README_Beta_10.txt` (198 lines) | | |
| Forum | all 29 threads and `INDEX.md` (every line, including the 49-comment thread) | | images linked to Zendesk (sign-in required) |
| Knowledge base | the 1 article and `INDEX.md` | | the attached PNG |
| pullPrintAuth (.NET) | 11 files as written (Program, Startup, csproj, 2 appsettings, launchSettings, AuthenticationAgent controller + service, UsbAccessoriesAgent controller + service, ApplicationAgent controller); 16 files with only blank, brace, `using` and comment-only lines stripped (UserManagement, UserJobs, DocumentManagement, PrintOperations services and controllers, PullPrintRunThread, 5 models, SupportedLanguages, IppClient lines 1-117) | `Ipp/IppClient.cs` lines 118-276, `LoginPage.html`, `PrintDocuments.html` (searched for network calls, attributes, tokens) | `IppRequest`, `IppResponse`, `IppConstants`, `IppAttribute`, `IppAttributeGroup`, `IppBinaryReader` (6 files, about 2,170 lines) |
| pullPrintAuth manifest | parsed whole (851 leaf values); every non-icon, non-translation entry read | | the built `solution.bdl` (noted only) |
| Demos common (.NET) | 13 of 18 `.cs` files plus the csproj | | 2 exception filters, 3 small models |
| simpleScan (.NET) | code lines of `ScanJobService`, `ScanJobAgentController`, `ScanJobAgentService`, `ScanJobController` | | Startup, Program, ApplicationAgentController, HTML, manifest |
| storedJob (.NET) | code lines of `StoredJobService`, `StoredJobController`, `ScanJobAgentController` | `StoredJob.html` (searched) | the other 6 `.cs`, manifest |
| simpleCopy (.NET) | code lines of `CopyService` | | the other 6 `.cs`, manifest |
| kioskAndBrowser | | Startup and 4 controllers (searched for routes and headers); manifest parsed, key entries read; `deviceProxy.js` lines 1-48 and 160-185; `application/application.js` first 90 lines (searched) | the other device-side pages, the server-side React bundle, Java, JS |
| statsDemo | | | all of it |
| Example host | | file-name inventory in 3 languages; search for TLS overrides and ports | all 56 `.cs`, 79 `.java`, 77 `.js` |
| Java and JS demos | | searches only (ports, TLS handling, presence of the card flow and IPP classes) | all source |
| Libraries | `OXPd2Lib.deps.json`, JS `package.json` and `index.js` | DLL and JAR inspected by listing names only (namespaces, package and class counts); JS bundle searched for names | library code itself (binary or minified) |
| Tools | SPU CLI `README.md` (216 lines), `san.conf`, `generateHPExtSDKExample.sh` (6 lines; the two lines carrying passwords were read with the values masked) | Postman collections and environment (parsed for folder names, request counts, variable names); root CA certificate (subject and dates) | SPU GUI `appsettings.json`, all tool binaries, the 72 schema copies under `tools/spu` |
| Specifications | 16 version file names; path lists of the 5 "service target" specs (parsed) | | everything else (lane B-other covers the specs) |
| `LICENSE.txt` | | headings of each block and searches over the whole 1,376 lines | body text of the standard licences |
| Beta 9 zip, documentation AppImage, Beta 10 zip | | | not opened (noted only) |

Counts: the extracted SDK holds 1,513 files. About 60 source and config files were read in full or in code-line form, about 10 more were sampled, the rest were inventoried.

---

## 3. Inventory

### 3.1 What is in `OXPd2/SDK/`

| Item | What it is | Source |
|---|---|---|
| `OXPd2-SDK-Beta-10-20260416.1.zip` | original download, 613 MB | directory listing |
| `OXPd2-SDK-Beta-9-20250923.1.zip` | previous beta, 605 MB, kept zipped, not opened. Must not be mixed with Beta 10 firmware | `OXPd2/SDK/README_Beta_10.txt:56` |
| `README_Beta_10.txt` | release notes | |
| `OXPd2-SDK-Beta-10/` | extracted SDK, 1,513 files: `libraries/`, `examples/`, `demos/`, `tools/`, `specifications/`, `documentation/`, `LICENSE.txt` | directory listing |

Release facts: release date 1 June 2026; SDK build 20260416.1; minimum firmware 6.38.0.793-202605190445 (`OXPd2/SDK/README_Beta_10.txt:5-7`).

### 3.2 Libraries

| Library | Form | Version and dependencies | What it exposes |
|---|---|---|---|
| .NET | `SDK/libraries/dotnet/netstandard2.0/Release/OXPd2Lib.dll` (1.5 MB) with `.pdb` | assembly `OXPd2Lib/1.0.0`, target .NET Standard 2.0; depends on Newtonsoft.Json 13.0.1, Microsoft.CSharp 4.7.0, System.Reflection.TypeExtensions 4.7.0, System.ValueTuple 4.5.0 (`SDK/libraries/dotnet/netstandard2.0/Release/OXPd2Lib.deps.json:10-17`) | namespaces `HP.Extensibility.Client.*` (Application, Authentication, Copy, Device, DeviceUsage, Discovery, JobStatistics, PrintJob, ScanJob, SdkSupport, Security, SolutionDiagnostics, SolutionManager, Supplies, UsbAccessories, plus OAUTH2 used by the demos), `HP.Extensibility.Service.*` and `HP.Extensibility.Types.*` (names read from the binary's string table) |
| Java | `SDK/libraries/java/oxpd2lib.jar` (1.8 MB, 1,660 entries) | manifest holds only `Manifest-Version: 1.0`; no version, no dependency list inside the jar | packages `com.hp.ext.clients.*` (same 15 services plus `discovery` and `oauth2`), `com.hp.ext.service.*`, `com.hp.ext.types.*` |
| JavaScript | `SDK/libraries/js/` : `index.js`, `lib/oxpd2.js` (1.3 MB bundle) and one file per service, each with a `.map` and a `.sig` | `package.json` says name `oxpd2`, version `1.0.0`, `"license": ""`, `"private": true` (`SDK/libraries/js/package.json:2-7`) | the same services; the per-service files are also loaded directly by pages running in the printer's browser (see 4.6) |

None of the three libraries has a client for the **userPolicy** or **webHook** services, although both have specifications; the .NET and Java libraries carry `Service.WebHook` types only. The userPolicy specification is at **alpha 2**, every other service is at beta (`SDK/specifications/com.hp.ext.service.userPolicy/1/0/_userPolicy-1.0.0.alpha-2.txt`, file names of the other 15 version files).

Licence: the libraries carry no licence text of their own. `SDK/LICENSE.txt` is a third-party notices file only (see 4.10).

### 3.3 Specification versions shipped in Beta 10

From the version file names under `SDK/specifications/com.hp.ext.service.*/`:

| Service | Version | Service | Version |
|---|---|---|---|
| application | 1.0.0 beta 14 | sdkSupport | 1.0.0 beta 11 |
| authentication | 1.0.0 beta 6 | security | 1.0.0 beta 6 |
| copy | 1.0.0 beta 3 | solutionDiagnostics | 1.1.0 beta 2 |
| device | 1.0.0 beta 7 | solutionManager | 1.0.0 beta 13 |
| deviceUsage | 1.0.0 beta 5 | supplies | 1.0.0 beta 4 |
| jobStatistics | 1.0.0 beta 7 | usbAccessories | 1.0.0 beta 13 |
| printJob | 1.0.0 beta 5 | userPolicy | 1.0.0 **alpha 2** |
| scanJob | 1.0.0 beta 10 | webHook | 1.0.0 beta 3 |

### 3.4 Examples, demos, tools

| Component | Languages | Port | Entry point (.NET) |
|---|---|---|---|
| Example host (`SDK/examples/`) | .NET (56 `.cs`), Java (79), JS (77) | 5000 | `SDK/examples/dotnet/OXPd2ExamplesHost/` |
| pullPrintAuth | .NET (29 `.cs`), Java (49), JS (37) | 5050 | `PPA/Program.cs` |
| simpleScan | .NET (7), Java (9), JS (10) | 5150 | `SDK/demos/simpleScan/dotnet/SimpleScan/` |
| simpleCopy | .NET (7), Java (9), JS (10) | 5250 | `SDK/demos/simpleCopy/dotnet/SimpleCopy/` |
| kioskAndBrowser | .NET (8), Java (10), JS (12) + device-side web app | 5450 | `SDK/demos/kioskAndBrowser/dotnet/KioskAndBrowser/` |
| statsDemo | .NET (12), Java (16), JS (14) | 5550 | `SDK/demos/statsDemo/dotnet/StatsDemo/` |
| storedJob | .NET (9), Java (12), JS (13) | 5650 | `SDK/demos/storedJob/dotnet/StoredJob/` |
| demos common | .NET (18), Java (26), JS (32) | | `SDK/demos/common/dotnet/DemosCommon/` |

Ports are from `OXPd2/SDK/README_Beta_10.txt:76-83`; the note says they can be changed in each project's Program file (`:87`).

Stacks: .NET demos target `net8.0` with `Microsoft.AspNetCore.Mvc.NewtonsoftJson` 6.0.0 and reference the DLL by relative path (`PPA/PullPrintAuth.csproj:3-7, 39-41`). Java demos and examples are Spring Boot 3.2.2 on Gradle (`SDK/demos/pullPrintAuth/java/build.gradle:2`, `SDK/examples/java/build.gradle:2`). JS demos are Express 4.18 on Node (`SDK/demos/pullPrintAuth/js/package.json:8`).

Each demo also has `common/bundle/spu_project.json` (the manifest project for the packaging tool), `common/bundle/build/solution.bdl` (a prebuilt development bundle) and `common/view/dist` (a prebuilt React admin page that the demo serves to the developer's PC browser).

Tools (`SDK/tools/`, 251 files):

- `postman/OXPd2.postman_collection.json`: 14 folders, 154 requests (Solution Manager 33, Application 30, SDK Support 15, Copy 13, USB Accessories 12, Scan Job 9, Authentication 8, Device 6, Supplies 6, Job Statistics 6, Solution Diagnostics 5, Device Usage 4, Security 4, Print Job 3), bearer auth. `CDM.postman_collection.json`: OAUTH2 (3), System (2), Services Discovery (1). `OXPd2 Workspace Environment.json`: variable names only, all values empty. A `multipart-packer` helper for Postman (net8.0).
- `certificates/`: `ExtSDKRootCA.pem`, `ExtSDKRootCA.key`, `generateHPExtSDKExample.sh`, `san.conf` (see 4.9).
- `spu/spu-cli` and `spu/spu-gui` (net8.0, Avalonia UI for the GUI): the Solution Packaging Utility. Executables ship for Linux x86-64 (ELF) and Windows x86-64 (PE) only; there is no macOS executable (checked with `file`, not executed).
- `documentation/oxpd2-sdk-documentation-0.10.0.AppImage` (276 MB, not opened; its content is already extracted to `OXPd2/Docs/SDK-Documentation/` per `README.md`).

---

## 4. Findings

### 4.1 How a real OXPd2 solution is structured in code

**The host process.** An ordinary web application. In .NET: `Host.CreateDefaultBuilder` with a `Startup` class (`PPA/Program.cs:17-22`), controllers with Newtonsoft JSON and string enums (`PPA/Startup.cs:38-41`), a named `HttpClient` "oxpd" for calls to the device (`PPA/Startup.cs:55-61`), and every service registered as a **singleton** (`PPA/Startup.cs:64-75`). All routes hang under a path base named after the demo, for example `/pullPrintAuth` (`PPA/Startup.cs:26, 102`).

**Two directions of traffic.**

1. *Server to device.* The server reads the device's service discovery tree once and caches it (`SDK/demos/common/dotnet/DemosCommon/Services/DeviceManagementService.cs:209-221`), then builds a typed client per service from the HTTP client, the device address and the discovery tree, for example `new UsbAccessoriesServiceClient(httpClient, networkAddress, servicesDiscovery)` (`PPA/Services/UsbAccessoriesAgentService.cs:56`). Device addresses default to `https://` (`DeviceManagementService.cs:184-187`).
2. *Device to server.* The device calls endpoints the solution declared in its manifest. These are the "agents". The shapes of the calls are fixed by HP in "service target" specifications shipped beside the service specs:

| Agent | Endpoints the server must expose (relative to the target path in the manifest) | Source |
|---|---|---|
| Authentication agent | `POST /prePromptResult`, `GET /prompt`, `POST /postPromptResult`, `POST /signoutNotification` | `SDK/specifications/com.hp.ext.service.authentication/1/0/serviceTarget.openapi.json` (paths) |
| USB accessories agent | `POST /registration`, `GET /registrationPrompt`, `POST /postRegistrationPromptResult`, `POST /operationCallback` | `SDK/specifications/com.hp.ext.service.usbAccessories/1/0/accessoriesAgentServiceTarget.openapi.json` |
| Scan job HTTP destination | `POST /` (the scan payload) | `SDK/specifications/com.hp.ext.service.scanJob/1/0/httpDestinationServiceTarget.openapi.json` |
| Job statistics agent | `POST /jobStatistics` | `SDK/specifications/com.hp.ext.service.jobStatistics/1/0/statisticsServiceTarget.openapi.json` |
| User policy agent (alpha) | `POST /configurationChange`, `POST /applyUserPolicy` | `SDK/specifications/com.hp.ext.service.userPolicy/1/0/userPolicyServiceTarget.openapi.json` |
| Application agent | `GET` on the application target: returns the HTML page the panel browser shows | `PPA/Controllers/ApplicationAgentController.cs:33-106` |
| Solution notification agent | `POST` on the notification target: install events and the install-time authorisation code | `SDK/demos/common/dotnet/DemosCommon/Controllers/SolutionNotificationAgentController.cs:25-46` |
| Scan / copy job agents | `POST .../scanJobNotification`, `.../copyNotification` (job status events) | `SDK/demos/simpleScan/dotnet/SimpleScan/Controllers/ScanJobAgentController.cs:34-43`; kiosk manifest context keys `SCANJOB_NOTIFICATION_PATH`, `COPY_NOTIFICATION_PATH` |

**Three tokens.** The demos model three access tokens per device, ordered by scope (`SDK/demos/common/dotnet/DemosCommon/Models/DeviceModel.cs:23-29`):

- *Admin token*: obtained with the device administrator's user name and password through an OAuth2 password grant against the device (`DeviceManagementService.cs:66-96`). Needed to install, uninstall and reissue the install code (`SDK/demos/common/dotnet/DemosCommon/Services/SolutionDeploymentService.cs:54-55, 76-77, 143-144`).
- *Solution token*: after install, the device posts a notification of type `ntAuthCode` to the notification agent; the server exchanges the code for a token with an authorisation-code grant (`SDK/demos/common/dotnet/DemosCommon/Services/SolutionNotificationAgentService.cs:43-57`, `DeviceManagementService.cs:98-128`). It expires and is renewed with a refresh-token grant (`DeviceModel.cs:125-134`, `DeviceManagementService.cs:130-163`). If the code is lost, an admin can ask the device to reissue it (`SolutionDeploymentService.cs:138-156`).
- *UI context token* and *authentication context token*: short-lived, per panel session. The device hands them to the server as HTTP headers on the agent calls, filled by macros in the manifest: `oxpd-ui-context = $SOLUTION_SESSION(UI_CONTEXT_TOKEN)$` on the application target and `oxpd-authn-contextId = $SOLUTION_SESSION(AUTHENTICATION_CONTEXT_TOKEN)$` on the authentication target (pullPrintAuth manifest, `applicationService.applications[0].target.applicationAgentTarget.targetHeaders[3]` and `authenticationService.authenticationAgents[0].target.targetHeaders[0]`). The pre and post prompt requests also carry a `SessionAccessToken` in the body (`PPA/Services/AuthenticationAgentService.cs:62-66, 90-94`).

Which token a call needs is written beside each call in the demos, for example scan job creation needs the UI context token (`SDK/demos/simpleScan/dotnet/SimpleScan/Services/ScanJobService.cs:121-124`) while reading default scan options needs the solution token (`:87-90`).

**Registration and discovery.** There is no network discovery of devices in the demos. A person types the device address into the demo's admin page and the server "binds" to it (`SDK/demos/common/dotnet/DemosCommon/Controllers/DeviceManagementController.cs:24-30`). Binding is only a cached address plus discovery tree; it never times out and is lost when the process stops. HP confirmed that and added that this is example code not designed for production (`SF/2026-11-06-57222527847443:28-32`).

**Installation.** The server posts the bundle to the device's Solution Manager as a multipart request with three parts: `content` (JSON install request), `solution` (the `.bdl`, media type `application/vnd.hp.solution-bundle`) and `context` (JSON values for the manifest's context keys) (`SDK/demos/common/dotnet/DemosCommon/Controllers/SolutionDeploymentController.cs:61-118`, `SolutionDeploymentService.cs:86`). The result is an operation that is polled until it succeeds or fails (`SolutionDeploymentService.cs:115-136`). A partner's write-up gives the raw REST form: `POST /ext/solutionManager/v1/installer/installSolution`, then poll `GET /ext/solutionManager/v1/installer/installerOperations/{operationId}` for `iosSucceeded` or `iosFailed` (`SF/2026-11-06-57213300079635:155-160`).

**The bundle and its manifest.** The pullPrintAuth manifest (project name `PullPrintAuthDemo`, written by SPU 1.6.0) declares:

- solution id `26b17488-4907-407f-b9a7-6b60ce8554b3`, vendor "HP OXPd SDK Demo", version 1.2.0 (`solutionManager.solutionDetails`);
- ten **context keys** with defaults, the install-time configuration: `HOST` (default `localhost:5050`), `NOTIFICATION_AGENT_PATH`, `APPLICATION_AGENT_PATH`, `AUTHENTICATION_AGENT_PATH`, `USB_REGISTRATION_TARGET_PATH` (each defaulting to a path under `/pullPrintAuth/api/...`), `HEADER_BACKGROUND`, `HEADER_FOREGROUND`, `CUSTOM_HEADER`, `NOTIFICATIONS` (default `["ntAll"]`) and `TRUSTED_SITES` (default `*`) (`solutionManager.contextDefinitions[0..9]`);
- a notification agent, an application (category `acStandardWalkup`), a print job agent, an authentication agent (pre-prompt check and sign-out notification both enabled), a security agent and a USB accessories agent;
- every target as `https` + `$SOLUTION_CONTEXT(HOST)$` + a path context key, with authorisation type `None`;
- one certificate authority packaged in the bundle (`solutionManager.certificateAuthorities[0]`, stored at `/assets/certificateAuthorities/<id>.pem`);
- trusted sites bound to the `TRUSTED_SITES` context key (`solutionManager.trustedSites`);
- translated strings for the titles and descriptions (i18n assets).

So **the server address is not baked into the bundle**: it is supplied as the `HOST` context value at install time, and one signed bundle can serve every customer. The scan, copy, statistics, supplies and diagnostics sections exist in the manifest project but are switched off in this demo.

**Configuration.** Beyond the context keys, the manifest has a `configuration` section (not used by the demo: `solutionManager.configuration.includeConfiguration = False`). The server side uses `appsettings.json`, where the HTTPS endpoint is commented out and must be filled in by the developer with a `.pfx` or a certificate-store entry (`PPA/appsettings.json:12-28`).

**Certificates: development.** Two trust directions:

- *Device trusting the server.* All targets are `https`. The SDK ships a development root CA (certificate and encrypted private key) and a six-line script that issues a server certificate for a given common name and IP address (2048-bit key, 500 days, subject alternative names for both the name and the IP) and exports a `.pfx` for Kestrel (`SDK/tools/certificates/generateHPExtSDKExample.sh:1-6`, `SDK/tools/certificates/san.conf:21-30`). The root CA is valid 15 Feb 2022 to 21 Jul 2038 (read with `openssl x509`). The demo bundles carry a CA certificate so the device trusts that chain (inferred that it is this same CA; the certificate bytes were not compared).
- *Server trusting the device.* The demos switch validation off entirely: `DangerousAcceptAnyServerCertificateValidator` under a "TODO: Fix this" comment in every .NET demo (`PPA/Startup.cs:59-60`), an `InsecureHttpClientFactory` in Java (`SDK/demos/common/java/lib/src/main/java/com/hp/extensibility/demoscommon/utilities/InsecureHttpClientFactory.java:26-56`), and an equivalent override in each JS `app.js` (search hit in `SDK/demos/*/js/src/app.js`; lines not read).

**Certificates: production.** The SDK shows no production pattern. What the forum adds: certificates added through the Solution Manager's Certificate Authorities resource are visible **only to that solution**; other solutions and the device's native apps need their own (`SF/2026-11-04-57156007627539:41`), and the bundle must be installed before `ImportCertificateAuthority()` can be used (`:78`). A production design therefore needs (a) a customer-trusted or public certificate on the server, with its CA either in the bundle or imported per device after install, and (b) real validation of the device's certificate, which the SDK does not demonstrate.

### 4.2 pullPrintAuth, call by call: the pattern for a sign-in hub with held-job release

Setup, done once by an administrator from the demo's admin page: bind the device, get the admin token, install the bundle with `HOST` set to the server, receive `ntAuthCode`, exchange it for the solution token (4.1).

**A. Card reader attached.**

1. The manifest's USB accessories agent registers one reader as "owned" (`registrationKind = rkOwned`) by USB vendor id and product id, here 1008 and 69 in decimal (0x03F0 and 0x0045) (manifest `usbAccessoriesService.usbAccessoriesAgent.registrations[0]`). Only readers listed in the manifest are delivered to the solution.
2. When that reader is plugged in, the device posts to `.../usbAccessoriesTarget/registration` with a `UsbAttached` payload (`PPA/Controllers/UsbAccessoriesAgentController.cs:21-35`).
3. The server waits for the solution token and opens the reader's HID interface for reading: `Accessories[resourceId].Hid.OpenHidOperation.ExecuteAsync(token, { ReportReadingActive = true })` (`PPA/Services/UsbAccessoriesAgentService.cs:50, 58-65`). An open failure is only written to the console (`:68-71`).

**B. Card swiped.**

4. The device posts the HID report to `.../usbAccessoriesTarget/operationCallback` (`UsbAccessoriesAgentController.cs:39-50`).
5. The server calls `LoginWithCard(data)`: it prepares a **pre-prompt result** in memory, success with user details or failure "Invalid Card" (`PPA/Services/AuthenticationAgentService.cs:148-185`). In the demo the card data is not decoded or looked up: any non-empty read is mapped to the fixed user `cardUser` (`:165-169`, `PPA/Services/UserManagementService.cs:116-126`).
6. The server answers the callback with an action: `InitiateLogin { AccessToken = <solution token>, AgentAccessPointId = 63a79165-7266-444d-a7f1-e69e31abd243 }` (`UsbAccessoriesAgentService.cs:87-97`). That id is the authentication agent declared in the manifest. This is the "USB action flow" that Beta 10 introduced for this demo (`OXPd2/SDK/README_Beta_10.txt:40`).

**C. The device starts sign-in.**

7. The device posts `prePromptResult` to the authentication agent target. Because a card login is in progress, the server returns the prepared result and the panel never shows a prompt (`AuthenticationAgentService.cs:53-60`).
8. A successful result carries `AuthenticationSuccess.Details` (display name, e-mail address, user name, preferred language, fully qualified user name; the manifest lists which attributes the agent may set: `authenticationService.authenticationAgents[0].modifiedUserAttributes`) and an action `InitiateAppLaunch { ApplicationAccessPointId = 37531a6f-... }` so the device opens the solution's application straight after sign-in (`AuthenticationAgentService.cs:172-179, 193-205`). The device now has a signed-in session for that user.

**D. Manual sign-in (no card).**

9. The user picks the agent from the panel's sign-in list. The device posts `prePromptResult`; the server stores the session token and answers "continue" (`AuthenticationAgentService.cs:62-78`).
10. The device's embedded browser does `GET .../authenticationAgent/prompt`; the server returns `LoginPage.html` (`PPA/Controllers/AuthenticationAgentController.cs:52-60`). The page posts the user name and password to the server's own `/authenticationAgent/login`, then calls `window.close()` (`PPA/WebContent/LoginPage.html:86-102`); cancel posts to `/cancelLogin` (`:114-127`).
11. When the browser closes, the device posts `postPromptResult`; the server returns the stored success, failure ("Invalid Username/Password") or cancel, plus the same auto-launch action on success (`AuthenticationAgentService.cs:81-106, 109-146`).

**E. The application opens.**

12. The device browser does `GET .../applicationAgent` with the manifest-defined headers: `oxpd-ui-context` (UI context token), `oxpd-authenticated-user` (`$SECURITY_CONTEXT(FQ_USER_NAME)$`), `oxpd-device-address` (`$DEVICE(IPV4_ADDRESS)$`), `oxpd-solution-id`, and a custom header (manifest `applicationAgentTarget.targetHeaders[0..4]`). The security macros work because the manifest's security agent declares the operators `DISPLAY_NAME`, `EMAIL_ADDRESS`, `USER_NAME`, `FQ_USER_NAME` (`securityService.securityAgent.declaredExpressionOperators`).
13. The server stores the UI context token, resolves the user from the header, records the device address, and returns `PrintDocuments.html` (`PPA/Controllers/ApplicationAgentController.cs:51-105`).

**F. Job list.**

14. The page asks the server (not the device) for the current user and that user's jobs: `GET /userManagement/currentUser` (`PPA/WebContent/PrintDocuments.html:226`), then `GET /userJobs?user=...` and `GET /documentManagement/documents` (`PPA/Controllers/UserJobsController.cs:30-35`, `PPA/Controllers/DocumentManagementController.cs:24-28`). The job store is a dictionary seeded from files in `WebContent/PrintFiles` (`PPA/Services/DocumentManagementService.cs:84-100`, `PPA/Services/UserJobsService.cs:57-78`).

**G. Release.**

15. The page posts the chosen document ids to `POST /printOperations/{requestingUserName}`; the server builds an operation and queues it on a single worker thread (`PPA/Controllers/PrintOperationsController.cs:31-50`, `PPA/Services/PullPrintRunThread.cs:41-58`).
16. For each document the server sends the device an **IPP Print-URI** request. The device then **fetches the document itself** from the server at `<server scheme and host>/WebContent/PrintFiles/<name>` (`PPA/Services/PrintOperationsService.cs:191, 200`). The request carries `document-uri`, `requesting-user-name`, and the UI context token as a "priority print auth cookie" attribute (`PPA/Ipp/IppClient.cs` about lines 160-168). The IPP endpoint is found in the discovery tree under the service name `com.hp.standard.feature.pwgIpp`, link relation `homeUrl`, falling back to `/ipp/print` (`PPA/Ipp/IppClient.cs:30-35, 55-64, 92`), and is posted to over `https` (`:262`).
17. The server polls `Get-Job-Attributes` every two seconds until the job is completed, cancelled, aborted or stopped, and prints one file at a time (`PrintOperationsService.cs:209-210, 242-310`). Cancel is `Cancel-Job` (`:320-338`). The page polls `GET /printOperations/{operationId}` for status (`PrintDocuments.html:363`).
18. "Priority print" enter and exit are separate IPP operations authorised by the UI context token (`PrintOperationsService.cs:93-128`, `PPA/Controllers/PrintOperationsController.cs:85-98`). What priority mode does on the device was not read (it is in the SDK guides, another lane).

**H. Sign-out.** The device posts `signoutNotification`; the server drops the session token and the stored result (`AuthenticationAgentController.cs:62-72`).

Things the demo does **not** show, which a real hub needs: decoding the HID reports into a card number (4.11, card readers), looking a card up in a directory, more than one device at a time, more than one sign-in in flight, any authentication of the device's calls to the server, persistence across restart, and delivery of a document that is not reachable by a plain unauthenticated URL.

Notable detail: the OXPd2 **PrintJob service is not what prints**. The library's PrintJob surface is only Capabilities and PrintJobAgents (`OXPd2/SDK/README_Beta_10.txt:154-156`); the manifest declares a print job agent, and printing itself goes through the device's standard IPP service.

### 4.3 simpleScan: the pattern for scan to cloud

1. The panel page calls the server, `POST /simpleScan/api/scanJob/defaultScanJob` (`SDK/demos/simpleScan/dotnet/SimpleScan/Controllers/ScanJobController.cs:30-34`).
2. The server reads the device's default options with the solution token: `ScanJobServiceClient.DefaultOptions.GetAsync` (`.../Services/ScanJobService.cs:87-99`).
3. It builds a scan ticket: scan options copied from the defaults for the HTTP destination, a destination of type **Http** whose host is the expression `$SOLUTION_CONTEXT(HOST)$`, path `/simpleScan/api/scanJobAgent/scanJobReceiver`, scheme `https`, plus optional **metadata** (a file name, content type and literal content the device sends along) and a base file name (`ScanJobService.cs:147-208`).
4. It creates the job under the scan job agent declared in the manifest, with the **UI context token**: `ScanJobAgents[agentId].ScanJobs.CreateAsync` (`ScanJobService.cs:121-133, 210`). A scan can therefore only be started while a user has the solution's application open on the panel.
5. **The device pushes the image data to the server** as HTTP POSTs to the receiver endpoint. A request is either plain JSON (a state message) or multipart with a JSON part named `content` and file parts named `scanFile` or `metadata` (`.../Controllers/ScanJobAgentController.cs:52-110`). The JSON carries the scan job id and a `TransmittingState` (`ScanJobAgentController.cs:118`, `.../Services/ScanJobAgentService.cs:64`).
6. The demo buffers each file part in memory and writes it to `./ScanFiles/<scanJobId>/<fileName>` under the process working directory, or `./ScanFiles/unknownId/` (`ScanJobAgentController.cs:112-135`). The file name comes from the request and is used unchecked.
7. Job status arrives separately as notifications to `.../scanJobAgent/scanJobNotification`; the demo uses them to disable the panel's Start button while a job is active and re-enable it on success, partial success, failure or cancel, by modifying the application's runtime chrome with the UI context token (`ScanJobAgentService.cs:48-59, 67-91`).

Not established from this lane: whether a multi-page scan arrives as one request or several, size limits, and the list of file formats (these are in the scanJob specification, another lane). Beta 10 adds a second destination type, Job Storage (4.4).

Known issue: in the JavaScript simpleScan demo, reading "Scan Job Receiver information" returns an empty array on physical devices (`OXPd2/SDK/README_Beta_10.txt:55`). Nothing in the JS files searched explains it.

### 4.4 storedJob: scan to the device's job storage and release from it (not print from cloud)

The lane brief treated storedJob as the print-from-cloud pattern. It is not: it stores a **scan** on the device and later releases it as a **copy**. Print from cloud is the IPP Print-URI flow in 4.2.

- Create: a scan job whose destination is `JobStorage` with a generated job name and a password type of none or alphanumeric PIN plus the PIN (`SDK/demos/storedJob/dotnet/StoredJob/Services/StoredJobService.cs:127-164`), created under the scan job agent with the UI context token (`:77-92`).
- List: `CopyServiceClient.CopyAgents[copyAgentId].StoredJobs.GetAsync(token, "includeMembers=true")` with the admin or solution token (`:105-119`).
- Release (print): `CopyAgents[id].StoredJobs[jobId].Release.ExecuteAsync(uiContextToken, { JobPassword, CopyOptions })` (`:210-230`). Remove: `...StoredJobs[jobId].Remove.ExecuteAsync` with the password (`:179-198`).
- The panel page lists jobs with a lock icon for protected ones and asks for the PIN (`.../WebContent/StoredJob.html:275-278, 482-496`); the demo passes the PIN to its own server in the URL query string (`:373, 514`, `.../Controllers/StoredJobController.cs:35-49`).

Nothing in the code read ties a stored job to a signed-in user; the only protection shown is the per-job PIN.

### 4.5 simpleCopy

Reads default copy options with the solution token and creates a copy job under the copy agent with the UI context token (`SDK/demos/simpleCopy/dotnet/SimpleCopy/Services/CopyService.cs:75-87, 109-121, 129-143`). Same shape as scan without a destination.

### 4.6 kioskAndBrowser: the panel UI model

- **The panel UI is a web page in the printer's embedded browser, served by the solution server.** The application target path in this demo is a static page on the server, `/kioskAndBrowser/deviceWebApp/index.html` (kiosk manifest context key `APPLICATION_AGENT_PATH`), served from `common/view/deviceWebApp/dist` (`SDK/demos/kioskAndBrowser/dotnet/KioskAndBrowser/Startup.cs:78, 99-103`). Pages are not stored in the bundle.
- **Application categories.** pullPrintAuth registers `acStandardWalkup`; this demo registers `acKiosk` (manifests, `applicationService.applications[0].details.category`). Beta 10 added kiosk-specific chrome values and a HomeScreen API to read and modify the device home screen (`OXPd2/SDK/README_Beta_10.txt:20-21`). What kiosk mode changes for the user was not read here (guides, another lane).
- **Chrome.** The manifest sets the frame around the page per application: header title, header and footer colours, footer visibility, Home button, Start button visible and enabled, soft keyboard availability, each either explicit, bound to a context key or left to the device default (`applicationService.applications[0].webApplicationChrome.*`). The same values can be changed at run time (4.3 step 7; `SDK/demos/kioskAndBrowser/common/view/deviceWebApp/dist/application/application.js:44-86`).
- **What the device browser gives the page.** The page reads `window.oxpd2.uiContextToken` (`.../application/application.js:23`): the browser injects an `oxpd2` object carrying the UI context token. The page then calls the **device's own REST services directly from JavaScript at `localhost`**, using the SDK's JS library files loaded as scripts (`.../common/js/deviceProxy.js:5, 31, 50-65`), caching the discovery tree in `localStorage` (`:163-175`). This requires the security agent's CORS switch: this demo sets `securityService.securityAgent.corsEnabled = True`, pullPrintAuth sets it `False`.
- So there are **two UI architectures**: page calls server, server calls device (pullPrintAuth, simpleScan); or page calls device directly (kiosk demo). The second removes a round trip but puts tokens and device calls in page script.
- The page can reset the inactivity timer (`application.js:29`) and read the start intent it was launched with (`:88-90`); the manifest can bind a default start intent (`DEFAULT_START_INTENT` context key).
- The demo server also exposes helpers to create and "tap" **simulated HID devices** through the SdkSupport service, for testing card flows without a reader (`SDK/demos/kioskAndBrowser/dotnet/KioskAndBrowser/Controllers/SdkSupportController.cs:33-45`).
- The kiosk security agent declares a longer operator list, which shows what user attributes a solution can receive: `DISPLAY_NAME`, `EMAIL_ADDRESS`, `EXCHANGE_MAILBOX`, `FQ_USER_NAME`, `HOME_FOLDER`, `LDAP_BIND_USER`, `USER_NAME`, `USER_DOMAIN`, `USER_PRINCIPAL`, `AUTH_TYPE`, `AUTH_AGENT_ID`, `SAM_ACCOUNT`, `SID` (kiosk manifest `securityService.securityAgent.declaredExpressionOperators[0..12]`). A password is not among them, as HP confirmed (`SF/2024-04-18-28551130456595:59-60`).
- HP offers **no UI library** for OXPd2 pages (`SF/2024-11-05-35098104536211:20`). The demo's device pages use Bootstrap 5.3.3 (file listing).
- The soft keyboard does not behave as documented in Beta 10: see 4.11.

### 4.7 Language matrix and what it implies

Full table: `OXPd2/SDK/README_Beta_10.txt:112-198`. Condensed (first beta in which each API was supported):

| Service | C# | Java | JS | Not supported in any language |
|---|---|---|---|---|
| Application | Beta 1 (StartIntent Beta 3, MessageCenter Beta 3, Homescreen Beta 10) | Beta 4 (5, 5, 10) | Beta 5 (6, 6, 10) | ResultIntent; MessageCenter Prompt |
| Authentication | Beta 2 | Beta 5 | Beta 6 | |
| Copy | Beta 6 | Beta 6 | Beta 6 | StoredCopyJobs (but see 6.1) |
| Device | Beta 2 (Email, Scan Beta 4; DeploymentInformation Beta 8) | Beta 4 (8) | Beta 6 (8) | |
| Device Usage, Supplies | Beta 7 | Beta 7 | Beta 7 | |
| JobStatistics | Beta 9 | Beta 9 | Beta 9 | |
| PrintJob (Capabilities, Agents only) | Beta 1 | Beta 4 | Beta 5 | |
| ScanJob | Beta 4 (ScanJobs Beta 5) | Beta 5 | Beta 6 | |
| SDKSupport | Beta 7-8 | Beta 7-8 | Beta 7-8 | |
| Security | Beta 4 | Beta 5 | Beta 6 | |
| SolutionDiagnostics | Beta 5 | Beta 5 | Beta 6 | |
| SolutionManager | Beta 1 (CertificateAuthorities Beta 2, Configurations Beta 3, RuntimeRegistrations Beta 9) | Beta 4 (5, 5, 9) | Beta 5 (6, 6, 9) | Installer Modifications; Solutions Certificates |
| USB Accessories | Beta 3 | Beta 5 | Beta 6 | Generic accessories; OpenAccessory (only HID and OpenHidAccessory work) |
| userPolicy, webHook | no client | no client | no client | specifications only (3.2) |

Implications:

- All three libraries are at the same level now; the gaps are identical. Language is not a capability decision.
- C# has been HP's lead language for every service and the .NET demos are the fullest set (the only place `StoredJobs` release was read working). The .NET library is netstandard2.0, loadable from the existing .NET services. Java is an equally complete second choice (Spring Boot 3.2.2 demos), relevant only if code from the Kotlin/Java apps were to be reused, but those are Android/Workpath UI apps whose device-facing code does not carry over (inferred).
- HP "tests and commits to supporting the signed libraries" and has no position on generated clients; a partner generating Go clients found the bundled OpenAPI files had broken references between specs (`SF/2022-10-10-10257827011987:67, 81-89`). Use HP's library rather than a generated client.
- Card readers: only HID is supported through the library. A reader that is not a HID keyboard-type device has no supported path.

### 4.8 Demo ports and host requirements

- Ports: 5000 (examples), 5050, 5150, 5250, 5450, 5550, 5650 (`OXPd2/SDK/README_Beta_10.txt:76-83`). Java and JS use the same numbers (`SDK/demos/pullPrintAuth/java/src/main/resources/application.properties:1`, `SDK/demos/pullPrintAuth/js/src/app.js:15`).
- The .NET example must be started as the self-hosted `OXPd2ExamplesHost` profile, not IIS Express; partners hit this in 2021 and again in 2025 (`SF/2021-12-01-4411689754003:26-36`, `SF/2025-06-06-41945943531283:36`). The launch settings carry both profiles: `http://localhost:49281` and `http://localhost:5000` (`SDK/examples/dotnet/OXPd2ExamplesHost/Properties/launchSettings.json:6, 21`).
- The device must reach the server over HTTPS on that port, by a name or IP address that matches the server certificate (script arguments, 4.1). The server must reach the device over HTTPS. A device simulator on Wi-Fi does not work reliably (4.11).
- Without Visual Studio: `dotnet run` in the project folder (`SF/2022-05-03-5961525346195:45`).
- Packaging needs Windows with WSL **version 1** and Ubuntu 22.04, or Linux (`SDK/tools/spu/spu-cli/net8.0/Release/README.md:8`). The readme mentions macOS only to say OpenSSL may need installing; no macOS executable ships.

### 4.9 The Solution Packaging Utility and bundle signing

The CLI's actions (`SDK/tools/spu/spu-cli/net8.0/Release/README.md:21-45`): `squashfs`, `verity`, `tar`, `signtar`, `signbdl`, `fimpak`, `fimbdl`, `fimdump`, `batch`, `zip` (deprecated), `validate`, `version`, `help`.

The build chain, as the batch example shows (`:79`): make a SquashFS image of the solution assets, compute DM-Verity hashes (the firmware uses them to protect the read-only image, `:137`), tar and gzip, sign the tarball with the **developer's own RSA private key** (`:93-97, 157`), wrap in a FIM package (`.pak`), then a FIM bundle (`.bdl`). The bundle type is one of `unverified`, `restricted`, `unrestricted` (`:173-176`). `signbdl` makes a detached signature of the bundle with the developer key (`:210-215`). `validate` checks a manifest (`:202-207`). `fimdump` prints a bundle's header, which is how partners check the type (`SF/2026-11-06-57213300079635:63-94`).

Bundle types in practice:

| Type | How it is made | Where it installs | Source |
|---|---|---|---|
| UnverifiedAftermarketSolution | normal build in the SPU | only on a device in LDB mode; otherwise `bundleTypeUnsupported` | `SF/2026-11-06-57213300079635:160, 194` |
| UnrestrictedAftermarketSolution | "Build Production Solution Bundle" (Build menu, Ctrl-B) in the SPU, then submitted to HP App Center for "VNV" signing | meant to install without LDB once HP has signed it | `OXPd2/Knowledge-Base/General--53055539144339-OXPd-2-Production-Bundle-Creation.md:10-24`; `SF/2026-11-06-57213300079635:226, 273` |
| Restricted | named by the CLI and by a partner; no description found in this lane | unknown | `README.md:175` |

The knowledge-base article (updated 1 July 2026) is the whole of HP's written production guidance in this lane: a bundle must declare whether it is production or development, and a production bundle must be submitted for final signing (`...Production-Bundle-Creation.md:10, 24`).

### 4.10 `LICENSE.txt`: what it is and is not

`SDK/LICENSE.txt` (1,376 lines) is a list of **third-party open-source notices** for npm packages (React 17, Material-UI 4, JSS, react-hook-form and others) and NuGet packages (Avalonia 11.3.2, Microsoft.Extensions.* 9.0.7, Newtonsoft.Json 13.0.3, ReactiveUI.Validation, Serilog, Superpower), each with its MIT, BSD or Apache 2.0 text. A search of the whole file for "HP Inc", "Hewlett", "HP Development", "beta" and "pre-release" returned zero hits (positive control: "MIT License" appears many times in the same file).

So the SDK package contains **no statement of what a partner may or may not do**: nothing on redistribution of the libraries with a product, beta terms, confidentiality or production use. Those terms must be in the click-through agreement on the HP developer portal and the partner agreement, which are outside this lane. The only related statements found: the library `README.md` says beta firmware and SDKs must not be redistributed to customers (`README.md`, intro paragraph, written by whoever assembled the library, not by HP), the demo sources are marked "All rights reserved" by HP (`PPA/Program.cs:2-3`), and the JS library declares itself `private` with an empty licence field (3.2).

### 4.11 Known issues, beta limitations and everything partners hit

**Release notes, known issues** (`OXPd2/SDK/README_Beta_10.txt:52-56`):

1. IPP does not print `.txt` files.
2. SPU: packages from Beta 2 or earlier do not migrate.
3. JS simpleScan returns an empty array for Scan Job Receiver information on physical devices.
4. Installing a Beta 9 bundle on Beta 10 firmware causes a hang.

Also in Beta 10: the USB registration record type changed (`usbAccessoriesRegistrationRecord` deprecated in favour of `usbAccessoriesAgentRegistrationRecord`, `:16`), so manifests from Beta 9 need rebuilding.

**Forum, by topic.** "HP" means a reply from an HP support or engineering author; dates are the reply dates. Zendesk hides author names from partner accounts, so only sign-off first names are visible.

| Topic | Problem | HP's answer and date | Source |
|---|---|---|---|
| Bundle signing | Development bundle rejected on a non-LDB device: `bundleTypeUnsupported` | Build a production bundle per the KB article; signed, it installs without LDB (6 Nov 2026) | `SF/2026-11-06-57213300079635:160, 220-226` |
| Bundle signing | Production bundle, signed through App Center V&V, still rejected with `bundleVerificationFailed`; the simulator log says no certificate was found in or after the signature block; the returned file differs from the submission only by a 538-byte fingerprint block | A bundle must be HP-signed via App Center and be of the unrestricted type; there is no tool to validate a signature, the only test is an install on a non-LDB device (6 Nov). HP has asked the signing team whether their service matches the current SDK (9 Nov). Still waiting (17 Nov 2026). **Unresolved.** | `:237-246, 273, 301-350, 361, 378` |
| LDB | Sign-in to enable LDB fails on an E87760 after moving to Beta 10 firmware | Not a known regression. LDB sign-in authenticates against an HP cloud endpoint (`jamanagement.api.hp.com`, same on FS5 and FS6); device admin sign-in comes first; check the proxy settings survived the firmware upgrade, since HP's FS5-to-FS6 settings migration is still being worked on; device logs are downloadable from the device's support tools page (6 Nov 2026). LDB is for development and demos only, not customer production (17 Nov 2026). Open. | `SF/2026-11-06-57213365367443:60-71, 110` |
| LDB | On an M430 with firmware 6.38.0.952, LDB could be enabled and disabled once; re-enabling causes a ten-minute restart and LDB stays off | No reply yet (posted 13 Nov 2026) | `SF/2026-11-13-57508706489107:10-20` |
| LDB | How LDB is enabled | Partner's description: at the physical panel, Settings, Developer Options, LaserJet Debug Bridge, sign in with the HP developer user name and an "LDB Service Key" created on the OXPd2 developer site; cannot be done remotely | `SF/2026-11-06-57213365367443:10, 20-22` |
| SPU | Bundle creation fails on Windows Server 2022 | WSL must be installed with Ubuntu 22.04; more importantly, to use the SPU **and the simulator on the same machine, WSL 1 is required**, because the simulator needs nested virtualization and Hyper-V allows only one user of it; this is a boot-time setting. HP suggested a second machine (5-17 Nov 2026). Open. | `SF/2026-11-02-57068486488979:26, 68-72, 105-115` |
| Firmware mismatch | A Beta 9 project rebuilt with Beta 10 fails to deploy on Beta 10 firmware ("addition of shortcut failed") for bundles that have an application | No HP reply; the partner fixed it with "reset all settings" on the device (a "5800") (1 May 2026) | `SF/2026-05-01-51327889667603:8-16, 40` |
| Firmware mismatch | Beta 9 bundle on Beta 10 firmware hangs the device | Release-note known issue | `OXPd2/SDK/README_Beta_10.txt:56` |
| Simulator | HPExtSim_6.38.0.793: "failed to retrieve IP address" timeout | See the "Failed to Retrieve IP" section of the simulator guide: shut down, delete `largeMacAddress` or `smallMacAddress` in the simulator's home directory, relaunch to get a new MAC address; give the VM more memory (20 Oct). Use a **wired** network: Wi-Fi adapters may not support multiple MAC addresses. Nested virtualization is required; on a Windows host Hyper-V must be disabled; the simulator cannot run inside a Hyper-V VM (21 Oct 2026). The partner got it working on a wired desktop. | `SF/2026-10-14-56425179192467:28, 79-101, 144-152, 164` |
| Simulator | After that, binding from the example host throws a JavaScript TypeError | Follow the order bind, then admin token (22 Oct); closed for inactivity 17 Nov 2026. Unresolved. | `:166, 191-203, 270-275` |
| Simulator | Same IP timeout on the 6.23 simulator in 2024; the older 6.19 image worked on the same machines | "Restart the simulator" (22 May 2024); closed without resolution | `SF/2024-05-20-29542361934483:14, 39` |
| Simulator | 6.23 image fails to start | Check network setup and VMware version; it then worked (Apr 2024) | `SF/2024-04-02-28021565712403:26, 39` |
| Simulator | Two simulators on one VM | Possible (small and large display) but both get the **same IP address**; different addresses are not possible; the simulator is a beta product (11 and 19 Jul 2023) | `SF/2023-05-11-16562279976979:18, 36` |
| Simulator | Admin PIN | A default exists and is documented in the Examples User Guide (18 Aug 2023) | `SF/2023-08-10-19405959459091:24-25` |
| Simulator | Reboot required after uninstalling a bundle with an `en-AU` language tag | Not reproducible on later simulators; a bundle is not expected to carry more than one I18N file (20 May 2022) | `SF/2021-12-17-4412940731539:49, 109` |
| Simulator | Where its logs are | Inside the VM under the simulator's `simtmp` directory, one `byproducts...` folder per session (17 Dec 2021) | `:28-38` |
| Simulator | Discovery tree retrieval loops | Example host was started under IIS, wrong port (12 Jun 2025). The partner's own IIS-hosted, plain-http client still hung; no further answer | `SF/2025-06-06-41945943531283:36, 51` |
| Card readers | A keyboard-emulating reader (vendor 0C27, product 3BFA) delivers base64 reports instead of the card number | The reader is supported. The solution must translate the HID reports itself: each report is an 8-byte keyboard report, key-down then key-up, with HID usage codes (0x1E is "1", 0x27 is "0", 0x28 is Enter) (2 Dec 2024) | `SF/2024-11-22-35687409372307:8, 87-110` |
| Certificates | Is there an equivalent of OXPd 1.x certificate management | Certificates go through the Solution Manager's Certificate Authorities resource and are visible only to that solution (6 Nov 2026); usable with runtime registrations, after the bundle is installed (12 Nov 2026) | `SF/2026-11-04-57156007627539:41, 78` |
| Buttons | Can home-screen buttons be registered and removed at run time as in OXPd 1.x | No: applications are declared in the manifest (2 Aug 2023). Run-time registration was promised for early 2024, postponed to 2025 (24 Jul 2024), and arrived in Beta 9 as Runtime Registrations. In the example it appears as a tab only when the installed solution declares a RuntimeRegistrationAgent (10 Dec 2025, 8 Jan 2026) | `SF/2022-05-23-6425667425555:60-62, 73, 164`; `SF/2025-12-03-47069605641747:28-29, 69` |
| Buttons | How many | No published limit; up to 20 was "being tested" (24 May 2024) | `SF/2024-04-18-28551130456595:51, 111` |
| Panel UI | No Help icon in the chrome | No plans; use a button of your own (24 May 2024) | `:113` |
| Panel UI | Soft keyboard: `textbox-mode="pin"` with `type="password"` shows a full QWERTY keyboard, not a numeric masked pad; `hex` and `fax` modes also wrong. Seen on the 6.38.0.793 simulator and an M430 on 6.38.0.952 | No reply (posted 30 Oct 2026) | `SF/2026-10-30-56990393792275:62-78, 100` |
| Panel UI | UI library | None exists (6 Nov 2024) | `SF/2024-11-05-35098104536211:20` |
| Device info | Device location | To be added in a future SDK (24 May 2024) | `SF/2024-04-18-28551130456595:115` |
| Device control | Reboot from the solution | Not available, no plans; the partner keeps using SNMP (24 May 2024) | `:117, 147` |
| Security | User password through the security macros | Not available (30 Apr 2024) | `:59-60` |
| Cloud | Microsoft sign-in and SharePoint | "Should be possible" with all Microsoft URLs in trusted sites, with a warning that session-data clearing may be incomplete (29 Jun 2023). Then: direct integration with public cloud services is not supported with OXPd; use Workpath (25 Jul and 14 Aug 2023) | `SF/2023-06-15-17607595895827:25-31, 98-100, 160` |
| High availability | Primary and secondary server on the device | HP firmware has never provided load balancing on the device; write it yourself in Workpath (4 May 2026) | `SF/2026-04-07-50604474194323:18` |
| Tooling | Postman password grant returns 405 | Use `https://` (1 Dec 2021) | `SF/2021-12-01-4411689387027:26` |
| Demo | pullPrintAuth sign-in shows "invalid sign in" before any prompt | Never diagnosed; closed for inactivity (2022) | `SF/2022-05-19-6339642208403:12, 62, 106-116` |
| OXPd 1.x | "Invalid uiContextId" when registering many buttons | An OXPd 1.8.2 thread filed in the OXPd2 forum; cured by lengthening a session value in the reserve-UI page (Nov 2022). Not an OXPd2 matter | `SF/2022-07-26-8111875577491:174, 548, 744, 757` |

**HP statements on the points the lane asked about:**

- *Production release timing.* None. The direct question, posted 6 Feb 2024, has no reply (`SF/2024-02-06-26006457726483:10, 17`). The portal's platform table lists firmware 6.3 through 6.34 (Beta 1 to 9), every row "pre-release" and "Not Supported" for VAV, and does not yet list Beta 10 (`OXPd2/Docs/platform-versions.md`). In the field in late 2026 the firmware files are named "FS6-Pilot" (`SF/2026-10-30-56990393792275:42-45`).
- *Supported device models.* Not defined: "The Model Numbers supported will be defined prior to production release" (`OXPd2/Docs/compatible-devices.md`). Models partners have actually run Beta 10 firmware on: HP Color LaserJet Flow E87760 and HP LaserJet MFP M430 at 6.38.0.952-202607142004, a "5800", and the simulator, which reports itself as an HP Color LaserJet Flow X87840 at 6.38.0.793 (`SF/2026-11-06-57213300079635:38-48`, `SF/2026-05-01-51327889667603:40`).
- *Generations.* HP equates FutureSmart 6 with OXPd 2 and FutureSmart 5 with OXPd 1 (`SF/2026-11-06-57213365367443:62`). A device moves from one to the other by firmware upgrade, and settings migration is unfinished (`:64`).
- *OXPd 1.x coexistence.* No statement in this lane on whether FutureSmart 6 firmware still serves OXPd 1.x solutions. The only contrasts drawn are functional (run-time buttons, certificate management, installation instead of configuration: `OXPd2/Knowledge-Base/...Production-Bundle-Creation.md:10`).
- *Simulator.* A beta product (`SF/2023-05-11-16562279976979:36`); requirements as in the table.
- *Limited-access features.* No forum statement. The userPolicy service being at alpha with no client library (3.2) and the library note that the "Limited Access" portal section returned 403 for Kam's account (`README.md`, "Not collected") suggest userPolicy is one of them (inferred).
- *On-premises servers.* No statement either way. Every example assumes a server the device reaches directly by address. The load-balancing thread came from a customer deploying in the cloud; HP did not object to that, only to device-side failover (`SF/2026-04-07-50604474194323:8, 18`).

### 4.12 How we would stand up a development environment

What is needed:

1. **A target device.** Either the simulator `HPExtSim_6.38.0.793.ova` or a physical device on FutureSmart 6 firmware at or above 6.38.0.793 with LDB enabled.
2. **A host for the simulator**: an x86-64 PC with VMware, nested virtualization available (Hyper-V off on Windows), a **wired** network, generous memory. One simulator per VM if distinct IP addresses are needed.
3. **A build machine for the SPU**: Windows with WSL 1 and Ubuntu 22.04, or Linux x86-64, with the .NET 8 runtime. If it is the same Windows machine as the simulator host, WSL must be version 1.
4. **A development server machine** reachable from the device by a fixed name or IP: .NET 8 SDK, the SDK's `OXPd2Lib.dll`, a server certificate issued from the SDK's development root CA for that name and IP, and the Kestrel HTTPS endpoint configured.
5. **An RSA key pair of our own** for `signtar` and `signbdl`.
6. **The SDK documentation**, already extracted to `OXPd2/Docs/SDK-Documentation/`, and Postman with the two collections for poking the device.
7. **A USB HID card reader** of the models customers use, or the SdkSupport simulated HID for early work.
8. **For a physical device**: an HP developer account with an LDB Service Key, device administrator credentials, outbound internet from the device to HP's LDB authentication endpoint (through the customer proxy if any).

What is missing today:

- **The simulator image is not in the library** (`OXPd2/Simulator/` is empty; `START-HERE.md` "Outstanding action").
- **The HP Extensibility Simulator Guide PDF** (403 for Kam's account, `README.md` "Not collected"); HP's troubleshooting answers point to it.
- **A suitable machine.** This workstation is a Mac. The SPU ships no macOS build, and the simulator is an x86 Linux VM needing nested virtualization (the simulator log path contains `linux-x86_32`, `SF/2021-12-17-4412940731539:28`). On an Apple-silicon Mac neither is expected to work (inferred, not tested). An x86-64 Windows or Linux PC is needed.
- **A physical OXPd2-capable device with pilot firmware**, and knowledge of how Datasec obtains that firmware.
- **Access to HP App Center V&V** and a working signing result (4.11).
- **The partner licence terms** for the SDK (4.10).

First milestone I would set: on the simulator, install the unmodified pullPrintAuth bundle against the .NET demo on a wired x86 PC and complete one card sign-in with a simulated HID. That exercises every moving part (certificates, install, authorisation code, USB callback, authentication agent, application page) before any Datasec code exists.

### 4.13 Risks of building on a beta

| Risk | Evidence | Consequence |
|---|---|---|
| No production path yet | signing rejection unresolved as of 17 Nov 2026; LDB excluded from production | nothing built can reach a customer until HP fixes signing and declares a release |
| No date, no model list | 4.11 statements | the mixed-fleet promise cannot be scheduled or scoped by model |
| Breaking changes between betas | Beta 9 bundle hangs Beta 10 firmware; USB record type replaced; Beta 2 packages do not migrate | every HP release needs a rebuild, a retest and a controlled device firmware match; a customer-side mismatch can hang a printer |
| Features arrive years late or not at all | run-time buttons: asked May 2022, delivered Beta 9 (Sept 2025); device location promised May 2024; reboot and Help icon refused | do not design around anything not in Beta 10 today |
| Documentation ahead of firmware | soft keyboard modes | PIN entry and similar details must be tested on real firmware, not taken from the guide |
| Unsupported APIs in every library | ResultIntent, MessageCenter Prompt, Certificates, generic USB | design within the supported subset |
| userPolicy at alpha with no client | 3.2 | per-user permission control on the device is not buildable from this SDK |
| Thin support | several threads closed for inactivity without a fix; replies take days to weeks; one engineer answers most technical questions | plan for self-diagnosis; raise blockers early |
| Fragile tooling | simulator networking, WSL 1 constraint, single IP per VM | setup cost; multi-device testing needs several VMs or real devices |
| HP's stance on cloud integration | 2023 statement | commercial and support risk even if technically feasible |
| Demo code quality | 5.3 | none of it is reusable as is |
| Licence terms not in hand | 4.10 | redistribution of `OXPd2Lib.dll` inside a Datasec installer is unconfirmed |

---

## 5. What this means for the port

### 5.1 Requirements that follow

1. **A server product, in C# on .NET 8**, exposing the agent endpoints of 4.1 over HTTPS and calling devices through `OXPd2Lib` (4.7). It replaces the on-device Workpath apps; the panel shows only its web pages.
2. **A device registry with per-device state**: address, discovery tree, solution token and refresh token (encrypted at rest), last-seen, firmware version. The demos' single "current device" singleton must be replaced by a lookup keyed on the device identity the calls carry (`oxpd-device-address`, `oxpd-solution-id` headers, plus the session tokens) (4.1, 4.2).
3. **An installer and enrolment flow**: admin credentials per device are needed once to install and to receive the authorisation code; they should not be stored afterwards (4.1).
4. **The sign-in hub maps onto the authentication agent plus USB accessories agent** exactly as pullPrintAuth shows: card read to pre-prompt result with user attributes, or a prompt page for the Microsoft sign-in or QR code, then auto-launch (4.2). The existing Entra logic (card to user lookup, token redemption, QR via SignalR) moves to the server.
5. **A HID report decoder** for keyboard-emulating readers, per reader model, and a manifest entry (vendor id, product id) for every supported reader. Adding a reader model means a new bundle and a new HP signing round (4.2 A, 4.11).
6. **Token sharing between the apps becomes trivial**: all apps are pages of the same server, which holds the user's Microsoft tokens; the device only carries the identity (4.2 E).
7. **Scan to OneDrive, SharePoint, Mailflow, Teams**: the device posts the scan to the server, which uploads through Graph (4.3). The server needs streaming receipt (not the demo's in-memory copy), temporary storage, and clean-up.
8. **Print from cloud and Universal Print release**: the server fetches the document, exposes it at a short-lived URL the device can reach, and sends IPP Print-URI (4.2 G). The device must be able to reach that URL and trust its certificate; formats are limited to what the device's IPP accepts (PDF and JPEG are what the demo prints; `.txt` is a known failure).
9. **Server certificate strategy per customer** and real validation of device certificates (4.1).
10. **Trusted sites**: the manifest's list must cover every origin the panel browser loads, including the Microsoft sign-in hosts if the Microsoft page is shown on the panel (4.11, cloud row). The demo default of `*` should not ship.

### 5.2 Constraints

- Scan, copy and stored-job actions need the **UI context token**, so they can only be started while the user is in the solution's application on the panel (4.3, 4.4).
- One `HOST` per installed bundle and no device-side failover: high availability must be a load balancer or DNS name in front of the server (4.11).
- The device must reach the server and, for print, the document URL. A "localised server" on the customer network fits this model directly; a cloud-hosted server needs inbound reachability from printers and outbound reachability to them, which most customer networks do not allow without a relay (inferred from the two traffic directions in 4.1).
- Home-screen buttons are fixed at install unless the solution declares a runtime registration agent (4.11).
- No password is ever available from the device's security context (4.6).

### 5.3 Reusable parts and what must not be copied

Reusable as patterns: the manifest structure and context-key parameterisation; the token handling sequence; the multipart install call; the scan receiver's multipart parsing; the IPP client classes (HP sample code, "All rights reserved": reuse needs licence clearance); the simulated-HID helper for automated tests.

Must not be carried into a product (all are weaknesses in the demos):

- TLS validation of the device disabled (`PPA/Startup.cs:59-60`).
- CORS open to any origin, method and header (`PPA/Startup.cs:42-45, 89-92`).
- No authentication on any server endpoint, including user management, document upload and the agent targets (targets declare authorisation type `None` in the manifest).
- Any non-empty card read signs in as a fixed user (`PPA/Services/UserManagementService.cs:116-126`).
- State kept in process memory and in singletons; one device, one sign-in at a time (`PPA/Services/AuthenticationAgentService.cs:30-32`).
- Uploaded and scanned file names used unchecked in file paths (`PPA/Services/DocumentManagementService.cs:152-156`; `SDK/demos/simpleScan/dotnet/SimpleScan/Controllers/ScanJobAgentController.cs:116-125`).
- Documents served to the printer from an open static folder (`PPA/Startup.cs:107-111`).
- A job PIN passed in a URL query string (`SDK/demos/storedJob/dotnet/StoredJob/Controllers/StoredJobController.cs:35-49`).
- Blocking `.Result` calls throughout, and a blocking sleep loop for job polling (`PPA/Services/PrintOperationsService.cs:255, 310`).
- The SDK's development root CA: its private key and the passphrase are in every copy of the SDK, so anything that trusts it trusts every SDK holder (section 8).

### 5.4 Traps

- Starting the .NET host under IIS Express (wrong port) (4.8).
- Simulator on Wi-Fi; simulator and WSL 2 on one machine (4.11).
- Mixing beta generations between SPU, bundle and firmware (4.11).
- Assuming `textbox-mode` gives a PIN pad (4.11).
- Assuming storedJob is print from cloud (4.4).
- Assuming the PrintJob service prints (4.2).
- More than one I18N file, or unusual language tags, in a bundle (4.11, 2021 thread; the fix is unconfirmed on current firmware).

---

## 6. Contradictions and doubts

1. **StoredCopyJobs.** The language matrix marks it unsupported in all three languages (`OXPd2/SDK/README_Beta_10.txt:139`), yet the release notes announce stored-job APIs for Copy (`:17`) and the .NET storedJob demo calls `CopyAgents[..].StoredJobs` list, release and remove through the library (`SDK/demos/storedJob/dotnet/StoredJob/Services/StoredJobService.cs:119, 198, 230`). The code is the truth; the matrix row looks stale.
2. **Cloud integration.** HP said Microsoft authentication "should be possible" and, weeks later in the same thread, that public cloud integration is not supported with OXPd (4.11). Unreconciled.
3. **Port in a forum answer.** HP wrote that "the examples are operating on port 5050" (`SF/2025-06-06-41945943531283:36`); the release notes and launch settings say the example host is 5000 and 5050 is the pull print demo.
4. **Printer URI scheme.** The IPP requests state the printer URI as `http://` while the transport is `https://` (`PPA/Ipp/IppClient.cs` about line 130 against line 262). Harmless in the demo; not to be copied blindly.
5. **Header typo in the manifest.** One header value in the pullPrintAuth manifest has a stray explicit value `$SEVICE` beside the correct expression `$DEVICE(IPV4_ADDRESS)$` (`solutionManager.notificationAgents[0].target.targetHeaders[1]`). The expression is the one in effect (binding type is Expression).
6. **Bundle signing semantics.** The SPU readme describes signing with a developer key; HP's forum answers say only HP's signature makes a bundle installable without LDB; the partner's HP-signed file was still rejected. How developer and HP signatures relate is not explained anywhere in this lane.
7. **Manifest versus JS library naming.** The JS library has no licence and is `private`; whether its per-service files may be served to the printer browser from our server in production (as the kiosk demo does) is a licence question, not a technical one.
8. **"Limited access".** The library readme mentions a portal section Kam's account cannot open. Nothing in the SDK says which features are limited.
9. **Stale portal table.** `OXPd2/Docs/platform-versions.md` stops at Beta 9.
10. **My own coverage.** Statements about Java and JavaScript rest on searches and file listings, not on reading the source. The example host was not read: anything it shows beyond the demos (message center, homescreen, runtime registrations, configuration, diagnostics) is not covered here.

---

## 7. Questions for Kam or his team

1. **Has Datasec been through HP App Center "VNV" signing for OXPd2, or does it have an HP contact who can say when signed bundles will install on Beta 10 firmware?** Why: without it nothing reaches a customer (4.11). If unanswered I assume development proceeds on simulator and LDB devices only, with production blocked on HP.
2. **Has HP told Datasec that an OXPd2 solution may integrate with Microsoft 365, given the 2023 forum statement that OXPd does not support public cloud integration?** Why: it is the whole product. If unanswered I assume it is allowed because the server, not the device, calls Microsoft, and I list it as a top risk to confirm with HP.
3. **What hardware is available: an x86-64 Windows or Linux PC with wired network for the simulator and SPU, and a physical FutureSmart 6 pilot device (which model)?** Why: the Mac cannot host either (inferred). If unanswered I assume a Windows 11 x86-64 PC must be provided, and that no physical device exists yet.
4. **What do the HP agreements Datasec accepted say about shipping `OXPd2Lib.dll` inside a product and about beta confidentiality?** Why: the SDK contains no such terms (4.10). If unanswered I assume the library may be redistributed with the server once HP releases a production SDK, and not before.
5. **Which card reader models must be supported at launch (USB vendor and product ids), and are any not HID keyboard-type?** Why: each must be listed in the signed manifest and decoded by our code; only HID works (4.2, 4.7). If unanswered I assume the six models of the earlier OXPd 1.x attempt.
6. **Where will the server run: one per customer site on the printer network, or a shared cloud service?** Why: printers must reach it and it must reach printers (5.2). If unanswered I assume one on-premises server per customer network, as Kam's brief says.
7. **Does HP's FutureSmart 6 firmware still run OXPd 1.x solutions?** Why: it decides whether "OXPd 1 and OXPd 2" means two fleets split by firmware generation or two interfaces on the same device. This lane has no answer. If unanswered I assume a split by firmware generation (FS5 runs OXPd 1.x, FS6 runs OXPd2).
8. **Is PIN entry on the panel part of the product?** Why: the numeric masked keyboard is broken in Beta 10 (4.11). If unanswered I assume an on-page HTML keypad is built instead of relying on the native keyboard.

---

## 8. Secrets and sensitive items seen (locations only)

| Item | Location | Note |
|---|---|---|
| Private key of the SDK's development root CA (RSA, encrypted) | `OXPd2/SDK/OXPd2-SDK-Beta-10/tools/certificates/ExtSDKRootCA.key` | shipped to every partner |
| Passphrase for that key, and the export password for generated `.pfx` files, in plain text | `OXPd2/SDK/OXPd2-SDK-Beta-10/tools/certificates/generateHPExtSDKExample.sh:5` and `:6` | with the key, lets any SDK holder issue certificates under this CA: never trust this CA outside a lab |
| An HP employee e-mail address in the root CA subject | `OXPd2/SDK/OXPd2-SDK-Beta-10/tools/certificates/ExtSDKRootCA.pem` (certificate subject) | personal data |
| The same CA certificate embedded in demo manifests | pullPrintAuth manifest, `solutionManager.certificateAuthorities[0].certificateContent` | public certificate, not a secret; shows the demo bundle trusts the dev CA |
| Hardcoded demo user password | `OXPd2/SDK/OXPd2-SDK-Beta-10/demos/pullPrintAuth/dotnet/PullPrintAuth/Services/UserManagementService.cs:60` | demo account only |
| The same demo credentials pre-filled in the login page | `.../PullPrintAuth/WebContent/LoginPage.html:71` and `:73` | demo only |
| Demo user e-mail address | `.../Services/UserManagementService.cs:57` | fictitious |
| Simulator default administrator PIN | `OXPd2/Support-Forum/2023-08-10-19405959459091-simulator-PIN-code.md:24` | default credential of the simulator |
| A device IP address in a URL | `OXPd2/Support-Forum/2026-11-06-57213365367443-...md:66` | HP lab address |
| Another partner's solution ids, vendor name, bundle signatures and a customer name | `OXPd2/Support-Forum/2026-11-06-57213300079635-...md:30, 57-61, 103, 145`; `...57213365367443...md:93` | third-party business data; do not reuse |
| First names of forum posters and HP staff | sign-offs throughout `OXPd2/Support-Forum/` | personal data; not reproduced here |
| A partner file-share link | `OXPd2/Support-Forum/2025-06-06-41945943531283-...md:22` | external link, not followed |
| Postman environment | `OXPd2/SDK/OXPd2-SDK-Beta-10/tools/postman/OXPd2 Workspace Environment.json` | checked: variable names only, all values empty |

Security weaknesses the port must not carry over are listed in 5.3. This lane read no Datasec product code, so it has nothing to report on weaknesses in the existing Workpath suite.
