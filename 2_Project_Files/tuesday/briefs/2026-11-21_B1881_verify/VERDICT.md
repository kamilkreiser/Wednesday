GATE B1881: GO WITH FINDINGS @ f81e36f on main 28d8d31

Round 1. Tier G2 (Sonnet, one reader). Read 2026-11-21 23:35 to 23:42 AEDT. origin main = 28d8d31b73c6475b33921c679499b0777fdf0448 (equals the kit's base); branch b1876/mps-docs-420-417 = f81e36f1335425d77a4469c2bb8f0971eae1273f, one commit, parent 28d8d31b; open pull requests 0; compare (gh api -X GET, project GH_CONFIG_DIR, account kamilDatasec) ahead 1, behind 0, files docs/ENGINE.md +1 -1 and infra/README.md +16 -0. Own clone in the session scratchpad (push URL invalid://no-push), detached at the head. Python 3.14.10.

No Blocker, no Major. Findings are Notes only (below).

## 1. Scope (by program)
- `git diff --name-only` base..head: exactly docs/ENGINE.md and infra/README.md. Blobs at head: ENGINE.md 5539adca563c8880bddb2ecdad8234c8d9233012, README.md 99eedfba00450e73d96b35e5ada54c116cd2f58d, both equal to the kit's prototype. Base blobs 3b5ffc81... and 55171ec9... as the kit says.
- ENGINE.md: 215 lines each; the only differing line number is 166; line 166 of head equals line 166 of base with `Engine only: the contract and the screens do not carry it` replaced once by the frozen new text (177 characters, 0 pipe characters; the row keeps its 4 pipes); non-ASCII lines 75 and 75. Control (a planted change on line 11) reads differing lines [11, 166].
- README.md: the diff is two pure insertions (13 lines after base line 32, 3 lines after base line 48), no replace or delete; removing the 16 added lines reproduces blob 55171ec94dbf77ae6b70cd1409ebbfc0e266d007 (control: removing 15 does not); non-ASCII lines 7 and 7; the longest added line is 127 characters; added non-ASCII bytes 0.
- The phrase `the contract and the screens do not carry it` over docs, src, tests, web, .github: 1 line at base, 0 at head (also 0 for `do not carry`). `az bicep` in the head README: 0 (control `az deployment`: 1).

## 2. Every added sentence against the code at main (lines printed)
ENGINE clause: `docs/api/openapi.json:1829` member `projection` of schema PurchaseResult (opens :1810), reached from the quote answer as `purchase` (:1311) and named `purchase.projection` in docs/API.md:605; `src/MpsCalc.Api/Quotes/PurchaseMapping.cs:264` `Projection = internalMetrics && p.Projection is { } pr ? ProjectionDto(pr) : null`; `PurchaseMapping.cs:321` `Restrict(...)` sets `Projection = null` at :342 (docs/API.md:613-614 says so); `web/src/screens/bom/PurchaseResultView.tsx:201` renders `<ProjectionTable>`, `ProjectionTable.tsx:37-41` is a `<table>` with a caption; `QuoteScreen.tsx:610` mounts the view. Every word is supported. The second clause (Api cannot state a fee) is byte-equal and agrees with docs/API.md:611-612.
README insertion A: `infra/env/showcase.bicepparam:8-9` `readEnvironmentVariable(...)` for both ids, no default; `infra/main.bicep:20-28` no default, 36 characters. "stops at the parameter file" is the deploy record's M5 (rc 1, BCP427 at showcase.bicepparam(8,45) and (9,45), relayed). Step 6 (README line 79 at head) does export both ids before its what-if: supported.
README insertion B: `main.bicep:40-41` the literal `'2026-10-01'` (a default, not computed); `modules/showcase.bicep:112` `timePeriod: { startDate: budgetStartDate }`; `endDate` on 0 lines of main.bicep and showcase.bicep (control `startDate` 1 line); the seven named siteConfig properties are each on 1 line of showcase.bicep:41-53 and `localMySqlEnabled` and `netFrameworkVersion` are on 0 lines (so "seven of them, not those two" is right, and nine = 7 + 2). The budget deltas, the nine Create lines, `v4.6` against `v4.0`, the budget start left at 2026-10-01 and 0 of the 12 hashed config/web fields changed are the deploy record's lines 112, 113, 116, 122 (relayed). "A date the service sets" rests on the record's "server-set" (relayed). All hosted facts are written "read on 2026-11-20" or "was accepted on 2026-11-20", none as always; the first-create case is written as "not measured". No word unsupported.

## 3. Reach (the kit's probe, run at the head; 244 files scanned)
`ENGINE.md`: C 6, X 3 (web/src/api/generated/openapi.snapshot.json:1006, :1812, :1829, the description strings); `infra/README`: C 4, X 0; `infra\README`: 0 and 0 (the kit's table has no row for it; the probe's control is the next two). Controls: `wwwroot` C 11, X 28 and `index.html` C 2, X 9: both equal the kit. The JSON is imported by exactly 2 files, both tests (web/src/test/internalNames.ts:3, web/src/screens/Lifecycle.b444.test.tsx:5); control `format/decimal` import: 40 files. `internalNames` is imported by 9 test files and web/e2e/bom.spec.ts only. csproj items reaching outside the project: 0 (control: 3 ProjectReference); vite.config.ts `publicDir|import.meta.glob|?raw|../docs`: 0 (control 26); web/public holds `proposal` only; scripts/package.sh names docs/ or infra/ on 0 lines (control wwwroot 5); json/md imports in non-test web source: 0 (control: 2 json imports in all of web/src); `MapOpenApi|AddOpenApi|Swagger` in src: 0 files (control UseStaticFiles|MapFallback: 1 file); the repository is private (gh api). No path to a customer found. Limit, as the kit says: source text only; no bundle or package was built or opened.

## 4. The CI python loop at the head (as ci.yml:104-118: python3 -I per file; BICEP = the project's v0.48.1, `Bicep CLI version 0.48.1`)
| File | rc | Ran |
|---|---|---|
| tools/demo/test/test_demo_doc.py | 0 | 10 |
| tools/demo/test/test_run_demo.py | 0 | 23 |
| tools/demo/test/test_seed.py | 0 | 33 |
| tools/demo/test/test_seed_hosted.py | 0 | 15 |
| tools/demo/test/test_seed_purchase.py | 0 | 12 |
| infra/tests/test_infra.py | 0 | 43 |
| infra/tests/test_validate_script.py | 0 | 6 |
| scripts/tests/test_ci_workflow.py | 0 | 8 |
| scripts/tests/test_deploy_pre1.py | 0 | 44 |
| scripts/tests/test_deploy_pre1_forms.py | 0 | 16 |
| scripts/tests/test_deploy_rollforward.py | 0 | 39 |
| scripts/tests/test_entra_all_roles.py | 0 | 19 |
| scripts/tests/test_scripts.py | 0 | 56 |
| scripts/tests/test_sdk_pin.py | 0 | 13 |
| scripts/tests/test_sdk_pin_routes.py | 0 | 51 |
15 files, loop rc 0, no `Ran 0`, every last line OK. (Runs were in the clone; the loop is the only thing that ran there.)

## 5. Words and secrets
Over the 17 added lines (the whole ENGINE line 166 counted) and the commit message: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Tuesday, Wednesday, Friday (and the other weekdays) 0 each, the underscore-aware scan with a planted `_by_<name>_` control firing for each; GUID pattern 0; azurewebsites, microsoftonline, app-mpscalc, u6agl3 0; `az bicep` 0; http 0; B-numbers 0; decided/approved/ruled/"product owner"/ruling 0; the word "tenant" 0; "subscription" 1 (the added sentence "a new subscription takes ..."; plain word, no id). Non-ASCII in added lines and message: 0; Cf characters 0 (control U+200B reads Cf). Commit message: subject 108 characters (as the kit says), one `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` line. Commit author and committer are the repo's configured address (equal; the kit's FACT 5; the address is not written into any text of mine). gitleaks 8.30.1 over base..head: rc 0, "1 commits scanned, no leaks"; planted random `ghp_` canary: rc 1. No CodeQL row applies (no code, test or workflow byte; hosted CodeQL decides).

## 6. The seat's FOR TUESDAY items
- Stale comment `infra/scripts/validate.sh:4` ("... is infra/README.md step 3"): confirmed at the head; the what-if is step 2, the create step 3. RECORDS: a ticket candidate (FOR-RECORDS.md), not a finding against this change.
- The X-39 control reading 2: confirmed. `X-39` is on 2 lines of docs/ENGINE.md (line 41, the R-30 row, which names X-39 as the purchase counterpart, and line 166); the row-anchored control `| X-39 |` reads 1. RECORDS: the kit's count was of the needle, not of the row; no effect on the edit.
- UTC/AEDT date: the deploy record's own labels are AEDT 2026-11-20 (what-if 09:25:59, apply 09:30:09); its UTC stamps read 2026-11-19 (about 22:25Z). The README writes "2026-11-20" with no zone. RECORDS (Note N2): correct as the AEDT date; a reader on UTC could read it a day off.

## Findings
| # | Sev | Finding |
|---|---|---|
| N1 | Note | The ENGINE row now reads "... shows it to that caller as a table (the web table, T-V5-7), and the Api cannot state a fee ..." so the word "table" appears twice. The parenthetical was kept on purpose (Q1, "keep every other word"). Not an error. FOUND at line 166 of head. TESTED: read as printed. NOT tested: nothing. HOW: python read of the line. In FOR-RECORDS. |
| N2 | Note | The README's date 2026-11-20 is the record's AEDT date; the record's UTC stamps are on 2026-11-19, and the README names no time zone. FOUND: deploy record lines 106, 206 against README lines 34 and 37 at head. Not wrong, a possible one-day misreading. In FOR-RECORDS. |
| N3 | Note | README step 6 "expected: Modify of the site's appsettings only" (unchanged, Q5) now sits beside a list that says a what-if shows other differences, and step 2 (the earlier numbered step) still says "0 Modify / 0 Delete" for the first deploy. The new sentences say to count net of the list and that steps 2 and 3 are the first deploy's record, which reads true. Left as the kit and the ticket's acceptance require. In FOR-RECORDS. |
| N4 | Note | `infra/scripts/validate.sh:4` stale pointer (step 3 for the what-if): ticket candidate, out of this lane. |
| N5 | Note | The kit's REACH table has no row for the backslash form of `infra/README`; the probe prints 0 and 0 for it (a spot not a measurement of Windows paths; the repo's mentions are comment lines with a forward slash). |

## What I did NOT test
No bundle build and no opening of the published zip (reach is by source text, as the kit states); no hosted CI, no CodeQL (no code changed; hosted decides); nothing against Azure (no az); the relayed hosted facts (what-if deltas, the accepted update, the 12 hashed fields) were read from the deploy record and not re-measured; the claim that a first budget create is refused or accepted is, as the README says, unmeasured; Jira was not re-read in this gate (the kit's drafter read both tickets, 0 comments at drafting); the ticket acceptance "MPSCALC-256, -267, -368 are not reopened" was not examined beyond the diff touching no code or test; no test was run outside the CI python loop (no dotnet, npm, browser). Clone at head only; main read by git and gh api, not run.

## Landing files in this folder
pr-title.txt, pr-body.md, squash-subject.txt (ends `(#PRNUM)`), squash-body.txt (ends `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`), landing.txt (wait script then head-pinned squash; `--min-checks 9`: the 9 distinct check names on PR 224's head 2bf1d822, the last merged pull request and the source of main 28d8d31b, read by gh api -X GET), FOR-RECORDS.md. PRNUM is a placeholder. No text says the product owner decided anything; the words are developer-only on Tuesday's reading.
