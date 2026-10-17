# Vision gate 22 (QuickQuote PR #10 ROUND 3 @ f31720e, Kam-authorised; held price re-checked, one-cent floor; v2.39): drafter's report

## BLUF
- **Drafted:** the gate-22 kit for QuickQuote PR #10 round 3. It is tier 1 and **round 3, authorised by Kam** (09:45:48, card
  `quickquote-pr10-r2-publish-hold-1017` = a: "then one more test gate. You decide the publish after that, on its own card"). There is no round 4
  without him.
  - **Kept:** gate 21's whole matrix (§N3-§N5, §N11) and its D4 shape (a NO GO means nothing merges and Kam gets ONE card whose default is HOLD).
  - **Added:**
    - §N10 re-tests G21-F1/F2/F4/F5/F7/F8 as red-at-`3a3399e` / green-at-`f31720e` pairs, in every print mode × AUD/USD/CAD and offline. It also
      re-runs gate 21's CLOSED rows.
    - §N11 adds the floor rows (F-AT / F-UNDER / F-SNAP), the new regression rows (B-TRANS, FLOOR-FX, FLOOR-CUR, KEY-COMMIT, SPIN, MODE-WANTED) and
      mutant I armed in the browser (MUT-I).
    - §N8.4 gathers the publish facts for Kam's ONE card.
  - **Not run:** the launcher, except under `--check`.
- **Head did NOT move.** `git ls-remote origin` at **11:33:28 AEDT**: the branch = `refs/pull/10/head` = `f31720ee677dbe2deb53dcb7991f1683a1b03ce1`;
  main = HEAD = `437ab4bc412b…`. The launcher re-read origin at 11:55:14 and 11:55:54: unchanged.
- **Biggest trap: WRONG (b), the paste instrument changed meaning.** Round 3 decides "committed" by the input event's `inputType`.
  - Gate 21's harness "pasted" with CDP `Input.insertText` (`qa-harness-g21-drive.cjs`:223). Chrome reports that as `insertText`, which round 3
    treats as a KEYSTROKE (judged quietly, only on `change`).
  - The builder's "paste" is a script: it sets `value` and dispatches a synthetic `insertFromPaste` (bounds file :122-127).
  - So neither earlier instrument is a paste any more. The brief requires a real clipboard paste, checked as `insertFromPaste` (else that row is VOID),
    and reports `insertText` separately as TYPED-WHOLE (the dictation case).
- **Tuesday must stamp 6 slots** (the launcher exits 47 until they are done):
  - `SELF-CHECK:` and `Self-check note:`;
  - `AZ-PRE-READ:`;
  - `N4-METHOD:` (D5; drafter: FULL-TEXT, as for gates 20 and 21) and its `RULED:` line;
  - D4's `RULED:` line;
  - `ROUTING-LINE:`, after adding `QA/Vision-gate22|tuesday-agent@agentmail.to|no` to `inbox_routing.conf`.

## Outputs
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-gate22-qq-pr10-r3.md`: the brief. 790 lines (gate 21's
  was 806); sha256 `8e3b72e0…`.
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate22.sh`: the launcher. 739 lines, chmod +x,
  `bash -n` rc 0, sha256 `0ccb9e31…`.
  - Built from gate 21's launcher by a script of exact substitutions, each required to match exactly once. Its structure and guard numbering are gate
    21's.
  - What changed: the gate number, the brief/READY/report paths, the target (pins, chain, trees, numstat, blobs, code anchors, the READY's anchors),
    the prior round (gate 21's report and tools), routing, and the embedded prompt.
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-qq-pr10-r3-READY-mail.txt`: lines 1-124 of
  `…/scratchpad/ready2.txt` (the Vision mail only; lines 126+ are NexusAI-O's RD-802 READY). 9,948 B, sha256
  `076c5afc0009aab58a823eed6335b9e62a6f9dfbd7d0e1a807e31b297db8fd39`, pinned by the launcher. Guard 31 also checks that it is 124 lines and contains no
  `NexusAI` text.
- This report.

**Not written:** `inbox_routing.conf` (0 gate-22 lines; not edited); the report folder (absent; per the brief, the gate creates it, as gate 21 did);
anything in Vision_Sales_Portal or the QuickQuote repo. Test copies went only to `…/scratchpad/g22test/`.

**Not done:** no push, merge, fetch, worktree, `az`, docker, mail, browser, npm or product process; no HTTP to any live or app host. `gh` was used only
for `gh api` GETs with Vision's gh-config, whose `hosts.yml`/`config.yml` mtimes are unchanged (12 Oct 18:09:30, re-read after the GETs). The access
word and the offline constant were never read. The seam (index.html:3816-3827) was located by line number only.

## MEASURED (every value printed by a read I took)
- **Origin (11:33:28):**
  - main `437ab4b`; `fix/qq-email-matches-print-2026-10-16` = `refs/pull/10/head` = `f31720e`.
  - `refs/pull/10/merge` = `75d7a8e9…` (it was `1345ea5` at gate 21, so GitHub recomputed it).
  - PR #8 `4d6ed6e` still open.
  - Backlog tip `01c8d7f9c4d8…`; its parent is `815aae7`.
  - `refs/pull/11/head` = `818a019`: the v2.36 release PR, closed and merged 2026-10-16 (NOTE only).
- **Chain:**
  - `f31720e`'s single parent is `3a3399e`. Author and committer time are both 2026-10-17 10:18:28 +1100.
  - 7 ahead / 0 behind main; 1 over R2; merge-base `437ab4b`. `3a3399e` is an ancestor (no force-push).
  - Trees: head `ee51fa7`, R2 `ec15fb2`, R1 `25ddfb8`, main `c71780c`.
- **Numstat:**
  - Whole delta `437ab4b..f31720e`: 8 files, +942/−125. This equals the PR files API (GET 11:38:58: 8 rows, blobs `e65f3b6`/`26825da`/`cd9118a`/`e40c20e`/
    `9cddb70`/`b3c5345`/`bdb602b`/`9dd5311`).
  - Round 3 `3a3399e..f31720e`: `index.html` +108/−30, `pdf.js` +6/−2, `custom-price-bounds.mjs` +200/−3.
- **Same blob at R2 and head:** server.js, strip.js, package.json, email-matches-print.mjs, email-print-mode.mjs, plus the whole gate-21 unchanged list
  (lockfile, Dockerfile, xlsx/mail/store, tests.yml, CLAUDE.md and others).
- **GitHub (GET 11:38:58):**
  - PR #10: open, not draft, mergeable_state clean, updated 00:30:24Z.
  - Runs on `f31720e`: 38986126280 (pull_request), 38986121215 (push) and 38986121428 (PR #10 dynamic), all completed success.
  - Check runs: 13, all success. CodeQL: "No new alerts in code changed by this pull request".
  - Code scanning: main 0 open, `refs/pull/10/head` 0 open.
  - Dependabot: #1 and #4 open (extract-zip, high; PR #8's).
  - Open PRs: #10 and #8.
- **Every file:line in the READY's NEW WORDS FOR KAM, verified verbatim at `f31720e`:**
  - S-RANGE at `index.html`:3487-3488. It is a template: "A custom price must be at least ${fmt(min)}/device/month and no more than 10 times the
    standard price of ${fmt(std)}/device/month."
  - Its suffixes: " Custom pricing is off until you change it." at :3457 (fields) and :3521 (the re-check); " The percentage was not applied." at :3622;
    " The quote was not sent." at `pdf.js`:156.
  - S-EMPTY at :3438 and S-NAN at :3435.
  - The no-price sentence at `pdf.js`:160-161 (unchanged) and the reopen sentence at `strip.js`:367 (unchanged).
  - The other cited lines: `customPriceMinPerMonth: 0.01` at :1752 ✓; `pdf.js`:153 is the `wantsCustom` gate ✓. The re-check is at :3515-3523; the READY
    says 3510-3524, which also covers the comment.
- **Kam's ruling:** `decisions.json` holds `quickquote-pr10-r2-publish-hold-1017` as ruled_choice a, ruled_ts 09:46:32, delivered 09:48:23. Option a's text
  is "…then one more test gate. You decide the publish after that, on its own card." CLARIFICATIONS still ends at C-20.
- **Ports:** gate 21 bound kernel-chosen ports (`listen(0, "127.0.0.1")`, its harness :108). The brief keeps that rule, and names `47310-47319` as the
  only fixed-port block (lsof rc 1 = free at 11:40:02; also clear of B252's 6990-6999).
- **Load:** 4.85 / 9.48 / 11.90 at 11:39.

## UNMEASURED (code readings or arithmetic only; the gate measures them)
- Every browser outcome: the trap predictions below and every §2a "expected email" row.
- Chrome's behaviour for: real paste into `type=number` (is `insertFromPaste` delivered? is a non-numeric paste refused outright?), the spinner, Arrow
  keys and the wheel (whether `inputType` is empty, the step results), and whether Enter in a field fires `change`.
- Whether a live FX lookup can land inside the renderer page in production (WRONG (m)). FX is blocked here, so this stays NOT TESTED unless the gate runs
  an instrument arm.
- The Mix-and-Match standard price with every app ticked (B-TRANS's premise).
- The floor/FX numbers. They are `node -e` arithmetic over the CONFIG values, not page readings:
  - CA$0.01 at seed is predicted to be CLEARED when live 1.3877 lands (0.007042 < 0.007206 USD).
  - A$0.01 survives 1.6123, but is cleared at 1.50, on a switch to USD, and on a switch to CAD. It survives a switch to NZD.
  - Every typed bound round-trips exactly without the 1e-9 tolerance at all seeds and both canned live rates, so mutant I is predicted EQUIVALENT there.
  - At the live rates the shown 2-dp maximum is ABOVE the true maximum (CA$277.54 vs 277.5399…; Manager-only A$80.62 vs 80.615), so only the snap can
    accept it.
- The PR body's "Round 3 section, FOR KAM item 5" (not read). The builder's `scripts/r3-mutants.py` and evidence folder (deliberately not read).

## TRAPS (in the brief's WRONG list (a)-(q); each is a claim for the gate)
1. **(b) The paste instrument changed meaning** (see BLUF).
2. **(c) Keystroke vs committed.** A too-low or empty figure reached by keystrokes is silent until `change`. The next press usually blurs the field
   (S-RANGE appears) and then sends a STANDARD quote in the same instant. KEY-COMMIT drives four press routes plus TYPED-WHOLE.
3. **(d) The spinner, the Arrow keys and the wheel** are judged at once, as committed. The builder did not drive them. Steps: `cpDay` 0.0001, the
   others 0.01, `min=0`; the spinners are not hidden. SPIN covers ArrowDown from the floor, ArrowUp from empty (`cpDay` empty → 0.0001 = below the
   floor), above the ceiling, and off-grid values.
4. **(e)/(m) The re-check runs through `render()`**: the global listener, the currency change, and a live rate landing (:3167). That makes it reachable
   in the renderer page too. A rate landing mid-render could clear a just-restored floor price, giving an emailed standard quote against a printed
   custom one. This is READ-ONLY-INFERRED. The READY's "devices" in its list of triggers is wrong: devices do not move the standard price.
5. **(f) Cleared, not flagged, including on transitional states.** The first click on Mix-and-Match drops to Manager only and wipes a price that would
   fit the selection the rep is building (B-TRANS). With Advanced off, the clear happens while the ticket is hidden (P3″).
6. **(g) The floor moves with FX.** A CAD floor price is cleared when gate 21's own canned 1.3877 lands. A currency switch at the floor clears it too.
   The READY admits no cell drives this.
7. **(h) Mutant I** is predicted equivalent at these rates. The gate arms it in the browser (MUT-I) instead of taking the prediction.
8. **(i) The snap also snaps UP to the floor:** `cpDay` 0.0003 (= A$0.0091/month) is taken as A$0.01.
9. **(j) `cpModeWanted` resurrects "Custom pricing only" unasked.** It is cleared only by `cpClear` and the re-check (3 assignments plus the
   declaration). It is not cleared by Advanced off, the ticket's "Reset to default", a currency change or a committed S-EMPTY.
10. **(k) Too high mid-entry is still said at once** (deleting a "." makes 31.05 into 3105), so G21-F5's flash survives there.
11. **(l) The renderer now ignores any posted price in "Standard pricing only"**, so a crafted 1e308 beside pmDefault gets 200 instead of 422. The gate
    checks that default-mode documents do not depend on `cpState`.
12. **(n) The builder's 16/32 red was run on a MODIFIED test file** ("with the old sentence's regex"). The gate runs it both unmodified (R-G, where the 15
    G20 cells should fail on WORDING) and with only the regex set back (R-G′).
13. **(o)** Chrome's number field decides which S-NAN routes exist: `abc` cannot be typed at all.
14. **(a)** The READY now HAS a NOT TESTED block. Two of its lines (the spinner, the floor under a landed rate) are DRIVEN here.

## Kam-facing facts for the ONE publish card (claims until the gate measures them)
- **Range:** A$0.01–A$310.00 / US$0.01–US$200.00 / CA$0.01–CA$284.00 per device per month on the full bundle at seed. On Manager only:
  A$0.01–A$77.50 / US$0.01–US$50.00 / CA$0.01–CA$71.00.
  - The floor is 0.01 of the quote currency, so in USD terms it moves with the rate. The ceiling is 10× the standard price and does not move.
  - The page prints USD as `$0.01`, not `US$`.
- **Ships:** 7 commits, 8 files, +942/−125, the hosted server module included (unchanged since round 2). No lockfile or Dockerfile change.
- **Rollback:** `v0.6.4-tool2.36-437ab4b`. Behaviour across versions: G20-F3 (a v2.39 tab after a rollback emails standard silently); G20-F4 (the lone
  revert); G21-F6 (a v2.36 tab after the publish shows W1, then gets a 422 no-price refusal).
- **The note:** on screen only, in "Standard + custom" (the paper CSS hides it), per gates 20-21.
- **NEW WORDS FOR KAM:** S-RANGE (changed wording) and two new sentences, S-EMPTY and S-NAN. File:line is verified above; the rendered text per currency
  is the gate's job.
- **Behaviour changes:**
  - A price that stops fitting is CLEARED, and the rep re-enters it.
  - A 422 can now happen only in a custom print mode.
  - Same-page reopen comes back standard.
  - Predicted: the floor price disappears when the exchange rate moves, and the custom mode comes back on its own.

## What Tuesday must stamp before launch (the launcher exits 47 / 48 / 41 / 32 until all are done)
1. `SELF-CHECK: re-read end-to-end for contradictions | <time, Tuesday, lines read>` and `Self-check note: …`.
2. `AZ-PRE-READ: linuxFxVersion …` (Vision's own AZURE_CONFIG_DIR, tenant d500ebad / sub 0c57ab37). I expect `…:v0.6.4-tool2.36-437ab4b`; the launcher
   prints a NOTE if the value does not name `437ab4b`.
3. `N4-METHOD:` = `FULL-TEXT` or `FIGURES`, plus D5's `RULED:` line.
4. D4's `RULED:` line. My draft carries gate 21's 08:02:02 shape (nothing merges; ONE card; HOLD by default if an OPEN instance lets a rep email a wrong
   document). The verdict is PROVISIONAL if any of these is NOT RUN: the red-proofs, the head grid and its N4, the R2-F1/R2-F2 pairs, or U-AT / U-OVER /
   F-AT / F-UNDER / B-STATE.
5. Add `QA/Vision-gate22|tuesday-agent@agentmail.to|no` to `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf` (pattern: the gate-21
   line, line 228). Then stamp `ROUTING-LINE: QA/Vision-gate22 …`; the line must begin with exactly that text.

## `--check`
- **On the real files (11:55:14 AEDT): rc 47.** Every content guard passes (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 45N 13 14 15 20 70 82 19
  24 53 60 61 62 64 69 75 44 38R 86 46). Only Tuesday's to-do guards are pending: 47 (AZ-PRE-READ), 48 (N4-METHOD), 41 (routing line), and 32 (6
  `@STAMP@`).
  - NOTE: fleet-monitor has no single live claude, so it is not a negative control.
  - NEG seats derived: `58663` (tuesday), `34873` (Datasec/Vision_Sales_Portal), `88790` (QA/NexusAI-gate24).
- **On a fully stamped scratch copy** (TEST values, FULL-TEXT, routing line added): **rc 0, "all guards pass"**. The pinned table printed at 11:55:54.
- **Negative controls, each refused as it should:**
  - READY with one byte appended: rc 31.
  - `N4-METHOD: WHATEVER`: rc 48.
  - PIN commits 6: rc 8.
  - PIN head set to `3a3399e`: rc 40.
  - Routing line absent: rc 41.
  - `ROUTING-LINE: done`: rc 32.
  - Brief without `WRONG (q)`: rc 31.
- **New guards beyond gate 21's:**
  - R2 is an ancestor, the head is exactly 1 commit over it, and the chain includes R2 → head.
  - Backlog `01c8d7f`'s parent is `815aae7`, and it is not on the head.
  - The round-3 numstat.
  - The round-3 code anchors are present at the head and absent at R2.
  - The round-2 bound form is gone from the head.
  - The seam starts at index.html:3816 (by line number only).
  - The head's bounds file carries the new `REFUSAL`, its synthetic paste, and 18 `test(` calls.
  - The READY is 124 lines with no NexusAI text.
  - Gate 21's harness still names `CDP Input.insertText` (WRONG (b)'s premise).

## Launch command (after the stamps)
`/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate22' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate22.sh'"`
