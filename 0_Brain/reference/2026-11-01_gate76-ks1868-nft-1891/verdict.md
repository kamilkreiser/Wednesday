# QA Gate 76 verdict: Secuura/Distributed_Secuura PR 1891 (KS-1868, nft-certificate fetchProtocolParams O41-P1), tier 2

## BLUF

**GO WITH NOTES.** I would keep tier 2. The product change only turns a read that could throw out of a catch into the same log-and-`return null` path an ordinary Error already takes. The sole caller that matters, `ensureFreshParams()`, never treats `null` as "fresh". The notes are one untested branch (G76-F1) and one pre-existing staleness property that the change now also reaches (G76-F2).

## Heads

- PR head: `968757f16f8d3c4ee60572c0e4f53cbd777a41e7`. This equals the expected head. Source: logs/head_start.log, logs/head_end.log (ls-remote at the end).
- develop: `85c56a3d1eb92c8399dcfd3d6ee2a717cf356428`, unmoved at the end (logs/head_end.log). The PR is one commit on develop's tip.
- The clone was clean at the end (no `git status` lines in logs/head_end.log).
- The diff is 4 files, +114/-1 (logs/pr.diff). The product file is provider.ts, +7/-1.

## FINDINGS

- **G76-F1 LOW** The inner fallback path for non-Error thrown values is untested. Mutant M10 (non-Error branch replaced with the constant `'x'`) survived: rc=0, 3 of 3 passed (logs/mut_M10.log). The test throws only an Error, a revoked Proxy and a throwing-getter Error. A plain string, or a null-prototype object (where `String()` throws a TypeError), is never thrown. My probe shows both behave as the code intends (logs/probe.log). Location: provider.ts:68 and the test file.
- **G76-F2 LOW (pre-existing, now also reachable)** `ensureFreshParams()` falls back to `cachedParams` with no age cap. `mintTransaction.ts:115` sets the TTL to `params.slot + 7200`, so cached params carry a stale slot. During a long Blockfrost outage a mint would be built with an old TTL, and the chain would reject it. That is a failed mint, not a wrong one. An ordinary Error already took this path; the PR extends it to unreadable values. It is not introduced by this PR and does not block it.
- **G76-F3 INFO** The PR body and fragment say `ensureFreshParams` was "read, not exercised", and that is right. No test covers the `index.ts` caller. See section 1.
- **G76-F4 INFO** `docs-fragments.mjs check` prints two ADVISORY lines (flow line 6249, cheat line 6235) on the head. Gate 75 saw the same two lines on a different head. I did not run the check at base (logs/frag_check.log).
- **G76-F5 INFO** My mutants M7 and M9 are the same edit (mine). That leaves 11 distinct mutants.

## 1. Product hunk

Changes (provider.ts:65-73, log: logs/pr.diff):
- The catch used to evaluate `err instanceof Error ? err.message : String(err)` inline, as an argument to `logger.error`.
- It now evaluates the same expression in an inner `try`. On failure `reason` becomes `'unreadable thrown value'`.

Does NOT change:
- The log message text `'Failed to fetch protocol parameters'` (provider.ts:72).
- The log key `error`.
- `return null` (provider.ts:73).

Unreadable values, from logs/probe.log:

| Value | Old read | New read |
|---|---|---|
| revoked Proxy | THROWS TypeError | `unreadable thrown value` |
| Error with throwing `.message` getter | THROWS Error | `unreadable thrown value` |
| null-prototype object | THROWS TypeError | `unreadable thrown value` |
| string, undefined, symbol | readable | unchanged |

Callers, from `git grep` (logs/callers.log); there are no callers outside nft-certificate except anchoring's own separate copy and tests:
- `cardano/index.ts:50`: `cachedParams = await fetchProtocolParams();` in `initCardanoNFT`, wrapped by `try` at :40 and `catch` at :58. `:51` is `if (!cachedParams) return false;`. A null result leaves mint "not ready". The old throw was caught by the catch, which also returned false. Behaviour is identical, as the author says.
- `cardano/index.ts:77`: `const fresh = await fetchProtocolParams();` in `ensureFreshParams()` (:75-84). It has no try/catch, so the author's claim is verified. Before, an unreadable throw rejected `ensureFreshParams`, so `mintNFTOnChain` (:114) rejected and no mint happened. Now `fresh` is null, so `if (fresh)` at :78 is skipped. `cachedParams` and `paramsRefreshedAt` are untouched. Line 83 `if (!cachedParams) throw new Error('Protocol parameters unavailable')` still fires when nothing is cached. Otherwise the old cache is returned at :84.
- `cardano/index.ts:114`: `const params = await ensureFreshParams();`. `mintNFTOnChain` is guarded at :96 by `cardanoReady` and `wallet`/`mintingPolicy`.
- `server.ts:49` calls only `initCardanoNFT`.

Safe for minting? Yes. No caller treats `null` as fresh. A null result either (a) fails the mint with "Protocol parameters unavailable" when nothing is cached, or (b) reuses the previously fetched params, as an ordinary Error already did. Nothing mints with absent params. The only residual is staleness (G76-F2): fee or TTL errors lead to a rejected transaction, not a wrong one. Tier decision: keep tier 2. The change reduces a throw out of the mint path to behaviour that already existed, and it adds no new mint capability.

## 2. Red-first and mutants

- Base product (provider.ts from develop) with the new test: rc=1, `Tests  2 failed | 1 passed (3)`. The two failures are R1 and R2, each `AssertionError: expected 'threw' to be null` (logs/red_base.log).
- Head product: rc=0, `Tests  3 passed (3)` (logs/green_head.log).
- Product sha256 `fa1e033dbcf98e49c1913e1b8b39ed5064afbed4e43c469ffd26e41484bcb623` before and after every run, restored each time (logs/run_py.log).

| Mutant | Result | Log |
|---|---|---|
| M1 fallback string changed | killed (2 failed) | logs/mut_M1.log |
| M2 read hoisted outside inner try | killed (2 failed) | logs/mut_M2.log |
| M3 inner catch rethrows | killed (2 failed) | logs/mut_M3.log |
| M4 return undefined instead of null | killed (3 failed) | logs/mut_M4.log |
| M5 log text changed | killed (3 failed) | logs/mut_M5.log |
| M6 reason left unset | killed (2 failed) | logs/mut_M6.log |
| M7 Error.message dropped (`String(err)`) | killed (1 failed) | logs/mut_M7.log |
| M8 log key renamed | killed (3 failed) | logs/mut_M8.log |
| M9 instanceof dropped (same edit as M7) | killed (1 failed) | logs/mut_M9.log |
| M10 non-Error branch constant `'x'` | **SURVIVED** (3 of 3 passed) | logs/mut_M10.log |
| M11 logger.error removed | killed (3 failed) | logs/mut_M11.log |
| M12 return `{}` instead of null | killed (3 failed) | logs/mut_M12.log |

The result is 10 killed and 1 survived among 11 distinct mutants (M9 is a duplicate of M7).

## 3. nft-certificate whole suite

I ran `npm ci --ignore-scripts` (rc=0, 1795 packages; logs/npm_ci.log) and built packages/shared with tsc (rc=0; logs/build_shared.log). Vitest ran with `nice 10` and maxWorkers=2.
- Base provider.ts, new test excluded: rc=0, 17 files, 134 of 134 (logs/suite_base.log).
- Head: rc=0, 18 files, 137 of 137 (logs/suite_head.log).
- Both runs match the author's figures. The head provider.ts sha was restored (RESTORE_OK, logs/suite_driver.log).

## 4. merge-tree

`git merge-tree --write-tree <develop> <head>` returned rc 0 with tree `284d5971fb2e3a257af39745b1fd3c9bca10fbcb`, and no conflicts (logs/merge_tree.log). That tree equals the head's own tree, as expected for a one-commit PR on develop's tip. The develop tree is `0becd64b5c6cbb7634629efc81d45de4fe9245aa`.

## 5. Fragment pair

- `docs-fragments.mjs check --root <clone>` on the head: rc 0, "flow 117 legacy + 46 new, cheat 112 legacy + 46 new; lint clean, render passes html_docs_check", plus the two ADVISORY lines in G76-F4 (logs/frag_check.log).
- Planted defect (an unclosed `<div><span>` appended):
  - cheat fragment: rc 1, "tags are not balanced" (logs/frag_planted_cheat.log).
  - flow fragment: rc 1, "tags are not balanced" (logs/frag_planted_flow.log).
- Restored by sha256: cheat `9abba66d0adfeff253e1e5c0701060498ab981c3b86ed89815f1a15687022485`, flow `c7213f0468de9ff8b42e385b6ab0334ef21dba5a923b2310dac6017510054751`, both unchanged after restore. The check after restore was rc 0 (logs/frag_check_after.log, logs/frag_driver.log).

## 6. END heads

PR head `968757f1…` (unchanged), develop `85c56a3d…` (unchanged). See logs/head_end.log.

## NOT TESTED

- A real Blockfrost call or a booted service.
- The `ensureFreshParams` and `mintNFTOnChain` path with an unreadable throw. It is read from source only; I did not write a test, as I report findings only.
- Node 24 or an LTS Node. I ran Node v26.8.1.
- Whether the docs-fragments ADVISORY lines pre-exist at base.
- The four platform suites, the anchoring service's own copy of the function, the pre-push hook legs (3 of 16 skipped by the author) and CI.
- Any deploy or merge.
