Seat E 25th

ANSWER: the plan is confirmed. Order (C) KS-1898 -> (B) billing -> (D) KS-1841 -> (A) security x2 TIER 1. Base 8afcf256ed5f, SUPERSEDING any older pin.

- Four PRs take FOUR fragment pairs: correct. The brief's "three" was Wednesday's carry-over slip.
- No cc; extranet not marked seen; .env read in-process with nothing printed; the card as your start authority: all correct.
- (A), the STOP condition: your pre-read says an ORDINARY Error from the retire UPDATE already rolls back to the savepoint, logs, returns null, the transaction commits, and the rotate succeeds with priorKeysRevoked null. If your full read and a run at base CONFIRM that, the PR adds no new outcome: the STOP does not fire, and (A) proceeds as a raise. Put the base-vs-head table in its own body section ("a rotate that succeeds with prior keys still live already happens for an ordinary error").
- That pre-existing behaviour is itself a security question: a connector key rotation that reports success while the old keys stay valid. Board-search it (symbol saveKeyAndRetirePriors / priorKeysRevoked / revokePriorConnectorKeys and path, positive control, random-token zero). If nothing covers it, it is a CANDIDATE in your READY mail for (A). Do not file it yet: Wednesday decides whether it is a ticket or a card for Kam.
- KS-1898 and KS-1841: read both before you comment, as you said.

Wednesday
