# A2 — MailFlow and Teams: source-code analysis (Workpath apps)

Lane A2, 2026-11-18. Library root for every path below: `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`.
Short path prefixes used in citations:

- `MF/` = `HPAM - Docs and Notes/Source Code/MailFlow-main/`
- `MFa/` = `MF/app/src/main/java/com/hp/print/mailflowas/`
- `TM/` = `HPAM - Docs and Notes/Source Code/Teams-main/`
- `TMa/` = `TM/app/src/main/java/com/hp/print/teams/`

"CVL" = the shared `commonvaluablelibrary` AAR. "HPAM" = HP Authentication Manager (the sign-in app).

---

## 1. BLUF

This lane holds the Kotlin/Java source of two Android (Workpath) apps: MailFlow 4.4 (Outlook mail) and Teams 4.4.3. Both are thin Microsoft Graph clients with a panel UI; everything that touches the scanner, the print engine, device settings and sign-in is delegated to shared libraries.

1. **Neither app signs in.** Each binds to HPAM through the `usermanagement` AAR (`UserManagementProxy` → `UserManagement.getToken()` / `getNewToken()` / `UserInfoCallback`) and uses the access token it is handed. MailFlow still contains its own WebView OAuth sign-in, but it is dead code.
2. **Scan and print are not in these repos.** The apps start CVL's `ScanSupportService` / `ScanPreviewFragment` and CVL's `PrintPreviewFragment` / `PrintJobProgressHandler`, then exchange **local file paths** with them. The port must replace "file on the device" with "file on the server".
3. **Office-to-PDF conversion is done by Microsoft Graph** (`…/content?format=pdf`), in MailFlow via a temporary upload into the user's own OneDrive app folder. That needs a Files scope that MailFlow's own scope list does not name; it works only because the token comes from HPAM's registration.
4. **Graph error handling is weak and must not be copied:** no `Retry-After` handling, blind `retry(2)` in MailFlow, none in Teams, several raw HTTP calls that bypass the 401 token-refresh path, large files read wholly into memory, MailFlow's "upload session" sent as one single PUT.
5. **Per-user state roams through HPAM**, not the device: `UserManagement.getUserProperty` / `updateUserProperty` hold quick messages, quick-access pins, EULA and remember-me flags. A server port needs the same store, shared with the Workpath fleet if users are to see the same pins and messages on both.

---

## 2. Coverage

Inventory command output: MailFlow-main 613 files (142 `.kt`, 38 `.java`, 233 `.xml`, 114 `.png`, 14 C/C++, 6 `.aar`, 12 `.htm`); Teams-main 392 files (115 `.kt`, 17 `.java`, 123 `.xml`, 78 `.png`, 14 C/C++, 4 `.aar`).

| | MailFlow | Teams |
|---|---|---|
| Read whole (every line) | 44 files: both `build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`, manifest, `release.yml`, `hpk.xml`, `notes`, `provider.cfg`, and 35 source files (app bootstrap, config, auth, token, splash, user-data store, error mapping, login fragment, admin consent, quick-message model) | 8 files: `README.md`, `notes`, both `build.gradle.kts`, `settings.gradle.kts`, manifest, `hpk.xml`, `LogoutPresenter` |
| Read with only `import`, blank and debug-log lines removed (all logic seen) | 24 files: all 7 Graph provider classes, the download/PDF provider, Gotenberg job and its 3 helper files, `DownloadPresenter`, `Html2Pdf`, `Util`, `Commons`, `BaseAppCompatActivity`, print preview activity and fragment, attachment fragments, scan option activity and fragment, `SendPresenter` | 19 files: the 6 `auth/` files, `Constants`, `TeamsConstants`, `URLStore`, `HttpHeader`, error mapping and exceptions, `AppConfigHelper`, `DataHolder`, `FallbackDns`, `DirectoryHelper`, `MainViewType`, `SortingType`, `NetworkTimeouts` |
| Sampled (how chosen) | 16 files. `SendFragment` (1,880 lines): function list by grep, then lines 196–327, 756–867, 926–1114 read (scan result, scan start, send and size limit). `MainActivity`, `MainFragment`, `MailBodyFragment`, `QuickMessagesActivity`, settings, `RememberMeFragment`, `WebViewEditor`, `MainPresenter`, models: grep for function names, string resources, shared-library calls, then targeted sections. `config.cfg`: first 60 and last 50 lines plus all ids. `MailFlow.moc`: first 40 lines plus element counts | 20+ files. All presenters: grep for every Graph call site, function and constant; then `ScanPreviewPresenter` 50–384, `DownloadPresenter` 85–384, `QuickAccessPresenter` 45–135, `SplashPresenter` 14–66 read. `SplashActivity`, `UserPreferencesStore`, `NavigationCache`, `FileItem`, `Utils`: grep plus sections. Whole app tree: grep for every scan and print call site. `Teams.moc`: frame and fidget ids, locale counts. `gradle.properties`: key names only (values deliberately not read) |
| Not opened | About 60 app source files (list adapters, view holders, MVP contract interfaces, provider interfaces, settings sub-fragments, `DisplayTime`, `EmailSelectActivity`, custom views); vendored `tokenautocomplete` (11 Java), `FloatingActionButton` (4 Java); `OnGuardLib` (13 Java, 14 C/C++, a `.docx` and a `.pptx`); tests; all 233 resource XML files (only `<string>` counts taken); EULA `.htm`; `web_view_editor.js`; `codeql.yml`, `gitleaks.yml`; the 6 AARs (binary, the shared-library lane's) | About 75 app source files (fragments `FilesFragment`, `QuickAccessFragment`, `RecentFragment`, `TeamsFragment`, `ChannelsFragment`, `SearchActivity`, dialogs, adapters, app guide, settings sub-fragments, most of `MainActivity`'s 1,649 lines); `OnGuardLib`; tests; all resource XML; EULA `.htm`; workflows; the keystore file; the 4 AARs |

Consequence for confidence: Graph calls, auth, error mapping, scan and print hand-off, storage and configuration are read at source. Screen-by-screen UI detail (exact button layout, every dialog text) is inferred from function names, layout ids and string resource names, and is marked "(inferred)" where so.

---

## 3. Inventory

| | MailFlow | Teams |
|---|---|---|
| Product name in HPK | "Mailflow for Authentication Suite" (`MF/packaging_release/hpk.xml:4`) | "Teams for Authentication Suite" (`TM/packaging_release/hpk.xml:4`) |
| Android package | `com.hp.print.mailflowas` (`MF/app/build.gradle.kts:42`) | `com.hp.print.cypher.teams`, namespace `com.hp.print.teams` (`TM/app/build.gradle.kts:23,39`) |
| Version | 4.4, code 4_04_00_00 (`MF/app/build.gradle.kts:46-47`) | 4.4.3, code 4_04_03_00 (`TM/app/build.gradle.kts:42-43`) |
| Gradle project name | `EmailPlus_Android` (`MF/settings.gradle.kts:1`) | `HPTeams_Android` (`TM/settings.gradle.kts:21`) |
| SDK levels | min 31, target and compile 35, Kotlin 1.9.25, AGP 8.13.1, Java 11 (`MF/build.gradle.kts:11-21`) | same (`TM/build.gradle.kts:2-11`) |
| Workpath platform | `LinkForDevice` 31.7, HPK schema v2.4 (`MF/packaging_release/hpk.xml:2,7-8`) | `LinkForDevice` 31.7, HPK schema v2.5 (`TM/packaging_release/hpk.xml:2,7-8`) |
| Entry point | `ui.splash.SplashActivity` (launcher), `CommonApp` application class (`MF/app/src/main/AndroidManifest.xml:24,36`) | `.ui.splash.SplashActivity`, `.app.CommonApp` (`TM/app/src/main/AndroidManifest.xml:10,21`) |
| Activities | 13: splash, email select, login, main, open source, information, print preview, new email, reply/draft email, settings, scan options, quick messages, admin consent (`MF/…/AndroidManifest.xml:35-122`) | 9: splash, main, open source, information, settings, scan preview, print preview, app guide, search (`TM/…/AndroidManifest.xml:20-81`) |
| Gradle modules | `:app`, `:OnGuardLib`, `:msgraph-sdk`, `:tokenautocomplete`, `:FloatingActionButton`, `:usermanagement` (`MF/settings.gradle.kts:3`) | `:app`, `:OnGuardLib`, `:usermanagement` (`TM/settings.gradle.kts:23-25`) |
| Architecture | MVP with RxJava 2; a provider indirection (`ServiceProviderManager`) left from a multi-mail-provider design, only "Outlook" configured (`MF/app/src/main/assets/provider.cfg:3-10`, `MFa/provider/ServiceProviderManager.kt:71-89`) | MVP with RxJava 2; presenters call Graph directly |
| Packaging | APK zipped with `hpk.xml` into `.hpk`; GitHub workflow builds on merge of a `release/*` PR labelled `release`, runs `:app:test :app:assembleRelease`, validates the MOC as XML, publishes HPK + SHA-256 + MOC as a GitHub release (`MF/.github/workflows/release.yml:27-31,130,148-154,198-206`) | Same pattern (`TM/notes:1-2`; `TM/.github/workflows/release.yml` exists, 219 lines, not read) |
| Remote-config schema (MOC) | `MF/app/moc_file/MailFlow.moc` (2,766 lines) + default `config.cfg` | `TM/data/moc/Teams.moc` (2,778 lines) |
| CI security | CodeQL and gitleaks workflows present (`MF/.github/workflows/`, not read) | same (`TM/.github/workflows/`, not read) |

### Shared and third-party libraries

| Library | MailFlow | Teams | What the app uses it for |
|---|---|---|---|
| `WorkpathLib-1.6.3.aar` (HP Workpath SDK) | yes (`MF/app/build.gradle.kts:182`) | yes (`TM/app/build.gradle.kts:149`) | Directly only `com.hp.workpath.api.access.AccessService` (`getCurrentPrincipal`, `signOut`) and `Result`; all scan and print use goes through CVL |
| `commonvaluablelibrary` (CVL) | 1.09.20 (`MF/app/build.gradle.kts:183`) | 1.09.22 (`TM/app/build.gradle.kts:151`) | SDK init and device capabilities, scan service and scan option model, print preview and print job, remote config, EULA screen, dialogs, settings screens, PDF preview renderer, Entra options screen, admin/SIO flags |
| `usermanagement-1.06.01.aar` (HPAM client library) | yes (`MF/usermanagement/build.gradle.kts:2`) | yes (`TM/usermanagement/build.gradle.kts`) | Token, token refresh, sign-in/out events, per-user properties, cloud endpoints |
| `cloudrendering-1.00.20.aar` | yes (`MF/app/build.gradle.kts:184`) | no | Only exception type, model classes and one "is format supported" helper are referenced; no rendering call is live (see 4.7) |
| `personalization-1.00.27.aar` | file present in `MF/app/libs/` but **not** in the dependency list; the app re-declares the two model classes itself (`MF/app/src/main/java/com/hp/print/lib/personalization/data/model/Token.kt`, `UserInfo.kt`) | no | Legacy |
| `quickaccess-1.00.11.aar` | no | yes (`TM/app/build.gradle.kts:150`) | Quick-access (pinned folders and files) UI and data model |
| `msgraph-sdk_1.50.04.aar` | module present, **not** a dependency of `:app` (`MF/app/build.gradle.kts:189-192`); replaced by Maven `microsoft-graph:5.34.0` plus a compatibility shim (`MF/app/src/main/java/com/microsoft/graph/extensions/GraphCompatibility.kt`) | no | Legacy |
| `OnGuardLib` (source module, JNI) | imported in two files; no call found in the app sources read (`MFa/Constants.kt:4`, `MFa/ui/print/PrintPreviewAppFragment.kt:20` uses only `FileUtils.deleteFile`) | Wrapped by `getAppPackageName()` and `getVaultClientId()` (`TMa/constant/Constants.kt:55-66`), but grep finds no caller of either wrapper in the app | Native "locker" for obfuscated values; effectively unused by both apps |
| Microsoft Graph Java SDK 5.34.0 | yes (`MF/app/build.gradle.kts:186`) | yes (`TM/app/build.gradle.kts:135`) | Graph requests |
| Others | Retrofit 2.5, OkHttp, RxJava 2, Gson, jsoup, android-mail, PdfiumAndroid, pdfbox-android, security-crypto, `tokenautocomplete` (recipient chips), `FloatingActionButton` | Retrofit 2.5, OkHttp 3.12, RxJava 2, Gson, Picasso, PdfiumAndroid, pdfbox-android, security-crypto | |

---

## 4. Findings — MailFlow

### 4.1 Start-up and session flow

1. `SplashActivity.onCreate` starts CVL initialisation (`presenter.initCVL()`), which loads the Workpath SDK and device capabilities (`MFa/ui/splash/SplashActivity.kt:87`, `MFa/ui/splash/presenter/SplashPresenter.kt:19-53`). Failure "SDK not installed" shows a text dialog; any other failure raises error **MF01** with a Retry button (`SplashPresenter.kt:40-45`).
2. User data is loaded (`MailFlowUserDataStore.load`), then remote config (`AppConfigHelper.loadAppData`) (`SplashActivity.kt:344-349`).
3. If the device user is a **local device administrator** (and the build is not debug) the app clears all user data and opens Settings only; it never shows mail (`SplashActivity.kt:459-483`).
4. If nobody is signed in at the device (`AccessService.getCurrentPrincipal` not OK or not authenticated) the app tries to launch HPAM by package name, passing its own app UUID as `EXTRA_APP`, and finishes; if HPAM is not installed it shows a "please sign in" panel with Exit (`SplashActivity.kt:159-181,290-318`).
5. Otherwise it subscribes to HPAM's user-management service and takes the token (4.2), then opens `MainActivity` (`SplashActivity.kt:435-457,531-538`).
6. The EULA check (`checkEula`, `callEulaActivity`) exists but nothing calls it: a case-insensitive grep for `checkEula()` over the whole app source returns only its definition (`SplashActivity.kt:365`); `callNextActivity` goes straight to main. The EULA settings menu entry is commented out too (`MFa/ui/settings/SettingsAppFragment.kt:93`). The EULA step is disabled in this build.

### 4.2 How the user's token is obtained

Mechanism and classes (all from the `usermanagement` AAR, package `com.hp.print.hpauthenticationmanager`):

| Step | Class and call | Source |
|---|---|---|
| Permission to bind | Manifest declares and uses `com.hp.print.hpauthenticationmanager.permissions.TokenLibraryPermission` | `MF/app/src/main/AndroidManifest.xml:17-18` |
| Bind | `UserManagementProxy(context).subscribeUserManagement(UserManagementCallback)`; returns false or throws when HPAM is absent | `MFa/ui/splash/SplashActivity.kt:66,271-288` |
| Service ready | `onUserManagementReady(userManagement)`; the object is parked in a global `UserManagementHolder` | `SplashActivity.kt:183-187`, `MFa/UserManagementHolder.kt:6-8` |
| Current token | `userManagement.getToken()` (a string, may be null or empty) | `SplashActivity.kt:187,439` |
| Decision | `SessionAccessPolicy.resolve(localAdmin, token)` → `LOCAL_ADMIN_SETTINGS`, `SIGN_IN_REQUIRED` or `CLOUD_DATA`. The file's own comment: the token "must be supplied by HP Authentication Manager, not app storage" | `MFa/auth/SessionAccessPolicy.kt:3-11` |
| Events | `userManagement.subscribeToUserInfo(UserInfoCallback)` with `onUserSignIn(token)`, `onNewAccessToken(token)`, `onUserSignOut()` | `SplashActivity.kt:206,223-254`; the same block is repeated in `MFa/ui/main/MainActivity.kt:168-225` (grep) |
| Refresh on 401 | `userManagement.getNewToken { newToken -> … }`, wait up to 10 s on a latch, store, replay the request once | `MFa/HttpClient.kt:48-85` |
| Where the token sits | `EncryptedSharedPreferences` file `SecuredPreferences`, keys `access_token` and `tenant_id` (AES-256 GCM values, SIV keys) | `MFa/SecuredPreferences.kt:13-36` |
| How Graph gets it | `AuthenticationManager : IAuthenticationProvider` returns the stored token for every request | `MFa/microsoft/auth/AuthenticationManager.kt:24-45` |
| Claims read | The app base64-decodes the JWT payload and reads `tid`, `oid`, `given_name`, `family_name`. No signature check (not needed for display, but see section 9). `getString` throws if a claim is missing, and the catch rethrows as `RuntimeException` | `SplashActivity.kt:509-529` |
| Endpoints | `CloudConfigProxy(context).cloudConfigFlow` gives a `CloudConfig` with `graphApi` and `oAuthAuthority`; the Graph client's `serviceRoot` is set to `graphApi + "/v1.0"`. So national clouds are selected by HPAM, not by the app | `MFa/microsoft/auth/MSAppAuthHelper.kt:50-75` |
| Sign-out | Menu "Sign out" calls Workpath `AccessService.signOut` then local logout; "Exit" does local logout only | `MFa/ui/main/MainActivity.kt:419-431` |
| Data wipe | On sign-out, disconnect, admin, or missing token: token, tenant id, name fields, user-data caches and both preference files cleared; every `EmailPlus_AppData*` folder deleted | `SplashActivity.kt:256-270`, `MFa/userdata/MailFlowUserDataStore.kt:116-122` |

**Fallback sign-in of its own: present in source, not reachable.**

- `MicrosoftLogInFragment` implements authorization-code sign-in in a WebView: builds `{oAuthAuthority}/common/oauth2/v2.0/authorize?client_id=…&scope=…&response_type=code&redirect_uri=…[&domain_hint=…]`, intercepts the redirect, and posts the code to `/common/oauth2/v2.0/token` (`MFa/microsoft/login/MicrosoftLogInFragment.kt:81-212`, `MFa/microsoft/auth/MSAppAuthHelper.kt:86-170`, `MFa/microsoft/constants/MSConstants.kt:3-13`). No PKCE parameters and no client secret are sent in that request (`MSAppAuthHelper.kt:122-126`).
- It is unreachable: `LoginActivity` carries the comment "We don't use this for MailFlow" (`MFa/ui/login/LoginActivity.kt:15`); `LoginProvider.setProvider(...)` is commented out (`MFa/provider/ServiceProviderManager.kt:76`); `SplashActivity.callLoginActivity`, `callEmailSelectActivity` and `showAdminConsentDialog` are private and have no caller (`SplashActivity.kt:485,540,549`; grep over `MFa/` shows the only other `callLoginActivity` is inside `EmailSelectActivity`, itself only reachable from those dead methods).
- `AdminConsentActivity` (WebView on `{oAuthAuthority}/common/adminconsent`, redirect `https://localhost`, captures `tenant=`) is likewise only reachable from the dead dialog (`MFa/tenant/AdminConsentActivity.kt:58-68,212-228`).
- Settings for "domain hint" and "URL address bar" still exist in config code (`MFa/AppConfigHelper.kt:205-207`) but their menu entries are commented out (`MFa/ui/settings/SettingsAppFragment.kt:99-102`).

Decision recorded: the port treats MailFlow as "token from the authentication component only"; the own-login code is legacy and is not a requirement.

### 4.3 User-facing functions and screens

| Function | Behaviour | Source |
|---|---|---|
| Folder list (left drawer) | Well-known folders first in fixed order: Inbox, Sent, Drafts, Deleted, Archive, Junk, Conversation history; Outbox hidden; then the user's other root folders; nested folders shown by depth | `MFa/microsoft/main/MicrosoftMainProviderImpl.kt:56-61,103-169` |
| Mail list | Per folder, newest first, incremental "read more" on scroll, refresh button, unread counts; filters All / Unread / Flagged / Has attachments | `MicrosoftMainProviderImpl.kt:221-244,575-590`; `MFa/provider/ServiceProviderManager.kt:75`; `MFa/ui/main/MainFragment.kt:232-259,382` (grep) |
| Search mail | Toolbar search box, results list, "no results" text | `MFa/microsoft/search/MicrosoftSearchProviderImpl.kt:28-48`; `MainFragment.kt:419,615,795` (grep) |
| Read mail | Header (sender initial, To, Cc with "+n"), HTML body in a WebView, inline images embedded; opening marks the message read | `MFa/microsoft/mail/MicrosoftMailProviderImpl.kt:37-88,104-176`; `MFa/ui/main/MailBodyFragment.kt:148-166` |
| Attachments panel | Tabbed panel from the mail body: view list and a print list with checkboxes and select-all; the message body itself appears as a printable item (`BODY_FOR_PRINT`) | `MailBodyFragment.kt:66-80` (offset listing); `MFa/ui/attachment/AttachmentViewFragment.kt:36-47`; `MFa/ui/attachment/AttachmentViewPaperAdapter.kt:31`; `MFa/ui/attachment/AttachmentViewListFragment.kt:122-170` |
| Print attachments / body | Select items → download (and convert) with progress "n of m" and Cancel → CVL print preview with print options → print | `AttachmentViewListFragment.kt:221-236,485-526`; 4.6 |
| New email with scan | Compose screen: To / Cc / Bcc recipient chips with people search, subject, rich-text body (WebView editor), scan button, scan settings, file name, page preview with arrows, attachment count badge, Send, save to Drafts | `MFa/ui/send/SendFragment.kt` (function list by grep; lines 232-327, 764-863, 1019-1114 read) |
| Reply | "Reply all" draft is created server-side, then edited in the same compose screen | `MFa/microsoft/send/MicrosoftSendProviderImpl.kt:119-168`; `MailBodyFragment.kt` footer handlers |
| Drafts | Open a draft, edit, add scans, remove attachments, save or send; back button offers save-to-drafts or discard | `SendFragment.kt:926-993,1377-1424` (grep and read); `MicrosoftSendProviderImpl.kt:47-76` |
| Forward | Not offered: a case-insensitive grep for `forward` over the whole app source finds one comment and no `createForward` call | `MicrosoftSendProviderImpl.kt:402` |
| People search / address book | Type-ahead on recipient fields calls people search; no separate address-book browser. `getContactList` returns an empty list | `MFa/microsoft/search/MicrosoftSearchContactProviderImpl.kt:22-53`; `MicrosoftMainProviderImpl.kt:602-607`; `SendFragment.kt:1007-1017` |
| Quick messages | Up to 5 canned body texts (3 defaults enabled), shown as a floating action menu in compose; options to auto-expand on reply and on new mail; edited in a dedicated screen; only for signed-in (SIO) users | `MFa/model/QuickMessage.kt:10-56`; `SendFragment.kt:561-627`; `MFa/ui/main/MainActivity.kt:398-410` |
| Remember me | Prompt and snackbar about saving the account to the device or HP cloud account | `MainFragment.kt:829-885` (grep); `MFa/ui/sio/RememberMeFragment.kt` (grep) |
| Overflow menu | App settings (admin or SIO), Quick messages (SIO), Information, Exit, Sign out | `MainActivity.kt:387-431` |
| Settings | Admin: default print options, default scan options, Microsoft Entra options. SIO users: sign-in management | `MFa/ui/settings/SettingsAppFragment.kt:83-106` |
| Information / open-source licences | Static pages from assets | `MFa/ui/information/` (not opened beyond grep) |

### 4.4 Microsoft Graph calls (MailFlow)

Base URL is `{cloudConfig.graphApi}/v1.0`. "SDK" = Graph Java SDK through the custom `HttpProvider` (401 → token refresh → one replay). "raw" = hand-built OkHttp or `URLConnection` request, which does **not** go through that refresh path.

| # | Method and endpoint | Purpose | Paging / limits | Path | Source |
|---|---|---|---|---|---|
| 1 | `GET /me/mailFolders?$top=200` | Folder tree | Only the first page is read; more than 200 folders are silently dropped | SDK | `MicrosoftMainProviderImpl.kt:81-90`; `MSConstants.kt:22` |
| 2 | `POST /$batch` with 8 × `GET /me/mailFolders/{wellKnownName}` | Resolve ids of inbox, sentitems, drafts, deleteditems, archive, junkemail, conversationhistory, outbox; cached in memory | One batch of 8; failure is logged and ignored | raw | `MicrosoftMainProviderImpl.kt:178-219` |
| 3 | `GET /me/mailFolders/{id}/messages/delta?$select=…` (+ `$skiptoken` or `$deltatoken`) | Mail list, "read more", new-mail check | Server page size; `Prefer: odata.maxpagesize=20` for Drafts only. `@odata.nextLink` skiptoken kept per folder for the next scroll; `@odata.deltaLink` token kept for new-mail polling; `@removed` entries drop from cache | SDK | `MicrosoftMainProviderImpl.kt:333-571`; `MSConstants.kt:16,18-20,23` |
| 4 | `GET /me/messages/{id}?$select=…` | Refresh one message | | SDK | `MicrosoftMainProviderImpl.kt:246-257` |
| 5 | `GET /me/messages/{id}?$select=body` | Body; cached in memory if ≤ 50 KB | | SDK | `MicrosoftMailProviderImpl.kt:90-102`; `MFa/Constants.kt:30` |
| 6 | `GET /me/messages/{id}/attachments?$select=id,name,contentType,size,isInline,…contentId` | Attachment list | First page only | SDK | `MicrosoftMailProviderImpl.kt:63-72`; `MSConstants.kt:15` |
| 7 | `POST /$batch` with `GET me/messages/{id}/attachments/{aid}` | Fetch inline images, rewrite `src="cid:…"` to `data:` URIs | Batches of 4 (`GRAPH_BATCH_LIMIT`); per-item failures logged and skipped | raw | `MicrosoftMailProviderImpl.kt:104-217`; `MSConstants.kt:26` |
| 8 | `PATCH /me/messages/{id}` `{isRead:true}` | Mark read | | SDK | `MicrosoftMailProviderImpl.kt:156-176` |
| 9 | `GET /me/messages?$search="kw"&$top=100&$select=…` | Mail search; `"` and `\` stripped from the keyword; HTTP 400 is turned into an empty result | First 100 only | SDK | `MicrosoftSearchProviderImpl.kt:28-48,105-113`; `MSConstants.kt:24` |
| 10 | `GET /me/people?$search="kw"` | Recipient suggestions; first scored e-mail address of each person | First page only | SDK | `MicrosoftSearchContactProviderImpl.kt:22-53` |
| 11 | `POST /me/sendMail` (`saveToSentItems=true`) | Send at once when the mail is new and has no attachment | | SDK | `MicrosoftSendProviderImpl.kt:78-84,263-274` |
| 12 | `POST /me/messages` | Create draft | | SDK | `MicrosoftSendProviderImpl.kt:218-230` |
| 13 | `PATCH /me/messages/{id}` | Update draft (subject, HTML body, recipients) | | raw | `MicrosoftSendProviderImpl.kt:237-261` |
| 14 | `DELETE /me/messages/{id}/attachments/{aid}` | Remove attachments the user deleted | | SDK | `MicrosoftSendProviderImpl.kt:374-395` |
| 15 | `POST /me/messages/{id}/attachments` (`fileAttachment`, base64 bytes) | Attach a file smaller than 3 MB | Whole file in memory | SDK | `MicrosoftSendProviderImpl.kt:41,407,415-437` |
| 16 | `POST /me/messages/{id}/attachments/createUploadSession`, then **one** `PUT {uploadUrl}` with `Content-Range: bytes 0-(n-1)/n` | Attach a file of 3 MB or more | Not chunked: the entire file is sent in a single PUT and is read into memory twice. If session creation fails the code logs and then throws "Upload session URL missing" | raw | `MicrosoftSendProviderImpl.kt:439-531` |
| 17 | `POST /me/messages/{id}/send` | Send the draft | | raw | `MicrosoftSendProviderImpl.kt:533-555` |
| 18 | `POST /me/messages/{id}/createReplyAll` then call 6 on the new draft | Reply | | SDK | `MicrosoftSendProviderImpl.kt:119-161` |
| 19 | `DELETE /me/messages/{id}` | Discard a draft | | SDK | `MicrosoftSendProviderImpl.kt:198-216` |
| 20 | `GET /me/messages/{id}/attachments/{aid}/$value` | Download attachment bytes | 60 s connect and read timeouts; whole file in memory when it is to be converted | raw (`URLConnection`) | `MicrosoftGraphPdfDownloadProviderImpl.kt:508-554,741-750` |
| 21 | `PUT /me/drive/special/approot:/MailFlowAS/{uuid}_{name}:/content` | Temporary upload of an Office file, a `.txt` wrapped in HTML, or the mail body HTML, into the user's OneDrive app folder | Simple upload, any size up to the 100 MB conversion cap (Graph's simple-upload limit is far lower: see section 6) | raw | `MicrosoftGraphPdfDownloadProviderImpl.kt:419-458` |
| 22 | `GET /me/drive/items/{id}/content?format=pdf` | Download the PDF rendition | Conversion error detected by CVL `ErrorUtils.isGraphConversionError` → "conversion timeout" message | raw | `MicrosoftGraphPdfDownloadProviderImpl.kt:460-487` |
| 23 | `DELETE /me/drive/items/{id}` | Remove the temporary file (in `finally`; failure only logged) | | raw | `MicrosoftGraphPdfDownloadProviderImpl.kt:488-501` |
| 24 | `GET /me` | Dead sign-in path only | | SDK | `MFa/microsoft/login/MicrosoftLoginProviderImpl.kt:29-37` |

**Scopes.** The app's own constant lists `mail.readwrite mail.send user.read people.read offline_access` (`MSConstants.kt:13`), used only by the dead sign-in. Calls 1–19 fit `Mail.ReadWrite`, `Mail.Send`, `People.Read`. Calls 21–23 need a Files scope (`Files.ReadWrite` or `Files.ReadWrite.AppFolder`, or the `Files.ReadWrite.All` that the HPAM registration holds per `START-HERE.md:52`). So printing any Office attachment or the mail body depends on the HPAM registration's Files permission and on the user having a OneDrive.

**Throttling and errors.**

- HTTP status is recovered by searching the exception message for `"400 :"`, `"401 :"`, `"403 :"`, `"404 :"`, `"409 :"`, `"429 :"`; anything else becomes 999 (`MFa/microsoft/error/MicrosoftErrorHandling.kt:72-94`).
- Mapping: 401 → `InvalidCredentialException` (message, then forced logout), 404 → file not found (or "mail does not exist" in body calls), 429 → `TooManyRequestsException` (a message only). 503 is in the mapping table but can never be produced, because the parser has no `"503 :"` branch (`MicrosoftErrorHandling.kt:62-70` against `72-94`).
- No `Retry-After` handling anywhere (grep `Retry-After` over `MFa/`: 0; positive control `Authorization` in the same tree: many hits).
- Presenters wrap most calls in RxJava `.retry(2)` with no delay (`MFa/Constants.kt:41`; `MFa/ui/send/presenter/SendPresenter.kt:50,79,99,216`; `MFa/ui/download/presenter/DownloadPresenter.kt:47,73`). `sendEmail` is deliberately not retried (`SendPresenter.kt:57-69`). A retried `saveToDrafts` for a new mail re-enters with `mail.id` already set after the first POST, so it patches instead of creating a duplicate (`MicrosoftSendProviderImpl.kt:53-59,229`); attachments already uploaded in the failed attempt are uploaded again because their local `id` is still empty (`MicrosoftSendProviderImpl.kt:401-403`) (inferred duplicate-attachment risk).
- Timeouts: connect 60 s, read/write 180 s, whole call 180 s (`MFa/NetworkTimeouts.java:6-8`).
- Graph request ids are logged on failure (`MicrosoftErrorHandling.kt:35-46`).

### 4.5 Scanning (MailFlow)

The app never calls the Workpath scan API itself.

| Step | What the app does | Source |
|---|---|---|
| Start | Forces scan preview ON, then starts CVL's `ScanSupportService` with action `REQUEST_SCAN` and a bundle: output directory = the app's private temp folder, destination = `ScanAttributes.Destination.ME` | `MFa/ui/send/presenter/SendPresenter.kt:106-124` |
| PDF password | If the chosen format supports encryption, encryption is on and no password is set, CVL's `EncryptionPasswordDialogFragment` is shown first | `MFa/ui/send/SendFragment.kt:764-773,865-889` |
| Result | Local broadcast `ACTION_SCAN_SERVICE` with extras `RESULT_SCAN_JOB_COMPLETE` (list of file paths), `RESULT_SCAN_JOB_CANCELED`, `RESULT_SCAN_JOB_FAIL`, `RESULT_SCAN_JOB_START_FAIL` | `SendFragment.kt:232-275` |
| Preview | PDF variants via CVL `PdfDocumentRenderer`; JPEG via an image pager (one file per page); any other format shows "preview unavailable" | `SendFragment.kt:246-254,277-307` |
| Naming | Default `Scan_<date>_<time>` in the device locale's date order; multi-file scans get `_001`, `_002` … suffixes (first file without suffix) | `MFa/Util.kt:78-105`; `SendFragment.kt:802-823` |
| Attach | Each scan file becomes a `NEW` attachment with its local path and size | `SendFragment.kt:775-790` |

Scan settings offered are CVL's `ScanSubOptionsFragment` (mode `FROM_SEND`) (`MFa/ui/send/option/ScanOptionFragment.kt:31-40`). The administrator's defaults, as declared in the remote-config schema, are: file type, resolution, quality, original sides, original size, content orientation, optimise text/picture, cropping, blank-page suppression, multi-feed detection, colour mode, sharpness, darkness, contrast, background clean-up, compression, PDF encryption, TIFF colour and mono compression, and "split attachment by page" with "max pages per attachment" (`MF/app/moc_file/config.cfg:110-393`). Shipped defaults include PDF, 300 dpi, portrait, and split disabled (`config.cfg:119,133,189,385`).

- **File formats:** the code names PDF, PDF/A, searchable PDF, searchable PDF/A and JPEG, and has an "else" for the rest (TIFF settings exist in the schema) (`SendFragment.kt:246-253`; `config.cfg:351-365`).
- **OCR:** the app has no OCR code; "searchable PDF" is a document-format value of CVL's `ScanDocumentFormatOption`. Whether the device or CVL performs the OCR is for the shared-library lane. (inferred: device-side)
- **Multi-page:** PDF = one file with pages; JPEG = one file per page (`SendFragment.kt:299-303`).
- **Size limit:** the sum of all non-deleted attachment sizes must be **strictly below** the configured limit, otherwise a dialog names the limit in MB (`SendFragment.kt:1043-1049,1104-1114`). The limit comes from remote config through CVL `MsEntraHelper.getAttachmentSizeLimit` (MB → bytes) (`MFa/AppConfigHelper.kt:164-167`); schema key `msEntraConfig / attachmentsSizeLimit`, shipped default 35 (`config.cfg:404-413`); the compile-time fallback is a CVL constant (`MicrosoftSendProviderImpl.kt:42-43`).
- **Debug build ("tablet mode"):** no scanner; test files from assets are broadcast as a fake scan (`SendPresenter.kt:125-190`).

### 4.6 Printing (MailFlow)

| Step | What happens | Source |
|---|---|---|
| Choose | One item → `downloadFile`; several → `downloadMultiFiles` with progress | `MFa/ui/attachment/AttachmentViewListFragment.kt:221-236` |
| Mail body | Body HTML fetched (calls 5, 6, 7 with inline images embedded), uploaded as `mail_body.html`, fetched back as PDF (calls 21–23) | `MicrosoftGraphPdfDownloadProviderImpl.kt:367-392,560-631` |
| Office and text attachments | Extensions `doc, docx, xls, xlsx, ppt, pptx, rtf, odt, odp, ods, txt`, and size ≤ 100 MB: bytes downloaded, (`.txt` wrapped in an HTML `<pre>` page), uploaded and fetched back as PDF | `MicrosoftGraphPdfDownloadProviderImpl.kt:63,127-185,693-703` |
| Everything else | Downloaded as-is to the temp folder (PDF, JPEG and whatever the device prints natively) | `MicrosoftGraphPdfDownloadProviderImpl.kt:188-208` |
| Free space | Checked against the attachment size before download | `MicrosoftGraphPdfDownloadProviderImpl.kt:121-124`; `MFa/DirectoryHelper.kt:105-116` |
| Hand to print | One CVL `TaskConfiguration` per file (random id, display name, local path), filled from the current print options by `buildTaskConfigurationFromOptions`, passed to `PrintPreviewAppActivity`, which hosts CVL's `PrintPreviewFragment` | `AttachmentViewListFragment.kt:485-526`; `MFa/ui/print/PrintPreviewAppActivity.kt:33-69` |
| Print | Entirely inside CVL (`PrintPreviewFragment.startPrinting`): Workpath print API or IPP is decided there, not here | shared-library lane |

Print options an administrator can default: copies, sides, colour mode, paper size, paper type, tray, collate (`config.cfg:7-104`).

Two older conversion paths remain in source but are not live:

- **Android WebView HTML→PDF** (`Html2Pdf`, uses the hidden `android.print` package and 600 dpi, no margins, paper size from the print option) is called only when a download result carries `downloadHtmlFullPath` with status `NONE` (`AttachmentViewListFragment.kt:268-273,297-301,354-392`; `MFa/utils/Html2Pdf.kt:21-69`). Nothing ever assigns that field (grep for `downloadHtmlFullPath =` over the app source: 0 hits; control: the field is read in 6 places in `AttachmentViewListFragment.kt`), so the path cannot run. `PrintPreviewAppFragment` (re-renders the body when paper size changes) is not instantiated by `PrintPreviewAppActivity`, which creates the CVL base class (`PrintPreviewAppActivity.kt:61`) (inferred: unused).
- **Gotenberg / LibreOffice conversion service** (`GotenbergCloudRenderingRequestJob`): posts a file to `/forms/libreoffice/convert` with `pdfa=PDF/A-1b`, authenticating with a client-credentials token. The class has no instantiation anywhere in `MFa/` (grep for the class name finds only its own file). It contains hardcoded credentials: see section 9.

### 4.7 Temporary files and clean-up

- Working folder: `<app files dir>/EmailPlus_AppData_<yyyyMMddHHmmss>`, with `Preview` and `Print_<timestamp>` sub-folders (`MFa/DirectoryHelper.kt:11-67`).
- Scans, downloaded attachments and converted PDFs all land there.
- Deleted when: the user signs out, HPAM disconnects, an admin is detected, the token is missing (`SplashActivity.kt:256-270`); an activity flagged `isTerminateApp` is destroyed (`MFa/base/BaseAppCompatActivity.kt:38-44`); and by `clearApp()` on fatal dialogs (`MFa/Util.kt:182-185`). Deletion matches every folder whose name contains `EmailPlus_AppData`, so leftovers of a crashed session go at the next clean-up (`DirectoryHelper.kt:69-93`).
- There is **no delete after a successful send or print**; files stay until one of the events above. (inferred from absence of a delete call in `SendPresenter` and the send provider)
- Release builds set `FLAG_SECURE` on every activity (no screenshots) (`BaseAppCompatActivity.kt:22-26`); `allowBackup=false`, cleartext traffic off (`MF/app/src/main/AndroidManifest.xml:25,33`).
- In-memory mail cache per folder (`MailListInfo.mailInfoList`) lives for the process.

### 4.8 Per-user data, configuration, licensing, accounting

- **Per-user roaming data:** seven properties prefixed `mailflow.` (`auth_token`, `user_profile`, `remember_me`, `eula`, `recent_sites`, `recent_site_searches`, `quick_message`) are read with `UserManagement.getUserProperty(name){…}` and written with `updateUserProperty(name, json)`; a local `SharedPreferences` copy is the fallback (`MFa/userdata/MailFlowUserDataStore.kt:16-27,53-103,244-268`). Where HPAM keeps them is the HPAM lane's question. `recent_sites` and the `auth_token` slot are leftovers (a SharePoint-style field and the dead sign-in's token).
- **Remote configuration:** CVL `ConfigHelper` / `RemoteConfigHelper` with frames `printConfig`, `scanConfig`, `msEntraConfig` (`MF/app/moc_file/config.cfg:7,110,404`) and an app frame holding `adminOptIn`, `msDomainHint`, `urlAddressBar` (`MFa/AppConfigHelper.kt:204-207`). The MOC file is the schema the HP management console renders; its comment says the description is the frame title "in the HPCC" (`MF/app/moc_file/MailFlow.moc:6`).
- **Licensing:** none in app code. Case-insensitive grep for `license|licence` over both apps' sources finds only the open-source-licences page (`MFa/ui/information/OpenSourceActivity.kt:19`, `TMa/ui/information/OpenSourceActivity.kt:14,38`).
- **Job accounting / statistics:** none in app code. Grep for `statistic|jobdata|accounting|loganalytics|HpamPrinterLogs` over both apps' sources: 0 hits (positive control in the same run: 13 `import` lines counted in `CommonApp.kt`). If scan and print jobs are reported, CVL or HPAM does it.
- **Build-time fields:** `API_K_MF` (from an untracked `config.properties`, `"null"` in release), `CLIENT_ID`, `EMAIL_PLUS_TOKEN`, `EMAIL_PLUS_BODY` (`MF/app/build.gradle.kts:11-21,60-84`).

### 4.9 Error codes (MailFlow)

Only two coded errors exist in the source (case-insensitive grep for a quoted two-letter-two-digit code over `MF/app/src/main/java`: 2 hits):

| Code | Text shown | Trigger | Source |
|---|---|---|---|
| MF01 | "Initializing error" / "Trying to load Device capabilities" | CVL initialisation returns an error other than "SDK not installed" at splash; device-capability load fails in the main screen; the SDK is still not initialised 10 s after the user pressed Print | `MFa/model/ErrorData.kt:14-20`; `SplashPresenter.kt:44`; `MFa/ui/main/presenter/MainPresenter.kt:40-51` (lines 20–60 read); `MFa/ui/download/presenter/DownloadPresenter.kt:85-103`; `MFa/Util.kt:62` |
| MF03 | "Connection error" / "Unable to communicate to Azure outlook services" | Any failure that is not one of the 17 named exception types, after the retries (`shownWithRetryDialog`); wired in the main (folder and mail list), search and download presenters | `ErrorData.kt:22-28`; `MFa/exception/ExceptionAlertMessageUtil.kt:94-119`; `DownloadPresenter.kt:54,78`; `MFa/ui/main/presenter/MainPresenter.kt` and `MFa/ui/search/presenter/SearchPresenter.kt` (grep, file-level) |

Both show a full-screen panel with the code as a link to the help article, Retry and Exit (`SplashActivity.kt:94-117`). There is no MF02 or MF04+ in this source. These two messages are hardcoded English, not string resources.

Uncoded errors, by exception type (`MFa/exception/CommonException.kt:5-21`; texts chosen in `ExceptionAlertMessageUtil.kt:23-91`): invalid credentials (401, forces logout), too many requests (429), network I/O, unable to get data, download, upload, search, invalid path, folder missing, file not found (404), insufficient storage, unsupported format, mail does not exist (404 on body), PDF conversion timeout, PDF converter API error, SDK error (with and without app termination).

### 4.10 Localisation (MailFlow)

- UI strings: English base (165 strings) and de, es, fr, it, pt (157 each) (`MF/app/src/main/res/values*/strings.xml`, counted); the build restricts resources to those six (`MF/app/build.gradle.kts:52`).
- EULA HTML in EN, DE, ES, FR, IT, PT (`MF/app/src/main/assets/`).
- MOC descriptions additionally carry `ja_JP` (`MF/app/moc_file/MailFlow.moc:8-14`).
- Layout is locked to landscape, RTL off (`MF/app/src/main/AndroidManifest.xml:30,37`).

---

## 5. Findings — Teams

### 5.1 Start-up, token, session

Same pattern as MailFlow, same library, same class names:

- Bind `UserManagementProxy`, take `getToken()`, apply `SessionAccessPolicy` (`CLOUD_FILES` / `LOCAL_ADMIN_SETTINGS` / `SIGN_IN_REQUIRED`), subscribe to `UserInfoCallback`, launch HPAM by package name when no session, local admin goes to Settings only (`TMa/ui/splash/SplashActivity.kt:150-220,275-277,419-439,485-494`, grep with line numbers; `TMa/auth/SessionAccessPolicy.kt:3-11`).
- Token stored in `SecuredPreferences.accessToken`; Graph SDK gets it from `AuthenticationManager` (`TMa/auth/AuthenticationManager.kt:14-24`).
- Refresh on 401 is an OkHttp `Authenticator` (`SessionAuthenticator`): `userManagement.getNewToken{…}`, 10 s latch, replay with the new bearer (`TMa/auth/SessionAuthenticator.kt:19-59`). It is attached to the shared Graph client and to the quick-access batch client (`TMa/auth/AppAuthManager.kt:36-45`; `TMa/ui/main/presenter/QuickAccessPresenter.kt` client builder).
- Endpoints from HPAM's `CloudConfigProxy`: `serviceRoot = {graphApi}/v1.0` (`AppAuthManager.kt:55-79`).
- **No own sign-in at all.** There is no login activity in the manifest (`TM/app/src/main/AndroidManifest.xml:20-81`); the authorize and token URLs are commented out and marked not to be used (`TMa/auth/AppAuthConstants.kt:8-11`). `SplashPresenter.attestation()` is a stub that reports success (`TMa/ui/splash/presenter/SplashPresenter.kt:53-55`); `URLStore` and `HttpHeader` (`/tokenProxy/v1/token`, `x-mode`, `x-token`) are remnants of an older token-proxy design (`TMa/util/URLStore.kt:5`, `TMa/attestation/HttpHeader.kt:5-6`).
- Logout calls `{oAuthAuthority}/common/oauth2/v2.0/logout` with the redirect URI, without credentials, then clears the stored token (`AppAuthManager.kt:100-128`; `TMa/ui/logout/presenter/LogoutPresenter.kt:25-36`).
- Extra network feature: `FallbackDns` caches up to 10 resolved IPs per host in plain `SharedPreferences` and reuses them when system DNS fails (`TMa/util/FallbackDns.kt:15-40,48-57`).
- Scope constant (documentation of intent, not used to sign in): `Team.ReadBasic.All Channel.ReadBasic.All User.Read offline_access Files.ReadWrite.All ChannelMessage.Send` (`AppAuthConstants.kt:16`).

### 5.2 User-facing functions and screens

Main view types: `QUICK_ACCESS, MY_TEAMS, MY_CHANNELS, MY_FILES, RECENT, QUICK_PRINT, QUICK_SCAN` (`TMa/ui/main/base/MainViewType.kt`).

| Function | Behaviour | Source |
|---|---|---|
| My teams | List of the user's joined teams | `TMa/ui/main/presenter/TeamsPresenter.kt:35-54` |
| Channels | Channels of a team | `TMa/ui/main/presenter/ChannelsPresenter.kt:32-49` |
| Channel files | The channel's files folder and sub-folders, list or grid with thumbnails, sorting by modified time or name (asc/desc), optional SharePoint-style column selection, sort and group-by (CVL `sharepoint.columns` classes) | `TMa/ui/main/presenter/FilesPresenter.kt:74-119,153-243`; `TMa/sort/SortingType.kt`; `TMa/storage/UserPreferencesStore.kt:108-133` |
| File operations | Rename, delete (multi-select), create folder | `FilesPresenter.kt:253-300,312-417,424-510` |
| Search | Search inside a channel's files folder; recent search terms remembered | `TMa/ui/search/presenter/SearchPresenter.kt:25-88`; `UserPreferencesStore.kt:99-102` |
| Recent | The user's recent drive items | `TMa/ui/main/presenter/RecentPresenter.kt:44-63` |
| Print a file | From files, recent, search or quick access: download (convert Office to PDF) → preview with options, or **direct print** without preview | `TMa/ui/main/presenter/DownloadPresenter.kt:85-91`; `TMa/ui/main/MainActivity.kt:1438-1492` (grep; 1474-1492 read) |
| Print a folder | From quick access: prints the files of a pinned folder, at most 10 files per folder | `DownloadPresenter.kt:448,761-814`; `TMa/constant/Constants.kt:34` |
| Scan to a channel folder | Scan preview screen with file name, duplex shortcut, scan options; upload to one or several destination folders; optional message posted to the channel with the files attached | `TMa/ui/scan/presenter/ScanPreviewPresenter.kt:53-302`; `TMa/ui/scan/ScanDescriptionAppFragment.kt:161-180` |
| Quick access | Pinned print items and pinned scan destinations (max 10 pins each), nicknames, "quick print" option, synchronised against Graph at open | `Constants.kt:35`; `MainActivity.kt:1091-1109` (grep); `QuickAccessPresenter.kt:45-135`; `quickaccess` AAR |
| App guide | First-run tutorial with fake list items | `TMa/ui/appguide/` (grep only) |
| Settings | Admin: print defaults, scan defaults; SIO users: sign-in management, quick-access options | `TMa/ui/settings/SettingsAppFragment.kt:78-86` (grep); `TMa/ui/settings/quickaccess/` |
| Small panels | Layout variants for 4.3-inch panels (`is4p3InchScreen`, `values-sw340dp`) | `TMa/ui/scan/ScanPreviewAppActivity.kt:107,120`; `TM/app/src/main/res/` listing |
| **Chats** | **Not present.** Case-insensitive grep for `.chats(`, `/chats`, `me/chats` over `TMa/`: 0 hits; every `ChatMessage` hit is the channel-message post (positive control: 19 `chatMessage` hits in the same grep) | `TMa/ui/scan/presenter/ScanPreviewPresenter.kt:263-301` |

Functions hide themselves when the device lacks a capability: `CommonSDKUtil.INSTANCE.isPrintSupport` / `isScanSupport` gate the print and scan entry points across the UI, and choose the default view (`MainActivity.kt:221-223` and about 40 further call sites in the grep).

### 5.3 Microsoft Graph calls (Teams)

All through the Graph Java SDK on one OkHttp client (timeouts 60 s connect, 180 s read/write/call: `TMa/NetworkTimeouts.kt`), except where marked raw.

| # | Method and endpoint | Purpose | Paging / limits | Source |
|---|---|---|---|---|
| 1 | `GET /me/joinedTeams` | Teams list | Follows `nextPage` to the end | `TeamsPresenter.kt:35-54` |
| 2 | `GET /teams/{id}/channels` | Channels | Follows `nextPage` | `ChannelsPresenter.kt:32-49` |
| 3 | `GET /teams/{id}/channels/{cid}/filesFolder` | Resolve the channel's drive item (drive id + item id) | | `FilesPresenter.kt:74-83`; `SearchPresenter.kt:61-65` |
| 4 | `GET /drives/{driveId}/items/{itemId}/children?$expand=thumbnails($select=large)` | Folder listing | Follows `nextPage` | `FilesPresenter.kt:98-119` |
| 5 | Same listing by other addressing: `/drives/{d}/root/children`, `/me/drive/items/{id}/children`, `/me/drive/root:/{path}:/children`, `/me/drive/root/children`, with `$select=id,createdDateTime,lastModifiedDateTime,name,parentReference,size,folder,file,remoteItem,content.downloadUrl` | Sub-folder navigation | Follows `nextPage` | `FilesPresenter.kt:153-243`; `TMa/constant/TeamsConstants.kt:5` |
| 6 | `PATCH /drives/{d}/items/{id}` or `/me/drive/items/{id}` | Rename | | `FilesPresenter.kt:272-300` |
| 7 | `DELETE /drives/{d}/items/{id}` or `/me/drive/items/{id}` | Delete | | `FilesPresenter.kt:368-417` |
| 8 | `POST …/children` (folder facet) | Create folder | | `FilesPresenter.kt:444-510` |
| 9 | `GET /drives/{d}/items/{id}/search(q='…')?$select=…&$top=400` | Search under the channel folder | `$top=400`, follows `nextPage` | `SearchPresenter.kt:76-88` |
| 10 | `GET /me/drive/recent?$select=…` | Recent files | Follows `nextPage`; UI cap constant 400 | `RecentPresenter.kt:44-63`; `Constants.kt:36` |
| 11 | `GET /drives/{d}/items/{id}/content?format=pdf` | Office → PDF, streamed to a temp file | Only `doc, docx, xls, xlsx, ppt, pptx`; refused above 80 MB (40 MB for Excel) | `DownloadPresenter.kt:147-234,593-649`; `TMa/util/Utils.kt:242-262` |
| 12 | `GET /drives/{d}/items/{id}` to read `@microsoft.graph.downloadUrl`, then a raw `GET` of that pre-authenticated URL | Download of files that need no conversion | Streamed, 60 s / 180 s timeouts | `DownloadPresenter.kt:298-379,677-730` |
| 13 | `PUT /drives/{d}/items/{folderId}:/{name}:/content?@microsoft.graph.conflictBehavior=fail` | Upload a scan smaller than 3.5 MB | Whole file in memory | `ScanPreviewPresenter.kt:49,183-206` |
| 14 | `POST /drives/{d}/items/{folderId}:/{name}:/createUploadSession` (`conflictBehavior=fail`), then the SDK's `LargeFileUploadTask.upload()` | Upload a scan of 3.5 MB or more, chunked by the SDK with its default chunk size | Proper chunked session (unlike MailFlow) | `ScanPreviewPresenter.kt:209-255` |
| 15 | `POST /teams/{id}/channels/{cid}/messages` | Post a channel message whose attachments are `reference` items: id = the GUID parsed out of the uploaded item's `eTag`, `contentUrl` = the item's `webUrl` with `&action=default…` cut off, name = file name; the body gets one attachment placeholder per file | Fails (throws) if no GUID is found in the eTag | `ScanPreviewPresenter.kt:257-302` |
| 16 | `POST /$batch` with `GET drives/{d}/items/{id}?$select=…[&$expand=thumbnails]` per pin | Check and refresh quick-access pins | One batch for all pins: up to 20 requests (10 print + 10 scan), which is exactly Graph's batch limit | raw: `QuickAccessPresenter.kt:45-135`; `Constants.kt:35` |

**Scopes needed:** `Team.ReadBasic.All` (1), `Channel.ReadBasic.All` (2), `Files.ReadWrite.All` (3–14, 16; channel files live in the team's SharePoint site), `ChannelMessage.Send` (15), as the app's own constant states (`AppAuthConstants.kt:16`).

**Throttling and errors:** same message-text parsing as MailFlow, with 403, 503 and 507 added: 401 invalid credentials, 403 no permission, 404 not found, 409 duplicate name, 429 and 503 too many requests, 507 insufficient storage (`TMa/error/MicrosoftErrorHandling.kt:31-66`). No `Retry-After` use; **no RxJava retry at all** (grep `.retry(` over `TMa/`: 0; positive control `subscribeOn` in `DownloadPresenter.kt`: 4). Whatever retry the Graph SDK's default OkHttp client applies is the only one (`AppAuthManager.kt:36-38` builds on `HttpClients.createDefault`) (inferred: the SDK's built-in retry handler is active; not verified here). A conversion failure recognised by CVL `ErrorUtils.isGraphConversionError` becomes a "timeout" message (`DownloadPresenter.kt:225-229`).

**Caching:** an in-memory `NavigationCache` keeps teams, channels per team and up to 50 folder listings (`TMa/storage/NavigationCache.kt:8-61`).

### 5.4 Scanning (Teams)

- The scan screen is CVL's `ScanPreviewFragment`, subclassed as `ScanPreviewAppFragment` and hosted by `ScanPreviewAppActivity`, which passes the temp folder path, the destination folder item(s), team id and channel id (`TMa/ui/scan/ScanPreviewAppActivity.kt:47-72`).
- CVL performs the scan and reports through the same local broadcasts as MailFlow: `RESULT_SCAN_JOB_COMPLETE` (file list), `RESULT_SCAN_JOB_START_FAIL` (error int), plus mode events `REQUEST_SCAN_UPLOAD_START_MODE`, `REQUEST_SCAN_PREVIEW_START_MODE`, `REQUEST_SCAN_PREVIEW_ERROR_END_MODE`, `REQUEST_SCAN_PREPARE_JOB_END_MODE` (`TMa/ui/scan/ScanPreviewAppFragment.kt:160-188`, grep).
- On "upload start" the presenter uploads every scanned file to every chosen destination (calls 13 or 14), with cancel support and a per-destination result list, then optionally posts the channel message (call 15) (`ScanPreviewPresenter.kt:83-180`).
- Naming: the user's file name plus extension; multi-file scans add `_001` … (first file unsuffixed), trimmed to 255 characters (`ScanPreviewPresenter.kt:304-350`). Name clashes are an error (`conflictBehavior=fail` → 409 "duplicate name").
- Scan settings: the same CVL option set and the same MOC schema as MailFlow, including `splitAttachmentByPage` (`TM/data/moc/Teams.moc:1063-2725`, ids by grep). A duplex shortcut is on the description panel (`TMa/ui/scan/ScanDescriptionAppFragment.kt:171-173`).
- No size limit is applied by the app before upload (no size check in `ScanPreviewPresenter.kt:83-255`).
- Quick scan: scanning straight to a pinned destination from the quick-access view (`TMa/ui/main/QuickAccessFragment.kt:821-830`, grep).

### 5.5 Printing (Teams)

- Convert or download to the temp folder (calls 11, 12), free-space check first (`DownloadPresenter.kt:158-166,309-311`).
- With preview: `TaskConfiguration.create(id, name, path)` + `buildTaskConfigurationFromOptions` → `PrintPreviewAppActivity` → CVL `PrintPreviewFragment` (or a preview-only fragment when the device cannot print) (`MainActivity.kt:1438-1470`; `TMa/ui/print/PrintPreviewAppActivity.kt:49-76`, grep).
- Direct print: `PrintJobProgressHandler.getInstance().init(activity)` then `startPrintWithSetParams(paths, true, listener)`; the listener clears the selection on `ErrorReason.NO_ERROR` (`MainActivity.kt:1476-1492`).
- Printable formats = what CVL says the device prints natively (`CommonSDKUtil.isSupportedFileFormatForPrint`) plus the six Office extensions (`Utils.kt:238-248`).
- The Workpath print API or IPP choice is inside CVL (shared-library lane).

### 5.6 Temporary files, per-user data, configuration, errors, localisation

- **Temp files:** `<app files dir>/HPTeams_AppData_<timestamp>` with `Preview` and `Print_<timestamp>`; same delete-by-name-match routine (`TMa/util/DirectoryHelper.kt:11-107`); `clearApp()` exists (`Utils.kt:47`). Same remark as MailFlow: no per-job delete seen in the presenters read.
- **Per-user roaming data** through `UserManagement` properties prefixed `teams.`: `quick_access`, `recent_searches`, `columns_state`, `remember_me_save`, `remember_me_do_not_show_again`, `eula_accepted`, `eula_accepted_opt_in`; EULA flags are also kept in a local preferences file keyed by the token's `preferred_username` (`UserPreferencesStore.kt:16-24,153-207`).
- **Remote config:** frames `printConfig` and `scanConfig` only; no `msEntraConfig` frame (`Teams.moc:5,1063`); app frame `adminOptIn`, `domainHint`, `urlAddressBar` (`TMa/util/AppConfigHelper.kt:101-104`).
- **Licensing, job accounting:** none in app code (greps in 4.8 covered both apps).
- **Error codes:** Teams has **no coded errors**. Case-insensitive grep for a quoted two-letter-two-digit code, `ErrorData`, `globalErrorLiveData` or `hpauthsuite` over `TMa/`: 0 hits (the same pattern finds 2 in MailFlow). SDK init failure shows a plain dialog (`SplashPresenter.kt:38-44`). Exception types add to MailFlow's list: file too large, no permission, duplicated name, folder not created (`TMa/error/CommonException.kt:17-21`).
- **Localisation:** English base 196 strings; de, es, fr, it, pt 195 each; resource folders also exist for `in` (Indonesian) and `zh-rTW`, and EULA files for IN and TW (`TM/app/src/main/res/` listing; `TM/app/src/main/assets/`). MOC locales: en_US, de_DE, es_ES, fr_FR, it_IT, pt_PT, ja_JP (`Teams.moc`, counted).

---

## 6. What this means for the port

### 6.1 What runs on the device today, and what a server needs instead

| Behaviour today | Why it is device-bound | Server-side equivalent and what it needs from the device |
|---|---|---|
| Token from HPAM over Android IPC (4.2, 5.1) | Same-device service binding, custom permission, in-process callbacks | The server's authentication component must expose the same contract as a server API: current token for "the user signed in at device X", refresh on demand, sign-in / new-token / sign-out events. The apps need only an access token for Graph and four claims (`tid`, `oid`, names, `preferred_username`). Needs from the device: the identity of the device session (which printer, which signed-in user) on every panel request |
| "Is a user signed in at the device?" via Workpath `AccessService.getCurrentPrincipal`; sign-out via `AccessService.signOut` (4.1, 4.2) | Workpath API | The OXPd authentication service: session state and a way to end the device session from the server |
| Local-admin branch: admin sees Settings only (4.1) | Workpath principal role | A device-admin signal from the OXPd session, or move these settings to the server's admin console entirely |
| Launch HPAM when no session (4.1) | Android intent | Redirect the panel browser to the server's sign-in page, carrying the return target (the app id the Workpath apps pass as `EXTRA_APP`) |
| Native panel UI (activities, fragments, WebView editor, recipient chips, landscape, 4.3-inch variants) | Android UI toolkit | Web pages served to the panel's embedded browser. Needs: browser capabilities of each OXPd generation (JavaScript level, on-screen keyboard behaviour, screen sizes) |
| Scan: CVL service writes files into the app's folder, broadcasts paths (4.5, 5.4) | Scanner driven on the device; result is a local file | Server starts a scan job on the device with the chosen settings and a **destination URL on the server**; the device pushes the pages; the server then calls Graph. Needs: OXPd scan job with HTTP(S) destination, the option set in 4.5 (file type incl. PDF/A and searchable PDF, resolution, sides, size, colour, blank-page removal, PDF encryption, split by page), job status and cancel events |
| Scan preview before sending (forced ON in MailFlow) | Rendered locally from the scan file | Server renders page images from the received file and serves them to the panel browser, or the feature is dropped. A decision, see section 7 |
| Print: local file path handed to CVL print (4.6, 5.5) | Print engine driven on the device | Server fetches or converts the document and submits a print job to the device from a **server URL or stream** with the options (copies, sides, colour, paper size, type, tray, collate). Needs: OXPd print-job submission, accepted formats per model, job status events |
| Device capability gates `isPrintSupport` / `isScanSupport`, native print formats (5.2, 5.5) | Read from the device through CVL | Query device capabilities through OXPd once per device and cache them server-side |
| Temp files in app-private storage, wiped on sign-out (4.7, 5.6) | Device file system | Server-side per-session spool with the same rule (wipe at session end) **plus** delete after each job, which the current apps do not do |
| Free-space check before download | Device storage | Server quota per session instead |
| Per-user properties via `UserManagement` (4.8, 5.6) | IPC to HPAM | Same key/value store reachable from the server; if it is shared with Workpath HPAM's store, the keys `mailflow.quick_message` and `teams.quick_access` etc. can roam across a mixed fleet |
| Remote config via Workpath config frames and the MOC schema (4.8) | HP management channel for Workpath apps | Server-side configuration with the same keys; the MOC and `config.cfg` are a ready-made list of every setting and its allowed values and translations |
| Graph calls (4.4, 5.3) | Not device-bound | Run unchanged on the server. Outbound network path moves from each printer to the server |
| `FallbackDns` on the device (5.1) | Works around printers' DNS failures | Not needed server-side |
| `FLAG_SECURE`, no backup | Android | Not applicable; replace with no-cache headers on panel pages |

### 6.2 Reusable parts

- The **Graph call list** in 4.4 and 5.3 is the functional contract of both apps: 23 live calls for MailFlow, 16 for Teams.
- The **Teams channel-message recipe** (reference attachment with the GUID from the eTag and the cleaned `webUrl`) is non-obvious and worth porting exactly (5.3 call 15).
- The **PDF conversion approach** (`?format=pdf`) and its extension lists and size caps (4.6, 5.3 call 11).
- **Folder ordering, filters, naming rules, size-limit rule** (4.3, 4.5, 5.4).
- **MOC + `config.cfg`**: settings catalogue with translations in seven languages.
- **String resources** in six languages (157–195 strings each) can seed the web UI's translations.
- **`SessionAccessPolicy`** is the cleanest statement of the session rule; both apps have a unit test for it (`MF/app/src/test/java/com/hp/print/mailflowas/auth/SessionAccessPolicyTest.kt`, `TM/app/src/test/java/com/hp/print/teams/auth/SessionAccessPolicyTest.kt`, not opened).

### 6.3 Traps not to carry over

1. **Raw HTTP calls skip token refresh** (MailFlow calls 2, 7, 13, 16, 17, 20–23): a token that expires mid-session fails on exactly the send and print paths. One HTTP layer with refresh for everything.
2. **No `Retry-After`; immediate blind retries** (4.4): a server concentrates many users' Graph traffic on few IP addresses and one app registration, so throttling becomes more likely than on per-printer clients. Honour `Retry-After`, back off, and queue.
3. **MailFlow's large attachment upload is one PUT** (call 16) and reads the file into memory twice; mail attachment upload sessions expect ranged chunks. Use proper chunking as Teams does (call 14).
4. **OneDrive round trip for PDF conversion** (calls 21–23): needs a Files permission and a provisioned OneDrive, leaves a file in the user's drive if the delete fails, and uses simple upload for content up to 100 MB although Graph documents simple upload for small files only (external knowledge, not from this library: verify the current limit). A server can convert locally or use an upload session; either removes the dependency.
5. **Status codes parsed from exception text** (4.4, 5.3), with 503 unreachable in MailFlow. Use the real response status.
6. **Only the first page is read** for folders (200), attachments, people and search (100) in MailFlow.
7. **Sign-in crash on missing claims**: `given_name` / `family_name` are read with a throwing getter and rethrown as a runtime exception (`SplashActivity.kt:516-529`). Guest or service-style accounts without those claims would crash at start. (inferred from code; not observed)
8. **Send without retry but with multi-step state** (draft → attachments → send): a failure after the draft is created leaves a draft behind; the retry of "save to drafts" can duplicate attachments (4.4).
9. **No per-job temp clean-up** (4.7): on a shared server this would accumulate other users' scans and mail attachments. Delete on completion and on failure.
10. **Dead code that looks alive**: MailFlow's own OAuth sign-in, admin consent, e-mail provider selection, Gotenberg job, `Html2Pdf`, `personalization` and `msgraph-sdk` AARs; Teams' attestation and token proxy remnants. None of it is a requirement.
11. **Teams batch at the limit**: 20 pins = 20 batch items, Graph's maximum; raising the pin cap would break the sync (5.3 call 16).

### 6.4 Requirements the port inherits

- Delegated Graph permissions, per app: MailFlow `Mail.ReadWrite`, `Mail.Send`, `People.Read` (+ a Files scope only if the OneDrive conversion is kept); Teams `Team.ReadBasic.All`, `Channel.ReadBasic.All`, `Files.ReadWrite.All`, `ChannelMessage.Send`.
- National-cloud support: both apps take Graph and authority hosts from HPAM's `CloudConfig` and never hardcode `graph.microsoft.com` in live paths (4.2, 5.1).
- Capability-driven UI: hide print or scan when the device cannot do it (5.2).
- Six UI languages at parity with today (seven in admin configuration).
- An attachment size limit configurable per customer (default 35 MB) for mail; conversion caps 100 MB (MailFlow) and 80 / 40 MB (Teams).

---

## 7. Contradictions and doubts

1. **Scopes: code versus documentation.** MailFlow's constant omits any Files scope (`MSConstants.kt:13`) while its print path needs one (4.4). `START-HERE.md:52` lists `Files.ReadWrite.All` on the HPAM registration, which explains why it works. The constant is stale, not the behaviour.
2. **App registrations.** Each app has its own `CLIENT_ID` build field and its own `msal…://auth` redirect constant (`MF/app/build.gradle.kts:61,84`, `MSConstants.kt:3`; `TM/app/build.gradle.kts:53,75`, `AppAuthConstants.kt:4`), while `START-HERE.md:52` describes a single "HP Authentication Manager" registration with a different redirect. In the live code the per-app client id is used only by dead paths: MailFlow's sign-in and admin consent; in Teams `getAppClientId()` has no caller at all (grep over the app source finds only its definition, `TMa/constant/Constants.kt:68-69`). (inferred: the per-app registrations are legacy.) Teams also keeps a commented-out "test" client id (`TM/app/build.gradle.kts:54`).
3. **Auth flow.** `START-HERE.md:53` says "auth code + PKCE". MailFlow's legacy sign-in sends no PKCE parameters (`MSAppAuthHelper.kt:86-126`). No conflict for the live product (HPAM signs in), but the legacy code is not an example to follow.
4. **Teams manifest permission.** MailFlow declares **and** uses `TokenLibraryPermission` (`MF/…/AndroidManifest.xml:17-18`); Teams only declares it with `<permission>` and has no `<uses-permission>` line for it (`TM/…/AndroidManifest.xml:7`). Either the library's own manifest merges the uses-permission in, or the declaration alone is enough for the binding as HPAM implements it. Not resolvable from these two repos.
5. **EULA.** Both apps carry full EULA flows, per-user acceptance storage and EULA assets in up to eight languages, yet in both the entry function `checkEula()` is defined and never called (`MFa/ui/splash/SplashActivity.kt:365`, `TMa/ui/splash/SplashActivity.kt:336`; grep over each app source returns only the definition). So no EULA is shown by either app in this code, while the help documentation may still describe one (outside this lane).
6. **MailFlow "logout" call.** `MicrosoftLogoutProviderImpl` takes the token from the legacy `auth_token` slot, which the HPAM flow never fills in the code read; `disableAccessToken` throws on a null token and the exception is swallowed (`MFa/microsoft/logout/MicrosoftLogoutProviderImpl.kt:11-19`; `MSAppAuthHelper.kt:173-176`). (inferred: MailFlow's logout makes no network call; the session really ends through Workpath sign-out or HPAM.)
7. **Error-code documentation.** The help portal has a "Mailflow MFxx" article (`START-HERE.md:47`); the source defines only MF01 and MF03. Codes in the article beyond those two would come from another version or another component. The article itself is outside this lane.
8. **Library versions differ**: CVL 1.09.20 (MailFlow) against 1.09.22 (Teams); the two `OnGuardLib` copies differ slightly in line counts (for example `secrets.h` 21 lines against 14). The repos are not built from one shared-library baseline.
9. **Version labels.** MailFlow HPK date 2023-04-19 and Teams 2023-11-22 (`hpk.xml:6` in each) are older than the 4.4 code; the `<date>` field is evidently not maintained.
10. **"MF03" wording** says "Azure outlook services" for what is any unclassified failure, including local I/O errors (4.9).

---

## 8. Questions for Kam or his team

1. **Is scan preview on the panel required in the server version?** MailFlow forces preview on before sending (`SendPresenter.kt:108-109`). On a server design it means the device uploads the scan, the server renders pages and the panel browser displays them: more round trips and a rendering component. If unanswered I assume: a first-page thumbnail and page count only.
2. **Should the server convert Office documents itself, or keep Microsoft's `?format=pdf`?** Keeping it preserves today's output and, for mail, the OneDrive dependency and Files permission (4.6). Converting on the server removes both but changes fidelity and adds a component. If unanswered I assume: keep Graph conversion for files already in SharePoint/OneDrive (Teams), and for mail attachments convert through a server-held location rather than the user's OneDrive only if a customer objects to the OneDrive round trip.
3. **Must per-user settings roam between Workpath and OXPd devices** (quick messages, quick-access pins, remember-me)? It decides whether the server reads and writes the same store that `UserManagement.getUserProperty` uses. If unanswered I assume: yes, same store and same key names.
4. **Is the Gotenberg conversion service (`…/forms/libreoffice/convert`) in use anywhere in the product today?** The MailFlow class is uncalled, but it carries live-looking credentials (section 9). If it is retired the credential should be revoked; if it is the intended server-side converter, that answers question 2. If unanswered I assume: retired.
5. **Are the per-app Entra registrations (MailFlow, Teams client ids) still in customers' tenants?** If customers consented to them, the port must not depend on them and customers can remove them. If unanswered I assume: one registration (HPAM's) is the only one that matters.
6. **Which features are in scope for a first release?** Candidates to drop, from the code: Teams rename/delete/create-folder, column chooser, app guide, quick access; MailFlow quick messages, drafts editing, mail search. If unanswered I assume: functional parity for scan-to and print-from, everything else second.
7. **Teams chats**: the Workpath app has none. Is that still the wanted scope? If unanswered I assume: channels only.
8. **Where do job statistics come from today?** Neither app records scan or print jobs (4.8). If CVL or HPAM does it, the server version must emit the same records (the Log Analytics tables named in `START-HERE.md:55`). If unanswered I assume: the server writes equivalent records for every scan and print job.
9. **Is dropping the in-app EULA deliberate?** Both apps have the EULA screens switched off in code (section 7, item 5). If a licence acceptance is still a contractual need it must be designed into the server version (where: admin console at install, or per user at the panel). If unanswered I assume: no per-user EULA in the server version.

---

## 9. Secrets and sensitive items seen (locations only)

| Item | Location |
|---|---|
| A client secret, client id, resource URI and service base URL for a PDF conversion API are hardcoded | `MF/app/src/main/java/com/hp/print/mailflowas/microsoft/download/GotenbergCloudRenderingRequestJob.kt:36-39` |
| A tenant id is hardcoded in a token endpoint path | `MF/app/src/main/java/com/hp/print/mailflowas/microsoft/download/AuthenticateGotenberg.kt:11` |
| Release-signing keystore committed to the repository | `MF/app/[keystore file name withheld]`; `TM/[keystore file name withheld]` |
| Keystore password, key alias and key password hardcoded in the build script | `MF/app/build.gradle.kts:34-37`; `TM/app/build.gradle.kts:29-32` |
| Entra application (client) ids hardcoded as build fields | `MF/app/build.gradle.kts:61,84`; `TM/app/build.gradle.kts:53,75` (and a commented-out test id at `:54`) |
| Redirect URIs that embed application ids | `MFa/microsoft/constants/MSConstants.kt:3`; `TMa/auth/AppAuthConstants.kt:4` |
| Native "locker" secrets header (not opened) | `MF/OnGuardLib/src/main/cpp/hdr/locker/secret/secrets.h`; `TM/OnGuardLib/src/main/cpp/hdr/locker/secret/secrets.h` |
| `gradle.properties` in Teams: key names only were read; they are build flags, no credential-looking keys | `TM/gradle.properties` |
| No personal data of real people seen in the files read. Developer first names appear in log tags and comments (for example `MSAppAuthHelper.kt:92`) | |

Security weaknesses in the existing product that the port should not carry over:

1. **Secrets shipped inside a client app and committed to source** (first two rows). Anything in an APK is extractable; on a server, secrets belong in a vault and never in the repository. The repositories have a gitleaks workflow, yet these values are present: either the scan allows them or it runs only on new commits.
2. **Signing key and its password in the repository** (rows three and four): anyone with read access can sign a package as the vendor.
3. **Debug hook in production code**: `CommonApp` registers an **exported** broadcast receiver for action `com.crash` that deliberately crashes the app (`MFa/CommonApp.kt:25-45`). Any other app on the device can send it.
4. **Verbose logging of configuration and Graph traffic**: Teams enables the Graph SDK logger at DEBUG level in all builds (`TMa/auth/AppAuthManager.kt:65-71`); both apps log the `CloudConfig` object (`MSAppAuthHelper.kt:58`, `AppAuthManager.kt:63`). On a server, logs must never contain tokens, mail content or file names by default.
5. **Access token readable by decoding without validation** is harmless for display, but the apps also take the tenant id from it and store it as trusted (`SplashActivity.kt:517-521`). A server must validate tokens it receives from any other component (issuer, audience, signature) before trusting claims.
6. **Legacy sign-in without PKCE** and with a spoofed WebView user agent in the admin-consent screen (`MSAppAuthHelper.kt:122-126`; `MFa/tenant/AdminConsentActivity.kt:86`): dead code, but it must not be the model for the server's sign-in.
7. **DNS answers cached in plain preferences and trusted when DNS fails** (`TMa/util/FallbackDns.kt:22-39`): TLS still protects the connection, so this is an availability workaround, not a break; it has no place on a server.
8. **User files written to the user's own OneDrive as a side effect of printing** (4.6): if the final delete fails, mail bodies and attachments remain in `Apps/…/MailFlowAS`. A privacy point to state to customers or to design out.
9. **Mail HTML rendered with JavaScript enabled** in the reading WebView (the annotation `SetJavaScriptEnabled` precedes the body WebView set-up at `MFa/ui/main/MailBodyFragment.kt:166`, section sampled; the settings lines themselves were not read) (inferred). In a web UI served by the server, mail HTML must be sanitised and sandboxed: it is hostile input displayed inside the server's own origin.
