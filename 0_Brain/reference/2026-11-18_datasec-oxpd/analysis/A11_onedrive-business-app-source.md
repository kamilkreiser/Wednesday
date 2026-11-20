# A11: the OneDrive business app source (the missing half of report A3)

Lane D of commission B1768 (work package WP0.6, what is left of it), Datasec / OXPd 2, written 2026-11-20. Read-only analysis. Nothing was built or run; no network call was made.

Path conventions (every claim carries `path:line`; line numbers are those of the files as they stand in the NAS copy of the library):

- Library root on this machine: `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/`. Report A3 names the same library as `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`.
- `OD/` = `HPAM - Docs and Notes/Source Code/CypherOneDrive-main/` under the library root.
- `ODJ/` = `OD/app/src/com/hp/print/cypher/`.
- `CVL/` = `HPAM - Docs and Notes/Source Code/CommonValueLibraryCypher-master/commonvaluablelibrary/src/main/java/com/hp/print/commonvaluablelibrary/` (library copy, version 1.09.22) and `CVLres/` = the same module's `src/main/res/`.
- `SP/`, `SP-J/`, `CVL2/` as report A8 defines them (the trees the product owner sent on 2026-11-20).
- Design documents: `02` = `02_architecture.md`, `03` = `03_plan-of-attack-and-build.md`, `05` = `05_readiness-to-build.md`, all in `0_Brain/reference/2026-11-18_datasec-oxpd/` (the copies corrected on 2026-11-20).

Secrets rule (C-3): no secret value is reproduced in this report. Section 6 gives locations only. Every file that could carry key material was displayed through a mask (GUIDs replaced, password and client-id lines replaced by their length).

**Mapping control (asked by the commission).** Report A3 cites `UP/settings.gradle.kts:48` for the Gradle root name "HP for Universal Print"; at the mapped NAS path `HPAM - Docs and Notes/Source Code/UniversalPrint-main/settings.gradle.kts` the same text is at line 44, not 48. Report A8 cites `OD/app/build.gradle.kts:33` for version 4.4.1; at the mapped path line 33 reads `versionName = "4.4.1"`. So the mapping holds for the OneDrive tree line for line; the Universal Print tree on the NAS is a copy whose line numbers drift from A3's by a few lines (not this lane's tree; noted for whoever next checks A3's Universal Print citations).

## 1. BLUF

1. **Report A3 never analysed OneDrive: its OneDrive half is five placeholder comments.** This report is that half, whole: the app, its journeys, its Microsoft calls, its secrets locations (section 2).
2. **The OneDrive app is bigger than the documents say.** It has four places, not one: My Drive, Recent, Shared with me, and Shared libraries (SharePoint sites, libraries and library columns inside the OneDrive app). `02` describes My Drive only (rows 15 to 27; section 10).
3. **28 Microsoft calls in the source, 22 live**, all Microsoft Graph v1.0, none to a sign-in endpoint. The app has no sign-in and no credential: the token is HP Authentication Manager's, refreshed once on a 401. No `Retry-After` handling anywhere; the one retry loop (large-upload pieces) has no limit (section 5).
4. **The code names no permission for the live path.** Four live calls read other users' drives (Shared with me); whether `Sites.ReadWrite.All` covers them must be checked on a tenant (section 5, question 2).
5. **F87 is DEAD, and now on the binary, not only the source.** `isSIOEnabled()` is a library method whose compiled body in the 1.09.20 binary Mailflow links is two bytes, "return false"; nothing can set it; both doors to quick messages are behind it. The same closes the quick-access rows of OneDrive and of SharePoint (A8's open question 1) (section 9).
6. **The shared scan and print screens are used identically by OneDrive and SharePoint** (the same sixteen library classes): eleven scan option groups, seven print option groups. The differences are around them: SharePoint adds library metadata at scan, OneDrive does not (section 7).
7. **The personal flavour (OQ-4) differs from the business one in two code branches, has no way to sign in, and is not packaged** (rows 64 to 66).
8. **Against the documents:** 22 rows compared: 12 confirmed, 3 contradicted (all by omission: F33, F37 and the same fact in section 5.6.3), 1 incomplete, 2 open points settled (F87, F93), 3 still unknown. 17 proposed corrections, none applied (sections 10, 11).
9. **Limits:** about 40 of 176 source files read whole or nearly, the three largest classes by ranges and search; no option's values inside the shared screens were read; nothing built, run, or checked on a printer or against Microsoft's documentation (section 13).


## 2. Prior work: what was already read, and what was not

### 2.1 Report A3

Read whole for this section (462 lines). **A3 analysed no OneDrive file and no OneDrive journey.** Its OneDrive half is five placeholders and nothing else:

| A3 line | What stands there |
|---|---|
| 30 | "OneDrive / SharePoint facts are in 4.1 (merged from the second half of this lane)" |
| 60-62 | Coverage heading "OneDrive / SharePoint (`OD/`, 532 files)" followed by "See 4.1.0 (coverage table supplied by the OneDrive half of the lane)". No table exists |
| 92-94 | Inventory 3.2: "See 4.1.1". No 4.1.1 exists |
| 100-102 | Section 4.1 is the single line `<!-- ONEDRIVE-SECTION-PLACEHOLDER -->` |
| 332 | `<!-- ONEDRIVE-PORT-PLACEHOLDER -->` (section 5.1) |
| 395 | `<!-- ONEDRIVE-DOUBTS-PLACEHOLDER -->` (section 6) |
| 413 | `<!-- ONEDRIVE-QUESTIONS-PLACEHOLDER -->` (section 7) |
| 432 | `<!-- ONEDRIVE-SECRETS-PLACEHOLDER -->` (section 8) |

Search that shows it: `PLACEHOLDER` over A3 finds exactly those five comment lines (102, 332, 395, 413, 432). A3 has no NOT READ section for OneDrive at all; its "Not opened" list (line 56) is Universal Print only. The two OneDrive facts A3 does state are in its Universal Print half: the path shorthand (`OD/`, `ODJ/`, lines 11-12), the file count 532 (line 60), and that the signing keystore's file name also appears in the OneDrive tree (line 439). The coverage note of `02` says the same: "report A3's OneDrive/SharePoint half was never written (its sections 4.1, 5.1, 6, 7 and 8 for OneDrive are placeholders)" (`02:7`).

So "the missing half" is the whole of the OneDrive app: coverage, inventory, findings, port notes, doubts, questions and secrets. Everything A3 wrote (Universal Print) is untouched by this report and is not repeated.

### 2.2 Report A8

Read whole (326 lines). A8 is the SharePoint app (`CypherSharePoint-main` 4.4.6) and the common library copy the product owner sent. What it established about OneDrive, all from file names, the build file by search and four searches (A8 lines 33, 266, 323: "No behaviour of the OneDrive app is established by this report"):

- OneDrive is a separate tree of 532 files, version 4.4.1, two flavours, common library 1.09.21, the same Workpath SDK, quick-access library and Graph SDK versions as SharePoint (A8 lines 270-274).
- 173 distinct class names, 143 shared with SharePoint; 30 only in OneDrive, among them `GetAllSitesTask`, `GetLibraryMetadataTask`, `UpdateLibraryFieldsTask`, `LibraryColumnMapper`, `SharedLibrariesStep`, `GetRecentTask`, `GetSharedListFolderTask`, `FileSizeComparator`, `QuotaLimitReachedException`, `UploadFileTaskReplace`: "these files were not opened" (A8 line 278).
- The same upload threshold, conversion limits, recent limit and pin limit as SharePoint (A8 line 279); 14 lines call `isSIOEnabled` (A8 line 280).
- OneDrive uses the library's `sharepoint/columns` package (24 import lines); 0 OneDrive files name a sensitivity label (A8 line 259).
- About the common library: A8 did **not** re-read the scan and print screens (A8 line 24: "the scan and print screens inside it were not re-read"; line 322).

### 2.3 Report A4 (where it covers the common library and OneDrive)

Read by search for the lines that name OneDrive, the common library or `isSIOEnabled`. A4 gives: the library's service layer (`ScanSupportService`, `PrintSupportService`, capabilities, configuration model) with source lines (A4 lines 135-143); "Scan option screens (20 options), print option screens (14)" as a file list "not read in detail" (A4 line 142); the device e-mail helper as used by OneDrive only (A4 line 177); OneDrive's package ids and library versions (A4 line 207); `isSIOEnabled()` returns false always (A4 line 290); the keystore and password locations (A4 lines 323-324). A4 did not list the options screen by screen, nor compare how two apps use them.

### 2.4 What this report adds

The whole OneDrive app (sections 3 to 6), the scan and print screens of the common library option by option and how the OneDrive and SharePoint apps each use them (section 7), F87 (section 9), the comparison with the documents and the proposed corrections (sections 10, 11).

## 3. What it is

- **One Android (HP Workpath) app, two build flavours, one of them shipped.** Gradle project `CypherOneDrive` with modules `:usermanagement`, `:OnGuardLib`, `:CVL`, `:app` (`OD/settings.gradle.kts:44-49`). Namespace and base application id `com.hp.print.cypher` (`OD/app/build.gradle.kts:24`, `:28`); flavours `onedriveforpersonal` and `onedriveforbusiness`, each adding its name as the application-id suffix (`:120-131`). Version 4.4.1, version code `4_04_01_00` (`:32-33`). Compile and target SDK 35, min 31 (`OD/build.gradle.kts`, the three `extra[...]` lines). Java 11 (`OD/app/build.gradle.kts:138-145`).
- **The package the release pipeline builds is the business flavour only**: `./gradlew :app:test :app:assembleOnedriveforbusinessRelease` (`OD/.github/workflows/release.yml:130`), packaged as `OneDrive_v<version>-release.hpk` holding `OneDrive-onedriveforbusiness-release.apk` and `hpk.xml` (`:140-154`). The HPK descriptor: name "OneDrive for Authentication Suite", vendor "HP Inc", platform `LinkForDevice` 31.7, install file `OneDrive-onedriveforbusiness-release.apk`, a fixed UUID at line 3 (`OD/app/packaging_release/hpk.xml:3-9`). No personal-flavour packaging step exists in that workflow (search of `release.yml` for `personal`, case-insensitive: 0 lines among the 16 lines that match `assemble|hpk|flavor|business|personal|zip|test`; control: `business` matches at `:130`, `:140`, `:141`).
- **Libraries, all vendored binaries except OnGuardLib:** `commonvaluablelibrary-1.09.21.aar` (`OD/CVL/build.gradle:2`), `usermanagement-1.06.01.aar` (`OD/usermanagement/build.gradle:2`), `WorkpathLib-1.6.3.aar` and `quickaccess-1.00.11.aar` (`OD/app/libs/`; `OD/app/build.gradle.kts:195-196`), `microsoft-graph` 5.34.0 (`:198`), OkHttp 3.12.0, Retrofit 2.5.0, Jackson 2.9.6 (`OD/build.gradle.kts`), RxJava 2, Picasso 2.8, Gson 2.11.0, PdfiumAndroid 1.9.8, pdfbox-android 2.0.27.0, security-crypto 1.0.0 (`OD/app/build.gradle.kts:160-191`).
- **Size:** 532 files; 160 `.java` and 27 `.kt` in the tree; under `OD/app/src` 176 source files, 23,772 lines (count by `wc -l`). One unit test, `OD/app/unitTests/com/hp/print/cypher/auth/SessionAccessPolicyTest.java` (28 lines). Five files in `ODJ/taskmanager/` are empty (0 lines each), as in the SharePoint tree (A8 line 57).
- **Four build types, all signed with the one release configuration** (`OD/app/build.gradle.kts:51-76`).
- **Manifest** (`OD/app/AndroidManifest.xml`): permissions `ACCESS_NETWORK_STATE`, `INTERNET`, `FOREGROUND_SERVICE` (`:5-11`); declares the permission `com.hp.print.hpauthenticationmanager.permissions.TokenLibraryPermission` (`:12`); backup off, cleartext off (`:20-21`). **Twelve activities**, all landscape: splash (launcher), main, app guide, information, open-source licences, settings, scan preview, print preview, print preview zoom, log-out, search, sites search (`:27-142`). **There is no log-in activity** in this manifest (the SharePoint manifest has one, A8 line 66). No service, no receiver.
- **Configuration form** for HP Command Center: `OD/app/moc_file/OneDrive.moc`, three frames (`printConfig` `:5`, `scanConfig` `:1207`, `appConfig` `:3079`) and 28 fidgets: 7 print defaults (copies, output sides, colour mode, paper size, paper type, paper tray, collate; `:19-1152`), 19 scan defaults (`:1221-2962`), `splitAttachmentByPage` (`:3025`, inside `scanConfig` here; the SharePoint form has it under `appConfig`, A8 line 64) and `enableSendToEmail` (`:3093`). The app also reads and writes `adminOptIn`, `domainHint`, `urlAddressBar` (`ODJ/utils/AppConfigHelper.java:21-26`).
- **Languages:** English (171 strings in `OD/app/res/values/strings.xml`) and seven translations of 167 strings each: `de`, `es`, `fr`, `in`, `it`, `pt`, `zh-rTW`; plus 8 (English) or 6 flavour strings per language under `res_onedriveforbusiness` (counts of `<string `). The build keeps English resources only for third-party libraries (`localeFilters += listOf("en")`, `OD/app/build.gradle.kts:39-41`): whether that filter also strips the app's own seven translations from the APK was not tested (nothing was built). EULA files for eight locales in `OD/app/assets/`.

## 4. Inventory of behaviour (numbered rows)

State column as in report A8: **LIVE** reachable as built; **DEAD (switch)** behind `WorkpathAccessService.isSIOEnabled()` (section 9 gives what "dead" rests on); **DEAD (commented out)**; **UNREFERENCED** class or method nothing calls. The business flavour is meant throughout; rows 64 to 66 cover the personal flavour.

### 4.1 Start-up, identity, session

| # | Behaviour | State | Source |
|---|---|---|---|
| 1 | Launcher icon opens the splash screen; the app class initialises the encrypted store and the Graph client | LIVE | `OD/app/AndroidManifest.xml:27-37`; `ODJ/common/CommonApp.java:13-17` |
| 2 | No sign-in of its own: the access token is read from HP Authentication Manager through the `usermanagement` binder (`getToken()`) and the destination is decided by one rule: device administrator → settings only; no token → sign-in required; else cloud files | LIVE | `ODJ/ui/splash/SplashActivity.java:192-194`, `:457`; `ODJ/auth/SessionAccessPolicy.java:18-26` |
| 3 | No token: the app starts HP Authentication Manager by package name and shows a sign-in request | LIVE | `ODJ/ui/splash/SplashActivity.java:400-425` |
| 4 | A device administrator never reaches cloud files: personal data is cleared and the settings screen opens (splash and main both check) | LIVE | `ODJ/ui/main/MainActivity.java:210-213`, `:474-475`; `ODJ/ui/splash/SplashActivity.java:472-485` |
| 5 | Identity is read from the token's claims `tid`, `oid`, `unique_name`, `family_name`, `given_name` (decoded, not verified); the drawer shows given and family name | LIVE | `ODJ/ui/splash/SplashActivity.java:526-536`; `ODJ/ui/main/MainActivity.java:343-345` |
| 6 | The token is kept in `EncryptedSharedPreferences` (`access_token`, `tenant_id`; AES256-SIV keys, AES256-GCM values) and sent as a Bearer header on every Graph request | LIVE | `ODJ/common/SecuredPreferences.kt:15-39`; `ODJ/auth/AuthInterceptor.kt:8-15` |
| 7 | On HTTP 401 the app asks HP Authentication Manager for a new token (`getNewToken`), waits at most 10 s, retries the request once with the new token; no new token → the 401 stands | LIVE | `ODJ/auth/SessionAuthenticator.kt:19-59` |
| 8 | A 401 that reaches the error mapper clears the stored token, shows "invalid credentials" and closes the app | LIVE | `ODJ/error/ErrorHandlingUtils.java:57-60`, `:107-108` |
| 9 | National clouds: the Graph base address comes from HP Authentication Manager's cloud configuration (`<graphApi>/v1.0`) | LIVE | `ODJ/common/GraphProvider.kt:50-67` |
| 10 | Network limits: connect 60 s, read/write 180 s, whole call 180 s; DNS fallback to cached addresses | LIVE | `ODJ/common/NetworkTimeouts.java:6-8`; `ODJ/common/GraphProvider.kt:32-44` |
| 11 | Sign out (toolbar button and menu entry) ends the device session with `AccessService.signOut` and closes the app; Exit closes the app only | LIVE | `ODJ/ui/main/MainActivity.java:678-680`, `:1004-1005`, `:1334-1335`, `:1342-1343` |
| 12 | On sign-out or loss of token: per-user cache cleared | LIVE | `ODJ/ui/splash/SplashActivity.java:266-279` |
| 13 | Screens protected from capture | LIVE | `ODJ/ui/splash/SplashActivity.java:95-96`; `ODJ/common/RootBaseAppCompatActivity.java:35`; `ODJ/common/PresenterAppActivity.java:26-27` |
| 14 | Per-user data roams through HP Authentication Manager's user-property channel, keys prefixed `onedrive.`: `quick_access`, `recent_searches`, `recent_site_searches`, `recent_sites`, `library_columns`, `library_column_state`, `predefined_column_state`, and three EULA keys | LIVE (the store); which keys live features write is per row below | `ODJ/storage/UserPreferencesStore.kt:14-24`, `:64-88`, `:111-120` |

### 4.2 Places and browsing

| # | Behaviour | State | Source |
|---|---|---|---|
| 15 | The first screen is **My Drive** (the user's own OneDrive root) | LIVE | `ODJ/ui/main/MainActivity.java:957-979` (the quick-access first screen is behind the switch; else `MY_DRIVE`) |
| 16 | Navigation drawer, opened by the toolbar icon, with five places: My Drive, Recent, Shared with me, Shared libraries, and (behind the switch) Quick access | LIVE (four places) | `ODJ/ui/main/MainActivity.java:997-1000`, `:750-823`; `ODJ/ui/main/base/MainViewType.java` |
| 17 | **My Drive**: folder listing of `/me/drive`, by item id or by path; all pages are followed by the task; a large thumbnail per file | LIVE | `ODJ/task/GetListFolderTask.java:88-117`, `:121-157` |
| 18 | **Recent**: the user's recent files (`/me/drive/recent`), folders and OneNote notebooks left out | LIVE | `ODJ/task/GetRecentTask.java:43-69`, `:82-87`; `ODJ/ui/main/MainBaseFragment.java:1524` |
| 19 | **Shared with me** (`/me/drive/sharedWithMe`, external shares allowed) | LIVE | `ODJ/task/GetSharedListFolderTask.java:35-63`; `ODJ/ui/main/MainBaseFragment.java:1526` |
| 20 | **Shared libraries** = SharePoint inside the OneDrive app, three steps: sites → libraries → files | LIVE | `ODJ/ui/main/sites/SharedLibrariesStep.java`; `ODJ/ui/main/MainActivity.java:801-823` |
| 21 | Sites: Graph site search with `*`, 500 per page, all pages followed | LIVE | `ODJ/task/GetAllSitesTask.java:33-39`, `:51-65`; `ODJ/ui/main/presenter/MainBasePresenter.java:1020-1022` |
| 22 | Recent sites: the last 3 opened, shown in the drawer, kept per user | LIVE | `ODJ/ui/main/MainBaseFragment.java:1152`; `ODJ/constants/AppConstants.java:70`; `ODJ/ui/main/MainActivity.java:693-720` |
| 23 | Libraries of a site (first page of the site's drives only; no paging loop) | LIVE | `ODJ/task/GetDrivesTask.java:30-46` |
| 24 | Files of a library: the same listing task on `/sites/{s}/drives/{d}`, and when the library's list is known each item also brings its list item and column values in the same request (`$expand=listItem($expand=fields)`), so there is **no batch request per page** as in the SharePoint app (A8 row 21) | LIVE | `ODJ/task/GetListFolderTask.java:62-86`, `:123-132` |
| 25 | Library columns: the list behind the drive, then all pages of its column definitions, mapped by the common library's column model | LIVE | `ODJ/task/GetLibraryMetadataTask.java:25-48`; `ODJ/common/sortcolumns/LibraryColumnMapper.kt` (66 lines, not opened) |
| 26 | Sort and group by a library column; the choice is kept per site and library for the user | LIVE (read by search) | `ODJ/ui/main/MainBaseFragment.java:288-309`, `:1681-1695` |
| 27 | Sort: newest, oldest, A to Z, Z to A, **and file size ascending and descending** (two more than the SharePoint app, A8 row 25); on 4.3-inch panels the sort entry moves to the overflow menu | LIVE | `ODJ/sort/SortingType.kt` (enum, 6 values); `ODJ/ui/main/MainActivity.java:1237-1239` |
| 28 | List view or grid view | LIVE (read by search) | `ODJ/ui/main/MainBaseFragment.java:677`, `:1088-1097`; `ODJ/constants/AppConstants.java:17-18` |
| 29 | Folder cache: 40 listings in memory, shown at once then reloaded | LIVE | `ODJ/storage/FolderNavigationCache.java:14-19`; `ODJ/ui/main/MainBaseFragment.java:1750` |
| 30 | Refresh button (reloads sites, libraries or the folder according to the step) | LIVE | `ODJ/ui/main/MainActivity.java:1286-1306` |
| 31 | Write permission read per folder (`permissions` of the drive item, a `write` role); rename and delete are offered only with it | LIVE | `ODJ/ui/main/presenter/MainBasePresenter.java:947-991`, `:1008`; `ODJ/ui/main/MainBaseFragment.java:627-628`, `:1518`, `:1529` |
| 32 | File details dialog | LIVE | `ODJ/ui/main/MainBaseFragment.java:639-640`; `ODJ/ui/dialog/FileDetailsDialog.java` (not opened) |

### 4.3 Search

| # | Behaviour | State | Source |
|---|---|---|---|
| 33 | Search files: in My Drive `/me/drive/root/search`, in a library `/drives/{d}/root/search`; 400 results, first page only; HTTP 400 shown as an empty result | LIVE | `ODJ/task/SearchCallableTask.java:114-136`, `:97-98` |
| 34 | Search in **Shared with me** uses the Microsoft Search API (`POST /search/query`, drive items, 400 results), then re-reads each hit as a drive item; duplicates removed | LIVE | `ODJ/task/SearchCallableTask.java:82-83`, `:138-172`, `:204-220`, `:223-229` |
| 35 | Last 3 search terms kept per user; a result opens in its folder | LIVE | `ODJ/ui/search/SearchActivity.java:187-193`, `:409` |
| 36 | Search sites by name (500 per page, all pages); last 3 site search terms kept | LIVE | `ODJ/ui/search/sites/task/RootSiteTask.java:56-77`; `ODJ/ui/search/sites/SitesSearchActivity.java:189-198` |

### 4.4 File management

| # | Behaviour | State | Source |
|---|---|---|---|
| 37 | Create folder: name checked against the names already listed, then created with "fail on conflict"; 409 and 400 each have a message | LIVE | `ODJ/ui/main/MainBaseFragment.java:881-904`; `ODJ/task/CreateFolderTask.java:125-142` |
| 38 | Rename a file or folder; a file keeps its extension; a file with no extension cannot be renamed (the task returns false) | LIVE | `ODJ/task/RenameFileTask.java:39-56`, `:59-71` |
| 39 | Delete one or several items, one request each, with progress and cancel | LIVE | `ODJ/task/DeleteFilesTask.java:40-75` |
| 40 | Edit the library column values of an existing file ("edit library columns" in the item menu): only in a shared library, with write permission, when the library has columns, and not on 4.3-inch panels | LIVE | `ODJ/ui/main/MainBaseFragment.java:629-633`, `:188-201`, `:1662`; `ODJ/task/UpdateLibraryFieldsTask.java:23-44` |

### 4.5 Print

| # | Behaviour | State | Source |
|---|---|---|---|
| 41 | Tap a file: download, then print preview | LIVE | `ODJ/ui/main/MainBaseFragment.java:768-771`; `ODJ/ui/main/presenter/MainBasePresenter.java:530-591` |
| 42 | Swipe a file row: direct print, no preview | LIVE | `ODJ/ui/main/MainBaseFragment.java:719-737`, `:759-763`, `:1168-1170` |
| 43 | Printable types: `pdf, jpg, jpeg, tiff, tif, txt` directly (the common library's list), Office files `doc, docx, xls, xlsx, ppt, pptx` after conversion; anything else "not supported file format" | LIVE | `ODJ/utils/Utils.java:345`; `CVL/utils/CommonSDKUtil.java:190-196` (as cited by A3 line 244 and A8 row 40); `ODJ/ui/main/MainBaseFragment.java:763` |
| 44 | Office conversion by Graph (`content?format=pdf`); limits 80 MB, Excel 40 MB; a conversion time-out has its own message | LIVE | `ODJ/task/DownloadConvertToPdfFileTask.java:42-43`, `:68-84`, `:119-121`; `ODJ/utils/Utils.java:363-371`; `ODJ/error/ErrorHandlingUtils.java:72-74` |
| 45 | Other files: the download address given by the listing, else one item read to get it; connect 5 s, read 6 s, no retry; free-space check first | LIVE | `ODJ/task/DownloadFileTask.java:40-41`, `:76-93` |
| 46 | Multi-select print (toolbar print button or the print button on the list): all selected files downloaded, then previewed together | LIVE | `ODJ/ui/main/MainActivity.java:1268-1270`; `ODJ/task/DownloadMultipleFilesTask.java:320-322`, `:408-418` |
| 47 | Print preview, print options and zoom are the common library's screens (section 7) | LIVE | `OD/app/AndroidManifest.xml:99-117`; `ODJ/ui/preview/PrintPreviewAppActivity.java` (218 lines, not read) |

### 4.6 Scan

| # | Behaviour | State | Source |
|---|---|---|---|
| 48 | A scan button on the list opens the scan screen with the open folder as destination. It is shown only where the user has write permission (the same flag as Create folder) and never on a device with no scanner | LIVE | `ODJ/ui/main/MainActivity.java:1023-1026`, `:1831`, `:2098`; `ODJ/ui/main/MainBaseFragment.java:864-866`, `:1583-1596` |
| 49 | Scan options, preview and job progress are the common library's (section 7); defaults from the configuration form | LIVE | `OD/app/moc_file/OneDrive.moc:1207`; `ODJ/ui/settings/SettingsAppFragment.java:104-108` |
| 50 | File name typed by the user (filtered input), else `Scan_<date>_<time>` with the date order of the device locale | LIVE | `ODJ/ui/preview/ScanDescriptionAppFragment.java:130-133`, `:288`; `ODJ/utils/Utils.java:145-165` |
| 51 | Several files from one scan: `_001`, `_002` from the second file (four digits from 1,000 files); name cut to 255 characters | LIVE | `ODJ/task/UploadFileTask.java:224-225`, `:645-681` |
| 52 | Upload under 3.5 MB in one request; else an upload session in 10 MiB pieces aligned to 320 KiB, each piece retried on 408, 429 and 5xx with a wait that doubles from 1 s to at most 15 s, with **no limit on the number of retries** | LIVE | `ODJ/task/UploadFileTask.java:73-78`, `:241-283`, `:316-334`, `:510-573`, `:596-601` |
| 53 | An existing file is never overwritten: "fail" on name conflict in both paths; one destination → duplicate-name error | LIVE | `ODJ/task/UploadFileTask.java:235`, `:296-297`, `:429`, `:445-446` |
| 54 | **Storage quota full has its own message** (HTTP 507, or Graph `quotaLimitReached`): "failed to upload, no quota". Not in the SharePoint app (class only in OneDrive, A8 line 278) | LIVE | `ODJ/task/UploadFileTask.java:286-292`, `:450-455`, `:728-769`; `ODJ/error/ErrorHandlingUtils.java:61-62` |
| 55 | **No library metadata at scan in this app.** The scan description screen has a file name and the e-mail option only; its base class has empty column methods. Column values are edited afterwards (row 40) | LIVE (absence) | `ODJ/ui/preview/BaseScanDescriptionAppFragment.java` (30 lines, all method bodies empty); search of `ODJ/ui/preview/ScanDescriptionAppFragment.java` for `LibraryColumn\|metadata`, case-insensitive: 0 lines; control in the same file: `email` 45 lines |
| 56 | Send to e-mail (only when the administrator enabled it): checkbox and recipient list, prefilled with the user's address, else the device default From; more than 5 recipients is refused | LIVE | `ODJ/ui/preview/ScanDescriptionAppFragment.java:214-238`, `:308-309` |
| 57 | The e-mail goes through the device's SMTP settings (`Email.send`) with the scans attached; "SMTP not configured" has its own message; if the upload fails a failure e-mail goes to the recipients, else to the user | LIVE | `ODJ/model/SendEmailTask.java:29`, `:60`; `ODJ/model/EmailSender.java:34-52`, `:103`; `ODJ/ui/preview/presenter/ScanPreviewPresenter.java:84-101`, `:112-148` |
| 58 | Cancel during upload; result list | LIVE | `ODJ/ui/preview/ScanPreviewAppFragment.java:158-160`, `:246-271` |

### 4.7 Settings, information, errors

| # | Behaviour | State | Source |
|---|---|---|---|
| 59 | Settings entry only for a device administrator: default print options, default scan options, Send to e-mail switch | LIVE | `ODJ/ui/main/MainActivity.java:1213-1217`; `ODJ/ui/settings/SettingsAppFragment.java:100-110` |
| 60 | Remote configuration read and write-back (`adminOptIn`, `enableSendToEmail`, `domainHint`, `urlAddressBar`) | LIVE | `ODJ/utils/AppConfigHelper.java:20-26`; `ODJ/ui/main/MainActivity.java:941-942` |
| 61 | Information page, open-source licences, app guide from the menu | LIVE | `ODJ/ui/main/MainActivity.java:1336-1341` |
| 62 | Errors by status: 401 (row 8); 507 no quota; 403 no permission; 404 not found; 409 same name; 429 and 503 too many requests; conversion time-out; insufficient device storage; file too large; else "unable to retrieve data". Status is recovered by searching the exception text for "401 :" and the like | LIVE | `ODJ/error/ErrorHandlingUtils.java:57-103`, `:122-146` |
| 63 | Three panel classes (`sw340dp`, `sw600dp`, `sw800dp` resource sets); reduced on 4.3-inch panels: rows 27, 40 | LIVE | directories under `OD/app/res/`; `ODJ/ui/main/MainActivity.java:226` |

### 4.8 The personal flavour (only as far as OQ-4 needs)

| # | Finding | Source |
|---|---|---|
| 64 | The personal flavour differs from the business one in **two code branches only**: the Shared libraries drawer entry is hidden, and the working-folder name. Everything else is the same code. The settings branch that names the business flavour has an empty body (its one line is commented out) | `ODJ/ui/main/MainActivity.java:337-338`; `ODJ/constants/AppConstants.java:76-80`; `ODJ/ui/settings/SettingsAppFragment.java:121-123`. Search of `ODJ` for `BuildConfig.FLAVOR`: 4 lines (the three above and a log line, `ODJ/ui/splash/SplashActivity.java:118`) |
| 65 | **The personal flavour has no way to sign in.** The app has no sign-in screen (row 2); the consumer authority endpoints are commented out (`ODJ/constants/OneDriveConstants.java:13-18`); the two constants that name a personal redirect address and a personal scope string are used by nothing (search for `REDIRECT_URI_FOR\|SCOPE_FOR_\|AUTH_GRANT_TYPE\|TOKEN_GRANT_TYPE` outside the constants file: 0 lines; control: the same names are found inside it at `:7-10`, `:20-21`). The only token source is HP Authentication Manager, whose manifest queries `com.hp.print.cypher.onedriveforbusiness` and not the personal package (A4 line 125) | as cited |
| 66 | The release pipeline does not build it (section 3) and the HPK descriptor names the business APK | `OD/.github/workflows/release.yml:130`; `OD/app/packaging_release/hpk.xml:9` |

**Answer for OQ-4 from the code:** the personal flavour is a leftover build variant of HP's original app: it compiles, it is not packaged, and as the tree stands it cannot obtain a token. Whether Datasec ever shipped it is not a code question; the code gives no sign that it did.

### 4.9 Present in the source but not reachable

| # | Behaviour | State | Source |
|---|---|---|---|
| 67 | Quick access: pinned print items and scan folders (10 each), quick print, quick scan, 4 recent files, "open on quick access first", folder print of up to 10 files, its settings entry, its `$batch` refresh | DEAD (switch) | `ODJ/ui/main/MainActivity.java:239-240`, `:320-333`, `:958-976`; `ODJ/ui/main/MainBaseFragment.java:553-557`, `:573-596`, `:612-613`; `ODJ/ui/settings/SettingsAppFragment.java:117-118`; `ODJ/constants/AppConstants.java:41-43`; `ODJ/ui/main/presenter/QuickAccessPresenter.kt:84-116` |
| 68 | Settings shown to a non-administrator; app guide at first use; "remember me" | DEAD (switch) | `ODJ/ui/main/MainActivity.java:1213`; `ODJ/ui/appguide/AppGuideActivity.java:111`, `:119`, `:164` |
| 69 | Sign-out confirmation screen (`LogoutActivity`), reached from Back on the sites list when the switch is false | **LIVE as coded**, unlike SharePoint (A8 row 70): Back at the sites step calls `startSignOut()` when the switch is false | `ODJ/ui/main/MainActivity.java:1075-1081`, `:1854-1855`. Not verified on a device |
| 70 | Domain hint setting, URL address bar setting, EULA entry | DEAD (commented out) | `ODJ/ui/settings/SettingsAppFragment.java:114`, `:122`, `:126` |
| 71 | `AccountInfoTask` (`GET /me`) | UNREFERENCED | the name occurs in 1 file, its own (`ODJ/task/AccountInfoTask.java`, 2 lines); control: `UploadFileTask` occurs in 5 files |
| 72 | `UploadFileTaskReplace` (an older upload path, 492 lines) | UNREFERENCED | the name occurs in 1 file, its own (3 lines) |
| 73 | "Create the destination folder if missing" in the upload task | DEAD (no caller passes the flag) | `ODJ/task/UploadFileTask.java:102-105`, `:181-182`, `:684-714`; both callers use the one-argument constructor: `ODJ/ui/preview/presenter/ScanPreviewPresenter.java:57`, `ODJ/ui/main/presenter/QuickAccessPresenter.kt:339` |
| 74 | Sensitivity labels (F89): **nothing in this tree** | absent | search of `ODJ` for `sensitivity`, case-insensitive: 0 files; control: `CommonSDKUtil` in 19 files. One line, as the commission asks: the OneDrive tree shows nothing of F89 |

Counts: **74 rows**: 63 live behaviours (rows 1 to 63), 3 personal-flavour findings (64 to 66), 8 rows of unreachable or absent code (67 to 74; row 69 is live as coded).

## 5. Every Microsoft call in the source

All Graph calls go to `<graphApi>/v1.0` (`ODJ/common/GraphProvider.kt:67`; the two hand-built URLs use the same base, `ODJ/task/UploadFileTask.java:386`, `ODJ/ui/main/presenter/QuickAccessPresenter.kt:106-115`). `{s}` site, `{d}` drive, `{l}` list, `{i}` item. "Select" means `$select=id,createdDateTime,lastModifiedDateTime,name,parentReference,size,folder,file,remoteItem,content.downloadUrl` (`ODJ/constants/OneDriveConstants.java:5`).

**Permissions named by the code or manifest: none for the live path.** The manifest names no Graph permission; the only scope strings in the tree are two unused constants, `offline_access user.read sites.readwrite.all` (business) and `offline_access user.read files.readwrite.all` (personal) (`ODJ/constants/OneDriveConstants.java:20-21`; unused: section 4.8 row 65). The live token's scopes are whatever HP Authentication Manager requested (report A1's subject). The "Needs" column is therefore stated from general knowledge of Microsoft Graph and was **not** checked against Microsoft's documentation (no network was used).

**Retry and throttling, for every row:** one retry on 401 after a token refresh (row 7). No `Retry-After` is read anywhere (search of `ODJ` for `retry-after`, case-insensitive: 0 lines; control: `conflictBehavior` 5 lines). 429 and 503 are shown as "too many requests". The only retry loop is the upload-piece loop (C21).

| # | Method and path | Used for | Paging | State | Needs (general knowledge) | Source |
|---|---|---|---|---|---|---|
| C1 | `GET /sites?search=*&$top=500` | all sites | all pages | LIVE | Sites.Read.All | `ODJ/task/GetAllSitesTask.java:33-39`, `:62-65` |
| C2 | `GET /sites?search=<q>&$top=500` | site search | all pages | LIVE | Sites.Read.All | `ODJ/ui/search/sites/task/RootSiteTask.java:56-62`, `:77` |
| C3 | `GET /sites/{s}/drives` | libraries of a site | first page only | LIVE | Sites.Read.All | `ODJ/task/GetDrivesTask.java:30-34` |
| C4 | `GET /sites/{s}/drives/{d}/list` | the list behind a library | n/a | LIVE | Sites.Read.All | `ODJ/task/GetLibraryMetadataTask.java:25-30` |
| C5 | `GET /sites/{s}/lists/{l}/columns` | column definitions | all pages | LIVE | Sites.Read.All | `ODJ/task/GetLibraryMetadataTask.java:36-46` |
| C6 | `GET /sites/{s}/drives/{d}/items/{i}/listItem` | list item id of a file (only when the listing did not give it) | n/a | LIVE | Sites.Read.All | `ODJ/task/UpdateLibraryFieldsTask.java:23-33` |
| C7 | `PATCH /sites/{s}/lists/{l}/items/{li}/fields` | write column values | n/a | LIVE | Sites.ReadWrite.All | `ODJ/task/UpdateLibraryFieldsTask.java:38-44` |
| C8 | `GET .../children` with Select and `$expand=thumbnails($select=large)`; in a library also `listItem` and `listItem($expand=fields)`. Eight path shapes: `/sites/{s}/drives/{d}/items/{i}`, `/sites/{s}/drives/{d}/root:/<path>:`, `/sites/{s}/drives/{d}/root`, `/drives/{d}/items/{i}`, `/me/drive/items/{i}`, `/me/drive/root:/<path>:`, `/drives/{d}/root`, `/me/drive/root`. No `$top` | folder listing (own drive, shared item, library) | all pages | LIVE | Files.Read (own), Files.Read.All (shared), Sites.Read.All (library) | `ODJ/task/GetListFolderTask.java:62-117`, `:121-157` |
| C9 | `GET /me/drive/recent` with Select | Recent | all pages | LIVE | Files.Read | `ODJ/task/GetRecentTask.java:43-69` |
| C10 | `GET /me/drive/sharedWithMe?allowexternal=true` with Select | Shared with me | all pages | LIVE | Files.Read.All | `ODJ/task/GetSharedListFolderTask.java:35-63` |
| C11 | `GET /me/drive/root/search(q='<q>')` or `/drives/{d}/root/search(q='<q>')` with Select, `$top=400` | file search | first page only | LIVE | Files.Read / Sites.Read.All | `ODJ/task/SearchCallableTask.java:114-136` |
| C12 | `POST /search/query` (entity type driveItem, from 0, size 400, 11 fields) | search in Shared with me | one request | LIVE | Files.Read.All (or Sites.Read.All) | `ODJ/task/SearchCallableTask.java:138-172` |
| C13 | `GET /drives/{d}/items/{i}` with Select | re-read each search hit of C12 (a failure is ignored) | n/a | LIVE | Files.Read.All | `ODJ/task/SearchCallableTask.java:204-220` |
| C14 | `POST .../children` (folder facet, `@microsoft.graph.conflictBehavior` = fail), the eight path shapes of C8 | create folder | n/a | LIVE | Files.ReadWrite(.All) / Sites.ReadWrite.All | `ODJ/task/CreateFolderTask.java:67-131` |
| C15 | `PATCH /drives/{d}/items/{i}` or `/me/drive/items/{i}` (name) | rename | n/a | LIVE | Files.ReadWrite(.All) / Sites.ReadWrite.All | `ODJ/task/RenameFileTask.java:58-71` |
| C16 | `DELETE /drives/{d}/items/{i}` or `/me/drive/items/{i}` | delete | n/a | LIVE | as C15 | `ODJ/task/DeleteFilesTask.java:52-65` |
| C17 | `GET /drives/{d}/items/{i}` then a plain GET of its `@microsoft.graph.downloadUrl` (no Graph token on that address; 5 s / 6 s) | download for print, only when the listing gave no download address | n/a | LIVE | Files.Read(.All) / Sites.Read.All | `ODJ/task/DownloadFileTask.java:76-93`; `ODJ/task/DownloadMultipleFilesTask.java:408-418` |
| C18 | `GET /drives/{d}/items/{i}/content?format=pdf` | Office to PDF | n/a | LIVE | as C17 | `ODJ/task/DownloadConvertToPdfFileTask.java:68-84`; `ODJ/task/DownloadMultipleFilesTask.java:320-322` |
| C19 | `PUT <item>:/<name>:/content?@microsoft.graph.conflictBehavior=fail`; four shapes: `/drives/{d}/items/{i}:/<name>:`, `/me/drive/root:/<path>/<name>:`, `/drives/{d}/root:/<name>:`, `/me/drive/root:/<name>:` | upload under 3.5 MB | n/a | LIVE | Files.ReadWrite(.All) / Sites.ReadWrite.All | `ODJ/task/UploadFileTask.java:234-283` |
| C20 | `POST <item>:/<name>:/createUploadSession`, body `{"item":{"@microsoft.graph.conflictBehavior":"fail"}}`, hand-built URL (four shapes: `/drives/{d}/items/{i}:/<name>:`, `/me/drives/{d}/items/root:/<path>:`, `/me/drive/items/root:/<path>:`, `/me/drive/items/{i}:/<name>:`), sent with OkHttp and a Bearer header built by hand from the stored token, **outside** the client that refreshes on 401 | start a large upload | n/a | LIVE | as C19 | `ODJ/task/UploadFileTask.java:378-415`, `:426-465`, `:85`, `:185-190` |
| C21 | `PUT <uploadUrl>` with `Content-Range`, 10 MiB pieces; 202 = next piece; retry on 408, 429, 5xx | the pieces of a large upload | n/a | LIVE | none (the session address is pre-authorised) | `ODJ/task/UploadFileTask.java:505-592`, `:596-601` |
| C22 | `GET .../permissions`: `/sites/{s}/drives/{d}/items/{i}`, `/sites/{s}/drives/{d}/root`, `/drives/{d}/items/{i}` | write-permission check | first page | LIVE | Files.Read(.All) / Sites.Read.All | `ODJ/ui/main/presenter/MainBasePresenter.java:947-991` |
| C23 | `GET /drives/{d}/items/{i}/children` | files of a selected folder for multi-download (quick-access folder print) | all pages | reachability not traced (section 13) | as C8 | `ODJ/task/DownloadMultipleFilesTask.java:206-252` |
| C24 | `GET /me/drive/root:/<path>:/children`, on 404 `POST` the folder, then list again | open a folder, creating it if missing | all pages | reachability not traced: one caller, `ODJ/ui/main/MainBaseFragment.java:1560`, whose own caller was not read | Files.ReadWrite | `ODJ/task/GetListFolderWithCreateFolderIfNotExistTask.java:47-55`, `:58-81`, `:124-152` |
| C25 | `POST /$batch` of `GET drives/{d}/items/{i}?$select=...` | refresh pinned quick-access items | n/a | DEAD (switch, row 67) | n/a | `ODJ/ui/main/presenter/QuickAccessPresenter.kt:84-116` |
| C26 | `GET /me` | user's profile | n/a | UNREFERENCED (row 71) | User.Read | `ODJ/task/AccountInfoTask.java:34-37` |
| C27 | `POST /me/drive/root.../children` | create the destination folder before upload | n/a | DEAD (row 73) | n/a | `ODJ/task/UploadFileTask.java:684-714` |
| C28 | the upload calls of `UploadFileTaskReplace` (`PUT ...content`, SDK `createUploadSession`, `PUT` pieces) | older upload path | n/a | UNREFERENCED (row 72) | n/a | `ODJ/task/UploadFileTaskReplace.java:248-268`, `:320-361` |

Counts by program (OneDrive app 4.4.1, business flavour): **28 rows; 22 live (C1 to C22), 2 whose reachability was not traced (C23, C24), 4 dead or unreferenced (C25 to C28).**

Not Graph and not Microsoft: Send to e-mail uses the Workpath SDK's device mail helper (row 57). No Graph `sendMail` exists in the tree (search of `ODJ` for `sendMail`, case-insensitive: 0 lines; control: `Email.send` 1 line). No Microsoft sign-in endpoint is called by this app: the only `login.microsoftonline.com` addresses are six commented-out lines (`ODJ/constants/OneDriveConstants.java:13-18`).

What the list means for scopes: C1 to C7 and the library forms of C8, C11, C14 to C20, C22 need a Sites scope; **C8 on `/drives/{d}` for a shared item, C10, C12 and C13 are the calls the SharePoint app does not make**: they read other people's drives ("Shared with me"). Whether delegated `Sites.ReadWrite.All` alone satisfies those four, or `Files.Read.All` / `Files.ReadWrite.All` is needed, is exactly the kind of statement that must be checked against Microsoft's documentation and on a tenant (section 12 question 2). The live calls show **no** need for `User.Read` in this app (C26 is unreferenced) and none for a mail scope.

## 6. Identity and secrets (LOCATIONS only)

During the read two tool outputs showed identifiers that are not credentials: (1) one search for the flavour constants printed `ODJ/constants/OneDriveConstants.java:9-10` unmasked; those two lines embed two application (client) ids inside redirect addresses; (2) `OD/app/packaging_release/hpk.xml:3` shows the app's Workpath UUID. Neither is repeated here. No password, key or token value was displayed at any point: every line of `OD/app/build.gradle.kts` that matches `password|client_id|clientid|api_k|secret` was replaced by its length before display.

| Location | What |
|---|---|
| `OD/[keystore file name withheld]` (2,523 bytes, tree root) | The release signing keystore, committed. **Not opened.** The same size as the SharePoint copy (A8 line 290) |
| `OD/app/build.gradle.kts:45`, `:47` | Keystore password and key password in clear text (masked; never displayed) |
| `OD/app/build.gradle.kts:44`, `:46` | Keystore path and key alias |
| `OD/app/build.gradle.kts:10-17` | A `config.properties` file one level above the tree root is expected to hold a key named `API_K_OD`; if the file is missing the build **creates it** with a placeholder value (`:13-15`). The file is not in the tree |
| `OD/app/build.gradle.kts:36-37`, `:55-56`, `:62-63` | Six masked lines in `defaultConfig` and the `release` and `debug` build types (build fields that carry the `API_K_OD` value or a client id). Their consumers: none in the app source: the only `BuildConfig` fields the source reads are `APPLICATION_ID`, `BUILD_TYPE`, `DEBUG`, `FLAVOR`, `VERSION_CODE` (count over `ODJ`) |
| `ODJ/constants/OneDriveConstants.java:9-10` | Two redirect addresses that each embed an application id (business, personal). Used by nothing (row 65) |
| `ODJ/constants/AppConstants.java:84-86` | The app's Workpath UUID as a constant |
| `ODJ/constants/AppConstants.java:6-7` | Imports of the OnGuard "locker"; no call to it anywhere in `ODJ` (search for `onguard\|Locker`, case-insensitive: those two import lines only) |
| `OD/OnGuardLib/src/main/cpp/` (8 `.h`, 6 `.cpp`) | The native locker that A4 line 151 says returns client id and secret material. **Not opened** |
| `OD/notes` (983 bytes), `OD/MIGRATION_NOTES.md` (7,367 bytes) | Not opened (section 13) |
| `OD/.github/workflows/*.yml` | `release.yml` read by search only; references to GitHub secrets by name were not looked for |

Weaknesses seen that the port should not carry over (none new in kind; A4 and A8 list the family): all four build types sign with the release key (`OD/app/build.gradle.kts:53`, `:59`, `:67`, `:73`); the Graph client logs at debug level in every build and the cloud configuration is logged (`ODJ/common/GraphProvider.kt:56-60`); token claims trusted without a signature check (row 5); status recovered by text search (row 62); the large-upload path sends the token on a client that cannot refresh it and retries a failing piece without limit (C20, C21, row 52); the download for printing has a 6 s read limit and no retry (row 45).

## 7. The common library's scan and print screens, and how the two apps use them

**Which copy was read.** The library tree `CommonValueLibraryCypher-master` (1.09.22). The copy the product owner sent (1.09.23) is at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1120/extracted/cvl/CommonValueLibraryCypher-master-2/` (the path A8 line 9 gives; the folder `OXPd_2/Source_Documents/` named in the commission does not exist in the project folder as of this read: a directory listing of `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/` shows `1_Project_Definition` to `5_Project_History` and `CLAUDE.md`). `diff -rq` of the two copies' `scan` folders: 0 differences; of their `print` folders: 0 differences (control: the `sharepoint` folders differ in 1 file, the one A8 line 240 names). So what follows holds for both copies. **Neither app links either copy**: OneDrive links the binary 1.09.21 and SharePoint the binary 1.09.20 (`OD/CVL/build.gradle:2`; `SP/CVL/build.gradle:2`); the screens inside those binaries were not read.

### 7.1 The scan option screen

One list of option groups, built in a fixed order and then pruned by what the device reports (`CVL/scan/ScanViewItems.java:27-42`, `:45-118`). Titles are the English strings of `CVLres/values/strings.xml`.

| # | Group (enum) | Title on the panel | Shown when | Source |
|---|---|---|---|---|
| S1 | `TYPE_RESOLUTION` | "File Type and Resolution" (holds "File Type", "Resolution", and by file type "Quality and File Size", "OCR Language", "PDF Encryption") | always; file type and resolution are each disabled if the device does not offer them | `CVL/scan/ScanViewItems.java:31`, `:46-53`; `CVL/scan/ScanOptionGroups.java:60`, `:67`, `:88`, `:113`, `:120`, `:141`; `CVLres/values/strings.xml:65`, `:103`, `:273`, `:329`, `:334`, `:407` |
| S2 | `ORIGINAL_DUPLEX` | "Original Sides" | device offers it | `CVL/scan/ScanViewItems.java:32`, `:54-58`; `CVLres/values/strings.xml:84` |
| S3 | `COLOR_MODE` | "Color/Black" | device offers it | `:33`, `:60-64`; strings `:91` |
| S4 | `ORIGINAL_SIZE` | "Original Size" | device offers it | `:34`, `:70-74`; strings `:5` |
| S5 | `ORIENTATION` | "Content Orientation" | device offers it | `:35`, `:76-80`; strings `:78` |
| S6 | `IMAGE_ADJUSTMENT` | "Image Adjustment" | device offers it | `:36`, `:94-98`; strings `:423` |
| S7 | `OPTIMIZE_TEXT_PICTURE` | "Optimize Text/Picture" | device offers it | `:37`, `:82-86`; strings `:368` |
| S8 | `CROP_MODE` | "Cropping Options" | device offers it | `:38`, `:100-104`; strings `:431` |
| S9 | `BLANK_PAGE` | "Blank Page Suppression" | device offers it | `:39`, `:88-92`; strings `:375` |
| S10 | `MULTI_FEED_DETECTION` | "Multi-feed Detection" | device offers it | `:40`, `:106-110`; strings `:381` |
| S11 | `SPLIT_ATTACHMENT` | "Document Separation" | when the option reports itself available (the rule inside `ScanSplitAttachmentOption.kt` was not read) | `:41`, `:113-117`; strings `:387` |
| n/a | `COLOR_DROPOUT_MODE` | (colour dropout) | **never**: removed and disabled unconditionally | `CVL/scan/ScanViewItems.java:66-68` |
| n/a | `FILE_NAME` | "File name" | not in this list: each app draws its own file-name field (row 50) | `CVL/scan/ScanOptionGroups.java:81` |

Eighteen groups are defined in the enum (`CVL/scan/ScanOptionGroups.java:46-171`), eleven are put in the list. Per-format screens exist for JPEG, OCR, PDF/A and XPS, PDF, RTF and HTML, TIFF and MTIFF (`CVL/scan/view/option/FileType/`, 11 files). **The values inside each option (the resolutions, the sizes, the formats offered) were not read**: 16 option fragment classes and 20 option classes, section 13.

### 7.2 The print option screen

| # | Group (enum) | Title | Shown when | Source |
|---|---|---|---|---|
| P1 | `NUMBER_OF_COPIES` | "Number of copies" | always | `CVL/print/PrintViewItems.java:28`; `CVLres/values/strings.xml:178` |
| P2 | `ORIGINAL_DUPLEX` | "Output Sides" | device offers it | `:29`, `:53-57`; strings `:85` |
| P3 | `COLOR_MODE` | "Color/Black" | not on a mono device | `:30`, `:48-51`; strings `:91` |
| P4 | `FINISHINGS` | "Finishings" | device offers it | `:31`, `:59-63`; strings `:120` |
| P5 | `PAPER_SELECTION` | "Paper Selection" (holds "Paper Size", "Paper Tray", "Paper Type", each disabled if not offered) | always | `:32`, `:71-84`; strings `:149`, `:151`, `:165`, `:435` |
| P6 | `COLLATE_MODE` | "Collate" | device offers it | `:33`, `:86-90`; strings `:316` |
| P7 | `PAGE_RANGE` | "Page Range" | always | `:34`; strings `:183` |
| P8 | `SENSITIVITY_LABEL` | (sensitivity label) | only when an app has registered a label provider | `:36-38` |
| n/a | `ORIENTATION`, `AUTO_FIT`, `STAPLE_MODE` | "Auto-fit", "Staple" | defined, not put in the list (the orientation pruning is commented out, `:41-46`; staple is pruned from a list it was never added to, `:65-69`) | `CVL/print/PrintOptionGroups.java:37`, `:92`, `:98` |

Fourteen groups defined (`CVL/print/PrintOptionGroups.java:37-116`), seven listed, an eighth conditional. One defect to leave behind: when the paper **source** is not available the code disables the paper **size** option (`CVL/print/PrintViewItems.java:81-84`).

Strings: the library's English file has 435 strings, 319 of them named `option_...`; `de`, `es`, `fr`, `in`, `it`, `pt`, `zh-rTW` have 337 each (241 `option_`), and there is a ninth set, Japanese, with 328 (counts of `<string ` per `CVLres/values*/strings.xml`). Neither app ships a Japanese string file of its own (section 3; A8 line 54).

### 7.3 What the two apps take from the library, and what differs

Both apps import **the same sixteen** scan and print classes of the library, and no others from those two packages (import search over `OD/app/src` and `SP/app/src/main/java`): `print.handler.PrintJobProgressHandler`, `print.view.preview.OnShowActionBarListener`, `PrintContentPreviewFragment`, `PrintPreviewFragment`, `PrintSubOptionsFragment`, `PrintSubPreviewZoomFragment`, `scan.handler.ScanJobProgressHandler`, `scan.option.ScanDocumentFormatOption`, `ScanFileNameOption`, `ScanOriginalDuplexOption`, `scan.ScanOption`, `scan.ScanOptionGroups`, `scan.view.dialog.SimpleDividerItemDecoration`, `scan.view.option.ScanOriginalDuplexFragment`, `scan.view.preview.ScanPreviewFragment`, `ScanSubOptionsFragment` (OneDrive 25 import lines, SharePoint 30; the difference is one class imported in 5 SharePoint files against 1, and `PrintPreviewFragment` 4 against 3).

| Point | OneDrive 4.4.1 | SharePoint 4.4.6 | Source |
|---|---|---|---|
| Scan and print screens | the library's, as 7.1 and 7.2 | the same | import search above |
| Library binary | 1.09.21 | 1.09.20 | `OD/CVL/build.gradle:2`; `SP/CVL/build.gradle:2` |
| Administrator defaults for both screens | 7 print and 19 scan fidgets | the same 7 and 19 | `OD/app/moc_file/OneDrive.moc` (ids at `:19-2962`); A8 line 64 |
| Document separation default | in the `scanConfig` frame | under `appConfig` | `OD/app/moc_file/OneDrive.moc:3025` (before `appConfig` at `:3079`); A8 line 64 |
| What the app adds to the scan screen | file name, Send to e-mail | file name, Send to e-mail, **one input per editable library column** | rows 50, 55, 56; A8 row 53 |
| Sensitivity-label print option (P8) | never: no provider in the tree | provider present, compiled off | row 74; A8 row 68 |
| Settings entries that open the two option screens | default print options, default scan options (administrator) | the same | `ODJ/ui/settings/SettingsAppFragment.java:100-108`; A8 row 58 |

So the shared screens are used identically; the differences are in what each app wraps around them.

## 8. Doubts and oddities in the source (not behaviour to copy)

1. **A library upload can be addressed to the user's own drive.** In the small-file path the second branch (`/me/drive/root:/<path>/<name>`) is taken whenever there is a path and no item id, before the code asks whether the destination is a shared library (`ODJ/task/UploadFileTask.java:254-277`). Whether a library destination can arrive with a path and no item id was not traced (section 13).
2. **The large-file path for a library with no item id builds `/me/drives/{d}/items/root:/<path>:/createUploadSession`** (`ODJ/task/UploadFileTask.java:402-405`), a different address shape from every other library call in the app (`/sites/{s}/drives/{d}/...` or `/drives/{d}/...`). Not tested.
3. **A null-pointer error during a page of a listing is swallowed** and the loop goes on (`ODJ/task/GetListFolderTask.java:143`; the same in `GetRecentTask.java:61`, `GetSharedListFolderTask.java:54-55`).
4. **Search in Shared with me makes one extra request per hit**, up to 400 (`ODJ/task/SearchCallableTask.java:193-198`, `:204-220`), with no throttling handling.
5. **The sites list follows every page before showing anything** (`ODJ/task/GetAllSitesTask.java:51-66`): on a tenant with thousands of sites this is many requests of 500.
6. **Create folder is checked twice in two ways**: a case-insensitive comparison with the names on screen, then Graph's own conflict rule; a source comment says the SDK's conflict behaviour "do not work properly" (`ODJ/ui/main/MainBaseFragment.java:897-904`; `ODJ/task/CreateFolderTask.java:128`).
7. **`OneDriveConstants` still calls the business scope `sites.readwrite.all`** while the app's own places (My Drive, Recent, Shared with me) are drive calls; the constant is unused (row 65), so it documents an intention, not behaviour.

## 9. F87: can `isSIOEnabled` ever be true in a shipped build?

Starting points read first: report A2 line 132 (quick messages are "only for signed-in (SIO) users", `SendFragment.kt:561-627`, `MainActivity.kt:398-410`) and A4 line 290 ("`isSIOEnabled()` returns false always ... every `isSIOEnabled` branch is dead").

1. **Where the switch is.** It is not a setting, a field or a configuration key. It is a method of the common library, `WorkpathAccessService.isSIOEnabled()`, whose first statement is `if (true) { return false; }` (`CVL/sdk/WorkpathAccessService.java:137-140`); the original logic after it (`:142-147`) cannot run. `isHPCloudUser()` is the same (`:108-111`). Nothing sets it: a search of the library source for `SIOEnabled`, case-insensitive, finds the definition and one caller, `CVL/ui/eula/EulaMainFragment.java:191`; no setter, no field.
2. **What Mailflow links.** The binary `commonvaluablelibrary-1.09.20.aar` (`HPAM - Docs and Notes/Source Code/MailFlow-main/app/build.gradle.kts:183`; the file is `MailFlow-main/app/libs/commonvaluablelibrary-1.09.20.aar`). That is older than the library source read, which is why A4 and A8 could only say "the source says false".
3. **The binary itself, read as bytes (new in this report).** The compiled method was read out of the archive with a class-file parser written for this read (no tool from the tree, nothing executed from it; script: `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/b4ad0f1c-3b01-4b93-8878-0f4f8805f9d5/scratchpad/tools/code_of.py`, a session file that will not persist). In `com/hp/print/commonvaluablelibrary/sdk/WorkpathAccessService.class` of **Mailflow's 1.09.20 binary**, `isSIOEnabled()Z` has a code length of 2 bytes, `03 ac`: push the constant 0, return it. The same two bytes for `isHPCloudUser()Z`. Control from the same class: `isAdmin()Z` is 64 bytes of real logic. The same result in OneDrive's 1.09.21 binary and in SharePoint's 1.09.20 binary.
4. **Mailflow cannot get a true from elsewhere.** No class in Mailflow or OneDrive extends or replaces `WorkpathAccessService` (search for `extends WorkpathAccessService|: WorkpathAccessService(|class .*WorkpathAccessService`: 0 lines; control: `WorkpathAccessService.getInstance` 16 lines in Mailflow). Mailflow calls the switch on 5 lines; the two that carry quick messages are the menu entry (`MailFlow-main/app/src/main/java/com/hp/print/mailflowas/ui/main/MainActivity.kt:400-404`: the "Quick messages" group is set to GONE when false) and the compose-screen button (`.../ui/send/SendFragment.kt:626-628`: `isSIOEnabled && quickMessage.isEnableQuickMessage`). The screen `QuickMessagesActivity` is started from one place only, the click handler of that hidden menu entry (`MainActivity.kt:405-409`).

**Answer: DEAD.** In the source and in the binary Mailflow ships with, the switch is the constant false, nothing can set it, and both doors to quick messages are behind it. This holds for any build made from this tree with the library binary that is in it. What the code cannot show is whether the build installed on customers' printers was made from this tree; that is a question about release records, not about a printer's behaviour, and `02:175`'s rule ("a requirement only if a Workpath 4.4 printer shows it") stays as the final check if anyone doubts the provenance.

The same evidence settles, for the same reason, every other row that rests on this switch in the three binaries read: OneDrive rows 67 and 68 here, and report A8's rows 65 to 67 and its open question 1 (SharePoint quick access), which A8 could not close because the binary "was not decompiled" (A8 line 73).

Not settled here: the Teams rows F82 and F83 (quick access) rest on the same method in the binary Teams links (1.09.22 per A8 line 260). The 1.09.22 **source** returns false (item 1); the Teams tree and its binary were not read in this lane (section 12 question 5).

## 10. Comparison with the documents

Rows of `02` that name OneDrive or the shared scan and print screens.

| Row (`02` line) | What it says | Verdict | Source side |
|---|---|---|---|
| F31 (`:91`) | scan options and formats | **Confirmed** for the option groups (sides, colour, size, orientation, resolution, image adjustment, blank page, multi-feed, plus cropping and optimise text/picture, which the row does not name); formats and the 75-600 range **not re-read** | 7.1 rows S1 to S10 |
| F32 (`:92`) | scan preview with remove, rescan, add page | **Still unknown** from source: the library's `ScanPreviewFragment` (364 lines) was not read | section 13 |
| F33 (`:93`) | print with sides, colour, paper size/tray, collate, copies, page range | **Contradicted by omission**: the option list also has Finishings and Paper Type | 7.2 rows P4, P5 |
| F34 (`:94`) | Office to PDF through Graph | **Confirmed** for OneDrive | C18; row 44 |
| F37 (`:97`) | "OneDrive: browse, scan to folder, print, rename, delete, create folder, search, sort, tile/list" | **Contradicted by omission**: the app also has Recent, Shared with me, Shared libraries (sites, libraries, column sort and group, column edit), size sort, direct print by swipe, multi-select print, a quota message, and write-permission gating | rows 18 to 27, 31, 40, 42, 46, 54 |
| F38 (`:98`) | optional Send to e-mail through device SMTP, default off | **Confirmed**; adds: at most 5 recipients, a failure e-mail when the upload fails | rows 56, 57 |
| F39 (`:99`) | SharePoint metadata at scan | **Confirmed as a SharePoint-app behaviour only**: the OneDrive app's own route into the same libraries has no metadata at scan | row 55 |
| F41 (`:101`) | roaming store keys | **Incomplete**: names the `sharepoint.` keys only; OneDrive's are prefixed `onedrive.` and include three that SharePoint has not (`library_columns`, `library_column_state`, `predefined_column_state`) | row 14 |
| F70 (`:158`) | document separation at scan | **Confirmed** as an option group of the shared scan screen ("Document Separation"); when it is offered was not read | 7.1 row S11 |
| F71 (`:159`) | file naming | **Confirmed** for OneDrive | rows 50, 51 |
| F72 (`:160`) | preview before printing, and direct print | **Confirmed** for OneDrive | rows 41, 42 |
| F73 (`:161`) | password-protected PDF, TIFF printing | **Still unknown**: a `PdfPasswordHandler.kt` exists in the library's print preview and was not read | `CVL/print/view/preview/PdfPasswordHandler.kt` |
| F87 (`:175`) | quick messages, conditional on the switch | **Settled: dead** in source and in the shipped binary | section 9 |
| F89 (`:177`) | sensitivity labels | **Confirmed** (nothing in OneDrive); out of scope by C-38 | row 74 |
| F93 (`:200`) | actions offered only with write permission; "whether the scan button is withheld too is not established" | **Established for the OneDrive app**: the scan button and Create folder follow the same write-permission flag; the button is also hidden on a device with no scanner. The SharePoint app's own method remains unread | `ODJ/ui/main/MainBaseFragment.java:864-866`, `:1583-1596`; `ODJ/ui/main/MainActivity.java:2098` |
| F94 (`:201`) | SharePoint printable types, limits, messages, swipe | **Same in OneDrive** except one message: OneDrive has the conversion time-out message and no separate "protected document" branch | rows 43, 44; `ODJ/task/DownloadConvertToPdfFileTask.java:116-123` |
| F95 (`:202`) | scan never overwrites | **Same in OneDrive** | row 53 |
| F96 (`:203`) | administrator gets settings only | **Same in OneDrive** | row 4 |
| Section 5.6.3 (`:504`) | "OneDrive: `/me/drive` browse, search, sort, tile/list, rename, delete, create folder, scan to folder, print" | **Contradicted by omission**, as F37 | rows 18 to 27 |
| Section 7.2 (`:703`) | delegated `Files.ReadWrite.All`, `Sites.ReadWrite.All`, `User.Read` for OneDrive/SharePoint | **Still unknown**: the code names no scope for the live path; the calls that reach other people's drives (C8 on a shared item, C10, C12, C13) are the ones a Files scope would be for; no live call needs `User.Read` | section 5 |
| Coverage note (`:7`), P3 (`:36`), R17 (`:927`), B1765 "not changed" line (`:1065`) | the OneDrive half is unread | **Out of date** from this report on | this report |
| OQ-4 (`:23`, `:504`, `:900`) | personal flavour not ruled | **Confirmed and strengthened**: two code branches differ, no sign-in path, not packaged | rows 64 to 66 |

Counts: 22 rows compared: **12 confirmed** (F31 in part, F34, F38, F39, F70, F71, F72, F89, F94, F95, F96, OQ-4); **3 contradicted, all by omission** (F33, F37, section 5.6.3; F37 and 5.6.3 are one fact stated twice); 1 incomplete (F41); 2 settled that were open (F87, F93); 3 still unknown (F32, F73, section 7.2); 1 group out of date (the coverage statements).

## 11. PROPOSED CORRECTIONS (none applied)

1. `02:97` (F37): replace the behaviour text with "OneDrive: four places (My Drive, Recent, Shared with me, Shared libraries); browse, scan to folder, print (preview, direct by swipe, multi-select), rename, delete, create folder, search, sort (date, name, size), tile/list; actions and the scan button only with write permission". Source: `ODJ/ui/main/MainActivity.java:750-823`; `ODJ/sort/SortingType.kt`; `ODJ/ui/main/MainBaseFragment.java:864-866`.
2. `02:97` area: add a feature row "OneDrive Shared libraries: sites (all pages), the last 3 sites, libraries, files with library column values, sort and group by a column, edit column values of an existing file; **no** metadata at scan from this route". Source: `ODJ/task/GetAllSitesTask.java:33-65`; `ODJ/task/GetLibraryMetadataTask.java:25-48`; `ODJ/ui/main/MainBaseFragment.java:629-633`; `ODJ/ui/preview/BaseScanDescriptionAppFragment.java`.
3. `02:97` area: add a feature row "OneDrive: a full storage quota gives its own message at scan upload". Source: `ODJ/task/UploadFileTask.java:728-769`; `ODJ/error/ErrorHandlingUtils.java:61-62`.
4. `02:97` area: add a feature row "OneDrive search: own drive and libraries by drive search (first 400), Shared with me by the Microsoft Search API (first 400); last 3 terms kept". Source: `ODJ/task/SearchCallableTask.java:114-172`; `ODJ/ui/search/SearchActivity.java:187-193`.
5. `02:93` (F33): add "finishings" and "paper type" to the list of print options. Source: `CVL/print/PrintViewItems.java:28-34`, `:71-84`.
6. `02:91` (F31): add "cropping" and "optimise text/picture" to the list of scan options, and state that colour dropout is never offered. Source: `CVL/scan/ScanViewItems.java:30-41`, `:66-68`.
7. `02:98` (F38): add "at most 5 recipients; when the upload fails a failure e-mail is sent to the recipients, else to the user". Source: `ODJ/ui/preview/ScanDescriptionAppFragment.java:308-309`; `ODJ/ui/preview/presenter/ScanPreviewPresenter.java:112-148`.
8. `02:101` (F41): add "OneDrive's keys are prefixed `onedrive.`: `quick_access`, `recent_searches`, `recent_site_searches`, `recent_sites`, `library_columns`, `library_column_state`, `predefined_column_state`". Source: `ODJ/storage/UserPreferencesStore.kt:14-24`.
9. `02:175` (F87): replace the Condition sentence with "Dead: the switch is a method of the common library that returns the constant false, in the source (`WorkpathAccessService.java:137-140`) and in the 1.09.20 binary Mailflow links (method body `03 ac`); not a requirement; F41 roams the data either way `[A11 §9]`". Source: section 9.
10. `02:200` (F93): replace "Whether the scan button is withheld too is not established in A8; settled in WP3.4" with "In the OneDrive app the scan button follows the same write-permission flag `[A11 §10]`; the SharePoint app's own rule is settled in WP3.4". Source: `ODJ/ui/main/MainBaseFragment.java:864-866`, `:1583-1596`.
11. `02:504` (section 5.6.3): replace "OneDrive: `/me/drive` browse, search, sort, tile/list, rename, delete, create folder, scan to folder, print" with the four places of correction 1, and add "the OneDrive app's file listing sets no page size and follows every page; the SharePoint app asks for 20 a page". Source: `ODJ/task/GetListFolderTask.java:121-157`; A8 row 20.
12. `02:703` (section 7.2): add "The OneDrive source names no scope for its live path; 22 live Graph calls `[A11 §5]`, of which four read other users' drives (Shared with me): whether `Sites.ReadWrite.All` covers them is checked on a tenant, not assumed; no live OneDrive call needs `User.Read`". Source: section 5; `ODJ/constants/OneDriveConstants.java:20-21`.
13. `02:7` (coverage note): replace "A full read of that tree is work package WP0.6 in document 2" with "That tree is now read: report A11 (74 rows, 28 Microsoft calls of which 22 live); what A11 did not open is listed in its section 13". Source: this report.
14. `02:927` (R17): replace "the risk now rests on the OneDrive half, which is still unread" with "the OneDrive half is read (A11); the risk rests on what A8 and A11 list as not opened, and on nothing having been run". Source: this report, section 13.
15. `03:142` (WP0.6): replace "**What is left of this package:** the OneDrive tree (unread); the common-library scan and print screens as the SharePoint app uses them (A8 did not re-read them); F87; and" with "Done by A11: the OneDrive tree, the shared scan and print screens (which groups, which titles; the values inside each option are not read), F87 (dead). **What is left:**". Source: this report.
16. `03:185` (WP3.9) and `02:504`: add to the reason "and the personal flavour differs from the business one in two code branches only and has no sign-in path of its own `[A11 rows 64-66]`". Source: `ODJ/ui/main/MainActivity.java:337-338`; `ODJ/constants/AppConstants.java:76-80`.
17. Report A8 line 311 (open question 1) and `03:142`'s "a look at a Workpath printer running SharePoint 4.4.6 for the rows A8 marks dead": add "the 1.09.20 binary the SharePoint app links returns the constant false from `isSIOEnabled` `[A11 §9 item 3]`, so rows 65 to 67 no longer need the printer look; the look is still wanted for the manual's 4 custom fields". Source: section 9.

## 12. Open questions for the product owner (through Tuesday, to the master list)

1. **Does the OXPd OneDrive tile carry all four places the Workpath app has (My Drive, Recent, Shared with me, Shared libraries)?** Why: `02` describes My Drive only; Shared with me alone accounts for four extra Graph calls and a second search method. *Default (Tuesday's, under the full-match ruling C-16):* yes, all four.
2. **Scopes for Shared with me.** The live token is HP Authentication Manager's; this report cannot say whether `Sites.ReadWrite.All` is enough for `sharedWithMe` and the Search API. *Default:* keep `Files.ReadWrite.All` in the registration as `02:703` has it, and let the first-run scope check on a tenant decide; no change to the consent text until then.
3. **SharePoint libraries are reachable from both apps, with different scan behaviour** (metadata inputs at scan in the SharePoint app, none in the OneDrive app). In one server module, does each tile keep its own Workpath behaviour? *Default:* yes: each tile matches its Workpath app exactly.
4. **F87: is "dead in source and in the binary" enough to drop Mailflow quick messages from release 1 without a printer look?** *Default:* yes; F41 still roams the stored data.
5. **Teams quick access (F82, F83) rests on the same switch.** The library source says false for the version Teams links; the Teams tree was not read here. *Default:* Tuesday has the Teams gating and binary checked (the method of section 9 item 3) before any work package builds F82 or F83.
6. **OQ-4, the personal flavour.** The code gives no sign it shipped (rows 64 to 66). *Default:* out, as the design already takes it.
7. **Do the shipped apps show their seven translations?** The build file filters library resources to English (`OD/app/build.gradle.kts:39-41`); whether that removes the app's own translations from the package was not tested. *Default:* build all eight languages as the string files have them; confirm on a Workpath printer when one is at hand.

## 13. What was NOT read

- **OneDrive tree, read whole** (imports, blank lines and log lines stripped from display): `constants/` (2 files), `auth/` (4 of 5; `BaseAuthManager.java`, 4 lines, not), `common/GraphProvider.kt`, `HttpClient.kt`, `NetworkTimeouts.java`, `SecuredPreferences.kt`, `UserManagementHolder.kt`, `CommonApp.java`; 16 task classes (`AccountInfo`, `GetAllSites`, `GetDrives`, `GetLibraryMetadata`, `UpdateLibraryFields`, `GetRecent`, `GetSharedListFolder`, `GetListFolder`, `GetListFolderWithCreateFolderIfNotExist`, `CreateFolder`, `DeleteFiles`, `RenameFile`, `DownloadFile`, `DownloadConvertToPdfFile`, `SearchCallable`, `UploadFile`) and `ui/search/sites/task/RootSiteTask.java`; `BaseScanDescriptionAppFragment.java`; `MainViewType`, `SharedLibrariesStep`; the manifest; `app/build.gradle.kts` (masked); `build.gradle.kts`; `hpk.xml`; `packaging_release/readme`.
- **Read in part (line ranges and searches):** `MainActivity.java` (lines 205-345, 690-840, 940-1100, 1200-1360 of 2,104); `MainBaseFragment.java` (150-215, 540-640, 880-905, 1580-1594 of 1,918, plus searches); `MainBasePresenter.java` (936-1000 of 1,095, plus its method list); `DownloadMultipleFilesTask.java` (196-216, 250-257, call sites); `ScanPreviewPresenter.java` (45-177); `SettingsAppFragment.java` (100-140); `ErrorHandlingUtils.java` (30-168); `SortingType.kt` (first 30 lines); by search only: `SplashActivity.java`, `ScanDescriptionAppFragment.java`, `ScanPreviewAppFragment.java`, `EmailSender.java`, `SendEmailTask.java`, `UserPreferencesStore.kt`, `AppConfigHelper.java`, `FolderNavigationCache.java`, `SearchActivity.java`, `SitesSearchActivity.java`, `Utils.java`, `QuickAccessPresenter.kt`, `UploadFileTaskReplace.java`, `settings.gradle.kts`, `release.yml`.
- **Not opened at all:** `QuickAccessFragment.kt`, `AppGuideActivity` and its three helpers, all seven dialog classes, adapters and view holders, the model and response classes, the comparators, `DirectoryHelper`, `FallbackDns`, `Loggable`, `NetworkUtils`, `SwipeUtil`, `ValidationHelper`, `ValidationUtils`, `LibraryColumnMapper.kt`, the settings sub-screens (domain hint, e-mail, quick access, URL bar), `PrintPreviewAppActivity`, `PrintPreviewZoomAppActivity`, `ScanPreviewAppActivity`, `InformationActivity`, `OpenSourceActivity`, `LogoutActivity`, `SearchPresenter`, `SitesSearchPresenter`, the `lib/mvp` classes, the unit test; the 175 XML files except string counts and eight flavour strings; `OneDrive.moc` beyond its frame and fidget ids; the EULA files, the two `.puml` diagrams, `opensource_license.html`; **`OD/notes` and `OD/MIGRATION_NOTES.md`**; `build.yml`, `codeql.yml`, `gitleaks.yml`; `gradle.properties`.
- **Consequences to keep in mind:** two calls are listed with reachability not traced (C23, C24); the condition under which a library destination with a path and no item id could fall into the own-drive upload branch (`ODJ/task/UploadFileTask.java:259-264`) was not traced; the paging of the folder list on screen (the fragment's "load more" footer) was not read, only the task's page loop.
- **Never opened, by rule:** `OD/[keystore file name withheld]`; the OnGuardLib native sources and Java classes.
- **Binaries:** not decompiled. From three `commonvaluablelibrary` archives exactly one class was read, `sdk/WorkpathAccessService.class`, and of it three method bodies as bytes (section 9). The scan and print screens **inside the binaries the apps link** (1.09.20, 1.09.21) were not read; section 7 is the 1.09.22 source.
- **Common library:** read whole: `scan/ScanViewItems.java`, `print/PrintViewItems.java`; read in part: `sdk/WorkpathAccessService.java:104-142`, `utils/CommonSDKUtil.java:186-198`, the title lines of `ScanOptionGroups.java` and `PrintOptionGroups.java`, string counts and 27 title strings. **Not opened:** every option class and option fragment (so no option's values are listed), `ScanSubOptionsFragment` (459 lines), `PrintSubOptionsFragment` (557), `ScanPreviewFragment` (364), `PrintPreviewFragment` (731), `PdfPasswordHandler.kt`, `ScanSplitAttachmentOption.kt`, both service classes (A4 covers them).
- **SharePoint tree:** one import search and one archive read; nothing else (A8 is its report).
- **Mailflow tree:** `MainActivity.kt:386-412`, `SendFragment.kt:622-628`, `app/build.gradle.kts` by search, four searches. **Teams tree:** not opened.
- **Documents:** A3 and A8 read whole; A4 by search (the lines naming OneDrive, the library or the switch); A2 line 132 only; `02` by search for the F rows and the lines cited; `03` lines 142 and those naming OQ-4; `05` and CLARIFICATIONS were **not** read whole (searched for OQ-4 only; C-38 and C-16 are cited as the commission and `02` state them).
- **Nothing was built or run. No statement here was checked on a printer or against Microsoft's documentation.** The "Needs" column of section 5 is general knowledge, not a checked fact.

