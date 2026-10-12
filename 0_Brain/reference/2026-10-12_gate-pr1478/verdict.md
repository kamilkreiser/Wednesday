# Gate verdict — PR #1478 (KS-1158 R1) — GO WITH NOTE

**Head:** `ab4434490b246db7d05178840f4b65ecfb0c6688` (origin `refs/pull/1478/head`, also branch `feature/ks-1158-anchoredat-carry-keys-on-authoritative-hash-j2`).
**Base:** merge-base = `524db0ce` (#1471 KS-1124). develop now `8dcbddb5` (+2 commits that touch auth/api-gateway/openapi only, not originate).
**Gate:** independent Opus QA, read-only. Own clone (`--no-hardlinks`) in the session scratchpad. No pushes, no comments, no board writes, no DB connections. A dummy unreachable `DATABASE_URL` (127.0.0.1:1) was used only so the import-time config check would pass for the probe.

## Defects
None Major.

1. **Minor (test coverage, not a code defect)**: the "deliberately NOT changed" forensic carry at `services/originate/src/services/anchorStateSync.ts:190` (`txHash: prior?.txHash ?? null`, which keeps a placeholder hash on the failed blob) has no pin. My mutation M7 nulls the placeholder there (`authoritativeTxHash(...)`). The 7 new cells **and** the full originate suite (98/1114) all stay green under it. Suggested follow-up: add one cell asserting `blobs.sim.txHash === SIM_TX`.
2. **Minor, pre-existing, not introduced here**: `authoritativeTxHash` (`anchorStateSync.ts:80`) rejects only `tx_` and `mock_tx_`. It **accepts** `mock_batch_tx_…`, which the non-production batch mock produces at `services/anchoring/src/index.ts:1900`. All three hash decisions in the file share this gap, and so do the `FABRICATED_TX_PREFIX` regexes repo-wide. It is outside R1's scope and belongs in a separate ticket. `TX_SIM_` (uppercase) and whitespace-prefixed placeholders are also accepted, but nothing produces them, so this is theoretical only.

## By my runs
| Check | Result |
|---|---|
| Diff scope | 2 files: the one expression at `anchorStateSync.ts:200` (+4 comment lines) and the new test file. Nothing else. |
| New cells on head | 7/7 pass |
| New cells against develop's `anchorStateSync.ts` (file swapped in) | **2 failed / 5 passed**: exactly cells 1 and 2 |
| Seat mutation: string truthiness | reds cells 1 and 2 ✓ |
| Seat mutation: never carry | reds cell 3 ✓ |
| Seat mutation: time alone | reds cells 1, 2, 4 ✓ |
| Seat mutation: hash test alone, key always present | reds cell 5 ✓ |
| Seat mutation: write suppressed for submitted priors | reds cells 1, 2, 3, 5, 6 ✓ |
| Own mutations | tx_sim_-only predicate reds cell 2. Constant time reds cell 3. Placeholder txHash nulled: **green everywhere** (defect 1). |
| originate jest on head, run twice | 98 suites / 1114 tests, rc 0 both times |
| tsc --noEmit on head | rc 0 |
| eslint on head | 0 errors. 23 warnings across 15 files, none in the touched files (control: the grep matched 15 file headers) |
| Merged tree (head + develop 8dcbddb5, tree 5a06303d) | jest twice: 98/1114. tsc rc 0. eslint 0 errors. New cells 7/7. |

Mutation table: `mutations.txt`. Predicate probe: `authoritativeTxHash_probe.txt`.

## Semantics
- **A real hash is never dropped.** 64-hex in lower case, upper case and whitespace-padded forms are all ACCEPTED, so anchoredAt is carried. Rejected: null, undefined, empty string, `tx_sim_`, `mock_tx_`, `tx_`, and a non-string number. A real Cardano hash is hex, so it can never contain `_`, which means the prefix test cannot hit one. The call passes `{ txHash }` only, so the `transactionHash || txHash || transactionId` chain resolves to txHash.
- **Readers of a document blob's anchoredAt**: `frontend/issuer/src/components/DocumentDetail.tsx:191` (display, only when `blockchain.anchored`), `routes/documents.ts`, `routes/anchors.ts` (anchor_store rows, not the blob), `routes/verification.ts:111` (`isAnchoredHonestly` keys on status plus txHash, never on anchoredAt), `api-gateway verification.ts` (live anchor row), and the SDK/certification types. None of them treats anchoredAt as a precondition. None of them reaches billing or confirmations (a repo-wide grep of non-test, non-md files found no billing reader; control: the grep matched `anchorStateSync.ts` 9 times). On an `anchor_failed` blob, losing a placeholder's anchoredAt changes no status, flag or charge.
- **Composition with #1471**: after KS-1124, a supplied `blockchain` REPLACES the stored blob in SQL and carries only `threadToken` (`documentRepo.ts:544, 579`). So omitting the key really removes anchoredAt; a JSONB merge does not mask it. The read-before-write race at `anchorStateSync.ts:178-212` (the #1471 gate's open item) is **unchanged and not widened**: the new predicate reads the same `prior`. In any interleaving, the outcome with and without this PR differs only in anchoredAt, and only when that stale prior held a placeholder.

## Not checked
- Seat J's own evidence: `5_Project_History/2026-10-12_seatJ-2nd/` contains no KS-1158 file, and no local worktree sits at the head (it was found on origin only). The seat's claims were checked by my own runs instead.
- Integration (DB-backed) suites were not run, because no DB connections were allowed.
- I did not establish whether `mock_batch_tx_` can actually reach a document blob.
