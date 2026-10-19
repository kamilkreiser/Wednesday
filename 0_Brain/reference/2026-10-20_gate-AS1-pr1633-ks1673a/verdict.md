VERDICT: GO WITH NOTE at head 76725fd4a5b7... (tier 1, round 1 of 2; landing tree 3b26d9bc0340ddf9cf371c0fc318936a9bef4e06 on develop 88b8ceb9f3041672d9575b40c09869d45ab1c111; 0 blockers, 6 notes)

model: claude-opus-5-5 -- G1 (tier 1, tenant-isolation fix on a High finding) -- P1-P4 no -- gauge 51%

## BLUF

- **I could not break the binding as org B.** I sent A's ids by path, query and body on all 14 bound routes, plus 20 id shapes and 13 token-org shapes. Nothing reached A's data, and Graph/MSAL was called **zero** times on every refused path.
- **"Not yours" matches "unknown id" on every route:** status, body bytes and headers (Date excluded) are equal. The same 14 attack cells are **red on develop**, and on head the owner gets a different answer on 7 read routes, so the instrument can see a difference.
- **No blockers. Six notes.** Two need a ruling from Wednesday:
  - **N1 (before deploy):** the only caller in the repo writes a **tenant** id where the fix now expects an **organisation** id. Every existing m365 row becomes owned by nobody. Reasoned from code, not measured on data.
  - **N2 (needs a ticket):** the unauthenticated OAuth callback still lets anyone holding a connectionId take over that connection. Measured; the same on develop.
- **The owner regression the author named is real, and I measured it (N3).** It is not the normal state after a restart, going by the repo's own migrations.
- One of my mutants **survives all 33 of the author's cells** (N4).

## Heads and landing (read at start and again at 15:05Z, via ls-remote from my clone)

- `refs/pull/1633/head` = `76725fd4a5b74e0c2ff58dad90bc2382dfc36966`; develop = `88b8ceb9f3041672d9575b40c09869d45ab1c111`. Unchanged between the two reads.
- `git merge-tree --write-tree origin/develop pr/1633` = `3b26d9bc0340ddf9cf371c0fc318936a9bef4e06`. This equals `pr/1633^{tree}`, which is also the author's predicted tree.
- `merge-base --is-ancestor origin/develop pr/1633` rc 0, so the head is a strict descendant.
- Three-dot diff: 4 files.

| file | numstat |
| -- | -- |
| `docs/openapi/secuura-api.yaml` | 4/6 |
| the test file | 442/0 |
| `index.ts` | 106/17 |
| `m365-integration.openapi.ts` | 8/2 |

## Blockers

None.

## Notes

### N1 — The organisation now comes from a different id space than the one existing rows were written with. Ruling needed before deploy. Reasoned, not measured.

The only in-repo caller of `POST /api/connections/init` is `frontend/admin/src/components/M365SetupWizard.tsx:93-98`. It sends `organizationId: selectedTenantId || 'default'`.

- `selectedTenantId` is a **Secuura tenant** id from `useTenantStore`.
- That store is populated only for `super_admin` / `system_admin` (`frontend/admin/src/components/Layout.tsx:107-111`).
- `'default'` fails develop's `z.string().uuid()`. So **before** this PR, the only path that worked was a system admin with a tenant selected, and it wrote a **tenant UUID** into `svc_m365_connections.organization_id`.
- The token's `organizationId` is `users.organization_id`, an `organizations.id`. Organisations carry their own `tenant_id` (`services/auth/src/repositories/userRepo.ts:555`; `services/api-gateway/src/routes/platform.ts:813`). The two id spaces are different.

Consequences after deploy, all fail-closed:

- **(a)** Every pre-existing connection row is owned by no token. Its connections, sites and synced documents become invisible to everyone, their real owner included.
- **(b)** The wizard's tenant choice is now silently stripped:
  - a system admin's new connection lands in the admin's own organisation;
  - if a platform-admin token carries no `organizationId`, the response is 403.

  This is consistent with the "no admin bypass" ruling, but neither the PR body nor the ticket comment states it.
- **(c)** Tenant admins, who previously got 400 on `'default'`, now succeed under their own organisation. That is an improvement.

I did not inspect real data or real admin tokens. **Wednesday should rule on re-connect versus backfill before deploy**, and the KS-1673 comment should say what happens to existing rows.

### N2 — `GET /api/callback` (unauthenticated) is a cross-org mutation sink keyed only by the connectionId. Measured. Pre-existing and unchanged. Needs its own ticket.

| cell | what I did | result at head |
| -- | -- | -- |
| C1 | Anonymous request: `?code=evil&state=<A's connId>`, with MSAL mocked to return the attacker's tokens | 302 `m365=success&...&tenant=ATTACKER-DISPLAY`. A's next OneDrive call went out with `Bearer ATTACKER-TOKEN-evil`: A's organisation now reads the attacker's Microsoft account as its own. |
| C2 | Anonymous request with a garbage code | A's connection flips to `status: 'error'`. A's next `POST /api/sites` is 400 "Invalid or disconnected connection". |

- **Existence oracle:** the redirect `Location` for a known id differs from an unknown one (`message=connection_not_found`).
- **On develop**, C1 and C2 give identical results.
- **Why this is a note, not a blocker:** after this PR I found no cross-org path that discloses a connectionId (`conn_<uuidv4>`). `GET /api/sites` was the leak, and it is closed. So the PR does not widen this.
- **Why it still matters:** a `connectionId` is still a bearer capability here. Calling this route "unbound by design" is too strong. It can be bound with a single-use `state` nonce stored at init.

### N3 — Owner impact of the warm-map ownership. Measured. Not the normal post-restart state according to the repo; reachable under scale-out.

**Setup:** connection `conn_late` (org A) is in the DB-by-id path but not in this process's warm map. That simulates a write made after boot, or by another replica.

| step, as A | head | develop |
| -- | -- | -- |
| `GET /api/connections/conn_late` | 200 | 200 |
| its pre-existing site listed / `libraries` | not listed / 404 | listed / 200 |
| `POST /api/sites` on it | **201** | 201 |
| the site just created: listed / `libraries` / `DELETE` | not listed / 404 / 404 | listed / 200 / 200 |
| `POST /api/documents/sync` on that site | 201, but Graph received the internal id `site_…` as the SharePoint site id and library `Documents` (a wrong call in real life) | 201, with the Graph ids `graph-new` / `lib-new` |
| the synced doc: listed / `GET` | not listed / 404 | listed / 200 |

**How reachable this is:**
- `deployment/azure/services.bicep` gives the m365 container app `minReplicas: 1`, `maxReplicas: 20`. Any connection created on replica X after replica Y booted is in this state on Y.
- That said, the callback, `/complete` and OneDrive already depend on the warm map, so multi-replica is already broken for this service before this PR.

**KS-1675** (connections probably never reload under fail-closed RLS):
- `migrations/039_rls_fail_closed.sql:20-23,79` explicitly **excludes** `svc_m365_connections` from the fail-closed flip; it keeps 038's permissive policy, where an unset GUC means all rows.
- `svc_sharepoint_sites` and `svc_synced_documents` are in neither 038 nor 039.
- So by the tree, `loadFromDb` re-warms all three after a restart, and this is **not** the normal post-restart state on one replica.
- I did not measure this against a live Postgres, and I did not read KS-1675 on Linear (I have no Linear tool here).

**Suggested fix-forward:** prove site/doc ownership through `dbGetConnection`, the DB-first path, rather than `memConnections`.

### N4 — Test gap: one of my mutants survives every one of the author's cells.

**X2:** `POST /api/documents/sync` with the site lookup reverted to `memSites.get(data.siteId)`. tsc rc 0. **Author 33/0, all green.** My cell D goes red.

No author cell sends B's **own** connection with A's siteId. My cell D does, at head:

| B sends | `downloadAndHashItem` received |
| -- | -- |
| A's internal site id | `('tokB','site_a1','Documents','item')`: no substitution |
| A's raw Graph site id plus library | `('tokB','graph-site_a1','lib-site_a1','item')` |
| B's own site (control) | `('tokB','graph-site_b1','lib-site_b1','item')` |

A's `GET /api/documents?siteId=site_a1` gained none of B's docs.

On the author's item 3 (the raw fallback): I measured that the raw id is passed through **under B's own token**. Whether Microsoft Graph would serve another tenant's site to B's token is **reasoned only** (Graph authorisation is per-token). I did not call Graph.

**Recommend** adding cell D to the PR's file.

### N5 — Timing on the DB-first routes (named-resource routes using `ownedConnection`).

- Both foreign and unknown ids take the DB lookup: by-id SELECT count 1 versus 1 on every DB-first route. The lookup is **not** skipped for an unknown id.
- But a foreign id returns a row, which then gets mapped plus two `decryptToken` calls (and a warn log for plaintext rows). An unknown id returns no row.
- In-process medians over 300 alternating samples per side:

| run | conn: foreign / unknown | noise (unknown vs unknown) | repeat: foreign / unknown | OneDrive (warm-map) foreign / unknown |
| -- | -- | -- | -- | -- |
| 2 | 294 / 228 µs | 123.6 / 124.0 µs | 151.6 / 122.0 µs | 127.8 / 127.3 µs (no gap) |
| 1 | 434 / 428 µs | 337 / 393 µs: **inconclusive** | 237 / 186 µs | 193 / 188 µs |

- This is the same request class (one query each) and small next to a real DB round-trip. **Low.**
- Fix-forward that removes the gap: `WHERE id = $1 AND organization_id = $2`.

### N6 — Minor observations, no action required for this PR.

- **(a)** The claim's "`index.ts` +123/−17" is 106 insertions and 17 deletions (123 changed lines).
- **(b)** `GET /api/onedrive/files?connectionId[toString]=x` returns 500 for every caller. `String()` throws, `next(error)` catches it, and the process survives. This is the pre-existing KS-1671 class on an authenticated route, and it is the same for every caller, so it is not an oracle.
- **(c)** Unauthenticated `/health` still returns cross-org aggregate counts (counts only, no rows).
- **(d)** A token org of `"  <A>  "` is trimmed and matches A (measured: 200). It is reachable only through a signed token.

## Q1 — Route census (my own instruments)

### Instruments

- **Primary:** the runtime Express router stack. I imported the real app through the seam and filtered `app._router.stack` for layers with a `.route`.
  - Positive control: it lists `GET /health` and `GET /api/callback`.
  - Result: **25 routes, 24 under `/api`**. The auth `app.use('/api', jwtAuthenticate…)` is stack layer 11, and **21 routes sit after it**.
- **Second instrument:** regex `^app\.(get|post|put|patch|delete)\('`. It also gives 25 at head and 25 on develop.
- `app.(all|route)(` / `Router(` = 0, so no route is mounted any other way.

### Route by route

| # | route | org-owned state | bound at head | evidence |
| -- | -- | -- | -- | -- |
| 1 | GET /health | aggregate counts only | no (unauthenticated) | read |
| 2 | GET /api/health | none (redirect) | n/a | read |
| 3 | GET /api | none (static) | n/a | read |
| 4 | GET /api/callback | **mutates a connection** | **no** | C1/C2 measured, N2 |
| 5 | POST /api/connections/init | creates a connection | yes: org from token, 403 if absent | I, T, T-proto |
| 6 | POST /api/connections/complete | connection (warm map) | yes | O |
| 7 | GET /api/connections/:id | connection (DB-first) | yes | O, S, T |
| 8 | DELETE /api/connections/:id | connection | yes | O |
| 9 | POST /api/connections/:id/refresh | connection | yes | O |
| 10 | POST /api/sites | site via connection | yes | O |
| 11 | GET /api/sites | sites | yes: filter, plus 403 with no org | O, S, T |
| 12 | GET /api/sites/:id/libraries | site | yes | O, S |
| 13 | DELETE /api/sites/:id | site | yes | O |
| 14 | POST /api/documents/sync | connection + site | yes | O, D |
| 15 | GET /api/documents | docs | yes: filter, plus 403 | O, T |
| 16 | GET /api/documents/:id | doc | yes | O, S |
| 17 | GET /api/onedrive/files | connection token | yes | O, S, T |
| 18 | POST /api/onedrive/files/:id/sync | connection token | yes | O, S |
| 19 | POST /api/teams/webhook-config | webhook rows | **no** (PR B) | read: org taken from the body |
| 20 | GET /api/teams/webhook-config | **every org's webhook URLs** | **no** (PR B) | read |
| 21 | DELETE /api/teams/webhook-config/:id | any org's webhook | **no** (PR B) | read |
| 22 | POST /api/teams/notify | every org's webhooks | **no** (PR B) | read |
| 23 | POST /api/outlook/exchange-token | none (caller's SSO token, nothing stored) | n/a | read |
| 24 | POST /api/outlook/verify-hash | none (public, proxies to originate) | n/a | read |
| 25 | GET /api/outlook/status | none (static) | n/a | read |

**Confirmed:** 25 routes / 24 under `/api` / 14 bound / 6 unbound (4 Teams, `/health`, `/api/callback`). The other 5 touch no org state.

**One refinement:** I classify `/api/callback` as unbound **and** mutating. See N2.

**The ticket's "22":** it reproduces as 25 minus the 3 health/info routes (`/health`, `/api/health`, `/api`). That is the 21 routes below the auth mount plus `/api/callback`, i.e. every route that is not health or info.

## Q2 — Attacks as org B: how they were run

### Harness

- A gate-only file, `services/m365-integration/src/__tests__/zz_gate_as1_attack.test.ts`, in my scratch clone. Never pushed.
- It uses the AP1 seam pattern:
  - **`../db`:** a **stateful** row store. The INSERT upsert is applied, and the by-id SELECT is answered from that store and counted.
  - **Graph SDK and MSAL** (`../sharepoint/client`, `../auth/token-manager`): recording mocks.
  - **`@secuura/shared`:** only `authenticate` is replaced, so each cell can pick its caller.
  - **express:** `listen` is mocked.
  - **Everything else is the real code**, driven over HTTP on 127.0.0.1.
- **Graph instrument:** a global `fetch` spy for `graph.microsoft.com` and `login.microsoftonline.com`. The SDK and MSAL recorders are counted separately, so the zero check covers all three.

### Cells and results at head: 28 tests, all pass

| cell | what it does | result |
| -- | -- | -- |
| O ×14 | For each named/list route: B with A's id versus B with an unknown id of the same shape. Asserts equal status, equal body **bytes**, equal headers (Date excluded), Graph/MSAL counters `{net:0, sdk:0, msal:0}`, no leak of 7 A markers (org, token, tenant name, Graph site id, library, site id, doc id), and an equal by-id DB lookup count. | All pass. `POST /api/sites` and `POST /api/documents/sync` answer 400 = 400 with byte-equal bodies. The other named routes answer 404 = 404. The list routes answer `200 {"success":true,"data":[]}` for both. |
| O-ctl | Positive control | As A, 7 read routes give an answer different from unknown. |
| S | 20 GET shapes (case, `%20`, `%5F`, `%09`, trailing `/`, `/API`, `//`, `[]`, `[0]`, repeated key, `[toString]`, `[__proto__][x]`, `%2F`) and 6 body shapes (array, two-element array, object, leading space, uppercase) | Never 200 on a connection, never a leak, Graph 0. |
| S-ctl | Positive control | A with `{connectionId:['conn_a1']}` gets 200 with 2 Graph calls, so S refused on ownership, not on shape. |
| T | 13 token shapes: no `req.user`; user without org; `''`; spaces; tab/newline; number; array `[A]`; object with `toString`→A; `null`; `true`; `new String(A)`; A+ZWSP; a mangled A | Every shape: connection 404, OneDrive 404. Every null-class shape: sites/documents/init all 403. The non-matching strings get 200 with nothing of A's. |
| T-proto | Body `{"__proto__":{organizationId:A},"constructor":{"prototype":…}}` sent with an org-less token | 403/403, and `Object.prototype.organizationId` stays undefined. |
| I | `init` with B's token and A's org in the body | 201. The row is owned by B (DB row and API agree). A gets 404, B gets 200. |
| D | B's own connection with A's site ids | See N4. |
| C1/C2 | The callback attacks | See N2. |
| Q4 | The warm-map owner case | See N3. |
| TM | Timing | See N5. |
| CENSUS | Route census | See Q1. |

### Negative control: the same file against develop's `index.ts`, swapped in and then restored, with `cmp` confirming

- **All 14 O cells, S, T, T-proto, I and D are red.**
- C1, C2 and Q4 pass on develop. They are observation cells, and their develop readings are what the N2/N3 tables compare against.

## Q3 — Existence oracle

- **Per route,** the "not yours" answer equals the "unknown id" answer in status, body bytes and headers (ETag and Content-Length included). Measured by the O cells above.
- **Confirmed the author's per-route note:** `POST /api/sites` and `POST /api/documents/sync` answer 400 = 400 rather than 404.
- **The DB-first lookup** is taken for both foreign and unknown ids (count 1 = 1). Timing class: N5.
- **The unauthenticated callback** is an oracle by redirect. That is N2, outside the bound set.

## Q5 — Cells can fail (each mutant compiled; tsc rc 0 for all; `index.ts` restored and `cmp`-verified after each run)

| mutant | author pass/fail | author reds | gate reds |
| -- | -- | -- | -- |
| M1: `ownedBy` without the equality | 17/16 | A1 A3 A4 A6 B1 A7 A8 A9 A11 A12 A14 A15 A17 A19 A21 I1: **identical to the claim** | 14 O + S, T, I, D |
| M3: `GET /api/sites` unfiltered | 30/3 | A7 A8 C1: **matches the claim** | O sites, T |
| M5: `ownedMemConnection` ignores ownership (`callerOrg(req); return connection;`, so no unused-parameter error) | 30/3 | A6 A19 A21: **matches the claim** | 3 O, S, T |
| MB: `GET /api/connections/:id` foreign 404 body differs by one trailing space | 32/1 | **B1**, so B1 compares bytes | O GET conn |
| X1 (mine): `GET /api/documents/:id` check reverted to `if (!doc)` | 32/1 | A15 | O GET doc |
| X2 (mine): documents/sync `memSites.get` | **33/0, survives** | none | D (see N4) |
| X3 (mine): `init` prefers `req.body.organizationId` | 32/1 | I1 | I |
| X4 (mine): `DELETE /api/sites/:id` uses `memSites.get` | 32/1 | A11 | O DELETE site |

**The author's file against develop's `index.ts`:** 22 failed, 11 passed, out of 33. This matches the claim.

## Q6 — Spec

- `npm run check:openapi --prefix <clone>` RC 0: "CHECK PASS: on-disk YAML matches generated" and "every published example resolves".
- **Positive control:** I re-added `organizationId` to the `z.object(` lines of `m365-integration.openapi.ts` and ran `generate-openapi -- --check`. RC 1, "CHECK FAIL: generated YAML differs". File restored afterwards.
- **The YAML delta is confined** to `components.schemas.M365InitConnectionRequest`: the property, `required` and the example (4+/6−).
- `/m365/connections/init` already publishes `"403"`.

## Q7 — Landing

- **Merge tree and three-dot:** as above.
- **Full m365 suite at head (= the landing tree):** 12 files, **114/114**, RC 0. Run twice: once with the service-local install, once after the root workspace install.
- **Product `tsc -p tsconfig.json --noEmit`:** RC 0.
- **Test file:** type-checked through an override config with `include src/**/*`, `types node, vitest/globals`. RC 0.
  - Controls: `--listFilesOnly` finds the file in the override program (1) and not in the default program (0).
  - A planted `const __gateCtl: number = "not a number"` in the author's test file gives RC 2, with TS2322 at line 444. File restored from a copy afterwards.

## How it was run

- **Clone:** `git clone --shared` of the cache clone into `scratchpad/gate_as1`. `core.sshCommand` set to the Secuura deploy key. Fetched `refs/pull/1633/head` and develop, then detached at `76725fd4a`.
- **Install and build:**
  - `packages/shared`: `npm ci --ignore-scripts`. The `blake2` native build fails on this toolchain with a tapi "unknown architecture" error, so scripts were skipped. Then `npm run build`.
  - Then `npm ci --ignore-scripts` at the clone's workspace root.
- **Paths:** every npm/vitest/tsc/tsx call used absolute `--prefix`, `--root`, `-p` or binary paths into the clone. Nothing ran from the Wednesday cwd.
- **Ports:** every HTTP listener ran inside vitest on `127.0.0.1:0` (an ephemeral port), not 55480-55489. No standalone server was started.
- **Processes:** none left running. `ps` shows only another gate's vitest (`gate_at1`), which I did not touch; that line is also the instrument's positive control.
- **Logs:** `scratchpad/as1_logs/` (`attack_head.log`, `attack_develop.log`, `mutants_summary.txt`, `mut_*.json`, `census.log`, `tsc_*.log`, `openapi_*.log`).

## NOT RUN

- **Preflight leg 3 (spec-auth) and leg 8 (served-spec)**, and the stack on :6882: they need Docker, which this Studio does not have and which the brief forbids. **Not faked.**
- **Leg 4, Schemathesis, Akto, Playwright, k6:** same reason.
- **Live Postgres:** not run, so the RLS/reload claims in N3 and the data impact in N1 are reasoned from the migrations and code.
- **Linear:** KS-1673 and KS-1675 not read (no Linear tool in this session).
- **Real Microsoft Graph or MSAL:** never called. Graph-side authorisation for the raw `siteId` fallback (N4) is reasoned only.
- **HEAD-method variants:** not exercised separately (Express maps them to the GET handlers).

## Wednesday tree check

`git -C /Volumes/DevMASTER/WEDNESDAY status --short` before this file was written showed:
- ` M 0_Brain/dashboard/data/usage_wednesday.json`
- `?? 0_Brain/reference/2026-10-20_gate-AU1-pr1634-ks1658/verdict.md`

Neither is mine. **No untracked path outside the allowed folders.** My only write in this tree is this file.

**The final re-run, just after writing this file, showed three NEW untracked paths outside the allowed folders.** All three are under `fleet/hooks`/`fleet/tests`, not `fleet/briefs_staged`:
- `?? 2_Project_Files/fleet/hooks/pretooluse_no_cd.sh.new`
- `?? 2_Project_Files/fleet/hooks/pretooluse_no_cd.sh.pre-1020-gitdir`
- `?? 2_Project_Files/fleet/tests/no_cd_gitdir_arms.sh`

**They are not mine.** I never wrote under `2_Project_Files/`, and they were absent from the earlier check. They look like a concurrent session editing the no-cd hook. Reported as the brief requires; whoever owns them should claim them.

sha256: 61f15ace0df54e9d00f475f70632b7b2503fbfe611b3d797f178fe1606c275f5
