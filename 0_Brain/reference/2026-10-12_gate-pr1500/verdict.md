# QA gate: Secuura Platform K PR #1500 (KS-1333 item 4)

- Head: b2f84e85b6c5bd6904c9b34c549a247aa2e24b29 (bundle sha256/16 a5df88e4d17ba16d confirmed; single commit, parent 361537eed238e9886f4cc22d8a91607a96fb1508)
- Author's base: develop 361537ee. REAL current origin/develop at gate time: 06d33fb4b321c77270ff958f9db6accc5a622da8 (one commit newer: KS-1477, services/auth only, no file overlap). I gated the clean merge of the head onto 06d33fb4 (merge commit 60bd890a9, scratch only, not pushed).

## VERDICT: GO WITH NOTE

The change does what it says: all four writers now persist NULL for an unknown height, no reader of the blob breaks on null, and every check reproduces; the note is that two other persisted writers (verification.ts:346 and verificationV2.ts:148) can turn that NULL back into a fabricated 0 and are not on KS-1509's list.

## By my runs
(All in my clone at the merge of head onto 06d33fb4; node_modules symlinked from the project, @secuura workspaces re-pointed at my clone, shared rebuilt in the clone.)
- ks1333 cells: 10/10 pass (4 null cells, refusals cell, 4 controls, 0-preserved control).
- Full originate suite: 101 suites / 1169 tests pass (matches the author), exit 0. (suite-summary.txt)
- tsc: originate exit 0; api-gateway exit 0. eslint originate (npm run lint): 0 errors, 23 pre-existing warnings. packages/shared builds.
- check:openapi: "CHECK PASS: on-disk YAML matches generated"; spec-examples "OK", exit 0.
- Revert-each-writer (to `|| 0`): writer 1 -> W1 cell red; writer 2 -> W2 red; writer 3 -> W3 red; writer 4 -> W4 red. Each reds its own cell, as claimed. Correction to the author's wording: reverting writers 1 and 3 ALSO reds the "refusals" cell (it drives those two), so "exactly its own cell" is true for 2 and 4 only. Harmless, not a gap.
- My mutant B (toBlockHeight returns 0 for null): all four null cells red (4 failed, 6 passed). Caught.
- My mutant C (anchorStateSync imports toBlockHeight from '../routes/verification', the cycle the move was meant to avoid): tsc is CLEAN (exit 0), but ks1333 loads 0 tests and 9 originate suites FAIL to load (whole run: 92 pass / 9 fail suites). Caught, loudly, by the suite not by tsc. Sources restored; clone clean.
- JSONB on real PG15 (15.14): null stays null with key present (typeof 'null'), real 0 stays 0, absent key is a third state. (pg15-jsonb-roundtrip.txt). I did not re-run the two tenancy modes; this is the JSONB semantics only. Postgres stopped.
- PR claim `||` vs `??`: for numeric block numbers they differ only on NaN (and '' for strings), and `?? 0` gives 0 for null, so the ticket's swap would not remove the harm. Agreed by reading (null/undefined -> 0 under `?? 0`); toBlockHeight is the right fix.

## Findings
- MINOR 1: two persisted heal writers still fabricate 0. verification.ts:346 and verificationV2.ts:148 do `blockHeight: toBlockHeight(chain.blockNumber) ?? blob.blockHeight ?? 0`; their result goes to persistHealedAnchor (the V2 comment says so). With the chain height unknown AND the blob now NULL (which this PR makes the normal case), a heal re-writes 0 over the NULL. These are not in KS-1509's list (documents.ts 883/905/938/1386, anchorStateSync.ts:191). Add them. Reachability is narrow (needs a confirmed tx with no block number), so not blocking.
- NOTE 2: API-visible change. Gateway verify (api-gateway verification.ts:677 `liveBlockHeight || persistedBlockHeight`, echoed at :783) now answers `blockHeight: null` where it answered 0 for an unknown height. `null` was already in that route's vocabulary (:831 pending case) and the shared verify schema is `z.number().nullable().optional()` (frontend/shared/src/schemas/verify.ts:62). The gateway guard (:668-671) needs an integer > 0, so it refuses 0 and null alike: outcome unchanged. Worth one line in the release note for API consumers.
- NOTE 3: verifier UI (ResultPage.tsx:497) and issuer DocumentDetail.tsx:120 use `||` fallbacks, so the screen still shows 0 for an unknown height. Safe, but the fabricated-looking 0 is still SHOWN; this PR fixes storage, not display.
- NOTE 4: the OpenAPI doc at secuura-api.yaml:11608 (`blockHeight: number`, required) is the VC-verify response from vc-issuer's own credential, not the document blob; unaffected (check:openapi passes).
- NOTE 5: base moved since the author's run (361537ee -> 06d33fb4); no overlap, merge clean, results above are on the merge.
- No Major found.

## Readers of blockHeight
(git grep over Blockchain/Dev at the head, all file types except .md; tests read separately: the full suite passes.)

| File | How it reads | Null-safe |
|---|---|---|
| originate/src/repositories/documentRepo.ts:65 | type `blockHeight?: number \| null` | yes |
| originate/src/services/anchorStateSync.ts:192 | `prior?.blockHeight ?? 0` (anchor_failed carry) | yes (but writes 0, in KS-1509) |
| originate/src/routes/verification.ts:346 | `toBlockHeight(chain) ?? blob.blockHeight ?? 0`, persisted | yes, but can re-fabricate 0 (Finding 1) |
| originate/src/routes/verificationV2.ts:148 | same, persisted | yes, same caveat |
| originate/src/routes/verification.ts:585, 1036; verificationV2.ts:240 | `chain.blockNumber` live from anchoring, not the blob | n/a |
| originate/src/routes/documents.ts:883/905/938/1386/1408 | writers of 0 / null (KS-1509) | n/a (writers) |
| originate/src/routes/certifications.ts:468, 1206 | writes `null as any` into the separate certification blob (certificationRepo.ts:33 `number`) | pre-existing, untouched |
| api-gateway/src/routes/verification.ts:634,668-677 | `?? null`, integer > 0 guard, `liveBlockHeight \|\| persisted` | yes (0 and null refused alike) |
| api-gateway/src/routes/verification.ts:330 | `latest.blockNumber \|\| latest.block_number \|\| 0` from anchoring row, not the blob | n/a |
| api-gateway/src/routes/verification.ts:783 | echoes `blockHeight` in response | yes (null already valid, :831) |
| frontend/shared/src/schemas/verify.ts:62 | `z.number().nullable().optional()` | yes |
| frontend/verifier/src/components/ResultPage.tsx:497 | `(a \|\| b \|\| 0).toLocaleString()` | yes |
| frontend/issuer/src/components/DocumentDetail.tsx:120 | `a \|\| b \|\| 0` | yes |
| frontend/issuer CredentialCard.tsx:35,246 / CredentialDetailModal.tsx:102 | `cardanoAnchor.blockHeight.toLocaleString()` from the VC, not the document blob | n/a (separate source; would throw on null if ever fed one) |
| packages/shared vc/types.ts, verifier.ts:220, cardano/transaction.ts, event-indexer.ts | VC / Blockfrost types, other source | n/a |
| sdk/javascript certifications.ts:47 | certification blob type | n/a |
| scripts/openapi-examples/*, docs/openapi yaml | comments / VC schema | n/a |
| mcp-server | no blockHeight reference exists in Blockchain/Dev | n/a |
| SQL / migrations / prisma | no blockHeight JSONB path or column reference | n/a |

No arithmetic, `.toString()`, or `> 0` comparison on the blob's height exists outside the gateway guard (which treats null like 0).

## NOT tested
- Platform S (or any external consumer) reading the persisted `blockchain.blockHeight`: nothing in this repo reads it; I cannot see Platform S, exports, or audit-row consumers outside Blockchain/Dev. All I can establish: no in-repo export, audit-row writer, SQL, or SDK/mcp code reads the field from the blob, and JSONB null is a valid, distinct-from-absent value. Ask the Platform S owner (or check their client for numeric-only parsing of this field) before release; if unanswered, the fallback is omit-the-key, which is a one-line change in toBlockHeight's callers.
- The two tenancy modes on real PG with the originate integration suites (I only checked JSONB semantics on PG15, not the author's full harness).
- Docker, Kintsugi, demo, production, live anchoring returning a null block number end to end.
- Frontend builds and browser rendering of a null height; gateway tests (only gateway tsc).
- Only the originate package's suite was run, not the whole monorepo's.
