Seat F 23rd

ANSWER: KS-1942 design. The design is ACCEPTED as proposed (items 1-5), with these rulings. They are Wednesday's readings of Kam's ruling text, card secuura-ks1942-register-sets-any-wallet-stake-1102 = a, option verbatim: "a Claude seat builds a trusted source (the wallet linked to the signed-in user; stake from a real or admin-set value), red-first cells, Opus QA gate, merge on Wednesday's GO; design brought back first".

- D1 = (a): createProposal's auto-register stores stake 0 with the caller's linked wallet. Today's 1000 grant is neither a real nor an admin-set value, so (b) would contradict the ruling. Consequence (a proposer needs an admin-set stake) goes to Kam on the panel tonight as FYI; if he says otherwise, his word supersedes this line, and the successor seat is told before it builds.
- D2 = (a): a non-admin body asking for a stake / DRep / committee value different from the stored one gets 403 "Only an admin can set stake or roles", no write. A new self-register sends stakedAmount 0 (schema unchanged).
- D3 = (a): the self-register id is the caller's userId. A conflicting older row (the linked wallet under a different id) answers 409 and writes nothing; re-keying existing rows is a DATA change and is Kam's (list it as a finding with the count measurable read-only, nothing more).
- D4: FILE the staking candidate now (you have the tools): one ticket, priority HIGH, after your board search (you already ran it: KS-1845 covers only GET /api/stake/all), assignee our board account, BLUF first, facts only: "POST /api/stake (and by the same shape the unstake routes, not read line by line) takes address and amount from the body with no ownership or chain check (services/staking/src/routes/stake.ts:189-245): any signed-in caller can create or grow a stake position for any address; txHash is logged but never verified". Say in it that KS-1942's design treats svc_stake_positions as NOT a trusted stake source for that reason. Name the key in your next mail.
- The platform-role check is `isPlatformRole` as in KS-1845; admins keep today's behaviour except omitted flags are KEPT (your item 3): accepted.
- Your matrix R1-R9 + C1-C5 + the real-PostgreSQL RLS proof + the five mutants is the acceptance matrix; C5 must state the T6 change under D1a in the PR body.
- Scope, tier and order: services/governance only, TIER 1 Opus gate, a SEPARATE PR built on develop AFTER PR 1939 merges.

Put this ANSWER and your design mail verbatim into your HANDOVER for the successor seat (it builds; you do not). Your own work now: PR 1939's gate 121 notes when they arrive, then wrap.

Wednesday
