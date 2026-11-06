STARTABLE: YES, after Tuesday fills the slots (S2 = the head sha40, S3 = MAIN plus the base sha40). The builder has READY (its STATUS last line, read at 11:00) and the branch is at origin. No decision is needed before the stamp; each Q below carries a default.

# Drafter report: B1321 SEAT-G349, tier-2 gate of b1311/hpsmpoc-review-door-pins (drafted 10:59-11:05 AEDT 2026-11-06)

## BLUF
Kit `2026-11-06_B1321_SEAT-G349_hpsmpoc-review-door-pins-gate.md` (50 lines; `grep -c -E '_''_''_''_'` prints 8: seven slots and the last line) plus `2026-11-06_B1321_slots.json` (8 keys, parsed by python). Sonnet, row G2 (`model-routing.md:109`, cap `:111`, id `models_latest.json:23`). Round 1 of 2 on the new class "review door pins". The gate re-runs the five plants at source (P0, PC, P-H1, P-H2, P-G1 with the 5 Expected/Actual pairs each), runs five plants of its own (X1 guard only for review calls, X2 HEAD on the attachments path, X3 a 14th closed write, X4 one header variant dropped, X5 PATCH out of MUTATING), reads the comment's three claims against `web/src/proxy.ts`, `bff.ts`, `AppShell.tsx`, tests whether the 13 and 52 counts can drift, and runs audit-dev, lint, typecheck, build, check-shards and the whole `npm test` at the head. A security-shaped finding in the door is a STOP to a tier-1 gate, never fixed. No listener, no port, no hosted call.

## Facts re-measured (instrument; control)
1. Refs 11:00 (`gh api -X GET`): main `13ac7d7e86a5675ee20eb987c62818e357599358`; `matching-refs/heads/b1311` one row `a2ad692f8d42ea6ab19361d52cbec3d3dfe35da8` (control `matching-refs/heads/b1295` length 1); open PRs 0; commit `a2ad692f` one parent `13ac7d7e`, files `reviewDoor.test.ts` +41 -0, `reviewDoor.ts` +1 -1; compare ahead 1 behind 0.
2. Every `file:line` of the kit was printed by `cat -n` or `awk NR==n` over raw contents at `a2ad692f` (reviewDoor.ts 33 lines, reviewDoor.test.ts 214, bff.ts 470, web/src/proxy.ts 136, AppShell.tsx 208, guard.ts 61, ci.yml 682); the three new `it(` rows are at `:136`, `:145`, `:154`; counts asserted at `:156`, `:164`, `:174`. `web/src/server/proxy.ts` does not exist (fetch printed 0 bytes), so the comment's "proxy.ts" is `web/src/proxy.ts`.
3. CLOSED at `:63-94`: 30 entries, 17 GET and 13 not-GET by my count of the listing (1 PUT, 1 PATCH, 7 DELETE, 4 POST); the gate re-counts by program.
4. Round count: shell loop over 707 `Briefs/*STATUS.md` first lines at 11:00: 162 open with `GATE VERDICT`, 15 match `door|pins`; none judges a review-door-pins class (B1305 is the door, GO WITH FINDINGS; B981 is a different pins class). Controls: both are hit.
5. Panes (`tmux list-panes -a`, names): wednesday, HPSM-POC-D56, H128, H129, R178 live; no G349 pane, no H127 pane. Partition reads: H128 `web/e2e/mock-rows.spec.ts`, H129 `web/src/e2e-runner.test.ts` and `ci.yml`, R178 records and Jira, D56 Azure and Entra (the brief's own partition); none touches the two paths.
6. CI predicate read from `ci.yml` at the head: `web-build` `:371` (audit-dev `:395`, lint `:396`, typecheck `:409`, build `:413`, check-shards `:426`), `web-unit` `:450` (`npm test` `:478`), `web` `:529`; scripts `web/package.json:10-12`. No e2e, dotnet or workflow path in the diff, so those legs are not run.
7. Landing source: records `CLARIFICATIONS.md` (5646 lines at 11:00), `grep -n -i 'head-pinned squash'` last hit `:5636` (C-299, PR #287 and #288, head-pinned squashes). Model rows: G2 `model-routing.md:109`, cap `:111`; `models_latest.json:23` is `claude-sonnet-5-5`.
8. Ports: none assigned and none needed (the rows call `handleApi` and `proxy` in process; the build and check-shards bind nothing). No lsof or kit scan run; the kit makes a listener a STOP.

## D-decisions
- D-1 The gate stays Sonnet G2 and hands a security-shaped door finding up as a STOP, per the G2 counter column.
- D-2 The builder's table is re-run verbatim and the "all 5 visitors" wording is judged from the gate's own 5 pairs (the builder says 4 of 5 differ).
- D-3 The 13 and 52 counts are tested by plants (X3, X4), not only by reading.
- D-4 The door's openness, rate limit, audit identity and reach are named NOT findings (the product owner's 6 Nov ruling), and the PR text must say the door is not changed.
- D-5 PR title, body, squash subject and squash body are files in the evidence folder; each sentence read at source; no name, card id or B-number.

## Q-questions for Tuesday (each with a default)
- Q-1 Port block? Default: none.
- Q-2 Gate tier: stay G2 (tests and one comment, no product byte)? Default: yes; a security-shaped finding becomes a STOP for a tier-1 gate.
- Q-3 Round count: round 1 of 2 on "review door pins", NO GO 0 before? Default: yes.
- Q-4 Run the e2e shards, dotnet and SQL Server? Default: no (nothing in the diff reaches them).
- Q-5 Hard stop: Step 0 + 90, target verdict Step 0 + 60? Default: yes. Latest-start clock is yours at the stamp.

## UNMEASURED
Every other use of `isReviewCall` and `isReviewPage` in non-test source (the gate's tree search); whether "the laptop" in the comment is exactly the `mock` mode (`config.ts` `resolveAuth` not read by me); the commit subject length (101, the builder's count); the plants' reds (read, not run); a cross-site write with a level cookie to a closed path (whether any row pins it); H128, H129, R178 and D56 branches' paths at the stamp (the gate re-runs the compare).

## Outside the fences
None. Read-only: DRAFTER_RULES, the two B1305 files and B1311 kit, slots, report and the builder's STATUS (a RELAYED claim file), `model-routing.md` (grep and awk), `models_latest.json` (grep), `gh api -X GET` (ref, matching-refs, commits, compare, pulls, contents raw at the head, records `CLARIFICATIONS.md`) under the project's `GH_CONFIG_DIR`, `tmux list-panes -a` names, `ls`, `df`, `uptime`, a shell loop over the STATUS first lines. Raw files kept in the session scratchpad. No git command in a project repo, no decision card, no Jira call, no hosted call, no mail, no ledger, no staged briefs, no scoreboard, no WEDNESDAY or FRIDAY tree, no cd typed. Two refused hook calls at the start (a `cd` and a bare `====`); neither ran.
