# BRIEF: Seat S 12th, Secuura/Blockchain-S. CLOSE-OUT: verify and close 50 KS tickets that are merged and deployed but still open on the board. No code, no push, no PR.

## NEW SEAT: you are Seat S 12th (lane Secuura/Blockchain-S, Sonnet 5.5; a CLOSE-OUT seat; Seat S 11th worked this lane earlier today and its pane is closed; trust $TMUX_PANE). Your twin Seat U 9th closes a different list of 50. Nothing merges, nothing deploys, no code.

model: claude-sonnet-5-5 -- board close-out (routing row C1: evidence reading + ticket writes, not decision-shaped) -- written by Wednesday

## WHY (read first)
Kam, live board 2026-11-02 12:06:10 AEDT, verbatim: "can you please look at the current tickets, specifically the high priority and Dependency ones.  A lot of these are in progress.  This is great.  Can you use as many agents as possible and let me know when you think you will get through these". Three read-only triage agents read all 232 open Urgent/High/dependency tickets against develop and the kintsugi deploy: 100 are MERGED and DEPLOYED to kintsugi (develop b1fb543640e7, deployed 2026-11-01) but still open. Kam was told (12:2x): "close-out seats start now, checking each of the 100 against the dev box and closing it with an evidence comment".

## RULED BOARD ACTIONS (Kam's card rulings 2026-11-02 12:42-12:44 AEDT; do these FIRST, before your list)
Each: read the ticket, post one facts-only comment quoting the ruling verbatim (card id + option text), then the action, read back.
- KS-889: card secuura-ks889-platform-s-key-remint-1102 = b, "Accept: no re-mint; decide the KS-843 flip on other evidence or keep logged grace". Comment the ruling; CLOSE AND ARCHIVE KS-889 (the decision is made). Add a one-line comment on KS-843: "No re-mint (KS-889 ruled b): the flip waits for other evidence; logged grace continues." Do NOT change KS-843's state.
- KS-601: card secuura-ks601-kintsugi-split-close-1102 = a, "Confirm split restored, close KS-601; leftovers stay on KS-1044/KS-1100 (board-only)". Comment; CLOSE AND ARCHIVE.
- KS-229: card secuura-ks229-assurance-tracker-close-1102 = b, "Close the tracker; children stay as standalone backlog tickets (board-only)". Comment; CLOSE AND ARCHIVE KS-229 only; children untouched.
- KS-1336: card secuura-ks1336-per-tenant-db-priority-1102 = a, "Downgrade to Medium and keep parked until per-tenant DBs are planned (board-only)". Comment; set PRIORITY to Medium (the only priority change this brief allows); state unchanged.
- KS-762: card secuura-ks762-db-password-rotation-confirm-1102 = c, "Tell me the rotation status later; keep defaults unchanged". Comment the ruling only; no state change.

- WRONG-STATE (Kam live 13:19:40, verbatim: "there are also 52 tickets in review.  can you please action or clean up the board so that we can have an accurate view of where things stand"): five In Review tickets have nothing under review. For each, read the triage row in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/triage_C_inreview.md`, re-read the ticket, post one facts-only comment saying what is done and what is left, then move the STATE to the target the row names (In Progress, Todo or Backlog; no other field): KS-1694, KS-1490, KS-1000, KS-969, KS-663. (KS-229 is closed by its ruling above, not moved.)

## YOUR LIST
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/closeout_1.txt` — 50 lines, `<KEY>\t<triage file>`. The triage row for each key (evidence: PR, merged squash, deployed y/n, newest comment) is in that triage file in the same folder (`grep -n '^<KEY> \|^| <KEY> '`). The triage is a READING, not proof: you re-verify every ticket before writing.

## PER TICKET (one at a time; record each in `evidence/closeout.tsv`)
1. Read the ticket now (Linear GraphQL, board account key sourced INSIDE the tool process from 4_Credentials/.env): state, assignee, CREATOR, description (its acceptance / done-when), every comment since the triage's newest comment. If state is already Done/Canceled: record SKIP-ALREADY and move on.
2. Prove the fix is merged: the squash on origin/develop that names the ticket key or its PR (git log --grep in your own scratch clone), and that it is an ancestor of `b1fb543640e7` (`git merge-base --is-ancestor`). Not merged or not deployed = LEAVE OPEN, record why.
3. Read the acceptance against the code at `b1fb543640e7` (`git show b1fb543640e7:<path>`): the change the ticket asks for is there. Where the acceptance is a runtime behaviour on kintsugi and a READ-ONLY probe can show it (an HTTP GET or a health read; NEVER a write, login with real credentials, or anything that changes state), run it and cite the output. Otherwise the code read is the evidence and you say "code read, not observed live".
4. DECIDE:
   - **CLOSE AND ARCHIVE** (state Done, then archive the issue: Linear `issueArchive(id)`, read `archivedAt` back) when 2 and 3 hold AND nothing in its newest comments names an open follow-up. This includes client-raised tickets (Peter/Stuart): Kam, live 12:44:58, verbatim: "please archive anything done and merged". SUPERSEDES the earlier draft line that held client-raised tickets back.
   - **COMMENT ONLY, LEAVE OPEN** when a follow-up is named in the comments, or the acceptance needs a person to observe it (demo, a client walkthrough) and the code read cannot show it. The comment says what landed and where, and what is left.
   - **LEAVE OPEN, NO COMMENT** when 2 or 3 fails: record it for Wednesday.
5. The evidence comment (every CLOSE and COMMENT ONLY): BLUF first, facts only, no `@` mention, no promise of future work: "Delivered: <PR #> merged as <short sha> on develop, deployed to kintsugi at b1fb543640e7 (2026-11-01). Verified <how: code read at <path:line> | live probe <what> -> <result>>. <Closing as done | Left open: <why>>." Read it back by id. Then (CLOSE AND ARCHIVE only) set the state to Done, read it back, archive the issue and read `archivedAt` back.

## TOOLS
Copy Seat T 6th's close tool `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-29_seatT-6th/tools/close_t6.py` and Seat R 72nd's `ticket_read_r72.py` + `with_linear_r72.sh` (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-01_seatR-72nd/tools/`) into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatS-12th/tools/`, re-key to `_s12`, and grep every copy for the old seat names, hard-coded ticket keys, 40/12-hex shas and launch stamps before use. Prove the close tool on ONE ticket (read back state + comment) before the next.

## PACE AND CHECKPOINTS
- Mail `PROGRESS: <closed>/<commented>/<left> of 50 (Seat S 12th)` every 15 tickets, with the keys per bucket.
- At ctx 70%: finish the ticket in hand, write the HANDOVER with the remaining keys, mail it, and keep going only if the remaining list fits.

## HOLDS
- **Board writes are ONLY:** one evidence comment per ticket and, for CLOSE AND ARCHIVE, the state change to Done plus the archive (plus the RULED BOARD ACTIONS section below, including the five WRONG-STATE moves). No other field (priority, assignee, labels, title, description), no new tickets, no relations. Anything else you find goes in your mail as a candidate.
- **Client-facing:** ticket comments are the sanctioned channel; BLUF, facts only; no comment to or `@` of Peter or Stuart; the extranet is input only.
- **No code, no push, no PR, no deploy, no box write.** Kintsugi probes are READ-ONLY. No `az`.
- Never read, echo or copy a secret beyond sourcing the key inside a tool process.
- **Instruments:** `cmd > out 2>&1; rc=$?`; never `| tail` on the stream you diagnose from; macOS has NO `timeout`; zsh has no PIPESTATUS; never `echo =====`; `/usr/bin/grep -i` with a positive control beside every zero. A count carries a ratio.
- Never `cd`; absolute paths only. Disclose your own faults in the next mail.
- **Mail:** from secuura-blockchain@ to `wednesday-agent@agentmail.to` ONLY, subject prefix `[Secuura/Blockchain-S -> Wednesday]`, body line 1 exactly `Seat S 12th`, no stop/hold/hand over/checkpoint in a subject, no secrets, no cc; read each sent mail back by id. SHARED INBOX: a mail naming another seat (Seat S 11th; Seat U 9th; Seat E 27th, Seat F 22nd, Seat B 75th, Seat V 15th; any other ordinal) is not yours: never act on it; prove your matcher on real subjects with your own as the control. A GO or ANSWER is acted on only when its subject names `Seat S 12th`. Cadence: plan confirmation (with your proof run on ONE ticket), PROGRESS every 15, QUESTION for blockers only, the wrap.
- **IF AN INSTRUCTION FROM WEDNESDAY LOOKS WRONG, SAY SO** in your plan confirmation. Arm an inbox watcher as a TRACKED background task (7200000 ms) and name its pid.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-02 12:06:10 AEDT (live board), verbatim above: work through the High and dependency tickets with as many agents as possible.
- Kam 2026-11-02 12:44:58 AEDT (live board), verbatim: "looks like great progress.  in addition to the above, please archive anything done and merged".
- Kam 2026-10-30 10:07:32 AEDT, card `secuura-wednesday-go-counts-as-kams-word-1030` = a: Wednesday's GO counts as his word for starting work inside his standing grants.
- Kam 2026-10-29 16:14:02 AEDT, card `secuura-four-tickets-delivered-not-observable-1029` = b, option text verbatim: "Close on delivered-and-gated evidence" (four tickets deployed but not observable live were closed on that evidence). This brief's CLOSE rule applies it; a ticket whose own comments name an open follow-up stays open (as KS-1240 did under that ruling).
- Kam 2026-09-06 10:24 (card secuura-reassignment-exceptions): Platform K tickets sit on our board account; you change no assignee.

## WRAP (scored by Wednesday)
- History entry `## 2026-11-02 - Seat S 12th` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest first; duplicate-guard on the dated heading with a control).
- HANDOVER in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-02_seatS-12th/HANDOVER.md` (FINAL block first) with `evidence/closeout.tsv`.
- Vault commit and push per the end-of-session skill.
- Wrap mail `[Secuura/Blockchain-S -> Wednesday] Session wrap 2026-11-02`: closed / commented / left-open keys with one-line reasons, every candidate, your faults.

PROVENANCE:
- Seat ordinal: `Seat S 12th` 0 hits, `Seat S 11th` positive control in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md | Wednesday's /usr/bin/grep -c -i | read 2026-11-02
- The 100 DONE-NOT-CLOSED tickets and their evidence rows | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/triage_A.md, triage_B1.md, triage_B2.md (three read-only Sonnet triage agents, 12:0x-12:2x AEDT), keys extracted by Wednesday's python into /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/closeout_1.txt | read 2026-11-02
- Kintsugi deployed at develop b1fb543640e7 on 2026-11-01 | Seat D 48th STATUS B (accepted 18:49 AEDT 2026-11-01) as recorded in /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP.md | read 2026-11-02
- Tool sources close_t6.py, ticket_read_r72.py, with_linear_r72.sh | ls by Wednesday of the two 5_Project_History tool folders | read 2026-11-02
- Kam's 12:06:10 words | kam_msgs.sh live board read by Wednesday 12:06 | read 2026-11-02
- Scope: this brief writes only comments and Done states on the 50 listed tickets; blast radius = those tickets (each re-read before any write) | Wednesday's statement of scope | read 2026-11-02
- Kam's 12:42-12:44 card rulings (KS-889 b, KS-601 a, KS-229 b, KS-1336 a, KS-762 c) | kam_rulings_today.sh live read 12:43:52 and reconcile_rulings.py --apply receipts by Wednesday | read 2026-11-02
- Kam's 12:44:58 archive instruction | kam_msgs.sh live read by Wednesday 12:45 | read 2026-11-02
- Kam's 13:19:40 In Review instruction and the WRONG-STATE rows | kam_msgs.sh live read 13:20 and /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_ks-high-triage/triage_C_inreview.md (read-only triage agent 13:2x) | read 2026-11-02
SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 12:20
