STARTABLE: YES

# B1054 DRAFTER REPORT: tier-2 QA gate kit for NexusAI RD-912 (branch b1044/nexusai-rd912-roster-reads @ 85df2de0)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1054_SEAT-G262_nexusai-rd912-gate-tier2.md` (121 lines; 8 lines carry the four-underscore pattern: the 7 slots S1-S7 and the last line; `@[A-Z_]+@` 0 with a firing control; non-ASCII 0; person-name scan 0, with "product owner" 5 as the control). Drafted Sun 1 Nov 2026 16:02-16:2x AEDT.

## BLUF
- This is a startable Sonnet G2 gate (model-routing.md:109) in the shape of B1050 (and its ADDENDUM-1: the organization-variables read goes to the repo-scoped endpoint) and B1023. Pane `Datasec/NexusAI-G262`. Ports 9750-9759 are reserved and should go unused. Round 1 of 2.
- **The class is the SAME as before, not a new one:** "a roster read holding an empty entry", B1023's class. RD-912 is B1023-1 and B1023-2 filed as a ticket. The only earlier verdict on the class is B1023's GO WITH FINDINGS, so no NO GO has been spent. That makes this gate 0 of 2 before, round 1 of 2.
- **The check that matters most** is the HOLD's re-run of the isolation probe (C5 part A). B1023's own `isoinject.js`/`isodrv.js` are copied unchanged (sha256 pinned) and run on the new head in down and stand-in modes, plus a base-swap run. The seeded user's `all` row must now be HTTP 200 and equal to the unarmed answer. B1023 received the handled error text there, so this row is RD-912's Done-when.
- The gate also runs work of its own beyond the builder's:
  - Part B probe: empties FIRST, stack-based site attribution per read, and a `nonlist2` arm. It should separate the builder's surviving mutant MX from the head and prove P4 (a non-list is unchanged from main) at runtime. The drafter's prediction from source says MX answers HTTP 500 where head and main answer the handled text.
  - New mutants: MP (keeps primitives) and MD (drops objects with a null name). Both are predicted F3 survivors that the unit differential catches.
  - MT-W14 and MT-main: empties AFTER the rows. MT-W14 is predicted to let W14 survive, which shows why the builder put them first.
  - W14/W34/W85: "wrap only two of three".
- **RD-913 may land while the gate runs.** B1050 wrote GO WITH FINDINGS at 16:03, so the MAIN-MOVED RULE treats that landing as EXPECTED BUT RE-VERIFY. The gate recognises it by three signals: the file list, lock blob `2e64988d`, and parent `79dc9f59`. It then rebuilds the merge in `worktrees/b1054-merge`, runs `npm ci` there, runs the rd869 file once, and verifies against the counts file at that merge (5268/311).

## Facts re-measured by the drafter (instrument, time)
- `git ls-remote` (16:03:06): main `89375808...`, branch `85df2de0...`, b1045 `79dc9f59...`, `refs/heads/b1054*` none.
- `gh api -X GET compare` shows ahead 1 and behind 0, with three files: test +110 -0 (`9a10c40f`), `server.js` +8 -3 (`d9e0bb05`), counts +2 -2 (`bcc17555`). The commit's parent is `[89375808]` and its tree is `ba9e3fd1`. The commit message was read whole and its sentences are quoted for C9.
- Raw contents GETs plus `git hash-object` (head and main):
  - `diff -U0` of `server.js` shows exactly the four hunks the builder kit specified.
  - The test file's first 675 lines `cmp`-equal main's. Its 17 `expect(` lines each carry `// FAIL:`. Percent signs 0, non-ASCII 0 (control: the counts file reads 3).
  - The counts key diff is `tests` 5267->5268 and `_updated` only.
  - RD-910's lines (main 8088-8089, head 8093-8094) are byte-equal.
  - The workflows, `verify-suite.sh`, `package.json`, `package-lock.json` and the harness are blob-equal at main and head.
- Census at head with the frame `getAllPrinterLogs({ limit: 1000 })` finds 12 lines (control: `getAllPrinterLogs` 53). The nine not wrapped are 7275, 8092, 8186, 8225, 9451, 10212, 10382, 13961, 14078. **The frame trap is written into the kit:** an unbounded `limit: ?1000` regex also matches the 15 `limit: 10000` reads, and a bounded regex reads 12.
- Hosted (16:03:16): one check-run, `audit-production-deps` 124755786199, failure. One run, 41275167489 npm-audit, push, failure. Package files equal main's, so this is main's red. No Build, Gitleaks Scan or CodeQL ran on the branch.
- Deploy switch (16:03:18): repo variables 0, repo-scoped organization variables 0, environments [dev]. The last 5 Deploy demo runs were all skipped, and the latest run's jobs `build` and `deploy` were skipped. `deploy-demo.yml` lines 26-32/53/91/95 were quoted from the head blob.
- Round census, first-line loop over 107 STATUS files: 37 verdicts and 6 NO GO (B592, B647, B667, B906, B912, B926), control 1. B1023 is the only verdict on the class.
- B1050 STATUS (mtime 16:03): its first line is the GO WITH FINDINGS verdict and its last line the matching `VERDICT:`.
- Seat G262: 0 files (control G259: 12). Panes at 16:04: HPSM-POC-G261, NexusAI-G259, fleet-monitor, tuesday. `session-tools/b1054` and `worktrees/b1054*` are absent.
- Ports 9750-9759: `lsof` rc 1 (unrestricted listing 15). The scan of 85 non-`.pre-` SEAT kits of 10-31 and 11-01 finds `975[0-9]` in 0 kits. Controls: `974[0-9]` in 9 kits (HPSM-POC and Composer, which is why I did not take 9740-9749) and `97[0-9][0-9]` in 16.
- Lock tool sha256 is `cf01baf...` (equals B1050's FACTS). At 16:04 the jest lock was not held and the queue was empty. load1 was 14.12.
- B1023 probe files (sha256, `wc -l`, read whole): `isoinject.js` `a6371f40...` (24), `isodrv.js` `9cccd40f...` (64), `r1-fence-quiet.js` `c16b65f9...`, `fence-preload.js` `55eaafcb...`, `tk.sh` `f9138721...`. **`isoinject.js` appends the empties AFTER the rows**, which is why part B adds `allfirst`.
- Model: `models_latest.json` line 23 `claude-sonnet-5-5`. `brief_seat.sh` line 24 `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`, so the level is written inside the quotes of the launch line.

## D-decisions (the drafter's; Tuesday may strike any)
- **D1. Class and round.** The class is the same: "a roster read holding an empty entry" (see BLUF). Rounds count NO GO verdicts, and B1023 was a GO, so this is round 1 of 2. Treating it as the same class is the conservative reading for the G-cap.
- **D2. One installed tree.** Every main-side run is a BASE-SWAP of `server.js` in `b1054-head`: write main's blob (`b673c3b4`, the builder's MR), run, then restore to `d9e0bb05` with a `diff --quiet` proof. This replaces a second worktree and a second `npm ci`, because load1 was 14 at drafting. It is valid because main and head differ in exactly the three paths and jest does not read the counts file. The kit has the gate prove that by program.
- **D3. The gate's own mutants beyond the builder's.**
  - MP and MD are predicted F3 survivors. Each must be caught by the gate's helper-check, which extracts `keepRosterRows` by program.
  - MT-W14 is predicted to let W14 survive, and MT-main is predicted to turn the 500 into a handled 200. Together they show the empties-first order is load-bearing.
  - W14/W34/W85 cover "wrap only two of three".
  - MX is separated by part B's `nonlist2`.
  - Grading: a predicted survivor caught by its named instrument is a Note. A survivor nothing separates is a Note carrying the unpinned property as ticket text.
- **D4. Part A copies B1023's probe files unchanged**, so the row that was B1023-1 is measured exactly as B1023 measured it. Part B is fresh and adds three things:
  - empties first;
  - per-read stack site attribution, which proves which of 7314/7334/8092 each read is;
  - the `nonlist2` arm.
  - The drafter's prediction from source is written into the kit; the gate writes its own to evidence first.
- **D5. Sibling (10190) in stand-in mode is NOT TESTED by design** unless the gate plants a user through `plantUser`/`withDb` extracted by program from the head test file (lines 71 and 58). F3 and W85 cover the sibling in down mode.
- **D6. Census rows are FINDINGS (Note), never fixes.** The gate must read `getStatsFromLogs` (head 5879) for 9451, which the builder did not.
- **D7. STATUS-NOW tightened.** The `WORKING:` line must be rewritten after every check AND at least every 20 minutes during a long ticket. This responds to the builder's two-hour stale line. That lapse (RELAYED, not re-measurable) and the stale `## TESTED (interim, 15:12 ...)` heading in the final B1044 STATUS (measurable) are graded process Notes.
- **D8. The hosted npm-audit red on the branch is a Note** (package files equal main's: RD-913's lane). Its job log is read GET-only in C8.
- **D9. Landing data:**
  - `pr-body.txt` carries an "Unchanged by this PR:" paragraph naming the nine census lines.
  - `merge-body.txt` carries one trailer line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, the same form as B1050's.
  - A program asserts both, plus no seeded name in any of the four files.
- **D10. Target verdict 150 minutes and hard stop 240 minutes**, as for B1023/B1044 (about 24 tickets, including one ~23-minute verify).

## Q-questions for Tuesday (each with a default)
- **Q-1 Tier.** Sonnet G2, with G1 considered and rejected: no security, destruction, deploy or client-tester surface; the helper is spelled out; B1023 measured the mechanism. Any finding that changes WHICH user an answer shows escalates to an Opus G1. **Default: YES, Sonnet G2.**
- **Q-2 Class and round.** Same class "a roster read holding an empty entry", 0 of 2 before, round 1 of 2. **Default: YES.**
- **Q-3 Ports.** 9750-9759 reserved and expected unused (harness `reservePort`); a fixed listener is a STOP. **Default: YES.**
- **Q-4 MX grade.** If `nonlist2` separates MX (predicted), it is a Note, with ticket text recommending a non-list cell. If nothing separates it, it is still a Note, stating that D3 is unobservable at runtime. **Default: Note either way.**
- **Q-5 RD-913 order.** If RD-913's PR is ready first, it may take the next merge turn (C-196). This gate then follows the MAIN-MOVED RULE: rebuild the merge, `npm ci`, run the rd869 file and the verify at the merge. **Default: YES; RD-913 first if both are ready.**
- **Q-6 Seat.** G262 (0 prior files; G260 and G261 are taken today). **Default: YES.**

## UNMEASURED (by the drafter)
- RD-912's current Jira state and comments. I did not read Jira; RD-912 is RELAYED from the builder kit's AUTHORITY and the builder's PRIOR WORK. The gate reads it in C9.
- The contents of the hosted job log 124755786199. I did not read it; the claim that it is main's 14-row red is inferred from the blob-equal package files. The gate reads it in C8.
- The part-B predictions: derived from source, not run. In particular, that the follow-up ask's reads are 7314 then 7334 (the builder's fired counts 1 at main and 2 after support this) and that the `{}` arm throws inside the analysis function's try at head and main but at the call site under MX.
- The history of B1044's stale `WORKING:` line (RELAYED from Tuesday at 16:01).
- The exact line extent of `plantUser`/`withDb` in the head test file (only their start lines, 71 and 58, were read).
- Whether another NexusAI seat (a records seat for RD-913) will queue on the jest lock during the gate.

## Outside-the-fences disclosure
- I wrote only the two files. Nothing was cloned, fetched, installed, run or written in the project.
- Network:
  - `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (compare, check-runs, runs, pulls, variables, the repo-scoped organization variables, environments, Deploy demo runs and jobs, raw contents);
  - one `git ls-remote` with `--no-optional-locks`.
- The raw GETs were saved to my session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/b1054/`), not the project.
- Read-only, no writes:
  - I read files under `!CODING/Datasec/NexusAI/session-tools/b1023/instrument/` (a finished gate's instruments) to hash and quote them;
  - I listed `session-tools/` and `worktrees/` names, the lock's queue and owner path, `tmux list-panes`, `lsof` and `uptime`.
- I never used `decision_queue.sh`, briefs_staged, the scoreboard, `_ledger.md`, or any WEDNESDAY/FRIDAY tree.
- One command was refused by a shell hook (a `======` separator); it had no effect, and I re-ran it with `----`.
- No decision-card id and no person's name appears in the kit.
