# Gateset 2026-10-05_gate54a — README for Wednesday

Drafted 2026-10-05 AEST. The work ran 2026-10-04 13:34Z – 14:02Z UTC; times come from `date -u`. Each figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate54a is a T1 gate over ONE Secuura/Blockchain PR: #1374, KS-1402.** The PR is titled "accept a connector token on the users lookup route". Seat B 57th is its author and merger.
- **Head:** `aa16f3256dbf86e654076a31ace1eb1b79a31e69` on `feature/ks-1402-lookup-accepts-connector-token-b55-1`.
- **Base:** develop `e6daa806e79a14a580f064db95e797c1fd671dc7`, which is PR 0 / #1373's squash. Its tree `3a55f42e9f84` == gate54f's END_TREE, so PR 0 landed exactly as gated.
- **Authority:** Kam's card `secuura-ks1402-lookup-refuses-connector-tokens` = **a** (live board 2026-10-02 09:58:39 AEST).

**Status: KIT COMPLETE, NOT LAUNCHED.** Two things are Wednesday's: the routing line (section 4) and the launch (section 5).
- The dry run against #1374's real head returns **rc 0** (repin_dryrun_ex1.out, 13:59:46Z – 14:00:30Z).
- Both instruments agree. The census shows 0 OVERLAP. The SIM launcher `--check` returns rc 0.
- The only thing the dry run reports is the missing routing line.

**What the drafter did:**
- It wrote only into this directory, with ONE exception, set out next.
- In `/Volumes/DevMASTER/!CODING/` it ran only these git verbs: `ls-remote`, `show`, `log`, `ls-tree`, `cat-file` (including `--batch`), `rev-parse` and `diff`. `lib_gate54a.git` refuses any other verb.
- External reads were GitHub REST GETs only: #1374, its files, the open-PR census and one compare inside `--check`. GH_TOKEN was read by name and never printed.
- It did not launch, add the routing line, send mail, post a comment, change a ticket, fetch, clone, create a worktree, install, run vitest / tsc / check:openapi, or delete anything.

**🔴 ONE WRITE OUTSIDE THIS DIRECTORY, BY THE DRAFTER'S OWN EXERCISE: an EMPTY directory `/Volumes/DevMASTER/!CODING/Secuura/x` (created 2026-10-04 13:48:19Z).**
- **Cause:** the first `guard_out` in `c2_cells_gate54a.sh` ran `mkdir -p` BEFORE its prefix test. The refusal control `c2_outrefusal_ex1` (rc 2) therefore created the directory it then refused.
- **Fix:** the prefix test now runs on the lexical path before any `mkdir`. `c2_outrefusal_ex2` (rc 2) asked for `…/Secuura/x2`, and `ls` proves `x2` was NOT created. `c5_spec_gate54a.sh run` has the same order.
- **What remains:** the directory is empty. The drafter did NOT remove it (never delete), so removing it is Kam's or Wednesday's call.

## 1. Drafter predictions on #1374 at aa16f3256dbf
The gate re-derives each of these at the head it pins. They are all READ ONLY, from git objects plus the API.

| check | file | result |
|---|---|---|
| C1 pin | pred1374_c1.out | **PIN PASS 12/12** (details below this table) |
| C2 behaviour | c2_plan_ex2.out | **PLAN OK only** (details below). **No install, vitest, tsc or mutation was run** (section 6). |
| C3 security (static) | pred1374_c3.out | **C3 STATIC PASS 5/5** (details below) |
| C4 docs §4 | pred1374_c4.out | **C4 DOCS PASS 10/10** (details below) |
| C5 spec (static) | pred1374_c5.out | **C5 STATIC PASS** (details below). **`check:openapi` was NOT run.** |
| C6 not covered | pred1374_c6.out | **6/6** (details below) |
| census | gh_census_ex1.out (13:39Z), repin_dryrun_ex1.api.out (14:00Z) | 21 other open PRs, **0 OVERLAP**, 0 co-tenants open yet (PR B and Seat D's PR not raised at 14:00Z), #1360 reported as client-human |

**C1 pin:**
- Both instruments read `aa16f3256dbf`. The PR is open and unmerged, mergeable True / unstable. Its one parent is develop; ahead 1, behind 0.
- API files == numstat == the 5 paths, matching the builder's +333/-4 path by path.
- 0 trailers; control `bf277eead268` prints 1.
- Only KS-1402 is hyphenated in the title, body, branch and commit. `Refs KS-1402` is present. The de-hyphenated context keys are KS 1402, 480, 564 and 739.
- **PR 0's 4 paths are absent** and blob-equal (control `88e8877a2a0d..e6daa806e79a` lists 4).
- Modes are 100644 (control 100755).
- **END_TREE `082190611d1f871a579b7fa1fb8e64959da53f4f`**; develop's tree is `3a55f42e9f84`.

**C2 behaviour (plan only):**
- The test is new: rc 0 at head, 128 at base. It has 4 cells.
- It has **3 module mocks** (logger, userRepo, session) and **0 of `../middleware/authenticate`**.
- It makes 1 `generateConnectorToken(` call and has 0 `type: 'access'` in its code lines.
- users.ts:266 reads `authenticate()` at base and `authenticateAccessOrConnector()` at head.
- tsconfig excludes `src/__tests__`.

**C3 security (static):**
- Over 724 registrations in 382 files: connector-admitting routes are {POST /stub} at base and {GET /lookup, POST /stub} at head, all in users.ts. There are 0 wholesale `.use` mounts.
- 44 → 43 plain-authenticate() routes, and the only one moved is GET /lookup.
- `authenticate()` body and jwt.ts are byte-equal.
- The users.ts code delta is 1 line. The /lookup handler body (75 lines) is byte-equal, with 7 of 7 gates present.
- The authenticate.ts code delta is the label line plus `route: req.baseUrl + req.path,`. There are 0 `originalUrl` in code lines; the must-hit control finds 122 elsewhere.

**C4 docs §4:**
- SKILL.md blob `eaf43dfd4d98`, with all 3 clauses.
- 2 of 2 docs changed, 0 platform-s.
- Each doc has ONE insert hunk (+108 and +28) and 0 removed lines. Each block carries KS 1402, opens with a heading and has balanced divs.
- The 3 timing lines are all dated and name a host.
- The timing grep agrees with the builder: 0 / 0 for each of the four terms; control `auth` 52 / 59.
- **D6 passes on the SEMANTIC sentence, not the literal one** (D2).

**C5 spec (static):**
- yaml `1ffd687b8a9d` is equal at base and head. 0 `*.openapi.ts` and 0 yaml in the diff.
- The must-hit control is `ea6fcecc3a6f`, the last commit to touch the yaml: it lists yaml 1 / ts 2.
- /lookup declares 200 400 401 403 404 (plus 429 500 502 503 from the shared responses).

**C6 not covered:** §5f applies (2 runtime paths; PR 0 control 0). The body states §5f, users:read UNMEASURED, no deploy, tsc excludes the test, and no S+K pair / no Akto.

## 2. Doubts for the GATE to rule
The drafter rules none of these. All are in the prompt.

- **D1 — TENANTLESS connector token (the one that could block).** This is static, from pred1374_c3.out `INFO D-TENANTLESS`.
  - `ConnectorTokenClaims.tenantId` is OPTIONAL (`jwt.ts:271`). `generateConnectorToken` spreads it only when it is present, and the exchange (`routes/internal.ts:72`) passes whatever the security service returns.
  - The /lookup guard is `if (!user || (callerTenantId && user.tenantId && user.tenantId !== callerTenantId))`. So a connector token minted with no tenant, carrying `users:read`, skips the cross-tenant 404. A READ predicts 200 for another tenant's user.
  - The same shape is pre-existing for access tokens. `auth.integration.test.ts:1398`'s own comment says tenants are "both undefined in test env".
  - The PR's cells all mint WITH a tenant. Probe arms P5 (connector) and P5b (access, pre-existing) measure it. The gate rules whether this is new exposure that blocks.
- **D2 — the C4 sentence.** The commission's words "no stated timing covers these suites" are NOT verbatim in the PR body. The body says "no tier budget or timing row covers the auth vitest suite", with the grep and its must-hit control. The flow doc says "No stated timing in either platform-k document covers the services/auth vitest suite". The gate rules whether this suffices.
- **D3 — authenticate.ts is covered by no test.** The PR states this itself. The label proof is the gate's probe P1 / P1C, and the mutation arm `authmw` should stay 4/4 green.
- **D4 — stale cites (polish).**
  - `jwt.ts:351` is an unchanged file and still says ONE route.
  - The test comment `:169` cites `authenticate.ts:105-:111`; `runWithTenantId(connector.tenantId)` is at `:118` at head.
  - The body's `authenticate.ts:107` is the BASE line; it is `:113` at head (pred1374_c3.out `INFO CLAIM`).
- **D5 — "a must-hit control of 9 vi.mock calls"** (the cheat-sheet block). The file has 3 module mocks; 9 is the substring count including `vi.mocked` (c2_plan_ex2.out).
- **D6 — the branch suffix `-b55-1`** was adopted from Seat B 55th under the B57 brief `:63`. This is information. The kit's branch rule is exact.
- **D7 — the /stub audit line also changes**: its text, plus a new `route` field. `git grep -i -F` finds 0 consumers of the old text at head. Platform S's consumers are unread.
- **D8 — the gateway claim.** `proxy.ts:461-466` and `documents.ts:1667-1671` carry the cited strings, 2 of 2 each (READ ONLY).
- **D9 — co-tenants.** PR B (KS-1015) is stacked on this head. Seat D 2nd's KS-1404 PR edits both docs. Each block is inserted at the doc's closing anchor (flow before base line 1626, cheat before 3661), so a co-tenant block at the same anchor conflicts textually. THE DOC RULE says to keep both.
- **D10 — not the gate's to rule:** KS-1402's self-move to In Progress; `mergeable_state: unstable`; the usage quota.

## 3. The kit's instruments
Each was exercised, and its outputs sit beside it. Runs named `*_exN` are exercises; `pred1374_*` runs are predictions.

| script | what it does | exercised runs (rc) |
|---|---|---|
| `lib_gate54a.py` | Shared helpers. `git()` allows ONLY show / log / ls-tree / cat-file / ls-remote / rev-parse / diff. | imported by all |
| `gh_census_gate54a.py` | PULLS read, PR body to file, census with co-tenant classes | `gh_census_help_ex1` (0); `gh_census_ex1` (0); `census_cc1_ex1` (0: a SIM co-tenant key classifies EXPECTED); `census_cc2_ex1` (0, 11 OVERLAP: a docs-only allowance with a lock overlap is an OVERLAP); `census_cc3_ex1` (0: the STACK test reads #1360 NOT STACKED, so OVERLAP) |
| `c1_pin_gate54a.py` | C1 P1-P8, END_TREE | `c1_help_ex1` (0); `c1_shortsha_ex1` (2); **`c1_control1373_ex1` (1: merged #1373 fails P2/P3/P4/P6/P8; the trailer control and P7 pass)**; **`c1_p7control_ex1` (1: a SIM head 88e8877a fails P7 with all 4 PR 0 paths)**; pred1374_c1 (0) |
| `c2_cells_gate54a.sh` + `c2_parse_gate54a.py` | C2 plan / install / run base / run head / tsc / mutate / probe | `c2_help_ex1` (0); `c2_plan_ex2` (0); **`c2parse_selftest_ex1` / `c2_parseselftest_ex1` (0, 14 of 14 arms)**: a load failure, a wrong-message red, a skipped cell, a red control cell, a regression, +5 tests, a console/JSON disagreement and a vacuous mutation are each caught. Refusals: `c2_refusal_ex1` (2: the shared checkout), `c2_builderwt_refusal_ex1` (2), `c2_outrefusal_ex1` (2, **but it created `Secuura/x`**, section 0), `c2_outrefusal_ex2` (2, created nothing). **install / run / tsc / mutate / probe were NOT executed.** |
| `c3_authsurface_gate54a.py` | C3 S1-S5 plus INFO (D1, stale cites, claims) | `c3_help_ex1` (0); **`c3_selftest_ex1` (0, 8 of 8)**: /me admitting connectors, a `router.use` mount, 404→200, `originalUrl` label, scope gate removed, a second code line and an `authenticate()` edit each FAIL on the named check. **`c3_basevsbase_ex1` (1: S1/S2/S3/S5 fail)**; pred1374_c3 (0) |
| `probe_ks1402_authsurface.test.ts.txt` | C3 runtime: P1 label, P1C must-hit, P2 on 14 routes, P2C, P3, P4, P5 / P5b | **NOT EXECUTED** (no install). It mirrors the PR's own harness. The tester must read it first. |
| `c4_docs_gate54a.py` | C4 D0-D6 | `c4_help_ex1` (0); `c4_selftest_ex1` (1, **BROKEN 9/10**: the host test matched "a host is meaningless", fixed) → **`c4_selftest_ex2` (0, 10 of 10)**; `c4_basevsbase_ex2` (1); pred1374_c4 (0) |
| `c5_spec_gate54a.sh` | C5 static SP1-SP3; `run` = check:openapi plus a planted-line control | `c5_help_ex1` (0); pred1374_c5 (0); **`c5_static_yamlcontrol_ex2` (1: head `ed268a995a88` fires SP1 and SP2)**; `c5_static_basevsbase_ex2` (0, a no-op reading); `c5_refusal_ex1` (2). The `_ex1` runs predate the SP3 superset fix. **`run` was NOT executed.** |
| `c6_notcovered_gate54a.py` | C6 N1-N6 | `c6_help_ex1` (0); **`c6_selftest_ex1` (0, 6 of 6)**; pred1374_c6 (0) |
| `fill_gate54a.py` | fills the prompt, launcher and pins | `fill_help_ex1` (0); `fill_stalebase_ex1` (1); `fill_badargs_ex1` (1: short sha plus `-b57-` branch); `fill_sim1374_ex2` (0) |
| `launcher_gate54a.TEMPLATE.sh.txt` | the launcher (gate54f's guards, re-keyed, plus a charter guard) | SIM `pr1374.SIM.launcher.sh`: `launcher_check_sim_ex1` (0); `launcher_stale_ex1` (9); `launcher_wronghead_ex1` (6); `launcher_movedev_ex1` (17); `launcher_nokw_ex1` (33); `launcher_noconstraint_ex1` (34); `launcher_nocharter_ex1` (8); `launcher_notty_ex1` (21, the only non-`--check` run; it refused at the TTY guard) |
| `repin_and_launch_gate54a.sh` | the launch action | `repin_help_ex1` (0); `repin_badargs_ex1` (9); **`repin_dryrun_ex1` (0, #1374 / aa16f3256dbf)**; **`repin_dryrun_wronghead_ex1` (11: B 55th's pre-doc head d26d406020f7 is refused)**; `repin_dryrun_census15_ex1` (15) |
| `prompt_gate54a.TEMPLATE.txt` | the tester's prompt (24 by-name keywords) | filled as `pr1374.SIM.prompt.txt` and `dry135946.SIM.prompt.txt` |

- `*.SIM.*`, `pins_gate54a.SIM-*.json`, `census_SIM_*.json`, `c1_SIM_*.json`, `pr1374.SIM-no*.prompt.txt` and `c2_selftest_console.fixture.txt` are exercise inputs or outputs. None of them is ever launched.
- The real `pins_gate54a.json` does not exist yet; the real launch writes it.
- The `__pycache__/` directory came from importing lib_gate54a.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1402-1374|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the launch action refuses with rc 1. The dry run reports the line as missing instead (repin_dryrun_ex1.out).

## 5. How Wednesday launches it
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate54a/repin_and_launch_gate54a.sh 1374 aa16f3256dbf86e654076a31ace1eb1b79a31e69 [--dry-run]
```
- Run it with `--dry-run` first.
- Add `WED_USAGE_STOP=…` only with Kam's recorded authority.
- The launch action does the same as gate54f's: PULLS API + census → ONE ls-remote → rc 11 head guard → rc 10 stale base → fill → race re-read → override (16) → usage gate (12) → launcher `--check` (13; STALE PIN exit 9) → `cockpit.sh add` (14).
- **If Seat D 2nd's PR merges first, develop moves.** That is rc 10, a RE-DRAFT.
- PR B being raised is not a refusal: it classifies as EXPECTED CO-TENANT if it is STACKED on this head.

## 6. What I could not adapt, or did not measure
- **No install, vitest, tsc, mutation, probe or `check:openapi` run.** The drafter was barred from cloning, creating worktrees, installing and writing outside this folder. So C2, the C3 runtime half and C5 `run` have NO drafter rc. The builder's figures remain claims: 77/836 → 78/840, cells 3 red / 1 green at base, tsc 0 = 0, check:openapi rc 0 with 405 examples.
- **The probe was not executed**, so a harness mistake in it is possible. It copies the PR's own working setup. The `/stub` arm mocks `createInvitedStub`, which the PR's test never mocks.
- **gate52's handlers / specdiff / keyscan were adapted in shape, not in code:**
  - handlers' static route reading became C3 S1-S5;
  - specdiff's yaml checks became C5 SP1-SP3;
  - keyscan became C1 P5/P6.
  - gate52's goldens and generator replay have no counterpart here: the PR touches no spec, and the only spec check this PR needs is `check:openapi` itself.
- **gate52's automatic RE-PIN over a moved develop is not adapted**, the same as gate54f: a move is rc 10 and a re-draft.
- **gate52's scratch-clone pin and its 135-control suite are not reproduced.** Each instrument carries self-test arms instead, and the launcher guards were exercised on a SIM fill.
- **Not controlled on a real launch:** usage gate (12), `cockpit.sh add` (14) and override (16). This is the same gap as gate54f.
- **The routing-present path is not exercised.** It needs the real line, which is Wednesday's to add.
- No Linear read. No read of Platform S.

## 7. Re-draft recipe (develop moved, or a new head)
1. **On a new head:** update kit.json `expected_head`, `drafted_head_blobs` and `numstat_claim`, and the `lookup_route_line_head` if users.ts moved. Then re-run `c1`, `c3`, `c4`, `c5 static` and `c6` (each also with `--selftest` / base-vs-base).
2. **On a develop move:** also update `base`, `base_tree`, `base_blobs` and `base_parent` / `pr0_commit` (if PR 0 is no longer the parent), and `timing_claim_counts` if the docs moved. Re-check D9's anchors.
3. Run `fill_gate54a.py --simulate`, then the SIM launcher `--check`, then `repin_and_launch_gate54a.sh … --dry-run`.
