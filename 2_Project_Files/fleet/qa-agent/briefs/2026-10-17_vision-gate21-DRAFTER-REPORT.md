# Vision gate 21 (QuickQuote PR #10 ROUND 2 @ 3a3399e, round 2 of 2 under the cap; custom-price bound ratio 10; v2.38): drafter's report

## BLUF
- **Drafted:** the gate-21 kit for QuickQuote PR #10 round 2. It is tier 1, round 2 of 2 under the two-NO-GO cap: a NO GO ships the closed
  instances and tickets the rest, with no round 3 without Kam.
  - **What it keeps:** gate 20's whole email-equals-print matrix (§N3-§N5).
  - **What it adds:** §N10 re-tests every G20 finding as a check that can fail (red at `7b952f6` or base, green at `3a3399e`, and a CLOSED / OPEN /
    NEW closure table). §N11 probes the ratio-10 bound at its edges on screen, print, email, workbook and the offline page.
  - **Not run:** the launcher only under `--check`.
- **Head did NOT move.** `git -C '<Vision>/Quoting Tool/hpas-quoting-tool' ls-remote origin` at **2026-10-17 07:39:16 AEDT** read:
  - `refs/heads/fix/qq-email-matches-print-2026-10-16` = `refs/pull/10/head` = `3a3399e947bf5faf8a8e0c0d3e11956c6590db98`;
  - `refs/heads/main` = `HEAD` = `437ab4bc412bc74d8da3b66a6ac5c71d7335c5d6`;
  - `refs/pull/10/merge` = `1345ea5…`.
  - `git cat-file -t`: `3a3399e` commit, `437ab4b` commit, `7b952f6` commit.
  - The launcher re-read origin at 07:57:44 and 07:58:10: unchanged.
- **The biggest trap (WRONG (b)): the bound is checked when a price is ENTERED, against the standard price at that moment. The renderer then re-checks
  it against the POSTED state, in EVERY print mode.**
  - The denominator follows the app selection: bundle USD 20, Manager only USD 5.
  - A rep sets A$300 (9.7×), then unticks apps. The page keeps printing that price, and the email is predicted to be refused with 422.
  - **That includes a "Standard pricing only" email**, because `pdf.js` calls `cpRestore` for any non-null `pdmUSD`. The stale `pdmUSD` that is
    still posted after Advanced off (gate 20's O4) reaches the same path.
  - I wrote a refused STANDARD email as a FAIL (§N3, §2a, P3', §N11 B-STATE). That is a drafting call: if you disagree, change it before you stamp.
- **Tuesday must stamp 6 slots** (the launcher refuses with rc 47 until they are done):
  - `SELF-CHECK:` and `Self-check note:`;
  - `AZ-PRE-READ:`;
  - `N4-METHOD:` (D5; drafter: FULL-TEXT, as you ruled for gate 20);
  - `ROUTING-LINE:`, and add `QA/Vision-gate21|tuesday-agent@agentmail.to|no` to `inbox_routing.conf`;
  - the `RULED:` lines of D4 and D5.

## Outputs
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-gate21-qq-pr10-r2.md` (the brief)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate21.sh` (chmod +x, `bash -n` clean)
- this report

**Not written:** `inbox_routing.conf` (not edited) and anything in the Vision project or the QuickQuote repo. Test copies of the brief, the routing
file and the launcher went only to the session scratchpad (`…/scratchpad/g21test/`).

**Not done:** no push, merge, fetch, `az`, docker, mail, browser, npm or product process. `gh` was used for GET reads only, with Vision's gh-config;
its two files' mtimes are unchanged (12 Oct 18:09:30, re-read 07:59). No HTTP went to any live or production host.

## SHAs measured (commands)
- **Origin:** `git --no-optional-locks -C "$R" ls-remote origin` at 07:39:16, values above. Main and HEAD are both `437ab4b`. PR #8 is still open
  (`4d6ed6e`). `backlog/qq-extract-zip-2026-10-16` = `815aae7` (F8's ticket; not an ancestor of the head).
- **Commit types:** `git -C "$R" cat-file -t 3a3399e | 437ab4b | 7b952f6` → commit ×3. `git -C "$R" rev-parse` gives the 40-hex values.
- **Chain** (`git log --format='%H %P'`), single parents: `437ab4b` ← `0fc280b` ← `a8d769b` ← `7b952f6` ← `a7e1835` ← `1f7db41` ← `3a3399e`.
  - `rev-list --count`: 6 ahead / 0 behind; merge-base `437ab4b`.
  - `7b952f6` is an ancestor of the head, so there was no force-push (the READY's claim holds).
- **Trees:** head `ec15fb2`, round 1 `25ddfb8`, main `c71780c`.
- **Numstat:**
  - whole `437ab4b..3a3399e`: 8 files, +657/−119, which equals the PR files API (GET 07:42:14);
  - round 2 `7b952f6..3a3399e`: 7 files;
  - per commit: `a7e1835` 6 files; `1f7db41` email-matches-print only; `3a3399e` index.html +2.
- **The hosted server module changes in round 2** (`a854ba2` → `e40c20e`, +9: the 422). Gate 20's "unchanged server module" premise is gone (WRONG (j)).
- **Unchanged:** the lockfile, Dockerfile, `.dockerignore`, xlsx/mail/store, tests.yml, server.test.mjs and CLAUDE.md have the same blobs at all three
  shas. So the gate still runs no docker.
- **GitHub (GET reads):**
  - PR #10: open, not draft, mergeable_state clean.
  - CI runs on `3a3399e`: 38962577169 (push), 38962582879 (pull_request) and 38962578337 (dynamic CodeQL), all completed success.
  - 13 check runs, all success. CodeQL: "No new alerts in code changed by this pull request".
  - Open code-scanning alerts: main 0, `refs/pull/10/head` 0.

## TRAPS — where round 2 could pass the matrix without fixing the defect, or fix it and break something else (all in the brief's WRONG list; each is a claim for the gate to measure)
1. **(b) Bound applied at entry, not on state change, while the email path re-checks in every mode.** See BLUF. Gate 20's grid would never see this
   because it never changes the apps after setting a price. P3' and §N11 B-STATE do.
2. **(c) Wrong-reason reds at `7b952f6`.** On `7b952f6` `#cpRefused` does not exist, so a bounds cell can fail on "no element" instead of on ∞.
   - The gate must classify every red as DEFECT-REASON or NEW-SURFACE-ABSENT.
   - It must use head mutants to show that each defect assertion can fail: G21-M1 (page-only bound off), M2 (renderer-only), M3 (route-only).
3. **(d) The builder's cells test only absurd values** (1e308, 0, −1, "27.9", {}, −100 %).
   - A ratio of 1000, or even 1e300, passes every one of them.
   - **G21-M4 (ratio → 1000) is predicted to be seen by NO committed cell.** §N11 tests the edge directly: A$309.99 / A$310.00 / A$310.01, Apply +900 / +900.01.
4. **(e) "More than zero" leaves G20-F1's same class (A$0.00) open.**
   - `0.001`/month, a `cpDay` of `0.0001`, or Apply −99.99 is accepted.
   - The ticket, the print and the email then read **A$0.00/device/month**.
   - Gate 20 put `pdmUSD: 0` → A$0.00 in F1's same class. §N11 L-EDGE measures this. I told the gate to treat it as a finding, not a FAIL, and to
     ask you if it needs a ruling.
5. **(f) Non-numeric and locale entries clear custom pricing SILENTLY.**
   - In `cpSyncFrom`, NaN or an empty value calls `cpRefuse("")` and switches the mode back to standard, with no sentence.
   - The fields are `type=number`, so `1,234.50`, `27,90` or `abc` probably read back as `""` (unverified).
   - The READY says "refuse anything else with a message", so this contradicts its claim. Email still equals print (both standard).
6. **(g) Typing passes through refusals, and a refusal drops the print mode.**
   - Backspacing an existing price to empty, or typing a leading `0`, sets `cpState = null`. That flips "Custom pricing only" to standard.
   - The next valid key restores the price but not the mode. The `role=alert` box flashes on the way.
   - Gate 20's F2 could not reach this, because typing was clobbered then. Covered by R1-F2'.
7. **(h) Mixed versions change shape.**
   - A v2.36 tab open across a v2.38 publish: W1 promises "press again to send standard pricing anyway". The second press now gets **422 "This quote
     asks for custom pricing but carries no custom price… Reload the page"** instead of standard.
   - G20-F3 (a v2.38 tab across a rollback emails standard silently) is unchanged; the builder says so.
   - These are publish-card facts.
8. **(i) The bypasses that remain.**
   - The 12 email-matches-print cells still bypass the route.
   - The 15 bounds cells use the test file's own `memStore`.
   - `status: "refused"` has never met Azure Table Storage: store-azurite does not exercise it.
   - Refused rows (with customer state) are kept until full retention.
9. **(n) The F6 fix's message relies on `window.cpClear`.** It is the real function only once the advanced module is loaded. The gate must assert the
   price is actually cleared, not just that the sentence shows.
10. **(j) A refusal consumes a quote number.** The reservation happens before the render. P15 counts it, including a double-press on a refused state.
11. **Smaller points:**
    - The ticket's own 4-dp `cpDay` display of A$310.00 (10.1918) is just above max, so a rep who retypes the shown figure is refused (drafter arithmetic).
    - `G21-M2` must run without re-running `node strip.js`, because strip regenerates the mutated file. The brief says so.

## Kam-facing facts for the eventual publish card (each still a CLAIM until the gate measures it)
- **THE NUMBER:** the maximum custom price is **10 × the standard per-device price of the current quote**. The builder chose the ratio, and it sits in
  `CONFIG.customPriceMaxRatio` for Kam to change.
  - With seeded rates on the full bundle: **A$310.00 / US$200.00 / CA$284.00 per device per month**.
  - On Manager only: A$77.50 / US$50.00 / CA$71.00.
  - These are my arithmetic from CONFIG. The gate's §N11 replaces them with measured figures.
- **The minimum is "anything above zero"** (trap 4). A 99.99 % discount is a valid custom quote that prints as A$0.00/device/month unless the gate
  finds otherwise.
- **Round 2 adds four sentences that reps (and, through the email, nobody else) will see:** the page refusal, the email refusal ("…The quote was not
  sent."), the no-price refusal ("Reload the page and press Email again"), and the reopen sentence ("Custom pricing is not saved with a quote, so it
  is off…"). The READY gives their exact wording.
- **Behaviour change:** reopening a custom quote, even in the same page, now comes back standard, and the rep is told so.
- **Version:** v2.38 (2.37 was gate 20's round 1 and never shipped). The published tag would be new; rollback is still `v0.6.4-tool2.36-437ab4b`.
- **Still from round 1:**
  - W1/W2 retired.
  - The note ruling and its paper caveat: G20-F5, the note is on screen only.
  - G20-F3: rollback with v2.38 tabs open emails standard silently.
  - G20-F4: the lone revert of `a8d769b` makes W1 false.
- **New with v2.38 (trap 7):** a v2.36 tab after the publish gets a refusal on press 2 instead of standard.
- **What a publish ships:** 8 files including the hosted server module, but no lockfile or Dockerfile change. A publish needs **Kam's own word**
  (C-20), not the gate's.

## What Tuesday must stamp before launch (the launcher refuses with exit 47 / 48 / 41 / 32 until all are done)
1. `SELF-CHECK: re-read end-to-end for contradictions | <time, Tuesday, lines read>` and `Self-check note: …`.
2. `AZ-PRE-READ: linuxFxVersion …`, read with Vision's own AZURE_CONFIG_DIR (tenant d500ebad / sub 0c57ab37). I expect `v0.6.4-tool2.36-437ab4b`;
   the launcher prints a NOTE if the value does not name `437ab4b`.
3. `N4-METHOD:` = `FULL-TEXT` or `FIGURES` (D5), plus D5's `RULED:` line.
4. D4's `RULED:` line. My D4 adds the cap clause and makes the verdict PROVISIONAL if any of these is NOT RUN: the R1-F1 red/green pair, or §N11's
   U-AT / U-OVER / B-STATE rows.
5. Add `QA/Vision-gate21|tuesday-agent@agentmail.to|no` to `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf` and stamp
   `ROUTING-LINE: QA/Vision-gate21 …`. The launcher requires the line to begin with exactly that text.
6. **Before stamping D4, decide one open point.** "Ships the closed instances" on a single PR, where an OPEN instance might be a customer-document
   defect, may not be separable. Decide what "ship" means here: merge plus a Kam card, or hold.

## `--check`
- **On the real files (07:57:44 AEDT): rc 47.** Every content guard passes. Only your stamps are pending:
  ```
  NOTE: fleet-monitor has no single live claude — not a negative control
  REFUSING: AZ-PRE-READ is '@STAMP@' — …
  REFUSING: the brief's N4-METHOD line is still TUESDAY-DECIDES — …
  REFUSING: no 'QA/Vision-gate21|tuesday-agent@agentmail.to|…' line in …/inbox_routing.conf — …
  REFUSING: the brief still carries 6 @STAMP@ placeholder(s) (…) — …
  guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 45N 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 38R 86 46); coordinator to-do pending (47 48 41 32 as listed above); exiting 47.
    origin re-read 2026-10-17 07:57:44 AEDT: main 437ab4b, QQEP 3a3399e, refs/pull/10/head 3a3399e; model claude-opus-5-5; GH-API-LEG READ-ONLY-VISION-TOKEN
    NEG seats (38R, derived live): `91571` (tuesday); `34873` (Datasec/Vision_Sales_Portal);
  ```
- **On a fully stamped scratch copy** (TEST values, `N4-METHOD: FULL-TEXT`, routing line added): **rc 0, "all guards pass"**, and the pinned table
  printed at 07:58:10.
- **Negative controls**, each refused as it should:
  - READY copy with one byte appended: rc 31.
  - `N4-METHOD: WHATEVER`: rc 48.
  - PIN commits 5: rc 8.
  - PIN head set to `7b952f6`: rc 40.
  - routing line absent: rc 41.
  - W1 in the launcher edited (curly to straight quote): rc 74.
  - `ROUTING-LINE: done`: rc 32.
- **Two refusals fired while drafting, both fixed:**
  - rc 31: the brief lacked the literal `WRONG (n)` and `cdcd490`.
  - rc 78: the prompt lacked `buildPrintDoc`.

## Launch command (after the stamps)
`/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate21' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate21.sh'"`

## Notes and limits
- **Gate 20's verdict body is not in the mail batch.** The batch file `/private/tmp/wed_newmail/batch_20261016T203647Z.txt` has the gate-20 verdict
  row (20:15Z, subject as commissioned), but its body field reads `None`, in both copies of the row. I read the body from the gate's own saved
  copy, `…/2026-10-17-vision-gate20-qq-pr10-email-matches-print/evidence/mail/verdict-body.txt` (sha256 `f16c98fb…`), and its report whole (sha256
  `ab77c006…`). The brief cites both.
- **Copying the READY was not needed.** You had already saved the round-2 READY (5,416 B, sha256 `303d9298…`). The launcher pins that sha.
- **Instruments now come from gate 20's `evidence/tools/`** (26 files, all present), not gate 19's.
- **Not verified, all left to the gate:**
  - what the live site serves (yours: AZ-PRE-READ);
  - every probe outcome above (they are code readings);
  - Chrome's `type=number` behaviour on pastes;
  - whether float arithmetic refuses an exact A$310.00 on any route.
- **Load** at drafting: 7.48 (07:44).
