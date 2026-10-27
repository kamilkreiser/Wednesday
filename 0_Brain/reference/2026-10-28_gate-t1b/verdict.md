# QA gate: tier 1 (G1): Secuura/Blockchain #1767 (KS-1771) and #1766 (KS-1772)

- **Tier:** 1 (G1: catch-block changes on the request path in two services, api-gateway and originate)
- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), subagent of Wednesday. I did not author any of this work.
- **Window:** 2026-10-27 16:57:05Z → 17:11:14Z for the run, plus write-up (2026-10-28 ~03:57–04:20 AEDT)
- **Workspace:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-t1-1028b/`
  - clone: `repo/`
  - worktree: `wt/`, detached and switched between `refs/gate/a` and `refs/gate/b`
  - logs: `out/`
  - gate scripts: `gate-src/`
  - mutant copies: `mutants/`
  - TMPDIR: `/tmp/gt1b`
- **Pushed / merged / commented / edited: nothing.**
  - I ran no git command against `!CODING/Secuura/Blockchain/2_Project_Files` or its worktrees.
  - I used no docker, no az, and no network beyond fetch and ls-remote.
  - I started no long-lived processes, so I stopped none. The loopback listeners lived inside the test runners and closed with them.
- **Gate worktree at the end:** `git status --porcelain` is empty.
  - Every swap was restored with `git checkout` and checked by sha256: `out/*-sha-{before,after}*.txt`, and `restore_ok: true` for all 14 mutants in `out/mutants-{a,b}.json`.
  - The driver files were moved out to `out/_moved/`.

## Pins

All values come from ls-remote against `git@github.com:Secuura/Distributed_Secuura.git`. Start is `out/ls-start.txt` and end is `out/ls-end.txt`.

| ref | start | end |
|---|---|---|
| develop | abdeb51c7627459172760c3a279b03c61bbaeeec (= brief) | **4131ed6108bb9a44cb7a6feeb288015ccfaed1eb (moved; see F9)** |
| refs/pull/1767/head | f293d9b34b1ebb888aeddf10ef62909121abbd70 | same |
| refs/pull/1766/head | 7389621fe9fcc9c044c98e5272baff7b50f41861 | same |
| refs/pull/1756/head (Peter) | 5d42cbd455184b33bad6a7a67bcf4b9071c63d31 | same |

- **#1767** is one commit, f293d9b34, on base 9b698b7aa1f8. develop is not its ancestor. 8 files, +367/−6.
- **#1766** is 127b24313 plus two merges of develop (9b698b7, then abdeb51). develop@abdeb51 is its ancestor. 7 files, +364/−8.

### Merge-tree (`git merge-tree --write-tree`)

| pair | rc | conflicts |
|---|---|---|
| #1767 × develop@abdeb51 | 1 | the two Projects Documents HTML files only. Both sides append at the tail; this is expected and resolved at merge. |
| #1767 × develop@4131ed6 (end) | 1 | same two docs only |
| **#1767 × Peter #1756** | **0** | none |
| #1766 × develop@abdeb51 | 0 | none |
| #1766 × develop@4131ed6 (end) | 0 | none |
| #1766 × Peter #1756 | 0 | none |
| #1767 × #1766 | 1 | the two docs only. Whichever PR merges second has to resolve a tail append. |
| Peter #1756 × develop@4131ed6 | 0 | none |

Peter's PR cannot be made to conflict by #1767, whichever way its docs conflict is resolved. The reason is that the two PRs touch different parts of every shared file:
- Peter's hunks in `verification.ts` are at `:18`, `:544` and `:885`. #1767's only hunk is at `:1064`.
- Peter's hunks in the Cheat Sheet are at `:436` and `:1634`. Every append in this batch is at the tail, around `:5050` and later.

## BLUF

| PR | verdict | worst finding |
|---|---|---|
| #1767 KS-1771 (api-gateway) | **GO** | INFO only. The docs tail conflicts with develop (F9), which is expected and handled at merge. |
| #1766 KS-1772 (originate) | **GO WITH NOTES** | LOW (F6): the five describer sites are fixed, but originate catches that **read the thrown value before calling fail500** still hang. Measured at `routes/systemErrors.ts:196` (`err instanceof z.ZodError`): a revoked Proxy or a Proxy whose getPrototypeOf trap throws still gets NO response at the head. This is outside the ticket's named sites, so it is not a defect of this PR. It is a follow-up. |

There is no MAJOR or MINOR finding in either PR. Each PR's claim holds at every named site, measured through a real Express app over loopback with hostile values of my own choosing. Describable values log byte-for-byte as before, and the controls are green at the head.

## Findings

### F1: INFO: #1767 diff read whole. Only the six named sites changed.
- The api-gateway hunks are these, with line numbers at the head (all files under `Blockchain/Dev/services/api-gateway/src/`):
  - `routes/audit-export.ts:28-41`: fail500
  - `routes/audit-export.ts:197-210`: the 502 catch
  - `routes/batch.ts:28-41`
  - `routes/notifications.ts:30-43`
  - `routes/platform.ts:508-521`: `logger.warn`, which keeps `windowsRead`
  - `routes/verification.ts:1067-1080`
- Each site's describer expression is character-identical to the line it replaces. Only the wrapping changed: a describe try with fallback `'thrown value that could not be described'`, then a separate log try. Each site's constant response line is unchanged.
- **The #1754 site is unchanged.** `platform.ts` has exactly one hunk (15 changed lines, at `:505`). The document-lookup catch, now at `:1148-1170`, is byte-identical to base.
- **The controls are untouched.** `ks1346-apigw-fail500-logs-type-and-field-names.test.ts` and `ks1510-document-lookup-logs-the-thrown-error.test.ts` show an empty diff from base to head.
- **Coverage is complete.** `git grep "getPrototypeOf(err"` over the non-test api-gateway sources at the head returns exactly 7 sites, and all 7 are now wrapped (the 6 named sites plus #1754's).

### F2: INFO: #1766 diff read whole. Only the five named sites changed.
- The originate hunks are these (under `services/originate/src/`):
  - `routes/adminConfig.ts:111-125`: fail500
  - `routes/adminConfig.ts:2246-2263`: the per-tenant catch
  - `routes/gdpr.ts:211-225`
  - `routes/systemErrors.ts:94-108`
  - `routes/webhooks.ts:573-587`
- **The `TENANT_COPY_FAILED` row is unchanged.** `results.push({ tenant: tenant.slug, error: 'TENANT_COPY_FAILED' });` is diff context, not a changed line, and it still sits outside both tries. The log meta still carries `tenant: tenant.slug`.
- **The controls are untouched.** ks1346a-d and ks730c show an empty diff from develop.
- **Coverage is complete.** `git grep "getPrototypeOf("` over the non-test originate sources returns exactly the 5 sites, all wrapped.

### F3: INFO: #1767 before/after, measured by the gate's own driver
- **Driver:** `gate-src/gate-t1b-apigw.test.ts`. It differs from the author's harness in four ways:
  - It uses one real Express app over loopback for **all** sites. The author used fake req/res dispatch for four of them.
  - It has a final error handler that answers **599**, so "Express caught a synchronous throw" can be told apart from "no answer".
  - It drives **different routes** for three of the helpers: notifications `GET /unread/count`, batch `POST /verify`, and audit-export fail500 through a `role` getter.
  - In the platform case, the **second** window's body read throws after a full first window, so `windowsRead: 1`. In the author's case the first window throws.
- **Values (8 per site):**
  - 2 controls: a plain Error, and a plain object `{code, detail}`.
  - 5 hostile values. Four are the author's shapes: a throwing `message` getter, a Proxy whose getPrototypeOf trap throws, a revoked Proxy, and a logger that throws. One is my own: **a prototype whose `constructor` read throws**.
  - 1 combined case: the logger throws **and** the value is undescribable.
- **Base** is 9b698b7's five route files, swapped in and then restored with the sha checked. Results are in `out/apigw-before-after.txt`.

| site | base: hostile values (6) | head: hostile values (6) | controls (base = head) |
|---|---|---|---|
| notifications fail500 (sync handler) | answered **599 by the Express error handler** (not the route) | 500 INTERNAL_ERROR, the fallback logged | 500, `gate control` / `thrown Object with fields [code, detail]` |
| batch fail500 | **NO ANSWER**, 1 unhandled rejection each | 500 INTERNAL_ERROR | 500, same lines |
| audit-export fail500 | **NO ANSWER** | 500 INTERNAL_ERROR | 500, same lines |
| audit-export 502 catch | **500 from the outer fail500** under the wrong log context; the combined case got **NO ANSWER** | **502 BAD_GATEWAY**, the 502 context logged | 502, same lines |
| platform audit-log catch | **NO ANSWER** | **200 degraded page**, warn carries `windowsRead: 1` | 200, same lines |
| verification document-types | **NO ANSWER** | 500 `Failed to fetch document types` | 500, same lines |

- **Totals for hostile values:**
  - Base: 25 of 36 got no answer. The other 11 got the wrong answer (6 got 599 from the error handler; 5 got the 500 from the outer catch).
  - Head: **36 of 36 got the route's own constant answer**, with 0 unhandled rejections.
- The author's per-site comments match what I measured. That includes the notifications comment ("synchronous, so Express handed the throw to the gateway's errorHandler") and the audit-export 502 comment ("answered by fail500's 500 under a different log context").
- **The author's cells at base:** I swapped in the base routes and ran their `ks1771` file. Result: **30 failed / 6 passed of 36, with 20 errors (unhandled rejections)**. This matches the author's claim (`out/author-cells-base-a.log`).

### F4: INFO: #1766 before/after, measured by the gate's own driver
- **Driver:** `gate-src/gate-t1b-originate.test.ts`. It uses real routers over loopback, the same 8 values, and a 599 error handler. Its routes differ from the author's:
  - systemErrors `PATCH /:errorId/resolve`
  - gdpr `GET /retention`
  - webhooks `GET /`
  - adminConfig fail500 through migrate-tenant-data's **outer** catch (`getPlatformPool` throws)
  - the per-tenant catch with **three tenants, the middle one throwing**, so tenants before and after it are both visible
- **Base** is develop@abdeb51's four route files, swapped in and then restored with the sha checked. Results are in `out/originate-before-after.txt`.

| site | base: hostile values (6) | head: hostile values (6) | controls |
|---|---|---|---|
| systemErrors fail500 (PATCH resolve) | NO ANSWER | 500 INTERNAL_ERROR, the fallback logged | unchanged |
| gdpr fail500 (GET /retention) | NO ANSWER | 500 | unchanged |
| webhooks fail500 (GET /) | NO ANSWER | 500 | unchanged |
| adminConfig fail500 (migrate outer catch) | NO ANSWER | 500 | unchanged |
| per-tenant catch (3 tenants, middle throws) | **500**, tenants asked `01`, so the loop stopped and tenant c was never tried. The combined case got **NO ANSWER** (the outer fail500 threw as well). | **200**, asked `012`, rows `a=copied, b="TENANT_COPY_FAILED", c=copied`, log `[tenant step, gate-b, fallback]` | 200, same rows at base and head |

- **The author's cells at base:** I swapped in develop's routes and ran their `ks1772` file. Result: **25 failed / 5 passed of 30**, which matches the author's claim (`out/author-cells-base-b.log`).

### F5: INFO: my own mutants, on copies under `mutants/`, all killed
- **Script:** `gate-src/mutants.py`.
- **Method:** each mutant reads the head file and writes a mutated copy under `mutants/`, outside `src/__tests__`. The copy must pass an esbuild parse. The script then swaps the copy in, runs the kill set, restores with `git checkout`, and checks the sha256 before and after (`restore_ok` is true for all 14).
- **Kill sets:**
  - A: ks1771, ks1346-apigw and ks1510, 66 cells.
  - B: ks1772, ks1346a-d and ks730c, 119 cells.

| mutant | cells that fail (kill) |
|---|---|
| MA1 verification.ts:1067 describe try removed | 4: the ks1771 verification describe arms |
| MA2 batch.ts:28 **log try removed** | 1: ks1771 batch "log arm" |
| MA3 platform.ts:508 describe try removed | 4: ks1771 platform describe arms |
| MA4 audit-export.ts:184 502 **log try removed** | 1: ks1771 502 "log arm" |
| MA5 notifications.ts:30 both tries removed (= base) | 5: 4 describe arms + the log arm |
| MA6 audit-export.ts:28 fallback text changed | 4: describe arms (they pin the exact fallback string) |
| MA7 platform.ts:1148 (#1754 site) log try removed | 1: ks1510 L8, so the read-only control still guards #1754 |
| MB1 gdpr.ts:211 describe try removed | 4: ks1772 gdpr D1 ×4 |
| MB2 adminConfig.ts per-tenant **log try removed** | 1: ks1772 per-tenant L1 |
| MB3 adminConfig.ts per-tenant describe try removed | 4: per-tenant D1 ×4 |
| MB4 webhooks.ts:573 **log try removed** | 1: webhooks L1 |
| MB5 systemErrors.ts:94 both tries removed (= base) | 5: D1 ×4 + L1 |
| MB6 adminConfig.ts:111 fallback text changed | 4: adminConfig D1 ×4 |
| MB7 per-tenant row pushed **inside** the log try | 1: per-tenant L1 (the row is lost when the logger throws) |

- 14 of 14 mutants were killed. Each describe-try mutant and each log-try mutant is killed by its own arm and by nothing else, which confirms the author's "the two arms are separate on purpose".
- My drivers assert nothing (they always pass). They are measuring instruments, not guards, so every kill comes from the PRs' cells and the controls.

### F6: LOW (#1766): catches that read the thrown value before fail500 still hang (outside the ticket's sites)
- **Location:** `services/originate/src/routes/systemErrors.ts:196` at the head, in `GET /api/system-errors`: `if (err instanceof z.ZodError) {` runs before `fail500`.
- **Measurement** (gate driver, site "systemErrors GET /"):
  - At the head: **NO ANSWER** for a Proxy whose getPrototypeOf trap throws, for a revoked Proxy, and for the combined case. Jest attributes each to `systemErrors.ts:196:12`, the `instanceof` check, not to fail500.
  - The other three hostile values are answered 500 at the head. They hung at base, so the PR does improve this route.
- **Control:** the same values on systemErrors `PATCH /:errorId/resolve`, whose catch goes straight to fail500, are answered 500 at the head.
- **Extent:** the same class covers about 15 more originate catches that read `err?.message` or `err?.code` before fail500. They are mostly in `adminConfig.ts` (for example `:189`, `:226`, `:289`, `:378`, …, `:1723`), plus `webhooks.ts:320` (`extractPgCode(err)`). The heuristic list is in `out/pre-helper-reads.txt`.
  - For an `?.` read, only the revoked-Proxy and getter-throw shapes bite.
  - The author's test header discloses the adminConfig reads ("a route whose catch first reads `err.message` … would throw THERE"). It does not mention systemErrors `GET /`.
  - The same heuristic finds none in the three api-gateway helper files.
- **Why LOW and not a block:** the ticket names five describer sites, and all five are fixed and pinned. This finding is about the class of bug, not about this diff. The PR title "cannot hang a request" is true only for the describer sites, so a follow-up ticket for pre-helper reads is the right home.

### F7: INFO: suites at the heads (Node v26.8.1, which is not LTS; the same caveat as the author's runs)

**#1767 at f293d9b:**
- ks1771 file: **36/36** (`out/a-ks1771-head.json`).
- With the controls: ks1771 + ks1346-apigw + ks1510 = **66/66**, rc 0 (`out/a-head-targeted.log`).
- Full api-gateway vitest suite (`--testTimeout=60000`): **125 files, 1248/1248**, rc 0, 13.0 s (`out/a-apigw-suite.log`).
- `tsc --noEmit -p services/api-gateway`: rc 0.
- Test-type ratchet (`check.cjs <abs>/services/api-gateway`): rc 0. It examined 160 files (125 under `__tests__`), with 27 errors, all in the baseline: 0 new, 0 stale.

**#1766 at 7389621:**
- ks1772 + ks1346a-d + ks730c: **119/119**, rc 0 (`out/b-head-targeted.log`).
- Full originate jest suite: **141 suites, 1690/1690**, rc 0, 13.5 s (`out/b-originate-suite.log`).
- `tsc --noEmit -p services/originate`: rc 0.
- originate is not in leg 16's list.

**Setup:** `npm ci --ignore-scripts` rc 0. The `packages/shared` build rc 0 and `dist/index.js` is present. `npm run generate --workspace=services/originate` printed "generate: OK".

### F8: INFO: docs, both heads
- `html_docs_check.mjs` on both docs: rc 0 at f293d9b and rc 0 at 7389621.
- `html_docs_matrix.test.sh`: **18 passed, 0 failed** at both heads (`out/docs-matrix-{a,b}.log`).
- **Every change is append-only.** Measured with difflib opcodes against each PR's own base:
  - #1767 Flow Diagrams: one `insert` of 16 lines at 4981 of 4984.
  - #1767 Cheat Sheet: one `insert` of 17 lines at 5050 of 5053.
  - #1766 Flow Diagrams: one `insert` of 16 lines at 4993 of 4996.
  - #1766 Cheat Sheet: one `insert` of 19 lines at 5072 of 5075.
  - Nothing was deleted or replaced.

### F9: INFO: develop moved during the window. Rechecked.
- develop went abdeb51 → **4131ed6** (#1764, KS-1766). The change touches two api-gateway test files only:
  - `ks1543-document-types-catch-logs-the-error.test.ts`: +5/−3. It covers the **same verification.ts document-types catch** that #1767 changes.
  - `ks1628-gateway-documents-verify-is-removed.test.ts`: +3/−1.
- I overlaid develop@4131ed6's two files onto #1767's head and ran them with ks1771: **4 files, 60/60**, rc 0 (`out/a-with-1764-tests.log`). The worktree was restored clean afterwards.
- **#1766 is no longer a strict descendant of develop.** Its merge-tree with 4131ed6 is rc 0, and the two diffs share no files.
- #1767's merge-tree with 4131ed6 is unchanged: the docs conflict only.

## NOT TESTED
- The four platform suites (Schemathesis, Akto, Playwright, k6), and the pre-push preflight legs other than leg 16 for api-gateway.
- A Node 24 LTS run. Everything above ran on Node v26.8.1.
- A real logger transport failure (winston) and real upstreams. All throws were synthetic, through mocks, stubbed `fetch` and stubbed repositories.
- The resolved docs after a merge with develop or with the other PR. The conflict is resolved at merge, so I could not check that file here. Re-run `html_docs_check.mjs` and the matrix on the merge result.
- Express 5 behaviour. Both services pin `express ^4.18`.
- Every other fail500 caller route in each file. I drove 2 to 3 routes per helper. The helper is shared, so this samples the helper's call sites; it does not enumerate them.
- Deploy.
