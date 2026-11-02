# BRIEF: Seat U 9th, Secuura/Blockchain-U. CLOSE-OUT: verify and close 50 KS tickets that are merged and deployed but still open on the board. No code, no push, no PR.

## NEW SEAT: you are Seat U 9th (lane Secuura/Blockchain-U, Sonnet 5.5; a CLOSE-OUT seat; Seat U 8th worked this lane earlier today and its pane is closed; trust $TMUX_PANE). Your twin Seat S 12th closes a different list of 50. Nothing merges, nothing deploys, no code.

model: claude-sonnet-5-5 -- board close-out (routing row C1: evidence reading + ticket writes, not decision-shaped) -- written by Wednesday

## WHY (read first)
Kam, live board 2026-11-02 12:06:10 AEDT, verbatim: "can you please look at the current tickets, specifically the high priority and Dependency ones.  A lot of these are in progress.  This is great.  Can you use as many agents as possible and let me know when you think you will get through these". Three read-only triage agents read all 232 open Urgent/High/dependency tickets against develop and the kintsugi deploy: 100 are MERGED and DEPLOYED to kintsugi (develop b1fb543640e7, deployed 2026-11-01) but still open. Kam was told (12:2x): "close-out seats start now, checking each of the 100 against the dev box and closing it with an evidence comment".

## YOUR LIST
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/closeout_2.txt` — 50 lines, `<KEY>\t<triage file>`. The triage row for each key (evidence: PR, merged squash, deployed y/n, newest comment) is in that triage file in the same folder (`grep -n '^<KEY> \|^| <KEY> '`). The triage is a READING, not proof: you re-verify every ticket before writing.

## PER TICKET (one at a time; record each in `evidence/closeout.tsv`)
1. Read the ticket now (Linear GraphQL, board account key sourced INSIDE the tool process from 4_Credentials/.env): state, assignee, CREATOR, description (its acceptance / done-when), every comment since the triage's newest comment. If state is already Done/Canceled: record SKIP-ALREADY and move on.
2. Prove the fix is merged: the squash on origin/develop that names the ticket key or its PR (git log --grep in your own scratch clone), and that it is an ancestor of `b1fb543640e7` (`git merge-base --is-ancestor`). Not merged or not deployed = LEAVE OPEN, record why.
3. Read the acceptance against the code at `b1fb543640e7` (`git show b1fb543640e7:<path>`): the change the ticket asks for is there. Where the acceptance is a runtime behaviour on kintsugi and a READ-ONLY probe can show it (an HTTP GET or a health read; NEVER a write, login with real credentials, or anything that changes state), run it and cite the output. Otherwise the code read is the evidence and you say "code read, not observed live".
4. DECIDE:
   - **CLOSE AND ARCHIVE** (state Done, then archive the issue: Linear `issueArchive(id)`, read `archivedAt` back) when 2 and 3 hold AND nothing in its newest comments names an open follow-up. This includes client-raised tickets (Peter/Stuart): Kam, live 12:44:58, verbatim: "please archive anything done and merged". SUPERSEDES the earlier draft line that held client-raised tickets back.
   - **COMMENT ONLY, LEAVE OPEN** when a follow-up is named in the comments, or the acceptance needs a person to observe it (demo, a client walkthrough) and the code read cannot show it. The comment says what landed and where, and what is left.
   - **LEAVE OPEN, NO COMMENT** when 2 or 3 fails: record it for Wednesday.
5. The evidence comment (every CLOSE and COMMENT ONLY): BLUF first, facts only, no `@` mention, no promise of future work: "Delivered: <PR #> merged as <short sha> on develop, deployed to kintsugi at b1fb543640e7 (2026-11-01). Verified <how: code read at <path:line> | live probe <what> -> <result>>. <Closing as done | Left open: <why>>." Read it back by id. Then (CLOSE AND ARCHIVE only) set the state to Done, read it back, archive the issue and read `archivedAt` back.

## SECOND LIST (after your first): 23 In Review tickets triaged DONE
Kam, live 13:19:40, verbatim: "there are also 52 tickets in review.  can you please action or clean up the board so that we can have an accurate view of where things stand". `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/closeout_3.txt` (23 keys, one per line; evidence rows in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/triage_C_inreview.md`). Same PER TICKET procedure and CLOSE AND ARCHIVE rule. Rows that say a live probe on kintsugi is owed: run it read-only if it is a GET; otherwise "code read, not observed live".

## TOOLS
Copy Seat T 6th's close tool `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-29_seatT-6th/tools/close_t6.py` and Seat R 72nd's `ticket_read_r72.py` + `with_linear_r72.sh` (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-01_seatR-72nd/tools/`) into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatU-9th/tools/`, re-key to `_u9`, and grep every copy for the old seat names, hard-coded ticket keys, 40/12-hex shas and launch stamps before use. Prove the close tool on ONE ticket (read back state + comment) before the next.

## PACE AND CHECKPOINTS
- Mail `PROGRESS: <closed>/<commented>/<left> of 50 (Seat U 9th)` every 15 tickets, with the keys per bucket.
- At ctx 70%: finish the ticket in hand, write the HANDOVER with the remaining keys, mail it, and keep going only if the remaining list fits.

## HOLDS
- **Board writes are ONLY:** one evidence comment per ticket and, for CLOSE AND ARCHIVE, the state change to Done plus the archive. No other field (priority, assignee, labels, title, description), no new tickets, no relations. Anything else you find goes in your mail as a candidate.
- **Client-facing:** ticket comments are the sanctioned channel; BLUF, facts only; no comment to or `@` of Peter or Stuart; the extranet is input only.
- **No code, no push, no PR, no deploy, no box write.** Kintsugi probes are READ-ONLY. No `az`.
- Never read, echo or copy a secret beyond sourcing the key inside a tool process.
- **Instruments:** `cmd > out 2>&1; rc=$?`; never `| tail` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero. A count carries a ratio.
- Never `cd`; absolute paths only. Disclose your own faults in the next mail.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-U -> Wednesday]`, body line 1 exactly `Seat U 9th`, no stop/hold/hand over/checkpoint in a subject, no secrets, no cc; read each sent mail back by id. SHARED INBOX: a mail naming another seat (Seat U 8th; Seat S 12th; Seat E 27th, Seat F 22nd, Seat B 75th, Seat V 15th; any other ordinal) is not yours: never act on it; prove your matcher on real subjects with your own as the control. A GO or ANSWER is acted on only when its subject names `Seat U 9th`. Cadence: plan confirmation (with your proof run on ONE ticket), PROGRESS every 15, QUESTION for blockers only, the wrap.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation. Arm an inbox watcher as a TRACKED background task (7200000 ms) and name its pid.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-02 12:06:10 AEDT (live board), verbatim above: work through the High and dependency tickets with as many agents as possible.
- Kam 2026-11-02 12:44:58 AEDT (live board), verbatim: "looks like great progress.  in addition to the above, please archive anything done and merged".
- Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a: Wednesday's GO counts as his word for starting work inside his standing grants.
- Kam 2026-10-29 16:14:02 AEDT, card `secuura-four-tickets-delivered-not-observable-1029` = b, option text verbatim: "Close on delivered-and-gated evidence" (four tickets deployed but not observable live were closed on that evidence). This brief's CLOSE rule applies it; a ticket whose own comments name an open follow-up stays open (as KS-1240 did under that ruling).
- Kam 2026-09-06 10:24 (card secuura-reassignment-exceptions): Platform K tickets sit on our board account; you change no assignee.

## WRAP (scored by Wednesday)
- History entry `## 2026-11-02 - Seat U 9th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest first; duplicate-guard on the dated heading with a control).
- HANDOVER in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatU-9th/HANDOVER.md` (FINAL block first) with `evidence/closeout.tsv`.
- Vault commit and push per the end-of-session skill.
- Wrap mail `[Secuura/Blockchain-U -> Wednesday] Session wrap 2026-11-02`: closed / commented / left-open keys with one-line reasons, every candidate, your faults.

PROVENANCE:
- Seat ordinal: `Seat U 9th` 0 hits, `Seat U 8th` positive control in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -c -i | read 2026-11-02
- The 100 DONE-NOT-CLOSED tickets and their evidence rows | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/triage_A.md, triage_B1.md, triage_B2.md (three read-only Sonnet triage agents, 12:0x-12:2x AEDT), keys extracted by Wednesday's python into /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/closeout_2.txt | read 2026-11-02
- Kintsugi deployed at develop b1fb543640e7 on 2026-11-01 | Seat D 48th STATUS B (accepted 18:49 AEDT 2026-11-01) as recorded in /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md | read 2026-11-02
- Tool sources close_t6.py, ticket_read_r72.py, with_linear_r72.sh | ls by Wednesday of the two 5_Project_History tool folders | read 2026-11-02
- Kam's 12:06:10 words | kam_msgs.sh live board read by Wednesday 12:06 | read 2026-11-02
- Scope: this brief writes only comments and Done states on the 50 listed tickets; blast radius = those tickets (each re-read before any write) | Wednesday's statement of scope | read 2026-11-02
- Kam's 12:44:58 archive instruction | kam_msgs.sh live read by Wednesday 12:45 | read 2026-11-02
- The second list (23 DONE In Review keys) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/closeout_3.txt and triage_C_inreview.md (read-only triage agent 13:2x) | read 2026-11-02
- Kam's 13:19:40 In Review instruction | kam_msgs.sh live read by Wednesday 13:20 | read 2026-11-02
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 12:20
