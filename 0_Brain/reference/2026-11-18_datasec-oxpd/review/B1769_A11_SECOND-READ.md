# B1769: second read of report A11 (the OneDrive business app source, WP0.6)

Second reader under commission B1769, Datasec / OXPd 2, 2026-11-20. Read-only on every source tree and on the NAS library; nothing executed from a source tree; no network call; no message to anyone. This file is the only file written. A11 itself is not edited.

Path shorthand (as A11): `L/` = `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/HPAM - Docs and Notes/Source Code/`; `OD/` = `L/CypherOneDrive-main/`; `ODJ/` = `OD/app/src/com/hp/print/cypher/`; `CVL/` = `L/CommonValueLibraryCypher-master/commonvaluablelibrary/src/main/java/com/hp/print/commonvaluablelibrary/`; `SP/` = `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1120/extracted/sp1/CypherSharePoint-main/`; `MF/` = `L/MailFlow-main/`; `TM/` = `L/Teams-main/`. Documents `02`, `03`, `05`, `CLAR` = the copies in `0_Brain/reference/2026-11-18_datasec-oxpd/`.

Section 0 was written last, after every check.

## 0. BLUF

1. **A11 stands.** Its main findings hold at source under an independent instrument: A3 held nothing on OneDrive; the app has four places and `02` describes one; F87 is dead in the source and in the binary; the shared scan and print screens are the same sixteen classes, eleven scan groups and seven print groups; the three absences hold. No finding of A11 was overturned.
2. **The 17 corrections: 11 hold as written, 6 hold with a changed sentence, 0 do not hold.** The six: 7, 8, 9, 12, 13, 17 (sentences in section 7; order of application in section 11).
3. **A writer must NOT apply:** the edit of report A8 (correction 17: the change goes in `03:142` only); "not a requirement" for F87 as if it were ruled (correction 9: use the changed sentence); "four calls" and "no call needs `User.Read`" in the scopes row (correction 12: nothing leaves the scope list); the counts "28 calls, 22 live" without the second read's figures (correction 13).
4. **Errors found in A11: 16 entries, 4 that matter to a builder** (section 10): a live call is missing from the list (the thumbnail image of every file, fetched outside the Graph client: 29 calls, 23 live); five task-manager files A11 calls empty are not empty (they hold the base class of every task; old line ends made the line count 0; A8 has the same error); "refreshed once on a 401" is not what the code enforces; "four calls read other users' drives" is too narrow. Also a missed contradiction: F42's "six languages" against eight string sets in the OneDrive tree.
5. **Further than A11 went:** the two calls it left untraced are traced (both unreachable in a shipped build: 6 dead, 0 untraced); the Teams binary (1.09.22) was read and returns the same constant false; the `scan` and `print` packages of the binaries the two apps link (1.09.20 and 1.09.21) are byte-identical in all 364 classes, so "identically" does not hang on the version gap.
6. **Secrets:** the two application ids and the Workpath UUID are not in A11 (0 occurrences each, compared without display). One structural finding: a 24-character string equal to the two password values in `OD/app/build.gradle.kts:45` and `:47` stands in A11 at lines 259 and 425, because the tree uses that same string as a location name; it is also in `02:619` and seven other reports (section 9). Tuesday's call; nothing was changed.

| Count | Value |
|---|---|
| Corrections: hold / hold with a change / do not hold | 11 / 6 / 0 |
| Inventory rows checked / failed | 25 of 74 / 0 (21 as written, 4 in part) |
| Microsoft calls: A11 / second read | 28 (22 live, 2 untraced, 4 dead) / 29 (23 live, 0 untraced, 6 dead or unreferenced) |
| Call rows checked in full | 22 of 28 |
| Open questions of A11 genuinely open | 3 of 7 |
| `isSIOEnabled` lines by program | library 3, OneDrive 14, Mailflow 5, SharePoint 16, Teams 16, Universal Print 2; no setter anywhere |

## 1. Check 1: the prior-work claim (A11 section 2)

Instrument: `/usr/bin/grep -n -i` over the whole of A3 (462 lines) for `onedrive|PLACEHOLDER|OD/|ODJ/`, then for `sharepoint|graph|/me/drive|CommonSDKUtil|CVL`. Control: the same file returns Universal Print content for `graph` (lines 24, 151, 263, 264, 268, 297-302, 399, 406).

| Claim in A11 | Result | Pointer |
|---|---|---|
| A3 holds five placeholder comments for OneDrive (102, 332, 395, 413, 432) | **HOLDS.** `PLACEHOLDER` matches exactly those five lines | A3:102, 332, 395, 413, 432 |
| Nothing else on OneDrive in A3 | **HOLDS.** `onedrive` (any case) matches 15 lines in A3: the title (1), the source-of-truth line (3), the two shorthand rows (11, 12), the lane sentence (22), three pointer lines (30, 60, 62), two headings (92, 100), the five placeholders, and the keystore remark (439). None states a OneDrive behaviour, file read, journey or call. Every `graph` line in A3 is Universal Print | A3 lines as listed |
| "five placeholders" against a table of eight rows | Wording only: A11's table (A11:37-46) lists eight rows, of which five are the placeholder comments and three (A3:30, 60-62, 92-94) are forward pointers to a section 4.1 that is empty. Not an error of fact | A11:35-46 |
| A11:48 "The two OneDrive facts A3 does state" then lists three (the shorthand, the count 532, the keystore name) | **Small slip:** three facts, not two | A11:48 |

**What `02` rested on for its OneDrive rows, A3 being empty** (followed from the Source column of each F row that names OneDrive):

| `02` row | Its stated source | What that source is |
|---|---|---|
| F37 (`02:97`) | `A6#61` | A6:611, a row of the product-documentation checklist ("OneDrive: browse, scan to folder, print, rename, delete, create folder, search, sort, tile/list", sources `S1 §4.3`, `NEW:127`): the manuals, not the code. `02:97` copies it word for word |
| F38 (`02:98`) | `A6#62` plus `[A8 rows 54-56]`, A4 line 177 | A6:612 (documentation); the SharePoint source for the detail |
| F34 (`02:94`) | `A6#53`, `[A2 §1 item 3]` | A6:603 (documentation); the Mailflow source |
| F39 (`02:99`) | `A6#63-64`; `[A8 ...]` | documentation, corrected from the SharePoint source |
| F41 (`02:101`) | `[A2 §8 Q3]`, `[A1 §4.7]`, `[A8 §5.1]` | Mailflow, Authentication Manager and SharePoint source; no OneDrive source |
| Section 5.6.3 and the scopes row (`02:504`, `02:703`) | the coverage note | `02:7` says it in terms: "OneDrive and SharePoint journeys here rest on the product documentation `[A6 §9 rows 61-64]`, the shared-library report `[A4]` and a short inventory of ... CypherOneDrive-main" (three files named: `app/build.gradle.kts:121-128`, `RootSiteTask.java`, `GetLibraryMetadataTask.java`) |

So before A11 no OneDrive behaviour row of `02` rested on a read of the OneDrive source: they rest on the manuals (A6), with a three-file inventory for the fact that sites and libraries exist in the tree. A11's claim holds and `02:7` already said so.

## 2. Check 2: F87 and the switch (A11 section 9)

Instruments, all mine: (a) `/usr/bin/grep -r -n -i "SIOEnabled"` over each tree, `.java` and `.kt`; control in each tree: the number of files naming `WorkpathAccessService`. (b) A class-file reader written for this check (Python standard library only: `zipfile` to open the `.aar` and the `classes.jar` inside it, then my own walk of the constant pool, fields and methods; run with `python3 -I` from the session scratchpad; A11's `code_of.py` was not opened or used; nothing from a source tree was executed). Control inside the same class: `isAdmin()Z` and `isWhiteListedAgent()Z`.

**(a) Every place the source sets or reads it, by program**

| Program (tree) | Lines naming `SIOEnabled` | Of which | Control (files naming `WorkpathAccessService`) |
|---|---|---|---|
| Common library source 1.09.22 (`CVL/`) | 3 | 1 definition (`CVL/sdk/WorkpathAccessService.java:137`), 1 log string in its dead tail (`:144`), 1 reader (`CVL/ui/eula/EulaMainFragment.java:191`). **No setter, no field** | 6 |
| Common library copy sent 2026-11-20 (1.09.23, `extracted/cvl/`) | 3 | the same three lines | 6 |
| OneDrive 4.4.1 | 14 | all reads: `AppGuideActivity.java:111, 119, 164`; `MainActivity.java:239, 320, 325, 328, 958, 1078, 1213`; `MainBaseFragment.java:553, 573, 612`; `SettingsAppFragment.java:117` | 6 |
| Mailflow | 5 | all reads: `ui/main/MainActivity.kt:389, 400`; `ui/main/MainFragment.kt:830`; `ui/send/SendFragment.kt:627`; `ui/settings/SettingsAppFragment.kt:96` | 7 |
| SharePoint 4.4.6 (`SP/`) | 16 | all reads | 8 |
| Teams | 16 | all reads (`AppGuideActivity.kt:93, 101, 135`; `FilesFragment.kt:747, 792`; `MainActivity.kt:192, 234, 514, 699, 704, 707, 1191, 1272, 1281`; `RecentFragment.kt:289`; `SettingsAppFragment.kt:86`) | 8 |
| Universal Print | 2 | reads (`GetJobsActivity.kt:326`; `SettingsAppFragment.kt:73`) | 5 |
| HP Authentication Manager, QuickAccessLibrary source | 0 | (and 0 files name `WorkpathAccessService`, so these two zeros carry no control from the same word; they are outside the claim) | 0 |

The source body: `CVL/sdk/WorkpathAccessService.java:137-140` is `public boolean isSIOEnabled() { if (true) { return false; }`, with the old logic unreachable at `:142-147`. `isHPCloudUser()` has the same shape at `:108-111`. A11's line numbers are exact.

**(b) The compiled body, read from the bytes**

| Binary | Linked by | sha256 (first 16 hex) | `isSIOEnabled()Z` | `isHPCloudUser()Z` | Control `isAdmin()Z` | Classes in the jar naming `isSIOEnabled` | Classes extending `WorkpathAccessService` |
|---|---|---|---|---|---|---|---|
| `MF/app/libs/commonvaluablelibrary-1.09.20.aar` | Mailflow (`MF/app/build.gradle.kts:183`; resolved from `flatDir { dirs("libs") }`, `:137-138`) | `a785fa5de2a0a4a0` | 2 bytes `03 ac` | 2 bytes `03 ac` | 64 bytes | 2 (the class itself, `EulaMainFragment`) | 0 |
| `OD/CVL/commonvaluablelibrary-1.09.21.aar` | OneDrive (`OD/CVL/build.gradle:2`) | `c873e26157c6cd2a` | `03 ac` | `03 ac` | 64 bytes | 2 | 0 |
| `SP/CVL/commonvaluablelibrary-1.09.20.aar` | SharePoint (`SP/CVL/build.gradle:2`) | `a785fa5de2a0a4a0` (the same file as Mailflow's) | `03 ac` | `03 ac` | 64 bytes | 2 | 0 |
| `TM/app/libs/commonvaluablelibrary-1.09.22.aar` | Teams (`TM/app/build.gradle.kts:151`; `flatDir` at `TM/settings.gradle.kts:12-13`) | `79f75ea0b119c699` | `03 ac` | `03 ac` | 64 bytes | 2 | 0 |
| `L/UniversalPrint-main/CVL/commonvaluablelibrary-1.09.20.aar` | Universal Print | `a785fa5de2a0a4a0` | `03 ac` | `03 ac` | 64 bytes | 2 | 0 |

`03 ac` is `iconst_0`, `ireturn`. The class is `public` (access 0x0021), not final, superclass `java/lang/Object`, has no field whose name carries `SIO`, and no class in any of the five jars extends it. In the app sources no class extends or replaces it and nothing reaches it by reflection (search of `MF/app/src`, `OD/app/src`, `TM/app/src` for `extends WorkpathAccessService|: WorkpathAccessService(|class .*WorkpathAccessService|setAccessible|getDeclaredMethod`: 0 lines; control: `WorkpathAccessService.getInstance` occurs 17 times in `MF/app/src`).

**(c) The two doors to quick messages in Mailflow**

| Door | Line | Result |
|---|---|---|
| The "Quick messages" menu group | `MF/.../ui/main/MainActivity.kt:400-404`: VISIBLE if `isSIOEnabled`, else GONE; its click handler `:405-409` is the only place that starts `QuickMessagesActivity` (search of `MF/app/src/main` for the class name: the import at `:44`, the intent at `:406`, the class's own file, and the manifest entry) | HOLDS |
| The compose-screen button | `MF/.../ui/send/SendFragment.kt:626-628` `needToShowFab()` = `isSIOEnabled && quickMessage.isEnableQuickMessage`; used at `:563` | HOLDS (A11 cites `:626-628`; the call is on `:627`) |
| A third way in: another app starting the screen | `MF/app/src/main/AndroidManifest.xml:112-113`: `QuickMessagesActivity` is `android:exported="false"` | closed (A11 did not check this; it holds) |
| Not a door, but not behind the switch | `SendFragment.kt:603-605` reads `quickMessage.isAutoNewMail` / `isAutoReply` after the early return at `:563`: I did not read whether those lines sit inside the block the return guards | **not traced**, see NOT CHECKED |

**Verdict: DEAD, as A11 says, and it holds on the binary.** In the source and in the binary each app links, `isSIOEnabled()` returns the constant false, nothing sets it, nothing overrides it. The limit A11 states is the right one: this is true of any build made from these trees with the binaries in them; whether the installed builds were made from these trees is a release-record question.

**Does the same evidence cover the other rows?**

| Rows | A11's claim | Second read |
|---|---|---|
| OneDrive quick access (A11 rows 67, 68) | covered | **HOLDS**: OneDrive's own 1.09.21 binary read, `03 ac`; all 14 OneDrive lines are reads |
| SharePoint quick access (A8 rows 65 to 67, A8 open question 1) | covered | **HOLDS**: SharePoint's own 1.09.20 binary read (byte-identical to Mailflow's), `03 ac`; all 16 SharePoint lines are reads. I did not re-check that A8's rows 65 to 67 each rest only on this switch (A8 is the report for that) |
| Teams F82, F83 | **not** settled: Teams tree and binary not read | **A11 is right that it did not settle it, and this read goes one step further:** the 1.09.22 binary Teams links was read here and is `03 ac`; Teams resolves it from `app/libs` (`TM/settings.gradle.kts:12-13`); all 16 Teams lines are reads. What remains unread is the Teams gating itself: whether every route to `QuickAccessFragment` passes one of those 16 lines (13 Teams files name quick access; I read 7 of the 16 call sites, `MainActivity.kt:192, 234, 699, 704, 707, 1272, 1281`). So for Teams: the switch is constant false in the binary (settled); that F82/F83 are wholly behind it is **likely but not traced** |

## 3. Check 3: the Microsoft call list (A11 section 5)

Instrument: one `/usr/bin/grep -r -n -E` over `ODJ/` for every way the app can issue a request (`buildRequest`, `Request.Builder`, `.url(`, `.newCall(`, `openConnection`, `new URL(`, Retrofit annotations, and the SDK verbs `get|post|put|patch|delete`), then the task files read at the hit lines (ranges printed with their line numbers, log lines and blanks dropped). Control: the same search returns the calls A11 lists (for example `task/GetAllSitesTask.java:37-39`). A second search for image loading (`picasso|.load(|thumbnail`) and for every literal `http(s)://` address in `ODJ/`.

**My count against A11's 28.**

| Measure | A11 | Second read | Note |
|---|---|---|---|
| Places in `ODJ/` where a request is issued (next-page requests not counted) | not given | **40**: 38 through the Graph SDK or OkHttp (22 files' worth: `AccountInfoTask` 1, `CreateFolderTask` 1, `DeleteFilesTask` 2, `DownloadConvertToPdfFileTask` 1, `DownloadFileTask` 1, `DownloadMultipleFilesTask` 3, `GetAllSitesTask` 1, `GetDrivesTask` 1, `GetLibraryMetadataTask` 2, `GetListFolderTask` 1, `GetListFolderWithCreateFolderIfNotExistTask` 2, `GetRecentTask` 1, `GetSharedListFolderTask` 1, `RenameFileTask` 2, `SearchCallableTask` 3, `UpdateLibraryFieldsTask` 2, `UploadFileTask` 4, `UploadFileTaskReplace` 4, `MainBasePresenter` 3, `QuickAccessPresenter` 1, `RootSiteTask` 1) plus 2 plain downloads by `URLConnection` (`DownloadFileTask.java:87-89`, `DownloadMultipleFilesTask.java:417-418`) | |
| Rows when grouped as A11 groups them (one per method and resource) | 28 | **28 of A11's rows found, every one; plus 1 that A11 does not list** = 29 | the missing one is the thumbnail fetch, below |
| Live | 22 (C1 to C22) | **23**: A11's 22, all confirmed live as coded, plus the thumbnail fetch | |
| Not traced | 2 (C23, C24) | **0**: both traced here, both not reachable in a shipped build | below |
| Dead or unreferenced | 4 (C25 to C28) | **6**: C23, C24, C25, C26, C27, C28 | |

**The call A11 does not list (an omission, not a wrong row).** Each file row in the list fetches its "large" thumbnail image from the address Graph returned: `ODJ/model/FileItem.java:79-84` keeps `thumbnails[0].large.url`, and `ODJ/ui/main/base/FileItemViewHolder.java:247-249` loads it with Picasso (`mPicasso.load(Uri.parse(mItem.getThumbnailUri()))`; the adapter is built with `Picasso.get()` at `ODJ/ui/main/MainBaseFragment.java:446`). That is one plain GET per file shown, to a Microsoft-hosted address, without the Graph client (so without the app's token header, time limits or 401 refresh). A11 names the `$expand` that asks for the address (C8, row 17) but not the fetch. For the port it matters: the server must fetch or proxy these images, and how long such an address stays valid was not checked (no network).

**The two calls A11 left untraced.**

| Call | Trace | Result |
|---|---|---|
| C24 `GetListFolderWithCreateFolderIfNotExistTask` | The task is created in one place, `ODJ/ui/main/presenter/MainBasePresenter.java:431`, inside `loadDataWithCreateFolderIfNotExist(FileItem)` (`:429`). That presenter method is called from one place, `ODJ/ui/main/MainBaseFragment.java:1560`, inside the fragment's own `loadDataWithCreateFolderIfNotExist(String defaultPath)` (`:1546`). **Nothing calls the fragment method**: the name occurs in 3 files (`MainBaseContract.java:60` the interface line, `MainBasePresenter.java` the implementation and its log lines, `MainBaseFragment.java:1546` and `:1560`) and nowhere else in `OD/app` (`.java`, `.kt`, `.xml`). Control: `downloadMultipleFiles` is found at its two `MainActivity` call sites (`:1270`, `:1280`) | **UNREFERENCED.** A11's pointer is slightly off: it calls `MainBaseFragment.java:1560` "one caller ... whose own caller was not read"; the own caller does not exist |
| C23 `GET /drives/{d}/items/{i}/children` in `DownloadMultipleFilesTask.retrieveFoldersChildren` | The method runs on every multi-download (`DownloadMultipleFilesTask.java:75`) but issues the request only for a list entry that is a folder (`:197-200`, `:206-210`). Two callers build the list: (1) the live multi-select print, `MainBaseFragment.java:869-872`, from the selected rows; the print button that leads there is disabled whenever a folder is selected (`ODJ/ui/main/MainActivity.java:1519-1523`, `:1535-1538`, `:1557-1560`, each through `isFolderSelected()` at `:1594-1606`); (2) quick-access folder print, `ODJ/ui/main/QuickAccessFragment.kt:475`, `:483` through `QuickAccessPresenter.kt:248-252`, which is behind the switch (A11 row 67) | **DEAD (switch) for the request itself**; the method is live but in the live path it never meets a folder. One step not proven: that a disabled button cannot be pressed (it is the only guard; the task itself does not refuse folders) |

**Rows checked in full (method, path, cited line, state).** 22 of the 28, by reading the cited lines:

| Row | Method and path as A11 states them | Cited lines say it? | State |
|---|---|---|---|
| C1 | `GET /sites?search=*&$top=500`, all pages | yes (`GetAllSitesTask.java:33-39`, loop `:51-66`) | live |
| C2 | `GET /sites?search=<q>&$top=500`, all pages | yes (`RootSiteTask.java:56-62`, `:77`) | live |
| C3 | `GET /sites/{s}/drives`, first page only | yes (`GetDrivesTask.java:30-34`; no next-page call in the file) | live |
| C4, C5 | list behind the drive; columns, all pages | yes (`GetLibraryMetadataTask.java:25-30`, `:36-46`) | live |
| C6, C7 | `GET .../listItem` only when the id is missing; `PATCH .../fields` | yes (`UpdateLibraryFieldsTask.java:23-33`, `:38-44`) | live |
| C8 | eight path shapes, Select, `$expand`, no `$top`, all pages | yes: three library shapes (`GetListFolderTask.java:68-86`) and five others (`:88-117`); select and expand `:123-132`; loop `:134-157` | live |
| C9 | `GET /me/drive/recent` | yes (`GetRecentTask.java:43-50`). **Paging is conditional, not simply "all pages":** the loop stops once `maxCount` items are added when `maxCount > 0` (`:69`); all pages only when the caller passes 0. I did not read which the Recent screen passes (`MainBaseFragment.java:1524`) | live |
| C10 | `GET /me/drive/sharedWithMe?allowexternal=true`, all pages | yes (`GetSharedListFolderTask.java:35-63`) | live |
| C11 | drive search, `$top=400`, first page only | yes (`SearchCallableTask.java:114-136`) | live |
| C12 | `POST /search/query`, driveItem, from 0, size 400, 11 fields | yes (`:138-172`; I count the 11 field names at `:148-158`) | live |
| C13 | re-read of each hit, failure ignored | yes (`:204-220`) | live |
| C14 | `POST .../children`, conflict "fail", eight shapes | yes (`CreateFolderTask.java:67-131`) | live |
| C15, C16 | `PATCH` and `DELETE` on `/drives/{d}/items/{i}` or `/me/drive/items/{i}` | yes (`RenameFileTask.java:58-71`; `DeleteFilesTask.java:52-65`) | live |
| C17 | item read then a plain GET of the download address, 5 s / 6 s | yes (`DownloadFileTask.java:76-93`) | live |
| C18 | `GET .../content?format=pdf` | yes (`DownloadConvertToPdfFileTask.java:68-84`) | live |
| C19 | `PUT ...:/content`, conflict "fail", four shapes | yes (`UploadFileTask.java:234-283`) | live |
| C20 | hand-built `createUploadSession`, four shapes, own OkHttp client and hand-built Bearer header | yes (`:378-415`, `:426-465`; token captured once at construction `:85`; client `:185-190` has no authenticator) | live |
| C21 | `PUT` pieces, 202 = next, retry on 408, 429, 5xx | yes (`:505-592`, `:596-598`) | live |
| C22 | `GET .../permissions`, three shapes, first page | yes (`MainBasePresenter.java:947-991`; only `getCurrentPage()` is read, `:1005`) | live |
| C26, C28 | unreferenced | yes: `AccountInfoTask` and `UploadFileTaskReplace` each occur in 1 file of `OD/app` (their own); control `UploadFileTask` in 8 files | unreferenced. **C28's row leaves out a fourth call of that class**, a `POST .../children` at `UploadFileTaskReplace.java:479` (dead with the rest) |
| C27 | dead: no caller passes the flag | yes: the three-argument constructor (`UploadFileTask.java:102`) has no caller; both callers use the one-argument one (`ScanPreviewPresenter.java:57`, `QuickAccessPresenter.kt:339`) | dead |

Not re-read line by line: C25 (its state rests on the switch, check 2).

**The three absences.**

| Absence claimed | My search (over `ODJ/`, any case, counted with `-c` and `-l`) | Control from the same tree | Result |
|---|---|---|---|
| No sign-in endpoint called | `login.microsoftonline`: 6 lines in 1 file; `oauth2`: 6 lines in 1 file; the file is `constants/OneDriveConstants.java` and the six lines are `:13-18`, each beginning `//`. Every literal `http(s)://` address in `ODJ/` was listed: those six and two licence links in a comparator. A search of the whole tree (`.java`, `.kt`, `.xml`, `.kts`, `.gradle`, `.properties`) for `login.microsoftonline` finds that one file only | the search finds the six lines | **HOLDS** for the app source. The vendored binaries (`usermanagement`, the Graph SDK) were not searched |
| No `Retry-After` read | `retry-after`: 0 lines, 0 files; `retryafter`: 0 | `conflictBehavior`: 5 lines in 4 files; `retry`: 11 lines in 2 files | **HOLDS, and it holds one level deeper than A11 shows:** the Graph client is built on a bare OkHttp client (`ODJ/common/GraphProvider.kt:32-44`, passed by `.httpClient(okHttp)` at `:62-65`), so the Graph SDK's own retry handler, which is added only when the SDK builds its default client, is not in the chain. That last clause is general knowledge of the SDK, not read from its binary |
| No limit on the large-upload retry | read of the loop: `retryAttempt` is declared (`UploadFileTask.java:508`), reset on a 202 (`:550`), incremented (`:567`) and passed to the wait (`:572`); it is compared with nothing. `MAX_RETR` and `maxRetr`: 0 lines | `retryAttempt`: 5 lines in 1 file | **HOLDS.** The only exits are success, a non-retryable status, the quota error, an exception from the request (not retried), or the user's cancel (`:511-514`) |

**One statement in this section that the source does not carry: "refreshed once on a 401" / "retries the request once" (A11:22, row 7, section 5 "one retry on 401").** `ODJ/auth/SessionAuthenticator.kt:19-59` asks for a new token and returns the request with it; it keeps no count and does not look at the prior response. If the retried request is answered 401 again, the HTTP library calls the authenticator again. What stops it is the HTTP library's own cap on follow-up requests, not this code (the cap is general knowledge of OkHttp, not read here). The sentence that holds: "on each 401 the app asks HP Authentication Manager for a new token, waits at most 10 s and repeats the request with it; nothing in the app limits this to one attempt".

**Counts A11 gives near the call list.**

| A11 | Second read |
|---|---|
| 532 files in the tree | 532 (`find -type f`) |
| 160 `.java` and 27 `.kt` in the tree | 160 and 27 |
| "under `OD/app/src` 176 source files, 23,772 lines" (A11:75) | **173** under `OD/app/src` (146 `.java`, 27 `.kt`); 174 under `OD/app` with the one unit test. 23,772 is the newline count of those 174 files, so the figure belongs to `OD/app`, and it undercounts (next row) |
| "Five files in `ODJ/taskmanager/` are empty (0 lines each)" (A11:75) | **WRONG.** They are 2,599, 888, 137, 227 and 145 bytes. They contain no line-feed character at all (old Macintosh line ends: 89, 29, 8, 9 and 6 carriage returns), which is why a line count prints 0. `AbstractProgressableAsyncTask.java` is the base class of every task in section 5 (`doInBackground`, `performTaskInBackground`, the completion and progress listeners). The same is true of the SharePoint tree's five files (2,610, 899, 148, 238, 156 bytes), so **A8 line 57 carries the same error** |

## 4. Check 4: the inventory (A11 section 4, 74 rows)

Rule stated before choosing: every fourth row starting at row 1 (1, 5, 9, ... 73: 19 rows), plus every row whose state is DEAD, UNREFERENCED or "absent", plus row 69 (the one A11 calls live against A8): 67, 68, 69, 70, 71, 72, 74. **25 rows.** Instrument: the cited lines printed with their numbers and read. Control: a row counts as checked only where the printed line carries the fact.

| Row | What A11 says | The cited line says it? |
|---|---|---|
| 1 | launcher → splash; app class starts the encrypted store and the Graph client | **yes** (`OD/app/AndroidManifest.xml:27-37`; `ODJ/common/CommonApp.java:13-17`) |
| 5 | identity from token claims `tid`, `oid`, `unique_name`, `family_name`, `given_name`, decoded not verified; drawer shows the names | **yes** (`SplashActivity.java:524-536`; `MainActivity.java:343-346`) |
| 9 | Graph base address from the cloud configuration | **yes** (`GraphProvider.kt:50-67`) |
| 13 | screens protected from capture | **yes, with a nuance A11 omits:** at two of the three cited places the flag is set only when the build is not a debug build (`SplashActivity.java:94-97`; `RootBaseAppCompatActivity.java:34-36`); `PresenterAppActivity.java:25-28` sets it always |
| 17 | My Drive listing, by id or path, all pages, large thumbnail | **yes** (`GetListFolderTask.java:88-117`, `:121-157`) |
| 21 | sites by search `*`, 500 a page, all pages | **yes** (`GetAllSitesTask.java:33-39`, `:51-65`; `MainBasePresenter.java:1020-1022`) |
| 25 | library columns: the list, then all pages of columns | **yes** (`GetLibraryMetadataTask.java:25-48`). `LibraryColumnMapper.kt` not opened by me either |
| 29 | folder cache of 40, "shown at once then reloaded" | **in part:** 40 entries yes (`FolderNavigationCache.java:14-19`); `MainBaseFragment.java:1750` shows the cached list; "then reloaded" is not on the cited lines and I did not look for it |
| 33 | file search, 400, first page; 400 shown as empty | **yes** (`SearchCallableTask.java:114-136`, `:97-98`) |
| 37 | create folder: name check, "fail on conflict", 409 and 400 messages | **yes** (`MainBaseFragment.java:881-906`, a case-insensitive check against folders on screen; `CreateFolderTask.java:125-142`) |
| 41 | tap a file: download, then preview | **in part:** the tap handler and the two download paths yes (`MainBaseFragment.java:767-772`; `MainBasePresenter.java:530-548`); "then print preview" lies further down the cited range and was not read |
| 45 | download address from the listing, else one item read; 5 s / 6 s; no retry; free-space check | **yes** (`DownloadFileTask.java:40-41`, `:76-93`) |
| 49 | scan options are the library's; defaults from the form | **yes** (`OneDrive.moc:1207`; `SettingsAppFragment.java:104-108`) |
| 53 | never overwrites; one destination → duplicate-name error | **yes** (`UploadFileTask.java:235`, `:296-297`, `:429`, `:445-446`) |
| 57 | device mail helper; "SMTP not configured"; failure mail to the recipients, else to the user | **yes** (`SendEmailTask.java:29`, `:60`; `EmailSender.java:34-52`, `:101-103`; `ScanPreviewPresenter.java:84-101`, `:112-148`). One addition from the same lines: the failure mail is built with the same file list as attachments (`:116`, `:125`), so the scans go out by mail even when the upload failed |
| 61 | information page, licences, app guide from the menu | **in part:** guide and information yes (`MainActivity.java:1336-1341`); the open-source licences entry is not on the cited lines |
| 65 | personal flavour cannot sign in: endpoints commented out, constants unused, HPAM queries the business package only | **yes** (`OneDriveConstants.java:13-18` each line begins `//`; the four constant names occur in 1 file of `OD/app`, their own, 6 lines; A4:125 lists `com.hp.print.cypher.onedriveforbusiness` and no personal package) |
| 67 | quick access behind the switch | **yes** for the cited switch lines (`MainActivity.java:239`, `:320-328`, `:958-976`; `MainBaseFragment.java:553`, `:573`, `:612`; `SettingsAppFragment.java:117-118`; `AppConstants.java:41-43` = 10, 10, 4). The individual features inside quick access were not read |
| 68 | settings for a non-administrator, app guide at first use, "remember me" | **yes** for the lines (`MainActivity.java:1213`; `AppGuideActivity.java:111`, `:119`, `:164`); what each guarded block does was not read |
| 69 | sign-out confirmation screen reached from Back at the sites step when the switch is false: live as coded | **yes** (`MainActivity.java:1075-1081`, `:1854-1857`). A real difference from SharePoint if A8 row 70 is right; not on a device |
| 70 | domain hint, URL bar, EULA entry commented out | **yes** (`SettingsAppFragment.java:114`, `:122`, `:126`) |
| 71 | `AccountInfoTask` unreferenced | **yes** (1 file in `OD/app`; control `UploadFileTask` in 8 files. A11 says the control is "in 5 files"; my count over `.java`, `.kt`, `.xml` is 8, the word-boundary form included; the difference does not touch the finding) |
| 72 | `UploadFileTaskReplace` unreferenced | **yes** (1 file) |
| 73 | "create the destination folder" dead: no caller passes the flag | **yes** (`UploadFileTask.java:102-105`, `:181-182`; both callers one-argument) |
| 74 | nothing on sensitivity labels | **yes** (`sensitivity`, any case: 0 files in `ODJ/` and 0 in the whole tree's `.java`, `.kt`, `.xml`, `.kts`; control `CommonSDKUtil` in 19 files, the same number A11 gives) |

**Result: 25 rows checked. 0 failed. 21 hold as written; 4 hold in part** (rows 13, 29, 41, 61: the fact at the cited line is narrower than the row's sentence; none is contradicted). The one false statement found in A11's sections 3 and 4 is not a numbered row: the "empty" task-manager files (check 3, last table).

## 5. Check 5: the four places, and the claim that `02` describes My Drive only

| Pointer | What it shows |
|---|---|
| Source: `ODJ/ui/main/base/MainViewType.java:3-11` | the enum has `QUICK_ACCESS`, `MY_DRIVE`, `RECENT`, `SHARED_WITH_ME`, `SHARED_LIBRARIES`, `QUICK_PRINT`, `QUICK_SCAN` |
| Source: `ODJ/ui/main/MainActivity.java:750-762` (My Drive), `:769-779` (Recent), `:786-796` (Shared with me), `:809-820` (Shared libraries) | four drawer entries each set their own view type; none of the four is behind the switch |
| Source: `ODJ/ui/main/MainActivity.java:957-980` | the first screen is `MY_DRIVE` unless the switch is true |
| Source: `ODJ/ui/main/sites/SharedLibrariesStep.java:3-7` | `SITES`, `LIBRARIES`, `FILE_ITEMS` |
| Source: `ODJ/ui/main/MainActivity.java:337-339` | the personal flavour hides the Shared libraries entry |
| Document: `02:97` (F37) | "OneDrive: browse, scan to folder, print, rename, delete, create folder, search, sort, tile/list" |
| Document: `02:504` (5.6.3) | "OneDrive: `/me/drive` browse, search, sort, tile/list, rename, delete, create folder, scan to folder, print. SharePoint: sites → libraries → folders ..." |
| Search of `02` for `sharedWithMe`, `Shared with me`, `Recent` as a OneDrive place | 0 lines name Recent files or Shared with me for OneDrive; control: `onedrive` matches 36 lines of `02`; `shared librar` matches 0 as a OneDrive place (1 line in all); `recent files` matches 1 line, the Teams row F81 (`02:169`) |

**HOLDS, both halves.** One qualification a writer needs: `02:7` (the coverage note) does already say that the OneDrive tree has "SharePoint site and library browsing inside it", so the design was not unaware of Shared libraries; what `02` lacks is any *requirement* row for Recent, Shared with me, or Shared libraries reached from the OneDrive tile.

## 6. Check 6: the shared scan and print screens (A11 section 7)

Instruments: (a) the two list-building files read whole with line numbers (`CVL/scan/ScanViewItems.java`, `CVL/print/PrintViewItems.java`); (b) the enum constants counted by `/usr/bin/grep -n -E` for a constant at four spaces of indent in `ScanOptionGroups.java` and `PrintOptionGroups.java`; (c) every import of the library's `scan` or `print` package in each app, by `/usr/bin/grep -r -h -o -E`, sorted and compared with `comm`; control: the total of all mentions of those two packages equals the import count in each app (25 and 30), so no class is used by its full name without an import; (d) **new in this read: the compiled classes of the `scan` and `print` packages compared byte for byte across the three binaries** (my own script, `zipfile` and `hashlib` only, nothing decompiled).

| Claim in A11 | Second read | Pointer |
|---|---|---|
| 16 library classes imported by both apps, the same 16, no others | **HOLDS exactly.** OneDrive 25 import lines, 16 distinct; SharePoint 30, 16 distinct; 0 only in one app. The two count differences A11 names are right (`SimpleDividerItemDecoration` 5 against 1; `PrintPreviewFragment` 4 against 3) | search (c) over `OD/app/src` and `SP/app/src` |
| 11 scan option groups in the list | **HOLDS**: 11 names at `CVL/scan/ScanViewItems.java:31-41`; pruning by what the device offers at `:54-117`; colour dropout removed unconditionally at `:66-68`; file type and resolution only disabled, never removed (`:46-53`) | as cited |
| "Eighteen groups are defined in the enum" (A11:297) | **WRONG by one: 19.** `ORIGINAL_SIZE`, `ORIGINAL_DUPLEX`, `DOCUMENT_FORMAT`, `SCAN_RESOLUTION`, `ORIENTATION`, `FILE_NAME`, `PDF_ENCRYPTION`, `COLOR_MODE`, `COLOR_DROPOUT_MODE`, `SCAN_PREVIEW`, `OUTPUT_QUALITY`, `OCR_LANGUAGE`, `OPTIMIZE_TEXT_PICTURE`, `BLANK_PAGE`, `TYPE_RESOLUTION`, `IMAGE_ADJUSTMENT`, `CROP_MODE`, `MULTI_FEED_DETECTION`, `SPLIT_ATTACHMENT` | `CVL/scan/ScanOptionGroups.java:46-171` (19 constant lines) |
| 7 print option groups listed, an eighth conditional; 14 defined | **HOLDS**: 7 at `CVL/print/PrintViewItems.java:28-34`; `SENSITIVITY_LABEL` added only if `SensitivityLabelManager.isFeatureEnabled()` (`:36-38`); 14 constants at `CVL/print/PrintOptionGroups.java:37-116` | as cited |
| The paper-source defect (source unavailable disables size) | **HOLDS** (`CVL/print/PrintViewItems.java:81-84`: the test is on `paperSourceOption`, the call is on `paperSizeOption`) | as cited |
| Staple pruned from a list it was never added to | **HOLDS** (`:65-69`; `STAPLE_MODE` is not among `:28-34`) | as cited |
| Titles | 17 title strings checked at the cited lines of `CVLres/values/strings.xml` (`:5, 65, 78, 84, 85, 91, 120, 149, 178, 183, 316, 368, 375, 381, 387, 423, 431`): **all 17 say what A11 says**. 435 `<string ` lines: holds | as cited |
| The two source copies (1.09.22 library, 1.09.23 sent) do not differ in `scan` or `print` | **HOLDS**: `diff -rq` 0 and 0 (69 and 61 files); control: `sharepoint` differs in 1 file. Versions at `commonvaluablelibrary/build.gradle.kts:12` of each copy | as cited |

**Does "identically" hold for the two apps?** It holds for *which library classes each app uses* (the import sets are equal). A11's sentence "the shared screens are used identically" (A11:331) says a little more than an import search can carry: equal imports do not show that the two apps pass the same arguments, subclass the screens the same way, or set the same defaults. A11's own table lists the wrappers that differ (metadata inputs, the placement of document separation in the form). The sentence that the evidence carries: "both apps use the same sixteen library classes for scan and print; what each app does around and with them was compared only at the points of the table in 7.3".

**A11 read the 1.09.22 source; the apps link the 1.09.20 and 1.09.21 binaries. What that leaves unproven, and what this read closes of it:**

| Question | Before this read | After check (d) |
|---|---|---|
| Are the scan and print screens the same in the two binaries the two apps link? | not known (A11: "the screens inside those binaries were not read") | **Yes at the class level.** In `SP/CVL/commonvaluablelibrary-1.09.20.aar` and `OD/CVL/commonvaluablelibrary-1.09.21.aar` the `scan` package has 186 classes and the `print` package 178, the same names, and **all 364 are byte-identical**. So for scan and print code the two apps link the same thing, and "identically" does not depend on the version gap |
| Do those binaries have the same option lists as the 1.09.22 source A11 read? | not known | **Partly closed.** The four classes that define the groups and the lists (`ScanViewItems`, `PrintViewItems`, `ScanOptionGroups`, `PrintOptionGroups`) are byte-identical in the 1.09.20, 1.09.21 and 1.09.22 binaries (same length and hash each). The 1.09.22 binary differs from 1.09.21 in 26 inner classes of option screens (13 in `scan/view/...`, 13 in `print/view/...`, each a `$1` or `$2` listener class), none of them a list or enum class. **Still unproven:** that the 1.09.22 *source* is what the 1.09.22 *binary* was compiled from (nothing was decompiled; the constant names `FINISHINGS`, `SENSITIVITY_LABEL`, `CROP_MODE`, `SPLIT_ATTACHMENT` are present in the binary classes where the source has them, which is consistent and no more) |
| Are the titles and the other strings the same in the linked binaries? | not known | **Not checked**: the resources inside the `.aar` files were not compared |
| Does `SensitivityLabelManager.isFeatureEnabled()` behave the same in 1.09.20 and 1.09.21? | not known | **Not checked** (outside `scan` and `print`; the jars differ by 65 classes in other packages: 691 against 756 under the library's package) |
| The values inside each option (resolutions, sizes, formats) | not read by A11 | not read here either |

## 7. Check 7: the 17 PROPOSED CORRECTIONS (A11 section 11)

Instrument: the document line printed by number (`awk 'NR==n'`) and compared with A11's quotation; the source lines printed and read; CLARIFICATIONS read whole (C-1 to C-44, 290 lines) for a ruling each correction could cross. "Doc line says it" = the text A11 says it replaces or extends is there, at that line.

| # | Target | Doc line says what A11 says? (printed) | Source supports the new sentence? | Verdict |
|---|---|---|---|---|
| 1 | `02:97` F37 | yes: "OneDrive: browse, scan to folder, print, rename, delete, create folder, search, sort, tile/list" (source column `A6#61`) | yes: four drawer places (`MainActivity.java:750-820`); six sort values (`SortingType.kt:7-13`); rename and delete shown only with the write flag (`MainBaseFragment.java:627-628`); scan button and create-folder follow the same flag (`:864-866`, `:1583-1596`); swipe prints directly (`:719-737`, in list view and outside multi-select only) | **HOLDS** |
| 2 | new row near `02:97` (Shared libraries) | n/a (new row) | yes: sites all pages (`GetAllSitesTask.java:33-66`); last 3 sites (`AppConstants.java:70`, `MainBaseFragment.java:1152-1153`); column definitions (`GetLibraryMetadataTask.java:25-48`); sort and group by a column saved per library (`UserPreferencesStore.kt:162`, `:177`, called from `MainBaseFragment.java`); edit column values (`MainBaseFragment.java:629-633`, `UpdateLibraryFieldsTask.java:23-44`); no metadata at scan (`BaseScanDescriptionAppFragment.java:10-30` all bodies empty; `LibraryColumn|metadata|ColumnDefinition` in `ScanDescriptionAppFragment.java`: 0 lines, control `email` 45) | **HOLDS.** A writer may add "(libraries of a site: first page only, `GetDrivesTask.java:30-34`)" |
| 3 | new row (quota message) | n/a | yes (`UploadFileTask.java:286-292`, `:450-455`, `:558-564`, `:728-770`; `ErrorHandlingUtils.java:61-62`) | **HOLDS** |
| 4 | new row (search) | n/a | yes (`SearchCallableTask.java:114-172`; `SearchActivity.java:187-193` with `RECENT_LIMIT` = 3) | **HOLDS** |
| 5 | `02:93` F33 | yes: "sides, colour, paper size/tray, collate, copies, page range; options limited to device capability" | yes (`CVL/print/PrintViewItems.java:28-34`: Finishings listed; `:76-79` paper type); and the list class is byte-identical in the 1.09.20 and 1.09.21 binaries (check 6) | **HOLDS** |
| 6 | `02:91` F31 | yes: "sides, colour, size, orientation, resolution 75-600, image adjustments, blank-page suppression, misfeed detection; formats ..." (no cropping, no optimise text/picture) | yes (`CVL/scan/ScanViewItems.java:37-38`, `:66-68`) | **HOLDS** |
| 7 | `02:98` F38 | **partly:** A11 says "add 'at most 5 recipients; when the upload fails a failure e-mail is sent ...'". `02:98` already says, for the SharePoint app, "goes to at most five recipients prefilled with the user's own address, and a failure mail is sent when the upload fails `[A8 rows 54-56]`; the server's Graph mail keeps those three behaviours" | yes for OneDrive (`ScanDescriptionAppFragment.java:308-310`; `ScanPreviewPresenter.java:112-148`) | **HOLDS WITH A CHANGE.** Do not add the two facts a second time. Sentence: "The OneDrive app does the same `[A11 rows 56, 57]`; when the upload fails and no recipient was entered, the failure mail goes to the user's own address (`ScanPreviewPresenter.java:117-125`)." |
| 8 | `02:101` F41 | yes: names the `sharepoint.` keys only, "three are written by live features" | yes for the seven names (`UserPreferencesStore.kt:14-22`). But the row's own style separates live from dead, and A11's sentence does not: `quick_access` is written only by quick access (`model/QuickAccess.kt`, dead by the switch); the other six are written from live screens (`SearchActivity.java:193`, `SitesSearchActivity.java`, `MainBaseFragment.java`) | **HOLDS WITH A CHANGE.** Sentence: "OneDrive's keys are prefixed `onedrive.`; six are written by live features (`recent_searches`, `recent_site_searches`, `recent_sites`, `library_columns`, `library_column_state`, `predefined_column_state`); `quick_access` is written only by the dead quick-access feature `[A11 row 14; B1769 §7]`." |
| 9 | `02:175` F87 | yes: "**Condition:** the Workpath code offers this only behind the dead `isSIOEnabled` switch (reports A2 line 132, A4 line 290); it is a requirement only if a Workpath 4.4 printer shows it (checked in WP0.6). F41 roams the data either way" | the fact, yes (check 2). The words "not a requirement" go further than a source read can: the row's own condition is a printer look, and A11 itself asks the product owner whether the source and binary are enough (its question 4). The same wording was used for F89 under "the rule of section 3.1" (`02:177`), so there is a precedent in the document, not a ruling | **HOLDS WITH A CHANGE.** Sentence: "**Condition settled at source and in the binary (A11 §9, second read B1769 §2):** `isSIOEnabled()` is a method of the common library that returns the constant false in the source (`WorkpathAccessService.java:137-140`) and in the 1.09.20 binary Mailflow links (method body `03 ac`); nothing sets or overrides it. By the rule of section 3.1 this row is not a requirement; the printer look named here before is no longer what decides it, unless the product owner asks for one (master list). F41 roams the data either way." |
| 10 | `02:200` F93 | yes, word for word: "Whether the scan button is withheld too is not established in A8; settled in WP3.4" | yes (`MainBaseFragment.java:864-866`, `:1583-1596`; `MainActivity.java:2097-2099` for the no-scanner case) | **HOLDS** |
| 11 | `02:504` (5.6.3) | yes, word for word: "OneDrive: `/me/drive` browse, search, sort, tile/list, rename, delete, create folder, scan to folder, print" | yes: no page size is set on the listing (`GetListFolderTask.java:121-132`, the options list is empty) and every page is followed (`:134-157`); A8:107 (row 20) says "20 per page" for SharePoint | **HOLDS.** Replace only that sentence; the rest of `02:504` is B1760's text |
| 12 | `02:703` (7.2) | yes: the row lists `Files.ReadWrite.All`, `Sites.ReadWrite.All`, `User.Read`, `Mail.Send` and its sources | in part. (a) "names no scope for its live path": yes. (b) "22 live Graph calls": yes (the 23rd live call is not Graph). (c) "of which four read other users' drives": **too narrow.** The four A11 names are the calls the SharePoint app does not make (A11:251 says so correctly); but inside a Shared-with-me folder the rename, delete, download, convert, upload and permission calls (C14 to C20, C22) also go to another user's drive, by `/drives/{d}/items/{i}`. (d) "no live OneDrive call needs `User.Read`": true of the calls (the one `/me` task is unreferenced), but the row is the registration's scope list, the product documentation lists `User.Read` for OneDrive (A6:353), and sign-in is the hub's, so a writer must not read this as "remove `User.Read`" | **HOLDS WITH A CHANGE.** Sentence: "The OneDrive source names no scope for its live path; it has 22 live Graph calls `[A11 §5]`. The Shared-with-me place reaches other users' drives (the listing, the Search API query, and every item call made inside a shared folder): whether `Sites.ReadWrite.All` covers them is checked on a tenant, not assumed. The product documentation lists `Sites.ReadWrite.All` and `User.Read` for OneDrive and `Files.ReadWrite.All` for Teams only (A6:353-355). The OneDrive app itself makes no `/me` call; `User.Read` stays in this row." |
| 13 | `02:7` coverage note | yes: "A full read of that tree is work package WP0.6 in document 2" is there | the counts need the second read's corrections | **HOLDS WITH A CHANGE.** Sentence: "That tree is now read in the main: report A11 (74 rows; 28 Microsoft calls listed, of which 22 are live Graph calls and 6 are dead or unreferenced after the second read, plus one live image fetch A11 does not list: `review/B1769_A11_SECOND-READ.md` §3); what A11 did not open is listed in its section 13." |
| 14 | `02:927` R17 | yes: "the risk now rests on the OneDrive half, which is still unread, and on A8's own limits" | yes | **HOLDS** |
| 15 | `03:142` WP0.6 | yes, word for word: "**What is left of this package:** the OneDrive tree (unread); the common-library scan and print screens as the SharePoint app uses them (A8 did not re-read them); F87; and" | yes; the row's own check ("second reader") and its exit ("Graph call list and journeys documented; F87 and F89 marked live or dead") are met by A11 plus this file | **HOLDS.** A writer may add "(second read: B1769)" |
| 16 | `03:185` WP3.9 and `02:504` | yes: `03:185` gives the reason "the release pipeline builds the business flavour only and the consumer sign-in endpoints are commented out"; `02:504` carries the OQ-4 sentence | yes: 4 lines name `BuildConfig.FLAVOR` in `ODJ/` (`AppConstants.java:76`, `MainActivity.java:337`, `SettingsAppFragment.java:121` with an empty body, `SplashActivity.java:118` a log line); no sign-in screen in the manifest; the constants unused | **HOLDS.** It adds a reason and rules nothing (OQ-4 stays open, C-32) |
| 17 | report A8 line 311 and `03:142` | `03:142` yes: "a look at a Workpath printer running SharePoint 4.4.6 for the rows A8 marks dead and for the manual's '4 custom fields' (A8 §9 questions 1, 2, 4)". A8:311 yes: its question 1 says the binary "was not decompiled" | yes: SharePoint's own 1.09.20 binary read here, `03 ac` (check 2) | **HOLDS WITH A CHANGE.** (1) **Not in report A8:** a report is a record of what its reader found; the correction goes in `03:142` (and nowhere in A8). The commission for A11 asked for sentences in `02`, `03` or `05` only (B1768, lane D item 6). (2) Sentence for `03:142`: "the 1.09.20 binary the SharePoint app links returns the constant false from `isSIOEnabled` `[A11 §9 item 3; B1769 §2]`, so A8 rows 65 to 67 (quick access, remember-me, app guide at first use) no longer need the printer look; the look is still wanted for the manual's '4 custom fields' (A8 §9 question 4)." |

**Counts: 17 corrections. HOLDS: 11** (1, 2, 3, 4, 5, 6, 10, 11, 14, 15, 16). **HOLDS WITH A CHANGE: 6** (7, 8, 9, 12, 13, 17). **DOES NOT HOLD: 0.**

**Against the rulings in CLARIFICATIONS:**

| Ruling | Corrections that touch it | Contradiction? |
|---|---|---|
| C-16 "Full match of everything" | 1, 2, 3, 4, 5, 6, 11 add behaviour the shipped app has: they follow the ruling. 9 and 17 take dead features out: consistent with the document's reading "parity means what Workpath ships" (`02:900`, D34), which is itself open question OQ-3 on its default (C-32), not a ruling | none. Correction 9 is the one place where a writer could put a ruling in the product owner's mouth: use the sentence above |
| C-38 sensitivity labels left out | 5 adds finishings and paper type and leaves the eighth, conditional print group (the sensitivity label) out | none |
| C-15 "As assumed" (scan and print behaviour; Send to e-mail replaced by server mail) | 7 | none: it adds a detail of today's behaviour |
| C-25 reuse the existing Entra registration | 12 | none if the sentence above is used; A11's own wording could be read as dropping `User.Read` from a registration that is being reused |
| C-32 the thirteen defaults accepted "for now", each still open | 16 (OQ-4) | none: no default is changed or closed |
| C-3 secrets | none of the 17 | see check 9 |

## 8. Check 8: the seven open questions (A11 section 12)

Searched before answering: CLARIFICATIONS whole (read, C-1 to C-44; the product owner's 25 answers are C-6 to C-30); `05_readiness-to-build.md` and `03` by `/usr/bin/grep -n -i` for `OQ-4`, `personal`, `quick message`, `F87`, `F82`, `F83`, `shared with me`, `recent`, `translation`, `language`; reports A1, A4, A6 for `Files.ReadWrite.All` and `sharedWithMe`; all reports for `localeFilters|resConfig`. Control: each search returns lines for a word known to be there (`OQ-4` in 15 lines: 7 in `02`, 8 in `03`).

| # | A11's question | Already answered? | Pointer |
|---|---|---|---|
| 1 | Does the OXPd OneDrive tile carry all four places? | **Yes, by the ruling as far as a ruling can:** C-16 is "Full match of everything", and `02:23` reads it as "every journey". The four places are shipped, live behaviour. This is a correction (1, 2, 11), not a question; listing it invites re-opening C-16. Keep it off the list unless someone wants *less* than parity | CLAR C-16; `02:23`, `02:900` |
| 2 | Scopes for Shared with me | **Not answered, but A11 omits evidence that narrows it.** The product documentation lists `Sites.ReadWrite.All` and `User.Read` for OneDrive and `Files.ReadWrite.All` for Teams only (A6:353-355), and `02:703` already quotes that. HP Authentication Manager asks for `openid profile offline_access` always and ten more scopes selectable per device, default all off, among them `Files.ReadWrite.All` and `Sites.ReadWrite.All` (A1:174). So what a customer's token carries is a per-device setting. Not a product-owner question: it is a tenant test (the first-run scope check `02:703` names) | A6:353-355; A1:174; `02:703` |
| 3 | Does each tile keep its own Workpath behaviour for the same libraries (metadata at scan in SharePoint, none in OneDrive)? | **Not answered anywhere.** C-16 points to "yes" (each app matched) but nobody has put the consequence to the product owner: two different scan screens for the same library in one product. Genuinely open | no hit |
| 4 | Is "dead in source and binary" enough to drop Mailflow quick messages without a printer look? | **Covered by an existing open question, not new:** it is a case of OQ-3, "everything Workpath does, no more" (question 3 of `05`, default (a), accepted for now by C-32). `03:182` already makes quick messages conditional ("if F87's condition holds"). Add it to OQ-3 as a named case, not as a new question | `05` question 3 (lines 59-62); CLAR C-32; `03:182`; `02:900` |
| 5 | Teams quick access (F82, F83) rests on the same switch | **Partly answered by this read:** the 1.09.22 binary Teams links returns the constant false (check 2), and it is resolved from the tree. Left: that every route to Teams quick access passes the switch (16 call sites; 7 read). That is a source read for an agent, not a question for the product owner. Note that `02:170-171` state F82 and F83 as unconditional requirements from report A2; if the gating holds they are dead rows of the same kind as F87 | check 2; `02:170`, `02:171` |
| 6 | OQ-4, the personal flavour | **A duplicate:** it is OQ-4 itself (question 4 of `05`, lines 64-68), open on default (a) "out", accepted for now (C-32). A11 adds evidence (rows 64 to 66), not a question | `05:64-68`; CLAR C-32 |
| 7 | Do the shipped apps show their seven translations? | **Not answered.** Related text exists and A11 did not connect it: F42 (`02:102`) says "Six UI languages at parity ... documentation says English only" and, for SharePoint, eight string sets; the plan has WP3.12 "the six languages" (`05:220`). The OneDrive tree has eight string sets (171 English, 167 in each of seven), so **F42's "six" is contradicted for OneDrive exactly as B1760 found for SharePoint, and A11's comparison (section 10) does not list F42.** On the filter itself: `OD/app/build.gradle.kts:39-41` is `androidResources { localeFilters += listOf("en") }`; A11 describes it as keeping English "for third-party libraries". From general knowledge of the Android build (not checked, no network, nothing built) that filter applies to all packaged resources, the app's own included, which would make the shipped OneDrive app English only and agree with "documentation says English only". Open until an APK or a printer is looked at | `02:102`; `05:220`; `OD/app/res/values*/strings.xml` |

**Result: of seven, 3 are genuinely open (3, 7, and the tenant test behind 2); 1 is answered by a ruling (1); 2 are existing open questions (4 = a case of OQ-3; 6 = OQ-4); 1 is agent work, half done here (5).**

## 9. Check 9: secrets in A11 itself

Instrument: a script of mine (Python standard library, run with `-I`) that (a) collects every GUID-shaped identifier from the four source files A11 names as holding one (`OneDriveConstants.java`, `AppConstants.java`, `hpk.xml`, `app/build.gradle.kts`) and counts its occurrences in A11 **without printing it**; (b) takes each quoted value on a `build.gradle.kts` line whose key names a password, a key or a secret, and counts its occurrences in A11, printing the line number and the length only; (c) searches A11 for the shapes of a password assignment, a client secret, a JWT, a PEM block, a Bearer token, a long hex or base64 run. Control for the GUID pattern: it finds the one GUID-shaped string in A11 (line 349, the session scratchpad path) and one in CLARIFICATIONS.

| Question | Result |
|---|---|
| The two application ids A11 says it did not repeat (`ODJ/constants/OneDriveConstants.java:9`, `:10`, 36 characters each) | **0 occurrences in A11.** Confirmed |
| The Workpath UUID (`OD/app/packaging_release/hpk.xml:3`, the same value at `ODJ/constants/AppConstants.java:85`, 36 characters) | **0 occurrences in A11.** Confirmed |
| A fourth identifier A11 does not mention by kind: a client id in `OD/app/build.gradle.kts:37`, `:56`, `:63` (36 characters; A11:263 calls these lines "build fields that carry the `API_K_OD` value or a client id") | 0 occurrences in A11 |
| Shapes: password assignment, `storePassword|keyPassword|client_secret|api key` with a value, JWT, PEM header, Bearer token, hex run of 32 or more | 0 lines each. Two long words found (A11:73, 34 characters; A11:421, 39 characters) are a Gradle task name and a class name |
| GUID-shaped strings in A11 | 1, at A11:349, inside the scratchpad path of the first reader's script (a session id, not an application id) |
| **The quoted values of the two password lines** (`OD/app/build.gradle.kts:45` `storePassword` and `:47` `keyPassword`, 24 characters each, equal to each other, and equal to the quoted value of `:46` `keyAlias`) | **This exact 24-character string occurs in A11 at lines 259 and 425.** A11 did not copy it from the password lines (it masked those by length); the string is in A11 because the same string is used in the tree as the name of something A11 gives as a LOCATION. I do not write the string here. **The same string stands in `02_architecture.md:619` and in seven other reports** (A1:541, A2:447, A3:438, A4:192 and 323, A8:290 and 320, R3:57, 104 and 115), each time as a location |

**Finding for Tuesday (not an error of A11's method; a property of the tree that masking by length cannot see):** in this tree a secret value and a location name are one and the same string, so no report can give that location without also carrying the value. A11's sentence "no secret value is reproduced in this report" (A11:14) is therefore not literally true, and neither is the equivalent sentence in the other reports. C-3 records the product owner's word that the library's keys are old and rotated; whether these two documents and eight reports should name that location differently is Tuesday's call. I changed nothing.

**Tool output of this second read that showed an identifier (declared, not repeated):** (1) a display of `ODJ/constants/AppConstants.java:84-86` that was meant to mask the lines printed the first characters of line 85, which hold the first 22 characters of the Workpath UUID; (2) a display of `OD/app/build.gradle.kts:36-42` printed line 37 unmasked, which holds a client id. Neither is a credential; neither is in this file. No password, key or token value was displayed at any point: the comparison in the table above was made inside the script and only line numbers, lengths and counts were printed.

## 10. ERRORS FOUND IN A11 (each with both pointers)

Ordered by what a writer or a builder would get wrong if it stood.

| # | A11 says (pointer) | The source says (pointer) | Weight |
|---|---|---|---|
| E1 | The call list is complete at 28, 22 live (A11:22, A11:247) | One live call to a Microsoft-hosted address is not listed: the thumbnail image of every file shown, fetched by Picasso outside the Graph client (`ODJ/model/FileItem.java:79-84`; `ODJ/ui/main/base/FileItemViewHolder.java:247-249`; `ODJ/ui/main/MainBaseFragment.java:446`). 29 rows, 23 live | **material for the port** (the server must fetch or proxy these) |
| E2 | C23 and C24 "reachability not traced" (A11:240-241, A11:247, A11:424) | Both traced: C24 is unreferenced (the fragment method `MainBaseFragment.java:1546` has no caller; the name occurs in 3 files, all definition or forwarding); C23's request is issued only for a folder in the list, which only quick-access folder print supplies (`DownloadMultipleFilesTask.java:197-210`; `MainActivity.java:1519`, `:1535`, `:1557`, `:1594-1606`; `QuickAccessFragment.kt:475`, `:483`). So 6 dead or unreferenced, 0 untraced | not an error, a gap now closed; changes the counts |
| E3 | "Five files in `ODJ/taskmanager/` are empty (0 lines each)" (A11:75) | Not empty: 2,599, 888, 137, 227 and 145 bytes, carriage-return line ends, no line feed. They hold the base class of every task. The line total 23,772 undercounts by their 141 lines. Report A8 line 57 has the same error for SharePoint (2,610, 899, 148, 238, 156 bytes) | **material**: a builder told these are empty would not read the task base class |
| E4 | "under `OD/app/src` 176 source files" (A11:75; repeated as "about 40 of 176", A11:28) | 173 under `OD/app/src` (146 `.java`, 27 `.kt`), 174 with the unit test under `OD/app/unitTests` | small |
| E5 | the token is "refreshed once on a 401"; "retries the request once" (A11:22, row 7 at A11:95, A11:214) | `ODJ/auth/SessionAuthenticator.kt:19-59` has no counter and no look at the prior response; a second 401 calls it again. Any limit is the HTTP library's | **material for the port** (the server should set its own limit) |
| E6 | "Eighteen groups are defined in the enum" (A11:297) | 19 constants (`CVL/scan/ScanOptionGroups.java:46-171`) | small |
| E7 | "four live calls read other users' drives" (A11:23, correction 12 at A11:402) | The four are the calls the SharePoint app does not make (A11:251 has it right). Inside a shared folder the item calls on `/drives/{d}/items/{i}` (C14 to C20, C22) reach another user's drive too (`CreateFolderTask.java:93-97`, `RenameFileTask.java:59-64`, `DeleteFilesTask.java:53-58`, `DownloadFileTask.java:80-84`, `DownloadConvertToPdfFileTask.java:79-84`, `UploadFileTask.java:254-258`, `:397-400`, `MainBasePresenter.java:986-991`) | **material for the scope test** |
| E8 | C24's "one caller, `ODJ/ui/main/MainBaseFragment.java:1560`, whose own caller was not read" (A11:241) | `:1560` is inside the fragment's own method (`:1546`); the task is created at `MainBasePresenter.java:431` | small (pointer) |
| E9 | C28 lists three calls of `UploadFileTaskReplace` (A11:245) | a fourth, `POST .../children` at `UploadFileTaskReplace.java:479` | small (dead code) |
| E10 | C9 Recent: paging "all pages" (A11:226) | all pages only when the caller passes `maxCount` 0; otherwise the loop stops at the cap (`GetRecentTask.java:36`, `:69`, `:96-98`) | small; the caller's value was not read by either reader |
| E11 | row 14: three EULA keys roam with the others (A11:102) | `UserPreferencesStore.kt:15` is the name of a local preferences file and `:23-24` are read and written through `getEulaPrefs(context)` (`:206-219`), which is a local `SharedPreferences` file (`:222-223`), not through `updateUserProperty` like the seven others (`:111-201`, `:300`) | small |
| E12 | "The two OneDrive facts A3 does state" followed by three (A11:48); "five placeholders" over a table of eight rows (A11:35-46) | A3:11-12, A3:60, A3:439 | wording |
| E13 | the comparison (section 10) has no row for F42 (languages) | `02:102` says six UI languages; the OneDrive tree has eight string sets (`OD/app/res/values*/strings.xml`: 171 and seven of 167), as A11's own section 3 records (A11:79) | **a missed contradiction**, the same one B1760 corrected for SharePoint |
| E14 | "no secret value is reproduced in this report" (A11:14) | check 9: a 24-character string equal to the values at `OD/app/build.gradle.kts:45` and `:47` stands at A11:259 and A11:425, as a location | structural, shared with `02:619` and seven reports; Tuesday's call |
| E15 | control figures: `WorkpathAccessService.getInstance` "16 lines in Mailflow" (A11:350); `UploadFileTask` "in 5 files" (A11:201) | 17 occurrences in `MF/app/src`; 8 files in `OD/app` | none on any finding |
| E16 | "The same result in OneDrive's 1.09.21 binary and in SharePoint's 1.09.20 binary" and Teams left open (A11:349, A11:356) | confirmed, and the Teams 1.09.22 binary gives the same `03 ac` (check 2) | A11 was right; the Teams half is now further along than A11 says |

No error was found in: the prior-work claim; F87's verdict; the four places; the 16 classes, 11 and 7 groups; the three absences; any of the 25 inventory rows checked; the quotation of any document line a correction replaces.

## 11. READY FOR THE WRITER (the corrections as they should be applied, in order)

Apply in this order (document order, `02` first). "A11 text" = the sentence exactly as A11 section 11 gives it. A writer applies nothing to A11, to A8 or to any other report.

| Order | Document line | Apply |
|---|---|---|
| 1 | `02:7` coverage note | correction 13 **with the changed sentence** of check 7 (counts: 28 listed, 22 live Graph calls, 6 dead or unreferenced, one live image fetch not listed) |
| 2 | `02:91` F31 | correction 6, A11 text |
| 3 | `02:93` F33 | correction 5, A11 text |
| 4 | `02:97` F37 | correction 1, A11 text |
| 5 | after `02:97` | corrections 2, 3, 4 as three new rows, A11 text (row ids to be chosen by the writer; they need the D/S binding and the three platform columns the table has, which A11 does not supply) |
| 6 | `02:98` F38 | correction 7 **with the changed sentence** (do not repeat what the row already says for SharePoint) |
| 7 | `02:101` F41 | correction 8 **with the changed sentence** (six live keys, `quick_access` dead) |
| 8 | `02:175` F87 | correction 9 **with the changed sentence** (fact stated; "not a requirement" by the rule of section 3.1, not as a ruling) |
| 9 | `02:200` F93 | correction 10, A11 text |
| 10 | `02:504` 5.6.3 | correction 11, A11 text, replacing the one OneDrive sentence only; then correction 16's added reason at the OQ-4 sentence of the same line |
| 11 | `02:703` 7.2 | correction 12 **with the changed sentence** |
| 12 | `02:927` R17 | correction 14, A11 text |
| 13 | `03:142` WP0.6 | correction 15, A11 text, then correction 17 **with the changed sentence**, in `03` only |
| 14 | `03:185` WP3.9 | correction 16, A11 text |

**Not in A11's list, found by this read; for Tuesday to decide whether the same writer carries them:**

| Line | What |
|---|---|
| `02:102` F42 | add for OneDrive what B1760 added for SharePoint: the OneDrive source holds eight string sets (English and `de`, `es`, `fr`, `in`, `it`, `pt`, `zh-rTW`); whether the shipped package carries more than English is not established (`OD/app/build.gradle.kts:39-41`) |
| `02:339` C10, or the OneDrive rows | the file list shows a thumbnail per file fetched from an address Graph returns (E1) |
| `02:170`, `02:171` F82, F83 | note that the binary Teams links returns the constant false from the same switch (check 2); the Teams gating is still to be read before either row is built |
| `02:1041`, `02:1067` ("Still owed") | these are dated history entries; a writer adds a new entry and does not edit them |

**A writer must NOT apply:**

1. Correction 17's edit of **report A8** (line 311). Reports are not rewritten; the change goes in `03:142`.
2. Correction 9's bare "not a requirement" as if ruled. Use the changed sentence.
3. Correction 12's "four" and its "no live OneDrive call needs `User.Read`" as written. Nothing is removed from the scope list of `02:703`.
4. Correction 13's "28 Microsoft calls of which 22 live" without the thumbnail fetch and the six dead.
5. Correction 7's two facts a second time in `02:98`.
6. From A11's body, into any document: "five task-manager files are empty" (E3); "176 source files" (E4); "refreshed once on a 401" (E5); "eighteen" scan groups (E6); "two calls not traced" (E2).
7. A11's open questions 1, 4 and 6 as new questions on the master list (check 8): 1 is ruled by C-16; 4 is a case of OQ-3; 6 is OQ-4.

## 12. What was NOT checked

- **Section 3 of A11** beyond the counts in check 3: the library versions, the manifest's twelve activities, the configuration form's 28 fidgets and the 19 scan defaults, the SDK levels. Not checked.
- **Inventory rows not in the sample: 49 of 74.** Rows 2 to 4, 6 to 8, 10 to 12, 14 to 16, 18 to 20, 22 to 24, 26 to 28, 30 to 32, 34 to 36, 38 to 40, 42 to 44, 46 to 48, 50 to 52, 54 to 56, 58 to 60, 62 to 64, 66 were not checked as rows, though the lines behind rows 7, 11, 14, 18, 19, 38, 39, 40, 42, 44, 48, 51, 52, 54, 55, 56, 64 and 66 were read for other checks and none contradicted its row except as listed in section 10.
- **Section 8 of A11 (doubts)**: items 1 and 2 were seen to be accurate while reading the upload task (`UploadFileTask.java:254-277`, `:402-405`); items 3 to 7 not checked as such.
- **A11's section 10 verdicts** for F32, F34, F39, F70, F71, F72, F73, F94, F95, F96: not re-derived. Only the rows a correction rests on (F31, F33, F37, F38, F41, F87, F93, 5.6.3, 7.2) and F42 were compared.
- **Call C25** and everything inside quick access: not read; their state rests on the switch.
- **Whether the Recent screen passes 0 or a cap** to the Recent task (`MainBaseFragment.java:1524`); whether `SendFragment.kt:603-605` (auto new mail and auto reply) sits inside the block the switch guards; whether a disabled print button can be pressed (the one guard on C23).
- **The Teams gating**: 9 of the 16 call sites and the 13 files that name quick access were not read. The Teams binary was read for one method only.
- **A8's rows 65 to 67**: that each rests only on the switch is A8's statement; not re-checked.
- **Binaries**: nothing decompiled. Read as bytes: one method table of one class in five archives, and byte equality of the `scan` and `print` packages across three. The `usermanagement`, `quickaccess`, Workpath and Graph SDK binaries were not opened; statements here about what the Graph SDK or the HTTP library does by default are general knowledge and are marked as such.
- **Resources inside the linked binaries** (strings, layouts): not compared. **The values inside each scan and print option**: not read.
- **Microsoft's documentation, a tenant, a printer, a built package**: none. No network call was made. Every permission statement remains unchecked, as in A11.
- **The NAS library outside the cited paths**: not searched (by rule). The keystore, the OnGuard sources, `OD/notes` and `OD/MIGRATION_NOTES.md`: not opened.
- **The project copy** `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Source_Documents/`: not opened; the trees under `kam_attachments_1120/extracted/` were used (`sp1` and `sp2` compare equal by `diff -rq`).
- **The product owner's 25 answers** were read as CLARIFICATIONS records them (the option label of each tap); the cards' full option texts were not opened.
- **A11 line by line for style or for every pointer**: only the pointers behind the nine checks.
