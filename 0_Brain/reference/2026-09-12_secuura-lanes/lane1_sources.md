# Lane 1 sources: originate route input guards (KS-1029, then KS-1103)

Gathered 2026-09-12 by a read-only research agent working for Wednesday.
- **Code:** read with `git show` / `ls-tree` / `log` / `grep` at develop `4554b25e21dfd01113bf40e8f6d34573345a5f37` (`4554b25e2`).
  - `git ls-remote origin refs/heads/develop` still returns that SHA.
  - Tip commit: "KS-1094: mask credential values in the k6 runner's echoed docker command (#958)", 2026-09-12T05:10:50+10:00.
- **Linear:** GraphQL `issue(id:)` for KS-1029, KS-1103 and KS-730, with `comments(first:50)` sorted by createdAt.
- **GitHub:** REST `GET /repos/Secuura/Distributed_Secuura/pulls?state=open` (paged; 49 open, all on base develop), then `GET /pulls/{n}/files` for every PR.
- Nothing was fetched, checked out, written or commented on.
- Path prefix used below: `O = Blockchain/Dev/services/originate`.

---

## BLUF

- **KS-1029 is still real at `4554b25e2`.**
  - `PATCH /dsr/:dsrId` (`O/src/routes/gdpr.ts:348-365`) never checks `dsrId`'s shape.
  - `gdpr.updateDSRStatus` casts it with `${dsrId}::uuid` (`O/src/services/gdprService.ts:342`) and, since KS-754 (#914, merged `0c8623e5b`), rethrows on any DB error (`:345-364`).
  - So `dsrId=0` or `not-a-uuid` goes 22P02 → rethrow → route catch → **500** (`gdpr.ts:362-363`).
  - `UUID_PATTERN` is defined at `gdpr.ts:39` and used at `:201` and `:296`, but not on this route.
- **KS-1103 is still real at `4554b25e2`.**
  - The `/verify` validator checks `body('hash')` (`O/src/routes/verification.ts:704`).
  - The handler destructures only `documentId, providedHash, documentData, contentHash, documentHash` (`:727`) and sets `hashToVerify = providedHash || contentHash || documentHash` (`:731`).
  - So a body with only `hash` gets the 400 at `:733-737`.
  - The published spec lists `hash` in `VerifyRequest` (`O/src/originate.openapi.ts:536`; `Blockchain/Dev/docs/openapi/secuura-api.yaml:6358`).
  - An existing test comment admits the gap: `ks563-certified-vs-anchored.test.ts:101`, "The route reads `providedHash | contentHash | documentHash` — not `hash`."
- **Neither ticket is fixed or claimed.**
  - Both are in Backlog. KS-1029 has no assignee; KS-1103 is assigned to kamil.kreiser@secuura.ai.
  - No open PR changes `routes/gdpr.ts` or `routes/verification.ts`.
  - No open PR names KS-1029, KS-1103 or KS-730 in its title, body or head ref.
  - No remote head names either ticket. The one `ls-remote` hit for "1029" was a SHA substring on `seat-b/ks-860-loopback-listen-guard`.
- **Files a fix would touch:**
  - `O/src/routes/gdpr.ts`: the PATCH handler only.
  - `O/src/routes/verification.ts`: the `/verify` handler at `:711-737`.
  - New `O/src/__tests__/ks1029-*.test.ts` and `ks1103-*.test.ts`.
  - No spec change is needed for KS-1103 (`hash` is already published).
  - KS-1029 needs no new status code: the PATCH spec already declares 400 and 404 (`originate.openapi.ts:3269,3272`).
- **Collisions:**
  - **No open PR touches either file.**
  - Open PRs touch nearby originate files:
    - #939 and #919: `routes/documents.ts`
    - #799: `routes/adminConfig.ts`, `middleware/auth.ts`
    - #912: `services/anchorStateSync.ts`
    - #919 and #813: `originate.openapi.ts`
    - #922, #919, #813 and #805: `secuura-api.yaml`
  - **#931 rewrites the `@secuura/shared` jest mock** in `ks563-certified-vs-anchored.test.ts` and `ks584-verify-row-selection.test.ts`, the two verify-route suites a KS-1103 test would copy.
    - A new ks1103 test that copies their hand-written mock will need `makeSharedMock` once #931 lands.
  - KS-730 (Backlog, not claimed) plans to edit the 15 `err.message` sites in `gdpr.ts`, including `:363` inside the PATCH handler. Do not run it at the same time as this lane.
- **Blast radius:**
  - **PATCH `/dsr/:dsrId`:** no frontend, SDK or service in the repo calls it. Only docs, the `/api` index at `O/src/index.ts:152`, and the KS-444 unit test mention it.
  - **`/verify` + `hash`:** every connector and frontend sends `contentHash` or `documentId`, except **`mobile/secuura-app/src/services/api.ts:158`, which sends `{ hash }` and so gets the 400 today**. Honouring `hash` fixes that client and changes no other caller.

---

## 1. The lanes file (Wednesday's plan)

Source: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-09-12_secuura-lanes/secuura_lanes.md`

- **Header** (`:3-8`): generated 2026-09-12 04:15Z against `4554b25e2`; 379 Linear issues; 48 open PRs on develop.
  - My live count at gather time was 49 open PRs (kksecura 38, dependabot 10, PeterObeden 1). One kksecura PR opened after the lanes file.
- **Rules shared by all lanes** (`:39-47`):
  - Branch from `4554b25e2` in a worktree.
  - Do not edit or regenerate `docs/openapi/secuura-api.yaml`.
  - No `package.json` or lockfile edits.
  - Stay out of `systemTest/performance/`, `Start_Up/`, `check-stack-safety.sh`, `CONTRIBUTING.md` and `.github/workflows/`.
- **Lane 1** (`:50-76`):
  - **Yours:**
    - `gdpr.ts` PATCH `/dsr/:dsrId` at :348 only, reusing `UUID_PATTERN` from :39.
    - `verification.ts` `/verify` validator and handler, :699-734 only.
    - New `ks1029-*.test.ts` and `ks1103-*.test.ts`.
  - **Not yours:**
    - `documents.ts` and `documentRepo.ts` (#939, #919).
    - `anchorStateSync.ts` (#912).
    - `middleware/auth.ts` and `adminConfig.ts` (#799).
    - `originate.openapi.ts` (#919, #813).
    - Existing test files changed by #931/#926/#937/#720.
    - The 15 `err.message` sites in gdpr.ts (KS-730).
    - The spec.
  - **Choices already made:**
    - KS-1029: reuse `UUID_PATTERN` and answer like the KS-431 sibling ("400/404, never 500").
    - KS-1103: "read `hash` in the handler", not "drop it from the spec".
    - If a new documented status code is needed, stop and QUESTION Wednesday.
  - **Suite:**
    - `cd Blockchain/Dev/services/originate && npx jest src/__tests__/ks1029-… src/__tests__/ks1103-… src/__tests__/ks444-gdpr-dsr-update-withdraw-guards.test.ts src/__tests__/ks431-gdpr-export-id-guard.test.ts`, then full `npm test`.
    - Known pre-existing reds: the ks444-webhooks pair, which #926 fixes.
    - Tamper control: remove each guard and the new cell must go red.
    - Schemathesis `not_a_server_error::PATCH /api/gdpr/dsr/{dsrId}` must be gone.
    - A `hash`-only body must get the same verdict as `contentHash`.
  - **Overlap:**
    - KS-730 edits the same gdpr.ts.
    - #931 rebuilds the `@secuura/shared` mocks.
    - The gateway's `routes/verification.ts` (Lane 3) is a different file with the same name.
- **Classification rows:**
  - KS-1029 (`:194`): High, Backlog, unassigned, class A.
  - KS-1103 (`:252`): Medium, Backlog, kamil, class A, "take the handler route, NOT 'drop it from the spec' (spec collides with 4 open PRs)".
  - KS-730 (`:181`): High, Backlog, kamil, "HOLD: 15 of the 71 sites are in originate/src/routes/gdpr.ts (Lane 1's file)".
- **Line-number check:** the lanes file cites `verification.ts:699-734`. At `4554b25e2` the validator array is `:697-710`, the handler starts at `:711`, the destructure is at `:727`, `hashToVerify` at `:731`, and the 400 spans `:733-737`. A fix touches roughly `:711-737`; the lanes range is close enough.

---

## 2. Linear tickets

### KS-1029
- **Title:** "KS-754 gate F-2 (MAJOR): PATCH /api/gdpr/dsr/{dsrId} regresses a malformed id from 200 to 500 — UUID_PATTERN exists in the same file and is not used on this route"
- **URL:** https://linear.app/secuura/issue/KS-1029/ks-754-gate-f-2-major-patch-apigdprdsrdsrid-regresses-a-malformed-id
- **Fields:**
  - State: Backlog (type backlog). Priority 2 (High).
  - Assignee: none. Creator: kamil.kreiser@secuura.ai.
  - Labels: none. Project: none. Team: KS (Secuura-PK). Parent: none. Children: none.
  - Created 2026-09-09T01:33:34Z; updated 2026-09-11T11:15:05Z.
- **Relations:**
  - related → KS-1016 (Done).
  - Inverse related ← KS-971 (Done), KS-682 (Done), KS-565 (Backlog).
- **Scope sentence, verbatim** (first paragraph of the description): "**Source:** tier-1 QA gate on PR #914, 2026-09-09. **One-line fix, and the precedent is a sibling route in the same file.**"
- **Full description, verbatim:**

> **Source:** tier-1 QA gate on PR #914, 2026-09-09. **One-line fix, and the precedent is a sibling route in the same file.**
>
> ## Measured, driven over real HTTP against the mounted router — three cases, one run
>
> | dsrId | base | head |
> | -- | -- | -- |
> | **malformed** (`not-a-uuid`) | 200 `{success:false,'DSR not found'}` | **500 INTERNAL_ERROR** |
> | well-formed, absent | 200 `{success:false}` | 200 `{success:false}` — *unchanged, the control* |
> | well-formed, **real** | 200 `{success:false}` ⟵ the KS-754 defect | **200** `{success:true}` ⟵ the fix working |
>
> ## The fix
>
> `routes/gdpr.ts:39` **already defines** `UUID_PATTERN` and already uses it at `:201` and `:296` — just not on this route. Validate the id before the lookup and answer **400/404**, never 500. This is the exact class **KS-431** was raised to fix, on `/export/:userId/download` in this same file, whose own comment reads *"Reject a non-UUID id up front — it cannot reference a real user → 404 (never a 500)"*. It does not weaken KS-754: a DB error stays loud; a client input error stops being a 5xx.
>
> ## Blast radius
>
> Admin-only (`SYSTEM_ADMIN`/`ORG_ADMIN`). **No data impact** — the throw IS the failing UPDATE, so nothing is written (read back from pg after every driven case). **No information disclosure in production** — verified under `NODE_ENV=production`, the pg message masks to `Internal server error`.
>
> Expect an automated sweep to surface it (KS-444/KS-431 history shows malformed-value probing of these routes). Also the KS-536 4xx rule.
>
> Report: `.../2026-09-09-qa-gate-ks754-pr914/report.md`

- **Comments** (2, oldest first):
  1. **peter@obeden.com, 2026-09-10T11:16:15Z:**
     > Still live on develop-current code, 2026-09-10, Mac, slot 1: `not_a_server_error::PATCH /api/gdpr/dsr/{dsrId}` ×1 in each of two `pre-merge` runs (`pre-merge-ks-682-2026-09-10T10-36-34Z-slot1`, `…T10-52-00Z-slot1`) — malformed id → 500. Not in the Schemathesis baseline, so it fails the gate until fixed or baselined against this ticket. PR under review https://github.com/Secuura/Distributed_Secuura/pull/896 (no service code).
  2. **peter@obeden.com, 2026-09-11T11:15:05Z:**
     > Reproduced by a Schemathesis `pr` sweep, 2026-09-11 — `not_a_server_error::PATCH /api/gdpr/dsr/{dsrId}`: `dsrId=0` (malformed) → `500 INTERNAL_ERROR`. Run `pr-ks-1016-2026-09-11T11-11-33Z-slot4`, local Docker slot 4 (`:7182`), develop `9b222d37c` + the KS-1016 systemTest branch (PR #952), macOS arm64. Not in `schemathesis-baseline.json`, so it fails the gate until fixed or baselined. Reproduce: `curl -X PATCH -H 'Authorization: Bearer <token>' -H 'Content-Type: application/json' -d '{"status":"pending","processedBy":"example-processedBy"}' http://localhost:6882/api/gdpr/dsr/0`.

- **Baseline check:** `git grep "dsr/{dsrId}"` over `systemTest/schemathesis` at `4554b25e2` has no hit in `config/schemathesis-baseline.json`. That matches "not in the baseline".

### KS-1103
- **Title:** "POST /api/verification/verify validates the published 'hash' field but never reads it — a spec-valid body gets 400 'Please provide a content hash…'"
- **URL:** https://linear.app/secuura/issue/KS-1103/post-apiverificationverify-validates-the-published-hash-field-but
- **Fields:**
  - State: Backlog. Priority 3 (Medium).
  - Assignee: kamil.kreiser@secuura.ai. Creator: kamil.kreiser@secuura.ai.
  - Labels: none. Project: none. Team: KS. Parent and children: none.
  - Created and updated 2026-09-12T00:30:43Z.
- **Relations:** related → KS-735 (Todo). No inverse relations.
- **Comments:** 0.
- **Scope sentences, verbatim** (BLUF bullets 1 and 3): "**A spec-valid verify body is refused.** The served spec's `VerifyRequest` publishes `documentId`, `hash`, `title` and `contentHash`. A body carrying only `hash` gets 400 "Please provide a content hash (from the document file) or a documentId."" and "**Cause:** the handler validates `hash` and never reads it."
- **Full description, verbatim:**

> ## BLUF
>
> * **A spec-valid verify body is refused.** The served spec's `VerifyRequest` publishes `documentId`, `hash`, `title` and `contentHash`. A body carrying only `hash` gets 400 "Please provide a content hash (from the document file) or a documentId."
> * **The same value as** `contentHash` **works.** It gets 200 `verified:false`, "This document hash is not registered…".
> * **Cause:** the handler validates `hash` and never reads it.
> * Pre-existing, found by the kintsugi deploy gate on `4554b25e2` (finding F-4, Minor).
>
> ## Recommendation
>
> * Read `hash` in the handler alongside the other hash fields, or drop it from the spec.
> * Make the 400 name the fields it accepts.
>
> ## Detail
>
> * **Cause, in** `services/originate/src/routes/verification.ts` **at** `4554b25e2`**:**
>   * `body('hash')` is in the `/verify` validator chain (around line 704);
>   * the handler destructures only `documentId, providedHash, documentData, contentHash, documentHash` (line 727);
>   * it sets `hashToVerify = providedHash || contentHash || documentHash` (line 731);
>   * the 400 follows at line 734.
> * **Replicated by the gate** at 22:56:16Z and 22:57:50Z. The `contentHash` control ran at 22:57:18Z.
> * **History:** KS-222 (archived) made the validator check every `VerifyRequest` field, `hash` included. The handler does not read `hash` today.
> * **Last touched** 2026-08-12; unchanged in the deploy range.
> * **Regression test (the gate's):** a spec-example body using `hash` returns the same verdict as `contentHash`.
>
> ### Evidence
>
> * **Report:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1/report.md`, section `### F-4 — Public verify: the published hash field is ignored at runtime, and the 400 says no hash was sent`.
>
> ### Dedupe
>
> * **Method:** a literal, case-insensitive census over all 1,089 KS issues (682 archived; title and description) and 2,946 comments (includeArchived), run 2026-09-12 by s188. Per-ticket comment counts equal direct API reads on 9 of 9 tickets.
> * **Searched:**
>   * the 400 text: 0
>   * `body('hash')`: 0
>   * `hashToVerify`: 1 (KS-222, archived)
>   * `providedHash`: 5 (KS-222, KS-281 and KS-282 archived; KS-607 and KS-608 unrelated)
> * **Result:** no existing home.
> * **Related:** KS-735 (the same `VerifyRequest` contract, a different defect).

- **"Last touched 2026-08-12" check:** `git log -- O/src/routes/verification.ts` at `4554b25e2` tops out at `d47f63202` 2026-08-12 "KS-584 P3 leg 2". Confirmed.

### KS-730 (overlap only; not in this lane)
- **Title:** "Security: 71 inline handlers still return err.message verbatim off-production — KS-727's enumerated remainder (api-gateway leaks it TWICE, at the edge)"
- **URL:** https://linear.app/secuura/issue/KS-730/security-71-inline-handlers-still-return-errmessage-verbatim-off
- **Fields:**
  - State: Backlog. Priority 2 (High).
  - Assignee: kamil.kreiser@secuura.ai.
  - Project: "Auth, Tenancy & Access Control". Labels: none. Relations: none. Comments: 0.
  - Created 2026-08-31T20:38:57Z; updated 2026-09-05T23:53:01Z.
- **Scope sentence, verbatim** (BLUF): "**71 response-side sites still return** `err.message` **verbatim unless** `NODE_ENV === 'production'`**.** KS-727 fixed the two *shared* handlers — `packages/shared/src/errors` (mounted by 12 services) and `services/auth`'s own — which was the high-leverage half. These 71 are per-route **inline** handlers: the same defect, a mechanical change, but 5 files across 3 services with their own test surface, so they were enumerated rather than folded into #767." Followed by: "**Do api-gateway first.** It is the edge, and it is the worst of them."
- **Its site table:** adminConfig.ts 46, **gdpr.ts 15**, systemErrors.ts 6, api-gateway/src/index.ts 2, tokenisation/src/index.ts 2.
- **Done-when includes:** "`services/originate` — `adminConfig.ts` (46), `gdpr.ts` (15), `systemErrors.ts` (6). Consider a small local helper rather than 67 edited ternaries".
- **Count check:** `git show 4554b25e2:O/src/routes/gdpr.ts | grep -c err.message` = **15**, which still matches.
  - One of them is `gdpr.ts:363`, inside the KS-1029 handler's catch.
  - The KS-1029 fix should leave that line alone.
- The full KS-730 description was read; it is not reproduced here beyond the parts that matter for this lane.

---

## 3. The code at `4554b25e2`

### 3a. Files
`git ls-tree -r --name-only 4554b25e2 | grep -E 'originate.*routes/(gdpr|verification)\.ts'` returns:
- `Blockchain/Dev/services/originate/src/routes/gdpr.ts` (593 lines)
- `Blockchain/Dev/services/originate/src/routes/verification.ts` (1302 lines)

### 3b. KS-1029: how the router is mounted and which middleware runs
- **Service app** (`O/src/index.ts`), in order:
  - `helmet` (:91), `cors` (:92), `overloadProtection` (:101).
  - `express.json({limit:'10mb'})` (:103), `urlencoded` (:104), `rejectNulBytes()` (:111).
  - Gateway provenance middleware (:215).
  - Multi-tenancy block, only if `MULTI_TENANCY_ENABLED==='true'` (:218-234).
  - Tenant-id resolver (:248-256), `tenantGucContext()` (:257).
  - Then **`app.use('/api/gdpr', gdprRouter)` (:288)**.
- **Router level:** `gdprRouter.use(authenticate())` at `gdpr.ts:164`. Every GDPR route needs a valid RS256 bearer; `authenticate` is at `O/src/middleware/auth.ts:65-119`.
- **Route level:** `requireRole('SYSTEM_ADMIN', 'ORG_ADMIN')` (`gdpr.ts:348`).
  - Defined at `auth.ts:125-144`.
  - No user → 401. A role not in the list → 403 `FORBIDDEN 'Insufficient permissions'`.
  - `super_admin` and `SUPER_ADMIN` normalise to `SYSTEM_ADMIN`.
- **Ownership:** **none.** There is no owner check, and no tenant or organisation check that the DSR belongs to the ORG_ADMIN's org.
  - Any SYSTEM_ADMIN or ORG_ADMIN can PATCH any DSR id.
  - Contrast `GET /dsr/:dsrId` (`gdpr.ts:321-335`), which loads the row and applies an owner-or-`GDPR_ADMIN_ROLES` check (`:327-330`).
  - Out of scope for KS-1029; noted for completeness only.
- **Gateway:**
  - `services/api-gateway/src/routes/proxy.ts:734-745`: a path-collapsing wrapper that runs the `/erasures` scope door only.
  - `:747-750`: `router.use('/api/gdpr', authenticateToken(true), proxy('originate', { '^/api/gdpr': '/api/gdpr' }))`.
  - So PATCH `/api/gdpr/dsr/:dsrId` is JWT-gated at the edge and proxied through unchanged.

### 3c. KS-1029: the handler, verbatim (`gdpr.ts:347-365` @ 4554b25e2)
```ts
347	/** Update DSR status (admin) */
348	gdprRouter.patch('/dsr/:dsrId', requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'), async (req: Request, res: Response) => {
349	  try {
350	    const { status, processedBy, notes } = req.body ?? {};
351	    if (!status || !processedBy) {
352	      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'status and processedBy are required' } });
353	    }
354	    // KS-444: enforce the published DSRUpdateRequest contract — a wrong-typed
355	    // processedBy (the sweep sent `{}`) or a non-vocabulary status previously
356	    // passed the truthy check and reached updateDSRStatus.
357	    const parsed = dsrUpdateBodySchema.safeParse(req.body);
358	    if (!parsed.success) return sendBodyValidationError(res, parsed.error);
359
360	    const updated = await gdpr.updateDSRStatus(req.params.dsrId, status, processedBy, notes);
361	    res.json({ success: updated, message: updated ? 'DSR updated' : 'DSR not found' });
362	  } catch (err: any) {
363	    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message } });
364	  }
365	});
```

### 3d. KS-1029: precedents in the same file
- `gdpr.ts:38-39`:
  ```ts
  /** Canonical UUID — users.id is a uuid column, so a non-UUID subject id is unresolvable. */
  const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  ```
- `gdpr.ts:199-203` (POST /consent) and `:294-298` (POST /dsr) both run `if (!UUID_PATTERN.test(userId)) return res.status(404).json({ success:false, error:{ code:'NOT_FOUND', message:'User not found' } })`.
  - Both sit *after* the Zod body parse. In POST /consent the check sits after the IDOR check too.
- `gdpr.ts:381-390`: the KS-431 export/download route inlines the same regex as a literal rather than `UUID_PATTERN`. It answers 404 `'User not found'` before calling the service. Its comment: "Reject a non-UUID id up front — it cannot reference a real user → 404 (never a 500)."
- **Wording for this route:** it already says `'DSR not found'`, in its 200 body at `:361` and in GET `/dsr/:dsrId`'s 404 at `:324`.
- **Do not reuse `mapGdprWriteDbError`:** at `gdpr.ts:136-156` it maps 22P02 to 404 `'User not found'`, the wrong noun for a DSR.
- **Ordering is not settled by the ticket.** Where the guard goes relative to the body checks decides what a malformed id plus an invalid body returns, 400 or 404. The ticket says only "Validate the id before the lookup and answer **400/404**".

### 3e. KS-1029: the data-access function (`O/src/services/gdprService.ts:326-366` @ 4554b25e2)
```ts
326	export async function updateDSRStatus(
327	  dsrId: string,
328	  status: DataSubjectRequest['status'],
329	  processedBy: string,
330	  notes?: string,
331	): Promise<boolean> {
332	  try {
333	    const auditEntry = JSON.stringify({ action: `status_changed_to_${status}`, timestamp: new Date().toISOString(), actor: processedBy });
334	    const result = await prisma.$executeRaw`
335	      UPDATE data_subject_requests SET
336	        status = ${status},
337	        processed_by = ${processedBy},
338	        completed_at = ${status === 'completed' ? new Date() : null},
339	        notes = COALESCE(${notes}, notes),
340	        audit_trail = COALESCE(audit_trail, '[]'::jsonb) || jsonb_build_array(${auditEntry}::jsonb),
341	        updated_at = NOW()
342	      WHERE id = ${dsrId}::uuid
343	    `;
344	    return result > 0;
345	  } catch (err: any) {
346	    // KS-754: a failed write must NOT come back as an ordinary `false`.
          ... (comment lines 347-357: `false` means "no such DSR"; rethrowing turns the route's 200 into a 500)
358	    logger.error('Failed to update DSR', { dsrId, status, error: err instanceof Error ? err.message : String(err), code: err?.code });
364	    throw err;
365	  }
```
- **Why the 500 happens:** a malformed `dsrId` fails the `::uuid` cast (22P02). Since KS-754 (merge `0c8623e5b`, PR #914, 2026-09-09) the function rethrows, and the route catch answers 500.
- **GET is not affected:** `getDSR` (`gdprService.ts:304-313`) swallows every error to `null` → 404.
- **Other internal callers of `updateDSRStatus`**, service-internal and not affected by a route guard:
  - `gdprService.ts:859` (executeErasure).
  - The comment block at `:1414-1448` (erasure step 12).
- **Adjacent, same class, out of ticket scope:** `POST /erasure/:userId` (`gdpr.ts:534-550`) passes body `dsrId` into `gdpr.executeErasure`, which reaches `updateDSRStatus`. Not measured.

### 3f. KS-1103: the `/verify` route, verbatim (`verification.ts:690-744` @ 4554b25e2)
```ts
690	/**
691	 * POST /api/verification/verify
692	 * Verify by hash or documentId (JSON body).
693	 * For strongest verification, use /verify-file with the actual document.
694	 */
695	verificationRouter.post(
696	  '/verify',
697	  [
698	    // KS-222: validate every field in the VerifyRequest spec schema
699	    // (documentId, hash, title, contentHash — all strings) plus the extra hash
700	    // aliases this handler also reads (providedHash, documentHash) and
701	    // documentData, so a non-string (e.g. {}) is rejected with 400 rather than
702	    // slipping through to a lookup miss that returns 200.
703	    body('documentId').optional().isString(),
704	    body('hash').optional().isString(),
705	    body('title').optional().isString(),
706	    body('contentHash').optional().isString(),
707	    body('providedHash').optional().isString(),
708	    body('documentHash').optional().isString(),
709	    body('documentData').optional().isObject(),
710	  ],
711	  async (req: Request, res: Response) => {
712	    try {
713	      // KS-222: enforce the declared body validators. Previously no
714	      // validationResult check existed, so the rules above were dormant and a
715	      // wrong-type hash reached the lookup and returned 200 instead of a 400.
716	      const validationErrors = validationResult(req);
717	      if (!validationErrors.isEmpty()) {
718	        return res.status(400).json({
719	          verified: false,
720	          error: 'Invalid request body: documentId, providedHash, contentHash and documentHash must be strings; documentData must be an object.',
721	        });
722	      }
723
724	      // Verification is a public endpoint — auth is optional
725	      // (used for audit logging if available, but not required)
726
727	      const { documentId, providedHash, documentData, contentHash, documentHash } = req.body;
728	      const db = (req as any).db || prisma;
729
730	      // Resolve the hash to verify against — accept multiple field names
731	      const hashToVerify = providedHash || contentHash || documentHash;
732
733	      if (!documentId && !hashToVerify && !documentData) {
734	        return res.status(400).json({
735	          verified: false,
736	          error: 'Please provide a content hash (from the document file) or a documentId.',
737	        });
738	      }
739
740	      // If documentData (raw content) is provided, hash it first
741	      let computedHash = hashToVerify;
742	      if (documentData && !computedHash) {
743	        computedHash = generateHash(documentData);
744	      }
```
- **What happens to `hash`:** it is validated as a string (`:704`) and then **never read**. Neither `hash` nor `title` appears in the destructure at `:727`; the only other `req.body` read in the file is `:1265` (the `/hash` route).
- **The type-error 400 at `:720`** lists "documentId, providedHash, contentHash and documentHash" and omits `hash` and `title`, although both are validated. The ticket's second recommendation ("Make the 400 name the fields it accepts") applies to `:736` and arguably `:720`.
- **Downstream:**
  - `computedHash` is normalised by `normaliseHash` (strips `sha256:`, `:869`) and looked up under strategy 1 (`:873` onward).
  - The route is mounted at `O/src/index.ts:273`, `app.use('/api/verification', verificationRouter)`. No router-level auth; public.
- **Precedent for the fix, in the sibling v2 router** (`O/src/routes/verificationV2.ts:445-446` @ 4554b25e2):
  ```ts
  const { documentId, hash, providedHash, contentHash, documentHash, documentData } = req.body || {};
  const hashToVerify = hash || providedHash || contentHash || documentHash;
  ```
  - The v2 400 (`:440`) names all five: "documentId, hash, contentHash, providedHash and documentHash must be strings; documentData must be an object."
  - The v2 missing-input message (`:450`) is "Provide a content hash (or documentData to hash), or a documentId."
  - v1 and v2 would then agree on alias precedence, but v2 puts `hash` first. Where `hash` sits in v1's chain is a builder choice the ticket does not make; it matters only when a body carries two different hash fields.

### 3g. KS-1103: the published spec
- **Source of truth:** `O/src/originate.openapi.ts:531-554` @ 4554b25e2.
  ```ts
  const VerifyRequestSchema = sharedRegistry.register(
    'VerifyRequest',
    z
      .object({
        documentId: z.string().optional(),
        hash: z.string().optional(),
        title: z.string().optional(),
        contentHash: z.string().optional(),
      })
      .passthrough()
      .openapi({
        example: { documentId: FX.document.id, hash: 'example-hash', title: 'example-title', contentHash: '<contentHash>' },
        description:
          'Verification request. Provide ONE OR MORE of documentId, hash, title, contentHash. ' +
          'The verifier tries chain-first, then originate-id lookup, then hash/title strategies.',
      }),
  );
  ```
- **Path registration** (`originate.openapi.ts:1906-1958`): `POST /api/verification/verify`, `security: []`, request body `VerifyRequestSchema`.
  - Description (`:1915-1916`): "The request envelope is permissive: provide documentId, hash, title, or contentHash."
  - `400` (`:1943-1950`): "Missing verification input (no documentId / hash / documentData)", schema `{ verified: boolean, error: string }`.
- **Generated YAML:** `Blockchain/Dev/docs/openapi/secuura-api.yaml`.
  - `:6353-6370` `components.schemas.VerifyRequest` has properties `documentId`, `hash` (`:6358`), `title`, `contentHash`, with the same description and example.
  - `:28737-28784` is the path, `$ref: "#/components/schemas/VerifyRequest"`; its 400 is described as "Missing verification input (no documentId / hash / documentData)".
- **Spec example check:** the spec's own example body uses `hash: 'example-hash'`, which is what a Schemathesis example run sends.
- **Baseline check:** `systemTest/schemathesis/config/schemathesis-baseline.json` has an entry for `POST /api/v2/verification/verify` at `:453` but none for v1 `/api/verification/verify`. I grepped only for the path string; the baseline was not read in full.
- **No spec edit needed:** reading `hash` in the handler makes runtime match the published contract.
- **KS-1029 spec** (`originate.openapi.ts:3253-3278`):
  - PATCH `/api/gdpr/dsr/{dsrId}`, params `z.object({ dsrId: z.string() })` with no uuid format, body `DSRUpdateRequestSchema` (`:2634-2655`).
  - Responses: 200 "DSR updated (success=false if id not found)", **400** (`:3269`), 401, 403 "Insufficient role", **404** (`:3272`), 429, 500, 502, 503.
  - Both 400 and 404 are already declared, so KS-1029 needs no new status code.

---

## 4. Tests that exist today

### Runner and config (`O` @ 4554b25e2)
- `O/package.json` scripts: `"test": "jest"`, `"test:integration": "jest --config jest.integration.config.js"`.
- devDeps: `jest ^29.7.0`, `ts-jest ^29.4.11`, `@types/jest ^29.5.14`. **Not vitest. No supertest**: tests start the app on an ephemeral port and use global `fetch`.
- `O/jest.config.js`:
  - `preset: 'ts-jest'`, `testEnvironment: 'node'`, `roots: ['<rootDir>/src']`, `testMatch: ['**/__tests__/**/*.test.ts']`.
  - `testPathIgnorePatterns` excludes `\.integration\.test\.ts$`.
  - `moduleNameMapper: { '^uuid$': '<rootDir>/src/testUtils/uuid-cjs.ts' }` (KS-466).
- `O/jest.integration.config.js`: `*.integration.test.ts`, DB-backed via TEST_DATABASE_URL, `testTimeout: 30000`.

### Coverage today for the two routes
- **PATCH `/dsr/:dsrId`:** `O/src/__tests__/ks444-gdpr-dsr-update-withdraw-guards.test.ts:76-114`.
  - Covers body guards only: missing fields → 400 BAD_REQUEST, `processedBy:{}` → 400 VALIDATION_ERROR, bad status → 400, `'processing'` → 200, spec-shaped → 200.
  - **All cells use a well-formed `DSR_ID = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee'` (`:51`). No malformed-id cell exists.**
- **Service layer for KS-754:** `O/src/__tests__/ks754-processed-by-widened.test.ts`.
  - Unit-tests `updateDSRStatus`: rethrow on 22P02 and 53300; 0 rows → `false`; 1 row → `true`.
  - Mocks `../db` and `../utils/logger`.
- **`/verify`:**
  - `O/src/__tests__/ks563-certified-vs-anchored.test.ts` and `ks584-verify-row-selection.test.ts` both drive `POST /api/verification/verify` with `{ contentHash: HASH }` only (`ks563:103-110`, `ks584:113-120`).
  - The `ks563:101` comment says "The route reads `providedHash | contentHash | documentHash` — not `hash`."
  - **No test sends `hash`. No test asserts the "Please provide a content hash" 400.** A `git grep` for that text, `providedHash` or `documentHash` under `__tests__` has one hit, the ks563 comment.
- **Nearby, not these routes:** `ks694-nodeenv-role-gate-bypass.test.ts:120` lists `/api/gdpr/dsr/pending` (GET).

### Pattern to copy for KS-1029: `O/src/__tests__/ks431-gdpr-export-id-guard.test.ts` (57 lines, the precedent the ticket names)
```ts
const mockExportUserData = jest.fn();
jest.mock('../services/gdprService', () => ({ exportUserData: mockExportUserData }));
jest.mock('../middleware/auth', () => ({
  // Auth/authz are not under test — pass everything through.
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  hasAnyRole: () => true,
}));
import express from 'express';
import { gdprRouter } from '../routes/gdpr';
const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);
// beforeAll: server = app.listen(0,'127.0.0.1'); baseUrl = http://127.0.0.1:<port>
it('404s on a malformed (non-UUID) userId without touching the DB — no raw 500', async () => {
  const res = await fetch(`${baseUrl}/api/gdpr/export/%23%F2%B5%92%9B/download`);
  expect(res.status).toBe(404);
  expect(mockExportUserData).not.toHaveBeenCalled();
});
it('reaches the service for a well-formed UUID userId', async () => { /* mockResolvedValueOnce → 200, toHaveBeenCalledWith(uuid) */ });
```
- ks444-gdpr-dsr-update-withdraw-guards uses the identical harness with `updateDSRStatus` mocked plus a `send(method, path, body)` helper (`:14-74`).
  - That makes it the closest harness for a KS-1029 cell: `PATCH dsr/0` and `dsr/not-a-uuid` with a valid body → 4xx, `mockUpdateDSRStatus` not called; well-formed control → called.
- gdpr.ts imports no `@secuura/shared` directly (imports at `gdpr.ts:14-18`: express, zod, gdprService, middleware/auth, utils/pgErrors). The gdpr suites do not mock `@secuura/shared`, so #931's mock rewrite does not touch this pattern.
- **Tamper control:** mocking `updateDSRStatus` to reject a 22P02-coded error for the malformed id reproduces the real 500 when the guard is removed. Without that, the mock returns `undefined` and the route answers 200.

### Pattern to copy for KS-1103: `O/src/__tests__/ks584-verify-row-selection.test.ts:24-128` (same harness as ks563)
- `process.env.NODE_ENV='development'` and a `DATABASE_URL` shim (the logger → config throws at load without it, `ks563:24-26`).
- `jest.mock('../db', () => ({ prisma: { $queryRaw: mockQueryRaw }, getTenantManager: () => null }))`.
- `jest.mock('../middleware/auth', …)` passthrough.
- `jest.mock('@secuura/shared', () => ({ runWithTenantId: (_t, fn) => fn(), queryWithTenantGuc: jest.fn() }))`, the hand-written partial mock that #931 replaces.
- `jest.mock('../repositories/documentRepo', () => ({ walkAncestors: …, walkDescendants: …, MAX_LINEAGE_DEPTH: 10 }))`.
- `app.use(express.json()); app.use('/api/verification', verificationRouter)`, listening on port 0.
- `beforeEach` sets `global.fetch = jest.fn().mockRejectedValue(...)` so the chain-first lookup misses. `realFetch` is kept for the test's own requests.
- **Regression cell the gate asks for:** the same `mockQueryRaw` rows, sent once as `{ hash: HASH }` and once as `{ contentHash: HASH }`; assert equal status and `verified`/`checks`. Plus the negative: `{}` still → 400.
- **#931 (open, kksecura, head `f2e0cb3c1`)** adds `O/src/__tests__/helpers/sharedModuleMock.ts` (`makeSharedMock(overrides)`, built from `jest.requireActual('@secuura/shared')`). It changes ks563 and ks584-verify-row-selection to:
  ```ts
  jest.mock('@secuura/shared', () =>
    require('./helpers/sharedModuleMock').makeSharedMock({
      runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
      queryWithTenantGuc: jest.fn(),
    }),
  );
  ```
  - Source: `GET /repos/Secuura/Distributed_Secuura/pulls/931/files` patch.
  - Consequence: a ks1103 test written on develop today can only use the hand-written partial mock (the helper does not exist at `4554b25e2`), and should be moved to `makeSharedMock` if #931 merges first.

---

## 5. Collision check (GitHub, live at gather time)

- **Method:** `GET /repos/Secuura/Distributed_Secuura/pulls?state=open&per_page=100`, one page.
  - 49 open PRs, all on base `develop`: kksecura 38, dependabot[bot] 10, PeterObeden 1.
  - For each, `GET /pulls/{n}/files?per_page=100` (paged); no PR hit the file cap.
- **PRs changing `O/src/routes/gdpr.ts` or `O/src/routes/verification.ts`: none.**
- **PRs changing any file under `O/src/routes/`:**

| PR | author | head SHA | routes file(s) | all originate files in the PR |
|---|---|---|---|---|
| #939 | kksecura | `481e0267f660a68fcaf74c4571166c48a86f1220` | `routes/documents.ts` | ks1068-blockchain-blob-type.test.ts, documentRepo.ts, documents.ts |
| #919 | kksecura | `d0aff46d48dce64b63badca4ec765a47e925cdda` | `routes/documents.ts` | ks739-transfer-custody-lookup-4xx-mapping.test.ts, originate.openapi.ts, documents.ts (+ secuura-api.yaml) |
| #799 | kksecura | `38f6377b9c6429be2627cb5454e98a36104a25b8` | `routes/adminConfig.ts` | ks764-admin-api-keys-revoke-route-contract.test.ts, middleware/auth.ts, adminConfig.ts |

- **Other open PRs touching originate or the spec** (not the lane's files, but nearby):
  - #931 kksecura `f2e0cb3c1`: `__tests__/helpers/sharedModuleMock.ts` (new), ks1061-shared-mock-completeness, gdprService.erasure, ks444-webhooks-create-description-guard, ks445-pg-error-classification, **ks563-certified-vs-anchored**, ks584-p3-auth-error-classification, ks584-p3-verify-list, **ks584-verify-row-selection**, ks695-erasure-by-external-ref, ks914-deliver-webhook-blocked-vs-failed, qa-f4-resolveonbehalfof-org-normalisation.
  - #912 kksecura `ae8751f38`: anchorStateSync.ts, ks1004, ks535 tests.
  - #937 kksecura `cf8b23366`: ks1059 test.
  - #926 `542492c41` and #720 `fcc611d29` (kksecura): ks444-webhooks-create-description-guard.test.ts.
  - #813 kksecura `54225cbbd`: originate.openapi.ts + secuura-api.yaml.
  - #922 `2b5075e9f` and #805 `97e2161fa` (kksecura): secuura-api.yaml.
  - #949 `7ee1a26e6` and #575 `7d32d8ae4` (dependabot): O/package.json.
- **Open PRs naming KS-1029, KS-1103 or KS-730** (case-insensitive regex over title, body and head ref): **none.**
- **Remote branches:** `git ls-remote --heads origin | grep -iE "1029|1103|ks-730|ks730"` matched only a SHA substring on `refs/heads/seat-b/ks-860-loopback-listen-guard`. No branch exists for either ticket.
- **Linear:** neither ticket has an attachment or linked PR (`attachments: []`), and neither is In Progress.
- **Not checked:** unpushed local worktrees of other seats.

---

## 6. Other callers and consumers (blast radius) @ 4554b25e2

### PATCH `/api/gdpr/dsr/:dsrId`
- **Search:** `git grep "gdpr/dsr"` over the whole tree, excluding node_modules and lockfiles.
- **No code caller issues a PATCH to it.** Hits are:
  - **Frontend:** `frontend/admin/src/pages/SystemHealth.tsx:99`, GET `/api/gdpr/dsr/pending` only.
  - **Scripts:** `scripts/smoke-test.sh:239`, GET pending only.
  - **E2E:**
    - `tests/e2e-v2/fixtures/api-client.ts:354` POST `/api/gdpr/dsr`.
    - `tests/e2e-v2/tests/tier1-api/gdpr-authz.api.spec.ts:43` GET `/dsr/user/:id`.
    - `tests/e2e/tests/cross-persona-e2e.prelaunch.spec.ts:1452-1479` POST, `:1586` GET `/dsr/:id`.
    - `email-notifications.prelaunch.spec.ts:486` POST.
    - `gdpr-compliance.prelaunch.spec.ts:57-59` POST paths.
  - **Schemathesis:** `systemTest/schemathesis/tests/test_auth_security.py:27,353`, GET `/gdpr/dsr/user/{user_id}`.
  - **Originate:** the `/api` index at `O/src/index.ts:152`; the spec at `O/src/originate.openapi.ts:3255` and `docs/openapi/secuura-api.yaml:30130`; unit test `ks444-gdpr-dsr-update-withdraw-guards.test.ts`.
  - **Docs only:** `Projects Documents/*` (Compliance Report, Development Summary, White Paper, Stakeholder-Guide-System-Administrator.md:349).
- **Gateway:** `services/api-gateway/src/routes/proxy.ts:747-750` (JWT + transparent proxy to originate). Also listed in the gateway prefix list at `services/api-gateway/src/index.ts:408`.
- **Internal service use:** `gdprService.updateDSRStatus` is also called by the erasure flow (`gdprService.ts:859`). A route-level guard does not reach it.
- **Reading:** a UUID guard on the route changes only malformed-id answers, 500 → 4xx. Well-formed ids behave as before, and no in-repo client sends a malformed id.

### POST `/api/verification/verify`
- **Search:** `git grep` for `verification/verify` and `'/verify'`. Request body per caller:

| caller | file:line @ 4554b25e2 | body field(s) sent |
|---|---|---|
| **mobile app** | `mobile/secuura-app/src/services/api.ts:157-158` (base `http://localhost:6882/api` / `https://api.secuura.io/api`, `:56-58`) | **`{ hash }`: 400 today; this ticket fixes it** |
| verifier portal (by ID) | `frontend/verifier/src/components/VerifyPage.tsx:79-85`; `ResultPage.tsx:104-110` | `{ documentId }` |
| verifier portal (file drop) | `frontend/verifier/src/components/VerifyPage.tsx:122-128` | `{ contentHash, fileName }` |
| issuer portal | `frontend/issuer/src/services/api.ts:358-363` | multipart `FormData` (not JSON; unaffected by field aliasing) |
| outlook add-in | `frontend/outlook-addin/src/utils/api.ts:74-77` | `{ contentHash: hash }` |
| gmail add-on | `frontend/gmail-addon/Code.gs:163-166` | `{ contentHash: hash }` |
| whatsapp bot | `connectors/whatsapp-bot/src/verify.ts:17-22` | `{ contentHash }` |
| flutter app | `connectors/flutter-verify-app/lib/services/verify_service.dart:18-24` | `{'contentHash': contentHash}` |
| libreoffice | `connectors/libreoffice-extension/src/secuura/verifier.py:70-72` | `{"contentHash": content_hash}` |
| nextcloud | `connectors/nextcloud-app/secuura/lib/Service/SecuuraClient.php:59-64` | `['contentHash' => $contentHash]` |
| euro-office | `connectors/euro-office-plugin/scripts/api.js:20-27` | `{ contentHash }` |
| python SDK | `sdk/python/secuura/client.py:102-103` | `{"contentHash": content_hash}` |
| smoke test | `scripts/smoke-test.sh:214-216` | `{"documentId":"doc-demo-degree-001"}` |
| azure deploy smoke | `deployment/azure/deploy-all.sh:311-314` | `{"contentHash":"sha256:smoketest"}`, expects 200 |
| insurance runner | `insurance-test-runner.js:401,419` | `{ documentId }` |
| KS-584 parity sweep | `scripts/verify/ks584-p3-parity-sweep.mjs:74` | `{ contentHash: hash }` (v1) |
| originate unit tests | `ks563-certified-vs-anchored.test.ts:104-107`, `ks584-verify-row-selection.test.ts:114-117` | `{ contentHash }` |

- **Gateway:**
  - `services/api-gateway/src/routes/proxy.ts:588-591`: `router.use('/api/verification', proxy('originate', { '^/api/verification': '/api/verification' }))`, with no auth ("no auth required for public verification").
  - `middleware/csrf.ts:98`: CSRF-exempt.
  - `index.ts:504-512` and `middleware/rateLimitSkip.ts:23`: global-limiter exempt.
  - The gateway's own `routes/verification.ts` handles `/api/documents/:id/verify` (`:398`) and `/api/certifications/:id/verify` (`:637`), **not** `/api/verification/verify`. It is Lane 3's file and a different module.
- **v2:** `/api/v2/verification/verify` (`O/src/routes/verificationV2.ts:422-461`) already reads `hash`. No change needed.
- **Reading:** adding `hash` to the v1 alias chain changes only bodies that carry `hash`.
  - A `hash`-only body goes from 400 to a real lookup.
  - No caller in the repo sends both `hash` and another hash alias, so alias order cannot change any existing caller's verdict.
  - The response shape is unchanged.

---

## What I could not establish
- **No tests, tsc, eslint or Schemathesis runs** (read-only). The 500 for a malformed `dsrId` is inferred from code (cast at `gdprService.ts:342` + rethrow at `:364` + catch at `gdpr.ts:362-363`). It matches Peter's two reproductions in KS-1029 comments.
- The `hash`-only 400 is likewise read from code (`verification.ts:727-737`) and matches the KS-1103 gate report. The gate report itself was not opened.
- **Not read:**
  - PR review or approval state and mergeability.
  - The QA reports cited by either ticket (`.../2026-09-09-qa-gate-ks754-pr914/report.md`, `Testing Agent MAIN/.../2026-09-12-kintsugi-deploy-4554b25e2-tier1-r1/report.md`).
  - The full `schemathesis-baseline.json` (grepped only).
- **Mobile app's production value:** whether `mobile/secuura-app` is shipped or used live is unknown. I only know it sends `{ hash }`.
- **ORG_ADMIN scope on PATCH `/dsr/:dsrId`:** there is no org/tenant ownership check (§3b). The tickets do not raise it; noted, not investigated.
- **Unpushed seat worktrees** that might already hold a fix are invisible to `ls-remote`.
