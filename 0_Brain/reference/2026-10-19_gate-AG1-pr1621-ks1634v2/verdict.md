VERDICT: GO WITH NOTE at head 0810a2edad95... (tier 1, round 1 of 2; landing tree 3e62bf28eb26 on develop 52f8777b6b4b; 0 blockers, 6 notes)

# GATE AG1: PR #1621 (KS-1634 v2 site), Opus, tier 1, round 1 of 2

Gate seat: AG1, independent. Clone: `scratchpad/ag1/repo` (worktree `scratchpad/ag1/land`). Nothing was written under `!CODING`. No GitHub or Linear writes.

## Heads (read at start 09:0xZ, re-read 09:14Z and 09:16Z with `ls-remote`)
- #1621 head `0810a2edad9521ea826634be79115e5cb52a103c`. Unchanged at all three reads. One commit on merge-base `8323f2f70cd7`, author `Kam Kreiser <kamil.kreiser@secuura.ai>`.
- **develop MOVED during the gate.** It was `6ec1b7badb9b` at start and `52f8777b6b4bd9b911c6ccb77157c1e7c52d44fc` at 09:14Z and 09:16Z. The new commit is one KS-1557 commit (`Refs KS-1557: The lineage certify path needs access to the PARENT document`, author kksecura): 7 files (`routes/certifications.ts` + 6 tests). It overlaps the PR's 2 files in **0** of them (grep count 0; the positive control, the same pattern run on the PR's own three-dot list, counts 2).
- **The author's predicted landing tree `548beee35fe5` is now VOID.** I reproduced it exactly on the old develop (merge-tree gave `548beee35fe52d104e99b2d686d7b8e65db7620d`, rc 0), and it no longer names the landing.

## Q5: Landing (instrument: `git merge-tree --write-tree`, `commit-tree`, jest `--json`, `tsc` incl. tests)
| | old develop `6ec1b7badb9b` | **live develop `52f8777b6b4b`** |
|--|--|--|
| merge-tree | `548beee35fe5` (= author's claim) | **`3e62bf28eb26e32a0cceb9964ca5e9518cf173d7`**, rc 0 |
| parent suite | 1495/1495 in 124, rc 0 (= claim) | 1497/1497 in 124, rc 0 |
| landing suite | 1502/1502 in 125, rc 0 (= claim) | **1504/1504 in 125, rc 0** |
| set diff landing vs parent | +7 tests, all from the ks1634-v2 file; 0 dropped; 0 status changes | same: +7, 0 dropped, 0 changed |
| tsc incl. tests (`tsconfig.gate.json` = originate tsconfig with the test exclusions removed, noEmit) | rc 0, 0 bytes | rc 0 on landing and parent, 0 bytes; 144 `__tests__` files in the program |

- tsc positive control: a planted `const x: number = "…"` in the PR's test file gave rc 2 with TS2322 at that line. Restored, `git diff --quiet` rc 0.
- Three-dot `develop...0810a2ed`: exactly **2 files** (A: the ks1634-v2 test, M: `routes/verificationV2.ts`, +205/-0) on both develops.
- Strict `git apply --check` of the PR patch (merge-base to head) at `6ec1b7badb9b`: rc 0. Negative control: the same patch onto the landing tree is refused ("already exists", "patch failed"). `verificationV2.ts` is byte-unchanged from `8323f2f` to `6ec1b7b` (`diff --quiet` rc 0) and from `6ec1b7b` to `52f8777` (it is absent from that name list).
- Setup: `npm ci` (originate + shared + root, `--ignore-scripts`), then `packages/shared` build rc 0, then `npm run generate --workspace=services/originate` rc 0.

## Q1: Is the honesty rule on EVERY v2 path? (instrument: read the whole of verificationV2.ts at head, all 535 lines, plus probes)
Every place where a blob reaches `presentBlockchainHonestly`, or where anchored/tx fields are built:
1. **`chainOnlyMatch` :232** (registry miss → chain-first). It now carries `simulated: chain.simulated`. FIXED. This is the only v2 site that builds an anchored blob from the chain reply.
2. **`buildMatch` :193**, `presentBlockchainHonestly(healed ?? certMeta.blockchain)`. The blob is the row's own stored blob (`chainBlobOfRow`), so it carries the row's own `simulated`. The heal returns early on `blob.simulated === true`, and `...blob` keeps any truthy non-boolean flag. Carries simulated: YES for the stored flag.
3. **`healBlobWithChainFact` :142-154** merges chain txHash/status/height into the row blob and does **not** read `chain.simulated`. This is the one remaining v2 place where a chain reply's `simulated` is dropped (see N4). It is not reachable from the in-tree anchoring.
4. The documentId-only path (:491) is `buildMatch` with `chain = null`, so it is the same as #2.
5. Top-level `simulated` (:209, :255) and `isAnchoredHonestly` (:215, :272) both read the honest blob. Correct.
v1 has the same line at both of its chain-first sites (`verification.ts` :723, :1266). The v2 chain-only site was the only one of its kind left behind.

## Q2: Real anchors and absent/undefined `simulated` (instrument: CONTROL cells + scratch route probe at develop and at landing)
- CONTROL cells green at develop and at landing: real anchor (no key), `simulated: false`, and `verified: 'false'`. Also the S1 inverted control.
- Probe through the real v2 router, landing (develop in brackets):
  - no key, `simulated: undefined`, `null` and `0` all stay on-chain: anchored true, real tx, isAnchored true. [develop: same.]
  - `'true'`, `1` and `'false'` are all refused: anchored false, txHash null, simulated true. [develop: all on-chain.] This is the KS-1628 / E12 rule: a truthy value refuses and mere presence does not.
  - Anchoring's real simulated shape (`txHash: null, simulated: true`) gives anchored false and simulated true at both levels. [develop: **anchored true**, no marker; txHash already null; isAnchored already false.]

## Q3: Stuart's S cell (instrument: tamper + two scratch variants of S1)
- **It reds on the tamper:** removing the product line gives a blob `082fd1c67742` equal to develop's own blob, and reds **3 of 7** (RED1, RED2, S1). The S1 inverted control stays green. Restored blob `5b6620fb3c5f` equals the PR blob.
- **Its guards are weaker than claimed (N2):**
  - (a) The v4 assertion checks `randomUUID()`'s own output, which is always v4, so it guards only the fixture. Variant A, with `documentId: 'not-a-uuid'` and the guard dropped, passes every S1 assertion. No assertion reads `documentId` or `documentUuid` off the reply.
  - (b) "The db was asked and answered no rows" asserts only `toHaveBeenCalled()`. The "no rows" part is the `beforeEach` fixture. Variant B makes the db answer one row with a stored simulated blob. It is a registry HIT (0 chain fetches, no `source`, title `t`), and it still passes every S1 assertion.
  - So S1 is genuine as a regression cell, but it is behaviourally RED1 with different `metadata`.
- **In-process scoping:** the test file's header (lines 151-163) states the substitution honestly. It names `POST /api/anchors` under a connector key, the gateway hop and anchoring's write path as NOT exercised. **The PR body itself was NOT read** (see NOT RUN).

## Q4: Red-first and my own mutations (instrument: jest on the PR test file)
- Develop product + PR cells: **3 failed / 4 passed**. The held 5 are 2 RED + 3 CONTROL, so held cells read 2 red / 3 green, as claimed; S1 is the 3rd red. Every red fails on the missing `simulated` marker (`Received: undefined`). Landing: **7/7**.
- **M1** (my plant: `simulated: false` hard-coded): 3 red (RED1, RED2, S1), 4 green. KILLED.
- **M2** (`simulated: chain.simulated === true`): **survives** all 7 cells and the full suite (1502/1502 in 125 on the old landing). The probe shows that under M2, `'true'` and `1` present as on-chain (N3).

## Blockers
None.

## Notes
- **N1. The landing tree in the claim is void, so re-pin before merge.** develop is now `52f8777b6b4b`. The landing tree is `3e62bf28eb26`, with landing 1504/1504 in 125 and parent 1497/124. The author's `548beee35fe5` and 1502/1495 are true only of `6ec1b7badb9b`.
- **N2. S1's two anti-vacuity guards do not guard the path.** The v4 guard is tautological and the db guard is "called", not "no rows". Both variants pass. Suggested tightening: assert `m.source === 'blockchain'` and `m.documentUuid === freshDocumentId`.
- **N3. The KS-1628 truthy rule is unpinned at the v2 site.** The mutation `=== true` survives every cell and the full suite.
- **N4. Sibling path: `healBlobWithChainFact` ignores `chain.simulated`.** Probe: a reply with `simulated: true` and a real 64-hex tx heals a stored `submitted` row to `confirmed`, isAnchored true. The handed-back blob is then passed to `persistHealedAnchor`. It is unreachable from the in-tree anchoring (simulated ⇒ txHash null ⇒ the heal refuses; probe: stays `submitted`), and v1's `confirmStalePendingAnchor` has the same shape. It is outside this PR's scope and is a ticket candidate.
- **N5. The CAUSE wording overstates the realistic leak.** With anchoring's actual reply (`buildVerifyResponse`: simulated ⇔ fabricated prefix ⇒ txHash null), develop already gave txHash null and isAnchored false. The live false claim was `blockchain.anchored: true` with no `simulated` marker. "A tx hash / explorer-shaped reply" holds only for RED2's synthetic shape.
- **N6. Falsy values now pass through to the wire.** `simulated: null` or `0` from the reply is now echoed as `blockchain.simulated: null/0` on a real anchor. This is cosmetic: anchoring never sends either. v1's identical line does the same.

## NOT RUN
- **The PR body.** No GitHub API identity was available: `gh auth status` reports "not logged in" for the Secuura project config, the global config and the Wednesday config. Q3's body-scoping is checked only against the test file's header. A search of the Secuura history was aborted after 120 s with no result.
- The author's push legs (13/16, 3 skipped) and the shell suites (91/91).
- Integration (DB-backed) jest suites, lint, Docker, and any running stack.
- Stuart's `@k-live` end-to-end: `POST /api/anchors` under a connector key, the gateway hop, and anchoring's write path.
- A real `git merge`: the landing was built with `merge-tree` + `commit-tree` (tree-identical).
- A golden diff and `index` lines: these do not exist for this pass.
- Red-first was run on develop `6ec1b7badb9b` only, not re-run on `52f8777b6b4b`. `verificationV2.ts` and the test are unchanged between the two.
- Probe and variant files live only in `scratchpad/ag1/probes/` and were not in any counted suite run.

43bd1c2f6646ee42c5c85c5e40dcc2a33681eaa12a213ae98b4fb73562972a47
