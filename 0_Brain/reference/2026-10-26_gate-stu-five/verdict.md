# QA gate, tier 2 batch, round 1 of 2 under the cap: five Secuura Platform K test-hardening PRs (Seats S 1st, T 1st, U 1st)

Gate: Sonnet, findings-only. Nothing pushed, merged, commented or fixed; no `!CODING` checkout touched (builders' evidence folders read only); Linear read only. One disposable container run for #1705 only, removed, lists proven identical.

Readings of origin (`git ls-remote origin`), develop `fee13f25d574cdbac32601cbe0176f7b6622fa57` and all five heads, branch/ref beside each:
- start 18:00 AEDT: `refs/heads/develop` fee13f25d574, `refs/pull/1701/head` b90a2c174f53, `1702` 7db575457780, `1703` 2c0df6dbd485, `1704` 0da23c8f3952, `1705` 68b498fe4d55. All equal to Wednesday's 17:59 read. No STOP.
- mid 18:01 (the fetch into my clone): the same six SHAs (`rev-parse` of the fetched refs).
- end 18:24:04 AEDT: the same six SHAs. Every verdict below is about the head named in it and expires if that ref moves.

## BLUF

| PR | Ticket | Seat | Head (verified) | Verdict | One line |
|---|---|---|---|---|---|
| #1701 | KS-1713 | S 1st | `b90a2c174f53c4a1131ad8c5d4aad1eb850dbeb0` | GO WITH NOTES | Re-run: M3 (`/api/webhooks` auth line deleted) RED on the new test, GREEN on the old; 15 mutants (9 builder's, 6 mine) all behave as the PR says; the judgement calls (a throw is not a refusal, only 401 counts) fail in the loud direction. Minors: a header-presence-only guard is still credited; two allowlist entries are unpinned or source-only. |
| #1702 | KS-1635 | S 1st | `7db575457780a96d224874d517a25cfd99876034` | GO | Red reproduced exactly (field only removed: service tsc rc 2, ratchet rc 1, 40 = 27 + 13 new). Green: tsc 0, ratchet 0 with 27/27 and 0 new, api-gateway 1176/1176 and 121 files before AND after, eslint 0 errors, `enforcement.ts` byte-identical to develop's. |
| #1703 | KS-1602 | T 1st | `2c0df6dbd4859d4c8e1e22781179fd236ddfeaa7` | GO WITH NOTES | The red/green reproduces with a control that can fail (warm develop: default and 500 ms pass, 200/100/1 ms fail with the `close` TypeError; fixed: all pass). Planted-throw copy: develop 2 errors, fixed 1. Notes: the ticket's other two faces (5 s walk cell, ECONNRESET) are not touched, so KS-1602 must stay open; the control is cache-state dependent. |
| #1704 | KS-1566 | U 1st | `0da23c8f3952adc64f5bdab8eba6cd808e9448ff` | GO | G6 (cap 1000) survives the old file 33/33 and is killed by exactly the new cell; so are caps 9 and 7. Jest originate suite 1655 -> 1656, 140 suites, 0 failed. |
| #1705 | KS-1578 | T 1st | `68b498fe4d5583503c672788f98b3e7acde3cb46` | GO WITH NOTES | Ran against a real migrated Postgres. The four mutants (key/query `startsWith`, key/query `includes`) all survive the old 18 cells and each is killed by exactly one new cell; inverted-equality control 13 of 20 red. Minor: `endsWith` (suffix) variants of the filter survive all 20 cells. |

Counts: GO x2 (#1702, #1704), GO WITH NOTES x3 (#1701, #1703, #1705), NO GO x0. No class here has an earlier NO GO, so nothing is near the cap.

**Combined tree.** Develop `fee13f25d574` + the five heads, merged by real `git merge --no-ff` in one worktree: rc 0 each, no conflict (merge commit tree `18400f260f3b`). `git merge-tree --write-tree` develop+each head: all five rc 0 and each tree id equals the real merge's; all ten pairs rc 0; the five PRs touch 20 distinct files, no file twice. On the combined tree: api-gateway vitest 1180/1180, 121 files (1176 develop + 4 from #1701; #1702 changes no count); `tsc --noEmit` rc 0; ratchet rc 0 with 27 errors, 27 in the baseline, 0 new.

**Recommended merge order** (no technical dependency; all conflict-free in any order): 1. #1702 first, because it has the widest footprint (16 files, 14 of them test files other seats may still touch), so merging it early shrinks the window in which a parallel branch can conflict. 2. #1701. 3. #1704, 4. #1703, 5. #1705 (single-file test additions; #1705 last only because its proof needs a database and so is the one a reader can least cheaply re-run). Each PR says `Refs`, not `Closes`, and that is right for all five: see the per-PR notes for which tickets stay open. Pre-merge boxes are unticked by the builders on purpose; the PR bodies and the pre-push result (13 of 16 legs, legs 3, 4 and 8 skipped, "not a pass") are the builders' own statements, which I did not re-run (see NOT TESTED).

## Method notes that apply to all five

- Runner: `spark_gate.sh` is pytest-only, so I ran every suite directly: `vitest run` (api-gateway, security), `jest` (originate), `tsc --noEmit`, the repo's `scripts/typecheck-tests/check.cjs`, `eslint`. Said once.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_stu_five_20261026/`. `dev` = develop `fee13f25d574`; `mg1701`..`mg1705` = develop with each head merged by a real merge (`mg1701` later also took the other four merges and became the combined tree; all #1701 single-PR results were taken before that). Substrate: `git worktree add` from the cache clone (refs `refs/gate/s5-*`), `node_modules` and `packages/shared/dist` APFS-cloned (`cp -c -R`) from the previous gate's install (`gate_r2_nine_20261026/dev`). That install was built from the lockfile at `28e2d27de337`; I checked that `package-lock.json` is unchanged and that `packages/shared`, `services/security` and `services/originate` source are unchanged between `28e2d27de337` and `fee13f25d574` (the only api-gateway changes are two test files). `dist/index.js` asserted present in all six trees. Not a fresh `npm ci`.
- No `cd`: every command ran with cwd set by a `perl chdir` wrapper (`rin.sh`) writing `scratch/<label>.out` and a `.meta` line carrying the exit code on its own line.
- Every mutation preceded by an anchor-count assertion (`== 1`), followed by a "bytes differ from the original" assertion, restored by writing the original bytes back and asserting the sha256 (scripts: session scratchpad `mut1701.py`, `mut1705.py`, `k1703.sh`, `k1704.sh`, `r1702.sh`). `git status` clean in every tree afterwards except my own untracked scratch, which I moved to `scratch/_quarantine_20261026/`.
- Load: heavy suites started at load1 under 12 (full api-gateway 4.7 to 5.2, security full 10.7, originate jest 8.8 / 9.4; the latter climbed to 17.5 during its run from other seats). One heavy run at a time.
- Linear read-only (comments first:50, sorted client-side, key sourced per command, never printed). `gh` is not logged in here, so I read the PR bodies from the seats' folders (`PR-body-*.md`, `PR-BODY-KS-1566.md`, `pr/KS-*_pr_body.md`), not from GitHub. Claims in them were challenged, not used as evidence.
- Evidence class: everything is MEASURED AT RUNTIME unless marked READ ONLY.
- Logs: `.../gate_stu_five_20261026/scratch/` (`*.out`, `*.meta`, `mut1701/*.json`, `mut1705/*.json`, `mut1705_dev.log`, `mut1705_mg.log`, `pg/`).

---

## #1701 KS-1713 `b90a2c174f53` (Seat S 1st): GO WITH NOTES

**FOUND**
- Diff vs merge-base `28e2d27de337` read whole: one file, `services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts` (+205 / -37). `proxy.ts` and `admin.ts` untouched. Matches the ticket's ask (a mount that lost `authenticateToken(true)` must not be rescued by another guard's refusal) and answers its "not enumerated" line.
- Mechanism: for each non-final handler, two probes: 401 to a headerless request, and 401 again when `req.user` is already the most privileged principal (`probeGuard`, `answers401`, `verifiesCredentialItself`, ks570 test lines ~200-250). A guard that only reads `req.user` (`requireScope`, `requireScopeOrRole`) waves the second probe through and stops counting. Two tightenings beyond the ticket's literal ask, which the seat flagged for a ruling: a throw is not credited, and only 401 counts.
- The two judgement calls, challenged: both change the predicate only in the fail-closed direction (they can turn a mount RED that was green; they cannot turn a RED green). The one risk is a false RED later if a legitimate new gateway-local guard answers 403 to a missing credential: the failure message tells the author to add authenticateToken or an allowlist entry, so it is loud and local. Controls that prove it: P1 below (loosening 401 to >= 400 is killed by exactly the "throw, 403 and 404 are not authentication" cell) and P3 (crediting a throw is killed by the same cell and the stale-entry cell). I judge both acceptable as shapes. Priority is Wednesday's.
- Minor M-1 (design limit, READ ONLY plus mutant G6 below): a guard that only checks that an `Authorization` header EXISTS (it never validates it) passes both probes and is credited. This is inherent in "does the guard read the credential itself" without recognising names, and `requireAdmin` is the only real guard of that class; the PR does not claim otherwise, but its test comment says "verifies". Fix-shape: none needed now; record the limit in the comment, or probe with a malformed header as a third question. Regression test: G6's shape should go RED if the third probe is added.
- Minor M-2: allowlist entries are source-read, as the entries say ("READ FROM SOURCE ... NOT probed live"). I re-read the claims against develop: `proxy.ts:1159` `/api/nft` has `authenticateToken(false)` then an inline NOT_DEPLOYED guard (reads `req.hostname.endsWith`, 404 to non-localhost callers while the URL is still the default, then `next()`); `services/nft-certificate/src/app.ts:45` mounts `jwtAuthenticate({ publicOps: ['POST /nft/verify/asset', 'POST /nft/verify/transaction'] })` on `/api`; `middleware/scopes.ts:27-30` `requireScope` 401s a missing user; `middleware/auth.ts:495` SESSION_INVALIDATED is raised on required and optional mounts (comment `:477`). All consistent with the entries (READ ONLY; no live gateway). The `/api/nft` entry is not pinned (mutant M6 stays green on old and new, as the PR says): deleting `authenticateToken(false)` from `/api/nft` is invisible. Not new, not a blocker.
- Note N-1: the doc comment at ks570 test line 264 still says "48 `/api/admin/*` routes"; the PR body says 39 are registered. I counted 39 (below). Pre-existing wording, left in place by the PR.
- Note N-2: this PR deliberately records, not tightens, that `/api/certifications` and `/api/nft` lack `authenticateToken(true)`; that stays with the open half of KS-736.

**TESTED / HOW (controls)**
1. Counts. ks570 file: develop 5 tests, merged 9 (+4, as stated). Full api-gateway vitest: develop 1176/1176, 121 files (1175 at the PR's base plus #1699's L5 cell that landed since); with #1701 merged 1180/1180, 121 files (`full_gw_dev.json`, `full_gw_mg1701.json`).
2. Both files in ONE invocation (new test and a byte-identical copy of develop's test as `ks570-oldcopy.test.ts`, `shasum` equal to develop's), unmutated control: 2 files, 14 passed (5 + 9). Then one product-file mutant at a time, new vs old:

| mutant (anchor count 1, landed, restored by sha256) | new test | old test |
|---|---|---|
| M3 `/api/webhooks` `authenticateToken(true)` deleted | RED (names `/api/webhooks`) | green 5/5 |
| M1 `/api/stake` `(true)` -> `(false)` | RED | RED |
| M2 `/api/stake` line deleted | RED | RED |
| M4 `/api/certifications` `authenticateToken(false)` deleted | RED (pin cell: "no longer carries authenticateToken(false)") | green |
| M5 `/api/certifications` `requireScope` deleted | RED (pin cell) | RED |
| M6 `/api/nft` `authenticateToken(false)` deleted | green | green |
| M7 `/api/documents` auth deleted | RED | green |
| M9 `erase-connector` auth deleted | RED | green |
| G1 `/api/users/lookup` auth deleted (mine; builder did not mutate it) | RED (names it) | green |
| G2 `POST /api/anchors` auth deleted (mine) | RED | green |
| G3 `POST /api/anchors/batch` auth deleted (mine) | RED | green |
| G4 `/api/documents` `(true)` -> `(false)` (mine) | RED | green |
| G5 `/api/webhooks` auth swapped for an inline guard that only checks `req.user` (mine, the M3 shape in another coat) | RED (names `/api/webhooks`) | green |
| G6 `/api/webhooks` auth swapped for an inline guard that 401s only when the header is absent (mine) | green (credited; M-1) | green |
| A1 `admin.ts`: `requireAdmin` removed from `GET /api/admin/document-types` | RED, 2 cells (sweep names the route; real-admin-cell) | green |

   I read why each RED is red from the JSON failure messages (M3, G1, G3, G5, A1: "Unauthenticated /api mount(s) with no recorded reason: <the mutated mount>"; M4: the pin cell's own message), not only the count.
3. Predicate mutants on the test file itself (own cells' teeth): P1 401 loosened to >= 400: killed by "a throw, a 403 and a 404 are not authentication" only; P2 privileged probe dropped: killed by the M3-shape cell (and stale-entry); P3 a throw credited: killed by the throw/403/404 cell (and stale-entry); P4 `/api/nft` allowlist entry removed: killed by the unexplained-mount cell and the stale-entry cell; P5 `/api/certifications` entry removed: three cells.
4. Enumeration re-derived (the ticket's "not enumerated"): a scratch copy of the PR's test with a dump cell: of the 109 mount/route groups the test builds, 48 carry the injected `authenticateToken(true)` identity, 39 are credited by leg 2 (`selfVerifies`), 87 authed. The 6 that refuse an anonymous caller yet also carry identity are exactly the PR's list (`/api/webhooks`, `/api/users/lookup`, `/api/documents`, `erase-connector`, `POST /api/anchors`, `POST /api/anchors/batch`); the 2 that refuse (or throw) without identity are `/api/certifications` (optional auth + `requireScope`) and `/api/nft`. The 39 are all gateway-local admin-router groups (including `/api/security/audit` and `/api/users/admin/*`, which live in the same router). Reproduced, not taken from the body.
5. tsc rc 0, ratchet rc 0 (27 in baseline, 0 new), eslint on the file rc 0; eslint control: a planted `debugger;` in a copy gives rc 1 (see #1702).

## #1702 KS-1635 `7db575457780` (Seat S 1st): GO

**FOUND**
- Diff read whole: 16 files, +6 / -37. `routes/verification.ts`: the `meetsVerificationLevel` field AND its 14-line "DEAD ... KEPT, deliberately ... Tracked as KS-1635" doc comment removed together (15 lines; right, the comment becomes false). `index.ts`: the name leaves the import (`enforceDocumentTypeRules`, `createWorkflowInstanceIfRequired` stay) and the call. 14 test files stop supplying it; six now-unused imports go with it; `ks1176` keeps its import because it still calls the function. The ticket's list of 14 test names matches the diff's 14 exactly.
- Repo-wide `git grep -c meetsVerificationLevel` on the merged tree: `enforcement.test.ts` 10, `ks1176` 13, `services/enforcement.ts` 2; nothing else. On develop it was also in `index.ts` 2, `routes/verification.ts` 2 and 12 other test files. Two other files reference `createVerificationRoutes` (`ks529-non-object-body-guard.test.ts`, `packages/shared/.../ks781-p3-3-body-parser-order.test.ts`) and neither mentions the dep, so nothing is left supplying it.
- `services/enforcement.ts` and `__tests__/enforcement.test.ts`: `cmp` rc 0 against develop's (the function is untouched; `:54` declaration and `:153` call survive).
- Note N-3 (READ ONLY): no test boots `index.ts`; the `createVerificationRoutes({...})` call in `index.ts:904` is covered by `tsc` only (the red below shows tsc does see it). That is adequate for a dropped required field.

**TESTED / HOW (controls)**
1. Control: develop unmutated: service `tsc --noEmit` rc 0, ratchet rc 0 (27 errors, 27 in baseline, 0 new).
2. RED, reproduced: in the develop tree remove ONLY the field and its comment from `VerificationRouteDeps` (anchor asserted, restored by `git checkout` and sha256): service `tsc` **rc 2**, one error `src/index.ts(904,65) TS2353`; ratchet **rc 1**, "40 errors: 27 in the baseline, 13 new" (TS2353 on `meetsVerificationLevel`: `index.ts` + 12 tests). Zero lines mention `routes/verification.ts` in either output, so nothing in it reads the dep. The two `ks1185` tests are named by neither check (variable, not a fresh literal), exactly as the PR says: they are caught only by the grep above.
3. GREEN on the merged tree: `tsc` rc 0; ratchet rc 0 ("27 errors: 27 in the baseline, 0 new; 0 stale"); `scripts/` untouched so the baseline is unedited.
4. Counts: full api-gateway vitest develop 1176/1176, 121 files; merged 1176/1176, 121 files (`full_gw_dev.json`, `full_gw_mg1702.json`); no count change, as a pure removal predicts.
5. eslint on the 16 files rc 0 (2 warnings, `index.ts` 117:3 `no-namespace` and 929:7 unused disable, both on develop at those lines); control: a planted `debugger;` in a copy of ks815 gives rc 1 (`no-debugger`).

## #1703 KS-1602 `2c0df6dbd485` (Seat T 1st): GO WITH NOTES

**FOUND**
- Diff read whole: one file, `services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts` (+10 / -1): `const HOOK_BUDGET_MS = 60_000` passed as `beforeAll`'s last argument, and `afterAll` returns when `server` was never assigned (`let server: Server` at `:91`). Matches ticket fix shapes 1 and 2; the PR says plainly it does not take shape 3 or the move to the integration config. `vitest.config.ts` untouched (no `hookTimeout`).
- Minor M-3: the ticket's other two faces of the same root cause are untouched, and the PR says so: the repo-walk cell at `:521` ("CONTROL: the scan REACHES the deployment surface") still runs on the 5 s test default, and the ECONNRESET at `:597`. I measured the walk cell at 979 ms here on a warm, quiet box (`sec_full_mg1703.json`), so it has about 5x headroom today and none under real fleet load. KS-1602 must therefore stay open (the PR already says `Refs`), or be re-scoped; KS-1734 (nine more files with the same 10 s hook) is the PR's own follow-up. Evidence class: MEASURED for the 979 ms, READ ONLY for what happens under load.
- Note N-4: a genuinely wedged hook now waits 60 s before the file reports. The PR states the trade; fine.
- Note N-5: the control the PR describes ("500 ms passes") is cache-state dependent; see below. Not a PR defect, but a reader who re-runs it cold will see a different table.

**TESTED / HOW (controls)**
1. Warm develop tree, the file alone: default 21 passed; `--hookTimeout=500` 21 passed; `200`, `100`, `1` each **1 file failed, 21 skipped**, `Hook timed out in <n>ms` followed by `TypeError: Cannot read properties of undefined (reading 'close')`. Merged tree: default, `1`, `100`, `200`, `500` all 21 passed (the per-hook budget beats the CLI override on vitest 4.1.12, as the PR says). The flag is a working control: it changes the develop outcome only below the hook's duration (0.2 to 0.5 s warm).
2. COLD state, honest disagreement with the PR's table, explained: my FIRST develop runs (first import into a fresh tree's transform cache) failed even at `--hookTimeout=500`, because the cold hook exceeds 500 ms; the merged tree's first run took 15 s wall and passed because the explicit budget is 60 s. After one warm run the develop table reproduced exactly. So "the hook takes 0.2-0.5 s" is a warm figure; cold it is longer than 0.5 s. This is a strengthening of the PR's case, not a contradiction.
3. Scratch copies (each created by an asserted edit, moved to quarantine afterwards): `beforeAll` throws on its first line: develop copy **2 errors** (the planted one, then the `close` TypeError), merged copy **1 error** (the planted one only). A real lapse through the fixed code (budget set to 1 ms in a copy): 1 error, "Hook timed out in 1ms", no TypeError. Mutant: afterAll guard removed from the fixed copy + the throw: the TypeError returns (4 error lines), so the guard is what removes it. Mutant: budget removed from the fixed copy (guard kept) + `--hookTimeout=1`: lapses at 1 ms with one error, so the budget is what rescues the real run. Each half of the fix is therefore needed and independently demonstrated.
4. Counts: whole `services/security` unit suite, develop and merged: 33 files, 361/361, 0 failed, 0 skipped, both (`sec_full_dev.json`, `sec_full_mg1703.json`; the PR claims no suite-level change, and none appears).
5. eslint on the file rc 0 (control rc 1 shown under #1702, same config).

## #1704 KS-1566 `0da23c8f3952` (Seat U 1st): GO

**FOUND**
- Diff read whole: one file, `services/originate/src/__tests__/ks1557-trusted-certification-evidence.test.ts` +7: a comment and one cell `expect(MAX_EVIDENCE_LOOKUPS).toBe(8)` directly after the cap cell. `MAX_EVIDENCE_LOOKUPS` is exported from `routes/verification.ts:257` (`= 8`) and the test already imported it. Matches the ticket's fix shape (the first of its two alternatives; the PR explains why a separate cell). No finding.

**TESTED / HOW (controls)**
- Unmutated: develop file 33 passed, merged 34 passed. Mutants of `routes/verification.ts:257` (anchor count 1, landed, restored, `git status` clean), develop's file vs the PR's:
  - cap 1000 (the gate's G6): develop **33 passed, survives**; merged **1 failed, 33 passed**, the one failure is the new cell by name.
  - cap 9: develop survives; merged 1 failed (the new cell). cap 7: develop survives; merged 1 failed (the new cell).
  - cap 1 (control that the old file is not blind to everything): develop already RED on the certifiedBy cell; merged RED on that cell and the new cell.
- Full originate jest suite: develop 140 suites, **1655** passed; merged 140 suites, **1656** passed; rc 0 both. Same as the PR's 1655 -> 1656 on the newer base.
- eslint on the file rc 0 (control rc 1 on a planted `debugger;` copy). `tsc` does not cover this file (originate's tsconfig excludes `__tests__`); ts-jest compiling it is its type check, as the PR says.

## #1705 KS-1578 `68b498fe4d55` (Seat T 1st): GO WITH NOTES

**FOUND**
- Diff read whole: one file, `ks1553-key-list-normalises-organisation-id.integration.test.ts`, +20: two cells in the organisation-arm block. Each mints the own key, asserts the EXACT id lists it (in-cell control), then asserts status 200 and that the near-miss lists nothing: the first 8 characters of `ORG_OWN`, and `ORG_OWN` + `x`. The product line under test is `services/security/src/index.ts:1486` `.filter(k => wantedOrg !== null && normaliseOrgId(k.organizationId) === wantedOrg)`, untouched.
- The ticket's count (17) vs the file (18 on develop, 20 with the PR): confirmed 18 and 20, as the PR says.
- Minor M-4: suffix-match variants of the filter survive. My mutants G1 (key `endsWith` query) and G2 (query `endsWith` key) leave all 20 cells green. The ticket asked for exactly the prefix and appended-character cells, and the cells deliver that, so this is not a defect of the PR against its ticket; it is the residue. Fix-shape (for the owner, if wanted): a third near-miss using the LAST 8 characters of the id and a fourth with a character PREPENDED. Evidence class: MEASURED AT RUNTIME. Severity Minor; the product code is correct today.
- Note N-6: prefix-with-8-characters also matches other organisations' ids in the fixture set (they share `abcdef00-`), which is fine here because the assertion is about the own key.
- Substrate source (per the template's rule): the stack built from `docker-compose.yml`'s `postgres` service, image `postgres:15-alpine` read from it (`docker image inspect` ok, no pull), initdb scripts mounted from `docker/init` (read-only, as the compose does), then `scripts/run-migrations.sh` over `migrations/` (the runner the deploy uses). I did not compare `docker/init/01-schema.sql` against `migrations/` (the 2026-09-07 KS-949 trap): the cells here are not schema-sensitive beyond `svc_api_keys`, whose FORCE RLS and the app role's flags I read back (below), but the disagreement between the two sources, if any, is neither reported nor ruled out.

**TESTED / HOW (controls)**
1. Container (the one allowed): `gate-stu-ks1578-pg`, 127.0.0.1:55433, `postgres:15-alpine`, throwaway credentials generated at run time into a 0600 file under `scratch/pg/` (never printed; the app password differs from the compose default). Start gate: anchored `pgrep -fl '^/bin/sh [.]githooks/pre-push'` was non-empty from 18:00 until about 18:22 (another seat's push); my start loop waited, and started at 07:22:59Z (18:22 AEDT) with the pgrep empty and load1 3.33. Port probe 0 listeners (and its control, `:22`, 0 listeners: that control cannot prove the probe works, since sshd is not listening here; the container bound without error, which is the real proof). Migrations: runner "applied=57, failed=0"; tracker rows read independently 57; the last file (`055_ks1557_backfill_...`) applied (1); the app role `secuura_app super=false bypassrls=false`; `svc_api_keys` `relforcerowsecurity = t`. A guard polled `docker ps` and load every 15 s (peak load1 5.4, slowest `docker ps` 1 s; no trigger).
2. No-DB refusal (control): the PR's file with no DSNs: rc 1, "need a MIGRATED Postgres", 20 tests skipped by the refusal design (it does not silently pass).
3. Untouched develop file: **18 / 18**. Merged: **20 / 20**, twice.
4. Mutants of `index.ts:1486`'s equality (anchor count 1, mutation landed, restored by sha256), the develop 18 cells vs the merged 20 cells:

| mutant | old 18 cells | new 20 cells |
|---|---|---|
| CTL equality inverted (`!==`) | 11 red (7 pass) | 13 red (7 pass): the 11 plus both new cells |
| A1 key `startsWith` query | 18/18 green (survives) | 1 failed: the 8-character prefix cell only |
| A2 query `startsWith` key | survives | 1 failed: the appended-character cell only |
| B1 key `includes` query | survives | 1 failed: the prefix cell only |
| B2 query `includes` key | survives | 1 failed: the appended-character cell only |
| G3 first 8 characters equal (mine) | survives | 2 failed: both new cells |
| G1 key `endsWith` query (mine) | survives | **20/20 green (survives)** |
| G2 query `endsWith` key (mine) | survives | **20/20 green (survives)** |

   The reds name the new cells, so the filter is reached with both queries (the ticket's worry that the arm refuses first does not apply). The inverted-equality control proves the tamper takes effect and the harness sees failures.
5. Teardown: `docker container remove --force --volumes gate-stu-ks1578-pg` at 07:23:51Z. `docker ps -a` names: before **228**, after **228**, `diff` empty; `docker volume ls -q`: before **738**, after **738**, `diff` empty; `:55433` listeners 0; no `gate-stu` container remains. The two dead credential files (0600) are left in `scratch/pg/` (never deleted); the container they belonged to no longer exists. I touched no other container, image or volume (no prune); the 228 pre-existing containers belong to other seats and were not touched.
6. eslint on the file rc 0 (control rc 1, see #1702).

---

## NOT TESTED (first-class output)

- The real pre-push hook and its 16-leg preflight on any head: not run. The builders' "13 of 16 legs ran, legs 3, 4 and 8 skipped, not a pass" is their statement; I did not reproduce it. Legs 3, 4, 8 need a local stack; none was stood up.
- Schemathesis, Akto, Playwright, k6: not run (test-only PRs, no stack; #1702 is a type-level removal). No running gateway/service anywhere: every claim about `/api/nft` and `/api/certifications` behaviour on the wire, and the nft-certificate service, is READ ONLY from source.
- GitHub side: PR bodies read from the seats' folders, not from GitHub (`gh` not logged in); checks, mergeability, review state, and the comment text on GitHub not read.
- Node: all runs on Node v26.8.1 (the seats' own warning; the LTS 24 line is not installed). Nothing was run on Node 24.
- A fresh `npm ci` of each tree: I cloned the previous gate's install (lockfile and the three services' source verified unchanged since its base). Not the cold-after-`npm ci` state where KS-1734's hook lapses appear; #1703's cold-whole-suite behaviour with the fix is therefore NOT TESTED (the PR also says not run).
- #1703: the 5 s `:521` walk cell and the `:597` ECONNRESET under real fleet load (not reproduced; the 979 ms is a quiet-box figure). A by-name set comparison of the 361 tests before and after (counts equal; names not diffed).
- #1704: the real-Postgres integration file for the same rule (the ticket's G6 also survived it); not run, not touched by the PR.
- #1705: the other `*.integration.test.ts` files and the security unit suite beyond the 361 above; mutants of other lines of the list filter (the `wantedOrg !== null` guard, the tenant filter); comparison of `docker/init/01-schema.sql` with `migrations/` (see substrate note).
- #1701: a tamper inside the `erasureDoor` sub-router (invisible to the test, pre-existing); `/api/nft` and `/api/certifications` re-measured live (not done; the entries are source-read).
- #1702: no test boots `index.ts` (see N-3).
- No Linear or GitHub write of any kind.

## My own instrument errors (reported in the open)

1. **My `rin.sh` wrapper reported rc 0 on a failed `exec`.** The first two ks570 runs (`ks570_dev`, `ks570_mg1701`) printed `rc=0 wall=0s` with an empty output file, because I passed a relative `./node_modules/.bin/vitest` that does not exist in the service directory and the wrapper's `exec` failure was not fatal. I noticed the empty output and `wall=0s` before reading anything into them, added `or die` to the exec, used absolute binary paths, and re-ran both. Those two empty results were never used.
2. **Fleet hooks refused three of my calls**, each without effect on results: `git -C $VAR` write verbs (fetch, update-ref) outside a script file (moved into script files with absolute literal paths, as the previous gate also did); an unquoted `=========` separator (zsh expansion); and an `rm -f` inside a heredoc for the container guard (the whole call was dropped before running; I rewrote the guard without any deletion and used `docker container remove` for the container only). The first `linear.sh` heredoc was dropped by the same refusal, so a later call ran before the file existed ("No such file"); I re-created it and re-ran.
3. **Mutation harness anchor, caught before use.** My first `mut1701.py` matched the header `router.use('/api/documents',` in a comment too (count 2); the script asserts the count, I changed the header match to include the trailing newline BEFORE the first run, so no mutant was applied from the failed form. (I found the second occurrence by reading, not by running.)
4. **`mg1701` changed role mid-session.** I merged the other four PRs into it after all single-PR #1701 runs (mutants, full suite) were done, to make the combined tree. The enumeration dump of #1701 (item 4) and the combined-tree numbers were taken on the combined tree; the #1701 mutant table and the 1180 count were taken on the single-PR tree. `proxy.ts` and `admin.ts` are identical in both.
5. **Overwritten summary file.** The second invocation of the 1701 mutant script (predicate mutants P1 to P5) overwrote `mut1701/summary.json`; the per-mutant JSON files (`mut1701/<id>.json`) and the first run's log (`scratch/mut1701.log`) are intact, and the P1-P5 figures in this report are from that run's output.
6. **My #1705 port-probe control is weak** (see item 1 of #1705): `:22` has no listener on this machine, so it could not show the probe can read a busy port. I did not have a second proof of the probe beyond the container binding successfully.
7. **A cold-cache surprise on #1703** (first develop runs failed at 500 ms where the builder's table passes) was my own state, resolved by one warm run; I report it above as a finding about the control, not as a PR error.
8. **A zsh unquoted glob** in one read-only `grep --include=*.ts` returned "no matches found" (no effect; the files were listed another way). Load: the 1704 full jest run started at load1 9.4 and ended at 17.5 from other seats; the result was a clean rc 0.
9. I retracted nothing: no finding of mine was found wrong.

## Left on disk (not deleted)

`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_stu_five_20261026/` (worktrees `dev`, `mg1701` (combined), `mg1702`..`mg1705`, `scratch/` with logs, `pg/` scripts and the two dead 0600 credential files, and `_quarantine_20261026/` holding the scratch test copies); the cache clone gained refs `refs/gate/s5-*` and six worktree entries. About 12 GB apparent, much of it APFS-shared clone data. Wednesday or the next wrap can quarantine the work dir and prune the worktree entries.
