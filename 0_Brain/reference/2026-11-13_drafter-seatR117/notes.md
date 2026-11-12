# Notes for Wednesday, Seat R 117th brief (drafter, 2026-11-13 08:1x to 08:3x AEDT)

Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatR117_raise.md` (STAMP block blank). KEPT 2 rows (KS-1197 row 56, KS-1855 P4 row 57); DROPPED 2 (KS-805, KS-1642 H9PIN-2).

## Rule or check BEFORE stamping

1. **READ BY YOU: KS-1855 O125-P4 is UNREAD BY WEDNESDAY.** Searched `daily/` 10-19, 10-28, 11-10..11-13 for "read every" (positive control: hits in 11-11 lines 54, 56 and 11-12 lines 157, 159, 187, so the search works); none names KS-1855. The only lines: 11-10 line 35 (prose summary of o125, "Report written by Wednesday"), line 50 (U 21st stamp accepted the stack and the flag), line 32 (Kam's card c). The READY header says "held after a source read" by the o125 operator. Read the READY's three sections before stamping (8 `+` lines in `routes/verification.ts`, 20 in ks1628 test, 4 in ks815 test).
   KS-1197: your own R 116th STAMP item 1 records that you read every product +/- line of this same READY; file unchanged since (held 13:50 10-28). Not re-read here.
2. **KS-1855 scope ruling needed (my lean: Refs, half two only, ticket stays open).** The patch is half two of Kam's card c (cert verify stand-in behind ENABLE_MOCK_ENDPOINTS). Half one (P3, admin.ts) is a different READY and not in the brief. The brief makes the body say so and forbids claiming the ticket. Also note behavioural change: with the flag unset (the default), the certifications verify now reaches the proxy; the brief tells the seat to count callers in tests/scripts (not measured by me).
3. **Tier (my lean, yours to rule):** both rows TIER 1 in ONE tier-1 READY (two PRs, cap three). KS-1197 per your R 116th ruling. KS-1855 P4 because your 11-10 line 35 labels all three o125 passes tier 1 and it changes a verify door; arguable (flag-gated test stand-in), so rule it. If you rule P4 tier 2, it must be a separate READY.
4. **Fresh fetch YES needed** for the URL-form develop fetch of ae5b615f4cc0 into `worktrees/s-r90-base` (R 116th's YES is spent). The brief says a STAMP YES is required.
5. **Drops, confirm:** KS-805 (Done+archived 11-04, PR 1599; fix already at oauth.ts:1390; patch rc 1). KS-1642 H9PIN-2 (Done+archived 11-03, PR 1618; H9/H9c already at test lines 119 and 126; patch `--check` rc 0 offset 14 = false pass, would duplicate cells). Both left in `night/`; I did not touch them. Two findings added for the board/Spark operator in the brief (checker false PASS; no landed-marker on READY files).
6. **Standing line carried** (no "do not merge until pre-merge tests run" sentence; the brief tells the seat to strip it from R 116th's body templates by counted edit and grep for it; Test Evidence still names what was NOT run).
7. **Floor/queue:** R 116th's 2220-2223 are OPEN (gates 346 GWN x2, 347 GWN 2222, GO 2223 per daily); they are in the B 169th queue. No intersection with my rows (below).

## Established facts (instrument, time)

- develop = `ae5b615f4cc0b5b7c0d57c6585453fbf6743abee`: `git ls-remote origin refs/heads/develop` via the project's repo-local `core.sshCommand` (read, never printed), 08:13:10 AEDT; equals your 08:11:41 pin.
- Applies-check, scratch clone `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatR117/scratch_clone` (git init, `fetch --filter=blob:none --depth=1 origin <sha>`, `read-tree FETCH_HEAD`, `checkout-index` of only the files each patch touches), `git apply --check -v` of each canonical `patch.diff`:
  - KS-1197: rc 0; enforcement.ts hunk #2 "succeeded at 153 (offset 1 line)". New ks1197 test absent at develop.
  - KS-1855 P4: rc 0, no offset (verification.ts + the two existing test files; first run failed only because I had not checked out the two existing test files; re-ran after checkout-index: rc 0).
  - KS-805: rc 1, "patch does not apply" (oauth.ts:1300 context gone). KS-1642: rc 0 "Hunk #1 succeeded at 129 (offset 14 lines)" (false pass).
  - No separate negative control run by me for the apply instrument; KS-805's rc 1 is a natural failing case from the same command.
- READY headers quoted: KS-1197 held 13:50 2026-10-28 tip 1d07ce26ae2f (enforcement.ts 3/2 + ks1197 test 102/0; A2 PASS, A4 9 of 13 red, suite 1255 -> 1268); KS-1855 P4 held 03:41 2026-11-10 tip d0b4825cc244 (verification.ts 8/1, ks1628 test 20/0, ks815 test 4/0; A2 PASS; A4 2 of 22 red; suite 1882 -> 1884); KS-805 held 09:58 2026-10-19 tip 78cb3c3939e3; KS-1642 H9PIN-2 held 17:15 2026-10-19 tip 722e07f19cee.
- Board (Linear GraphQL read-only, own script `lin.py` in the session scratchpad, key read inside python from the project `.env`, not printed, 08:1x): KS-1197 Backlog, prio 4, kamil.kreiser@secuura.ai, updated 2026-10-12, 2 comments (Peter's); KS-1855 Backlog, prio 2, same assignee, updated 2026-11-09T19:50Z, 1 comment (Kam's card c). KS-805 Done archived 2026-11-04 (PR 1599 attached); KS-1642 Done archived 2026-11-03, assignee None (PR 1618 attached). Nobody is Peter or Stuart. No open PR carries the keys.
- PRs: `gh pr list --state open --limit 500 --json ...files` = 93 open (control 2079 present; no PR at 100 files). Whole-word regex over title, branch, body: no hit for 1197, 1855, 805, 1642, 1952. No open PR touches enforcement.ts, routes/verification.ts, the ks1628/ks815 tests, or any ks1197/ks1855 path. Merged (`--limit 400`): PR 2157 (KS-1952, 2026-11-12T06:42Z) and PR 2204 (KS-1466, 2026-11-12T02:36Z) touched those product files and are inside develop; no merged PR carries KS-1197 or KS-1855.
- Merge-queue intersection (REST `pulls/<n>/files`, 18 PRs: 2147 2144 2141 2137 2125 2134 2126 2098 2097 2096 2095 2090 2089 2079 2220-2223): NONE. Gateway-touching ones are neighbours only: 2125 index.ts; 2134, 2096, 2095, 2089 single test files.
- Floor 08:19: panes %0 and %1 only; load 1.25; no `worktrees/.push-lock`; history guard R 116th 1, R 117th 0 (`/usr/bin/grep -E -i -c`).

## Could not establish

- Repo-wide caller count of `meetsVerificationLevel` at ae5b615f4cc0: my tree-wide `git grep --cached` on the blobless clone began fetching every blob and was stopped; only the checked-out enforcement.ts was read (defined line 54, used line 154). The brief carries R 116th's measure (one caller, enforcement.ts 154) and tells the seat to re-grep.
- Whether `/api/certifications/:id/verify` has callers in tests/scripts (consumers affected by the flag gate): not measured.
- Whether either patch's cell passes under vitest at ae5b615f4cc0: only `git apply --check` was run, no tests (the Spark's A4/A5 are at the older tips).
- Gate availability (Opus) and whether B 169th is live: yours.
- R 116th's tools count: `ls` showed 28 top-level entries (HANDOVER says 36 re-keyed + extras): I quoted my `ls`.

## Fences kept
Wrote only the brief, this file, and `scratch_clone/` (git init/fetch/read-tree/checkout-index/apply --check there only) plus `lin.py`, `open.json`, `open.err` in the session scratchpad. No push, PR, comment, mail, Linear write; no git write verb under `!CODING`. The only network reads: ls-remote and one fetch into the scratch clone via the source repo's own deploy-key command; GitHub REST/`gh pr list` reads; Linear GraphQL queries.
