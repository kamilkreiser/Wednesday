# B504 drafter report (read-only; Datasec / HPSM-POC; drafted 2026-10-23 08:59-09:05 AEDT)

Brief written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B504_SEAT-G52_hpsmpoc-b502-gate-tier2.md` (79 lines, shape cloned from B495: Step 0 copy + cmp, Step 0b unstamped refusal, REFUSE, Stamp, HOLD, 9 checks, severity, verdict formats). Nothing launched, no one contacted, no fetch, no worktree, no node/npm run.

## Facts measured (instrument -> reading)
| Fact | Instrument | Reading |
|---|---|---|
| b461 head | `git --no-optional-locks ls-remote origin` | `a3a4679a503cf5b4f29672b68c4b7c8faba350cc` (= `refs/pull/193/head`); `refs/pull/193/merge` = `3ebf6c63...`; main `ee26d9fc...`; 08:59:13 |
| PR 193 | `gh api pulls/193` (account verified via `gh auth status`) | open, base main, 14 files, +1136 -62, 4 commits, mergeable true, state `blocked` (checks pending) |
| Delta | `gh api compare 53052201...a3a4679`, `commits/a3a4679` | ahead 1 behind 0; files `web/scripts/e2e.mjs` 91/6 and `web/src/e2e-runner.test.ts` 172/0; one parent `53052201...` |
| Alert 12 | `alerts/12 --jq` | top-level `.state` empty (null, as Tuesday measured); `most_recent_instance.state` = `fixed`, path e2e.mjs, line 303, commit `53052201...`; control alert 1 `fixed fixed` |
| Open list on PR ref | `alerts?ref=refs/pull/193/head&state=open` length | 0; without `state=open` the call returns 1 (#12, fixed) = the control; main `state=open` 0 |
| Analyses | `code-scanning/analyses?ref=refs/pull/193/head` | at `a3a4679` all four categories `results_count` 0 (old head `5305220` javascript-typescript: 1) |
| Check-runs of the head (08:59:18) | `commits/a3a4679/check-runs` | 18 runs: 14 completed success (CodeQL, 4 Analyze, vitest, web build, gitleaks, dependency review, Bicep, 5 of 6 e2e); **4 in progress**: `web e2e (playbook-mobile-2)`, `api on SQL Server (api-assessment)`, `api on SQL Server (api-other-and-feedback)`, `api (ASP.NET Core)` |
| Required contexts | `branches/main/protection/required_status_checks` | `api (ASP.NET Core)`, `web (Next.js)`, `infra (Bicep validate)`, `secrets (gitleaks, full history)`, `dependency review ...`; `web (Next.js)` is not a run name in the list above (the brief asks the gate to say which run carries it) |
| Open PRs | `pulls?state=open` | only #193 |
| CI web job | `ci.yml` at the head (GET, `-i` grep) | node 24, `npm ci`, `npm test` (= `vitest run`); no TZ/env hit found (brief says run `TZ=UTC`); lint = `eslint --max-warnings=0`, typecheck = `next typegen && tsc --noEmit` |
| Patch content | `compare` patch of both files | six exports, 11 new rows (names read from the patch); leads (i)-(vii) in the brief come from this read |
| Panes | `tmux list-panes -a -F '#{@cockpit_name}'` | tuesday, `Datasec/HPSM-POC-F1`, `-F2`, `-T1`, fleet-monitor; no `G52` |
| Load | `uptime` | 2.84 / 5.34 / 6.45 (08:59) |
| `.tools/b504`, `wt-b504-*`, `refs/heads/b504*` | `ls -d`, `ls-remote` | absent (control: `refs/heads/b46*` 7 lines; `.tools/b198`, `node24`, `b267` exist) |

## Port block measurement
- Candidate blocks checked: allocations named in `tuesday/briefs/*.md` run through 8490-8499 (B501), 8500-8509 (B502), 8510-8519 (B503). `grep -n -E '85[2-4][0-9]'` over all briefs returned only hex strings; the four `8500-8529` hits are `lsof` range checks in the B502 and B502-B503 report files, not allocations.
- `lsof -nP -iTCP:8480-8599 -sTCP:LISTEN`: empty, rc 1 (08:59). **Chosen: 8520-8529.** No positive control run by the drafter (the gate does the bind-and-free control in REFUSE).
- Live processes at 09:00 (ps): B503 vitest under `.tools/b503`, B501 `dotnet test` under `wt-b501-fix` (so the Api-suite rule is reproduced in the brief, conditional: the gate is web-only and should start no dotnet).

## Decisions made in the draft (Tuesday can overrule)
- Gate worktrees: `-base` = parent `53052201` (the "before"), `-head` = `a3a4679`, `-mut`; merge-forward onto current main is NOT built (branch is 3 ahead of an old base, 12 behind, by Tuesday's decision) and is listed NOT TESTED.
- The four property mutants of the builder brief's requirement 6 are MP1 (mode), MP2 (location in `os.tmpdir()`), MP3/MP3b (symlink, ownership), MP4 (override). Added own mutants G1-G10, U (chmod-after), W1-W3 (run-path wiring).
- **W1 survival is declared Major** (the markers' purpose on the reading side is pinned by no executed row: only one source-text row for the writing side, per the builder's M11 claim). That is my reading of the patch, UNMEASURED; Tuesday may soften it to Minor.
- Creation-time mode is judged by a `umask 000` run plus a source anchor; a chmod-after variant is expected green and reported as a limit (Note).
- Check-runs still running at the verdict: the verdict waits or says `CI pending`; a plain GO needs all completed success/neutral.
- Hard-stop time and launch time left to Tuesday (CI on the head was still running; the gate re-polls to the hard stop).

## What I could not measure
- No node/npm/vitest/mutant run (so the 70/70, 2118, 13/13 and 11-rows-red-on-parent figures are all RELAYED).
- Whether `os.homedir()` with `HOME` unset returns the passwd home (brief makes the gate measure it; stated as drafter reading only).
- Whether the `readApi` protocol permits a cheap loopback stub (Check 2c is conditional, NOT TESTED allowed).
- Which run carries the required context `web (Next.js)`.
- Whether the four in-progress checks finish green; whether Linux behaviour matches (CI Linux unit job is the only evidence).
- The Jira side: not read (no ticket was needed for the delta).

## Slots left for Tuesday (10 lines with four underscores; control: a scratch file holding four underscores reads 1)
STAMP; LAUNCH WINDOW; Stamped by; Launch authority; Hard stop; b461 head at launch; Alert 12 state + check-runs at launch; Main at launch; Model receipt + load1; and the last line `READ-WHOLE-BY-TUESDAY: DONE ____`. Self-checks run on the brief: slot count 10, at-sign pattern 0, non-ASCII 0, person-name tokens 0, decision-card ids 0.
