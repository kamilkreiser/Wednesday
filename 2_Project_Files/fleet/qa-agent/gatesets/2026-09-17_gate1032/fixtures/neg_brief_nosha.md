# QA Agent Invocation Brief — Secuura/Blockchain **TIER 1** **ROUND 1** gate (round 1 of 2 under the cap): PR #1032 (KS-1194, Seat A) @ `70ee7b6c0` — `services/auth`: a verification-request save that did not persist is never acknowledged. `saveVerificationRequest` writes the row first and sets the memory copy only after it lands; an infrastructure failure answers 503 and anything else is rethrown (500). The review's approve saves the APPROVED row BEFORE raising the level; a level update that throws or answers `null` restores the row to PENDING and answers 503. A new 11-cell vitest.

**TIER 1, and why (Wednesday's receipt, `GS/receipt_1032.md`):** the verification level is an assurance level other services gate on. The defect the ticket names (#1015 gate F5) is a 200 over a request row that does not exist, and an approve that **raised the user's level while the row stayed PENDING**. Kam ruled the card `secuura-ks1194-failed-save-answers-200` **fail-closed** (07:50 AEST: *"Seat A builds it"*; *"failed save answers 503; approve raises the level only after the row persists; tier-1 gate; merge held for your tap"*). **This gate does NOT authorise a merge. The merge waits for Kam's tap**, relayed in a signed Wednesday mail naming the head. No rendered surface changes: the real-browser half of tier 1 does not apply (say so, with the reason, in one line).

**Drafted** 2026-09-17 22:13–22:4x AEST (clocks from `date`) by Wednesday's drafting subagent. `GS/` = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1032/`: scripts at its root, every run output under `GS/out/`, and `DRAFTER_REPORT.md` holding the predictions, the disagreements and what the drafter could not predict.

**PRIOR REPORT** (the gate that found this defect, #1015 / KS-1018, finding F5, rows S6a–S6d and L4): `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1018-1015-77145ce84-tier1-r1/`. Read F5 before planning. The house-helper contract this change sits beside is #1018's (KS-1050, `updateUserOrThrow`): `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1050-1018-efd677e98-tier2-r2/`. The QA agent has no inbox.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. You are FINDINGS-ONLY. You never fix, merge, push, deploy, comment on Linear or GitHub, file, tick an ack box, or `@` anyone. You mail ONE verdict to Wednesday.

## HOLDS (verbatim — they bind you)
- Client-facing communication = ticket comments only, and not from you. **Nobody messages Peter or Stuart.** Anything needing a push goes to Wednesday as an escalation candidate.
- Never delete; cleanup means quarantine. Fresh `mktemp -d` per attempt. NEVER `rm`.
- **KS-535: the local stack stays HOLD.** No shared docker stack, no `:6882`/`:7082` slot, no kintsugi, no demo, no deploy, no `az`. NEVER the wallet mnemonic, a `.env`'s contents or real key material. **This gate needs NO container and NO upstream.** Run auth's REAL `userRoutes` + REAL `userRepo` + REAL `errorHandler` + REAL `isInfrastructureDbError` in-process over a stateful `db` stub (the ks1050 test's pattern: `vi.mock('../db')` keeping the `users` row and the `verification_upgrade_requests` rows, only the subject-DEK store stubbed). Run `docker info` ONCE and print its rc on its own line; UP is not permission; create no container.
- **Network: loopback only.** Every listener binds `127.0.0.1:0`. **Any listener or login stub your runs start, you end by pid.** Identify it by port + argv + cwd, SIGTERM that pid, never a pattern kill, never pid 1, and recount after. Quote an `lsof` TCP LISTEN census at start and close, with cwd/argv per node pid and the `login_stub.mjs` count. At 22:30:35 there were 21 LISTEN rows and 4 node `login_stub.mjs` listeners with cwd under `worktrees/raise-0917-b-audit-2` (another seat): none are yours. At 22:41:08: 17 rows, 0 stubs, 0 node listeners under the drafter's clone.
- **The Secuura checkout is READ-ONLY:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`.
  - Work in your OWN clone (`git clone --shared --no-checkout` into your own fresh `mktemp -d`). Git write verbs run there only, from a script file; never run `merge-tree --write-tree`, `worktree`, `fetch` or `checkout` in the checkout.
  - Never enter any seat's worktree or another gate's clone (other gates are live). The seat's records (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-17_seatA-7th/ks1194/`) are READ-ONLY files; their runner hard-codes the seat worktree — never execute it.
  - Pin by SHA, never `origin/*`.
  - NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout or any of its worktrees.
  - Never `cd` on a command line; absolute paths only.
- **node_modules per ENTRY — create one only where something runs.** Farm `Blockchain/Dev/node_modules` (987 entries, `.vite` skipped, `@secuura/*` relinked INTO your tree), `packages/shared/node_modules` (8) and `services/auth/node_modules` (9 incl. `.package-lock.json`, `.vite` skipped), each per ENTRY. Never link a node_modules tree wholesale. Build the shared dist per tree (auth's `vitest.config.ts` aliases `@secuura/shared/utils/logger` to `packages/shared/dist/`) and assert `@secuura/shared` resolves IN TREE from auth. Node runs only with cwd inside your clone.
- **PROBES AND SCRATCH FILES LIVE OUTSIDE `services/auth/`** (the #1018 round-2 gate's F-3): not under `src/`, no `.test.ts` anywhere under the service root, and no scratch tsconfig left under it either (the drafter's own slip, below).
  - **Drafter pattern (MEASURED, `GS/out/drafter_probe.out`):** the probe at `<tree>/Blockchain/Dev/qa_probe_1032/qa1032-drafter-probe.test.ts`, every `vi.mock` / `import` path ABSOLUTE (9 of them). A scratch `vitest.qa1032.config.mts` beside it, passed with `--config`: `root` = the probe dir, `include` = the probe file only, `setupFiles` = auth's `vitest.setup.ts` (absolute), and the `@secuura/shared/utils/logger` alias (absolute). Template: `GS/src/qa1032-drafter-probe.template.ts` (`__AUTH__` = the absolute `services/auth` path).
  - **Before your first tamper row, prove it** (drafter: head 65 files, 0 qa_probe): auth `vitest list --filesOnly` lists 0 qa_probe (control: the ks1194 test listed), and `tsc -p . --listFilesOnly` lists 0 qa_probe (control: `routes/users.ts` listed).
- **Keys by NAME only:** `GH_TOKEN` and `LINEAR_API_KEY` are read by a script from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`; `AGENTMAIL_API_KEY` by NAME from `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env`. NEVER print a credential value. **GitHub: GET only** (a by-SHA fetch into your own clone through a GIT_ASKPASS helper is allowed). **Linear: query only.** Copy `GS/gh_read_1032.py` and `GS/linear_read_1032.py`.
- **Scope cap (Kam's 40% weekly-usage cap): no Akto, no k6, no Playwright, no Schemathesis run.** They are NOT COMMISSIONED. You RULE whether Schemathesis or Akto is REQUIRED (item 9).
  - **Time-box: 40 minutes of work.** A leg that would blow it is NOT RUN, with its blocker named.
  - Priority if time runs short: 1 → 2 → 3 → 4 → 5 → 8 → 6 → 7 → 9 → 10.
- No `rm`; stderr is never discarded (write it to a file); every clock reading comes from `date`. Do no memory maintenance of your own store inside this session.

## 1. Target (read 22:13–22:30 AEST — `GS/out/gh_read.out`, `GS/out/linear_read.out`, `GS/out/drafter_setup.out`, `GS/out/devmove_read.out`)

| item | value |
|---|---|
| PR / ticket | **#1032 / KS-1194**: Linear In Progress, prio 2, related KS-1018, 2 comments (`05e914f9` Kam's ruling relayed; `e4886f22` the PR note). Branch `feature/ks-1194-auth-verification-requests-a-failed-save-still-answers-200-a`. Open, not draft. **4 commits, 2 files, +286 −31.** Title "KS-1194: a verification-request save that did not persist is never acknowledged". Body 8,491 chars, 0 at-signs, 0 closing phrases, `Refs KS-1194`, a `## Test Evidence` block, and "Not in this change: the MFA auto-approve branch". KS ids in the body: KS-1194 ×5, KS-1018 ×2, KS-1201, KS-256, KS-943. 0 reviews, 1 issue comment. |
| head | **`70ee7b6c0`** = the branch = `refs/pull/1032/head` (ls-remote 22:13:01, 22:26:54, 22:30:34; PR API 22:26:01). The change **`00236c10bc9c237e64e008f6bb927c816a8bb29c`** (parent `d7e95cd9f`), then three develop merges: `29d9f90fa` (← `81ee4b729`), `c82f5edd5` (← `75ad0e55c`, which carries #1018 in the same users.ts), `70ee7b6c0` (← `0a2b1603f`, #1028, api-gateway only). Head tree **`1111602c4ef8a8ca08b3f500ee241ec5fc1c0577`**. |
| the 2 files (develop `0a2b1603f` → head blobs) | `Blockchain/Dev/services/auth/src/routes/users.ts` `c723a68af` (= #1018's landed blob) → **`8299a2558`** (+67 −31). `…/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` absent → **`bc8f924c3`** (+219, 11 cells). |
| develop | Pinned **`0a2b1603fe52f0f3b8152588af78bbeab0237be7`** (#1028's squash) = the head's merge-base and second parent. **develop MOVED during drafting to `bb848b8283eb5ee6a6180067315b76f1321e7b6b`** (KS-1211: vitest / @vitest/mocker 4.1.11 in 26 standalone locks + the root lock; 43 files, **0 GUARDED paths, 0 JUDGED files**; includes `services/auth/package-lock.json`). compare develop...head = merge_base `0a2b1603f`, **diverged, ahead 4, behind 1, files 2**. Merged tree (drafter clone, `merge-tree --write-tree 70ee7b6c0 × bb848b828`): **`beee976ddcd75978e7b99f49cc175c85f7abfdb1`**, 0 conflicts. |
| UNTOUCHED (blob identical at develop and head) | auth `repositories/userRepo.ts` `9060b308e` · `repositories/dbErrors.ts` `f94faf0d3` · `middleware/errorHandler.ts` `1cf66e74c` · `db.ts` `cf0ee130b` · `types/index.ts` `9b0b4f08a` · `index.ts` `edabbf871` · `__tests__/ks1018-…` `6723276d0` · `__tests__/ks1050-…` `ffb3e801a` · `__tests__/ks949-platform-admin-seed-identity.test.ts` `4f03e6f4f` · `auth.openapi.ts` `2c356c3c7` · `package.json` `814e88419` · `vitest.config.ts` `8bb96293a` · `vitest.setup.ts` `bc18c1875` · `tsconfig.json` `a7952bdea` · `packages/shared/src/db/tenant-guc.ts` `86953b978` · `docs/openapi/secuura-api.yaml` `122d3a2f8` · Dev `eslint.config.mjs` `8c5374c60`. |
| Linear (22:26:31) | **`attachmentsForURL(pull/1032)` = 1 node: KS-1194 `contributes`**, created 12:09:14Z. Controls: `pull/1018` → KS-1050 `contributes`; `pull/99999` → 0. KS-1194 In Progress. |
| siblings (PR files API, 22:26:01) | 21 open PRs. **Exact shared files with #1032: 0.** Auth-path neighbours: #575, #649, #948 (each `services/auth/package.json`, JUDGED → exit 18 if one lands). This lineage's cap: #1029, #1031, #1032. Seat A builds KS-1215 next, locally. |
| the Secuura checkout (read only) | branch `feature/ks-597-b-caller-scoped-externalref`, porcelain 0, 112 `.git/worktrees`, auth `node_modules/.vite` = `vitest` at 22:17:56, 22:18:02, 22:30:34 and 22:41:08. `.git/config` sha256 `09959c342094001c…` and 939 refs at the first three; **`f9ef2cb7e4b9fa5a…` and 940 refs at 22:41:08** (another session; the drafter ran read verbs only there — attribute nothing). |
| toolchain | node v24.7.0; vitest **4.1.10** installed in the checkout (= develop `0a2b1603f`'s root lock; `bb848b828`'s locks say 4.1.11); typescript as installed (re-read yours). |
| REPORT DIRECTORY | `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1194-1032-70ee7b6c0-tier1-r1/`. Write `NOT-TESTED.written-first.md` FIRST, then `report.md` and `evidence/`. |

## 2. Spec / DoD — what this gate must establish

**The change, READ at `70ee7b6c0` (`users.ts`):**

- **`saveVerificationRequest`** (`:1156`): no database → memory only, return (unchanged). Otherwise `INSERT … ON CONFLICT (id) DO UPDATE SET status, reviewed_at, reviewed_by, rejection_reason`; on a throw it logs `logger.error('DB saveVerificationRequest failed', {error, code})` (no request id), then `isInfrastructureDbError` → `ServiceUnavailableError` (503, "Authentication service temporarily unavailable, please retry"), else rethrow (500). **Memory is set only after the INSERT resolves. The INSERT's `rowCount` is not read.**
- **`POST /me/verification`** (`:1257`): zod → `getUserById` → level ordering → `findPendingVerificationRequest` → **the MFA auto-approve branch `:1276-1284`** (`targetLevel === 'STANDARD' && user.mfaEnabled` → `await userRepo.updateUser(user.id, {verificationLevel: 'STANDARD'})`, **return discarded**, **no request row saved**, 200 `status: 'APPROVED'`) — **untouched by #1032** → else build PENDING, `saveVerificationRequest`, 200 PENDING.
- **`POST /verification/:requestId/review`** (`:1323`): admin role gate 403 → `getVerificationRequest` 404 → KS-467 tenant check for non-platform admins → not PENDING 400 →
  - **approve:** `approved = {...request, status APPROVED, reviewedAt, reviewedBy}`; `saveVerificationRequest(approved)`; `raised = await userRepo.updateUserPlatformScope(...)` inside try (a throw logs `'Verification approve: raising the verification level failed'` with `{requestId, userId, error}`); `if (!raised)` → restore `saveVerificationRequest({...request, status: 'PENDING', reviewedAt: undefined, reviewedBy: undefined})` (a restore throw logs `'…the level was not raised and the request row could not be restored to PENDING; the row may read APPROVED at an unchanged level'` with `{requestId, userId, error}`) → throw 503; else 200 `data: approved`.
  - **reject:** `rejected = {...}`; `saveVerificationRequest(rejected)`; 200 `data: rejected`.
- **`updateUserPlatformScope`** (`userRepo.ts:535`) = `runWithPlatformScope(() => updateUser(...))`. **`updateUser`** (`:796`): under platform scope `currentTenantId()` is undefined, so it resolves `tenantForRls` via `getUserByIdPreAuth` (`auth_find_user_by_id`), runs `UPDATE users … WHERE id` (**no try/catch: a raw pg error propagates**), answers **`null` on rowCount 0**, else returns `getUserById(id, tenantForRls)` — **a read-back that can itself throw 503 or answer `null` AFTER the UPDATE landed** (the helper docblock `:930-957`: "`null` … the UPDATE matched no row, OR the trailing read-back found nothing").
- **The house helper** `updateUserOrThrow` (`userRepo.ts:960`, #1018 / KS-1052) wraps tenant-scope `updateUser` only; there is no platform-scope variant. Its contract: 503 `"<operation> could not be confirmed. Please retry — if you already succeeded, you may not need to."`; its docblock forbids asserting "the change was not applied" (QA F-929-2).
- **Postgres (READ):** `verification_upgrade_requests` (`migrations/001_initial-schema.sql:669`) has no `tenant_id`, so migration 009's RLS loop skips it (KS-467's comment: "carries no RLS policy"); no trigger names it. An upsert with no `WHERE` therefore always reports 1 row.
- **The OpenAPI (MEASURED + READ):** neither verification route is in the published spec (`docs/openapi/secuura-api.yaml`: 10 `/api/users` paths, 0 containing `verification`; control `/api/users/me:` present). `auth.openapi.ts`'s header lists them as "still not registered". `npm run generate-openapi -- --check` at head: `CHECK PASS`.

**The seat's claims (READY `GS/mail_1032_ready.md`, spf/dkim/dmarc pass; measure every one):**
> - C1. A verification-request save that did not persist answers 503 (infrastructure) or 500, never 200 PENDING.
> - C2. Approve saves the APPROVED row BEFORE raising the level; a level update that fails or matches no row restores the row to PENDING and answers 503.
> - C3. Residual (stated): if that restore also fails, the row may read APPROVED at an unchanged level; 503 with one error line naming the request id.
> - C4. develop `0a2b1603f` merged in; tree `1111602c4` = the merge-tree prediction; auth subtree `f822c95f8` and shared `dbd72dea0` unchanged by the merge.
> - C5. Files vs develop: users.ts +67 −31, the new test +219.
> - C6. Tamper table `ks1194/tamper_1194_r7.py` at this head, 60 s ceilings: T0 0 · RP-DEV 9 · REORDER 4 · SWALLOW 5 · MEMFIRST 1 · NORESTORE 3 · NOLOG 1 · TI 0; 23 reds, all AssertionError, tsc 0.
> - C7. Auth 65 / 773 at 60 s; 771 / 773 at default (two ks949 cells ≥5 s timeouts at load 32.7). tsc (service program) 0. eslint 0 / 0. The test-including tsc program NOT measured.
> - C8. NOT covered: a real Postgres, multi-replica memory, **the MFA auto-approve branch**, Schemathesis / Akto / Playwright / k6.
> - C9. Links: KS-1194 `contributes`; Refs, no closing phrase.

### WHERE THE READY AND THE DRAFTER'S MEASUREMENTS DISAGREE, OR WHERE THE CELLS ARE SILENT (lead with these; each is a PREDICTION — `GS/DRAFTER_REPORT.md`)

Drafter harness (`GS/out/drafter_probe.out`, rows `GS/out/rows_probe_{dev,head}.json`, 31 rows × develop / head): the real routes + the real repo over a stateful db stub with a per-row fault plan — the INSERT `ok | infra (ECONNREFUSED) | other (22001) | zero (rowCount 0, nothing stored)`; `UPDATE users` `ok | zero | infra | other`; the pre-auth lookup `ok | infra`; the read-back after a landed UPDATE `ok | infra | empty`.

- **D0 — the census of every save path (MEASURED; C1 / C2 hold wherever the store throws).** At head every THROWING save answers 503 (infra) or 500 (other), never 200, with no row written and nothing kept in memory:
  - submit S-INFRA 503 / S-OTHER 500 (develop 200 PENDING, no row); S-INFRA-THEN-LIST: the memory fallback lists 0 at head, 1 at develop;
  - approve A-SAVE-INFRA 503 / A-SAVE-OTHER 500, row PENDING, level basic, 0 `UPDATE users` (develop: 200 approved, **level raised, row PENDING** = the ticket);
  - A-UPD-ZERO / A-UPD-INFRA / A-UPD-OTHER / A-PREAUTH-INFRA: 503, row restored PENDING, reviewed_by null, level basic;
  - reject R-SAVE-INFRA 503 / R-SAVE-OTHER 500, row PENDING;
  - controls: S-OK, A-OK (SYSTEM_ADMIN and ORG_ADMIN), R-OK 200 unchanged; S-NODB 200 PENDING (memory only, unchanged).
- **D1 — the MFA auto-approve branch is not fail-closed (MEASURED, pre-existing, not widened; the READY's C8 names it NOT covered).** develop = head:
  - M-UPD-ZERO (the UPDATE matches 0 rows) → **200 "Verification level upgraded to STANDARD (MFA already enabled)", `status: APPROVED`, level still `basic`**;
  - M-UPD-INFRA / M-UPD-OTHER → **500** (not 503: `updateUser` does not classify its own UPDATE's error);
  - M-READBACK-INFRA → 503 with the level RAISED; M-READBACK-EMPTY → 200, level raised.
  - It saves no request row at all (READ). It is the KS-1052 class `updateUserOrThrow` exists for; the PR body excludes it explicitly.
  - Drafter predicts: **NEW to this gate, pre-existing, Minor-to-Major, TICKET** — unless Wednesday rules Kam's fail-closed ruling covers every verification-level acknowledgement. RULE it, with the 0-row reachability (KS-943's docblock: a 0-row UPDATE under fail-closed RLS "is not hypothetical"; here the caller is post-auth in its own tenant — READ).
- **D2 — "level raised while the row stays PENDING" is still reachable at head (MEASURED on the real repo; not stated by the PR).**
  - **A-READBACK-INFRA** (the UPDATE lands, the read-back SELECT throws ECONNREFUSED → `updateUser` throws 503 → caught → restore): **head 503, row PENDING, level ENHANCED**. develop: 503, row PENDING, level ENHANCED — the same end state (not widened).
  - **A-READBACK-EMPTY** (the UPDATE lands, the read-back finds nothing → `null`): **head 503, row PENDING, level ENHANCED**; develop 200, row APPROVED, level ENHANCED (consistent). A narrow change: a consistent success becomes an inconsistent 503.
  - READ reachability: under platform scope `updateUser` resolves `tenantForRls` once and reads back under it (QA F-1), so the empty read-back is predicted rare; a connection loss between the two separately pooled statements is not.
  - NOT measured by the drafter: what an admin's next action does to that state (a re-approve should be idempotent; a REJECT would leave REJECTED + a raised level). Measure both.
  - Drafter predicts **Minor** (503, not 200), STILL OPEN as an unstated residual of KS-1194, TICKET or SHIPS-WITH a stated-residual line. RULE it against Kam's "approve raises the level only after the row persists".
- **D3 — the restore-failure log line asserts a cause it cannot know (MEASURED).** **A-DOUBLE-READBACK** (UPDATE landed, read-back throws, restore throws): head 503, **row APPROVED, level ENHANCED** (consistent), and the line reads **"the level was not raised … the row may read APPROVED at an unchanged level" — false on both counts.** The #1018 helper's docblock forbids exactly this stronger cause (QA F-929-2). Also: on the `null` path (A-UPD-ZERO) no error line names the request id at all (only `errorHandler`'s generic `Error occurred`, plus `updateUser`'s `warn` with the user id — READ). C3's "one error line naming the request id" holds only when the restore throws. Drafter predicts **Minor**, SHIPS-WITH a wording fix ("could not be confirmed") or TICKET.
- **D4 — house helper vs copy (READ + MEASURED).** The change does not call `updateUserOrThrow` (it cannot as-is: platform scope). Its 503 body is the generic infrastructure message, not the helper's "could not be confirmed". The RESPONSE asserts no forbidden cause → Record; the LOG does (D3). The code comment "matches no row (updateUser answers null, KS-943)" repeats the narrower reading the docblock warns against → Record.
- **D5 — a save that persists nothing is still acknowledged (MEASURED; READ-unreachable in Postgres).** `rowCount` is never read: S-ZERO 200 PENDING, no row; **A-SAVE-ZERO 200 approved, row PENDING, level ENHANCED** (the ticket's end state); R-SAVE-ZERO 200 rejected, row PENDING; A-RESTORE-ZERO 503, row APPROVED, level basic, **no error line**. READ (§2): the upsert has no `WHERE`, the table has no RLS and no trigger, so Postgres always reports 1 row. Drafter predicts **Record**, unless you find a trigger, rule or RLS policy that can make it 0.
- **D6 — the 11 cells do not pin the 503 wording, the log payload, the restore's reviewed_at or the 200 bodies (MEASURED tampers, `GS/out/drafter_tamper.out`).** Each row: tsc 0, whole auth 65 / 773, **0 reds**, 0 outside, restored; the consequence measured by the probe ON THE TAMPERED TREE:

  | tamper | form | consequence the cells miss |
  |---|---|---|
  | **X-503-WORDING** | the approve 503 → "Verification approve was not applied: the level update matched no row" | A-UPD-ZERO / A-READBACK-INFRA answer the forbidden cause (the latter with the level raised) |
  | **X-LOG-NOUSERID** | the double-failure payload → `{ requestId }` | the line loses the user id and the cause |
  | **X-LOG-RAISE-DROPPED** | the raise-failure `logger.error` → `void err` | A-UPD-INFRA: no line names the request |
  | **X-RESTORE-KEEP-REVIEWEDAT** | restore `{...approved, status: 'PENDING', reviewedBy: undefined}` | the restored PENDING row keeps the approval's `reviewed_at` |
  | **X-APPROVE-BODY-STALE** / **X-REJECT-BODY-STALE** | `data: request` | 200 bodies say `status: PENDING` over an APPROVED / REJECTED row |

  Plus two that DO red (drafter controls): X-SAVE-INFRA-AS-500 → 3 reds; X-RESTORE-REJECTED → 2 reds. Drafter predicts **Minor test gaps**, SHIPS-WITH optional cells or Record.
- **D7 — the ks949 timeouts are load, not the PR (MEASURED).** At load 3–6: develop `0a2b1603f` 64 / 762 and head 65 / 773, **0 failed at DEFAULT ceilings and at 60 s**; `ks949-platform-admin-seed-identity` alone 30 / 30 on both trees. The builder's two reds were at load 32.7. Record.
- **D8 — the contract (MEASURED + READ).** Both routes are outside the published spec (pre-existing; `auth.openapi.ts` header, whose "/admin/* still not registered" is stale — the YAML carries 4 `/api/users/admin/*` paths). The new 503 / 500 are undeclared. `generate-openapi --check` CHECK PASS. In-repo callers (drafter READ: `git grep` for `me/verification` and `users/verification` over the whole repo at head, control users.ts 5 hits): no portal, SDK, mobile, connector or gateway caller; the only caller is `systemTest/schemathesis/tests/test_user_admin_isolation.py:328-345`, a VERIFIER 403 role-gate test, unaffected. Drafter predicts: a contract gap Record, not a blocker.

### MUST ESTABLISH — each a question to MEASURE. Name the tree beside every count.

1. **THE FAIL-CLOSED CENSUS, develop vs head, on the REAL routes + REAL repo.**
   - Enumerate every code path in `services/auth` that saves a verification request or acknowledges a verification level: submit, the MFA auto-approve, approve, the restore, reject, and any other caller of `saveVerificationRequest` / `verificationLevel` writes you find (re-derive the census yourself with `git grep` + a positive control per pattern; the drafter found 4 `saveVerificationRequest` call sites + the MFA `updateUser`).
   - Per path × {store throws infra, throws other, persists nothing (0 rows / `null`), the level UPDATE lands but its read-back throws / is empty}: status, code, message, `data.status`, the statement order, the stored row (status, reviewed_by, reviewed_at), the stored level, every `logger.error` (message + payload keys), and the memory copy.
   - **FAIL (Blocker, F-class): at head, any 200 / 200 PENDING / 200 APPROVED / 200 REJECTED whose store THREW, or any 200 approve with the level raised and the row not APPROVED, on a path #1032 changed.** D1 (untouched branch) and D5 (0-row, READ-unreachable) are ruled separately.
   - Drafter (MEASURED): D0, D1, D2, D5. Put A-READBACK-INFRA, A-DOUBLE-READBACK and M-UPD-ZERO in your table by name.
2. **APPROVE ORDERING, RESTORE AND THE STATED RESIDUAL.**
   - The APPROVED row saved before the level UPDATE (statement order); a level update that throws OR answers `null` restores PENDING with reviewed_by AND reviewed_at cleared, and answers 503.
   - The stated residual (C3): restore throws → row APPROVED at an unchanged level, 503, ONE error line with the request id. **Is that line sufficient for an operator** (does it carry the user id, the target level, the cause; is it true when the level WAS raised — D3)?
   - **Is there any path where the level is raised while the row stays PENDING?** Drafter: yes, D2. Then measure the admin's next move on that state (re-approve; reject).
3. **HOUSE HELPER vs COPY.** Does the change use `updateUserOrThrow` or a copy? Compare the status, the wording and the log against the helper's contract and docblock (`userRepo.ts:930-975`). A copy that contradicts the contract is a finding (precedent QA F-929-2). Drafter: D3, D4.
4. **TAMPERS on the WHOLE auth suite** (`vitest run --testTimeout=60000 --hookTimeout=60000`, json): denominator asserted **65 / 773**, pending 0, project tsc rc per row (non-compiling = VOID), sha-restored + `git diff --quiet`, reds per ks1194 cell split ASSERTION vs other, 0 outside the file.
   - **The seat's 8 rows re-derived EXACTLY** from its runner's `ROWS` literal (READ the file; parse the literal; never execute the runner). Drafter (MEASURED, all tsc 0, all 65 / 773, all restored): **T0 0 · RP-DEV 9 · REORDER 4 · SWALLOW 5 · MEMFIRST 1 · NORESTORE 3 · NOLOG 1 · TI 0 = 23 reds, 8 / 8 = C6.**
   - **The drafter's 8** (D6): 6 zero-red rows with consequences + X-SAVE-INFRA-AS-500 3 + X-RESTORE-REJECTED 2.
   - **PLUS your own**, aimed at what neither table pins: e.g. the restore target `...approved` instead of `...request`; `if (!raised)` → `if (raised === null)` with a throwing update; memory set inside the catch; the reject path saving the looked-up object in place; a `rowCount` check added (does any cell notice?).
5. **MERGE-IN.** Prove, in your clone: each of the three merges equals `merge-tree --write-tree` of its own parents (drafter: `29d9f90fa` → `c896e5492`, `c82f5edd5` → `691d29189`, `70ee7b6c0` → `1111602c4`, all EQUAL, 0 conflicts, each brought exactly develop's own delta: 7, 19, 2 files); develop `0a2b1603f`..head = exactly users.ts + the ks1194 test (+67 −31, +219); the users.ts patch-id `fix^..fix` = `0a2b1603f..head` (drafter `c1264e780015` both); the ks1194 test byte-identical fix = head; auth subtree `c82f5edd5` = head `f822c95f8`, shared `dbd72dea0` everywhere.
6. **CHECKS.**
   - Auth vitest at develop `0a2b1603f` and head, **at default ceilings AND 60 s** (drafter: 64 / 762 and 65 / 773, 0 failed both ways, load 3–6); the ks949 file alone at default on both trees (30 / 30). Quote the 1-minute load beside every run and attribute any timeout.
   - `tsc --noEmit -p .` rc 0 each.
   - **THE TEST-INCLUDING tsc PROGRAM** (auth's tsconfig EXCLUDES `src/__tests__`): a scratch tsconfig **outside** the service root or moved out after, `--listFilesOnly` proof the ks1194 test is in it and not in the project program, and a planted control. Drafter: **37 error lines on BOTH trees, all in 21 OTHER test files (TS6133 unused etc.), 0 in the ks1194 test**; plant +1. Say whether 37 = 37 is a pre-existing baseline (it is on develop).
   - eslint by rule AND message on users.ts (both trees) and the ks1194 test, with a firing control. Drafter: 0 / 0 / 0; the control gives 2 `@typescript-eslint/no-unused-vars` **warnings** (rc 0 — the rule is warn-level: say whether a 0-error rc proves anything).
7. **CALLER BEHAVIOUR + CONTRACT.** Does any caller in the repo (portals, add-ins, SDKs, mobile, systemTest, tests, `docs/openapi/`) depend on 200 from a failed save? Does the published contract declare 503 / 500 for these routes (D8)? Run `npm run generate-openapi -- --check`. A contract gap is a finding, not a blocker.
8. **LINEAR / GITHUB at run time and immediately before the mail:** `attachmentsForURL(pull/1032)` = KS-1194 `contributes` only (controls `pull/1018` → KS-1050; `pull/99999` → 0); 0 closing phrases in the title, body and all 4 commit messages (planted controls); the body has `Refs KS-1194` and a `## Test Evidence` block; **KS-1194 stays In Progress on merge (§5f: a live sweep is owed)**.
9. **SCHEMATHESIS / AKTO: REQUIRED?** Rule with a measured reason. Drafter's view: both routes are outside the published spec (D8), so neither generator can reach them, and the defect needs a store fault neither can inject.
10. **CARRY-FORWARD per finding, CLOSED / STILL OPEN / NEW, each SHIPS-WITH or TICKET:** KS-1194 = #1015 F5 (per path: submit, approve, reject); D1 (MFA auto-approve); D2 (level raised, row PENDING via the read-back); D3 (the log line); D5 (0-row); D6 (unpinned properties); D8 (contract gap); KS-1018 item 3 (the memory-only path — untouched). Also report the checkout bounds and NOT TESTED at equal prominence.

## 2a. LEGITIMATE SHAPES — the fail-closed save IS a checker (required)

Rule under test: a verification-request save or a level raise whose effect is not confirmed is never answered 200; a confirmed one is answered exactly as before.

| shape — its ordinary form | expected verdict | clause | predicted-by |
|---|---|---|---|
| submit, healthy DB | 200 PENDING, 1 row, memory set | INSERT resolves | drafter (measured S-OK) + seat cell |
| submit, no database configured | 200 PENDING, memory only (unchanged) | `!isDbAvailable()` | drafter (S-NODB) + seat control |
| approve, healthy DB, SYSTEM_ADMIN and ORG_ADMIN in-tenant | 200 approved, row APPROVED, level raised, save before UPDATE | `raised` truthy | drafter (A-OK, A-OK-ORGADMIN) + seat cell |
| reject, healthy DB | 200 rejected, row REJECTED, level untouched | save resolves | drafter (R-OK) + seat control |
| MFA user asks STANDARD, healthy DB | 200 APPROVED, level standard (unchanged) | untouched branch | drafter (M-OK) |
| a second submit while one is PENDING | 400 "already pending" (unchanged) | `findPendingVerificationRequest` | NOT PREDICTED (measure) |
| review of a non-PENDING row | 400 "Request already <status>" (unchanged) | status gate | NOT PREDICTED (measure) |
| a retry after a refused submit | 200 PENDING, exactly one row | nothing kept in memory | drafter (S-INFRA-THEN-LIST) + seat cell |
| in-repo callers | none depends on 200 from a failed save | — | drafter (READ census, D8) |
| Platform-S / an out-of-repo portal | UNKNOWN — body not in repo | — | NOT PREDICTABLE |

## 3. Scope
- **Charter:** falsify "a verification-request save that did not persist is never acknowledged; approve raises the level only after the row persists" on the real auth routes and repo; hunt every other acknowledgement of a verification level; prove no legitimate submit / approve / reject changed.
- **In scope:** auth `POST /api/users/me/verification` (including the MFA auto-approve branch), `GET /api/users/me/verification`, `POST /api/users/verification/:requestId/review`; `saveVerificationRequest` and the three readers; `updateUser` / `updateUserPlatformScope` / `updateUserOrThrow` as called; the ks1194 test; tampers; the auth suite; tsc (both programs); eslint; the OpenAPI; Linear/GitHub reads.
- **Out of scope / do NOT touch:** any stack, container, real Postgres, the api-gateway stage (NOT commissioned; READ only), multi-replica behaviour, deploy, the edge; any write to Linear / GitHub; any seat worktree; Peter / Stuart.

## 4. Credentials (POINTER ONLY — never values)
Secuura `.env` (`GH_TOKEN`, `LINEAR_API_KEY`) and Wednesday's `.env` (`AGENTMAIL_API_KEY`), both by NAME at the paths in HOLDS. Principals are injected by the probe's `authenticate` mock inside `runWithTenantId` (the ks1050 pattern).

## 5. State-mutation & cleanup
Exclude-and-report-only against anything shared. Your clone is disposable; quarantine by MOVE (outside the service root), never `rm`. Assert the whole-suite denominator is unpolluted (65 / 773 at head) with your probe present.

## 6. Output boundary
Findings, reports and recommendations ONLY — no code, tests, tickets or config in the product. Every finding carries its evidence class (**MEASURED AT RUNTIME / PROBED / READ ONLY / RELAYED**), severity, target (PR or TICKET), SHIPS-WITH or TICKET, disposition and oracle. Name every prediction slip against its predictor (the READY, the seat, the drafter, Wednesday).

## 7. Known-fragile / known-changed
- **The db stub is NOT Postgres.** Say which rows depend on it (D2's empty read-back, D5's 0-row upsert). A real RLS 0-row UPDATE was not driven.
- The seat's runner hard-codes its worktree `worktrees/raise-0916-a` and asserts its HEAD: read its `ROWS` literal, never execute it.
- `vi.mock` hoisting: mock paths are resolved relative to the test file — the out-of-service probe needs ABSOLUTE paths (the drafter's 9).
- develop moved to `bb848b828` (vitest 4.1.11 locks) while the farm runs the checkout's 4.1.10: say whether that matters (drafter: merged tree `beee976dd` 65 / 773 on the 4.1.10 farm; auth `src/` and shared subtrees equal the head).
- Recent, do NOT flag as new: #1018 (KS-1050 `updateUserOrThrow` in the same users.ts), #1015 (KS-1018 the read side), #1028 (KS-744 gateway), #1027 / KS-1211 (lock bumps).
- Known open: KS-1018 item 3 (the memory-only path), KS-1188 F3 (a different acknowledge-after-partial-write), the #1031 gate (originate, running in the chain).

## 8. Logistics / BOUNDS
- Quote these at start, mid and close as THREE timestamped readings: the checkout's porcelain count, `.git/config` sha256, for-each-ref count, `.git/worktrees` count, origin develop SHA, `refs/pull/1032/head`, the checkout branch, and the auth `node_modules/.vite` reading. Other sessions move refs; attribute nothing without evidence.
- **If `refs/pull/1032/head` moves, STOP: the brief is about a different SHA.** develop moving is expected: judge it by content, name it, merge it onto `70ee7b6c0` in your clone, name the merged-tree OID, and re-run items 1, 4 and 6 on the merged tree if the move touches `services/auth/src/`, `packages/shared/src/` or auth config.
- **The launcher `--check` guards by PATH BLOB at the current develop,** never by develop's SHA. It checks 19 files: the 2 PR files (LANDED at their #1032 blobs → exit 19) plus userRepo / dbErrors / errorHandler / db / types / index / the ks1018, ks1050 and ks949 tests / auth.openapi / auth package.json / vitest.config / vitest.setup / tsconfig / shared tenant-guc / the YAML / eslint.config.mjs. On a develop move it also checks the GUARDED paths `services/auth/src/` + its config, `packages/shared/src/`, `docs/openapi/` and `eslint.config.mjs`.
- Hygiene:
  - `/bin/bash` is 3.2: write runners in Python.
  - zsh: no PIPESTATUS; `"$VAR:path"` applies history modifiers (write `"${VAR}:path"`); never begin a line with `=====`.
  - `git grep -c` prints nothing for a zero; `rev-parse` of a missing path echoes its argument (use `cat-file -e`).
  - Every scripted edit asserts its anchor count = 1 and a marker.

## VERDICT DESTINATION
Report into the REPORT DIRECTORY (§1), `NOT-TESTED.written-first.md` first. Verdict: ONE line — GO, GO WITH FINDINGS, or NO GO — on `70ee7b6c0` as the delta over develop `0a2b1603f`, AND on the merged tree (name the then-current develop and the merged-tree OID; drafter `bb848b828` → `beee976dd`). **A GO is a gate verdict, not a merge authorisation: the merge waits for Kam's tap.** Mail it FROM `coagent@agentmail.to` TO `wednesday-agent@agentmail.to`, subject EXACTLY `[QA -> Wednesday] TIER 1 GATE #1032 (KS-1194) 70ee7b6c0 — <GO | GO WITH FINDINGS | NO GO>`.

Every finding in the verdict carries CLOSED / STILL OPEN / NEW and SHIPS-WITH or TICKET.

**MERGE ADDENDUM** (fill every `<..>`): "on Kam's tap only: squash `70ee7b6c0` onto develop `<then-current develop; bb848b828 at draft close>` (merged tree `<OID>`; drafter `beee976dd`); #1032 attaches to KS-1194 only, linkKind `contributes`, no closes; KS-1194 stays In Progress on merge (§5f: live sweep owed); equality targets after the squash: `services/auth/src/routes/users.ts` blob `8299a2558` / ks1194 test `bc8f924c3`; auth vitest 64/762 at develop `0a2b1603f` → 65/773 at head → `<merged n/n>` (re-measure); dispositions: `<per finding, SHIPS-WITH or TICKET>`; NEW: `<yours>`; Records for KS-1194's facts comment at merge: the stated residual (restore fails → APPROVED at an unchanged level, 503) `<with your D3 ruling>`, `<D2 ruling: level raised with the row PENDING via an unconfirmed read-back>`, the MFA auto-approve branch `<D1 ruling>`, the 0-row upsert `<D5>`, the undeclared 503 / 500 `<D8>`, `<yours>`."

## NOT COMMISSIONED (say so if asked)
Schemathesis, Akto, Playwright, k6, any docker stack, a real Postgres, a real RLS 0-row UPDATE, multi-replica memory, the api-gateway stage, preflight legs 3/4/8, the edge, a live Platform-S call, a real browser.

## PROVENANCE
- READY + tier | `GS/mail_1032_ready.md` (spf/dkim/dmarc pass), `GS/receipt_1032.md` | read 2026-09-17 22:13
- Kam's ruling | KS-1194 comment `05e914f9` (card `secuura-ks1194-failed-save-answers-200`, fail-closed, 07:50:34 AEST), `GS/out/linear/KS-1194.comments.md` | read 22:26:31
- The finding's origin (F5) | the PRIOR REPORT dir above; KS-1194's description | read 2026-09-17
- Seat's records | `…/5_Project_History/2026-09-17_seatA-7th/ks1194/` (`tamper_1194_r7.py` sha256 `75762edf1ff402ad`, `tamper.out`, `suites.log`, `mergetree.out`) | READ 22:15
- Head, commits, files, compare, blobs, siblings | `GS/out/gh_read.out` 22:26:01; ls-remote 22:13:01 / 22:26:54 / 22:30:34 | 2026-09-17
- develop move | `GS/out/devmove_read.out` 22:26:54; `GS/out/drafter_merged.out` 22:27:45 | 2026-09-17
- Links | `GS/out/linear_read.out` 22:26:31 | 2026-09-17
- Drafter measurements | `GS/out/drafter_setup.out` 22:17:55, `drafter_suites.out` 22:18:42, `drafter_probe.out` 22:21:11 (+ `rows_probe_{dev,head}.json`), `drafter_tamper.out` 22:23:00–22:24:40 (+ `tamper_rows.json`, `tamper/`), `drafter_openapi.out` 22:28:34, `guard_candidates.out`, `bounds_mid.out` 22:30:34, `census_{before,mid}.out` | 2026-09-17
