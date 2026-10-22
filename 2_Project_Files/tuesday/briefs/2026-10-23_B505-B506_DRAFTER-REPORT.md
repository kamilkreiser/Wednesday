# B505 / B506 drafter report (read-only; drafted 2026-10-23, measurements 09:08-09:12 AEDT)

Files written (only these three): `2026-10-23_B505_SEAT-G53_hpsmpoc-b501-telemetry-gate-tier1.md` (96 lines, tier 1 Opus, pane `Datasec/HPSM-POC-G53`, ports 8530-8539), `2026-10-23_B506_SEAT-G54_hpsmpoc-b503-gate-tier2.md` (79 lines, tier 2 Sonnet, pane `Datasec/HPSM-POC-G54`, ports 8540-8549), and this report. Launch lines are inside the briefs (`BRIEF_SEAT_LEVEL=opus` / `sonnet`). Shapes cloned: B505 from the B471 telemetry tier-1 gate (its checks, fence line, canary hunt, severity) with B504's conventions; B506 from B504.

## Facts and instruments (all read-only)
| fact | instrument | value |
|---|---|---|
| b501 head | `git ls-remote origin` | `f12cb266a80be8c536538da34fccf44180d6cda8` (control `b46*` = 7 lines) |
| main | `ls-remote` | `ee26d9fc9dc9395a08b64768179b2e16907993de` |
| b503 head = `refs/pull/194/head` | `ls-remote` | `c8b9d4caeb81dcee84e778b6e10f51d703ecc161`; `refs/pull/194/merge` = `4880e35d...` |
| b501 delta | `gh api compare 486e74e6...f12cb266` | 7 commits, 17 files, +2223 -0 (sum of the per-file table = 2223, agrees); 12 added, 5 modified |
| b501 vs main | `compare ee26d9fc...f12cb266` | diverged, ahead 7, behind 1, merge-base `486e74e6` |
| main's one move | `compare 486e74e6...ee26d9fc` | 1 commit, 19 web-only paths; shared with the 17: 0 (`grep -c -x -F -f`; control self = 17) |
| product lines | per-file table | API 547 + web 296 = 843 (builder's figure agrees); `testCapture.ts` 62 extra |
| `undici` | `web/package.json` at main | direct dependency 7.29.1 (so the web sender adds no package) |
| b501 PR / CI | `pulls?state=open`, check-runs, code-scanning | no PR; 0 check-runs; 0 analyses; 0 alerts (not scanned) |
| open PRs | `pulls?state=open` | #193 (b461), #194 (b503) |
| PR #194 | `pulls/194`, `compare`, `commits` | open, 1 file (+71 -0), 1 commit, parent `ee26d9fc`, trailer present, mergeable true / `blocked` |
| blobs | `contents?ref=` `.sha` | `dates.ts` `3db3f3fd...` equal at main and head; `dates.test.ts` `aeecd6d2...` main, `fd7f901c...` head |
| PR #194 checks 09:08 | `check-runs` | 7 completed, 11 in progress (incl. `web unit tests (vitest)`, two SQL Server legs, `api (ASP.NET Core)`, 5 web e2e, 2 Analyze); open alerts on PR ref 0 |
| required contexts | `branches/main/protection/required_status_checks` | `api (ASP.NET Core)`, `web (Next.js)`, `infra (Bicep validate)`, `secrets (gitleaks, full history)`, `dependency review ...` |
| live seats | `tmux list-panes -a -F '#{@cockpit_name}'` | tuesday, F1 (B502/b461), G52 (B504 gate of #193), F2 (B503/b503), T1 (B501/b501), fleet-monitor; no G53, no G54 |
| ports | `lsof -nP -iTCP:8480-8599 -sTCP:LISTEN` | empty (rc 1). Taken: 8490-8499 B501, 8500-8509 B502, 8510-8519 B503, 8520-8529 B504. Assigned: 8530-8539 B505, 8540-8549 B506. Word-bound grep of the briefs for 853x/854x: 0 files (control 1) |
| absent refs/trees | `ls-remote b505*/b506*`, `ls -d .tools/b505 b506`, `find wt-b505-* wt-b506-*` | none; control `.tools/b198` exists |
| account | `gh auth status`, `gh api user` | the project account (handle not quoted in the briefs) |
| load | `uptime` | load1 1.92 at 09:08 |
| brief checks | `grep -c` of four-underscore pattern; `@[A-Z_]+@`; non-ASCII; person/card-id scan | both briefs: 9 slot lines (matches the "reads 9" statement), 0 at-sign hits, 0 non-ASCII, 0 name or card-id hits; controls fired (at-sign 1, raw byte 1, underscores 1) |

## What the briefs add (so Tuesday can check my judgement)
- B505 is round 1 of 1; a NO GO ends telemetry (the brief says so, names no round 2). It makes "the app is never stopped and no response changes" a hard check (differential across five receiver modes, fault injection), re-derives every old finding id from B471's REGRESSION/FINDINGS (B431/B436/B447/B471) as closed / avoided / carried / moot including the three classes named in the task, requires the gate's own canaries and own closed grammar written before any payload, own corpus seed not in the list of used seeds, loopback-stub-only egress with the fence from the first run (and `NO_PROXY` for .NET), SQL Server rule with the PR legs read and the PR number as a stamp slot, merge prediction only in the gate's own clone, CI complete before a GO.
- B506 makes the regression test B487 named explicit as Check 2 (BD1 under `TZ=UTC` alone, 10 cells), adds BD5/BD6, the equivalent noon mutant c3 that must survive, eight test-side mutants (wrong, invalid and east-of-UTC child zone, missing import, memo, `cwd`, hang), vacuity/zone-proof and environment (`NODE_OPTIONS`, `LANG`) checks, and requires proof of real contention (the builder's first two "under load" runs made none).
- Leads I wrote from reading code (marked as leads, not findings): `ref` not derivable from request headers; token goes to the configured ingestion host; two `recordCall` lines in `bff.ts`; `onRequestError` never reads the error; route-match attacks; long accepted string turns telemetry ON silently; B506 child inherits `...process.env`.

## Could not measure
- No npm, node, dotnet, vitest, fetch or worktree was run: nothing about test results, mutants, canaries, row bytes or CI log content is measured by me; every such figure in the briefs is marked RELAYED.
- Whether the PR for b501 will exist at launch (it is a stamp slot; the brief says the gate waits and a GO needs the SQL Server legs).
- The ICU/Node 24 strings on the CI runner; Node 24 behaviour of the child (the builder ran it on v24.21.0; I did not).
- Which run carries the required context `web (Next.js)` (left to the gates).
- `gh` `mergeable` for b501 (no PR).

## Slots left for Tuesday (each a four-underscore slot; 9 lines per brief including the last line)
B505: STAMP, LAUNCH WINDOW, Stamped by, Launch authority, Hard stop + target verdict time, b501 head and main at launch, the b501 PR (number/head/base or "not yet open"), model receipt + load1, and `READ-WHOLE-BY-TUESDAY: ____`.
B506: STAMP, LAUNCH WINDOW, Stamped by, Launch authority, Hard stop, head/main/PR #194 check-runs at launch, the round rule (default written as 1 of 2; the builder brief did not state a round count, so I made it a slot), model receipt + load1, and `READ-WHOLE-BY-TUESDAY: ____`.

## Notes for Tuesday
- PR #194's `web unit tests (vitest)` and the SQL Server legs were still running at 09:08; B506 tells the gate to wait and re-read until the hard stop.
- B505 expects the PR number via the stamp slot; if the PR cannot be opened before the launch, the gate can still do everything but the PR-ledger reads and its verdict is capped at GO WITH FINDINGS (CI pending / not scanned).
- Port blocks 8530-8539 and 8540-8549 are my assignment; nothing else claims them.
