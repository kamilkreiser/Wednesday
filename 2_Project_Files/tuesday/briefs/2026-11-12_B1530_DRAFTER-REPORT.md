STARTABLE: YES (after Tuesday stamps the 12 slots; no blocker found; one condition below on main having moved)

# B1530 DRAFTER REPORT (drafted 2026-11-12 10:21-10:29 AEDT, `date` printed 10:21:22, 10:23:53, 10:26:26, 10:28:58)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1530_SEAT-M128_mps-389-391-sdk-guard-picker-spec.md` (96 lines, ASCII, 0 non-ASCII bytes by python; `____` count 12 = S0-S10 plus the last line, same count by the split-quote grep). Seat `Datasec/MPS-M128`, branch `b1530/mps-389-391-sdk-guard-picker-spec`, TWO commits (one per ticket) on the one branch, plain push, no PR, not deployed. Model row C2 (`model-routing.md:92`), `claude-sonnet-5-5` (`models_latest.json:23`), launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, gate after G2 (`model-routing.md:109`). Port block 9850-9859.

## BLUF
- Main moved during drafting: `baf0aabec3c02457072ee848b166b17d3d7b0e80` at 10:21, `793d0a9c52c961852b4a1f04bb826ffff752ce74` at 10:26 (one commit, #185's squash: `FeedbackStore.cs` and three files under `tests/MpsCalc.Api.Tests/`). Open PRs 0. The blobs of all four files the kit reads (`test_sdk_pin.py` f502ffd4, `playwright.config.ts` 9dbc5a1d, `b100-picker-many.spec.ts` a1e4c15, `ci.yml` de0ac3b5) are identical at both shas. The kit names 793d0a9c as the drafter's base; Tuesday re-reads for S2.
- MPSCALC-391 is bigger than its ticket says. The "seventh row" is a page-estimate sub-row (`PageEstimateRow.tsx:30`, `<tr className="bom-subline"><td />...`, rendered at `PurchaseBomEditor.tsx:484` after each device line). The spec reads that row in THREE places (`toHaveCount(6)` `:58`, `td:nth-child(2)` `:59`, `td:nth-child(1)` `:61`), so changing the literal 6 to 7 would turn the spec red at `:60` or `:62`. D-9 scopes the reads to line rows and measures the sub-row count from the rendering (B1). I did not run the spec (read-only drafter, no checkout); which SKU is a device is UNMEASURED.
- MPSCALC-391 runs in the **stub CI step only**: `playwright.config.ts:35` `testMatch` (api-off) lists only `STUB_OFF_ONLY` and `BOTH_MODES`, and the spec's `beforeEach` skips when "API STUB ON" is absent (`:37`). The kit has the seat prove it by `--list` in both modes, 3 runs in the stub shape, a stub-OFF run reading 2 skipped, and one whole stub-step run at head (heavy).
- MPSCALC-389: the drafter ran the gaps on the base guard (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1530/probe.py`): double- and single-quoted `dotnet-version` return `[]` (control: the unquoted plant returns its one problem); workflow-level `DOTNET_ROLL_FORWARD` returns `[]`; a repeated `global-json-file` returns `[]` (first value kept, `:84`); a `dot.net/v1/dotnet-install.sh` run step returns `[]`; a flow-style `with: {...}` returns a misleading cause. Red-first rows are planted on copies and are red by assertion (stubs first, so a missing name is not the red).

## FACTS RE-MEASURED (instrument; control)
- Main, open PRs, `^b15` branches: `gh api -X GET` git/ref, pulls?state=open, git/matching-refs/heads/b15 (9 branches); control `matching-refs/heads/b1526` 1 row. `b1527*`, `b1528*`, `b153*`: 0 rows.
- Lane check: `compare main...<branch>` for all 9 `^b15` branches. Hits on my files: b1502 (`playwright.config.ts`, `ci.yml`) and b1520 (`test_sdk_pin.py`, `global.json`, `docs/ENGINE.md`); both are #178 and #183, closed and merged (`pulls?state=all&head=datasecau:<branch>`), and the branches' blobs for my files equal main's. Control: the b1520 list prints `test_sdk_pin.py`. The other seven lists name none of my paths. B1527 and B1528 granted paths read from their stamped kits' partitions (B1527 kit not re-read whole by me; I used the partition you listed and the B1528 kit text): none of my three paths.
- Panes: `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` printed `%0 tuesday`, `%1 fleet-monitor`, `%138 Datasec/MPS-M127`, `%141 Datasec/MPS-M126`, six unnamed. No M128.
- Ports 9850-9859: `lsof -nP -iTCP:9850-9859 -sTCP:LISTEN | wc -l` 0 (control: 13 listeners machine-wide). Digit-bounded scan of 44 non-`.pre-` SEAT kits of 11/12 Nov: 0 files for `985[0-9]` (control `984[0-9]`: 3 files, B1488, B1527, B1528). The first control attempt with `-` in the boundary class read 0 for `984x` because the B1528 kit writes the range `9840-9849`; I replaced it with a digit-only boundary and the control fired.
- Jira (read helper written in my scratch folder, reads the project `.env` in-process, token never printed): MPSCALC-389 Backlog updated 2026-11-11T22:26:13, MPSCALC-391 Backlog updated 22:26:21, 0 comments each; control MPSCALC-361 Done. JQL `project = MPSCALC AND ( key = ... )`.
- CI predicates read from `ci.yml` at base with `grep -n`: python job `:84`, loop `:102-107`; web job `:45`, steps `:61 :62 :63 :73 :79 :82`; `env:` `:25-27` (two DOTNET names); `setup-dotnet` `:38`, `:118`; `bash scripts/package.sh` `:130`.
- Tree (705 blobs): one `global.json`, no `dotnet-install*`, one workflow file; `scripts/package.sh` and `run-demo.sh` DOTNET usage read (package.sh: none; run-demo.sh sets `DOTNET_ROOT` for laptops, outside CI).
- Tools: `codeql` not installed (so the kit uses regex pre-scans with planted controls for both Python and JS/TS), `gitleaks` and `pdftotext` present, `python3` 3.9.6 (kit forbids newer syntax). Heavy locks none, `.git-lock` absent, `.tools/b1530` absent, df 1281 GiB free.
- Project identity email non-empty (1 line with `@`).

## D-DECISIONS (all in the kit, DECISIONS section)
- D-1 scope: guard only; no change to `global.json`, `ci.yml`, `package.sh`, csproj, SDK install. D-2 quoted keys plus fail-closed on unreadable forms (flow mapping, anchors, block scalars, repeated key). D-3 `DOTNET_*` env as an ALLOW-list of the two names at `ci.yml:26-27` (deny-lists miss `DOTNET_ROOT`, `..._ON_NO_CANDIDATE_FX`, `DOTNET_INSTALL_DIR`). D-4 install tokens (`dotnet-install`, `dot.net/v1`, `--roll-forward`, `RollForward`, other dotnet `uses:`). D-5 scripts CI runs: closed list `scripts/package.sh`, derived from `ci.yml` run lines. D-6 nested `global.json` walk over a root parameter. D-7 host refusal text NOT changed (not ours); the docstring records what the host prints and `pin_note()` makes the guard's own failure name the pin. D-8 same file. D-9 391 fix: line rows `:not(.bom-subline)` = 6, sub-rows = a measured literal, reads at `:59` and `:61` scoped to line rows, and the single `LEFT_OUT` entry at `:18` deleted.
- Two commits instead of the template's one, because the tickets are independent and Tuesday can see which ticket a red belongs to (Q-1 default below).

## Q-QUESTIONS FOR TUESDAY (each with a default; the kit's S4 slot carries them)
- Q-1: two commits on the one branch (one per ticket). Default YES.
- Q-2: the guard's `DOTNET_` allow-list is exactly the two names at `ci.yml:26-27`; a future harmless name costs one deliberate edit. Default YES.
- Q-3: the sub-row count in the spec is a measured literal (with a comment), not computed from the page. Default YES.
- Q-4: one whole stub-step Playwright run at head (heavy slot), for the ticket's "the step's census rises by the spec's rows" beyond the `--list` proof. Default YES.
- Q-5: D-7 changes no refusal text; `pin_note` and a docstring paragraph instead. Default YES.

## UNMEASURED
- Whether the spec's test 2 is green at base, and which of the six SKUs is a device (B1 measures both). The `td:nth-child` consequence is DERIVED from `PageEstimateRow.tsx:30`, not run.
- Linux behaviour of everything (hosted CI is the first Linux read); Python 3.12 on the runner vs 3.9 here.
- Whether `.cs` tests read `playwright.config.ts` (a code search for `LEFT_OUT` listed `.cs` files, which probably use the name for something else; the kit makes the seat read them). The code search index is partial (5 hits), so it is not an absence proof.
- The B1527 kit was not read whole by me; I took its granted paths from your message.
- Run-time of the seat (150-minute READY default is a guess, three Playwright shapes at 3 runs each plus one whole stub step plus two heavy builds).

## OUTSIDE THE FENCES (disclosure)
- Wrote only the two files in `briefs/` plus scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1530/` (jira_get.py, probe.py, base file copies, tree.txt, compare.txt, ticket text files, `src/` copies of `web/src/screens/bom/*.tsx`).
- Also wrote `/private/tmp/claude-501/kits.txt` (a list of kit file names for the port scan), outside the scratch folder; read-only list, nothing else.
- Read the project `.env` in-process in the Jira helper (as the template kits do); read `Datasec_DEV` project `CLAUDE.md` and `JIRA.md`. Did not read `fleet/briefs_staged/`, scoreboard, `_ledger.md`, any other client tree, or any card. No hosted site called; the Jira GETs and `gh api -X GET` (including one `search/code` GET) are the only external reads. No `cd`. One earlier Bash call was refused by the no-cd hook (I had typed `cd /tmp`); re-issued without it.
- I ran the base guard's `problems()` on planted COPIES held in memory (scratch probe), never on the repo's checkout.
