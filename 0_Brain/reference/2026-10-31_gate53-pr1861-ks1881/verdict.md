# QA GATE 53: Secuura/Blockchain PR #1861 (KS-1881, Seat S 9th), Tier 1, Round 1
**Head gated: d11d65e7996eabb4d183a6cec8eb11aad174c0b9.** `ls-remote` at gate start: `refs/pull/1861/head` = d11d65e7 (unchanged from S's READY mail), develop = ddc644fb4869. Head is the merge of develop dc8c210cb29d into fix commit d0f2ed87f0ab; merge-base with develop is dc8c210cb29d. develop's one newer commit (#1860) touches no transfer or shared file (`git diff --stat head..origin/develop -- services/transfer packages/shared` shows only this PR's own lines), and `git merge-tree --write-tree` against ddc644 is clean (rc 0, tree b7184981).

## VERDICT: GO WITH NOTES. No finding needs fixing before merge. F1 is a test gap worth one cell; F5 is a docs wording fix that can ride the merge-prep fragment conversion.

| File | Change | Gated |
|---|---|---|
| services/transfer/src/routes/workflows.ts | +9 -1: `import { isPlatformRole } from '@secuura/shared'`; first statement of POST /escalate is `if (!isPlatformRole((req as any).user?.role)) return 403` | yes |
| transfer/src/__tests__/ks1881-workflows-escalate-requires-a-platform-admin.test.ts | new, **13 cells** (10 refuse, 3 admit) | yes |
| Projects Documents/*.html (Flow Diagrams 130, Cheat Sheet entry) | +10 / +16 | noted only (converts to a fragment at merge prep; F5) |

Nothing else is in the diff: no lockfile, manifest, shared helper, baseline or hook (`git diff --name-status` merge-base..head = 4 files). **Q5 scope: clean.**

**(1) Role check over HTTP** (instrument: `probes/g53-escalate-shapes.test.ts`, the real `workflowRoutes` mounted in an express app on 127.0.0.1, `approvalWorkflowService` replaced by a Proxy that records every property read; oracle written separately with char codes, ASCII a-z fold only, `typeof === 'string'` only, self-checked).
- Same predicate as gate 47: the shared `isPlatformRole` (packages/shared/src/security/keyRevokePolicy.ts, `PLATFORM_ROLES`), not a new list. Shared is untouched by this PR.
- Head: **76/76 assertions pass**, 75 rows recorded (`rows_head.json`).
  - Admitted (200, sweep called once): exactly the ASCII case variants of SYSTEM_ADMIN / SUPER_ADMIN (6 rows).
  - Refused 403, body exactly `{"success":false,"error":{"code":"FORBIDDEN","message":"Admin role required"}}`, sweep never called, **zero reads of the service object** (65 rows): lead/trail space, tab, LF, NUL, ZWSP, BOM, hyphen, no separator, PLATFORM_ADMIN, ADMIN, admin, OWNER/owner, ORG_ADMIN/org_admin, ISSUER_ADMIN, VERIFIER, SYSTEM, SERVICE, empty, space; long-s (both), dotless ı, dotted İ, fullwidth, Cyrillic Е, Greek Α, combining acute, precomposed Ń; `__proto__`, `constructor`, `hasOwnProperty`, `toString`, `valueOf`; arrays (flat, nested, two-element), null, undefined, 0, 1, NaN, true, false, `{}`, toString object, toPrimitive object, String object, Symbol, function, BigInt, Set, nested `{role}`; req.user absent, a string, null, an array, a number, `{}`, `{roles:[…]}` only, `{Role:…}` (capital R), a null-prototype OWNER; and OWNER sending a body that claims `role: SYSTEM_ADMIN` / `all: true`.
  - Recorded, not failed: `role` inherited via prototype and a null-prototype SYSTEM_ADMIN are admitted (both are a genuine SYSTEM_ADMIN value; JWT claims decode as own properties, `middleware/index.ts:110/121` sets `req.user = decoded`). Same as gate 47.
  - A `role` getter that throws: the async handler rejects, the request never answers (3 s client timeout), sweep not called. Fails closed but see F3.
- **Positive control:** the same probe against the base product file (dc8c210 `workflows.ts` swapped in, sha256 restored, `head_sha256.txt`): **66 of 76 fail; 74 of 75 rows admitted with the sweep called**, including OWNER, no role, no req.user, arrays, symbols. The only non-200 at base is the malformed-JSON row (parser 400). So the probe sees the old open door.

**(2) Placement and leakage** (instrument: read of the handler + the Proxy read-recorder above + mutant M15).
- The guard is the handler's first statement; nothing in the handler runs before it. The Proxy recorded zero property reads of `approvalWorkflowService` on every refused row, so no service or DB call precedes the decision. The handler reads no body.
- Mutant M15 (sweep moved above the guard) is killed by S's tests and by mine.
- App-level middleware still runs first in index.ts (helmet, cors, `express.json()`, `rejectNulBytes`, requestLogger, `jwtAuthenticate` on `/api`). That is pre-existing and route-independent: a non-admin sending malformed JSON gets the parser's 400, not 403 (probe row "OWNER malformed JSON"; in the real app the shared `errorHandler` shapes it). Not a regression, no sweep.
- Refusal body is a constant; nothing from the request or principal is echoed. Headers on refusal: content-type, length 78, a fixed weak etag, `x-powered-by` (pre-existing express default; helmet removes it in the real app).

**(3) Other doors** (instrument: `git grep` over the whole head tree, html excluded, for `processEscalations`, `workflows/escalate`, `workflowRoutes`, `dbInsertStepInstance`, `svc_approval_step_instances`, case-insensitive `escalat`; plus the gateway, nginx/Caddy configs, compose ports and `.github`).
- `processEscalations` has **exactly one caller**: `routes/workflows.ts:223`, now behind the guard. Defined at `approvalWorkflowService.ts:591`. No scheduler, `setInterval`, cron, queue/message handler or script calls it; transfer `index.ts` has no timer.
- The table it writes (`svc_approval_step_instances`) is written only via `dbInsertStepInstance` (`approvalWorkflowService.ts:298`), whose callers are :444/:509 (workflow start and `processApproval`, not the escalation sweep) and :619/:624 (inside the sweep).
- `workflowRoutes` is mounted once (`index.ts:446`, behind `jwtAuthenticate` at :442). `transfer.test.ts:232` mocks it.
- Other "escalate" hits are different actions: the api-gateway admin verification-queue mock (`routes/admin.ts:1066-1075`, sets a mock item's status) and the admin UI's action type (`frontend/admin/src/services/api.ts:481`). Neither reaches the transfer sweep.
- Reach: the api-gateway proxies only `/api/transfers` and `/api/delegations` to transfer (`proxy.ts:1106/1113`) and serves its own `GET/POST /api/workflows` and `GET/DELETE /api/workflows/:id` from Redis (`proxy.ts:1124-1149`); nginx/Caddy configs contain no transfer route; compose publishes no transfer port (`ports: !reset []`, "Pen-test F-04"). So POST /api/workflows/escalate is reachable only service-to-service on the internal network.
- **No unguarded second door found.**

**(4) Tests and mutants**
- Red-first (Spark deterministic run, `probes/spark/facts.json`): base product 3 pass / **10 fail**, head **13/13**. Matches S (10 of 13; S measured at cb2320368, same product file).
- Transfer suite at head, `--maxWorkers=2`, alone: **8 files / 105/105**. Matches S.
- `tsc -p services/transfer --noEmit`: 0 errors; positive control (an injected TS2322) caught, 2 errors (`tsc_head.log`, `tsc_pc.log`).
- Mutants (`probes/mut1861/run_mutants.py`, unique anchors asserted, sha256 4fa46352… restored after the run): 16 mutants of the guard.
  - **S's 13 cells kill 15 of 16**: guard removed, truthy role, negated, `String()` coercion, exact-case list, full-Unicode `toUpperCase`, SYSTEM_ADMIN only, +OWNER, +ORG_ADMIN, array first element, dropped `return`, 401, changed message, sweep before guard, missing user admitted.
  - **Survivor: M11, `trim()` before the check** (F1).
  - My probe kills **16 of 16** (`mut_g53_probe.json`; run with the throwing-getter row removed, since its unhandled rejection makes vitest rc 1 on its own).

## FINDINGS
- **F1 Note (fix before merge: n; one cell recommended). Whitespace is not pinned.** Mutant M11 (`isPlatformRole(role.trim())`) passes all 13 of S's cells: no cell sends `' SYSTEM_ADMIN'` or `'SYSTEM_ADMIN\n'`. The helper itself refuses them today (my probe, 5 rows), so behaviour is right; the regression net is not. Instrument: mutant run.
- **F2 Note (n). S's "6 of 6 mutants" is consistent but narrower** than this gate's 16; S's six all appear in my set and are killed. Nothing to correct.
- **F3 Info, pre-existing class (n). Async handler with no try/catch on Express 4.** If reading `req.user.role` threw, the promise rejects unhandled: the request hangs and, with no `unhandledRejection` handler in transfer `index.ts`, Node's default would terminate the service. Unreachable from a decoded JWT (plain JSON object), and every other async handler in this router has the same shape (e.g. :64, :87, :145, :193), so not attributable to this PR. Instrument: probe row "user role getter throws" + grep of index.ts.
- **F4 Info (n). Platform-admin definitions still differ across components** (gate 47 F5: auth counts `admin`/`super_admin`; `isPlatformRole` refuses `admin`). This route at base admitted everyone, so nobody legitimate loses access except non-platform roles; consistent with KS-1845 / gate 47.
- **F5 Note (n; fix wording at fragment conversion). Docs and ticket comment overstate the gateway.** "the gateway serves `/api/workflows/*` itself" is not accurate: the gateway serves four exact/`:id` paths and simply has no route for POST /api/workflows/escalate; the reason no edge caller exists is that transfer is not proxied for `/api/workflows` and publishes no port. The conclusion (nothing in the repo calls it) stands. Docs still in hand-numbered form ("130."); converts at merge prep per S's mail.
- **F6 Info (n). Ticket's "check whether anything scheduled calls this route with a non-platform token":** in-repo answer is none (no scheduler, CI workflow or script references `/escalate`). An out-of-repo caller (e.g. an Azure job hitting the service directly) remains unmeasured, as S says. If one exists and uses a non-platform token, it will now get 403 and overdue steps will stop escalating silently.

**UNMEASURED:** a real JWT through `jwtAuthenticate` (stand-in middleware sets req.user); a running stack, the database, the real sweep; any out-of-repo scheduler or Azure job calling the service; the four platform suites (Akto, Schemathesis, Playwright, k6); eslint (S claims clean); the pre-push hook legs S reports; html docs content beyond the diff read; deploy.

## HOW
- Clone: `git clone --no-checkout` (local) from gate 47's clone into the non-existent `repo/`, `rev-parse --show-toplevel` asserted equal before any fetch; remote set to Secuura/Distributed_Secuura with the Blockchain deploy key as `core.sshCommand`, push URL `no_push_qa_gate`. Fetched `refs/pull/1861/head` and develop, detached checkout of d11d65e7.
- Setup: `npm ci --ignore-scripts` in Blockchain/Dev from the head locks (1795 packages), build of @secuura/shared only.
- vitest via `npx --prefix <transfer> vitest run --root <transfer> --maxWorkers=2`, one suite at a time.
- Probes copied into `src/__tests__` only for their runs, then moved to `probes/_quarantine/`; base swap and mutants restored with sha256 asserted; `git status` clean afterwards. Clone removed after the gate.
- No git write verb in /Volumes/DevMASTER/!CODING/**. PR body could not be read (gh in the Blockchain config dir is not logged in); S's READY mail stood in for it. Linear read only. Every process I started has exited.
- Instrument faults: the hook refused `git -C $R` variable forms, re-run with literal paths; the throwing-getter row made the probe's vitest rc 1 despite 76/76 passes, so the mutant run used a copy without that row.

## Spark shadow (`spark_gate.sh` with `--node-modules`, work dir in the session scratchpad; `spark_review.py` with S's mail as the PR body; copies in `probes/spark/`)

| Item | Spark | Me |
|---|---|---|
| Red-first base / head | 10 fail / 13 pass | same (from its facts) |
| Verdict | GO WITH NOTES | GO WITH NOTES |
| Findings | 8 Notes, all "claim unmeasured in facts" (suite, tsc, eslint, mutants, hook legs, docs check, out-of-repo scheduler) | 6 (2 Note, 1 docs Note, 3 Info) |
| Suite / tsc / mutants | flagged unmeasured | measured: 105/105, 0 errors (+control), 15/16 by S's cells |
| Role-shape matrix + base control | not run | 75 rows, base admits 74 |
| Second-door enumeration | not done | one caller, none unguarded |
| Whitespace mutant gap (F1) | missed | found |
| Async-throw / hang (F3) | missed | found (Info) |
| Gateway wording (F5) | missed | found |
| Ticket fetch | worked this time (gates 46/47 had IndexError) | read directly |
| Reliability | attempt 1 repetition-abort + invalid JSON; attempt 2 valid | n/a |

Spark's deterministic half agrees exactly; its review is safe (no false Major) but adds no security signal beyond "not in facts".
