## QA GATE - TIER 1, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 41's returned text, 19:3x AEDT. Opus. Probes in `probes/`, copied from the session scratchpad.)

**Subject:** PR #1838, KS-1384 F-a, head f27499dd9027 at start and end. No money defect found in the code.

### FIX BEFORE MERGE (text only, no head change)
1. MINOR: "its spec field is the only consumer-visible change" and "F-a moves no money" are overstated. (a) Outside NODE_ENV=production, POST while anchoring is down then POST again: base 202 then 400 "already anchored", 0 forwarded; head 202 then 202, 1 forwarded. So F-a can reach a first mint base blocked forever; no double fee, anchoring's own row blocks a repeat. docker-compose.yml:572 hardcodes originate to development; docker-compose.production.yml sets production; which file each box uses is UNMEASURED. (b) Originate anchor GET in the pending window: base transactionId = anchor id, verified true; head transactionId null, simulated true, simulatedTxRef tx_anchor_..., verified false. verified false is more honest; simulated true on a real pending anchor is wrong; other paths already show this shape on base. (c) A failed saveAnchorToDb used to answer 500; now cannot (by reading).

### FOLLOW-UP (none block)
- Test gaps: `no-reset-inside-window` (near-unreachable; gate's cell E4 kills it), `no-continue-after-confirmed` (a chain-confirmed row past the window whose confirmed write returns 0/null must never be failed).
- Starvation is pre-existing, not worsened: on real Postgres 25 older non-final rows with non-hex hashes left a real stuck row at scanned 0 over 4 passes. Such rows are what base's saveAnchorToDb wrote on a network mismatch. F-a stops new ones, does not clean old. Rev 4 §6 "every in-flight row ends" rests on this. Box census owed.
- Permanent flapping never fails a row (20 passes). Design's direction; a stranding path.
- Provider matrix: only 404 counts as answered; 400/402/403/418/425/429/500/503/ECONNRESET polled 0, 0 writes; 200 {} confirms (pre-existing `if (tx)`); 200 null counts as answered.
- Dead code: BuiltStatusUpdate.conditional read only by tests; `status` added to the SELECT never read. Rev 4 says metadata_payload.timestamp; code reads .secuura.timestamp (real shape).
- threadTokenMint: passed 1/1 alone here; "fails at base too" NOT reproduced; a 60 s timeout under load in the suite.

### Q1 no behaviour change at submit: TRUE at anchoring, FALSE overall (finding 1a). Q2 reconciler's count: SOUND; 15 real-Postgres cells; differential 2,000 runs: head earlier than base 0, head-only failures 0; control fired. Q3 tests bite on the money lines: 33 mutants, 22 killed, 7 survived the full suite (polled-default-1, no-reset-inside-window, max-tracked-1, confirmed-null-counts, no-continue-after-confirmed, x-dbdown-ts-null, x-updatedAt-apart), 4 survived the targeted lane, some equivalent. Q4 rev 4 scope delivered. Q5 no contradiction with the review.

### Counts: spark_gate head 42/42 on 4 files, base 34 red, 8 pass. Anchoring 599/600. Real lane 110/110. Originate 1862/1863 (the red is the gate's own untracked file). tsc 1 error at index.ts:346, identical at base, an artefact of the gate's dependency layout. Container g41-pg-1838 removed by id.

### NOT TESTED: a real provider outage; Blockfrost; whether two passes suffice on a congested chain; the straddled millisecond; which NODE_ENV any box runs; Node 24; eslint, check:openapi, docs checks, hook legs; Schemathesis, Akto, Playwright, k6, a running stack; the SDK's internal retries.
