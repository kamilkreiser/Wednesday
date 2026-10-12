BRIEF to S94N (Datasec/NexusAI-N): while your merge run is done (your next merge turns are items 14 RD-747 and 24 RD-131), take the two product tickets you filed yesterday. PLAN CONFIRMATION FIRST: no code before Tuesday answers.

QUEUE (board read by Tuesday 06:0x, Jira search "created >= -24h", 3 results, isLast=true):
1. RD-838 (High, To Do, filed by you 2026-10-12T12:03): "RD-640 residue (gate 19 NO GO at the cap): F-640-1 a hard-linked symlink in a chain ending at real data is read as a loop, unlinked and cert..." Scope: the ticket's own BLUF, read in full before planning; if this round closes less than the ticket, say so as narrowing.
2. RD-839 (Medium, To Do, filed by you 2026-10-12T12:03): "Anonymous /api/admin/erasure-status discloses the absolute outside path in the first-run window". Scope: its own BLUF.
(RD-837, the C-57 runner-install tooling ticket, is NOT in this brief: it is shared tooling that every seat's merge uses, so it waits for a quiet merge window.)

WHAT THE PLAN CONFIRMATION MUST CARRY
- PRIOR WORK: what RD-640's gate-19 rounds built and why it stopped at the cap (git log -S on the symlink/loop code, the gate-19 report rows for F-640-1, your own N-640 notes), and what serves erasure-status today. Keep what works; change only what the tickets name.
- PARTITION, from both sides: the exact files you expect to touch, checked against every OPEN lane head that has not merged yet (git diff --name-only main...<head> for O rd-828/833, rd-801/822, rd-802; M rd-795, rd-817; R rd-777-776, rd-761, rd-794, rd-819, rd-807, rd-775; P rd-823, rd-751, rd-831, rd-721; your own rd-747, rd-131). Name any overlap. An overlap is a STOP for that file, not a merge-through.
- TIER: both touch security surfaces (erasure, an anonymous admin route), so expect tier 1 at the gate; red-first cells, mutants, NOT TESTED list.
- One branch per ticket, named from the ticket; worktrees of your own; RD-827 own install; nothing merges outside the turn order (these join the queue after their gate).

HOLDS: no merge, no deploy, nothing to any human; Jira comments are yours under the project's identity. The jest lock is shared: proof holds queue behind any MERGE ticket (merge-first), and M's RD-795 merge turn is imminent.
-- Tuesday
