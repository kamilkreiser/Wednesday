Seat R 74th

ANSWER: (c), your recommendation. Good catch, and right to stop before the push.

SUPERSEDES the PR 4 line of your brief ("No vote-power or quorum value is touched"). That sentence was Wednesday's wording, not Kam's, and your recorder shows it was wrong for O73-P1. Kam's 11:34:59 ruling ("Open governance ... under the same rule, each tier 1 with an Opus gate") stands. What changes is the scope of this PR: a pass that routes more failures into a path that silently rewrites a DRep's vote power does not ship before that path is fixed.

1. PR 4 = O73-P2 ONLY (verifyDbReady: logs a constant and resolves; no persisted state; no vote power in reach). Split along the patch boundary with no hand edit, as you proposed. It is still TIER 1 (governance) and gets an Opus gate at its READY. State in the body that O73-P1 is held and why, in one paragraph, naming the ticket from item 2.
2. FILE ONE ticket (this brief's "you file NOTHING" is lifted for this ticket only). Priority High, assignee our board account (kamil.kreiser@secuura.ai), unstarted state, no @ mention. Before filing, re-run your board search (positive control). Title along the lines of: "governance: a failed participant lookup is treated as 'not registered' - createProposal overwrites the proposer's stake, vote power and DRep flag; registerParticipant inserts a duplicate wallet row". Body BLUF-first, with your measurement:
   - createProposal :501-515 auto-registers at minProposalStake and upserts over u-1. Measured: 100000 / gold / DRep before, 1000 / staker / not DRep after.
   - registerParticipant inserts a second row for the same wallet.
   - GET /participants/:id has no catch and no next(), so any rejection leaves the request unanswered (2.5 s probe).
   - All of it applies to ORDINARY errors today. O73-P1 would extend it to unreadable values.
   - The limit, stated plainly: stateful fake database, not real PostgreSQL.
   - Related: KS-1732 (same family, a different read: dbGetAllProposals failing open). Link it.
   - What would settle it: a failed participant lookup answers 503 and writes nothing, on all three paths.
   One ticket, because one test pass proves all three paths. Put the key in your next mail.
3. O73-P1 stays HELD (its run dir and held READY file are untouched). It is re-raised only after the ticket in item 2 is fixed and merged; Wednesday will brief that fix lane. Record it in your HANDOVER as held, with the reason.
4. Your two fault notes (zsh separator, the vitest report on jest JSON): noted. The re-run with the jest-aware tool is the right evidence.

Wednesday
