VERDICT #1583 (KS-1485 item 2) head 16fc1d201fc03484921911cc9ca42c474ffba7d5: GO WITH NOTE (correct and complete for authoritativeTxHash; sibling regexes anchorHonesty.ts:28 / honestAnchor.ts:17 still miss mock_batch_tx_, outside this PR)
VERDICT #1581 (KS-1387) head 6b4bcaec11fa4aea156a11bbaa23b56b09126b63: GO (TS2742 reproduced without Docker under differing nested type versions: tip fails, head clean; one low test-brittleness note)
SHA256/16: 712c5587b5a8d103

Gate H2, tier 2 through-code, round 1 of 2. Not security-shaped: both changes are non-behavioural for any real hash (a type annotation; a stricter placeholder rejection). Live develop re-read by ls-remote and fetch: 385fc288fae831f2ca15b9d091c844f33285b784. Heads re-read: #1583 16fc1d20..., #1581 6b4bcaec... (both match the brief). Everything below was run by me in my own clone, h2/repo (clone --shared, detached at develop), with the repo's own jest and tsc by path.

## FOUND

1. **#1583 diff is exactly as named.** Two files: anchorStateSync.ts (+2/-2: the doc comment line 75 and the condition line 81) and the new ks1485 suite (61 lines). Nothing else. merge-base is the live tip.
2. **Placeholder prefixes, #1583 (gate step 2).** Every writer of a hash that can reach `authoritativeTxHash`, by grep at the live tip:
   - `tx_` : anchoring/src/index.ts:1219 (`tx_<64hex>`), originate routes/anchors.ts:72 (`tx_<row.id>` fallback), `tx_sim_` at routes/anchors.ts:212 and routes/documents.ts:922, deployment/cardano/scripts/test-contracts.ts:75 (`tx_test_`). All are covered by `startsWith('tx_')`.
   - `mock_tx_` : anchoring/src/index.ts:1794, timestamping/src/index.ts:492 and 701, transfer/src/index.ts:828, packages/shared/src/prism/mock-client.ts:147, 258, 284. Covered.
   - `mock_batch_tx_` : anchoring/src/index.ts:1986, the ONLY writer. Covered by the new clause (line 81 at head).
   - I found no other txHash / transactionHash / transactionId writer with a placeholder prefix (greps for `sim_`, `fake_`, `dev_`, `demo_`, `stub_`, `simulated_` etc. returned nothing). Non-hash mocks (`mock_block_`, `mock_jwt_`, `mock_signature_`, `mock_app_`, `mock_req_`) do not feed this function. **So `authoritativeTxHash` at the head rejects every placeholder prefix any writer produces. No accepted-writer finding against the PR.**
3. **ADJACENT, not in the PR's file set (note, not a defect of #1583):** three sibling placeholder tests still do NOT match `mock_batch_tx_`, because they use `/^(tx_sim_|mock_tx_|tx_)/`: originate `services/anchorHonesty.ts:28` (used at 36, 70, 97), anchoring `honestAnchor.ts:17` (used at 33; also `anchorStatusUpdate.ts:89`, `index.ts:1464`), and the comment at anchoring `cardano/index.ts:218`. A `mock_batch_tx_...` hash is therefore still treated as non-fabricated by those readers (isSimulatedAnchor / honestTxView / fabricated-hash checks). That is the same bug class the PR closes in one reader. The PR title says "item 2", so this may be item 1 or a later item of KS-1485; I could not tell from the brief. Severity LOW to MEDIUM (honest-labelling gap, dev/test mock path only, production has no mock batch path). Wednesday should confirm it is tracked.
4. **#1581 diff is exactly as named.** governance.ts line 19 `const router: Router = Router();` (+1/-1) and the new ks1387 suite (34 lines). Nothing else.
5. **TS2742 reproduction (gate step 3): REPRODUCED under a constructed layout, NOT reproduced under the Dockerfile's literal layout.**
   - Dockerfile layout built faithfully without Docker (h2/dsim): /shared = packages/shared with its own `npm ci` and build, /app = services/governance with its own `npm ci` from its own lockfile, `node_modules/@secuura/shared` symlinked to /shared. Both lockfiles pin `@types/express-serve-static-core` 4.19.9, so the two nested copies are the SAME version. Governance `tsc` at the tip: exit 0; at the head: exit 0. TS2742 does not reproduce here, which matches the author.
   - Variant: same layout, but /app's copy pinned to 4.17.43 so the two nested copies DIFFER (contrived by me). Tip: `routes/governance.ts(19,7): error TS2742: The inferred type of 'router' cannot be named without a reference to '@secuura/shared/node_modules/@types/express-serve-static-core'. This is likely not portable. A type annotation is necessary.` Head: exit 0, clean. So the annotation does cure the exact TS2742 the ticket names whenever two differing nested copies exist, and the local build at the tip can not show it.
   - Caveat: with today's lockfiles the clean Docker layout does not hit it. The ticket's failing image probably had a different or older resolved version at the time. The fix is correct and harmless either way; I cannot say what in the original failure differed.
6. **Test brittleness (#1581), LOW.** `ks1387...test.ts` regex `/=\s*Router\(\);\s*$/` is anchored to end of line: appending a trailing comment on the declaration line (`const router: Router = Router(); // x`) turns the CONTROL cell red. A comment on its own line above is fine. It pins source text, not the compiler outcome; my reproduction in finding 5 is the compiler-level evidence it does not give. It would accept `const router: Router` from a different `Router` import only if the import line check passed; the import check is present (exact `import { Router, ... } from 'express'`).
7. **Merge predictions (gate step 5), all with `git merge-tree --write-tree` on live develop.**
   - File overlap between all six PR pairs among #1581-#1584: 0. Each PR touches exactly 2 files.
   - #1581 alone: clean, tree f33b620c79e8. #1583 alone: clean, tree ca1d381e06ef.
   - #1581 then #1583 and #1583 then #1581: both clean, identical tree 6cb736a1575c68bb484748256042e489f61a35d5.
   - All four (#1581-#1584) in five different orders: all clean, all tree **47a455d77decfa848276c374aba96d7f160606bb**. R's prediction (47a455d77dec) is CONFIRMED on the 12-character prefix.
   - Planted conflicting control (my own commit editing the same line of governance.ts, then of anchorStateSync.ts, merged against #1581 / #1583): both report `CONFLICT (content)`, rc=1. So the detector can see a conflict, and the zero-conflict results above are real.

## TESTED (all at live develop 385fc288, results from my own runs)

| Check | Result |
|---|---|
| #1583 red-first (tip product + PR suite) | 3 failed / 4 passed (7) : the three RED cells |
| #1583 green (head product + PR suite) | 7 / 7 |
| Mutant: remove the `mock_batch_tx_` clause (hunk revert, comment kept) | RED 3 failed |
| Mutant: typo the prefix `mock_batch_t_` | RED 3 failed |
| Control: comment-only change to the doc comment | still 7 / 7 (stays green) |
| Full originate at head | 113 suites, 1400 / 1400 (author said 1400: matches) |
| Neighbours at tip product: ks535, ks1158-r1, ks587 plus ks1485 pattern | 4 suites, 44 / 44 |
| tsc originate at head (`tsc -p ... --noEmit`) | exit 0 |
| #1581 red-first (tip product + PR suite) | 1 failed (the RED cell) / 2 passed (3) |
| #1581 green (head product) | 3 / 3 |
| Mutant: drop the annotation | RED 1 failed |
| Mutant: `Router` -> `any` | RED 1 failed (the test rejects the wrong type, good) |
| Control: trailing comment on the declaration line | NOT stable: CONTROL cell goes red (finding 6) |
| Control: trailing comment on tip product | red as expected (RED cell + CONTROL cell) |
| Full governance at head | 5 suites, 119 / 119 (author said 119: matches); tip baseline 4 suites, 116 |
| tsc governance at tip and at head (workspace install, hoisted types) | both exit 0 (so local tsc is blind to the ticket, finding 5) |
| TS2742 Docker-layout simulation | see finding 5 |
| Merge predictions | see finding 7 |

## HOW

`npm ci --ignore-scripts` then `npm run build -w packages/shared` in h2/repo/Blockchain/Dev; jest via `node_modules/.bin/jest -c services/<svc>/jest.config.js --rootDir services/<svc>`; tsc via `node_modules/.bin/tsc -p`. Scripts in h2/: setup.sh, install.sh, dockersim.sh, dsimbuild.sh, variant.sh, variant2.sh, suites.sh (logs suites_1583.log), gov.sh (gov.log), merge.sh, merge_planted.sh (merge.log). Mutants were applied by sed on files inside h2/repo only, never in the !CODING checkout. The two untracked-file warnings in git status inside h2/repo (.bak files) are my mutant backups.

## NOT tested

- Real Docker image build (Docker not used, by rule). The dsim layout is my reconstruction of the Dockerfile's install order (stage 0 shared `npm ci` + build, stage 1 `npm ci`, hand symlink); it omits the `npm prune --omit=dev`, which runs after the build and cannot affect it.
- The exact failing install that the ticket saw: not constructible from the repo today (identical pinned versions). I could construct TS2742 only with deliberately differing nested versions.
- Whether `mock_batch_tx_` hashes ever reach the sibling regexes at runtime (finding 3): I checked they are untouched by either PR and do not match; I did not run the anchoring service or its DB path.
- Integration tests (DB-backed, excluded by the default jest config) and any other service's suites.
- GitHub PR metadata, CI status and comments (not read; read-only rule and no writes).

## Severities

- LOW to MEDIUM, note: sibling placeholder regexes miss `mock_batch_tx_` at Blockchain/Dev/services/originate/src/services/anchorHonesty.ts:28 and Blockchain/Dev/services/anchoring/src/honestAnchor.ts:17 (comment at anchoring/src/cardano/index.ts:218). Outside both PRs.
- LOW: ks1387 suite trailing-comment brittleness, Blockchain/Dev/services/governance/src/__tests__/ks1387-governance-router-has-an-explicit-type.test.ts (the `=\s*Router\(\);\s*$` match).
- INFO: #1581's own symptom needs differing nested type versions to reproduce; the annotation fixes it when it does.

Round 1 of 2.
WALL-CLOCK: 6
