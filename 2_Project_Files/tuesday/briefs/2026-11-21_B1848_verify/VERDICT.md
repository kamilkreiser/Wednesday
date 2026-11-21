GATE B1848: GO WITH FINDINGS @ manifest d4c6f78e

# B1848 VERDICT: independent review of the seven wave-3 documents (kit B1842, OXPd 2, lane K)

Reviewer: Sonnet 5.5, in-session G2 reader for Tuesday. 2026-11-21. Wrote only into this folder and `/private/tmp/b1848-gate/`. No project file edited, no Jira, no message, `Source_Documents/` and every key folder untouched. Nothing security-shaped was found (no secret value, no key path, no person's name).

## BLUF
- **GO WITH FINDINGS.** Integrity holds (manifest and all seven documents equal their rows); whose-words holds (0 attributions without a `CL`/`03` quote; 0 names, control fires); secrets and key folders hold (gitleaks rc 0 twice, control rc 1; 0 key paths).
- Item 2 found **0 ABSENT and 0 NEIGHBOUR** on the register (D1) and the two design drafts (WP0.8 map, WP0.10 note). It found 4 WEAKER cells and 1 TWO-CLAIMS cell in D1, 12 WEAKER and 1 TWO-CLAIMS in the WP0.8 map, 2 WEAKER in the WP0.10 note, and 6 of 44 sampled K1-K4 cells not SUPPORTS (3 WEAKER, 3 TWO-CLAIMS; 0 NEIGHBOUR, 0 ABSENT). All are the grade's "findings" class; none changes an answer a document gives.
- The register has 21 rows, 0 APPROVED, every row names a design line it differs from and an authority; the one row where its status could mislead (DEV-09, "RULED" while `02` says "Not ruled") is flagged by the register itself as its QUESTION 1.
- **The main process finding is about the instrument, not the seat:** the EXCERPTS file clips every source line at about 310 characters (255 of 2158 excerpt lines are clipped; 133 of the register's 221). Most of the register's cites are to `03:108`, whose supporting words sit past character 310, so the file alone cannot support an N1 re-read of D1. I read the clipped lines in the project documents themselves (`02`, `03`, `CL`, `A1`, `A2`, `C1`, `C2`, `D1`, `D2`, `A9`, all under `Design/` and `Analysis/`, not `Source_Documents/`) and recorded the result. Clipped `LIB:` and `SRC:` lines I could not open (path rule); those cells are judged from the excerpt alone and the 9 clipped `SRC:` lines are JSON description strings that no claim rests on.

## Item 1: INTEGRITY (holds)
| check | result |
|---|---|
| `shasum -a 256` of the manifest | `d4c6f78e65b79d61878792ba8b00a7ae9495f66d14d3a9b2e7da8aca6b206baf` = the commission's value |
| each document: sha256, bytes, lines vs its manifest row | 7 of 7 equal on all three (sha256 True, bytes True, lines True per row) |
| comparator control | a scratch copy with one byte appended: sha, bytes and lines all differ (the check can fail) |
| my scratch copy (used for items 3 to 6) | 7 of 7 sha256 equal to the manifest, 140682 bytes = the sum of the manifest bytes |
HOW: `shasum -a 256 <manifest>`; `python3 -I` reading `Briefs/2026-11-21_B1842_MANIFEST.txt` and recomputing `hashlib.sha256`, `len`, `count(b'\n')` per row.

## Item 2: N1 and N2 (does the citation support the claim)
**Instrument.** A cell here is a table cell, or a non-table claim line, that holds at least one backtick citation (a naive ` | ` splitter; a pipe inside backticks splits one cell in two, so cell counts are approximate; citation counts are exact). Citations were paired with the EXCERPTS file by program (`/private/tmp/b1848-gate/dump.py`: key = document file, line, citation string), 875 excerpts for 875 claim-line citations, 0 claim-line citations without an excerpt, 0 excerpts without a citation, 0 empty excerpts (control: a planted citation with no excerpt is reported). 33 further citations sit in `>` scope-note lines or `###` headings (doccheck does not excerpt them): 15 scope-note citations are the plan rows the scope sentence names; 18 are K4 group headings "listed at ScanViewItems.java:31" etc., which I verified by program against the excerpt of the range `ScanViewItems.java:31-41` and `PrintViewItems.java:28-34` (18 of 18: line number and group name both match).
**Method.** Every cell of D1, of the WP0.8 map (D2) and of the WP0.10 note (D7) was read against its excerpt, and against the source line itself where the excerpt is clipped. For the 20 mechanical WP0.8 rows (column name, type, bicep line and stream-declaration line) and the 14 SAME NAME rows (property name at the OXPd 2 line) I also ran a program: 20 of 20 and 14 of 14 matched, 0 failures. K1 to K4: **seed 1848**, `random.seed(1848); random.sample(pool, 44)` over the 310 cited cells of K1 to K4 in file order (K1 45, K2 87, K3 25, K4 153); the 44 sampled cells are printed below.
**Counts per document (CELLS; verdict closed list SUPPORTS / WEAKER / NEIGHBOUR / ABSENT / TWO-CLAIMS):**
| document | counts |
|---|---|
| D1 register | SUPPORTS 137, WEAKER 4, NEIGHBOUR 0, ABSENT 0, TWO-CLAIMS 1 (cells 142); 221 citations |
| D2 WP0.8 map | SUPPORTS 117, WEAKER 12, NEIGHBOUR 0, ABSENT 0, TWO-CLAIMS 1 (cells 130); 180 citations on claim lines (181 per doccheck, one sits in a scope note) |
| D7 WP0.10 note | SUPPORTS 60, WEAKER 2, NEIGHBOUR 0, ABSENT 0, TWO-CLAIMS 0 (cells 62); 86 citations |
| K1 (sample 5 of 45) | SUPPORTS 2, WEAKER 1, NEIGHBOUR 0, ABSENT 0, TWO-CLAIMS 2 (cells 5) |
| K2 (sample 12 of 87) | SUPPORTS 9, WEAKER 2, NEIGHBOUR 0, ABSENT 0, TWO-CLAIMS 1 (cells 12) |
| K3 (sample 5 of 25) | SUPPORTS 5, WEAKER 0, NEIGHBOUR 0, ABSENT 0, TWO-CLAIMS 0 (cells 5) |
| K4 (sample 22 of 153) | SUPPORTS 22, WEAKER 0, NEIGHBOUR 0, ABSENT 0, TWO-CLAIMS 0 (cells 22) |
SUPPORTS cells whose excerpt was clipped and whose support I read in the source document instead: the `03:108` cells (53 of D1's 142, by program), `02:683`, `02:684`, `02:175`, `02:177`, `02:640`, `02:752`, `02:167`, `03:378`, `03:654`, `03:395`, `03:396`, `03:214`, `A1:403` (supplies sent only with new jobs; poll every minute: present at the end of the line), `C2:49` ("Consequence ... a card swipe while a walk-up user is inside a native menu cannot sign in"), `D1:296`, `D1:519`.

### Every cell that is not SUPPORTS in D1, the WP0.8 map and the WP0.10 note
| doc | cell | citation | verdict | reason | cell text (60 chars) |
|---|---|---|---|---|---|
| D1 | L25 c3 | 02:915 | WEAKER | 02:915 lists (a) device-held and (b) cloud/server-held as the options; it does not say which one Workpath does | device-held jobs is option (a) of D16 (02:915) |
| D1 | L34 c3 | D1:519, D1:296 | WEAKER | D1:296 gives MFUG p.31-32 and p.33; the p.31-34 form is on D1:519 (also cited), not on D1:296 | app settings at the printer under the Administrator Access C |
| D1 | L39 c4 | 03:183 | WEAKER | 03:183 says "quick messages (if F87's condition holds)"; the printer-look wording is 03:108 | quick messages are not built unless a printer look shows the |
| D1 | L39 c6 | 03:108 | TWO-CLAIMS | status "F87 dead at source (03:108)" and "D3 reads the compose lines" share one citation; the second is a pointer to K1 with no line | NOT A DEVIATION: F87 is dead at source (03:108); D3 (PD:Anal |
| D1 | L43 c0 | 03:224 | WEAKER | 03:224 names the tracking and the weekly gap report; "they come when tests exist" is not on that line | The function-table tracking and the weekly gap report of WP6 |
| D2 | L12 c0 | ReportingClient.kt:13 | TWO-CLAIMS | one cite (ReportingClient.kt:13, an import) for "imported from the SDK" and for "no source file in LIB defines it" (kit measurement, not marked RELAYED) | The field list of StatisticsJobData is UNMEASURED: the class |
| D2 | L25 c2 | statisticsServiceTarget.openapi.json:2001 | WEAKER | absence of extendedUserInfo is cited to the userInfo line (2001); the absence itself rests on the L10 set comparison (1835-2018) | no property of this name; statisticsData has userInfo (SRC:O |
| D2 | L25 c4 | statisticsServiceTarget.openapi.json:2001 | WEAKER | state cites the userInfo line (2001); that line does not show extendedUserInfo is absent | NO SOURCE FIELD (SRC:OXPd2-SDK-Beta-10-20260416/specificatio |
| D2 | L34 c2 | statisticsServiceTarget.openapi.json:1963, statisticsServiceTarget.openapi.json:1968, statisticsServiceTarget.openapi.json:1720 | WEAKER | excerpt of :1720 is only `"type": "integer"`; that it belongs to the sequenceNumber schema (:1968 is the $ref) is not in the excerpt | resourceId (SRC:OXPd2-SDK-Beta-10-20260416/specifications/co |
| D2 | L34 c4 | statisticsServiceTarget.openapi.json:1963, main.bicep:399, statisticsServiceTarget.openapi.json:1720 | WEAKER | same: the integer type is cited at :1720 with no schema name in the excerpt | SAME NAME (SRC:OXPd2-SDK-Beta-10-20260416/specifications/com |
| D2 | L36 c2 | statisticsServiceTarget.openapi.json:1835-1842 | WEAKER | absence cited to lines 1835-1842 (the head before the properties start at 1843); properties run to 2018 | no deviceInfo property in statisticsData (SRC:OXPd2-SDK-Beta |
| D2 | L36 c4 | ReportingClient.kt:76, statisticsServiceTarget.openapi.json:1835-1842 | WEAKER | same range 1835-1842 offered for "statisticsData has no such field" | SERVER BUILDS IT (DERIVED: Workpath builds it on the device, |
| D2 | L45 c2 | openApi.bundle.json:1444, openApi.bundle.json:2535 | WEAKER | 2535 is the head of schema `supply`; the excerpt does not show that each suppliesList item uses it | suppliesList of suppliesInfo (SRC:OXPd2-SDK-Beta-10-20260416 |
| D2 | L46 c1 | ReportingClient.kt:153, StatsRepository.kt:98-114 | WEAKER | excerpt is `jobObj.add("deviceInfo", infoJson)`; that this object is the supply payload is not in the excerpt (LIB not opened) | a deviceInfo object added to the one supply payload (LIB:HPA |
| D2 | L46 c2 | openApi.bundle.json:1420 | WEAKER | absence cited to the head line 1420 (`"suppliesInfo": {`) only | no device block in suppliesInfo (SRC:OXPd2-SDK-Beta-10-20260 |
| D2 | L46 c4 | openApi.bundle.json:1420 | WEAKER | same head-line citation for "no source field" | SERVER BUILDS IT (DERIVED: no source field, SRC:OXPd2-SDK-Be |
| D2 | L61 c0 | ReportingClient.kt:13, 03:145 | WEAKER | the import line shows the SDK package; "lives only in the SDK binary" is not shown by it | QUESTION 1 (Tuesday, then the product owner through S11): th |
| D2 | L63 c0 | main.bicep:399, statisticsServiceTarget.openapi.json:1720, 03:64 | WEAKER | same as L34: :1720 is a bare integer type line | QUESTION 3 (Tuesday): resourceId is string in the template ( |
| D7 | L65 c0 | SetGroupPasswordDialogContent.xaml:1, UI-Regression-Test-Catalogue.md:2944 | WEAKER | one dialog file at line 1 shows the file exists; "21 files are controls, dialogs and resources" is not shown | The other 21 .xaml files are controls, dialogs and resources |
| D7 | L66 c0 | UI-Regression-Test-Catalogue.md:60 | WEAKER | the Total row (:60) gives 40 and 115; "9 modules" is the count of rows :51-:59, not on :60 | The catalogue counts 40 features and 115 test cases across 9 |

(The full table of all 378 judged cells, with the SUPPORTS rows, is `N1_TABLE.md` in this folder.)

### The 44 sampled cells of K1 to K4 (seed 1848), all printed
| doc | cell | citation | verdict | reason | cell text (60 chars) |
|---|---|---|---|---|---|
| K1 | L18 c1 | SendFragment.kt:349 | WEAKER | excerpt shows the call `initFab()` at 349; "in onViewCreated" is not in the excerpt | LIB:MailFlow-main/app/src/main/java/com/hp/print/mailflowas/ |
| K1 | L30 c1 | SendFragment.kt:608-614 | SUPPORTS | excerpt shows the cited line; read | LIB:MailFlow-main/app/src/main/java/com/hp/print/mailflowas/ |
| K1 | L34 c1 | SendFragment.kt:117 | TWO-CLAIMS | one cite (:117) for "declared false" and for "occurs 4 times, no other line sets it" | LIB:MailFlow-main/app/src/main/java/com/hp/print/mailflowas/ |
| K1 | L41 c1 | MainActivity.kt:389-393 | SUPPORTS | excerpt shows the cited line; read | LIB:MailFlow-main/app/src/main/java/com/hp/print/mailflowas/ |
| K1 | L42 c2 | MainActivity.kt:405-410 | TWO-CLAIMS | the cell states the guard ("only when the switch is true", range cited in the previous cell) and the button target (405-410); only the second is cited here | the quick-messages group of the menu is shown only when the  |
| K2 | L9 c0 | MainActivity.kt:218, MainActivity.kt:230, MainActivity.kt:240 | TWO-CLAIMS | three cites cover the start-up entry only; "eight references ... only when the switch is true" carries none in this cell (they are in table 1) | Answer for F82 (quick access): UNDETERMINED. The eight refer |
| K2 | L11 c0 | QuickAccessFragment.kt:709-712, QuickAccessFragment.kt:355-356, FilesFragment.kt:761-762 | WEAKER | 761-762 is an isPrintSupport test; the switch test is at 747 (not cited here); "the only way to pin" is an absolute with no count or control | Answer for F83 (folder print): UNDETERMINED, for the same re |
| K2 | L19 c1 | AppGuideActivity.kt:93 | SUPPORTS | guard line / block end shown by the excerpts | LIB:Teams-main/app/src/main/java/com/hp/print/teams/ui/appgu |
| K2 | L19 c2 | AppGuideActivity.kt:93, AppGuideActivity.kt:96 | SUPPORTS | guard line / block end shown by the excerpts | LIB:Teams-main/app/src/main/java/com/hp/print/teams/ui/appgu |
| K2 | L20 c1 | AppGuideActivity.kt:101 | SUPPORTS | excerpt shows the cited line; read | LIB:Teams-main/app/src/main/java/com/hp/print/teams/ui/appgu |
| K2 | L27 c1 | MainActivity.kt:707 | SUPPORTS | excerpt shows the cited line; read | LIB:Teams-main/app/src/main/java/com/hp/print/teams/ui/main/ |
| K2 | L31 c3 | FilesFragment.kt:747-774 | WEAKER | 747-774 shows the pin options under the switch; "for a folder" is not in the excerpt | for a folder: shows "pin to quick scan" and "pin to quick pr |
| K2 | L45 c2 | FilesFragment.kt:747, FilesFragment.kt:792, RecentFragment.kt:289 | SUPPORTS | excerpt shows the cited line; read | yes (LIB:Teams-main/app/src/main/java/com/hp/print/teams/ui/ |
| K2 | L46 c1 | MainActivity.kt:260-261 | SUPPORTS | excerpt shows the cited line; read | restore of a saved quick-access view after the activity is r |
| K2 | L46 c2 | MainActivity.kt:244 | SUPPORTS | excerpt shows the cited line; read | DERIVED: restores a state reached earlier, not a new entry ( |
| K2 | L53 c0 | QuickAccess.kt:26, MainActivity.kt:699-712, FilesFragment.kt:747 | SUPPORTS | excerpt shows the cited line; read | DERIVED from tables 1 and 2: on a fresh install, with the sw |
| K2 | L55 c0 | B1769:51 | SUPPORTS | excerpt shows the cited line; read | Context only (report, not source): the second review's secti |
| K3 | L9 c0 | 03:146 | SUPPORTS | excerpt shows the cited line; read | WP0.9 requires the licence terms of each candidate to be rea |
| K3 | L11 c0 | 2026-11-21_B1842_SEAT-X24_oxpd2-wave3-documents.md:169 | SUPPORTS | excerpt shows the cited line; read | No licence text of any candidate is in the project folder or |
| K3 | L21 c1 | 02:176, 03:65 | SUPPORTS | excerpt shows the cited line; read | 02:176; S12 tests "a mail body with inline images" (03:65) |
| K3 | L22 c1 | 03:65 | SUPPORTS | excerpt shows the cited line; read | 03:65 |
| K3 | L44 c0 | 02:917 | SUPPORTS | excerpt shows the cited line; read | QUESTION 2 (the product owner, D18): which converter ships?  |
| K4 | L33 c2 | ScanOriginalDuplexOption.java:80-82 | SUPPORTS | excerpt shows the cited line; read | NONE, BOOK, FLIP (SRC:CommonValueLibraryCypher-master-2/comm |
| K4 | L39 c1 | ScanOptionGroups.java:94 | SUPPORTS | excerpt shows the cited line; read | ScanColorModeOption (SRC:CommonValueLibraryCypher-master-2/c |
| K4 | L45 c3 | ScanOriginalSizeOption.java:29 | SUPPORTS | excerpt shows the cited line; read | SIZE_AUTO (SRC:CommonValueLibraryCypher-master-2/commonvalua |
| K4 | L51 c2 | ScanOrientationOption.java:86-88 | SUPPORTS | excerpt shows the cited line; read | AUTO_DETECT, PORTRAIT, LANDSCAPE (SRC:CommonValueLibraryCyph |
| K4 | L58 c2 | ScanImageAdjustmentOption.java:191-199 | SUPPORTS | excerpt shows the cited line; read | darkness: LEVEL_0 to LEVEL_8 (SRC:CommonValueLibraryCypher-m |
| K4 | L58 c3 | ScanImageAdjustmentOption.java:29 | SUPPORTS | excerpt shows the cited line; read | LEVEL_4 (SRC:CommonValueLibraryCypher-master-2/commonvaluabl |
| K4 | L59 c4 | ScanViewItems.java:94-98 | SUPPORTS | excerpt shows the cited line; read | removed and disabled when the device does not offer it (SRC: |
| K4 | L60 c4 | ScanViewItems.java:94-98 | SUPPORTS | excerpt shows the cited line; read | removed and disabled when the device does not offer it (SRC: |
| K4 | L66 c1 | ScanOptionGroups.java:127 | SUPPORTS | excerpt shows the cited line; read | ScanTextPhotoOptimizationOption (SRC:CommonValueLibraryCyphe |
| K4 | L72 c4 | ScanViewItems.java:100-104 | SUPPORTS | excerpt shows the cited line; read | removed and disabled when the device does not offer it (SRC: |
| K4 | L99 c3 | PrintCopiesOption.java:24 | SUPPORTS | excerpt shows the cited line; read | 1 (SRC:CommonValueLibraryCypher-master-2/commonvaluablelibra |
| K4 | L105 c1 | PrintOptionGroups.java:86 | SUPPORTS | excerpt shows the cited line; read | PrintDuplexOption (SRC:CommonValueLibraryCypher-master-2/com |
| K4 | L105 c4 | PrintViewItems.java:53-57 | SUPPORTS | excerpt shows the cited line; read | removed and disabled when the device does not offer it (SRC: |
| K4 | L124 c1 | PrintOptionGroups.java:110 | SUPPORTS | excerpt shows the cited line; read | PrintPaperSelectionOption (SRC:CommonValueLibraryCypher-mast |
| K4 | L132 c4 | PrintViewItems.java:86-90 | SUPPORTS | excerpt shows the cited line; read | removed and disabled when the device does not offer it (SRC: |
| K4 | L144 c2 | 03:188 | SUPPORTS | excerpt shows the cited line; read | F31 scan option set, PDF password dialog (03:188) |
| K4 | L147 c2 | 02:92 | SUPPORTS | excerpt shows the cited line; read | F32 (02:92) |
| K4 | L148 c0 | PrintPreviewFragment.java:51 | SUPPORTS | excerpt shows the cited line; read | PrintPreviewFragment (SRC:CommonValueLibraryCypher-master-2/ |
| K4 | L149 c0 | PdfPasswordHandler.kt:27 | SUPPORTS | excerpt shows the cited line; read | PdfPasswordHandler (SRC:CommonValueLibraryCypher-master-2/co |
| K4 | L149 c2 | 02:161 | SUPPORTS | excerpt shows the cited line; read | F73 (02:161) |
| K4 | L159 c0 | 02:161, 03:188 | SUPPORTS | excerpt shows the cited line; read | QUESTION 1 (Tuesday): F73's design asks who asks for the pas |
| K4 | L166 c0 | 03:188 | SUPPORTS | excerpt shows the cited line; read | UNMEASURED: the values inside the 1.09.20 to 1.09.22 binarie |

Two notes on the verdicts. (a) I counted `TWO-CLAIMS` where one cell makes two claims and cites only one, per the kit's rule; none is a wrong claim. (b) The WP0.8 absence cells (`no deviceInfo property`, `no device block in suppliesInfo`, `no property of this name`) are true on the kit's own measurement (14 names in both, 3 and 2 on one side; I did not re-measure them: LIB/SRC not opened) but are cited to a head line, so the excerpt cannot show them; the L10 cell that does cite the full range 1835-2018 is SUPPORTS.

## Item 3: whose words (N5, N11) (holds)
| check | result | control |
|---|---|---|
| strict kit regex `product owner (has )?(decided|ruled|approved|chose|wants)` over the 7 documents | 0 hits | planted line `the product owner approved X`: 1 |
| broad regex (product owner / he / his / Kam within 60 characters of decid-, rul-, approv-, chose, want, agree, accept, answer, confirm, said, asked, settl-, prefer, expect) | 5 hits, all read: D1 line 9 (a requirement that class 3 waits for approval, `03:108`), D1 line 48 (a QUESTION), K3 line 44 (a QUESTION), D7 OP-3 and OP-5 (ANSWERED, quoted, `03:397` and `03:399`) | n/a |
| lines with ruled / ruling / answered / decided / approved that carry a `CL` or `03` citation | 20 | |
| lines with those words and NO `CL`/`03` citation | 2, both scope notes defining the status list and the classes (no decision attributed) | |
| names (kit's ban list from `doccheck.py` line 45: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite; case-sensitive, underscore-aware) | 0 in each of 7 documents | planted `Kam` fires 1; planted `x_by_Kam_y` fires 1; `Kamera` fires 0 |
Excerpts behind the attributions: `CL:` lines are "his tap verbatim from the board export" (CL says so at the heading); `03:397`, `03:399`, `03:400` carry "ANSWERED: ... ([PO A17]/[PO A15]/[PO A16])" quoting him. No choice of Tuesday's or the seat's is written as his. The one place a status could read as his decision when the source is silent is DEV-09 (see item 6). N11 limit: a source identifier on the ban list (`Inch`) cannot be spelled under the check; D4 and D6 describe those identifiers without spelling them (the seat's STATUS says so; I found 0 hits).
HOW: `/usr/bin/grep -n -i -E` over my scratch copy `/private/tmp/b1848-gate/copy/`; `python3 -I` regex rebuilt from the `BAN` list read from `doccheck.py` (read, not run).

## Item 4: secrets and key folders (N6, N7) (holds)
| check | result |
|---|---|
| gitleaks 8.30.1, control FIRST: a folder with one token built by program from two halves (never printed) | rc 1, "leaks found" 1 |
| `gitleaks dir` over the scratch copy of the 7 documents, options `--no-banner --redact --ignore-gitleaks-allow --exit-code 1` | rc 0, "no leaks found", 140682 bytes scanned |
| same under neutral names `1.txt` to `7.txt` | rc 0, "no leaks found", 140682 bytes |
| extra program scan: password/secret/token assignments, hex runs of 32+ (sha256 pins removed), e-mail addresses | 0 / 0 / 0 in all 7 (control strings each fire 1) |
| key folders and names in cited paths (`certificates`, `keys`, `*.key`, `*.pem`, `*.jks`, `*.p12`, `*.pfx`, `*.keystore`, `keystore`, `3_Access_Keys`, `4_Credentials`) | 0 of 75 distinct cited LIB/SRC/PD paths; 0 other hits in text except one scope note in K2 (line 6) that says a keystore-like name was not opened (no name given) |
| cited paths against the files `02:648-662` names as holding secrets (config.properties, notes, moc_file, `*.cfg`, CardValidator, Encryptor, Gotenberg request classes, EncryptionUtils, MicrosoftAuthService, generateHPExtSDK, build.gradle, hpam keys, AzureUserModel, the diagnostics-password line) | 0 hits (control: a path ending Encryptor.kt matches 1) |
`A2:218` is cited once and its text says only that the class "contains hardcoded credentials: see section 9" (no value; verified at the source line).

## Item 5: N12 absolutes
132 lines in the seven documents hold one of no/none/never/every/all/always/only/nothing (matched outside backticks; per document D1 23, WP0.8 31, K1 13, K2 24, K3 10, K4 14, WP0.10 17). Most are quoted source ("nothing pushed to either tool's repository"), status words ("NOT A DEVIATION", "none needed"), or scope notes ("Nothing here is the product owner's decision; every QUESTION below"). Those that state a finding and do **not** carry count, frame and a control in the document:
| doc | line | the absolute | what is missing |
|---|---|---|---|
| D1 | 5 | "no row carries" APPROVED | no count or control in the document (mine: 0 of 21 rows, control NEEDS APPROVAL 6 rows) |
| WP0.8 | 12 | "no source file in `LIB` defines it" | relayed from the kit, not marked RELAYED, no count or control |
| WP0.8 | 25, 36, 46 | "no property of this name", "no `deviceInfo` property", "no device block in `suppliesInfo`" | cited to a line that cannot show an absence; no count |
| WP0.8 | 37, 38 | "no column `sequenceNumber`/`userInfo`" | frame is right (lines 384-402, 17 columns counted in the BLUF) but no control |
| WP0.8 | 61 | "lives only in the Workpath SDK binary" | no frame, no control |
| K1 | 12 | "the auto lines are never reached" | DERIVED from three cited lines; no count or control |
| K1 | 41, 43, 44 | "none found at the lines read" | frame stated and marked UNMEASURED; no count (minor) |
| K2 | 11 | "the only way to pin a folder for print" | no count, frame or control |
| K2 | 40 | "always hidden on other screens" | no count or control |
| K2 | 43, 44, 48 | "reachable only from ...", "added only inside the switch block", "reached only through the quick-access screen" | DERIVED; no count or control (K2 line 50 gives `firstScreen` 7 lines, control `isFirstPinned` 6, which backs line 10 only) |
| K4 | 12 | "colour dropout is removed ... on every device" | no count or control |
| K4 | 23 to 27 | "disabled, never removed" (five rows) | holds for lines 46-53 as cited; "never" has no wider frame or control |
| K4 | 156 | "no TIFF or MTIFF password handling was found" | count (7 files) and frame given; the control and the file list are "in STATUS", outside the document |
| K4 | 5 | "0 pruned paths" | no control |
| WP0.10 | 65 | the catalogue "gives them no section of their own" | rests on heading counts with no control |
Backed and fine: K1 line 34 (4 occurrences, control `isAutoReply` 1), K2 line 10 (backed by line 50), K3 line 10 (counts over 38 files, control `converter` 20, cache 0 of 64 with control `xunit` 10; the frame is 7 searched words, which cannot rule out other candidate names), K4 line 5 (`cmp` 0 of 134 with the library side held at 69, 61, 4).
HOW: `re` over the scratch copy, words outside backticks; each line read.

## Item 6: the deviation register (D1)
| check | result | control |
|---|---|---|
| rows `^\| DEV-` | 21; each has all 8 columns non-empty | |
| class: 1 (eleven, one struck), 2 (two), 3 (one), U (five), none (two) | equals the BLUF's counts | |
| statuses | RULED 10, NEEDS APPROVAL 6, WAITS SPIKE 2, REMOVED 1, NOT A DEVIATION 2: all on the closed list | |
| the word APPROVED | 0 in the 21 rows; 1 in the file (line 5, "is not on the list and no row carries it") | planted APPROVED row fires 1; NEEDS APPROVAL rows 6 |
| each row names a requirement row (F, W, D or A6 id) with a `02`/`03`/`D1` cite, and an authority (C-entry `CL` line, plan line, or the `02` row) | 21 of 21 | |
| class 3 and class U rows all NEEDS APPROVAL, pointing at OQ-6 `03:378` | 6 of 6 | |
Points for a reader, none a defect of the register: (i) DEV-09 is "RULED (CL:116) as to C-19" while `02:185` calls the row "Not ruled: open question OQ-5"; the register says so in the cell and as QUESTION 1; the status word RULED in a column read at a glance could mislead, and the closed list has no "ruled in part". (ii) DEV-12 and DEV-13 are class 2 with WAITS SPIKE; DEV-13's Workpath behaviour is UNMEASURED (the register says so). (iii) The labels D1/D2/D3 name both the seat's documents and the analysis reports (the register cites report `D1:519` and calls the K1 read "D3"); a reader cannot tell which D1 is meant.

## Item 7: fit for what Kam will read
1. **WP0.10 note: readable as it stands in its BLUF and OP-1 to OP-6 question lines** (plain English with defaults and ANSWERED marks); the operation, type and screen tables are for engineers; a reader can stop after the question lines.
2. **K3 (converter licences): readable as it stands**: 53 lines, a plain checklist and one named candidate; only the labels D18, S12, C-17 need a gloss.
3. **The register: needs a records pass first**: the BLUF and the six QUESTION lines read, but the table is codes (DEV-nn, C-nn, F/W/D ids, file:line) with no plain sentence per row saying what changes for the user.
4. **K1, K2 (Mailflow, Teams): need a records pass**: the answers (INSIDE THE GUARDED BLOCK; UNDETERMINED) sit in code-structure language (guard clause, early return, call sites) with no one-line "what this means for the product" for the product owner.
5. **WP0.8 map and K4 (option values): engineer documents** (column names, schema properties, 169 lines of option identifiers); they need a one-paragraph plain summary above the BLUF before Kam sees them.

## What I did NOT check
- LIB and SRC source files: not opened (the path rule bars `Source_Documents/`); every `LIB:`/`SRC:` cell is judged from the EXCERPTS file only, clipped at about 310 characters (the clipped `SRC:` lines are JSON description strings; 0 of the LIB excerpt lines are clipped, by program).
- 266 of the 310 K1 to K4 cells (the sample is 44; K4 has 131 unsampled); the K2 rows are the likeliest place for more TWO-CLAIMS and WEAKER cells (3 of its 12 sampled cells were TWO-CLAIMS or WEAKER).
- The kit's own measured counts (17 and 3 columns, 16 properties, 14 shared names, 16 Teams references, 11 and 7 groups, `cmp` 0 of 134, 266 `.cs` files): not re-measured; I checked only that the K2 table has 16 rows (8 naming F82/F83, 8 "none"), the K4 headings against the group-list excerpts, and the register's row counts.
- `doccheck.py` not re-run; STATUS and the kit's other sections beyond those the commission named; Jira; whether any printer, tenant or binary behaves as documented (all UNMEASURED in the documents, correctly so).
- Whether the product owner would agree with any default (that is his).
