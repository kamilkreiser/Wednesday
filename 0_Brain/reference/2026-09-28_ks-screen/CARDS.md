# Card verification — the four "card-for-Kam" flags from SCREEN.md

**Date:** 2026-09-28 · **For:** Wednesday · **Client:** Secuura/Blockchain only
**Code read at:** develop `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817` ("KS-888: a mint whose key save fails…", #1322), via `git show` / `git grep` in the no-checkout clone. All paths are under `Blockchain/Dev/`.
**Tickets read:** in full from Linear (description + every comment, `comments(first:50)`, sorted client-side by `createdAt`). Read-only.
**Prior-ruling search:** `decision_queue.sh list ruled` (449 lines) and `list open` (3 open cards), grepped for each ticket id and subject words; `decisions.json` full-text grepped for the same (control: 1,074 `secuura-` hits, so the grep can see); `0_Brain/reference/` grepped for dated folders.
**Nothing was changed.** No ticket comment, no card posted, no push.

## Summary

| Ticket | Verdict | Card? |
|---|---|---|
| KS-1351 item 1 | **Agent-decidable.** One of the two options would break a live screen, so it is not a real choice. | No |
| KS-1335 | **Agent-decidable.** The "published field" premise is overstated. | No |
| KS-1227 | **Agent-decidable.** It is test-only. | No |
| KS-1054 | **Kam's**, but only for the F-928-2 half (should a failed migration stop the gateway). The stage ordering is agent work. | **Yes** (1 card) |

Governing rule for the three agent verdicts: the autonomy grant `0_Brain/learnings/2026-08-07_autonomy-grant-ship-decisions.md`, items 3–4 (decide on technical grounds). None of the three touches production, money, external comms, anything irreversible, a scope change or a published contract, which are that file's stop-list. Each chosen default leaves every served response and every screen unchanged.

---

## 1. KS-1351 item 1: declare the revocation fields on `VCCredentialStatus`, or stop writing them?

**Ticket:** Backlog, P3, filed 2026-09-27 15:04, 0 comments. It asks for the fields and the repository to "agree … decided rather than patched".

### Premises, verified at d9ce1403
- **The type has no revocation fields.** `packages/shared/src/vc/types.ts:27-33` declares `id`, `type`, `statusPurpose?`, `statusListIndex?`, `statusListCredential?`. **VERIFIED.**
- **`revoke()` writes them.** `services/vc-issuer/src/repositories/credentialRepo.ts:239-247` sets `revoked: true`, `revokedAt`, `revocationReason` inside `credentialStatus` and casts `as SecuuraCredential`. It persists that at `:255-259`. **VERIFIED.**
- **The tests read them.** `services/vc-issuer/src/__tests__/credentialRepo.test.ts:72`, `:142-144` (the four TS2339 sites). `:32` writes `revoked: false` in a fixture literal. **VERIFIED.**
- **Item 2.** `credentialRepo.ts:95` is `let result`, assigned once. **VERIFIED.**

### Found at source, not in the ticket (this is what decides it)
- **A live screen reads the field.** The issuer portal shows its "revoked" state from `credential.credentialStatus?.revoked`: `frontend/issuer/src/components/CredentialCard.tsx:119` and `CredentialDetailModal.tsx:84`. It declares its own local type with `revoked?: boolean` (`CredentialCard.tsx:60-61`). The whole-tree grep for `credentialStatus?.revoked|revokedAt|revocationReason` finds only these 2 frontend sites and the 4 test sites (control: `credentialStatus` appears in 15 files).
- **The field is on the wire.** `GET /api/credentials/:id` returns the stored credential as is (`services/vc-issuer/src/routes/credentials.ts:264-274`). The spec publishes `credentialStatus` as an open record (`vc-issuer.openapi.ts:123`, `z.record(z.string(), z.unknown())`).
- **So "stop writing the fields" would break the issuer portal's revoked display.** It would also change a served response. "Declare the fields" changes no runtime behaviour. Only the declare option is really open, so this is not Kam's.

### ⚠ A separate observation that needs measuring, not a card
- `POST /api/credentials/:id/revoke` (`credentials.ts:284-309`) calls only `credentialRepo.revoke()`. It does not touch the status list.
- The verifier decides revocation **only** from the status list (`packages/shared/src/vc/verifier.ts:112-120`, `:431-450`). It does so only when a `statusListResolver` is configured.
- `statusListResolver` is declared (`verifier.ts:24`) and read (`:435-437`), but **no caller wires one**. `git grep statusListResolver` over `packages/shared/src` and `services/vc-issuer/src` finds only those three verifier lines.
- The `POST /api/credentials/verify` route passes `checkStatus: true` and no resolver (`credentials.ts:338-342`).
- **Read from source, NOT measured:** a credential revoked through that route may still answer `verified: true`.
- Linear literal search for `statusListResolver`: 0 hits, so no ticket covers it.
- Per `learnings/2026-09-11_before-carding-a-measurement-check-it-has-not-already-run.md`, this needs a measured red on a seat before it becomes a ticket or a card. It must not go to Kam as a claim yet.

### Prior ruling
- None on KS-1351 or `VCCredentialStatus`. 0 hits in ruled, open and `decisions.json`.
- Nearest: `secuura-ks1116-presentation-credential-ownership-model` (bind-creator, 09-13) and `secuura-ks692-status-revoke-interim-posture` (a, 09-16). Both are about who may revoke or read, not the type shape. Neither decides this.

### Verdict
**Agent-decidable** under the autonomy grant, items 3–4. The chosen default has no runtime or contract change.

Default for the seat:
- Declare `revoked?: boolean`, `revokedAt?: string`, `revocationReason?: string`. Prefer a Secuura extension of the status type (`SecuuraCredentialStatus extends VCCredentialStatus`, used by `SecuuraCredential`) over widening the W3C-shaped base type in `packages/shared`.
- Item 2 is `const` at `credentialRepo.ts:95`.
- The TS2339 count over an `exclude: []` program goes 4 → 0.

---

## 2. KS-1335: Teams-notify rotation. Redefine `lastSentAt`, or add a `last_attempted_at` column?

**Ticket:** Backlog, P3, filed 2026-09-26 00:11, 0 comments.

### Premises, verified at d9ce1403
- **The rotation key.** `services/m365-integration/src/index.ts:1252-1256`: `ORDER BY last_sent_at ASC NULLS FIRST, created_at ASC LIMIT $2`. **VERIFIED.**
- **Written only on success.** `index.ts:1337-1340` writes `last_sent_at = NOW()` inside `if (resp.ok)`. The guard-blocked / failed branch (`:1321-1334`), the non-ok branch (`:1341-1342`) and the catch (`:1343`) do not write it. **VERIFIED.**
- **The known limit is written in the code** at `index.ts:1246-1251` and pinned by R3 in `src/__tests__/ks934-teams-notify-request-path-bound.test.ts` (header `:21`, `:312`). **VERIFIED.**
- **DDL in two places.** `docker/init/06-m365-tables.sql:63`, and `services/api-gateway/src/startup-migrations.ts:361` plus the guarded add-column at `:526-527`. **VERIFIED.** The same guarded `information_schema` pattern that shape 2 needs is already in the file (`:522-528`).

### Premises that are WRONG or overstated
- **Route name.** The ticket says `GET /api/teams/webhooks`. The field is actually returned by `GET /api/teams/webhook-config` (`index.ts:1161-1176`, `lastSentAt: r.last_sent_at` at `:1172`). The string `/api/teams/webhooks'` gets 0 hits in `index.ts` (control: `webhook-config` gets 6).
- **"Published field" is overstated.** `lastSentAt` is **not** in the published schema:
  - `M365TeamsWebhook` in `services/m365-integration/src/m365-integration.openapi.ts:268-278` has `id, channelName, webhookUrl, organizationId, events, createdAt`, and `.passthrough()`.
  - The generated `docs/openapi/secuura-api.yaml:5009-5030` matches.
  - It reaches the wire only through passthrough.
  - **No consumer in the tree:** `git grep -i lastSentAt` over `Blockchain/Dev` finds 1 file, `index.ts` itself. The admin M365 wizard (`frontend/admin/src/components/M365SetupWizard.tsx`) never reads it.

### Prior ruling
- None. 0 hits for KS-1335, `last_sent_at`, `lastSentAt`, `teams/notify`, `m365`, `last_attempted_at` in ruled, open and `decisions.json`.
- The parent KS-934 has one ruled card (`secuura-934-blocks-every-push-needs-one-approval`, a merge approval, unrelated).
- No dated reference folder.

### Verdict
**Agent-decidable** under the autonomy grant, items 3–4.
- Shape 2 (`last_attempted_at`) is additive, nullable and unused by anything else. It follows the existing guarded-add pattern and leaves the returned `lastSentAt` meaning exactly as it is.
- The ticket itself calls shape 2 "the honest one".
- Nothing is published, client-facing or irreversible. The column only reaches production through a normal deploy, which stays Kam's step under never-touch-prod.

Default for the seat:
- Shape 2, with DDL at both sites and the backfill guarded like `:522-528`.
- Order by `last_attempted_at ASC NULLS FIRST, created_at ASC`.
- Write it on every attempt.
- Rewrite R3 in the same change, plus the ticket's "second call reaches past the limit" test.

---

## 3. KS-1227: the ks1072 anchor-store witness. Keep counting every stub request, or filter by document path?

**Ticket:** In Progress, P4.
- Comment 2026-09-27 07:09: PR #1304 open at `c8233156f`.
- Comment 2026-09-27 13:21: merged as `7409da5c9` on the gate32 GO. "NOT Done … The keep-vs-filter decision this ticket raises is still open."
- `git merge-base --is-ancestor 7409da5c9e03 d9ce1403` → true, so the merge is in the code read.

### Premises, verified at d9ce1403 (`services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts`)
- **Counts every stub request.** `postTier2` (`:113-130`) pushes every `req.url` (`:116`) and asserts the list equals exactly one read of this document (`:128`). **VERIFIED.**
- **The listener leak is already fixed.** Detach is in a `finally` (`:119-125`), and R2 (`:201-205`) pins one listener after a status red. **VERIFIED.** The ticket's loose end 2 is closed.
- **The current rule is pinned.** R1 (`:190-200`) forces a second, non-hit request to reach the stub and expects the witness to red. So a hit-only filter now reds. Its comment (`:191-192`) already says "the witness counts EVERY stub request, as merged". **VERIFIED.** Loose end 3 is closed.
- **Still open:** the choice itself, and the optional reword of the `:128` message ("tier 2 answered", when the witness proves tier 2 was *asked* once).

### Prior ruling
- None. 0 hits for KS-1227, `postTier2`, `witness`, `anchor-store` in ruled, open and `decisions.json`.
- `reference/2026-09-22_round18-census/pool18_list.out:45` lists it as test-only (+24/-8, `prod=[]`). That is a census, not a ruling.
- Nearest: `secuura-ks1171-when-is-an-anchor-absent` (c, 09-25) is a product anchoring rule, not this test helper.

### Verdict
**Agent-decidable** under the autonomy grant, items 3–4.
- It is one test helper in one test file, with no product, contract, client or production effect.
- The ticket calls it "Test-only, a tidy-up of one helper".

Default: **keep** "every stub request counts".
- Reason: it fails closed. A stray request reds instead of hiding (R-1029-2), and R1 already pins it.
- Record the choice in the helper's comment next to `:125-128`, reword `:128` to "tier 2 was asked once", then close KS-1227.
- A filter would only be worth it if a future file points `ANCHORING_SERVICE_URL` at this stub for a second reason. Today only R1 does, on purpose.

---

## 4. KS-1054: boot-migration stage order, and how a first-boot failure is made visible

**Ticket:** Backlog, P2, filed 2026-09-09.
- 1 comment (2026-09-09 13:42) split the tenant-DB half out to KS-1055.
- The ticket says F-928-2 (migration failure is log-only) "is a design decision with deploy consequences and is **Kam's**, tracked separately".
- **"Tracked separately" is not true on the board.** A Linear literal search for `F-928-2` finds only KS-1054 and KS-1125. KS-1125 (Done) says: "F-928-2 (should `failed` gate readiness or the boot) is the CTO's design call, not this ticket." No ticket owns it.

### Premises, verified at d9ce1403
- **The file stage runs before the CORE stage.** In `services/api-gateway/src/startup-migrations.ts`, stage 1 (files) is at `:947-990` and stage 2 (`CORE_MIGRATIONS`) at `:992-1003`. The header (`:8-21`) documents that order. **VERIFIED.**
- **039 depends on a table only CORE creates.**
  - `oauth_apps` is created in `CORE_MIGRATIONS` (`startup-migrations.ts:477`) and in `docker/init/08-oauth-tables.sql`. No `migrations/*.sql` file creates it.
  - `migrations/039_rls_fail_closed.sql:225-228` has an **unguarded** `RETURNS SETOF oauth_apps`, while `:162-165` is guarded.
  - This matches "type oauth_apps does not exist". **VERIFIED** from source. The 7-failure boot-1 count is the QA gate's 09-09 measurement, relayed and **not re-run here**.
- **Failure is log-only on the gateway.**
  - `runStartupMigrations(): Promise<void>` (`:930`), so failed counts only change log level and wording (`:966-972`, `:999-1003`).
  - Its only call site wraps it in try/catch → `log('warn', 'Startup migrations skipped')` (`services/api-gateway/src/index.ts:1188-1194`).
  - **VERIFIED.**
- **Tenant databases get CORE only.** `startup-migrations.ts:1186`. **VERIFIED.** That is KS-1055, the split-out half.

### Premises that are STALE
- **"`run-migrations.sh` exits 0 when migrations fail" is no longer true.**
  - Since KS-1031 (#1183, commit `16c59d1ad`) it exits 3 (`scripts/run-migrations.sh:22-26` header, `:171-190`).
  - Compose services wait on `migrations: condition: service_completed_successfully` (`docker-compose.yml:545-546` and the other service blocks).
  - So **the local compose stack already stops on a failed migration**. Only the gateway's own start-up run (the path Azure deploys use, header `:8-14`) is still log-only.
- **"CI and local stacks" as the exposure is probably too wide.** A fresh compose volume gets `oauth_apps` from `docker/init/08-oauth-tables.sql` before either migration path runs. Read from source, not measured.
  - The window that remains is a gateway-only first boot on an empty database: a new Azure environment, a DR restore into an empty server, and tenant databases (KS-1055).

### Prior ruling
- None on KS-1054 or F-928-2. 0 hits for KS-1054, F-928, `039_rls`, `boot 1`, `migration failure` among Secuura cards (ruled/open/`decisions.json`). The one `boot 1` hit is a NexusAI card.
- **Related, not a ruling:**
  - Kam ruled (c) on `secuura-ks1304-withtenant-tenant-pool-and-admin-writes` (09-26, "start planning the database").
  - The resulting plan `reference/2026-09-26_secuura-tenantdb-plan/PLAN.md:112`, `:137` puts "fix the boot-1 order (KS-1054)" and "make the runner exit non-zero" into Phase 1. That plan is a recommendation and has **not** been ruled.
  - Kam's nearest precedent in spirit is `secuura-ks1194-failed-save-answers-200` → **fail-closed** (09-17).

### Verdict
**Split.**
- **Stage ordering is agent-decidable** under the autonomy grant, items 3–4. It is a correctness fix that can be proved on a fresh database with a two-sided drill (039 applies on boot 1 and the policy has the fail-closed shape). It does not reach production until Kam's normal deploy step. Pick between the ticket's shapes on technical grounds: run CORE before files, or guard 039's `oauth_apps` function the way `:162` already is.
- **F-928-2, whether a failed migration should stop or flag the gateway, is Kam's.** It is a production-availability trade-off: a migration that fails every boot, as 002/005 once did, would hold production down under the strict option. The ticket and KS-1125 both name it his, and no ruling exists. **Card below.**

```json
{
  "id": "secuura-ks1054-f9282-migration-failure-visibility",
  "client_project": "Secuura/Blockchain",
  "title": "KS-1054: when a database migration fails at start-up, should the gateway keep serving, flag it on its health check, or refuse to start?",
  "bluf": "No action needed unless you disagree with the default. Today a failed migration on the gateway is only a log line (startup-migrations.ts:930, index.ts:1188-1194). So a brand-new database can start with tenant isolation open until its second start (KS-1054; QA measured 09-09, not re-run). Local stacks already stop on a failure (run-migrations.sh:190, since KS-1031). I recommend (a): keep serving, but make /health report the failure, because the deploy scripts already check /health. Either way we fix the start-up order now.",
  "options": [
    {
      "key": "a",
      "label": "Keep serving, flag it on /health",
      "detail": "The migration run returns its failed count. /health reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it and the deploy reads as failed. The running service is not stopped."
    },
    {
      "key": "b",
      "label": "Refuse to start",
      "detail": "Any failed migration makes the gateway exit non-zero, the same as local stacks since KS-1031. Strictest. Risk: a migration that fails on every start would keep production down until it is fixed."
    },
    {
      "key": "c",
      "label": "Leave start-up log-only, check new databases instead",
      "detail": "No change to start-up. A new environment or tenant database is not declared ready until a pg_policy check shows the fail-closed shape (the ticket's fix shape 3). This covers the known cause but nothing new."
    }
  ],
  "recommended": "a",
  "default_action": "If you do not answer: nothing about start-up behaviour changes. Wednesday briefs a Claude seat to fix only the stage order (proved on a fresh database), and failures stay a log line until you rule."
}
```

---

## Notes for Wednesday
- **Only one card comes out of the four.** The other three have measured defaults that an agent can build under the autonomy grant. Report them as decisions taken, not as questions, per that grant's "report what I decided".
- **KS-1351's side observation** (revoke via `/api/credentials/:id/revoke` may not reach verify, because no `statusListResolver` is wired) is the most serious thing in this pass. It is read from source only. Measure it on a seat before anything is filed or carded.
- **KS-1054's "tracked separately"** points at no ticket. If Kam rules, the ruling should be delivered into KS-1054 itself, since no F-928-2 ticket exists.
