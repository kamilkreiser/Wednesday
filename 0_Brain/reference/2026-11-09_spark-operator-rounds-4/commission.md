# Spark OPERATOR round 4 (o117). Commissioned 2026-11-09 ~17:5x by the 17:3x Wednesday seat.
Why: o116 ended 17:48 with the queue empty (rule 2026-10-28: never keep the Spark idle).

Read WHOLE and follow, in order: round 1 /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds/commission.md, round 2 .../2026-11-09_spark-operator-rounds-2/commission.md, round 3 .../2026-11-09_spark-operator-rounds-3/commission.md and its report.md (same folder) for what was examined and rejected and why.

Changes from rounds 1-3:
1. ROWIDs use o117.
2. Also EXCLUDE: KS-2142, KS-2146, KS-2066 (o116 PASSes, HELD) and everything o116 rejected (KS-2149, KS-1812, KS-2005, KS-2026, KS-2124, KS-2115, KS-2100); KS-1807 and KS-2151 (Seat Y 11th, docs, launched 17:45: it may edit Blockchain/Dev/docs/SCOPES.md, Blockchain/Dev/docs/security/AGENT-DOCUMENT-OPERATION-RULES.md, Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md, Blockchain/Dev/CONNECTORS.md and other pages describing anchoring: touch NO file under Blockchain/Dev/docs/ and not CONNECTORS.md); KS-1473 (PR 2132).
3. Live seats: G 31st, R 91st, T 22nd, S 45th as round 3 says; Y 11th as above. The open-PR file census at the API remains the authority.
4. The drainer: start it exactly as the tooling says, inside run_in_background, NEVER with `nohup ... &` (o116 did; that is a deviation).
5. Prefer a mix that climbs one rung where the evidence allows: at least one task above doc_only (test_only_input or a small multi-hunk test change), stated as the rung tried.
6. HOLD every PASS with hold_ready.py (clean --dry-run, then the real run), report each READY path and rc. Do not raise, push, post or mail. Never fetch or run any git write verb in a /Volumes/DevMASTER/!CODING/ checkout.
7. Stop after 4 rounds or 75 minutes.
Output: final message line 1 'Spark rounds o117: <n> briefed, <p> PASS (<h> held), <f> FAIL, <q> still queued', then per ticket as round 1; also save to /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds-4/report.md if your Write is accepted.
