STARTABLE: YES

# B1025 DRAFTER REPORT | SEAT-H90 | HPSM-POC round-2 pins, class "customer security preview, part B" (HPSMPOC-388), ROUND 2 OF 2 (THE CAP)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1025_SEAT-H90_hpsmpoc-388-part-b-round2-pins.md`, 206 lines (`wc -l`), sha256 prefix `87778f4a55e7d772`; `.pre-stamp` beside it is an exact copy (`cmp` rc 0, same sha256). Drafted Sun 1 Nov 2026 07:2x-07:4x AEDT, read-only.

## BLUF
One forward commit (at most two) on `b1016/hpsmpoc-388-security-workspace-part-b` @ `db9c2625`, TEST PATHS ONLY, that closes B1022-1 (g3), -2 (g4), -3 (g18), -4 (g14). The kit spells: (1) two default-empty maps in `testing/harness.ts` (`assessmentsFor` by customer API id, `reportsFor` by assessment id with `"pending"`/`"fail"`), ADDED lines only, line 13 (the g14 anchor) byte-equal, so every existing row gets the same answers; (2) one `issuedRow` row in `reports.test.ts`; (3) three rows in `SecurityReports.test.tsx` (stale row on rerender to a second customer whose read never answers; two issued runs, newest withheld vs newest approved, with the read URL list asserted); (4) one two-run row in `SecurityRoadmap.test.tsx` (newest in progress, older scored); (5) one added line in each of the four no-write role rows asserting exactly one GET to `/api/v1/assessments/ASM-2/reports`. 5 new rows + 4 tightened; expected 3777 -> 3782, 258 files. Every row must be GREEN at the head and RED under its own re-made plant; p5/p6/p7 re-run to prove the harness lines left the release rows' meaning. Non-test blobs proved equal to `db9c2625` by an `ls-tree` program with a control (77c3132e..db9c2625 flags product paths). No timers, no new test file, no row pins the A2 reading (B1022-7). e2e not run (product bytes unchanged; the gate's 416/46/0 relayed). Sonnet (C2 line 92). Launch through `launch_when_cool.sh`, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Facts re-measured (instrument; control)
- Seat: H90 free. Word scan `/usr/bin/grep -rlw H90` over `2_Project_Files/tuesday/` 0 files; control `H89` 10 files. Panes (`tmux list-panes -a`): `%0` tuesday, `%140` Datasec/MPS-R106, `%139` Datasec/NexusAI-G253, `%1` fleet-monitor: no HPSM-POC pane.
- B-number: 0 `B1025` names in `tuesday/briefs/` and in the project `Briefs/` (control `B1022` 3 in `Briefs/`).
- Refs (`git --no-optional-locks ls-remote`, shared `2_Project_Files`): branch `db9c2625815b78db19419380c5cb55a41b37f43b`; main `77c3132e213b24616e6f1af9379d2fee66c889b7`; `refs/heads/b1025*` 0 (control `b1016*` 1). Open PRs 0 (`gh api -X GET pulls?state=open`; control `state=closed&per_page=3` = [268, 267, 266]). `cat-file -t db9c2625` = commit.
- Delta: `git diff --numstat 77c3132e db9c2625` 31 paths (matches the gate). Commits: e4019e7, 8a7c872, db9c262.
- Plant anchors (from the gate's `.tools/b1022/plants.py`, read as data): g3, g4, g14, g18, p5, p6, p7 each count 1 at `db9c2625` (`git show | /usr/bin/grep -c -F`); zero control `NOSUCH-zz7f3a-b1025` 0.
- Test-only folder: `git grep -l -E 'testing/(harness|fixtures)' db9c2625 -- web/src` = 20 files, 20 of them `*.test.ts(x)`, 0 others (matches gate C2 "20 test files and 0 product files").
- Harness at head (49 lines): the assessments route answers the same two runs (ASM-2 report-issued when `world.issued`, ASM-1) for every customer; the reports route answers `world.reports` for every id; the result route the same result for every id: the cause of g4/g18 surviving, as the gate says.
- `useAsync` (`web/src/lib/use-async.ts` 7-23): the effect does not reset `state` on a key change, so the previous answer stays while a new key loads (the g3 mechanism, confirmed at source).
- `customerForRoute` (`lib/customers.ts:83-87`): any `CUST-`-shaped id resolves to an API-only customer with `apiId = id` (so the second customer id in the g3 row resolves).
- `Object.hasOwn` already used in product (`RoadmapScreen.tsx:70`, `:78`); `tsconfig.json` lib `["dom","dom.iterable","esnext"]`.
- CI (`ci.yml` blob `0176b4915d69...` at head = main's): on: 14-18; web-build 371 (npm ci 387, audit 390, audit-dev 395, lint 396, typecheck 409, build 413, check-shards 426); web-unit 450 (npm test 478); web-e2e 483; web 526. `package.json`: lint `eslint --max-warnings=0`, typecheck `next typegen && tsc --noEmit`, test `vitest run`, build `node scripts/build.mjs`. ESLint config = next core-web-vitals + typescript (no explicit no-duplicates rule; whether one is inherited is UNMEASURED, so the kit lets import lines gain names instead of adding a second import).
- Ports: 9630-9639 `lsof -sTCP:LISTEN` 0; word-boundary scan `\b963[0-9]\b` over the 57 non-`.pre-` SEAT kits of 2026-10-31 and 2026-11-01: 0 files (control: `\b940[0-9]\b` hits B1016 and B1022; `\b941[0-9]\b` hits B1009, which is why 941x was not taken). Reserved; no listener expected (unit rows only).
- Round count: 538 `*_STATUS.md` in `Briefs/`, 130 with a first line starting "GATE VERDICT"; filter `part b"|b1016/|HPSMPOC-388` (-i) on those first lines: 1 (B1022, NO GO round 1 of 2); control `security preview`: 3 (B953, B965 = part A's class, closed; B1022). So this is round 2 of 2 on the class.
- Landing rule: analysis `CLARIFICATIONS.md` at main `06e8d8f9` (5035 lines, `gh api -X GET` raw), line 5018 (PR #268 landing, a round-2 class): "a head-pinned squash".
- Model: `model-routing.md` line 92 = row C2 (S55 1st), 93 = C3, 108 = G1, 109 = G2, 111 = G-cap (`grep -n`; zero control 0). `models_latest.json` line 23 `claude-sonnet-5-5`. `brief_seat.sh` line 24 `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`.
- Load: `uptime` 07:33 load averages 2.65 2.32 3.51. `.tools/.git-lock` absent. Helpers present: `.tools/b198/lock.sh`, `.tools/b267/waitload.sh`, `.tools/node24/bin/node`; gitleaks 8.30.1.
- Kit hygiene: four-underscore lines 9 (8 slots + last line; control 1); `@X@` 0; non-ASCII 0 (control 1); person-name tokens 0 (control 1); `C-<digit>` 0 (control 1).

## D-decisions (in the kit)
D-1 per-id capability as two default-empty harness maps, added lines only, no per-run result map (the g18 row needs only a per-customer run list); D-2 no new test file; D-3 no timers (waits on recorded requests or rendered words; the gate's scratch used a 50 ms wait, the kit replaces it); D-4 no row pins the A2 reading (newest run issued in every report row); D-5 re-run p5/p6/p7; D-6 Sonnet, READY 90 / hard stop 150 min; D-7 one commit (two only if each is green alone; never amend).

## Q-questions for Tuesday (each with a default)
- Q-1 Gate tier for the round-2 gate: DEFAULT tier 1 on Opus (G1 line 108), as round 1, because the rows pin the customer report release rule. Alternative: tier 2 (G2 line 109, which names Opus 1st when the follow-up's mechanism sits on a G1 surface).
- Q-2 Harness maps (D-1) vs the gate's module-mock style in a new test file: DEFAULT D-1 (the rows sit with the rows of the same rule, and 0 removed harness lines prove nothing existing changed).
- Q-3 The no-write walk asserts EXACTLY one report read (ASM-2): DEFAULT exact (the gate measured exactly one); the seat STOPs if its head reads another count. Alternative: at least one.
- Q-4 Timings: DEFAULT target READY 90 minutes, hard stop 150, after Step 0.
- Q-5 Seat H90, ports 9630-9639 reserved (none expected): DEFAULT accept.
- Q-6 One commit vs two (harness, then rows): DEFAULT one.

## UNMEASURED
No worktree, npm, test, lint or typecheck was run by the drafter. Each new row's result on the harness (the gate proved the same shapes with module mocks only); whether the g3 row bites WITHOUT a timer on the harness (the kit reasons it does, because the stale render precedes the recorded request, and tells the seat to STOP rather than add a timer if not); whether the walk's report read lands before the final assertion (the kit wraps it in `waitFor`); whether `eslint-config-next` warns on a second import from one module; whether p6/p7 also turn the new rows red.

## Outside the fences (disclosure)
- One stray scratch write outside the session scratchpad: an early command redirected a `git grep` listing to `/tmp/claude-501/x` (1011 bytes, file names only, no secret); left in place (never delete). Other scratch files are under the session scratchpad (`kits.txt`, `gates.txt`, `importers.txt`, `clar.md`).
- The `.pre-stamp` copy was made with `cp -n` and verified by `cmp` (rc 0) rather than a second Write, so the copy is byte-exact.
- Read as data (no run, no write): the gate's `.tools/b1022/plants.py`, `gproof.py` (grep) and `quarantine/zz-b1022-g.scratch.test.tsx.ran1`. No decision card read; no `decision_queue.sh`; no Jira call; no HTTP to any hosted host; git verbs read-only with `--no-optional-locks`; `gh` `-X GET` only under the project's `GH_CONFIG_DIR`.
