STARTABLE: YES (MPS lane M-F, MPSCALC-407 items 1 and 2; one file owned; blocked only on Q1, the one NuGet restore, which Tuesday answers at the stamp)

## BLUF
Kit `tuesday/briefs/2026-11-16_B1640_SEAT-M151_mps-lane-mf-fleet-line-id-rows.md` (77 lines), sidecar `.measured` (96 lines, `stamp_check.py` exit 0). Main `56bfe232cbf4c98a9752f949f1f279d755565750` read 21:54:39 and again 22:00:59, no open PR. The seat adds two test methods (ROW A, ROW B) to `tests/MpsCalc.Api.Tests/FleetLineIdTests.cs` only: ROW A is the committed row that removes line 2, renumbers line 3 to 2 and changes the moved line's colour override (expected `fleet[2].monoClickOverride` 0.0125 -> null then `fleet[2].colourClickOverride` 0.065 -> 0.07; red under the mutant `Number(x)` -> `Number(o)` at `PriceAudit.cs:250`); ROW B calls `FleetLineIds.Keep` directly with two STORED lines both numbered 1 and two id-less swapped SENT lines (red under `new[] { false }` at `QuoteEndpoints.cs:1672`), and if the mutant cannot turn it red the seat records item 2 as accepted-unpinned. Item 3 (the contract wording) is out, as the commission says. Sonnet, row L6 (`model-routing.md:85`), gate G2 (`:109`). Launch name `Datasec/MPS-M151`, level sonnet inside the quotes.

## Facts re-measured with instruments (all in the sidecar)
- Main sha, open PRs 0, `matching-refs/heads/b1640` 0 (control `b1626` 1): `gh api -X GET`.
- MPSCALC-407: Backlog, 0 comments; `ctx2.py` held/dropped check: no hold window (control key 404 fires). The test file's one commit is `58320ea0` (#196).
- Pointers printed by `awk NR==n` over a tarball of main: `PriceAudit.cs:250` and `:119-124`, `QuoteEndpoints.cs:1653` (Keep), `:1665-1671`, `:1672`, `:1680-1681`; `FleetLineIdTests.cs` helpers and rows (R1 `:112-134`, class closes `:324`); no `R12_`/`R13_` name exists (control `R11_` found).
- The id-bearing test files are exactly two (`FleetLineIdTests.cs`, `FleetLineIdStoreTests.cs`), so neither pin exists anywhere else. `PricingPolicy.cs` has 0 `ClickOverride` hits (control `PriceAudit.cs` 2), so ROW A can be a Theory over both metrics settings like R1.
- Toolchain: dotnet `10.0.404` at the project's `.tools/dotnet-10.0.404`; `Directory.Build.props:6` TreatWarningsAsErrors true; CI `ci.yml:42-43`. Machine cache holds Xml `10.0.13`, the csproj pins `10.0.15` (`MpsCalc.Api.csproj:32`): the NU1102 restore failure is RELAYED from B1626's STATUS, not re-run (a restore is not mine to run).
- Load 7.78 at 21:56; no `heavy-lock` or `git-lock` folder, no `b1640` folder; no `Datasec/MPS-*` pane.

## Template deviations (named)
- B1626 is the nearest dotnet kit and was taken for shape, HEAVY protocol, restore and push form; its two loops and the counted-load rules are dropped (no timing question here). B1617 contributed the stamp slot list. There is no STATUS 'Deviations' section in B1626's or B1617's file (section headings read: Step 0, Toolchain, BLUF, PINS, PRIOR WORK, BASELINE, PREDICTIONS, PART A, PART A LOOP, PART B, CHECKS, RESIDUE, NOT RUN, FOR TUESDAY, Trees left, Commits); its Part B facts (NU1102, one registry restore, 91 tests 53 s) were carried as RELAYED only.
- Fully qualified type names are mandated for ROW B so the diff adds no `using` line and removes none (`git diff -U0` removed lines 0 is the kit's property).

## D-decisions
- D1: ROW B uses a direct `FleetLineIds.Keep` call, because an HTTP save cannot send a repeated line number (refused 400, `FleetLineIdTests.cs:274-278`) and the only HTTP route to two stored lines numbered 1 is `FleetLineIdStoreTests`' private `MakeOld`, in a file this lane does not own.
- D2: the unsure branch is explicit: ROW B is committed only if mutant mB turns it red; otherwise item 2's own second branch (accepted-unpinned, one recorded sentence) applies, and the same mutant must leave every existing row of both fleet line id files green (the ticket's premise, measured by the seat).
- D3: planted mutants edit product files in the clone and are undone with the Edit tool, `git diff --quiet -- src` proving it; the path property (only the one test file differs base to head) is the landing check.

## Q-questions for Tuesday (each with a default)
- Q1: allow ONE registry restore of the single id `System.Security.Cryptography.Xml` 10.0.15 through a seat-local nuget.config and its own `--packages` folder (the form B1626 used and Tuesday answered YES to)? Default: YES. If NO, the seat stops at Step 2 with `STOPPED: NEEDS TUESDAY Q1 is no`.
- Q2: row L6 and gate G2 as the commission names. Default: yes.
- Q3: launch order. The sweep default is MPS M-F, M-S2, M-E2 one waiter at a time; this lane is path-disjoint from both siblings (they write only `web/**`) but all three share the heavy-lock slots. Default: M-F first (the only one needing dotnet, hence the registry restore).
- Q4: no ruling is asked on item 3's wording.

## UNMEASURED
- ROW A's and ROW B's expected values are DERIVED from the source and not run: no restore, build or test was run by the drafter (a restore needs the registry request of Q1). The mutants' red results, the baseline count of the two files, the 9 + 3 attribute count with the Theory expanded, and the whole-solution build and test counts are the seat's measurements.
- 11 of the 15 origin branches whose names hold fleet/line/audit/407/170/195/198 were not compared against the lane's one path; the seat's PRIOR-WORK check does that.
- Whether a seller without internal-metrics changes the moved line's override the same way (the Theory's `false` case): derived from `PricingPolicy.cs` holding no override token; the kit lets the seat degrade that case to a Fact with the reason named.
- Hosted CodeQL for C#: not runnable locally (arm64 extractor); the kit says NOT RUN.

## Inputs table (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Source |
|---|---|---|
| 0 | the kit, project `.tools`, df, uptime | exist at launch |
| 1 | origin main sha (S2), Jira 407, branches | gh/Jira GET, no earlier output |
| 2 | clone from step 1, csproj and `global.json` at base, nuget.config written in step 2(b) | steps 1, 2(b) |
| 3 | baseline list from step 2(d) | step 2(d) |
| 4 | helper methods `ThreeLines`, `Create`, `Read`, `Save`, `Audit`, `Ids`, `Numbers`, `WithoutIds` (all in the file at base); the two product lines for the mutants (at base) | base |
| 5 | the commit from step 4; the ban list file `2026-11-10_GATE-VERIFIER-STANDARD.md` (exists) | step 4, base |
| 6 | the checked commit | step 5 |

## Outside-the-fences disclosure
- Wrote only: the kit, its `.measured` sidecar, this report, and scratch under `fleet/state/s284/b1640/` (`build_kit.py`, `measure.py`, `fill.py`, `M.json`, a tarball and tree of main, the first two sidecars moved to `old.measured` and `old2.measured`). No push, PR, Jira write, mail, board write, `az`, deploy, `cd`, dotnet run, Artifact tool. `decision_queue.sh` not called at all. No token printed. The ledger and `fleet/briefs_staged/` were not read. Reads: the commission, DRAFTER_RULES, SWEEP-2150, B1626/B1617/B1623 kits and the B1626 STATUS, `gh api -X GET` (ref, pulls, branches, commits, compare, tarball of main) under the project's own `GH_CONFIG_DIR`, `jdesc.py`/`ctx2.py` copies from the sweep scratch folder (GET-only).

DRAFTED B1640: kit 77 lines, sidecar rc 0, questions 4
