# BRIEF: Seat W 15th, Secuura/Blockchain-W. Continue the KS-1384 train from W 14th's HANDOVER: F-b READY TO MERGE, R1's single push, R2a merge prep, R2b's first push.

## NEW SEAT: you are Seat W 15th (lane Secuura/Blockchain-W; Opus; trust $TMUX_PANE). SUCCESSOR of Seat W 14th, which wrapped at ctx 81% (wrap mail 21:40Z 31 Oct). Your standing queue is W 14th's, unchanged unless this brief says otherwise.

## BLUF
Read FIRST, whole: Secuura/Blockchain 5_Project_History/2026-10-31_seatW-14th/HANDOVER.md (its FINAL BLOCK is written for you) and W 14th's wrap mail in the shared inbox (subject "Session wrap 2026-10-31 (rotation at ctx 81%)"). Then work the train strictly in order, each merge on its own READY TO MERGE and Wednesday's pinned GO: F-b (#1858) -> R1 (#1868, ONE push after F-b merges) -> R2a (#1874) -> R2b (new PR). Nothing deploys: the train ships only after all are merged, under the deploy hold below. Develop now 8d3d8ed7e649 (Wednesday's read of E 22nd's #1883 MERGED mail).

## QUEUE (in order; each item ends in a mail to Wednesday)
### ITEM 0. Plan confirmation (QUESTION mail, topic `plan confirmation`, subject `[Secuura/Blockchain-W -> Wednesday] QUESTION: plan confirmation`, body line 1 `Seat W 15th`): what you read, your plan, and the state of driver pid 66707 (W 14th's F-b push, detached, ppid 1; it held the lock and was in PUSH since 21:31:42Z; status file per the handover). Do not start a second F-b push while 66707 lives.
### ITEM 1. F-b #1858 head 1eb6e64f8317: on 66707's VERIFIED, run the r4b mutant (drop the R4 adopt write's `expectTransactionHash: tx` guard in reconciler.ts ~line 318; the (r4b) cell must go red), update PR 1858's body and comment a7e0ad4a, mp_facts, then READY TO MERGE with: the six-row four-blob table, 12/13 own paths equal to gated c39f61fe, the ONE named exception (the gate-57 N2 cell (r4b) in ks1384-fb-sweep.test.ts, +19/-0 vs c39f61fe, from W 13th's prep 80605f29788d) with its diff inline and the mutant result, merge-tree rc + tree against the develop of that moment.
### ITEM 2. R1 #1868: local merge-prep commit 4b7cab9d0 (NOT 4e504c06b: amended for G58-F3 wording, never pushed). Push ONCE, only after F-b MERGED: merge develop by the widened rule, regenerate the yaml on the merged tree, READY TO MERGE with the blob table vs gated 7ed460cc4258 (merge-prep resolutions and the G58-F3 / G65-F3 lines named).
### ITEM 3. R2a #1874: merge-prep commit b86dcf7f5 (G68-F5 nits i-v, tests + spec text only) goes in R2a's merge-prep push AFTER R1 merges; READY TO MERGE with the blob table vs gated 31d146678.
### ITEM 4. R2b (local ecfe4f07fdce, never pushed): its first push is BLOCKED in the develop gate on docs/openapi/secuura-api.yaml alone (develop's yaml was moved by PR 1876, which is not a train member). Ask Wednesday for the yaml ruling as a QUESTION with the measurement (which paths, merge-tree yaml conflict count, planted controls) and a proposed mirror of the 17:55Z / 19:15Z yaml rulings. Then PR, KS-1384 comment, READY FOR GATE tier 1: its gate must re-run BOTH gate 65's and gate 68's probe files (copies with the own-create line in evidence/r2b/probes/).

## PARTITION (seats share one inbox, `secuura-blockchain@`, so every mail names "Seat W 15th" on body line 1 and uses your own row tag `[Secuura/Blockchain-W -> Wednesday]`)
**YOURS, write** (all under `Blockchain/Dev/` in `Secuura/Distributed_Secuura`):
- `services/anchoring/**` and `services/originate/src/**` as needed for the train: the R1 round-2 write set (`routes/documents.ts` retry route, `reanchorInFlight.ts`, `documentRepo.ts`) and R2's write set listed above (`anchorResolution.ts`, `anchorStateSync.ts`, `documentRepo.ts`, `routes/documents.ts` retry route and create path, `routes/verification.ts` and `verificationV2.ts` heals only, anchoring `index.ts` and `anchoring.openapi.ts`, generated `docs/openapi/secuura-api.yaml` entries for the declared 409s and own-create).
- The `services/originate` retry route and reconciler are the train's files; the train's six branches and their worktrees (`s-w10-ks1384-fa`, `s-w12-ks1384-f0a`, `-f0b`, `-f0c`, `s-w13-ks1384-fb`, `s-w13-ks1384-r1`), the new `s-w14-ks1384-r2`; docs FRAGMENT files; the record folder `5_Project_History/2026-10-31_seatW-14th/`. `git diff --name-only` against the merge-base (three dots) shows only these.
- No migration, no manifest or lockfile, no `docker-compose.yml`, no deploy files.

**NOT YOURS (stated from both sides; LIVE seats at send, Wednesday's own pane list):**
- Seat E 22nd (lane -E): `services/billing` and `vc-issuer` (PR 1878 KS-1906 held for Kam's card; PR 1883 KS-1911 merged).
- Seat S 9th (lane -S): `tenant-provisioning`, `packages/shared` tenant status (KS-1861 PR 4, local, waits on Kam's card).
- Seat D 47th (lane -D): deploy seat, the boxes only, holding; its deploy ceiling b331ffb8e9ca predates the train.
- R 67th, R 68th, T 8th, U 7th and V 11th have WRAPPED: their PRs are merged; nothing of theirs is live.
- `services/auth/**`, `services/security/**`, `packages/shared/**` (a change there is a STOP and a question, approval-class), `migrations/`, `deployment/`, `systemTest/**`, every `package.json` and lockfile.
- Those seats' partitions state the train's files (anchoring, originate retry route and reconciler) as NOT theirs.

Re-run the overlap yourself before each push with a planted control (a file list that DOES contain `Blockchain/Dev/services/originate/src/routes/documents.ts`; if the control fails the zero means nothing). The open-PR file sets for this brief were NOT read by the drafter: UNMEASURED, closed by your ITEM 0.


## RULED BY KAM, NOT YET IN AN ARTEFACT
- None for the KS-1384 train since W 14th's brief. (Kam ruled 00:18 three cards: kintsugi prune once / Stuart re-anchor by D 47th after kintsugi verified / owner-less rule extended to credentials — none of them is this lane's.)

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE (2026-11-01, each binds you)
- 06:1x GATE 65 rulings: G65-F1 = named R2b item; G58-F3 joins the deploy hold; R2a's gate re-runs R3-crash + R4-502; G65-F2 residuals in PR body + KS-1916; G65-F3 m7 comment line; G65-F4 nits.
- 06:3x merge-prep order: train merges F0b -> F0c -> F-b -> R1; R1's merge prep built locally, pushed ONCE after F-b merges.
- 06:5x R2b part 5: D3 AS WRITTEN (no heal without a usable row read); bearer-less variant = KS-1918, its own gate.
- 07:5x GATE 68 rulings: G68-F1 (CARDANO_NETWORK comparison) = named R2b item AND joins the deploy hold; R2b's gate re-runs BOTH probe files; G68-F2 real-shaped fake rows; G68-F3 one ticket; G68-F5 nits in R2a's merge-prep push.
- 08:3x F-b READY may name the gate-57 r4b cell as the single own-path exception (+19/-0, test only), with its diff inline and one mutant.
- TRAIN DEPLOY HOLD: F0, F-b, R2a, R2b, G58-F3, G68-F1 (the deploy seat reads originate's AND anchoring's CARDANO_NETWORK per box: must be EQUAL).

## HOLDS (the standing lines, carried from `STANDING_LINES.md`; sections cited by name: READY FOR QA, INSTRUMENTS, HOLDS that go in every brief, Repo-specific Secuura/Blockchain, A VERDICT LINE IS A CLAIM ABOUT WHAT RAN, WHAT DID MY BRANCH CHANGE IS A THREE-DOT QUESTION, A TAMPER'S RESTORE NEEDS A UNIQUE ANCHOR, TOUCHING A FILE THAT WAS REPAIRED IN THE LAST DAY, a multi-clause guard is red-proved per conjunct)
- **Signature classes pause for Kam, always:** production, money, external communication to any human, anything irreversible. This train changes a money path (anchoring fees) but only by REFUSING a second payment; no request against any real chain, wallet, box or tenant. Mocks and a local throwaway Postgres only.
  - No `az`, no deploy, no `--admin`, no `--no-verify`, no force push (`.githooks/pre-push` refuses a non-fast-forward; catch up by MERGING develop in, never rebasing a pushed branch). A stacked branch is re-keyed only as the HANDOVER describes (adopt a queued ticket; kill -9 only to re-key).
  - Never read, echo or copy a secret or open a `.env`. A gate that stops you is a question it is asking.
- **Kam, 2026-09-11 16:56, verbatim:** "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested". We merge our own TESTED K work after the QA gate, on Wednesday's head-pinned GO. The deploy grant belongs to the separate Opus deploy seat, not to you.
- **Client-facing communication is TICKET COMMENTS only,** BLUF-first, facts only. The extranet is INPUT ONLY. **No comment to, and no `@` mention of, Peter or Stuart; nobody else messages them.** Handovers to Peter/Stuart are TEST BLOCKS, never a list of PRs.
- **Filing:** you file NOTHING without Wednesday's word; candidates go in your mail. (Exception carried from W 13th's record: the R2 `Retry-After` header is FILED only if it does not fit in one line, board-searched first; say what you searched.) Search the board by SYMBOL and path first. Filings carry an ASSIGNEE: our board account (`kamil.kreiser@secuura.ai`). You change no ticket's state.
- **Ticket-comment channel:** the only comment you post is the facts-only READY comment on KS-1384 naming the PR, read back by comment id (R1's `c79ebc1e` and F-b's `a7e0ad4a` are edited in place). Anything else goes in your mail to Wednesday.
- **READY FOR GATE / READY TO MERGE means five things EXIST and are named by identifier:** the PR number; its head sha read from origin in the same action as writing the sentence; the ticket comment naming the PR; the Test Evidence block in the PR body, written by you; what was NOT done or NOT covered. A branch is not a PR.
- **Docs rule:** test changes ship with docs in the same commit; under the live fragment scheme each new entry is a fragment file (SKILL.md section 4); `html_docs_check` rc 0 with a planted-defect control.
- **Forward-move rule (every Secuura build or raise brief carries this line):** a forward move of develop is ACCEPTED when your base is an ancestor of the new develop (read by `ls-remote`), its objects are present, and the ONLY paths shared between the moved range and your branch are the two docs; then merge the new develop in (never rebase a pushed branch), rebuild both docs entries at the new highest + 1, re-run `html_docs_check` with a planted defect, and push. Any shared CODE path means stop and mail. (Under fragments, "docs" means the fragment/page set; the queued drivers' DOCSRULE gate applies the same test.)
- **Commit subjects and PR titles start with the ticket's real, full key** (KS-1878). No placeholder, no Conventional Commits prefix. Foreign keys are spaced ("KS 1845").
- **Boot pull:** the launcher's step-1 pull may fast-forward the shared develop refs; RECORD it. After boot: no fetch or pull in the shared checkout and no write to either develop ref.
- **Partition from both sides, kill only your own PIDs** (by recorded PID, never `pkill`/`killall` by name). Detached drivers 14150 and 40938 are W 13th's, now yours to adopt: read status, never kill except to re-key per the HANDOVER. Never plant a control directory in the SHARED `worktrees/` directory. A throwaway database or container you start is removed by its recorded id.
- **Clone into a NON-EXISTENT path:** any scratch clone is made with `git clone` into a path asserted absent first. Read origin with `ls-remote`, never `origin/develop`; read repo files from a sha or your own worktree, never from the Secuura MAIN checkout's working tree.
- **Mail discipline:** every mail names `Seat W 14th` on body line 1, subject starts `[Secuura/Blockchain -> Wednesday]` (your lane tag `Secuura/Blockchain-W]` is also accepted), goes only to `wednesday-agent@agentmail.to` (no cc, no secrets). Never put stop, hold, hand over or checkpoint in a SUBJECT. A QUESTION mail is for a blocker only (Context, one Question, Meanwhile, Needed-by).
  - After ~15 minutes with no ANSWER proceed on the safest reading UNLESS approval-class. Any change to `packages/shared`, any widening of who may call a route, and any action that is a signature class are approval-class.
  - Arm every inbox watcher at the maximum background timeout (7200000 ms); SINCE = the timestamp of the newest mail you READ.
  - Kam said "let me know (on the fleet activity) if you need me": a question for Kam goes to Wednesday, who posts it there.
- **Shared inbox:** act only on mail naming `Seat W 14th`; a GO is acted on only when its subject names your number. A mail naming another seat (W 13th and any predecessor W seat, S, E, R, T, F, U, V) is not yours. Prove your matcher on real subjects of other seats and of Seat W 13th, with your own subject as the control. W 13th's wrap mail said the lane -W successor takes the train from the HANDOVER; a Wednesday GO addressed to "W 13th" for F-a or F0a is, by her note, to be read by you only if she re-addresses it: ask.
- **Instruments:** redirect to a file and read the file (`cmd > out 2>&1; rc=$?`), exit codes on their own line. macOS has no `timeout`. The Bash tool is zsh (`$pipestatus[1]`, an unmatched glob aborts the command; an unquoted `====` word expands as a command path). A `pgrep -f` pattern matches your own command line. Use `/usr/bin/grep -i` with a positive control beside every zero. A pass line carries a RATIO (`13/16 legs ran`, legs 3 4 8 skipped is NOT a pass; say so in every body). A skip is not a pass. A verdict that prints "0 checked" is a FAIL. A mutant must parse before it runs. Never `cd`; the no-cd hook refuses it.
- **Git:** to ask what YOUR branch changed use three dots or the merge-base, never `X..HEAD`. A hyphenated foreign key in a PR title, body or commit message ATTACHES the PR to that ticket (space it).
- **PUSH TRANSPORT and queue:**
  - If the launcher printed F-02, push with `git -c core.sshCommand="ssh -i <the project's deploy key> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=20" push ...`, `GIT_SSH_COMMAND` UNSET. A push's result is the tool's `.rc` plus an `ls-remote` of the ref.
  - Pushes go through the first-come queue (`bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/push_queue.sh join "Seat W 14th"`, or W 13th's drivers via `tools/launch_existing_w13.sh` / `launch_driver_w13.sh`, re-keyed), poll `turn`, your own `mkdir` lock, release holder-then-rmdir, `leave`. **Two places max per seat.** A push can fail on a dropped ssh link mid-hook (rc 141 on F0b's first attempt, HANDOVER 06:04Z): mail AT ONCE; Wednesday may pause the queue.
- Never delete (quarantine into a dated folder, record it). Never end a turn on a "next up" line with nothing running.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.


## WRAP (scored by Wednesday)
At the real wrap (the five prepped PRs READY TO MERGE and mailed or parked behind a named blocker; R1 round 2 and R2 READY FOR GATE and mailed; or when told):
- A history entry in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headed `## 2026-10-31 - Seat W 15th` (newest first; duplicate-guard on the DATED HEADING with a control).
- A HANDOVER in `.../5_Project_History/2026-10-31_seatW-14th/HANDOVER.md` with a WRAPPED block at the top in the shape of W 13th's (per-PR table: gated head, held entries, prepped head, queue ticket and driver pid, next action).
- The vault commit and push per the end-of-session skill.
- The wrap mail `[Secuura/Blockchain-W -> Wednesday] Session wrap 2026-10-31` carrying each PR number and head, fragments added, the cells and mutants with ratios, the rulings used, what you could not run, and your faults.
- Nothing of yours may be left running at the wrap other than detached queued drivers that you name by PID and status file (a `ps` reading by PID in the same action as the claim). `s-w13-pg` and the other live inputs: removed only when the train no longer needs them, with counts.


PROVENANCE:
- Seat ordinal: `Seat W 14th` 1 hit, `Seat W 15th` 0, `Seat W 16th` 0 in Secuura/Blockchain 5_Project_History/history.md (grep -F; control: the 14th count is non-zero) -> next free is `Seat W 15th` | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-11-01
- F-b head 1eb6e64f8317, driver pid 66707 detached in PUSH, R1 local 4b7cab9d0, R2a local b86dcf7f5, R2b local ecfe4f07fdce, R2b push blocked on the yaml | W 14th wrap mail 21:40Z, /private/tmp/wed_newmail/batch_20261031T214121Z.txt (read by Wednesday); pid 66707 checked by Wednesday with ps (ppid 1, tty ??) | read 2026-11-01
- Develop = 8d3d8ed7e649b760d32a2d07b068dcd018f07f52 (Wednesday's ls-remote of refs/heads/develop on the Secuura remote) | git ls-remote from /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate65-r1r3-1868/repo | read 2026-11-01
- KS-1384 state (open: In Progress, 20 comments, last comment 2026-10-31T15:51:20Z); scope: "One anchor row per (document_id, network): a repeat POST /api/anchors resets the existing ..." (title); this brief narrows to the train's remaining members F-b, R1, R2a, R2b | Linear issue read by Wednesday (GraphQL, comments first:100 sorted client-side) | read 2026-11-01
- Gate 65 and gate 68 rulings, the F-b r4b exception, D3 as written | Wednesday's ANSWER mails of 2026-11-01 to Secuura/Blockchain-W (staged copies in the Wednesday session scratchpad; verdicts at /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate65-r1r3-1868/verdict.md and /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate68-ks1384-r2a-1874/verdict.md) | read 2026-11-01
- Standing lines carried verbatim from W 14th's brief (PARTITION, HOLDS, WRAP sections) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-31_seatW14_ks1384_train_finish.md | read 2026-11-01

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-01 08:44
