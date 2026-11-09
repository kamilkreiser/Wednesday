VERIFY B1406: GO WITH FINDINGS @ 514e5f9 on main 31234f5

# Tier-2 docs gate (G2), lane M8, branch `b1406/mps-docs-runbook`

Independent read-only verifier for Tuesday, 2026-11-10 06:44-06:5x AEDT. Scratch clone in the session scratchpad, push URL set to `DISABLED`; `gh api -X GET` only under the MPS `GH_CONFIG_DIR`. No PR, Jira, mail or board. The builder's STATUS was read whole and treated as claims.

Blockers: 0. Majors: 0. Minors: 4 (below). Info: 3.

## 1. Pins and partition
| Check | Instrument | Result | Control |
|---|---|---|---|
| Branch tip | `git ls-remote` (deploy key) | `514e5f9830a21d2cf80cad91cc3520207692db1d refs/heads/b1406/mps-docs-runbook` | the same call prints main `31234f5f...` |
| Main now | `gh api -X GET .../git/ref/heads/main` (06:44:44 AEDT) and `ls-remote` | `31234f5f0e17dadcd5d6955055d477e660d204b7` = kit S2 base; main has not moved | |
| Compare | `gh api -X GET compare/main...514e5f98` | ahead 1, behind 0, merge base = main; files: `modified docs/IMPORTER.md +5 -0`; 1 commit `514e5f98` | |
| Lane | the kit's OWNS line (DEMO/IMPORTER/ENGINE/RECONCILIATION.md, ROOT:SETUP_RUNBOOK.md) | **1 of 1** changed paths inside OWNS | |
| Other MPS lanes | `grep -i docs/IMPORTER.md` over the B1400-B1409 kits | each of the 9 other kits names it once, and that one line is the M8 partition line (M8's own path). No other lane owns it | `docs/` count per kit 2-4 |
| Open PRs | `pulls?state=open --jq length` | 0 | `pulls?state=closed&per_page=1` top = #166 |
| Other origin branches on the path | `diff --name-only main...<b> -- docs/IMPORTER.md` over all 190 origin refs | 10 hits: this branch, and 9 stale ones (b03, b104 x5, b1116, b303, b560). 8 are heads of merged PRs (#3, #78, #65, #69, #66, #143, #84, #104); `b104/mpscalc-147-customisation` has no PR and was superseded by `-r2` (#69); 121 behind. None is live | `b14*` filter lists 3 refs |

## 2. ALREADY-ON-MAIN lines, re-checked at main 31234f5f (by program)
| Line | Check | Result |
|---|---|---|
| MPSCALC-200 (whole) | `grep -c 294 docs/IMPORTER.md` = 0 (control `262` = 1); `:127` says the 262 are rows and that 371 is the care-pack SKU total; `:115`/`:116` define "Read" (22 + 8 = 30 mapped devices) and explain the 4 A3 rows outside the catalogue | **TRUE**. The contradiction the ticket names is gone. Residue R-1 is real: the 3 (A4) and 15 (A3) in-catalogue unread rows are "not counted further here" |
| MPSCALC-195 (ENGINE.md part) | `docs/ENGINE.md:177`: 1e-18 bound and 1.02e-28 measured; `tests/MpsCalc.Engine.Tests/DealUsageTests.cs:215` asserts `<= 1e-18m` relative | **TRUE** |
| MPSCALC-207 (docs part) | `IMPORTER.md:17` "any mapped model sheet"; `:93-95` "prove checks the store against its own recorded section only ... cannot see a section the importer bounded wrongly, or a SKU removed from both"; singular counts quoted; `src/MpsCalc.Import/Parity/ParityProof.cs:55,59,98` uses `Count(n, "option record", "option records")` | **TRUE** |
| MPSCALC-178 (DEMO.md footer part) | `docs/DEMO.md:61` (also :14, :131) footer follows state; `grep -c -i -E 'until Kam rules\|until the footer'` = 0, control `footer` = 5 | **TRUE** |

## 3. Code-fact sentences in the diff (all of them: 9 claims in the added paragraph and 4 in the commit body; fewer than 15 exist)
| # | Sentence (added, docs/IMPORTER.md:143-146 at head) | Source at head | Verdict |
|---|---|---|---|
| 1 | "The source lifecycle is built, in the API" | `src/MpsCalc.Api/Sources/SourceAdminEndpoints.cs:20-23` maps imports / validate / activate / rollback | TRUE |
| 2 | "... and not in the importer" | `git grep -i activate\|rollback` in `src/MpsCalc.Import`, `tools/MpsCalc.ImportCli`: one comment only (`ReferenceDocumentValidator.cs:15`), no lifecycle | TRUE |
| 3 | `docs/API.md`, section "Source lifecycle" | `docs/API.md:635` `## Source lifecycle (...)` | TRUE |
| 4 | "(stage, validate, activate and roll back a governed source version)" | API.md:636 "stage -> validate -> activate -> (rollback)"; routes above | TRUE |
| 5 | "It is off by default" | `SourceLifecycle.cs:59` `PathKey = "MpsCalc:SourceVersions:Path"`; `:160` empty returns null; key absent from all 3 `appsettings*.json` (count 0 of 3 files) | TRUE |
| 6 | "... and runs on the development stub only" | `SourceLifecycle.cs:164-166` `mode != AuthMode.DevStub` throws "Start refused: ... must be empty in Entra (hosted) mode" | TRUE |
| 7 | "per-type staging and raw spreadsheet upload (FR-ADM-013)" not built | API.md:673-674, :704; `SourceAdminEndpoints.cs:170` `SOURCE_TYPE_NOT_SUPPORTED` | TRUE |
| 8 | "the expire action (FR-ADM-010)" not built | API.md:704; `SourceGovernance.cs:6-7` "Expired ... nothing sets yet" | TRUE |
| 9 | "a hosted switch-on and the admin console screens" not built | API.md:705; `SourceVersions` in infra/scripts/.github: 0 (control `ReferenceStorePath` 3 files); `admin/sources` in `web/src` outside `generated/`: 0 files (generated: 2) | TRUE |
| 10 | Commit: "No existing line is changed" | compare `+5 -0` | TRUE |
| 11 | Commit: "off by default, development stub only" | as 5, 6 | TRUE |
| 12 | Commit: DEMO.md footer "already on main" | section 2 | TRUE |
| 13 | Commit: the other sentence "belong[s] to the API.md lane" | kit partition: `docs/API.md` is M11's; the sentence is still at `docs/API.md:440-441` | TRUE |

0 false, 0 not shown.

## 4. Name, id, secret and hidden-character scan
- Instrument: python `re`, case-insensitive, `(?<![A-Za-z])<name>(?![a-z])` over the ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite); plus `ghp_|gho_|github_pat_`, `AKIA...`, `-----BEGIN`, `eyJ...`, GUID shape, `https?://`, `azurewebsites.net`, `onmicrosoft.com`, `atlassian.net`, secret words, `B\d{2,4}`, seat/gate ids, every Cf-category character and every non-ASCII character.
- Over the 5 added lines (428 chars) and the commit message (673 chars): **0 hits**.
- Control string `x _by_Kam_ y _by_waite_ ghp_abc <U+200B> B1406 https://h.azurewebsites.net`: **7 hits** (Kam, Waite, ghp_, https://, azurewebsites.net, B1406, Cf 0x200b), so the scanner can fire.
- The added lines are pure ASCII. The context line `:140` above them holds an arrow and an ellipsis; it is pre-existing and unchanged.

## 5. CI jobs that read the changed file
- `.github/workflows/ci.yml` (the only workflow) jobs: `dotnet` (:30), `web` (:45), `python` (:68; loop at :86 is `tools/demo/test/test_*.py infra/tests/test_*.py scripts/tests/test_*.py`), `package` (:93). No markdown, link or `git ls-files` docs job.
- `git grep -i IMPORTER.md` over tests/tools/scripts/infra/web/.github: only `tests/MpsCalc.Import.Tests/OutputGuardTests.cs:35,71,138`, which writes its own synthetic `docs/IMPORTER.md` (`_trackedBytes = "# tracked file\n"`, :23) in a temporary repo and never reads the real doc; and an error string in `tools/MpsCalc.ImportCli/Program.cs:218`. `scripts/package.sh`: 0 `docs` lines.
- The only doc-reading test in CI, `tools/demo/test/test_demo_doc.py`, reads `docs/DEMO.md`, whose blob is identical at main and head (`130cb91c`). **RUN locally at the head tree (git archive): rc 0, 10 tests OK.** Control: the same test with DEMO.md replaced by one line gives rc 1.
- NOT RUN: dotnet, web, package jobs and CodeQL. They do not read this file; hosted CI plus CodeQL on the PR is the proof.

## Findings
- **M-1 (Minor, metadata):** commit `514e5f98`'s git author is a person's name and work address. 161 of 162 main commits are authored `kamilDatasec <...noreply...>`. The name is not in the message or the added lines, and the squash re-authors it, so it does not reach main in the squash form. Land by squash only, never by rebase or merge commit.
- **M-2 (Minor, partial ticket):** this change closes only one of the three sentences of MPSCALC-178. `docs/API.md:440-441` (the `lifecycleEvents` sentence for the body-less routes) is still open and belongs to lane M11. The landing texts say "part of"; the records seat must not move 178 to Done on this PR alone.
- **M-3 (Minor, true residue outside the diff):** `docs/DEMO.md:165` comments that sourcing `4_Credentials/.env` gives `MPSCALC_API_CLIENT_ID`; the builder measured `.env` key names without it, and `tools/demo/seed.py:147-150` refuses without it. This is the builder's R-2; confirmed by source. Not edited here (no ticket names it); file a backlog row.
- **M-4 (Minor, records hygiene):** the STATUS file's first line still reads `PROGRESS B1406: PENDING` while its last line is `READY`. This is cosmetic.
- **I-1 (Info):** the kit's CI fact omits `tools/demo/test` from the `python` job; `ci.yml:86` includes it. The builder caught this (R-4), and this gate ran that test.
- **I-2 (Info, not part of this PR):** the root records commit `1af6c445` (MPSCALC-225) sits on the local root branch `records/b1406`, parent root `main` `13db4d11` (unchanged), and is **not landed**. Spot-checked: 1 line added, and the scan finds 0 names, ids, secrets, GUIDs, URLs or non-ASCII in the row or the message. Its claims hold at code main: `seed.py:119-121` (host), `:147-150` (client id); `showcase.bicepparam:8`; `API.md:952` apiScope form; `infra/README.md:39` `siteHostName`. Landing it (`git merge --ff-only records/b1406` in the root, under `.tools/.git-lock`) is Tuesday's call.
- **I-3 (Info):** MPSCALC-200's R-1 (3 and 15 unread in-catalogue rows not decomposed) needs a seat allowed into the local price-book store. Counts only.

## Landing
Squash with the head pinned (project CLAUDE.md:50 CodeQL rule: seats push, the coordinator opens the PR and merges once CodeQL is green; MPS convention `--squash --match-head-commit`). The files beside this one: `pr-title.txt`, `pr-body.txt`, `squash-subject.txt`, `squash-body.txt`, `landing.txt`. All are ASCII except the mandated trailer of `pr-body.txt`. Scan: 0 names, B-numbers or seat ids. Nothing deploys.
