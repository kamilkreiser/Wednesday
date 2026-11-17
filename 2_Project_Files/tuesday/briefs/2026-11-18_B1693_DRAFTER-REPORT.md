STARTABLE: YES

Drafter: Sonnet 5.5 Agent-tool drafter for Tuesday. Clock: started Wed 18 Nov 2026 08:09 AEDT (`date` 08:09:06), kit and sidecar finished about 08:18 (`date` readings: 08:09:06, 08:10:28, 08:13:30, 08:16:18, 08:17:36). Files written: the kit `2026-11-18_B1693_SEAT-M157_mps-lane-m-d5-stale-v2-text.md`, its sidecar `.measured` (from `stamp_check.py --init`, 97 lines filled; 15 are parser artefacts or instruction text marked "no claim"), and this report. `stamp_check.py <kit>` exits 0 (97 claims, 97 measured, 0 not measured).

## BLUF
- Lane M-D5 (MPSCALC-411) is startable at CODE main `863e03376a08f4953e0198390ae412fc837e0d5b` (re-read at 08:10; the root records repo's main `74fe202a` is NOT the base and is named in the kit as such). It is ONE commit on `b1693/mps-lane-m-d5-stale-v2-text`, TWO paths: `docs/API.md:379` (E1) and `tests/MpsCalc.Api.Tests/QuoteApiTests.V0Home.cs` lines `:14` (E2), `:38-:39` (E3), `:69` (E4). No generated file, no contract file, no `Dtos.cs`, no sync, no npm.
- Authority verified at source: root `CLARIFICATIONS.md` C-109 (header at line 2716; "What it settles" at 2720: option (b), developer-only documentation corrected from what the code does without the product owner's word review; "Work owed" at 2722). The four lines are one docs sentence and three test comments (developer-only). The kit quotes both lines and has the seat measure that none of the four reaches a customer surface.
- Ticket read whole by Jira GET (own GET-only helper, token read in-process, never printed): MPSCALC-411 Backlog, 0 comments, its para 5 quoted in the kit. A NEW comment on MPSCALC-364 (41366, 2026-11-18 08:05, newer than the 41072 the previous lane read) records #210's landing and says clause 3 reads NOT MET and is held by 411; it confirms the plan and is quoted in the kit.
- Model C2 (`model-routing.md:92`, as the template), launch level sonnet inside the quotes. Gate: **G3** (`model-routing.md:110`, "comment corrections", "No gate: the builder's own red-proof plus Wednesday's completion check"), with G2 (`:109`, "docs") named as the fallback. Reason and the other reading are in Q3.
- Scratch proof: with the four frozen replacements applied to a copy of the main tarball: the comment-only proof of the test file reads equal (control: one identifier changed reads unequal); `until lane V2 fills` 1 at base -> 0; `until the Home work fills` 0 at base and 0 after; `dotnet build MpsCalc.slnx -c Release` `0 Warning(s)` `0 Error(s)`; `git diff --stat` in a scratch git repo reads `2 files changed, 5 insertions(+), 5 deletions(-)`.

## Model row and gate, re-printed (`/usr/bin/grep -n -E '^\| (L3|C1|C2|G2|G3) '` over `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md`)
- Line 92: `| C2 | **Multi-file build or feature that fails the local predicate, not decision-shaped, not auth-design and not a destroying path** | no | no | **1st** (RULED, Kam 2026-10-10 09:06:47: ...) | gate (tier 1 or 2 per G rows) | ...`
- Line 82: `| L3 | **Two- or three-file fix, spelled out** (rung 3: code_patch2 / bash_patch2) | no | **1st** ...`: the edit's size fits it, but line 91 (C1's Spark cell) says local workers never merge or push (RULED 09-25 rule 2) and this lane clones, commits and pushes: so a Claude seat, row C2.
- Line 109: `| G2 | **Tier 2**: tests-only, spec-only, docs, config/CI, tooling, and follow-ups whose mechanism a prior gate already measured | ... | **1st** (proposal; SUMMARY decision 2) | ... A Sonnet G2 that finds a security-shaped issue hands the PR to G1.`
- Line 110: `| G3 | **Tier 3**: backlog or citation fixes, ticket hygiene, comment corrections | — | — | — | — | — | No gate: the builder's own red-proof plus Wednesday's completion check (RULED 09-05). | — |`
- Model id `claude-sonnet-5-5` (the `sonnet` entry of `models_latest.json`, printed).

## Facts re-measured with instruments (sidecar has each literal)
- Main `863e0337...` by `gh api -X GET .../git/ref/heads/main` (08:10); compare to main `ahead_by` 0; open PRs 0; the paginated all-state list has 210 rows (controls: #202 and #210 present); the only PR naming `MPSCALC-364` or `MPSCALC-411` in title, body or head ref is #210 (closed, names 364); `matching-refs/heads/b1693` 0 rows (control `heads/b1686` 1 row).
- The code (`awk NR==` over the main tarball): `QuoteFigures.cs:125-128` (purchase `HardwareProfit, null, PurchaseTotalExTax, DealProfit`; rental `null, null, Portfolio?.ContractValueExTax, null`), `:149` the `ReadyToExport` constant, `:216/:219` the `ListFilter` record and its `Parameters` dictionary, `:227` the group list including `Groups.ReadyToExport`. The test's own `:71-:74` assert `readyToExport` answers OK and `readyToExports` is refused with INVALID_FILTER. The test quote at `:37` is `ApprovedRentalQuote()`, so E3's "tcv for this rental" agrees with `:128`.
- The four stale lines were printed as python `repr` of the raw lines (all ASCII): `docs/API.md:379`, `V0Home.cs:14`, `:38`, `:39`, `:69`. Counts at base over `docs`, `src`, `tests`, `web/src`: `until lane V2 fills` 1 (`V0Home.cs:38`); `until the Home work fills` 0; `until lane V2 builds` 1; `lane V2 flips` 1; `lane V2` 8 rows; control `oneOffGp` in `docs/API.md` 2. After the edits: 0, 0, 0, 0, and `lane V2` 5 rows (`docs/API.md:379`, `Dtos.cs:464`, `QuoteApiTests.V2Ready.cs:11`, `V0Home.cs:12`, `QuoteApiTests.V2Staff.cs:11`).
- Readers (FACT 4): every `tests/` or `web/src` file holding `docs/API.md` holds it in a comment (3 test files); `"API.md"` as a path-built reader: 0 rows; control `"IMPORTER.md"` 3 rows in `OutputGuardTests.cs`. The test file's name `V0Home` is copied into no file of `web/src`, `src`, `docs`, `scripts`.
- Added lines of the four replacements: 5 (E3 is two lines), non-ASCII 0 (control planted U+200B reads 1); `git diff --check` rc 0; gitleaks 8.30.1: the scratch range rc 0, a planted `ghp_` canary rc 1; names scan on the four NEW strings (`(?<![A-Za-z])<name>(?![a-z])`, the ban list of `2026-11-10_GATE-VERIFIER-STANDARD.md` line 31) 0 hits, controls `_by_Paul_` and `B1693` fire.
- Toolchain by path: dotnet `10.0.404` at `<project>/.tools/dotnet-10.0.404/` (printed). No node needed. `timeout` is `/usr/bin/timeout` on this machine.
- Machine: load 9.06 7.04 6.60 at 08:12; free 1084 GiB; `Datasec/MPS-` panes 0 (control: `tuesday` 1); no `.heavy-lock-*` directory.

## Table: each step's inputs, and where each comes from (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 1 setup | base sha, SSH remote, deploy key, `.tools/.git-lock` protocol | exist at BASE / Stamp S2 |
| 2 predictions | the kit's counts | the kit |
| 3 base measures | clone, dotnet toolchain | step 1 |
| 4 pre-edit reads | `QuoteFigures.cs`, `API.md`, `V0Home.cs` at base | BASE |
| 5 the commit | frozen strings E1-E4, two files | kit, BASE |
| 6 checks | the commit, base sha, the two-path list, the ban-list file | step 5, BASE, `2026-11-10_GATE-VERIFIER-STANDARD.md` (exists) |
| 7 push | the commit, deploy key | step 5, BASE |

## D-decisions (mine, for Tuesday to overturn)
- D1: ONE commit (not two): no generated file changes and no sync runs (the ticket's para 5), unlike the template lane.
- D2: the E1 lead `**Shape first, values later.**` is changed to `**Shape first, then values.**` in the same sentence. "Values later" would still read as work owed. The ticket allows "say that the contract was written first and that the values are filled now, or drop the line"; I chose to keep the line, because `docs/API.md:380-384` is a bullet that reads better with its lead-in. Q1.
- D3: E2 names `QuoteFigures.ListFilter.Parameters`, a token `docs/API.md` already writes (`:386`-ish, `QuoteFigures.ListFilter.Parameters["group"]`) and the code defines at `:219`. No new identifier.
- D4: E4 keeps the file's own `B311 T-V2-2 ` prefix (it is before OLD) and the kit says the name scan covers the four NEW strings and the commit message only. "The server refused before (400 INVALID_FILTER)" is taken from the old comment's own words and marked RELAYED in the kit (a history clause the code no longer exercises).
- D5: the method name at `:67` (`..._lane_V2_builds_it`) is NOT changed (the ticket says a method name is code); the kit says why the acceptance phrases do not match it.
- D6: the seat runs the whole-solution test once at base with a cap of 1800 s (the template lane's seat measured 7 m 13 s at base and 9 m 5 s after; the drafter's own try for that lane hung, cause unmeasured), then once after the edit if base completed. The drafter ran NO dotnet test: UNMEASURED.

## Q-questions for Tuesday (each with a default)
- Q1: E1 keeps the sentence and changes its lead to "Shape first, then values."; the alternative is to drop line 379. Default: keep and change (in the kit; S4).
- Q2: the three other `lane V2` lines that remain (`Dtos.cs:464`, `V2Ready.cs:11`, `V2Staff.cs:11`) and `V0Home.cs:12` name lane V2 as the author of code; the ticket says they are not asked to change. Default: report only (S4 Q3).
- Q3: gate G3 or G2? The table's G3 row lists "comment corrections" and carries no gate; the G2 row lists "docs". The change is one docs sentence plus three comment lines with a program proof that no code moved. Default: G3 (no gate; Tuesday's completion check reads `QuoteFigures.cs:125-128`, `:149`, `:227`, the two diffs and `V0Home.cs:71-74`). If Tuesday reads the docs sentence as wanting an independent read, G2 costs one Sonnet gate; the kit has no change to make for either.
- Q4: no dotnet test is retried after a timeout (default as the template; S4).

## UNMEASURED
- Any `dotnet test` result on the edited tree (the drafter ran none; the seat's base and after runs decide; hosted CI is the arbiter).
- The seat's own `git log` identity lines and the push read-back (no git write in the project by the drafter).
- Whether the Api tests' count equals the template lane's 3663 today (main moved by the squash only).
- The literal `Failed!` as a dotnet-test failure line (a green run prints only `Passed!`; the template STATUS shows `Failed:     0` inside the `Passed!` lines).
- That the "refused before" in E4 matches an earlier build of the code (RELAYED from the old comment).

## Outside-the-fences disclosure
- Jira: GET only, via a helper I wrote in my scratchpad (`jget.py`), reading the project `.env` in-process; it printed nothing of the token. GETs: MPSCALC-411, -364, -315, -361 and two `search/jql` GETs with parentheses (`project = MPSCALC AND ( key = ... )`).
- `gh api -X GET` only, under the project `GH_CONFIG_DIR`: the main ref, compare, the paginated PR list, `matching-refs`, the contents of four files at the main sha and the main tarball (downloaded into my scratchpad and extracted there).
- I read the project's root `CLARIFICATIONS.md` (C-109), the template lane's STATUS (`1_Project_Definition/Briefs/2026-11-18_B1686_STATUS.md`, read for counts and its READY/PRIOR WORK shapes) and `git -C '<project>' rev-parse HEAD` (the root records main). I read the B1692 kit (a records kit) only through `grep` counts and one `-o` context match to decide that it shares no path in the code repo.
- `dotnet build` ran in my scratchpad copy of the tarball with dotnet 10.0.404 from the project's `.tools`; it did a NuGet restore (the same step CI does). No file in any project folder was written. I created scratch git repos (`gscratch`, `gl2`) in my scratchpad for `git diff --stat`, `--check` and gitleaks controls; they are not project repos.
- I did not read `.local/`, `Source_Documents/**`, any price book, `fleet/briefs_staged/`, `scoreboard.md`, or `_ledger.md`, and did not use `decision_queue.sh`. I typed a `cd` once by mistake (the hook refused it; nothing ran) and later a command with `rm -rf` of a scratchpad directory (the hook refused it; nothing ran).
- Files written: the three named above plus scratch files in `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/0f6ab911-939a-403c-8cca-13683e6f84b8/scratchpad` (`jget.py`, `apply.py`, `gs.sh`, tarball and edited copies, `build.log`).
