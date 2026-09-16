# [Wednesday -> Secuura/Blockchain] SEAT A: raise Ornith's held diffs for api-gateway, demo-service, packages/shared and auth as PRs, one ticket per PR
# STAGED 2026-09-16 21:06. Plan and measurements: `WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-16_raise_PLAN.md`.
# Kam approved this work (panel 2026-09-16 20:40:59, confirmed 20:41:47 "yes. claude agents"): *"you have the approval to spin up other local agents to test, approve, merge and move things forward"*. Approval of each PR = Wednesday's GO naming the head SHA, after a QA gate verdict at that head plus your Test Evidence block (Kam's 2026-09-11 TESTED grant; CONTRIBUTING.md "Adopted merge flow" step 6).

## BLUF
- **What:** you raise **16 PRs**, one per ticket (bundles below). Each applies local-model (Ornith) diffs that passed their checker 7/7 at develop M55 `48e65c435` and were source-read by Wednesday.
- **Your partition: you write ONLY in**
  - `Blockchain/Dev/services/api-gateway/**`
  - `Blockchain/Dev/services/demo-service/**`
  - `Blockchain/Dev/packages/shared/**`
  - `Blockchain/Dev/services/auth/**`
- **NOT yours. These partitions are RESERVED for seats B and C (not launched tonight on Kam's 21:1x "dont go overboard" — they may be launched later), so never edit them, even for a one-line fix you notice:**
  - Seat B: `Blockchain/Dev/services/{security,originate,anchoring,vc-issuer,kyc}/**`, `Blockchain/Dev/docs/openapi/secuura-api.yaml`, `Blockchain/Dev/docs/VOCABULARY.md`
  - Seat C: `Blockchain/Dev/scripts/**`, `.githooks/**`, `Start_Up/**`, `systemTest/**`, `Blockchain/Dev/deployment/**`, `Blockchain/Dev/CONTRIBUTING.md`, `Blockchain/Dev/docs/DEV-PROCESS.md`, repo-root `CLAUDE.md`
  - If your work seems to need a file outside your partition, STOP and mail a QUESTION.
- **WHOSE / WHERE:**
  - Remote: `origin` = `git@github.com:Secuura/Distributed_Secuura.git`, identity `kksecura`.
  - Base: `origin/develop`, which was `0b25f823f` at drafting. Re-read it before every branch.
  - Branches: `feature/ks-<n>-ornith-<slug>`.
  - Tickets: team KS, on the board account.
  - Local work happens ONLY in your own worktree: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-a`. Never switch branches, pull, or edit in the shared checkout `2_Project_Files`.
- **Your files did NOT move between M55 and the tip.** Measured with the GitHub compare API: all 36 changed files are under `systemTest/schemathesis/`. The diffs apply at the tip as held, except for the named accommodations below. `0b25f823f` is not in the local object store, so fetch first.

PROVENANCE:
- Kam's approval for Claude seats to test, approve, merge | Kam panel chat 2026-09-16 20:40:59 + 20:41:47 (kam_msgs.sh, view=wednesday) | read 2026-09-16
- origin/develop = 0b25f823f; 36 files changed since 48e65c435, none touched by any READY file | GitHub REST branches + compare 48e65c435...0b25f823f (2026-09-16_raise_PLAN.md lines 17-19) | read 2026-09-16
- the held diffs and their PR NOTES | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_*.diff.md + night/done.md | read 2026-09-16
- partition: no file in two seats (111 paths, 0 overlaps) | 2026-09-16_raise_PLAN.md partition table (mechanical check) | read 2026-09-16
- merge rule: TESTED = QA gate verdict at head + Test Evidence + Wednesday's GO naming the head SHA; feature PRs squash | Blockchain/Dev/CONTRIBUTING.md:107 + "Adopted merge flow" step 6 at develop | read 2026-09-16
- Kam rulings carried verbatim in this brief | decision_queue.sh list ruled --undelivered | read 2026-09-16

## ITEM 0: before any PR
1. **Plan confirmation.** Mail `wednesday-agent@agentmail.to`, subject `[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (seat A)`. Body: this queue as you re-derived it at the tip, any bundle that no longer applies (named, not forced), and **every warning your launcher printed at boot, verbatim**. Start when you get the ANSWER. If there is no ANSWER after 15 minutes, wait: this is approval-class.
2. Set up the worktree:
   ```
   git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" fetch origin > f.out 2>&1; rc=$?
   git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" worktree add --detach "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-a" origin/develop
   ```
   Then run `npm ci` in `<wt>/Blockchain/Dev` once. A fresh worktree has no deps, and preflight reports that honestly (CLAUDE.md KS-691).
3. **Baseline:** at `origin/develop`, run each service suite you will touch and record the pre-existing reds, so each PR's "no new red" is measured against it. The KS-960 READY recorded **auth at M55 = 734 tests, 3 pre-existing failures**.

## HOW TO APPLY A READY FILE (all bundles)
READY files are in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`. Read them; never edit them. Each has header lines (`#`: what it is, Wednesday's source read, PR NOTES), then one or more fenced blocks marked diff.
1. Copy the fence body or bodies into a scratch patch.
2. **Split it into one patch per file** at each `--- ` / `+++ ` pair. Several READYs miscount hunk headers, so a multi-file patch can swallow the next file's `--- /dev/null` as a removed line.
3. **De-indent any file header that starts with a space.** Measured in your set: `READY_KS-1073` line 11 (` --- /dev/null`) and `READY_KS-871-PartB` lines 10–11.
4. **Strip fake `diff --git …` / `index 1234567..abcdefg` lines.** `READY_KS-871-PartA` has them. They make git create an empty test file first and defeat `--3way`.
5. **Paths:** several READYs use service-relative paths (`services/…`, `packages/…`). Apply those with `--directory=Blockchain/Dev`, or prefix them.
6. Apply each section: `git -C <wt> apply --3way --recount --ignore-whitespace <section>` (redirect output to a file, then read `rc`). If that fails, try `patch -p1 --fuzz=2 -d <wt> < <section>`. If that also fails, **apply the READY's `-`/`+` lines by hand at the line it names** and write "applied by hand from the -/+ lines" in the PR body.
7. After applying, `git -C <wt> diff` must show every `+`/`-` line of the READY and nothing else, apart from the PR-NOTES edits you make deliberately.
8. **Red-proof before green.** For a product fix: apply the TEST section(s) first, run the new test and record the red count. Then apply the product section and record green. For a TEST-ONLY bundle: apply the tamper the READY names, run to get red, restore the product file with `git -C <wt> checkout -- <file>`, run to get green, and confirm `git diff` shows no product change.
9. **Accommodations measured by Wednesday's apply check** (scratch copy at M55, your queue in order):
   - 37 of 40 sections apply clean.
   - `READY_KS-1101-C` product hunk: the context line `if (response.ok) {` is missing. Insert the `+` block by hand inside `if (response.ok) {` in `routes/health-dashboard.ts` (~:62).
   - `READY_KS-871-PartB` product hunk: its context does not match `middleware/audit.ts:105-111`. Apply the one `-`/`+` pair at `:108` by hand.
   - `READY_KS-1050` import hunk (`routes/users.ts` :13–19): it applies alone, but conflicts after KS-1018's import edit to the same block. Merge by hand and keep both imports.
   - The rest apply clean in queue order.

## THE FLOW, per PR (no step skipped)
1. `git -C <wt> fetch origin`, then `git -C <wt> switch -c feature/ks-<n>-ornith-<slug> origin/develop`. **Same-file bundles are strictly serial:** cut the next branch only AFTER the previous PR on that file has merged. Open PRs awaiting GO: **at most 3** at once (PLAN Q2).
2. Apply (above), do the PR-NOTES edits, then run the tests named in the bundle. Every command is `cmd > out 2>&1; rc=$?`, then read the file. **No pipes on a status. zsh has no `PIPESTATUS`.**
3. Commit and push the branch. The pre-push preflight runs. **Never `--no-verify`. Never force-push.** If the hook refuses with `::error::… is missing — … deleted` lines from `check-stack-safety.sh`, that is the KS-1034 class under a worktree hook: STOP and mail a QUESTION (PLAN Q7).
4. Open the PR against `develop`. The body must carry:
   - the ticket
   - the READY filename(s)
   - the checker run dir from the READY header
   - the sentence *"authored by the local model (Ornith) from a Wednesday-written brief; source-read by Wednesday; re-run by seat A at `<sha>`"*
   - the bundle's PR-must-say lines
   - the **Test Evidence block** in DEV-PROCESS form: Touched / Ran / NOT run / Migrations+config; the platform-suite lines, where Schemathesis records the **failing SET vs the develop baseline set, never a bare count**; the Unit suites line; the Cross-cutting guards line
5. Comment on the ticket naming the PR (facts only, no @-mentions).
6. Mail `wednesday-agent@agentmail.to`, subject **`[Secuura/Blockchain -> Wednesday] READY FOR QA: #<n> <ticket> @<head sha>`**. Read the head SHA from origin in the same action (`gh pr view <n> --json headRefOid`). Body:
   - first line `Seat A`
   - PR URL, ticket plus the ticket comment naming the PR
   - Test Evidence summary
   - **what was NOT done or NOT covered**
   - accommodations used
7. **STOP that PR** until Wednesday's GO. Meanwhile you may start the next file-disjoint bundle, within the 3-open limit.
8. GO arrives in `secuura-blockchain@agentmail.to` (the project inbox per `fleet/inbox_routing.conf`) as `[Wednesday -> Secuura/Blockchain] GO: #<n> <ticket> @<sha>`. **Merge only if `<sha>` equals the PR's head read from origin now.** If it differs, do not merge; mail a QUESTION. To merge, as author: `gh pr merge <n> --squash --match-head-commit <sha>` (CONTRIBUTING.md:107: feature PRs into develop are squash). **No `--admin`.** If GitHub refuses because a review is required (Kam may apply his `raise-to-1` ruling), STOP and mail. Do not approve your own PR; GitHub returns 422.
9. After the merge: `git -C <wt> fetch origin`, confirm the PR is `MERGED` and note the merge commit (`gh pr view <n> --json state,mergeCommit`), set the ticket state (below), then move on.
10. **If the QA gate returns findings:** fix on the same branch, updating from develop with a merge and never a rebase plus force-push. Re-run the tests and send a new READY FOR QA mail with the new head SHA. An old GO never covers a new head.

**Never merge without a GO naming the head SHA. Never deploy. Never `--no-verify`. Never force-push.**

## Ticket state on merge
Close a ticket (Done) **only if the PR delivers the ticket's WHOLE scope sentence** (read it again at close time). Otherwise comment what landed, with the PR and merge commit, and leave it open. The per-bundle default is below; the ticket wins over the default.

## QUEUE (cheapest first: test-only, then product; same-file chains in order)
Scope sentences are the Linear titles, read 2026-09-16 ~21:1x with `issue(id){title state comments(first:50)}`, sorted client-side. All 16 tickets are open (Backlog).

### A1. KS-1130: TEST-ONLY
- **READY:**
  - `READY_KS-1130-E1twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1130-E7twin_ornith35b-q8_TESTONLY-PASS-7of7-DECLSPLICED_2026-09-15.diff.md` (the DECL-SPLICED body is the runnable one)
  - `READY_KS-1130-E3twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "ks1069: tier-2 twin cells for E1/E7/E3 + the falsified comments (:323, :244, :618-621, header :35-38) + the shadowed typeof at :623"
- **PR must say:** no product change; three tier-2 twin files, each tamper-graded. Tampers are named in each READY header: E1 :617 placeholder-prefix guard removed; E7 the one-line ternary; E3 :627 `Boolean(persistedSimulated)` → `=== true`. The ticket's items 2–4 (the comment rewords at `routes/verification.ts` :323/:244/:618-621, the ks1069 test header :35-38, the :623 shadowed `typeof`) are NOT in the diffs. Do them in this PR if the ticket's words are met; otherwise say so.
- **Tests:**
  - each new file: `npx vitest run src/__tests__/ks1130-tier2-<e1|e3|e7>-twin.test.ts` in `Blockchain/Dev/services/api-gateway`, red under its tamper, green at the tip
  - the whole suite: `npm test -w services/api-gateway -- --run`
  - `npm test -w packages/shared`
  - `npx tsc --noEmit -p services/api-gateway`
- **On merge:** Done if items 2–4 landed too; otherwise comment and leave open.
- ⚠ If you do the comment rewords in A1 or the P1–P2 edits in A2, those PRs also touch `routes/verification.ts`. A1 → A2 → A7 → A8 → A9 then become ONE serial chain.

### A2. KS-1123: TEST-ONLY
- **READY:**
  - `READY_KS-1123-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1123-F3_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "api-gateway verify: an empty-string / 0 / false anchor status is one edit (`??`→`||` at :597) from an unearned ON-CHAIN claim on both tiers and no cell would notice — plus the unpinned "always has a status" / "statusless only" claims and three stale pointers (QA-967/968 F3 + F1 + F2 + P1–P3)"
- **Collision:** BOTH files are auto-named `ks1123-api-gateway-verify-an-empty-string.test.ts`. Apply F2, rename it (e.g. `ks1123-f2-anchor-failed-stale-confidence.test.ts`), then apply F3 and rename that (e.g. `ks1123-f3-empty-status-is-off-chain.test.ts`).
- **PR must say:**
  - F3 tamper is `:597 ??→||`; F2 tamper is `:709` (the guard dropped).
  - **F1 is KS-1073's cell** (bundle A7). Land it once and cite it.
  - P1–P3: cite `:312` or drop the number at `:644`; move the G6 JSDoc above `makeFetchDocFromAnchorStore` (`:263`). Do them here if cheap.
- **Tests:** as A1, with these files.
- **On merge:** leave open with a comment. Close KS-1123 when A7 (KS-1073) merges, provided P1–P2 have landed.

### A3. KS-960: TEST-ONLY, tamper-graded
- **READY:** `READY_KS-960_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "Two schema sources disagree on whether users.email is unique — a statement valid against one is 42P10 against the other, so a suite can be green on a shape that never runs"
- **PR must say:** ONE new file, no product change. It pins that `createUser` conflicts on `email_lookup_hash`. Tamper: `services/auth/src/repositories/userRepo.ts:688` → `ON CONFLICT (email) DO UPDATE SET`. **This closes the owed PIN only. The ticket's "⛔ DO NOT RECONCILE THESE TWO FILES YET" stands.**
- **Tests:**
  - the new file: `npx vitest run src/__tests__/ks960-two-schema-sources-disagree-on-whether.test.ts` in `services/auth`, 3 red under the tamper, 6/6 at the tip
  - `npm test -w services/auth -- --run` (compare against the baseline's 3 pre-existing reds)
  - `npm test -w packages/shared`
  - `npx tsc --noEmit -p services/auth`
- **On merge:** **leave OPEN**, with a comment that the pin landed.

### A4. KS-1165
- **READY:** `READY_KS-1165_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`
- **Scope:** "api-gateway CSRF excludedPaths carries no /api/v2/verification entry — the v2 verify paths are not excluded as v1's are"
- **PR must say:** adds `'/api/v2/verification/verify'` to `middleware/csrf.ts` excludedPaths, beside v1's (the v2 twins are published anonymous). Cite KS-801's case-sensitivity class; do not re-file it. The ticket's DoD asks for "one gateway cell pins the chosen behaviour through the real mount order". Say how the new cells reach the mount order, or add that cell.
- **Tests:** the new `ks1165-…` file red→green, the api-gateway suite (`contentType.test.ts` must stay green), shared, tsc.
- **On merge:** Done if the three DoD boxes are met.

### A5. KS-932: packages/shared
- **READY:** `READY_KS-932_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`
- **Scope:** "timeoutMs does not bound DNS resolution — a hung lookup leaves safeOutboundRequest pending well past its declared deadline"
- **PR must say:** one product file, `packages/shared/src/security/ssrf-guard.ts`, plus `ks932-timeout-bounds-dns.test.ts`. `shared` is consumed by every service, so name that in Touched.
- **Tests:**
  - `npx vitest run src/__tests__/ks932-timeout-bounds-dns.test.ts` in `packages/shared`, red→green
  - `npm test -w packages/shared`
  - `npm run build --workspace=packages/shared`, then the api-gateway suite as the consumer smoke
  - tsc
- **On merge:** Done.

### A6. KS-844: demo-service
- **READY:** `READY_KS-844_ornith35b-q4_PASS-7of7-REANCHORED_2026-09-15.diff.md` (the REANCHORED body is the one to apply)
- **Scope:** "demo-service mounts no error handler — a raw 0x00 body returns express's default HTML with a stack trace and absolute paths"
- **PR must say:** imports `NextFunction` and adds a four-arg JSON error handler after the 404 handler.
- **Tests:** the new `ks844-…` file red→green, `npm test -w services/demo-service`, shared, `npx tsc --noEmit -p services/demo-service`.
- **On merge:** Done.

### A7. KS-1073 (`routes/verification.ts`, chain 1 of 3)
- **READY:** `READY_KS-1073_ornith35b-q8_PASS-7of7_2026-09-15.diff.md`. **De-indent the ` --- /dev/null` at fence line 11.**
- **Scope:** "Tier-2 verify has no statusless-blob cell — the carve-out is unguarded on the tier a third party reaches"
- **PR must say:** a one-line change to the `persistedAnchored` carve-out at ~:685, so a statusless row counts only when it is NOT `_source === 'anchor_store'`. This changes the verify predicate. The new file's statusless tier-2 cell is **KS-1123's F1**; say so on KS-1123.
- **Tests:** the new `ks1073-tier-2-verify-has-no-statusless.test.ts` red→green, the api-gateway suite, shared, tsc. Schemathesis `pr` per PLAN Q1 (it changes a verify response).
- **On merge:** Done. Then close KS-1123 if its P1–P2 landed in A2.

### A8. KS-1087 (`routes/verification.ts`, chain 2 of 3)
- **READY:** `READY_KS-1087_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`. It has no header lines; the run dir is `local-model/runs/2026-09-15_ks1087-ornith35b-night6`.
- **Scope:** "workflow-approve deletes the pending document and answers 200 "Document has been created" without reading originate's response — a refused forward (401, measured) loses the document"
- **PR must say:** the ticket's recommendation **item 1 only**: report approval and delete the pending doc only after originate returns 2xx. **Item 2** (forward a credential originate accepts) is a design call, untouched. Say so.
- **Tests:** the new `ks1087-…` file red→green (the 401 stub must not yield 200, and the pending doc survives), the api-gateway suite, shared, tsc.
- **On merge:** **leave OPEN** (item 2), with a comment.

### A9. KS-1072 (`routes/verification.ts`, chain 3 of 3)
- **READY:** `READY_KS-1072_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`. No header; run dir `local-model/runs/2026-09-15_ks1072-ornith35b-night5`.
- **Scope:** "The latest-anchor selector documents a `confirmedAt` tiebreak it does not implement — and since KS-1057 that selector decides the verdict"
- **Tests:** the new `ks1072-…` file red→green, the api-gateway suite, shared, tsc.
- **On merge:** Done.

### A10. KS-864 (`routes/system-status.ts`, chain 1 of 2)
- **READY:**
  - `READY_KS-864-PartA-helper_ornith35b-q8_PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-864-PartB-portals_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`
- **Scope:** "Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — system-status.ts hard-codes secuura-staging-* hosts, westeurope and a dead URL suffix". Acceptance (ticket): *"`system-status.ts` reports hosts and region from configuration or from the live deployment identity, not from literals naming a subscription decommissioned 2026-06-25."*
- **Collision:** both test files are named `ks864-dead-estate-pointers-in-runtime-source.test.ts`. Rename A → `ks864a-…`, B → `ks864b-…`.
- **PR must say:** Part A is the helper (a parameter rename plus the dead staging branch removed; keep or drop the model's one comment line). Part B is the three portal ternaries → env-or-compose-default. After both, `grep -c 'ashypond\|westeurope\|secuura-staging-' system-status.ts` should equal only the 17 untouched call-site arguments; measure it and state the number. **The ticket's 2026-09-12 comment adds item 2 (portals probed on `:80` while nginx serves `:8080`) and item 3 (the headline ignores red panels). Part B's default stays `:80`, so neither is closed here.** Say so.
- **Tests:** both new files red→green, the api-gateway suite, shared, tsc.
- **On merge:** **leave OPEN** (items 2–3 and the 17 call sites), with a comment.

### A11. KS-1101 (`routes/system-status.ts`, chain 2 of 2)
- **READY:**
  - `READY_KS-1101-A_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (`services/health.ts`)
  - `READY_KS-1101-B_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (`routes/system-status.ts`)
  - `READY_KS-1101-C_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (`routes/health-dashboard.ts`; **product hunk by hand**, see HOW TO APPLY)
- **Scope:** "Gateway health aggregates read anchoring's HTTP status only, so its degraded body (#728) never reaches /health/deep, /system/status or the health dashboard"
- **PR must say:** three aggregates now read the probed body and map `status: 'degraded'` to down/unhealthy, with the reasons included. The ticket's regression cell is Part A's 🔴. Note on KS-671 that the code comment pointing at KS-671 can now point here.
- **Tests:** the three new files red→green, the api-gateway suite, shared, tsc. Schemathesis `pr` per Q1.
- **On merge:** Done.

### A12. KS-871 (`middleware/audit.ts`)
- **READY:**
  - `READY_KS-871-PartA-details-path_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (strip the fake `diff --git`/`index` lines)
  - `READY_KS-871-PartB-deriveAction_ornith35b-q8_PASS-7of7_2026-09-15.diff.md` (de-indent the headers; **product line `:108` by hand**)
- **Scope:** "The audit log records `req.path` AFTER the response, so a REFUSED erasure is logged with the path trimmed to `/` instead of /api/gdpr/erasures". Acceptance: *"A refused erasure is audited with `/api/gdpr/erasures` … driven; admitted requests unchanged; the fix is at the capture point so other `router.use` gates in the file benefit."*
- **PR must say:** `auditPath` is captured at entry; `details.path` (`:280`) and `deriveAction` (`:108`) read the original URL. Line 274 (`req.path === '/api/auth/login'`) is a third inside-finish read the ticket did not name. It is out of scope, and the PR must say so.
- **Tests:** both new files red→green (they drive the KS-843 door in-process), the api-gateway suite, shared, tsc.
- **On merge:** Done.

### A13. KS-745
- **READY:** `READY_KS-745_ornith35b-q4_PASS-7of7_2026-09-15.diff.md`
- **Scope:** "api-gateway audit export calls /api/audit/logs — a route the security service does not have, so the export 404s every time"
- **PR must say:** `routes/audit-export.ts` :138 → `/api/audit` and :144 reads `data.data.logs`. **End-to-end reachability stays UNMEASURED** (the ticket's own words); the unit test is the proof.
- **Tests:** the new `ks745-…` file red→green, the api-gateway suite, shared, tsc.
- **On merge:** Done.

### A14. KS-999 (auth, `repositories/userRepo.ts`)
- **READY:** `READY_KS-999_ornith35b-q4_RECHECK-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "getUserById's decrypt path escapes the KS-253 classifier — `return await fromRow(...)`, and the characterisation cell that cannot reach its own conclusion"
- **PR must say:**
  - Item 1 is the one-word `await` at `:406`, a 500→503 change on the normal production path. **AUTH SERVICE, not auth logic** (Wednesday's reading of Kam's 2026-09-15 16:40).
  - Rename the auto-named test to `ks999-getuserbyid-awaits-fromrow.test.ts`.
  - Do item 3 (rename the ks949 "UNAWAITED fromRow" characterisation cell) and item 4 (the logger mock) in this PR.
  - Item 2 (the four calling route families) is the QA gate's job.
  - The four sibling `return fromRow(` sites (`:442/:508/:581/:623`) are OUT of scope. File ONE follow-up ticket for them after searching the board by symbol `return fromRow(` and path `userRepo.ts`, and say what you searched.
- **Tests:** the new file red→green, `npm test -w services/auth -- --run` against the baseline, shared, tsc.
- **On merge:** Done if items 1, 3 and 4 landed; otherwise comment and leave open.

### A15. KS-1018 (auth, `routes/users.ts`, chain 1 of 2)
- **READY:** `READY_KS-1018_ornith35b-q8_PASS-7of7-REANCHORED-TDZINLINED_2026-09-15.diff.md` (apply the body as held; it is already reanchored and TDZ-inlined)
- **Scope:** "Security/correctness: three verification-store reads swallow EVERY DB error with a bare `catch { }` and answer from an in-memory map — a DB outage reads as 'no such request'"
- **PR must say:** `ServiceUnavailableError` and `isInfrastructureDbError` are imported; the three catches log and rethrow infrastructure errors, and otherwise fall through as before.
- **Tests:** the new file red→green, the auth suite against the baseline, shared, tsc.
- **On merge:** Done.

### A16. KS-1050 (auth, `routes/users.ts`, chain 2 of 2)
- **READY:** `READY_KS-1050_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (**import hunk merged by hand after A15**)
- **Scope:** "users.ts:933 answers success: true over a 0-row profile update — KS-943 changes the symptom from stale values to undefined ones"
- **PR must say:** the null guard → 500 `PROFILE_UPDATE_NOT_PERSISTED`. The decision is Wednesday's reading of the ticket's first-named option, following **the wallet precedent**. Say so.
- **Tests:** the new `ks1050-…` file red→green, the auth suite against the baseline, shared, tsc.
- **On merge:** Done.

## RULED BY KAM, NOT YET IN AN ARTEFACT
Source: `bash 2_Project_Files/tools/decision_queue.sh list ruled --undelivered`, filtered to Secuura and to what bears on this seat. Rulings verbatim from `decision_queue.sh show <id>`.
- **`secuura-required-approvals-zero-after-the-untick` → `raise-to-1`** (ruled 2026-09-10T10:38:57):
  - *"[raise-to-1] Raise required approving reviews from 0 to 1 on the require-pr-gates ruleset"*
  - **Not yet applied.** Measured 2026-09-16 ~20:5x: `GET /rules/branches/develop` → `required_approving_review_count: 0`.
  - Effect on you: if it flips mid-run, `gh pr merge` will be refused. STOP and mail.
- **`secuura-agent-github-identity` → `identity`** (ruled 2026-08-26T17:12:33):
  - *"[identity] Create an agent GitHub identity in the Secuura org (rec) + Stuart approves today's two"*
  - Not executed. `kksecura` approving `kksecura` returns 422. Do not try.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Every PR waits for Wednesday's GO after its QA gate. One merge at a time, head pinned.
- Client-facing communication is ticket comments only. No @-mentions to Peter or Stuart.
- Never delete; cleanup means quarantine.
- Kintsugi first, demo behind gates. **No deploy in this brief.**
- `.github/workflows` untouched.
- KS-1050: the wallet precedent (`PROFILE_UPDATE_NOT_PERSISTED`, 500).
- KS-999: "auth service, not auth logic". Item 2 is the gate's.
- KS-1087: item 1 only.

## HOLDS
- **Usage (Kam, panel 2026-09-16 21:1x): "dont go overboard. try not to go beyond 40% token allocation."** Every QA gate is a launch through `fleet/usage_gate.sh` (cut 40, `fleet/USAGE_STOP`). If Wednesday mails STOP for usage: finish the PR in hand, push, mail its state, wrap.
- **Signature classes pause for Kam, always:** production · money · external communication to any human · anything irreversible.
- **Client-facing communication is TICKET COMMENTS only.** The extranet is input only. Nobody but Kam messages Peter or Stuart.
- **Handovers to Peter/Stuart are TEST BLOCKS, never a list of PRs.** Wednesday composes them; you do not hand over.
- **No `--no-verify`, no force pushes, no `--admin`.** A gate that stops you is asking a question: answer it.
- **Never deploy.** No kintsugi or demo, no `deploy.sh`, no remote `docker compose`. (Project hold: no deploy without migration 048 applied first. KS-1031.)
- **Other authors' PRs, and open PRs not in this queue (#887, #920, #922, #923, #995 …), are not yours.**
- **Seats of this project share one inbox** (`secuura-blockchain@agentmail.to`, per `fleet/inbox_routing.conf`). **A mail naming a PR or ticket that is not in YOUR queue is not yours.** Ignore it. GO/ANSWER mails name the PR number.
- **Your own `git worktree` only.** Never the shared checkout.
- Before filing any ticket, search the board by the SYMBOL, the file path or the error string, and say what you searched. The unit of a ticket is the test pass (Kam, 2026-09-07 13:23). New and unassigned tickets go to the board account.
- A control must be able to fail. A zero from an instrument nobody showed could fire is not a zero.
- `cmd > out 2>&1; rc=$?`, then read the file. macOS has no `timeout`. A `pgrep -f` pattern matches your own command line.
- **If a line in this brief looks wrong at source, say so** in a QUESTION mail. While blocked, re-check the inbox every ~3 minutes. Anything approval-class (a merge, a prod or demo effect, external comms) waits for the ANSWER however long it takes.
- **Session end:** send the wrap mail `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-1x` (first line `Seat A`) listing every PR: number, head, state, and ticket state.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-16 21:08
