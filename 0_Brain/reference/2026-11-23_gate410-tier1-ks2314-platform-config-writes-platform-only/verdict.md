PR 2286: GO WITH NOTES (at head 1d906e3c0a57c4101cb1a48c34752c091cbec8b7; tier 1)

# Gate 410, tier 1 (Opus), PR 2286 (KS-2314), 2026-11-23 ~04:16-04:55Z (15:16-15:55 AEDT)

**Authority:** Kam, 2026-11-23 10:13:07, card `secuura-platform-config-who-may-write-ks2314-1122` = a ("Platform admins only, for all five"). The KS-1701 ruling (one shared check) also applies.

**How rulings:** Wednesday's W69_answer_plan (QA, QB, QC in; QD design A; QE a separate item; QF insert-only) and W69_answer_leg14 (A1, with settingsSavePayload.ts added).

**Scope:** findings only. Nothing was fixed, posted, mailed, merged, or written to GitHub or Linear.

## Pins
- **First pin, 04:16:11Z (git ls-remote):**
  - develop b8470f5fd331759f770aca7ae6077442773cf396
  - refs/pull/2286/head 1d906e3c0a57c4101cb1a48c34752c091cbec8b7
  - refs/pull/2159/head 7b54e7cbb6f0082a32b496c1773aa2e43bfe3ea2
- **Second pin, 04:43:12Z:** all three unchanged.
- **gh (read-only):** OPEN, not draft, base develop, MERGEABLE, 1 commit, 9 files, +663 -22, updatedAt 04:13:54Z, 1 comment, 0 reviews. Title "Refs KS-2314: …" (no closing keyword).
- **The head:** ONE commit whose parent is b8470f5fd331, which is develop now. So develop has not moved since the build.
- **The develop I ran is b8470f5fd331, for every suite.**
- **The merged state:** local commit 903e5eefa400. merge-tree rc 0, tree f2c177ed4467, which is the PR's own tree. Never pushed.

## How I measured
- **Clone and worktrees:**
  - Clone: `_work/g` from GitHub (`--reference-if-able` gate 409's clone, `--dissociate`). Git write verbs ran only through `_work/gitx.sh`.
  - Worktrees:
    - `d`: develop
    - `h`: merged (suites, static, browser)
    - `x`: merged (mutants, probes)
    - `r`: develop + the 3 cell files (red-first)
    - `p`: planted controls
    - `c`: develop+2286+2159
  - The clone's own main checkout did not complete. It was never used; every measurement ran in the worktrees.
- **node_modules:** APFS clones (`cp -c`) of earlier gates' trees:
  - gate 409: root, packages/shared, issuer
  - gate 400: api-gateway
  - gate 408: originate
  - gate 407: admin
  - That was a read; nothing was written in their trees.
  - The manifests are blob-equal to develop: root package and lock, shared, admin, api-gateway, originate and issuer package.json.
  - The PR changes 0 package or lock paths.
  - There are 0 absolute symlinks; the workspace links are relative.
- **Environment:**
  - Node v26.8.1.
  - TMPDIR is `_work/tmp`. The shell suites and tsx used a short symlink, `/private/tmp/g410t → _work/tmp`; it was moved into `_quarantine` at the end.
  - Commands needing a cwd went through `_work/run_cwd.py` (no shell `cd`).
- **Tools** (all in `_work/`):
  - `suites.sh`, `an_suites.py`, `shell_suites.sh`
  - `mutants_g410.py`: the seat's 53 plus G19, re-typed from its `mutants_w69.py` and `mutants_a1_w69.py`, plus 20 of mine
  - `static_g410.py`, `overlap.py`
  - `probes/` (gateway, originate and issuer probes, and the browser host `stack_g410.ts`)
  - `lin_read_g410.py`: gate 409's read-only reader
  - Every probe file was copied into `x`, run, then moved to `_quarantine`.
- **End state:**
  - d, h, x, p, c and r all have 0 porcelain lines.
  - Nothing is listening on 56882 or 56102.
  - No container was started.

## Findings

There is no HIGH and no MEDIUM finding. The guard is on every caller-reachable writer of the five kinds that I could find (Q1). It is the one shared check on all three sides (Q2). Reads are untouched (Q4). All four suites are unchanged apart from the 398 new names (Q8).

### LOW
**G410-2286-1: the cells miss four non-equivalent mutants. None is wrong in the shipped code.**
- **Z05 and Z08 SURVIVE all 263 gateway cells:** requirePlatformAdmin added to GET `/api/admin/verification-policies/audit`, or to GET `/api/admin/document-types/:id/documents`.
  - The Q4 read pins cover 7 GET paths (plus the 2 proxy GETs), but not these two, nor `/verification-policies/regional`.
  - Code read: those GET lines are byte-identical to develop (see Q4).
- **Z12 SURVIVES all 122 originate cells:** refuseUnlessPlatform moved below POST /document-types' body read and its 400 validation, so an ORG_ADMIN with an incomplete body gets 400 instead of 403.
  - The cells send only valid bodies, so "first, before the body is read" is true in the code but pinned by no cell.
  - Measured on the shipped code (probe): ORG_ADMIN with `{}`, an array, or a `__proto__` body gets 403 "Insufficient permissions" with 0 statements, on all 10 POST and PUT handlers.
- **Equivalent at the UI** (each survives the 13 admin cells):
  - **Z14 and Z15:** failureDetail copying ANY status or code, not only a number or a string.
    - Only `updateSettings` throws into saveSettings, and it always sets a number status and only a string code. So "copies only a number status and a string code" holds in the code, with no cell on failureDetail itself.
  - **Z18:** the page keyed on code FORBIDDEN alone, with any status. The gateway's FORBIDDEN is always a 403 (`errorHandler.codeForStatus`, requireAdmin, requirePlatformAdmin).

**G410-2286-2: words. "SYSTEM_ADMIN and SUPER_ADMIN count in any ASCII case" does not hold for originate's 13 handlers.**
- **Where it is said:** PR body, What, the "Every new check" bullet. Facts comment 735781cd, line 11: "any letter case".
- **Measured (probe):** at originate, PUT /settings by `Super_Admin` and by `system_admin` gets 403 at the router gate, requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), before refuseUnlessPlatform runs.
  - requireRole folds only `super_admin` and `SUPER_ADMIN`.
  - The PR's own originate pins say so: `system_admin` is in GATE_REFUSED.
- **What is accurate:** the sentence holds for the gateway and proxy (cells and my probe: `sYsTeM_aDmIn` writes).
- **Not a defect of this PR:**
  - It fails closed.
  - The router gate predates it, and is the KS-1701/KS-2309 neighbourhood: originate's gate is not the one shared check.
  - The sentence should say "at the gateway". At originate, only SYSTEM_ADMIN, SUPER_ADMIN and super_admin reach the guard.

**G410-2286-3: QE confirmed, and wider than stated. DocumentTypesManager crashes on ANY object-shaped error, not only the new 403.**
- **Measured:** the real issuer component in jsdom under an error boundary (probe `g410-probe-doctypes`), with Create pressed:
  - The new 403 body `{error:{code:'FORBIDDEN',message}}` makes the boundary catch "Objects are not valid as a React child (found: object with keys {code, message})".
  - **The same crash happens today on a 400 with an object error.**
  - Control: a string error renders as text, with no crash.
- **So:** the defect is pre-existing. This PR makes it the normal path for every ORG_ADMIN create in the issuer's "Document Types" menu.
- **Code read, no crash:**
  - the delete (no res.ok check) does nothing silently;
  - WorkflowsManager's create and delete ignore the status, so the list simply reloads unchanged.
- **The deploy note is accurate.** It names the crash and the gateway half.

### Info
- **Census frame and count: see Q1.**
- **A third "workflows" store exists:** transfer's `POST /api/workflows`, which writes `svc_approval_workflows`.
  - The gateway answers `POST /api/workflows` itself (proxy.ts) and proxies only `/api/transfers` and `/api/delegations` to transfer, whose comment says "transfer service not deployed on Azure".
  - So it is not reachable through the gateway. Listed only.
- **requireAdmin's own 403 also turns Save off.** It is also code FORBIDDEN, "Admin access required", for any non-admin role.
  - Harmless: such a role cannot write. Those roles also cannot load settings, so Save is already off.
- **The leg-14 runner is red on both arms, identically.** 128 passed, 2 failed, 1 skipped of 131 on develop AND on merged.
  - The same 6 FAIL lines: docs_fragments B7 and no_tracked_credentials_root ×3, plus the 2 summary lines.
  - Cause: my TMPDIR lies inside the WEDNESDAY git work tree, so their "not a git checkout" controls fail.
  - Environmental, not the PR.
- **"Platform Name" confirmed.** Settings.tsx 180-181 reads and writes `general.name`; the defaults and seed hold `general.platformName` (settingsStore.ts 39).
  - In my browser proof, a super_admin save stored `general.name: "G410 super_admin save"` beside `platformName: "Secuura"`.

## The commission's questions

- **Q1 COMPLETENESS (the census).**
  - **The frame searched** (merged tree, non-test sources):
    - every `services/*/src` and `packages/shared/src`;
    - `frontend/*/src` and `tests/` for callers.
  - **Patterns:**
    - (a) the redis store setters and deleters of the five kinds, plus `setNotificationSettings('platform-settings')`, `writeStoredSettings` and the backfill;
    - (b) SQL INSERT, UPDATE and DELETE on `document_type_configs`, `workflow_configs`, `admin_integrations`, `admin_settings`, `verification_policies` and `svc_gateway_settings`, plus any file naming those tables;
    - (c) write routes (single-line and multi-line definitions) naming the five kinds;
    - (d) Prisma-style model writes (0; control: the same pattern finds other model writes, e.g. `.customers.update(` ×4);
    - (e) PolicyStore.createPolicy/updatePolicy (0 callers; control: the definition is found).
  - **Caller-reachable writers: 32 routes.** Every one refuses a non-platform caller.
    - **Gateway admin.ts, 15** (the PR's): document types 4, workflows 3, integrations 4 (with /test), settings 1, verification policies 3.
    - **Gateway proxy.ts, 2** (the PR's): POST and DELETE /api/workflows.
    - **Gateway platform.ts, 1, already platform-only:** POST `/api/platform/templates/clone-to-tenant` writes `document_type_configs` and `workflow_configs` into a tenant DB. requireSuperAdmin = isPlatformRole.
    - **Originate adminConfig.ts, 13** (the PR's).
    - **Originate adminConfig.ts, 1, already platform-only:** POST `/migrate-tenant-data` (refuseUnlessPlatform; inserts `document_type_configs`).
  - **System writers with no caller-chosen value (unchanged):**
    - the GET seeds: document types 704, integrations prune and seed 916/924, the boot-time policy seed 1463;
    - settingsStore's Redis refill and seed-row backfill (they copy the stored record).
  - **Other paths:**
    - `PUT /api/settings/notifications` writes the per-user `notif-user:` space and refuses userId `platform-settings` (KS-1262).
    - **Service-to-service writers: none found.**
  - **The PR missed no writer.**
- **Q2 THE GUARD. Holds.**
  - **The checks:** requirePlatformAdmin, workflowPlatformCheck and refuseUnlessPlatform each call the shared `isPlatformRole`. dist equals src; dist checked.
  - **No new spelling list:** 0 role literals in added non-comment lines (control: 2 in added comment lines).
  - **Refusal bodies are each side's existing ones:**
    - gateway and proxy: 403 FORBIDDEN "Platform admin access required";
    - originate: requireRole's "Insufficient permissions" (Z22 killed).
  - **After authentication on every route:**
    - admin.ts: right after requireAdmin on all 15;
    - proxy: after authenticateToken(true) and workflowAdminCheck;
    - originate: router-level authenticate.
    - Mutants placing the guard before authentication: the seat's G16, my Z01 on a parser-first route and Z02 on proxy are all killed.
  - **Spellings:**
    - Admitted at the gateway: SYSTEM_ADMIN, SUPER_ADMIN, super_admin, system_admin, Super_Admin, `sYsTeM_aDmIn`.
    - Refused: platform_admin and PLATFORM_ADMIN (at requireAdmin and workflowAdminCheck), ` SYSTEM_ADMIN`, `SYSTEM_ADMIN `, `ſuper_admin`, `SUPER_ADMİN`, an array or numeric role (unit and probe).
    - ORG_ADMIN, ISSUER_ADMIN, org_admin, issuer_admin and Org_Admin get 403 with 0 store calls and 0 queries.
    - Originate: see G410-2286-2.
  - **No existence oracle:** ORG_ADMIN on an existing vs a missing id gets the same 403 and identical body on all 9 id routes, with 0 store calls.
- **Q3 ORDER (QF). Holds; nothing leaks.**
  - On all 7 parser-first routes, a malformed body gets 400 for ORG_ADMIN, for no token and for SYSTEM_ADMIN alike. It is the parser's answer, with 0 store calls and 0 queries.
  - A NUL body gets the same VALIDATION_ERROR body for ORG_ADMIN. The answer does not depend on the role or the record.
  - On the parser-last routes, and proxy POST: ORG_ADMIN with a malformed body gets 403 (Z20 killed).
  - **ks815's no-token NUL cell** ("POST /api/admin/document-types refuses a NUL") passes on both arms.
- **Q4 READS UNCHANGED. Holds.**
  - All 49 GET route lines in admin.ts, proxy.ts and adminConfig.ts are byte-identical, develop vs merged. 22 of them name a kind or a settings path (the five kinds' reads, plus the public policy read and the per-user notification and privacy reads).
  - No refuseUnlessPlatform was added inside a GET.
  - **No read changed.** The pins do not cover two of them: see G410-2286-1.
- **Q5 THE SETTINGS PAGE (A1). Holds.**
  - **Where the decision lives:** the save decision is in settingsSavePayload.ts (failureDetail, plus the failed outcome's status and code). The page only maps `failed && 403 && FORBIDDEN` to Save off plus the banner.
  - **Not dismissible:** the banner has no button.
  - **Cells:** CSRF_TOKEN_MISSING 403, 400, 500 and 403-with-no-code leave Save on. Z16 (CSRF too) and Z17 (any 403 with a code) are killed.
  - **Network errors:** request() returns `{status: 0, error: string}`, so there is no code and Save stays on (code read; no cell).
  - **KS-1231 P2:** the KS-1231 shell suite is 39/39 on both arms, and 48/48 on develop+2286+2159.
  - **Browser (Playwright, Chromium):**
    - **The stack:**
      - the admin app's own vite from the merged tree (a wrapper changing only the port and the /api target);
      - the merged tree's REAL createAdminRoutes alone, under tsx;
      - verifyToken = jsonwebtoken RS256 with a throwaway in-process key;
      - the REAL redis module in its in-memory fallback mode;
      - an in-memory stand-in answering the three svc_gateway_settings statements;
      - stub login and /me.
    - **NOT real auth, the gateway's index.ts, CSRF or nginx.**
    - **ORG_ADMIN:**
      - Settings loaded; the press was refused (PUT 403);
      - "Platform admin access required" and the reason showed;
      - Save was disabled; no success banner.
      - After the error alert was closed, the reason stayed, Save stayed disabled, and a second press sent no PUT (host log).
      - The stored record stayed origin `seed`.
    - **super_admin:** saved ("Settings saved successfully!"), Save stayed on, no reason banner, and the record became origin `put`.
- **Q6 PR 2159.**
  - **merge-tree both orders:**
    - 2286 × 2159 and 2159 × 2286: rc 0, the same tree 00f6717f7467.
    - Via develop, both orders: (develop+2286)+2159 and (develop+2159)+2286 give rc 0 and the same tree.
  - **Planted controls, each committed on 2286 in `p`:**
    - admin.ts, the line before 2159's insertion: rc 1, CONFLICT admin.ts (both orders).
    - settingsSavePayload.ts, the line 2159 inserts after: rc 1, CONFLICT (both orders).
    - A non-adjacent plant 2 lines away: rc 0, as the seat also found.
  - **The combined tree runs:**
    - 2159's ks2111 cells (SYSTEM_ADMIN), ks2314, ks815, ks1256 and ks1230: 338/338;
    - admin whole: 201/201;
    - KS-1231 shell: 48/48.
  - **The other open PRs:** 16 besides 2159, and **0 touch any of the 9 paths**. Control: 2286's own list matches 9 of 9; 2159 hits 2.
- **Q7 CELLS and MUTANTS.**
  - **398 cells:** gateway 263, originate 122, admin 13.
  - **Red first on develop b8470f5fd331, with the 3 files copied in:**
    - 112 R are red by assertion: gateway 81 (78 "expected 200/201 to be 403", 3 "expected 400 to be 403"), originate 26, admin 5;
    - 286 P are green: 182 + 96 + 8;
    - 0 load failures.
  - **Merged:** 398/398.
  - **Mutants** (control green first and last; every file sha-restored; x clean):
    - **The seat's 53, re-typed: 53/53 killed.** G01-G18, G20-G24, X01, P01-P05, O01-O14, A01-A10. G19 (platform_admin) survives, equivalent as stated.
    - **Mine:**
      - killed: Z01, Z02 (before authentication), Z03, Z04, Z06, Z07 (guard on a GET), Z10 and Z11 (ORG_ADMIN admitted on a proxy route), Z16, Z17, Z20, Z21, Z22;
      - **survivors:** Z05, Z08, Z12, and Z14, Z15, Z18 (G410-2286-1). Z13 (guard just below `const d = req.body`) is equivalent.
- **Q8 WHOLE** (develop → merged, failure-name sets compared):
  - **api-gateway vitest:** 2101 (2092 pass, 9 skip, 0 fail) → 2364 (2355, 9, 0). 263 new names, all in the ks2314 file; 0 changed.
  - **originate jest:** 3284/3284 → 3406/3406. 122 new; 0 changed.
  - **admin vitest (harness config):** 188/188 in 11 files → 201/201 in 12. 13 new; 0 changed.
  - **packages/shared vitest WHOLE:** 1743 tests, 1742 pass and 1 fail on BOTH arms. **The failing-name sets are IDENTICAL:** `wallet-signature … KS-278 accepts a valid wallet signature over the message`.
    - The 11-22 lesson: ks1536-one-role-vocabulary is 99/99 on both arms.
  - **tsc:** 0 errors for api-gateway, originate and admin on both arms. Planted: rc 2 on each.
  - **eslint src:** 0 errors on both arms, with warnings equal (31, 29, 57). The PR's changed files: 0 errors, warnings 20, 0 and 2, as the body says. Planted debugger: rc 1 on each.
  - **The admin vite build:** rc 0 on both arms. Planted unresolved import: rc 1.
  - **Leg 14 (all 131 shell suites, both arms):** see Info. KS-1231 is 39/39 and the KS-528 router guard 27/27 on both arms.
- **Q9 CONSEQUENCES** (code read, plus the probe in G410-2286-3):
  - **Issuer portal, ORG_ADMIN menu only** (Layout.tsx 93-95):
    - Document Types: create crashes to the ErrorBoundary; delete silently does nothing.
    - Workflows: create and delete silently do nothing.
    - ISSUER_ADMIN gets the issuer menu, which has neither (the routes are reachable by URL, with the same outcome).
  - **Admin dashboard:**
    - Settings for ORG_ADMIN and ISSUER_ADMIN: Save refused once, then turned off with the reason.
    - The DocumentTypes, Workflows and IntegrationHub tabs live only inside `/platform/clients/:id` (ClientDetail). That is the Platform section, shown only to the local super_admin mapping.
    - VerificationPolicies.tsx and DocumentTypeDetail.tsx are not routed.
  - **Issuer Connectors and Settings:** they hit downloads and per-user notifications only, so they are unaffected.
  - **No other client was found:**
    - e2e: orgadmin-exhaustive uses loginAsAdmin (read, not run);
    - smoke and k6 only GET;
    - m365 only builds redirects.
- **Q10 WORDS.**
  - **The PR body:**
    - the figures are reproduced: 398 = 112 R + 286 P with the per-suite split; 53/53; 2101→2364, 3284→3406, 188→201; 1742/1743 ×2; eslint 20/0/2;
    - "No migration, package, lock, nginx or compose file" holds;
    - "Every GET keeps its old gate" holds;
    - the 2159 section holds (tree 00f6717f7467; one unchanged line, `const body = …`, between the two admin.ts edits).
    - **Exception:** the "any ASCII case" sentence (G410-2286-2).
  - **The deploy note** is present and accurate. QE is understated, not wrong (G410-2286-3).
  - **The "Platform Name" finding** is present and accurate.
  - **Facts comment 735781cd:** read-only, 3,960 B, unedited (updatedAt .129Z is before createdAt .138Z); KS-2314 is In Progress, priority 3, 2 comments.
    - It has the narrowing (KS-1863, KS-2236, KS-2279/KS-2313), the deploy note, QE and Platform Name.
    - Line 11's "any letter case" is G410-2286-2.
    - Line 1, "get 403 on every write of the five kinds", holds per the Q1 census.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- **Hook refusals, which ran nothing:**
  - a `=====` separator;
  - two unquoted `for … in $VAR` lists (re-issued under bash);
  - a `git -C <worktree> commit` (re-issued through gitx.sh).
- **A wrong rc read:** my first planted-control line printed rc 0 beside a listed CONFLICT, because `$?` was read after a substitution. I re-measured with each rc captured alone (the figures above). The non-adjacent plant 2 was then also kept as recorded.
- **Probe artefacts, which I did not count:**
  - The gateway probe's proxy half sends the role in an HTTP header. Node trims header whitespace and rejects non-Latin-1, so ` SYSTEM_ADMIN` read as admitted there, and the two Unicode cells threw.
  - The predicate itself refuses all four (unit check), and the admin.ts half refused them.
  - My first issuer and originate probe runs failed on tooling (vitest path; TS6133 unused names) and were re-run.
- **Playwright MCP** wrote 12 snapshot and console files (04-34 to 04-35Z) into `/Volumes/DevMASTER/WEDNESDAY/.playwright-mcp/`. They were moved into `_work/evidence/playwright_mcp/`; the other files there were untouched.
- **Scratch outside my folder:** the `/private/tmp/g410t` symlink, whose files stayed in `_work`. It was moved to `_quarantine`.
- **Edits to my own tools mid-session:** `run_cwd.py` was edited once, to honour a short TMPDIR.
- **The browser host and vite** were stopped by task id. No process was killed by name.
- **Linear:** the Linear key was read from the Blockchain project's `.env` into memory by the read-only reader, never printed. The 4 throwaway browser identities and their RS256 key existed only in the host process.
- No mail, no `cd`, no `rm`, no `!CODING` write (the seat's record was only read), no GitHub or Linear write, no container, no deployed box or database. D 81st's work was not touched.

## Not run
- Real auth, the full gateway index.ts (CSRF, limiters), nginx or compose in the browser.
- Any originate path through the gateway's unauthenticated `/originate/` mount.
- The e2e Playwright suites, Schemathesis, Akto, k6.
- Node 24.
- Preflight legs other than 14 (its runner ran whole).
