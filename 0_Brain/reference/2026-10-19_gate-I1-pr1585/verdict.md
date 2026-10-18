GO WITH NOTE — PR #1585 (KS-1626) head 664d3fd2494b15cde3c34175c0c979dbee0edc9a onto develop 5d1be7b06279950e3bfe176c237e5d640eb04581
Headline: all six regex lines are the only product change; the census finds no reader left that takes mock_batch_tx_ for a real hash; red-first, 6/6 mutants and suites reproduce; merge is a clean fast-forward; four non-blocking notes, all pre-existing or comment-only.
b2c462b2c2a0a8d3

Gate I1, tier 1 FULL, round 1 of 2. Independent QA (Opus), findings only. Live refs re-read at the start and the end with ls-remote: develop 5d1be7b06, PR head 664d3fd24 (unchanged).
Scratch: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/i1/ (scripts *.sh, logs/, tests/ = gate-owned behaviour cells). All paths below are under Blockchain/Dev/.

## FOUND

Blocking: none.

- **N1 LOW (comment, missed eighth enumeration)** services/originate/src/routes/anchors.ts:62: `// KS-587: a placeholder hash (\`tx_sim_\`/\`mock_tx_\`/\`tx_…\`)`. This is the same three-prefix list as the seven comments the PR edited. It is not the measurement record the PR deliberately left (api-gateway routes/verification.ts:679), and the PR does not name it. Comment only: there is no behaviour effect, because line 66 re-exports the fixed FABRICATED_TX_PREFIX. The other two-prefix mentions (anchorSubmission.ts:97, index.ts:1563, reconciler.ts:20, originate.openapi.ts:399/501, originate routes/verification.ts:99/188, anchorStateSync.ts:199) give examples rather than full lists, and I count them as fine.
- **N2 INFO (pre-existing, out of scope; answers gate Q3)** Two placeholders cannot be caught by ANY prefix regex, because they are bare 64-hex: services/anchoring/src/mocks/mockProvider.ts:57-72 (demo-mode MockAnchoringProvider; already documented as "KS-587's to fix" at services/anchoring/src/cardano/index.ts:215-235) and services/demo-service/src/seed/utils/cardano.ts:18 (`mockTxHash`, seeded demo data). No prefixed placeholder writer escapes the new regex.
- **N3 INFO (pre-existing, by design)** api-gateway routes/verification.ts persisted read: once fixed, the claim is honest (`verified:false`, `verificationConfidence:'off-chain-only'`, `anchored:false`), but `blockchain.txHash` still echoes the raw `mock_batch_tx_…` (cells B-G2 and B-G3). This is as documented at :681-685 ("echoed values NOT rewritten here") and is identical for tx_sim_. In the real pipeline both upstreams already null it first: originate GET /api/documents/:id composes through composeHonestBlockchainBlob (documents.ts:1160), and anchoring by-document goes through honestTxView.
- **N4 INFO (drift risk, the root of this bug)** The same literal lives in six places across three services. Inside one service, services/anchoring/src/anchorReadback.ts:115 inlines its own copy instead of importing FABRICATED_TX_PREFIX (honestAnchor.ts:17). The mutants confirm the two are independent: M1 does not touch A2, and M2 does not touch A1. A follow-up could import the constant there.
- **Pre-existing, prefix-agnostic, not in this PR's sites (LOW, for the backlog)** services/originate/src/routes/documents.ts:1593-1596: the deprecated `POST /api/documents/:id/verify` (sunset 2026-08-14, still routed) spreads `document.blockchain` raw with `anchored: status !== 'anchor_failed'` and does not compose it honestly. A stored raw placeholder of ANY prefix would be echoed as anchored. It does not affect mock_batch_tx_ specifically, because the originate writers (simulatedFieldsFromAnchor; anchorStateSync.ts:81 authoritativeTxHash) do not store a raw batch hash.
- **Author-claim correction (no defect)** The claim that "each product file differs from the tip only on its regex line" is not exact. Four of the five product files also carry their named comment edit: honestAnchor.ts:5, anchorReadback.ts:110, anchorHonesty.ts:6 and originate routes/verification.ts:42. Every one of those is comment-only. The commit message itself describes the change accurately.

### 1. Diff by hunk (head vs develop = merge-base)
11 files, +368/-13, one commit 664d3fd24. These are exactly the 11 named files: 8 product/comment files and 3 new tests. Product hunks:
- honestAnchor.ts: :5 comment + :17 regex.
- anchorReadback.ts: :110 comment + :115 regex.
- originate services/anchorHonesty.ts: :6 comment + :28 regex.
- originate routes/verification.ts: :42 comment + :52 regex.
- api-gateway routes/verification.ts: :655 + :692 regex only.

Comment-only files: anchoring.openapi.ts:72, cardano/index.ts:218 (inside a `//` block), verifyAnchorStatus.ts:13 (inside a `/** */`). That is seven comment edits in total. Every hunk changes 1 line for 1 line, with no blank-line churn. The comment at api-gateway :679 is untouched, as the PR says.

### 2. Census: every placeholder-deciding reader at the head (grep of services/, packages/, scripts/, frontend/, deployment/, sdk)
Prefix-negative readers. All of them now include mock_batch_tx_:
- anchoring honestAnchor.ts:17 FABRICATED_TX_PREFIX, used by honestAnchor.ts:33 (honestTxView, which serves GET /api/anchors/:id at index.ts:886 and by-document at index.ts:1622), index.ts:1464 (upsert simulated column) and anchorStatusUpdate.ts:89 (status-update simulated column).
- anchoring anchorReadback.ts:115 (GET /api/anchors/verify/:hash via index.ts:603).
- originate services/anchorHonesty.ts:28, used by :36 isSimulatedAnchor, :70 simulatedFieldsFromAnchor, :97 composeHonestBlockchainBlob. These are re-exported at routes/anchors.ts:66 and used at anchors.ts:107/224, documents.ts:964/1160/1445 and anchorStateSync.ts:298/418.
- originate routes/verification.ts:52 FABRICATED_TXHASH_RE, used at :58 presentBlockchainHonestly, which feeds every v1/v2 verify builder (:689, :775, :978, :1075, :1231; verificationV2.ts:193/232).
- api-gateway routes/verification.ts:655 (live) and :692 (persisted).
- originate services/anchorStateSync.ts:81 authoritativeTxHash startsWith list. This one already included mock_batch_tx_ before the PR (KS-1485, 4a547a119).

Positive real-hash readers. These already reject mock_batch_tx_, because they require /^[0-9a-f]{64}$/i: anchoring anchorSubmission.ts:98, index.ts:1568 (REAL_TX_64HEX_RETRY), reconciler.ts:52/83; originate routes/verification.ts:165 REAL_TXHASH_RE (rowHasRealTx :177, :407, :427; verificationV2.ts:131/136/395); frontend/issuer/src/utils/cardano.ts:135.

`simulated`-flag-only readers: anchoring reconciler.ts:75 (`AND simulated = FALSE`, also gated by REAL_TX_64HEX), originate verificationV2.ts:129/393 (then REAL_TXHASH_RE), and api-gateway :376-388 tier-2 (carries anchoring's flag, then the :692 guard).

Result: no reader at the head treats `mock_batch_tx_<hex>` as a real on-chain hash. No other `startsWith('mock_'…)`, `includes`, or `/^mock/` classifier exists. The only `mock_signature_` checks (api-gateway index.ts:871, originate documents.ts:1267) concern signatures, not tx hashes.

### 3. Writers
`mock_batch_tx_` has exactly one writer: services/anchoring/src/index.ts:1986. It is non-production only, guarded by the NODE_ENV check at :1970. It writes through dbUpdateAnchorStatus(submitted, transactionHash), which now records simulated=true (cell B-A4), and then confirms the row at :2001-2008 without touching simulated.

Other placeholder writers, all matched by the new regex:
- `tx_`: anchoring index.ts:1219, originate anchors.ts:72 fallback, deployment/cardano/scripts/test-contracts.ts:75 (`tx_test_`).
- `mock_tx_`: anchoring index.ts:1794, timestamping index.ts:492/701, transfer index.ts:828, packages/shared/src/prism/mock-client.ts:147/258/284.
- `tx_sim_`: originate anchors.ts:212, documents.ts:922.

Not prefix-detectable: see N2. `mock_block_` (index.ts:1805/1998) is a blockHash, not a tx hash.

## TESTED / HOW

### 4. Behaviour
I wrote three gate-owned files: tests/anchoring-gatei1-behaviour.test.ts, originate-gatei1-behaviour.test.ts and apigw-gatei1-behaviour.test.ts. They were copied into a scratch worktree and use the exact batch shape: `mock_batch_tx_`+64 hex, status confirmed, simulated false, block_number null for anchoring and 4242 for the verify paths. Each one ran BEFORE (product files taken from develop) and AFTER (head):

| Cell | Path driven | Before (develop) | After (head) |
|---|---|---|---|
| B-A1 | buildVerifyResponse db (GET /api/anchors/verify/:hash) | txHash=mock_batch_tx_…, cardanoScanUrl=https://preview.cardanoscan.io/transaction/mock_batch_tx_… | txHash null, simulated true, simulatedTxRef set, url null |
| B-A2 | same, chain-sourced payload | txHash + fabricated explorer URL | null / simulated / null |
| B-A3 | honestTxView (GET /api/anchors/:id, /document/:id) | {txHash: mock_batch_tx_…, simulated:false} | {txHash:null, simulated:true, simulatedTxRef} |
| B-A4 | buildAnchorStatusUpdate (batch mock submitted write) | simulated param false | true |
| B-O1 | originate real route POST /api/verification/verify | blockchain.txHash=mock_batch_tx_…, anchored true, checks.isAnchored true | simulated true, txHash null, anchored false, isAnchored false |
| B-O2 | simulatedFieldsFromAnchor / composeHonestBlockchainBlob | {} / raw hash | simulated + ref / txHash null |
| B-G1 | api-gateway real router, live chain-scan reply | verified true, on-chain | verified false, off-chain-only |
| B-G2 | api-gateway tier-1 persisted blob | verified true, on-chain | off-chain-only (txHash echoed, N3) |
| B-G3 | api-gateway tier-2 anchor-store row | verified true, on-chain | off-chain-only |

The controls B-AC1, B-OC1 and B-GC1 (a real 64-hex hash) stay real/on-chain both before and after.

### 5. Red-first, mutants, controls, suites, tsc
- **Red-first**: the PR's ks1626 cells against develop product files go red on exactly A1, A2 / O1, O2 / G1, G2. The controls stay green (3 pass, 2 fail per service). At the head all 5/5 are green in each service. This matches the author.
- **Mutants**: each one drops `mock_batch_tx_|` from a single line, with numstat 1/1, and is restored by checkout afterwards. All six are killed:
  - M1 honestAnchor.ts:17: killed by RED KS-1626 A1 (also B-A3, B-A4).
  - M2 anchorReadback.ts:115: killed by A2 (also B-A1, B-A2).
  - M3 anchorHonesty.ts:28: killed by O1 (also B-O2).
  - M4 originate verification.ts:52: killed by O2 (also B-O1).
  - M5 api-gateway :655: killed by G1 (also B-G1).
  - M6 api-gateway :692: killed by G2 (also B-G2, B-G3).
- **Comment-only control**: I put all seven comment lines back to their develop text and kept the six regex lines. The diff against develop then showed exactly the six regex lines, and all ks1626 and behaviour cells stayed green (anchoring 10/10, originate 8/8, api-gateway 9/9). The comments carry no behaviour.
- **Full owning suites** (`npm test` per service, after `npm ci` and `npm run build -w packages/shared` in Blockchain/Dev):
  - anchoring: develop 370/371 → head 375/376.
  - originate: develop 1400/1400 (113 suites) → head 1405/1405 (114).
  - api-gateway: develop 1186/1186 (123 files) → head 1191/1191 (124).
  - Each gains exactly +5. The one red, identical on both sides, is threadTokenMint.test.ts "parameterises mint + spend with a deterministic per-seed policyId", the KS-562 root-workspace install split. I reported it and did not chase it.
  - The author's counts reproduce.
- **tsc** (Dev/node_modules/.bin/tsc -p services/<svc>/tsconfig.json --noEmit): 0 errors for anchoring, originate and api-gateway at both develop and head, and also at the head with the gate's test files present.

### 6. Merge prediction
- Live develop is 5d1be7b06 and is the merge-base. Develop has 0 commits since the base, and the overlap set is empty.
- `git merge-tree --write-tree develop pr` returns rc 0, and its tree f8cd19864 equals the PR's tree, so the merge is a clean fast-forward.
- Planted control: a develop-side commit that rewrites honestAnchor.ts:17 differently. Merged with the PR, it gives rc 1 with "CONFLICT (content): Merge conflict in …/honestAnchor.ts", so the conflict probe does detect conflicts.

## NOT tested
- No booted services or live HTTP against a real Postgres/anchoring stack (Docker is forbidden). anchoring index.ts calls app.listen on import, so its GET /api/anchors/:id, /document/:id and /verify/:hash handlers were driven through the pure functions they call (honestTxView, buildVerifyResponse, buildAnchorStatusUpdate), not through Express. The originate and api-gateway verify routes were driven in-process through their real routers.
- I did not run the batch mock's setTimeout timeline end to end (index.ts:1984-2010). Its write was checked through buildAnchorStatusUpdate only.
- I did not drive the deprecated originate POST /api/documents/:id/verify; the finding about it comes from reading the code.
- I did not check other open PRs for overlap (gh not used); the overlap check covers live develop only.
- Frontend/mobile/sdk display code was grep-censused only. Nothing there classifies placeholders apart from the 64-hex positive check at frontend/issuer/src/utils/cardano.ts:135.
- Integration suites (*.integration.test.ts) were not run, since they are excluded from the owning `npm test` configs.

## Severities
- BLOCKER/HIGH/MEDIUM: none.
- LOW: N1 services/originate/src/routes/anchors.ts:62 (stale three-prefix comment). Pre-existing documents.ts:1593-1596 (deprecated verify spreads the blob raw; prefix-agnostic).
- INFO: N2 anchoring/src/mocks/mockProvider.ts:57-72 and demo-service/src/seed/utils/cardano.ts:18 (bare-hex placeholders). N3 api-gateway routes/verification.ts:681-685/:692 (echoed txHash, by design). N4 anchoring/src/anchorReadback.ts:115 (duplicate inline regex).

WALL-CLOCK: 11
