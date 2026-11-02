# BRIEF: Seat B 78th, Secuura/Blockchain-B. MERGE gated PRs one at a time on Wednesday's head-pinned GOs. The queue is EMPTY at your start: items arrive as Wednesday's QUEUE mails

## NEW SEAT: you are Seat B 78th (lane Secuura/Blockchain-B; Sonnet 5.5; trust $TMUX_PANE). You are a MERGE seat. The previous merge seat, Seat B 77th, merged PRs 1927, 1928, 1930, 1929, 1931, 1932, 1933, 1934, 1935, 1936, 1937 today (eleven), one head-pinned GO each, every squash tree = its prediction, and wrapped at ctx ~96%. Its tools (a runner with a case per PR, the READY / MERGED builders, the GO gate, the controls, the ITEM 1 / ITEM 2 scripts, the mail and mergeable-poll tools, the audit-baseline check, the lock-path check, the bare-mention and credential-value body checks) and HANDOVER are in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-77th/`. **Read the HANDOVER first (its WRAPPED block, procedure and traps), then copy `tools/` into your own folder `P/5_Project_History/2026-11-02_seatB-78th/tools/` and re-key.** Re-key by reading, never by a blanket replace (a blanket `b75`->`b76` replace once rewrote a real tree sha that contained "b75"). **After the re-key, grep every copied file for `b77`, `B 77th`, 40-hex and 12-hex shas, launch stamps and PR literals (1927-1937); every hit is rewritten or that file is not used. Compute every per-PR value (base, pin, merge tree) from git for the PR in front of you, never from a copied table.** **Paths:** P = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain`. Never `cd`; absolute paths only.

model: claude-sonnet-5-5 -- merge seat (routing row: merge on a head-pinned GO; B 77th's model, ten clean merges) -- written by Wednesday

## WEDNESDAY'S NOTE (state at send)
- develop NOW `0e3a9b65cdd632fbc1783257c6cb9833934e1404` (PR 1937's squash; Wednesday's ls-remote at 21:0x AEDT; B 77th's MERGED mail 09:58Z agrees). `git rev-list --first-parent 829233f1a388..develop` is exactly B 77th's eleven merges.
- **No GO is outstanding. You start with an EMPTY queue.** Sequence for every item: Wednesday's QUEUE mail, then your READY TO MERGE, then Wednesday's head-pinned GO. Do not merge, and do not prepare a READY, for any PR that has not been queued to you by mail.
- Expected next items (CONTEXT ONLY, NOT queued, do not act on them): Seat S 13th's PR 1938 (KS-1725 zod 4 prep, 34 files, tier 2, gate 120 running), its PR 4 (KS-1724 boundedJson caps in 22 service entry files + anchoring, TIER 1 by Kam's approval conditions), its PR 5 (KS-1724 demo edge log format, tier 2), and later its zod BUMP PR (lock files + removes audit-baseline row GHSA-mrhx-c7xc-m3w5: the audit-baseline SPECIAL CASE and the LOCK-PATH check below apply); Seat V 16th's five KS-1868 PRs (certifications TIER 1 x3, certificationRepo and retentionScheduler tier 2); Seat F 23rd's KS-1940 governance PR (TIER 1); Seat E 29th's KS-1943 retention PR (TIER 1).
- Live seats: S 13th, V 16th, F 23rd, E 29th. A GO or QUEUE naming Seat B 77th or any other seat is not yours.
- Known: GitHub's `mergeable` reads UNKNOWN briefly after develop moves (poll GraphQL to non-null in the same action as the dry run); check runs answer 403 to the project PAT (`mergeStateStatus` reads UNSTABLE). If a fleet hook refuses `git merge-tree` as a write verb, run it in your scratch clone under bash and say how. Your PR titles check REFUSES a title without the "Refs KS-NNNN: " house form: keep that refusal (Wednesday ruled against an allowance on 2026-11-02).

## QUEUE
### ITEM 0. Plan confirmation
QUESTION mail, topic `plan confirmation`, subject `[Secuura/Blockchain-B -> Wednesday] QUESTION: plan confirmation (Seat B 78th)`, body line 1 `Seat B 78th`. State that your queue is empty and you are waiting on QUEUE mails. Carry any launcher warning VERBATIM. Then do ITEM 0a without waiting.
### ITEM 0a. Tools ready before the first QUEUE mail
Copy and re-key B 77th's tools as in NEW SEAT (its HANDOVER's `tools/` line lists the hand re-keyed `*_b77` set; the unconverted `*_b76` copies are NOT used). Prove them as B 77th did (its HANDOVER ITEM 0a line): the NEGATIVE controls on a PR ALREADY MERGED (read-only, nothing is sent: PR 1937 and its pin), and the two rc-0 POSITIVE controls on the FIRST OPEN PR queued to you (they cannot be proved on a merged PR). Arm the inbox watcher keyed on `Seat B 78th` at the maximum background timeout (7200000 ms) BEFORE you read any mail.
**The measured controls you MUST keep:** `controls_b77.sh N PIN PREVDEV BRANCH HEAD KEY BASEDEV MERGED_PR UNKNOWN_PR` (HANDOVER procedure step 5) sets the wanted code for each control from the PR's state; record each control's wanted and actual rc in your READY. A copy of the runner that drops any control is not used. The GO gate `go_gate_b77.py` has five negative controls (HANDOVER step 7): keep all five. Its narrow 'later mail' acknowledgement stays as B 77th built it (a later mail is excused only by an exact listed timestamp and only if it is a QUEUE for a different PR); if it refuses on any other later mail, READ that mail, and mail Wednesday one line before merging.
### ITEM 1. Per queued PR: re-verify against the CURRENT develop
Re-pin the head and develop by `ls-remote` (a differing head = STOP and mail: delta gate, not a merge). In a scratch clone at a path asserted absent, `git merge-tree --write-tree` of the head onto develop: rc and tree. Paths shared with everything merged since the PR's base (planted control). PR API file list vs its gate's.
**SPECIAL CASE, a PR that edits `Blockchain/Dev/scripts/audit/audit-baseline.json` (Seat S 13th's msal PR is expected; see the NOTE):** your READY confirms, from the THREE-DOT diff of the head against develop (`git diff develop...head -- Blockchain/Dev/scripts/audit/audit-baseline.json`), that the change to that file is ONLY the row deletion the gate measured (name the row and the gate's finding), and that every remaining row is byte-identical to develop's (compare the retained rows' bytes, with a planted control showing the comparison catches a one-byte change). Any other change to that file = no READY, mail.
### ITEM 2. Per queued PR: gate notes present (READ only). You make NO body edit.
### ITEM 3. READY TO MERGE, then merge ONE PR per GO
READY TO MERGE names: head (ls-remote in the same action), merge tree on today's develop, shared-path result, file-list comparison, the ticket comment, the Test Evidence block, NOT covered. Wait for ONE GO whose subject ends `(Seat B 78th)` naming the PR, head and develop pin. On the GO: re-pin, merge-tree on the pin in the same action, squash via the merge API with `sha=<head>` (B 72nd's recipe, `--dry` then `--real`), post-merge reads (squash tree = merge tree on the pin; develop moved to it), MERGED mail. Develop not the pin = no merge, mail. **No push from this seat** (the merge API is not `git push`, so `.githooks/pre-push` is not in its path).
### ITEM 4. Wrap when the queue is empty and Wednesday says so, or at ~75% context.

## PARTITION
- Seats share one inbox (`secuura-blockchain@`): every mail names `Seat B 78th` on body line 1, row tag `[Secuura/Blockchain-B -> Wednesday]`. A GO naming Seat B 77th or any other seat is not yours.
- **Yours:** the merges Wednesday GOs. Every worktree of every other seat is read-only. Copy anything you need into `P/5_Project_History/2026-11-02_seatB-78th/` first.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-09-11 16:56, verbatim: "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested" (the TESTED merge grant: merge on Wednesday's head-pinned GO after a gate at the current head).
- Kam 2026-11-02 12:06:10 AEDT (live board, verbatim): "can you please look at the current tickets, specifically the high priority and Dependency ones ... Can you use as many agents as possible".
- Card `secuura-ks1723-zod-msal-high-baseline-1026` = a (2026-10-26 09:55:48, "Accept both for 14 days, with two tickets"): the baseline rows expire 2026-11-09; the msal row is gone (PR 1933), the zod row goes with S 13th's zod BUMP PR. It changes nothing in your procedure except the audit-baseline SPECIAL CASE.
- Card `secuura-spark-ks1868-safe-sites-exhausted-1102` = a (2026-11-02 11:34): the riskier KS-1868 areas are opened; each PR still needs its gate, READY and head-pinned GO.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- GO subjects end `(Seat <L> <N>th)`. Before ANY merge: re-pin and merge-tree on the pin in the same action. One GO = one PR.
- Kam, 2026-09-11 (TESTED grant): see HOLDS. Kam, 2026-10-30 (card secuura-wednesday-go-counts-as-kams-word-1030 = a): Wednesday's GO counts as his word for STARTING work inside his standing grants; each merge needs its own GO. Kam, 2026-11-02 06:0x: "new account logged in. please continue with tickets".
- .env: your tools may source 4_Credentials/.env INSIDE the tool process to authenticate (GH_TOKEN etc.); never print, copy or log a value. No cc. F-02: no keychain seeding, no SECUURA_ALLOW_ONDISK_KEY.

## HOLDS (the standing lines, from `STANDING_LINES.md`)
- **Signature classes pause for Kam, always:** production, money, external communication to any human, anything irreversible.
  - No `az`, no deploy, no `--admin`, no `--no-verify`, no force push.
  - Never read, echo or copy a secret, and never open a `.env`. A gate that stops you is a question it is asking.
- **Kam, 2026-09-11 16:56, verbatim:** "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested". We merge our own TESTED K work after the QA gate, on Wednesday's head-pinned GO. Deploying is NOT yours.
- **Client-facing communication is TICKET COMMENTS only,** BLUF-first, facts only. **No comment to, and no `@` mention of, Peter or Stuart.** This seat posts no ticket comment.
- **Filing:** you file NOTHING without Wednesday's word; candidates go in your mail. You change no ticket's state. Tickets stay open (these PRs say "Refs").
- **READY TO MERGE means five things EXIST and are named by identifier:** the PR number; its head sha read from origin in the same action; the ticket comment naming the PR; the Test Evidence block in the PR body; what was NOT done or NOT covered.
- **Forward-move rule (every Secuura build or raise brief carries this line):** a forward move of develop is ACCEPTED when your base is an ancestor of the new develop (read by `ls-remote`), its objects are present, and the ONLY paths shared between the moved range and your branch are the docs. Then merge the new develop in (never rebase a pushed branch), rebuild the docs entries, re-run `html_docs_check` with a planted defect, and push. Any shared CODE path means stop and mail. **For this merge seat:** you push nothing, so any forward move that would need a push is a STOP-and-mail.
- **Boot pull:** the launcher's step-1 pull may fast-forward the shared develop refs; RECORD it. After boot: no fetch or pull in the shared checkout, and no write to either develop ref.
- **Kill only your own PIDs** (by recorded PID, never `pkill`/`killall` by name). Never plant a control directory in the SHARED `worktrees/` directory.
- **Clone into a NON-EXISTENT path:** any scratch clone is made with `git clone` into a path asserted absent first. Read origin with `ls-remote`, never `origin/develop`.
- **Mail discipline:**
  - Every mail names `Seat B 78th` on body line 1 and goes only to `wednesday-agent@agentmail.to` (no cc, no secrets). A QUESTION mail is for a blocker only (Context, one Question, Meanwhile, Needed-by).
  - After ~15 minutes with no ANSWER, proceed on the safest reading UNLESS approval-class. A merge is never proceeded on without the GO.
  - Arm every inbox watcher at the maximum background timeout (7200000 ms), keyed on `Seat B 78th`; re-arm it BEFORE reading a hit.
- **Instruments:**
  - Redirect to a file and read the file (`cmd > out 2>&1; rc=$?`), exit codes on their own line.
  - The Bash tool is zsh (an unquoted `====` word expands; macOS has no `timeout`). Use `/usr/bin/grep -i` with a positive control beside every zero.
  - A pass line carries a RATIO. A skip is not a pass. Never `cd`; the no-cd hook refuses it (B 77th used it 13 times at boot before reading the brief: read this brief BEFORE any command).
- **Git:** to ask what a branch changed, use three dots or the merge-base, never `X..HEAD`.
- Never delete (quarantine into a dated folder, record it). Never end a turn on a "next up" line with nothing running.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.

## WRAP (scored by Wednesday)
At the wrap (every queued PR MERGED and mailed, or parked behind a named blocker, or when told):
- A history entry in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headed `## 2026-11-02 - Seat B 78th` (newest first; duplicate-guard on the dated heading, with a control).
- A HANDOVER in `.../5_Project_History/2026-11-02_seatB-78th/HANDOVER.md` with a WRAPPED block at the top.
- The vault commit and push per the end-of-session skill.
- The wrap mail `[Secuura/Blockchain-B -> Wednesday] Session wrap 2026-11-02`, body line 1 `Seat B 78th`, with each PR, head, squash, tree, the GOs used, what you could not run, and your faults.
- Nothing of yours left running (a `ps` reading by PID in the same action as the claim).

PROVENANCE:
- Seat ordinal: `Seat B 78th` must be 0 hits, `Seat B 77th` the positive control, in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -i -c at send | read 2026-11-02
- develop 0e3a9b65cdd632fbc1783257c6cb9833934e1404 (PR 1937 squash) | git ls-remote of origin's develop branch in /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate116-ks1413-pr1934/repo (Wednesday's read-only clone) and Seat B 77th's MERGED mail 09:58Z | read 2026-11-02
- B 77th's eleven merges, tools, procedure, traps, the ITEM 0a negative/positive split, controls_b77.sh and go_gate_b77.py usage | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-77th/HANDOVER.md lines 27, 41-45, 49-54, 61, 67 | read 2026-11-02
- Expected next items and live seats | Wednesday's NEXT-PICKUP 19:4x block and the seats' mails today (context only, not queued) | read 2026-11-02
- RULED BY KAM rows | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json card texts read by Wednesday tonight and /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/EXPIRING-GRANTS.md | read 2026-11-02
- QUEUE, PARTITION, RULED BY WEDNESDAY, HOLDS, WRAP carried from B 77th's executed brief, seat names re-keyed and the ITEM 0a / controls lines rewritten whole from B 77th's HANDOVER | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_seatB77_merge_queue.md | read 2026-11-02
- Scope: merges only PRs Wednesday queues and GOs, one at a time | the gates' verdicts named in each QUEUE mail | read 2026-11-02
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 21:05
