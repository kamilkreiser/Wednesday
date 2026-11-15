PR 2230: GO WITH NOTES (at head 220df650550aeb1ef1df43b1eb7919f48fb7140a; tier 1)

Gate 358 (tier 1, Opus), 2026-11-15 17:38 to 17:50 AEDT. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub. No Cardano network call of any kind (no submit, no sign, no read).

**Pins.**
- `gh api` at 17:38:23, `git ls-remote` at 17:38:48 (`scratch/pin1.out`), both again at 17:49:06/07 AEDT (`scratch/pin2.out`). Nothing moved:
  - develop ce35818d50aebe7f41fc41f677ee03079c36d7ad
  - refs/pull/2230/head 220df650550aeb1ef1df43b1eb7919f48fb7140a (open, not merged)
  - refs/pull/2081/head 17c453253d68206d9d3fcbb723a7ffc9d9291a3d
- PR 2230 is 3 commits on 48883ba5976b, **7 files** (+509 -6): `cardano/transaction.ts`, `cardano/provider.ts`, `walletSpend.ts`, `walletView.ts`, one cell file, the fragment pair.
- develop moved 48883ba → ce35818 by one test file outside anchoring; the anchoring tree is e13fe1f02e26 at BOTH (rev-parse), so "develop" below means develop's own anchoring tree.

## FOUND

**G358-2230-1 (Low; documentation honesty; fix before merge, no code change needed).** The PR body, the READY mail and the fragments carry stale and self-contradicting statements left over from commits 1–2:
- Body "Scope": *"No overlap with open PR 2081 … it touches … `cardano/provider.ts`; this PR touches none of those."* **False**: this PR changes `provider.ts` (+12). The body's own banner, two screens up, says the opposite ("Overlap with PR 2081 (`provider.ts`)"). The READY mail repeats the false line ("I touch none of those") and says "4 paths".
- Body "Touched": 3 paths. Actual: 7.
- Body Test Evidence table: 11 cells / 8 of 11 red / 838 passed. At this head: 15 / 12 of 15 / 842 (my measurement, and the banner's own figures).
- Body "One thing raised, deliberately not fixed here" (walletSpend `toBuildUtxo` drops the fields): it **was** fixed by commit 3 (`carryFacts`). The READY carries both "F1: BUILT" and "RAISED, NOT FIXED" for the same thing. The cell file's `(e2e)` header still says "Raised for a ruling rather than fixed here" and "DROPS these fields".
- Body "The change" and **both fragments** name `assertFeeCoversSignedBytes`; no such function exists. It is `assertFeeCoversSignedTransaction`.
- `assertFeeCoversSignedTransaction`'s own doc comment (transaction.ts) still says the ref-script cost is one "we cannot compute". The function now computes it when the size is known.
- The seat's HANDOVER "What shipped" (b37e1305d, 4 paths) is also stale. It is the seat's record; noting it, not grading it.

Exact action: the body's Touched, Scope, Test Evidence and "One thing raised" sections are rewritten to the measured state (a GitHub edit, no commit). The fragment function name and the two stale comments should be fixed in the next commit that touches them, or in a follow-up. None changes behaviour.

**G358-2230-2 (Medium; latent; pre-existing; NOT this PR's scope; for the board, needs a ticket).** There is a sibling path with the same defect class, and it is not covered. The thread-mint spend (`threadMintSpend.ts:101-109`, route at `index.ts:1162-1166`) fetches the **same platform wallet** through `fetchUtxosAll` and hands every pass-1 coin to Lucid through `toLucidUtxo` (`threadMintSpend.ts:66-76`). That function hard-codes `scriptRef: null, datum: null, datumHash: null`. So the 4,405-byte reference-script coin reaches Lucid looking plain:
- Lucid can select it.
- It cannot see the Conway ref-script charge, so the fee comes out low.
- Spending it consumes the deployed script.

This PR's exclusion lives only in `buildAnchorTransaction`. **UNMEASURED**: I did not run Lucid's coin selection, and I did not establish whether the thread-mint route is live on demo-pk. Read at source only.

Exact action: one ticket to apply `unspendableForAnchor` (or an equivalent filter) to the thread-mint candidates, and to stop `toLucidUtxo` from blanking the script and datum facts.

**G358-2230-3 (Low; test gap).** The guard's call site inside `buildAnchorTransaction` is pinned by no cell. My `guard_unwired` plant (`if (false) assertFeeCoversSignedTransaction(…)`) turned **0** cells red across the PR's 15 cells, my 6 probes, and 5 KS-1384 files (94 tests). The guard is tested only by direct calls. Why the gap is real but small:
- Because of the exclusion, its ref-script term can never fire from a real build today.
- CSL's own pricing normally covers the signed bytes.

So removing the call would be invisible. Suggested: one cell that spies on the guard, or a build fed a deliberately underpriced protocol param, to show the build refuses.

**G358-2230-4 (Info).** The Conway tiering is correct but not pinned by the PR:
- The guard uses `CSL.min_ref_script_fee` (CSL 15.0.3). My Q1a confirms it is the tiered rule: 4405→66,075; 25,600→384,000; 30,000→463,200 (the 4,400 bytes above the first tier priced at 15×1.2).
- My `guard_flat_price` plant (`refBytes * price`) was caught only by my Q1b. The PR's cells use 4,405 bytes, which sits under the first tier.

No effect below 25,600 bytes.

**G358-2230-5 (Info).** The guard counts reference scripts on **spent** inputs only. The Conway rule also charges reference scripts on **reference inputs**. This does not matter today:
- The anchor builder never adds a reference input (`git grep` for `reference_input`: 0 hits in anchoring src).
- My probes read `body.reference_inputs()` = none on every built tx.

Worth one line in the guard if reference inputs are ever added.

**G358-2230-6 (Info; defence in depth, observed).** With the reference-script exclusion line deleted (`excl_drop_refscript`), the PR's `(excl) reference script` cell and both `(repro)` cells stay green. The reason is that the guard fails closed: the coin has a hash and no size, so the guard refuses with KS-2196 anyway. That line is pinned by `(small)` and `(retry)`, plus my Q1c, Q2b and Q2c. Correct behaviour; recorded so nobody reads those three cells as isolating the exclusion.

## TESTED

**Q1. The fee rule and where the price comes from.**
- **Source of the price:** `provider.ts:313-320`. `fetchProtocolParams()` maps Blockfrost `epochsLatestParameters().min_fee_ref_script_cost_per_byte` into `ProtocolParams.minFeeRefScriptCostPerByte`, as a string, only when the field is `!= null`, so 0 survives. `@blockfrost/openapi` types it as `number | null`, and Blockfrost's UTxO type has `reference_script_hash` and no size field (read in node_modules, blockfrost-js 6.1.1).
- **Caching:** the params are cached by `cardano/index.ts` (`ensureFreshParams`, TTL refresh).
- **The guard** (`transaction.ts`, `assertFeeCoversSignedTransaction`) requires `CSL.min_fee(signed tx, a, b) + CSL.min_ref_script_fee(Σ ref-script bytes on the body's inputs, price/1)`. It fails closed in three cases: size unknown, price absent, or an input that was never offered. It runs on the **signed** CBOR before return, so before any submit.
- **An anchor whose inputs carry the 4,405-byte script** is never built:
  - with a plain coin present, the plain coin is selected (Q2b);
  - with none, the build throws a retryable shortage (Q2a, Q2c);
  - a family outpoint carrying one is refused permanently.
- If the size were reported, the guard demands bytes + 66,075. The PR's `(ref-fee)` cell checks this and my Q1b checks the tiered variant.
- **My simulated ledger minimum** (bytes + tiered ref fee over spent and reference inputs) was met by every tx built at the head in Q1c, Q2b and Q2c.

**Q2. Stuart's failure, red at develop and green at head.**
- **The PR's cell file**, by vitest JSON (`scratch/out-redproof-*.json`):
  - head: **15/15** passed, rc 0;
  - develop's anchoring src: **12 of 15 red**, 3 pass (`(plain)`, `(mixed)`, `(e2e)`).
  - This equals the READY. The develop reds:
    - the five `(excl)`/`(repro)` cells: "promise resolved instead of rejecting", meaning develop builds a tx from script coins;
    - `(small)`: develop selects the script coin;
    - `(retry)`;
    - `(guard)`, `(ref-fee)`, `(ref-closed)`: red because the function is missing;
    - `(facts)`, `(param)`: AssertionError.
- **My own independent reproduction** (`scratch/probe/gate358-probes.test.ts`, `out-probes-*.json`): the **real** builder driven through `spendFromView`, with a simulated node that refuses as FeeTooSmallUTxO when fee < bytes-min + tiered ref fee.
  - **At develop:**
    - Q2c throws `FeeTooSmallUTxO supplied 177425 expected 243324`. The gap is 65,899, against Stuart's 178,393 / 244,248 (gap 65,855), the same arithmetic.
    - Q2a and Q2b red the same way; Q1c red (177,777 < 243,676).
  - **At head:** 6/6 green. Q2c: the first fetch (script coins only) throws the KS-2196 shortage, the bounded refetch runs, and the second fetch builds on the plain coin. Every tx sent satisfied the simulated node.

**Q3. 2230 × 2081 (`scratch/mt.sh`, `out-mt.txt`).**
- `merge-tree --write-tree` 2230×2081 and 2081×2230: rc 0, tree **7e591ac6a60b** both ways (equals AA 6th's figure).
- Onto my develop ce35818d:
  - (dev+2230)+2081: rc 0 → tree **746f0d92f497**;
  - (dev+2081)+2230: rc 0 → tree **746f0d92f497**.
  - Identical final trees, so **merge order cannot change behaviour**.
- Every added line of both PRs' `provider.ts` hunks is present in the final blob 46300c404828: 10/10 from 2081, 12/12 from 2230. The two hunks are disjoint: 2081 changes `getTransaction`'s null/undefined; 2230 changes `ProtocolParams` and `fetchProtocolParams`.
- **Planted control:** an adjacent-line edit of `minFeeB: string;` against 2230 gave rc **1**.
- **Whole anchoring suite on the merged tree** (scratch commit 875afa02cae4): 871 passed, 1 failed (the same pre-existing threadTokenMint). That is 843 + 28 (2081's cells).

**Q4. Secrets and network.**
- **Secrets:** a regex sweep of the diff's added lines (mnemonic/secret/key/password/xprv/addr_sk/long tokens/24-word phrases) found prose and identifiers only. The planted control (a 32-char token) matched. The keys are `CSL.PrivateKey.generate_ed25519()`, ephemeral per run; the Blockfrost key is the literal `'key-not-real'`; the outpoint hashes are synthetic `H('x')`.
- **Network:** `@blockfrost/blockfrost-js` is `vi.mock`ed file-wide, and no cell calls submit, init or fetch. This was read at source, not proven by a network sandbox.

**Q5. AA 6th's F1/F2: CLOSED, as claimed.**
- **F2** (the guard carries the Conway term): built. Every guard line was killed by a plant: `guard_no_refterm`, `guard_unoffered_ok`, `guard_nosize_skip`, `guard_noprice_free` and `guard_off_by_one` were each caught by the PR's cells. The price plumbing (`param_unmapped`, `param_truthy`) was caught by `(param)`.
- **F1** (the view round trip keeps the facts): built. `carryFacts` is on both `toViewUtxo` and `toBuildUtxo`, and `view_drops_facts` and `build_drops_facts` are each caught by `(facts)`.

**Mutants: 19 of mine, one per changed behavioural line** (`scratch/plant.py`, `plants.sh`, `out-plants.txt`). The suite under each is the PR cell, my probes, and the 5 KS-1384 spend, builder, view, thread-mint and family files: 94 tests, baseline 0 red.
- 18 of 19 went red.
- One survivor: `guard_unwired` survived everything (G358-2230-3).
- `guard_flat_price` was caught only by my Q1b, not by the PR's cells (G358-2230-4).
- `guard_offered_no_required` was caught by 2 KS-1384 family cells, not by the PR's own cells.
- Every restore was by `git checkout HEAD --`; the blobs read back 5439586e9a5d, 6e3def0ba1aa and d729e9629206 each time, and porcelain ended at 0.

**Whole anchoring suite**, interleaved, vitest JSON, Node v26.8.1, CSL 15.0.3 (`out-suites.txt`):

| Tree | Run 1 | Run 2 | load1 at start |
|---|---|---|---|
| develop ce35818d | 62 files, 827 pass / 1 fail | same | 11.97 / 6.28 |
| head 220df650 | 63 files, 842 pass / 1 fail | same | 11.72 / 5.06 |
| develop+2230+2081 | 64 files, 870 pass / 1 fail | (one run) | 8.82 |

- The 1 fail is the pre-existing `threadTokenMint.test.ts > parameterises mint + spend with a deterministic per-seed policyId`, present in all three trees.
- 827 + 15 = 842. This equals the READY.

**tsc / lint** (`out-tsclint.txt`; load1 3.4):
- `tsc --noEmit -p services/anchoring/tsconfig.json`: rc 0 at develop and at head. That tsconfig excludes `src/__tests__`.
- Over src plus tests (a scratch tsconfig extending it): 1 error at both trees, the pre-existing `ks1868…:46` TS6133. This equals the READY.
- Planted TS2322: rc 2; restored.
- ESLint API (Dev root flat config) on all 5 changed TS files: 0 errors / 0 warnings. Planted control: 2 errors + 2 warnings.
- **docs-fragments check:** OK. Lint is clean and the render passes `html_docs_check`; the two ADVISORY lines are not KS-2196's. A planted unbalanced tag in the KS-2196 cheat fragment gave rc 1, naming the file. Restored, eaff29efa8aa.

## HOW
- **Clone:** `scratch/clone`, `git clone --reference` to the Blockchain project's object store (read-only alternates). Fetched with that project's deploy key via a script-local `GIT_SSH_COMMAND`; push URL `DISABLED` (shown in pin2).
- **Worktree:** one sparse worktree, `scratch/wt` (Blockchain/Dev, Projects Documents, systemTest support). One root `npm ci --ignore-scripts` plus a `packages/shared` build, at load 25→19, both rc 0.
  - This is valid for both trees because the lockfile is unchanged and develop's anchoring tree is byte-equal to the PR's base.
  - Trees were switched by `checkout --detach` (suites) or by checking out develop's 4 src files (red-proof, probes).
- **Probe file:** copied in only for runs and moved out after.
- **Scratch commits:** merge commits for Q3 were made with commit-tree in the scratch clone only, with a scratch identity.
- **GitHub:** PR JSON by `gh api` GET (kksecura), saved as `scratch/pr2230.json`.
- **Load:** heavy legs ran at load1 3.4–12; the npm ci ran at ~25 (ungated).
- **No writes outside this folder.**

## NOT TESTED (UNMEASURED)
- A live node, Blockfrost, or demo-pk. The "node" is my simulator of the Conway fee rule for a vkey-only tx with CSL's tiered `min_ref_script_fee`; it is not the ledger.
- The deploy (owed to a D seat, card 1107).
- Lucid's coin selection on the thread-mint path, and whether that route is live (G358-2230-2).
- `*.integration.test.ts` (needs Postgres), the repo pre-push preflight, `check:test-types` (anchoring is not enrolled; the seat named this), Node 24, a container build, and the four platform suites.
- Linear KS-2196 / KS-2197: not read.
- Stuart's redrafted reply: read for accuracy against my measurements (its arithmetic and its "fix" paragraph match the code). Whether and when to send it is Kam's call.
- The seat's claim that only the 4,405-byte coin yields an integral tx size: not recomputed.
