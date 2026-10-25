STARTABLE: YES (after your stamp; load, heavy slots 1 and 2 and the CI check-runs are the only waits)

# B696 drafter report: SEAT-G127, gate of MPS PR #116 (tier 2, round 1 of 2)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B696_SEAT-G127_mps-116-gate-tier2.md` (84 lines, long lines like the B692 template; slot grep reads 8, `@X@` 0, non-ASCII 0). Read whole: DRAFTER_RULES, B692 kit (both pages), B694 commission, B694 STATUS.

## BLUF
Everything the builder claims about the diff reproduces from the raw files at the head. The gate has nothing left to prove except the live parts: CI/CodeQL (still running), the dotnet job, and eslint / `playwright --list`, which need `npm ci` (kit asks you for `Q-1: YES`, which covers scratch rows and the registry install into the gate's own worktree). Drafter prediction: GO WITH FOLLOW-UPS (title/body Notes, 43 non-exact `getByLabel`, unsynced snapshot).

## Facts re-measured (instrument; clock 22:09-22:20 AEDT)
- `ls-remote`: main `a85f8bd5...` (unmoved); branch = `refs/pull/116/head` = `65f6dedc6f7429a7fbb911492c9439381ef2cee6`; merge ref `eecd679c399747f6819282287a5c13d5d757a283`. `commits/<merge>` GET: parents `a85f8bd5`, `65f6dedc`; tree `470347684cc1...` = head commit tree (`commits/<head>`). #115 `fdbe9b21`, #112 `f2102e35` unmoved. `b696*` none.
- `pulls/116`: open, not draft, 2 commits, 2 files, +2 -2, `mergeable` true / `blocked`. Compare: ahead 2 behind 0.
- Python over raw `contents` (head vs main): openapi differs on line 218 only (2165 split lines, `wc -l` 2164), parses, old sentence 1 -> 0, new sentence 519 chars ASCII no quote/backslash, found once inside the local `CLARIFICATIONS.md` line 1343 (`### C-67` heading at 1338; C-66 at 1327 and C-68 at 1348 are the controls), swap-back reproduces base line 218 True. Spec differs on line 180 only (382 split lines), head line is `getByLabel('Quote type', { exact: true })`. Non-ASCII in added lines 0. Blobs: openapi `1831d47a` -> `82a24f83`, spec `dc6cfd7f` -> `9038e41e`. `MANUAL_ITEM_FORBIDDEN` by `grep -o`: 5 -> 6.
- Commit messages and title: regex scan (key, B-number, C-nn, percent, coordinator names, non-ASCII) 0 hits (control `MPSCALC-1` = 1). **PR body** holds `MPSCALC-290`, `MPSCALC-334`, the date and a `Co-Authored-By: Claude Opus 5.5` line (commits say Sonnet 5.5). Squash settings `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`: two commits, so the squash subject is the PR TITLE (clean), body not in squash (documented, untestable). Graded Note.
- Check-runs at 22:09: CodeQL umbrella `neutral`, seven others `in_progress` (dotnet, python, web, four Analyze). Analyses on `refs/pull/116/head`: 2 (python, actions), 0 results; main control lists csharp, js-ts, python. Open alerts: PR ref 0, main 0 (no positive control for a zero; kit says so). Ruleset: CodeQL thresholds `errors` + `high_or_higher`, empty required-check list.
- CI predicate from `ci.yml` main: lines 42-43 build + test whole solution, `sql` count 0, `dotnet` 9 lines. `Api.Tests.csproj:29` links the openapi file.
- Ports 9980-9989: `lsof` rc 1 (control 7000 lists). Word-boundary scan over 144 non-`.pre-` SEAT kits of 10-24/25: 6 hits, B647 (took the block), B648, B650, B656, B659, B663, all finished lanes with no pane; zero in live kits B682-B695. Control: `996x` fires 4 lines on B694. No kit written after this one.
- Panes: no `Datasec/MPS-G127`; M26 and G125 live. `.tools`: `heavy-slot-1` and `-2` exist (other seats', not read further), slot 3 absent; `b696`/`wt-b696-*` none. Load 7.33 9.28 9.88 at 22:09. Model row G2 at `model-routing.md:109` (G-cap 111, C2 build row 92); `claude-sonnet-5-5` at `models_latest.json:23`. Round count: 27 of 241 gate/status first lines hold NO GO, none on a one-line description/spec change (B524, the nearest, GO WITH FINDINGS) so 0 of 2.

## D-decisions (override at the stamp)
- D1 Dotnet instrument: prefer the PR's own dotnet check-run (quoted, with job log), plus a narrow run of the classes reading `Contract/openapi.json` only if the check-run is pending at the verdict; whole-solution only if the check-run is red/missing. Kit requires the gate to say which was used.
- D2 Q-1 covers a scratch spec copy and `npm ci` from the registry in the gate's own worktree (mirrors your B694 Q-4); without it the eslint and Playwright re-measure is NOT TESTED and the verdict conditional.
- D3 Checks are C1 Part A, C2 Part B, C3 whole PR/CI/CodeQL/merge/hygiene, C4 STATUS/prior work/Jira; the mutant method of B692 is not used (nothing is code under test).
- D4 Whole-line hygiene scans of line 218 hit base-existing `B309`, `C-12`, `SEC-RBAC-005`, `MPSCALC-209`; the kit makes the word-level diff the judge (the builder reported the same).
- D5 Hard stop suggested 75 min target / 2 h; Tuesday fills the clocks. Port block 9980-9989 as you assigned.
- D6 Snapshot drift is a Note per your stamp; the words question (internal ids in customer-facing text) is "raised, not graded".
- D7 PR body vs squash: gated on the two-commit rule (title is the subject); body items Note.

## Q for Tuesday
- Q1 Answer `Q-1: YES` at the stamp? Default YES (needs only a registry install in a gate-owned worktree; machine already has node 26.8.1 / npm 11.19.0).
- Q2 Should the Opus attribution line in the PR body be corrected by you before landing (the squash text ignores it)? Default: leave, the gate records it as a Note.
- Q3 CodeQL csharp/js-ts were not yet reported at 22:09; if they are still pending at launch the gate waits up to 30 min beyond its last heavy job, then the verdict is conditional. Default: accept.

## UNMEASURED by me
dotnet job result; eslint; `playwright --list` before/after; the 4th CodeQL language results; whether #115 or #112 land before launch; the gauge; what the heavy-slot holders say; the live squash text.

## Outside the fences
None. Reads were `ls-remote`, `gh api -X GET` only (pulls, commits, contents raw, check-runs, runs, code-scanning, rules, repo settings, compare, git/trees), local reads of CLARIFICATIONS.md, the briefs folder, STATUS files, ci.yml copy, model files, `lsof`, `uptime`, `ls`, `tmux list-panes`. One slip: my first batch typed a `cd` inside a bash string; the hook refused the whole call, nothing ran. Scratch copies of raw files live under the session scratchpad only. No Jira, no decision_queue, no HTTP to any hosted host, no write outside the two files.
