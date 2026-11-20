PR 2267: NO GO (at head 540af1ec55ddcf495c04039e38e29988dfd664e7; tier 1)

# Gate 390, tier 1 (Opus), PR 2267 (KS-2287), 2026-11-20 ~13:30-13:55 AEDT

## Pins
- **Pinned twice, at 13:30:39 and 13:53:34**, with gh pr view plus ls-remote (gh credential helper, own clone). Same values both times:
  - PR 2267 is OPEN, not draft. Head 540af1ec55dd, base 038425cafaec, 1 commit, 6 files, +531 -19, updatedAt 2026-11-20T02:27:48Z.
  - develop = 038425cafaecfb29e800e0a9187d76f9fddc3622.
  - PR 2099 head = 8967de8b17558890dc4ace2732cb8350768df601.
- **Merged state = the head.** The head's only parent is 038425cafaec, which is the develop tip, so merging is a fast-forward. Every "merged" figure below was measured on the head.
- **PR body at source:** 12,325 bytes, sha256 ced799fb01a2…. It is byte-identical to the builder's drafts/pr_body.md.

## How I measured
- **Clone:** `_work/g`, cloned from the GitHub URL with `--reference-if-able` the shared checkout and `--dissociate` (no alternates file left). These worktrees are mine:
  - `h`: the head (= merged state);
  - `d`: develop;
  - `x`: mutants;
  - `m`: PR 2099's head plus one planted commit;
  - `mm`: a scratch merge commit fa6aa94e56c9 of the head and PR 2099's head.
- **node_modules:** `cp -c` of root, packages/shared, services/auth and services/shared (plus packages/shared/dist) from gate 389's `_work/h`. The root and auth lockfiles are byte-identical between gate 389's develop 35d677937401 and 038425cafaec. packages/shared and services/shared are unchanged between them. Absolute symlinks: 0.
- **Run conditions:** Node v26.8.1 (not LTS), vitest 4.1.12, TMPDIR /private/tmp/g390t.
- **Scripts** (all under `_work/`): `run_cwd_g390.py`, `suites_g390.sh`, `mutants_g390.py`, `probes/g390-probe.test.ts`, `probes/pglite_uuid_case.mjs`, `lin_read_g390.py` (one read-only GraphQL query). Evidence is in `_work/evidence/`.
- **End state:** h, d and x each show 0 porcelain lines. users.ts in x is sha256 0aaf3af2e575…, the same as h. Planted files are in `_work/_quarantine/`.
- **Not touched:** no seat tree, GitHub or Linear write, no database server, no container.

## Findings

### HIGH
**G390-2267-1: "never on themselves" can be bypassed. An ORG_ADMIN raises its OWN level, up to STANDARD, by spelling its own id in upper case.**
- **FOUND.** The new self rule compares the path parameter with the token's user id as raw strings: `if (id === adminId)` (users.ts, inside the KS-2287 block). Three things line up:
  - The id format check before it, `z.string().guid()`, accepts upper-case hex.
  - The target lookup `SELECT … FROM users WHERE id = $1` runs against a `UUID` column (001_initial-schema.sql, startup-migrations.ts and init.sql all say `id UUID PRIMARY KEY`). Postgres reads UUID input in any letter case.
  - `adminId` is the token's `userId = user.id`, and Postgres returns that lower-case.

  So `PATCH /api/users/admin/<OWN-ID-UPPER-CASE> {"verificationLevel":"STANDARD"}` from an ORG_ADMIN fails the self comparison. It then finds its own row and passes the tenant 404, because it is the same row. The cap passes for STANDARD or lower. The organisation rule compares the caller's row with the target's stored organisation, and here both are the SAME row, so it passes. The level is written.

  The gateway forwards the id verbatim: admin.ts, `encodeURIComponent(id)`; normalisePath only collapses slashes.

  This breaks a clause of Kam's card verbatim ("never on themselves"). It also breaks Wednesday's Q3 = (a), the PR body's "never on itself", the openapi text and the KS-2287 facts comment. The bypass is bounded: STANDARD or lower, and only for a caller that has an organisation. But it is one request, needs no other account, and is reachable through the shipped gateway.
- **TESTED:**
  - *zod:* `z.string().guid()` on an upper-case UUID answers true (`zod_probe.mjs`).
  - *PGlite (in-process):* a UUID table with getUserById's exact SQL shape. An upper-case spelling of a stored lower-case id returns the row (the id comes back lower-case), and an `UPDATE … WHERE id = $upper` writes it (evidence/pglite_uuid_case.out).
  - *Through the real router:* the PR's own harness with only the by-id repository reads and writes made case-insensitive, as Postgres is:
    - P1, own id in lower case: 403 "Cannot change your own verification level".
    - P2, same caller, same body, own id in UPPER case: **200**, the row's level BASIC to STANDARD. `updateUserPlatformScope` was called with the upper-case id (evidence/probe_log_x.txt).
  - *No cell covers it:* the harness's Map is keyed exactly, so an upper-case id answers 404 there.
  - *The obvious fix is safe for the cells:* comparing case-insensitively (mutant X9) keeps all 2,029 cells green. Comparing `target.id === adminId` after the lookup would also work, since that value is canonical from the row.
  - NOT tested: a real Postgres engine or a booted gateway and auth. PGlite is Postgres's own UUID input function.
- **HOW:** `probes/pglite_uuid_case.mjs`, `probes/g390-probe.test.ts` (copied into x, run, then moved to `_quarantine/g390-probe.ran2.test.ts`), `zod_probe.mjs`.

### LOW
**G390-2267-2: rule mutants that every one of the 2,029 cells misses.** None of them opens a hole at this head; they are pinning gaps. All ran on the whole auth suite and all compile.
- **FOUND, and why each one matters:**
  - **X4:** create refuses a JSON `null` level (400 instead of the default BASIC). The ruling and the PR body name null as allowed, and no cell sends null. My probe P3 shows the head gives 201 BASIC.
  - **X7:** create lets an org admin choose `NONE` (cap computed as "not above BASIC" instead of "BASIC only"). The ruling says absent, empty or BASIC only, and no cell creates at NONE.
  - **X3:** `trim()` removed. Only a tightening; no cell sends padding. Probe P5: `' standard '` and `'STANDARD\t'` are accepted and written as STANDARD.
  - **X6c:** create's platform check by exact name `role === 'SYSTEM_ADMIN'`. That would cap super_admin and SUPER_ADMIN on create, and no create cell uses them. The PATCH twin (X6) IS killed, by the ks1536 cells.
  - **X8:** the "unchanged" compare case-folded on raw values. Equivalent at this head, because both sides are already canonical.
  - **X2:** the caller row read with the tenant-scoped `getUserById`. The mock answers both reads from one map. On a real database it could only fail closed (403).
  - **X5:** organisation compared case-folded. Equivalent for UUIDs.
  - **No self-id case mutant exists:** the shipped code IS the defect (G390-2267-1).
- **TESTED:** `mutants_g390.py` against the whole auth suite (evidence/mutants.out). X2, X3, X4, X5, X6c, X7 and X8 each read tsc 0 and failed 0 of 2,029.
- **HOW:** the same script; the probe results are in evidence/probe_log_x.txt.

**G390-2267-3: some sentences do not hold.**
- **FOUND:**
  1. "never on itself", in the PR body, the KS-2287 facts comment e94e5ef8 and auth.openapi.ts/yaml, does not hold (G390-2267-1).
  2. "yaml regenerated (+30 -4)", in the PR body, the READY and the commission: the yaml diff is **+24 -6**. 30 is the total of changed lines. The six numstats do total +531 -19 as stated.
  3. "Platform admins (`SYSTEM_ADMIN`, `SUPER_ADMIN`, either casing)": `system_admin` in lower case is refused 403 at the PATCH door's exact-string role list (pre-existing; probe P11). So "either casing" holds only for SUPER_ADMIN. Cosmetic.
- **Everything else I checked holds:**
  - N1: "itself included" (probe P9).
  - N3: Users.tsx offers basic, standard, enhanced, high and government; there is no none or social option.
  - N4: the three demo ORG_ADMIN seeds carry a tenantId and no organizationId.
  - "an unknown value read back as BASIC" (mapDbVerificationLevel `|| 'BASIC'`).
  - 37 cells, 1,992 and 2,029 tests, tsc, eslint, ratchet, fragments and check:openapi all match my figures.
  - The facts comment: 1 comment on KS-2287, by the board account, created 02:28:02Z. I read it read-only via the Linear API. KS-2287 is In Progress, priority 2.
- **TESTED / HOW:** `git diff --numstat` (own clone); `lin_read_g390.py` (evidence/ks2287_linear.json); probe log.

### INFO (outside this PR, for routing)
**G390-2267-4: the pre-existing KS-467 own-ROLE rule has the same upper-case-id bypass.**
- FOUND: `if (safeUpdates.role && id === adminId)` is unchanged by this PR. Probe P2b: an ORG_ADMIN PATCHing its own id in upper case with `{"role":"VERIFIER"}` got 200 and the role changed. SYSTEM_ADMIN still cannot be granted, because of the separate platform-only role check.
- Not this PR's defect, but the same fix shape applies. Wednesday may route it to a ticket. The sweep belongs to whoever fixes it: the other `=== req.user.userId` / `=== adminId` comparisons on by-id routes.

**G390-2267-5: N1 and N2 are not made worse.**
- N1: the PR closes only the one-request move-and-set; probe P8 shows a resent stored HIGH still passes alongside a move. The two-request walk-round still works, including the variant where the admin moves ITSELF into the target's organisation (P9: 200 then 200, level set). The PR states this.
- N2: the review-approve path is untouched (diff: users.ts hunks only at the helpers, create and PATCH).

## The commission's questions
- **Q1, the rule:**
  - Cap: ENHANCED, HIGH and GOVERNMENT give 403. A padded `'GOVERNMENT '` also gives 403 (P5).
  - Other organisation, no organisation, and none on either side: 403.
  - Self: 403 with a lower-case id, but **bypassed with an upper-case one (G390-2267-1)**.
  - Value check on both doors: unknown, a number, `{}`, `''`, an array, `true`, a dotless-i `hıgh`, a long-s `ſocial`/`ſtandard`, and (on PATCH) `null` all give 400. The canonical name is what gets written.
  - Bare `admin` on PATCH is capped. With no users row (a platform_admins holder) it gets 403 (P10).
  - Platform admins stay uncapped and unbound: SYSTEM_ADMIN, super_admin and SUPER_ADMIN set GOVERNMENT on a foreign-tenant user (P11 and the cells), and SYSTEM_ADMIN may set its own level.
- **Q2, the caller's organisation:**
  - It is read from the caller's users row under platform scope.
  - A stale token claim loses in both directions (the cell, and P7).
  - A missing caller row gives 403 (P6).
  - The one-request move-and-set gives 403 and stores nothing.
  - A foreign-tenant target still gives 404, and mutant M14's shape is pinned by the 404 cell.
- **Q3, "unchanged is not a change":**
  - It is compared with the stored, mapped level read before the request. No other field in the same request can change that value; the only write happens after the rules.
  - Lowering HIGH to BASIC passes.
- **Q4, create:**
  - For a non-platform caller only absent, null, `''` or BASIC (any case) pass; anything else gives 403.
  - Smuggled keys `organizationId`, `verification_level`, `level` and `tenantId` are ignored. The user is created at BASIC in the caller's tenant (P12).
  - Gaps: null and NONE are not pinned (G390-2267-2).
- **Q5, mutants:** reproduced on the merged state, whole auth suite each, with my own spellings:

  | mutant | tsc | failed | killed by |
  |---|---|---|---|
  | M1 (cap dropped) | 2* | 5 | ENHANCED/HIGH/GOVERNMENT cells, bare admin |
  | M5 (organisation rule dropped) | 2* | 6 | other organisation / no organisation / none-and-none / move-and-set / token claim |
  | M6 (null == null) | 0 | 1 | none-and-none |
  | M8a (token claim only) | 2* | 2 | token-claim cell |
  | M8b (claim ?? row) | 0 | 1 | token-claim cell |
  | M12 (unchanged counts as a change) | 0 | 2 | the two resend controls |
  | X1 (self rule dropped) | 0 | 1 | self cell |

  \* tsc 2 = noUnusedLocals on the local my `if (false)` edit orphaned. The cells kill each one regardless. Survivors are listed in G390-2267-2.
- **Q6, the whole suite and static checks:**
  - Auth suite: develop 1,992/1,992 in 162 files; head 2,029/2,029 in 163 files. Failure-name sets equal (both empty).
  - New file alone: 37/37.
  - tsc 0 (planted: 1).
  - eslint on users.ts, auth.openapi.ts and the new test: 0 (planted: no-debugger error plus 2 no-unused-vars).
  - Ratchet: 41 baselined, 0 new, 0 stale, 163 files (planted: rc 1, new errors named).
  - Fragments: OK (planted two-heading fragment: FAIL).
  - check:openapi: CHECK PASS plus 422 examples resolve (planted yaml edit: CHECK FAIL).
  - The yaml is consistent with auth.openapi.ts, but it is +24 -6, not +30 -4.
- **Q7, PR 2099:**
  - merge-tree of the head against PR 2099's live head: rc 0.
  - Planted control (PR 2099 head plus an edit to the create request's `verificationLevel` description line): rc 1, CONFLICT (content) in the yaml.
  - The head against develop: rc 0.
  - On the scratch merge commit, `generate-openapi --check` passes. At these heads the second merger's regeneration would be a no-op, and the PR body's instruction is correct.
- **Q8, the PR body and facts comment:** see G390-2267-3.

## What would turn this to GO
One line in the PATCH rule: compare the self condition on a canonical id. Either `target.id === adminId` after the lookup, or both sides lower-cased. Add a cell where the caller sends its own id in upper case against a case-insensitive by-id mock; it should be 403 with the row unchanged. Optionally add cells for create `null` (201 BASIC) and create `NONE` (403). Then re-gate as a delta.

## Not run
- The four platform suites, a booted auth service or gateway, a real Postgres engine (PGlite only, in-process), the admin dashboard, any deployed environment, and Node 24.
