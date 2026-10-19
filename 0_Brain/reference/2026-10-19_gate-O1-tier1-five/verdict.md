#1597 KS-1634: GO WITH NOTE at head 8ec96bbac643dcb69ba90b2d81634f6cd40e85f1 (gated tree b64be7e50092c55af3d6670f065c2a75601ec584 = its predicted landing tree). Closes L1+L6 on both v1 sites and on the N1 route. A sibling chain-first site in v2 (`verificationV2.ts:231` chainOnlyMatch) still drops `simulated`. Minor 1, not in scope.
#1590 KS-1628 item 3: GO at head 68270e124aac103f0d56519b4cbee25d4ea7f544. Behaviour-neutral refactor; the 1 red anchoring cell is threadTokenMint:71 and fails identically on develop.
#1596 KS-1595 item 1: GO at head 83b5758bc77959c22603c4c1db736db032a32eda. Test-only; kills all 4 gdpr.ts mutants I planted (including the gate's 3).
#1598 KS-1471: GO at head 35a5fcb93c538dd2dfe113c1228f93d7e1d43c23. Log-metadata change only; no authorisation decision moves.
#1599 KS-805: GO WITH NOTE at head 73101f01c32e90b554dfa694b511fa4075a441fe. [] gives 400, an omitted field gives 200, the yaml diff is 1 line (`minItems: 1`), and check:openapi bites. Whether this is ALL of KS-805 cannot be told from the repo (archived history pairs KS-805 with a KS-839 contract sentence). The route and spec copies of the schema are written twice by hand.
sha256/16: fe8620d0e1225302

# GATE O1: five tier-1 PRs, batched, round 1 of 2

`git ls-remote` at 11:57 AEDT (re-read at the end): develop `78cb3c3939e319332e387ffecb075a169edd4a39`, tree `1ca89b2b5b7280ced0760012b09338dec94766aa`. All five heads equal the brief. Each head is one commit.
- Merge bases: #1597, #1598 and #1599 sit on develop 78cb3c39. #1590 and #1596 sit on 83ed01af70fd, which is 3 merges behind (#1588, #1587, #1589).

## FOUND / TESTED / HOW, per PR

### #1597 KS-1634 (originate `routes/verification.ts`, 2 new suites)
- **Item 1, diff.** 3 files, +293/−2:
  - `routes/verification.ts`: :712 and :1192 `chain?.verified` → `=== true`; :723 and :1266 add `simulated: chain.simulated`.
  - Two `__tests__/ks1634-*.test.ts` files, 6 cells each.
  - Nothing else.
- **Item 2, red-first.** I copied both suites onto develop's code (wt-dev). All 6 RED cells failed on `expect(...).toBe` assertions. All 6 CONTROL cells passed. On the landing tree, 12/12 pass.
- **Item 3, mutants** (`o1/mutants.sh`), all killed:
  - M1, :712 back to truthy: killed by `RED L1 verify-file`.
  - M2, :723 drop `simulated`: killed by `RED L6 verify-file` ×2.
  - M3, :1192 back to truthy: killed by `RED L1 verify`.
  - M4, :1266 drop `simulated`: killed by `RED L6 verify` ×2.
- **4(a), is `=== true` right everywhere a reply is read?** YES. I grepped every caller of `/api/anchors/verify` in services. There are four readers of the chain-first reply, and after this PR all four are strict:
  - `confirmStalePendingAnchor` :454 (`!== true`)
  - :712 and :1192 (`=== true`, this PR)
  - `verificationV2.ts:111` `fetchChainFact` (`=== true`, already)

  Anchoring always sends a boolean (`anchorReadback.ts` `verified: true`, and every 404/400/500 body sends `verified: false`). So the strict read refuses only shapes anchoring never sends: probe L1 `'false'`, L1b `'true'` and L1c `1` all become `verified:false`.
- **4(b), does carrying `simulated` change any answer for a real anchor?** NO answer changes. I measured it with `o1/probe/o1probe.test.ts`, which drives the real v1 and v2 routers with a registry miss, 12 replies × 3 routes, develop vs landing, timestamps normalised (`o1/cmp.py`).
  - Real-anchor replies in anchoring's real shapes are **byte-identical** on all 3 routes: R1 db/confirmed, R2 chain-scan, R4 null height, R5 submitting.
  - Anchoring never sends the key on a real anchor (`anchorReadback.ts:133`, spread only when simulated). The blob gets `simulated: undefined`, and JSON drops it.
  - The ONLY difference on a real anchor is R3, an explicit `simulated:false` (a shape anchoring does not produce). It now shows `blockchain.simulated: false` on v1 /verify and /verify-file. The answer is unchanged (`verified`, `isAnchored`, `anchored` and txHash are all the same).
  - Control: the NEG case (`verified:false`) is identical on both trees. The 14 DIFF rows are all L1/S cases, so the comparator does see differences.
- **4(c), can the Blockfrost chain-scan branch return a placeholder hash?** Not as written. That branch builds `txHash: tx.tx_hash` from `bf.addressesTransactions` (`anchoring/src/index.ts:719-724`), which is a real chain transaction id. It runs only when `isCardanoReady()`.
  - If it ever did carry a placeholder, `buildVerifyResponse`'s prefix rule turns it into the S1 shape (`txHash:null, simulated:true`).
  - At that point `presentBlockchainHonestly`'s HASH rule can no longer catch it, because the hash is already null. What catches it is the `simulated` flag this PR now carries: probe S1 on v1 goes from develop `blockchain.anchored:true, simulated absent` to landing `anchored:false, simulated:true`.
  - `isAnchoredHonestly` already said false on both trees, because it requires a 64-hex txHash.
  - The cached-hit path returns the same body.
- **4(d), does it close the N1 route?** YES for POST /api/verification/verify on a registry miss. The probe (anchoring called 1/1 each time) gives:
  - L1 `'false'` → `verified:false` with no blockchain, where develop said `isAnchored:true`.
  - S2 simulated with a real hash → `isAnchored:false`, `anchored:false`, txHash null, where develop said `isAnchored:true`.
  - S3 `simulated:'true'` → off-chain.
  - S1 → `anchored:false`, `simulated:true`.
  - **Not closed on the sibling public route POST /api/v2/verification/verify** (CSRF-excluded at `api-gateway/src/middleware/csrf.ts:117`). There, `chainOnlyMatch` (`verificationV2.ts:231-239`) still builds its blob without `simulated`. The probe is SAME on both trees:
    - S1: `blockchain.anchored:true`, no simulated marker (isAnchored false).
    - S2 and S3: `isAnchored:true`, txHash presented.
  - Only S1 is a shape today's anchoring produces. See Minor 1.
- **4(e), NOTE (not a finding).** The commit's author identity is not a Secuura identity, as disclosed. The tree I gated is `b64be7e50092c55af3d6670f065c2a75601ec584`. The solo prediction onto develop gives that same tree, so after an author-only force-push to the same tree this verdict carries over.
- **Suite.** On the landing tree, originate is 1461/1461 (120 suites). That is develop 1442 + 12 (#1597) + 7 (#1596). #1597's solo predicted tree IS its head tree, so its solo count is 1442 + 12 = 1454, which matches R's 1454.

### #1590 KS-1628 item 3 (anchoring `anchorReadback.ts`)
- **Diff.** 2 files, +54/−1: an import of `FABRICATED_TX_PREFIX` from `./honestAnchor`, the inline regex swapped for it, and one 4-cell suite. The exported regex (`honestAnchor.ts:17`) is character-identical to the removed inline copy, so production behaviour does not change.
- **Red-first on develop.** P1 and P2 RED fail on assertions (`expected 'zz1628_…' to be null`, `expected null to be 'tx_sim_…'`). P3 and P4 CONTROL pass.
- **Mutant.** M5 restores the inline regex and is killed by P1 and P2.
- **Item 6.** Anchoring on the predicted landing tree is **379/380**; the solo predicted tree is 2823f5d0, and anchoring is identical in the chained tree. The single failure is `threadTokenMint.test.ts` "parameterises mint + spend…", `Error: Could not serialize the data: Error: Unsupported type` at `@lucid-evolution/plutus/dist/index.js:272` via `applyParamsToScript` (test :71).
  - On develop it is **375/376**, with the same cell and the same error.
  - It is the BACKLOG.md:182 install-layout row (multi-pinned `@lucid-evolution/*`). Note that the string "KS-562" appears nowhere in the repo at develop (0 hits from `git grep 'KS-562'`; the BACKLOG row is found by name). I matched it by symptom, not by ticket id.
- **Rebase.** Develop's 3 merges did not touch anchoring, so R's 379/380 on the old base equals my landing figure.

### #1596 KS-1595 item 1 (test only)
- **Diff.** 1 file, +128 (`ks1595-gdpr-connector-context-reaches-the-service.test.ts`, 7 cells).
- **Red-first.** It is a pin, so all 7 cells pass on develop's code, as expected for a test-only PR. Its bite was measured with mutants on `routes/gdpr.ts` `connectorContext` (:468-479), all killed:
  - G1, tenantId and organizationId swapped: R1, R2 and R3 red.
  - G2, organizationId always undefined: R1 and R2 red.
  - G3, always null (`|| req`): R1, R2 and R3 red.
  - G4, the `connector:` prefix strip removed: R1 and R3 red.

  G1-G3 are the gate's three mutants from the PR 1543 gate. My first G3 form failed ts-jest type-check (file error, not a kill), so I re-ran it in a type-safe form.
- **Suite.** The solo predicted tree (9845efd3) gives originate **1449/1449**. R's 1412 was measured on the old base. Develop's moves add 37 originate cells (develop is 1442 now). This is inferred from the delta: I did not run 83ed01af.

### #1598 KS-1471 (api-gateway `middleware/auth.ts`)
- **Diff.** 2 files, +101/−1. The only product line is :275, `path: req.path` → `req.baseUrl + req.path`, inside `refuseConnectorBearer`'s `logger.warn` metadata.
  - The 401 status, the body and the control flow are untouched. Both callers (:300 front door, :481 `authenticateToken`) are untouched. **No authorisation decision changes.**
  - CONTROL L4 (401 UNAUTHORIZED, names x-api-key) and L5 (a human Bearer gets 200) pass on both trees.
- **Red-first.** L1 and L2 fail on develop (`expected [ '/abc' ] to deeply equal [ '/api/credentials/abc' ]`). L3, L4 and L5 pass.
- **Mutants.**
  - M6, back to `req.path`: killed by L1 and L2.
  - M6b, `req.originalUrl`: killed by L2 (the query-string token).
- **Suite.** api-gateway on the landing tree is **1111/1111** (develop 1106 + 5), which matches R.

### #1599 KS-805 (auth)
- **Diff.** 4 files, +137/−2:
  - `routes/oauth.ts:1301` `UpdateOAuthAppSchema.redirectUris` gains `.min(1)`.
  - `auth.openapi.ts:2900` gets the same.
  - `secuura-api.yaml`: `git diff --numstat` gives `1 0`. The single line is `minItems: 1` under `/api/oauth/apps/{id}` `patch`.
  - One suite, 7 cells.
- **No authorisation decision changes.** It is body validation only. `authenticate()` and the ownership checks are untouched, and C1 and C2 still reach `updateApp`.
- **Red-first on develop.** R1 fails (`expected 200 to be 400`) and R2 fails (`expected true to be false`). C1-C5 pass.
- **Behaviour on the landing tree:**
  - PATCH `redirectUris: []` → 400, and `updateApp` is not called (R1).
  - An omitted field → 200 (C2).
  - One URI → 200 (C1).
- **Mutants:**
  - M7, `.min(1)` removed from the route: killed by R1 and R2.
  - **The bite as the brief asked:** M8, `.min(1)` removed from `auth.openapi.ts`, makes `generate-openapi --check` **rc=1** ("CHECK FAIL: generated YAML differs").
  - M9, the yaml `minItems` line removed: also rc=1.
  - Baseline control on the landing tree: rc=0 ("CHECK PASS"). `check-spec-examples` is rc=0 in all three runs.
- **Suite.** auth on the landing tree is **1068/1068**, which matches R. My first run gave 1059/1060 plus 2 file errors, because the suite was run with cwd outside the service: ks1009 "could not locate the Dev root" and ks949. With cwd = service dir it is 1068/1068. That was environmental, not the PR.
- **Is it the whole of KS-805?** It cannot be determined from the repo.
  - The string "KS-805" appears ONLY in this PR's new test. Control: `KS-822` hits 12 times in the yaml at the same ref.
  - That test's header calls this "Q5" and says Q3 was closed by KS-822. Q1, Q2 and Q4 (if they exist) are not visible.
  - The repo's `2_Project_Files/5_Project_History/history.md` has 0 hits for KS-805, but also 0 for the control KS-1634, so that search proves nothing.
  - A wider read-only grep of `Blockchain/5_Project_History/` did hit archived seat histories, e.g. `2026-10-10_seatR-30th/history.md.before:6750`: "2. KS-805 + the KS-839 contract sentence after #922" (successor open items, 2026-09-17).
  - So KS-805 once carried a strand tied to a KS-839 contract sentence. #1599 does not mention it. That is evidence the ticket may be wider than Q5. It is not proof.
  - Linear was not read.
- **Design observation (not a defect of this PR).** The PATCH body schema is written twice by hand: `routes/oauth.ts:1299-1305` (runtime) and `auth.openapi.ts:2897-2903` (spec source). They already differ: the route trims `name` (`z.string().trim()`) and the spec does not.
  - The `check:openapi` gate ties the yaml to `auth.openapi.ts` only. Nothing ties `auth.openapi.ts` to the route.
  - Under M8 the unit suite stays green: ks805 imports only `routes/oauth`. A future drift between the route and the spec copy is caught by neither gate.
  - A single exported schema reused by the registry would close it.

## Merge prediction (`git merge-tree --write-tree`, in order, all rc=0, no conflicts)

| step | PR | tree after | solo onto develop |
|---|---|---|---|
| 0 | develop 78cb3c39 | 1ca89b2b5b7280ced0760012b09338dec94766aa | n/a |
| 1 | #1597 | b64be7e50092c55af3d6670f065c2a75601ec584 | b64be7e50092 (= head tree) |
| 2 | #1590 | e35d1d7d3bfb56ed6760b53090752220839d08b4 | 2823f5d02cb65215c5c10fc111ac77c39e62f390 |
| 3 | #1596 | 7a62bfc2bb1eb021b51eb0612c838db34d9badd9 | 9845efd3fa1b44c807ec1fd34361bb71d87af796 |
| 4 | #1598 | 8a13248d524bd3b5a89b7581f46858d93bf87f73 | 882d36d39e8d (= head tree) |
| 5 | #1599 | **d794200379ef0a675c25cfe7c3a9948864db0d7e** | 36ab32c59161 (= head tree) |

- **Files.** Pairwise shared-file count is 0 for all 10 pairs. Control: #1597 against itself gives 3. develop..final touches exactly 12 files = 3+2+1+2+4.
- **#1597 vs #1590.** They are disjoint: originate vs anchoring, no shared file. They also agree semantically. #1597 relies on anchoring's `simulated: true` marker, and #1590 keeps producing it from an identical regex: P1 pins the export path, and S1 in my probe is the shape it emits.
- **Suites on the final tree d794200.** `packages/shared` was rebuilt there (tsc rc 0, 29 dist entries):
  - anchoring 379/380 (KS-562-class cell only)
  - api-gateway 1111/1111
  - auth 1068/1068
  - originate 1461/1461

## HOW
- **Clone.** `git clone --shared` into `o1/repo`, with origin set to git@github.com:Secuura/Distributed_Secuura.git. I fetched develop and pull/{1597,1590,1596,1598,1599}/head with the master checkout's `core.sshCommand` plus `-o ServerAliveInterval=30`.
- **Worktrees.** All are inside o1/:
  - `wt-dev` (develop)
  - `wt-land` (the chained prediction commit 8fe088e8 → tree d794200)
  - `wt-1596` (the solo prediction, tree 9845efd3)
- **node_modules.** Per-entry symlinks into the master checkout's installed modules (read-only). The `@secuura/*` relative links were re-created so they resolve inside each worktree. Vitest's `.vite` cache and jest's `--cacheDirectory` land in o1/.
- **Commands.** Suites ran with jest/vitest by absolute path. The cwd was set with a python `subprocess(cwd=)` wrapper (`o1/incwd.py`); no `cd`.
- **Scripts.** All in o1/, run with /bin/bash: `s1.sh` `s2.sh` `s3.sh` (diffs and merge-tree), `wt.sh`/`wtall.sh`, `suites.sh`, `redfirst.sh`, `mutants.sh`/`mutants_g3.sh` (+`mutate.py`, `cells.py`), `probe.sh` (+`probe/o1probe.test.ts`, `cmp.py`), `openapi.sh`.
- **Clean-up.** Temporary files were removed and mutants restored by EXIT traps with literal paths. `git status --porcelain` in every worktree afterwards shows only the untracked node_modules links.
- **Self-report.**
  - A hook refused my first `git -C $VAR fetch` and a `$VAR` rm in a heredoc. I re-issued both with literal paths; nothing was bypassed.
  - A read-only background grep of `Blockchain/5_Project_History/` finished after the first draft. Its KS-805 hits are folded into #1599 above.

## NOT tested
- Linear (the KS-805 scope, KS-562 and KS-1634 ticket text). No live stack, Blockfrost or kintsugi, so 4(c) is answered from the code plus a probe with a mocked fetch, not against a real chain scan.
- R's READY mail itself (I measured against the brief's table).
- ESLint, `check:test-types`, tests/e2e and systemTest.
- #1596's 1412 on the old base (I did not run 83ed01af).
- The R3 `simulated:false` wire change was not checked against downstream consumers (anchoring never sends that shape).

## Severities (file:line)
- **Minor 1 (#1597 scope edge, not blocking):** `services/originate/src/routes/verificationV2.ts:231-239` `chainOnlyMatch` is a third chain-first presenter and does not carry `chain.simulated`.
  - On public POST /api/v2/verification/verify with a registry miss, the probe is SAME on develop and landing.
  - Reachable shape S1 (a placeholder anchor_store row): `blockchain.anchored:true`, no simulated marker. This is the half of L6 that #1597 fixes on v1.
  - Unreachable today: S2 and S3 give `checks.isAnchored:true`.
  - Wants a follow-up ticket.
- **Minor 2 (pre-existing, both v1 and v2):** the chain-first blobs hard-code `anchored: true` and drop anchoring's `status`/`acknowledged`. A reply with `status:'submitting', acknowledged:false` (the KS-726 class) is presented as `isAnchored:true` (probe R5, the same on both trees).
  - Sites: `verification.ts:716-724`, `:1259-1267`, `verificationV2.ts:232-239`.
  - Not introduced by any of the five PRs.
- **Nit 1 (#1597):** both `ks1634-*.test.ts` headers and every cell title say "KS-1628 L1/L6", not KS-1634 (:1-8, :96-141).
- **Nit 2 (#1590 neighbour, out of its item):** originate keeps its own copy of the regex, `services/originate/src/routes/verification.ts:52` `FABRICATED_TXHASH_RE`, beside the exported `services/originate/src/services/anchorHonesty.ts:28`. This is the same drift class item 3 removes in anchoring.
- **Nit 3 (#1596):** cells R1-R3 are labelled RED but are green on develop, by design for a test-only pin. Their bite is the mutants above.
- **Observation (#1599):** the route and spec schemas are hand-duplicated (`routes/oauth.ts:1299`, `auth.openapi.ts:2897`). See above.

MODEL: claude-opus-5-5
WALL-CLOCK: 18 minutes (11:41:04 -> ~11:59 AEDT)
