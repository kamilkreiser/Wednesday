# A8: the SharePoint app source and the common library (supplied 2026-11-20)

Lane A8 of the Datasec / OXPd analysis, written 2026-11-20 under commission B1760. Read-only analysis of the two source trees the product owner attached to the live board on 2026-11-20 (CLARIFICATIONS C-33). It fills the SharePoint half of the gap that reports A3 and A4 left open (report A4 lines 237, 301; open question OQ-7).

Path conventions used for sources in this report:

- `SP/` stands for the root of the SharePoint tree, `CypherSharePoint-main/` (on disk: `2_Project_Files/fleet/state/kam_attachments_1120/extracted/sp1/CypherSharePoint-main/`).
- `SP-J/` stands for `SP/app/src/main/java/com/hp/print/cypher/sharepoint/`.
- `CVL2/` stands for the root of the common library tree, `CommonValueLibraryCypher-master-2/` (on disk: `.../extracted/cvl/CommonValueLibraryCypher-master-2/`).
- `CVL2-J/` stands for `CVL2/commonvaluablelibrary/src/main/java/com/hp/print/commonvaluablelibrary/`.
- `OD/` stands for the OneDrive tree in the read-only library copy, `HPAM - Docs and Notes/Source Code/CypherOneDrive-main/`.
- Every claim carries `path:line`. Line numbers are those of the file as supplied.

Secrets rule (C-3): no secret value is reproduced anywhere in this report. Section 8 gives locations only.

## 1. BLUF

1. **The SharePoint app's source is now in hand, and it is a separate app.** `CypherSharePoint-main` builds one APK and one HPK, "SharePoint for Authentication Suite", package `com.hp.print.cypher.sharepoint`, version 4.4.6, with the UUID the licence portal lists (`SP/packaging_release/hpk.xml:3-4`; `SP/app/build.gradle.kts:20`, `:45`). It is not a flavour of the OneDrive tree: the two are sister code bases that share 143 of their class names (section 7).
2. **What the app does is small and clear.** Sites (all, recent, search) → libraries → folders; print (preview, or swipe for direct print) with Office files converted by Graph; scan to the open folder with library metadata; create folder, rename, delete, edit column values; optional e-mail of the scan through the device's SMTP. 64 live behaviours are listed with their source lines (section 4), and 18 live Graph calls (section 5.2).
3. **It has no sign-in and no credential of its own.** The token comes from HP Authentication Manager; refresh on 401 is one call back to it. The app's own Microsoft sign-in screen is still in the source and is started by nothing (rows 2, 7, 69).
4. **Three things in the source are not in the product.** Quick access and "remember me" sit behind the HP switch that always returns false; sensitivity labels (read, choose at scan, block "Do Not Print") are complete enough to read and are compiled off by one constant (rows 65 to 68). None is a parity requirement unless a printer shows it or the product owner asks for it.
5. **The manual and the source disagree in two places.** The manual says four custom fields at scan; the source offers one input for every editable column of five types, with no cap (row 53). The documents say six languages; this app ships eight (row 62).
6. **The common library that came with it is the one already analysed.** `CommonValueLibraryCypher-master-2` is version 1.09.23; it differs from the library copy (1.09.22) in 2 files of 798: the version line and one added date-formatting function. Report A4 stands for it. It provides device services and UI, and no authentication, licensing or logging framework (section 6).
7. **Buildable to parity from source: yes for the SharePoint app's own behaviour, with three reservations.** The library the app links is a binary one to three versions older than the library source read (the scan and print screens inside it were not re-read); nothing was built or run; and one module named in the build settings (`:mtl`) is not in the archive (section 9 question 3).
8. **The gateway source is still missing.** Neither tree is the gateway.

## 2. Coverage

| Area | Files | Read whole or nearly | Read in part / by search | Not opened |
|---|---|---|---|---|
| `CypherSharePoint-main` | 553; 220 source files under `app/src/main/java` (31,158 lines) | about 30: build files (4), manifest, 4 workflows, `hpk.xml`, packaging readme, `auth/` (6 of its 8 files), `GraphProvider`, `HttpClient`, constants (2), `AppConfigHelper`, `SplashActivity`, `SecuredPreferences`, `AppDataHolder`, 14 of 17 task classes | about 25, by method list, line ranges and search: the three largest UI classes (about 40% of their 5,635 lines), upload and multi-download tasks, scan screens, sites, search, settings, sensitivity provider, e-mail sender, stores, error mapping | about 165 source files (dialogs, adapters, view holders, models, comparators, quick access, app guide, the dead sign-in screen), 157 XML resources apart from counts, assets, the keystore, OnGuardLib sources |
| `CommonValueLibraryCypher-master-2` | 798 | 3 short files and the build version line | 4 files by search; whole-tree `diff -rq` against the library copy; package and file counts | everything else: covered by report A4 through the 2-file diff |
| `CypherOneDrive-main` (library copy, comparison only) | 532 | none | file-name list, build file by search, 4 searches | all source |

Section 10 gives the full list of what was not read. How the read was steered: every class that calls Graph was found by search and read first; UI classes were read where a menu, a button or a switch decides whether a behaviour is reachable.

## 3. Inventory

### 3.1 The SharePoint tree

- 553 files (count by `find -type f`). By extension: 198 `.java`, 157 `.xml`, 106 `.png`, 36 `.kt`, 8 `.htm`, 8 `.h`, 6 `.cpp`, 4 `.yml`, 4 `.kts`, 4 `.aar`, and single files. Under `SP/app/src/main/java`: 184 `.java` and 36 `.kt`, 31,158 lines.
- The second archive the product owner sent (`extracted/sp2/CypherSharePoint-main`) is the same tree: `diff -rq` between the two reports 0 differing files.
- Gradle (Kotlin DSL) project named `CypherSharePoint` (`SP/settings.gradle.kts:44`) that includes five modules: `:app`, `:usermanagement`, `:mtl`, `:CVL`, `:OnGuardLib` (`SP/settings.gradle.kts:45`). **There is no `mtl` directory in the tree** (a directory listing of `SP/` shows `app`, `app_icons`, `CVL`, `OnGuardLib`, `packaging_release`, `usermanagement`, `gradle`, `.github`). Whether Gradle tolerates the missing module was not tested: nothing was built (section 9).
- One application, no product flavours: `flavorDimensions += "default"` is declared and no flavour is defined (`SP/app/build.gradle.kts:127`). This differs from the OneDrive tree, which has two flavours (report A4 line 237).
- Package and namespace `com.hp.print.cypher.sharepoint` (`SP/app/build.gradle.kts:20`; `SP-J/constant/AppConstants.java:17`). This is the package HP Authentication Manager expects (report A4 line 125).
- Version **4.4.6**, version code `4_04_06_00` (`SP/app/build.gradle.kts:44-45`). Compile SDK 35, min SDK 31, target SDK 35 (`SP/build.gradle.kts:7-9`). Java 11 (`SP/app/build.gradle.kts:129-132`). Android Gradle Plugin 8.13.1, Kotlin 1.9.10 (`SP/settings.gradle.kts:28-29`).
- Four build types: `debug`, `debugautotest`, `release`, `releaseautotest` (`SP/app/build.gradle.kts:53-92`). All four sign with the one `release` signing configuration (`SP/app/build.gradle.kts:55`, `:76`; the two autotest types inherit by `initWith`, `:69`, `:88`).
- Libraries, all vendored as binaries, none as source except OnGuardLib:
  - `commonvaluablelibrary-1.09.20.aar` (2.1 MB) (`SP/CVL/build.gradle:2`). The common library tree supplied with it is a later version (section 5.1).
  - `usermanagement-1.06.01.aar` (`SP/usermanagement/build.gradle:2`).
  - `WorkpathLib-1.6.3.aar` and `quickaccess-1.00.11.aar` in `SP/app/libs/` (`SP/app/build.gradle.kts:182-183`).
  - `OnGuardLib` as a source module with native C++ (`SP/app/build.gradle.kts:166`; `SP/OnGuardLib/build.gradle.kts:55-56`); the `locker/alg` package is excluded from the build (`SP/OnGuardLib/build.gradle.kts:51`).
- Third-party: `microsoft-graph` 5.34.0, OkHttp 3.10.0, Retrofit 2.5.0, RxJava 2, Picasso 2.8, Gson 2.11.0, Jackson 2.9.5, PdfiumAndroid 1.9.8, pdfbox-android 2.0.27.0, `androidx.security:security-crypto` 1.0.0 (`SP/app/build.gradle.kts:146-214`; `SP/build.gradle.kts:12`).
- Languages: string resources for English (193 strings) and seven translations: `de`, `es`, `fr`, `in`, `it`, `pt` (174 strings each) and `zh-rTW` (173) (count of `<string ` per `SP/app/src/main/res/values*/strings.xml`). EULA files for eight locales in `SP/app/src/main/assets/`.
- Layout qualifiers `sw340dp`, `sw600dp`, `sw800dp` (directory names under `SP/app/src/main/res/`): the three panel classes report A4 line 172 describes.
- Tests: one unit test, `SP/app/src/test/java/com/hp/print/cypher/sharepoint/auth/SessionAccessPolicyTest.java` (27 lines).
- Five files in `SP-J/taskmanager/` are empty (0 lines each): `IProgressTracker.java`, `OnAsyncTaskCompleteListener.java`, `OnAsyncTaskProgressUpdateListener.java`, `AbstractProgressableAsyncTask.java`, `AsyncTaskManager.java`. The classes of those names that the app uses come from the common library.

### 3.2 Build and packaging

- **What the release pipeline builds.** One APK and one HPK. `SP/.github/workflows/release.yml` runs when a pull request from a `release/*` branch carrying the label `release` is merged into `main`, or by hand (`:3-14`, `:27-31`). It checks that the pull request changed `versionName` or `versionCode` (`:104-107`), runs `./gradlew :app:test :app:assembleRelease` on Java 21 (`:122-130`), validates the configuration form as XML (`:148`), zips `SharePoint-release.apk` and `hpk.xml` into `SharePoint_v<version>-release.hpk` with a SHA-256 file (`:150-155`), tags the commit `v<version>` (`:171-190`) and publishes a GitHub Release holding the HPK, the checksum and the configuration form (`:192-207`).
- The three other workflows: `build.yml` runs the unit tests on push and pull request (`SP/.github/workflows/build.yml:22-23`); `codeql.yml` analyses `actions`, `c-cpp` and `java-kotlin` (`SP/.github/workflows/codeql.yml:23-28`); `gitleaks.yml` scans for secrets (`SP/.github/workflows/gitleaks.yml:23`).
- **The HPK descriptor.** `SP/packaging_release/hpk.xml`: schema version 2.4 (`:2`), UUID `66ed8112-0e9c-4823-b457-f751de06aae5` (`:3`), name "SharePoint for Authentication Suite" (`:4`), vendor "HP Inc" (`:5`), platform `LinkForDevice` 31.7 (`:7-8`), install file `SharePoint-release.apk` (`:9`), empty default configuration and no providers (`:10`). The same UUID is compiled into the app (`SP-J/constant/AppConstants.java:137`). It is the UUID review finding R1-04 found in the licence portal's app list (`review/R1_parity.md` line 30).
- **The configuration form** that HP Command Center shows the administrator: `SP/app/moc_flie/SharePoint.moc` (158 KB; the folder name is spelled `moc_flie` in the tree). Three frames: `printConfig`, `scanConfig`, `appConfig`. Three frames start at `:5` (`printConfig`), `:1207` (`scanConfig`) and `:3028` (`appConfig`). Its 28 fidgets (count by search for `<fidget id=`): 7 print defaults (copies, colour mode, output sides, paper size, paper tray, paper type, collate); 19 scan defaults (file type, colour mode, resolution, quality, original size, original sides, content orientation, optimise text/picture, darkness, contrast, sharpness, background cleanup, blank page, cropping, multi-feed detection, compression, TIFF colour compression, TIFF mono compression, PDF encryption); and 2 under `appConfig`: `enableSendToEmail` (`SP/app/moc_flie/SharePoint.moc:3042`) and `splitAttachmentByPage` with `maxPagesPerAttachment` (`:3094-3119`). The app also reads and writes three `appConfig` keys that the form does not offer: `adminOptIn`, `domainHint`, `urlAddressBar` (`SP-J/AppConfigHelper.java:21-26`).
- A hand-build note and a packaging note give the same recipe as the pipeline: `SP/packaging_release/readme:1-3`. The file `SP/notes` (2 lines) holds two more hand-build command lines; it was searched for keywords only and not printed (section 8).
- **The manifest.** `SP/app/src/main/AndroidManifest.xml`: permissions `ACCESS_NETWORK_STATE`, `INTERNET`, `FOREGROUND_SERVICE` (`:5-11`); it declares the permission `com.hp.print.hpauthenticationmanager.permissions.TokenLibraryPermission` (`:12`); `allowBackup` false, cleartext traffic off, `useEmbeddedDex` true (`:21-26`). Thirteen activities (count of `<activity`), all landscape: splash (the launcher entry), log-in, main, app guide, information, open-source licences, settings, scan preview, print preview, print preview zoom, log-out, search and sites search (`:28-154`). No service and no receiver is declared: the upload service and the broadcast receiver of the HP original are commented out (`:156-166`).

## 4. Feature inventory (numbered checklist)

How to read the State column:

- **LIVE**: reachable in the app as built.
- **DEAD (switch)**: the code is present but sits behind `WorkpathAccessService.isSIOEnabled()`, which returns false unconditionally in the common library source (`CVL2-J/sdk/WorkpathAccessService.java:137-140`; the same in `isHPCloudUser()`, `:108-111`). The SharePoint app is linked against the binary `commonvaluablelibrary-1.09.20.aar`, which was not decompiled; the statement rests on the library source of version 1.09.23 and on report A4 line 290, which found the same in 1.09.22.
- **DEAD (constant)**: compiled off by a constant in the SharePoint source itself.
- **UNREFERENCED**: a class that no other class starts.

A row marked DEAD or UNREFERENCED is not a parity requirement unless a Workpath printer running SharePoint 4.4.6 shows the behaviour (the rule of `02_architecture.md` section 3.1).

### 4.1 Start-up, identity and session

| # | Behaviour | State | Source |
|---|---|---|---|
| 1 | The home-screen icon opens a splash screen that starts the Workpath SDK through the common library; "SDK not ready" and "SDK not installed" stop the app with a dialog | LIVE | `SP/app/src/main/AndroidManifest.xml:28-38`; `SP-J/ui/splash/SplashActivity.java:319-355`; `SP-J/ui/main/CommonValuableLibInit.java:43-54` |
| 2 | The app has no sign-in of its own: it takes the user's access token from HP Authentication Manager through the `usermanagement` library (`getToken()`) | LIVE | `SP-J/ui/splash/SplashActivity.java:168-199`, `:376-397` |
| 3 | No device session, or no token: the app starts HP Authentication Manager, passing its own UUID so that it is reopened after sign-in, and closes itself. If HP Authentication Manager is not installed it shows a "no user" screen with an Exit button | LIVE | `SP-J/ui/splash/SplashActivity.java:129-151`, `:214-232`, `:404-434` |
| 4 | A device administrator never reaches cloud files: personal data is cleared and the app opens its settings screen instead | LIVE | `SP-J/auth/SessionAccessPolicy.java:15-23`; `SP-J/ui/splash/SplashActivity.java:475-513`; `SP-J/ui/main/MainActivity.java:230-233` |
| 5 | Token push while the app runs: sign-in and each refreshed access token are stored (Android `EncryptedSharedPreferences`); a sign-out event clears everything and shows the sign-in request | LIVE | `SP-J/ui/splash/SplashActivity.java:234-275`; `SP-J/SecuredPreferences.kt:13-30`; the same callbacks in `SP-J/ui/main/MainActivity.java:399-460` (method list read, bodies not) |
| 6 | The user's identity is read from the token's claims `tid`, `oid`, `unique_name`, `family_name`, `given_name` (decoded, signature not checked); the drawer shows given name and family name | LIVE | `SP-J/ui/splash/SplashActivity.java:526-544`; `SP-J/ui/main/MainActivity.java:871-874` |
| 7 | On HTTP 401 the app asks HP Authentication Manager for a new token (`getNewToken`), waits at most 10 seconds and retries the request once | LIVE | `SP-J/auth/SessionAuthenticator.kt:20-56`; `SP-J/auth/AuthInterceptor.kt:8-15` |
| 8 | National clouds: the Graph base address and the sign-in authority come from HP Authentication Manager's cloud configuration | LIVE | `SP-J/core/GraphProvider.kt:44-62` |
| 9 | Sign out (toolbar button and menu entry) ends the device session (`AccessService.signOut`) and closes the app; Exit closes the app only | LIVE | `SP-J/ui/main/MainActivity.java:877-884`, `:1005-1008`, `:1331-1332`, `:1369-1370` |
| 10 | On sign-out or loss of the token service: token, tenant id, user data, site and folder caches and the app's working folders are wiped | LIVE | `SP-J/ui/splash/SplashActivity.java:277-289` |
| 11 | Name-resolution fallback: when the system DNS fails, addresses cached from an earlier successful lookup are used | LIVE | `SP-J/utils/FallbackDns.kt:21-38`; `SP-J/core/GraphProvider.kt:92` |
| 12 | Network time limits: connect 60 s, read/write 180 s, whole call 180 s | LIVE | `SP-J/NetworkTimeouts.java:4-6`; `SP-J/core/GraphProvider.kt:86-89` |
| 13 | Screens are protected from screen capture in non-debug builds | LIVE | `SP-J/ui/splash/SplashActivity.java:95-97`; `SP-J/common/PresenterAppActivity.java:27`; `SP-J/common/RootBaseAppCompatActivity.java:34` |

### 4.2 Browse and search

| # | Behaviour | State | Source |
|---|---|---|---|
| 14 | The first screen after start is the list of sites | LIVE | `SP-J/ui/main/MainActivity.java:312-313` |
| 15 | Sites list: Graph site search with the query `*` when nothing is typed, 500 per page, all pages followed; HTTP 403 gives a "no permissions" message | LIVE | `SP-J/task/RootSiteTask.java:30-35`, `:53-72`, `:92-96` |
| 16 | Recent sites: the last 3 sites opened are listed above all sites and kept per user | LIVE | `SP-J/ui/main/base/BaseSitesFragment.java:146-147`, `:374-393`; `SP-J/constant/AppConstants.java:126`; `SP-J/storage/UserPreferencesStore.kt:19`, `:127-129` |
| 17 | Navigation drawer with "All sites" and "Recent sites". The drawer is locked against a swipe (`:784-785`) but the toolbar icon opens it in code (`:1014-1016`). Not verified on a device | LIVE (as coded) | `SP-J/ui/main/MainActivity.java:783-831`, `:1014-1016` |
| 18 | Site → its document libraries (first page of the site's drives; no paging loop) | LIVE | `SP-J/task/GetDrivesTask.java:30-44` |
| 19 | Site → its lists (first page); the list behind a library is found by matching the web address, then the display name, else the only list | LIVE | `SP-J/task/GetListsTask.java:28-33`; `SP-J/ui/main/base/BaseSitesFragment.java:400-440` |
| 20 | Folder listing: children by item id or by path, 20 per page, shown page by page, with a large thumbnail per file | LIVE | `SP-J/task/GetListFolderTask.java:94-129`, `:130-159` |
| 21 | Library column values for each listed item: one batch request per page, one list-item read per file (skipped on 4.3-inch panels). The list item is addressed by the GUID inside the drive item's eTag | LIVE | `SP-J/task/GetListFolderTask.java:133-137`, `:176-204`, `:268-288` |
| 22 | Column definitions of the library (first page). Columns shown: not read-only, not in the `_Hidden` group, of type text, yes/no, currency, date/time or number | LIVE | `SP-J/task/GetColumnsTask.java:37-43`; `SP-J/ui/main/ColumnHelper.kt:16-36` |
| 23 | Column chooser: show or hide library columns; the choice is remembered per library for the session | LIVE | `SP-J/ui/main/base/BaseMainFragment.java:303`, `:1782-1806`; `SP-J/storage/FolderNavigationCache.kt:102-119` |
| 24 | Sort by a library column and group by a column, with section headers | LIVE (read in part) | `SP-J/ui/main/base/BaseMainFragment.java:1985-2043`, `:2162`, `:2177` |
| 25 | Sort: newest, oldest, A to Z, Z to A; on 4.3-inch panels the sort entry moves into the overflow menu | LIVE | `SP-J/ui/main/base/BaseMainFragment.java:1180-1198`; `SP-J/sort/SortingType.java:3-8`; `SP-J/ui/main/MainActivity.java:1280-1282` |
| 26 | List view or grid view with thumbnails | LIVE | `SP-J/ui/main/base/BaseMainFragment.java:1517-1531`; `SP-J/model/FileItem.java:203-208` |
| 27 | Folder cache: up to 40 folder listings and 40 column sets held in memory; a cached folder is shown at once and then reloaded | LIVE | `SP-J/storage/FolderNavigationCache.kt:12-24`; `SP-J/ui/main/base/BaseMainFragment.java:513-522` |
| 28 | Refresh button | LIVE | `SP-J/ui/main/MainActivity.java:1333-1334` |
| 29 | Write permission is read per folder or item (`permissions` of the drive item, looking for a `write` role). Create folder, rename and delete are offered only with it. Whether the scan button is also withheld was not established (the method that decides it was not read) | LIVE | `SP-J/ui/main/base/BaseMainPresenter.java:1003-1062`; `SP-J/ui/main/base/BaseMainFragment.java:875-889`, `:924-926`, `:1260-1269` |
| 30 | File details dialog | LIVE | `SP-J/ui/main/base/BaseMainFragment.java:658-659`, `:726` |
| 31 | Search files inside the current library (drive search, 400 per page; HTTP 400 is shown as an empty result); the last 3 search terms are kept per user | LIVE | `SP-J/task/SearchCallableTask.java:70-79`, `:100-105`; `SP-J/ui/search/SearchActivity.java:133`, `:186-192` |
| 32 | Search sites by name; the last 3 site search terms are kept per user | LIVE | `SP-J/ui/search/presenter/SitesSearchPresenter.java:70`; `SP-J/ui/search/SitesSearchActivity.java:133`, `:183-191` |
| 33 | A search result opens in its folder | LIVE | `SP-J/ui/search/SearchActivity.java:395`; `SP-J/ui/main/MainActivity.java:302-310` |

### 4.3 File management

| # | Behaviour | State | Source |
|---|---|---|---|
| 34 | Create folder; a duplicate name (409) and an invalid name (400) each have their own message | LIVE | `SP-J/task/CreateFolderTask.java:107-120`; `SP-J/ui/main/MainActivity.java:1337-1339` |
| 35 | Rename a file or folder; a file keeps its extension | LIVE | `SP-J/task/RenameFileTask.java:33-47`, `:57-72` |
| 36 | Delete one item, or several after a long press starts multi-select; items are deleted one request each, with progress | LIVE | `SP-J/task/DeleteFilesTask.java:40-66`; `SP-J/ui/main/base/BaseMainFragment.java:563-580`, `:793` |
| 37 | Edit the library column values of an existing item | LIVE | `SP-J/task/UpdateColumnValueTask.java:37-51`; `SP-J/ui/main/base/BaseMainFragment.java:664-665`, `:765` |

### 4.4 Print

| # | Behaviour | State | Source |
|---|---|---|---|
| 38 | Tap a file: it is downloaded and opened in the print preview | LIVE | `SP-J/ui/main/base/BaseMainFragment.java:528-542`, `:1482-1488`; `SP-J/ui/main/MainActivity.java:1840-1866` |
| 39 | Swipe a file row (list view): direct print with the default settings, no preview | LIVE | `SP-J/ui/main/base/BaseMainFragment.java:1550-1584`, `:1722-1727`, `:1483-1485` |
| 40 | Printable types: `pdf, jpg, jpeg, tiff, tif, txt` directly, and `doc, docx, xls, xlsx, ppt, pptx` after conversion; anything else gives "not supported" | LIVE | `SP-J/utils/Utils.java:357-366`; `CVL2-J/utils/CommonSDKUtil.java:190-194`; `SP-J/ui/main/base/BaseMainFragment.java:1723-1726` |
| 41 | Office files are converted by Graph (`content?format=pdf`). Size limits: 80 MB, Excel 40 MB, and 1 GB or more always refused | LIVE | `SP-J/task/DownloadConvertToPdfFileTask.kt:41-43`, `:53-62`; `SP-J/utils/Utils.java:394-406` |
| 42 | A conversion time-out at Microsoft (HTTP 500 naming a time-out) has its own message | LIVE | `SP-J/task/DownloadConvertToPdfFileTask.kt:96-109`; `CVL2-J/utils/ErrorUtils.kt:7-11`; `SP-J/error/ErrorHandlingUtils.java:59-60` |
| 43 | A protected (encrypted) Office document that Graph cannot convert has its own message | LIVE | `SP-J/task/DownloadConvertToPdfFileTask.kt:93-94`, `:103-104`; `SP-J/error/ErrorHandlingUtils.java:58` |
| 44 | Other files are downloaded from the item's download address (connect 5 s, read 6 s) after a free-space check on the device | LIVE | `SP-J/task/DownloadFileTask.java:42-43`, `:77-91` |
| 45 | Multi-select print: all selected files are downloaded (converted where needed), then previewed together; per-file failures are listed | LIVE | `SP-J/ui/main/MainActivity.java:1311-1314`, `:1708-1726`; `SP-J/task/DownloadMultipleFilesTask.java:107-160` |
| 46 | Print preview with the print options and a zoom screen (both from the common library) | LIVE | `SP-J/ui/main/MainActivity.java:1861-1866`; `SP/app/src/main/AndroidManifest.xml:111-129` |

### 4.5 Scan

| # | Behaviour | State | Source |
|---|---|---|---|
| 47 | A scan button inside a folder opens the scan screen with that folder as the destination; hidden when the device has no scanner | LIVE | `SP-J/ui/main/MainActivity.java:1042-1047`, `:1908-1912` |
| 48 | Scan options, preview and job progress come from the common library; the defaults come from the configuration form (section 3.2) | LIVE | `SP-J/ui/preview/ScanPreviewAppFragment.java:228-252`; `SP/app/moc_flie/SharePoint.moc:1207` |
| 49 | File name: typed by the user, or `Scan_<date>_<time>` with the date in the device locale's order (`yyyyMMdd`, `MMddyyyy` or `ddMMyyyy`) | LIVE | `SP-J/utils/Utils.java:131-150`; `SP-J/ui/preview/ScanDescriptionAppFragment.java:137-145`; `SP-J/task/UploadFileTask.java:233-239` |
| 50 | Several files from one scan: `_001`, `_002` suffixes from the second file on (four digits from 1,000 files); the name is cut to 255 characters | LIVE | `SP-J/task/UploadFileTask.java:536-559` |
| 51 | Upload: under 3.5 MB in one request; otherwise an upload session in 10 MiB pieces (aligned to 320 KiB), retried on 408, 429 and 5xx with a growing wait of at most 15 s | LIVE | `SP-J/task/UploadFileTask.java:61-65`, `:274-289`, `:317-328`, `:586-598` |
| 52 | An existing file is never overwritten: the upload asks Graph to fail on a name conflict, and the user gets a duplicate-name error | LIVE | `SP-J/task/UploadFileTask.java:272`, `:297-298`, `:357-358`, `:367` |
| 53 | Library metadata at scan: one input per editable column (text, number, currency, yes/no, date or date and time), written to the uploaded file's list item after the upload. Not offered on 4.3-inch panels | LIVE | `SP-J/ui/preview/BaseScanDescriptionAppFragment.java:41-56`, `:57-97`, `:100-105`, `:108-118`; `SP-J/ui/preview/presenter/ScanPreviewPresenter.java:114-119`, `:279` |
| 54 | Send to e-mail (only when the administrator enabled it): a checkbox and a recipient list on the scan screen, prefilled with the user's address, else the device's default From address. The message shown at the limit says at most 5 recipients (the code that enforces it, `ScanDescriptionAppFragment.java:381`, was not read) | LIVE | `SP-J/ui/preview/ScanDescriptionAppFragment.java:276-297`; `SP-J/ui/preview/ScanPreviewAppFragment.java:138-143`; `SP/app/src/main/res/values/strings.xml:133` |
| 55 | The e-mail goes out through the device's SMTP settings (`Email.send`) with the scanned files attached; From is the device default address, else the signed-in user's address; "SMTP not configured" has its own message | LIVE | `SP-J/model/EmailSender.java:28-49`, `:64-73`; `SP-J/model/SendEmailTask.java:35-57`; `SP-J/ui/preview/presenter/ScanPreviewPresenter.java:95-112` |
| 56 | If the upload fails while Send to e-mail is on, a failure e-mail is sent (to the chosen recipients, else to the user) | LIVE | `SP-J/ui/preview/presenter/ScanPreviewPresenter.java:126-166` |
| 57 | Upload result: a list of the files that failed, with detail; cancel during upload | LIVE | `SP-J/ui/preview/ScanPreviewAppFragment.java:146-149`, `:380-430`, `:565-583` |

### 4.6 Settings, information, languages, errors

| # | Behaviour | State | Source |
|---|---|---|---|
| 58 | Settings are offered to a device administrator only: default print options, default scan options, and the Send to e-mail switch | LIVE | `SP-J/ui/settings/SettingsAppFragment.java:81-93`; `SP-J/ui/main/MainActivity.java:1244-1248` |
| 59 | Remote configuration: the app reads its `appConfig` frame and writes its settings back (`adminOptIn`, `enableSendToEmail`, `domainHint`, `urlAddressBar`) | LIVE | `SP-J/AppConfigHelper.java:21-26`, `:72-79`, `:81-131`; `SP-J/ui/main/MainActivity.java:941-949` |
| 60 | Information page and open-source licences page | LIVE | `SP-J/ui/main/MainActivity.java:1366-1367`, `:1961-1964`; `SP/app/src/main/AndroidManifest.xml:75-89` |
| 61 | App guide (tutorial) from the menu | LIVE | `SP-J/ui/main/MainActivity.java:1363-1364`, `:1921-1924` |
| 62 | Eight languages: English plus German, Spanish, French, Indonesian, Italian, Portuguese, Traditional Chinese | LIVE | directories `SP/app/src/main/res/values`, `values-de`, `-es`, `-fr`, `-in`, `-it`, `-pt`, `-zh-rTW` |
| 63 | Error messages by HTTP status: 401 "invalid credentials" and the app closes; 403 no permission; 404 not found; 409 same name; 429 and 503 too many requests; plus "insufficient storage" and "file too large" | LIVE | `SP-J/error/ErrorHandlingUtils.java:65-94` |
| 64 | Three panel classes (layout sets for 340, 600 and 800 dp widths); several features are reduced on 4.3-inch panels (rows 21, 25, 53) | LIVE | directories `SP/app/src/main/res/layout-sw340dp`, `layout-sw600dp`, `values-sw800dp`; `SP-J/ui/main/MainActivity.java:245` |

### 4.7 Present in the source but not reachable

| # | Behaviour | State | Source |
|---|---|---|---|
| 65 | Quick access: pinned print items and pinned scan folders (10 each), quick print, quick scan, "open on quick access first", folder print of up to 10 files, its settings entry | DEAD (switch) | `SP-J/ui/main/MainActivity.java:338-351`, `:964-966`; `SP-J/ui/main/base/BaseMainFragment.java:600-624`, `:639-649`; `SP-J/ui/settings/SettingsAppFragment.java:95-98`; `SP-J/constant/AppConstants.java:58-60` |
| 66 | "Remember me" dialog and the sign-in management settings entry | DEAD (switch) | `SP-J/ui/main/MainActivity.java:1927-1930`; `SP-J/ui/settings/SettingsAppFragment.java:95-97` |
| 67 | App guide shown automatically at first use | DEAD (switch) | `SP-J/ui/main/MainActivity.java:655-657` |
| 68 | Sensitivity labels: read a file's label, block printing of a "Do Not Print" label, choose a label before a scan upload and assign it after | DEAD (constant) | `SP-J/sensitivity/SharePointSensitivityLabelProvider.java:38`, `:56-58`, `:93-96`; `SP-J/ui/main/CommonValuableLibInit.java:68-73`; `SP-J/ui/preview/ScanPreviewAppFragment.java:166-172`, `:229-235` |
| 69 | The app's own Microsoft sign-in screen (authorisation-code flow with its own client id, redirect address and scope list) | UNREFERENCED | `SP-J/ui/login/LogInActivity.java:16`; `SP-J/ui/login/LogInFragment.java:175`, `:390`; `SP-J/constant/SharepointConstants.java:7-13`; `SP-J/auth/AppAuthManager.java:148-174`. A search for `LogInActivity` finds 4 lines, all inside those two files |
| 70 | Sign-out confirmation screen (`LogoutActivity`) | UNREFERENCED | `SP-J/ui/main/MainActivity.java:1967-1970` (its only caller, `startSignOut`, is itself called nowhere: 1 line found) |
| 71 | HP's cross-app upload service and broadcast interface ("horizontal" actions) | DEAD (not in the manifest) | `SP/app/src/main/AndroidManifest.xml:156-166`; `SP-J/constant/AppConstants.java:101-107` |
| 72 | Domain hint setting and URL address bar setting | DEAD (commented out) | `SP-J/ui/settings/SettingsAppFragment.java:100-106` |
| 73 | EULA entry in settings | DEAD (commented out) | `SP-J/ui/settings/SettingsAppFragment.java:92` |

Counts: 73 rows; 64 LIVE (rows 1 to 64), 9 not reachable (rows 65 to 73).

## 5. Graph and identity

### 5.1 Identity and token handling

- **The app holds no credential of its own in the live path.** The token is HP Authentication Manager's, obtained over the `usermanagement` binder (rows 2, 5, 7). It is kept in `EncryptedSharedPreferences` under the key `access_token` beside `tenant_id` (`SP-J/SecuredPreferences.kt:16-36`) and attached as a Bearer header to every Graph request (`SP-J/auth/AuthInterceptor.kt:8-15`). One request path builds the header by hand from the same stored token (`SP-J/task/GetListFolderTask.java:52`, `:187`).
- **No refresh token is handled by the app.** The refresh code is commented out (`SP-J/auth/AppAuthManager.java:33-146`); refresh is HP Authentication Manager's job (report A4 line 114).
- **The app's own OAuth client is dead code** (row 69). It names a redirect address, the `/organizations/` authorise, token and log-out paths and the scope string `offline_access user.read sites.readwrite.all` (`SP-J/constant/SharepointConstants.java:7-13`), and takes its client id from a build field (`SP-J/constant/AppConstants.java:140-142`; `SP/app/build.gradle.kts:61-65`, `:80-84`). Nothing starts that screen. So the scopes of the live token are whatever HP Authentication Manager requested, not this string.
- **OnGuardLib** is linked, and one accessor reads a "vault client id" from its native locker (`SP-J/constant/AppConstants.java:144-146`); a search for `getVaultClientId` finds that definition and no caller. The locker's native sources were not opened (section 8).
- **Device session.** The app reads the Workpath principal directly once (`AccessService.getCurrentPrincipal`, `SP-J/ui/splash/SplashActivity.java:214-232`), asks the common library whether the principal is an administrator (`:475-477`) and ends the session on sign-out (`SP-J/ui/main/MainActivity.java:879`).
- **Per-user data that roams** goes through HP Authentication Manager's user-property channel (`getUserProperty` / `updateUserProperty`, `SP-J/storage/UserPreferencesStore.kt:167-186`), which report A4 line 111 identifies as the store in the user's own OneDrive. Six keys, all prefixed `sharepoint.`: `quick_access`, `recent_searches`, `recent_site_searches`, `recent_sites`, `remember_me_save`, `remember_me_do_not_show_again` (`SP-J/storage/UserPreferencesStore.kt:14-21`). Of these, three are written by live features: `recent_searches`, `recent_site_searches`, `recent_sites` (rows 16, 31, 32). EULA acceptance keys exist in the store but have no caller outside it (a search for `isUserAlreadyCheckedEula` finds one file, `:147-152`).

### 5.2 Every Graph call in the source

All calls go to `<graphApi>/v1.0` (`SP-J/core/GraphProvider.kt:61`) except the label calls marked beta. `{s}` site id, `{d}` drive id, `{l}` list id, `{i}` item id.

| # | Call | Used for | State | Source |
|---|---|---|---|---|
| G1 | `GET /sites?search=<q>&$top=500` (+ next pages) | all sites, site search | LIVE | `SP-J/task/RootSiteTask.java:53-72` |
| G2 | `GET /sites/{s}/drives` | libraries of a site | LIVE | `SP-J/task/GetDrivesTask.java:30-34` |
| G3 | `GET /sites/{s}/lists` | list id behind a library | LIVE | `SP-J/task/GetListsTask.java:28-33` |
| G4 | `GET /sites/{s}/lists/{l}/columns` | column definitions | LIVE | `SP-J/task/GetColumnsTask.java:37-43` |
| G5 | `GET /sites/{s}/drives/{d}/root/children`, `.../root:/<path>:/children`, `.../items/{i}/children` with `$top=20`, `$select=id,createdDateTime,lastModifiedDateTime,name,parentReference,size,folder,file,eTag`, `$expand=thumbnails($select=large)` | folder listing | LIVE | `SP-J/task/GetListFolderTask.java:95-129`; `SP-J/constant/SharepointConstants.java:5` |
| G6 | `POST /$batch` of `GET /sites/{s}/lists/{l}/items/{id}` | column values per listed item | LIVE | `SP-J/task/GetListFolderTask.java:184-190`, `:268-288` |
| G7 | `GET /sites/{s}/lists/{l}/items/{id}?$expand=fields($select=<columns>)`, up to 5 tries | column values of one item | LIVE | `SP-J/task/GetListFolderColumnTask.java:93-110` |
| G8 | `PATCH /sites/{s}/lists/{l}/items/{id}/fields` | write column values (after scan, or edit) | LIVE | `SP-J/task/UpdateColumnValueTask.java:45-51` |
| G9 | `GET /sites/{s}/drives/{d}/items/{i}/permissions` or `.../root/permissions` | write-permission check | LIVE | `SP-J/ui/main/base/BaseMainPresenter.java:1024-1038` |
| G10 | `GET /drives/{d}/root/search(q='<q>')` with `$select` as G5, `$top=400` | search in a library | LIVE | `SP-J/task/SearchCallableTask.java:72-79` |
| G11 | `POST .../children` with a folder facet | create folder | LIVE | `SP-J/task/CreateFolderTask.java:72-111` |
| G12 | `PATCH /sites/{s}/drives/{d}/items/{i}` (name) | rename | LIVE | `SP-J/task/RenameFileTask.java:58-63` |
| G13 | `DELETE /sites/{s}/drives/{d}/items/{i}` | delete | LIVE | `SP-J/task/DeleteFilesTask.java:51-57` |
| G14 | `GET /sites/{s}/drives/{d}/items/{i}` then the `@microsoft.graph.downloadUrl` address | download for print | LIVE | `SP-J/task/DownloadFileTask.java:77-93`; `SP-J/task/DownloadMultipleFilesTask.java:441-453` |
| G15 | `GET /drives/{d}/items/{i}/content?format=pdf` | Office to PDF | LIVE | `SP-J/task/DownloadConvertToPdfFileTask.kt:53-62`; `SP-J/task/DownloadMultipleFilesTask.java:313-322` |
| G16 | `PUT .../<name>:/content?@microsoft.graph.conflictBehavior=fail` | upload under 3.5 MB | LIVE | `SP-J/task/UploadFileTask.java:253-289` |
| G17 | `POST /sites/{s}/drives/{d}/items/{i}:/<name>:/createUploadSession` (conflict behaviour `fail`) then `PUT` of byte ranges to the session address | upload of 3.5 MB or more | LIVE | `SP-J/task/UploadFileTask.java:317-328`, `:365-379`, `:446-448` |
| G18 | `GET /me` | user's e-mail when the token did not give one | LIVE | `SP-J/task/AccountInfoTask.java:22-37` |
| G19 | `POST /$batch` of `GET sites/{s}/drives/{d}/items/{i}?$select=...&$expand=thumbnails` | refresh pinned quick-access items | DEAD (switch, row 65) | `SP-J/ui/main/presenter/QuickAccessPresenter.kt:84-109` |
| G20 | `POST <graphApi>/v1.0/drives/{d}/items/{i}/extractSensitivityLabels` and `/assignSensitivityLabel`; label lists from `/v1.0/security/dataSecurityAndGovernance/sensitivityLabels` and a `/beta` `me/informationProtection/policy/labels` fallback | sensitivity labels | DEAD (constant, row 68) | `SP-J/sensitivity/SharePointSensitivityLabelProvider.java:180-230`, `:282-284`, `:372-383`, `:425-429` |

Token endpoint call of the dead sign-in screen: `POST <authority>/organizations/oauth2/v2.0/token` (`SP-J/auth/AppAuthManager.java:156-173`).

Not Graph: Send to e-mail uses the Workpath SDK's device mail helper (`Email.getDefaults`, `Email.send`, `SP-J/model/SendEmailTask.java:26`, `:57`). No Graph `sendMail` call exists in the tree: a search for `sendMail` over `SP/app/src/main/java` finds 0 lines (control in the same tree: `Email.send` 1 line).

### 5.3 Permissions the live calls need

Stated from general knowledge of Microsoft Graph, not checked against Microsoft's documentation in this pass (no network was used): G1 to G17 are within delegated `Sites.ReadWrite.All` (G8, the list-item field write, is the call that makes the "write" level necessary for a user who only scans with metadata); G18 needs `User.Read`. Nothing live needs a mail scope. This matches the scope string of the dead sign-in screen (section 5.1) and the documented pair `Sites.ReadWrite.All` and `User.Read` that `02_architecture.md` section 7.2 already cites from report A6. The live calls do not show a need for `Files.ReadWrite.All` in the SharePoint app; whether HP Authentication Manager's token carries it is in report A1, not here.

## 6. The common library (`CommonValueLibraryCypher-master-2`)

### 6.1 What was supplied

- 798 files; library version **1.09.23** (`CVL2/commonvaluablelibrary/build.gradle.kts:12`). Three modules: `:app` (demo), `:commonvaluablelibrary`, `:workpath` (`CVL2/settings.gradle.kts`, last line). Two vendored SDK binaries, `WorkpathLib162.aar` and `WorkpathLib163.aar` (directory `CVL2/workpath/`). Three workflows: `codeql.yml`, `gitleaks.yml`, `release-merged-pr.yml`. Six unit-test files (`CVL2/commonvaluablelibrary/src/test`).
- **It is the library copy that report A4 analysed, one version later.** The read-only library copy (`CommonValueLibraryCypher-master`, version 1.09.22) also has 798 files, and `diff -rq` between the two trees reports **2 differing files and no file present on one side only**: the version line (`commonvaluablelibrary/build.gradle.kts:12`, 1.09.22 → 1.09.23) and `CVL2-J/sharepoint/columns/LibraryColumn.kt`, which gains one function, `displayValueExact` (date and date-time column values shown in the device's date format and 12/24-hour setting, `:80-106`). **Report A4 sections 3.1, 4.2 and 4.3 therefore stand for this tree**; this report does not repeat them.

### 6.2 What it provides, against the five headings asked

| Heading | Provided? | Detail | Source |
|---|---|---|---|
| Authentication | **No.** Identity read only | `WorkpathAccessService` reads the device principal (id, e-mail, name, administrator flag). No token, no Graph client: a search of `CVL2/commonvaluablelibrary/src/main/java` for `graph.microsoft`, `access_token` and `Bearer ` finds 0 lines (control in the same tree: `ScannerService` 11 lines). Its two "HP cloud sign-in" switches return false always | `CVL2-J/sdk/WorkpathAccessService.java:108-111`, `:137-140`; report A4 line 136 |
| UI | Yes | Scan option screens and scan preview, print option screens and print preview with zoom, PDF rendering, dialogs, toolbar, settings screens, EULA, a web page view; SharePoint library-column model, sort popup and field editor (`sharepoint/columns`, 12 files); Microsoft Entra options screen with an attachment size limit (`msentra`, 5 files); sensitivity-label option screens in the print options | package listing of `CVL2-J/` (file counts per directory); `CVL2-J/print/view/preview/PrintSubOptionsFragment.java:184`, `:470` |
| Device services | Yes | SDK start-up, scan and print job submit, progress and cancel, capabilities, remote configuration read and write | report A4 lines 135-141 (unchanged files) |
| Licensing | **No** | No class file whose name contains "licen" (0 found by file-name search). 141 source lines contain the word; they were not classified (the library has EULA and open-source licence screens, `CVL2-J/ui/eula`, 5 files) | file-name search; report A4 line 145 |
| Logging | No framework | `android.util.Log` under a `[CVL]` prefix | report A4 line 145; example `CVL2-J/sensitivity/SensitivityLabelManager.java:137` |

Sensitivity labels in the library: an interface the app implements (`CVL2-J/sensitivity/SensitivityLabelProvider.java`, 29 lines), a manager that turns the feature on only when an app registers a provider (`CVL2-J/sdk/CommonValuableLib.java:102`; `CVL2-J/sensitivity/SensitivityLabelManager.java:35-50`), a print-option screen to change a label, and a block on printing a label named "Do Not Print" (`CVL2-J/sensitivity/SensitivityLabelManager.java:129-136`; `CVL2-J/print/view/preview/PrintPreviewFragment.java:658`).

### 6.3 Which of the five apps use it

| App | Library version pinned | How it is used | Source |
|---|---|---|---|
| SharePoint 4.4.6 | 1.09.20 (binary) | 192 import lines: dialogs 40, utilities 30, SDK 13, list widgets 13, settings base 11, print preview 11, fragments 10, sensitivity 9, toolbar 8, the rest scan and configuration. It does **not** use the library's `sharepoint/columns` package (0 imports; that package is absent from the 1.09.20 binary: 0 classes of that path in its `classes.jar`, against 6 for `sensitivity` and 8 for `msentra`) | import count over `SP/app/src/main/java`; `SP/CVL/build.gradle:2` |
| OneDrive 4.4.1 | 1.09.21 | Uses `sharepoint/columns` (24 import lines) for its own SharePoint-library feature; 0 files name a sensitivity label | `OD/CVL/build.gradle:2`; import search over `OD/app/src` |
| Teams, Mailflow, Universal Print, HP Authentication Manager | 1.09.22, 1.09.20, 1.09.20, 1.09.00 | As report A4 lines 204-208 describe; not re-read here. 0 files in Teams, Mailflow and Universal Print name a sensitivity label (control in each tree: `CommonSDKUtil` in 19, 5 and 9 files) | report A4 lines 204-212 |

So the sensitivity-label interface of the library (requirement row F89) has exactly one implementing app in all the source read, the SharePoint app, and there it is compiled off (row 68). No shipped app in the source uses it live. Version 1.09.23 is pinned by no app in the trees read.

## 7. SharePoint app against the OneDrive app

Read for OneDrive in this pass: its root listing, `app/build.gradle.kts` by search, `CVL/build.gradle`, the list of its class file names, and four searches. Its source was **not** read; the OneDrive half of report A3 is still unwritten.

| Point | SharePoint | OneDrive | Source |
|---|---|---|---|
| Repository | its own tree, 553 files | its own tree, 532 files | file counts |
| Version | 4.4.6 | 4.4.1 | `SP/app/build.gradle.kts:45`; `OD/app/build.gradle.kts:33` |
| Flavours | none | `onedriveforpersonal`, `onedriveforbusiness` | `SP/app/build.gradle.kts:127`; `OD/app/build.gradle.kts:121-129` |
| Common library | 1.09.20 | 1.09.21 | `SP/CVL/build.gradle:2`; `OD/CVL/build.gradle:2` |
| Workpath SDK, quick-access library, Graph SDK | 1.6.3, 1.00.11, 5.34.0 | the same | `SP/app/build.gradle.kts:161`, `:182-183`; `OD/app/build.gradle.kts:195-198` |
| Source layout | `app/src/main/java/com/hp/print/cypher/sharepoint` | `app/src/com/hp/print/cypher` | directory listings |
| Class files by name | 219 distinct names | 173 distinct names | 143 names are common to both |
| Only in SharePoint (76 names) | sites and libraries base classes, the library-column code (`GetColumnsTask`, `GetListsTask`, `GetListFolderColumnTask`, `UpdateColumnValueTask`, `ColumnHelper`, column sort and group classes, `EditColumnDialogFragment`), the sensitivity-label provider, the dead sign-in screen | n/a | name comparison |
| Only in OneDrive (30 names) | n/a | `GetAllSitesTask`, `GetLibraryMetadataTask`, `UpdateLibraryFieldsTask`, `LibraryColumnMapper`, `SharedLibrariesStep` (OneDrive's own route into SharePoint libraries, built on the library's `sharepoint/columns`), `GetRecentTask`, `GetSharedListFolderTask`, `FileSizeComparator`, `QuotaLimitReachedException`, `UploadFileTaskReplace` | name comparison; these files were not opened |
| Upload threshold, conversion limits, recent limit, pin limit | 3.5 MB; 80 MB and 40 MB; 3; 10 | the same values | `SP-J/task/UploadFileTask.java:61`; `OD/app/src/com/hp/print/cypher/task/UploadFileTask.java:74`; `OD/app/src/com/hp/print/cypher/utils/Utils.java:369-371`; `OD/app/src/com/hp/print/cypher/constants/AppConstants.java:42`, `:70` |
| Dead HP switch | 16 lines call `isSIOEnabled` | 14 lines | searches |

What this means: **the two apps are sister code bases from one HP ancestor, not one code base.** They share names, constants and structure, and each has grown its own SharePoint-library code: the SharePoint app with classes of its own, the OneDrive app through the common library. `02_architecture.md` section 5.6.3 cites the OneDrive classes (`GetLibraryMetadataTask`, `UpdateLibraryFieldsTask`) as the SharePoint pattern; the shipped SharePoint app does the same job with `GetColumnsTask` and `UpdateColumnValueTask` (calls G4, G8).

## 8. Secrets and sensitive items (locations only)

No value is reproduced here. During the read, one tool output showed a client identifier (an application id, not a credential) at `SP/app/build.gradle.kts:64` and `:83`; it is not repeated. The two password lines of that file were masked before display and were never shown.

| Location | What |
|---|---|
| `SP/datasec_printer_keystore` | The release signing keystore, committed at the tree root (2,523 bytes). **Not opened.** Report A4 line 323 lists five identical copies in the other app repositories; whether this is a sixth copy of the same file was not checked (that would need reading the file) |
| `SP/app/build.gradle.kts:24`, `:26` | Keystore password and key password in clear text. Not displayed |
| `SP/app/build.gradle.kts:23`, `:25` | Keystore path and key alias |
| `SP/app/build.gradle.kts:12-17`, `:56-60` | A `config.properties` file at the tree root is expected to hold a key named `API_K_SP` for debug builds. The file is not in the tree (it is git-ignored, `SP/.gitignore:38`); release builds set the field to null (`:79`) |
| `SP/app/build.gradle.kts:61-65`, `:80-84` | The app's Entra client id as a build field (used by dead code only, row 69) |
| `SP-J/constant/SharepointConstants.java:7` | A redirect address that embeds an application id |
| `SP/OnGuardLib/src/main/cpp/hdr/locker/secret/secrets.h` (33 lines) and `SP/OnGuardLib/src/main/cpp/src/locker/glue/locker.cpp` (275 lines) | The native "locker" that report A4 line 333 says embeds client id and secret material. **Not opened** |
| `SP/notes` (2 lines) | Hand-build command lines. Searched for the words `storepass`, `keypass`, `password`, `jarsigner`, `apksigner`, `keystore`: 0 found. Not printed |
| `SP/.github/workflows/release.yml:34`, `SP/.github/workflows/gitleaks.yml:25-26` | References to GitHub secrets by name (no value in the file) |
| `CVL2/` | No key-like file found (file-name search for keystores, `.jks`, `.pem`, `.key`, `.p12`, `.pfx`, `config.properties`, certificates: 0; the same search finds the keystore in `SP/`). Four lines match a password pattern; all four initialise the PDF-encryption option's fields to an empty string (`CVL2-J/scan/option/ScanPDFEncryptionOption.java:15`, `:53`; `CVL2-J/scan/view/option/FileType/PDFOptionFragment.java:51-52`) |

Weaknesses seen in the SharePoint source that the port should not carry over (none is new in kind; reports A1 and A4 list the family):

1. All four build types, including the debug ones, sign with the release key (`SP/app/build.gradle.kts:55`, `:69`, `:76`, `:88`); a debug-signed build is trusted by the token service like a release (report A4 line 343).
2. The Graph client logs at debug level in every build (`SP-J/core/GraphProvider.kt:52-54`), and the cloud configuration is logged (`:50`).
3. Token claims are trusted without a signature check and a missing claim crashes the start-up (`SP-J/ui/splash/SplashActivity.java:526-543`).
4. HTTP status is recovered by searching the error text for "401 :" and similar (`SP-J/error/ErrorHandlingUtils.java:157-172`).
5. The download of a file for printing uses a 5 s connect and 6 s read time limit with no retry (`SP-J/task/DownloadFileTask.java:90-91`).

## 9. Open questions

1. **Is quick access shown in the SharePoint app on a Workpath 4.4.6 printer?** The source says no (row 65: behind a switch that the library source returns false for). The library binary the app links (1.09.20) was not decompiled. A look at a printer settles it. *Why it matters:* the Teams quick-access rows F82 and F83 have no SharePoint twin, and none should be added unless a printer shows it.
2. **Are sensitivity labels a feature in progress that release 1 of the OXPd product must carry?** The code is complete enough to read as unfinished work (label lookup, a label chooser before scan upload, a "Do Not Print" block) and is switched off by one constant (row 68). Only the product owner can say whether it ships. Not ruled.
3. **The module `:mtl`** is named in `SP/settings.gradle.kts:45` and has no directory in the tree. Is the supplied archive complete, or does the build fetch it from elsewhere?
4. **Does the manual's "4 custom fields" at scan (requirement F39, from report A6) describe an older version?** The 4.4.6 source shows one input per editable column with no cap (row 53; a search of the two scan-description classes for a limit finds 0 lines, control `forEach` 2).
5. **The gateway source is still not supplied.** C-33 records that the product owner did not know what "gateway" meant; the question is asked again on a card and is not answered. Nothing in either tree supplied today is the gateway.

## 10. What was NOT read

- **SharePoint tree.** Of 220 source files under `SP/app/src/main/java`, about 30 were read whole or nearly whole (the build files, the manifest, the four workflows, `hpk.xml`, six of the eight files of `auth/` (the other two are 4 lines each), `core/GraphProvider.kt`, the constants, `AppConfigHelper`, `SplashActivity`, 14 of the 17 task classes). The three largest classes (`MainActivity` 2,243 lines, `BaseMainFragment` 2,290, `BaseMainPresenter` 1,102) were read by method list and by ranges (about 40% of their lines). Read by search or method list only: `UploadFileTask`, `DownloadMultipleFilesTask`, the scan preview and scan description classes, the sites classes, the search classes, the settings classes, `SharePointSensitivityLabelProvider`, `EmailSender`, `UserPreferencesStore`, `FolderNavigationCache`, `ErrorHandlingUtils`, `FallbackDns`, `Utils`. **Not opened at all:** `QuickAccessAppFragment.kt` and its presenter beyond one search, `AppGuideActivity` beyond 20 lines, every dialog class, every adapter and view holder, the sort comparators, `DirectoryHelper`, `GetListFolderWithCreateFolderIfNotExistTask`, `LogInFragment` beyond two lines, the model classes, the 157 XML resources except the string counts and ten string lines, the eight EULA files, the two `.puml` diagrams, the configuration form beyond its frame and fidget ids, `SP/notes` (keyword search only), the unit test.
- **Never opened, by rule:** `SP/datasec_printer_keystore`; the OnGuardLib native sources (`secrets.h`, `locker.cpp`, `auth.cpp`) and its Java crypto classes.
- **Binaries:** the four `.aar` files were not decompiled. `commonvaluablelibrary-1.09.20.aar` had its `classes.jar` listed for class paths only. So every statement about what the library does inside the SharePoint app rests on library source one to three versions newer than the binary the app ships.
- **Common library tree.** Read: the version line, the module list, directory and file counts, `WorkpathAccessService` at two methods, `CommonSDKUtil` lines 190-204, `ErrorUtils.kt`, `SensitivityLabelManager` by search, the diff against the library copy. Everything else rests on report A4, justified by the 2-file diff (section 6.1).
- **OneDrive tree.** File names and four searches only (section 7). No behaviour of the OneDrive app is established by this report.
- **Nothing was built or run.** No Gradle task, no script, no test. No statement here was checked on a printer. Panel behaviour (for example whether the drawer opens, row 17) is a reading of the code.
- **Git history** of neither tree was available (the archives hold no `.git` directory) and none was examined.

