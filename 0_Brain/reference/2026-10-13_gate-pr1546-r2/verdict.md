# VERDICT: GO WITH NOTE — PR 1546 (KS-1032) fix round 1 DELTA, head 234fe0b0b6bb19860f7a1b183bbc315cbce7fefb · Major 0 / Minor 2 / Info 6
REPORT-HASH: sha256/16 4e98f3e1a91a1741

Gate: independent Opus QA gate, tier 1, round 2 of 2 (DELTA), commissioned by Wednesday. Findings only; nothing fixed.

**Head gated: 234fe0b0b6bb19860f7a1b183bbc315cbce7fefb.** Its parent is ad366066e620037d753f9421bcd051ad09a9a7af (the round-1 head) and its tree is e5e084b96767171c1a85194211b204408bf65a60. `git rev-list --count ad366066..head` = 1. All of these come from `git rev-parse` in a `clone --shared` in the gate scratchpad, which fetched `refs/pull/1546/head` and `refs/heads/develop` from origin.

**Develop measured: 026c2d1614065c79fc8d96007ac0d80f19fb9363** (same fetch).

`gh pr view 1546` (read-only, using the project's GH_TOKEN) reports:
- headRefOid 234fe0b0…, base develop
- OPEN, MERGEABLE
- 10 files

## Bottom line

**The delta changes no behaviour.**
- With comments removed, the code in all three non-test `.ts` files is byte-identical between ad366066 and the head. A one-token control edit changes that fingerprint.
- The non-comment lines of both env templates are identical.
- All 67 round-1 cells give the same result on the new head.

**M1 is closed in the texts the deploy seat reads.** I measured GA1, GA2 and GC5 myself, reading `data.tenantId` from the HTTP response. The body, `routes/metering.ts`, both env templates and `docs/ENVIRONMENT-VARIABLES.md` all say what I measured. The multi-tenant production 400, a static read in round 1, is now measured as well. It is true on the metering path.

**m1 is closed.** In the author's file, g2 turns only GB1 red and g5 only GB2. GB0 is a real control: a wrapper that silently puts the strip back turns only GB0 red. **m2 is closed.**

**Two Minor text residues remain:**
- **n1.** `utils/gatewayProvenance.ts` still states M1's "single-tenant answers exactly as before … measured".
- **n2.** m3 is not fully closed. `docs/ENVIRONMENT-VARIABLES.md:123` tells operators to look for a boot line that says headers are "honoured from ANY caller", and that line no longer exists. `deployment/azure/services.bicep` still says "fail-OPEN" in three places.

Both are comment or documentation text with no behaviour change, so they can be ticketed under the round cap. **Do not recommend deploying from this verdict:** the deploy waits for GATEWAY_VOUCH_SECRET per DEPLOY-BLOCKERS.

---

## MINOR

### n1. M1's false claim survives in the rationale file the boot comment points to (`services/originate/src/utils/gatewayProvenance.ts:64-73`, PR text untouched by the delta)
**FOUND.** Lines 69-73 say:

> "Blast radius, **measured rather than assumed**: with the trust headers gone the KS-458 block falls back to DEFAULT_TENANT_ID … so a SINGLE-TENANT deploy **answers exactly as before**. … where it is on, the **tenant is lost** until the secret is set."

Lines 64-66 describe the deploy gate as "check Platform-S metering end to end". They have no tenant assertion.

`index.ts:208-211` points readers here ("The full rationale … lives in utils/gatewayProvenance.ts"). This contradicts the corrected `routes/metering.ts:73-75` in the same PR, which says "holds ONLY where S's key tenant is already DEFAULT … UNMEASURED".

**TESTED (instrument: jest on the real `index.ts` through the listen-spy harness; `evidence/r2_m1_b.log`):**
- R2-GA1, secret unset, Platform-S with Bearer: **200, data.tenantId = DEFAULT**. That is not "as before"; develop gives S's own tenant (round-1 `gateA_wt_dev.json`).
- R2-GA6, secret unset, a legitimate gateway-shaped human whose JWT tenant and gateway `x-tenant-id` are T_HUMAN: **200, data.tenantId = DEFAULT**. The claim is false for every caller whose tenant is not DEFAULT, not only for Platform S. Round-1 develop control: develop honours the header tenant (GA3 on develop = 200 on the header's tenant).
- R2-MT1: multi-tenant production gives **400**, not "tenant is lost" (see i3).
- "Measured rather than assumed" is not true of the sentence it labels.

**Why Minor, not Major.** Every deploy-facing text is now correct and DEPLOY-BLOCKERS step (3) is amended (read: `0_Brain/tasks/DEPLOY-BLOCKERS.md:30`). This is a developer comment, but it is the same false sentence M1 was about.

**Fix:** rewrite lines 64-73 to match metering.ts:57-77. Ticket it or fold it into KS-1599.

### n2. m3 not fully closed: two more operator texts still describe unset as fail-open
- **`docs/ENVIRONMENT-VARIABLES.md:122-124`** (two lines below the new "Unset FAILS CLOSED" prose in a hunk the delta edited). It says: "originate logs a WARNING at boot naming the consequence (`[gateway-provenance] DISABLED — …honoured from ANY caller…`) … Check that line to know which state a box is in."
  - The head never emits that line. Its unset boot line is `[gateway-provenance] FAIL-CLOSED — GATEWAY_VOUCH_SECRET is unset, so identity/tenant/role headers are DROPPED…` (`gatewayProvenance.ts:187`; observed in this run's jest log).
  - The head's own cells assert the message does NOT contain "honoured from ANY caller" (`ks1032-unconfigured-vouch-fails-closed.test.ts:166`, `ks1041-gateway-provenance.test.ts:233`).
  - An operator told to grep for "DISABLED" finds nothing, and the doc quotes a fail-open statement as the current state.
- **`deployment/azure/services.bicep:126-128`** ("Empty is valid and fail-OPEN … Fail-closed would mean an unconfigured deploy loses every gateway-set identity"), **`:129`** (`@description` "Empty => provenance check inert"), **`:685`** and **`:823-824`** ("the documented fail-open"). The PR body says this estate was deleted on 2026-07-31, so the practical risk is low. It is still a template in the tree that contradicts the shipped behaviour.
- **Honest note:** the round-1 gate's m3 listed five sites and missed both of these. Round 1 scoped its grep; this round grepped the whole `Blockchain/Dev` tree (`evidence/item4_grep_head.txt`).
- **Fix:** correct the quoted boot line and the bicep comments. Text only.

## INFO

- **i1. Line references made stale by this commit.** `utils/requestTenant.ts:17-18` and the body's m2 block name the three writers as `index.ts:251`, `metering.ts:65` and `tenant-context.ts:91`. At the head they are **index.ts:252** and **metering.ts:83**. The delta's own comment insertions moved them, by +1 and +18 lines. `tenant-context.ts:67/:91` is correct. "`index.ts:251` (this function)" is also loose wording: that line *calls* the function.
- **i2. "401 only when the token exchange failed / the only 401 shape"** (metering.ts:69, the body table, both env templates) is narrow. **R2-GA7:** secret unset with an *invalid* Bearer also gives **401**, with the handler not run. This does not affect the deploy check, which asserts tenant.
- **i3. The multi-tenant production 400, now MEASURED** (`evidence/r2_mtprod_inband.log`, `r2_mtprod_setctl.log`, `r2_mtdev_unset.log`). Setup: real `index.ts`, `NODE_ENV=production`, `MULTI_TENANCY_ENABLED=true`, with `getTenantManager` mocked to a live-looking manager so the `extractTenantContext` block engages; the plain harness has it null.
  - **R2-MT1**, unset, Platform-S: **400 "Missing tenant context"**.
  - **Control R2-MTCTL1**, secret set and vouched: **200, data.tenantId = T_CONN**.
  - **R2-MT1 under NODE_ENV=development**: **200, DEFAULT**.

  The texts' claim is therefore true on the metering path. "On **every** request" is overstated: `GET /api` answered 200 and `/health` 503 in both the unset and the vouched states, because they are mounted before the block. The texts also file the 400 under "measured by the gate (GA1/GA2/GC5)", but round 1 never measured it. It is measured now.
- **i4. Extra mutant x1** (the no-strip wrapper ALSO restores the vouch header) **SURVIVES all 71 cells**. This is expected: the verdict is recorded before the restore, and nothing downstream re-reads `x-gateway-vouch`. The author's comment that restoring it "would be a different scenario (a caller who holds the secret)" is therefore inaccurate. Harmless.
- **i5. GB0 is a unit-level control.** It calls the wrapped middleware directly, not through the app. The in-app proof that the strip is really removed is that g2, g5, g11 and g12 turn GB1 or GB2 red. Those cells could not go red if the headers were stripped before reaching the route. Mutant x2 (the wrapper restores nothing, so the strip silently returns) turns **only GB0** red, and GB1 and GB2 stay green. So GB0 is a control that can fail, and it is the only cell that catches that case, as the author's comment says.
- **i6. DEPLOY-BLOCKERS step (3) checks Platform S only.** R2-GA6 shows that on an unset or mismatched box every gateway caller whose tenant is not DEFAULT is switched to DEFAULT, humans included. The Platform-S tenant assertion still detects the condition, because it is the same secret, so the check is sufficient. The texts just describe the blast radius as Platform-S-only.

---

## FOUND / TESTED / HOW — by brief item

**1. "No behaviour change"**
- **Delta** = 8 files, +267/-21 (`git diff --stat ad366066..234fe0b0`, `evidence/delta_stat.txt`, full diff `evidence/delta.diff`).
- **Non-test code** (instrument: TypeScript `transpileModule` with `removeComments`, sha256/16; `evidence/item1_codeonly.txt`):
  - `index.ts` fccc0f69099e4243 = fccc0f69099e4243
  - `routes/metering.ts` 33e40127363fff81 = 33e40127363fff81
  - `utils/requestTenant.ts` 5d51d79b3a5524c5 = 5d51d79b3a5524c5
  - The raw files differ. **Control:** a one-token code edit to metering.ts (`reqTenantId` preferring `req.user.tenantId`) changes the fingerprint to aac78d71d945f54d.
- **The C2 test file** is code-identical too (ed6f27331d646f26 = ed6f27331d646f26).
- **Env templates:** the non-comment, non-blank lines are identical. `.env.example` 6ff952ce801d7828 = 6ff952ce801d7828; `env.example` f124cbf61985747f = f124cbf61985747f. **Control:** planting `GATEWAY_VOUCH_SECRET=x` gives 5aa762537c45eb8a.
- **ENVIRONMENT-VARIABLES.md** is prose and one table cell.
- **Every non-test hunk is comment or text only.**
- **Round-1 cells on the new head** (jest JSON; `evidence/head_all_cells.json`): the 36 author + 4 new + 31 gate cells give **71/71**. Compared cell by cell with round 1's `gateA_wt_gate.json`, `gateBC_head.json` and `head_ks1032_ks1041.json`: **67 common, 0 differ**. GA1 again logs `200 tenantArg a0000000-…0001` and GC5 `200 a0000000-…0001`.
- **Full originate unit suite on the head:** **107/107 suites, 1337/1337** (`evidence/unit_head.json`). This matches the author's 107/1337.
- **`tsc --noEmit`:** head rc 0 / 0 errors. **Control:** a planted type error gives rc 2 / 1 error (`evidence/tsc_*.log`).

**2. M1 re-measured by the gate**
- **Gate cells:** `evidence/gate_cells_r2/gate1546r2-m1-{unset,set}.test.ts`. `getUsageSummary` is mocked to return the real function's shape `{tenantId: <arg>, …}` (`chargeEvents.ts:302`), so the number read is the HTTP `data.tenantId` an operator would assert. The JWT is mocked by name: `gate-connector-jwt` carries T_CONN.
- **Results** (`evidence/r2_m1_b.log`):

| cell | secret | request | measured |
|---|---|---|---|
| R2-0 | unset (NODE_ENV=test, MULTI_TENANCY unset) | — | control |
| R2-GA1 | unset | Bearer + trust headers, no vouch | **200, data.tenantId = DEFAULT** |
| R2-GA2 | unset | no Bearer | **401**, handler not called |
| R2-GA6 | unset | gateway-shaped human, tenant T_HUMAN | **200, DEFAULT** |
| R2-GA7 | unset | invalid Bearer | **401** |
| R2-GC1 (control) | set | correct vouch + Bearer | **200, data.tenantId = T_CONN** (so the tenant check CAN tell the states apart) |
| R2-GC5 | set | mismatched vouch, same length, + Bearer | **200, DEFAULT** |
| R2-GC5b | set | no vouch sent (gateway side unset) + Bearer | **200, DEFAULT** |
| R2-GC5c | set | mismatched vouch, no Bearer | **401** |
| R2-MT1 / MTCTL1 / MT1-dev | see i3 | | 400 / 200 T_CONN / 200 DEFAULT |

- **Texts checked against these measurements:** body "Deploy condition" block and table; `routes/metering.ts:55-77`; `.env.example:329-340`; `env.example:464-475`; `docs/ENVIRONMENT-VARIABLES.md:106-120`.
- Status, tenant, the Bearer condition and "mismatched = unset" are all correct. The 400 is not marked as a static read, but it is now measured and true (i3).
- No sentence in these texts is wrong beyond i1 to i3. The surviving wrong sentence is elsewhere (n1).

**3. m1 (the new GB cells)**
- GB0, GB1, GB2 and GB2b are **4/4 green on the head**.
- **Mutation** (instrument: `evidence/tools/mut.py`, run against all 71 cells; each mutated file is restored from a pristine copy and asserted byte-identical; baseline 71/0 and restored 71/0; `evidence/mutation_r2.log`):

| id | mutant | result | author cells red | gate cells red |
|---|---|---|---|---|
| c0 | CONTROL, comment-only | survived (correct) | 0 | 0 |
| g2 | metering verdict read removed (author-named) | killed | **GB1 only** (expected 401, received 200) | GB1, GB3 |
| g5 | index.ts KS-458 wiring reverted to the ungated read (author-named) | killed | **GB2 only** (expected DEFAULT, received 7777…) | GB2 |
| g11 (new) | metering shim accepts 'unconfigured' locally | killed | GB1 | GB1, GB3 |
| g12 (new) | index.ts call site forces the verdict to 'vouched' | killed | GB2 | GB2 |
| x1 (new, test side) | the wrapper also restores the vouch | **survived** (i4) | 0 | 0 |
| x2 (new, test side) | the wrapper restores nothing (strip back) | killed | **GB0 only** | 0 |
| x3 (new, test side) | the wrapper fakes verdict = 'vouched' | killed | GB0, GB1, GB2 | 0 |

- **The author's claims "g2 reds GB1 only, g5 reds GB2 only" are CONFIRMED** among the author's cells. The body's "16/16 across both KS-1032 files" restore is consistent: 12 + 4.

**4. m2 and m3 grep** (`git grep -n -i -E` over the whole `Blockchain/Dev` tree at the head; `evidence/item4_grep_head.txt`; controls in `evidence/item4_grep_control.txt`)
- **`fail[- ]?open`:**
  - The quoted-as-superseded control occurrences are found: `.env.example:330`, `env.example:465` and `ENVIRONMENT-VARIABLES.md:108`, all three reading "REPLACES the previous … fail-OPEN …".
  - Live hits about this secret: **services.bicep:126, 685, 823** (n2).
  - All other hits are other subsystems (RLS, Redis, rate limits, HIBP, and so on), each read.
  - **Control:** the same pattern at ad366066 finds the five round-1 m3 sites (`.env.example:329`, `env.example:464`, `ENVIRONMENT-VARIABLES.md:74`, `:106`, `index.ts:210`). All five are gone at the head.
- **`never … raw header` variants:** 0 hits at the head.
  - **Control:** at ad366066 the C2 comment hit (`…test.ts:245`).
  - At the head the only hit is the corrected C2 comment, which quotes the old claim as superseded (NOT "…").
- **`verified context`:**
  - Head: 2 hits, both quoting it as superseded (`test.ts:245`, `requestTenant.ts:15`).
  - **Control** at ad366066: 2 live claims (`test.ts:245`, `requestTenant.ts:13`).
- **`honou?red from any caller`:**
  - `ENVIRONMENT-VARIABLES.md:123` is live (n2).
  - The 3 test hits assert its ABSENCE.
- **`answers 401`:**
  - `metering.ts:52` (unvouched, no Bearer: true) and `:60` (quoting the old claim as wrong).
  - `gatewayProvenance.ts:49` and `ks1041-gateway-provenance.test.ts:24` describe the forged no-Bearer probe, which is true (GA2/GB1).
- **`single-tenant … unchanged`:** only `metering.ts:74`, which carries the corrected qualifier. The sibling claim in `gatewayProvenance.ts:71` uses other words and was found by reading (n1).

**5. Scope**
- The delta's 8 files are exactly the declared set:
  - `.env.example`, `env.example`, `docs/ENVIRONMENT-VARIABLES.md` (m3);
  - the new `ks1032-second-lines-hold-without-the-strip.test.ts` (m1);
  - `ks1032-unconfigured-vouch-fails-closed.test.ts` (the C2 comment, m2);
  - `index.ts` (m3), `routes/metering.ts` (M1), `utils/requestTenant.ts` (m2).
- Nothing outside them.
- The whole PR, `git diff --numstat 405e33a1..head`, is 10 files, which equals the `gh pr view` files list.
- **The body was read via `gh pr view 1546`** (read-only, project `GH_TOKEN`; `evidence/pr1546_body.md`), not via the author's local copy.

**6. Merge prediction against live develop 026c2d16** (`evidence/overlap_mergetree.txt`)
- The merge-base is 405e33a1. Develop moved 2 files since then (`routes/verification.ts` and the ks1119 integration test). **Overlap with the PR's 10 files = 0.** **Planted control** (`ENVIRONMENT-VARIABLES.md` added to develop's list) = 1.
- `git merge-tree --write-tree develop head` gives **rc 0, tree 5e583dcedd92ad65e37b7820cbd863b75f4e4556**.
- **Negative control:** a scratch commit f8245f48 (develop plus an edit to `.env.example:329`, a line the delta rewrites) merged with the head gives **rc 1, CONFLICT (content) in Blockchain/Dev/.env.example**.
- **On the merged tree:**
  - all author and gate cells: **80/80** (`evidence/merge_cells.json`);
  - full unit suite: **107/107, 1337/1337** (`evidence/unit_merge_clean.json`);
  - `tsc`: rc 0.
- `evidence/unit_merge.json` (1336/1337) is a **discarded run**. My two scratch mtprod cell files sat in the tree, and `ks1293-originate-suite-is-hermetic` correctly flagged them as manifest drift. That is an incidental positive control of that guard. The clean re-run is the one quoted.

## NOT tested, and whether it could hide a Major
- **No live stack, Docker or remote box.** Kintsugi and demo are unmeasured: their effective secret, MULTI_TENANCY, and whether Platform S's key tenant equals DEFAULT. This is the deploy blocker's job. It could hide a real cross-tenant usage disclosure on an unset or mismatched box. That is why the deploy waits.
- **JWT verification is mocked** (`verifyJwtRs256`). The multi-tenant run mocks `getTenantManager` and `getRequestPrisma`, so it shows the real `extractTenantContext` and index wiring, not a real tenant pool.
- **The gateway itself was not run.** Bearer plus headers together is round 1's static read of `api-gateway/src/middleware/auth.ts:419-427`.
- **The author's pre-push hook (16/16 legs) was not re-run.** KS-1599's existence and content were not read (no Linear query this round). DB-backed integration suites, Schemathesis, Akto, Playwright and k6 were not run. No Postgres was used, so no reserved port was touched.
- **Round 1's 147-route enumeration was re-run only as part of the 71 cells** (GA5, GB3, GC7, all green, so still 0 differences). It was not re-run under the new GB file's wrapper.
- **Housekeeping, not a test:** the shared Wednesday scratchpad clone at `scratchpad/repo` had its remote URL set to the same GitHub URL and gained `refs/gate/*` from my first fetch. The gate's own work used `scratchpad/g1546r2/repo`. Nothing was written in `!CODING`, nothing was pushed, and nothing was written to GitHub or Linear.

## Evidence index (`evidence/`)
- Delta: `delta.diff`, `delta_stat.txt`, `item1_codeonly.txt`.
- Cells:
  - `gate_cells_r2/` (R2-M1 unset and set, mtprod and its SET control);
  - round-1 cells reused from `../2026-10-13_gate-pr1546/evidence/`.
- Runs: `head_all_cells.json`, `r2_m1_b.*`, `r2_mtprod_inband.*`, `r2_mtprod_setctl.*`, `r2_mtdev_unset.*`, `unit_head.*`, `unit_merge_clean.*`, `merge_cells.*`, `tsc_*.log`.
  - `r2_m1.*` is a superseded first run without GA6 and GA7.
  - `r2_mtprod.json/.log` is a load failure (worker exit on the production config guard), fixed by setting REDIS_URL and ANCHORING_SERVICE_URL dummies.
- Mutation: `tools/mut.py`, `mutation_r2.log`, `mut_*.json/.log`.
- Grep: `item4_grep_head.txt`, `item4_grep_control.txt`.
- Merge: `overlap_mergetree.txt`, `tools/negctl.sh`.
- PR: `pr1546.json`, `pr1546_body.md`.

Hash recipe: delete line 2, take sha256 of the rest, keep the first 16 hex characters.
