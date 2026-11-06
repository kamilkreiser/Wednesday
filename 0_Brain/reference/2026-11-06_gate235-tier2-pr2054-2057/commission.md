# Gate 235 commission: Secuura / Blockchain, PRs 2054, 2055, 2056, 2057 (batched), TIER 2, round 1 of 2 each

Written by Wednesday 2026-11-06. Model: Sonnet, row G2. Batched under Kam's 2026-09-18 rule: disjoint by file by the seat's report, one session, one clone. Give one verdict per PR.

Tier reasons, and they are claims. 2055 and 2057: test only. 2056: ten log lines lose a field. 2054: a stored value changes from 0 to null on four writes, the highest risk here.

STOP LINE, per PR: if a reader in any service, gateway, frontend, generated spec or SDK treats a stored block height of 0 differently from null in a way a caller sees, or if 2056's change alters anything but log output, stop that PR's review and write NO GO at tier 2 for that PR with one line: re-commission at tier 1. Say it and carry on with the other three.

My own search, framed: git grep at develop over Blockchain/Dev/services/*/src and Blockchain/Dev/packages, tests excluded, for block height beside a comparison. Hits: documents.ts:1019 and :1780 (the '|| 0' writes), anchorStateSync.ts:592 (stored > 0), anchorSubmission.ts:560 (a different field by its name, unread). Frontends, responses and the spec were NOT searched by me. That is your question 1.

QA GATE: findings only; fix nothing; write nothing outside this folder; no box; no docker; post nothing; network only for git fetch into your own clone. Absolute paths, never cd. DevMASTER has about 26 GiB free and falling: one shallow, small clone, no second one, no full install where a targeted one proves the point; say what you could not run because of that. Overwrite verdict.md at the end. A commit on any head voids that PR's verdict. Re-read the five refs with ls-remote at your start and say so if any moved.

Read first: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md; pins.txt here; the four READYs named there. Every count in them is V 24th's and not re-run by V 25th.

## Questions
1. PR 2054, KS-1509: enumerate every reader of the stored height across the repo at the head: services, frontends, generated types, the spec, and any status or confirmation logic. The READY says no predicate and no response shape change. A value that was 0 now reads null in what a client receives: is that a response change? Which is true on a real path? Does the ticket's 'seven other places' match the four changed, and where are the other three? What does toBlockHeight do with bad input? Plant one tamper of your own.
2. PR 2056, KS-1937: is the address gone from all ten lines, and from anything else those functions log, including error objects? The READY says provider error text is still forwarded, unmeasured: read whether it can carry the address and report it. Does the address still reach the mailer? Is losing who was refused acceptable under the ruling, which is Kam's card secuura-ks1346-logging-thrown-objects-leaks-secrets (read with decision_queue.sh show, never add)?
3. PR 2055, KS-1666 N1: run gate 203's mutant OWN1. Is A5b the only failing cell, as claimed? Sample one tamper. Is 'routes/certifications.ts byte-identical' true?
4. PR 2057, KS-1600 item 2: a pin of existing behaviour, so what would make its cells fail? Sample the two-removal tamper. Does the test go through the real stack, as its name says? Item 3 is Kam-ruled and unbuilt: is the PR body's wording now true, given V 25th's Finisher note corrects 'default no behaviour change'?
5. All four: the docs fragments against the code. The hook verdict in each READY says PREFLIGHT INCOMPLETE, legs 3, 4, 8 skipped, local stack not up: state what those legs would have checked that matters to each PR. Merge tree of each head on develop per pins.txt: rc and full tree; shared paths with what moved since its base and with the other three PRs; a merge order if one is needed. PR bodies: does any sentence claim more than was measured?

## Output
verdict.md: for each PR, a line giving PR number, GO, GO WITH NOTES or NO GO, and head; then BLUF, findings with severity, file:line, evidence path, FOUND / TESTED / HOW, what was NOT tested, your own conduct. Final message: one verdict line per PR plus one line per finding.
