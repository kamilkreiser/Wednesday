PR 2268: GO WITH NOTES (at head 98d1032ffa21914338419ca323e20dd719eeb4fe; tier 1)

# Gate 392, tier 1 (Opus), PR 2268 (KS-2300), 2026-11-20 ~16:35-17:06 AEDT

## Pins
- **Pinned twice, at 16:34:58 and 17:05:47**, with git ls-remote plus gh pr view (Secuura project gh credential, read-only). Same values both times:
  - PR 2268 OPEN, MERGEABLE, head 98d1032ffa21, ONE commit, parent = develop 90ef2cf004e3 (PR 2267's squash). 9 paths, +527 -22. updatedAt 05:31:44Z.
  - develop = 90ef2cf004e39676fe7afde2c12313dcf71a8995; PR 2099 head = 8967de8b17558890dc4ace2732cb8350768df601.
- **Merged state = the head** (fast-forward on the develop tip). Every "head" figure below is the merged state.
- PR body at source: 11,468 B, sha256 8fd3ed16ffc7 (evidence/pr_body.md).

## How I measured
- Clone `_work/g` from GitHub (`--reference-if-able` gate 391's clone, `--dissociate`). Worktrees: `h` (head, suites/static), `x` (head, mutants/probes), `d` (develop), `p` (PR 2099 head + my planted commit, never pushed).
- node_modules and `packages/shared/dist` copied (`cp -c`) from gate 391's `_work/h` (no lockfile or shared change between 2929ec29ff07 and this head). Node v26.8.1, vitest, TMPDIR /private/tmp/g392t.
- Scripts in `_work/`: `run_cwd_g392.py`, `suites_g392.sh`, `static_g392.py`, `mutants_g392.py` (gate 391's engine, my spellings), `lin_read_g392.py` (one read-only GraphQL query), `probes/g392-probe.test.ts` (the PR's own ks2300 harness + my Q1-Q4 probes, writes JSONL, asserts nothing), `probes/g391-selfapprove.g392.test.ts` (gate 391's probe, STANDARD added).
- Probes ran on `x` and on `d`; afterwards moved to `_work/_quarantine/`. End state: h, x, d each 0 porcelain lines; x users.ts sha256 e254e46f2367… = the head blob.
- Not touched: no seat tree, no GitHub or Linear write, no database server, no container, no mail.

## Findings

No HIGH or MEDIUM finding. Every rule holds as ruled, through the real router; nothing I tried gets an above-STANDARD approval, a cross-organisation approval, a self-review or an organisation change through for a non-platform caller.

### LOW
**G392-2268-1: two non-equivalent mutants of the approve bound survive all 2,069 cells (pinning gaps; no hole at this head).**
- **G16, the bound ignores a reviewer with NO organisation:** `if (!subjectOrganizationId || (reviewerOrganizationId && reviewerOrganizationId !== subjectOrganizationId))`. Under it an org-less ORG_ADMIN (KS-2299's seeds) approves STANDARD for any user of its tenant who has an organisation. The only reviewer-null cell ("a reviewer with no organisation approves nothing") uses a subject that ALSO has no organisation, so the subject-null clause refuses first. The PR's stated consequence ("org-less org admins approve nothing") is therefore true at the head but not pinned one-sided. A reviewer with no users row is not a cell either (my probe: 403, correct).
- **G13, the token claim as a FALLBACK when the row has no organisation:** `reviewerRow?.organizationId ?? req.user?.organizationId`. The builder's M17c (claim wins over the row) is killed; the fallback order is not, because no cell gives an org-less (or row-less) reviewer a claim of the subject's organisation. "Token claim never wins" holds at the head (probe Q2-claim, Q2-norow: 403) but is only half-pinned.
- Fix shape for a follow-up: one cell, ADMIN_NOORG (claim = ORG_A1) approves STANDARD for USER_A1 = 403. It kills both.
- Also survived, and equivalent at this head: G5 (self rule moved after the PENDING check: only a non-PENDING own request answers 400 instead of 403, no write either way), G6 (reviewer row read tenant-scoped: its own row is in its own tenant), G11 (self rule on `request.userId` instead of `subject.id`: both folded).

**G392-2268-2: words that do not hold exactly (nothing false that matters).**
1. "Platform admins (`SYSTEM_ADMIN`, `SUPER_ADMIN`, any case)" (PR body and flow fragment; the test header says "any ASCII case"): `isPlatformRole` folds any case, but both routes' role gates admit only `SYSTEM_ADMIN`, `super_admin`, `SUPER_ADMIN` (+ `ORG_ADMIN`, and `admin` on PATCH). Probe: `system_admin`, `Super_Admin` get 403 "Admin role required" on review. Fail closed and pre-existing; gate 391 made the same note.
2. "every SQL write to `users` in `services/*/src` (23 statements)" (PR body, ticket): NOT reproduced. My scan (UPDATE / INSERT INTO / DELETE FROM users, multi-line, non-test, all services' `src`) finds 16 hits, one of them inside a comment (auth.ts:1363), so 15 statements; adding services/auth/integration gives 21. The builder left no script for this count. The CONCLUSION holds (see Q4).
3. The ticket's facts comment says the originate door went to "its own ticket" without the number (KS-2302); the READY already disclosed this.

### INFO
**G392-2268-3: the cap reads the canonical target but the approve writes the raw stored string.** A stored target of `standard` or ` standard ` passes the cap and is written verbatim to `users.verification_level` (probe Q1-target). Unreachable: submit's zod enum (users.ts:160-163) stores only STANDARD/ENHANCED/HIGH/GOVERNMENT and no other writer of `verification_upgrade_requests` exists (saveVerificationRequest callers: submit, approve, reject, restore). Pre-existing for platform callers; not a defect of this PR.

**G392-2268-4: gate 391's g391-selfapprove probe, re-run as-is, measures only its first level on the head.** Its memory store keeps the first (refused) request PENDING, so HIGH/GOVERNMENT/STANDARD then answer "already pending" (400) and review 404. ENHANCED: submit 200, review **403** "Cannot review your own verification request", level BASIC. On develop all four read 200/200 with the level raised (evidence/selfapprove_{x,d}.jsonl). My per-level probe with fresh state (Q3) covers all four on the head.

## The commission's questions
- **Q1 THE CAP: holds.** ORG_ADMIN approve (evidence/probe_x.jsonl, Q1-target):
  - ENHANCED, `enhanced`, `Enhanced`, ` ENHANCED`, `ENHANCED `, `\tHIGH`, `high`, GOVERNMENT, `gOvErNmEnT`: 403 "Only a platform admin can approve a verification request above STANDARD", no save, no write, row PENDING, level BASIC.
  - Fail closed: `PLATINUM`, `''`, long-s `ſtandard`, `STANDARD\0`, `STANDARD` + zero-width space, `ENHANCEDİ`: 403, nothing written.
  - STANDARD (and `standard`, ` standard `, BASIC, SOCIAL): 200; NONE: KS-1236 400. See G392-2268-3.
  - Order: a capped approve performs exactly ONE platform-scope read (the tenant check's subject); the KS-1236 read and the reviewer-row read never run (Q1-order).
  - Reject uncapped: ENHANCED/HIGH/GOVERNMENT/PLATINUM reject = 200 REJECTED, level unchanged.
  - Platform uncapped: SYSTEM_ADMIN, SUPER_ADMIN, super_admin approve GOVERNMENT = 200. `system_admin`, `Super_Admin`, `org_admin`, `ORG_ADMIN `, `admin`, `ISSUER_ADMIN`, `platform_admin` = 403 at the role gate.
  - Shapes: action `APPROVE`, `['approve']`, `{x:'approve'}`, `approve ` = 400, PENDING kept. A body `targetLevel`/`verificationLevel` of GOVERNMENT on a STANDARD request is ignored (STANDARD written).
  - **No spelling or shape got an above-STANDARD approval through.**
- **Q2 THE ORGANISATION BOUND: holds.** Other organisation same tenant: 403 "Only an admin of the user's own organisation…". Token claim of the subject's org with the row in A1: 403. Reviewer with no users row: 403. Reviewer row org in upper case vs subject lower: 403 (fail closed; the column is UUID so real values are canonical). Empty string on both sides: 403. Bare `admin` cannot review at all (role gate).
  - **Move-then-approve is closed:** PATCH USER_A2 into ORG_A1 = 403 (org unchanged), then approve = 403. ORG_ADMIN moving ITSELF into A2 (lower, upper with another field, array) = 403 ×3, then approve A2's user = 403.
  - Gaps in pinning only: G392-2268-1.
- **Q3 SELF-REVIEW: holds.** Self submit STANDARD / ENHANCED / HIGH / GOVERNMENT, then approve = 403 "Cannot review your own verification request" and reject = 403, row PENDING, level BASIC (all four). Token id upper and mixed case: 403 (self). Request `user_id` stored upper against the lower subject row: 403. Percent-encoded or padded token ids are other ids (no row) and are refused by the bound (403); a token id is server-minted, not caller-spelled. Platform self-approve (SYSTEM_ADMIN, super_admin, SUPER_ADMIN) = 200, as ruled. The red baseline: on develop the same self path writes the raised level (G392-2268-4).
- **Q4 THE ORGANISATION RULE ON PATCH: holds.** For ORG_ADMIN and bare `admin` alike (38 cases, Q4-patch):
  - own-tenant org, foreign org, nonexistent org, non-UUID: identical 403 bodies, `getOrganizationTenant` called 0 times, no write. **No oracle.** (develop: 200 / 400 / 400 / 400 with a lookup each.)
  - resend lower/upper/mixed: 200 (one lookup, as before). Padded resend: 403.
  - null over nothing: 200, no lookup. null over a value: 403. `''` over nothing or value: 403.
  - Non-strings (123, `[stored]`, `{id}`, true, false, 0): 403. (develop wrote the ARRAY `[stored]` with 200, since `String([x]) === x`; the PR closes that too.)
  - Self move: 403. Foreign-tenant target: 404, no lookup. Platform move: 200. `organization_id` / `OrganizationId` / `orgId` keys: dropped by the allow-list, org unchanged.
  - **Census at this head (auth + api-gateway), my own:** request doors that write `users.organization_id` = auth `PATCH /api/users/admin/:id` (userRepo field map :824 -> UPDATE :893) only, reached also through the gateway's forward. `createUser` (:688) carries `user.organizationId`, but none of its request callers sets it: admin create (users.ts:703-722), invite stub (createInvitedStub), register (KS-1107 refusal auth.ts:236), social (auth.ts ~1390) and wallet (wallet.ts:212). `PATCH /me` takes names and phone. KS-2272's invite claim (auth.ts:984) writes hash/status/emailVerified/role only. Gateway: only the demo seed INSERT (admin.ts:1296) and the level UPDATE (:1395, platform-only since KS-1936). No `prisma.user(s).update/create` anywhere in services (zero; positive control: the regex finds the 15 raw statements). **The builder's census missed no organisation door.** Outside the two services, originate's INSERT (adminConfig.ts:2155) sets no organisation.
- **Q5 THE FIVE REWRITTEN CELLS: faithful.**
  - ks467:319: still pins "foreign and missing org indistinguishable", now as 403, and ADDS `getOrganizationTenant` not called (kills the builder's M16). Nothing weakened beyond the ruling.
  - ks467:330: 200 + write reversed to 403 + no write, exactly Kam's b; its platform control (:336) is untouched.
  - ks467 approve cell: keeps "app-gated platform-scope write" at STANDARD, and pins ENHANCED = 403 with no write, as option a's detail ("the existing test that pins ENHANCED is rewritten"). `submitRequest` gains a defaulted `targetLevel`, so the file's other two review cells are unchanged.
  - ks1236:148: still proves KS-1236 binds a tenant admin (STANDARD target, HIGH subject -> 400, nothing saved, PENDING); the shared organisation is the minimum the new bound needs. Green on develop by design, as stated.
  - ks1536:219: still proves bare `admin` is not a platform role (a platform caller would pass the rule and reach KS-467; G2 is killed by it).
  - Red-first reproduced: head's four test files on develop's users.ts = **133 cells, 23 failed** (19 new + 4 rewrites), the READY's figures.
- **Q6 MUTANTS (whole auth suite each, on the merged state; evidence/mutants.out, mutants_m1_m10.out):**

  | mutant | tsc | failed | killed by |
  |---|---|---|---|
  | M1 cap removed | 0 | 7 | ENHANCED/HIGH/GOVERNMENT, lower-case, unknown, stale, ks467 approve |
  | M2 cap on raw string | 0 | 2 | lower-case `enhanced`, `PLATINUM` |
  | M3 unknown admitted | 0 | 1 | `PLATINUM` |
  | M6 self rule removed | 0 | 4 | the four self cells |
  | M7 self approve-only | 0 | 1 | self reject |
  | M8 self without fold | 0 | 1 | upper-case token |
  | M10 org rule removed | 0 | 8 | move/clear/give/self/bare + ks467 ×2 + ks1536 |
  | M12 org compare without fold | 0 | 1 | resend upper |
  | M13 null over nothing = change | 0 | 1 | null over nothing |
  | M14 null = no change | 0 | 1 | clear with null |
  | M17 bound removed | 0 | 2 | other org, token claim |
  | M17c claim wins | 0 | 1 | token-claim cell |
  | G1 org rule on truthy presence | 0 | 1 | clear with null |
  | G2 org rule exempts bare admin | 0 | 2 | ks1536, bare cell |
  | G3 bound also on reject | 0 | 1 | other-org reject control |
  | G4 cap also on reject | 0 | 2 | ENHANCED reject control, ks467 approve |
  | G14 org rule only when stored | 0 | 4 | give-org, ks1536, ks467 ×2 |
  | G15 bound ignores subject null | 0 | 1 | subject with no org |
  | **G13, G16** | 0 | **0** | **survivors, non-equivalent: G392-2268-1** |
  | G5, G6, G11 | 0 | 0 | survivors, equivalent at this head |

  BASE 2069/2069. Product file restored and sha256-checked after every mutant. (My first M1/M10 spellings did not parse; re-spelled and re-run, both compile.)
- **Q7 WHOLE:**
  - Auth suite: develop 2038/2038 in 163 files; head 2069/2069 in 164 files; failure-name sets equal (both empty).
  - tsc 0 (planted: rc 2, 1 error). eslint `--max-warnings 0` on the six TS files: rc 0; on develop's five: rc 0 (planted no-debugger + unused: rc 1).
  - Ratchet: 41 baselined, 0 new, 0 stale, 164 test files (planted: 1 new, rc 1).
  - Fragments: OK (planted two-h2 fragment: FAIL).
  - check:openapi: CHECK PASS (planted edit of the KS-2300 yaml line: CHECK FAIL; yaml restored, sha256 equal). The yaml's +6 -3 is exactly auth.openapi.ts's three text changes.
  - merge-tree head vs PR 2099's live head: **rc 0** (tree 650bc0b3556b). Planted control (my commit 54ed991310d1 on PR 2099's head rewriting the same `organizationId` description line; never pushed): **rc 1**, CONFLICT (content) in secuura-api.yaml. Head vs develop: rc 0. PR 2099 touches only the yaml among this PR's nine paths. The body says "Whichever of the two PRs merges second regenerates the yaml": present.
  - Not re-run: the standalone 6-service ratchet and its leg test.
- **Q8 WORDS:**
  - PR body: the rules, messages, placement, consequence, red/green 23/133 and 133/133, 2038/2069 suite figures, +6 -3, nine paths +527 -22, merge-tree figures and residual list reproduce. Exceptions: G392-2268-2.1 and .2. The M-table: every row I re-ran (M1-M3, M6-M8, M10, M12-M14, M17, M17c) is killed as stated; my kill sets are by the whole suite.
  - KS-2300 ticket (read-only): High (priority 2), In Progress; title and BLUF match the plan; the four checklist lines include Q1c; created 05:04:35Z, before the push. "23 statements": G392-2268-2.2.
  - Facts comment 97be504c (1,804 B; updatedAt 05:31:14.857Z not after createdAt 05:31:14.875Z, so unedited): every measurable sentence holds (head, parent, rules, 31/19/12, 5 rewrites, 20 mutants, suites, static legs, merge-tree). Push timings are the builder's (UNMEASURED beyond ls-remote).
  - Consequence (org-less org admins approve nothing): TRUE at the head (probe: 403), half-pinned (G392-2268-1).
  - Residuals: KS-2279 (gateway org DELETE), KS-2302 (originate org DELETE), KS-2298, KS-2299, the unregistered review route (auth.openapi.ts header lists it as deferred): stated correctly; none is made worse by this PR.

## Two-NO-GO cap
Not engaged.

## Not run
- The four platform suites, a booted auth or gateway, a real Postgres (the cells and probes use mocked repositories; no SQL changed), a real Redis, the admin dashboard, any deployed environment, Node 24.
- The standalone 6-service ratchet and its leg test.
