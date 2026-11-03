# QA gate 159 (TIER 1, Opus, round 1): Secuura PR 1976, KS-1868 anchoring reconciler + thread-token trust registry

**Verdict: GO WITH NOTES. Trust question: MERGE.** By the brief's own test, nothing to hold. With an unreadable value, head gives the same outcome as base with an ordinary Error in every cell I measured, at all three changed catches, in both modes and both logger formats. No fix is needed before merge.

There is one PRE-EXISTING fail-open (G159-F3). It is the same at base and head and this PR does not cause it. It should go to Kam as its own card and does not block this PR.

There is also one consistency point for Wednesday. Under gate 148's rule, any change from fail-closed to fail-open goes to Kam whatever the brief says. This PR has that shape at `utxoIsTrusted`: base rejected, head says trusted. But that site has no production callers (G159-F2). If Wednesday applies the gate-148 rule here, it becomes HOLD-FOR-KAM on a single card that combines F2 and F3.

- **Subject:** PR 1976 (Refs KS-1868).
  - commit 1: `bdc1d4d8449e74a5be0b231fe9efb759078333e0`
  - commit 2 (head): `dba3a90a95c9fb6028d1529195ed0af464259158`
  - build base: `4d1ab2cb6574e2b221353ac3a1de56d515711aaf`
- **Head pin:** re-read by `ls-remote` at the end of the gate (2026-11-03T00:06Z). `refs/pull/1976/head` = dba3a90a (unchanged), and develop = `66cbe4e52d5afadc9d13ca141200026cc68d5095`.
- **Code:** taken from a `git clone --shared` of the Secuura checkout, placed at `repo/`. I fetched the PR head and develop from GitHub into MY clone only. All worktrees are of my clone (`wt_*`, `wt2_*`). The Secuura checkout and the author's worktrees were only read.
- **READY mail:** `evidence/r77_pr1976_ready.txt`, read whole.

## Environment note (read first)
The Secuura checkout's installed `node_modules` are STALE: zod 3.25.76 where the tree requires ^4.6.7, and the shared dist has no `boundedJson`, `zod3-compat` or emitter exports.

My first suite run, round 1 in `wt_*` linked to those installs, load-failed 20 anchoring files the same way at base, head and develop. Its result was 20 failed files with 3 failed tests (`logs/suite_*.log`). That run is environmental and I discarded it.

Every figure below comes from **round 2** (`wt2_*`). Those worktrees link read-only to the fresh install in the author's own worktree `worktrees/s-r76-anchoring-recon`, which has zod 4.6.7, and its `@secuura/shared` points at its `packages/shared`.
- The `packages/shared` tree hash is `edf16d9a` at base, head and develop alike.
- The probe was run in BOTH environments. The base-vs-head analyses are identical apart from timestamps (`logs/analyse_base_head.log` and `logs/analyse2_base_head.log`, 0 diff lines once timestamps are removed).

## Answers

**Q1, the class bar: MET at all three changed catches.** These are reconciler.ts:399 (per-row), reconciler.ts:420 (whole pass) and threadTokenIndex.ts:72 (registry load).

**Q2, trust.**
- **Registry:** in non-strict mode, an unreadable value now gives `[]`. Then `utxoIsTrusted` = **true** for a FOREIGN UTxO, and `filterUtxosByRegistry` passes every UTxO through with null attribution. That is exactly what an ordinary registry Error and an empty registry already give at base and at head. So it cannot make anything trusted that an ordinary failure would not.
- At base, the same unreadable values instead made the call REJECT (no trust answer, no log line). Base was closed by accident, and head is open, the same as the ordinary case (F2).
- Strict mode rejects every value at base and at head. Head rethrows the ORIGINAL value; base rethrew the read error.
- **Reconciler:** head never marks a row `confirmed` or `failed` that base would not mark after an ordinary Error. Head does confirm or fail more rows than base did after an *unreadable* value. That is because base abandoned the pass, while head carries on exactly as it does for an ordinary Error. Every write head makes still needs the chain to say "confirmed", or two answered "not found" passes past the window plus a complete search that finds nothing.
- **Empty registry:** at base, an empty registry means trusted in non-strict mode. That is the documented pre-NFT fallback. But the same fallback also fires on ANY registry query failure while the registry is POPULATED. That pre-existing fail-open is F3.

**Q3, the two-commit shape: CONFIRMED.**
- `git diff --stat HEAD~1 HEAD` = 1 file, 1+/1-: the `vi` import on line 1 of the reconciler test.
- Commit 1 touches exactly the 6 PR paths.
- Base + squash gives tree `59b05712…`, the same as the head tree (`logs/shape.log`).

**Q4, re-measured figures: they match the author's,** with one difference in which cell flaked under load (see Figures).

## Findings

### G159-F1: class bar met at every changed catch (PASS)
- **FOUND:** At head, every unreadable value matches base with an ordinary Error. The comparison covers: settled state, returned value, rejection identity, the rows written (`updates`), the pass results, the log-line messages, unhandled rejections and uncaught exceptions.
- The values tested were: revokedProxy, a message getter that throws, a Symbol message, null, undefined, a BigInt message, a bare BigInt, an Error whose toJSON throws, a message whose toJSON throws, a message whose toString throws, an object whose toString throws, and a null-prototype message. Ordinary Error and plain string were the controls.
- **Registry:** 2 envs × 2 modes × 3 functions × 14 values = 168 cells, plus 24 populated/empty controls. Every head-hostile cell equals base-ordinary.
- **Reconciler:** checkTx, SELECT, updateStatus and give-up-with-checkTx × 14 values, plus the no-fault controls. Every cell equals base-ordinary.
- The only text that changes is the logged `error` field. It reads `"unreadable thrown value"` for unreadable values, `"Symbol(s)"`, `"10"` for a BigInt message, and `"[object Object]"` for an object message.
- **TESTED:** `logs/probe2_{base,head}.jsonl` (264 cells each) and `logs/analyse2_base_head.log`, where 4 cells diverge, all at the UNCHANGED sweep catch (F4). The round-1 environment gave the same result: `logs/probe_*.jsonl`.
- **HOW:** `scripts/gate159_probe.test.ts`, the same bytes copied into `wt2_base` and `wt2_head` and run by vitest. It loads the REAL reconciler.ts, threadTokenIndex.ts, utils/logger.ts (winston 3.19, with NODE_ENV test giving the debug-level dev format and NODE_ENV production giving info-level json) and @secuura/shared. Only `../db`'s `query` and the reconciler's chain/DB/wallet deps are replaced.
- The reconciler's `log` is index.ts's own production `log()` (JSON.stringify to console.log). It is extracted from that worktree's index.ts source text by regex, because index.ts starts the HTTP listener on import, so it cannot be imported. index.ts and logger.ts are identical at base and head.
- Output is captured at stdout/stderr/console. I did not use an instrumented logger.
- **Controls:**
  - The capture fires: the ordinary-Error cells carry their log lines.
  - The instrument can see a divergence. 59 base-hostile cells differ from base-ordinary: registry rejects with a TypeError or `getter boom`; the BigInt message breaks the dev-format JSON.stringify; the throwing toJSON breaks production's safe-stable-stringify at error level; the reconciler pass is abandoned or rejects.
  - The 4 sweep cells diverge at head too.

### G159-F2: unreadable registry failure: base REJECTED, head says TRUSTED (INFO; the same as an ordinary Error; no production caller)
- **FOUND:** `utxoIsTrusted(FOREIGN UTxO)` in non-strict mode:
  - **revokedProxy / getterThrows:** base rejected (`TypeError: Cannot perform 'get' on a proxy…` / `getter boom`), head resolves **true**.
  - **msgBigInt and msgThrowingToJSON:** base rejected only under the dev logger format (NODE_ENV≠production). Under production the debug line is not emitted, so base already resolved true.
  - **Ordinary Error, at base and head:** true.
  - **Populated registry, no fault:** false (control).

  `filterUtxosByRegistry` behaves the same way: all UTxOs, attribution null.

  This is a fail-closed → fail-open transition only relative to base's ACCIDENTAL rejection. Relative to the brief's bar (base with an ordinary Error) it is unchanged.
- **Reachability:** `git grep` across the whole tree at head and at develop finds NO production caller of `loadActiveRegistry`, `filterUtxosByRegistry`, `utxoIsTrusted`, or of the module `threadTokenIndex` at all. The only callers are the PR's own test and the module's internal calls. Positive control: the grep finds the PR test's imports and the definitions. `STRICT_THREAD_TOKEN_INDEX` is set in no compose, env or config file; the only mention is in a design doc. So every environment runs non-strict.
- **TESTED:** the utxoIsTrusted and filterUtxosByRegistry rows in `logs/analyse2_base_head.log`.
- **HOW:** As F1.
- The PR's flow fragment says "base gave that for 8 of the 12 … REJECTED for the other 4". That holds under the dev logger format only. Under NODE_ENV=production I measured 2 of those 4 rejecting at base.

### G159-F3: PRE-EXISTING fail-open: any registry query failure makes every UTxO trusted, even with a populated registry (MEDIUM, base = head, for Kam's KS-1256 context; not caused by this PR)
- **FOUND:** In non-strict mode (the default, and the setting everywhere), the registry being populated with `pol1` gives:
  - foreign UTxO, no fault: **untrusted**;
  - foreign UTxO, the registry query throws an ordinary Error (`boom`): **trusted**.

  `filterUtxosByRegistry` then returns the attacker's UTxO with the genuine one. That is the "datum hijacking" the module header says this filter exists to stop.

  The code comment justifies this degrade as "the migration may not have run". But the catch does not distinguish a missing table from a transient DB error (connection refused, timeout, pool exhausted). Contrast `index.ts:1266`, which does test for `relation … does not exist`.

  The same is true of an empty registry (the documented pre-NFT fallback). Both are identical at base and head.
- **Mitigation today:** nothing in production calls these functions (F2), so it is latent. It becomes live the day the read path is wired to them in non-strict mode.
- **TESTED:** populated/no-fault vs throw/ordinary cells at base and head, both envs.
- **HOW:** As F1. Controls: populated gives false and empty gives true, at base and head.
- **Pinned by the tests:** the PR's tests pin this behaviour. Mutant `idx M6_site`, which makes the non-strict branch fail CLOSED (rethrow), is KILLED by 5 cells (control C2 among them: "an ordinary Error in non-strict mode resolves []"). A later fail-closed fix will have to change those cells on purpose.

### G159-F4: residual unguarded read in a changed file: the R6 sweep catch (LOW, base = head, not in this PR's scope)
- **FOUND:** reconciler.ts:280-281 (`no-hash row search errored`) still logs `error: err?.message` unguarded. With an unreadable value from `scanWallet`, `checkTx` or `updateStatus` during the sweep:
  - the sweep is abandoned after the first no-hash row (`scanned` 1, not 2);
  - the line logged is the incidental read error (`Reconciler pass failed`);
  - nothing is written.

  Head and base are identical. This is fail-closed: rows are left alone. The production wallet-scan callers throw ordinary Errors as far as I read. The PR fragment discloses that only these three catches are covered.
- **TESTED:** reconciler `sweepScan` × 14 values (the 4 DIFF rows in `logs/analyse2_base_head.log`).
- **HOW:** As F1.

### G159-F5: the author's measured claims re-measured (INFO)
- **FOUND:** red-first, suites, tsc, eslint and fragments all match the READY and the fragment. Details are under Figures.
- One difference: in my full head run, the cell that timed out under load was `threadTokenMint` (60 s), not the pool-listener C1. A named re-run of the file alone failed with the pre-existing `Could not serialize the data: Error: Unsupported type`.
- The pool-listener file passed 5/5 in the full runs and alone, at head and at develop.
- **TESTED/HOW:** the logs named under Figures.

### G159-F6: two-commit shape (PASS)
- **FOUND:** as Q3. Commit 2's message says it is test-only by ruling.
- **HOW:** `scripts/shape.sh`, run with `commit-tree` in my clone.

## Figures (round-2 environment; vitest 4.1.10 as installed, testTimeout 60 s)
- **Red-first** (base product + the PR's two head test files, `wt2_red`; `logs/redfirst2.log`):
  - reconciler 8 failed / 12;
  - registry 5 failed / 9;
  - 13 AssertionErrors, no crash or timeout.

  The round-1 environment gave the same: `logs/redfirst.log`.
- **New tests at head:** 2 files / 21 pass.
- **Whole anchoring unit suite** (`logs/suite2_*.log`):

  | Tree | Files | Tests | Passed | Failed |
  |---|---|---|---|---|
  | head | 61 | 817 | 816 | 1 |
  | base | 59 | 796 | 795 | 1 |
  | develop 66cbe4e5 | 59 | 796 | 795 | 1 |

  - The single failure is always `threadTokenMint … deterministic per-seed policyId`.
  - At base and develop it fails with `Unsupported type` (1.0–1.5 s).
  - At head the full run timed it out at 60 s under load. **Named re-run:** the file alone at head failed with `Unsupported type` (`logs/rerun_threadTokenMint_head.log`).
  - So it is pre-existing on develop and not caused by the PR.
  - Pool-listener file re-runs: head 5/5, develop 5/5 (`logs/rerun_poollistener_*.log`).
- **tsc** (`logs/tsc2_*`):
  - product `tsconfig.json`: 0 errors at base, c1 and head;
  - product + tests (a gate tsconfig that drops the `__tests__` exclude): base 1, **c1 2**, head 1. The one error is `TS6133 'UNREADABLE'` in the already-merged `ks1868-anchoring-message-coercion-unreadable-throw.test.ts`. The base and head sorted lists are identical.
  - c1's extra error is `TS6133 'vi'`, the positive control for commit 2.
  - Anchoring has no typecheck-tests ratchet baseline, so "ratchet 1→1" means this raw count.
- **eslint** (`logs/eslint2_*`):
  - head 4 files: 0 errors / 0 warnings;
  - base 2 product files: 0/0;
  - c1: 0/1 (`no-unused-vars` on `vi`), the positive control for commit 2;
  - planted file: 1 error and 1 warning (`no-debugger`, `no-unused-vars`), rc 1. The planted file was moved to `logs/_plant/`.
- **docs-fragments** (`scripts/frag.sh`, `logs/frag_*`):
  - `check` OK, rc 0: flow 117 legacy + 112 new, cheat 112 + 112.
  - Planted unclosed `<div>`: FAIL rc 1 for flow (`opened 1, closed 0`) and for cheat (`opened 3, closed 2`). Both restores were sha-OK.
  - The two pmatrix ADVISORIES (flow line 6249, cheat 6235) are PRE-EXISTING: identical at base (`logs/frag_check_base.log`).
- **Mutants** (`scripts/mutants.py`, `logs/mutants_table.log`, `logs/mutant_*.log`): **22 run, 22 KILLED, 0 survived.** The unmutated control was 21/21.
  - Each of 3 sites got: M0 revert to the unguarded read; M1 inner try dropped; M2 always the constant; M3 no String(); M4 inner catch rethrows; M5 a different constant; M6 a site mutation (row: `break` after a failing row; pass: no log line; idx: non-strict rethrows, i.e. fails closed).
  - idx also got M7: strict throws a new Error instead of the original.
  - Every kill was a test failure with no timeout, and every restore was sha-OK.
  - Weakest kill: idx M3 (no String()), killed by 1 cell.

## Merge-tree onto develop 66cbe4e5
**CLEAN, and the merge changes exactly the PR's 6 paths.**
- Merge-base is 4d1ab2cb. develop has moved 9 commits and 52 paths since. The overlap with the PR's 6 paths is 0. develop's nearby changes are only other KS-1868 fragment files; it changed nothing under `services/anchoring/` or `packages/shared/`.
- `git merge-tree --write-tree 66cbe4e5 dba3a90a` → rc 0, tree `a695bf80daaa739181cd0dfd1825ccafa94ee070`.
- The diff of the merged tree against develop is exactly the PR's 6 paths, and every merged blob equals the head blob (`logs/mergetree.log`).
- **Positive control** (`scripts/mergetree_pc.sh`, `logs/mergetree_pc.log`): `git merge-file` on scratch copies. The real develop file gives 0 conflicts with output byte-equal to head, for both product files. A develop copy edited on the PR's lines gives 2 conflicts in each file.
- The first control attempt, inside `mergetree.sh`, errored because `git mktree` needs a non-recursive listing. Its output is in that log and it was replaced by the merge-file control.
- Because develop changed nothing in anchoring or shared, the develop suite (equal to base) plus the head suite stand in for the merged service. I did not run a separate merged-tree suite.

## NOT TESTED
- A real Postgres, a real chain or Blockfrost provider, a booted anchoring service (index.ts wiring), or the real `walletLabelScan`. The reconciler ran with plain-function deps and index.ts's `log()` re-evaluated from source.
- Whether any real dependency (pg, Blockfrost, Lucid) can throw an unreadable value at these sites. These are operator-authored goldens.
- A production wiring of the registry functions, because none exists (F2). The trust analysis is of the module's contract.
- Multiple reconciler replicas, or the `running` flag under overlapping timers. The third pass in each cell only shows that `running` is released.
- Node 24 or any LTS release; every run used host Node v26.8.1. The shared dist used is the author's worktree build (same source tree hash), not one I built. My own rebuild against the stale checkout install did not compile cleanly and was not used.
- The four platform suites and the pre-push hook legs 3, 4 and 8 (the READY's PREFLIGHT INCOMPLETE).
- The other KS-1868 sites (the ticket lists 253), beyond confirming the sweep residual in F4.
- `uncaught` and `unhandled` stayed empty in every cell, and I have no cell where they were provably reachable. Treat those zeros as "none seen", not as a proven negative.
- The full eslint config of the repo beyond these files, and the R 76th recorder itself. I did not re-run it; the gate's own probe replaces it.

## Housekeeping
- No process started by this gate is running (`ps`: nothing with this workdir).
- Worktrees `wt_*` (round 1, stale environment) and `wt2_*` (round 2) remain in the workdir, holding the untracked probe, gate tsconfig and vitest config files. Nothing was deleted.
- No write was made outside the workdir.
