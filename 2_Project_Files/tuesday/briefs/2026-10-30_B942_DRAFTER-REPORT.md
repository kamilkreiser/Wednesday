STARTABLE: YES after your stamp, but NOT at once: load1 read 21.57 at 13:43 and 5.81 at 13:45 (four gates and four builders live), so launch_when_cool will hold it; this gate is the heaviest of the two (five or six production builds); CI and CodeQL on the head were still running at 13:44 (CodeQL neutral; the gate reads them last, after a wait)

# B942 drafter report (2026-10-30, about 13:42 to 14:05 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B942_SEAT-G219_hpsmpoc-250-tailwind-logo-gate-tier2.md` (67 lines; 8 four-underscore lines = 7 slots + the last line, lines 59-65 and 67, by `grep -n -E '_''_''_''_'`; at-sign slot pattern 0, control 1; non-ASCII bytes 0 by `LC_ALL=C grep -c '[^ -~]'`). Shape: B938 (stamped this session) for structure and conventions; the checks are B936's own step-5 CSS program and step-6 plants, re-run independently. I read everything read-only: gh `-X GET` under the project `.gh-config`, `git --no-optional-locks ls-remote` on the shared repo, raw `contents?ref=` reads into my scratchpad, no Jira call, no `cd`, no hosted HTTP, no ref written, no message, nothing in the project folder.

## BLUF
Seat `Datasec/HPSM-POC-G219` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), ports 9740-9749, gates PR #250 @ `df5d24fc` (2 commits on main `e21d8044`, 0 behind, 2 paths: globals.css +4 -0, HpLogo.test.tsx +122 -12). Round 1 of 2 on class "Tailwind source exclusion and logo-test pins, config and tests only". The heart is the gate's OWN CSS program over base, commit-1 and head builds: deletions only, no product class lost (whole-candidate matcher with the `bg-white` / `rounded-lg` controls), no test-only rule left, head css = c1 css, the mut control ships the plant tokens back, and a non-class census proving `[data-scroll-x] { position: relative; }` (G216's coupling) and the print rule (G217's) still ship. Then the test-file deltas, plants p5-p14 (+p5m, p5i) head red / base green, nine judge mutants, suites in CI order, a cross-lane combo build (#249 + #250 + #244) that proves #244's first `max-md:` rules still ship, CI and CodeQL last.

## Facts re-measured (instrument; control)
- **PR and refs (13:43-13:44):** #250 open, draft false, mergeable true, `blocked`; head `df5d24fc`, base `e21d8044`; commits `6681c1ef` (globals.css only) and `df5d24fc` (HpLogo.test.tsx only), both unsigned; 2 files +126 -12; title 144 chars with the three keys. `refs/pull/250/merge` `dfc17d46`, parents `e21d8044` and `df5d24fc`, tree `1b4e0176` = head tree. Open PRs #244-#251.
- **globals.css:** base 125 lines `719dc5efc90d87f1`, head 129 `37ce43cd68207c80`; `diff` = four lines after line 3 (comment + three `@source not`). `[data-scroll-x] { position: relative; }` base 65 = head 69 (SOURCE survives; the built sheet is the gate's C2f). Print rule base 109 = head 113.
- **Patch:** 0 added non-ASCII bytes (control 1); its one non-ASCII line is the existing `globals.css:5` ellipsis, as context.
- **HpLogo.test.tsx:** 513 -> 623 lines; `it(` lines 29 -> 34 (builder: cases 40 -> 45); 0 non-ASCII; the fixture string "Demo Person" 3 at base, 4 at head (a pre-existing fixture, not a name).
- **Tree census at the head:** 210 `*.test.ts(x)`, all under `web/src`; no other test-shaped file in `web/` outside `web/e2e` (57 entries). So the three globs cover every test file today.
- **Checks at 13:44:** 18 runs; CodeQL `neutral`; Analyze javascript-typescript and csharp in progress; `web (Next.js)` not yet listed.
- **Overlap:** #244-#249 and #251 share 0 paths with #250 (file lists read by GET). Couplings found: #244 (G215) adds the first `max-md:` classes; #246 (G216) relies on `[data-scroll-x]`; #247 (G217) on the print rule; #249 (G218) changes `AppShell.sidebar.test.tsx` (a reader of globals.css source) and `GlobalNav.tsx` (rendered by HpLogo.test's AppShell rows) and three `web/e2e` files (now outside Tailwind's sources).
- **Ports:** 9740-9749 0 listeners (unrestricted 22 lines); a word-bounded 974x scan of the 50 non-`.pre-` 10-30 SEAT kits in both folders: 0 (controls 1/0). `.tools/b942` absent (control `.tools/b198` lists).
- **Panes 13:45:** tuesday, G218, G217, G216, G215, H68, H66, H67, H64, H63, H59, fleet-monitor. No G219.
- **Round count:** 102 `GATE VERDICT` first lines (B805 and B817 present); the loose scan hit only B730, B760, B784, B833, B868 (other logo classes and PRs); no NO GO on this class or PR.
- **Probe (Python copy of the head's FRAME regex):** true for `outline-none`, `outline-hidden`, `ring-0`, `shadow-none`, `border-0`, `border-collapse`, `ring-offset-2`; false for `divide-y`, `rounded-lg`. The gate measures it in the real test (C4).

## Builder claims found wrong or loose at drafting
1. **PR body: "40 removed (31 class rules and 9 @property blocks), each with a class token found only in test files or e2e".** An `@property` registration carries no class token; it went because only test-only rules used it. A text Minor for Tuesday's body edit.
2. **Two byte frames, not named:** commit 1 says "Tailwind sheet 49,190 B -> 46,116 B" (one file); the body and READY line say "49848 -> 46774" (both files summed; the second file is 658 B either way). Both are consistent. The gate prints both.
3. **"10 of 10 planted defects" (body) vs "12 of 12 with the main/image variants" (STATUS):** the same plants counted in two ways. A text note.
4. **The builder's own Correction 2:** the kit's literal "product hits = 0" reads 1 for `m-3` and 2 for `m-5` (prose in comments), and it is cleared by the oracle build. The gate reproduces both and runs its own oracle (C2h) from a `git archive` extract, with nothing moved inside a worktree. The builder moved 267 files inside its mut worktree.
No code claim found wrong.

## D-decisions (mine, in the kit)
- D-1: **Own CSS program, own trees.** The builder's `cssdiff.py` is read-forbidden. The gate compares only sha256 lists with the builder's evidence.
- D-2: **Non-class census (C2f)** names `[data-scroll-x]` and the print rule explicitly, because two sibling gates rely on them.
- D-3: **FRAME over-strict and blind probes are Note-class** (ticket text). A future `outline-none` on the wrapper or `main` would redden a row, and `divide-*` is not judged. Neither is a defect of this PR's claim.
- D-4: **Role words in the diff are test fixtures, not an escalation.** These are `signedInAs("partner", ...)`, `SignInScreen auth="entra"` and a stubbed `fetch`. The gate lists and classifies each, and STOPs only for a PRODUCT role/auth shape.
- D-5: **C6 cross-lane combo.** This is PR #249's head with #250's 2 files and #244's 4 files written over it. The paths are disjoint and all three PRs sit on `e21d8044`. It is cut FIRST under load and never blocks alone.
- D-6: Hard stop: target 150 and HARD STOP 210 minutes after Step 0.
- D-7: A NO GO here is round 1 of 2, which means a fix kit, not the cap.

## Q-questions for Tuesday (each with a default)
- Q-1: Run the C6 combo? Default YES, cut first if load stays above 7.
- Q-2: Run the C2h oracle (a sixth build, from a `git archive` extract)? Default YES after C2 a-g; cut before C6 only if load forbids.
- Q-3: Should the FRAME probes be graded Note with ticket text? Default YES.
- Q-4: Should the test-fixture role words be classified, not escalated? Default YES.
- Q-5: What does a NO GO mean? Default: the PR is parked open and Tuesday writes a round-2 fix kit.
- Q-6: Is the PR body corrected before the gate (items 1-3 above) or after? Default: after, from the gate's numbers.

## Stamp slot defaults (suggested)
S1 STAMPED <time> by Tuesday s206, D-1 to D-7 accepted; S2 from the stamp until 17:30, launch_when_cool at load1 below 7; S3 Q-1 to Q-6 as the defaults; S4 Tuesday under the 2026-10-30 10:07:23 commission, the 2026-10-16 merge-once-tested grant, the 2026-09-13 as-many-agents rule, the Datasec CodeQL policy and the 2026-10-22 Sonnet-first grant; YES to the four-refspec fetch, npm ci into own trees and the oracle extract, wt-b942-mut and wt-b942-combo, loopback 9740-9749, own gitleaks; S5 target 150 / HARD STOP 210 after Step 0; S6 Tuesday's own read at the stamp; S7 `model: claude-sonnet-5-5 -- G2 -- gauge <n>%` with load1.

## UNMEASURED
All runtime numbers in the kit are the builder's, written as predictions. Also unmeasured: the CodeQL `neutral` reason, whether `web (Next.js)` and the e2e shards will pass, whether the combo tree builds green, the two-commit squash title under `COMMIT_OR_PR_TITLE`, and the runner's build.

## Outside-the-fences disclosure
None breached. I listed `.tools` names once, ran `ls -d` on `.tools/b942` (absent) and used `.tools/b198` as the control. I opened nothing under `.tools/b936/` or any `wt-b936-*`. My scratch files are in the session scratchpad only: the patches, raw files, PR bodies, tree list and the gate-verdict first lines.
