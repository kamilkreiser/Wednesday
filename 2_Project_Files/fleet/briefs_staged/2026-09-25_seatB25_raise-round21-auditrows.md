# SUCCESSOR BRIEF: Seat B 25th, Secuura/Blockchain. Round 21: raise four held Ornith passes as three PRs, and measure the three audit-baseline rows that lapse 2026-09-30. From Wednesday

## BLUF
You are **Seat B 25th**, the successor of Seat B 24th. Seat B 24th wrapped its board round and scored 0.98. Round 20 is merged (#1202-#1212, develop `6ab9d5021e96`) and deployed to kintsugi (Seat B 23rd). This round has **two jobs, and neither one deploys anything**:
1. **RAISE** four HELD local-model (Ornith) passes as **three PRs** on develop. **PR 1 = KS-1131** items 1 (F-A) and 2 (F-B): two READYs on ONE file, in ONE PR. **PR 2 = KS-1281**, vc-issuer. **PR 3 = KS-1128**, api-gateway. Each PR goes through a QA gate at its tier. Merges happen one at a time, and only on Wednesday's signed GO, under Kam's open-ended TESTED grant (2026-09-11).
2. **MEASURE the three `audit-baseline.json` rows that lapse at 2026-09-30T00:00Z (Wed 30 Sep, 10:00 AEST).** For each row, find out whether the advisory is still reported and whether an upgrade can fix it, or whether the only option is to renew it. Then **PROPOSE, one mail per row.** **You do not decide, and you do not edit the baseline.** Renewing a row moves an existing expiry. The advisory-baseline standing authority (Kam, 2026-09-09 08:12) does not cover that, and it never covers a HIGH advisory. Every proposal checks the grant's clauses in writing.
**Order:** ITEM 0 (plan confirmation), then ITEM 1 (the audit rows, read-only, because the date is fixed), then ITEM 2 (the raises), then HOLD for GO.
**Whose / where:** your own `s-b25-*` worktrees at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/` (ABSOLUTE paths, never under the clone). Push to `feature/…` branches on origin (`Secuura/Distributed_Secuura`) with base `develop`. PR bodies say `Refs KS-<n>` with linkKind `contributes`, and never use a closing word. Your record folder is `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-25_seatB-25th/`.
**Authority:** Kam's week instruction (panel 2026-09-21 14:05:04, `WEEK-INSTRUCTION.md` live, valid_until 2026-09-27): *"continue with the tickets, both local LLM and through the Claude agents"*. The TESTED grant (MERGE AUTHORITY below).

## ITEM 0: read, re-measure, then a PLAN CONFIRMATION mail BEFORE the first push
1. Read the following WHOLE: `5_Project_History/history.md` top entry (Seat B 24th, :24); `HANDOVER-seatB-22nd-successor-2026-09-23.md` (182 lines: the LEG D warning, the carried items, the tooling notes); this brief's four READYs and their briefs (paths in QUEUE).
2. **Refuse the launcher's single-session pull** (`Launch_Claude.command` "pull latest … if safe") and say so in the plan mail. Do not write to the shared checkout or its `.git`. The only exceptions are `worktree add` for your own `s-b25-*` worktrees and the `git fetch origin develop` in HOLDS.
3. **Re-measure the tip:** `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` must read `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`. If develop has moved to a descendant, run `git diff --name-only 6ab9d5021e96 <new>` against your 5 PR paths plus `Blockchain/Dev/scripts/audit/` (S66: the diff decides, not the SHA). An empty intersection is a measured non-event. Anything else means STOP that item and mail.
4. Reproduce every value in VERIFIED BEFORE SENDING: canonical sha16s, per-file blobs after apply, stacked-order equality, collisions, ticket states and the hyphenated-key scanner on the 3 branch names and 3 subjects. **The READY headers say "brief NOT LOCATED". That is wrong: all four briefs exist (paths in QUEUE).**
5. **Plan confirmation** (QUESTION mail, topic `plan confirmation (Seat B 25th)`). Include every launcher preflight warning VERBATIM. Answer each question below:
   - **Q1** Seat, pane and inbox filter. Confirm you REFUSED the launcher pull.
   - **Q2** The grouping, 3 PRs as tabled. For PR 1 the proposal is two commits, F-A then F-B. Either order gives identical bytes (measured).
   - **Q3** Tiers. PROPOSED: **tier 1 ×3, gated as ONE batch.** KS-1131's own briefs say tier 2. The drafter reads tier 1 for two reasons: the path is an auth-surface suite (`services/auth/src/__tests__/`), and F-A RELAXES a guard on the reset-token path (it counts call-shaped matches only). The 2026-09-21 precedent put auth-surface test pins at tier 1. Say which you read. Wednesday rules.
   - **Q4** Apply modes. KS-1131 F-A and F-B, and KS-1281 section 1, apply with `--recount --ignore-whitespace` (their checker-recorded opts; their hunk headers are miscounted). KS-1281 section 2 and both KS-1128 sections apply strict. Assert blob and line count after every apply.
   - **Q5** Branches and subjects, scanner result.
   - **Q6** The census per lane: auth REPORT, vc-issuer REPORT, api-gateway STOP on the 13th's ALLOW set. The `:5432` leg STOPs on every lane. See the KS-1128 note.
   - **Q7** The audit-row plan in ITEM 1, and the instrument you will use to freeze the clock.
   - **Q-AUTH** KS-1131 is the ONLY path under `services/auth/`. `auth.ts` and `wallet.ts` are read, never edited. Confirm.
   - **Q-1281** RULED by Wednesday 2026-09-25 (queue.md 10:3x comment + daily note): the VC store `vc_credentials_store` is NOT an auth-credential surface (not under `services/auth/`; the edit removes boot DDL only; no issuance, signing, verification or access line changes), so KS-1281 is in scope. Nothing to ask; confirm you read it.
   - **Q-DEPLOY** You deploy nothing. Confirm.
   Wednesday rules by ANSWER. You proceed only on the ANSWER.

## ITEM 1: THE THREE ROWS LAPSING 2026-09-30 (measure and propose; build nothing, edit nothing)
File: `Blockchain/Dev/scripts/audit/audit-baseline.json` at `6ab9d5021e96`. `baseline-contract.mjs` compares `expires` against the UTC date: *"`expires: 2026-09-06` means DEAD ON THE 6th"*. So all three rows lapse at 2026-09-30T00:00Z = **Wed 30 Sep 10:00 AEST**. From then, preflight legs audit:gate and audit:locks refuse EVERY Blockchain/Dev push, from every author.

| # | GHSA | package | ticket (state) | severity (registry, drafter read 10:4x) | row's own reason, in short | drafter's lock read at the tip (NOT an audit run) |
|---|---|---|---|---|---|---|
| R1 | GHSA-frvp-7c67-39w9 | @hono/node-server | KS-530 (Backlog) | medium | "fix is >=2.0.5 only, a semver-MAJOR v1->v2 bump" | **The registry now lists a 1.x patch, `< 1.19.15` → patched `1.19.15`**, so the row's premise looks STALE. Locks: root `node_modules/@hono/node-server` 1.19.17 (patched, prod-marked); root `@prisma/dev/node_modules/@hono/node-server` 1.19.11 (devOptional); `services/mcp-server` 1.19.14 (**prod: a runtime image**); `services/originate` 1.19.11 (devOptional) |
| R2 | GHSA-jjmj-jmhj-qwj2 | react-router-dom | KS-528 (In Progress) | medium | v7-only migration | **The registry lists react-router-dom `>=6.30.2 <=6.30.5` → patched `6.30.6`**. All 4 locks carry 6.30.4 (admin, issuer, verifier, root; prod). **Kam's 09-17 migrate-and-date ruling re-dated rows 11 and 12 (the two `react-router` rows) and NOT this one.** That card said this row "IS fixable by a patch and is being fixed separately". No such fix is on develop, and no branch at origin names it (drafter's `ls-remote` grep) |
| R3 | GHSA-mwp4-54f8-5fhr | ip-address | KS-729 (In Progress) | **HIGH** | root + issuer legs via @cardano-sdk/core ^9.0.5 | Root and `frontend/issuer` still resolve `node_modules/ip-address` **9.0.5** (patched is 10.3.1). mcp-server is 10.7.0 and shared/anchoring are 10.4.0. **Kam ruled `override` (to 10.3.1) on 2026-09-17 18:31:29** (card `secuura-audit-row-ip-address-high-override`: *"Overrides in the issuer and root package.json, the issuer build + unit suites, tier-1 QA gate with a real-browser pass on the issuer"*). It has not landed |

**For each row, MEASURE:**
- (a) **Is the row still reported?** Run the repo's own gate (`scripts/audit/audit-gate.mjs` and `audit-locks.mjs`, the preflight legs) at develop in your own worktree. Print the ratio of legs that RAN. `audit-gate: npm audit errored … SKIP` is a SKIP, not a pass. A row the gate prints as "no longer reported — remove" is a REMOVE candidate. Note that the set churns (2026-09-09).
- (b) **The lapse, proved with a frozen clock** at 2026-09-30T00:00Z, the way the #1020 gate measured it on 09-17. Put any preload outside the repo, with its own positive and negative controls (Wednesday's 2026-09-20 17:55:58Z ruling). Expect exactly R1-R3 to lapse. Rows 11 and 12 lapse 2026-10-02 and are NOT in scope. **Report KS-528's v7 status anyway**, because their row text says the seat reports before 2026-10-01 if the migration slips.
- (c) **Is an upgrade reachable?** Resolve it in a scratch copy inside your OWN worktree (`npm install --package-lock-only` or the equivalent), never in the shared checkout, and push nothing. R1: can mcp-server move to ≥1.19.15, and what happens to the @prisma/dev-nested and originate devOptional copies? R2: 6.30.4 → ≥6.30.6 in the 4 locks, and does `react-router` move with it? R3: the ruled override. Say whether it can land and pass a tier-1 gate before 2026-09-30.
- (d) **Runtime reach**, with a control (clause 2): which runtime images carry the vulnerable version, and whether the package sits in both a test lock and a shipped tree (the EXCEPTION).

**Then PROPOSE, one QUESTION mail per row** (topic `audit row <GHSA> 2026-09-30 proposal`), each with Context / Question / Meanwhile / Needed-by **Sat 26 Sep 18:00 AEST**. Each proposal is one of FIX (a bump PR, built only on Wednesday's ANSWER), REMOVE (the gate no longer reports it) or RENEW (a new date plus the reason). **Every mail carries the grant check in writing, clause by clause** (`0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md`): (1) severity moderate or below; (2) MEASURED not to reach a runtime image, with a control, by you; (3) the expiry is the SHARED re-triage date; (4) flagged to Kam in the same action; the EXCEPTION (a test lock plus a shipped tree stops for Kam); and "does NOT cover": **HIGH ever, anything shipped, any measurement without a control, and it is BASELINING ONLY: no pin bumped, NO EXISTING EXPIRY MOVED.** On the drafter's reading, every RENEW here falls outside the grant, so a RENEW goes to Kam. R3 is HIGH, so any path except the ruled override goes to Kam. The grant is Wednesday's, not yours: you measure and propose, and you never clear your own blocker.

## ITEM 2: THE QUEUE (3 PRs, all tier 1 as proposed; ONE batch gate)
The READYs, their runs and their briefs are in Wednesday's tree and are READ-ONLY to you. Apply each canonical `patch.diff` verbatim, per section, with its `section_<k>.opts`. Any deviation not named here is a STOP. Both KS-1128 runs PASSED (`night/done.md` rows :502 and :503). **Only the READY's run (`night2`, after Wednesday's decl_splice harness fix) is canonical.**

**PR 1: KS-1131 items 1 + 2 (F-A CALLSHAPED + F-B), self-testing, ONE file**
- File: `Blockchain/Dev/services/auth/src/__tests__/ks963-preauth-rethrow.test.ts` (tip blob `9427c652ac2d`, 327 lines). This file is both the product (its helper `assertConsumeIsGuarded`) and its test.
- READYs: `night/READY_KS-1131-KS-1131_ornith35b-q4_BRIEFED-CODEPATCH-KS963-PREAUTH-RETHROW-PASS-7of7_2026-09-25.diff.md` (F-A, run `runs/2026-09-25_ks1131-ornith35b-night3`, canonical sha16 `a31104081f161344`, +28/−1) and `…-FB-COMMENT-IS-NOT-A-GUARDED-CONSUME-PASS-7of7_2026-09-25.diff.md` (F-B, run `…-night4`, sha16 `d90c0ed605a9d169`, +27/−0). Briefs: `night/briefs/KS-1131.md` (F-A) and `night/briefs/KS-1131-FB/KS-1131.md` (F-B).
- Checker, verbatim: F-A `PASS A4 RED-FIRST … (1 failed / 15 run …)`, `PASS A5 … (15 passed / 15 run)`, suite `baseline: total=828 failed=0 | after: total=830 failed=0`, `A7 tsc rc 0`. F-B has the same shape (1 red of 15; 828 → 830).
- Blobs after (drafter): F-A alone `560bb49c242f` / 354 lines. F-B alone `4f921648add5` / 354. **Both stacked `041396c7fce5` / 381, identical in both orders.** Expected auth suite on the stacked file: 832 (828 + 4). This number is not measured.
- **Red proof, one arm per fix (a conjunction is proved per conjunct):** with both test hunks and neither fix, EXACTLY the F-A red cell and the F-B red cell go red, and the controls stay green. With F-A's fix only, exactly the F-B red cell stays red. With both fixes, everything is green. Name the cell each arm falsified.
- Ticket SCOPE (KS-1131 BLUF, quoted): *"The tier-1 gate measured that all three read RAW TEXT and so can be fooled in both directions — a false red on a comment, a false green on a deleted consume, a false green on a non-`await` write — while the product itself is correct on every one of the five pre-auth callers driven over real HTTP. One file, one test pass, one helper away from closing."* **This PR NARROWS the ticket. It does not close it:** items 3 (F-C, `:256` non-await write) and 4 (P2, positional wallet slice) remain. Name both in the body. The brief's residual also goes in the body: call-shaped counting still false-greens `// consumeResetToken(x)` in the `!user` block. Mark it UNVERIFIED unless red-proved.
- Branch `feature/ks-1131-ks963-structural-cells-count-raw-text-a-comment-naming-r21-callshaped-fa-fb-1`; subject (80) `KS-1131 CALLSHAPED: ks963 helper counts consume CALLS, not mentions (items 1, 2)`. `Refs KS-1131`.

**PR 2: KS-1281 EXISTENCECHECK, vc-issuer, two files**
- `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` (tip `030d3112dd38` / 265 → after `8a46bbf7f0d5` / 261) and NEW `…/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts` (→ `125b65f81aaf` / 46; absent at the tip).
- READY `night/READY_KS-1281-KS-1281_ornith35b-q4_BRIEFED-CODEPATCH-CREDENTIALREPO-PASS-7of7_2026-09-25.diff.md`, run `runs/2026-09-25_ks1281-ornith35b-night`, sha16 `f4dca715e93586c5`. Section 1 needs `--recount --ignore-whitespace` (strict rc 128 `corrupt patch at line 19`). Section 2 is strict. Brief: `night/briefs/KS-1281.md`.
- Checker: `A4 (1 failed / 2 run)`, `A5 (2 passed / 2 run)`, suite 127 → 129, 0 new reds, tsc rc 0.
- Ticket SCOPE (quoted): *"Remove the runtime `CREATE TABLE` from `credentialRepo.ensureTable()`, since the migration path already owns the table, or reduce it to an existence check."* **This PR COVERS the code scope by the second shape (an existence check). Say which shape in the body.** It is still `Refs` only. The ticket is a runtime boot WARN, so §5f applies: Done waits for Wednesday's closing pass after a kintsugi log observation. Body lines, from the brief's UNMEASURED section: a DB not built by migration 001 no longer gets the table created at runtime; whether the least-privilege role can SELECT the table on every environment is NOT measured. The one other held READY on this file is KS-1121 `@@ -70,41`. It is region-disjoint, it is not in this round, and it was reallocated to a Claude seat.
- Branch `feature/ks-1281-vc-issuer-boot-warns-could-not-ensure-vc_credentials_store-r21-existencecheck-1`; subject (69) `KS-1281 EXISTENCECHECK: vc-issuer credentialRepo sends no runtime DDL`. `Refs KS-1281`.

**PR 3: KS-1128 SEEDWARN, api-gateway, two files**
- `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` (tip `cf371028fb56` / 1227 → `cd2583963f04` / 1229) and NEW `…/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts` (→ `39e6b0a87e8c` / 80; absent at the tip).
- READY `night/READY_KS-1128-KS-1128_ornith35b-q4_BRIEFED-CODEPATCH-STARTUP-MIGRATIONS-PASS-7of7_2026-09-25.diff.md`, run `runs/2026-09-25_ks1128-ornith35b-night2`, sha16 `4dbb93b735102d1a`. Both sections strict. Brief: `night/briefs/KS-1128.md`.
- Checker: `A4 (2 failed / 4 run)`, `A5 (4 passed / 4 run)`, suite 750 → 754, tsc rc 0.
- Ticket SCOPE ("What is owed", quoted): *"Raise the arm to `warn` with a message that names it a failure (`Platform tenant seed FAILED (platform DB)`), error text to 200 chars, in the same shape as the main-DB arm."* and *"A cell that proves it: boot the real `runStartupMigrations()` with `PLATFORM_DATABASE_URL` pointing at a database whose `tenants` table cannot take the insert, and assert the `[WARN]` line."* **This PR NARROWS the ticket.** The code ask is met. The proof uses an in-process fake pg, not the real PostgreSQL the ticket names, so that bullet remains. Say so in the body.
- **Readers outside your lane (the LEG D lesson):** `packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts:177`, `services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts:382` and `scripts/__tests__/ks949_main_seed_idempotence.test.sh:77` all read this product file by TEXT. Run all three on the head. The sibling api-gateway suites `ks1062`, `ks1125` and `ks1272` drive the same function.
- **Census:** the new test stubs `DATABASE_URL`/`PLATFORM_DATABASE_URL` at `*.invalid:5432`, and its CONTROL cell asserts the pg redirect. The `:5432` leg must read **0 attempts**. Any attempt is a STOP, as the rule says.
- Branch `feature/ks-1128-the-platform-tenant-seeds-catch-logs-platform-tenant-seed-r21-seedwarn-1`; subject (75) `KS-1128 SEEDWARN: a failed platform tenant seed logs WARN FAILED, 200 chars`. `Refs KS-1128`.

**For all three PRs:**
- Prettier was not run by any brief. The repo's formatting gate runs on your push; state its result.
- Lanes (runner from `package.json` at the tip): auth `vitest`, vc-issuer `vitest run`, api-gateway `vitest`, plus packages/shared and the shell-suite runner for PR 3. Take the baselines BARE at `6ab9d5021e96` and SERIALLY (the 21st: in parallel they skipped 13 vc-issuer tests). Report `bare N / patched N+k` per lane and `tsc --noEmit` per service.
- Tooling: copy `5_Project_History/2026-09-23_seatB-21st/raise/` (`raise20.py` with the cumulative-count fix; `wtadd20.sh`, `push20.sh`, `lock20.sh`/`lockfn20.sh`/`lockproof20.sh`, `targets20.py`, `dry20.sh`, `merge20.py`, `merge_series20.sh`, `verify_pr22_b22prefix.py`) as `*21.*` into YOUR record folder. Keep the pre-fix copies beside them. Re-key them to your 3 keys and lock `worktrees/.push-lock-21/`, and prove the lock's four arms on a SCRATCH path. The self-testing precedent is Seat B 22nd's `2026-09-23_seatB-22nd/raise/ks1143-*` (P0 baseline / P1 red-first / P2 green-after). `bodies20.py` was never re-keyed, so hand-write the bodies.
- Every READY FOR QA mail carries the five things in STANDING_LINES "READY FOR QA": the PR number, its head read from origin in the same action, a ticket comment naming the PR, the Test Evidence block written by you who ran the tests, and what was NOT covered. Add the tier-1 batch tree and the GO string you expect: `GO: merge #<a>, #<b>, #<c> batch`.

## THE ROUND ENDS AT READY 3 PLUS THE THREE ROW PROPOSALS, THEN HOLD
Your only wake is a DKIM-passing mail from `wednesday-agent@` with that exact GO subject, naming every head. Merge one at a time: dry run first, sha-pinned, re-predicted over the then-current develop, targets.json written from the gate's MERGE ADDENDUM verbatim, inside the lock, with the ruleset re-read first. All tickets STAY In Progress after merging. No GO means no merge. At ctx ~80, hand over HOLDING.

## HOLDS
- **No deploy of any kind, and nothing to demo.** PRs 2 and 3 change runtime images (vc-issuer, api-gateway). Kintsugi is a separate seat on Wednesday's commission after the merges. Demo = UAT and moves only on Peter's nod. Migration 048 before any deploy (not exercised).
- **Nothing to Peter or Stuart beyond ticket comments.** Comments are facts only, BLUF-first, and name PRs, shas and tickets, never a fleet seat. Any rule-7 bytes go to Wednesday first. The extranet is input only.
- **Never delete: quarantine** into a dated folder and record the move. **No `--no-verify`, no `--admin`, no force-push.** A gate that stops you is asking a question.
- **Fetch develop before wrap:** `git fetch origin develop` in `2_Project_Files`, then `cat-file -t` of the fetched tip (the local model's G6 gate reads this object store).
- **Signature classes pause for Kam:** production, money, external communication to a human, anything irreversible.
- **Auth:** the ONLY path under `services/auth/` in this round is `ks963-preauth-rethrow.test.ts`. Any other byte under `services/auth/` is a STOP.
- **The audit baseline:** no edit, no re-date, no removal in this round. Proposals only (ITEM 1).
- `Refs` only. Put no key other than the PR's own in any branch, title, subject or squash body (MG-3). KS-963, KS-950 and KS-1062 are Done and ARCHIVED; they appear in the diffs as CONTENT only. Never reopen them.
- Redirect to a file and read `$?` on its own line. The Bash tool is zsh, where `${PIPESTATUS[0]}` is empty. zsh also reads `"$T:path"` as a modifier (Seat B 24th's own slip), so brace it: `"${T}:path"`. After every `git apply`, restore disk modes from the index and assert `test -x .githooks/pre-push`.
- A control must be able to fail. A pass line carries a RATIO. "What did my branch change" is `X...HEAD`.
- Search the board by symbol, path and error string before filing anything. File no tickets in this round unless Wednesday's ANSWER says so.
- Other clients are out of scope entirely.
- **GitHub refuses an approval from our own account (HTTP 422).** Meet it and STOP. Wednesday's GO is the approval.

## MERGE AUTHORITY (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md`)
*"We approve our own work; the author merges once it is TESTED"* (Kam 2026-09-11 16:56:00 / 16:56:44 / 16:58:04). TESTED = a QA gate verdict (GO or GO WITH FINDINGS) at the PR's current head, plus a Test Evidence block, plus our own suites. *"Wednesday's GO, naming the head SHA, is the approval."* *"Untested, or no GO → no merge."*

## RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura)
- **The five 09-22 cards (KS-1084 part B, KS-974, KS-1163, KS-998, KS-789) are DELIVERED** by Seat B 24th's comments (`ae430016…`, `c52a3cfa…`, `8a6cc696…`, `003d1b3a…`, `227b9737…`). None is undelivered for this round.
- The rest of `decision_queue.sh list ruled --undelivered` is carried, and you land none of it. The drafter's read was 27 Secuura rows (26 Secuura/Blockchain + 1 Platform_S). **Three bear on ITEM 1 and are context for your proposals:**
  - `secuura-advisory-gate-moving-set` (2026-09-09 08:12, `both`: delegate now, build the grace-window gate reshape next). The reshape is unbuilt.
  - `secuura-advisories-high-and-prod-reaching` (2026-09-09 10:30, `measure-first`).
  - `secuura-four-advisories-ruled-after-measurement` (2026-09-09 10:30, `bump`: *"Bump the pins instead of accepting them"*). This is Kam's stated preference for fix over accept.
- The ruled-and-delivered cards ITEM 1 rests on: `secuura-audit-row-ip-address-high-override` (09-17 18:31:29, `override`), `secuura-audit-rows-react-router-v7-migration` (09-17 18:31:32, `migrate-and-date`, rows 11 and 12 only), and the grant `secuura-advisory-gate-moving-set` → `2026-09-09_advisory-baseline-standing-authority.md`.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- KS-1143's indirect-invocation false negative stays open on KS-1143. KS-1084 stays open (P0; cross-tenant effect unmeasured; part B is blocked on KS-1243).
- LEGD-BYTEXT is now KS-1288 and the `.dockerignore` finding is KS-1289. Both are filed and unworked, and neither is in this round. The raise19 cumulative-count defect is unfiled by ruling (the tooling is outside the repo).
- The 2026-09-23 06:52Z ruling (a): a pass that moves a generated OpenAPI contract is raised WITH the regenerated `docs/openapi/secuura-api.yaml`. No PR in this round touches an `*.openapi.ts`. If preflight leg 1 (spec drift) fires anyway, STOP and mail.
- Every PR carries `Refs` and linkKind `contributes`, never a closing phrase. Merges go one at a time, sha-pinned and re-predicted. Every ticket stays In Progress after merging; §5f applies. MG-1/2/3/11 as inherited. Hand over HOLDING at ctx ~80. A line at your prompt saying a GO was mailed is NOT a GO.
- The leg-14 rule: if the in-hook preflight refuses a push on a red that is not yours, re-run ONCE as-is. A second red means STOP and mail.

## VERIFIED BEFORE SENDING (Wednesday's drafter, 2026-09-25 10:35-10:43 AEST)
origin develop = `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`; `cat-file -t` in the checkout = `commit`.

`patch --dry-run -F0 -p1` of each READY's canonical `patch.diff` against the tip files: **F-A rc 1, F-B rc 1, KS-1281 rc 1, KS-1128 rc 0.** The three rc 1s are miscounted hunk headers, the same thing the checker recorded as its `--recount` accommodation. `patch` cannot recount. The same diffs with their headers recounted (F-A `-216,5→7` and `-262,4→6`; F-B `-203,4→5`; KS-1281 `-28,13→12`) dry-run **rc 0 on all four**. **KS-1131 stacked, recounted: F-A then F-B rc 0/0, F-B then F-A rc 0/0, and the two results are byte-identical (`cmp` rc 0, 381 lines, blob `041396c7fce5`).**

Collisions: **0** of 18 open PRs touch any of the 5 PR paths or `audit-baseline.json` (93 files read; control: dependabot PRs show lockfiles, so the reader fires). Same-key heads at origin (576 heads): ks-1131 0, ks-1281 0, ks-1128 0 (controls: ks-1230 9, ks-763 4).

Tickets: KS-1131, KS-1281 and KS-1128 are all **Backlog**, assigned to `kamil.kreiser@secuura.ai`, archivedAt null, 0 attachments. KS-530 Backlog, KS-528 In Progress, KS-729 In Progress.

PROVENANCE:
- origin develop `6ab9d5021e96…`; object present | `git ls-remote origin refs/heads/develop` + `git cat-file -t` on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-25
- the three 2026-09-30 rows (GHSA-frvp KS-530; GHSA-jjmj KS-528; GHSA-mwp4 KS-729) and their reasons | `git show 6ab9d5021e96:Blockchain/Dev/scripts/audit/audit-baseline.json` | read 2026-09-25
- lapse = dead ON the date, UTC | `git show …:Blockchain/Dev/scripts/audit/baseline-contract.mjs` :10, :92, :122 | read 2026-09-25
- lock versions (hono 1.19.14 mcp-server prod; react-router-dom 6.30.4 ×4; ip-address 9.0.5 root + issuer) | python parse of 45 `package-lock.json` via `git show` at the tip (control: express in 28 locks) | read 2026-09-25
- advisory severities and patched versions (frvp 1.19.15 on 1.x; jjmj 6.30.6; mwp4 HIGH, 10.3.1) | GitHub REST `GET /advisories/<id>`, read-only, `GH_TOKEN` from the project `.env` | read 2026-09-25
- the advisory grant's clauses, verbatim | `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md` | read 2026-09-25
- the ip-address `override` and react-router `migrate-and-date` rulings; the three undelivered 09-09 advisory cards | `0_Brain/dashboard/data/decisions.json` + `decision_queue.sh list ruled --undelivered` | read 2026-09-25
- canonical sha16s, apply opts, checker verdicts | `runs/<run>/out.md.checker/{patch.diff,section_*.opts}` + the READY files (`cmp` READY fence vs canonical = 0 on all four) | read 2026-09-25
- dry-run rcs, stacked equality, blobs after | `patch --dry-run -F0 -p1` + `patch -F0` in scratch `/private/tmp/…/scratchpad/raise25/` + a python git-blob hash (control: the tip blobs equal `git ls-tree`) | read 2026-09-25
- open-PR collisions | GitHub REST `pulls?state=open` + `pulls/<n>/files` | read 2026-09-25
- same-key heads | `git ls-remote origin 'refs/heads/*'` | read 2026-09-25
- ticket states and scope sentences; content keys KS-963, KS-950, KS-1062 Done and archived | Linear GraphQL read-only, Secuura key | read 2026-09-25
- cross-package readers of startup-migrations.ts | `git grep` at the tip | read 2026-09-25
- Seat B 24th's wrap, the five comment ids, "nearest audit fuse 2026-09-30" | `5_Project_History/history.md` :24-:36 | read 2026-09-25
- KS-1128's two PASS rows; night2 canonical after the harness fix | `night/done.md` :502-:503 + Wednesday `git log` 06c9da23f / ad00fa610 | read 2026-09-25

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 10:46
