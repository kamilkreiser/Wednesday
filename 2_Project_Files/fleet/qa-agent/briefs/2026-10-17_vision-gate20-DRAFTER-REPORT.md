# Vision gate 20 (QuickQuote PR #10 @ 7b952f6, email matches print, guard removed, v2.37; C-20 fix 2): drafter's report

Drafted 2026-10-17, 05:47 to ~06:10 AEDT, by a read-only drafter for Tuesday.
Outputs:
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-gate20-qq-pr10-email-matches-print.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate20.sh` (chmod +x, `bash -n` clean)
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_vision-qq-pr10-READY-mails.txt` — a byte-for-byte copy of the builder's two mails that you saved to the session scratchpad (sha256 `ac43ba5ddda1c49a4607207a7e34478bed400460b0ddd8c02a1aa6f38d7dba70`, the same at source and copy). The scratchpad does not last, and the gate needs the mails on disk. The launcher pins this sha.
- this report

Nothing else was written in `fleet/`. I did not edit `inbox_routing.conf`. Test copies of the brief, the routing file and the launcher went only to the scratchpad (`…/scratchpad/g20test/`). There was no push, merge, `az`, docker, mail, browser, npm or product process, and no write in the Vision project or the QuickQuote repo. The launcher was run only with `--check`. `gh` was used only for GET reads, with Vision's gh-config; that directory's file mtimes are unchanged (12 Oct 18:09:30).

## Numbering
- This is **gate 20**.
- The routing file stops at `QA/Vision-gate19`. It has no `gate20` name for any project (case-insensitive grep: 0).
- The new route name is `QA/Vision-gate20`. The target id is `QQEP`.
- Gate 18 (PR #8) was never launched: there is no report folder and no pane. If PR #8 merges before launch, main moves and the launcher refuses.

## What I kept from gate 19, and what I changed
- **Kept:**
  - the PIN parser and the same guard numbering;
  - the GET-only `gh` shim, the empty `AZURE_CONFIG_DIR` and the unset list;
  - the model read from `models_latest.json` (`claude-opus-5-5`);
  - THE MODEL RULE, the question and verdict routes, HELD, the floor and egress rules, the deadlines (120 / 420 / 900 s) and 38R's live negative seats;
  - NO DOCKER (45N). The lockfile, Dockerfile, server module, `xlsx.js`, `mail.js` and `store.js` are the same blobs at base and head.
- **Changed:**
  - **The pins.** Main is `437ab4b` (exact). The chain has 3 commits (`0fc280b`, `a8d769b`, `7b952f6`), each with a single parent. Both trees are pinned. The numstat is pinned for the whole delta and for each commit, and the `test:print` insertion is pinned. Blobs are pinned for the 6 changed files and for 17 unchanged ones.
  - **Guard 74.** It now proves Kam's W1/W2 are **absent** at the head and **present** at base. This is a sha256 scan of every string literal, so the base check is the control that shows the scanner can find them. It also pins the fix-2 anchors: `buildPrintDoc`, `cpExport`/`cpRestore`, `emailCopy`, `advanced.js`, `"2.37"` and the print CSS.
  - **Guard 31.** It pins the mails file by sha256. It requires the READY to have **no** NOT TESTED line, and the STATUS's only untested line to be carried verbatim in the brief.
  - **No T9 dependency.** Gate 19's report and instruments are on Laptop-DEV, so the prompt refuses any T9 path.
  - **Guard 48 (D5) is now `N4-METHOD`: FULL-TEXT | FIGURES.**
  - **AZ-PRE-READ.** It prints a NOTE if the stamped tag does not name `437ab4b`.

## Traps found while drafting (all in the brief's WRONG list; each is a claim for the gate to measure)
1. **(b) The "red 9/9 on main's code" was measured on a different main.**
   - `0fc280b` was rebased: its author date is 14:13, and its parent `437ab4b` is 15:07.
   - On `437ab4b` the v2.36 guard is in the page, so the new test's custom and both cells should fail on the guard (no post on the first press), not on figures.
   - §N2 runs the test on `437ab4b` **and** on pre-guard `e4ce536`. Mutants M2/M3/M7 are what prove the figures assertion can fail.
2. **(c) Neither builder test goes through the server route.** `email-matches-print.mjs` hands the stubbed body straight to `renderQuotePdf({advanced:true})`. §N3 uses `createApp()` and a capturing stub mail, as gate 19 did.
3. **(d) "Print text identical to main's" only holds after normalisation.**
   - I ran `pdftotext` on the builder's own PDFs. The differences are the quote number, `v2.36`→`v2.37` (two lines) and one line's spacing.
   - The brief expects exactly the qnum and version tokens to differ, and fails anything else.
4. **(e) The test's oracle compares money tokens from the screen DOM.** It never looks at the PDF itself. The drafter's `pdftotext` of the builder's email PDF against print PDF shows only qnum lines differ (4, 6 and 4 lines). That is why I recommend **FULL-TEXT** for D5.
5. **(f) "Reverts on its own" is unsafe.**
   - Reverting `a8d769b` alone brings back W1 ("This email sends standard pricing only… will not be in the email") while the email now carries the custom price.
   - So the sentence would be false. P12 measures it in the gate's own tree.
   - This belongs on the publish card: the safe rollback is the image.
6. **(g) The note exclusion cannot be seen in any PDF.**
   - The print CSS `.q-savings{display:none}` already hides the note in every PDF, printed or emailed, because `page.pdf` renders print media.
   - `emailCopy` changes only the screen DOM that the test reads.
   - Mutant M4 shows this. For the publish card: "Kam can reverse it" changes nothing a customer sees unless the print CSS changes too.
7. **(h) Rollback with v2.37 tabs open.**
   - A v2.37 page posting to a rolled-back v2.36 server emails **standard**, with no guard in front of it. That is the C-20 defect, back and silent, for every open tab.
   - This is inferred from the code. P11(b) measures it, and P11(a) measures the reverse.
   - It belongs on the publish card.
8. **(i) `pdmUSD` has no upper bound.** The check is finite and ≥ 0, so `1e308` passes. P10 measures crafted bodies.
9. **(a) The READY carries no NOT TESTED block.** Case-insensitive count: 0. The gate writes its own.
10. **C-05 reopen loses the custom price by design.** The server module does not store print mode or `custom`, and that blob is unchanged. Reopening leaves the page's current custom price in place, so it can carry into another quote. P6(a)-(c) measure this. It is reported, not graded; the comparison that counts is email = print.
11. **The FX race.** If a rep prints before the live rate arrives and emails after it, the paper and the email can differ. P9 answers the FX request inside Chrome with a canned rate, so there is no network.

## Verified at source (drafter, 05:47-06:10)
- **Heads (`ls-remote`, 05:47:35, and again at `--check` 06:04:53 / 06:06:52):** main `437ab4b` (= HEAD), branch `7b952f6`, `refs/pull/10/head` `7b952f6`, `refs/pull/10/merge` `d46f5f5d`.
- **Chain and trees:** the chain and its parents; head tree `25ddfb8`; main tree `c71780c` (equal to `818a019`'s, the builder's "main-818a019" evidence).
- **Diff:** 3 ahead / 0 behind. 6 files, +275/−108, which equals the PR files API. The unchanged-blob list holds.
- **GitHub (GET reads):**
  - PR #10 is open, not draft, mergeable_state clean.
  - CI runs 38949473743 and 38949480136 each passed 5/5 jobs. Check runs, including CodeQL, are all success.
  - Main has 0 open code-scanning alerts. Dependabot shows #1 and #4 open (extract-zip).
- **Code:**
  - The server module passes the whole posted `state` to `renderQuotePdf` and stores only its allowlist.
  - `btnReset` calls `cpClear`. `applyAdvanced(false)` sets the mode to default with no event.
  - `cpExport` survives Advanced off (it is inside the module).
- **Live and rulings:**
  - Live is expected to be `v0.6.4-tool2.36-437ab4b` (your 10-16 note, 15:25). So a publish ships exactly the 6-file delta: no lockfile, Dockerfile or server change.
  - Backlog `cdcd490` exists, and `5ef2a60` is v1.88.
  - C-20 says fix (2) needs Kam's own word to publish.
- **Load:** 5.70 at 05:51.

## Not verified
- What the live site serves now (yours: AZ-PRE-READ).
- Every probe outcome above. They are code readings, not measurements.
- Whether the offline `index.html` can be unlocked into advanced mode without a server. §N5.3 tells the gate to read the page and say how.
- Whether Chromium still keeps the `Secure` cookie on loopback (gate 19 measured yes).

## `--check`
**On the real files (06:04:53 AEDT), rc 47.** Every content guard passes; only your stamps are pending:
```
NOTE: fleet-monitor has no single live claude — not a negative control
REFUSING: AZ-PRE-READ is '@STAMP@' — Tuesday reads the live linuxFxVersion before launch and writes it there
REFUSING: the brief's N4-METHOD line is still TUESDAY-DECIDES — Tuesday sets FULL-TEXT or FIGURES (decision D5) before launch
REFUSING: no 'QA/Vision-gate20|tuesday-agent@agentmail.to|…' line in /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate19 line) before launch.
REFUSING: the brief still carries 5 @STAMP@ placeholder(s) (Self-check line and note, AZ-PRE-READ, the RULED lines of D4-D5) — the coordinator re-reads end-to-end and stamps all of them before launch
guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 45N 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 38R 86 46); coordinator to-do pending (47 48 41 32 as listed above); exiting 47.
  origin re-read 2026-10-17 06:04:53 AEDT: main 437ab4b, QQEP 7b952f6, refs/pull/10/head 7b952f6; model claude-opus-5-5; GH-API-LEG READ-ONLY-VISION-TOKEN
  NEG seats (38R, derived live): `94442` (tuesday); `34873` (Datasec/Vision_Sales_Portal);
```
**On a fully stamped scratch copy** (placeholders filled, `N4-METHOD: FULL-TEXT`, routing line added): **rc 0, "all guards pass"**, with the pinned table printed (06:06:52).

**Negative controls,** each refused as it should:
- W1 edited in the launcher (curly quote to straight): rc 74.
- `N4-METHOD: WHATEVER`: rc 48.
- AZ-PRE-READ unstamped: guards 47 and 32.
- The STATUS untested line removed from the brief: rc 31.
- The mails file tampered (one byte appended): rc 31.
- PIN commits 2 instead of 3: rc 8.

Two refusals fired while drafting and were fixed:
- rc 31: the brief was missing the literal "WRONG (d)" and the full mails sha.
- A malformed blob comparison for the server module was rewritten as a prefix match on `a854ba2`.

## To launch, Tuesday:
1. **Read the live linuxFxVersion** with Vision's own az config (tenant d500ebad / sub 0c57ab37) and write it on the `AZ-PRE-READ:` line. I expect `…:v0.6.4-tool2.36-437ab4b`; the launcher NOTEs if the line does not name `437ab4b`.
2. **Re-read the brief end-to-end and stamp it:**
   - the `SELF-CHECK:` line and the `Self-check note:`;
   - **D4 RULED** (class and PROVISIONAL rule);
   - **D5 RULED**, and set the `N4-METHOD:` line to `FULL-TEXT` (my reading) or `FIGURES`.
3. **Add this routing line** to `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf` (I did not):
   `QA/Vision-gate20|tuesday-agent@agentmail.to|no`
4. Keep PR #8 unmerged until launch, or the main pin refuses.
5. Run: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate20' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate20.sh'"`
6. **For fix (2)'s publish card, later (it needs Kam's word under C-20):**
   - W1/W2 retirement and the note line (your two rulings);
   - from the verdict: P11(b) (rollback with tabs open), P12 (the lone revert) and M4/WRONG (g) (the note is hidden on paper and in the PDF either way).
