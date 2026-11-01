# BRIEF: Seat B 73rd, Secuura/Blockchain-B. MERGE gated PRs one at a time on Wednesday's head-pinned GOs: first PR 1900 (KS-1868 kyc x5, TIER 1), then each queue item Wednesday sends

## NEW SEAT: you are Seat B 73rd (lane Secuura/Blockchain-B; Sonnet 5.5; trust $TMUX_PANE). You are a MERGE seat. The previous merge seat, Seat B 72nd, merged six PRs tonight (1894, 1895, 1896, 1899, 1897, 1898) with this procedure and wrapped at 14:14Z; its tools are in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-72nd/tools/` (merge_b72.py, run_merge_b72.sh, mergeable_poll_b72.py, item1_b72.sh, the per-PR ticket-key case): copy into your own folder and re-key to `_b73`. Read its HANDOVER first. **Paths in this brief:** P = `/Volumes/DevMASTER/!CODING/Secuura/Blockchain`. Never `cd`; use absolute paths only.

## BLUF
- **PR 1900** (KS-1868, "Refs", services/kyc/src/index.ts five catch sites + five new tests, **TIER 1**), author Seat F 20th. Head `a06c3441c2371a6f33bb75855e9953d55990de87`, one commit on develop `8126b22bd5aa505be194996c9301b6e1ced5583e`. develop NOW `8afcf256ed5fb38d05f7273e08e1b912446bac5c` (Wednesday's ls-remote 01:4x AEDT 2026-11-02). Gate 85 (Opus, tier 1) = GO WITH NOTES at this head (verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/verdict.md`); merge-tree clean on a1350ccb and 8afcf256 per the gate. F 20th is PATCHing the gate 85 notes (G85-F1..F7) into the body now: check for that section in ITEM 2; if absent at your READY, say so and do not merge. Ticket comment on KS-1868 naming PR 1900: 72b61792.
- Your job: re-pin, prove the PR merges cleanly onto the develop it will land on, confirm the notes, READY TO MERGE, then merge ONLY on its own GO. Then each further queue item Wednesday mails (expected: PRs 1901 and 1902 after gate 86; E 25th's and V 12th's PRs after their gates), one at a time. No code changes. Nothing deploys.
- **Known from B 70th-72nd:** GitHub's `mergeable` reads UNKNOWN briefly after develop moves; poll gh's GraphQL `mergeable` to non-null in the same action as the dry run. `mergeable_state` reads "unstable" and the check runs answer 403 to the project PAT: name that limit in every MERGED mail. Paths under `systemTest/` are at the REPO ROOT.

## QUEUE
### ITEM 0. Plan confirmation
QUESTION mail, topic `plan confirmation`, subject `[Secuura/Blockchain-B -> Wednesday] QUESTION: plan confirmation (Seat B 73rd)`, body line 1 `Seat B 73rd`. Carry any launcher warning VERBATIM. Then start ITEMS 1-2 (read-only) without waiting.
### ITEM 1. Re-verify against the CURRENT develop
Re-pin the head and develop by `ls-remote` (a differing head = STOP and mail: delta gate, not a merge). In a scratch clone at a path asserted absent, `git merge-tree --write-tree` of the head onto develop: rc and tree. Paths shared with everything merged since the PR's base (planted control). PR API file list vs gate 85's.
### ITEM 2. Gate notes present (READ only). You make NO body edit.
### ITEM 3. READY TO MERGE, then merge ONE PR per GO
READY TO MERGE names: head (ls-remote in the same action), merge tree on today's develop, shared-path result, file-list comparison, the ticket comment, the Test Evidence block, NOT covered. Wait for ONE GO whose subject ends `(Seat B 73rd)` naming the PR, head and develop pin. On the GO: re-pin, merge-tree on the pin in the same action, squash via the merge API with `sha=<head>` (B 72nd's recipe, `--dry` then `--real`), post-merge reads (squash tree = merge tree on the pin; develop moved to it), MERGED mail. Develop not the pin = no merge, mail. **No push from this seat** (the merge API is not `git push`, so `.githooks/pre-push` is not in its path).
### ITEM 4. Wrap when the queue is empty and Wednesday says so, or at ~75% context.

## PARTITION
- Seats share one inbox (`secuura-blockchain@`): every mail names `Seat B 73rd` on body line 1, row tag `[Secuura/Blockchain-B -> Wednesday]`. A GO naming Seat B 72nd is not yours.
- **Yours:** the merges Wednesday GOs. Every worktree of every other seat is read-only. Copy anything you need into `P/5_Project_History/2026-11-02_seatB-73rd/` first.

## RULED BY KAM, NOT YET IN AN ARTEFACT
(none that bind a merge seat. Kam 2026-11-01 21:27/21:32, verbatim: "please spin up as many agent agents as possible and use the spark as much as you can to work through tickets" / "yes . override the limit and continue to 100%" — the authority for launching past the usage band; it changes no hold.)

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- GO subjects end `(Seat <L> <N>th)`. Before ANY merge: re-pin and merge-tree on the pin in the same action. One GO = one PR.
- Kam, 2026-10-30 (card, Wednesday's GO counts as his word for STARTING work inside his standing grants): start ITEMS 0-2 on this brief; each merge needs its own GO.
- .env: your tools may source 4_Credentials/.env INSIDE the tool process to authenticate (GH_TOKEN etc.); never print, copy or log a value (SUPERSEDES "never open a .env" below for that case only). No cc. F-02: no keychain seeding, no SECUURA_ALLOW_ONDISK_KEY.

## HOLDS (the standing lines, from `STANDING_LINES.md`)
- **Signature classes pause for Kam, always:** production, money, external communication to any human, anything irreversible.
  - No `az`, no deploy, no `--admin`, no `--no-verify`, no force push.
  - Never read, echo or copy a secret, and never open a `.env`. A gate that stops you is a question it is asking.
- **Kam, 2026-09-11 16:56, verbatim:** "For the time being, I / you will approve our own elements" and "FIx and merge all tickets after they are tested". We merge our own TESTED K work after the QA gate, on Wednesday's head-pinned GO. Deploying is NOT yours.
- **Client-facing communication is TICKET COMMENTS only,** BLUF-first, facts only. **No comment to, and no `@` mention of, Peter or Stuart.** This seat posts no ticket comment.
- **Filing:** you file NOTHING without Wednesday's word; candidates go in your mail. You change no ticket's state. KS-1868 stays open (these PRs say "Refs").
- **READY TO MERGE means five things EXIST and are named by identifier:** the PR number; its head sha read from origin in the same action; the ticket comment naming the PR; the Test Evidence block in the PR body; what was NOT done or NOT covered.
- **Forward-move rule (every Secuura build or raise brief carries this line):** a forward move of develop is ACCEPTED when your base is an ancestor of the new develop (read by `ls-remote`), its objects are present, and the ONLY paths shared between the moved range and your branch are the docs. Then merge the new develop in (never rebase a pushed branch), rebuild the docs entries, re-run `html_docs_check` with a planted defect, and push. Any shared CODE path means stop and mail. **For this merge seat:** you push nothing, so any forward move that would need a push is a STOP-and-mail.
- **Boot pull:** the launcher's step-1 pull may fast-forward the shared develop refs; RECORD it. After boot: no fetch or pull in the shared checkout, and no write to either develop ref.
- **Kill only your own PIDs** (by recorded PID, never `pkill`/`killall` by name). Never plant a control directory in the SHARED `worktrees/` directory.
- **Clone into a NON-EXISTENT path:** any scratch clone is made with `git clone` into a path asserted absent first. Read origin with `ls-remote`, never `origin/develop`.
- **Mail discipline:**
  - Every mail names `Seat B 73rd` on body line 1 and goes only to `wednesday-agent@agentmail.to` (no cc, no secrets). A QUESTION mail is for a blocker only (Context, one Question, Meanwhile, Needed-by).
  - After ~15 minutes with no ANSWER, proceed on the safest reading UNLESS approval-class. A merge is never proceeded on without the GO.
  - Arm every inbox watcher at the maximum background timeout (7200000 ms), keyed on `Seat B 73rd`.
- **Instruments:**
  - Redirect to a file and read the file (`cmd > out 2>&1; rc=$?`), exit codes on their own line.
  - The Bash tool is zsh (an unquoted `====` word expands). Use `/usr/bin/grep -i` with a positive control beside every zero.
  - A pass line carries a RATIO. A skip is not a pass. Never `cd`; the no-cd hook refuses it.
- **Git:** to ask what a branch changed, use three dots or the merge-base, never `X..HEAD`.
- Never delete (quarantine into a dated folder, record it). Never end a turn on a "next up" line with nothing running.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation.

## WRAP (scored by Wednesday)
At the wrap (both MERGED and mailed, or parked behind a named blocker, or when told):
- A history entry in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` headed `## 2026-11-02 - Seat B 73rd` (newest first; duplicate-guard on the dated heading, with a control).
- A HANDOVER in `.../5_Project_History/2026-11-02_seatB-73rd/HANDOVER.md` with a WRAPPED block at the top.
- The vault commit and push per the end-of-session skill.
- The wrap mail `[Secuura/Blockchain-B -> Wednesday] Session wrap 2026-11-02`, with each PR, head, squash, tree, the GOs used, what you could not run, and your faults.
- Nothing of yours left running (a `ps` reading by PID in the same action as the claim).

PROVENANCE:
- Seat ordinal: `Seat B 73rd` 0 hits, `Seat B 72nd` 4 hits (control) in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md (/usr/bin/grep -c -i by Wednesday) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | read 2026-11-02
- PR 1900 head a06c3441 and develop 8afcf256 | git ls-remote git@github.com:Secuura/Distributed_Secuura.git by Wednesday at 01:4x AEDT | read 2026-11-02
- Gate 85 = GO WITH NOTES (G85-F1..F7), tier 1 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/verdict.md | read 2026-11-02
- KS-1868 state (open: In Progress, Low, our board account; umbrella, 'Refs' only; scope: this brief narrows to merging PR 1900, the ticket stays open; blast radius: merge seat, no product edit) | Linear ticket KS-1868 read by Seat F 20th at ITEM 0 (its plan confirmation 13:08Z) and its READY 14:02Z naming comment 72b61792 | read 2026-11-02
- B 72nd's tools and six merges | ls of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatB-72nd/tools/ (B 72nd wrap 14:14Z) and its six MERGED mails | read 2026-11-02
- Merge row C5 = Sonnet first | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md | read 2026-11-01
- HOLDS and WRAP carried from B 72nd's executed brief, re-keyed and grepped for B 72nd's state | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_seatB72_ks1868_merge_1894_1895.md | read 2026-11-02

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 01:42
