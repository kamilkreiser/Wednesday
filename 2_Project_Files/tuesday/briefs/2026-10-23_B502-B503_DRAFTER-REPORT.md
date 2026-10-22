# B502 + B503 DRAFTER REPORT (2026-10-23, drafted 08:27-08:40 AEDT, read-only)

Briefs: `2026-10-23_B502_SEAT-F1_hpsmpoc-b461-codeql-tempfile.md` (126 lines) and `2026-10-23_B503_SEAT-F2_hpsmpoc-b487-1-bare-day-test.md`. Shape cloned from B496 (SEAT-L4) with B496 ADDENDUM-1 and B490 ADDENDUM-3 conventions. Every Tuesday decision is a four-underscore slot. Nothing was launched, fetched, committed or sent; the only writes are these three files (plus scratch files in the session scratchpad).

## Slots left for Tuesday
- B502 (10 lines with the four-underscore pattern, counted by program: 9 slot lines + the last line): `STAMP`, `LAUNCH WINDOW`, Stamped by, Launch authority, Hard stop/target READY, b461 head at launch, Alert 12 state at launch, **LIVE PASS PROOF (yes/no: one real desktop live-API pass in the seat's block, or refusal-path proofs only)**, Model receipt + load1, and `READ-WHOLE-BY-TUESDAY`.
- B503 (11 lines: 10 slot lines + the last line): `STAMP`, `LAUNCH WINDOW`, Stamped by, Launch authority, Hard stop/target READY, Main at launch, **BD2 scope (report | build)**, **Z1/B487-2 scope (no | yes)**, **rename the existing bare-day row (no | yes + name)**, Model receipt + load1, and `READ-WHOLE-BY-TUESDAY`.
- Launch order, pane re-check (F1/F2 free at 08:27; fallbacks F3/F4 named) and model row are Tuesday's.

## Facts and instruments
| Fact | Instrument |
|---|---|
| gh account is the project's (`gh auth status` under the project `GH_CONFIG_DIR` read the Datasec account, active) | `gh auth status`, 08:27 |
| main = `ee26d9fc9dc9395a08b64768179b2e16907993de`; b461 = `53052201a9680b1ce396b782d6788d67f6ec7ac2`; no `b502*`/`b503*` ref (`b50/feedback` only) | `git ls-remote --no-optional-locks origin refs/heads/main 'refs/heads/b4*' 'refs/heads/b5*'`, 08:27 and 08:30 |
| PR #193 open, head = b461 sha, base main; it is the only open PR | `gh api pulls/193`, `pulls?state=open` |
| b461 vs main: diverged, ahead 3, behind 12, 14 files (list in B502) | `gh api compare/ee26d9fc...53052201`, `compare/main...b461` |
| Alert #12 open, `js/insecure-temporary-file`, security high, rule severity warning, `web/scripts/e2e.mjs` line 303, commit 53052201; PR-ref alert list holds only it; main's list holds only #1 (fixed) | `gh api code-scanning/alerts?ref=refs/pull/193/head`, `...ref=refs/heads/main` |
| Rule help text (CWE-377/378, "use tmp library", owner-only + not pre-existing) | `gh api code-scanning/alerts/12 --jq .rule.help` |
| `MARKERS` at line 250, `readMarkers` 251, write at 303, `dataDir` with `Date.now()` at 340; 402 lines at the head; main's file is 122 lines with 0 `MARKERS`/`tmpdir` | `gh api contents?ref=<sha>` raw, saved to scratchpad, `grep -n`, `wc -l`, `grep -c` |
| Markers purpose: cross-run record of seeds that already ran a pass; `liveApiRefusals` refuses ("already ran a pass"); gates used `E2E_LIVE_API_MARKER=<path under .tools>` | read of `e2e.mjs` 100-170/250-303, `live-api-preconditions.mjs` header, B461/B475/B479 STATUS greps (lines cited in B502) |
| CodeQL check failure text; four `Analyze (...)` runs completed success at 08:30 (csharp too) | `gh api commits/53052201/check-runs` |
| "csharp configuration not found" warning | MEASURED-BY-TUESDAY only (relayed in the commission); not re-observed: it is stated as such in B502 |
| HPSMPOC-310 = PR #192, squash `merge_commit_sha` = main `ee26d9fc`, head 6182defd; 19-file list; the two code/test paths are `web/src/lib/dates.ts` (34 lines) and `web/src/lib/dates.test.ts` (60 lines) | `gh api pulls/192`, `gh api compare/486e74e6...ee26d9fc --paginate`, `gh api contents` raw |
| Bare-day product line 11; bare-day row at test lines 55-59 | read of both files at main |
| B487-1 text, BD1 mutant, fix-shapes, M480-DEF, Z1, B487-7 | B487 STATUS read WHOLE (187 lines) |
| CI has 0 `TZ` lines (control `NEXT_TELEMETRY_DISABLED` 3); web unit job runs `npm test`; vitest config: jsdom, no `pool` setting | `gh api contents` of `ci.yml` (678 lines) and `vitest.config.mts`, `grep -c` |
| Type-stripped import of `dates.ts` under `TZ=America/Los_Angeles` prints `10 Oct 2026`, `1 Jan 2026`; `new Date("2026-10-10")` / `("2026-01-01")` give `9 Oct 2026` / `31 Dec 2025` | `node -e` on a scratchpad copy; **Node v26.8.1 on this machine, not Node 24** |
| Live panes at 08:27: `tuesday`, `Datasec/NexusAI-M1`, `Datasec/HPSM-POC-T1`, `fleet-monitor` (F1/F2 free) | `tmux list-panes -a -F '#{@cockpit_name}'` |
| Ports: F1 = 8500-8509, F2 = 8510-8519; `lsof` on 8500-8529 empty (rc 1); no brief names an 85xx block (only `8570` twice, as a bare number); other blocks in use: B496 8440-8449, B490 8390-8399, B493 8410-8419, B495 8430-8439, B501 8490-8499, and 8450-8489 (B497-B500) | `lsof -nP -iTCP:8500-8529 -sTCP:LISTEN`; `grep -o -E '8[0-9]{3}-8[0-9]{3}'` over the 10-22/10-23 briefs and the per-brief port lines |
| `.tools/b502`, `.tools/b503`, `wt-b502/3-*` absent; `.tools/b198/lock.sh`, `.tools/b267/waitload.sh` exist | `ls -d`, `ls | grep -c` |
| load1 3.17 at 08:27 | `uptime` |
| B501 "Yours" list | read of `2026-10-23_B501_SEAT-T1_hpsmpoc-telemetry-smaller.md` PARTITION |

## Partition intersection (program: `scratchpad/intersect.py`, run with `python3 -I`)
Yours: F1 = `web/scripts/e2e.mjs`, `web/src/e2e-runner.test.ts`; F2 = `web/src/lib/dates.test.ts`; T1 = the 14 B501 paths/prefixes (exact paths and `/`-ending prefixes).
```
F1 B502 x F2 B503: n shared = 0 []
F1 B502 x T1 B501: n shared = 0 []
F2 B503 x T1 B501: n shared = 0 []
controls: planted shared path F2+T1: 1 (want 1) | self-compare F1: 2 (want 2) | prefix control: 1 (want 1)
```
Seat-vs-lane (13 `compare main...branch` file lists): F1 shares 2 with b461 only (its own branch; control 2 = ok); F2 shares 1 with b465 (`dates.test.ts`; b465 is PR #192's already-merged history branch, listed as not a stop); T1 shares 42 with b429 (parked, expected per B501) and 2 with b496 (`web/package*.json`; PR #190 is merged, history branch). All other lane/seat cells 0. **Intersection of the three seats' Yours: EMPTY.** Caveat: `compare main...<branch>` for squash-merged branches lists the whole branch diff, so those hits are history, not live overlap; which of b459/b460/b462/b467/b472 are merged was not established (all show 0 shared anyway).

## What I could not measure
- CodeQL itself: whether the fix form clears `js/insecure-temporary-file` (no local run; B502 makes the PR's CodeQL run on the new head the instrument and requires a bounded poll). Whether `mkdtempSync` under `os.tmpdir()` is accepted by the query is unknown, so B502 requires a per-user default for the markers.
- The "csharp configuration not found" warning (relayed; by 08:30 `Analyze (csharp)` was success; whether the warning remains on the PR is unknown).
- Node 24 behaviour of the type-stripped child import (measured on Node v26.8.1 only); vitest's installed version (config asks `^5.0.5`), the default pool in that version, the CI runner's zone and ICU output.
- Whether any suite count (no npm install/ci/test, no build, no worktree, no fetch was run); whether the new rows go red under `--pool=threads` and which cells BD3/BD4/BD2 are killed in.
- The pickup note "(B487-1; + B479-1 runner env if partition allows)": I did not find the pickup file; the text is cited as relayed. B479-1's text comes from the B479 STATUS headline and Check 3 (read by grep, not whole).
- Whether `web/AGENTS.md`/`web/CLAUDE.md` impose rules (the briefs tell the seats to read them).
- Whether b459/b460/b462/b467/b472 are merged.

## Choices to review
- B502 forbids a README edit even though the marker's location may deserve a line; the README does not name the marker today (grep), so the briefs only report it.
- B502 requires the default markers location to be per-user (not the shared temp directory) because a one-shot random name would break the cross-run purpose; the exact location is left to the seat.
- B503 prefers a child process pinned to `America/Los_Angeles` over a runtime `TZ` switch (vacuous under `threads`, as the gate said) and asks for a 5-zone x 2-pool red matrix for BD1 plus BD3/BD4; BD2 (east-of-UTC mirror) and Z1 are slots, not defaults.
- Timestamps in the briefs are the times read from `date` output in my commands (08:27, 08:30); no time was typed from memory. The drafter's two `Write`/`Edit` tool constraints meant no `date` substitution inside file bodies.
