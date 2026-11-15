PR 2240: GO WITH NOTES (at head 067274804d31ffb8d1b0288292fbe2d8a5b6b377; tier 1)

# Gate 365, tier 1 (Opus): PR 2240, KS-2103, an anchoring chain reply that is empty, null or has no recognised shape

A GO is a statement about this SHA only. It does not cover a deploy. Findings only: nothing was fixed, posted, mailed, pushed, merged, or written to Linear or GitHub.

## Pins (gh api)
- First pin, 12:49:32Z: head `067274804d31ffb8d1b0288292fbe2d8a5b6b377`, open, merged=false, mergeable=true, 5 commits, 6 files. develop `263a28fcca82`.
- Re-pin before this verdict, 13:03:23Z: the head is unchanged and the PR is still open and unmerged. **develop moved to `659d17071685`**, two commits after `263a28` (KS-716 `systemTest/akto/config/secrets.example.yml`, KS-2138 `Blockchain/Dev/scripts/__tests__/react_router_v7_portals.test.sh`). Neither touches any of the PR's 6 paths or anything under `services/anchoring`.
- The PR's base is `bbb75755064e`, the PR 2081 squash. Its `services/anchoring` tree is `a54221c9613b`. It is identical at `bbb75755064e` and `263a28fcca82` (both read with `rev-parse`), so suite A below is the real base's.

## How it was measured
- Own clone: `scratch/repo`, a `--no-hardlinks` copy of the seat's `s-aa7-base` object store, read only. The commits are identified by SHA. Detached at the head. `npm ci` (1794 packages). `@secuura/shared` built (`ignore-scripts`). TMPDIR `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/g365t`.
- Every vitest, tsc or eslint run started with load1 at or below 8 (`scratch/tools/waitload.sh`; readings in `scratch/out/*.load`). Load was 9.7-12.3 at 12:49-12:53Z, and I waited.
- node v26.8.1, vitest 4.1.12, macOS arm64.

## Answers to the commission

**(1) Card 1110, cell by cell, with the REAL blockfrost-js.** My own file is `scratch/repo/Blockchain/Dev/services/anchoring/src/__tests__/g365-real-client-shapes.test.ts`. It is not in the PR.
- What runs: the real `BlockFrostAPI` 6.1.1, with only its constructor redirected through `customBackend` to a listener on 127.0.0.1. It runs no retries, uses no key and makes no external network call. Its replies go through the real `getTransaction` and the real `waitForConfirmation`.
- Results at the head, 4 of 4 green:
  - **These all THROW a plain Error:** an empty 200, a 204, `null`, `{}`, `[]`, `"x"`, `0`, `{"block":""}`, `{"block":7}`, and a `{marker, hash}` body.
  - Each message names only the shape class. An example is "...returned an empty body (KS-2103)" for both the empty 200 and the 204, which confirms gate 248 F1's `''`. No message contains the body marker, the tx hash or the block hash.
  - A 404 gives `null`. A real `tx_content`, including `valid_contract:false`, is returned as the same object. With no client, the result is `undefined` and the listener receives 0 requests, so 2081's tri-state is untouched. A 502 throws with `status_code` 502.
- `undefined` from a configured client cannot come from real got/blockfrost-js. The PR's E3b pins it with a spy.
- The same file at develop `263a28`: 3 RED by AssertionError (0 TypeError). The answers cell stays green.

**(2) The harm.**
- PR cells E1 and E2 (production schedule, fake timers): confirmed false, polled 0, errored 30, `lastAnsweredElapsedMs` undefined, `definitelyAbsent` false.
- E5 drives guard 3 after a node 400: 0 retries, 1 submit, no `failed` write. The control E5c, on a 404 window, does schedule the retry.
- E7 is a mixed window: polled 2, `lastAnswered*` equals the second 404's, and the window is not absent.
- My real-client windows agree:
  - 30 empty 200s and 30 204s: polled 0, errored 30, not absent.
  - `{}`: confirmed false, no blockHash.
  - 3 404s then `null` bodies: polled 3, `lastAnsweredAttempt` 3.
- All 14 PR cells are green at the head. On develop with the PR's file copied in, 10 are RED, all by AssertionError, and the 4 controls are green.

**(3) The other callers fail SAFE.**
- `settleExpiredSpenders` (`walletSpend.ts:140-146`) catches the throw and settles nothing.
- `anchorSubmission.ts:556` returns `'rest'` when `txInfo` throws.
- E6b and E6c pin both, against literal copies of the production closures, with a literal-presence guard on each.
- Two more consumers, by read, are also safer now (neither is named in the PR):
  - The reconciler's `checkTx` (`index.ts:2376`; `reconciler.ts:343` treats a pass as answered only when `polled > 0`). A malformed reply no longer counts toward the give-up failure.
  - The batch path (`index.ts:2187`). `{}` no longer writes `confirmed` with an undefined blockHash.

**(4) Nothing else moved.**
- `confirmation.ts` changes in comments only. With comments stripped, the diff is two whitespace-only lines.
- `anchorSubmission.ts` is byte-identical (`git diff --quiet` rc 0; control `provider.ts` rc 1).
- The ks671 diff is exactly the two fixture lines (`{ block_height: 1 }` to `{ block: 'b'.repeat(64), block_height: 1 }`), each with a `// KS-2103:` comment. No assertion changed.
- 2081's `ks1171-8k-no-client-is-not-an-answer.test.ts`: 28 of 28 green by name. ks671: 23 of 23. ks2103: 14 of 14.

**(5) The error message echoes no body and no hash.**
- `replyShape` returns only a class word.
- PR cell D3 and my real-client cell assert it, and my mutants g5 (echo the JSON body) and g6 (echo the txHash) turned both red.
- Gap: see N1.

**(6) What this admits.** No real Blockfrost success reply is refused, by read:
- blockfrost-js 6.1.1 `txs()` returns `res.body`, typed `components['schemas']['tx_content']`.
- @blockfrost/openapi 0.1.86 declares `tx_content.block: string` as non-optional.
- **The anchoring image installs from `services/anchoring/package-lock.json`, which pins blockfrost-js 6.2.0 / openapi 0.1.92**, not the 6.1.1 the tests resolve from the hoisted workspace tree. I `npm pack`ed both versions and read them. `txs()` is identical, and `tx_content.block: string` is still required (N3).
- Blockfrost's `/txs/{hash}` answers 404 until the transaction is in a block, so a found tx always carries `block`.
- Not measured against the live service.

**(7) /health still reads an empty 2xx as reachable.** It is acceptable as a separate ticket, at Low-Medium severity (N2).
- The proxy records success when `txs` resolves, before `getTransaction` judges the shape.
- It misleads monitoring only. While every poll logs `error: ...`, `/health` can say `ok`. It has no fee path and no row write.
- It should be filed, not rolled into this PR. Card 1110's text governs what counts as an answer to the poller, not the health signal.

## Own mutants, one per changed line class
Results are in `scratch/out/mutants.tsv`. Every restore was sha256-equal, and the tree was clean after the run.

| Mutant | Planted change | Result |
|---|---|---|
| g1 | drop `reply !== null` | **survives (equivalent)**: `null.block` throws a TypeError, so `null` is still errored. See N4. |
| g2 | `typeof block === 'string'` becomes `block !== undefined` | red: mine, E3b, E6a (AssertionError) |
| g3 | drop `block !== ''` | red: mine, E3b, E6a |
| g4 | return `undefined` instead of throwing | red: 11 cells, including E1, E2, E3a, E6b, E6c, E7, D3 and my mixed window |
| g5 | echo `JSON.stringify(reply)` in the message | red: mine, D3 |
| g6 | echo `txHash` in the message | red: mine, D3 |
| g7 | revert one ks671 fixture line | ks671 staleness cell red. The throw propagates, so it is a TypeError-class red, not an assertion. |
| g8 | echo a string body in `replyShape` | **survives**. See N1. |

## Suites, tsc, eslint, merge
- **Whole anchoring vitest:**
  - Head: 65 files, 885 tests, 884 passed.
  - develop `263a28`: 64 files, 871 tests, 870 passed.
  - The single red on both sides is `threadTokenMint` round-trip, "Could not serialize the data: Error: Unsupported type" (gate 248 F2). It is pre-existing and still that and only that.
  - The +14 is exactly the new file. Every named suite (ks1171*, ks726*, ks1384-f0, ks1868*, mock-provider, ks2196, ks671) is green, by elimination: one failing file of 65.
- **tsc** over src and tests (config at `g365t/tsconfig.g365.json`): 1 error, the pre-existing TS6133 at `ks1868-anchoring-message-coercion-unreadable-throw.test.ts:46`, and 0 in changed files. A planted TS2322 fired.
- **eslint** (repo `eslint.config.mjs` through the API, cwd `Blockchain/Dev`) on the 4 changed .ts files: 0 errors, 0 warnings, 0 ignored. A planted unused const fired.
  - Note: the CLI with `--config` from outside cwd silently ignores or misparses these files. That is a trap for the next gate, not a defect of the PR.
- **docs-fragments check:** OK, with two ADVISORYs. I did not re-measure whether they are pre-existing. I read the fragments: they contain no secret and no hash, and their figures match the evidence.
- **merge-tree** with develop `263a28`: clean in both orders, the same tree `85282a39`, and the anchoring subtree equals the head's. A planted same-line `provider.ts` edit on develop conflicts (rc 1).
  - develop `659d17` was not in my clone's objects. Its two commits touch 2 files disjoint from the PR's 6, so a conflict is impossible by path. This is not measured by merge-tree. The merge seat should re-run it at merge time.

## Notes (none blocks)
- **N1, Low.** D3's "never the body" is pinned for object bodies only. No cell feeds a non-empty string body and checks the message, so mutant g8 survives. The current code does not echo it (`a string`). Owner: one cell, in a follow-up or the merge seat's choice.
- **N2, Low-Medium, separate ticket.** `/health` reachability reads an empty 2xx as `ok` (answer 7). The builder named it. Wednesday routes it.
- **N3, Info.** The tests resolve blockfrost-js 6.1.1 (hoisted). The image ships 6.2.0 from the service lock. I read 6.2.0's `txs` and types and found them identical in the respects that matter. No test ran on 6.2.0.
- **N4, Info.** `reply !== null` is defensive and equivalent (g1). Without it, `null` would still throw, with TypeError text instead of "null". This is harmless.
- **N5, Info.** 2081's cell 8k-9 title now describes the old mechanism. Its assertion is still green, and the builder named it.
- **N6, Info.** The PR text lists three callers. Two more consumers of the poller's result (the reconciler and the batch confirm) are also made safer. The PR does not say so.

## NOT covered by this gate
- A real Blockfrost, node or unreachable chain. The live service's reply shapes.
- An image built from the service lock (6.2.0).
- Guard 3 in a built container. E5 drives it in process.
- The four platform suites.
- How often a provider sends an empty 2xx.
- A merge-tree execution on develop `659d17`.
- Re-running the builder's m1-m6 (I ran my own g1-g8 instead).
- The docs-fragments planted control.

## Deploy (card 1107)
In my judgement this fix meets card 1107's precondition. A configured client's empty, null or shapeless 2xx can no longer read ABSENT, cannot make guard 3 pay a second fee, and cannot confirm without a block hash. This holds at the head, by red-to-green cells, real-client cells and mutants.

Anchoring may deploy on this fix once it is merged and Kam gives his word. The deploy is his and Wednesday's, not this gate's. Two things Kam should weigh, neither caused by this PR:
1. The pre-existing `threadTokenMint` red (gate 248 F2, a plutus Constr split that may affect the real thread-token mint, before signing, so no fee).
2. Nothing here was measured against the live Blockfrost.
