STARTABLE: YES after your stamp, but NOT at once: load1 read 11.17 at 11:15 (eleven builders live), so launch_when_cool will hold it; CI and CodeQL on the head were still running at 11:14 (the gate reads them last, after a wait)

# B938 drafter report (2026-10-30, about 11:14 to 11:35 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B938_SEAT-G215_hpsmpoc-244-primitives-gate-tier2.md` (67 lines; 8 four-underscore lines = 7 slots + the last line, lines 59-65 and 67, counted by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0, control 1; non-ASCII bytes 0 by `LC_ALL=C grep -c '[^ -~]'`). Shape: B913 (the tier-2 web gate of #241) for the checks and B922 (latest stamped HPSM-POC gate) for the conventions (VERDICT last line, FOR TUESDAY landing facts, merge-ref read, CodeQL read, STATUS-NOW, Stamp, Launch line). I read everything else read-only: gh `-X GET` under the project `.gh-config`, `git --no-optional-locks` on the shared repo, no Jira call, no `cd`, no hosted HTTP, no ref written, no message, nothing in the project folder.

## BLUF
Seat `Datasec/HPSM-POC-G215` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), ports 9700-9709, gates PR #244 @ `b0f1db04` (2 commits on main `e21d8044`, 0 behind, 4 paths +13 -5). Round 1 of 2 on class "a shared primitive that widens content". The gate re-measures both page-width claims (360 and 390 at 1 px letter spacing, four roles), the 760-cell grid at base, ref `9659148c` and head, the -401 cell table with the 8 residue cells, the residue CAUSE by a scratch plant, the from-md look (CSS emission, 767/768 computed style, pill heights), exports and test rows, eight plants (each red) plus one equivalent (green), suites in CI order, CI and CodeQL last, and overlap with the live lanes.

## Facts re-measured (instrument; control)
- **PR and refs (11:14):** PR #244 open, draft false, mergeable true, `blocked`; head `b0f1db04`, base `e21d8044`; commits 2 (`0d32c79e`, `b0f1db04`, both unsigned); 4 files +13 -5; title 151 chars with both keys. `refs/pull/244/merge` `de13b4fc` parents `e21d8044`, `b0f1db04`, tree `459d15ca` = head tree. Open PRs: #244 only. Instrument: gh GET, `ls-remote`.
- **The patch** (compare, read whole; 0 non-ASCII bytes): the product change is exactly `whitespace-nowrap` -> `md:whitespace-nowrap` on the StagePill wrapper and `max-md:px-1` (+ `max-md:tracking-normal` on the head) added to `thClass`/`tdClass`; both still double-quoted literals. `partner/parts.tsx` untouched.
- **`max-md:` is new to the codebase:** `git grep -n -i -E 'max-md:' e21d8044 -- web/src` = 0 lines; at the head 5 lines (2 in Table.tsx, 3 in Table.test.tsx). Tailwind `^4`. So the kit makes the gate prove the built CSS carries the rules and the 767/768 boundary by computed style (C5).
- **Pill weights at ref vs main** (`git show`): `StatusPill` and `RelationshipPill` were `rounded-full px-2.5 py-0.5 text-xs font-semibold` at `9659148c` and are `rounded-md px-2.5 py-1 text-xs font-bold` at `e21d8044`. That is what the residue-cause plant mR reverses (font weight only), in a scratch tree.
- **Required contexts:** the five, read from branch protection. **Checks at 11:14:** 13 runs; `CodeQL` completed **neutral** (B922's PR read `success`); Analyze python/actions success, javascript-typescript/csharp in progress; `web (Next.js)` and e2e shards not yet listed; analyses on the merge ref 0, on the head ref 2; open alerts 0.
- **Overlap:** live branches `b928` (1 file), `b931` (2), `b932` (2): shared with the 4 paths 0 each (control: the 4 against themselves 4).
- **Instruments:** `.tools/b913/probe5.cjs` `cc0498f95e2157f9` (56 lines), `lib.cjs` `6f81e7b439ecfb77` (58), `.tools/b908/scratch/crawl.mjs` `95597931a0fa3753` (92), `.tools/b760/scratch/probe.cjs` `495ec186ee717ee2` (32): all present, equal to the B929 kit's prefixes. Helpers `lock.sh` `d9df031bcce14e93`, `waitload.sh` `cbd78c3800469050`.
- **Ports:** `lsof -nP -iTCP:9700-9709 -sTCP:LISTEN` 0 lines (unrestricted 15); listeners in 9600-9699: 9604, 9605, 9634, 9635 (builders). The 970x word scan of the 10-30 kits hit only `lsof 9700-9999` range text in B916, B918, B920, B933 (no block claimed). `.tools/b938` and `.tools/wt-b938-head` absent.
- **Panes 11:15:** tuesday, H67, H64, H61, H62, H63, H59, H60 (the builder, parked), fleet-monitor. No G215.
- **Round count:** 98 `GATE VERDICT` first lines; the loose scan hit only other PRs and classes; no NO GO on this class or PR. "NO GO 0 of 2 ... round 1 of 2".
- **Model:** `model-routing.md` G2 `:109`, G-cap `:111`; `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus.

## Builder claims found wrong or loose at drafting
1. **"Existing tests modified 2" (READY line) / "Two existing test rows change" (PR body): the patch shows 1 existing row modified (the StagePill pin) and 1 row ADDED in `Table.test.tsx` (+5 -0).** The builder's own Corrections item 1 says so, but the READY line and PR body did not follow. It is a text Minor, inside the stamp's Q-1 (fewer changes, not more). The kit has the gate count it (C2b) and grade it (C9).
2. **The PR body carries `B908-7` (a `B###` token) and a non-ASCII generated-by line.** It is Tuesday's text, not the builder's code. Neither can go into the squash text. The kit tells the gate to say so in the squash proposal.
3. "16 of 24 / residue 8" counts all four roles on all routes. B913 counted 20. The builder's reconciliation looks right; the gate recounts and names the extra 4 cells.
4. CodeQL check-run `neutral` at 11:14 is not in the builder's STATUS, which saw 0 check-runs before the PR existed. This is new; the gate explains it from the run's output.

## D-decisions (mine, in the kit)
- D-1: **Two instruments.** The copied `probe5.cjs` is the -401 definition, but the builder used it too. So every never-cut number is also read by the gate's own `own.cjs` (B760/B908 methods), and the two must agree within 0.5 px.
- D-2: **Residue cause by plant mR** (font-bold -> font-semibold in StatusPill and RelationshipPill, scratch tree only) plus mR1 (StatusPill only). The 8 cells must fall to the ref. If they do not, it is a Major, because the recorded acceptance rests on that cause.
- D-3: **P1x:** the 360 check is extended to all 38 routes x 4 roles at base and head (152 cells each). A cell that is wide at the head but not at base is a Blocker. One that is wide at both is a page-lane Note.
- D-4: **Eight plants plus one equivalent** (m1, m1b, m2a, m2b, m2c, m3, m4, m5 must go red; m6 token reorder must stay green). Four of them are rebuilt for the browser: m1, m2c, m4 and mR.
- D-5: Hard stop: target verdict 150 minutes and HARD STOP 210 minutes after the gate's Step 0 (three builds, about 2600 probe cells, four plant builds, a CI wait).
- D-6: NO GO here is round 1 of 2, so it means a fix kit, not the cap.

## Q-questions for Tuesday (each with a default)
- Q-1: Does the residue acceptance stand as recorded in the PR body, so the gate grades the measured 8 cells as a Note? Default YES (as briefed).
- Q-2: May the gate change the frozen `ui/Tag.tsx` in its scratch mut tree only, to prove the cause (never committed)? Default YES.
- Q-3: Should P1x (360 on every route) be run? Default YES; cut it first if load stays above 7.
- Q-4: What does a NO GO mean for the PR? Default: the PR is parked open and Tuesday writes a round-2 fix kit.

## UNMEASURED
All runtime numbers in the kit (they are the builder's, written as predictions); the CodeQL `neutral` reason; whether `web (Next.js)` and the e2e shards will pass; the two-commit squash title under `COMMIT_OR_PR_TITLE`; the runner's fonts.

## Outside-the-fences disclosure
None breached. I computed sha256 prefixes of four instrument files and two helpers under `.tools/` (read only) and listed `.tools/b938` and `.tools/wt-b938-head` (both absent). I did not open `.tools/b929/` or any `wt-b929-*`. Scratch files are in the session scratchpad only (PR body, patch, path lists).
