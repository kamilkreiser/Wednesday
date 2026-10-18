# Spark screen, part 9 (2026-10-19 ~08:50-09:10 AEDT): KS-1628 follow-up L1 + L6 - census done, fix shape CONFIRMED, two briefs written and hand-proven, ROUND NOT RUN: the builder's lane guard refuses KS-1628 (two OPEN PRs attached)

By a Spark census-and-brief sub-agent for Wednesday (routing receipt: claude-sonnet-5-5, row C8, P1-P4 no, gauge 21%). Secuura only. Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write; no Linear read; no `hold_ready`. `/Volumes/DevMASTER/!CODING/Secuura/` was never written to (the node_modules links in my scratch clone point INTO it, read only).

## Pinned sha and how I read it

`f95ad12fe5c22f8d037e7139d052363422463c79` = R's sha, develop did not move. Read with `git -C <cache/src> ls-remote origin refs/heads/develop` at ~08:53, again at 09:08 (same sha), and by round.sh itself at 08:59:33 and 09:00 ("base: develop f95ad12f..."). The cache did NOT hold the object (`cat-file -t` fatal); I fetched it with round.sh's own line (`git -C cache/src fetch -q origin +refs/heads/develop:refs/remotes/origin/develop`), after which `cat-file -t` = `commit`. (The Secuura checkout itself is not a git root, `ls-remote` there fails; the cache's origin is the same GitHub remote.) The develop delta over SCREEN_8's `83ed01af70fd` is exactly #1587 and #1588 (KS-1628 1 of 3 and the precursor).

## R's two sites, re-read at the tip (`Blockchain/Dev/services/originate/src/routes/verification.ts`)

- `:712` `          if (chain?.verified) {` (inside `verificationRouter.post('/verify-file', ...)`, the `rows.length === 0` branch opened at `:704`; fetch at `:707`, no auth header).
- `:716-723` the blob: `anchored: true, network: chain.network, txHash: chain.txHash, blockHeight: chain.blockNumber, cardanoScanUrl: chain.cardanoScanUrl, confirmedAt: chain.confirmedAt` handed to `presentBlockchainHonestly`; the response then hard-codes `verified: true` (`:731`).
- `:1191` `                if (chain?.verified) {` (the `/verify` handler, STRATEGY 1, `rows.length === 0` at `:1156`; fetch `:1185` with the caller's bearer); blob `:1258-1265`, response `verified: true` at `:1271`.
- `:454` `    if (chain?.verified !== true || !chainTx || !REAL_TXHASH_RE.test(chainTx)) return blob;` (confirmStalePendingAnchor, strict, as R said). `verificationV2.ts:111` is also strict (`chain?.verified === true ? chain : null`).
- `presentBlockchainHonestly` `:54-71`: `const simulated = Boolean(b.simulated) || (tx !== undefined && FABRICATED_TXHASH_RE.test(tx));` - so a blob without `simulated` is judged on the `txHash` prefix only.

R's readings are CORRECT on every point. Site numbers are within a line of "about 712 and 1191".

## Census (step 1): anchoring's `GET /api/anchors/verify/:hash` and everything on its reply path

Route: `anchoring/src/index.ts:452` `app.get('/api/anchors/verify/:hash', ...)` -> `handleAnchorVerifyByHash` `:593-733`. No response transformer exists (the only middleware touching bodies is the request parser `express.json()` at `index.ts:253`). The body builder is `anchorReadback.ts` `buildVerifyResponse` `:99-161`.

| field | value / type | where set | file:line |
|---|---|---|---|
| `verified` | `true`, literal boolean | the one success body (DB hit `index.ts:642`, cached chain hit `:657`, fresh chain hit `:719`; all three go through `buildVerifyResponse`; the cache stores that same body, `:718`) | `anchorReadback.ts:126` |
| `verified` | `false`, literal boolean | 400 bad hash | `index.ts:597` |
| `verified` | `false`, literal boolean | 404 not found in DB, Blockfrost not configured | `index.ts:650` |
| `verified` | `false`, literal boolean | 404 cached negative scan | `index.ts:659` |
| `verified` | `false`, literal boolean | 404 Blockfrost or wallet not initialised | `index.ts:666` |
| `verified` | `false`, literal boolean | 404 no on-chain anchor | `index.ts:728` |
| `verified` | `false`, literal boolean | 500 on throw | `index.ts:731` |
| `simulated` | `true` only (the key is ABSENT otherwise, never `false`), via a conditional spread | `...(simulated ? { simulated: true, simulatedTxRef: rawTxHash } : {})` | `anchorReadback.ts:132` |
| `simulated` (the local) | boolean, true iff `rawTxHash` is a string matching `/^(tx_sim_\|mock_tx_\|mock_batch_tx_\|tx_)/` | the ONLY derivation; the `anchor_store.simulated` column is NOT in the SELECT list (`index.ts:608-634`), so this route ignores it | `anchorReadback.ts:115` |
| `txHash` | `null` when simulated, else the raw hash | `const txHash = simulated ? null : rawTxHash` | `anchorReadback.ts:116`, emitted `:131`; `cardanoScanUrl` null when no txHash `:133` |
| `blockNumber` | `number` or `null` (`toBlockNumber`, KS-1129) | `anchorReadback.ts:93-97`, emitted `:134` | |

Neighbouring anchoring routes (NOT on the path originate calls; listed because "everything it calls" was asked): `index.ts:898` `verified: !txView.simulated && anchor.status === 'confirmed'` (a boolean expression, GET /api/anchors/:id); `index.ts:1144`, `:1163`, `:1174` (POST /api/anchors/verify, `verified` false/false/true, wrapped in `data`); `index.ts:891` and `:1635` `simulated: true, simulatedTxRef` from `honestTxView` (`honestAnchor.ts:33-35`: flag true OR placeholder prefix -> `txHash: null`, `simulatedTxRef: raw`, which can be a 64-hex string, but `txHash` is still null).

Clients of the reply (who reads it): originate `verification.ts:440` (stale confirm, strict `!== true` at `:454`), `:707` (-> gate `:712`, LOOSE), `:1185` (-> gate `:1191`, LOOSE); originate `verificationV2.ts:103` (strict `:111`); api-gateway `routes/verification.ts:642` (reads `j.verified === true && !j.simulated`, SCREEN_5 brief text; out of scope).

**Plain answers.**
1. Can anchoring ever emit a non-boolean `verified`? NO. Every assignment in the whole `anchoring/src` (non-test) is a literal `true`/`false` or the boolean expression at `index.ts:898`. A string `'false'` can only reach originate from a reply that anchoring did not build (a proxy, a mock, an edited upstream). L1 is real in originate's gate and is defence in depth against anchoring, not a live anchoring bug.
2. Can it emit `simulated: true` together with a real 64-hex `txHash`? NO on this route: `simulated` is true only when the hash matches a placeholder prefix, and then `txHash` is forced to `null` (`anchorReadback.ts:116`, `:131`). A real 64-hex hash cannot match the prefix regex (it holds no `_` and does not start `tx_`). So R's "simulated + real hash" shape is not producible by anchoring either. **What anchoring DOES emit is `simulated: true, txHash: null, simulatedTxRef: <placeholder>`** - and that is the shape that matters live: at the tip originate drops `simulated`, the blob arrives at the presenter with `txHash: null` (so no prefix test fires), and the response carries `blockchain.anchored: true` with no `simulated` marker. I measured it (the RED "the shape anchoring really sends" cell fails by assertion at the tip, passes with the edit). `checks.isAnchored` is already false for that shape (`isAnchoredHonestly` needs a 64-hex string), so the user-visible damage is the `blockchain` blob and not the check; the top-level `verified: true` is unchanged by L6 (it rests on L1's gate).
3. The fix shape (strict gate; carry `simulated` into the blob) is CORRECT: `simulated` arrives under exactly that name, as a boolean, on the live reply. So I briefed.

**Controls (each fired in the same run).**
- grep census: `git grep -n "verified:\|simulated" f95ad12f -- Blockchain/Dev/services/anchoring/src` (tests excluded) returned the rows above, including the known-present positive hits `anchorReadback.ts:126` (`verified: true`) and `:132` (`simulated: true`) and `index.ts:597`; the same run produced no assignment of a string, number or variable to `verified`.
- A second control for "the loose gate is real": my new tests send `verified: 'false'` and `simulated: true` through the REAL router at the tip and FAIL by assertion (L1 answered `verified: true`), so the harness does exercise the path (it is not a silent zero), and the three CONTROL cells (real reply) pass at the tip and after.
- A grep-pattern control: `grep '[^ -~]'` for non-ASCII bytes returned 3 hits on the earlier golden (the comment em dashes at the tip) and 0 on the final goldens, so the "ASCII only" claim for the final product hunks is a pattern that can fire.

## The result (steps 2 and 3)

**Split into two briefs**: the work is 4 product edit lines (gate + inserted field, at each of two sites about 480 lines apart) + a test = 5 edit points, over the commission's 3. One brief per site, each with its own NEW jest file.

| # | site | brief dir (`local-model/night/briefs/`) | tier / rung | edit points | lint | dry-run | control | round |
|---|---|---|---|---|---|---|---|---|
| p1 | `POST /verify-file` (`:712`, insert after `:722`) | `ks_1628_l1l6_p1` (`KS-1628.md`, `golden.diff`, `spark.pins`) | code_patch, rung 2 | 3 (2 product hunks + NEW test, 142 lines) | rc 0 | rc 2 REFUSED | rc 2 REFUSED | NOT RUN |
| p2 | `POST /verify` (`:1191`, insert after `:1264`) | `ks_1628_l1l6_p2` | code_patch, rung 2 | 3 (2 product hunks + NEW test, 146 lines) | rc 0 | rc 2 REFUSED | not run (same builder) | NOT RUN |

**The blocker, verbatim (all four attempts: dry-run p1, dry-run p2, control p1, same line):**

`SPARK ROUND ks_1628_l1l6_p1: REFUSED — builder rc 2: build_input: REFUSED KS-1628 — attached to OPEN pull request(s) ['#1590', '#1589'] — a lane has it (merged/closed PRs do not refuse)`

Context lines from the builder: `ticket KS-1628 · In Progress (started) · Low · assignee=-`; attached PRs #1590 OPEN, #1589 OPEN, #1588 merged, #1587 merged. This is `night/build_input.sh:196-201`, an unconditional gate on the Linear ticket's attached PRs; the only override is `supersedes=<pr>[,<pr>]` ("this brief is its fix round / replacement") and, after that, the state gate (`:205-213`) would also need `started_ok=<reason>` because the ticket is In Progress. Neither is mine to give: `supersedes` would be a false statement (my briefs replace neither PR), and both are a ruling about R's live lane. I did not pass them, did not rename the brief to another ticket number, and did not edit the builder. **Round: none, and no rebrief counter spent.** I stopped at the dry-run, the commission's own rule being "do not brief a guess"; the briefs are not a guess, they are blocked by a harness gate.

What the two open PRs actually touch (read from the PR heads, fetched into the cache as `refs/spark-l1l6/pr1589` and `pr1590`): #1589 (`53cb4ec76`, "Refs KS-1628 (PR 2 of 2): retire the public POST /api/documents/:id/verify") = 30 files, api-gateway `routes/verification.ts` and `index.ts` and `middleware/audit.ts`, `originate.openapi.ts`, tests, systemTest; **NOT** originate `routes/verification.ts`. #1590 (`68270e124`, "Refs KS-1628 item 3: anchorReadback reads placeholders through the exported FABRICATED_TX_PREFIX") = `anchoring/src/anchorReadback.ts` (+3/-1) and one new test; **NOT** originate. So there is NO file overlap between my briefs and the open PRs; the refusal is purely the ticket-level lane rule. (#1590 does edit `anchorReadback.ts`, the file my census cites; it only changes how the placeholder prefix is referenced, line 115's behaviour is the same.)

## Hand-proved (before any brief was written)

Both new test files were run in a scratch clone at the tip (`jest`, from the Secuura checkout's node_modules via links, `--rootDir` instead of `cd`):
- p1 file at the tip: 3 failed / 3 passed (the 3 RED by assertion, the 3 CONTROL green); with its two edits: 6 passed.
- p2 file at the tip: 3 failed / 3 passed; with its two edits: 6 passed. Both sets of edits together: 12 passed, no cross-talk.
- The first draft was one 11-cell file; `tsc` under ts-jest refused it for p1 (`TS6133` unused `HASH` in the verify-file variant: the `noUnusedLocals` that the checker's A7 would also have hit), found and fixed before the briefs were written.

## Briefs: contents

Header: `File:` verification.ts, `Test file:` the new test, `Tip:` f95ad12f..., `Runner: jest`, `Tier: code_patch`, `Rung: 2`; written 08:58-09:00 AEDT from `date`. Sections filled: Scope (narrows: this site only; "Refs KS-1628, does NOT close it"; census facts), The mode, What is wrong, Where (every line, "must change" bold), The exact change (2 hunks, `git diff -U1`, ASCII, byte-exact), The test (given whole), Red cells, Cells and controls, UNMEASURED, Collision, Output. Pins: `tier=code_patch`, `ref=.../ks563-certified-vs-anchored.test.ts` (the harness copied: real router on a real listener, `jest.mock` of `../db`, `../middleware/auth`, `@secuura/shared` via `helpers/sharedModuleMock`, `../repositories/documentRepo`; the anchoring call answered through `global.fetch`, the test's own calls through the saved real fetch), `line=712` / `line=1191`, `ctx=65536`.

The golden for p1 (`ks_1628_l1l6_p1/golden.diff`, product hunks `@@ -711,3 +711,3 @@` and `@@ -722,2 +722,3 @@` then the new file) and for p2 (`@@ -1190,3 +1190,3 @@` and `@@ -1264,2 +1264,3 @@`) were each generated from a clone at the tip with only that site applied.

### Red cells and controls (exact titles; `verify-file` in p1, `verify` in p2)
- RED KS-1628 L1 verify-file: a string "false" verified is not a verified reply
- RED KS-1628 L6 verify-file: simulated true with a real hash is not on-chain
- RED KS-1628 L6 verify-file: the shape anchoring really sends (simulated true, txHash null) is not on-chain
- CONTROL KS-1628 verify-file: a real hash, a positive integer height and verified true are verified and on-chain
- CONTROL KS-1628 verify-file: simulated false on a real reply stays on-chain
- CONTROL KS-1628 verify-file: a boolean false verified is not a verified reply
- (p2: the same six with `verify` in place of `verify-file`)

## Run dirs / artefacts

- No round run dir. Builder-refusal dry dirs (round.sh's own): `local-model/spark/state/dry/ks_1628_l1l6_p1_20261019-085940`, `.../ks_1628_l1l6_p2_20261019-090001`. Control-attempt run dir (refused, empty of a verdict): `local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1-control`.
- Dry-run/control outputs: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/spark_l1l6/dry_p1.out`, `dry_p2.out`, `control_p1.out`.
- Scratch folder (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/spark_l1l6/` (`clone/` the tip clone with both fixes applied and the two test files, `gen.py` and `mkbrief.py` the generators, `golden_p1.diff`, `golden_p2.diff`, `_old/` the superseded 11-cell draft file).

## To run the rounds once Wednesday rules (nothing else is needed)

    bash local-model/spark/round.sh local-model/night/briefs/ks_1628_l1l6_p1 --dry-run supersedes=1589,1590 started_ok="<reason>"
    (then --control with the same pins, then the one real round; same for p2)

The pins are Wednesday's to choose (and arguably wrong: `supersedes` claims a replacement). The cleaner routes are (a) a NEW Linear ticket for L1/L6 so the briefs can be renamed `KS-<new>.md` (the lint and builder key on the file name), or (b) waiting until #1589 and #1590 merge and passing `started_ok`. If either happens, the briefs need only the filename and the `Refs` line changing.

## Things Wednesday should read before holding (choices not in the commission)

1. **I split into two briefs and made two test files** (commission asked for one brief and one test file): 4 product edit lines + 1 test is 5 edit points, over the 3-point cap, and the two sites are about 480 lines apart so they cannot share a hunk. Two rounds would follow, one per brief, if you want both; I treated "ONE real round" as per brief.
2. **I added a cell the commission did not name**: `RED ... L6 ...: the shape anchoring really sends (simulated true, txHash null) is not on-chain`, because the census shows the real-hash shape cannot come from anchoring. The commissioned real-hash cell is kept (defence in depth). Drop the third RED cell if you want exactly R's shape; the product edit does not depend on it.
3. **The L6 edit is `simulated: chain.simulated,`** (a verbatim copy, key present as `undefined` when absent), not `simulated: chain.simulated === true`. The existing presenter rule is `Boolean(b.simulated)` (KS-1628's own ruling), so a string `simulated` would count as simulated (fail closed). I left that to the presenter as the commission said and did not assert it.
4. **The gate is `chain?.verified === true`** (not an early-return `!== true`), the smallest edit, matching `confirmStalePendingAnchor` and `verificationV2.ts:111`.
5. **The L1 cells assert the fall-through answer**, `body.verified === false` and no `blockchain` key (the handler's not-in-registry / not-found answer), not a particular status or message; both handlers return that shape on the miss path in the harness (measured in the test run).
6. **Hunks are `git diff -U1`** (1 context line each side) so no context line carries non-ASCII (the em dashes in the neighbouring comments at `:714` and `:1256`). The `-U3` form had three non-ASCII context lines.
7. **Not done because the gate stopped me**: control PASS (p2), the byte-identical/TREE-IDENTICAL golden verdict, the real model rounds, checker lines. None is claimed.
8. **I fetched two PR heads into the cache** (`refs/spark-l1l6/pr1589`, `pr1590`; a fetch into Wednesday's cache, not the Secuura checkout) to answer "do the open PRs touch my files". They can stay; `git -C cache/src update-ref -d` would remove them (not done; I do not delete).
9. **The refusal rests on the builder's live read of Linear/GitHub** (`GH_TOKEN` and the Linear key in the Secuura `.env`, read by the builder, not by me). I read no ticket text and have no Linear/GitHub read of my own for KS-1628; I did not look for an existing follow-up ticket for L1/L6.
10. Both sites are on KS-1628's file (`routes/verification.ts`), Seat R's surface, and the file has changed twice in the last day (#1587, #1588). Open-PR overlap on that file beyond the two attached PRs: NOT checked.

## NOT measured
- No model call, no checker run (A2a..A7), no whole-originate-suite run, no tsc run beyond ts-jest's per-file compile of the two new tests.
- No query of anchoring's DB or a live service; the census is source-only at the tip.
- The api-gateway reader (`routes/verification.ts:642`) was not re-read this session; its shape is quoted from the SCREEN_5 brief.
- Whether KS-1628 has a separate L1/L6 ticket: not looked up.


## Re-key to KS-1634 and rounds (09:12-09:25 AEDT, on Wednesday's instruction after the L1/L6 ticket was filed)

**Re-key.** `night/briefs/ks_1628_l1l6_p1` and `_p2`: `KS-1628.md` renamed (mv) to `KS-1634.md`. Edited only: the `# ` title line, the DRAFT line ("KS-1634 (the filed L1/L6 follow-up of KS-1628)"), the Scope "Refs KS-1634, does NOT close it", and ONE sentence appended to "What is wrong" (R's sharpening: the presenter's only two simulated signals are the placeholder txHash and the `simulated` flag; anchoring removes the first at `anchorReadback.ts:116`, the site drops the second, so neither file looks wrong alone; both sites return top-level `verified: true` / `status: 'anchored'` as literals, so the honesty marker is the only load-bearing field). Product hunks, test file and cells UNCHANGED (cell titles still say KS-1628 because the test files are byte-for-byte the proved ones). Remaining "KS-1628" mentions in UNMEASURED/Collision (the lane) left alone. I did not read the ticket (no Linear reader of my own); the builder read it.

**Lane guard:** passed for KS-1634 (no refusal). develop re-read before the rounds: `f95ad12fe5c22f8d037e7139d052363422463c79`, did NOT move. `tunnel.sh check` UP before each round.

| step | p1 verify-file | p2 verify |
|---|---|---|
| brief_lint | rc 0 | rc 0 |
| dry-run | rc 0 (`state/dry/ks_1628_l1l6_p1_20261019-091328`, 119383 B) | rc 0 (`state/dry/ks_1628_l1l6_p2_20261019-091347`, 119311 B) |
| CONTROL | CONTROL-PASS, golden BYTE-IDENTICAL, 83 s, `runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1-control-r2` | CONTROL-PASS, golden BYTE-IDENTICAL, 70 s, `runs/spark_secuura_2026-10-19_ks_1628_l1l6_p2-control` |
| ONE real round | **PASS**, 144 s round, 69.891 s model, 35212+2122 tokens | **PASS**, 154 s round, 69.388 s model, 35216+2132 tokens |
| run dir | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p1` | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1628_l1l6_p2` |
| golden | **DIFFERS** (see below: two path lines only) | **DIFFERS** (same) |
| rebrief | none spent | none spent |

(The earlier refused control left `..._p1-control` empty; the passing one is `-control-r2`.)

### Checker lines, verbatim (both rounds identical in shape; p1 / p2 differ only in the counts shown)
- `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/verification.ts , Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts }`
- `PASS A3b every must_change site the ticket names is changed by the product hunk (1 site(s))`
- `PASS A3c every '+' line the brief adds is in the product hunk (2 line(s)), and no tip line is re-added as a '+' (A3d)`
- `A3i: ... OK 2 line(s) byte-exact incl. leading whitespace (of 2; 2 line(s) added by the apply)`
- `PASS A4 RED-FIRST: src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)`
- `PASS A5 GREEN-AFTER: ... passes with the product hunk (6 passed / 6 run)`
- `INFO control cell present: 3 cell(s) passed BEFORE and 6 AFTER (the harness reaches the code both times)`
- `baseline: total=1442 failed=0 | after: total=1448 failed=0` ; `NEW reds: []` ; `PASS A6 whole services/originate suite: no NEW red vs the untouched tip`
- `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- p1: `SUMMARY files=2 +144/-1 ... red_first=yes apply_mode=strict` ; p2: `SUMMARY files=2 +149/-1 ...`
- `RESULT: PASS (7/7)` ; `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=1)` ; `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

### The golden "DIFFERS", and the one thing Wednesday must read before holding
`diff` of each model patch against the brief's `golden.diff`: exactly TWO lines differ per patch, the new test file's `diff --git` line and its `+++ b/` line. **The model named the new test file `ks1634-a-simulated-anchor-verified-by-hash.test.ts`, not the path the brief gives** (`ks1628-l1l6-verify-file-...` / `ks1628-l1l6-verify-...`). Cause, measured in `input.json`: the builder's `suggested_test_file` is derived from the KS-1634 ticket title, and the model took that over the brief's `Test file:` line (the brief path appears in the input too, once). Every other byte (product hunks, the whole test body) equals the golden. The checker passes because A3 takes the test set from the patch. **Both rounds therefore create the SAME file path**: p1 and p2 cannot both be applied as they stand (the second would collide on a new file). Classification: **brief/harness interaction, not a model fault** (the model followed an instruction present in its own input; the content is byte-identical to the proved golden). Fix for whoever applies them: rename one test file (or merge the two into one) before raising; or add `test_file=`-style pin and rebrief (not spent). The first brief's golden for the product is unaffected.

Also: the model's patches were NOT read line by line beyond the golden diff above (`diff` is the evidence); no READY written, nothing held, raised or pushed.
