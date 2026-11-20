# B1760: the SharePoint source read applied to the OXPd architecture, plan and readiness note

Datasec / OXPd, 2026-11-20. One writer, commissioned by Tuesday (brief `2_Project_Files/tuesday/briefs/2026-11-20_B1760_OXPD-SHAREPOINT-SOURCE_COMMISSION.md`). This is a re-commission: the first writer was lost to a power cut at about 10:34 and left nothing in the documents (the six `.pre-B1760` backups were byte-equal to the documents when this pass began: `cmp` return code 0 for all six, checked before the first edit; the backups were not re-created).

## BLUF

1. The SharePoint app's source, supplied by the product owner on 2026-11-20 (C-33), has been read and written up: `analysis/A8_sharepoint-app-and-common-library.md` (326 lines; 73 feature rows, of which 64 live and 9 unreachable; 20 Graph calls, of which 18 live).
2. The three documents are corrected from it: 12 changed places in `02_architecture.md`, 10 in `03_plan-of-attack-and-build.md`, 7 in `05_readiness-to-build.md` (diff hunks against the backups, by program). Seven requirement rows were added (F90 to F96): the count of F rows in document 1 goes from 74 to 81.
3. The source contradicts the documents in 4 places (table 2). 6 statements that rested on "the SharePoint source is not in the library" are now answerable and were updated (table 3).
4. OQ-7 is answered for SharePoint and **not** for the gateway. No other open question was touched.
5. One thing only the product owner can decide was found and is marked "not ruled", not decided: whether the switched-off sensitivity-label feature ships. It is not written as a new numbered question (this pass was told not to touch the other open questions).

## How to read the tables

`SP/` is the root of `CypherSharePoint-main`; `SP-J/` is `SP/app/src/main/java/com/hp/print/cypher/sharepoint/`; `CVL2/` is the root of `CommonValueLibraryCypher-master-2`; `OD/` is the OneDrive tree in the read-only library copy. "A8 row n" is a row of the feature checklist in report A8 section 4.

## 1. SharePoint behaviour that had no requirement row

Each is live in the 4.4.6 source. "Now" says which row carries it.

| # | Behaviour | Source line | Now |
|---|---|---|---|
| N1 | All-sites list by site search, every result page | `SP-J/task/RootSiteTask.java:53-72` | F90 |
| N2 | Recent sites: last 3, per user | `SP-J/ui/main/base/BaseSitesFragment.java:374-393`; `SP-J/constant/AppConstants.java:126` | F90 |
| N3 | Site search with the last 3 terms kept | `SP-J/ui/search/SitesSearchActivity.java:133,183-191` | F90 |
| N4 | Create folder | `SP-J/task/CreateFolderTask.java:107-120` | F91 |
| N5 | Rename, extension kept | `SP-J/task/RenameFileTask.java:33-47,57-72` | F91 |
| N6 | Search inside the open library, last 3 terms kept | `SP-J/task/SearchCallableTask.java:70-79`; `SP-J/ui/search/SearchActivity.java:133,186-192` | F91 |
| N7 | List or grid view with thumbnails | `SP-J/ui/main/base/BaseMainFragment.java:1517-1531` | F91 |
| N8 | File details dialog; refresh | `SP-J/ui/main/base/BaseMainFragment.java:658-659`; `SP-J/ui/main/MainActivity.java:1333-1334` | F91 |
| N9 | Library column values shown per file | `SP-J/task/GetListFolderTask.java:176-204,268-288` | F92 |
| N10 | Column chooser | `SP-J/ui/main/base/BaseMainFragment.java:1782-1806` | F92 |
| N11 | Sort and group by a column | `SP-J/ui/main/base/BaseMainFragment.java:1985-2043` | F92 |
| N12 | Edit the column values of an existing file | `SP-J/task/UpdateColumnValueTask.java:37-51` | F92 |
| N13 | Column types offered (five) and the filter on read-only and hidden columns | `SP-J/ui/main/ColumnHelper.kt:16-36,43-48` | F92, F39 |
| N14 | Write actions only with write permission | `SP-J/ui/main/base/BaseMainPresenter.java:1003-1062`; `SP-J/ui/main/base/BaseMainFragment.java:875-889` | F93 |
| N15 | Printable types; Office conversion limits 80 MB and 40 MB | `SP-J/utils/Utils.java:357-366,394-406` | F94 |
| N16 | Own messages for a conversion time-out and a protected document | `SP-J/task/DownloadConvertToPdfFileTask.kt:93-109` | F94 |
| N17 | Swipe on a file row: direct print | `SP-J/ui/main/base/BaseMainFragment.java:1550-1584` | F94 |
| N18 | Scan never overwrites; duplicate-name message | `SP-J/task/UploadFileTask.java:272,297-298,367` | F95 |
| N19 | A device administrator gets settings only | `SP-J/auth/SessionAccessPolicy.java:15-23`; `SP-J/ui/splash/SplashActivity.java:475-513` | F96 |
| N20 | Scan mail: files attached, five recipients, failure mail | `SP-J/model/EmailSender.java:28-49`; `SP-J/ui/preview/presenter/ScanPreviewPresenter.java:95-166`; `SP/app/src/main/res/values/strings.xml:133` | F38 (amended) |
| N21 | Roaming keys with the prefix `sharepoint.` | `SP-J/storage/UserPreferencesStore.kt:14-21` | F41 (amended) |

Found and deliberately **not** made requirements, because they are implementation of the Android app and not behaviour a user sees, or are covered by the sign-in hub rows: the upload split at 3.5 MB and its retry rule (A8 row 51; the plan's shared Graph layer WP3.8 already owns chunked upload), the in-memory folder cache (A8 row 27), the name-resolution fallback (A8 row 11), the network time limits (A8 row 12), the error-message table by HTTP status (A8 row 63), the token hand-over from HP Authentication Manager (A8 rows 2, 3, 5, 7, 9, 10: the server owns the token, `02_architecture.md` section 6.4). If Tuesday or the product owner wants any of these as a row, A8 has the lines.

## 2. Requirement rows the source contradicts

| # | Row | What the document said | What the source says | Source line | Change |
|---|---|---|---|---|---|
| X1 | F39; §5.6.3 | "metadata entry at scan (4 custom fields)" | One input per editable column, five types, no cap; none on 4.3-inch panels. A search of the two scan-description classes for a limit finds 0 lines (control `forEach`: 2) | `SP-J/ui/preview/BaseScanDescriptionAppFragment.java:41-56,100-105`; `SP-J/ui/main/ColumnHelper.kt:43-48` | F39 corrected; §5.6.3 corrected. The manual's figure is kept as a question (A8 §9 question 4) |
| X2 | F42 | "Six UI languages" | The SharePoint app has eight string sets and a nine-locale configuration form | directories `SP/app/src/main/res/values*` (193 strings English; 174 in six sets; 173 in `zh-rTW`); `SP/app/moc_flie/SharePoint.moc:8-16` | F42 amended for SharePoint only; the six of Mailflow and Teams (report A2) is not disturbed |
| X3 | §5.6.3 | `GetLibraryMetadataTask`, `UpdateLibraryFieldsTask` "in the Workpath source show the pattern" for SharePoint | Those classes are the OneDrive app's (names found only in `OD/`). The SharePoint app uses `GetColumnsTask` and `UpdateColumnValueTask` | `SP-J/task/GetColumnsTask.java:37-43`; `SP-J/task/UpdateColumnValueTask.java:45-51`; name comparison in A8 §7 | §5.6.3 corrected |
| X4 | F74 | "App Guide tutorial at first launch" | In SharePoint the automatic showing is behind the dead switch; the menu entry is live | `SP-J/ui/main/MainActivity.java:655-657,1363-1364` | F74 amended for SharePoint |

Count: 4 contradictions.

Checked and found to **agree** with the source (no change): F38 "through the device's SMTP, default off" (`SP-J/model/SendEmailTask.java:57`; `SP-J/AppConfigHelper.java:141`); F39 "sort; multi-select print and delete" (A8 rows 25, 36, 45); F71 `Scan_<date>_<time>` and `_001` suffixes (`SP-J/utils/Utils.java:131-150`; `SP-J/task/UploadFileTask.java:536-559`); F72 preview and direct print (A8 rows 38, 39); F34 conversion through Graph (`SP-J/task/DownloadConvertToPdfFileTask.kt:53-62`); the §7.2 permission pair for SharePoint (A8 §5.3, with the limit stated there); C19 "five application agents" with SharePoint as its own tile (`SP/packaging_release/hpk.xml:3-4`).

Not compared, because A8 did not read the code that decides them: F31, F32, F33, F70, F73 (scan and print option screens and the preview editor are inside the common library binary).

## 3. B1757 statements that rested on "the SharePoint source is not in the library", now answerable

| # | Where | Statement | Answer | Change |
|---|---|---|---|---|
| S1 | 02 coverage note | "whether it is built from `CypherOneDrive-main` at another revision or from a repository that is not in the library is unknown (OQ-7)" | A repository of its own, `CypherSharePoint-main`; one APK, one HPK, no flavours (`SP/settings.gradle.kts:44`; `SP/app/build.gradle.kts:20,127`; `SP/.github/workflows/release.yml:130-155`) | Update paragraph added to the coverage note; the old sentences kept |
| S2 | 02 P3 | "the separately shipped SharePoint package has no source in the library" | Supplied; version 4.4.6 (`SP/app/build.gradle.kts:45`) | P3 row reworded |
| S3 | 02 R17, R30 | "must be supplied (OQ-7, R30)"; "the shipped SharePoint package has no source in the library" | Supplied and read | Both risk rows carry a B1760 clause; scores untouched |
| S4 | 02 F89; 03 WP0.6 | "Only if a shipped app uses the interface (to be established in WP0.6)" | Established: one implementing app (SharePoint), compiled off (`SP-J/sensitivity/SharePointSensitivityLabelProvider.java:38,56-58`); 0 files in the four other app trees | F89 marked not a requirement; "not ruled" for the product owner |
| S5 | 03 BLUF 4, phase-0 inputs, WP3.4, §6 | "the source that builds the SharePoint app" as an outstanding input; "WP3.4 ... sized on the manual until the SharePoint source is supplied" | Received and read | Four places updated; WP3.4 scope rewritten from the source |
| S6 | 05 question 7, kit items 12 and 13, WP0.6 line, "not verified" list | "Nothing in the library builds it"; "Default: SharePoint is built from the manual alone" | Received and read | Question 7 marked answered in part, with the old text kept below it |

Count: 6.

## 4. Every change, one row each

| Id | Document, place | Change | Why (source line) |
|---|---|---|---|
| B1760 / SP-SOURCE | 02 coverage note (line 7) | Update paragraph: source supplied, where it is kept, what A8 did not read, the gateway still missing | C-33 (`CLARIFICATIONS.md` lines 200-204); `SP/packaging_release/hpk.xml:3-4` |
| B1760 / SP-SOURCE | 02 §2 row P3 | SharePoint named as a second, separate app | `SP/app/build.gradle.kts:20,45` |
| B1760 / SP-SOURCE | 02 §10 R17, R30 | B1760 clause on each | A8 §10 |
| B1760 / F38-MAIL | 02 §3.3 F38 | Attachments, five recipients, failure mail | `SP-J/model/EmailSender.java:28-49`; `strings.xml:133` |
| B1760 / F39-FIELDS | 02 §3.3 F39 | "4 custom fields" removed as a requirement; sort values named; pointer to §3.8 | `SP-J/ui/preview/BaseScanDescriptionAppFragment.java:41-56` |
| B1760 / F41-KEYS | 02 §3.3 F41 | SharePoint's keys named | `SP-J/storage/UserPreferencesStore.kt:14-21` |
| B1760 / F42-LANG | 02 §3.3 F42 | Eight languages for SharePoint | `SP/app/src/main/res/values*` |
| B1760 / F74-GUIDE | 02 §3.7 F74 | First-launch guide dead in SharePoint | `SP-J/ui/main/MainActivity.java:655-657` |
| B1760 / F89-LABELS | 02 §3.7 F89 | Condition settled; not a requirement; not ruled whether it ships | `SP-J/sensitivity/SharePointSensitivityLabelProvider.java:38` |
| B1760 / NEW-ROWS | 02 new §3.8 | F90 to F96 and a closing paragraph on what is not a requirement | table 1 above |
| B1760 / F39-CLASSES | 02 §5.6.3 | Class names corrected; the SharePoint journey from the source; "one module, two tiles" marked as this design's choice | `SP-J/task/GetColumnsTask.java:37-43`; A8 §7 |
| B1760 / PERMS | 02 §7.2 OneDrive/SharePoint row | The source agrees; marked unchecked against Microsoft's documentation | `SP-J/constant/SharepointConstants.java:11`; A8 §5.2 |
| B1760 (entry) | 02 §11 | New change-log entry, 11 numbered items, a "not changed" line and a "still owed" line | n/a |
| B1760 / SP-SOURCE | 03 BLUF 4 | SharePoint source marked supplied; gateway marked still missing | C-33 |
| B1760 / SP-SOURCE | 03 §3 phase 0 inputs | The SharePoint bullet marked received | C-33 |
| B1760 / PHASE3-ORDER | 03 §3 phase 3 order item 2 | No longer waits on the source | A8 |
| B1760 / E3.1 | 03 §3 phase 3 exit | F90-F96 counted | 02 §3.8 |
| B1760 / WP0.6 | 03 §4 WP0.6 | SharePoint half done; what is left | A8 §10 |
| B1760 / WP3.4 | 03 §4 WP3.4 | Scope from the source; F39, F90-F96 | A8 §4, §5.2 |
| B1760 / SP-SOURCE | 03 §6 blocker line | Marked no longer a blocker | C-33 |
| B1760 / SP-SOURCE | 03 §8.3 lead sentence and OQ-7 row | "answered in part": SharePoint yes, gateway no | C-33 |
| B1760 (entry) | 03 §9 | New change-log entry, 5 numbered items | n/a |
| B1760 | 05 BLUF 2 | Update bullet | C-33 |
| B1760 | 05 question 7 | Answered in part; the label feature named as the product owner's to decide; old text kept | A8 §1, §9 |
| B1760 | 05 question 7 "Blocks" line | No longer blocks | A8 |
| B1760 | 05 kit items 12, 13 | 12 still needed; 13 received | C-33 |
| B1760 | 05 "what can start" WP0.6 line | SharePoint half done | A8 |
| B1760 | 05 "not verified" list | SharePoint entry marked; one new point on the limits of the read | A8 §10 |
| B1760 | 05 last lines | Pointer to this file and to A8 | n/a |

## 5. Counts (by program)

- A8: 326 lines; 10 sections; 73 feature rows (`grep` for table rows that start with a number), 64 marked LIVE; 20 Graph rows (G1 to G20), 18 live.
- `02_architecture.md`: 951 → 985 lines; 12 diff hunks against `02_architecture.md.pre-B1760`; 25 lines name B1760; F rows 74 → 81.
- `03_plan-of-attack-and-build.md`: 438 → 450 lines; 10 hunks; 15 lines name B1760.
- `05_readiness-to-build.md`: 174 → 184 lines; 7 hunks.
- SharePoint tree: 553 files; 220 source files under `app/src/main/java`, 31,158 lines; 13 activities; 28 configuration fidgets. `diff -rq` of the two SharePoint archives: 0 differing files.
- Common library: 798 files in each copy; `diff -rq` between the library copy (1.09.22) and the one supplied (1.09.23): 2 differing files, none present on one side only.

The line and hunk counts were taken again after the last edit and after the PDFs were rendered; they are the final figures. No hunk in any of the three documents is a pure deletion (0 of 12, 0 of 10, 0 of 7). The three PDFs were re-rendered with `md2pdf.sh` (38, 17 and 6 pages); the earlier PDFs are kept as `.pdf.pre-B1760`.

## 6. Not done, and not verified

- **Nothing was built or run.** No Gradle task, no test, no script from either tree.
- **About 55 of the SharePoint app's 220 source files were read** (about 30 whole, about 25 by method list, line range or search). The rest, and all 157 XML resources apart from counts, were not opened. The full list is A8 section 10.
- **The OneDrive tree was not read** (file names and four searches only). Requirement F37 and the OneDrive parts of §5.6.3 still rest on the manual.
- **The common library was not re-read**; the 2-file diff is the reason report A4 is taken to stand. The library binary the SharePoint app links (1.09.20) was not decompiled.
- **Never opened:** the keystore at the SharePoint tree root; the OnGuardLib native sources.
- **No Graph permission was checked against Microsoft's documentation** (no network).
- **`CLARIFICATIONS.md` was not edited** (outside this pass). C-33 is quoted from it.
- **No new numbered open question was written.** Two candidates are in A8 section 9 (questions 1 and 2) for Tuesday to put to the product owner if she chooses.
- **The gateway:** nothing was learned. Neither tree is the gateway.

## 7. Secrets

Locations only are in A8 section 8. One client identifier (an application id) appeared in a tool output during the read and is not repeated anywhere. The two password lines of `SP/app/build.gradle.kts` (24 and 26) were masked before display. No keystore was opened.
