VERDICT: GO WITH NOTE (tier 1 batch, round 1 of 2; develop 9207fe336797b136f3f12fb6da169fba7fd900b7; #1630 GO WITH NOTE, #1631 GO, #1632 GO WITH NOTE; 0 blockers, 7 notes)

model: claude-opus-5-5 -- G1 (tier 1 batch: an auth scope widening, an API-key fail-closed parse, an anchor-heal guard) -- P1-P4 no -- gauge 51%

- **#1630 KS-1653: GO WITH NOTE.** Head `19bb05069f03c8b6e9c35a2e0960cb3030dcf289`. Landing tree alone on live develop `9207fe336797`: `74fe7c1a407919f36c71a33bf769ffb94cfd2748` (on the brief's develop `88b8ceb9f304`: `8de20974a299`, equal to the author's).
- **#1631 KS-1639: GO.** Head `40ab71dd0fec5543722fedae2c5b5c5cd3d85ac1` (commit 1 `8d1dde1a5444` is the Spark's, commit 2 is the seat's cell F4). Landing tree alone on live develop `9207fe336797`: `5fcabf38d42ba6481fa08564a67b670de16eb4b5` (on `88b8ceb9f304`: `0653cef42825`, equal to the author's).
- **#1632 KS-1661: GO WITH NOTE.** Head `77e5c5472534b6e4c817890640c4a0f6da291705`. Landing tree alone on live develop `9207fe336797`: `4ed63efdde4a29c58d319352eb216928b6448185` (on `88b8ceb9f304`: `fc1cd1546a96`, equal to the author's).
- **Stack in order 1630, 1631, 1632 on live develop `9207fe336797`:** `29f134c4d9e5d45bc3da52fc1c19847c69e917f4` (on `88b8ceb9f304`: `198e44b77a54`, equal to the author's).

## BLUF

All three heads match the brief and stayed unchanged from 14:56Z to 15:18Z. **Develop moved during the gate**, from `88b8ceb9f304` to `9207fe336797`: #1634 (KS-1658) and KS-1673 m365 landed. Neither touches a batch file, and I re-took every tree and re-ran all three suites on the new head. The suites on the real stacked merge are green. Compared by cell name on the new head: auth 1,089 to 1,095, security 354 to 361, originate 1,518 to 1,523. Every service is +N new cells only, with 0 vanished, 0 non-passed and 0 status changes. Each PR reds first on develop's product file exactly as the author said, and the controls hold. No blockers. Two notes need someone to act:

- **#1630 widens the gate more than its brief says (N1).** The brief says "no other caller changes", and that is wrong. Any sk_ key that holds `documents:transfer-custody` and none of the old admitting scopes can now reach `POST /api/users/stub`, and the gateway's `/api/users` catch-all exposes that route. That covers keys minted by a tenant admin or a provisioning key. No minter gains a capability, because each could already mint `certifications:write`.
- **#1632's neighbour-guard count is at least 11, not 7 (N4).** The four `settled`/`failed` guards also survive the whole originate suite when the mutant compiles. The author's "six pinned elsewhere" most likely includes compile-error false kills: ts-jest TS6133 "declared but never read". I reproduced that mechanism. KS-1676 should be widened. This does not block #1632.

## Findings

No blockers.

**N1 (#1630) - the widening, enumerated.** Holders of `documents:transfer-custody` today:
- (a) Platform S's per-org connector key, minted by api-gateway `routes/platform.ts:592` `S_CONNECTOR_SCOPES`. It also carries `certifications:write`, so it is admitted before and after with no change.
- (b) Any sk_ key minted through security `POST /api/keys` (`index.ts:1161`). The `scopes` field is a free-form `z.array(z.string())` (`index.ts:665`). The minters are the `KEY_ADMIN_ROLES` (SYSTEM_ADMIN, SUPER_ADMIN, ORG_ADMIN, ISSUER_ADMIN, ADMIN; `index.ts:1099`) and provisioning connector keys (`organizations:register`, non-escalating scopes only; `provisioningPolicy.ts:97-114`). Originate's `/api/admin/api-keys` forwards here.
- Not holders:
  - Interactive tokens: `getDefaultScopesForRole` gives only OWNER `documents:write` (`packages/shared/src/security/scopes.ts:287`).
  - OAuth tokens: `AVAILABLE_SCOPES` does not offer the scope, which the KS-855 R2 table pins.
- The connector token carries the key's stored scopes verbatim (`auth/routes/internal.ts:72`, `jwt.ts:281`).

**Answer:** yes, a class of holder gains access. A (b) key with `documents:transfer-custody` and none of `*`, `users:*`, `users:read`, `users:create`, `certifications:write` was 403'd at `/stub` and is now admitted. It can mint or resolve INVITED stubs in its own tenant directly, not only through originate's transfer-custody, which already forwards the caller's bearer to `/stub` (`originate/routes/documents.ts:1591-1630`). Gateway `routes/proxy.ts:536` mounts `/api/users` for authenticated callers, so this is reachable from outside. No minter gains a capability, because every minter of such a key could already mint an admitting scope. The ticket's Recommendation (quoted in `night/briefs/ks_1653_p1/KS-1653.md`) chose exactly this change, and the diff does nothing more: one comment line plus one `if` line, zero `-` lines. The brief's sentence "no other caller changes" should not be repeated in the PR record.

**N2 (#1630) - resource wildcard not admitted (pre-existing, not widened).** `hasUsersStubScope` matches literally. A `documents:*` key passes originate's transfer-custody gate through `hasScope`'s resource wildcard (`scopes.ts:163-180`), but it still gets a 403 at `/stub`. That was true before the PR and stays true after it. The patch neither causes nor fixes it. Flag it if KS-1653's intent was "whoever may transfer custody may mint the holder".

**N3 (#1630) - comment placement (cosmetic).** The new two lines sit between the KS-564 comment block and the `certifications:write` return that block explains. The block now reads as if it explained the KS-1653 line. This could go in the comments-only follow-up the author already owes.

**N4 (#1632) - neighbouring unpinned guards: 7 confirmed, plus at least 4 more.** I ran compile-safe mutants against the WHOLE originate suite, 1,515 cells. The unmutated control was green.

- **Survived, matching the author's seven:**
  - v1 stored `blob.simulated` (`verification.ts:432`)
  - v1 stored tx shape (`:434`)
  - v1 incoming `verified !== true` (`:455`, mutated to `!chain`)
  - v1 incoming tx shape (`:455`)
  - v2 stored `simulated` (`verificationV2.ts:130`)
  - v2 stored tx shape (`:132`)
  - v2 incoming tx shape (`:137`)
- **Also survived (not in the author's seven):** v1 `settled` off (`:435` to `false as boolean`), v1 `failed` off (`:436`), v2 `settled` off (`:133`), v2 `failed` off (`:134`).
  - The `failed` pair is behaviour-relevant. Neither call site pre-filters (`verification.ts:802,1324`, `verificationV2.ts:192`). So an `anchor_failed` blob with a real tx and a confirming chain reply would be presented as `confirmed`, and `persistHealedAnchor` would write it.
- **Killed:**
  - v1 attribution (`sameTx || sameDoc || true`): killed by `ks584-verify-row-selection` "different registration".
  - v2 attribution: killed by `ks584-p3-verify-list` "DIFFERENT registration".
  - v2 `fetchChainFact` `verified === true` (`:111`): killed by the CONTROL "KS-1634 v2: a reply whose verified is not true makes no match".
- **The false-kill mechanism, reproduced.** My first pass removed `settled ||` and `failed`, set the attribution to `true`, and deleted the v2 attribution line. Each left a local unread. ts-jest then failed 35 suites (v1) or 24 suites (v2) with `TS6133 'settled' is declared but its value is never read` (log `logs/mut/N03-v1-settled.json`). A run like that looks like a kill and is not one.
- The author's "six others pinned elsewhere" names no mutant text, so I cannot prove which of the six were false kills. But my compile-safe count leaves only three neighbouring guards pinned (two attribution, one v2 `verified`), against the author's six.
- KS-1676 (filed by the author) should list the `failed`/`settled` pair on both paths. **Not a blocker for this PR.**

**N5 (batch) - develop moved mid-gate.** At 15:16Z live develop was `9207fe336797`. Since `88b8ceb9f304` it has added `05ad5d3ac` (#1634, KS-1658: `originate/src/utils/idNamespaceCollision.ts` plus a test) and `9207fe336` (KS-1673: m365 `index.ts`, its openapi, and `docs/openapi/secuura-api.yaml`). There is no file overlap with the batch. The author's trees and my `88b8ceb9f304` trees match, but they are no longer the landing trees. **Merge against the `9207fe336797` trees above, re-taken at the real head.** The new originate base (1,518) and stack (1,523) were run on this head.

**N6 (environment, not the PRs).**
- (i) My first security develop run in parallel returned rc 1 while its JSON said `success: true`, 354/354. It did not reproduce in two re-runs (rc 0 both) and is unexplained.
- (ii) `auth/ks1009-wallet-status-reveals-only-existence.test.ts` finds the Dev root from `process.cwd()`. Run from any cwd outside the tree, it load-fails on BOTH develop and stack (8 cells). It is green when vitest runs with cwd at the service (`tools/vt.mjs` uses `process.chdir`, not a shell `cd`). All counts above come from the cwd-at-service runs.
- (iii) `npm ci` of `packages/shared` failed on the `blake2` native build. `npm run build` (tsc) of `packages/shared` still ran rc 0, and the suites resolve against the root workspace install.

**N7 (#1631) - M8 survives by design, as the author said.** On the non-string branch, `Boolean(x)` mutated to `x === true` passes all 7 cells. It differs only for numbers and objects, which node-postgres never delivers for a `BOOLEAN` column. The ticket's deny-list snippet (`!/^(f|false)$/i`) is killed by F3, F4 and N1.

## Per-PR questions, answered

**#1630:**
- **Callers and holders:** N1.
- **Diff does nothing more than the Recommendation:** yes. `git diff develop...pr` shows `users.ts` +2/-0 and the new test file +108.
- **Spark patch byte identity:** `runs/spark_secuura_2026-10-20_ks_1653_p1/out.md.checker/patch.diff`, applied with `git apply --cached` on parent `46e4343a5312`, gives `8d30ad068224`, which equals the head's tree.
- **Red-first:** with develop's `users.ts`, S1 and S2 fail and 4 cells pass.
- **C1 is the admission-half red:** `return scopes.includes('certifications:write')` to `return false` reds **exactly C1** (1 of 6).
- **Other mutants:**

| mutant | cells red |
| -- | -- |
| drop the new line | S1, S2 |
| new line admits `documents:write` | S1, C3 |
| new line returns false | S1, S2 |
| drop `users:read` | C2 |
| empty scopes admitted | C4 |
| admit everything | C3 |

  Eight mutants, eight killed, unmutated control 6/6.

**#1631:**
- **Real string `is_active` paths: none.**
  - `rowToApiKey` has three callers: `index.ts:519` (revoke lookup, `SELECT * FROM svc_api_keys WHERE id = $1`), `:570` (boot loader, `SELECT * FROM svc_api_keys`) and `:1855`/`:1878` (validate, `SELECT * FROM security_find_api_key_by_hash($1)`, which returns `SETOF svc_api_keys`).
  - The column is `BOOLEAN` in every definition I read: `018_svc_api_keys_reconcile.sql:77`, gateway `startup-migrations.ts:434`, `002_verification-tiers.sql`.
  - The cache (`memApiKeys`) holds mapped `ApiKey` objects, not rows.
  - A grep of `services/security/src` for `is_active::text`, `row_to_json`, `to_json(`, `json_agg` and `jsonb_build_object` finds 1 hit, the new test's comment. Positive control: `::text` occurs 5 times in `index.ts`, so the instrument sees casts.
  - The only string fixture is `row-converters.test.ts:226` (`'t'`), which stays green.
  - No `setTypeParser` is registered.
- **F4's anchor mutants, run myself:**

| tests in place | M6 (drop `^`) | M7 (drop `$`) |
| -- | -- | -- |
| commit-1 test file alone (6 Spark cells) | survives, 0 red | survives, 0 red |
| head test file (with F4) | reds exactly F4 | reds exactly F4 |

  Dropping both anchors also reds exactly F4.
- **Red-first:** develop's `converters.ts` with the commit-1 file gives 3 failed / 3 passed (F1-F3). With the head file it gives 4 failed / 3 passed (F1-F4).
- **Fail closed:** `''`, `'maybe'`, `null` and an absent column read inactive (N1, F3). Real booleans are unchanged (B1).
  - Making `''` active reds N1.
  - Making the non-string branch `true` reds B1 and N1.
  - Dropping `.trim()` reds T1, and dropping the `i` flag reds T1.
- **Spark patch identity:** applied on `46e4343a5312`, it gives `58b6f8432b0f`, equal to commit 1's tree. Commit 2 touches only the test file (+6).

**#1632:**
- **Both hunks confirmed, and the guard is TRUTHY:** v1 `:455` adds `chain.simulated ||`, v2 `:130` adds `|| chain.simulated`, with no `=== true`.
  - Mutating either guard to `=== true` reds exactly H3.
  - Dropping v1's guard reds H1 and H3; dropping v2's reds H2 and H3.
  - Inverting v1's guard reds C1, H1 and H3; inverting v2's reds C2, H2 and H3.
- **Red-first:**
  - Both develop files: H1, H2 and H3 fail, C1 and C2 pass.
  - v1 only: H1 and H3.
  - v2 only: H2 and H3.
- **No `index` lines:** `grep -c '^index '` counts 0, against 3 `diff --git` headers as the control. `git apply --cached` of the canonical `patch.diff` gives `8d8c2228afd7` on `46e4343a5312`, equal to the tip's tree. On `88b8ceb9f304` it gives `fc1cd1546a96`, equal to the merge-tree landing.
- **Neighbour count:** N4.

**Batch:**
- **File-disjoint:** the three-dot diffs touch 2, 2 and 3 files with no overlap: `auth/routes/users.ts` plus its test; `security/converters.ts` plus its test; originate `verification.ts`, `verificationV2.ts` plus its test.
- **Merge-trees:** each merges clean (rc 0) on both develops, and the stack merges clean on both (real `git merge --no-ff` in a scratch worktree). Trees are listed at the top.
- **Suites by cell name:** see the BLUF and the table below.
- **New test files type-check:** `tsc --noEmit` of each new test file under its service tsconfig gives rc 0 with 0 errors, for auth, security and originate (with jest types). Positive control: adding a file with `const x: number = "..."` gives rc 2 and 1 error. Neighbour control: `ks1129-heal-persists-a-number.test.ts` type-checks rc 0 under the same config.
- **Load-average timeouts:** none in any of my runs. All auth, security and originate stack cells passed, so 0 failure messages contain "timed out". Load was 10 to 22 on 28 cores. `ks578-ks643-revoke-authorization` alone gives 11/11 and `ks949-platform-admin-seed-identity` alone gives 31/31. The slowest single cell was 2.9 s, under the 5 s limit.

## What was tested and how

- **Clone:** `git clone --shared` from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` into `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a3368218-953e-40df-ac8f-2e5abee5552f/scratchpad/gate_at1/repo`. Its `core.sshCommand` was set to the cache clone's value. I fetched `refs/pull/{1630,1631,1632}/head` and `develop` into `refs/gate/*` and re-read heads by `ls-remote` at start (14:56Z) and end (15:18Z).
- **Worktrees:** `gate_at1/base` (develop) and `gate_at1/stack` (develop plus `merge --no-ff` 1630, 1631, 1632), each with its own `npm ci --prefix <tree>/Blockchain/Dev` and its own `npm run build --prefix .../packages/shared`.
- **Runners:** every vitest and jest run is `node <tree>/Blockchain/Dev/node_modules/<tool>` through `gate_at1/tools/vt.mjs` and `gate_at1/tools/jt.cjs` (`process.chdir` to the service, absolute `--root`/`--rootDir`). Nothing ran from the Wednesday cwd.
- **Comparison:** JSON reports were compared per cell (file plus full name) by `gate_at1/tools/cmp.py`.
- **Mutants:** planted by line number with a one-occurrence assertion by `gate_at1/tools/mut.py` (`mut.py.v2` keys by file plus full name). Each was restored with `git checkout`, and the harness asserted `git status` clean after each one. The stack worktree is clean at its final tree, `29f134c4d9e5`.
- **Logs:** `gate_at1/logs/`.

Suites, compared by cell name. The develop columns are the develop baseline; the stack columns are develop plus the three PRs.

| service | develop `88b8ceb9f304` | stack `198e44b77a54` | develop `9207fe336797` | stack `29f134c4d9e5` |
| -- | -- | -- | -- | -- |
| auth | 1,089 (98 files) | 1,095 (99) | 1,089 (98) | 1,095 (99) |
| security | 354 (32) | 361 (33) | 354 (32) | 361 (33) |
| originate | 1,510 (126) | 1,515 (127) | 1,518 (127) | 1,523 (128) |

Every column is all passed, rc 0, 0 skipped, 0 vanished, and every new cell belongs to its PR.

## NOT RUN

- Integration suites (`*.integration.test.ts`, DB-backed) and anything needing Docker or a live stack: no Docker by rule.
- Preflight legs 3, 4 and 8.
- No server, GitHub or Linear reads or writes beyond `git fetch` / `ls-remote`.
- The Linear ticket text was not read. KS-1653's Recommendation was taken from the Spark brief's verbatim quote.
- The author's own mutant scripts were not available, so N4's comparison to their "six" is inferred.
- `tsc --noEmit` of the whole services; only the new test files were type-checked.
- The open-PR census; I did not repeat the author's.
- No live request through the gateway for N1. Reachability is from source (`proxy.ts:536`, `authenticate.ts:94`).
- No running mutant for the N4 `anchor_failed` behaviour beyond the surviving `failed`-guard mutants.

Wednesday tree check (`git -C /Volumes/DevMASTER/WEDNESDAY status --short`, run before writing this file): untracked paths are all under `0_Brain/` (two other gates' `verdict.md` files and this folder). None is outside the allowed roots.
sha256: e5184f8e4c659546730c74282f81aa0682cf4c7db36004d15ed4c1174f91eb3d
