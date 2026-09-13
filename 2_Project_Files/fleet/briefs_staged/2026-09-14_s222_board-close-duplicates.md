# s222 — Secuura/Blockchain (BOARD SEAT, pane `Secuura/Blockchain-C`) — close the five TRUE-DUPLICATE clusters into their survivors on Kam's 08:55 standing rule; nothing else on the board moves

## BLUF
- **You are Secuura s222, a BOARD seat on pane `Secuura/Blockchain-C` (subject tag `[Secuura/Blockchain-C -> Wednesday]`), successor to s219** (wrapped 22:55:52Z — its history entry is in `5_Project_History/history.md` above s220's/s218's; if it is not, STOP and mail). Linear writes only under the project's board identity: no repo write, no worktree, no PR, no deploy, nothing to Peter/Stuart, no extranet, never delete.
- **KAM RULED (terminal, 2026-09-14 08:55 AEST, verbatim): *"if these are truly duplicates, no need for external review or comment, let's just close them and archive them ourselves. This should be a standing rule going forward."*** Lesson: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-14_true-duplicates-are-closed-and-archived-by-us-no-external-review.md`. It supersedes s219's "Peter and Stuart rule per cluster" for the FIVE TRUE-DUPLICATE clusters only; the 25 OVERLAPPING clusters are NOT duplicates and stay untouched.
- **The clusters and survivors, from s219's records (read them WHOLE first, read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-14_s219/records/clusters.md` (rows C4, C20, C23, C24, C31 — their full membership is THERE; this brief names only the survivors and the members Wednesday read at 2026-09-14 08:58), `records/comment_body.md` (what was posted), `records/tickets/` (the per-ticket saves). Survivors: **C4 → KS-848** (alt. KS-933 — see below), **C20 → KS-826** (s219's stated preference: KS-1051 — see below), **C23 → KS-1026** (the fixing PR #916), **C24 → KS-987**, **C31 → KS-783**. Seven duplicates in all (the records name them), every one created by our account (Wednesday read creator fields at 2026-09-14 08:58: kamil.kreiser@secuura.ai on all twelve ids below) — none is Peter's or Stuart's, so the rule reaches all seven.
- **Partition:** this seat touches ONLY the tickets in those five clusters + ONE follow-up comment on KS-485. Live seats: s220 (bare pane, MERGE seat — its merges move develop and close KS-790/KS-798/841/799/KS-991 by squash: not yours), s221 (`-D`, L1 successor, launching), QA gates on `QA/Secuura-*` panes. The inbox is shared: a mail naming another seat is not yours.

## QUEUE
1. **ITEM 0 — MEASURE (read-only): every ticket in the five clusters re-read by number (`includeArchived:true`; state, assignee, creator, archivedAt, relations, `comments(first:50)` client-sorted, attachments/PR links); s219's records diffed against the live read; develop `ls-remote` (a moved develop changes nothing here — name it). Plan mail → proceed WITHOUT waiting if the twelve state lines below still hold and no member is Peter's or Stuart's (Wednesday CONFIRMS this plan in advance); a member that moved, or a client-human creator → STOP on that cluster and mail.**
2. **ITEM 1 — SURVIVOR CHECK, two clusters need your read: C4** — s219 chose KS-848 (older id) with KS-933 as the alternative (4 relations, the KS-892 family context): pick the survivor by the rule *the ticket with the fixing PR, else the one holding the most context, else the older id*, and say which and why in the comments; **C20** — s219 preferred KS-1051 (High; holds the measurement, three fix shapes, the Ask, four relations) over the rule's older id KS-826: Wednesday ACCEPTS KS-1051 as C20's survivor under "the ticket that holds the work" — close KS-826 into KS-1051 unless your read says otherwise (then mail).
3. **ITEM 2 — per duplicate, in this order, one ticket at a time, census of the cluster + KS-485 after every write (0 walks on the rest):** (a) carry onto the survivor anything the duplicate holds that the survivor lacks (a measurement, a fix shape, a relation, a PR link) as ONE facts-only comment on the survivor, or state "nothing unique"; (b) write the `Duplicate of <survivor>` relation; (c) ONE facts-only comment on the duplicate: the survivor id, the read that proved it (the words/lines from both tickets), "closed under Kam's 2026-09-14 08:55 standing rule (true duplicates are closed and archived by us)"; (d) state → the completed state s218 used (**Done**, then archive; the choice beyond Done is Kam's, as the s218 precedent recorded); (e) read back the comment by id, 0 at-signs.
4. **ITEM 3 — ONE follow-up comment on KS-485** (facts-only, **NO at-sign** — the mention exists on `2e69115a`): "Update: Kam ruled (2026-09-14 08:55) that true duplicates are closed by us — the five true-duplicate clusters (C4, C20, C23, C24, C31) are closed and archived into their survivors: <duplicate → survivor, ×7>. The 25 overlapping rows above stand as information; nothing to rule on." Read back by id.
5. **ITEM 4 — wrap:** records `5_Project_History/2026-09-14_s222/`, history entry ABOVE s219's, wrap mail: closed N / carried M / survivors chosen (C4, C20 with the reason) / the KS-485 follow-up id / board count before/after (`board_count.sh`; all seven are Backlog → active expected unchanged at 103, backlog 273 → 266; quote the real numbers).

## State lines read by Wednesday at 2026-09-14 08:58 (Linear GraphQL, includeArchived:true)
- KS-848 · Backlog · assignee kamil.kreiser@secuura.ai · creator ours · 0 comments · relations none — C4 survivor (s219's pick)
- KS-933 · Backlog · assignee ours · creator ours · 3 comments (newest 2026-09-07T03:28Z) · related KS-928/KS-930/KS-926 — C4 alternative survivor
- KS-826 · Backlog · assignee ours · creator ours · 1 comment (2026-09-07T03:25Z) — C20 (rule's survivor)
- KS-1051 · Backlog · assignee ours · creator ours · 0 comments · related KS-1046/KS-961 — C20 (s219's preferred survivor; ACCEPTED)
- KS-1026 · In Progress · assignee ours · creator ours · 1 comment (2026-09-09T01:38Z) · related KS-993 — C23 survivor (PR #916)
- KS-994 · Backlog · assignee ours · creator ours · 0 comments · related KS-969/KS-990 — C23 duplicate
- KS-987 · Backlog · UNASSIGNED · creator ours · 1 comment (2026-09-07T22:22Z) — C24 survivor (assign to the board account on close of its duplicate)
- KS-1021 · Backlog · UNASSIGNED · creator ours · 0 comments — C24 duplicate (assign, then close)
- KS-783 · Backlog · assignee ours · creator ours · 1 comment (2026-09-07T03:25Z) · related KS-579 — C31 survivor
- KS-809 · Backlog · assignee ours · creator ours · 1 comment (2026-09-07T03:25Z) — C31 duplicate (both tickets' 09-07 "cross-linking, not collapsing" decision is quoted in s219's row — Kam's 08:55 rule supersedes it; say so in the comment)
- KS-485 · Todo · assignee ours · creator peter@obeden.com · 29 comments (newest 2026-09-13T22:51Z = s219's proposal) — the ONE follow-up comment goes here
- The remaining C4 members (two more tsconfig tickets) are named in s219's `clusters.md` row C4 — read them there and at source; Wednesday did not read them in this action.

RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-09-14 08:55 (terminal): true duplicates are closed and archived by us, no external review or comment — THIS SEAT DELIVERS IT (the artefact = the seven closes + the KS-485 follow-up).
- 2026-09-14 08:11 (panel): card `secuura-board-dedupe-31-clusters` → b — delivered by s219 (KS-485 comment `2e69115a`); nothing further.
- Standing (unchanged, from the s218/s219 briefs): tickets already on Peter/Stuart stay theirs; client-facing communication = ticket comments only, the extranet is not a channel; one ticket per logical path when creating (none created here).

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- (2026-09-14 08:5x, Wednesday) This plan is CONFIRMED in advance (QUEUE 1). C20's survivor = KS-1051 (accepted). Archive, never delete. No relation other than `Duplicate of`. Nothing on KS-772.

PROTOCOL
- Mail: plan mail first (subject `[Secuura/Blockchain-C -> Wednesday] QUESTION: plan confirmation s222`), then a STATUS after ITEM 2, then the wrap. Wednesday's ANSWERs wake you by mail + a pointer tap; the 15-minute fallback stands for non-approval-class questions; a board close is reversible (archive) and inside the rule — not approval-class.
- Instruments: s218's `linear_ops.py` (re-keyed) in `5_Project_History/2026-09-14_s218/item0/` is the write instrument s219 also used — controls before the first live write as s218 ran them (identical-census diff 0 / altered-census diff fires / at-sign assert / CAS restore refused on a wrong expected state).

HOLDS
- Standing Secuura lines (the s219 brief §HOLDS, unchanged). Plus: ONLY the five clusters' tickets + KS-485 are written; the 25 overlapping clusters are not touched; no state change on any survivor except assignment of KS-987; no at-sign anywhere in this seat's writes; never `rm`; no repo verb.

SELF-CHECK
- Wednesday, 2026-09-14 08:58: state lines above copied from one GraphQL read in the same action as this brief; the cluster membership beyond the twelve ids is s219's record (`clusters.md`), not re-read; nothing in this brief contradicts Kam's 08:55 words or the 08:11 ruling (which s219 delivered).

PROVENANCE:
- KS-892 state (Duplicate, archived 2026-09-08T00:18:11.315Z, updated 2026-09-07T03:27) — named only as the KS-892 collapse family in the C4 context, NOT queued | Linear ticket KS-892 (includeArchived:true) | read 2026-09-14
- KS-848 state (Backlog, 0 comments) | Linear ticket KS-848 | read 2026-09-14
- KS-933 state (Backlog, newest comment 2026-09-07T03:28Z) | Linear ticket KS-933 | read 2026-09-14
- KS-826 state (Backlog, newest comment 2026-09-07T03:25Z) | Linear ticket KS-826 | read 2026-09-14
- KS-1051 state (Backlog, 0 comments) | Linear ticket KS-1051 | read 2026-09-14
- KS-1026 state (In Progress, newest comment 2026-09-09T01:38Z) | Linear ticket KS-1026 | read 2026-09-14
- KS-994 state (Backlog, 0 comments) | Linear ticket KS-994 | read 2026-09-14
- KS-987 state (Backlog, unassigned, newest comment 2026-09-07T22:22Z) | Linear ticket KS-987 | read 2026-09-14
- KS-1021 state (Backlog, unassigned, 0 comments) | Linear ticket KS-1021 | read 2026-09-14
- KS-783 state (Backlog, newest comment 2026-09-07T03:25Z) | Linear ticket KS-783 | read 2026-09-14
- KS-809 state (Backlog, newest comment 2026-09-07T03:25Z) | Linear ticket KS-809 | read 2026-09-14
- KS-485 state (Todo, newest comment 2026-09-13T22:51Z) | Linear ticket KS-485 | read 2026-09-14
- Kam's 08:55 ruling (quoted verbatim above) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-14_true-duplicates-are-closed-and-archived-by-us-no-external-review.md | read 2026-09-14
- s219's cluster table and comment | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-14_s219/records/clusters.md | read 2026-09-14
- scope: the five TRUE-DUPLICATE clusters of s219's table (C4, C20, C23, C24, C31), quoted: "TRUE DUPLICATE (class) — one survivor" (C4), "TRUE DUPLICATE (the ask)" (C20), "TRUE DUPLICATE" (C23), "TRUE DUPLICATE (one mechanism)" (C24), "TRUE DUPLICATE by the words — with the prior decision quoted" (C31) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-14_s219/records/clusters.md | read 2026-09-14

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-14 08:59
