GO WITH NOTES (the worst of: PR 2029 GO; PR 2030 GO WITH NOTES; PR 2031 GO WITH NOTES)
PR 2029 (KS-1585 m2, tier 2, 33c4b9a0d24a): GO
PR 2030 (KS-1585 reader, tier 1, f107b9688445): GO WITH NOTES
PR 2031 (KS-1377, tier 1, 30a085c55431): GO WITH NOTES

# Gate 214, round 1 of 2, resumed (the 11:43 session died at 11:47 with no verdict)

## BLUF

No blocker. All three PRs do what they say, on a real PostgreSQL built by the containers' own path. Every figure in Seat G 27th's READYs that I re-ran reproduced exactly. Merged together on the current develop tip: unit 54 files 507 of 507, integration 9 files 148 of 148, and the same behaviour table as PR 2030 alone.

Two notes need a human's eye. Neither is a regression; base behaves the same in both.
1. PR 2031: with a database CONFIGURED but down at boot, a validate miss still answers 200 "Key not found". Kam's card text covers this case and the code comment says otherwise (F1).
2. PR 2030: a deleted, demoted or gone user with a live ADMIN token is now refused for an organisation, but still mints and revokes tenant-level keys, and the refusal tells them how (F2).

**Develop moved.** pins.txt says bd92121e0228. develop read 4ccdc3b3e7cf at 12:00:10 and at 12:12:29 AEDT, one commit (KS-1534: api-gateway paths and fragments). The three PR heads did not move and equal pins.txt at both reads. This verdict is about those three SHAs. The merge trees are given onto both develops below.

## Findings

**F1, Minor, PR 2031, not a regression; ruling residue, Wednesday to route.** `services/security/src/index.ts:1985-1994`. The 503 is gated on `isDbAvailable()`. That flag is false in two different states: memory-only (no DATABASE_URL) and a boot race (DATABASE_URL set, the first probe failed; `db.ts` keeps retrying). The comment says "Only while the database is SUPPOSED to be there (isDbAvailable())", which is wrong for the boot race.
- MEASURED AT RUNTIME (`runs/evidence/boot_{base,p2031,merged}_{memory,race}.json`): boot race and memory-only both answer 200 "Key not found", on head and on base alike.
- A postmaster stopped AFTER a healthy boot answers 503, and 200 again after restart (`stop_merged.json`; base `stop_base.json` answers 200 during the stop).
- Why it matters (READ ONLY): the gateway caches that 200 as a rejection for 30 s (`api-gateway/src/middleware/auth.ts:308`), so during a boot race a valid key can read as rejected.
- Kam's card `secuura-ks1370-validate-when-the-revoke-check-cannot-read`, its bluf: "refuse when a configured database cannot be read, answer from memory only when the service runs with no database at all". Option a's detail: "A failed stored read with a database configured returns 503". Wednesday's ANSWER 06:42:22Z item 3: "YES, 503 SERVICE_UNAVAILABLE ... never falling through to "Key not found"".
- Fix shape, not done, READ ONLY as to the fix: decide memory-only from whether a database is configured, not from the flag, and correct the comment. The unit cell C2 stubs `isDbAvailable: () => false` for memory-only, so it cannot tell the two states apart; a cell for the boot race is owed. Accepting this as a note or requiring a commit is the humans' call. A commit voids this verdict.

**F2, Minor, PR 2030, not a regression, outside the ruling's wording.** `index.ts:1392` and `packages/shared/src/security/keyRevokePolicy.ts:263-267`.
- MEASURED AT RUNTIME (`runs/evidence/table_p2030.json`, `table_base.json`): every non-live user in the table (demoted, deleted, deactivated, suspended, pending, invited, inactive, row gone, row in another tenant), token still saying ADMIN of T: mint with no organisation 201 and a key created; revoke of a tenant-level key 200 and the key revoked. Identical on base.
- The refusal text for the organisation mint reads "...omit organizationId to mint a tenant-level key".
- Kam's ruling is about rows ("Keep them; readers apply a row only while the user is still ADMIN"), so the PR meets it. The fragments say "naming an organisation", so they are true. But the harm the PR's comment names (a token from before the change still minting) survives for org-less keys, and the PR's NOT-done list does not name this.
- Action, not mine: Wednesday decides whether it needs a ticket. Whether a tenant-level key reaches more than an organisation key: NOT measured.

**F3, Nit, PR 2030.** `index.ts:1189-1200`: answerScopeReadFailure's long JSDoc sits above classifyScopeReadError and that helper's own one-liner. READ ONLY; the seat reported it and I confirm it. No behaviour effect.

**F4, Nit, PR 2030.** `Projects Documents/fragments/cheat/KS-1585-scope-rows-apply-only-to-a-live-admin.html` quotes the 403 as "outside admin organisation scope". That is the internal reason (`keyRevokePolicy.ts:274`). MEASURED: the mint's body message is "API keys may only be minted for an organisation in your admin organisation scope; omit organizationId to mint a tenant-level key". Revoke's refusal text was not captured.

**N5, Note, PR 2030, MR5.** Equivalence is conditional, and "survivor" is only true of the seat's narrow run. MEASURED (`runs/evidence/mr5.jsonl`, reader on a user whose users row is in T2 with a scope row in T):
| reader | as secuura_app | as the RLS-exempt superuser | secuura_app inside runWithPlatformScope |
|---|---|---|---|
| head | 0 rows | 0 rows | 0 rows |
| MR5 | 0 rows | 1 row | 0 rows |
Live control: 1 row in all four arms run. So MR5 is equivalent as deployed: compose runs security as `secuura_app` with NOBYPASSRLS, READ from docker-compose.yml:473. It is NOT equivalent on a connection RLS does not bind. The deployed boxes' actual DATABASE_URL role: NOT read. MR5 does pass ks1585, ks1570, ks1584 and all 142 integration cells, but the whole unit suite kills it through the text cell P2 (1 failed of 495). The tenant match is pinned by source text only, never by behaviour.

**N6, Note, PR 2031.** Attached to KS-1370 through its branch name. **What a merge does to KS-1370: UNMEASURED.** I did not read Linear; my network was git fetch only. What is known, from Seat G 28th's `census_after_pr2031_a.txt` and READY only: attachments for the PR URL are KS-1377 and KS-1370 (In Progress); its last state change was Kam's In Review to In Progress on 5 Nov; PR 1602 "sits on KS-1370 the same way"; KS-1570 appears in the 2029 and 2030 branch names and is NOT attached, so the branch-name rule is not one I can predict. The title and body say "Refs" with no closing form. PR 1602's merge would be the precedent, if it is af788a4c8 (2026-10-19, Refs KS-1377; I did not confirm the number). To measure before merge, READ ONLY: KS-1370's history around that date.

## Answers

**1. Scope (own diff).** PR 2029: 4 files +98/-1. PR 2030: 9 files +697/-17. PR 2031: 7 files +392/-17. One commit each on 5fc5569ed96a; equal to the READYs.

Hunks in the shared `services/security/src/index.ts`:
- PR 2030: `-44`, `-1188,0 +1189,46`, `-1312,3`, `-1588`, `-1711,3`, `-1718`, `-1720,2`
- PR 2031: `-457`, `-1973,0`, `-1974,0`
- Disjoint. Merge-tree of the two heads rc 0 in both orders, same tree e74b3ee9786b. Planted conflict on the 2031 line, on top of the 2030 head: rc 1 in both orders. Any other pair of PRs shares 0 paths.

**2. PR 2030.** Substrate: PostgreSQL 15.19, private cluster, `docker/init/*` in lexical order including the real `01-create-app-role.sh`, then 59 migrations, built from `wt/dev`. I chose it because it is the containers' path. Migrations alone do not build (stops at 006: `svc_w...` missing, `runs/evidence/two_schema_builds.txt`), so there is no second working source to reconcile. FORCE RLS on users and on the scope table. Reader and writer on the real routes (`table_base.json`, `table_p2030.json`; merged identical):

| caller, token says ADMIN of T, scope row {A1} in T | reader rows base/head | mint A1 base/head | revoke A1 key base/head (key active after) | writer PUT head |
|---|---|---|---|---|
| live admin/active; Admin/ACTIVE fold | 1/1 | 201/201 | 200/200 (no) | passes the target check (400 at my fixture org) |
| role user; role issuer_admin | 1/0 | 201/403 | 200/403 (yes) | 404 |
| status deleted, deactivated, suspended, pending, invited, inactive | 1/0 | 201/403 | 200/403 (yes) | 404 |
| users row gone | 1/0 | 201/403 | 200/403 (yes) | 404 |
| users row in another tenant | 1/0 | 201/403 | 200/403 (yes) | 404 |

- A2 outside the scope: 403 for all, both revisions.
- Another tenant's live ADMIN (rows in T only): 0 rows in T2; every mint and revoke 403, keys active, both revisions.
- Sub-only token, live: 201.
- 12 of 12 user rows: head admits exactly the two live spellings; no caller gained anything.
- Outage, app role cut off: base 500, head 503 SERVICE_UNAVAILABLE on mint and revoke, for live, demoted, gone, other-tenant callers; 0 minted, key active. Real postmaster stop, live caller only: base 500, merged 503 on both, key active.
- Mutants, 3 of the seat's plus my own: MR2 6 failed, MR4 1 failed, MM2 2+1 failed, all equal to the seat's json. Own G2 (revoke catch decides anyway): killed, 2+1. Own G1 (fragment also admits pending): survives ks1585, ks1570 and ks1584 because writer and reader widen together, so PARITY holds; killed by the whole integration suite (g1548-i2 pending cells) and P4.
- GRANT: **no new GRANT needed**, MEASURED on this substrate with no grant added by me: `has_table_privilege(secuura_app, users, SELECT)` is true. READ: `provisionAppRole` grants ALL TABLES at each gateway boot when APP_DB_PASSWORD is set, and the writer already reads users as this role on base. No migration is needed. The deploy note is present: PR body line 71, and both fragments. No box was read, so the note's "confirm" stands.

**3. PR 2031.**
- Upsert: the seat's held-lock cell reproduces (3 of 8 on base). My own real concurrency, 30 validates with a revoke in the middle, 15 rounds (`usage_{base,p2031,merged}.json`): base lost 154 uses over 9 rounds; head and merged lost 0. Rounds that actually raced: base 9, head 12, merged 10 of 15; in the rest the revoke won first. last_used_at kept on a forward-moved row; NULL stays NULL; is_active lands false; validate then answers "Key revoked".
- READ ONLY: dbSaveApiKey's callers are mint (fresh id) and revoke; saveKeyAndRetirePriors inserts a fresh id. The comment "Only a REVOKE reaches this branch" holds.
- Miss: see F1 for the one arm that does not answer 503. Memory-only 200: correct.
- Nine cells: A develop product 9 failed 18 passed; B miss branch reverted 3+6 failed; C 27 of 27. All reproduced. The diff is 6 expect lines NOT_FOUND to LOOKUP_FAILED, 5 titles, 2 header sentences, one constant and its why-comment; 0 linesOf lines changed (control: 10 and 8 present); cell counts 10/10 and 8/8. That is exactly the ANSWER's "6 expectations, 5 titles, 2 header sentences". Condition 1's paragraph is in the body, with the key spaced.
- Who treats a 200 "Key not found" as data, READ ONLY: production callers are exactly two.
  - `api-gateway/src/middleware/auth.ts:282` checkApiKey (with its wrapper validateApiKey:273; used at :536): `!data.valid` is rejected and cached 30 s at :308; a 503 goes to `couldNotAnswer` at :298, is answered 503 and not cached.
  - `auth/src/routes/internal.ts:43` connector-token: 200 invalid is 401; non-2xx is 502.
  - Neither needs a change. Stubs only: ks480 and ks1240b in the gateway's tests. The e2e spec `ks-4-phase5b-reconcile.api.spec.ts:385` is indirect. The published spec already lists 503 (`security.openapi.ts`).

**4. PR 2029.** The token is correct. The script run unmodified on my cluster through a docker shim (`runs/evidence/rls_runs.txt`):
- Empty users: base DRIFT 1 / OK 31 / FAIL 1; head DRIFT 0 / OK 31 / FAIL 1 (known finding, out of scope).
- One users row: base DRIFT 1 / OK 32 / FAIL 0; head DRIFT 0 / OK 32 / FAIL 0 / PASSED; the diff is that one line.
- Planted control: action_provenance removed from the spec gives a DRIFT line. Same plant in the test: S2 alone red, 1 failed 4 passed. Test on base 2 red 3 green; head 5 of 5.

**5. Suites** (all mine, Node v26.8.1, not an LTS line):
| tree | unit | integration | tsc | test-types (files, under __tests__) | eslint (security/src) | docs check |
|---|---|---|---|---|---|---|
| base 5fc5569ed96a | 50 files, 480 | 7, 124 | 0 | 69, 57, 0 errors | 0 errors, 2 warnings | OK |
| 2029 | 51, 485 | not run (no integration surface) | 0 | 70, 58, 0 | same 2 | OK |
| 2030 | 52, 495 | 8, 142 | 0 | 72, 60, 0 | same 2 | OK |
| 2031 | 51, 487 | 8, 130 | 0 | 71, 59, 0 | same 2 | OK |
| merged on 4ccdc3b3e7cf | 54, 507 | 9, 148 | 0 | 75, 63, 0 | same 2 | OK |
0 failures, so nothing to classify. The 2 warnings are the no-useless-assignment pair, on base too. Edited fixtures on base's product: 30 of 30. Seat's reds on base: integration 14 of 18 and 2 of 6; unit 10 of 15 and 4 of 7. Planted docs defect: rc 1, naming the fragment. Docs checks print the page ADVISORY on base too.

**6. Merge.**
| | onto bd92121e0228 (pins.txt) | onto 4ccdc3b3e7cf (tip) |
|---|---|---|
| PR 2029 | rc 0, 63cda436eb8c | rc 0, 44113352d455 |
| PR 2030 | rc 0, dde581bd6975 | rc 0, 10ff93693131 |
| PR 2031 | rc 0, 35bb9234a0ce | rc 0, 7d1d98bb277d |
Shared paths with everything merged since 5fc5569ed96a: 0, 0, 0, against both 65 paths (pin) and 71 (tip); planted control 1 each time. All three merged on the tip: tree 3805982a3b69, 19 files, exactly the union of the three PRs' paths. KS-1370: N6.

## Reproduced vs not, of the READY figures
Reproduced: every suite count, every red count, the outage, MR2/MR4/MM2/MR5/K2/K3, the script's DRIFT/OK/FAIL counts, the nine-cell arms, 2 eslint warnings, the examined-file counts, the hunks.
Not re-run: mutants MM4, MM5, MM6, K1, K4, K5. The seat's push hook lines and its Linear census, which I read and relay as the seat's.

## NOT tested
Any box or dormant row count; the deployed role and grants; a running stack; pgbouncer (compose reaches the service through it; my service connected directly, so its error shape under an outage is unmeasured); gateway and auth end-to-end against a live security service (READ ONLY above); Linear; the four platform suites; hook legs 3, 4, 8; Node 24; other Postgres locales (en_US.UTF-8 only); PR 2029's integration suite on its own (it has no integration surface; the merged run covers it).

## Conduct
- Reused the partial `repo/`: objects usable, the 5 worktrees clean at the pins, its main checkout half-staged and untouched. Its `runs/d2030.diff` and `lsremote_start.txt` are not cited.
- Added `repo/wt/merged`. Moved the partial p2029 node_modules to `scratch/_quarantine_2026-11-06/` rather than deleting; its partial frontend node_modules stay in place. An empty `p2029_partial_frontend` folder is left there too. Deps by APFS clone from `worktrees/s-g27-ks1585r` (read only), only the trees security needs.
- Fetched develop into my clone once, with the clone's configured key. No npm install. Nothing posted.
- One cluster: 127.0.0.1:55214, TCP only, stopped by recorded pid 83028 at 12:12, confirmed gone, port empty. Data left in `scratch/pg`, gitignored. The cluster was stopped and restarted twice by my real-stop probe.
- Mutants, overlays and probes ran only in my worktrees; each restored and read clean at the end. Probe sources: `scratch/probes/`; used copies in the quarantine. Logs: `runs/r/`, passwords stripped by the runner; one check for them read 0, with no planted control.
- Suites ran one at a time, with only file reads beside them. One `grep -r` was scoped to my own `runs/` folder: not a sweep of 0_Brain/reference, but it is the form the commission forbids over that tree, so I name it.
- TMPDIR stayed inside my folder (`tmp/`) and worked; no short path outside was needed.
