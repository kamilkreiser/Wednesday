STARTABLE: YES (after Tuesday's stamp; six questions, each with a default that lets it start; Q-1 and Q-3 change what ships to the client tester, read them first)

# B1586 drafter report: HPSM-POC builder, lane R of the reviewer-feedback plan (F11, contents page and links in the executive PDF), seat H169

Drafted 2026-11-15 17:31 to 17:47 AEDT (`date` printed 17:31:06, 17:31:37, 17:33:02, 17:33:33, 17:36:42, 17:38:05, 17:38:22, 17:40:47, 17:46:13). Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1586_SEAT-H169_hpsmpoc-lane-r-pdf-contents-page.md` (87 lines). Sidecar `...contents-page.md.measured`: 74 claims, `stamp_check.py <kit>` rc 0. Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1586/`.

## BLUF
- **The plan's one unchecked risk is measured, and the answer is GO: PdfPig 0.1.16 writes internal link annotations.**
  - The package's own doc file lists `PdfPageBuilder.AddLink(ExplicitDestination, PdfRectangle)` and `AddLink(LinkAnnotation)`.
  - A scratch probe, built with the project's drive-local dotnet 10.0.404 against the cached 0.1.16 package (its DLL is byte-identical to `lib/net9.0`), wrote a 4-page PDF. Page 2 links forward to pages 3 and 4 before they exist; pages 3 and 4 link back to page 2.
  - PdfPig's own reader read every link back as a GoTo to the right page. A zero border (`/Border [ 0 0 0 ]`) is accepted, so nothing is drawn around a link on screen or on paper. The trailer `/ID` pair the renderer patches for determinism is still there.
  - So no library change is needed. Step 1 of the kit makes the seat re-run the same probe and STOP with the evidence if it differs.
- **The build is a small change in `Pdf/`:**
  - `Layout.Compose` reserves page 2, lays out the sections unchanged (each moves down one page), then fills page 2. It holds the heading "Table of contents" and one row per bookmark (the existing "n. Title" plus the page number), and each row is a GoTo link.
  - `DrawChrome` puts a GoTo link to page 2 over the existing running-header text on every page after the cover.
  - Bookmarks are kept. The heading is the plan's quoted word (ACTION-PLAN:190) and the only new word.
- **Two things the plan did not see, now in the kit:**
  1. **The readiness report uses the same renderer** (`ReadinessReportGenerator.cs:55`). A renderer-only change would give it a contents page too. Q-1, default (a): the executive report only, through one optional `ReportModel` parameter `ContentsHeading`, which the readiness builder sets to null.
  2. **The Demo copy name check would start refusing some customers if the heading were a renderer literal** (DERIVED: `ReportingEndpoints.cs:496`, `:661-665`, `:799`). That check treats any printed word of 4+ letters that is not a string of the report MODEL as "telling". So "Table" and "contents" would refuse the Demo copy of a customer named, for example, "Contents Hospitality (sample)". Putting the heading in the model, as `ContentsHeading`, makes it one of the report's own words. The kit pins this with a test whose scratch mutant must fire.
- **Three tests go wrong, one of them silently.** The golden outline locator `FindIndex(p => p.Contains(heading))` and the HPSM-section slice would land on the contents page, which now prints every heading first: both go red. The SOW-order test stays green with no meaning left. The kit names all three as REWRITE and adds a "silent class" duty.
- **Deploy note (Q-3):**
  - An issued report keeps its stored PDF.
  - The Demo copy of any report issued BEFORE a deploy is redrawn and compared byte for byte (`ReportingEndpoints.cs:457-458`, `:485`), so it is refused ("This report changed after it was issued", `:514`) until the report is issued again.
- **Partition:**
  - b1577 (41 paths) touches nothing under `HpsmPoc.Modules.Reporting` (MEASURED, with a control).
  - Lane P's conditional `ReportModelBuilder.cs` and lane N's `ReportingEndpoints.cs` are both NOT-yours; this kit edits neither.
  - Product paths: `Pdf/Layout.cs`, `Pdf/PdfPigReportRenderer.cs`, `Report/ReportModel.cs`, one argument in `Readiness/ReadinessReportModelBuilder.cs`, and the ADR-R11 row of the module README.
- **Seat set-up:**
  - Base `f32b209bfa6f33c3c0268c1daa76753c816b316e`, 0 open PRs. Seat H169, pane `Datasec/HPSM-POC-H169`, branch `b1586/hpsmpoc-pdf-contents-page`.
  - Ports 10020-10029: SQL Server 10020, Azurite 10021. CI's own Azurite port is 10000, which is inside lane P's block.
  - Model Sonnet (`model-routing.md:92`, C2), gate G1 (`:108`, a client-tester deliverable), id `claude-sonnet-5-5` (`models_latest.json:23`).

## Facts re-measured with instruments
- **Main and PRs.**
  - `gh api -X GET branches/main` gave `f32b209b...` at 17:31 (2026-11-15T05:04:28Z).
  - `pulls?state=open` length 0. Control `state=all&per_page=3`: 319, 318, 317 (closed). `pulls/99999` returned 404.
  - `matching-refs` b1584, b1585, b1586 each length 0. b1577 length 1 at `fda88777...`. Control b1541 length 1.
- **b1577 versus main.** `compare/f32b209...fda88777` gave ahead 1, behind 0, 41 files. Of those, under `HpsmPoc.Modules.Reporting`: 0. Control: `HpsmPoc.Modules.Assessment` src gave 2.
- **PdfPig probe** (`probe/`, saved log `probe3.out`):
  - Build: 0 warnings, 0 errors. The five reader lines are copied into the kit verbatim.
  - `/S /GoTo` count 4. `/Border [ 0 0 0 ]` count 1 on the zero-border build; control: 0 on the default build.
  - Two runs differ only inside the random `/ID` (`cmp` first difference at byte 2280, in the trailer), which the renderer replaces.
- **Toolchains.** Drive-local `dotnet --version` gave 10.0.404. `node --version` gave v24.21.0. `global.json` pins 10.0.404 with rollForward disable. `Directory.Build.props` has TreatWarningsAsErrors true and net10.0.
- **Census** (`census.py` over the tarball, frame: every file):
  - 236 rows in 60 files. Control: one planted heading line adds exactly 1 HEADING row.
  - "table of contents" (case-insensitive) under `api/` and `web/src`: 0. Control "detailed findings" under `api/src`: 2.
  - `AddLink|LinkAnnotation` under `api/src`: 0. Control `AddPage`: 2.
  - `AddImage|AddPng|AddJpeg` in the two Pdf files: 0 and 0. The PDF has no logo, so the back-link is the header text, as the plan says.
- **Web and infra reads of the changed files.** The needles `Layout.cs`, `PdfPigReportRenderer.cs`, `ReportModel.cs`, `ReadinessReportModelBuilder.cs` and `HpsmPoc.Modules.Reporting/README.md` hit 0 files each in `web/`, `infra/` and `scripts/`. Control: `ReportModelBuilder.cs` hits 2 (`gate-b99-labels.test.ts`, `summary-paragraphs.ts`). So by DRAFTER_RULES fence 8 no web job reads the changed files. Step 6a makes the seat re-prove this over its final diff.
- **Jira** (`jsearch.py`, a GET-only copy of the d1577 helper; token read in-process, never printed):
  - `project = HPSMPOC AND ( summary ~ "contents" OR summary ~ "link" OR summary ~ "PDF" )` gave COUNT 39. Summaries naming contents or hyperlink: 0. Control "PDF": 8.
  - `text ~ "table of contents"` gave 17, none an F11 ticket by summary.
  - `created >= "2026-11-15"` gave 3 (484, 483, 482), none F11.
  - So no F11 ticket existed at 17:38. The records seat B1583 creates it; the kit has a TICKET slot.
- **Branches.** 335 names. The loose pattern hit 5 (b125, b140, b215 PDF name and alias work; b1059 and b1113 web tile links), none of them this work.
- **Ports.**
  - `lsof -nP -iTCP:10020-10029 -sTCP:LISTEN`: 0. Unfiltered: 33.
  - Scan of 31 non-`.pre-` SEAT kits of 14-15 Nov for `1002[0-9]`: 0 each. Control `992[0-9]` over the B1577 kit: 2.
  - Panes at 17:38: `%0 tuesday`, `%63 Datasec/MPS-M141`, `%54 Datasec/MPS-M140`, `%1 fleet-monitor`, plus unnamed panes. No HPSM-POC pane.
  - Load 28.12 at 17:40: expect load-gate waits.
- **CI lines at f32b209** are the same as the B1577 kit's (87, 184, 252, 255, 303, 314, 630). The api job's Azurite start is at 76-85 and its by-name Azurite judge at 89-121; the SQL judge runs 277-310.
- **CodeQL.** csharp-queries 1.11.0 is installed (`ls`). The gate standard records that C# cannot extract on this arm64 box (gate B1564, 2026-11-15). The kit says csharp NOT RUN, uses hand rows, and names hosted CodeQL as the only C# proof. The B1577 template's csharp step is out of date on this point.

## Census by program (frame: every tracked file of the f32b209 tarball; rows in `d1586/census_rows.tsv`)
**Property:**
- **REWRITE** when a line locates a section by its heading text across the whole document, or on the first page that holds it, or pins an executive page number or page count.
- **UNAFFECTED** when a line reads a page by a role that does not move (the cover; "every page after the cover"), reads the readiness PDF under Q-1 (a), or reads model data.

| file | verdict | why |
|---|---|---|
| `Pdf/Layout.cs`, `Pdf/PdfPigReportRenderer.cs` | REWRITE (product) | D1 and D2 |
| `Report/ReportModel.cs` | REWRITE (product) | `ContentsHeading` parameter and its constant (D3) |
| `Readiness/ReadinessReportModelBuilder.cs:79-90` | REWRITE (product) | `ContentsHeading: null` (Q-1 a) |
| `Reporting/README.md:74` | REWRITE (doc) | ADR-R11 lists what the PDF has |
| `PdfReportGoldenTests.cs:33-38` (+3 executive goldens) | REWRITE | `FindIndex(...Contains(heading))` lands on page 2; regenerate the goldens, then prove the diff is +1 only |
| `PdfReportGoldenTests.cs:116-120` | REWRITE | the HPSM slice lands on the contents page |
| `PdfReportGoldenTests.cs:55-58` | REWRITE (silent) | still green, but now measures the contents page's order |
| `PdfReportGoldenTests.cs:62-75`, `:148-156`, `:189-196` | UNAFFECTED | chrome on every page after the cover; bookmark titles unchanged; page count `>= 5` |
| readiness goldens (4), `ReadinessReportGoldenTests.cs`, `ReadinessData.cs:91`, `ReadinessBandBoundaryTests.cs` | UNAFFECTED under Q-1 (a) | no contents page; under (b) all REWRITE |
| `B140RunningHeaderTests.cs` | UNAFFECTED | header text and baseline unchanged; page 2 still has it |
| `B140NameGlyphsTests.cs`, `B125RenamedCustomerPdfTests.cs:174`, `B215DemoAliasPdfTests.cs:346` | UNAFFECTED | they read page 1 |
| `B215DemoAliasPdfTests.cs:69`, `:75` | UNAFFECTED | header on every later page; stored and copy both drawn at head |
| `TableKeepTogetherTests.cs` | UNAFFECTED | the contents page has no table header |
| `B223NameFormsTests.cs:102` | UNAFFECTED | Contains over the model's strings |
| `IntegrationTests.cs:54`, `ReportModelTests.cs:28`, `ReadinessReportGeneratorTests.cs:31` | UNAFFECTED | model section ids |
| `B226*`, `B228*` name-check suites | UNAFFECTED by design (D3); a red is a STOP, not a rewrite | the heading is a model word |
| live-API web specs (`playbook-report-withheld-live-api.spec.ts`, `playbook-content-050-live-api.spec.ts`) | UNAFFECTED, NOT RUN | in no CI shard |

These verdicts are context readings of each line, not runs. The dynamic census (kit Step 4) decides.

## Chain table (rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 | kit, project identity, drive-local dotnet, docker, pinned MSSQL and Azurite images | exist at BASE / on the box |
| 1 | `mut`; gh; the drafter's probe folder (exists now in d1586/probe) | step 0; drafter |
| 2 | `mut` restored; Azurite up (started in step 2 itself, before the test run); fixtures `TestData`, `ReadinessData` (exist at BASE) | step 0 |
| 3 | `head`; Q-answers | step 0, stamp |
| 4 | `head` product files built | step 3 |
| 5 | REWRITE list (steps 2 and 4); BASE renders (step 2); `mut` for red-at-BASE runs | steps 2, 4 |
| 6 | `head` complete; BASE results; containers (started in 6b/6c) | steps 2, 5 |
| 6e | the diff | step 5 |
| 7 | all green | steps 4-6e |
| 8 | pushed sha, census files, renders | steps 2, 4, 5, 7 |

## D-decisions (made in the kit, each reversible by Tuesday at the stamp)
- **D-1 No library change.** PdfPig stays 0.1.16 and `Name` stays "pdfpig-0.1.16". Links use the package's own `AddLink`/`LinkAnnotation`, measured above.
- **D-2 The contents page is one fixed page 2.** It is filled after layout, because the section pages are known only then. If the rows would not fit on that page, the build throws; nine rows fit, so in practice it never does.
- **D-3 The contents page is not added to the bookmarks.** Bookmark titles are unchanged; only their pages move by one.
- **D-4 The back-link is on every page after the cover, the contents page included.** The plan says "every page after the cover", and a self-link is harmless.
- **D-5 Zero-width link borders.** Nothing is drawn, so printing is unaffected. Measured on the probe.
- **D-6 Jobs.** No web job is run unless Step 6a's scan finds a reader. The api job and both SQL Server parts run whole: Assessment tests render and store PDFs (B215, B223-B228, Blob). Infra runs always (fence 8).
- **D-7 File names.** The new test files are `ContentsPageTests.cs` and `ContentsHeadingNameCheckTests.cs`, not B-numbered, because the kit's own name scan bans `B1586` on added lines.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 Which reports get the contents page.** The readiness report shares the renderer.
  - Default (a): the executive report only. The F11 text says "Executive report". The readiness PDF stays byte-identical, and its five goldens do not move.
  - (b): both. The readiness builder passes the heading too, and its goldens and `ReadinessData.Section` become REWRITE rows.
- **Q-2 The heading word.**
  - Default: "Table of contents", as the plan quotes it (ACTION-PLAN:190, the reviewer's words, Tuesday's reading).
  - The commission notes Kam approved "Contents" as a heading in Security Composer. The kit does not assume that carries across products. Say "Contents" at the stamp to swap it; the kit then changes that one literal.
- **Q-3 Existing data, as deploy notes.**
  - After a deploy, issued reports keep their stored PDF, with no contents page.
  - The Demo copy of every report issued before the deploy, showcase samples included unless they are re-seeded, is refused with "This report changed after it was issued" until the report is issued again.
  - Default: accept it, measure what can be measured, and state it in the PR body. The seat reads the seeder's idempotence and says whether a hosted re-seed re-issues sample reports. Nothing is deployed by this kit.
- **Q-4 Model.** Row C2 says Sonnet, and the gate is G1 (Opus, client-tester deliverable). Default: Sonnet as written.
- **Q-5 The ticket key in code comments.** Default: the TICKET slot's key, if the records seat B1583 has created it by the stamp. Otherwise "none yet", and comments cite no key. The commit message never carries a key.
- **Q-6 Partition with lanes P and N.** Their kits (B1584, B1585) did not exist when this kit was drafted (`ls briefs | grep B158[3-6]` gave nothing at 17:36). Default: Tuesday checks their OWNS lines against this kit's NOT-yours list at the stamp. Any overlap on `Report/ReportModel.cs` or `Readiness/ReadinessReportModelBuilder.cs` is resolved in favour of whichever kit is stamped first.

## UNMEASURED
- Everything the seat runs. The drafter ran no project build, no project test, no container and no CodeQL. In particular:
  - the red set of Step 4: the census predicts it, nothing has run it;
  - whether nine rows fit at Letter size (DERIVED: ContentTop is 722 pt from the bottom; nine 18 pt rows plus a 36 pt heading is about 200 pt);
  - the D4 byte-identity of the null-heading PDF with BASE;
  - the name-check mutant control.
- **A screen-reader run.** The PDF is untagged (ADR-R11), so the links are not announced as links. The kit states this limit and does not claim a test.
- The landing-rule quote (CLARIFICATIONS.md line 3617) and the hosted CodeQL languages are RELAYED from the H-2 kit.
- Whether b1577 lands during the work. It touches no Reporting path; A MOVED MAIN requires a re-run because showcase content feeds sample reports.
- **A latent issue, DERIVED and not run, outside this kit.** Words the renderer prints by itself that are not model strings may already be "telling" to the Demo copy name check today. Examples: "Prepared for" (`Layout.cs:76`), "Confidential", "Current score (filled)". A customer named "Prepared Foods (sample)" might have its Demo copy refused at main. Worth a records-seat look; not built here.

## Outside-the-fences disclosure
Reads:
- `DRAFTER_RULES.md` and the commission file.
- The plan folder: ACTION-PLAN, FEEDBACK, RESULT (grep), COMMISSION-ACTION-PLAN (grep).
- The B1577 kit, its drafter report and ANSWER-1.
- `model-routing.md` (rows), `models_latest.json` (grep), `brief_seat.sh` (grep), and the headers of `stamp_check.py` and `launch_when_cool.sh`.
- `2026-11-10_GATE-VERIFIER-STANDARD.md` (grep of step 7).
- The project's `CLAUDE.md` (grep).
- `gh api -X GET` under the project's `GH_CONFIG_DIR`: main, pulls, matching-refs, the branch list, one compare, Pdf commits, and the f32b209 tarball.
- Jira: four JQL searches via a GET-only helper copy.

No `decision_queue.sh` call was made: no card was needed, since the ruling text is in the commission.

Local runs, in my work folder only:
- tarball extraction, `census.py` (with a planted control) and `fill.py` (writes only the sidecar);
- the PdfPig probe: a scratch .NET console project built with the drive-local dotnet against the local NuGet cache, with a `nuget.config` that clears every feed except that cache folder. No network feed was used and no file was written under `!CODING`. The build wrote `obj/` and `bin/` inside `d1586/probe/`.
- `lsof`, `tmux list-panes`, `uptime`.

Writes, besides those scratch files: only the kit, its sidecar (by `stamp_check.py --init`, then filled) and this report.

Nothing else was touched: no `decision_queue.sh list`, no Jira write, no git or GitHub write, no file under `/Volumes/Datasec_DEV/!CODING/`, no message, no tmux send-keys, no az, no docker, nothing deployed, no `_ledger.md`, no WEDNESDAY, FRIDAY or non-Datasec tree.

DRAFTED B1586: kit 87 lines, sidecar rc 0, questions 6
