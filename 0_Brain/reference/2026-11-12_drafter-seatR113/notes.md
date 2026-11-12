# Drafter notes: Seat R 113th brief (2026-11-12 ~21:3x AEDT)

Output: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatR113/brief_R113.md` (~43 KB, about 3 KB over the ~40 KB target: R 112th's carried text is by pointer, the over-run is the measured FACTS for two rows). Nothing written under `!CODING/`; the only writes are this folder and the drafter's scratchpad (blob copies, merge-file copies, three tsc copies with a symlink to `s-a28-ks2182`'s node_modules). No mail, pane tap, board post, launch, git write verb or fetch. Reads: `ls-remote`, GitHub REST/GraphQL/contents/blob APIs with the Secuura project's gh config, Linear GraphQL (key read inside python, never printed), `git hash-object` and `git merge-file` on files (no repository touched). STAMP block left blank.

## Queue as drafted
1. Row 48 = KS-2029, tier 2, test-only, one file (`tests/e2e/tests/fixtures/test-helpers.ts`), shape (a), ad-hoc tsc leg with planted control.
2. Row 49 = KS-2173 (the `Vote delegated` line only), tier 2, product file `governanceService.ts` lines 1234-1238 plus a new red-first jest cell; needs a ONE-PR overlap ruling for PR 2099; starts only if the reading after row 48's READY is 42 or under.

## Measured distance, PR 2099 hunks vs the Vote delegated line (develop 13e62febfba8)
- Hunk 2 `@@ -1206,6 +1208,13 @@` covers old lines 1206-1211 and inserts 7 lines after old line 1208. The call is at 1234-1238. Last old hunk line 1211 to call start 1234 = 23 lines (22 unchanged between). Insertion point (1208/1209) to call start = 25 lines. Hunk 1 (`-603,11`, ends old 613) = 621 lines away.
- Instrument: `pulls/2099/files` patch headers; develop's file differs from 2099's base blob only at line 420 (one-line, same length), so the hunk numbers apply unshifted. Call text byte-identical at 2099's head, at line 1243 there (+9).
- `git merge-file -p` (pure file op, symmetric, NOT merge-tree) of the planned fix against 2099's head: rc 0, 0 markers. Controls: a one-line edit at develop lines 605-611 and 1208-1209 conflicts; every other line in 1200-1240 (including 1234-1238) does not. Nearest conflicting edit is 25 lines above the call.

## Where Wednesday must rule at the stamp
1. **ONE-PR overlap ruling (OVL_IGNORE_PRS=2099) for row 49.** The census hits [2099] on a write path, so the seat's plan will ask. The drafter cannot grant it; the brief makes the seat state its own both-orders merge-tree gate (controls in both hunks) before any push and says no push without the ANSWER. Decide whether to pre-grant it in the STAMP (naming 2099's head 8967de8b1755) or leave it to the plan.
2. **Scope of KS-2173.** The board seat's 10:15Z comment makes KS-2173 "the one ticket" for wallet addresses in governance logs: two more layers (the `Request received` log in `services/governance/src/index.ts`, itself on PR 2099, and the shared `errorHandler` in `packages/shared`, which every service builds against). The brief confines row 49 to the one line, `Refs KS-2173` only (no close word), and carries the two layers as part 2. Rule: confirm, and say who owns part 2 and at what tier (the drafter did not read those two files).
3. **Fix shape of the log call.** Drop only the two addresses (keep the ticket's `delegationId` and the two ids), or `{ delegationId }` alone. Whether participant ids are personal data is UNMEASURED (KS-1955 treats a wallet as the data subject's own data). The brief has the seat put this to you as a one-line item at its plan.
4. **Row 49 start threshold (42 after row 48's READY) and wrap/stop numbers (60/55).** Drafter's arithmetic from R 112th's meter (PLAN 30.4, READY 49.4, wrap 51.5 for a first product row): row 48 +5 to +9, row 49 +12 to +17. Change if you prefer.
5. **Whether PR 2216 joins the carried READY list** (2194, 2195, 2197, 2198, 2200, 2201). R 112th's brief kept 2209-2215 off it; the brief leaves 2216 to you.
6. **Gate 340.** The verdict file's first line reads GO WITH NOTES (b12dd042761d, tier 2, round 1) but its mtime (21:26) and its "to 21:27" text sit at or after the machine clock at my read: possibly still being written. The brief says let the mail decide; confirm at the stamp, and that no fix round (existing-branch driver family, not in the narrow kit) is expected.
7. **Kit scope.** The narrow kit's row-47 pieces are hard-wired to KS-2174 and auth; the brief has the seat write 49-shaped versions by counted shift and list them in its plan (as R 112th was told). Rule if you would rather name the list now. Also the clone-source question: `s-a28-ks2182` still matches develop's root pair (unchanged by PR 2213) but carries the stray node_modules symlink to `s-t24-l1` (trap i, with its quarantine-in-your-tree fix); `s-r112-ks2174` also matches but is protected (PR 2216 open), so it is NOT a source. Say if you want a different source.
8. **Floor at the stamp.** tmux at 21:25 showed only %0 and %1; B 158th and S 75th are being drafted. Re-list.

## Established (instrument, time)
- develop `13e62febfba85b867831a42a95cb8bcb558084d2`: `git ls-remote` 21:25:29 AEDT; PRs 2099 8967de8b1755, 2215 ba847c2ef9f9, 2216 b12dd042761d, 2212, 2214, 2052 unmoved; PR 2213 merged. The move from eab5ac6bff8d is one commit, three governance files, nothing under tests/e2e, no lock.
- Root pair at develop (contents API) c5649b43817c / 11f32889c6d5, equal to eab's; `git hash-object` shows `s-a28-ks2182` and `s-r112-ks2174` match, `s-t24-l1` and `s-r101-ks1053` hold the old pair. Governance and shared package blobs equal `s-a28-ks2182`'s.
- Census 21:3x: 102 PRs, 455 rows, controls PASS (`.env.example` [2052], absent path []); test-helpers.ts and all of tests/e2e hit 0; governanceService.ts hits [2099]; userRepo.ts now [2216].
- KS-2029: file blob unchanged since eab (`0627bac77990`); tsc 5.9.3 re-run at 13e62febfba8: unchanged file = the two TS2339 at (113,59) and (113,77); two optional members = no output; planted third member = one TS2339 at (115,94). `ci:e2e` runs in `systemTest/playwright` (workflow lines 285-308), a different package from tests/e2e (closes R 112th's unmeasured item).
- KS-2173: line numbers equal the ticket's and eab's; 41 logger calls in 7 governance source files (control: o160's 41), one carries a wallet value; no test names "Vote delegated" (32 files, control `delegateVote` 4).
- History guard: R 112th heading 1, R 111th 1, R 113th 0.
- tmux %0 and %1 only; load 6.68/4.72/4.03; 2.2 TiB free; `worktrees/.push-lock` absent (control: `lock-holder.json`, `lock-released.txt` exist).

## Could not establish (and what would close it)
- Real merge-tree of the row 49 fix against 2099 in both orders: the seat runs it (drafter may not run `merge-tree --write-tree`); my `merge-file` is a one-order symmetric proxy.
- Which command runs the governance jest suite from a fresh tree: the clone source's governance node_modules holds one entry (`@types/node`) and jest comes from the root; nothing was run. The seat's set-up proves it.
- Whether `s-a28-ks2182`'s `packages/shared/dist` is fresh: not compared; the seat builds its own (trap ii).
- Whether `systemTest/playwright` imports the tests/e2e fixture; what tests/e2e's own Playwright install resolves (declares ^1.40.0, root installed 1.61.1).
- The bodies of governance cells that mock the logger (only ks1940's mock line was read); KS-2060's Linear state and whether 2099 is about to merge or move (head last updated 2026-11-08); the push queue; the docs-fragments outcome for both rows; Node 24.
- Gate 340's full verdict (first line and header only read).
