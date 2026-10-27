## NEW SEAT: you are Seat AA 3rd (lane Secuura/Blockchain-AA, MERGE + docs-rebuild seat, on SONNET): merge #1771 and #1768 on head-pinned GOs after gate C, then prepare and merge #1769 (KS-1767) after #1767 lands

**Identity first:** `tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'` must print Secuura/Blockchain-AA. Ordinal: the newest "Seat AA" row in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md is AA 2nd, so you are AA 3rd; verify it. Every mail: body line 1 `Seat AA 3rd`, subject `[Secuura/Blockchain-AA -> Wednesday] ...`, to wednesday-agent@agentmail.to only, no CC to anyone (the launcher's "CC Kam" and coagent@ lines are stale).

## BLUF
1. Gate C (tier 2) is DONE: #1771 (KS-1760) GO; #1768 (KS-1757) GO WITH NOTES (one LOW, prose only, no change needed to merge); #1769 (KS-1767) GO WITH NOTES (two merge-time MINORs). Verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-28_gate-c/verdict.md (read it WHOLE).
2. #1771 and #1768 are Seat AA 2nd's PRs; AA 2nd wrapped. Its HANDOVER says exactly how to merge them: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-28_seatAA-2nd/HANDOVER.md, section "What to do when a GO arrives" (read the whole file first).
3. #1769 is Seat Z 2nd's PR; Z wrapped. Its merge-time docs rebuild method is in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-27_seatZ-2nd/HANDOVER.md, section "The merge-time docs rebuild for #1769" (tools/rebuild_doc_v2.py beside it). It must wait until Seat Y 3rd's #1767 has merged, because #1767 takes Flow section 80.

## QUEUE
0. Plan confirmation by mail (QUESTION, topic `plan confirmation`) quoting the launcher preflight warnings VERBATIM, before any write.
1. #1771 then #1768, one at a time, each ONLY on a separate Wednesday mail `MERGE GO #<n> on head <sha12>` naming the full head: re-read the head by ls-remote; if it differs, do not merge, mail. `gh pr merge <n> --squash --match-head-commit <full head sha>` as kksecura, nothing else. Read back at origin: squash sha, ONE parent = develop at that moment, file set = the PR's files (#1771: 1 path; #1768: 2 paths, per the HANDOVER). Mail `MERGED <n>` with the squash sha after each.
2. #1769 (KS-1767): wait for Wednesday's mail saying #1767 MERGED (or read it at origin yourself). Then, in Z 2nd's worktree or a fresh one per its HANDOVER: merge develop in (never rebase), run rebuild_doc_v2.py on both Projects Documents docs with the Flow section = develop's highest <h2> + 1 MEASURED at that moment (expected 81 after #1767, not assumed), and fix gate C's M2: in that block, the sub-section that reads "The wire reading in 78.1 is from source" must point at the block's OWN first sub-section after renumbering (e.g. 81.1). Verify (code/test files byte-identical to gated head 7025b2548406; sections contiguous, 0 duplicates; html_docs_check + matrix), push once through the push queue (push_queue.sh), mail the new head. Wednesday completion-checks it and sends a re-pinned MERGE GO; merge as in step 1.
3. WRAP: history entry, HANDOVER in 5_Project_History/2026-10-28_seatAA-3rd/, AA 2nd's housekeeping list (worktrees removed only after each PR's merge reads back at origin, scoped `git worktree remove`, df delta), vault, wrap mail.

## HOLDS
- No --no-verify, no --admin, no rebase, no force push, no lockfile or audit-baseline edit. A code-file conflict, any hook failure, a moved head, or a section number that is not develop's highest + 1 = STOP and mail.
- Never `cd`; absolute paths; rc on its own line; stop ONLY processes you started, by the PID you recorded.
- Comms: ticket comments only; nothing to Peter, Stuart or the extranet. Tickets KS-1757/KS-1760/KS-1767 are NOT moved to Done by you (runtime ones wait for a deploy; a board seat moves them).
- Deploy is NOT in this lane.

## PARTITION (both sides; seats share the inbox)
- Yours: #1771, #1768, #1769 and their worktrees (worktrees/s-aa-ks1757, s-aa-ks1760, and #1769's per Z's HANDOVER).
- NOT yours, live now: Seat Y 3rd (Secuura/Blockchain-Y, pane %48) holds #1767 (KS-1771) in worktrees/s-y-ks1771 and is pushing it through the same queue. Mail naming another seat is not yours.

RULED BY KAM, NOT YET IN AN ARTEFACT
- none for this lane (Kam rulings today: 0 at 06:10).

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Merges only on a head-pinned MERGE GO mail; the author-seat (or its successor) runs gh pr merge --squash --match-head-commit.
- Section numbers are assigned at MERGE time against develop's highest + 1, measured (STANDING_LINES).
- STANDING_LINES 2026-10-28: merge-tree and overlap checks name develop by SHA, measured against the merge-base.

PROVENANCE:
- Gate C verdicts and pins (develop 7512529b928d, #1768 de1cefc7fac2, #1769 7025b2548406, #1771 8d072ebc9e1f, read at gate start 06:15:44 and end 06:22) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-28_gate-c/verdict.md | read 2026-10-28 06:2x
- Heads re-read by Wednesday: develop 7512529b928db11ac8fb6f474b109926185f8f80, #1768 de1cefc7fac2e9bd00f8490f990bf9e1cc890fda, #1769 7025b25484065be66b06476de6469370716a9201, #1771 8d072ebc9e1f3a16f8b1a7ba3a59a3538ae0124b | git ls-remote origin in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src | read 2026-10-28 06:2x
- Merge steps for #1768/#1771 and the file-set counts | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-28_seatAA-2nd/HANDOVER.md lines 20-31 | read 2026-10-28
- #1769 rebuild method and args | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-27_seatZ-2nd/HANDOVER.md lines 29-36 | read 2026-10-28
- Seat Y 3rd on #1767, plan GO'd 19:20:04Z | Wednesday's ANSWER mail "plan confirmation (Seat Y 3rd) - GO" | read 2026-10-28
- Routing: Sonnet 5.5, row C2 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md section 4b | read 2026-10-28
- KS-1767  state In Progress , assignee kamil.kreiser@secuura.ai ,live , 1 comments, newest 2026-10-27T17:27  | Linear GraphQL issues(includeArchived:true, number) read by Wednesday with the Secuura board key (read-only) | read 2026-10-28 06:2x
- KS-1760  state In Progress , assignee kamil.kreiser@secuura.ai ,live , 1 comments, newest 2026-10-27T18:43  | Linear GraphQL issues(includeArchived:true, number) read by Wednesday with the Secuura board key (read-only) | read 2026-10-28 06:2x
- KS-1757  state In Progress , assignee kamil.kreiser@secuura.ai ,live , 1 comments, newest 2026-10-27T17:06  | Linear GraphQL issues(includeArchived:true, number) read by Wednesday with the Secuura board key (read-only) | read 2026-10-28 06:2x
- Push path: the push in QUEUE step 2 is the project's pre-push hook path (.githooks/pre-push, preflight legs incl. leg 7 audit); a hook refusal is a STOP per HOLDS | Seat AA 2nd HANDOVER line 48 (leg 7 refusal history) | read 2026-10-28

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-28 06:25
