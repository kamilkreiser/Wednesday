# [Wednesday -> Secuura/Blockchain] SEAT B: raise Ornith's held diffs for security, originate, anchoring, vc-issuer, kyc and the OpenAPI yaml as PRs, one ticket per PR
# STAGED 2026-09-16 21:06. Plan and measurements: `WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-16_raise_PLAN.md`.
# Kam approved this work (panel 2026-09-16 20:40:59, confirmed 20:41:47 "yes. claude agents"): *"you have the approval to spin up other local agents to test, approve, merge and move things forward"*. Approval of each PR = Wednesday's GO naming the head SHA, after a QA gate verdict at that head plus your Test Evidence block (Kam's 2026-09-11 TESTED grant; CONTRIBUTING.md "Adopted merge flow" step 6).

## BLUF
- **What:** you raise **20 PRs**, one per ticket. KS-1172 and KS-1173 share ONE PR. Each applies local-model (Ornith) diffs that passed their checker 7/7 at develop M55 `48e65c435` and were source-read by Wednesday.
- **Your partition: you write ONLY in**
  - `Blockchain/Dev/services/security/**`
  - `Blockchain/Dev/services/originate/**`
  - `Blockchain/Dev/services/anchoring/**`
  - `Blockchain/Dev/services/vc-issuer/**`
  - `Blockchain/Dev/services/kyc/**`
  - `Blockchain/Dev/docs/openapi/secuura-api.yaml` (GENERATED: always regenerate, never hand-edit)
  - `Blockchain/Dev/docs/VOCABULARY.md`
- **NOT yours. Two other seats run in parallel on these, so never edit them:**
  - Seat A: `Blockchain/Dev/services/api-gateway/**`, `Blockchain/Dev/services/demo-service/**`, `Blockchain/Dev/packages/shared/**`, `Blockchain/Dev/services/auth/**`
  - Seat C: `Blockchain/Dev/scripts/**`, `.githooks/**`, `Start_Up/**`, `systemTest/**`, `Blockchain/Dev/deployment/**`, `Blockchain/Dev/CONTRIBUTING.md`, `Blockchain/Dev/docs/DEV-PROCESS.md`, repo-root `CLAUDE.md`
  - If your work seems to need a file outside your partition, STOP and mail a QUESTION.
- **You are the ONLY seat that regenerates the OpenAPI yaml.** The generator reads every `services/<svc>/src/<svc>.openapi.ts`. Run it on your branch tip each time; never merge a hand-edited yaml.
- **WHOSE / WHERE:**
  - Remote: `origin` = `git@github.com:Secuura/Distributed_Secuura.git`, identity `kksecura`.
  - Base: `origin/develop`, which was `0b25f823f` at drafting. Re-read it before every branch.
  - Branches: `feature/ks-<n>-ornith-<slug>`.
  - Tickets: team KS, on the board account.
  - Local work happens ONLY in your own worktree: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-b`. Never the shared checkout `2_Project_Files`.
- **Your files did NOT move between M55 and the tip** (GitHub compare API: all 36 changed files are under `systemTest/schemathesis/`). `0b25f823f` is not in the local object store, so fetch first.
- **Collision:** open PR **#922** (KS-679, head `e60a24c50`) also changes `docs/openapi/secuura-api.yaml` and `anchoring.openapi.ts`. It is not yours. If it merges first, your regeneration picks it up. Never copy its hunks.

PROVENANCE:
- Kam's approval for Claude seats to test, approve, merge | Kam panel chat 2026-09-16 20:40:59 + 20:41:47 (kam_msgs.sh, view=wednesday) | read 2026-09-16
- origin/develop = 0b25f823f; 36 files changed since 48e65c435, none touched by any READY file | GitHub REST branches + compare 48e65c435...0b25f823f (2026-09-16_raise_PLAN.md lines 17-19) | read 2026-09-16
- the held diffs and their PR NOTES | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_*.diff.md + night/done.md | read 2026-09-16
- partition: no file in two seats (111 paths, 0 overlaps) | 2026-09-16_raise_PLAN.md partition table (mechanical check) | read 2026-09-16
- merge rule: TESTED = QA gate verdict at head + Test Evidence + Wednesday's GO naming the head SHA; feature PRs squash | Blockchain/Dev/CONTRIBUTING.md:107 + "Adopted merge flow" step 6 at develop | read 2026-09-16
- Kam rulings carried verbatim in this brief | decision_queue.sh list ruled --undelivered | read 2026-09-16

## ITEM 0: before any PR
1. **Plan confirmation.** Mail `wednesday-agent@agentmail.to`, subject `[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (seat B)`. Body: this queue as re-derived at the tip, any bundle that no longer applies (named), and **every warning your launcher printed at boot, verbatim**. Start on the ANSWER. This is approval-class, so wait for it.
2. Set up the worktree:
   ```
   git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" fetch origin > f.out 2>&1; rc=$?
   git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" worktree add --detach "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-b" origin/develop
   ```
   Then run `npm ci` in `<wt>/Blockchain/Dev` once (KS-691).
3. **Baseline:** at `origin/develop`, run `npm test -w services/<svc>` for security, originate (jest), vc-issuer, kyc and anchoring, plus `npm run check:openapi`, and record the pre-existing reds.

## HOW TO APPLY A READY FILE (all bundles)
READY files are in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`. Read them; never edit them.
1. Copy the fenced diff body or bodies into a scratch patch. **Split it into one patch per file** at each `--- ` / `+++ ` pair (hunk headers are often miscounted).
2. **De-indent any header that starts with a space.** Measured in your set: `READY_KS-1172-A3` line 16 and `READY_KS-1172-B3` line 15 (` --- a/…`). This is formatting, not content.
3. **Paths:** service-relative paths (`services/…`) apply with `--directory=Blockchain/Dev`.
4. Apply each section: `git -C <wt> apply --3way --recount --ignore-whitespace <section>` (redirect output, read `rc`). If that fails, try `patch -p1 --fuzz=2 -d <wt> < <section>`. If that also fails, **apply the READY's `-`/`+` lines by hand at the named line** and say so in the PR body. Then `git -C <wt> diff` must show every READY `+`/`-` line and nothing unintended.
5. **Red-proof before green.** For a product fix: test sections first, record the red, then the product section, record green. For TEST-ONLY: apply the tamper the READY names, get red, `git -C <wt> checkout -- <product file>`, get green, and confirm no product diff.
6. **Accommodations measured by Wednesday's apply check** (scratch copy at M55, your queue in order):
   - 49 of 52 sections apply clean.
   - `READY_KS-975-item2` product hunk (`rateLimitScope.ts` ~:223) and `READY_KS-976-A` product hunk (`index.ts` ~:1467) apply **only with `patch --fuzz=2`**. Read the result against the READY's -/+ lines.
   - `READY_KS-1121` second hunk of `__tests__/credentialRepo.test.ts` (~:55): its context does not match. Apply that hunk by hand.
   - `READY_KS-692` has TWO diff fences, product and test. Apply both. The product hunk needs `--recount` (the header says new=34, the actual is 31).
7. **Test-file name collisions:** KS-974 A/B, KS-976 A/B and KS-1074 A/B/C each share one auto-generated test name. Apply one part, rename its test as the bundle says, then apply the next.

## THE FLOW, per PR (no step skipped)
1. `git -C <wt> fetch origin`, then `git -C <wt> switch -c feature/ks-<n>-ornith-<slug> origin/develop`. **Same-file bundles are strictly serial.** Cut the next branch only after the previous PR on that file merged. The yaml counts as a shared file for every bundle that regenerates it. At most 3 PRs open awaiting GO (PLAN Q2).
2. Apply, do the PR-NOTES edits, run the tests named. `cmd > out 2>&1; rc=$?`, then read the file. No pipes on a status; zsh has no `PIPESTATUS`.
3. Commit and push. The pre-push preflight runs. **Never `--no-verify`. Never force-push.** If the hook refuses with `check-stack-safety.sh` "… is missing — … deleted" lines, that is the KS-1034 class under a worktree hook: STOP and mail a QUESTION.
4. Open the PR against `develop`. The body must carry:
   - the ticket
   - the READY filename(s)
   - the checker run dir from the READY header
   - *"authored by the local model (Ornith) from a Wednesday-written brief; source-read by Wednesday; re-run by seat B at `<sha>`"*
   - the bundle's PR-must-say lines
   - the **Test Evidence block** (DEV-PROCESS form: Touched / Ran / NOT run / Migrations+config; the platform-suite lines with the Schemathesis failing SET vs the develop baseline set; Unit suites; Cross-cutting guards `npm test -w packages/shared`)
5. Comment on the ticket naming the PR (facts only, no @-mentions).
6. Mail `wednesday-agent@agentmail.to`, subject **`[Secuura/Blockchain -> Wednesday] READY FOR QA: #<n> <ticket> @<head sha>`**. Read the head from origin in the same action. Body:
   - first line `Seat B`
   - PR URL, ticket plus comment
   - Test Evidence summary
   - **what was NOT done or NOT covered**
   - accommodations used
7. **STOP that PR** until Wednesday's GO. You may start the next file-disjoint bundle meanwhile.
8. GO arrives in `coagent@agentmail.to` as `[Wednesday -> Secuura/Blockchain] GO: #<n> <ticket> @<sha>`. **Merge only if `<sha>` equals the PR head read from origin now.** To merge: `gh pr merge <n> --squash --match-head-commit <sha>` (CONTRIBUTING.md:107, feature PRs squash). No `--admin`. If GitHub demands a review, STOP and mail; never approve your own PR (422).
9. After the merge: fetch, confirm `MERGED` and the merge commit, set the ticket state, move on.
10. **Findings:** fix on the same branch (merge develop in; no rebase plus force-push), re-run, and send a new READY FOR QA mail with the new head. An old GO never covers a new head.

**Never merge without a GO naming the head SHA. Never deploy. Never `--no-verify`. Never force-push.**

## Ticket state on merge
Close (Done) **only if the PR delivers the ticket's WHOLE scope sentence**. Otherwise comment what landed (PR plus merge commit) and leave it open. Per-bundle defaults are below; the ticket's words win.

## Test commands (run from `<wt>/Blockchain/Dev`)
- **Single file:**
  - vitest services: `npx vitest run src/__tests__/<file>` inside `services/<svc>`
  - originate (jest): `npx jest src/__tests__/<file>` inside `services/originate`
- **Whole service:** `npm test -w services/<svc>` (security, vc-issuer, kyc and anchoring are `vitest run`; originate is `jest`)
- **Cross-cutting guards (any service change):** `npm test -w packages/shared`
- **Types:** `npx tsc --noEmit -p services/<svc>`
- **OpenAPI** (any bundle marked YAML): `npm run generate-openapi`, then `npm run check:openapi`. The regenerated `docs/openapi/secuura-api.yaml` is committed in the same PR.
- **Schemathesis `pr`** on your slot per PLAN Q1: `export SECUURA_STACK_SLOT=3; source systemTest/slot-target.sh`, then `python3 scripts/run.py pr` in `systemTest/schemathesis`. Record the failing SET. If there is no stack or memory is short, the line reads `not run: <measured reason>`.

## QUEUE (test-only first; chains in order)
Scope sentences are the Linear titles, read 2026-09-16 ~21:1x with `issue(id){title state comments(first:50)}`, sorted client-side. All open: Backlog, except KS-1172 and KS-1173 (Todo).

### B1. KS-1120: TEST-ONLY (vc-issuer)
- **READY:**
  - `READY_KS-1120-F1_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1120-F2_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md` (the q8 twin `READY_KS-1120-F2_ornith35b-q8_…` is equivalent; raise ONE)
- **Scope:** "GET /api/presentations/:id exact-or-404: the memory-path PREFIX class and the DB-miss → memory get are unpinned, and the test's `pgModel` under-reports the base disclosure (QA-966 F-1 + F-2 + F-3)"
- **PR must say:** no product change. F1 tamper is `:128` exact get → a `startsWith` scan. F2 tamper is `:127` → `return undefined`. **F-3 (reword the test header :29-31, :190-193, per the ticket's recommendation item 3) is not in the diffs. Do it in this PR.**
- **Tests:** both files red under tamper and green at the tip, `npm test -w services/vc-issuer`, shared, tsc.
- **On merge:** Done if F-3 landed.

### B2. KS-1171 record 8j: TEST-ONLY (anchoring)
- **READY:** `READY_KS-1171-8j_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md` (descriptive file name; the q8 twin is equivalent, so raise ONE)
- **Scope:** "Guard 3's re-poll reads a MIXED window as ABSENT — one early "not found" then an unreachable chain still schedules a retry that can re-mint a written-ahead transaction (#805 tier-1 r3 residue)"
- **PR must say:** pins record 8j only (tamper `:260`, confirmed gated on polled). **The mixed-window design decision stays with the ticket.**
- **Tests:** the file red under tamper and green at the tip, `npm test -w services/anchoring`, shared, tsc.
- **On merge:** **leave OPEN**, with a comment.

### B3. KS-1118 F-2: TEST-ONLY (originate, jest)
- **READY:** `READY_KS-1118-F2_ornith35b-q4_TESTONLY-JEST-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "POST /api/verification/verify: the `documentHash`-over-`hash` precedence is unpinned, and the why-comment + test header overclaim "every body that worked before keeps its answer" (QA-965 F-2 + F-3)"
- **PR must say:** F-2 pin (tamper `:742`, hash read third). **F-3 (narrow the two overclaiming sentences to the ticket's wording) is not in the diff. Do it in this PR.**
- **Tests:** the file red under tamper and green at the tip, `npm test -w services/originate` (READY: 637 → 637), shared, tsc.
- **On merge:** Done if F-3 landed.

### B4. KS-887: TEST-ONLY, modify in place (security)
- **READY:** `READY_KS-887_ornith35b-q4_TESTONLY-MODIFYINPLACE-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "KS-869 test defect (mine): the WRITE-half column-list pin can be satisfied by the COALESCE clause, so a statement missing connector_id from the column list passes all six cells". Acceptance: *"The X2 tamper reds. The current fix still passes."*
- **PR must say:** one file, `ks869-connector-id-persisted.test.ts:84-91`. It captures the column list, plus a `,$14,$15)` placeholder pin. Tamper: `index.ts:313` connector_id dropped. The placeholder pin matches TWICE in `index.ts`; optionally tighten it with a `svc_api_keys`-anchored regex. Cite the gate's X2 measurement.
- **Tests:** red under tamper and 6/6 at the tip, `npm test -w services/security`, shared, tsc.
- **On merge:** Done.

### B5. KS-975, items 1 + 2 (security `rateLimitScope.ts`)
- **READY:**
  - `READY_KS-975-item1_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-16.diff.md`
  - `READY_KS-975-item2_ornith35b-q4_VITEST-PASS-7of7_2026-09-16.diff.md` (**product hunk with fuzz**)
- **Scope:** "rateLimitScope tri-state: a MALFORMED `sub` silently became a 403 on the ungated /check, and `null` still slips through explicitScope's second line"
- **PR must say:**
  - Kam ruled on 2026-09-16 at 07:01 (card `secuura-ornith-decision-class-tickets-1121-629-975`, a): *"keep the 403 and pin it"* and close item 2's backstop hole in the same pass.
  - Add the one sentence at `rateLimitScope.ts:114-116`: *"A MALFORMED `sub` is itself a refusal (KS-975 item 1, ruled 2026-09-16) — pinned by ks975-malformed-sub-is-refused.test.ts."*
  - Item 2 is unreachable at the wire today (`resetRateLimitSchema` refuses `null` first). The backstop now agrees with the schema. **This is not a live fix.**
- **Tests:** item-1 file red under tamper and green at the tip; item-2 file red→green; `npm test -w services/security`; shared; tsc.
- **On merge:** Done, citing the card.

### B6. KS-747 (security `security.openapi.ts`, YAML)
- **READY:** `READY_KS-747_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`
- **Scope:** "Spec drift: GET /api/security/keys declares no parameters while the handler requires organizationId — the contract suite can never reach its 200 branch"
- **PR must say:** inserts `request: { query: z.object({ organizationId: z.string().uuid() }) }` in the GET `/api/security/keys` registration. The handler is unchanged. The served contract follows the registry. **Regenerate the yaml.**
- **Tests:** the new file red→green, the security suite, shared, tsc, `generate-openapi` + `check:openapi`. Schemathesis `pr` per Q1.
- **On merge:** Done.

### B7. KS-908 (security `index.ts`, chain 1 of 4)
- **READY:** `READY_KS-908_ornith35b-q4_PASS-7of7-REANCHORED_2026-09-15.diff.md` (apply the REANCHORED body)
- **Scope:** "connectorId persists but is invisible through the API — POST and GET both return null while the row holds the value"
- **PR must say:** two inserted lines (the POST 201 `data` and the GET list view, `|| null`).
- **Tests:** the new file red→green, the security suite, shared, tsc.
- **On merge:** Done.

### B8. KS-888 (security `index.ts`, chain 2 of 4)
- **READY:** `READY_KS-888_ornith35b-q4_PASS-7of7-STUBMERGED_2026-09-15.diff.md` (apply this file; its stub hunk is already dropped)
- **Scope:** "dbSaveApiKey SWALLOWS a failed INSERT — POST /api/keys answers 201 for a key that was never written; blast radius is ALL key persistence, not one column". Acceptance: with the column absent, `POST /api/keys` does not return 201 (a driven test).
- **PR must say:** the catch at `:330-332` re-raises SQLSTATE classes 42/23/22 (structural). 08/57 stay log-only (the decision comes from the ticket's fix shape). **`dbSaveApiKey` is also called at `:1261` and `:1329`, where a structural error now surfaces too.**
- **Tests:** the new file red→green, the security suite, shared, tsc.
- **On merge:** Done.

### B9. KS-974 (security `index.ts` chain 3 of 4 + `requestSchemas.ts` + `security.openapi.ts`, YAML)
- **READY:**
  - `READY_KS-974-A_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (paths lack `Blockchain/Dev/`)
  - `READY_KS-974-B_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`
- **Scope:** "Published bound vs runtime bound on rate-limit scope: /check enforces code UNITS against a published code-POINT maxLength, and scopeField bounds the untrimmed string"
- **Collision:** rename A → `ks974-check-key-bound-code-points.test.ts`, B → `ks974-scope-field-bounds-the-trimmed-value.test.ts`.
- **PR must say:**
  - A bounds `/check`'s `key` by code points, inline. Hoisting `boundedByCodePoints` (export + import from `requestSchemas.ts`) is optional polish.
  - B: `scopeField()` gets `.trim()` before `.min(1)`.
  - **By hand:** the openapi description clause in `security.openapi.ts` (leading/trailing whitespace is stripped from `tenantId`/`userId`). Then regenerate the yaml.
- **Tests:** both files red→green, the security suite (READY: 213 → 216), shared, tsc, `generate-openapi` + `check:openapi`.
- **On merge:** Done.

### B10. KS-976 (security `index.ts`, chain 4 of 4)
- **READY:**
  - `READY_KS-976-A_ornith35b-q4_PASS-7of7-r2_2026-09-15.diff.md` (**product hunk with fuzz**)
  - `READY_KS-976-B_ornith35b-q4_PASS-7of7-r2_2026-09-15.diff.md`
- **Scope:** "Rate-limit refusals name the wrong field: 400 says "Key required" when the key was fine, and 403 says "Caller has no tenant" when the caller has one"
- **Collision:** rename A → `ks976-reset-400-names-the-failing-field.test.ts`, B → `ks976-403-says-which-scope-claim-failed.test.ts`.
- **PR must say:** `/reset`'s 400 names the first failing field. The 403 says "present but unusable" vs "no tenant" at `:1379` and `:1489`. Hoisting the inline predicate into `scopeRefusalMessage(user)` is optional polish. Keep the real-HTTP harness (port 0, `SECURITY_DISABLE_BOOT`, regex-free `b64url`).
- **Tests:** both red→green, the security suite, shared, tsc.
- **On merge:** Done.

### B11. KS-1121 (vc-issuer)
- **READY:** `READY_KS-1121_ornith35b-q4_VITEST-MODIFYINPLACE-REANCHORED-PASS-7of7_2026-09-16.diff.md` (**test hunk 2 by hand**)
- **Scope:** "Security: credentialRepo.getById resolves a credential by SUBSTRING (LIKE '%id%' + includes()) — reached from GET /api/credentials/:id AND under POST /api/credentials/:id/revoke, and the partial match is pinned as intended by its own test (KS-1020's sibling)"
- **PR must say:**
  - **KAM RULED 2026-09-16 07:01** (card `secuura-ornith-decision-class-tickets-1121-629-975`, a): *"delete the substring branch exactly as #966 did for presentations (exact-or-404) and flip the one pinned test"*.
  - Behaviour change: `GET /api/credentials/:id` answers 404 for any non-exact id, and `POST …/revoke` refuses a fragment.
  - Ownership checks are KS-1116, not this PR.
  - Route-level cells were not written.
- **Tests:** the modified `credentialRepo.test.ts` (3 red at the tip → 11/11), `npm test -w services/vc-issuer`, shared, tsc.
- **On merge:** Done, citing the card.

### B12. KS-692 (vc-issuer `routes/status.ts`)
- **READY:** `READY_KS-692_ornith35b-q4_CODEPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md` (two fences)
- **Scope:** "Security: /api/status revoke/unrevoke has no tenant ownership check — an ISSUER_ADMIN in any tenant can revoke another tenant's credential (KS-586's deferred half, now untracked)"
- **PR must say:**
  1. **A deliberate, RULED, INTERIM narrowing** (card `secuura-ks692-status-revoke-interim-posture`, a, "Narrow now, bind-creator later"): `ISSUER_ADMIN` is dropped from `STATUS_WRITE_ROLES`. Tenant-scoped admins LOSE revoke/un-revoke until `credential_status_lists` has an owner column. The ownership model is Kam's `bind-creator` (card `secuura-ks1116-presentation-credential-ownership-model`, 2026-09-13), which is KS-1116 work.
  2. **The sibling suite's test count DROPS 14 → 13, and that is correct.** `ks586-status-write-authorization.test.ts` uses `it.each(STATUS_WRITE_ROLES…)`. There are zero failures either way. Whole vc-issuer went 108 → 113 in the READY run. Say this, or a reviewer will read it as deleted coverage on a security PR.
  3. **The stale-pointer fix at `status.ts:36` (KS-586 → KS-692) is deliberate.** It cost a bad round trip on Peter's #730, and it is now the only thing telling the next reader not to re-add `ISSUER_ADMIN`.
  4. **The controls are platform admin across `SYSTEM_ADMIN`/`SUPER_ADMIN`/`super_admin`, plus anonymous still 401.** A "legitimate caller still succeeds" control was impossible, because the removed caller is the one in question.
  5. KS-643 is Done/archived (its `decideTenantAccess` is what `bind-creator` should reuse). KS-621 is still Backlog and unruled; this does not resolve it.
- **Tests:** the new `ks692-status-write-platform-only.test.ts` (3 red → 6/6), `npm test -w services/vc-issuer`, shared, tsc.
- **On merge:** **leave OPEN by default** (PLAN Q3). Comment that the interim narrowing landed and link KS-1116.

### B13. KS-629 (kyc, YAML)
- **READY:**
  - `READY_KS-629-A_ornith35b-q4_VITEST-PASS-7of7_2026-09-16.diff.md`
  - `READY_KS-629-B_ornith35b-q4_VITEST-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "kyc `livenessVideo` is accepted by spec and runtime, then silently discarded — no code path reads it"
- **PR must say:**
  - **KAM RULED 2026-09-16 07:01** (card `secuura-ornith-decision-class-tickets-1121-629-975`, a): *"REMOVE the field from schema and spec (nothing reads it)"*.
  - `git mv` A's test `ks629-kyc-livenessvideo-is-accepted-by-spec.test.ts` → `ks629a-liveness-video-removed-from-runtime-schema.test.ts`.
  - **A spec-breaking change:** `livenessVideo` is removed from the published selfie-upload schema. The runtime never processed it, and `z.object` still strips it silently.
  - Regenerate the yaml. The `livenessVideo:` block at ~`:4427` must disappear.
- **Tests:** both source-pin files red→green, `npm test -w services/kyc`, shared, tsc, `generate-openapi` + `check:openapi`.
- **On merge:** Done, citing the card.

### B14. KS-1160 (originate `routes/webhooks.ts`)
- **READY:** `READY_KS-1160_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "originate POST /api/webhooks persists the RAW url where PATCH persists the normalised one — validateWebhookUrl(url) is consulted, its .url discarded (webhooks.ts:257 binds ${url}, :262 echoes it; PATCH :300 pushes urlValidation.url)"
- **PR must say:** `:257` and `:262` use `urlValidation.url`. Cite Peter's §6 finding on #720 (comment 5479494525).
- **Tests:** the new file red→green, `npm test -w services/originate`, shared, tsc.
- **On merge:** Done if the DoD is met.

### B15. KS-1028 (originate `services/gdprService.ts`)
- **READY:** `READY_KS-1028_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md` (paths lack the prefix)
- **Scope:** "KS-754 gate F-1 (MAJOR): a step-12 throw skips the USER_ERASED fan-out AFTER the crypto-shred — local data destroyed, four subscribers keep theirs"
- **PR must say:** **Wednesday chose option (b) over (a).** Step 12 is captured, the fan-out runs, and the error is re-raised into the outer catch. (a) would have marked a DSR completed before the shred ran. Say this on the ticket too. KS-1031 (F-4, same path) is untouched. Cite the gate report path in the ticket.
- **Tests:** the new file red→green, originate, shared, tsc.
- **On merge:** Done.

### B16. KS-1074 (originate `services/anchorStateSync.ts`, chain 1 of 2)
- **READY:**
  - `READY_KS-1074-A_ornith35b-q4_JEST-RETRY-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1074-B_ornith35b-q4_JEST-RETRY-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1074-C_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal path, not just the failure path #936 fixes"
- **Collision:** all three are named `ks1074-the-poller-reconcile-blob-writers-also.test.ts`. Rename:
  - A → `ks1074-poller-confirm-writer-preserves-thread-token.test.ts`
  - B → `ks1074-reconcile-writers-preserve-thread-token.test.ts`
  - C → `ks1074-poller-simulated-writer-preserves-thread-token.test.ts`
  - Normalise `\u{1F534}` / `—` escapes in the titles.
- **PR must say:**
  - **Wednesday's decisions:** carry `threadToken` on EVERY writer (a mint is independent of the anchor outcome, per KS-1058's reasoning). Do a per-write `getDocument` read, not one read before the loop, because a single early read races the create-time mint.
  - The 🔴 cells are the ticket's requested runtime repro, at unit level.
  - Also answer the ticket's comment MINOR-2 (the truthy guard in `markDocumentAnchorFailed`), or say it is not addressed.
- **Tests:** three files red→green, originate (READY: 637 → 641), shared, tsc.
- **On merge:** Done if MINOR-2 is addressed or recorded elsewhere; otherwise comment and leave open.

### B17. KS-1158 R1 (originate `anchorStateSync.ts`, chain 2 of 2)
- **READY:** `READY_KS-1158-R1_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "L3a gate records (#912 r2 / #937): the placeholder-hash anchoredAt carry keys on string truthiness not authoritativeTxHash(), the network carry has one pin, stale line references in the ks1059 / ks1058 test headers"
- **PR must say:** R1 only. `:170` keys the carry on `authoritativeTxHash()`; keep or drop the `<KS-1158>` comment tag. R3 (the network pin) and R5 (the header re-points) remain.
- **Tests:** the new file red→green, originate, shared, tsc.
- **On merge:** **leave OPEN** (DoD needs R1+R3+R5).

### B18. KS-794 (originate `originate.openapi.ts`, chain 1 of 2, YAML)
- **READY:** `READY_KS-794_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "verify-file returns `fileSize` on every 200 and neither response schema declares it"
- **PR must say:**
  - `fileSize` becomes an optional int on `VerifyResponse` and `V2VerifyResponse`. **This is the ticket author's option 1, taken on their stated preference.**
  - **By hand:** amend the two 200-response NOTE descriptions at `:2067-2070` / `:2116-2119` to "declared optional in the schema (KS-794)". Regenerate the yaml.
  - Read the ticket's 2026-09-04 comment (a second undeclared field, `fileHash`). If the ticket owns it, say it is not closed here.
- **Tests:** the new file red→green, originate (READY: 637 → 642), shared, tsc, `generate-openapi` + `check:openapi`.
- **On merge:** Done unless the `fileHash` gap is recorded as this ticket's scope. In that case, comment and leave open.

### B19. KS-1133 (originate `originate.openapi.ts`, chain 2 of 2, YAML)
- **READY:**
  - `READY_KS-1133-A_ornith35b-q4_JEST-PASS-7of7-RETRY_2026-09-15.diff.md`
  - `READY_KS-1133-B_ornith35b-q4_TESTONLY-JEST-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "verify-hash precedence: v1 hash-LAST, v2 hash-FIRST — document the split on both routes' descriptions (Kam 2026-09-13)"
- **PR must say:**
  - Kam's 2026-09-13 `accept-split` ruling.
  - A: both verify routes' descriptions lead with their precedence sentence.
  - B: the v2 route cell (tamper at `verificationV2.ts:446`).
  - **Cite `ks1103-verify-hash-field.test.ts` P1 as v1's cell; do not duplicate it.**
  - Checklist item 4 (`VerifyRequest` prose at `:551` lists an incomplete alias set) is your call; the ticket says fix it only if the sentence is touched.
  - Regenerate the yaml.
- **Tests:** A red→green, B red under tamper and green at the tip, originate, shared, tsc, `generate-openapi` + `check:openapi`.
- **On merge:** Done.

### B20. KS-1172 + KS-1173: ONE PR (originate + anchoring + VOCABULARY.md, YAML)
- **READY:**
  - `READY_KS-1172-A3_ornith35b-q4_JEST-MODIFYINPLACE-THREE-VERBS-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1172-B3_ornith35b-q4_MODIFYINPLACE-THREE-VERBS-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1172-D3_ornith35b-q4_DOCPATCH-THREE-VERBS-PASS-6of6_2026-09-15.diff.md`
  - (**Ignore the `_superseded_*` two-verb files.** De-indent A3 :16 and B3 :15.)
- **Scope:**
  - KS-1172: "Add `note` and `verified` to the lifecycle vocabulary (LIFECYCLE_VERBS + LIFECYCLE_EVENT_ACTIONS) — S needs both for the Note feature and the Flow project"
  - KS-1173: "Flow verbs: add `note`, `certified` and `verified` to the lifecycle vocabulary (platform-s Flow project)"
- **PR must say:**
  - Three verbs: `note`, `certified`, `verified`.
  - Originate `lifecycleActions.ts` + `lifecycleEventRepo.test.ts` (modified in place). Anchoring `anchorSchema.ts` + `anchorSchema.test.ts`. `docs/VOCABULARY.md` §2/§3.
  - The TRANSITIONAL `certify` is untouched; `certified` is a different verb.
  - **Amend the two pin cells' TITLES. Regenerate the yaml** (S's PS-614 gate reads it).
  - **Merged is not deployed.** The gateway image is rebuilt on deploy, and deploy is not in this grant.
  - Do NOT migrate stored rows (see `ks661-vocab` below).
- **Tests:**
  - originate `npx jest src/__tests__/lifecycleEventRepo.test.ts` (1 red → green)
  - anchoring `npx vitest run src/__tests__/anchorSchema.test.ts` (1 red → green)
  - both suites, shared, tsc for both, `generate-openapi` + `check:openapi`
- **On merge:**
  - **KS-1172 → Done.**
  - **KS-1173 stays OPEN by default** (PLAN Q4). Its body asks K two questions, which are not in this PR: (1) a named field for credential references on a lifecycle event, and (2) whether `verified` may anchor against the certifier's K document id with the verifying org as issuer org (PS-845 is blocked on it).
  - Comment facts only: merged at `<sha>`, **not deployed**, the two questions open. Kam's 09-15 comments promised a deploy ping on DEPLOY; do not ping on merge. No @-mentions.

## RULED BY KAM, NOT YET IN AN ARTEFACT
Source: `bash 2_Project_Files/tools/decision_queue.sh list ruled --undelivered`, filtered to Secuura and to this seat's bundles. Rulings verbatim from `decision_queue.sh show <id>`.
- **`secuura-org-trust-boundary-within-tenant` → `bind`** (ruled 2026-09-07T19:01:15). Bears on KS-1173 question 2 (cross-org anchoring for `verified`), which is why KS-1173 stays open:
  - *"[bind] Bind the issuer to the actor - 403 on a mismatch, exactly as onBehalfOf already does (Recommended)"*
  - detail: *"Makes the file self-consistent with the check fifteen lines above it, and makes the public display mean what a reader assumes. A genuine delegation need goes through the onBehalfOf mechanism that already exists for it, not an unchecked field."*
- **`ks661-vocab` → `residue`** (ruled 2026-08-24T06:58:16). Bears on B20: do not rewrite stored lifecycle rows.
  - *"[residue] Leave as test residue"*
  - detail: *"Zero writes; reversible by construction; Stuart mirrors the same call (agent's recommendation)"*
- **`secuura-required-approvals-zero-after-the-untick` → `raise-to-1`** (ruled 2026-09-10T10:38:57):
  - *"[raise-to-1] Raise required approving reviews from 0 to 1 on the require-pr-gates ruleset"*
  - **Not yet applied** (measured `required_approving_review_count: 0` on 2026-09-16 ~20:5x). If it flips, merges refuse: STOP and mail.
- **`secuura-agent-github-identity` → `identity`** (ruled 2026-08-26T17:12:33):
  - *"[identity] Create an agent GitHub identity in the Secuura org (rec) + Stuart approves today's two"*
  - Not executed. Self-approval returns 422. Do not try.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Every PR waits for Wednesday's GO after its QA gate. One merge at a time, head pinned.
- Client-facing communication is ticket comments only. No @-mentions to Peter or Stuart.
- Never delete; quarantine.
- Kintsugi first, demo behind gates. **No deploy in this brief.**
- `.github/workflows` untouched.
- KS-1028: option (b).
- KS-1074: carry `threadToken` on every writer, with a per-write read.
- KS-888: re-raise classes 42/23/22 only.
- KS-1172 + KS-1173: ONE PR (three verbs).

## HOLDS
- **Signature classes pause for Kam, always:** production · money · external communication to any human · anything irreversible.
- **Client-facing communication is TICKET COMMENTS only.** The extranet is input only. Nobody but Kam messages Peter or Stuart.
- **Handovers to Peter/Stuart are TEST BLOCKS, never a list of PRs.** Wednesday composes them; you do not hand over.
- **No `--no-verify`, no force pushes, no `--admin`.**
- **Never deploy.** No kintsugi or demo, no `deploy.sh`, no gateway image push. Project hold: **no deploy without migration 048 applied first** (KS-1031).
- **Other authors' PRs, and open PRs not in this queue (#922, #995, #887, #920 …), are not yours.**
- **Parallel seats share one inbox** (`coagent@agentmail.to`, prefix `Secuura/Blockchain`). **A mail naming a PR or ticket not in YOUR queue is not yours.**
- **Your own `git worktree` only.** Never the shared checkout.
- Before filing any ticket, search the board by SYMBOL, path or error string, and say what you searched. One ticket per test pass (Kam, 2026-09-07 13:23). New and unassigned tickets go to the board account.
- A control must be able to fail. `cmd > out 2>&1; rc=$?`. macOS has no `timeout`. zsh has no `PIPESTATUS`.
- **If a line in this brief looks wrong at source, say so** (QUESTION mail). Approval-class items wait for the ANSWER.
- **Session end:** send the wrap mail `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-1x` (first line `Seat B`) listing every PR: number, head, state, and ticket state.

SELF-CHECK: claim-bearing lines re-read via self_check_view.sh (repeated ticket ids, numbers, close/open dispositions) - no contradiction found; the whole brief was NOT re-read end-to-end by Wednesday (the drafter mechanically checked 111 paths / 0 overlaps and replayed each queue at the base) | 2026-09-16 21:06
