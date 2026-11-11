# Gate 313, TIER 2 (Sonnet, routing v1.0 tier-2 row), ONE batched session: R 100th round 3 = PR 2183 (KS-2141, test-only bash, UNGATED batch member raised by R 99th), PR 2184 (KS-1959, vc-issuer src/db.ts probeDb guard), PR 2185 (KS-2011, api-gateway services/redis.ts: in-memory fallback notification settings now EXPIRE after 24 h: a BEHAVIOUR CHANGE), PR 2186 (KS-2160, test-only, ks1547 preflight suite), PR 2187 (KS-1163, Start_Up/start-secuura.sh + two bash suites: start-up waits up to MAX_HEALTH_WAIT for five more services, Kam's card a: a BEHAVIOUR CHANGE). Five PRs, one verdict file with one section per PR. Commissioned 2026-11-12 ~03:0x AEDT by the Mac mini Wednesday seat (01:41 rotation successor). If any PR touches a security surface by your read (authn, authz, tokens, secrets, data destruction), RAISE it to tier 1 in the verdict and say why; do not continue it as tier 2.

Method: copy-and-change of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate312-tier2-pr2179-2182/commission.md (read it whole: its common-rules pointer to the gate 306 commission, its Constraints, its output shape and its controls all apply unchanged). Calibration: gate 312's verdict.md in that folder.

Pins (Wednesday's ls-remote ~03:0x AEDT; RE-READ at start and end, say whether each moved):
- develop 801a2a7145c6ad7ea5d6139b799b18d45ba824d3 (PR 2179's squash)
- PR 2183 head 16a5be1fafa0e5c37ddf5872849b236e7456529b
- PR 2184 head 1c5ca4bb36c0b632c93d8e8b6f2d066c85cd1519
- PR 2185 head 6e9281eb7e242881477a6fbf1f392717ae4100ed
- PR 2186 head bb40ba50978ad56a21a989e7d50ede02b6d78843
- PR 2187 head 8de22966e7f96b7c1d5c55a313bc6c8d520905b0
All four of 2184-2187 were cut on 4f85ca04c622 (an ancestor); ask every merge-tree question onto 801a2a7145c6.

READY (read whole; reproduce, do not trust): /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate313-tier2-pr2183-2187/ready_r100_round3_mail.txt (the R 100th section, from 'READY FOR GATE round 3'). It asks you to read three named behaviour changes: PR 2185 (24 h expiry, TTL.privacy = 86,400 s, checked by the existing 60 s interval; the expiry value is the operator's reading of the Redis branch, accepted by Wednesday), PR 2187 (one unhealthy service of five holds start-up up to 120 s, then warns; success line now 32), PR 2184 (a probe failure with an unreadable thrown value now resolves false instead of rejecting). For each: is the change what the ticket asks, is it named in the PR body, is it pinned by a cell that would fail without it (run your own mutants), and what does it NOT cover. PR 2186's red proof is a PLANT on preflight.sh line 246 in the seat's tree (never in the diff): reproduce it in YOUR scratch copy. PR 2183 was never gated: read it as a full tier-2 member.

Spark shadow (after your verdict, the same session): run local-model/gate/spark_gate.sh / spark_review.py WITH --pr-body-file on ONE product PR of your choice (2185 preferred) and record its verdict, recall against yours and any false claims, as gate 312 did.

OUTPUT: verdict.md in THIS folder (first lines: one 'PR N: GO / GO WITH NOTES / NO GO (at head ...; tier ...)' line per PR; then a section per PR with findings numbered G313-<PR>-N and graded Minor / Note / Info, each with its evidence; then the Spark shadow). If your Write is refused, return the verdict text in full. Constraints as gate 312's: write only in this folder (scratch clone under scratch/), read-only git verbs in the shared Secuura checkout, no push, no PR comment, no Linear write, no mail, no rm, no cd, never print .env values.
