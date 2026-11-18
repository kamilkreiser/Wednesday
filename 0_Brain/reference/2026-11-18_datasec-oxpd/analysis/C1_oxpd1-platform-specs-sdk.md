# C1: OXPd 1.x platform: specifications, SDK, demos, simulator, tools

Lane C1 of the Datasec / OXPd analysis, 2026-11-18. Library root: `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`. All source paths are relative to that root. Abbreviations used in citations: `D/` = `OXPd1-NET-Java/Docs/`, `S/` = `OXPd1-NET-Java/SDK/`, `M/` = `OXPd1-NET-Java/Demos/`, `T/` = `OXPd1-NET-Java/Tools/`, `SIM/` = `OXPd1-NET-Java/Simulator/`. A citation `D/<file>.md:NN` is a line number in that file; `:NN` alone repeats the file named last in the same bullet or table.

## 1. BLUF

This lane holds HP's OXPd 1.x (.NET/Java, SOAP) platform: 30 service specifications and guides, four SDKs (latest 1.8.4.1, built June 2025), three demo sets, the OXPd Simulator 1.3 and five tools. The five facts that most shape the port:

1. **Nothing is installed on a 1.x device and nothing is signed by HP.** The solution is a server that writes registration records (sign-in agent, card reader, buttons, trusted sites, CA certificate) into each device by admin-authenticated SOAP 1.2 calls on port 7627; disk initialisation wipes them (4.1, 4.19).
2. **The server must hold every device's administrator password for run-time use**, not only at install: opening the browser remotely, home-screen messages and every registration are admin-class calls (4.2).
3. **The sign-in hub maps cleanly**: an Authentication Agent (pre-prompt for a card swipe, browser prompt page for QR or device code, post-prompt verdict) plus an owned USB HID card reader whose raw reports reach the server; the identity, including an opaque token, is posted by the device into each app button's first request through `$AUTHUSER_...$` macros (4.4, 4.6, 4.17).
4. **The panel is an old WebKit browser** (AppleWebKit 523 on legacy "Oz"/FutureSmart 3, 534+ on FutureSmart 4/5), with a 10-second JavaScript limit, no pop-ups, no downloads, screens from 160x64 to 1280x800; Microsoft sign-in pages cannot be expected to work on it (4.7, 4.13).
5. **Print release means jobs held on the server** and sent by IPP inside a "priority print" reservation keyed by the app's UI context (Print-Job or Print-URI); there is no device job-storage API. Scan is a device POST to a server receiver, and only from inside the app's browser session (4.8, 4.12).

Also decisive: the full 1.8 feature set needs FutureSmart 4.7 or later; "Pro" devices are a separate REST dialect frozen at 1.7 (4.20); TLS trust is the classic field failure (4.2).

## 2. Coverage

Method: the first agent (cut off) wrote section 4.1 to 4.20 and a draft 4.21; this second pass read that draft whole, re-checked 35 of its cited sources line by line (list at the end), read the items marked "read whole" below, and wrote sections 1 to 3 and 4.21 to 8.

| Area | Files | Read whole | Sampled (how chosen) | Not opened |
|---|---|---|---|---|
| `D/*.md` specifications and guides | 30 Markdown, 9,503 lines; 16 images | 29 of 30 cited with line numbers by the first agent (every file except the authorization-agent spec); the authorization-agent spec (100 lines) read whole in this pass. 35 cited line ranges in 20 of the files re-read in this pass. | | Images (16) not viewed |
| `D/PDF/` | 7 PDFs (OXP Device 1.6/1.7 "Pro" addenda, Pro overview and quick start, "Oz" getting started) | 0 | 0 | All 7: they cover Pro and legacy Oz devices, which this lane recommends treating as out of scope (4.20); the Pro model is taken from the Pro Overview knowledge-base article instead |
| `S/` four SDKs | 16,780 files (1.8.2.1: 4,490; 1.8.4: 2,371; 1.8.4.1: 2,372; 1.7.3.2 Pro: 7,543) | `Manifest.txt`/`Revision.txt` of all four; 1.7.3.2 release notes | 1.8.4.1: `SoapProxy.cs`, `DiscoveryTreeTranslator.cs`, the `I*Proxy.cs` interfaces, both `.csproj`, the Java `SoapProxy.java`, the Java authentication example and agent, the jar listing (`unzip -l`), the generated XML documentation (macro search); chosen as the files that carry the wire behaviour. 1.8.4 vs 1.8.4.1 compared by `diff -rq` | The other ~2,300 files of 1.8.4.1 (generated proxies, javadoc), the bulk of 1.8.2.1 and 1.7.3.2 |
| `M/` demos | 1,660 files (1.9: 605; 1.8: 605; 1.2: 447) | Release notes of 1.2; portal release note of 1.9 | Demos 1.9 `AuthnAuthz` and `PullPrint` sources (closest to the suite); file lists of 1.8 and 1.9 compared; trust-all callback search across 1.9 | ScanPreview, OneTouchScan, MoreOptions, Quota, Statistics, CopyKiosk, SendFax, RemoteControlPanel sources (described from the walkthrough only) |
| `SIM/` | 201 files + `Jedi_Simulator_SDK1.zip` (427 MB) | Simulator guide (in `D/`) | File-type inventory of Simulator 1.3; `unzip -l` of the Jedi zip | Nothing run; Jedi zip not extracted |
| `T/` tools | 2,058 files | OXPm 1.7 release notes; OPS 1.0.20 release notes (first agent); Jedi Resource Analysis release notes head; Button Manager manifest and revision | OXPm schema and example records; WJA user guide PDF (pages cited by the first agent); OXPd UI kit directory tree | All binaries (never run); OPS PDFs; Jedi RA PDF; the 1,534-file UI kit beyond its tree |
| Outside the lane, used for context | | `START-HERE.md`, `README.md`, `README-INDEX.md`, Kam's verbatim brief; BLUF and section 5 of B1, B2, B3 | Support forum: 10 threads chosen by keyword (TLS, cipher, .NET 8, HP approval, lifecycle); knowledge base: 3 articles (TLS 1.3, Pro overview, FutureSmart 4 security); `General/Release-Notes/` 3 notes found by searching for `1.8.4` | The other ~1,036 forum threads, the Pro forum |

## 3. Inventory

### 3.1 SDKs (`S/`)

| Package | Build (Revision.txt) | Files | What is inside | Notes |
|---|---|---|---|---|
| `hp-ext-XX-oxpd-1.8.4.1` (latest, extracted) | 2025-06-23, rev `73175e27` | 2,372 | `OXPdLib/DotNet` (C# source, `OXPdLib-1.8.4.dll` for .NET Framework 4.8 and `OXPdLibCore-1.8.4.dll` for net8.0, `.chm`, XML docs), `OXPdLib/Java` (`OXPdLib-1.8.4.jar` with 100 WSDL/XSD under `META-INF/wsdls/`, javadoc, helper source), `ExampleClients/{DotNet,Java}`, `ExampleAgentServices/{DotNet,Java}`, `IIS-SetupExamples.bat` | 862 `.java`, 206 `.cs`, 28 `.aspx`, 26 `.sln`. Portal release note: only change is the three-value duplex mode (`General/Release-Notes/release-note-287186.md`) |
| `hp-ext-XX-oxpd-1.8.4` | 2024-05-01, rev `6350435c` | 2,371 | Same layout | Release 1.8.4.0 (3 May 2024): OpenJDK 21, JAX-WS 4.0.1, Gradle 8.5+, .NET Framework 4.8 and .NET 8 support, simulator split out (`General/Release-Notes/release-note-228356.md`) |
| `hp-ext-XX-oxpd-1.8.2.1` | 2020-11-17, rev `b56695f0` | 4,490 | Same plus `OXPdSimulator/` (1,988 `.rqt`, 84 `.rsp`) | Previous generation; keep only for comparison |
| `OXPd1.7.3.2ProfessionalOnlybeta` | 2018-08-30, rev `a50df0bd` | 7,543 | Pro-only SDK with `Build`, `Demos`, `OXPdUI`, `OXPdSimulator`, release notes, white paper | Pro (REST) devices only; helper package renamed so it can coexist with 1.8 (4.20) |

Entry points of the SDK examples: one ASP.NET page per service (`ExampleClients/DotNet/<Service>Client/*.aspx`) installed into IIS by the batch file; Java examples are command-line programs; the four agents (Authentication, Authorization, Quota, Statistics) exist as IIS `.svc` services (.NET) and `Endpoint.publish` servers (Java) (4.17).

### 3.2 Demos (`M/`)

| Package | Build | Demos | Notes |
|---|---|---|---|
| `hp-ext-oxpd-demos-1.9` | 2024-05-01, rev `6350435c` (same as SDK 1.8.4) | AuthnAuthz, CopyKiosk, MoreOptions, OneTouchScan, OXPdRemoteControlPanel, PullPrint, Quota, ScanPreview, SendFax, Statistics | All C#/ASP.NET on .NET Framework 4.8 (148 `.cs`, 30 `.aspx`); "Demos 1.9" is a package version, not an OXPd 1.9 platform (`General/Release-Notes/release-note-228361.md`: "Updated to use the OXPd 1.8.4 SDK libraries") |
| `hp-ext-oxpd-demos-1.8` | 2020-10-19 | Same ten | Built on OXPdLib 1.8.2 |
| `OXPd_Demo_1.2` | June 2017 | AuthnAuthz, MoreOptions, OneTouchScan, OneTouchScanPro, OXPdRemoteControlPanel, PullPrint, Quota, ScanPreview, Statistics | First release separated from the SDK (`M/OXPd_Demo_1.2/OXPd_Demo_1.2/hp-ext-oxpd-demos-1.2-ReleaseNotes.txt`) |

### 3.3 Simulator and tools

| Item | Version, build | Files | Kind |
|---|---|---|---|
| `SIM/hp-ext-oxpd-simulator-1.3` | 2024-05-01 | 199 | Windows desktop program + canned responses (4.16) |
| `SIM/Jedi_Simulator_SDK1.zip` | inner SDK 2021-06-03 | zip, 427 MB | FutureSmart firmware simulator, kept zipped (4.19) |
| `T/hp-ext-release-oxpm.1.7.0.0` | 25 Feb 2015 | 38 | Web Jetadmin fleet registration schemas and examples + WJA user guide PDF |
| `T/HP_OXPd1_ButtonManager-1.1.0` | 2025-09-17 | 5 (one `.exe`, its config, `OXPdLib-1.8.4.dll`) | Windows desktop tool, undocumented |
| `T/hp-ext-oxpdui-1.4` | 2020-10-19 | 1,534 | Omni and Windjammer JS/CSS/image kit, MultiUI examples |
| `T/OXPdProServices_1.0.20` | (release notes) | 34 | Pro-only external storage server |
| `T/Jedi_ResourceAnalysis_1.2.1` | notes for 1.2.0, Sept 2014 | 442 | Device memory profiling harness |

### 3.4 Languages and packaging

C# (.NET Framework 4.8 WCF/IIS, plus a net8.0 client-only library) and Java 21 (JAX-WS 4 / Jakarta); panel side HTML/JavaScript/CSS with the OXPd UI kit (Omni `oxpdui-omni.js`; Windjammer `oxpd.js` on Prototype 1.6.0.3). There is no packaging format on 1.x: a solution is a web server plus the registration calls it makes (or XML records imported into Web Jetadmin) (4.19).

## 4. Findings

### 4.1 Architecture: where code runs and who calls whom

- OXPd is the device layer of HP's Open Extensibility Platform: one web-application solution, implemented once, executed across the fleet (D/oxpd-architectural-overview.md:17). The 1.6 release replaced the OXPd 1.4 model (one XML configuration schema that drove the panel UI) with a true web-application model: an embedded browser on the panel plus separate device web services (D/oxpd-architectural-overview.md:28-42, 59-69).
- Solution code runs OFF the device, on a server. HP's own portal page says most of the application logic runs on an external server and not within the device browser, in contrast to OXPd JavaScript (D/oxpd-net-java.md:19).
- Two directions of traffic (D/oxpd-architectural-overview.md:71-78):
  - For the user interface the DEVICE is the client and the solution is the server: the panel browser loads HTML/JS from the solution's web application.
  - For imaging and print services the SOLUTION is the client and the device hosts the services (SOAP).
  - A third direction exists for agents and callbacks: the device calls SOAP endpoints that the solution hosts (authentication agent, authorization agent, quota agent, statistics agent, accessory events, scan notifications); see 4.4 to 4.9.
- Binding: SOAP 1.2 only; SOAP 1.1 is not supported; WSDL/XSD is the contract and tool chains generate the proxies; errors are SOAP faults (D/oxpd-architectural-overview.md:193-199). Device-to-agent calls use SOAP 1.2 with the August 2004 WS-Addressing namespace (D/oxpd-authentication-agent-service-specification.md:33-52; D/oxpd-authorization-service-specification.md:82-99).
- Device service endpoint pattern: `https://{device}:7627/hp/device/webservices/OXPd/<Name>Service`; an unencrypted twin on `http://{device}:57627/...` exists only if the device administrator enabled it for troubleshooting (D/oxpd-authorization-service-specification.md:78-80; same pattern in D/oxpd-quota-service-specification.md).
- No implicit sessions: the design is stateless SOA; all correlation is passed explicitly as data (D/oxpd-architectural-overview.md:128-132). Context is carried by opaque GUID strings:
  - UI context id: created when the browser application is invoked, destroyed when it exits; sent by the browser to the solution in an HTTP header; many device calls are rejected without the currently valid id, so some device APIs cannot be called while the browser is not displayed (D/oxpd-architectural-overview.md:150-154).
  - Accessory context id (4.6), authentication context id (4.4), quota context id (4.8).
  - Server session id (the web app's own browser session) and server context id (a free-form string the solution puts in a callback registration; the device returns it on every callback, so it can carry the device address or tenant key) (D/oxpd-architectural-overview.md:162-182).
- Native modal dialogs (paper jam and the like) cover the browser; the page's JavaScript keeps running but the user cannot interact until the dialog is dismissed (D/oxpd-architectural-overview.md:120-122).
- Backward compatibility: devices keep the old OXPd:Workflow 1.4 XML model side by side with the 1.6 browser/web-service model (D/oxpd-architectural-overview.md:93-95).
- HP explicitly leaves server-side quality of service to the solution: sizing, devices per server, behaviour at the panel while the server is being updated (D/oxpd-architectural-overview.md:291-301).

### 4.2 Security model

| Topic | What the specification says | Source |
|---|---|---|
| Channel | HTTPS mandatory when the device is the server; optional when the device is the client (HP recommends always). SMB/CIFS scan delivery is not encrypted and not recommended. | D/oxpd-security-model-overview.md:17-21 |
| Device as client: server validation | The device validates the solution server's certificate against the CA certificates in its OXPd CA store AND requires the certificate Subject CN to match the URI host exactly. The spec states this precludes IP addresses. | D/oxpd-security-model-overview.md:27-29 |
| CA store | Managed by the device administrator (EWS page or OXPd:CertificateManagement). On Jedi (FutureSmart) devices the OXPd CA store "is synonymous with" the Windows machine certificate store, and an empty CA store makes every outbound HTTPS connection fail (this text predates the Linux-based FutureSmart 5 firmware; see 6). Self-signed certificates are "not recommended/supported"; HP reports incompatible self-signed certificates and warns validation may get stricter with firmware. | D/oxpd-certificate-management-service-specification.md:21-33 |
| Client certificates | Devices may be unable to answer a client-certificate request; servers should not request them. | D/oxpd-security-model-overview.md:33 |
| Device as server: identity | Whether the solution validates the device's certificate is the developer's choice; HP concedes the tools to manage device identity certificates are not readily available. | D/oxpd-security-model-overview.md:41-43 |
| Caller authentication to the device | HTTP Basic on every OXPd method. Only two users exist: `admin` (the device administrator password) and `guest` (password ignored). Missing credentials: 401; invalid: 403; guest calling an admin method: SOAP fault, HTTP 500. | D/oxpd-security-model-overview.md:61-68, 84-143 |
| Method classes | Configuration methods: admin. Runtime methods: admin (anything that decides what the walk-up user sees), or guest plus a context id (resource-consuming calls), or guest only. | D/oxpd-security-model-overview.md:145-171 |
| Context id as capability | The context id is a device-generated nonce delivered only to endpoints that an admin-authenticated configuration call registered. | D/oxpd-security-model-overview.md:159-161 |
| Device calling the solution | Endpoint registrations may carry optional network credentials that the device presents as HTTP Basic; proxy authentication (407) supported; for non-browser requests ANY 3xx redirect fails the connection; the browser follows redirects. | D/oxpd-security-model-overview.md:183-205 |
| Data at rest on device | Network credentials and metadata blobs given to OXPd services are encrypted when written to permanent storage. | D/oxpd-security-model-overview.md:207-214 |
| Walk-up user credentials to the solution | A top-level button may be configured to require sign-in, and the admin chooses which of the walk-up user's credentials are sent to the solution: once per browser invocation, in the body of the initial HTTP POST. | D/oxpd-security-model-overview.md:216-226 |
| Key sizes | The document still quotes a 1024-bit recommendation, then notes NIST deprecation and 2048-bit from 2014 (stale text). | D/oxpd-security-model-overview.md:45-51 |
| Test service | Disabled by default since minor revision 1.1; needs an admin `EnableService` call after every reboot. | D/oxpd-security-model-overview.md:175-177 |

TLS versions, ciphers and certificate trouble in the field (support forum and knowledge base, sampled by keyword `TLS 1.x|cipher`: 18 forum threads and 1 KB article match; 7 threads and the KB article read). These are support-staff replies, none flagged official:

| Issue | What HP says | Source |
|---|---|---|
| Default TLS level | A clean device by default accepts only TLS 1.2; the level is set on the EWS page `secure_comm.html`. | `OXPd1-NET-Java/Support-Forum/2021-02-18-360051949494-Could-not-establish-trust-relationship-for-the-SSL-TLS.md:23` |
| Cipher suites | Device and server must share a cipher suite; the device's list is edited on the same EWS page. Thread was an M527 (FutureSmart 3/4 era) failing with TLS alert 70 against IIS. | `.../Support-Forum/2025-07-20-43146442117907-Https-SSL-TLS-Certificate.md:53-55` |
| TLS 1.3 | No TLS 1.3 in 2020-2021 (no date given); arrived with FutureSmart 5.5. Known defect: HTTPS requests with `Expect: 100-continue` may get HTTP 400 on Linux-based devices; HP's examples set `Expect100Continue=false`. | `.../Support-Forum/2020-06-17-360047182614-TLS-1-3-support.md`; `.../Support-Forum/2022-11-22-11492088428819-Firmware-5-5-OXPd-TLS-1-3-support.md:24`; `OXPd1-NET-Java/Knowledge-Base/Issues--11899822165011-TLS-1-3-HTTPS-Requests-with-100-Continue-May-Result-in-400-Bad-Request.md:8-12` |
| Scan delivery over TLS 1.3 | Device-to-server scan upload failed intermittently (panel error 49.38.03) on FutureSmart 5.5 behind a reverse proxy; the partner could not reproduce it on FutureSmart 5.8. | `.../Support-Forum/2023-06-09-17413087339667-Sending-scanned-images-fails-on-TLS-1-3.md:10, 231` |
| .NET 8 client | OXPdLib 1.8.4 on .NET 8 fails device trust (`RemoteCertificateNameMismatch`, chain errors); `ServicePointManager` callbacks do not apply on .NET 8; HP suggests CoreWCF with a proper certificate; older models (M602, X585) cannot put a SAN in their identity certificate. | `.../Support-Forum/2025-01-24-37773710045075-Proxies-calls-not-working-with-OXPd-1-8-4-in-NET-8.md:114, 136-138` |
| HP's own advice on device certificates | HP support tells partners to copy the SDK's accept-every-certificate callback because "HP devices use self-signed SSL Certificates". | `.../Support-Forum/2021-02-18-360051949494-...md` (third reply) |
| Simulator | Jedi Simulator 1.9 and earlier fail with the .NET example clients unless the line enabling TLS 1.2 is removed. | `S/OXPd1.7.3.2ProfessionalOnlybeta/hp-ext-XX-oxpd1.7-ReleaseNotes-1.7.3.2.txt:87`; `General/Release-Notes/release-note-287186.md` |

Consequence that shapes everything: the solution server must hold the DEVICE ADMINISTRATOR PASSWORD of every device it drives, not only at installation but at run time, because run-time calls such as `ReserveUIContext`, `ReleaseUIContext`, `SetHomescreenMessage`, `SetCustomMessage` are admin-class (D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:800, 890, 900).

### 4.3 Service discovery and versioning

- OXPd 1.6 had one uniform service set on MFPs, so no discovery was needed. OXPd 1.7 added single-function printers that implement a subset, plus backward-compatible enhancements, and made discovery mandatory; solutions must not infer capability from model name and firmware (D/oxpd-service-discovery-specification.md:11-13).
- Mechanism: the DevMgmt service, a plain HTTP GET of `http(s)://{device}/DevMgmt/DiscoveryTree.xml` (ports 80 and 443), common to all devices (D/oxpd-service-discovery-specification.md:37-42). Solutions are told not to parse the XML but to use `OXPdDiscoveryTree` / `DiscoveryTreeTranslator` in OXPdLib (.NET and Java) (D/oxpd-service-discovery-specification.md:44, 56-70).
- A service is identified by resource type (for example `OXPd:Scan`) plus revision = the schema namespace with a date code (for example ending `2010/04/14`); backward-compatible enhancements are expressed as a MINOR revision (for example `UIConfiguration.SetHomescreenMessage` needs minor 1.1) (D/oxpd-service-discovery-specification.md:52-84).
- Devices older than 1.7 may support a service without listing it in the tree (D/oxpd-service-discovery-specification.md:71).
- The IPP endpoint is discovered the same way: resource type `pwg:hpIPPPrint`, revision ending `2.0`, and the resource URI is taken from the tree (D/oxpd-service-discovery-specification.md:86-104).
- The compatibility guide repeats that the table is not to be used in code; use discovery (D/sdk-compatibility-guide.md:13).

### 4.4 Authentication service (on the device) and AuthenticationAgent (on the solution)

Purpose: front-panel user authentication by a server-side agent. Authorization is a separate service (D/oxpd-authentication-service-specification.md:13-15).

Device-side operations (OXPd:Authentication):

| Operation | Class | Effect | Source |
|---|---|---|---|
| `RegisterAuthenticationAgent(AuthenticationAgentRecord)` | admin | Adds or replaces (same Id) an agent record; the device creates a "Proxy" sign-in method that can be assigned to features on the EWS Security > Access Control page like any built-in method; auto-enabled. | D/oxpd-authentication-service-specification.md:42-69 |
| `GetAuthenticationAgentRecords()` | admin | Lists OXPd agent records only (not built-in or embedded agents). | :71-75 |
| `UnregisterAuthenticationAgent(AgentId)` | admin | Removes record and Proxy; no effect on a current session. | :77-83 |
| `ReserveAuthenticationContext(AgentId)` | run time | Non-UI initiated sign-in: when the panel is idle (nobody signed in, home screen shown) the server makes the device start the authentication process with that agent; returns the AuthenticationContextId at once, before the process completes. Works for any enabled agent whose id the caller knows. | :96-106 |
| `ReleaseAuthenticationContext(AuthenticationContextId)` | run time | Non-UI initiated sign-out (equivalent to Reset); asynchronous. | :240-244 |

The registration record: Id (UUID), Name, LocalizedName and LocalizedDescription (string tables), AuthenticationAgent (the solution's SOAP endpoint with timeouts), EnablePrePromptCheck, UserPromptTarget (a browser target: the sign-in page URL), EnableSignoutNotification with retry count and interval, optional ServerContextId (D/oxpd-authentication-service-specification.md:46-63). Records live in non-volatile memory and are cleared by a disk initialisation (:65).

Solution-side operations (OXPd:AuthenticationAgent, SOAP 1.2 called BY the device):

| Operation | When | Returns |
|---|---|---|
| `GetPrePromptResult(AuthenticationContextId, ServerContextId, language)` | Only if EnablePrePromptCheck. Before any UI. | Succeeded (with identity, optional overrides and preferences), Canceled, Failed (optional message), or Continued (go to prompting). Also serves as a reachability probe before the browser opens. |
| `GetPostPromptResult(AuthenticationContextId, ServerContextId, language)` | Immediately after the sign-in browser closes. | Succeeded (identity...), Canceled, Failed (optional message). |
| `SignoutNotification(AuthenticationContextId, ServerContextId)` | When sign-out completes, if enabled. | Not sent if the device loses power; retried per the record. |

Sources: D/oxpd-authentication-service-specification.md:108-216, 246-256; D/oxpd-authentication-agent-service-specification.md:84-123, 143-155. The agent must answer within `AuthenticationAgent.ResponseTimeout` (D/oxpd-authentication-agent-service-specification.md:86).

The process, as the device runs it (D/oxpd-authentication-service-specification.md:112-216):
1. The device generates an AuthenticationContextId (nonce) for this attempt and the resulting session.
2. Optional pre-prompt check (above).
3. User prompting: the device opens the embedded browser on UserPromptTarget. The first request carries the headers `OXPd.AuthenticationContextId` and `OXPd.UIContextId` (:148). It is a POST if the target defines an InitialPostQueryFormatString, else a GET (:152). The page may be any XHTML/JS the browser supports and may run any number of prompts; it may read a SHARED accessory (card reader) with the UIContextId (:171). The masthead home/start buttons are always hidden in a sign-in context (:169). An "Advanced" button appears if several sign-in methods exist (:161). The page ends by closing the browser; a UI timeout or browser error ends the process (:171).
4. Post-prompt check: the device "has no knowledge of what transpired" in the browser (:175); it asks the agent for the verdict.
5. On Succeeded the Proxy fills the device security context with the returned identity, the device runs authorization, then applies user preferences (panel language, launch an application access point) (:200-204). On Failed the panel shows a failure message (the agent's, if given). A persistent message with the user's DisplayName is shown while signed in (:214).

Limits and facts for an Entra sign-in:
- A UIContextId created during authentication CANNOT start scan jobs or enter priority print mode (:150).
- User preferences: panel language and keyboard for the session; user overrides: default e-mail fields and fax billing code for the native apps (D/oxpd-authentication-agent-service-specification.md:161-175).
- Sign-out: user Sign Out or Reset, UI inactivity timeout, `EndUserSession(uiContextId)` from an application, or `ReleaseAuthenticationContext` from the server (D/oxpd-authentication-service-specification.md:234-256).
- "Swipe to sign in" with no touch: `SetHomescreenMessage` shows the instruction; an OWNED card reader delivers the swipe to the server; the server calls `ReserveAuthenticationContext`; the device calls `GetPrePromptResult`; the server answers Succeeded with the identity; no browser opens (D/oxpd-authentication-service-specification.md:96-106, 116-129, and figure titles at :229-230).

### 4.5 Authorization service and AuthorizationAgent (introduced in 1.7)

- One singleton Authorization Agent Proxy per device (D/oxpd-authorization-service-specification.md:59). Endpoint `https://{device}:7627/hp/device/webservices/OXPd/AuthorizationService` (:78).
- A permission is any named device function; the same permission has the same name on every device; permissions are dynamic (:105-109). `GetPermissions(lang)` lists Id/Name/LocalizedName (flat, no tree) (:158-166); `GetSignInMethods(lang)` lists the sign-in methods currently enabled (:170-175).
- `SetConfiguration(ProxyConfiguration)` / `GetConfiguration()`: the configuration holds the agent endpoint, the GuestPermissionSet (what unauthenticated users may do), AddNewPermissionToGuestPermissionSet, DefaultSignInMethod, EnableSignInChoice, an optional PermissionToSignInMethodMap, change-notification settings, optional GuestUserOverrides and ServerContextId (:234-254). Setting a configuration makes this Proxy the device's primary authorization agent and OVERRIDES the built-in access control: the EWS access-control sections are greyed out (:264-282). Setting null restores the built-in agent (:270).
- Run time: after every successful sign-in all permissions are denied unless granted; for every user except the built-in admin and service accounts the device calls the agent's `AuthorizeUser` with the identity, the device date and time and the ServerContextId; the agent returns the permission list and optional overrides (:349-373). If the agent does not answer properly only guest permissions are granted and an error message is shown (:377).
- `ChangeNotification` to the agent when the configuration changes, a referenced sign-in method disappears, or a permission is added; the payload carries no detail, the agent must re-read (:300-322).
- The OXPd authorization proxy and embedded-extensibility authorization agents are mutually exclusive (:381-383).
- The service also manages permissions of "HP JetAdvantage Link" (the earlier name of the Workpath platform, inferred) top-level buttons, with no special steps (:72-74; same statement in D/oxpd-authorization-agent-service-specification.md). For a mixed estate this means a 1.x authorization agent can also grant or deny the Workpath apps' buttons on the same device (inferred).
- Agent side (D/oxpd-authorization-agent-service-specification.md, read whole, 100 lines): SOAP 1.2 with WS-Addressing 2004; one runtime operation, `AuthorizeUser`, answered with a `UserAuthorizationResult` (granted permission list plus optional email/fax overrides) and the `ChangeNotification` callback. HP's recommended recipe: build the user's list, add every guest permission, then remove permissions whose sign-in method the user did not use.

### 4.6 Accessories service (USB card readers)

- Remote access to USB accessories plugged into the device (D/oxpd-accessories-service-specification.md:41). Only the HID class has usable methods; CCID and others are not available (:185-187). HID devices that declare multiple report IDs are not recognised (:185).
- Registration (admin): `RegisterSharedAccessory(vendorId, productId, serialNumber)` or `RegisterOwnedAccessory(record with callback and optional server context id)`; serial null is a wildcard; a new record with the same key replaces the old; `UnregisterAccessory`; `GetSharedAccessoryRecords`, `GetOwnedAccessoryRecords`; `GetSupportedAccessoryClasses` (:63-147). Records are non-volatile and cleared by disk init (:97, 131). Only registered accessories are enumerable (`EnumerateAccessories`, :151-153).
- SHARED accessory: usable only by the application that holds the valid UI context id: `ReserveSharedAccessoryContext(uiContextId, vid, pid, serial)`; the accessory context dies with the browser (:49-55, 161-167).
- OWNED accessory: belongs to one web application; the device sends an `OwnedAccessoryEvent` with the accessory context id to the registered callback on registration, at boot and on plug-in; usable at any time, also with no browser open (:57-61, 119, 133). The event is not guaranteed; `ResendOwnedAccessoryEvent` forces it or may be polled to refresh the id (:175-177). Contexts are revoked on unplug (:179).
- HID use: `HidOpen`, `HidGetInfo`, `HidStartReading(accessoryContextId, serverContextId, callback)` which delivers `HidReportEvent` callbacks carrying raw reports and an ordinal (1, 2, 3...) so the solution can detect a lost event; reports may be batched; `HidStopReading`; `HidReadReport` and `HidWriteReport` on the control pipe (for example to make the reader beep); `HidClose` (reading must be stopped first) (:189-229).
- The service passes reports raw: the solution must decode keyboard-wedge HID usage codes into characters itself (:199).

### 4.7 Embedded browser and UIConfiguration service

Browser engine and limits:

| Item | Fact | Source (D/oxpd-browser-use-model-and-ui-configuration-service-specification.md) |
|---|---|---|
| Engine | WebKit on every OXPd device. | :117-125 |
| User agent | Carries OS (OZ or WinCE), look and feel, WebKit version and firmware. Examples: Windjammer `LF: WJ2.1` with `AppleWebKit/523.15`; Omni `CP:Pulsar1; UI:Omni; TH: Opus` with `AppleWebKit/534+`. | :400-412 |
| Markup | HTML4 + CSS3 on Windjammer; HTML5 + "CSS4" on Omni; XHTML 1.0; DOM2; JavaScript and AJAX. | :285-296 |
| Images | GIF (animated), BMP, JPEG, PNG under 1,920,000 pixels; transparency yes; alpha blending and opacity no; SVG no. | :291-292, 320-322 |
| Not available | Pop-ups (`window.open` does nothing), remote JS debugging, plugins/video, XPath, file inputs, downloads. No address bar or back/forward. Unlisted MIME types raise an error dialog. | :137, 298-326 |
| Cookies | All cookies are session cookies of the USER LOGIN session; deleted on UI timeout, successful login and logout (as of 1.7). | :330-344 |
| JS run time | JavaScript runs on the device UI thread; execution is cut at 10 seconds. | :350 |
| Cache | RAM cache; the main HTML document is never cached; sub-resources are cached per standard headers; cleared only on power cycle. | :609-627 |
| Fonts | Omni: HP Simplified only; Windjammer: Arial, Courier New, monospace. | :356-361 |
| Screen data | `window.screen.*`, `window.innerWidth/innerHeight`; language via Accept-Language. Fleet ranges from 800x600 colour touch to 640x240 monochrome. | :375-398 |
| Keys | Digits, `*`, `#`, C; START = keyCode 113 (F2) and HELP = 112 (F1) on keydown; Home, Sleep, Reset, Stop are not delivered to the page. | :418-459 |
| Soft keyboard | Native keyboard on input focus; Omni uses `placeholder` and a `textbox-mode` attribute (fax, fraction, latin-only, hex, pin); can be disabled so the page supplies its own. `onkeypress` is not fired while the native keyboard is up; `onchange` fires on OK (Windjammer). | :465-530 |
| Inactivity | The browser times out with the device UI inactivity timeout (default 60 s, 10 to 300 s) and the user is logged out; `window.OXPd.resetUIInactivityTimer()` may extend it but not indefinitely. | :538-546 |
| Trusted sites | The browser only loads URLs inside the configured trusted-sites list (wildcards allowed); an empty list trusts everything. | :669-679; D/oxpd-architectural-overview.md:114 |

The `window.OXPd` JavaScript extension (:548-593): attributes for masthead buttons (start, home, help visible/enabled; all default FALSE), `signInEnabled`, `infoEnabled`, `signInDisplayNameEnabled`, `resetEnabled`, `headerIcon` (homescreen applications only), `footerCollapsed`, `softKeyboardEnabled`, `headerBackgroundColor`, `headerForegroundColor`, read-only `uiInactivityTimeoutPeriod`, `onResetReload`, and the three context ids `UIContextId`, `AuthenticationContextId`, `QuotaContextId`; methods `beep()`, `resetUIInactivityTimer()`, `launchNativeApplication(appId)` (deprecated), `launchApplication(appId)`. Not every extension exists on every firmware; test before use (:552). `window.close()` returns to the home screen (:151). Header/footer customisation inside Authentication and Quota views only from FutureSmart 4.10.0 (2410028); no footer on panels of 4.3 inches or less (:248-255).

UIConfiguration operations (:635-659):

| Operation | Purpose | Notes |
|---|---|---|
| `RegisterTopLevelButton(record)`, `UnregisterTopLevelButton(id)`, `GetTopLevelButtonRecord(s)` | Home-screen buttons that open the browser on a URL. Record: id (UUID), title, description, icon, requestedPosition, browserTarget. | HP tested to 20 buttons per device (:729). Same id overwrites (:738). |
| `SetBrowserConfiguration` / `GetBrowserConfiguration` | trustedSites, connectionTimeout (default 1 min), responseTimeout (default 5 min). | Set REPLACES the list: read, merge, write, or other vendors' sites are lost (:679). |
| `ReserveUIContext(uri)` / `ReleaseUIContext(id)` | Open or close the browser programmatically, as if a button had been pressed; only when the panel is idle, nobody signed in and no authentication pending; does NOT trigger authentication/authorization. | Admin credentials (:788-800). |
| `GetUIAttributes()` | controlPanelId, userInterfaceId, themeId, button icon size and formats, isColor; hasHardHomeButton and screenResolutionWidth/Height from FutureSmart 4.8. | Minor 1.2, release 1.7 (:691-704). `GetUIProfile()` deprecated (:706-708). |
| `GetConfigurableUIAttributes()` | uiInactivityTimeout. | :719-723 |
| `SetDefaultApplication(id)` / `GetDefaultApplication()` | Make a registered OXPd application the HOME SCREEN (replaces the native home screen); loads guest context, reloads on sign-in/sign-out. | Release 1.8 (:810-827). |
| `SetApplicationFailureBehavior` and getters | Custom error message when an application fails to load; `isDismissible=false` locks users out of the native home screen if the server is down. | Minor 1.4, release 1.8.2 (:752-776). |
| `SetHomescreenMessage` / `GetHomescreenMessage` | Persistent message on the home screen; survives power cycle. | Minor 1.1, release 1.7; admin (:882-890). |
| `SetCustomMessage` / `GetCustomMessage` | Persistent message in all applications; last writer wins; cleared by power cycle. | :892-900; D/oxpd-authentication-service-specification.md:216 |
| `EndUserSession(UIContextId)` | Application-initiated sign-out. | :902-904 |
| `GetCurrentLanguage()`, `GetApplicationAccessPoints()` | Panel default language; list of all native, embedded and OXPd application access points. | :906-914 |

### 4.8 Print: IPP extensions, pull print and held-job release (introduced in 1.7)

- OXPd 1.x has no "print job service" of its own. Printing from a solution is standard IPP on the device (`http://{device}:631`, `:80`, `https://{device}:443` + a resource URI from the discovery tree, normally `/ipp/print`) with HP vendor extensions tied to the OXPd context model (D/oxpd-ipp-extensions-specification.md:36-59, 79-87).
- Priority print mode: vendor operations `Priority-Print-Enter` (0x4029) and `Priority-Print-Exit` (0x402A), authorised by the attribute `priority-print-auth-cookie` whose valid value is the CURRENT UIContextId. While reserved: other IPP clients get `server-error-busy`; port 9100/LPD connections are accepted but held; the mode ends on Exit, on the UI inactivity timeout or when the context becomes invalid (D/oxpd-ipp-extensions-specification.md:98-149).
- `Print-Job` (push the bytes) and `Print-URI` (the DEVICE fetches the document from a URL) accept the same cookie to run as priority jobs (:151-157, 185-200). Print-URI adds `print-uri-user-name` / `print-uri-password` (HTTP Basic the device presents when fetching) and `print-uri-cookie` (up to 4 sets, becomes the Cookie header) (:196-210). For an HTTPS document URL the device validates the server against the OXPd CA store; failures abort the job with `document-access-error` and a detail string (:219-235).
- `Get-Job-Attributes` returns `job-uuid`, the OXPd job id that matches the ids used by OXPd:Statistics and OXPd:Quota (:264-276).
- OXPdLib helper methods: `PriorityPrintEnter(uiContextId)`, `PriorityPrintExit(uiContextId)`, `PrintJob(uiContextId, data, copies, duplexMode, colorMode)`, `PrintURI(documentUri, userName, password, cookie, uiContextId, copies, duplexMode, colorMode)`, `...WithFinishing` variants (staple, punch, fold... since 1.8.1), `GetJobAttributes(jobId)`; `duplexMode` became a three-value string in 1.8.4.1, the boolean `duplex` is deprecated (:61-75, 159-183, 237-262, 289-297).
- So "pull print" on 1.x means: the jobs are HELD ON THE SERVER (or in the cloud), not on the device. The user signs in, presses the solution's button, the browser page lists the server-held jobs, and on release the server enters priority print mode with the UIContextId and either pushes the data (Print-Job) or tells the device to fetch it (Print-URI) (D/oxpd-ipp-extensions-specification.md:278-283, figure). The data sent must be a print-ready stream the device understands (the cookie example fetches a `.pcl` file, :210) (inferred: no rendering service is offered).
- A UIContextId obtained during the sign-in prompt cannot enter priority print mode (D/oxpd-authentication-service-specification.md:150), so release cannot be chained inside the authentication browser session; it needs an application (button or homescreen app) context.

### 4.9 Quota service and QuotaAgent

- One quota solution per device (singleton Proxy), configured with `SetConfiguration(ProxyConfiguration)` / `GetConfiguration()` (admin). The configuration names the QuotaAgent endpoint, two browser targets (StartJobUserPromptTarget, LimitReachedUserPromptTarget), the flags EnablePostAuthCreditsStringCheck and EnableStartJobPrePromptCheck, reconcile retry settings and an optional ServerContextId; it overrides any built-in quota system and greys out the EWS pages; cleared by disk init (D/oxpd-quota-service-specification.md:52-90).
- Covered jobs: copy (including stored copy), retrieved and "Print From" jobs, scan to e-mail/folder/fax, OXPd scan and IPP-based pull print. NOT covered: stored print jobs, internal pages, external push print (port 9100, normal IPP), PC fax out, received fax (D/oxpd-quota-service-specification.md:15-22).
- Agent operations called by the device, each keyed by a device-generated QuotaContextId (D/oxpd-quota-service-specification.md:106-305; D/oxpd-quota-agent-service-specification.md:59-215):

| Agent operation | When | Answer |
|---|---|---|
| `GetPostAuthCreditsString` | Right after a user signs in, if enabled. | A message shown on most screens for the session (for example a balance). |
| `GetStartJobPrePromptResult` | When Start is pressed on a quota-eligible job, if enabled. | Stop (optional message; no statistics are generated), Continue (optional limits: total, mono and colour impression credits and costs; limit-reached action Stop/Continue/Prompt; optional countdown display), or Prompt. |
| `GetStartJobPostPromptResult` | After the start-job browser prompt closes. | Stop or Continue as above. |
| `GetLimitReachedPostPromptResult` | After the limit-reached browser prompt closes (job paused). | Stop, or Continue with credit addends. |
| `Reconcile` | Job end (completed, stopped, cancelled, failed, power cycle). | Receives the final costs; returns a credits string; retried per configuration. |

- The quota browser prompts carry `OXPd.QuotaContextId` and `OXPd.UIContextId` headers; such a UIContextId cannot start scan jobs or enter priority print mode (D/oxpd-quota-service-specification.md:160-162). Costs can overrun credits because of the paper pipeline depth; HP suggests a minimum balance or allowing one job of debt (D/oxpd-quota-agent-service-specification.md:217-225).
- Relevance: the quota agent is how 1.x solutions gate native copy/scan jobs and account for IPP pull-print jobs. The Workpath suite has no quota feature in the brief, so this service is optional for the port (inferred).

### 4.10 Statistics service and StatisticsAgent

- Registration (admin): `RegisterStatisticsAgent(StatisticsAgentRecord)`, `GetStatisticsAgentRecords()`, `UnregisterStatisticsAgent(AgentId)`. Record: Id, names, StatisticsAgent endpoint (with timeout and retry), AckRequiredForDelete (true = Critical Agent), DataPersistenceFrequency (Job or JobAndSheet), per-sheet notification flags for printed and scanned sheets, optional ServerContextId (D/oxpd-statistics-service-specification.md:130-160). HP tested to 10 agents per device (:35).
- Agent operations called by the device: `EndJobNotification(DeviceId, JobId, Ordinal, JobStatisticsData, ServerContextId)`, `ScannedSheetDeliveredNotification`, `PrintedSheetDeliveredNotification`; the agent acknowledges each (D/oxpd-statistics-service-specification.md:39-47, 206-260; D/oxpd-statistics-agent-service-specification.md:68-92).
- Device keeps job data in a ring buffer of at least 256 jobs; the ordinal lets the agent detect a gap and recover with `GetJobList()` and `GetJobData(Ordinal)` (admin), which is for recovery only, not polling (D/oxpd-statistics-service-specification.md:49-53, 68-80, 298-306).
- Critical Agent: if the buffer is full and the oldest job was not acknowledged by a Critical Agent, the device LOCKS and starts no new jobs until delivery succeeds or the agent is unregistered; most devices support one Critical Agent (D/oxpd-statistics-service-specification.md:82-92). A trap: registering as critical and then going offline stops the customer's printer.
- Payloads must be interpreted through the OXPdLib helpers, not parsed directly (D/oxpd-statistics-service-specification.md:13). Only the DeviceId GUID is in a notification; `DeviceInfo.GetManufacturerInfo()` maps it to model, serial and so on (D/oxpd-device-info-service-specification.md:29).
- Notifications are not guaranteed to be timely; a user must never be made to wait on one (D/oxpd-statistics-service-specification.md:186).

### 4.11 DeviceInfo and CertificateManagement

- DeviceInfo: `GetManufacturerInfo()` (ModelName, ProductNumber, DeviceSerialNumber, DeviceID GUID, FirmwareVersion, FormatterSerialNumber, IPAddress in IPv6 form, Hostname, MacAddress) and `GetCustomerInfo()` (MachineName, DeviceLocation, AssetNumber, CompanyName, CompanyContact). Setting is not supported (D/oxpd-device-info-service-specification.md:22-62).
- CertificateManagement (admin for all methods): `ExportCertificates()` (PEM list), `ImportCertificate(certificate)`, `RemoveCertificate(certificate)` on the OXPd CA store; limited number of certificates per device; no validity check on import (D/oxpd-certificate-management-service-specification.md:35-61). This is how an installer pushes the CA that signed the solution server's TLS certificate to each device.

### 4.12 Scan service (1.6), Copy and SendFax (1.8), Test

Scan (D/oxpd-scan-service-specification.md):
- Needs the UI context: a scan can only be STARTED while the solution's browser application is on the panel (`StartScanJob3(uiContextId, serverContextId, scanTicket)`, :285), and not from an authentication or quota browser session (D/oxpd-authentication-service-specification.md:150).
- There is no native options screen: the web application must draw its own scan-options UI in the browser from the profiles the device returns (:136).
- Ticket building: `GetTransmissionModeProfile()`; `GetBasicOptionsProfile3(mode)` and `GetDefaultBasicOptions3(mode)`; `GetFileOptionsProfile(fileType, colorMode)` and `GetDefaultFileOptions(...)`; `ValidateScanTicket3(ticket)`; every setting must have a value; validation does not test that the destination is reachable (:151-258). The `...3` methods are minor revision 1.4, `...2` are 1.1; older ones still work without the newer options (:70-103).
- Delivery: the DEVICE pushes the files. Transmission mode `Job` (all files after processing; all destination types) or `Image` (each image as it is ready; HTTP/HTTPS only, used for thumbnail preview). Destination types: Http, HTTPS (an HTTP POST to a receiver URL on the solution), NetworkFolder (CIFS), LocalFolder, Ftp (:153-179). HTTP receivers must allow large request bodies (:178).
- A metadata file can be sent with the images; its content is a solution-defined format string with device-expanded macros; Content-Type is always text/plain over HTTP (:225-242).
- Monitoring: an optional callback `IScanServiceCallback.ScanJobEvent()` (only for HTTP/HTTPS destinations) with ordinal, timestamps, counters and state transitions; or polling `GetScanJobStatus(scanJobId)`, which works outside a UI context; status is kept for active jobs and the last 32 completed, across power cycles (:246-248, 346-384). `GetScannerStatus()` before starting (:271-281). `CancelScanJob(uiContextId, scanJobId)` needs the uiContextId that started the job (:386-399).
- During the scan the device shows its own progress and intervention dialogs, independent of the browser (:292).

Copy (D/oxpd-copy-service-specification.md), introduced in OXPd 1.8, "FutureSmart fleet" only (:52-54): remote control of the native copy job, no access to the image pipeline. `GetCopyOptionsProfile`, `GetDefaultCopyOptions`, `ValidateCopyTicket`, `GetDeviceStatus`, `StartCopyJob(uiContextId, serverContextId, copyTicket, validate)`, `GetCopyJobStatus`, `CancelCopyJob`, callback `ICopyServiceCallback.CopyJobEvent()` (:384-400). Stored copy jobs since minor 1.1 / release 1.8.1: `jobExecutionMode=Store` with optional password, folder and name; `ReleaseCopyJob`, `DeleteStoredCopyJob`, `EnumerateStoredCopyJobs` (:245-302). Note: this enumerates stored COPY jobs only; nothing in the Markdown specifications offers an API to enumerate or release stored PRINT jobs (job storage) on 1.x.

SendFax (D/sendfax-service-specification.md), introduced in OXPd 1.8, FutureSmart only (:43-53): `GetSendFaxOptionsProfile`, `GetDefaultSendFaxOptions`, `ValidateSendFaxTicket`, `GetDeviceStatus`, `StartSendFaxJob(uiContextId, serverContextId, ticket)`, `GetSendFaxJobStatus`, `CancelSendFaxJob`, callback `ISendFaxServiceCallback.SendFaxJobEvent()` (:316-329). No access to the fax address book, speed dials or forwarding (:51). Not needed by the suite in the brief.

Test (D/oxpd-test-service-specification.md): `SyncEchoString/Binary`, `AsyncEchoString/Binary` (round-trip and callback reachability probes that may be used for triage at a customer), plus test-automation methods that must NOT be used in production: `LaunchAppAccessPoint`, `ExecuteJavaScript(uiContextId, script)`, `GetBrowserState`, `GetScreenCapture` (PNG of the panel), `PressKey`, `PressScreen`, `SetCaret` (:41-148). Disabled by default; `EnableService()` after each reboot (:21-39). On Professional devices the test callback is REST, not SOAP, and needs a separate URI (:81-83). The troubleshooting tables list the classic field failures: firewall, web proxy and NAT blocking device-to-server callbacks, and server request-size limits (:57-63, 89-96).

### 4.13 Panels, look and feel, and the OXPdUI kit (Omni, Windjammer)

- Two UI generations. Windjammer (WJ1.5, 2.1, 2.6, 2.7, 4.0) is the older HP panel style: FutureSmart 3 and the legacy "Oz" devices; Omni (theme "Opus") is the current style on FutureSmart 4 and 5 (D/oxpd-look-and-feel-guide.md:53-145; D/omni-ui-user-guide.md:48). HP advises Omni for new implementations (D/oxpd-netjava-documentation.md:48). FutureSmart 3 devices updated to OXPd 1.8.3+ still report the Windjammer UI (D/oxpd-look-and-feel-guide.md:107-109).
- The panel is identified by `GetUIAttributes()` (controlPanelId, userInterfaceId, themeId) and by the user-agent tokens `CP:`, `UI:`, `TH:` (Omni) or `LF: WJx.y` (Windjammer) (D/oxpd-look-and-feel-guide.md:55-145).
- Screen sizes the server pages must serve, from the hardware chart (D/oxpd-look-and-feel-guide.md:151-193) and the FS 4.8+ table (:57-79):

| Class | Resolution | Example controlPanelId | Notes |
|---|---|---|---|
| 10.1 inch | 1280x800 | Aurora, Albatross, Aurora2, Mango, Jarvis | No hard keys; touch only |
| 8 inch HD | 1024x768 | Phantom, Corona, Eagle, Orange, Hallabong | |
| 8 inch | 800x600 | PhotonR, Pharos, Pulsar, Oriani (FS3) | Hard Home key on the older ones |
| 8 inch wide (FS3) | 800x300 | Equinox | Hard keys: Start, Stop, Sleep, Reset, keypad |
| 4.3 inch | 480x272 | STP, Quasar, Quantum, Ripken, Sugar, Jindotgae, AceMid | Typical for single-function printers; no footer on 4.3 inch or smaller |
| 2.7 inch, NO touch | 320x240 | CCPI27 | Navigation by keypad and arrow keys only |
| 1.7 inch, NO touch, 4 lines | 160x64 | CCPI (FS3, WJ4.0) | Up/Down/OK/Back keys; text entry by a `prompt()` spinner (D/oxpd-windjammer-ui-user-guide.md:318, 358-396) |

- "Kb" variants have a pull-out hardware keyboard (D/oxpd-look-and-feel-guide.md:160-190); the browser supports full hardware keyboards (D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:461-463).
- FutureSmart 3 has no icon transparency: true yellow (ffff00) is the transparent key colour on 8-bit panels (D/oxpd-look-and-feel-guide.md:197-217).
- The OXPdUI kit (`Tools/hp-ext-oxpdui-1.4`, and inside the SDK): `Omni/lib/oxpdui-omni.js` (+ debug build), `oxpdui-omni.css`, `oxpdui-omni.html` templates, an options library with localisation files, examples, API docs, and a Windjammer-to-Omni HTML converter; `Windjammer/OXPdUILib` (oxpd.js, WJ40.js, per-style CSS, depends on prototype-1.6.0.3.js); `MultiUI` examples that serve both (D/omni-ui-user-guide.md:58-85; D/oxpd-windjammer-ui-user-guide.md:49-81; D/oxpd-ui-user-guide-0.md:49-56).
- Omni is responsive: the library classifies the screen by pixel area into sm/md/lg/xl and tags every element; initialisation hangs off an `oxpdui_ready` event; custom elements such as `<hp-button>`; reserved namespaces `Omni`, CSS `hp-` and `global_oxpd_` (D/omni-ui-user-guide.md:98-199). In a desktop browser the library simulates the masthead and a screen-size switch bar when the user agent or a variable is set to `OXPDUILIBDEVMODE` (D/omni-ui-user-guide.md:245-282).
- HP's design budget for a panel page: under 3 MB of memory, avoid files over 1 MB, avoid heavy libraries, 5 to 15 components per screen, paginate lists (about 50 list items is the practical ceiling) (D/oxpd-ui-user-guide-0.md:212-249). Combined with the old WebKit builds (523.15 on Oz, 534+ on FutureSmart 4) this rules out modern SPA frameworks and unpolyfilled ES6+ on the 1.x panel (inferred from the engine versions; the specification does not list ECMAScript levels).

### 4.14 The SDK as HP describes it (SDK user guide)

- Deliverables: `OXPdLib-1.8.x.dll` (.NET) and `OXPdLib-1.8.x.jar` (Java): client proxies for every device service plus the callback/agent service skeletons the solution implements; generated from versioned WSDL/XSD plus hand-written helpers. The specification is the `.chm` extracted from the schemas; "the schemas are no longer provided in the SDK" (D/oxpd-sdk-user-guide.md:55-56, 60, 83-84). One library serves all 1.8-compliant devices (:69).
- Release content by generation (D/oxpd-sdk-user-guide.md:89-110): 1.6 = Accessories, CertificateManagement, Scan, Test, UIConfiguration; 1.7 = Authentication, Authorization, DeviceInfo, IPP, Quota, Statistics (each with its agent); 1.8 = Copy, SendFax, UIConfiguration extensions for default homescreen applications.
- Callbacks versus agents: 1.6 callbacks are one-way SOAP from device to server (Scan, Test, Accessories); 1.7 agents are two-way SOAP initiated by the device (:112-116).
- Proxy factories: since 1.7 the client first fetches the discovery tree, then a `<Service>ProxyFactory.CreateProxy(discoveryTree, hostname, adminPassword)` returns the proxy; this hides whether the device speaks SOAP or REST (the REST variant was for Pro devices). Proxies wrap an expensive channel factory and should be cached per device (:123-150).
- Supported host platforms for HP's examples: .NET Framework 4.8 on IIS 10 (WCF), and Java SE 21 with JAX-WS RI 4.0.1; Visual Studio 2022; Ant 1.7.1, Eclipse 2023-12 or Gradle 8.5+ (:186-210, 373-378, 476-535). The Java examples publish agents with "a simple java server" on a URI printed to the console (:395-414). There is no .NET (Core) 8 build of OXPdLib mentioned other than "the .NET 8 Core libraries" being needed to build the example clients (:491) (see 4.16 for what is in the package).
- Layout: `OXPdLib/DotNet` (dll, chm, generated code, helpers, proxy factories), `OXPdLib/Java` (jar, javadoc, generated source, helpers), `ExampleClients/{DotNet,Java}` (one client per service plus callback handlers), `ExampleAgentServices/{DotNet,Java}` (the four agents) (:154-174).
- Operational notes: raise IIS request-size limits for scan uploads (default about 28.6 MB) (:223-241); open firewalls and NAT for device-to-server callbacks (:242-243); never use `localhost`/127.0.0.1 in URLs given to a device (:270, 349).
- LICENCE TERMS stated in the guide (D/oxpd-sdk-user-guide.md:462-468): licensed SDK users may distribute the pre-built libraries unchanged as part of a solution; they may NOT distribute the library source or a modified library, and may not use the source "or any other means of reverse engineering" on the protocol the libraries use to talk to a device. The JavaScript/CSS/image kit may be distributed unchanged, not modified.

### 4.15 Demos (walkthrough guide; source reading is in 4.17)

HP states the demos are not production code: error checking, security and resource management were left out on purpose (D/oxpd-sdk-demos-walkthrough.md:35). All are IIS / .NET Framework 4.8 web applications installed beside the SDK and the OXPdUI folder (:37-97).

| Demo | What it shows | How it is registered | Source |
|---|---|---|---|
| ScanPreview | Image transmission mode; thumbnails of each page on the panel (first 10 pages) | Top-level button to `/ScanPreview/Default.aspx` via the UIConfigurationClient example page | :99-134 |
| MoreOptions | The scan "More Options" widget of the UI kit (needs an 8 inch panel) | Button | :136-170 |
| OXPdRemoteControlPanel | Desktop exe using the Test service to capture the panel and press keys | None (admin password required, must not be blank) | :172-185 |
| OneTouchScan | Pressing the button starts a scan immediately; files land on the server | Button | :187-219 |
| Authentication and Authorization | A complete sign-in agent + authorization agent with a browser prompt; the guide names two demo users with different permissions (:244-245), but the shipped `AuthnAuthz/AuthenticationAgent/users.xml` holds five user entries | `AuthenticationAgentRecord.xml` loaded through the AuthenticationClient page; `AuthorizationProxyConfiguration.xml` through AuthorizationClient; serverContextId used as the device identifier | :221-246 |
| PullPrint | Lists test files and prints the selected ones over IPP, showing per-job progress | Button to `/PullPrint/Default.aspx` | :248-280 |
| Statistics | Statistics agent writing a CSV | StatisticsClient page, binding Soap12, URI `/Statistics/StatisticsAgent.svc` | :282-311 |
| Quota | Quota agent with start-job and limit-reached prompts; three demo users; IPQFS `userName=$AUTHUSER_USERNAME$&displayName=$AUTHUSER_DISPLAYNAME$`; prompt binding "Plain", agent binding "Soap12" | QuotaClient page | :313-403 |
| Copy Kiosk | Copy service + default homescreen application ("kiosk") + masthead theming + optional sign-in | Its own page: device address, admin password, EWS port, OXPd port, HTTPS switches; "Register" then "Set as Default App" | :405-508 |
| SendFax | SendFax service | Button | :510-555 |

Every registration in the walkthrough is done by hand, one device at a time, from a web form that takes the device address and admin password. Fleet registration is not covered by the demos (see 4.19).

### 4.16 Simulator (user guide)

- The OXPd Simulator is a Windows desktop program (`OXPdSimulator.exe`, started by `Start.bat`) that mocks the device side of all core OXPd 1.8 services plus DevMgmt (discovery tree) and IPP, with canned responses per method that can be overridden by files (`TestFiles/<Service>/Responses/Default<Method>.rsp`, `<Method>_<n>.rsp`) and request logging (D/oxpd-simulator-user-guide.md:79-83, 113-122, 607-637).
- Needs: Windows, .NET Framework 4.6-4.7, IIS 7+ (D/oxpd-simulator-user-guide.md:91-96), and a server certificate bound with `netsh http add sslcert` to port 7627 (the OXPd SOAP port) as well as 443 (:213-265). It therefore cannot run on Kam's Mac without a Windows VM. (Corrected: the first draft also listed a "Developer Pack 4.6" and a "Visual C++ 2013 redistributable"; a case-insensitive search of the guide for `visual c|vcredist|developer pack|targeting pack` finds neither; the same search finds `Visual Studio Command Prompt` at :213, so it can match.)
- Package (`SIM/hp-ext-oxpd-simulator-1.3`, 199 files: 84 `.rsp` canned responses, 29 DLLs, Chromium `.pak` files, sample images): built 2024-05-01 from the same source revision as SDK 1.8.4 and Demos 1.9 (`SIM/hp-ext-oxpd-simulator-1.3/Revision.txt`). The 1.8.4.0 release note states the simulator was split out of the SDK into its own release from then on (`General/Release-Notes/release-note-228356.md`); SDK 1.8.2.1 still carries `OXPdSimulator/` inside it.
- It includes a simulated panel browser built on CefSharp/Chromium, NOT the device WebKit; HP warns of differences and requires testing on a real device before release (D/oxpd-simulator-user-guide.md:79, 87, 389, 897). It supports sign-in through a registered authentication agent, authorization greying of sample Copy/Email buttons, top-level buttons, default application, screen-size approximation buttons, and a subset of the `window.OXPd` object (D/oxpd-simulator-user-guide.md:395-427, 861-881).
- Limits: jobs are mock jobs with configurable delays and page counts; `ExecuteJavaScript` is not executed; accessory reads return canned or random data; default admin password is a fixed default (location: D/oxpd-simulator-user-guide.md:440, 498) (:518-527, 651, 789).
- The guide names several "internal use only" methods that are not in the public specifications: `HidStartRemoteReading`, `ReserveRemoteUIContext`, `StartRemoteScanJob2`, `Export/Import/RemoveRemoteAppCertificate` (D/oxpd-simulator-user-guide.md:653, 691-693, 745, 820). These look like the hooks behind HP's remote-app/Workpath bridge (inferred); they are not available to partners.

### 4.17 What is actually in the latest SDK package (`S/hp-ext-XX-oxpd-1.8.4.1`, source reading)

- No loose WSDL or XSD files (a `find` for `*.wsdl`/`*.xsd` in the extracted tree returns 0; positive control: the same search finds 34 files in the OXPm package), matching the guide's statement. BUT the Java jar carries the full contract set under `META-INF/wsdls/` (100 WSDL/XSD entries listed with `unzip -l` on `S/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/Java/lib/OXPdLib-1.8.4.jar`). Namespaces and date codes found there:

| Contract | Namespace date code | Contract | Namespace date code |
|---|---|---|---|
| common, faults | 2010/04/14 | authentication, authenticationagent | 2013/03/01 |
| accessories (+ callback) | 2010/04/14 | authorization, authorizationagent | 2013/03/01 |
| scan (+ callback) | 2010/04/14 | deviceinfo, security domain, servicediscovery domain | 2013/03/01 |
| test (+ callback) | 2010/04/14 | statistics, statisticsagent, job and media domains | 2014/06/26 |
| uiconfiguration | 2010/04/14 | quota, quotaagent | 2015/07/22 |
| certificatemanagement | 2010/04/14 | copy (+ callback), options and devicestatus domains | 2017/04/04 |
| sendfax (+ callback) | 2018/03/19 | pushprintcontrol, pushprintcontrolagent | `dev` (unreleased) |

- The jar and the dll are still NAMED 1.8.4 inside the 1.8.4.1 package (`OXPdLib-1.8.4.jar`, `OXPdLib-1.8.4.dll`), but the binaries differ from those in the 1.8.4 package (`diff -rq` of the two trees reports 1,042 differing files; the manifests differ only by one new javadoc page for `IppConstants.DuplexMode` and a jQuery bump). A deployed library cannot be told apart by file name.
- .NET: `OXPdLib-1.8.4.dll` targets .NET Framework 4.8 (`S/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/DotNet/OXPdLib.csproj:14`) and a second build `bin/Release/net8.0/OXPdLibCore-1.8.4.dll` targets .NET 8 with `System.ServiceModel.Http/Primitives/Duplex` 4.5.3 (`.../OXPdLibCore.csproj:4, 31-33`). Both are strong-name signed with an HP key that is not shipped (only `OXPdLibDll-public.snk` is). The net8.0 build is the CLIENT side; hosting the agent and callback SOAP services on modern .NET would need CoreWCF or similar, which the SDK does not show (the agent examples are IIS `.svc` services on .NET Framework) (inferred).
- Java: `OXPdLib-1.8.4.jar` (packages `com.hp.www.schemas.imaging.OXPd.{service,domain,common}.*` and `com.hp.www.oxpd.helpers`, 92 helper classes); the examples use `jakarta.jws` / `jakarta.xml.ws` (JAX-WS 4) and publish an agent with `Endpoint.publish("http://<ip>:8091/AuthenticationAgentServer", ...)` over plain HTTP (`S/hp-ext-XX-oxpd-1.8.4.1/ExampleAgentServices/Java/AuthenticationAgentService/src/com/hp/www/oxpd/exampleservices/AuthenticationAgentServer.java:31-32`; `.../AuthenticationAgentService.java:10-27`).
- How the client talks to a device (`S/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/DotNet/SoapProxy.cs`): URL `https://<host>:7627` + the resource URI from the discovery tree, or the fixed path `/hp/device/webservices/OXPd/<Service>` when the tree has none (:152-206); HTTP 57627 only in debug mode (:184-187); a WCF custom binding with text encoding `Soap12WSAddressingAugust2004` over HTTPS transport with HTTP Basic (:268-291, 313); user `guest` with an empty password for guest-class methods and the admin user otherwise (:355-380); the channel factory is cached per proxy (:244-330). Trap: both library proxies put the device admin password into their string form (`OXPdLib/DotNet/SoapProxy.cs:383-389` `ToString()`; `OXPdLib/Java/OXPdLibHelpers/src/com/hp/www/oxpd/helpers/SoapProxy.java:265-268` `toString()`), so logging a proxy object writes the password to the log.
- Discovery: `DiscoveryTreeTranslator.GetOXPdDiscoveryTree(hostname)` GETs `/DevMgmt/DiscoveryTree.xml` and parses LEDM `SupportedFeature`, `SupportedIfc` (manifest URI) and `SupportedTree` nodes (`.../DiscoveryTreeTranslator.cs:38-97, 217-321`).
- Proxy interfaces (the definitive operation list; `S/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/DotNet/I*Proxy.cs`). Beyond what the Markdown specifications document, the code shows: `GetSupportedAgentBindings()` / `GetSupportedCallbackBindings()` on every service; `Statistics.UnregisterAllCriticalStatisticsAgents()` (IStatisticsProxy.cs:55); `UIConfiguration.ResetUIInactivityTimer(uiContextId)` (IUIConfigurationProxy.cs:108); `Ipp.GetPrinterAttributes()`, `CancelJob(jobId)`, `SendRequest(IppRequest)` (IIppProxy.cs:44-57, 575-583); and remote-app variants not for partners: `ReserveRemoteUIContext(SignedMessage)`, `HidStartRemoteReading`, `StartRemoteScanJob2/3`, `Import/Remove/ExportRemoteAppCertificate(s)` (IUIConfigurationProxy.cs:105; IAccessoriesProxy.cs:90; IScanProxy.cs:70, 87; ICertificateManagementProxy.cs:40-49).
- An undocumented `PushPrintControl` service and `PushPrintControlAgent` (operations `GetConfiguration`, `SetConfiguration`; agent operation `ControlPushPrint`; a proxy configuration with a `pushPrintControlAgent` endpoint and an `errorBehavior` of type `PrintDirectives`) exist ONLY as WSDL/XSD and 8 classes inside the jar, namespace suffix `dev`; nothing in the .NET source, the Markdown specifications or the proxy interfaces mentions it (search for `pushprint` in `OXPdLib/DotNet`: 0 files; positive control: 8 hits in the jar listing). It looks like an agent that decides what happens to ordinary driver ("push") print jobs, which would be the 1.x hook for holding jobs (inferred from the names only; unreleased; do not plan on it).
- What the authentication agent can hand back (from the Java example's constructor arguments, `.../AuthenticationAgentService.java:57-71, 104-110`): `AuthenticatedUserInfo` with authenticationType, fullyQualifiedUserName, userName, displayName, sidString, ldapBindUser, userPrincipalName, sAMAccountName, homeFolderPath, userDomain, ndsContext, ndsTreeName, emailAddress, exchange mailbox URI and free key/value pairs; and `AuthenticationInfo` adding a cookie string, an "opaque authentication token", a password, user preferences and user overrides.
- Token hand-off to other applications: the library documentation lists the macros a browser target's InitialPostQueryFormatString may contain, including `$AUTHUSER_USERNAME$`, `$AUTHUSER_USERPRINCIPALNAME$`, `$AUTHUSER_EMAIL$`, `$AUTHUSER_DISPLAYNAME$`, `$AUTHUSER_OPAQUEAUTHNTOKEN$`, `$AUTHUSER_PASSWORD$`, `$AUTHUSER_SIDSTRING$`, `$AUTHUSER_DEPARTMENT$`, `$AUTHUSER_ATTR_...$`, and device macros `$DEVICE_ID$`, `$DEVICE_SERIAL_NUM$`, `$DEVICE_HOSTNAME$`, `$DEVICE_IP_ADDRESS$`, `$DEVICE_MACADDRESS$`, `$DEVICE_MODELNAME$`, `$DEVICE_FW_VERSION$` (occurrences counted in `S/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/DotNet/bin/Release/OXPdLib-1.8.4.XML`). So on 1.x the DEVICE carries the signed-in identity from the authentication agent to any top-level button's first POST: the agent returns an opaque token, and each application button is registered with an IPQFS that posts that token and the device id. This is the 1.x counterpart of "HP Authentication Manager shares the token with the other apps".
- TLS handling in HP's own samples: every .NET example and demo installs a certificate callback that accepts ANY device certificate (for example `M/hp-ext-oxpd-demos-1.9/Demos/PullPrint/Default.aspx.cs:17-29`; `M/hp-ext-oxpd-demos-1.9/Demos/AuthnAuthz/AuthenticationAgent/Enterprise/UserPrompt.aspx.cs:17-20`) and widens the protocol set to TLS 1.1 and 1.2 by hand (`S/hp-ext-XX-oxpd-1.8.4.1/ExampleClients/DotNet/AuthenticationClient/AuthenticationClient.aspx.cs:53-58`); the Java examples switch on `NaiveTrustProvider.setAlwaysTrust(true)` (`S/hp-ext-XX-oxpd-1.8.4.1/ExampleClients/Java/Authentication/AuthenticationExample/src/com/hp/www/oxpd/exampleclients/AuthenticationExample.java:57-63`). The reason given in the code comments: devices ship with self-signed identity certificates.
- Samples in the package: 13 .NET example clients (one ASP.NET page per service plus DiscoveryTree, a console test application) and 5 .NET callback handlers (Accessories, Copy, Scan, SendFax, Test); 4 .NET and 4 Java agent services (Authentication, Authorization, Quota, Statistics); 20 Java examples (for example `Accessories/EnumerateAccessories`, `Accessories/AccessoriesCallbackHandler`, `UIConfiguration/AddAndRemoveButton`, `Authentication/AuthenticationExample`, `IPP/IppExample`, `Scan/StartScan`, `Scan/ScanCallbackHandler`) (directory listing of `S/hp-ext-XX-oxpd-1.8.4.1/ExampleClients` and `ExampleAgentServices`).

### 4.18 What the demo source shows (Demos 1.9: `M/hp-ext-oxpd-demos-1.9/Demos`)

Authentication demo (`AuthnAuthz/AuthenticationAgent`):
- Registration record: agent endpoint with binding `Soap12` and 60 s timeouts; prompt target with binding `Plain`; `enablePrePromptCheck=false`; IPQFS `ServerContextId=<value>` and the same value as `serverContextId`, i.e. the record is PER DEVICE: the server context id is how the server knows which device is talking (`.../AuthenticationAgentRecord.xml:17-34`).
- The prompt page reads the request header `OXPd.AuthenticationContextId` and the posted `ServerContextId`, and injects both into the page as JavaScript variables (`.../Enterprise/UserPrompt.aspx.cs:27-52, 58-72`). Three page variants are served by user agent: Omni, Windjammer, four-line.
- The panel script posts the credentials by AJAX to a server-side sign-on service, then calls `window.close()`; on a wrong password it shows a message and stays (`.../Enterprise/omniuserprompt.js:27-55`).
- The server stores the attempt in a static dictionary keyed by serverContextId (one pending attempt per device) (`.../SignOnService.svc.cs:17, 30-52`); `GetPostPromptResult` fetches it, checks that the AuthenticationContextId matches and returns Succeeded with userName, displayName, emailAddress, fullyQualifiedUserName, or Canceled when nothing is pending (`.../AuthenticationAgentService.svc.cs:44-79`).
- This is exactly the shape an Entra sign-in needs: the prompt page can show a QR code or device-code and poll the server; when the server has the Entra result it tells the page to close; the device then asks `GetPostPromptResult` and receives the identity. A card swipe uses the pre-prompt path instead (4.4).
- Authorization demo: `AuthorizeUser` maps the user name to a role and returns the role's permission list; the proxy configuration names the demo authentication agent's id as `defaultSignInMethod` (`AuthnAuthz/AuthorizationAgent/AuthorizationAgentService.svc.cs:29-47`; `.../AuthorizationProxyConfiguration.xml:23-28`). So an OXPd authentication agent becomes a sign-in method id that can be made the default for the whole panel.

Pull print demo (`PullPrint`):
- The page learns the device address from the HTTP request's source address (or a `hostname` parameter) and the UI context from the `OXPd.UIContextId` header (or a query parameter) (`PullPrint/Enterprise/WindjammerDisplay.aspx.cs:43-67`). Source-address identification breaks behind NAT or a proxy; the IPQFS device macros are the robust alternative (4.17).
- Sequence: on load `PriorityMode(contextId, true, host)` = `PriorityPrintEnter`; list files; on Print, for each selected document `ippProxy.PrintURI(documentURI, userName, password, cookies, uiContextId, 1, false, null)`; poll `GetJobAttributes(jobId)` for `job-state` and show per-job progress; on exit `PriorityPrintExit` (`PullPrint/Enterprise/omniDisplay.js:187-209, 319-332`; `PullPrint/IPPService.svc.cs:126-141, 158-258`). The IPP proxy is created from the discovery tree and the host name alone, with no admin password (`PullPrint/IPPService.svc.cs:53-57`): the UIContextId is the only credential.
- The device itself downloads the document from the server URL (Print-URI), so the server must be reachable FROM the device and present a certificate the device trusts when HTTPS is used (4.8).

Package facts: "Demos 1.9" is a demo-package version, not an OXPd 1.9 platform: it was built on 2024-05-01 from the same source revision as SDK 1.8.4 and ships `OXPdLib-1.8.4.dll` (`M/hp-ext-oxpd-demos-1.9/Revision.txt`; `diff` of the 1.8 and 1.9 file lists shows only the library version in each demo's `bin` changing from 1.8.2 to 1.8.4). Demos 1.8 was built 2020-10-19. Demo 1.2 is the older Pro-era set and includes `OneTouchScanPro` (`M/OXPd_Demo_1.2/...`). All demos are .NET; no Java demo sources were found in the 1.9 package listing for AuthnAuthz or PullPrint.

### 4.19 Registration life cycle and fleet management

What must exist on EVERY device before the solution works (all admin-authenticated calls to that device, all stored in the device's non-volatile memory and all wiped by a disk initialisation):

| Step | Call | Source |
|---|---|---|
| 1. Device trusts the solution server | `CertificateManagement.ImportCertificate(CA)`; empty store = no outbound HTTPS at all | D/oxpd-certificate-management-service-specification.md:25, 53 |
| 2. Browser may reach the server | `UIConfiguration.SetBrowserConfiguration` (merge trustedSites) | D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:669-679 |
| 3. Device proxy settings if any | Device web proxy configuration (EWS / Web Jetadmin) | T/hp-ext-release-oxpm.1.7.0.0/oxpm.1.7.0.0/OXPm1.7.0.0-Documentation-1.0/OXP Management - V1.7.0.0 - WJAUserGuide.pdf p.9 |
| 4. Sign-in method | `Authentication.RegisterAuthenticationAgent(record)` | D/oxpd-authentication-service-specification.md:42-69 |
| 5. Card reader | `Accessories.RegisterOwnedAccessory` (or Shared) per vendor/product id | D/oxpd-accessories-service-specification.md:83-135 |
| 6. Access policy (optional) | `Authorization.SetConfiguration(proxyConfiguration)`, or assign the agent on the EWS Access Control page | D/oxpd-authorization-service-specification.md:256-282 |
| 7. Application buttons | `UIConfiguration.RegisterTopLevelButton` per app (max about 20) and optionally `SetDefaultApplication` | D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:725-750, 810-827 |
| 8. Usage reporting (optional) | `Statistics.RegisterStatisticsAgent` | D/oxpd-statistics-service-specification.md:130-160 |
| 9. Home-screen hint (optional) | `UIConfiguration.SetHomescreenMessage` | D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:882-890 |

There is no package, no bundle, no signing and no HP approval on 1.x: an HP support reply of March 2026 states that OXPd solutions "sit on a server and register with the devices" and that for OXPd 1.8 "and the soon to be released OXPd 1.9" no HP approval is required before deploying at a customer site, while OXPd 2 will need validation and HP signing (`OXPd1-NET-Java/Support-Forum/2026-03-04-49615404208147-Does-deploying-OXPd-based-applications-to-customer-printers-require-HP.md:26-30`; a forum reply, not marked official).

Who does the registering:

| Tool | What it is | Limits | Source |
|---|---|---|---|
| The solution's own installer/console | Calls the registration methods through OXPdLib with each device's admin password. This is what the SDK examples and demos do, one device at a time. | The vendor must build fleet handling, re-registration after disk init or firmware reset, and drift detection. | D/oxpd-sdk-demos-walkthrough.md:105-127, 423-438 |
| HP Web Jetadmin with OXPm | WJA stores repositories of "OXPd device functions" (button records), USB accessory records, authentication agent records and authorization proxy configurations, imported as XML files that follow the OXPm `solutionregistration` schema, and applies them to one device, a batch, or by automatic group + policy; also sets the browser configuration, the proxy and the OXPd CA store. HP recommends WJA "because of its advanced automation capabilities (ability to restore a device after a disk init, etc.)". | OXPm 1.7.0.0 (February 2015) needs WJA 10.3 or later; it covers buttons, accessories, authentication agents and the authorization proxy; statistics agent and quota schemas are "Beta" and not supported by WJA; nothing for 1.8 features (default application, failure behaviour, copy/fax). | WJA User Guide PDF p.2, p.5; `T/hp-ext-release-oxpm.1.7.0.0/oxpm.1.7.0.0/hp-ext-XX-oxpm-ReleaseNotes-1.7.0.0.txt:13-34` |
| OXPd Button Manager 1.1.0 | A small Windows desktop tool (`OXPdButtonManager.exe`, .NET Framework 4.8, ships `OXPdLib-1.8.4.dll`), built 2025-09-17, the newest artefact in this folder. No documentation is in the package. By its name it lists/removes/adds top-level buttons on a device (inferred). | Only three files; not opened (binary). | `T/HP_OXPd1_ButtonManager-1.1.0/Revision.txt`; `.../Manifest.txt` |
| OXPm package | Not a program: 34 files = the `solutionregistration.xsd` schema (namespace `.../OXPm/service/solutionregistration/2010/12/13`) and example XML files (`FleetTopLevelButton`, `FleetAuthenticationAgentRecord`, `FleetAuthorizationProxyConfig`, `FleetOwnedAccessoryRecord`, `FleetSharedAccessoryRecord`, `FleetStatisticsAgentRecord`, `FleetQuotaProxyConfig`) that a vendor ships to customers for import into WJA. | The example record has one fixed serverContextId for the whole fleet and no per-device macro (a grep for `$...$` macros in the examples returns nothing), so a WJA-pushed record cannot carry a per-device identifier in serverContextId; the per-device identity must then come from IPQFS device macros or DeviceInfo. | `T/hp-ext-release-oxpm.1.7.0.0/oxpm.1.7.0.0/hp-ext-XX-oxpm-1.7.0.0/http__www.hp.com_schemas_imaging_OXPm_service_solutionregistration_2010_12_13/FleetAuthenticationAgentRecordExample1.xml:1-46` |
| OXPd UI 1.4 | The Omni/Windjammer CSS/JS/image kit (4.13), 1,534 files, built 2020-10-19. | Unchanged since 2020. | `T/hp-ext-oxpdui-1.4/Revision.txt` |
| OXPd Pro Services (OPS) 1.0.20 | A Windows server product (InstallShield installer, Apache CouchDB 1.2.0, OpenSSL 0.9.8h prerequisites) that Pro (OfficeJet Pro / PageWide Pro) devices needed as external storage for button records, agent registrations, browser configuration and statistics, plus a macro parser. | Pro only; obsolete for later Pro firmware; irrelevant to FutureSmart. Bundles end-of-life components. | `T/OXPdProServices_1.0.20/.../OPSv1.0.20 Release Notes.txt:1-63`; `OXPd1-NET-Java/Knowledge-Base/General--115009512188-OXPd-Professional-Overview.md:189-211` |
| Jedi Resource Analysis 1.2.x | A memory-profiling harness (batch file + HP test executables) to measure how much device memory a solution's registrations and pages consume on FutureSmart (Jedi) devices, firmware 22.1 onward; uses the OXPd Test service. Release notes inside are for 1.2.0 (September 2014). | 2014 device list; not needed for the port's design. | `T/Jedi_ResourceAnalysis_1.2.1/JediResourceAnalysisSDK_1.2.1_ReleaseNotes.txt:1-80` |
| Jedi Simulator SDK (zip, 427 MB) | A separate FutureSmart ("Jedi") firmware simulator with print and scanner simulators (five PDF guides and an inner SDK zip dated 2021-06-03). | Kept zipped; not opened beyond the listing. A 1.7.3.2 release note says Jedi Simulator 1.9 and earlier fails with the .NET example clients unless TLS 1.2 is removed from the example. | `unzip -l` of `SIM/Jedi_Simulator_SDK1.zip`; `S/OXPd1.7.3.2ProfessionalOnlybeta/hp-ext-XX-oxpd1.7-ReleaseNotes-1.7.3.2.txt:87` |

### 4.20 Devices, firmware, "Pro", and what is deprecated

- Version history as the documents state it: OXPd 1.4 = XML "Workflow" model (still present side by side); 1.6 = embedded browser + Accessories, CertificateManagement, Scan, Test, UIConfiguration; 1.7 = agents (Authentication, Authorization, Quota, Statistics), DeviceInfo, IPP extensions, service discovery, single-function printers; 1.8 = Copy, SendFax, default homescreen application ("kiosk"); 1.8.1 = print finishing options and stored copy jobs; 1.8.2 = application failure behaviour; 1.8.3 = brings FutureSmart 3 devices to the 1.8 API with the Windjammer UI; 1.8.4.1 = three-value duplex mode (D/oxpd-sdk-user-guide.md:89-110; D/oxpd-ipp-extensions-specification.md:61-75; D/oxpd-copy-service-specification.md:245; D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:752; D/oxpd-look-and-feel-guide.md:109). The newest SDK in the library is 1.8.4.1, built 2025-06-23 (`S/hp-ext-XX-oxpd-1.8.4.1/Revision.txt`). OXPd 1.9 is announced as "soon to be released" in March 2026 but no 1.9 SDK is in the library (forum thread above).
- The firmware floor for the full 1.8 feature set: "The first fleet release to support the full OXPd 1.8 feature set is FutureSmart 4.7" (portal release notes for SDK 1.8.4.0 of 3 May 2024 and 1.8.4.1 of 30 June 2025: `General/Release-Notes/release-note-228356.md`, `General/Release-Notes/release-note-287186.md`). The 1.8.x SDK packages themselves ship no release notes (only `Manifest.txt` and `Revision.txt`; the 1.8.4.1 `Revision.txt` lists the release-note files as untracked build inputs). FutureSmart 3 devices reach 1.8 only from OXPd 1.8.3 and keep the Windjammer UI (D/oxpd-look-and-feel-guide.md:107-109).
- Other firmware anchors found in the specifications: `hasHardHomeButton` and screen resolution attributes need FutureSmart 4.8+ (D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:702-704); `launchApplication`, `onResetReload` and header/footer customisation in sign-in and quota views need FutureSmart 4.10.0 (:250, 840, 847); PageWide 774/779 and P779xx need FutureSmart 4.9+ (D/sdk-compatibility-guide.md:63-64, 92); TLS 1.3 arrived with FutureSmart 5.5 and has a known defect: HTTPS requests with `Expect: 100-continue` may get HTTP 400, so clients must disable Expect-100 (`OXPd1-NET-Java/Knowledge-Base/Issues--11899822165011-TLS-1-3-HTTPS-Requests-with-100-Continue-May-Result-in-400-Bad-Request.md:8-12`). The specifications do NOT give a table of "firmware X = OXPd 1.y"; HP's rule is to ask the device through the discovery tree (D/oxpd-service-discovery-specification.md:13).
- Device families in the compatibility guide (D/sdk-compatibility-guide.md:15-161): about 140 rows, every one marked for OXPd Java/.NET: current FutureSmart LaserJet/PageWide Enterprise and Managed lines (for example the 5700/5800/6700/6800 series, X55745/X57945/X58045/X65455/X67755, E7xxxx/E8xxxx Managed MFPs), Digital Sender Flow 8500 fn2 and ScanJet N9120 fn2, FutureSmart 3-era devices (M525, M575, M630, M725, M775, M830, M880, CM4540, M4555, ScanJet 8500...), ten legacy "Oz" MFPs marked `*` = subset of services (M3035, M4345, M5035, M9040/M9050, CM3530, CM4730, CM6030/CM6040, Digital Sender 9250C...), and Pro devices marked `**`.
- "Pro" / "Professional": HP's low-end OfficeJet Pro and PageWide Pro class, as opposed to "Enterprise" (FutureSmart). OXPd Professional implemented the 1.6/1.7 function set with a different architecture: REST instead of SOAP 1.2, a proprietary XML-driven panel browser ("SIPs" UI XML) instead of WebKit HTML, no OXPd UI library, coarser errors, and on older models the external OXPd Pro Services server for storage (`OXPd1-NET-Java/Knowledge-Base/General--115009512188-OXPd-Professional-Overview.md:151-277`). Statistics is missing on the oldest OfficeJet Pro models and Quota on the PageWide Pro ones (`S/OXPd1.7.3.2ProfessionalOnlybeta/hp-ext-XX-oxpd1.7-ReleaseNotes-1.7.3.2.txt:38-47`).
- Pro is frozen at OXPd 1.7: "OXPd version 1.7 is required on Pro devices. Later versions of OXPd are not supported" (D/sdk-compatibility-guide.md:161); "Pro Devices are not supported in the OXPd 1.8 release" (D/oxpd-netjava-documentation.md:59); Pro support was removed from the 1.8 SDK and a special Pro-only SDK 1.7.3.2 (September 2018, Java helper package renamed to `com.hp.www.oxpdpro.helpers` so it can coexist with 1.8) is the last Pro library (`S/OXPd1.7.3.2ProfessionalOnlybeta/OXPd1.7.3.2ProOnly_WhitePaper.pdf` p.3-4). Supporting Pro devices would mean a third protocol dialect and an XML UI: treat as out of scope unless Kam says otherwise.
- Deprecated inside 1.8: `GetUIProfile` (use `GetUIAttributes`), `launchNativeApplication` (use `launchApplication`), the boolean `duplex` IPP parameter, the older scan method generations (still functional), and the 1.4 XML workflow model (D/oxpd-browser-use-model-and-ui-configuration-service-specification.md:641, 840; D/oxpd-ipp-extensions-specification.md:168; D/oxpd-scan-service-specification.md:72).
- End of life: HP states there is "no specified product lifecycle policy for OXPd libraries" (`OXPd1-NET-Java/Support-Forum/2019-03-07-360028606394-OXPd-1-8-Product-Lifecycle-Policy.md:22`, a support reply from 2019). No end-of-life date for OXPd 1.x was found in this lane's material.
- Admin passwords: FutureSmart 4 added password complexity, minimum length (default 8) and account lockout for the local administrator password, and a separate remote configuration password (`OXPd1-NET-Java/Knowledge-Base/General--115005970107-FutureSmart-4-Security-Features.md:8-39, 91, 130-131`, sampled by keyword). A server that retries OXPd calls with a stale admin password can lock the device's admin account (inferred from the lockout feature).


### 4.21 OXPd 1.x versus OXPd2, concept by concept

The OXPd2 column comes from the OXPd2 lanes' BLUF and section 5 only (`B1_oxpd2-platform-guides.md`, `B2_oxpd2-api-contracts.md`, `B3_oxpd2-sdk-demos-forum.md` in this analysis folder; cited as B1 5.2 and so on). The fact that a device speaks one platform or the other, never both, is from B1 BLUF (HP portal `how-it-works.md:28`).

| Concept | OXPd 1.x (this lane) | OXPd2 (B lanes) | What one server must abstract |
|---|---|---|---|
| What is deployed | Nothing on the device; registration records written by admin SOAP calls; no HP approval for 1.8/1.9 (4.19) | A bundle of declarations (`solution.bdl`) with no code, signed by HP after "VAV/VNV"; unsigned bundles only on a device in LDB developer mode, which wipes solutions when toggled; at the time of B3 no partner had a signed bundle that installs (B1 BLUF 3; B3 BLUF 1) | A "device onboarding" driver per platform: 1.x = register records; 2 = install bundle and exchange the install code within 5 minutes |
| Wire protocol, device side | SOAP 1.2 + WS-Addressing 2004, port 7627, HTTP Basic `admin`/`guest` (4.1, 4.2) | REST/JSON, 16 services, 201 operations (B2 BLUF) | One capability interface per function (sign-in, reader, UI, scan, print, stats, device info) with a SOAP and a REST implementation |
| Device calling the server | SOAP agent endpoints (Authentication, Authorization, Quota, Statistics) and one-way SOAP callbacks (Accessories, Scan, Copy, Test) (4.14) | HTTP "targets" declared in the manifest, parameterised by `$SOLUTION_CONTEXT(HOST)$`; callbacks authenticated only by a static credential in the solution context (B1 5.1; B2 5) | Inbound adapters that map both to the same internal events (card presented, sign-in requested, sign-out, scan file arrived, job ended) |
| Server's credential to the device | Device admin password, needed at run time (4.2) | Admin password once at install; then a per-device solution token and refresh token (B2 5; B3 5.1 item 3) | A per-device secret store holding two kinds of secret; on OXPd2 the admin password can be discarded after install, on 1.x it cannot |
| Sign-in | Authentication agent record; pre-prompt (card, silent), browser prompt page, post-prompt verdict; `ReserveAuthenticationContext` to start sign-in from the server; sign-out notification (4.4) | Authentication agent with pre-prompt, prompt page, post-prompt and sign-out; server-initiated `login(succeeded, details)`; 409 if the panel is not idle; `forceLogout` (B1 BLUF 4; B2 BLUF 1, 5) | One sign-in state machine: trigger (card, QR, panel), optional interactive page, verdict with identity, sign-out; "card tap while someone is signed in" handled as sign-out then sign-in on both |
| Identity to the apps | The device posts `$AUTHUSER_...$` macros (user name, UPN, email, an opaque token of up to the agent's choosing) into each button's first POST (4.17) | Security Context attributes (max 256 pairs of 512 characters) read through `resolveSecurityExpression` or header macros; tokens must stay on the server (B2 BLUF 4; B1 5.1) | A server-side session keyed by device id + platform session id holding the Entra tokens; the platform carries only an id. On 1.x pass a short random session handle as the opaque token, never an Entra token |
| Authorization | Singleton authorization proxy that replaces the device's access control; per-user permission list (4.5) | `userPolicy` agent, still Alpha (B2 BLUF, 5) | Optional policy module; the suite should work without it on both |
| Panel UI | WebKit 523/534+, HTML4/5, 10 s JS limit, no pop-ups or downloads, `window.OXPd`, screens 160x64 to 1280x800, Omni/Windjammer kits (4.7, 4.13) | Chromium 87 (QtWebEngine 5.15), no pop-ups, file inputs or downloads; cookie and cache behaviour "under development"; seven test groups down to 320x240 (B1 BLUF 5; B1 5.1) | Server-rendered pages with a thin platform shim; one markup level that the 1.x WebKit can render, or two templates (Omni-era 1.x and OXPd2); no Microsoft sign-in page on the panel in either |
| Card readers | Accessories service: USB HID only, owned or shared, raw reports with ordinals; multi-report-ID HID not recognised (4.6) | `usbAccessories`: owned HID readers declared in the signed bundle by vendor/product id; raw reports; a new reader model needs a new signed bundle; collides with another vendor owning the same model (B1 5.1, 5.3; B3 5.1 item 5) | One HID keyboard-report decoder per reader model, shared by both adapters (the earlier OXPd1 attempt has per-model handling, per `START-HERE.md`) |
| Scan | Scan service: needs the app's UI context (not the sign-in one); device POSTs files to a server HTTP(S) receiver; ticket built from profiles; callback or polling (4.12) | `scanJobs` needs a UI-context token; device POSTs `multipart/mixed` to the destination (B2 BLUF 3) | A "scan to server" receiver with streaming, size limits and per-job secrets, then shared Graph upload code |
| Print and release | IPP to the device; priority print mode keyed by UIContextId; Print-Job (push) or Print-URI (device pulls, Basic or cookie auth); no device job storage API; undocumented `PushPrintControl` in the jar only (4.8, 4.17) | No REST print call; IPP to the device; the OXPd2 priority extensions for Print-Job/Print-URI marked "currently not supported"; IPP certificate check on by default from 6.25.0.730 (B2 BLUF 2; B1 5.1) | A "send job to device" interface: IPP Print-Job by default, Print-URI optional; jobs held on the server (or in Universal Print) for both; priority mode only where available |
| Statistics | Statistics agent, ordinals, ring buffer of at least 256 jobs, optional critical agent that locks the device (4.10) | `jobStatistics` agent with user identity, acknowledge or lose; `deviceUsage`, `supplies`; critical registration blocks jobs (B1 5.1; B2 5) | One usage ingest, de-duplicated by device + job id, forwarded to the existing Log Analytics tables; never register as critical by default |
| Device identity | DeviceInfo: DeviceID GUID, serial, model, firmware, MAC (4.11) | `device` service; `$DEVICE(ID)$` macro (B1 5.1) | One device record keyed by serial number, with platform, version and capability set |
| Capability discovery | `/DevMgmt/DiscoveryTree.xml`, service revisions and minor revisions (4.3) | Not covered in the B sections read | A capability probe at onboarding and after firmware change |
| Fleet deployment | Vendor tool calling the registration API per device, or Web Jetadmin + OXPm XML (buttons, accessories, authentication, authorization only); records lost on disk init (4.19) | The server's own installer (admin grant, install, context, CA import, install-code exchange); no HP fleet tool documented (B1 5.1) | Onboarding, drift detection ("is my registration still there?") and self-repair as a first-class server feature for both |
| Network direction | Two-way: device to server (browser, agents, callbacks, Print-URI fetch) and server to device (SOAP, IPP) (4.1) | Two-way, same shape (B1 BLUF 2, 5.2 item 2) | A server on the customer LAN (Kam's "localised server") fits both; a cloud server would need a relay |
| Test tooling | Windows-only OXPd Simulator 1.3 with a Chromium panel (not the device engine) (4.16) | OVA simulator not yet downloaded (`START-HERE.md`) | Automated tests against both simulators and real devices of each generation |

## 5. What this means for the port

### 5.1 Requirements (each tied to a finding)

1. **An OXPd 1.x device adapter is a SOAP 1.2 client and a SOAP 1.2 server.** The server calls device services on `https://{device}:7627` and hosts the agent and callback endpoints the device calls (4.1, 4.14). With .NET: OXPdLib's net8.0 build covers the client side only; the agent side needs CoreWCF (HP's own forum advice) or hand-written SOAP endpoints validated against the WSDLs in the jar; .NET Framework 4.8 on IIS is the only hosting HP demonstrates (4.17; 4.2 TLS table). With Java: the jar plus JAX-WS 4 covers both sides (4.17). The choice of stack for the 1.x adapter is the first architecture decision; B3 recommends .NET 8 for OXPd2 (B3 5.1 item 1).
2. **A per-device secret store holding the device admin password** for the life of the registration (4.2), encrypted, never logged (the library's own `ToString()` leaks it, 4.17), with lockout-aware retry (4.20, FutureSmart 4 lockout).
3. **Onboarding per device**: probe the discovery tree; import the server's CA into the OXPd CA store; merge (never overwrite) trusted sites; register the authentication agent, owned card readers, top-level buttons (at most about 20 per device), optional authorization configuration, statistics agent and home-screen message (4.19). Re-check and repair after disk initialisation, firmware change or reboot (records are non-volatile but wiped by disk init; owned-accessory events may need `ResendOwnedAccessoryEvent`, 4.6).
4. **Sign-in hub on 1.x**: card swipe → owned accessory HID report → server decodes the card number → `ReserveAuthenticationContext` → device calls `GetPrePromptResult` → server answers Succeeded with identity (4.4). QR / device-code / first enrolment → pre-prompt answers Continued → the prompt page (served by the server) shows a code and polls the server → page closes → `GetPostPromptResult` returns the identity (4.4, 4.18).
5. **Token hand-off to the apps on 1.x**: register each app button with an `InitialPostQueryFormatString` posting `$AUTHUSER_OPAQUEAUTHNTOKEN$`, `$AUTHUSER_USERPRINCIPALNAME$` and `$DEVICE_ID$`; the opaque token is a server-side session handle, the Entra tokens never leave the server (4.17, 4.21).
6. **Panel UI built for the oldest engine in scope**: ES5-level JavaScript, no framework that needs a modern engine, under 3 MB per page, paginated lists, layouts for the screen classes in 4.13, keyboard-only navigation if 2.7-inch/4-line panels are in scope (4.7, 4.13). The Omni UI kit may be shipped unchanged (licence, 4.14).
7. **Print release on 1.x**: Universal Print secure/pull jobs are held server-side; on release the app page (with its UI context, not the sign-in context) enters priority print mode and sends the job by IPP Print-Job, or by Print-URI from a short-lived URL the device can reach and trusts (4.8, 4.18). The server must deliver a print-ready format (PDF or PCL) the device accepts (inferred, 4.8).
8. **Scan on 1.x**: the app page builds the ticket from the device profiles, starts the scan with its UI context, and the device POSTs to a server receiver (HTTPS, large bodies allowed); progress by callback or `GetScanJobStatus` (4.12).
9. **Usage logs**: a non-critical statistics agent with ordinal gap recovery feeding the existing Log Analytics tables (4.10).
10. **Certificates**: a server certificate whose CN (and SAN) is the server's DNS name, never an IP, issued by a CA that is imported into every device's OXPd CA store; TLS 1.2 with cipher suites the oldest devices accept; `Expect: 100-continue` disabled for FutureSmart 5.5+ (4.2).

### 5.2 Constraints

- One authorization proxy and one quota proxy per device, and most devices allow one critical statistics agent (4.5, 4.9, 4.10): if a customer already runs another vendor's access-control or accounting product on the device, the suite cannot also own those roles. Sign-in agents and buttons can coexist (several records allowed, 4.4, 4.7).
- The OXPd authorization proxy and embedded authorization agents are mutually exclusive (4.5).
- `SetBrowserConfiguration` replaces the trusted-sites list; another vendor's sites are lost if it is written without merging (4.7).
- UI contexts from the sign-in or quota prompt cannot scan or print (4.4, 4.9); release cannot happen inside the sign-in page.
- Inactivity timeout 10 to 300 s (default 60) ends the session; long Graph operations must call `resetUIInactivityTimer` sparingly (4.7).
- The device must reach the server (browser, agents, scan upload, Print-URI) and the server must reach the device (SOAP, IPP): a LAN server, no NAT in between, no 3xx redirects on agent endpoints, no `localhost` URLs (4.1, 4.2, 4.14).
- Card readers: HID class only, single report id; CCID and other classes unavailable (4.6).
- Pro devices (REST, XML panel UI, frozen at 1.7) and legacy Oz devices (subset of services) would each be another dialect (4.20).

### 5.3 Reusable parts

- OXPdLib 1.8.4 (dll/jar) may be redistributed unchanged inside the product; its source may not be redistributed or modified (4.14).
- The Demos 1.9 AuthnAuthz agent and prompt page pattern (record per device, server-context id, AJAX sign-on then `window.close()`) and the PullPrint sequence (priority enter, Print-URI, poll `GetJobAttributes`, priority exit) are the right skeletons, rewritten without their weaknesses (4.18, section 8).
- The OXPm `solutionregistration` schema and example records, if customers want Web Jetadmin to push the records (4.19).
- The Omni UI kit (unchanged) for panel look and feel (4.13).
- The 1.x discovery logic (`DiscoveryTreeTranslator`) for capability probing (4.17).

### 5.4 Traps

- **Accept-all TLS everywhere in HP's samples and support answers** (4.2, 4.17): copying them makes the server trust any device, including an impostor. The device's identity certificate is self-signed by default; the product needs certificate pinning per device at onboarding (trust on first use, recorded) or customer-issued device certificates (inferred design response).
- **Critical statistics agent**: registering as critical and going offline locks the customer's printers (4.10).
- **Application failure behaviour** with `isDismissible=false` or a default (home-screen) application locks users out of the native panel when the server is down (4.7). Use neither by default.
- **Device identification by source IP** (PullPrint demo) breaks behind NAT; use `$DEVICE_ID$` macros or the server context id (4.18).
- **`$AUTHUSER_PASSWORD$` and the `password` field of `AuthenticationInfo`** exist (4.17); never ask the device to hold or forward a user password.
- **Library file names do not change between 1.8.4 and 1.8.4.1** (4.17): record the build revision of the shipped library, not the file name.
- **Simulator is Chromium, not the device WebKit**: UI that works in the simulator can fail on a device (4.16).
- **TLS 1.3 on FutureSmart 5.5** (Expect-100, scan upload failures fixed in 5.8) (4.2).
- **The undocumented `PushPrintControl` service** is tempting for device-side hold-and-release but is unreleased (`dev` namespace) (4.17).

## 6. Contradictions and doubts

| Topic | Source A | Source B | Assessment |
|---|---|---|---|
| Simulator prerequisites | First draft of this report listed a Developer Pack and a VC++ 2013 redistributable | `D/oxpd-simulator-user-guide.md:91-96` lists Windows, .NET Framework 4.6-4.7, IIS 7+ only | Corrected in 4.16 |
| Demo users | Walkthrough names two demo users (D/oxpd-sdk-demos-walkthrough.md:244-245) | `M/hp-ext-oxpd-demos-1.9/Demos/AuthnAuthz/AuthenticationAgent/users.xml` has five user entries | Code wins; corrected in 4.15 |
| Schemas in the SDK | "The schemas are no longer provided in the SDK" (D/oxpd-sdk-user-guide.md) | 100 WSDL/XSD inside `OXPdLib-1.8.4.jar` `META-INF/wsdls/` (4.17) | They are present, only not as loose files |
| Library version naming | Package 1.8.4.1 | Files named `OXPdLib-1.8.4.*`, binaries different from 1.8.4 (1,042 differing files by `diff -rq`) | Version in file name is not reliable |
| Duplex parameter type | Spec: a string (`D/oxpd-ipp-extensions-specification.md:70, 166`) | Release note 1.8.4.1: "a duplexMode enum" (`General/Release-Notes/release-note-287186.md`) | Enum of string values (`IppConstants.DuplexMode`); no conflict in practice |
| CA store on FutureSmart | "Synonymous with the Windows machine certificate store" on Jedi (D/oxpd-certificate-management-service-specification.md:25) | FutureSmart 5 devices are Linux-based (`OXPd1-NET-Java/Knowledge-Base/Issues--11899822165011-...md:8`) | Text predates FutureSmart 5; the behaviour (empty store = no outbound HTTPS) should be tested on FS5 |
| Key size | 1024-bit recommendation (D/oxpd-security-model-overview.md:49) | NIST deprecation and 2048-bit from 2014 (:51) | Stale text; use 2048-bit or more |
| Device certificate trust | Security model: validating the device certificate is the developer's choice (D/oxpd-security-model-overview.md:41-43) | HP support tells partners to accept every certificate (forum 2021-02-18); a later HP reply (2025) recommends CoreWCF with a proper certificate | No HP-endorsed pattern for device identity; the port must design one |
| OXPd 1.9 | "Soon to be released OXPd 1.9" (forum, March 2026, 4.19) | No 1.9 SDK in the library; "Demos 1.9" is a demo-package version built on 1.8.4 | Treat 1.8.4.1 as the latest 1.x; ask Kam whether HP has shared a 1.9 beta |
| Pro devices and OPS | Compatibility guide: OPS "is required" on OfficeJet Pro (D/sdk-compatibility-guide.md:161) | Pro overview points to a white paper on the "Removal of OPS on Pro Printers" (`OXPd1-NET-Java/Knowledge-Base/General--115009512188-OXPd-Professional-Overview.md:315`) | Pro is out of scope regardless; stale either way |
| Revision files | Every `Revision.txt` in the lane begins with the line `hp-ext-oxpdui-1.4.zip` whatever the package, and several append a build machine's `git status` | | A build-script artefact; only the date and commit hash are meaningful |
| Release notes | 1.8.x SDK packages contain no release notes | Portal copies exist in `General/Release-Notes/` | Use the portal copies |
| Demos 1.8 vs 1.9 | Same ten demos | Only the bundled OXPdLib version differs (first agent's `diff`, 4.18) | Consistent |

## 7. Questions for Kam or his team

1. **Which device generations are in the customers' 1.x fleets?** (FutureSmart 5 / 4.7+ with Omni; FutureSmart 3 with Windjammer; legacy "Oz"; single-function printers with 4.3-inch panels; 2.7-inch or 4-line non-touch panels; any OfficeJet/PageWide Pro.) Why: it fixes the browser engine, screen sizes, UI kit and which services exist (4.13, 4.20). If unanswered: FutureSmart 4.7 and later only, touch panels of 4.3 inches and larger, Omni UI; Oz and Pro out of scope.
2. **Will customers accept a server that stores each device's administrator password permanently?** Why: on 1.x run-time calls are admin-class, so the server cannot discard it as it can on OXPd2 (4.2, 4.21). If unanswered: yes, stored encrypted per device on the customer's local server, with an onboarding tool that never displays it.
3. **Who issues the server's TLS certificate and what DNS name will the local server have?** Why: devices validate the server against their OXPd CA store and require a CN match with no IP addresses; the CA must be pushed to every device (4.2, 4.19). If unanswered: the customer's internal CA, an FQDN in the customer's DNS, CA imported by the onboarding tool.
4. **Do customers already run another vendor's access control, accounting or pull-print product on their OXPd devices (or Web Jetadmin policies)?** Why: authorization, quota and critical statistics are singletons, trusted sites are overwritten by naive writers, and card readers may already be owned (4.5, 4.7, 4.9, 4.10). If unanswered: assume coexistence is needed: sign-in agent and buttons only, no authorization or quota proxy, non-critical statistics, merged trusted sites.
5. **Should the 1.x adapter be .NET or Java?** Why: the existing back end is C#, but OXPdLib's .NET 8 build is client-only and HP's agent hosting is .NET Framework/IIS; the Java library covers both sides on Java 21; the earlier OXPd1 attempt is Java (4.17, 5.1 item 1). If unanswered: .NET 8 with CoreWCF for agent endpoints, after a spike that proves a device can call a CoreWCF agent.
6. **Is Universal Print "secure release" acceptable as server-held jobs on 1.x devices?** Why: 1.x has no device job-storage API, so the `_Secure` Workpath behaviour cannot be reproduced on the device (4.8, 4.12). If unanswered: yes, jobs held in Universal Print or on the server and released by IPP.
7. **Is Web Jetadmin used by the target customers, and should the product also ship OXPm XML records?** Why: WJA can restore registrations after disk init, but OXPm 1.7 covers only buttons, accessories, authentication and authorization, and a WJA-pushed record cannot carry a per-device server context id (4.19). If unanswered: the product's own onboarding tool is primary; OXPm records are an optional extra.
8. **Has HP given Datasec any OXPd 1.9 material?** Why: HP called it "soon to be released" in March 2026; none is in the library (6). If unanswered: build on 1.8.4.1.

## 8. Secrets and sensitive items seen, and weaknesses not to carry over

Secrets and sensitive items (locations only, no values copied):

- `M/hp-ext-oxpd-demos-1.9/Demos/AuthnAuthz/AuthenticationAgent/users.xml:7, 13, 19, 25, 31`: demo user passwords in plain text (HP demo data, not real people).
- `D/oxpd-sdk-demos-walkthrough.md:244-245`: demo credentials printed in the guide.
- `D/oxpd-simulator-user-guide.md:440, 498`: the simulator's default administrator password is documented.
- 16 Java example clients in `S/hp-ext-XX-oxpd-1.8.4.1/ExampleClients/Java/` assign a hardcoded placeholder device admin password (for example `.../Authentication/AuthenticationExample/src/com/hp/www/oxpd/exampleclients/AuthenticationExample.java:68`, `.../UIConfiguration/AddAndRemoveButton/src/com/hp/www/oxpd/exampleclients/AddAndRemoveButton.java:65`; 17 files in total match `adminPassword = "<literal>"`, the 17th is the library `toString()` below).
- `T/Jedi_ResourceAnalysis_1.2.1/MemoryProfiler09-25-2014/DirtyUtilities/Configuration/hpservercertificate.pfx`: a server certificate file (not opened; may hold a private key).
- Strong-name keys: only `OXPdLibDll-public.snk` is shipped in each SDK; the private key the `.csproj` files reference (`OXPdLibDll.snk`) is not present.
- No real customer data or tenant identifiers were seen in this lane.

Weaknesses in HP's samples that the port must not carry over:

- Certificate validation disabled: an accept-all callback in 20 `.cs` files of Demos 1.9 (for example `M/hp-ext-oxpd-demos-1.9/Demos/PullPrint/Default.aspx.cs:17-29`) and in the SDK examples; `NaiveTrustProvider.setAlwaysTrust(true)` in the Java examples (4.17).
- The device admin password appears in the string form of every OXPdLib proxy (`S/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/DotNet/SoapProxy.cs:383-389`; `.../OXPdLib/Java/OXPdLibHelpers/src/com/hp/www/oxpd/helpers/SoapProxy.java:265-268`): never log proxies, or wrap them.
- Agent endpoints published over plain HTTP in the Java examples (`.../AuthenticationAgentServer.java:31-32`), and the unencrypted device port 57627 in debug mode (4.17).
- Demo sign-on state in a static in-memory dictionary, one pending attempt per device, no expiry (`M/hp-ext-oxpd-demos-1.9/Demos/AuthnAuthz/AuthenticationAgent/SignOnService.svc.cs:17`) (4.18).
- Device identified by the request's source IP (PullPrint) (4.18).
- Passwords posted from the panel page to the server by AJAX (AuthnAuthz prompt): acceptable only over HTTPS; the port should not collect directory passwords at the panel at all.
- `$AUTHUSER_PASSWORD$` macro and the `password` field of the authentication result: do not use (4.17).
- The Test service's remote-control methods (`ExecuteJavaScript`, `PressScreen`, `GetScreenCapture`) must not be enabled in production (4.12).
- The OXPm example records use one fixed server context id for the whole fleet (4.19): per-device identity must come from somewhere else.

---

Claims spot-checked in this pass (source re-read at the cited lines): SOAP 1.2 only; CN match and no IPs; empty CA store; sign-in UI context cannot scan or priority-print; 10-second JavaScript limit; 20 buttons; `ReserveUIContext` admin-only; priority-print opcodes; critical-agent locking; Pro frozen at 1.7; HID-only and multi-report-id limit; stale 1024-bit text; Test service disabled by default; `SetHomescreenMessage`/`SetCustomMessage` admin-only; header/footer from FutureSmart 4.10.0; Omni advised and Pro not in 1.8; quota coverage list; SDK licence terms; `OXPdLib.csproj` net48; `OXPdLibCore.csproj` net8.0 and ServiceModel 4.5.3; guest user with empty password; port 57627 in debug; PullPrint IPP proxy without admin password; 100 WSDL/XSD in the jar and none loose; `PushPrintControl` only in the jar; 1,042 differing files between 1.8.4 and 1.8.4.1; HP-approval forum reply; OXPm date, WJA 10.3 and beta statistics/quota schemas; OneTouchScanPro in Demos 1.2; TLS 1.3 / Expect-100 KB article; no lifecycle policy; `$AUTHUSER_...$` macro list including `AUTHUSER_ATTR_`; duplex mode; Jedi Simulator TLS 1.2 note; simulator prerequisites (corrected); demo user count (corrected).

Completed by a second agent (Opus) after the first (Fable) was cut off; 35 claims spot-checked, 2 corrected.
