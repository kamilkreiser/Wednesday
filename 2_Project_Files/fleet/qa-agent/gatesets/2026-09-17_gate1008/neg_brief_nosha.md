# QA Agent Invocation Brief — Secuura/Blockchain **TIER 1** **ROUND 1** gate: PR #1008 (KS-1087 item 1, Seat A) @ `HEAD-SHA-REMOVED` — `POST /api/workflow-instances/:id/approve` awaits originate's status for the forward: a non-2xx or a transport error answers **502 `ORIGINATE_FORWARD_FAILED`** and KEEPS the pending document; only a 2xx deletes it.

**TIER 1, and why:** a behaviour change (a new 502) on an authenticated workflow route, and the change decides whether a pending document is DELETED (data-destruction semantics). The route is mounted in EVERY environment: `createVerificationRoutes` sits in a bare block at `index.ts:883-896`, NOT inside `if (ENABLE_MOCK_ENDPOINTS)` (TypeScript AST with a positive control — the `log('warn', 'Mock endpoints enabled…')` call reads as inside that `if`; `mount_ast.out` 00:59:22). The tier rule is `0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`. There is no rendered surface (no in-repo caller of this route, item 9), so the real-browser half of tier 1 does not apply. Say so. **Round 1 of 2 for the KS-1087 class under the cap.**

**Drafted** 2026-09-17 00:55–01:1x AEST by Wednesday's drafting subagent. The gate set is `2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008/`. Every SHA, blob, line number and count below was READ in the same step as the sentence that states it; the `.out`/`.json` named beside each fact is the instrument, and its time is inside it. The seat's claims (Seat A's READY mail 2026-09-16T14:53:04Z, spf/dkim/dmarc pass, `mail_1008_ready.md`; the PR body `gh/pr1008_body.md`; the seat's records `Blockchain/5_Project_History/2026-09-16_seatA/a8-ks1087/`) appear as **"the seat reports X; measure it"**. They are inputs to falsify, never evidence. **Rows marked `drafter (measured HH:MM, <file>)` were run once by the drafter in a `--shared` scratch clone to prove the harness is feasible. They are still PREDICTIONS for you: re-measure every one.** A prediction that misses is the drafter's slip to name, not a finding against the PR.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. You are FINDINGS-ONLY. You never fix, merge, push, deploy, comment on Linear or GitHub, file, tick an ack box, or `@` anyone. You mail ONE verdict to Wednesday.

## PRIOR REPORT ON DISK (not a round N-1 of this PR — the gate that FOUND the defect KS-1087 fixes)
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1041-951-02a22f4bb-tier1-r2/report.md` (`:336-341`): the recorded forward (`x-user-id` only, no bearer) replayed into the real originate app got **401 in both vouch modes**, and with originate answering 401 the real gateway handler returned **200 `approved`** and deleted the pending document. No prior verdict exists on any #1008 SHA.

## HOLDS (verbatim — they bind you)
- Client-facing communication = ticket comments only; the extranet is not a channel; anything needing a push goes to Wednesday as an escalation candidate for Kam's WhatsApp. Handovers to Peter/Stuart are test blocks, never a list of PRs. Nobody messages Peter or Stuart.
- never delete; cleanup means quarantine. Fresh `mktemp -d` per attempt. NEVER `rm`.
- **KS-535: the local stack stays HOLD.** No shared docker stack, no `:6882`/`:7082` slot, no kintsugi, no demo. NEVER touch a wallet mnemonic, a `.env`, or `config/secrets.yml`. **This gate needs NO container.** Everything runs in-process: vitest cells against the REAL `createVerificationRoutes` (and the REAL `authenticateToken` for item 4) on loopback, originate stubbed at the HTTP seam with a hit counter. Run `docker info` ONCE and print its rc on its own line (**the drafter did NOT run it**). **Up is NOT permission.** Create no container and touch no `secuura-*` container.
- **Network: loopback only.** Every listener binds `127.0.0.1:0` (KS-860). No off-host traffic. (The seat's unreachable cell dials `127.0.0.1:1` — loopback, and a refused connect.)
- The gate never merges. **Scope cap tonight (Kam's 40% weekly-usage cap): no Akto, no k6, no Playwright.** Schemathesis: **not run: measured reason** (0 docker images on this host; the only venv is 4.25.2 vs the pinned 4.27.1) per Wednesday's 2026-09-16 13:53Z ruling — **you decide whether the leg is REQUIRED for this change (item 9)**. Time-box: **45 minutes** of work. If a leg would blow it, record it NOT RUN with its blocker named.
- NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout or any of its worktrees. Never `cd` in your own tool calls. Clone by SHA into your scratch (`git clone --shared`), and run write verbs THERE only, from a script file.
- **Live neighbours:** the #1006 (KS-844, tier 1) gate is RUNNING in its own clone and the #1007 (KS-864, tier 2) gate may still be (#1007 merged at 01:12:54), and Seat A's worktree is live. Never enter any of them, never read or write `gatesets/2026-09-17_gate1006/` or `…_gate1007/`, never run vitest in the checkout.
- NEVER print a credential value, and never open a secrets file. Count, never echo. Do no memory maintenance of your own store inside this session.

## 1. Target (read 00:55–01:06 AEST by `git ls-remote`, `git`, the GitHub API and the Linear API — `git_read.out`, `blob_dump.out`, `gh_read.out`, `linear_read.out`, `blobs_read.out`, `consumer_read.out`, `mount_read.out`, `mount_cond_read.out`, `mount_ast.out`, `strand_read.out`, `nginx_read.out`)

| item | value |
|---|---|
| PR / ticket | **#1008 / KS-1087 (item 1 of 2)**. Branch `feature/ks-1087-ornith-workflow-approve-keeps-pending`. Author `kksecura`. Open, not draft, `mergeable true / unstable`. **1 commit, 2 files, +183 −1.** Title "KS-1087 (item 1): workflow-approve keeps the pending document when originate refuses the forward". Body 5,850 chars: `## Test Evidence` ×1, `Part of KS-1087` ×2, **closing phrases found by `(?i)\b(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+KS-\d+` = `[]`**, KS ids {KS-1087}, **0 at-signs**, 0 ack markers. 0 reviews, 0 review comments, 1 issue comment (linear[bot] `5699509924`, KS ids {KS-501, KS-1083, KS-1084, KS-1087}). `gh_read.out` 00:57:25, raw `gh/` |
| head | **`HEAD-SHA-REMOVED`** = `refs/heads/feature/ks-1087-ornith-workflow-approve-keeps-pending` = `refs/pull/1008/head` (ls-remote 00:55:40; PR API 00:57:25). Tree `2c33b4f8d`. **Only parent `93629700c3d219c1d8ca61d69150bb9b623fc1be`** (#1005's squash). Author date 2026-09-17 00:46:38 +1000. |
| base / develop | **develop = merge-base = `93629700c`** at 00:55:40 (ls-remote) and 00:57:25 (branches API). `rev-list develop..head` = 1, `head..develop` = 0; compare `develop...head` = merge_base `93629700c`, **status ahead, ahead 1, behind 0, files 2**. At that reading the merged tree was the head tree (asserted by merge-base in `drafter_setup.out` 01:00:06). **DEVELOP MOVED WHILE THIS BRIEF WAS DRAFTED:** `git ls-remote` 01:13:23 reads develop **`0308b7a0447a2c01c12aad358c9b4d04a5178210`** = **#1007's squash** (KS-864, merged 2026-09-16T15:12:54Z), parent `93629700c`, **3 files, all `services/api-gateway/`: `routes/system-status.ts` `956083916`, new `__tests__/ks864a-dead-estate-helper.test.ts` `eb6ea8c22` and `__tests__/ks864b-dead-estate-portals.test.ts` `a073703d2` — file-disjoint from #1008**; compare `develop...dd7086d5a` now reads merge_base `93629700c`, **diverged, ahead 1, behind 1, files 2** (`develop_move_read.out`). The launcher's `--check` at 01:12:58 read the move and cleared it by content (`check.first-run-before-develop-move-edit.out`). **So the merged tree is NOT the head tree:** build it (head + a local merge of `0308b7a04` in your clone, never pushed). The drafter's merge was clean; verification.ts `d0585dc34` and the ks1087 test `7832724f3` are blob-EQUAL to head's there, and the api-gateway suite reads **46 files / 394** (`drafter_merged.out` 01:13:53–01:14:03). If develop has moved again by your start, merge the then-current develop and re-derive. |
| the 2 files (develop → head blobs) | `services/api-gateway/src/routes/verification.ts` `de34b2de7` → **`d0585dc34`** (numstat 9 1) · `services/api-gateway/src/__tests__/ks1087-workflow-approve-deletes-the-pending-document.test.ts` **added `7832724f3`** (174 lines, 3 cells). All under `Blockchain/Dev/`. `git_read.out`, `diff_develop_to_head.patch`, copies in `src/` |
| UNTOUCHED (blob identical at develop and head; `blobs_read.out` 01:05:47) | api-gateway `src/index.ts` `6f38c819e` · `src/middleware/auth.ts` `20311010d` · `src/services/redis.ts` `47659ee9c` · `src/services/enforcement.ts` `533cd309c` · `package.json` `841d8c6ad` · `vitest.config.ts` `5888e0b32` · `vitest.setup.ts` `22c110768` · `tsconfig.json` `c981e6a92` · originate `src/routes/documents.ts` `c3a818ac8` · Dev `eslint.config.mjs` `8c5374c60` · `docs/openapi/secuura-api.yaml` `122d3a2f8` · Dev `package-lock.json` `17d2061b3` · issuer `DocumentList.tsx` `4e319ad29` · mcp-server `api-client.ts` `26a6a3cd1` |
| Linear (00:58:10) | **KS-1087 In Progress**, priority 2, 2 comments (`1a9082e7` 09-11; `af51e52a` 09-16, the seat's facts comment, 0 at-signs), relations related KS-1083 / KS-1084. **Attachments: #1008 only, `linkKind = 'contributes'`, status open; `attachmentsForURL(pull/1008)` = 1 node (KS-1087, contributes).** `linear_read.out`, raw `linear/` |
| siblings (PR files API, 00:57:25) | 21 open PRs besides #1008. **#1006: 0 api-gateway files (disjoint). #1007: `services/api-gateway/src/routes/system-status.ts` + `__tests__/ks864a-dead-estate-helper.test.ts` + `__tests__/ks864b-dead-estate-portals.test.ts` — file-disjoint from #1008, but in the SAME api-gateway suite; #1007 has since MERGED (`0308b7a04`, 01:12:54 AEST), so the merged denominator moved (row above).** No other open PR touches `verification.ts`, the ks1087 test, originate `routes/documents.ts`, or either consumer file. #995 touches `api-gateway/src/utils/trustHeaders.ts`; #923 an api-gateway test; dependabot #649/#575 touch `services/api-gateway/package.json` + the Dev lockfile (GUARDED: the launcher refuses if one lands); 8 dependabot PRs touch the Dev lockfile. `gh_read.out` |
| the Secuura checkout (read only) | `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`: HEAD `355d82c8b` on `feature/ks-597-b-caller-scoped-externalref`, porcelain 0, `.git/config` sha256 `e0fa706f4bdae277`, **889 refs**, **110** `.git/worktrees` entries (00:55:40; `git worktree list` = 111 incl. main before and after the drafter's clone, `drafter_setup.out`). Quote all of these at start, mid and close. |
| toolchain | vitest **4.1.10**, typescript **5.9.3**, node **v24.7.0**, express **4.22.2** (from the checkout's `Blockchain/Dev/node_modules`), eslint **10.7.0**; `@secuura/shared` realpath IN TREE from `api-gateway/src` at both trees (`drafter_setup.out`). |
| the Ornith READY | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1087_ornith35b-q4_PASS-7of7_2026-09-15.diff.md` (run dir `local-model/runs/2026-09-15_ks1087-ornith35b-night6`). Its hunk header says `@@ -972` (the file moved 19 lines since). |

## 2. Spec / DoD — what this gate must establish

**KS-1087 (from `linear/KS-1087.json`)** — its Recommendation: (1) *"Report approval and delete the pending document only after originate returns 2xx. On any other status, or a network error, keep the pending document and return an error to the caller."* (2) forward a credential originate accepts — **NOT in this PR; the ticket stays open**. (3) regression cells for 401 and a network error. (4) KS-1083's vouch list. It also says: **"NOT established: whether any environment has workflow-gated document types."**

**The change, READ at `dd7086d5a` (`src/verification_head.ts`, `diff_develop_to_head.patch`).**
- **`:909`** `router.post('/api/workflow-instances/:id/approve', authenticateToken(true), mockBodyParser, async …)`. **`:916-923`** already `approved`/`completed` → 400 "Workflow already completed"; `rejected` → 400. **`:929-946`** role / user step authz → 403 (two different body shapes, pre-existing). **`:954-968`** a non-final step persists and answers 200 with no forward.
- **`:970-972` the final step sets `instance.status = 'approved'` and PERSISTS it (`setWorkflowInstance`) BEFORE the forward** (unchanged by this PR — it matters for item 3).
- **`:994-1012`**: `const forwardStatus: number = await new Promise<number>((resolveStatus) => { … })` wrapping the old `http.request`. `resolveStatus(proxyRes.statusCode || 0)` runs **in the response callback, i.e. on HEADERS** (`:1003`), not inside `proxyRes.on('end')` (`:1000-1002`); `proxyReq.on('error')` → `resolveStatus(0)` (`:1008`). **No timeout on the request** (`consumer_read.out` §7: the file has 8 `timeout` mentions, none on this `http.request`; READ `:995-1011`). No `'error'` listener on `proxyRes`.
- **`:1013-1016`**: `forwardStatus < 200 || >= 300` → `res.status(502).json({ success: false, error: { code: 'ORIGINATE_FORWARD_FAILED', message: 'Approved, but the document could not be created in originate; the pending document was kept', status: forwardStatus } })`. **`:1017`** the delete, only after the check.

**The seat reports (READY mail + PR body; measure every number):**
> - Red before green: READY test alone 2/3 red (`expected 200 not to be 200` ×2), control green; after the product hunk 3/3.
> - Tampers (verification.ts restored to its sha each row; AssertionErrors only): status check removed → 401 + unreachable red; delete moved before the check → 401 red by the NEW survival assertion only, unreachable by `uDeleteCount`; delete removed → control red by the NEW deletion assertion only; T0 / T0-after green.
> - api-gateway **44 files / 388** (baseline 43 / 385 at `93629700c`); shared **842/842**; `tsc -p` rc 0; eslint: test file clean, verification.ts 5 warnings = develop's.
> - Applied with `git apply --recount`; "the applied -/+ lines equal the READY's apart from one identical delete line git shows as context"; ragged indentation inside the new Promise wrapper kept as the READY's bytes; the READY's 401 cell never asserted survival (hoisted `deleteCount`); two `_`-prefixed dead locals.
> - NOT done: item 2; a live approve against a running originate; platform suites; preflight legs 3/4/8; **a type-check including the test file**.
> - Asks the gate to weigh: the route is absent from the published spec; `resolveStatus` fires on headers, not `end`.

### WHERE THE SEAT AND THE DRAFTER'S MEASUREMENTS DISAGREE, OR WHERE THE SEAT'S HARNESS CANNOT SEE (lead with these; each is a PREDICTION for you to re-measure)
1. **The kept document is STRANDED, and the seat's stub cannot see it.** The route persists the instance as `approved` (`:970-972`) before forwarding. With a **stateful** redis stub, drafter row `R-stateful-true` at head: approve with originate 401 → **502**, deletes 0, instance `approved`; originate then fixed (201), approve again → **400 "Workflow already completed", originate hits 0, deletes 0**; reject → **400 "Workflow already completed and cannot be rejected"** (`probe_rows_head.json`, `drafter_probe.out` 01:01:59). No route re-forwards the kept document. With the seat's **stateless** stub shape (`getWorkflowInstance` returns a fresh `pending_approval` object every call) the same retry reads **200 + 1 delete** (`R-stateful-false`) — so the ks1087 cells cannot observe this state. Downstream (READ, `strand_read.out` 01:02:21): `GET /api/documents/:id` keeps answering `status: 'pending_approval'` for that id (`:1291-1310`) and sign/sign-request/anchor/share answer **403 `PENDING_APPROVAL`** (`:370-392`, `:1387-1390`) until the Redis key expires (`setex … TTL.workflow * 24`, `redis.ts:600-606`; `TTL.workflow` value NOT read) or forever on the in-memory fallback. **And KS-1087 item 2 is open: originate answers 401 to this forward as the gateway sends it today (#951 r2 report)** — PREDICTION: wherever workflow-gated document types exist, EVERY final approval now answers 502 and strands. Rule it (item 3).
2. **The forward has no timeout: an originate that accepts and never answers means the approve never answers.** Drafter row `O-no-response` at head: **NO RESPONSE within the client's 2,500 ms**, originate hits 1, deletes 0, instance already `approved`. At base the same row answered **200 in 1 ms and deleted** (fire-and-forget). What bounds it in a deployment is nginx `proxy_read_timeout 120s` (`nginx.conf:128`) / `60s` (`nginx-demo.conf:329`) (`nginx_read.out` 01:06:40, READ) — PREDICTION: a 504 from nginx at 120 s / 60 s, then item 1's strand. Measure the in-process hang with a longer client wait and name what bounds it.
3. **The seat's tamper rows ran ONE file (ran=3), not the api-gateway suite** (`a8-ks1087/tamper-summary.txt`). The drafter re-ran them on the WHOLE suite (388 cells, `numPendingTests` 0 on every row): same reds (table in item 7).
4. **Including tsc — the seat did not run it; the drafter did: 5 new error lines, all in the new test file** (item 8).
5. **Seat claims that held (re-measure, don't re-litigate):** 43/385 → 44/388 and shared 44/842 (`drafter_suites.out` 01:00:33–39); the applied `-`/`+` lines equal the READY's after cancelling the one delete line removed-and-re-added (`parser_proof.out` 01:03:12, multisets and order EQUAL, one-byte control DIFFERS); eslint 5 warnings = 5 at base, 0 on the test file (`drafter_static.out` 01:05:00); Linear `contributes` only; spec 0 matches.

### The questions, each with its measurement. Name the tree beside every count. (W = Wednesday's; D = added by the drafter.)

**1 (W). EVERY OUTCOME OF THE FORWARD, ON THE REAL ROUTE IN-PROCESS.** Mount the real `createVerificationRoutes` on `127.0.0.1:0` with a **stateful** redis stub and an originate stub on `127.0.0.1:0` that counts hits. Drafter harness `qa1008-drafter-probe.test.ts` (recording, not pass/fail; `probe_rows_{base,head}.json`, drafter measured 01:01:45–59; rerun your own, with a 0-hit negative control):

| outcome at originate | base `93629700c` | head `dd7086d5a` | predicted-by |
|---|---|---|---|
| 200 / 201 / 204 | 200, delete 1 | **200, delete 1**, hits 1 | drafter (measured) |
| 302 | 200, delete 1 | **502 `status:302`, delete 0** | drafter (measured) |
| 400 / 401 / 403 / 404 / 409 / 422 | 200, delete 1 | **502 `status:<code>`, delete 0** | drafter (measured) |
| 500 / 503 | 200, delete 1 | **502, delete 0** | drafter (measured) |
| socket destroyed before headers | 200, delete 1 | **502 `status:0`, delete 0** | drafter (measured) |
| closed port `127.0.0.1:1` | 200, delete 1 | **502 `status:0`, delete 0** | drafter (measured) |
| accepts, never answers | 200 in 1 ms, delete 1 | **NO RESPONSE in 2.5 s, delete 0, instance `approved`** | drafter (measured) |
| 201 headers, socket destroyed mid-body | 200, delete 1 | **200, delete 1** (no unhandled error: rc 0, `success` true) | drafter (measured) |
| 201 headers, body never ends | 200, delete 1 | **200 in 2 ms, delete 1** | drafter (measured) |
| 401 headers, body never ends | 200, delete 1 | **502, delete 0** | drafter (measured) |

Name every outcome where the document is deleted without a COMPLETED 2xx (the drafter's: the two mid-body rows) and every outcome kept after a real success (drafter: none — but see item 3's strand and item 2's hang). Also measure what the seat's own tampers could not: a connection reset mid-body with an `'error'` on `proxyRes` and no listener (PREDICTION: no crash — Node's IncomingMessage emits `'error'` only when a listener exists; drafter row 201-then-destroy showed rc 0 and `success` true).

**2 (W). `resolveStatus` FIRES ON HEADERS, NOT `'end'`.** Measured above: a 2xx whose body errors or never ends → delete + 200. **Is that correct?** READ originate's `POST /api/documents` (`services/originate/src/routes/documents.ts`, blob `c3a818ac8`, `documentsRouter.use(authenticate())` at `:146`, handlers from `:344`): does it write its 2xx status only after the document is persisted (then headers = committed, and deleting is right), or can it flush headers first? Say which, with line numbers. Drafter tamper **G5 (resolve moved into `'end'`) leaves all 388 cells GREEN** — the suite cannot tell headers from end; name that as a coverage gap or nothing.

**3 (W). IDEMPOTENCY / RETRY — and the strand (disagreement 1).** Re-measure `R-stateful-true` and `R-stateful-false` on head AND base. At base (fire-and-forget) the drafter's first-call `originate_hits 0` is an instrument artefact: the response is sent before the forward lands (it lands during the next call). Answer: after a 502, does a second approve forward again? (Drafter: no — 400, hits 0.) Any duplicate side effect at originate? (Drafter: none from a retry, because there is no retry; but in the hang case, if originate eventually answers 2xx, the delete still happens after the client has gone — measure.) **Rule the stranded state with FEW HICCUPPS:** *Claims* (the 502 message "Approved, but … the pending document was kept" — true); *Purpose* (the ticket's item 1 — "keep the pending document and return an error to the caller" — met); *User expectations* (an `approved` instance whose document can never be created, signed, anchored or shared, and cannot be re-approved or rejected); *History* (base lost the document silently). Severity and target are yours — a finding against #1008, or a TICKET beside item 2 (retry path / persist `approved` only after a 2xx). Say which, and why.

**4 (W). AUTH AND OWNERSHIP UNCHANGED.** (a) By parser: the route's call arguments before the handler (`authenticateToken(true), mockBodyParser`) and the handler's statements `:910-968` byte-identical base vs head (AST leaf walk over the handler with the `:994-1017` span masked; a control edit inside the authz span must DIFFER). (b) At runtime (drafter measured, both trees): **real `authenticateToken`, no token → 401 `UNAUTHORIZED`, originate hits 0, deletes 0, instance unchanged**; role step wrong role → **403** (`{"error":"Not authorized to approve this step. Required role: issuer"}`), hits 0, deletes 0; user step wrong user → **403 `FORBIDDEN`**, hits 0, deletes 0. **Note: the ks1087 cells stub `authenticateToken` to a pass-through, so "the 401 cell" is ORIGINATE's 401, not the caller's** — name it so no reader confuses them.

**5 (W). THE ERROR BODY.** Drafter (measured): the 502 body is the fixed literal plus `status: <originate's status code | 0>`; it never contains originate's body (marker `ORIGINATE-SECRET-BODY-MARKER` absent in all 17 head rows), a path, or the originate port. READ: the literal at `:1014` has no `NODE_ENV` branch, so the body is the same in every env — measure it under at least `production` and `development` to prove the READ. **D: rule whether echoing originate's status integer (401 / 403 / 500 / 0) to the caller is disclosure** (upstream topology hint) — Polish, Record, or nothing. Drafter tamper G6 (a 502 body that also carries originate's body) leaves all 388 cells green: no cell reads the 502 body (READ: the 401 cell reads only `res.status`).

**6 (W). THE ORNITH-AUTHORED HUNK.**
- **Parser proof** (drafter measured 01:03:12, `parser_proof.cjs`/`.out`, TypeScript 5.9.3; `src/verification_head_reindented.ts`): **P1 head vs a re-indented copy (wrapper body shifted one level, `resolveStatus` to callback depth): transpile IDENTICAL, AST IDENTICAL 7041/7041, diags 0/0.** Controls, all as expected: C2 `resolveStatus` moved into the `'end'` listener → both DIFFER · **C3 type-only `: number` removed → transpile IDENTICAL, AST DIFFERS** (the transpile blind spot) · C4 the 502 `status` key removed → both DIFFER. The ragged lines (indent widths read): `:996-997` at 10 inside a call opened at 10, `:1003` at 14 where its siblings are 12, `:1005-1011` at 8 inside a wrapper opened at 8. **The indentation places `resolveStatus` visually beside the `'end'` listener; it is not inside it** — the READ trap a reviewer falls into, and the reason Wednesday's item 2 exists.
- **READY vs applied:** READY hunk −2 +10, applied −1 +9; the one line both removed and re-added by the READY is `await redisService.deletePendingDocument(documentId);`; after cancelling it, minus and plus multisets EQUAL and plus-in-order EQUAL; control (one trailing space) DIFFERS.
- **Promise wrapper leak paths (D):** the executor never rejects; it can only resolve or stay pending. Pending forever = item 2's hang (the awaiting handler and its socket are held). A synchronous throw inside the executor (e.g. `http.request` refusing an invalid `x-user-id` header value) would reject → the async handler rejects → Express 4 does not catch it → `unhandledRejection` (index.ts registers a handler at `:1182`). `createdBy` comes from the token's `userId` (`enforcement.ts:243-248`, READ). PREDICTION: parity with base (the same throw escapes the base handler), unreachable without a crafted `userId`; measure one row if the time-box allows, else NOT TESTED.

**7 (W). TAMPERS ON FINAL BYTES + GATE TAMPERS AIMED AT CONTROLS.** Text anchors (Python `str.count` = 1), markers asserted after, **WHOLE api-gateway suite per row** (~2.4 s), sha256-asserted restore (`git checkout -- <file>`; verification.ts head sha256 `98cbe16eccd8…`, ks1087 test `dfa4680c3f8f…` — re-derive from your clone), porcelain asserted before every row (the farm's symlinks baseline at 25 `??` lines). **Read `numFailedTests`, `numPendingTests`, `numFailedTestSuites`, `success` AND cells-run beside every colour.** A load failure is NOT a red; a skipped cell is NOT a pass. Note: vitest reports `numFailedTestSuites 2` for ONE failed cell here (the file and its describe both count) — do not read it as two files.

All rows: drafter (measured 01:03:41–01:04:10, `drafter_run.out`, `drafter_run_summary.json`, `vt_t_*.json`), head tree, 388 cells, pending 0 on every row.

| id | tamper (anchor count 1) | api-gateway (388) | predicted-by |
|---|---|---|---|
| T0 | — | 388/388 | drafter (measured) |
| **S1** (seat) | the `if (forwardStatus < 200 …) { 502 … return; }` block removed | 386: 401 cell + unreachable cell (`expected 200 not to be 200`) | seat (file only) / drafter (whole suite) |
| **S2** (seat) | the delete moved before the check | 386: 401 cell (`the pending document survives a refused forward: expected 1 to be +0`) + unreachable (`expected 1 to be +0`) | seat / drafter |
| **S3** (seat) | the delete removed | 387: control (`the pending document is deleted once originate accepts: expected +0 to be 1`) | seat / drafter |
| **G1** (CONTROL-aimed) | `>= 300` → `>= 500` (4xx counts as success) | 387: **401 cell only** | drafter (measured) |
| **G2** (CONTROL-aimed) | `resolveStatus(proxyRes.statusCode \|\| 0)` → `resolveStatus(0)` (every response a failure) | 387: **control only** (`expected 502 to be 200`) | drafter (measured) |
| **G3** | transport error `resolveStatus(0)` → `resolveStatus(201)` | 387: **unreachable cell only** | drafter (measured) |
| **G4** | `>= 300` → `>= 400` (3xx counts as success) | **388/388 — invisible** (no 3xx cell) | drafter (measured) |
| **G5** | `resolveStatus` moved into `'end'` | **388/388 — invisible** (item 2) | drafter (measured) |
| **G6** | 502 body gains `upstream: <originate body>` | **388/388 — invisible** (item 5; the drafter did not prove the tamper's runtime effect — the `'end'` may land after the 502 is written; build yours so it provably echoes) | drafter (measured, weak row) |
| G7 | `// qa inert comment` above the check | 388 | drafter (measured) |
| T0-after | — | 388 | drafter (measured) |

- **Red before green (seat: READY test alone 2/3 red on the untouched product):** re-run the ks1087 file on base `93629700c` (copied into your base tree) and name the tree. The drafter did not; its probe rows show base answering 200 + delete on 401 and on a transport error, which is what those two cells assert against.
- **G4 / G5 / G6 and disagreement 1 are coverage gaps of the new cells** (3xx, headers-vs-end, the 502 body, a stateful retry). Grade each as Polish / Record / nothing against #1008 — they are not regressions.

**8 (W). SUITES / TYPES / LINT.**

| check | tree | predicted | predicted-by |
|---|---|---|---|
| api-gateway `vitest run` (cwd `<tree>/Blockchain/Dev/services/api-gateway`) | base `93629700c` | **43 files / 385**, pending 0 | seat / drafter (measured 01:00:33, `vt_gw_suite_base.json`) |
| the same | head `dd7086d5a` | **44 / 388**, pending 0 | seat / drafter (measured 01:00:35) |
| the same | **merged** (head + local merge of develop `0308b7a04`) | **46 / 394**, pending 0; ks1087 file alone 3/3 | drafter (measured 01:14:02, `vt_gw_suite_merged.json`, `vt_ks1087_merged.json`) |
| the same | develop `0308b7a04` alone | PREDICTION **45 / 391** (merged minus the ks1087 file's 1 / 3) — NOT measured | drafter (arithmetic) |
| packages/shared `vitest run` | head | **44 / 842** | seat / drafter (measured 01:00:39) |
| `tsc --noEmit -p services/api-gateway` | both | rc 0 — **`exclude` has `src/__tests__`** (`consumer_read.out` §9): vacuous for the test file | seat / READ |
| **INCLUDING program** (`tsconfig.qa-including.json`: `extends ./tsconfig.json`, `include ["src/**/*.ts"]`, `exclude ["node_modules","dist"]` — the exclude MUST be overridden or it inherits `src/__tests__`; placed for the run, moved out by rename; `--listFilesOnly` proves inclusion) | base → head | **base 30 error lines in 10 files; head 35 in 11; 0 in verification.ts at either; ks1087 listed at head (44 `__tests__` files vs 43); 5 NEW, all in the ks1087 test:** `:65` TS18047 `'gateway' is possibly 'null'`, `:66` TS18047 `'originator'`, **`:119` TS6133 `'_deadPort' is declared but its value is never read`** (the `_` prefix quiets eslint, not `noUnusedLocals`), `:171`/`:172` TS18046 `'body' is of type 'unknown'` | drafter (measured 01:05:00, `drafter_static.out`, `tsc_including.out`) |
| positive control | head | planted `function qaPlant() { const QA_UNUSED_PLANT = 1; }` in the ks1087 test → including tsc +2 TS6133; eslint 2 `no-unused-vars` warnings; restore sha-identical | drafter (measured) |
| eslint (flat config `Blockchain/Dev/eslint.config.mjs`, cwd `Blockchain/Dev`, paths relative to it) | head / base | ks1087 test **0/0**; verification.ts **0 errors / 5 warnings** at both (head lines 594/998/1361/1437/1107 = base 594/997/1353/1429/1099 shifted) | seat / drafter (measured; first run used Dev-prefixed paths → "No files matching", kept as `drafter_static.first-run-eslint-path-wrong.out`) |

Grade the 5 including-tsc lines (the api-gateway test programs are not type-checked anywhere the drafter found — Polish or nothing; say whether any hides a real defect: TS18046 on `body.success` does not, the cell's runtime asserts it).

**9 (W). CONSUMERS AND SCHEMATHESIS.**
- **Callers (READ, `consumer_read.out` 00:58:31, `mount_read.out` 00:58:45):** whole-repo `git grep workflow-instances` at head = 9 lines: the route file (4), the ks1087 test (2), a ks815 test comment (1), **issuer `DocumentList.tsx:153` — `api.get('/workflow-instances')` only**, **mcp-server `api-client.ts:106` — GET `/api/workflow-instances/:id` only**. A second pattern (`instances/.*approve|approveWorkflow|workflowInstance.*approve`, case-insensitive) finds only the test and the route; control `workflows/.*approve` = 1 in verification.ts. **PREDICTION: no in-repo caller of `POST …/approve` exists, so none breaks on a 502 it never saw.** Name what this census cannot see (an out-of-repo client, a portal in another repo, string-built paths).
- **Reach:** `nginx.conf:184` and `nginx-demo.conf:410` both proxy `location /api/` to `api_gateway_pool` (`nginx_read.out`, control 39 / 45 `location` lines); the mount is unconditional (AST). So the route is reachable wherever the gateway is.
- **Spec:** `docs/openapi/secuura-api.yaml` (the only yaml under `docs/openapi`): `workflow-instances` = **0**, control `^paths:` = 1 (`consumer_read.out` §2). **SCHEMATHESIS — REQUIRED or not? Decide with evidence.** Drafter PREDICTION: **NOT REQUIRED** — Schemathesis generates from the published spec and cannot reach an unpublished route; the behaviour is covered in-process with a stubbed originate. Weigh "an undocumented 502 on a live authenticated route" and say whether the absence from the spec is itself a Record. Either way it stays **not run: measured reason** tonight.

**10 (W). LINEAR — re-read immediately before the mail.** `attachmentsForURL("https://github.com/Secuura/Distributed_Secuura/pull/1008")` and each node's `metadata.linkKind`: expected **exactly 1 node, KS-1087, `contributes`** (drafter 00:58:10). **Any `closes` on any ticket for #1008, or a closing phrase in the body or the commit message naming any ticket, is a Major** (a merge would walk KS-1087 to Done with item 2 open). Drafter: body closing phrases = `[]`; commit message (READ `git_read.out`) has "the ticket stays open for it", no closing verb before a KS id — re-run the regex on both. Merge prediction: KS-1087 stays In Progress.

**11 (W). MERGED TREE.** Merge the then-current develop into head in your own clone (never pushed); run the api-gateway suite on base `93629700c`, head and merged, naming each. Develop moved to `0308b7a04` (#1007) during drafting: drafter merged 46 / 394 (item 8). Also re-run the ks1087 probe outcomes on the merged tree if the time-box allows (#1007 touches only `system-status.ts` and its own tests, READ). The launcher judges a develop move by content (below).

**12 (D). THE MOUNT.** Re-prove with your own parser run that `createVerificationRoutes` is outside `if (ENABLE_MOCK_ENDPOINTS)` (`index.ts:841`) with the positive control on the `log('warn', 'Mock endpoints enabled…')` call at `:842` — a text read of `:828-845` suggests the opposite, and `index.ts:874-882`'s comment says the routers were moved out.

## 2a. LEGITIMATE SHAPES — the new status check IS a checker (required)

The check at `:1013` decides DELETE vs KEEP. Its failure path is destructive in one direction (a wrongly-classified success deletes nothing but strands; a wrongly-classified failure deletes a document originate never created). The ordinary shapes a real originate or network really produces:

| id | shape | expected verdict at head | the clause that yields it | predicted-by |
|---|---|---|---|---|
| L1 | originate 201 with a JSON body (the real create) | 200, delete once | `2xx` | drafter (measured: O-201) |
| L2 | originate 200 / 204 | 200, delete once | `2xx` | drafter (measured) |
| L3 | originate 401 — **today's real answer to this forward** (#951 r2) | 502, keep | `< 200 \|\| >= 300` | drafter (measured: O-401) |
| L4 | originate 400 / 409 / 422 (validation or duplicate `contentHash`) | 502, keep | same | drafter (measured) |
| L5 | originate 5xx / restarting (connection refused) | 502, keep | same + `'error'` → 0 | drafter (measured: O-500, O-503, O-closed-port) |
| L6 | an HTTPS originate URL (`originateUrl.startsWith('https')` → `require('https')`, `:979`) | same classification | same code path, different module | READ (NOT measured; loopback TLS is out of the time-box — say so) |
| L7 | originate slow but answering within nginx's 120 s | answer when originate answers | await | PREDICTION (not measured beyond 2.5 s) |
| L8 | originate never answering | **no answer from the route** (item 2 of disagreements) | no timeout | drafter (measured 2.5 s) — the checker's gap |

**A row that answers wrong for L1–L5 is a Blocker against #1008. L8 is a finding to grade, not a legitimate shape the check was meant to handle.**

## 3. Scope
- **Charter:** explore the approve route's new forward classification and delete decision with the REAL router on loopback, a stateful store, a counting originate stub, a parser, and aimed text-anchored tampers — including tampers aimed at the controls — looking for (a) any outcome that deletes without a completed 2xx or keeps after a real success, (b) a hang or leak the new await introduces, (c) an authz or ownership change, (d) disclosure in the 502, (e) a cell that cannot fail or a harness that cannot see a state, (f) ticket linkage, callers and spec.
- **In scope:** the 2 files; the approve and reject routes and their consumers (read + probe); originate's `POST /api/documents` (read only); the api-gateway suite on base / head / merged; including tsc / eslint; Linear; the caller + spec census.
- **Out of scope / do NOT touch:** any stack, container, demo or kintsugi box; item 2 (the forward credential); `GATEWAY_VOUCH_SECRET`; fixing anything; #1006 / #1007 and their gates; Seat A's worktree.

## 4. Credentials (POINTER ONLY — never values)
None are needed for the measurements. For read-only API calls, `GH_TOKEN` and `LINEAR_API_KEY` by NAME from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` (the provenance of this set's `gh_read.py` / `linear_read.py`). `AGENTMAIL_API_KEY` by NAME from `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env` for the verdict mail. The real `authenticateToken` runs against the throwaway RS256 keypair `vitest.setup.ts` generates in-process; never read a real key. No wallet.

## 5. State-mutation & cleanup
- Nothing outside your scratch and the report directory. Create no container.
- Quarantine scratch tests and scratch configs by rename; never `rm`. Fresh `mktemp -d` per attempt.
- **node_modules farm (measured, `drafter_setup.py`/`.out` 01:00:06–14):** build `Blockchain/Dev/node_modules` per ENTRY from the checkout (987 entries, `.vite` skipped) with `@secuura/` relinked INTO each tree; **per-ENTRY farms for `services/api-gateway/node_modules` (8 entries) and `packages/shared/node_modules`, skipping `.vite`** — the checkout has a `.vite` cache dir in `api-gateway/node_modules`, and a directory symlink would let vitest write into the checkout. Other packages' node_modules (24) may be directory symlinks. Build the shared dist in each tree (`tsc -p .`, rc 0, 1–3 s) and assert `realpath(require.resolve('@secuura/shared'))` from `api-gateway/src` is IN TREE.
- **Porcelain:** the farm's symlinks show as 25 `??` lines per tree. Baseline them; assert nothing else appears.

## 6. Output boundary
Report directory (you create it): `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1087-1008-dd7086d5a-tier1-r1/`. It holds:
- `report.md`
- `evidence/`: your gate test file(s) and the outcome rows per tree (with hit counts and the 0-hit control), the retry/strand rows (stateful and stateless), the authz rows, the parser proofs (indentation, authz span, mount), the suite JSON per tree and per tamper row (with `numPendingTests` / `numFailedTestSuites`), `tsc_including.out` with `--listFilesOnly`, the eslint JSON, the Linear re-read, the caller + spec census with controls, `docker_info.rc`.
- `NOT-TESTED.written-first.md`, written BEFORE any run. It lists:
  - a live approve against a running originate, and KS-1087 item 2 (the forward credential);
  - whether any environment has workflow-gated document types (the ticket's own "NOT established");
  - an HTTPS originate (L6); a real Redis (TTL expiry of a stranded pending document; `TTL.workflow`'s value);
  - nginx's 120 s / 60 s bound on the hang (READ, not measured);
  - out-of-repo callers of the route;
  - a real browser (no rendered surface) and any portal;
  - the four platform suites by path — `systemTest/schemathesis` (not run: measured reason; REQUIRED-or-not ruled in item 9) · `systemTest/akto` · `systemTest/playwright` · `systemTest/performance` (NOT COMMISSIONED, 40% cap, stack HOLD);
  - preflight legs 3/4/8 (the seat's SKIPPED legs, not a pass).

Every finding carries its evidence class (MEASURED AT RUNTIME / PROBED / READ ONLY / RELAYED), its severity, its target (the PR or a TICKET), and SHIPS-WITH or TICKET. Every "is this a bug?" call names its FEW HICCUPPS oracle.

## 7. Known-fragile / known-changed
- **A stateless store stub hides the strand** (disagreement 1): use a stateful one for every retry question.
- **`numFailedTestSuites` double-counts** (file + describe) in this suite: read `numFailedTests` and cells-run.
- **`tsc -p services/api-gateway` type-checks 0 `__tests__` files**: the including program must override `exclude`, and `--listFilesOnly` must list ks1087.
- **The indentation lies about scope** at `:1003` (item 6): read by parser, not by eye.
- **At base the forward is fire-and-forget**: a hit counter read immediately after the response undercounts (the drafter's base `R-stateful-true` first-call `originate_hits 0`). Wait for the hit before reading it.
- **The seat's unreachable cell builds a `deadApp` + `deadServer` that nothing calls** (`:87-120`) before the app it actually uses (`:121-160`; line numbers by `grep -n`): dead scaffolding — Polish or nothing.
- Census instruments: pair every count with a positive control from the same file; `/usr/bin/grep -i`; `git grep -c` prints nothing for a 0 (the drafter's own `verify-document` control in `blob_dump.out` printed nothing — treat silence as unread, not as 0).
- vitest 4.1.10: `vitest run <file> --reporter=json --outputFile=<path>`, SOLO, never watch. Whole api-gateway suite ~2.4 s. A hanging-originate cell needs `server.closeAllConnections()` before `close()`, and a per-test timeout above your client wait.
- `/bin/bash` here is 3.2: write runners in Python. zsh: no `PIPESTATUS` (`cmd > out 2>&1; rc=$?`), no `timeout`; never start a command line with `=====` (zsh expands `=word`).
- **Recent changes — do NOT flag as new:** #1005/KS-1073 (verification.ts's verify predicate, the `de34b2de7` base), #1004/KS-932 (packages/shared ssrf), KS-815 (the verification router guards its own body), KS-1083/KS-1084 (the vouch list, related), the two 403 body shapes at `:938` / `:943`, `let body` unused at `:998` (eslint warning at base too).
- **Known open gaps:** KS-1087 item 2; the ticket's "NOT established" reachability.

## 8. Logistics / BOUNDS
- **Session time-box:** 45 minutes of work (§HOLDS).
- **Read verbs only in the checkout.** Quote at start, mid and close: the checkout's porcelain count, `.git/config` sha256, `for-each-ref | wc -l`, the `.git/worktrees` count, origin develop, `refs/pull/1008/head` and the branch.
- **The head is a MOVING reading** while Seat A is live: THREE timestamped readings (start / mid / end), each with the branch name beside its SHA. **If `refs/pull/1008/head` moves, STOP: this brief is about `HEAD-SHA-REMOVED`.** develop moving is expected.
- **The launcher's develop arm.** At the CURRENT develop it judges ELEVEN files by blob: verification.ts (base `de34b2de7`; the PR's `d0585dc34` → exit 19 LANDED), api-gateway `src/index.ts` `6f38c819e` / `src/middleware/auth.ts` `20311010d` / `src/services/redis.ts` `47659ee9c` / `src/services/enforcement.ts` `533cd309c` / `package.json` `841d8c6ad` / `vitest.config.ts` `5888e0b32` / `vitest.setup.ts` `22c110768` / `tsconfig.json` `c981e6a92`, originate `src/routes/documents.ts` `c3a818ac8`, Dev `eslint.config.mjs` `8c5374c60`. If develop moved past `93629700c`, it REFUSES (exit 18) when the delta touches a GUARDED path: those files, the ks1087 test, `docs/openapi/`, the Dev lockfile, issuer `DocumentList.tsx`, mcp-server `api-client.ts`. A move elsewhere proceeds: merge it in your clone and re-derive every count, above all the api-gateway denominator. **Its `--check` at 01:12:58 ALREADY read "origin develop MOVED 93629700c -> 0308b7a04: commits=1 files=3 — disjoint from the GUARDED list" (#1007's squash).**
- **Escalation:** none mid-run (you have no inbox). Anything the brief does not answer → record your interpretation in the report and in the verdict mail.

## VERDICT DESTINATION
ONE mail to `wednesday-agent@agentmail.to`, subject EXACTLY:
`[QA -> Wednesday] TIER 1 GATE #1008 (KS-1087) dd7086d5a — <VERDICT>`

`<VERDICT>` is GO / GO WITH FINDINGS / NO GO on `HEAD-SHA-REMOVED`, as the delta over base `93629700c` (the merge-base) AND on the merged tree with develop `0308b7a04` (or the then-current develop — name both). Say plainly:
1. **Every forward outcome** (item 1) per tree with hits and deletes; any delete without a completed 2xx; any keep after a real success.
2. **Headers vs `end`** (item 2): originate's commit-before-status reading and your ruling.
3. **Retry and the strand** (item 3): stateful vs stateless rows; severity; PR or TICKET.
4. **Auth** (item 4): the parser proof and the 401 / 403 rows with hits 0.
5. **The 502 body** (item 5) per NODE_ENV; the status-integer ruling.
6. **The Ornith hunk** (item 6): indentation proof with controls; READY equality; wrapper leak paths.
7. **Tampers** (item 7): every row with cells-run and pending; the three invisible rows.
8. **Suites / including tsc / eslint** (item 8) per tree; **callers, reach, Schemathesis REQUIRED-or-not** (item 9); **Linear** (item 10); the mount (item 12); what was NOT tested (`docker info` rc on its own line).

Give the merge seat its ADDENDUM: "squash `dd7086d5a` onto develop `0308b7a04` (or the then-current develop; file-disjoint from #1007's squash and from #1006 by the PR files API; dependabot #649/#575 touch api-gateway package.json); #1008 attaches to KS-1087 only, linkKind contributes — KS-1087 stays In Progress for item 2; equality targets after the squash: verification.ts `d0585dc34` / ks1087 test `7832724f3`; api-gateway 45/391 → 46/394 (develop count: re-measure), packages/shared 44/842 unchanged; Records: <yours>". Add any test-quality finding (the stateless stub, the invisible G4/G5/G6 rows, the 5 including-tsc lines, the dead `deadApp` scaffolding) and the strand / hang rulings with their targets.

**Mechanism note.** The QA project has no `send_brief.sh` of its own. The verdict mails that have reached Wednesday were sent from `coagent@agentmail.to` through the AgentMail API:
- `POST https://api.agentmail.to/v0/inboxes/coagent@agentmail.to/messages/send`
- JSON body `{"to": ["wednesday-agent@agentmail.to"], "subject": "...", "text": "..."}`
- header `Authorization: Bearer $AGENTMAIL_API_KEY`, with the key by NAME from `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env`, read by your script and never echoed

Use whichever path exists. The MAIL is the end state either way: confirm the API answered 2xx and quote the message id. The body = the report's BLUF + the eight plain statements + the ADDENDUM + the NOT-TESTED block + the report path. Timestamps in the mail come from `date`, never estimated.

## NOT COMMISSIONED (say so if asked)
Akto / Playwright / k6 (40% cap, stack HOLD); Schemathesis beyond the REQUIRED-or-not ruling; any deployed environment, the demo box or kintsugi; a real originate; KS-1087 item 2; a real browser; #1006 / #1007 and their gates; the ack boxes; any fix (a forward timeout, persisting `approved` only after a 2xx, a retry path, dropping `status` from the 502 body, the including-tsc lines, the dead scaffolding: the owner's).

## PROVENANCE
All files are in `2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1008/`:
- **The seat's mail:** `mail_1008_ready.md` (2026-09-16T14:53:04Z), saved verbatim by Wednesday, spf/dkim/dmarc pass; Wednesday's receipt `answer_1008_receipt.md`. The PR body: `gh/pr1008_body.md`. The seat's records (read only): `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-16_seatA/a8-ks1087/` (`tamper-summary.txt`, `applied-product.diff`, `gw-suite.out`).
- **git and API reads:**
  - `git_read.sh`/`.out` (00:55:40) — heads (incl. #1006 `86fe59e6b` / #1007 `b28ed490a`), parent, rev-list, numstat/raw, commit message, checkout state
  - `blob_dump.sh`/`.out` (00:55:56) — `src/verification_{develop,head}.ts`, `src/ks1087_head.test.ts`, `diff_develop_to_head.patch`, `diff_U0_verification.patch`
  - `derive_gh_read.py` → `gh_read.py`/`.out` (00:57:25; raw in `gh/`); `derive_linear_read.py` → `linear_read.py`/`.out` (00:58:10; raw in `linear/`)
  - `consumer_read.sh`/`.out` (00:58:31), `mount_read.out` (00:58:45), `mount_cond_read.out` (00:58:54), `mount_ast.cjs`/`.out` (00:59:22; first run without a positive control kept as `mount_ast.first-run-no-positive-control.out`), `mock_env_read.out` (00:59:09), `strand_read.out` (01:02:21), `nginx_read.out` (01:06:40), `blobs_read.out` (01:05:47), `src/gateway_index_head.ts`
- **Drafter probes, run in a `--shared` scratch clone** (`scratchpad/gate1008_draft_y2qsfb0y/`; worktrees base `93629700c` / head `dd7086d5a`; source checkout worktree count 111 before and after):
  - `derive_setup.py` → `drafter_setup.py`/`.out` (01:00:06–14), `drafter_paths.json`, `drafterlib.py`
  - `drafter_suites.py`/`.out` + `vt_gw_suite_{base,head}.json`, `vt_shared_suite_head.json` (01:00:30–39)
  - `qa1008-drafter-probe.test.ts` + `drafter_probe.py`/`.out` + `probe_rows_{base,head}.json` (01:01:45–59; the probe file was moved out of each tree to `_quarantine_probe_*` in the clone workdir)
  - `parser_proof.cjs`/`.out` (01:03:12) + `src/verification_head_reindented.ts`
  - `drafter_run.py`/`.out` + `drafter_run_summary.json` + `vt_t_*.json` (01:03–01:04:10)
  - `drafter_static.py`/`.out` + `tsc_including.out` (01:05:00–11; first run `drafter_static.first-run-eslint-path-wrong.out`)
- **Tier rule:** `0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`. **The gate that found the defect:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1041-951-02a22f4bb-tier1-r2/`.
- **develop moved during drafting:** `develop_move_read.sh`/`.out` (01:13:23, ls-remote + GitHub API GET only) and `drafter_merged.py`/`.out` + `vt_gw_suite_merged.json` / `vt_ks1087_merged.json` (01:13:53–01:14:03; worktree `wt_merged` in the same clone).
- **Launcher:** `launchers/launch_qa_secuura_ks1087_1008.sh`, generated by `gen_launcher_1008.py` from `launch_qa_secuura_ks844_1006.sh` (20 asserted substitutions + residual guard + 61 output controls + bash -n; `gen_launcher.enumerate-to-scratch.out` enumerated `#1008` = 9 to scratch first and the real write took that measured count; `gen_launcher.out` 01:12:51). `--check` via `check_launcher.sh` in `check.out` (the LAST run on the final bytes of brief + prompt; its time and `launcher --check rc=` on its own last line); the first run, before the develop-move edit, kept as `check.first-run-before-develop-move-edit.out` (01:12:58, rc 0). Negative controls, `--check` only, in `controls_check.out`.
