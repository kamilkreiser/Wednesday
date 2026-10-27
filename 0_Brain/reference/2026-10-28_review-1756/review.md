# Review: PR #1756 (KS-955 product half): gateway vouch on hand-built originate forwards + bootstrap-env generates GATEWAY_VOUCH_SECRET

- **Reviewer:** tier-1 code reviewer (findings only), commissioned by Wednesday ~10:2x AEDT 2026-10-28
- **Started:** Wed 28 Oct 2026 10:28:54 AEDT · **Ended (final pin read):** Wed 28 Oct 2026 10:38:23 AEDT
- **Pins at start:** PR head `5d42cbd455184b33bad6a7a67bcf4b9071c63d31`, develop `8894c7486f82f6eb682fecb879791f53312537b1` (ls-remote, which matched the fetched refs)
- **Pins at end:** PR head `5d42cbd455184b33bad6a7a67bcf4b9071c63d31`, develop `8894c7486f82f6eb682fecb879791f53312537b1`. **Unchanged.** PR state open, `mergeable_state=unstable`, `updated_at` 2026-10-27T10:32:55Z.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/review-1756-1028/repo` (fresh; toplevel asserted before the fetch). It is left checked out at the local merge-preview commit `f46d484e3` (tree `6dd8c6741ef7`, parents develop + PR head).
- **Node:** v26.8.1 · vitest from the api-gateway lockfile · `TZ=UTC`
- **PR merge-base:** `65bea6ce6a5e` (the PR's recorded base). The diff is 17 files, +509/-44, which matches the PR.
- **Nothing was written** to GitHub, Linear, any box or any repo other than this clone.

## VERDICT: **APPROVE WITH NOTES**

The fix is correct, contained, red on develop and green on the head, and it merges cleanly. **It is also more urgent than the PR says.** The PR states the secret is "unset everywhere". In fact it has been set on api-gateway and originate on **both kintsugi and demo** since 19 and 20 Oct, so the wrong-tenant defect this PR fixes is **live on both boxes today**.

## Check table

| # | Check | Result | Evidence | Control |
|---|---|---|---|---|
| 1 | All five named forwards send the vouch | **PASS** | head `verification.ts:553` (workflow-approve), `:898` (POST /api/documents); `proxy.ts:586` (upload), `:671` (signatories), `:699` (third-party-verifiers); each calls `vouchHeaderFor('originate')` | the generic proxy (`proxy.ts:402-404`) uses the same helper; ks1041/ks1090 suites green |
| 2 | Other gateway→originate forwards without the vouch | **4 remain** (none carries trust headers) | `batch.ts:160` (/api/certifications, a WRITE), `batch.ts:208` (/api/verify), `platform.ts:330` (refresh-tenants), `verification.ts:183` (checkDocumentExists GET). All send `Authorization` only. | grep for `ORIGINATE_SERVICE_URL`, `services.originate`, `originate:4000`, `:6000` over `api-gateway/src` (non-test); `health.ts:209` probe and `system-status.ts` excluded as health-only |
| 3 | Vouch is sent only to originate | **PASS** | `originateForward.ts:46` `VOUCH_RECIPIENTS = {'originate'}`; hand-built sites hard-code the `'originate'` key and target `services.originate.url` | `ks1090-vouch-reaches-only-originate.test.ts` green at the merge preview |
| 4 | A client-supplied `x-gateway-vouch` is stripped at the edge | **PASS** | `trustHeaders.ts:43-44` pattern includes `gateway-vouch`; `index.ts:329-334` applies it to ALL inbound requests ahead of auth and routes (the batch mount is at `:809`) | `ks1041-vouch-header-strip` and `ks1041-edge-strip-wiring` tests green |
| 5 | Never echoed in a response, log or error body | **PASS (by reading)** | No new log line prints headers. Error logs carry `err.message` only (`proxy.ts:597`, `verification.ts:580/909`). originate deletes the header in all three branches (`gatewayProvenance.ts:221-238`: vouched deletes it, unvouched and unconfigured strip it), so it cannot be reflected downstream. | Not exercised at runtime. Logger redaction for the key is absent (P2b, deferred on KS-1083). |
| 6 | originate verifier is constant-time; unset vs set | **PASS** | `vouchMatches` (`gatewayProvenance.ts:172-179`): rejects an empty secret, checks length then `crypto.timingSafeEqual`. Unset → `unconfigured` → strip (FAIL-CLOSED). Set → ACTIVE: honours only a matching vouch. | `describeState` (`:185-198`): **ACTIVE iff the secret is truthy** |
| 7 | Unit red→green (gateway) | **CONFIRMED** | head: 3 files / 17 tests pass. develop `proxy.ts` + `verification.ts` put back in the head tree: **3 failed** (RED POST /api/documents, GET signatories, GET third-party-verifiers), 14 passed. Restored → green. | The unset-secret CONTROL cells and the 415 characterisation pass in both states, so the reds are discriminating |
| 8 | Unit red→green (bootstrap) | **CONFIRMED** | head script: 7/7. `BOOTSTRAP_SH=<develop's bootstrap-env.sh>`: **4 failed / 3 passed**, the exact cells the PR names | My extra arm: a pre-existing custom value was preserved (hash-equal); one key line |
| 9 | Full api-gateway unit suite on the merge result | **PASS** | local merge preview `f46d484e3`: **126 files / 1255 tests pass** (shared rebuilt, api-gateway `npm ci`); `tsc --noEmit` rc=0 | covers the PR's NOT-RUN item "the final merge commit itself" for the gateway unit layer |
| 10 | Mergeability vs develop `8894c7486f82` | **CLEAN** | `git merge-tree --write-tree` → `6dd8c6741ef7`, rc=0; the merge diffs from develop in exactly the PR's 17 files | overlap with develop since base: `verification.ts` (#1767 KS-1771, hunk at `:1064`, independent of `:544`/`:885`), the two Projects Documents HTML files and `systemTest/CLAUDE.md`. All auto-merged. |
| 11 | Prior review threads | **none** | 0 reviews, 0 review comments, 1 issue comment (linear[bot] linkback) | read via REST at start and end |

## Findings

### MAJOR
**None in the code.** The live-state point (Q3 below) is a factual error in the PR description that changes urgency. It is not a defect in the change.

### MINOR
- **m1. The docs and comments overclaim "every" originate forward.** `docs/ENVIRONMENT-VARIABLES.md:138` ("Every gateway → originate call carries the vouch"), `utils/originateForward.ts:20` ("Every originate forward now takes its vouch from here") and `originate/src/utils/gatewayProvenance.ts:91` ("by every hand-built originate forward") are all false at the head. Four hand-built originate calls still go out unvouched: `routes/batch.ts:160` and `:208`, `routes/platform.ts:330`, `routes/verification.ts:183`. Today none of them forwards a trust header, so vouching them would change nothing, and the code is right to leave them. The sentences should say "the five forwards that carry trust headers". Otherwise the next reader will assume a new trust-header forward is covered.
  - **Related, not this PR's scope:** `POST /api/batch/certifications` (`batch.ts:160`) is a tenant-scoped WRITE that forwards no `x-tenant-id`, so originate files it under `DEFAULT_TENANT_ID` whether or not the secret is set (originate `requestTenant.ts` → `certifications.ts:108`). It is the same family as KS-1084, and KS-1083's call-site table already lists it as "no, see KS-1084". It is worth confirming a ticket holds it.
- **m2. The workflow-approve forward carries no tenant to keep.** `verification.ts:546-553` sends `x-user-id` and the vouch but no `x-tenant-id`. Vouching it therefore cannot "keep their tenant" as the PR body and the `ENVIRONMENT-VARIABLES.md` paragraph imply. Today it 401s regardless (no Bearer, KS-1087, as the code comment says). Once KS-1087 adds a Bearer, approved documents will still land in `DEFAULT_TENANT_ID`. That is not a regression, but KS-1087 should carry it.
- **m3. The PR description's live-state claims are wrong (see Q3).** "Hidden only because the secret is unset everywhere" is false for kintsugi and demo. "Nothing here touches deployed environments" is true of the diff, but the next deploy of develop after the merge **changes behaviour on both boxes**: gateway-created documents start landing in the caller's tenant, and signatories and third-party-verifiers reads start scoping to the caller's tenant. That is the fix, but it should be stated, and documents mis-filed since 19 and 20 Oct need a decision on repair (see Q3).

### LOW
- **l1. The test does not pin two of the five forwards.** The unit test drives three forwards live. Upload is unreachable (415, characterised) and workflow-approve is not driven. Nothing would catch a future edit that drops `vouchHeaderFor` from `verification.ts:553` or `proxy.ts:586`. A cheap static cell (assert each hand-built originate `http.request`/`fetch` site sits next to a `vouchHeaderFor('originate')` call) would close that.
- **l2. The generated secret sits in a mode-644 `.env`.** `bootstrap-env.sh` creates `.env` with `cp` from the template, so the file inherits 0644 (measured in a sandbox copy). The same is already true of `PII_ENCRYPTION_KEY` and `DEMO_SERVICE_KEY`, and D 36th recorded demo's stack `.env` at 644. This is pre-existing and not introduced here, but the new secret is a credential that impersonates the gateway. A `chmod 600 "$ENV_FILE"` would be a one-line follow-up.
- **l3. Mismatch window on running local stacks.** `start-secuura.sh` → bootstrap now arms the secret on the next start. A stack where only one of api-gateway/originate is recreated loses gateway identity (KS-1083 F3). The comment at `bootstrap-env.sh:266-270` and the docs say to recreate both. That is fine as documented, but a developer who restarts only originate will see tenant 403/404s.

### INFO
- **i1. Generation.** `fill_if_blank` (pre-existing helper) generates with `openssl rand -hex 32` (256-bit CSPRNG, 64 lowercase hex). It writes only on an empty value (`get_value` → `-z`), replaces via `.env.tmp` + `mv` in the same directory, and never touches `.env.local` for this key. When `.env` is absent it is first created from `env.example` (`:76-81`) and then filled. If `openssl` is missing, the script exits early (`:63-66`). The test's six arms plus my custom-value arm confirm this.
- **i2. Containment design** is unchanged from KS-1041: a static shared secret over the plain-HTTP compose network, with reach as the defence (HMAC per request is the named follow-up). The PR does not widen reach: one more caller site, same recipient.
- **i3.** The PR adds no new `x-tenant-override` exposure. The upload forward copies every inbound header (pre-existing), which includes the allow-listed `x-tenant-override`. With the vouch, originate would now honour it, exactly as it already does on the generic proxy. The upload forward is unreachable today (415).
- **i4. Docs accuracy, `/health/ready`:** correct. On local the compose nginx (`nginx-demo.conf:403`) proxies `/health/ready` to the gateway's `deepHealthHandler` (`health.ts:241`), which answers 200 when ready and 503 when a dependency is down. "HTTP 200 once its dependencies are up" is accurate. `systemTest/CLAUDE.md` uses `/health` (static nginx 200) for a different purpose (reachability), and both are fine.
- **i5. `gatewayProvenance.ts` diff** is comment-only (lines 89-91 inside a `/** */` block).
- **i6. P2b (`SENSITIVE_KEYS`)** is deferred, with a sound reason recorded on KS-1083 (2026-10-26): shared-logger redaction runs only in production, and the gateway logs through its own winston logger.

## Q3: LIVE STATE (is GATEWAY_VOUCH_SECRET set on the boxes, and is the defect live?)

**Answer: YES on both boxes. The wrong-tenant defect is LIVE on kintsugi and demo today and has been since the secret was armed (kintsugi ~2026-10-19 16:48Z, demo 2026-10-20).** How much real impact it has had (rows actually mis-filed) is **UNMEASURED**.

**What ACTIVE means (instrument: code read).** `describeState(secret)` returns the ACTIVE line **only when `secret` is truthy** (`gatewayProvenance.ts:185-192`). Otherwise it returns FAIL-CLOSED. originate reads the secret once from `process.env.GATEWAY_VOUCH_SECRET` (`originate/src/index.ts:216-219`). An ACTIVE boot line therefore proves a non-empty secret in originate's environment.

**Kintsugi:**
- Today: originate boot line `[gateway-provenance] ACTIVE …` at 2026-10-27 23:06:10Z, StartedAt 23:06:07Z. Instrument: `5_Project_History/2026-10-28_seatD-37th/evidence/kintsugi/postswap_20261027T230742Z.txt:56-63` ("ACTIVE lines since its start: 1"), also `revision_entry_k7.txt:46-47`. **originate's secret is SET.**
- api-gateway side: not re-measured today. history.md, Seat D 22nd (2026-10-19): "Armed `GATEWAY_VOUCH_SECRET` … placed in `.env` (gitignored …). Blast radius … 2 of 33 containers; both carry sha256/16 `9c2fbbcc7351b60b`", i.e. **set and EQUAL in api-gateway and originate**. Subsequent deploys assert `.env` byte-identical before and after. If the gateway lacked it, every proxied request would be unvouched too and the per-forward defect would be masked by a broader outage. No record shows that.

**Demo:**
- history.md, Seat D 23rd (2026-10-20): armed on api-gateway + originate, sha16 equal, boot line DISABLED → ACTIVE.
- Seat D 30th (2026-10-22/23), `2026-10-23_seatD-30th/evidence/draft_KS485_combined.txt:3-5`: "SET, NON-EMPTY, and the SAME value in both" (SHA-256 prefix read in-container, hasher controlled against the empty-string digest); originate boot line ACTIVE (2026-10-21 12:06:41Z), "ACTIVE 1, DISABLED 0, FAIL-CLOSED 0"; `MULTI_TENANCY_ENABLED=false` on both services.
- Today: D 37th's demo round is mid-build (the `heartbeat.demo.d7.d37.txt` tail shows api-gateway building), and the demo `.env` copy is asserted IDENTICAL (`demo/envcopy_ks535before_20261027T231612Z.txt`). No ACTIVE line is recorded for demo today yet. The latest measured state is SET.

**Why that makes the defect live (instrument: code read at develop `8894c7486f82`):**
- develop's `verification.ts` and `proxy.ts` hand-built forwards carry **no** vouch: 0 `vouchHeaderFor`/`x-gateway-vouch` mentions in `verification.ts`, and the 2 in `proxy.ts` are the generic `onProxyReq` mint only.
- With the secret set, originate marks those requests `unvouched` and strips `x-tenant-id`. `resolveRequestTenantId` (`originate/src/utils/requestTenant.ts`) then falls to `DEFAULT_TENANT_ID` (`a0000000-…-001`), and `documents.ts:260`/`certifications.ts:108` use it. That is KS-1083 R2-1, measured in-process by the 2026-09-11 gate and end-to-end by Peter on develop with a hand-set secret (201, then 404 in the caller's tenant).
- Kam's own 2026-09-11 KS-1083 comment said "Do not set `GATEWAY_VOUCH_SECRET` on any environment yet" for exactly this reason. The KS-1032 ruling (2026-10-13, "fail closed, deployed only after the secret is set") then led to arming both boxes on 19 and 20 Oct **without** this forward fix.

**Who is affected:** any `POST /api/documents` through the gateway (the non-workflow path) by a caller whose verified tenant (JWT, or a super-admin `X-Tenant-Override`) is **not** `DEFAULT_TENANT_ID`. The document is saved under the default tenant with a 201, and then 404s for its owner, because GETs go through the vouched proxy and are scoped to the owner's tenant. `GET /api/signatories` and `GET /api/third-party-verifiers` read the **default tenant's** rows for such a caller. That is a wrong-tenant read, and potentially a cross-tenant read if the default tenant has rows.
- On demo, D 30th recorded that `DEFAULT_TENANT_ID` equals every active Platform S key's tenant, so **uat-ps connector traffic is unaffected by construction**.
- The exposure is limited to users or admins acting in a non-default tenant.

**UNMEASURED, and what would measure it (read-only, on each box, approval-class):**
- (a) Count `documents` rows created since the arming time with `tenant_id = DEFAULT_TENANT_ID` whose creating user's tenant (users table / JWT tenant) ≠ default.
- (b) Count users and API keys whose tenant ≠ default (if 0, impact is nil by construction).
- (c) Optionally, originate request-path verdicts for `POST /api/documents` (`unvouched` with a non-empty secret).

**Consequence for this PR:** merging and deploying it **fixes live wrong-tenant writes and reads** on both boxes. Once deployed, new documents land in the caller's tenant. Documents already mis-filed since 19 and 20 Oct stay in the default tenant until repaired, if (a) finds any. This should ride the next deploy round, not wait.

## NOT TESTED
- **The live systemTest cell** `test_tenant_isolation_gateway_create.py` needs a running local slot. Docker was not started. What it would prove: as a SYSTEM_ADMIN with `X-Tenant-Override` = a non-default isolation tenant, a document created via the gateway's own `POST /api/documents` reads back 200 in that tenant and 403/404 in the default tenant. That is R2-1 end to end, on the real originate with RLS. It refuses non-local targets before any fixture writes (module-scoped autouse `_local_slot_only`), and relies on `gateway_vouch_active` to ensure the secret is shared. Its asserts discriminate correctly (it rejects a 5xx as "absent").
- **originate's unit suite (jest).** The PR's originate change is comment-only (verified by diff), so it was not run.
- **m365-integration, Schemathesis, k6, Playwright, Akto, shell suites** beyond the one bootstrap test.
- **Box state today for demo's boot line, and kintsugi's api-gateway secret today.** Both come from prior-seat records, as cited, not re-measured. No box was touched.
- **Runtime proof that the vouch never appears in a log or response.** This was established by reading only.

## Instrument errors / caveats
- `gh pr view --json …statusCheckRollup` failed: "Resource not accessible by personal access token". CI check results are therefore **UNREAD**. `mergeable_state=unstable` (via REST) suggests at least one check is not green or is pending.
- Two Bash calls were refused by workspace hooks: a `$VAR`-expanded `git -C` (the hook could not see the path, so it was re-run with the literal path), and an unquoted `====` (zsh `=` expansion). Neither had any effect.
- To run develop's gateway source against the head test, I checked out develop's `proxy.ts`/`verification.ts` into the clone's index and then restored them with `git checkout <head> -- …`. The clone now sits at the local merge-preview commit (my clone only).
- `KS-108` returned no issue from Linear (team KS, number 108). It is probably a typo for KS-1083, which was read in full along with KS-955.
- The bootstrap test's own `trap rm -rf` cleans its mktemp dir under `/tmp/rv1756`. That is the PR's test behaviour, not a reviewer action.
