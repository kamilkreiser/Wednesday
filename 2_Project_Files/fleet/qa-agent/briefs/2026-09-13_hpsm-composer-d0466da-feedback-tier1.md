# QA GATE, TIER 1: Datasec/HPSM Policy Composer - the FEEDBACK feature @ d0466da (feature-scoped, round 1) — LOCAL ONLY

**Commission (the DELIVERABLES oracle).** Kam, typed in Tuesday's terminal, 2026-09-13 16:53:31 AEST (the prompt log records 16:55), verbatim: *"Please get the HPSM agent to identify what else is left to complete and whether there are any issues with the product.   Also get the agent to add the feedback feature as deployed in Nexus AI to the HPSM project. Naturally change all settings so that any feedback is registered against HPSM and works properly."*
- Recorded verbatim at `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-13_hpsm-s43-successor-recover-remaining-feedback.md` L6.
- This gate tests the second and third sentences only.

**Gate commission.** Tuesday, `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-13_hpsm-s45-answer-feedback-gate-before-live.md` L1-8: a FEEDBACK-scoped tier-1 gate NOW, local only, on `d0466da`, ports 21480-21599, first claim on the docker lock.
- **The LIVE feedback upgrade waits for this verdict.** It needs GO, or GO WITH FINDINGS with no Blocker or Major on the feedback surface (L3-6).
- Rate severity honestly. Never rate it to fit that bar.

**Head:** `d0466daaa7f2ae30b2da8f8fd537e95250da0aa8`, local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`.
- **Feature delta** `9b8ea76c073cefab0319d2bec7b5a82c54b4e9d1..d0466da`: 22 commits, 5 on the first parent:
  - `935b46c` F-API: migration `0016_feedback.sql`, the feedback routes, contract 0.14.0;
  - `aab9726` feedback root: edge `client_max_body_size 52m` on `/api/feedback`, `PC_FEEDBACK_RETENTION_DAYS`;
  - `ca4e75e` edge route-table row;
  - `cfd3cc6` G9 guard probes (tests only);
  - `d0466da` F-WEB: widget, My feedback, the platform_admin admin screen; naming (b).
- `afc10e9..d0466da` is 342 commits, NOT pushed. HPSM-light `origin/main` = `afc10e98c51505be1f1943335370cf2de3b47d44`. Not live on any stack.
- The launcher refuses unless the head is reachable from `refs/heads/main`.
- **Your verdicts are about d0466da only. A later head needs a new brief, not a re-pointed launcher.**
- **TWO verdicts, each GO / GO WITH FINDINGS / NO GO: `DELIVERABLES` and `SECURITY`, both about the feedback feature.**

## Prior state (context only; round 1 of a feature-scoped class, no carry-forward)
- **No gate has tested feedback.** The builder's READY FOR QA document is `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-s45/feedback-ready/README.md` (read it whole). Its results table (L46-59) is a CLAIM, not evidence.
- **Nearest gates on the rest of the product**, under `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/` (Blocker/Major/Minor/Polish):
  - `caf63fd` acceptance + security: DELIVERABLES NO GO 1/2/10/4 · SECURITY GO WITH FINDINGS 0/0/3/1;
  - `87c0026` delta: both GO WITH FINDINGS.
  - Neither covers feedback. Do not redo their work. **This brief's LOCAL ONLY rule governs even where those reports describe other environments.**
- **Lane M16 (migration 0016 and rollback):** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-s45/m16-0016-rollback/REPORT.md`.
- **This codebase has repeatedly shipped tests that could not fail.**

## Charter (read first, in full)
- **Charter:** `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. Rule 1 (FAIL condition first) and Rule 2 (NOT TESTED is output) govern every row.
- **Deliverables:** walk the feature against Kam's commission and the rulings. Look for anything missing, partial, falsely claimed, or not working properly end to end.
- **Security:** attack the feedback surface as a hostile tenant, a hostile role, a careless user pasting a credential, and a hostile file.

## 1. Target — LOCAL ONLY
- **LOCAL ONLY.** Your own clone and your own compose stacks on 127.0.0.1. Out of scope: the live Azure demo, every other stack, and every other seat's worktree. No request, no ssh, no `az`, no `gh`.
- **Clone:**
  - `D="$(mktemp -d)"; git clone --no-hardlinks '/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer' "$D/pc"`, then check out the head DETACHED. Run `scripts/install-hooks.sh` in YOUR clone.
  - For the upgrade path, a second clone (or a worktree inside YOUR clone) detached at `9b8ea76`.
  - **Never write into the original repository or its `.git`:** no `git worktree add` there, no fetch into it, no lock files. Read it only with `git --no-optional-locks`.
- **Your stacks,** 127.0.0.1 only, free at briefing. **Ports 21480-21599 are the gate's; nothing outside that range is yours.**
  - `policy-composer-qa-fb-up`, edge **21480**, the UPGRADE-PATH stack:
    - bring it up at `9b8ea76` (15 migrations) and create ordinary data (a second tenant, an engagement, sign-ins);
    - then redeploy the SAME project and volumes at `d0466da`, so compose `migrate` applies 0016 over 15;
    - most probes run here, because it has the shape the live upgrade will take.
  - `policy-composer-qa-fb-fresh`, edge **21580**: `d0466da` on empty volumes (16 migrations from zero). It is the schema-comparison control, and the stack for superuser, RLS and trigger-tamper probes.
  - Both use compose defaults (demo switch OFF) unless a probe needs ON; say which. Generate stack passwords per run (pattern `scripts/ci.sh` L13-17). `PC_EDGE_PORT` sets the edge (`compose.yaml` L130).
  - **Optional, last:** clean-clone CI with `PC_CI_EDGE_PORT=21495` and `PC_E8_SOW_TEXT=/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/_extracted/sow_e8.md`.
    - `scripts/ci.sh` L9 names its own throwaway project `pc-ci-<run_id>`. It is the ONE project not named `policy-composer-qa-fb-*`.
    - Record its name in the docker ledger, and let `ci.sh` tear it down.
- **Browser:** the local image `mcr.microsoft.com/playwright:v1.63.0-noble` (present at briefing), via `apps/web/e2e/run.sh <your project>`.
- **Environment:** local compose, idp-mock synthetic identities, synthetic tenants, non-prod.
- **LEAVE ALONE:** never stop, recreate, exec into, send traffic to, or remove the volumes of anything you did not start. That includes:
  - lane A's stack `pc-lane-a`;
  - S45's seat and lane stacks `pc-s45-*` (among them 24080-24780 and 25080-25599) and `integ-s44`;
  - any `pc-ci-*` you did not start;
  - any `policy-composer-qa-*` project other than your two.
  - **Any port outside 21480-21599 belongs to someone else.**
- **Shared daemon, THE DOCKER LOCK.**
  - Run EVERY docker step (build, up, down, run, exec, and every suite that calls docker) as `lockf -k /private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/dc13ed6b-f206-4b51-b117-ff3f2723cf9b/scratchpad/docker.lock <cmd>`.
  - The gate has FIRST claim (S45 answer L12). Hold the lock one step at a time.
  - Run test runners with `--maxWorkers=2`.
  - **A timeout gets at most 2 re-runs; after that the row is LOAD-BLOCKED** (NOT TESTED, with the reason). Never raise a timeout.
  - Count volumes at START (137 at briefing, 2026-09-13 13:47Z) and at END.
- **END:** `docker compose -p <each of your projects> down` with VOLUMES KEPT (no `-v`). Never `docker system|volume|image prune`, and never remove anything you did not create.

## 2. Spec / DoD - REFERENCE DOCUMENTS (read-only; every row cites document + line)
- **AUTHORITATIVE, Kam's commission:** verbatim above. Also at `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-13_hpsm-s43-successor-recover-remaining-feedback.md` L6.
- **HOW IT WAS TO BE PORTED** (Tuesday's S43 brief, the same file, L32-46):
  - Postgres + RLS + the object store (L39).
  - `created_by` comes from the verified token; display name + role, no email; never NexusAI's `'anonymous'` (L40).
  - Every signed-in role submits. Triage, update and delete are role-gated. Cross-tenant access is 404 (L41).
  - Everything registers against HPSM: no NexusAI or `RD` strings or URLs (L42).
  - The Telegram coordinator is OUT of scope (L44).
  - RED-first tests, mutants and axe (L45).
  - **L42's "HPSM Policy Composer in every string" is SUPERSEDED on screen by naming (b), below.**
- **RULINGS THAT CHANGED THE SPEC.** An intentional change is not a gap; contradicting a ruling is a finding.
  - **Tuesday 08:07:30Z CONFIRMED**, `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/5_Project_History/HANDOVER-S43_seat-hpsm-28f5.md` L101:
    - (i) platform_admin triage;
    - (ii) tenant data, 365 d retention, report-only expiry, soft delete;
    - (iii) F-API ships 0016.
    - Amendment 2 (same line): a one-at-a-time docker lock, `--maxWorkers=2`, at most 2 re-runs then LOAD-BLOCKED.
    - The purge policy went to BACKLOG only (§7).
  - **Tuesday 09:14:10Z, naming (b):** HANDOVER-S43 L114 and L127 (D-S43-10); `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/5_Project_History/HANDOVER-S44_seat-hpsm-375c.md` L43.
    - The product name on screen comes from `apps/web/src/brand.ts` (`PLATFORM_DEFAULT_BRAND.productName`). "HPSM" stays internal.
    - **So "registered against HPSM" is measured as:**
      - the item is stored and audited in the Composer's own database, tenant and audit chain;
      - nothing names NexusAI or `RD-`, or carries a NexusAI URL or `anonymous`;
      - the screen shows the brand productName.
      - **The literal word "HPSM" absent from the screen is NOT a gap; "HPSM" present on screen IS a finding against naming (b).**
- **The builder's declaration:** the S45 README above. L18-24 rulings implemented; L26-44 what is in it; L61-69 known and declared; L71-75 the upgrade note; L77-78 not claimed.
- **PARITY REFERENCE, NexusAI.** READ ONLY: open the files, run nothing, no git verb there. The gate tests HPSM only.
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/backend/routes/feedback.js`:
    - GET list L54, GET `/report` L75, GET `/summary` L122;
    - POST L165 (types feature/bug/feedback L193; `created_by || 'anonymous'` L253);
    - GET attachment L295, PATCH L336, POST triage L372;
    - POST coordinator-action L405 (OUT of scope, S43 brief L44);
    - DELETE L483;
    - mounted at `/api/feedback` in `backend/server.js`.
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/backend/feedbackAttachments.js`: L58-59 (10 MB x 5 files); L67-75 (png, jpeg, gif, webp, pdf, docx, xlsx, txt/log).
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/backend/feedbackTriage.js`: rule-based clarity triage.
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/static/js/feedback-widget.js`: type buttons L30-38; title maxlength 200 L46; "Up to 5 files, 10 MB each" L57-61; paste a screenshot L237-250.
  - `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/static/js/feedback-admin.js`: the admin list, download, update and delete.
- **The HPSM implementation** (read-only, in YOUR clone at the head):
  - `apps/api/src/routes/feedback.ts`: roles L25-35; list excludes deleted L104; the platform tenant is 404 L262-263; scanned fields L403; Idempotency-Key conflict L423; upload route outside `operation()` L526-530; download L573-635 (headers L630-633); `asPlatform` L637-660; update L678; triage L721; soft delete L737-750.
  - `apps/api/src/authz.ts`: L23 `FEEDBACK_AUTHORS` = all seven roles; L72-75 tenant permissions (create, list, get, download); L93-99 platform permissions (all seven ops, platform_admin only).
  - `packages/api-contract/src/document.ts`: L88 types; L103-110 limits: 5 attachments, 10 MiB each, request 53,477,376 bytes, title 200, description 10,000, page URL 2,000.
  - `packages/api-contract/src/openapi.json`: L5 `0.14.0`; paths L4719 `/feedback`, L4953 `/feedback/{feedbackId}`, L5199 `/feedback/{feedbackId}/attachments/{attachmentId}`, L5315 `/feedback/{feedbackId}/triage`.
  - `apps/api/src/feedback-attachments.ts`: L26-43 types; L80 `sanitiseDisplayName`; L194-196 Content-Disposition.
  - `apps/api/src/feedback-multipart.ts`.
  - `apps/api/src/secrets.ts` L13: `MAX_JSON_DEPTH = 64`.
  - `packages/db/migrations/0016_feedback.sql`.
  - `docker/edge.nginx.conf`: L27 `/api/`; L34-41 `location = /api/feedback`.
  - `compose.yaml` L63: `PC_FEEDBACK_RETENTION_DAYS`.
  - `apps/web/src/feedback/`: FeedbackWidget.tsx L42 and L283 "My feedback"; FeedbackAdmin.tsx. `apps/web/src/router.tsx` L33: `/admin/feedback`.
  - `scripts/feedback-sweep.sh` L1-22.
- **Suites** (each runs in YOUR clone or against YOUR stack, and nowhere else):
  - `apps/api/test/api-feedback.db.test.ts`, `apps/api/test/api-feedback-attachments.db.test.ts` and `packages/db/test/wp4-0016.db.test.ts` through `scripts/test-db.sh` (its own internal-only postgres, no published port, L3).
  - `scripts/stack-rls-test.sh`, `scripts/stack-api-isolation.mjs` and `scripts/egress-test.sh`, with `PC_COMPOSE_PROJECT` / `PC_EDGE_URL` set to YOUR project and edge.
  - `scripts/secret-scan.sh` over YOUR clone.
  - `apps/web/e2e/run.sh <your project>` with `feedback-widget.spec.ts`, `feedback-admin.spec.ts` and `feedback-body-size.spec.ts`.
  - `scripts/feedback-sweep.sh --edge http://127.0.0.1:21480`.
  - **A repo test is evidence only after you watch it FAIL on a defect you planted in YOUR clone.**
- **Builder evidence** under `qa-s45/` and in the S43/S44/S45 scratchpads is a claim, not evidence.

## 2a. LEGITIMATE SHAPES
Not a checker; a product feature. Pair every refusal probe with the ordinary input that must pass. **A guard that refuses ordinary use is a finding.**

| ordinary shape | expected |
|---|---|
| a consultant submits a bug with a title and description, no attachment | 201; in their My feedback; not in `consultant-2`'s |
| 5 attachments of 10 MiB each (the contract maximum), through the edge | 201 (README L56 claims 5 x 10 MB accepted) |
| a pasted PNG screenshot | 201; downloads byte-identical (sha256) |
| a `.docx`, an `.xlsx`, a UTF-8 `.log` with tabs | 201 |
| prose saying "password policy", "token lifetime", "rotate the API key" | 201: the scan refuses credential VALUES, not the words |
| a title of exactly 200 characters; a description of 10,000; accented, CJK, emoji | 201 |
| the same `Idempotency-Key` retried with the same body | one item, the same answer |
| platform_admin lists a named customer tenant, triages, PATCHes admin notes, soft-deletes behind the confirmation | success, each audited in that tenant's chain |

## 3. Scope
### 3.1 DELIVERABLES - traceability matrix
- **Row:** `ID | requirement | source + line | status | evidence path | evidence class`.
- **Status:**
  - MET / PARTIAL / NOT MET;
  - **RULED** — cite the ruling's path + line;
  - **OUT OF SCOPE** — S43 brief L44;
  - **NOT TESTABLE LOCALLY** — say why.

**Minimum rows:**
1. **Submit from the product.**
   - A floating Feedback button on every signed-in screen.
   - An accessible dialog: type (feature/bug/feedback), title, description, attachments by picker AND by paste, page path (commission; NexusAI widget L30-61; README L42).
   - Each of the seven roles can submit in a tenant where it holds a role (authz.ts L23, L72).
2. **Registered against HPSM** (commission; S43 brief L40-42; naming (b)).
   - The item lands in `pc.feedback_item` under the submitter's tenant.
   - `created_by` is the verified principal, with display name + role and NO email.
   - Nothing in the screen, API responses, DB rows, audit events, logs, sweep output or the web bundle names `NexusAI`, `Nexus AI`, `RD-<digits>` or `anonymous`. Grep all of them, with a planted positive control.
   - The screen shows `PLATFORM_DEFAULT_BRAND.productName`.
3. **My feedback:** the submitter sees their own items (FeedbackWidget.tsx L42), and only theirs.
4. **Triage by platform_admin only** (README L44; ruling (i)).
   - List a named tenant, get, download, triage, update (status, priority, admin notes), and soft delete behind a confirmation.
   - Clarity triage: `feedback-triage.ts` L2 claims NexusAI's rules were "ported rule for rule". Compare against NexusAI `feedbackTriage.js` on at least 5 inputs, including a vague one and a detailed one.
5. **Attachments** upload and download end to end through the edge, with identical sha256, for every NexusAI type (feedbackAttachments.js L67-75 vs feedback-attachments.ts L26-43).
6. **Retention** (ruling (ii)).
   - `PC_FEEDBACK_RETENTION_DAYS` defaults to 365 and accepts 1-36500; an invalid value stops the api at start (README L13; compose.yaml L63).
   - Every new item records its retention and an `expires_at`.
   - **Expiry is REPORT-ONLY:** `scripts/feedback-sweep.sh` reports past-retention items and deletes nothing (L12-14). Construct an expired item on YOUR stack and show it is reported and not purged.
     - If that needs a superuser trigger bypass, do it on `policy-composer-qa-fb-fresh` only and record how. Otherwise mark it NOT TESTED.
   - Deletion is SOFT only.
7. **Works properly through the edge** (edge.nginx.conf L34-41; README L14, L56).
   - The exact `location = /api/feedback` (52m = 54,525,952 bytes) lets the contract maximum through.
   - Between the API cap (53,477,376 bytes) and 52m, the answer is the API's JSON problem detail. Above 52m, it is nginx's 413.
   - Every other feedback path (`/api/feedback/{id}`, `/attachments/`, `/triage`) routes through `/api/` (L27) and works.
8. **Idempotency-Key:** a retry gives one item; the same key with a different body is refused (routes L423).
9. **Accessibility:** axe WCAG 2.2 AA on the widget, My feedback and the admin screen; a keyboard-only submit (charter §5).
10. **Parity gaps to DISPOSITION, never to assume:**
    - NexusAI GET `/report` (L75) and GET `/summary` (L122) have no HPSM route (contract paths L4719-5315). RULED (cite it), PARTIAL (the sweep as a substitute), or NOT MET.
    - NexusAI stores a page URL; HPSM stores the page path only (README L42). Cite a ruling, or mark it PARTIAL.
    - The sweep's Jira half is UNAVAILABLE (sweep L15-18).
11. **Migration 0016 upgrade path:** §3.3.
12. **The builder's claims, re-derived** (README L53-57: e2e 92/92 including 12 feedback tests; axe 0 violations; body-size proof; G9 mutants).
    - Run the three feedback e2e specs on YOUR stack.
    - Plant one defect per spec in YOUR clone, and watch each go RED.

**MET needs runtime evidence.** READ ONLY cannot carry MET alone.

### 3.2 SECURITY - attack plan (the feedback surface)
**Every probe states FAIL first and has a POSITIVE CONTROL proving the instrument fires.**

| # | Attack | FAIL if | Control |
|---|---|---|---|
| 1 | **Tenant isolation on every feedback id.** create (a `tenant_id` you hold no role in; the platform tenant, routes L262-263), list, get, update, triage, delete, attachment download. Each with a foreign id, a nonexistent id, UPPER/mixed case, braces, a `urn:uuid:` prefix, and a foreign attachmentId under your own feedbackId | anything but a 404 byte-identical (status, body, headers except date/request id) to a nonexistent id; any 500 (W4B-m1 closed at `9b8ea76`: a `urn:uuid:` 500 on feedback is NEW) | your own id in your own tenant gets 200 |
| 2 | **Role matrix:** 7 roles x 7 operations, tenant-side and platform-side (`?tenant_id=`) (authz.ts L72-75, L93-99). Only platform_admin lists a tenant, triages, updates, deletes. `consultant` cannot read `consultant-2`'s item in the SAME tenant, nor any other tenant's. auditor and customer_approver submit and read only their own (L72-75). A non-platform caller on a platform operation gets 403 before any lookup (routes L637) | a denied cell succeeds server-side; a 403-vs-404 difference reveals existence | the permitted role succeeds on the same request |
| 3 | **RLS as `pc_app`** on `pc.feedback_item` / `pc.feedback_attachment` (0016 L107-114). With the GUC set to tenant A: SELECT, INSERT, UPDATE and DELETE of tenant B rows; the GUC unset or garbage; an INSERT carrying B's tenant_id; an UPDATE moving your own row's tenant_id to B (grants L149-154) | a row crosses; a write commits; a table is not FORCED | the same statement in-tenant succeeds |
| 4 | **Immutability triggers** (0016 L120-141), as `pc_app`: change an identity column (L120-121); change anything after `deleted_at` is set (L126-135); DELETE an item, although DELETE is granted (L138-139, L148); UPDATE or DELETE an attachment (L140-141) | any of them commits | a permitted triage-column UPDATE on a live item commits |
| 5 | **Attachments.** Content-type spoofing (a PNG header named `.exe`, HTML named `.png`, SVG, a PDF/HTML polyglot). Filename traversal `../../x`, NUL, CR/LF, quotes and `;` (Content-Disposition injection, feedback-attachments.ts L194-196). 10 MiB and 10 MiB + 1 byte. The request at 53,477,376 bytes and above; through the edge at 52m and 52m + 1. A zero-byte file. 6 files. Binding: A's attachment downloaded by another user, tenant or role. The download is bearer-only; routes L392 drops a download token from page URLs. If you find ANY link or token path for a feedback attachment, probe forgery, replay and expiry; if none exists, record that (READ ONLY + one probe without a bearer) | an unsupported type is stored; a header is injected; a storage key escapes the tenant prefix; any 500; a download succeeds for the wrong principal | a valid PNG round-trips with a matching sha256 and `application/octet-stream`, `attachment`, `nosniff`, `private, no-store` (routes L630-633) |
| 6 | **Credential-shaped text** in EVERY feedback free-text field: title, description, page path (routes L403), admin notes and triage fields, and the attachment filename. Grep the DB dump, logs, audit, sweep output and every response for the marker | the marker persists or is echoed; a 500 | ordinary prose (§2a) passes |
| 7 | **JSON depth:** a PATCH/triage body nested deeper than 64; a multipart field carrying deep JSON | anything but 422 `PAYLOAD_TOO_DEEP` (secrets.ts L13; S-m3 closed at `a4172b3`); a 500 | a 10-deep body gets its ordinary answer |
| 8 | **XSS and injection:** `<script>`, `<img onerror>`, `javascript:` in title, description, page path, filename and admin notes. Render them in My feedback AND the admin screen with the Playwright browser, watching for dialogs, console and network. SQL fragments in filters and sort | a payload executes; SQL error text leaks | a benign value round-trips; a `dangerouslySetInnerHTML` planted in YOUR clone makes the browser probe fire. **No browser available: NOT TESTED, never inferred from source** |
| 9 | **CSRF-equivalent:** any state-changing GET on a feedback path; a bearer in a cookie or URL; credentialed CORS with `Origin: evil` | a GET mutates; a token in a URL or cookie; `Access-Control-Allow-Credentials` with a reflected origin | a PATCH with the bearer succeeds |
| 10 | **Audit:** every action writes its event in the item's tenant chain: `feedback.created` (L479), `feedback.listed` (L546), `feedback.viewed` (L567), `feedback.attachment_downloaded` (L617-624), `feedback.updated` (L710), `feedback.triaged` (L729), `feedback.deleted` (L746). The chain still verifies afterwards | an action with no event; an event in the wrong tenant; the chain breaks | an untampered chain verifies |
| 11 | **Error leakage** on authenticated feedback calls: 400, 403, 404, 409 (idempotency), 413 (API and nginx), 422, and 503 `OBJECT_STORE_UNAVAILABLE` / `FEEDBACK_ATTACHMENT_INTEGRITY_FAILED` (stop MinIO or alter one object on `policy-composer-qa-fb-fresh` ONLY) | a stack trace, SQL, a path, a storage key, a host, or another tenant's existence | a known 404 body is recorded |
| 12 | **Resource, BACKLOG.md L52** (each upload held whole in API memory, about 51 MiB). Measure api memory (`docker stats --no-stream`) before, during and after ONE maximum-size submission, then at most 3 concurrent maximum-size submissions, ONCE. **Never a flood:** no loops, no retries beyond §1's re-run rule | the api crashes, restarts, or does not return to baseline | a small submission's footprint |
| 13 | **Edge route table:** `/api/feedback` answers 401 `UNAUTHENTICATED` without a bearer (README L14). The 52m exact location widens no other path: `/api/feedback/`, `/api/feedback/x`, `/api/feedbackX`, `/api/feedback?x=1`, `/api/other` | a body over the `/api/` limit accepted on another path; a feedback path answers without auth | on the exact path, a body between the API cap and 52m reaches the API (JSON problem detail, not nginx HTML) |

**Probe 6 and the DECLARED gap.** BACKLOG.md L45 says the credential-shapes GUARD TEST cannot see `createFeedback`'s upload route.
- MEASURE the upload's scan at runtime yourself.
- If the route scans every field, the guard gap is KNOWN: rate it, do not re-report it as new, and do not re-litigate the guard's design.
- If the route misses a field, that is a NEW finding.
- The detector's syntax gaps (A-m1, A-p2, W4B-m3; BACKLOG.md L869) are KNOWN.

### 3.3 Migration 0016 - the 15 -> 16 upgrade (YOUR stacks only)
- **Oracle:** M16 REPORT L12-18.
  - 0016 creates `pc.feedback_item` (L14) and `pc.feedback_attachment` (L71), with RLS forced (L107-114), 1 function + 4 triggers (L120-141) and column grants to `pc_app` (L148-154).
  - The only link out is the FK to `pc.tenant`. **Nothing existing is altered.**
  - Read-only cross-check: `git --no-optional-locks diff --name-status 9b8ea76..d0466da -- packages/db/migrations/ packages/db/src/migrate.ts` lists ONE added file.
- **Measure on `policy-composer-qa-fb-up`:**
  - at `9b8ea76`: `pg_dump --schema-only` (catalog A), plus row counts per table;
  - upgrade to `d0466da`; the migrate log must say `migrations applied: 0016_feedback.sql; already applied: 15`;
  - dump again (catalog B).
  - **FAIL if** B minus A holds anything other than the 0016 objects, or if any pre-existing object's definition, grant, policy or row count changed.
- **Compare** catalog B with `policy-composer-qa-fb-fresh`'s schema. **FAIL if they differ.** That is a finding; do not reconcile.
- **Pre-existing data survives:** the tenant, engagement and sign-ins created at base read identically after the upgrade.
- **KNOWN, not re-reported:** redeploying `9b8ea76` over a 0016 database fails, because the migrator refuses (M16 REPORT L5-10, L25-28). The rollback policy is lane TK's.
  - You MAY reproduce the refusal ONCE on `policy-composer-qa-fb-up` if it is cheap, then roll forward.
  - **Never attempt R2 (the reverse SQL, `reverse-0016.sql`): that is Kam's word only (S45 answer L17).**

## 4. Credentials (pointer only)
- **No live credential is needed for a LOCAL gate, and none is in scope.** Read NOTHING under `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/4_Credentials/`. The launcher exports its identity dirs only for isolation. Run no `az`, no `gh`.
- **Personas:** the idp-mock's synthetic users, `apps/idp-mock/src/app.ts`:
  - the seven roles at L9-18;
  - users at L48-73: `platform-admin`, `content-manager`, `consultant`, `security-reviewer`, `bridge-operator`, `auditor`, `consultant-2`, `customer-approver-a`, `customer-approver-b`;
  - tokens from YOUR stack's `POST /idp/token` (L121-150), e.g. `http://127.0.0.1:21480/idp/token`;
  - create a second customer tenant through the product's own admin flow on your stack.
- **Tokens are credentials:** never in the report, the evidence or the mail. Write "credentials present".

## 5. State-mutation & cleanup
- **Sanctioned:**
  - your own clones;
  - your two compose projects and their volumes, plus the CI's own throwaway project;
  - the synthetic tenants, users' sign-ins and feedback items you create on YOUR stacks;
  - superuser, trigger and object-store tamper on `policy-composer-qa-fb-fresh` only.
- **Reachable:** submitted (with and without attachments), triaged, updated, soft-deleted, past-retention (constructed; say how), and the 15 -> 16 upgrade.
- **Gaps (documented, not failures):** real Jira ticketing (the sweep's Jira half is UNAVAILABLE); purge (ruled out); any live or Azure behaviour (out of scope).
- **Never `rm`:** a new `mktemp -d` per attempt; quarantine, never removal; `${X:?}` on every expansion.
- **END:** stacks down with volumes KEPT. List volumes before and after, and every project, volume and image you created.

## 6. Output boundary / 6a. Evidence class
- **Findings, reports and recommendations ONLY** (Kam, 2026-08-11). Describe the fix-shape and the regression test in prose.
- **Evidence class on every finding and every row:** MEASURED AT RUNTIME (LOCAL) / PROBED / READ ONLY.
- **Build the schema the product deploys** (compose `migrate`). If a suite builds a different one, that is a finding; do not reconcile.

## 7. Known-fragile / known-changed
**RULINGS IN FORCE** (§2): 08:07:30Z (i)-(iii) plus amendment 2; 09:14:10Z naming (b); no purge. A mismatch is a finding.

**KNOWN AND DECLARED at d0466da.** A mismatch with a declaration is a finding; the declared item itself is not new.
- **Line numbers** in BACKLOG.md were read 2026-09-13 13:45Z. The README cites `:51` and `:848`; those entries now sit at L52 and L849. Cite by title if they move again.
- BACKLOG.md L45: the credential-shapes guard cannot see the upload route (§3.2 probe 6: measured, not re-litigated).
- BACKLOG.md L52: orphan objects on a failed upload or an `Idempotency-Key` race; about 51 MiB per upload held in API memory (§3.2 probe 12).
- BACKLOG.md L849: no purge; expiry is report-only, by ruling.
- `scripts/feedback-sweep.sh` L15-18: the Jira half is UNAVAILABLE.
- BACKLOG.md L804: e2e tenants accumulate (not torn down).
- README L69: the pre-existing skip `packages/renderers/test/measure-preview.test.ts:30`.

**KNOWN FROM PRIOR GATES THAT STILL APPLY at d0466da.** Copied from the model brief §7 and BACKLOG. Each is still an open `- [ ]` at read time, and no first-parent merge in `caf63fd..d0466da` claims to close it. **Only these touch the feedback surface:**
- No CSP anywhere; S-m1: no nosniff, frame protection, HSTS, or Cache-Control on tenant JSON, and a `Server:` banner (BACKLOG.md L136-138, L843). Rate their IMPACT on the feedback screens; do not report their absence as new.
- S-m2: internal services are routed onto the edge (BACKLOG.md L129).
- MinIO ROOT credentials in the api (BACKLOG.md L688). The same client stores feedback attachments.
- A stored-output object orphaned on commit failure (BACKLOG.md L695). Feedback's sibling is L52.
- A credential-shaped display name on storeOutput answers 500 (BACKLOG.md L709). **Feedback uses the same display-name helper (`printableDisplayName`, routes L22), so the same 500 on a feedback path is a NEW instance of a KNOWN class:** report it, citing L709.
- The credential detector's syntax gaps, round 3 (BACKLOG.md L869).
- Q2(a) no signing key and "Not signed" outputs: still in force, but outside this gate.

**CLAIMED CLOSED between caf63fd and d0466da** (first-parent merges; NOT gated here):
- W5-M1 `f80ebc4`;
- W6-M1/m1/m2/m3 `47305ce`;
- W5-M3 and W5-m5 `693a5db`;
- W5-M2 `87c0026`;
- W4B-m2 `246fb92`;
- S-m3 (deep JSON gives 422) `a4172b3`;
- W4B-m1 (`urn:uuid:` gives 404) `9b8ea76`.
- **The last two are ORACLES on feedback** (§3.2 probes 1 and 7). Their regression on a feedback operation is a NEW finding, not KNOWN.

**Still owed:** a KNOWN item that silently gives a WRONG RESULT on the feedback surface, or a security gap reachable there, IS a finding. Mark it "KNOWN, re-rated", with its BACKLOG line.

## 8. Logistics
- **One session, LOCAL ONLY.** Order:
  1. clone, docker ledger START;
  2. `policy-composer-qa-fb-up` at base, data, the upgrade (§3.3);
  3. `policy-composer-qa-fb-fresh`;
  4. SECURITY probes 1-6;
  5. DELIVERABLES rows 1-8;
  6. SECURITY probes 7-13;
  7. e2e + axe;
  8. sweep and retention;
  9. CI (optional);
  10. the rest.
  - Anything unfinished is NOT TESTED, with the reason.
- **Head readings** of the original repo at start, mid and end: SHA + branch + time, via `git --no-optional-locks`. S45's lanes are working, so main may move.
- **Launch:** Tuesday runs the launcher in one tmux pane (`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/HPSM-feedback' "bash '<launcher>'"`), never nohup. The launcher sets `CLAUDE_CONFIG_DIR=/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.claude`, and HPSM's own `AZURE_CONFIG_DIR`/`GH_CONFIG_DIR` for isolation only.
- **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-d0466da-feedback-tier1/report.md` (a NEW path; the launcher refuses if it exists). In this order:
  - **BLUF:** both verdicts + severity counts on the feedback surface;
  - **findings:** FOUND / TESTED / HOW, oracle, evidence class, Blocker / Major / Minor / Polish with justification (priority is the humans' call);
  - the matrix;
  - the security table, with each control's result;
  - migration 0016;
  - **NOT TESTED**;
  - the docker ledger; the head readings.
- **Findings-only:** never fix, commit or file tickets. Run long commands in the FOREGROUND; never end a turn waiting on a background notice.
- **No inbox:**
  - where the brief is silent, take the safest reading and record it;
  - approval-class work (anything on the live demo, R2, money, external comms, anything irreversible) is not done. List it under NOT TESTED.
- **Before any mail:** grep the evidence folder and the report for bearer tokens (`eyJ`), stack passwords and your planted markers, with a positive control, and record that the grep ran.
- **INTERIM mail AT ONCE for any Blocker** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] INTERIM BLOCKER — Policy Composer FEEDBACK feature @ d0466da (tier 1)`. Then keep testing.
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`:
  - subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer FEEDBACK feature @ d0466da (tier 1)`;
  - first line `DELIVERABLES: <GO | GO WITH FINDINGS | NO GO> · SECURITY: <GO | GO WITH FINDINGS | NO GO>`;
  - then the severity counts on the feedback surface, and the report path.
  - **Datasec's coordinator is TUESDAY; never `wednesday-agent@`.**

PROVENANCE:
- Kam's commission, verbatim, 16:53:31 AEST | `TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md` L56; prompt log `TUESDAY/1_Project_Definition/Discovery/00_prompt-log.md` L2291-2292 (records 16:55); S43 brief L6 | read 2026-09-13 23:48 AEST
- Gate commission (feedback-scoped, tier 1, local, 21480-21599, first lock claim, live-upgrade conditions, no R2) | S45 answer L1-17; pickup L76-80 | read 2026-09-13 23:48 AEST
- READY FOR QA 13:40:24Z, the delta, rulings implemented, declared items, upgrade note | the S45 README, read whole | read 2026-09-13
- Head `d0466da` = `refs/heads/main` and reachable; 342 commits `afc10e9..d0466da`; 22 in `9b8ea76..d0466da`; 5 first-parent merges; origin/main `afc10e9`; 15 -> 16 migrations with one added file | `git --no-optional-locks` rev-parse / merge-base / rev-list / log --first-parent / ls-tree / diff --name-status | read 2026-09-13 13:43-13:48Z
- Rulings 08:07:30Z and 09:14:10Z | HANDOVER-S43 L101, L114, L127; HANDOVER-S44 L43 (grep -n) | read 2026-09-13
- BACKLOG.md L45, L52, L129, L136-138, L688, L695, L709, L804, L843, L849, L869 | grep -n on the HPSM worktree (HEAD `fff3969`, BACKLOG.md clean) and on commit `96eb89a` (same lines) | read 2026-09-13 13:45Z
- HPSM implementation lines | `git show d0466da:<path>` of routes/feedback.ts, authz.ts, document.ts, openapi.json, feedback-attachments.ts, feedback-multipart.ts, secrets.ts, 0016_feedback.sql, edge.nginx.conf, compose.yaml, ci.sh, test-db.sh, idp-mock app.ts, router.tsx, FeedbackWidget.tsx, feedback-sweep.sh | read 2026-09-13
- M16 facts | M16 REPORT.md L1-70 | read 2026-09-13
- NexusAI parity lines | grep -n of the five NexusAI files (NexusAI 2_Project_Files at `cd2b543`); S43 brief L32-46 | read 2026-09-13
- KNOWN still applying and claimed-closed | model brief `2026-09-13_hpsm-composer-09c1591-brief-acceptance-security-tier1.md` L162-213; BACKLOG open checkboxes; `git log --first-parent caf63fd..d0466da` | read 2026-09-13
- Ports 21480/21495/21580 free and no listener anywhere in 21480-21599; 137 volumes; the Playwright image present; docker answers within 30 s; the lock file exists | lsof, docker volume ls, docker image inspect, docker info, ls | read 2026-09-13 13:44-13:47Z

SELF-CHECK: re-read end-to-end for contradictions; LOCAL ONLY throughout; no live host named, and no other stack named by port except the S45 lane ranges in §1's leave-alone list; the report path and verdict subject agree with the launcher | 2026-09-13 23:55 AEST
