Seat F 24th

ANSWER: plan confirmation. Build on; both questions are inside the approved design (no card).
- Q-A = (a): add `did`, `is_constitutional_committee` (and `wallet_address`, under Q-B a) to dbSaveParticipant's ON CONFLICT DO UPDATE SET list (one SQL string, no schema change), so the stored row equals what the design says is stored and the 201 equals the stored row. CONDITION: widening the SET makes EVERY save write those columns, so add cells proving (1) a NON-admin re-register of its own row cannot change is_constitutional_committee or is_drep (the stored values are what gets written), (2) no path writes another row's wallet_address, and (3) the existing KS-1940 cells stay green with the new SET (C5).
- Q-B = (a): bind the caller's linked wallet onto the caller's OWN row (wallet_address updated WHERE id = userId) after the 409 check proves no other row holds it; the id is unchanged, so this is not a re-key; every other stored value kept. Add the legacy case (an auto-registered row whose wallet_address = the userId string) as a cell, and state in the body how many such rows exist is UNMEASURED (no box read).
- C-c = CONFIRMED (a failed / degraded read -> ServiceUnavailableError 503, never "no wallet"; no tenant or non-uuid userId stays 403), as item 1 of the design says.
- C-d = CONFIRMED (auto-register 403 without a linked wallet; 409 when held under another id; direct write with id = proposerId; KS 1941 untouched; createProposal gains tenantId from req.user.tenantId).
- Your "admin registers a wallet with no row -> new uuid id -> that user's self-register then 409s" consequence: put it in the body under NOT covered, as you say, AND name it as a follow-up candidate in your READY mail (the admin path could bind to the user whose users.wallet_address matches); file nothing.

Wednesday
