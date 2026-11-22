PR 2274: GO WITH NOTES (at head cf24d89acb50859e11d6ad1edda8b72cff9fc138; tier 1)

# Gate 398, tier 1 (Opus), PR 2274 (KS-2315), 2026-11-22 ~21:15-21:30 AEDT

The merge GO stays Wednesday's to hold until Kam rules card `secuura-system-errors-platform-only-ks2315-1122`. This verdict covers the build of its default option a only.

## Pins
- **Pinned twice, at 21:15:18 and 21:26:46**, by git ls-remote (through the Secuura project's gh credential helper, read-only) and gh pr view. Same values both times:
  - PR 2274 OPEN, not draft, MERGEABLE, head cf24d89acb50, ONE commit, parent = develop c8fd1653a5dc. 5 files, +277 -9, tree 0c70393b5fa4. updatedAt 10:13:19Z (not changed since the READY).
  - develop = c8fd1653a5dc9b79c41f752b29afb296910831a4 (PR 2272 and PR 2273 are both merged into it).
- **Merged state = the head.** `git merge-tree --write-tree origin/develop pr/2274` gives rc 0, and the tree is the head's own tree 0c70393b5fa4.

## How I measured
- My own clone `_work/g` from GitHub (`--reference-if-able` gate 397's clone, `--dissociate`). Worktrees:
  - `h` = head (suites, static, probe);
  - `d` = develop (suites, red-first, probe baseline);
  - `x` = head (mutants).
- node_modules and `packages/shared/dist` were APFS-cloned from gate 397's `h`. Between that head (8f7c7bd9) and develop, no package.json, lockfile or `packages/` file changed, and the PR changes none either (diff rc 0 both times).
- Node v26.8.1 (not LTS). jest for originate, vitest for packages/shared. TMPDIR = `_work/tmp`. For check:openapi only, TMPDIR was the relative path `../../../tmp`, which resolves to the same `_work/tmp`: tsx's IPC socket path under the absolute `_work` path is longer than the 104-byte unix-socket limit (EINVAL on the first try; evidence kept).
- Scripts are in `_work/`: `run_cwd_g398.py`, `suites_g398.sh`, `an_suites_g398.py`, `redfirst_g398.py`, `probes/g398-probe-a.test.ts` + `probe_run_g398.py` + `an_probe_g398.py`, `mutants_g398.py` (my own engine: M1-M8 rebuilt from the PR's table, plus E1-E8 of mine), `static_g398.py` (gate 397's, re-pointed), `openapi_g398.py`, `mt_g398.py`, `lin_read_g398.py` (read-only GraphQL; the key is read into memory from the Secuura credentials file and never printed).
- **Probe a** (findings-only, asserts nothing):
  - Real parts: the real router and the real `requireRole`.
  - Stand-ins: authenticate (the caller comes from the test), and errorTrackingService (fully mocked, every call recorded).
  - Matrix: 28 callers x 60 requests = 1,680 requests per arm. The requests cover 4 mount spellings (`/api/system-errors`, `/api/client-errors`, `/API/System-Errors`, `/api/CLIENT-errors`) x 15 shapes: the four routes, case and trailing-slash variants, HEAD, bad query, bad and absent body, a garbage errorId, the two ingests and a POST to the mount root.
  - Run on h and on d. Each probe copy was moved to `_work/_quarantine/probe_copies` after use.
- **End state:**
  - h, d and x have 0 porcelain lines. x's systemErrors.ts sha256 equals h's (23e65ab0f61f…).
  - Docker: 0 of 106 container names match g398. I used no container.
  - Not touched: no seat tree, no `!CODING` write, no GitHub or Linear write, no database, no mail, no launch, no `cd`, no `rm`.

## Findings

No HIGH and no MEDIUM finding. The bound holds as ruled, on both mounts, for every caller shape I could build.

### LOW
**G398-2274-1: five surviving mutants. The behaviour holds; the cells do not pin it.**
- No cell sends a non-canonical non-platform role. Adding an alias to the four `requireRole` lists survives all 167 cells (0 failed):
  - E1: `org_admin` added;
  - E2: `ADMIN` added;
  - E3: `platform_admin` added.
- R3 and C2 cover only the two GETs on the second mount. Two mutants that open the writes on `/api/client-errors` only also survive (0 failed):
  - E5: the alias mount unguarded on PATCH and POST;
  - E6: ORG_ADMIN admitted on the two writes via the alias mount only.
  - E4 (the alias mount unguarded on all four) is killed, by R3 only (2 cells).
- The head itself refuses every one of these. In probe a, `org_admin`, `ADMIN`, `admin` and `platform_admin` get 403 with 0 service calls on all 48 gated requests, on every mount spelling.
- Fix shape, if wanted:
  - add `org_admin`, `ADMIN` and `platform_admin` rows to P1;
  - add R3 rows for `PATCH /api/client-errors/:id/resolve` and `POST /api/client-errors/resolve-by-service`.

**G398-2274-2: words. "That is the same set the shared isPlatformRole admits" (PR body, Summary) is not exact.**
- `isPlatformRole` (packages/shared keyRevokePolicy.ts:140) applies an ASCII fold. It admits `system_admin`, `System_Admin`, `Super_Admin` and any other ASCII-case variant of SYSTEM_ADMIN or SUPER_ADMIN.
- `requireRole` admits exactly three spellings: SYSTEM_ADMIN, SUPER_ADMIN and super_admin. Probe a: `system_admin`, `System_Admin` and `Super_Admin` get 403 on all 48 requests.
- The gate is the narrower of the two, so it fails closed. The same three variants were refused on develop too, so nothing changes for them.
- Worth knowing: `system_admin` is a spelling the code base treats as platform elsewhere:
  - admin `Layout.tsx:109/126` (the platform menu);
  - api-gateway `admin.ts:499` (seed data);
  - originate `certifications.ts:135`.
  A real `system_admin` token, if one is ever minted, would see the KS-2315 dashboard degradation even though it is a platform user. That is pre-existing and also applies to gdpr.ts:669/702.

**G398-2274-3: the new standing leg. packages/shared is red on SIX cells on develop, not one. The PR changes none of them.**
- Whole `vitest run` in packages/shared, both arms: 1,730 tests, 1,724 passed, 6 failed. The failing-name sets are IDENTICAL on develop and on the merged state: 0 only on the head, 0 only on develop, 0 changed status.
  1. ks1536-one-role-vocabulary **G2**: the expected one, `services/originate/src/routes/gdpr.ts: 7 > 6`. systemErrors.ts counts 4 lists on the head, its baseline 4.
  2. ks1725-zod3-compat **F**: 113 `zod3Issues(<x>.issues)` calls against the pinned 114.
  3. ks1725-zod3-compat **J**: `services/prism/src/index.ts` has no `z.record` under `claims`. That file was last changed by fe514a7b2, KS-624, 2026-11-16, which rewrote prism's issue path.
  4. ks727-errorhandler-class-guard corpus 2: "the entrypoint inline-site corpus is exactly the declared set".
  5. ks727-errorhandler-class-guard corpus 2: "every inline error handler … is a pure forwarder".
  6. wallet-signature KS-278: "accepts a valid wallet signature". This may be environmental (Node 26 crypto). Not separated.
- The builder's "1 failed, 102 passed" is the two-file run (ks1536 + ks2125), and it reproduces as the G2 line. The commission's premise ("ALREADY RED on one cell") holds for that file only. Cells 2-5 are code-text guards and look like real develop reds that predate today. They are for Wednesday to route, not this PR's.

### Info (not findings)
- **The `/api/client-errors` alias mount is dead for its stated purpose ("Alias for error boundary POSTs", index.ts:307).**
  - All three frontends' ErrorBoundary POST to `/api/client-errors` itself. The router has no `POST /`, so originate answers 404 on both arms (probe a: "POST root" 404 for every caller and mount).
  - The gateway has no `/api/client-errors` proxy at all. The repo-wide grep of api-gateway/src finds 0 `client-errors` matches; the control, `/api/system-errors`, is found at proxy.ts:1303.
  - The mount's only live effect is a second door to the four admin routes, which this PR now closes.
  - Pre-existing; a candidate for follow-up.
- **The stale spec text is a little wider than the residual states.**
  - The two descriptions stated in the residual are confirmed: originate.openapi.ts:4000 and :4027, and secuura-api.yaml 32946 and 33016.
  - They also still say "In dev this route is open".
  - The same stale string is on `/dsr/pending` (3437) and `/deletion-log` (3909), already known from gate 397.

## The commission's questions
- **Q1 THE BOUND: holds.** Probe a, head:
  - **Refused:** 1,152 non-platform requests to the gated routes (24 caller shapes x 48), 403 each, ONE body byte-for-byte (`{"success":false,"error":{"code":"FORBIDDEN","message":"Insufficient permissions"}}`), 0 service calls. The caller shapes:
    - ORG_ADMIN plain, with organisation and tenant claims, and with `roles:['SYSTEM_ADMIN']`, `isAdmin` and `isPlatformAdmin` extras;
    - org_admin, ISSUER_ADMIN, OWNER, VERIFIER, ADMIN, admin, platform_admin;
    - role-less, null and empty role;
    - system_admin, System_Admin, Super_Admin;
    - leading space, trailing space and trailing newline;
    - `SUPER_ADMıN` and `ſUPER_ADMIN`;
    - array roles, and an object with a `toString`.
  - **Refused before parsing:** malformed input from an ORG_ADMIN (unknown query parameter, `service:{}`, no body) gets 403, not 400.
  - **Unauthenticated:** 401 on all 48.
  - **Platform:** SYSTEM_ADMIN, SUPER_ADMIN and super_admin get 36 x 200 + 12 x 400 (the bad inputs), identical row-for-row to develop.
  - **Only the ORG_ADMIN changed:** head vs develop differ on exactly 144 rows, all of them the three ORG_ADMIN shapes (3 x 48).
  - **Equivalence:** requireRole's fold is NOT the same set as isPlatformRole's; it is a strict subset (G398-2274-2).
- **Q2 OTHER DOORS: none open.**
  - Non-test code reaching `system_errors`:
    - errorTrackingService, through these four routes;
    - errorHandler.ts and logger.ts (writes);
    - gdprService.ts:488-534 (retention anonymise, reached only from the SYSTEM_ADMIN `/retention/enforce` and the sweep);
    - migrations.
  - The control: the 20 files the grep finds repo-wide.
  - The gateway forwards `/api/system-errors` behind `authenticateToken(true)` only (proxy.ts:1303-1306). Its unauthenticated `/originate/` pass-through also lands on originate's own authenticate plus requireRole.
  - No other router, service or the analytics service reads the table.
  - The two ingest routes are not among the four. They answer 201 for every caller and every mount, identical on both arms (probe a; C3).
  - Pre-existing and not new: `POST /api/system-errors/ingest` direct to originate needs no caller.
- **Q3 THE DASHBOARD: degrades, nothing breaks** (code read of SystemHealth.tsx and services/api.ts):
  - `apiRequest` returns `{ok:false}` on a non-2xx. It does not throw, redirect or log out.
  - Stats: null, so the two error cards show `—` and the breakdown is hidden.
  - Errors: `[]`, so the tab says "No system errors found. All systems healthy." That is false reassurance, as named.
  - "Resolve All (<service>)" appears once a service is picked from the four hard-coded options. Its 403 is awaited and ignored, then everything refetches. No per-row resolve button renders, because there are no rows.
  - The DSR and retention tabs are untouched.
  - The page is in every role's menu (Layout.tsx:88).
- **Q4 THE CELLS: reproduced.**
  - Counts: 47 = R1 8 + R2 2 + R3 2 + P1 16 + P2 4 + C1 12 + C2 1 + C3 2.
  - Red-first (head's two files on develop's product in d, then restored, porcelain 0): **81 run, 14 failed, 67 passed, 0 suites failed to run.** Every failure is an assertion: 12 x `403` vs `200`, 2 x `403` vs `400` (R2). The failures are R1 x8, R2 x2, R3 x2 and the two inverted ks694 cells. The new file goes 12 red / 35 green; ks694 goes 2 red / 32 green.
  - Green on the head: 81 of 81 (inside the whole suite).
- **Q5 MUTANTS** (x; 9 files, 167 cells; the no-mutant control has 0 failed; restored and sha256-checked each time):

  | mutant | failed | killed by |
  |---|---|---|
  | M1 ORG_ADMIN back on GET /stats | 4 | R1 x2, R3 stats, ks694 |
  | M2 ORG_ADMIN back on GET / | 5 | R1 x2, R2 query, R3 list, ks694 |
  | M3 ORG_ADMIN back on PATCH | 2 | R1 x2 |
  | M4 ORG_ADMIN back on POST rbs | 3 | R1 x2, R2 body |
  | M5 requireRole dropped on PATCH | 6 | R1 x2, P1 x4 |
  | M6 ISSUER_ADMIN added on POST rbs | 1 | P1 ISSUER_ADMIN |
  | M7 authenticate dropped on GET /stats | 18 | R1, R3, C1, ks694 … |
  | M8 requireRole('SUPER_ADMIN') on GET / | 5 | C1 x3, ks694 x2 |
  | E4 alias mount unguarded, all four | 2 | R3 x2 |
  | E8 ORG_ADMIN with an organisation claim admitted | 4 | R1 (claims) x4 |
  | E7 ASCII-fold platform (isPlatformRole set) | 0 | survives: a widening to platform case variants only, not a security regression |
  | **E1 org_admin / E2 ADMIN / E3 platform_admin added** | **0** | **survivors: G398-2274-1** |
  | **E5 alias writes unguarded / E6 alias writes admit ORG_ADMIN** | **0** | **survivors: G398-2274-1** |

  M1-M8 reproduce the PR table's kill counts exactly. 16 of 16 compiled.
- **Q6 WHOLE:**
  - **originate:** develop 3,171 of 3,171 in 242 files; head 3,218 of 3,218 in 243. Failure sets both empty. 49 test names only on the head (47 new + 2 inverted ks694 names), 2 only on develop (the two old ks694 ORG_ADMIN names), 0 changed status.
  - **packages/shared vitest:** identical failing-name sets on both arms, but six names, not one (G398-2274-3). systemErrors.ts stays at 4.
  - **tsc:** 0 (planted: rc 2, 1 error).
  - **eslint** `--max-warnings 0`: the three files rc 0; systemErrors.ts at develop rc 0 (planted: rc 1).
  - **check.cjs originate:** 337 examined, 276 under `__tests__`, 0/0/0 (planted: 1 new, rc 1).
  - **Fragments:** OK (planted: FAIL).
  - **check:openapi:** CHECK PASS.
  - **Standalone ratchet:** rc 1 on api-gateway ks815 TS2345 x2. The leg test is 45/48. This is the same clone-install gap gates 395 and 397 recorded; the PR touches no api-gateway file. UNMEASURED here, not red against the PR.
  - **Overlap:** 18 other open PRs (control: package-lock.json in 11; no truncated file list). 0 touch any of the 5 paths.
  - **merge-tree:** vs develop rc 0. The planted control (a local commit, never pushed, rewriting the PATCH line) gives rc 1, CONFLICT in systemErrors.ts.
- **Q7 WORDS:**
  - **Hold:**
    - the direction line (default a pending Kam; b narrows to the two writes; c closes unmerged);
    - the summary, the census (gdpr.ts:669/702 `requireRole('SYSTEM_ADMIN')`; e2e-v2 `admin.api.spec.ts:57` <500 and `:102` <501; the seeded `admin@secuura.com` is SYSTEM_ADMIN; proxy.ts:1303-1306);
    - the residuals, every figure (14 red, 35/32 green, 81/81, M1-M8, 3,171/242, 3,218/243, 337/276, the KS-1536 line) and NOT RUN.
  - **Exceptions:** G398-2274-2 (the isPlatformRole sentence) and G398-2274-3 (true as a two-file figure; the whole suite has five more reds that the PR does not cause).
  - **KS-2315** (read-only): In Progress, priority 2, one comment. Facts comment 945f60e3 (2,747 B): updatedAt is not after createdAt, so it is unedited. Every sentence I could check holds.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- **Hook refusals, re-issued:**
  - a zsh `=` separator;
  - a `$G` command-word split;
  - a `git -C $G worktree` write flagged as outside WEDNESDAY (a variable-path false positive). I re-issued it with the literal `_work` path.
- **check:openapi** first ran with the absolute `_work/tmp` TMPDIR and failed with EINVAL on tsx's socket path (evidence: `check_openapi_h.out` was overwritten by the passing run; the failure is quoted above). I re-ran it with the relative TMPDIR, which resolves to the same folder.
- **The first overlap pass** split paths on whitespace, which broke the fragment names. I re-ran it with exact names; the result is the same (0 overlap).
- **Builder's record:** I read `mutants_w57.py`'s mutant table read-only to rebuild M1-M8. My engine is my own.
- I read no mail and used no `cut -c`.

## Not run
- The four platform suites, a booted originate or gateway, the dashboard in a browser, a real Postgres, any deployed environment, Node 24.
- The api-gateway ratchet leg on a proper install.
- Separating wallet-signature's red into environment or code.
