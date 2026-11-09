# Spark o123: report (expanded by Wednesday 00:5x from the operator's final message; its own save was 329 B)
Spark rounds o123: 1 briefed, 1 PASS (1 held), 0 FAIL, 0 still queued. develop d0b4825cc244 both ends. load1 3.3-4.6 throughout.

HELD: KS-1516 (Kam card secuura-ks1516-unverified-timestamp-claims-1102 = a), code_patch2 rung 3, PASS 7/7 in 125 s, byte-identical to golden (golden control also 7/7 incl. A6 whole timestamping suite and A7 tsc rc 0).
READY: 2_Project_Files/local-model/night/READY_KS-1516-KS-1516-O123-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-INDEX-PASS-7of7_2026-11-10.diff.md (present by ls 00:5x). Brief: night/briefs/ks_1516_o123_p1_timestamping_opentimestamps_and_blockchain_report_verified_false/.
Product: Blockchain/Dev/services/timestamping/src/index.ts +9/-2 (4 hunks): create sets verified=false for opentimestamps + blockchain (response and INSERT; no verified_at); verifyTimestamp returns verified:false with a reason for both types before any DB lookup (row or no row, even a stored verified=true row); rfc3161 unchanged.
Test: new ks1516-opentimestamps-and-blockchain-are-never-reported-verified.test.ts, 124 lines, 10 cells: R1-R6 red at tip, green after (create x2, forged verify no row x2, stored verified row x2); C1-C4 rfc3161/no-attestation controls green both ways. Suite 105 -> 115.
Open-PR census: 69 PRs / 329 files both ends; none lists the two files; planted control PRs 649 and 575 (timestamping/package.json) seen.
TIER 1 GATE OWED (evidentiary path, live API change). FLAGS: a stored verified=true row now answers false and loses its timestamp/tsaUrl fields; the old JSON-decode switch for the two types is dead code, left in; live clients reading `verified` for these types NOT searched.
RESIDUE (not done): already-stored verified=true rows (a count, then an approval-class backfill); supportedTypes + OpenAPI text; Blockchain/Dev/CONNECTORS.md 'known deviation, KS-1516' sentence goes stale; options b/c.
Queue empty by SCOPE (1 of 5 rounds, ~13 of 90 min), not pool exhaustion; KS-2008 left deferred behind KS-2017. Queue-drain wrote spark/done.md and state/queue.log.
