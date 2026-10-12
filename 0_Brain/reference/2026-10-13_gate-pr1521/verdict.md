# Gate verdict: Secuura Platform K PR #1521 (KS-1533 arm 1)

**Gate:** independent adversarial QA, Opus tier 1 (auth / key-minting surface). Findings only: nothing was written to the project, GitHub or Linear.
**Date:** 2026-10-13. **Brief:** `GATE_BRIEF.md` (this folder). **Charter:** `2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## VERDICT: NO GO (1 Major in the diff, with a one-line fix)

| id | sev | where | one line |
|---|---|---|---|
| **M1** | **Major** (in diff) | `services/security/src/index.ts:1057-1071` + `:1114-1115` | The provisioner exemption also lets a provisioner `rotate`. It can still retire **another organisation's** live connector keys, so **Path 3 stays open for that caller class**. This contradicts the gateway's own Guardrail 1 (`api-gateway/src/routes/platform.ts:517-528`), and the PR's test at `ks1533-key-mint-organisation-arm.test.ts:248` pins the hole as legitimate. |
| **M2** | **Major** (ticket-level, NOT in this diff; does not block this merge by itself) | `services/originate/src/routes/adminConfig.ts:924-947` (role gate `:38`) | **Path 1 is still open through the sibling writer.** `POST /api/admin/api-keys` admits ORG_ADMIN and writes `organization_id = body.organizationId` with no organisation check. The PR body's "Path 1 closed here: yes" holds for the security route only. Code-read, not measured. |
| m1 | Minor | `index.ts:1077` (stored), `:1181` (raw `===` list filter) | `organizationId` is compared **normalised** but stored **raw**. `''`, `'   '`, `' <own>'`, `'\t<own>'` and an upper-case own id are all 201 and land verbatim in the row. |
| m2 | Minor (evidence quality) | PR body, "KS-764 call-site guard 15/15" | That guard is a **revoke** call-site guard. It stays 15/15 under both load-bearing deletions of this PR (mutants Ma and Mb below), so it is not evidence for this change. Only the new HTTP file covers the mint wiring. It does kill both mutants. |
| m3 | Minor (part of M1) | `ks1533-...test.ts:248` | The cell is titled "the connector's OWN provisioner", but the route never compares the provisioner's own connector with the one it names. The title asserts a property the code does not have. |
| P1 | **pre-existing, high severity, separate ticket** | `index.ts:196-243` (KS-577) | **Concurrent rotates leave the connector with ZERO active keys**, and both callers are handed dead keys. Measured on real PostgreSQL: N=2 left 0 active in 9 of 10 trials. Identical on develop, so not introduced here. |

**Head under test:** `c02c0b5dcc22d3a59c7faa787b08a2871bfdafda` (PR #1521). **develop:** `425ad3e00ae40ddbce6ead62c127c610e2e67a16`. **Merge-base:** `250596098fa9c2b5e1d5930afeef882143b5f5f1`.

**To reach GO:** apply M1's fix and change cell `:248` to a platform-role rotate (or add the regression cell described under M1). A narrow re-gate of M1 only is enough. **M2 and P1 need their own tickets.** M2 must be closed (or explicitly accepted by Kam) before KS-1533 or the KS-695 erasure is called done.

---

## How the head was obtained (and asserted)
- The project checkout was used **read-only**: `git config --get core.sshCommand`, `git remote -v`, `git status`, `cat-file`. Its local HEAD is `40ed3573b` and it does **not** contain `250596098fa9`, so V's bundle could not be applied there or in a shared clone without a fetch.
- `git clone --shared --no-checkout` went into the scratchpad. The push URL was set to `DISABLED`, and `refs/pull/1521/head` and `develop` were fetched with the project's deploy-key `core.sshCommand` (read-only fetch).
- **Asserted:** fetched `refs/pull/1521/head` = `c02c0b5d…`, and `git ls-remote origin` = `c02c0b5d…`. develop is `425ad3e0…` both locally and remotely.
- V's bundle sha256 was re-measured as `3e2f299b5c7aa0c3…`, matching the brief. It was not used, because the fetch gave the same head.
- **Diff, measured:** `git diff --stat 250596098fa9 c02c0b5d` gives 2 files, **+312 −8**: `services/security/src/index.ts` (58) and the new `__tests__/ks1533-key-mint-organisation-arm.test.ts` (262). This matches V. develop has moved one commit since (`425ad3e00`, KS-1511, test-only, in `services/security/__tests__`). The PR is not rebased onto it. **The merged tree was built and tested** (below).

## The instruments, and the control that each one could fail
| instrument | what it is | control that could fail |
|---|---|---|
| Gate harness `evidence/harness/gate1521.test.ts` | Drives the **real** security app over real HTTP: real `express.json`, the shared RS256 `authenticate()`, and the real router order with `requireKeyAdminOrProvisioner` before the handler. It reads the **store** back independently after every call: SQL against `svc_api_keys` in PG mode, the module map in memory mode. | (a) A seeded platform mint must be visible to the read-back. (b) No token gives 401. (c) **The same harness goes RED on develop** (2 failures: an ISSUER_ADMIN's duplicate-key rotate retires the victim, and the attacker's concurrent rotate is 201). So it can detect Path 3. |
| Classifier `evidence/harness/classify.py` | An oracle written down **before** reading results (in its docstring). It compares 560 cells and flags any non-platform caller that retired the victim. | It flags 10 new Path-1 cells under mutant Ma. My own oracle errors are listed openly below. |
| Real PostgreSQL 18 | A throwaway cluster in the scratchpad, on loopback `127.0.0.1:55432`. It has a minimal `svc_api_keys` with the service's columns, **no RLS**. Stopped after use. | `initDb()` must return true or the harness throws ("refusing to run a memory test labelled postgres"). psql was used as a second, independent reader for the race. |
| Suites | vitest at head, develop and the merged tree | develop and head counts must differ by exactly the new file (16 tests). |

**Corrections to my own work, made in the open:**
1. **The first `packages/shared` run showed "6 files failed".** That was my harness, not the code. The six repo guards locate the Dev root from `process.cwd()`, and I had run from the WEDNESDAY folder. Re-run from the package directory, it gives 49/949 at both head and develop.
2. **My first organisation case-variant cells were theatre.** I used digit-only UUIDs (`22222222-…`), and `.toUpperCase()` does not change them. They were redone with hex-letter UUIDs and a guard asserting that the variant really differs in case.
3. **The first secret scan of the evidence folder printed "clean" because the grep itself errored** (an invalid `(RSA |)` group). It was redone with a valid pattern and a positive control: 3 of 3 control hits, 0 hits in evidence.
4. **Oracle errors in `classify.py`, left in the file deliberately:**
   - 4 cells (`provisioner × other_tenant × non-string connectorId`) were expected 400 and are 403. `decideMint` refuses the foreign tenant before the body is parsed, so the order is correct and my oracle was wrong.
   - 3 `malformed_case` provisioner-rotate cells were expected 403 and are 201. They retire nothing, because a different connector string matches nothing. Under Guardrail 1 they arguably should still be 403, and M1's fix makes them so.

---

## Findings in detail

### M1: the provisioner can still retire another organisation's keys (Path 3 is not closed)
- **Oracle violated:** Product consistency (the gateway's own Guardrail 1: *"rotation stays platform-admin-only … a provisioning key … must not be self-service"*, `platform.ts:517-528`) and Purpose (the PR's claim "closes Path 3").
- **The code:** `index.ts:1057-1071` exempts `isPlatformRole || isProvisioner` from the `connectorId` refusal. The rotate at `:1114-1115` then runs for anyone who passed. `revokePriorConnectorKeys` scopes by connector id and tenant only (`:226-230`). Nothing binds a provisioner's named `connectorId` to its own connector or its own organisation.
- **Reproducing shape** (measured, real HTTP, memory **and** Postgres):
  1. Platform role mints org A2's connector key: `{tenantId: TA, organizationId: A2, connectorId: "platform-s:a2-ref"}`.
  2. The caller is a token with exactly the claims auth's `generateConnectorToken` mints (`auth/src/services/jwt.ts:288-296`): `role: connector`, `type: connector`, `scopes: ["organizations:register"]`, `tenantId: TA`, `organizationId: A1`.
  3. It sends `POST /api/keys {name, tenantId: TA, connectorId: "platform-s:a2-ref", rotate: true}`, with `organizationId` set to A1, A2 or omitted.
  4. **Result: 201, and A2's previously active key is now `is_active = false`.** Cells: `provisioner × {own_org, other_org, orgless} × other × rotate` (3 of 3). Files: `evidence/results/head-pg.json`, `head-mem.json`, and `classification.txt`, under "victim retired by non-platform caller".
- **Before vs after the PR:**

  | build | non-platform cells that retired the victim |
  |---|---|
  | develop | **18**: ADMIN, ORG_ADMIN, org_admin, ISSUER_ADMIN, org-less issuer_admin, provisioner, 3 each |
  | head | **3**, all provisioner |

  So the PR closes 15 of 18 and leaves exactly this class.
- **Reachable through the gateway (code-read, NOT measured end to end):** `POST /api/security/keys` is mounted as `authenticateToken(true)` followed by a proxy rewriting to `/api` (`api-gateway/src/routes/proxy.ts:1189-1191`). The `x-api-key` branch swaps the caller's bearer for an auth-minted connector JWT (`middleware/auth.ts:419-421`) and sets `x-tenant-id` from the key. The proxy forwards Authorization. I found no connector route allowlist in `proxy.ts` or `index.ts`. **So the holder of a provisioning `sk_` key can do this with the key alone, by going around `register-connector`'s Guardrail 1.** The security service's own header (`provisioningPolicy.ts`) says it must enforce its limits "ITSELF, because a key can also be presented here directly".
- **Blast radius:** any organisation's connector inside the provisioner's tenant. The cross-tenant case is refused (measured: `other_tenant` gives 403). The caller also **receives a fresh live key bound to that organisation's connector**, which is the "credential-replacement capability" the gateway guardrails exist to prevent. **Likelihood:** it needs a provisioning key, which is high privilege. A leaked one is exactly the threat the guardrails were written for.
- **Minimal fix (probed in scratch, not authored to the project):** inside the `connectorId` block, after the existing refusal, add `if (isProvisioner && data.rotate === true) → 403`. Measured with that probe ("N"):
  - non-platform victim retirements: **0**
  - `register-connector`'s nine forwarded shapes: **unchanged**
  - V's file: 15/16, and the only red cell is `:248`, the one that pins the hole
  - full gate harness: green

  A broader probe ("F", refusing every non-platform `rotate`) also closes it, but it refuses `rotate:true` sent without a connector, which is otherwise a no-op. Prefer N.
- **Regression test the owner should add:** a provisioner token naming another organisation's `connectorId` with `rotate: true` gets 403, **and** that organisation's key is still active, read back from the store. Change `:248` to a platform-role rotate. Optionally pin that a provisioner may still set `connectorId` **without** rotate (register-connector's path).

### M2: Path 1 is still open via originate's admin mint (ticket-level)
- **Oracle:** Purpose (KS-1533 Path 1) and History (KS-764 F-764-01: "originate's sibling route came to exist" by exactly this shape).
- **The code:** `adminConfig.ts:38` admits `SYSTEM_ADMIN, ORG_ADMIN`. At `:947`, `orgId = d.organizationId || user.organizationId || null`, then `INSERT INTO svc_api_keys (… organization_id …)` with no `decideTenantAccess` or organisation check anywhere in the handler (`:924-1000`).
- **Shape:** an ORG_ADMIN of A sends `POST /api/admin/api-keys {name, organizationId: B, permissions: [...]}`, which is expected to give 201 with `organization_id = B` in A's tenant.
- **NOT measured** (code-read only; originate was not booted). It is outside this diff. It writes no `connector_id` and does not rotate, so it is **not** a Path 3 vector. Its only revoke (`:1080-1090`) goes through `decideKeyRevoke`.
- **Fix shape:** call `decideTenantAccess(user, tenantId, {targetOrganizationId: d.organizationId ?? null})` before the INSERT, the same as this PR does on the security route. Regression test: the same cell as R1, against originate.

### m1: organisation ids are compared normalised but stored raw
- Measured as an ISSUER_ADMIN of A1:
  - `''` and `'   '` give 201, stored verbatim instead of NULL. This violates the "absent has ONE representation" rule in `keyRevokePolicy.ts`.
  - `' <A1> '` and `'\t<A1>'` give 201, stored padded.
  - Upper-case own id gives 201, stored upper-case.
  - Upper-case or padded **foreign** ids are correctly 403.
- **Consequence (code-read):** `GET /api/keys` filters with raw `k.organizationId === organizationId` (`index.ts:1181`), so such a key is invisible to its own organisation's listing.
- The raw write predates this PR. The PR adds the normalised comparison next to it.
- **Fix:** persist `normaliseOrgId(data.organizationId)` (null for blank), or refuse non-canonical ids with a 400.

### P1 (pre-existing): concurrent rotate leaves zero active keys
- Measured on real PostgreSQL, with psql as a second reader:
  - **20 concurrent** platform rotates on one connector left **0 active of 21**: head 3 of 3 runs (plus 8 of 8 earlier runs), develop 3 of 3.
  - **N=2** (a double-submit or retry) left **0 active in 9 of 10** trials.
  - **Sequential control: 1 active of 21** every time.
- **Mechanism:** each request INSERTs its own key, then runs `UPDATE … WHERE connector_id=$1 AND tenant_id=$2 AND id <> <own>`. Two interleaved requests each retire the other's new key.
- In memory mode the race does not appear (1 of 21), because no real `await` separates insert from revoke there. **This is why the existing suites cannot see it.**
- **Not introduced by #1521.** It is reported because the brief asked for the race and because severity is high: a connector outage, with both callers given dead keys (via `register-connector` rotate as well).
- **Fix shape:** do the insert and the revoke in one transaction under `pg_advisory_xact_lock(hashtext(tenant_id||connector_id))`, or retire only keys created before the new one.

### Item 7: the masked mutant survivor is genuinely masked (equivalent on every reachable input)
- Mutant S, `isProvisioner = caller?.role === 'connector'` (scope dropped):
  - 0 of 560 matrix cells and 0 of 16 smuggling shapes differ from baseline
  - V's file stays 16/16
- **Reachability probe** through the real `decideMint` (`evidence/harness/reach.mjs`):
  - role `connector` passes **only** with `organizations:register`
  - `Connector`, `CONNECTOR` and `' connector'` are refused (exact-case match)
  - so no caller reaches the route clause as a scope-less `connector`
- **Verdict:** a defence-in-depth clause, not a coverage gap. Keeping it is reasonable. V's scope-less cell already pins the property.
- **Curio, not a finding:** `decideMint` and the route clause both accept a **string** `scopes` claim by substring (`"x organizations:registerx"` is allowed). It is unreachable today, because the only issuer of `role: connector` tokens (`jwt.ts:288-296`) always emits an array. It would become a finding if any issuer ever emits a space-delimited `scopes` string.

### Item 8: regressions

| tree | security | packages/shared | KS-764 guard |
|---|---|---|---|
| head | 30 files / 327 tests, rc 0 | 49 / 949, rc 0 | 15/15 |
| develop | 29 / 311, rc 0 | 49 / 949, rc 0 | 15/15 |
| **merged** (PR + develop, `3ffbdd608`, scratch) | 30 / 327, rc 0 | n/a | n/a |

- Head minus develop on security is exactly the new file's 16 tests. All of V's suite figures are reproduced.
- **But see m2:** the KS-764 guard stays 15/15 under mutant **Ma** (organisationScope argument dropped) and **Mb** (connectorId block disabled). V's file kills both (3 and 2 red), and my classifier flags Ma (10 Path-1 cells flip to 201).

### Item 6: `register-connector` still works for the legitimate roles
- The exact mint body was replayed at the security service: `S_CONNECTOR_SCOPES`, `connectorId: platform-s:<ref>`, a fresh organisation, `rotate` on or off.
- Results:
  - `super_admin`, `SUPER_ADMIN` and `SYSTEM_ADMIN` give 201 both ways, and rotate reports `priorKeysRevoked: 1`
  - the provisioner (no rotate) gives 201
  - `platform_admin` gives **403 at both head and develop**
- **Identical head vs develop, so no regression.** The `platform_admin` 403 is pre-existing (KS-1536): the gateway's `SUPER_ROLES` admits a bearer the security service refuses, so a `platform_admin` registration 502s.

### Item 2: smuggling shapes (all held)
Each was tried as an ISSUER_ADMIN of A1 against connector A2 with rotate. The victim stayed active in all 16, and no `connectorId` was ever stored.

| shape | result |
|---|---|
| query `?connectorId=…&rotate=true`, header `x-connector-id`, body `ConnectorId`, `connectorid`, `connector_id`, `" connectorId"`, `__proto__`, `constructor.prototype`, nested `data` | 201 with `connector_id` NULL (zod strips unknown keys) |
| duplicate JSON key (own then other) | last wins, then 403 |
| `connectorId: null` | 400 |
| whitespace or trailing-space connectorId | 403 |
| `rotate: "true"` | 400 |
| urlencoded body | 400 |
| `x-tenant-id` set to another tenant | 403 |

### Item 1: the matrix in numbers
- **Size:** 10 roles × 4 targets × 7 connectorId shapes × rotate on/off = **560 cells per mode**.
- **Status histogram, identical in memory and Postgres:** 403 × 362, 400 × 108, 201 × 90. **Memory vs Postgres disagreements: 0 of 560.**
- **Invariant, asserted on every non-2xx cell:** a refusal writes no row and retires no key. It held in all cells at head.
- **develop vs head:** 130 cells differ, all in the ADMIN, ORG_ADMIN, org_admin, ISSUER_ADMIN and org-less roles, which are the intended changes. **No provisioner, platform, user or `platform_admin` cell changed.**

## ADMIN: not ruled (Kam's card, KS-1535); what each option would mean
**Measured today:**
- `ADMIN` of A1 may mint for another organisation in its tenant (201).
- It is refused cross-tenant (403).
- It **can no longer name any `connectorId`** (403), so it is no longer a Path 3 vector after this PR.

**Option (a), keep it unbounded:** a tenant `ADMIN` can still create a key row carrying organisation B's id, which the KS-695 erasure would trust. Path 1 then remains open for `ADMIN` by policy.

**Option (b), add `ADMIN` to `ORG_BOUNDED_ROLES`:**
- That set lives in `packages/shared` and also drives **revoke** (KS-764) and originate's revoke. Bounding it changes revoke for `ADMIN` too.
- An `ADMIN` with no organisation claim would then be refused whenever it names an organisation, the same standing cost as the KS-779 org-less accounts.
- The UNDECIDED cell in V's file would flip to 403.

## What was NOT tested (Rule 2)
- **No real gateway or auth hop.** M1's reachability through `POST /api/security/keys` with `x-api-key` is code-read only (`proxy.ts:1189`, `auth.ts:419`). The security leg used tokens with the exact claim shape auth mints, signed by a test key.
- **originate was not booted.** M2 is code-read only.
- **Postgres has no RLS and no real migrations.** The schema is minimal, and I connected as superuser. The RLS GUC path (`runWithTenantId`) ran but was not enforced. The `organizations` lookup branch (tenant resolved from organizationId) was not exercised, because every cell sent `tenantId` or relied on the caller's tenant.
- **Not run:** the platform suites (Schemathesis, Akto, Playwright, k6), other services' suites, `tsc` and `eslint`, and V's pre-push hook. Nothing was run against Kintsugi, demo or any box.
- The **erasure** half of R8 (KS-695) was not run. It is 501 at this head.
- Only some of V's 10 mutants were re-run: the survivor S, plus my Ma and Mb. The other 7 were taken on V's report.
- Races beyond platform-vs-platform and attacker-vs-platform (for example, rotate concurrent with a revoke) were not run. `API_KEY_ROTATION_GRACE_SECONDS > 0` was not tested.
- Expired, `nbf` or tampered tokens were not tested. Roles not in the matrix (`OWNER`, `issuer`) were not tested. Upper-case `SUPER_ADMIN` and `SYSTEM_ADMIN` were tested only in the `register-connector` replay.

## Evidence (this folder)
- `evidence/harness/`: `gate1521.test.ts`, `regconn.test.ts`, `classify.py` (the oracle is in its docstring), `reach.mjs`.
- `evidence/results/`:
  - matrix: `head-mem.json`, `head-pg.json`, `dev-pg.json`, `dev-mem.json`
  - races: `race-{head,dev}-{1,2,3}.json`, `race-pair.json`
  - `register-connector`: `regconn-{head,dev,N}.json`
  - mutants: `mut-{S,Ma,Mb,F,N}.json`
  - `classification.txt`, `suite_summaries.txt`
- **Secret scan of `evidence/`:** 0 hits. The pattern covers JWT (`eyJ…`), PEM private keys and `sk_` hex, with a positive control of 3 of 3. Test RSA keys were generated in memory and never written.
- Scratch state: the clone, three worktrees and the PG cluster live only in the session scratchpad. PG is stopped. `index.ts` was restored byte-identical after every mutant (sha256/16 `c230c31cc51a2baa`, asserted each time).

## PROOF debrief
- **Past:** shared clone and fetch, head asserted, diff measured, real-HTTP harness at head and develop in two storage modes, a smuggling battery, races on real PG, mutants, a `register-connector` replay, and the suites at head, develop and the merged tree.
- **Results:** the PR does what it says for ORG_ADMIN, ISSUER_ADMIN, org-less and ADMIN (15 of 18 Path 3 cells closed, Path 1 closed on this route, refusals write nothing). It leaves Path 3 open for the provisioner, which is M1, and its tests pin that as intended.
- **Obstacles:** the project checkout lacked the merge-base, so a scratch fetch was needed. The socket path was too long, so PG ran on loopback. My cwd harness error in the shared suite was corrected.
- **Outlook:** after M1's fix, a narrow re-gate of M1 only. M2 and P1 need their own tickets.
- **Confidence:** high on M1 (measured in both modes, with a control that goes red on develop). Medium on M2 (code-read). High on P1 (real PG, psql cross-check, sequential control).
