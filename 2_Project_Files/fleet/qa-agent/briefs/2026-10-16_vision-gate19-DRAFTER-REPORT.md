# Vision gate 19 (QuickQuote PR #9 @ 5f08fe0, the email guard, C-20): drafter's report

Drafted 2026-10-16, 14:01 to ~14:20 AEDT, by a read-only drafter for Tuesday.
Outputs:
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-gate19-qq-pr9-email-guard.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate19.sh` (chmod +x, `bash -n` clean)
- this report

Nothing else was written in `fleet/`. Test copies of the brief, routing file and launcher were made in the session scratchpad only. There was no push, merge, `az`, docker, mail, browser or product process, and no write in the Vision project. The launcher was run only with `--check`. `gh` was used only for GET reads, with Vision's gh-config; that directory's file mtimes are unchanged (12 Oct 18:09).

## Numbering
This is **gate 19**. Gate 18 (PR #8) was drafted an hour earlier but is not stamped or launched: at 14:08 its brief still had 7 placeholders and there was no `QA/Vision-gate18` pane. The routing file stops at `QA/Vision-gate17`. The `gate19B` / `gate19C` names in old `inbox_routing.conf.pre-0922-*` backups are September NexusAI gates, so they don't collide. The new route name is `QA/Vision-gate19` and the target id is `QQGD`.

## What I kept from gate 18, and what I changed
- **Kept:** the PIN parser and the guards that apply to one commit (6/7/8/9/18/22/23/74/31/39/10/17/12/78/13-15/20/70/82/19/24/53-75/44/38R/86), the GET-only `gh` shim, the model read from `models_latest.json`, the empty-identity setup, the unset list, THE MODEL RULE, the question and verdict routes, HELD, the floor rules, the Laptop-DEV paths, and the stale-T9 rule.
- **Dropped:** all docker work. Guard 45D became 45N, which requires the brief and prompt to forbid docker. The launcher no longer runs a single docker command, not even a read. The PR files API and `rev-parse` both show that the Dockerfile, lockfile and `.dockerignore` are the same blobs, and the image would run the same `node strip.js` the gate runs on the host. The az shim is also dropped.
- **Set by your commission, so not left open:** `GH-API-LEG: READ-ONLY-VISION-TOKEN` and `AZ-READ-LEG: TUESDAY-READS`. Guard 47 now only checks that AZ-PRE-READ is stamped.
- **New:** guard 48 for `LEG7-METHOD` (D5).
- **New pins in guard 74:**
  - Kam's W1 and W2 by sha256, checked in the launcher's own copy, in `strip.js` and in the test file at the head.
  - The READY's line must equal `Warning: ` + W1 exactly.
  - The `test:print` change must be exactly one inserted file.
  - The only line removed from `strip.js` must be the old label line.
  - The package.json dependency maps must be equal (checked by JSON parse).
- **Deadlines:** browser cell 120 s, red-proof or mutant arm 420 s, whole `test:print` 900 s, nothing above 900 s. The brief tells the gate to raise its own copy of `qa-run.py`'s 420 s ceiling and to say that it did.

## Traps found while drafting (all in the brief's WRONG list)
1. **"Warning:" is a label, not part of Kam's text (WRONG (a)).**
   - Kam's card `quickquote-guard-words-1016` quotes the warning starting at "This email sends…".
   - The code renders W1 with no prefix and no glyph.
   - I hashed the card's strings and the code's constants: they are byte-identical (W1 sha256 `0d5beedb…eb25b9`, 220 bytes; W2 `4c73c159…3ec797d`, 28 bytes).
   - The commit message has ASCII quotes, but it is not shown to reps (WRONG (b)).
2. **The builder's test never reaches the server (WRONG (c)).** It stubs `/api/quote/email` and checks only the posted state. Whether the second press really "sends standard pricing" is decided by the unchanged server path. So §N3 and §N7 drive `createApp()` with the real `renderQuotePdf` and a capturing stub mail, and §N7 checks that the email after the second press carries only standard figures.
3. **Programmatic print-mode resets don't disarm the guard (WRONG (d), my inference).** `index.html` sets `pmDefault.checked = true` without firing an event in three places: Reset form, emptying the custom ticket, and turning Advanced off. After that, the button can still say "Send standard pricing anyway" in standard mode. The money would be right; the screen would be stale. These are probes E2-E4.
4. **A double-click sends (WRONG (e)).** The first click arms the guard and the second sends, with no debounce. Probe E1 measures it. It is a finding for you or Kam, not a FAIL, because the approved words say "press the button again".
5. **The red-proof needs the head's test run on base code (WRONG (f)).** The test file doesn't exist at `e4ce536`. §N2 builds that tree and runs three mutants (G19-M1 to M3).
6. **A publish of `5f08fe0` would ship PR #7 too (WRONG (h)). This is the one that matters at PUBLISH GO.**
   - Live is expected to be `v0.6.3-tool2.35-3dd15bc` (your 10-13 note, 12:29).
   - `git diff --stat 3dd15bc 5f08fe0` is 4 files, +225/−18. That is the guard plus PR #7's `basic-ftp` override and its 34-line lockfile change.
   - PR #7 was merged but never published (C-18), and only your tier-2 source check covered it.
   - C-20's grant covers "the GUARD only". The gate lists the exact live-to-head delta in §N8.3. Deciding whether that needs Kam's word is yours at PUBLISH GO, not at launch.
7. **The box is overloaded (WRONG (i)).**
   - Load at 14:08 was 184.10 / 226.20 / 234.67, with eleven MPS lanes running.
   - The brief requires one browser at a time, sequential runs, one retry per cell, and the load recorded beside every timing.
   - Under D4, the verdict is PROVISIONAL only if the red-proof or the head's S2/S3 rows are NOT RUN.
8. **Gate 18 may run alongside this gate.** It is docker-heavy and uses `qa-g18-*` and `work-g18`. This gate never touches either. If gate 18 is live, the launcher prints a NOTE.
9. **Moving main.** If PR #8 merges first, main moves. The launcher pins main exactly, so a launch after that refuses and needs a re-pin. A gate already running continues on its shas, and §12 names the cells to re-run.
10. **Timestamps disagree (WRONG (l), not load-bearing).** `decisions.json` has `ruled_ts` 13:29:39 and 13:52:18. Your commission and note say 13:25:51 and 13:51:38. The choice and the text agree everywhere.

## Verified at source (drafter, 14:01-14:20)
- **Heads (`ls-remote`, 14:01:52 and again at the `--check` runs 14:18:50 / 14:19:20):** main `e4ce536`, branch `5f08fe0`, `refs/pull/9/head` `5f08fe0`, `refs/pull/9/merge` `deb50819`.
- **Chain:** one commit, single parent `e4ce536`, tree `dc6aef6`.
- **Diff:** numstat 1/1, 28/1, 175/0. This matches the PR files API (3 files, +204/−2).
- **Unchanged blobs:** all 17 the brief lists, including `index.html` `447b129`, the lockfile and the Dockerfile.
- **GitHub (GET reads):**
  - PR #9 is open, not merged, mergeable_state clean.
  - Runs 38842678755 and 38842703255 succeeded, 5/5 jobs each.
  - CodeQL check runs succeeded.
  - Main has 0 open code-scanning alerts. Dependabot shows #1 and #4 open (extract-zip; PR #8's business).
- **Clarifications:** C-20 is present with "Kam's grant covers the GUARD only".
- **Server:** `createApp` accepts a `clock` option.
- **Page:** the `.svc-warn` light and dark rules and the three `printMode` radios exist.
- **Model:** `models_latest.json` opus is `claude-opus-5-5`.
- **Gate 17's tools:** all 20 named tools are on the T9.

## Not verified
- The builder's two measurement STATUS mails (02:10Z and 02:3xZ) are not on disk anywhere I searched. That is why D5 exists.
- Whether Chromium keeps the `Secure` session cookie on `http://127.0.0.1` (WRONG (j)). The brief gives a CDP fallback.
- The live `linuxFxVersion` (yours to read).
- Whether E1-E8 behave as I inferred.
- That `fbd892e` (the QQ BACKLOG commit) exists. The gate checks it.

## `--check` on the real files (final run, 14:18:50 AEDT)
```
NOTE: fleet-monitor has no single live claude — not a negative control
REFUSING: AZ-PRE-READ is '@STAMP@' — Tuesday reads the live linuxFxVersion before launch and writes it there
REFUSING: the brief's LEG7-METHOD line is still TUESDAY-DECIDES — Tuesday sets GATE-METHOD or STATUS-MAILS (decision D5) before launch
REFUSING: no 'QA/Vision-gate19|tuesday-agent@agentmail.to|…' line in /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate17 line) before launch.
REFUSING: the brief still carries 7 @STAMP@ placeholder(s) (Self-check line and note, AZ-PRE-READ, the RULED lines of D4-D5) — the coordinator re-reads end-to-end and stamps all of them before launch
guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 45N 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 38R 86 46); coordinator to-do pending (47 48 41 32 as listed above); exiting 47.
  origin re-read 2026-10-16 14:18:50 AEDT: main e4ce536, QQGD 5f08fe0, refs/pull/9/head 5f08fe0; model claude-opus-5-5; GH-API-LEG READ-ONLY-VISION-TOKEN
  NEG seats (38R, derived live): `74294` (tuesday); `34873` (Datasec/Vision_Sales_Portal); `27153` (QA/NexusAI-batch23);
rc=47
```
After that run I fixed two stray placeholder mentions of gate 18 in the brief, so the count is now **5**: the SELF-CHECK line, the Self-check note, AZ-PRE-READ, D4 RULED and D5 RULED.

Two refusals fired during drafting and were fixed:
- rc 74: a bare `rev-parse <sha>:<missing path>` echoes its argument, so the "new file absent at base" check read as present. It now uses `cat-file -e`, and `blob()` uses `--verify -q`.
- rc 31: the brief was missing the literals "WRONG (c)" and "WRONG (f)".

## Tests on scratch copies (session scratchpad; nothing in `fleet/` touched)
- **Fully stamped copy** (placeholders filled, `LEG7-METHOD: GATE-METHOD`, routing line added): **rc 0, "all guards pass"**, pinned table printed, origin re-read at 14:19:20.
- **Negative controls:**
  - W1 with one curly quote changed to straight in the launcher: refused, "own copy of Kam's words does not hash".
  - `LEG7-METHOD: STATUS-MAILS` with no mails file: refused by guard 48.

## To launch, Tuesday:
1. **Re-read the brief end-to-end and stamp it:**
   - the SELF-CHECK line and note;
   - `AZ-PRE-READ`: read the live linuxFxVersion with your az (tenant d500ebad / sub 0c57ab37). One reading can serve gates 18 and 19 if taken right before both;
   - `LEG7-METHOD` (D5): GATE-METHOD, or STATUS-MAILS after saving the two STATUS mails verbatim to `briefs/2026-10-16_vision-qq-printmode-STATUS-mails.txt`;
   - D4 RULED and D5 RULED.
2. Add `QA/Vision-gate19|tuesday-agent@agentmail.to|no` to `fleet/inbox_routing.conf`.
3. Decide whether to launch at the current load, and whether to run it alongside gate 18. Keep PR #8 unmerged until this gate launches, or the main pin refuses.
4. Run: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate19' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate19.sh'"`
5. **At PUBLISH GO (later, not now):** read §N8.3 on what a publish of `5f08fe0` ships beyond the guard (PR #7's lockfile change) against C-20's "the GUARD only".
