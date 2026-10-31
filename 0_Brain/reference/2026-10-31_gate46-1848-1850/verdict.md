## QA GATE 46 - TIER 1, ROUND 1 (batched) - Secuura/Blockchain (Platform K) - KS-1410 - Sat 31 Oct 2026
Findings only. Nothing pushed, commented, merged or mailed. Nothing under !CODING written. Clone `repo/`: toplevel asserted before the fetch, push URL `no_push_qa_gate`, `git status --porcelain` = 0 lines at the end. ls-remote at 10:32 and 11:07 AEDT: #1848 = a50a420a480f, #1849 = a1214248ccf6, #1850 = aa858a8453ce, develop = cb2320368ae4. All three match R's heads. All three share merge-base a8c554659cb3, and none of the three product files has changed on develop since then (blob-equal). Load ~7.5-11. Runs were one at a time with `--maxWorkers=2`.

**Summary: #1848 GO WITH NOTES · #1849 GO WITH NOTES · #1850 GO WITH NOTES.** The only fix-before-merge item is the DOCS-HOLD html conflict (F1).

### Blob table (`git diff --name-only mb..head`, rev-parse at mb / head / develop)
| PR | file | mb -> head | develop |
|---|---|---|---|
| 1848 | tenant-provisioning/src/index.ts | 387ed875 -> 2e49eb19 (+12 -6) | 387ed875 |
| 1848 | __tests__/ks1410-provisioning-500-... (new) | -> 4e0feddc (+78) | absent |
| 1849 | api-gateway/src/routes/platform.ts | bbdb015d -> 96955580 (+5 -2) | bbdb015d |
| 1849 | __tests__/ks1410-platform-templates-500-... (new) | -> 748c73e0 (+70) | absent |
| 1850 | mcp-server/src/http-server.ts | fce4a317 -> 3f372ce7 (+18 -9) | fce4a317 |
| 1850 | __tests__/ks1410-mcp-http-500-part-a / part-b (new) | -> 2d5212f9 / 973d7c7f | absent |
| all | the 2 Projects Documents html | 60aa336c/bdba7f56 -> a different blob in each PR | 2b5ffe9f/78638473 |
No other files are in any of the three PRs.

### Common to all three
- **F1 Mechanical. Fix before merge: YES (DOCS HOLD).** `git merge-tree --write-tree origin/develop pr/N` returns rc 1 for every PR. The conflicts are ONLY in the two html files (`probes/mergetree_{1848,1849,1850}.txt`). The three PRs also carry three different blobs of the same two html files, so they will conflict with each other in turn.
- **F2 Info. Fix before merge: no.** All four new test files are source-text guards. They take only the single line that holds `.status(500).json(`. A leak placed on the NEXT line SURVIVES R's tests in every service: mutants T3, P3 and K2. My behavioural probes kill all three. Suggestion: add a behavioural cell (the harness pattern from ks1544 / ks1510).
- **F3 Info. Fix before merge: no. Pre-existing and identical at base.** `const message = err instanceof Error ? err.message : String(err)` still runs inside every catch. Four kinds of thrown value make that line throw: a null-prototype object, a `toString` that throws, a `message` getter that throws, and a revoked Proxy. The handler then gives NO answer and raises an unhandled rejection. My probes show the same result at head and at base, in tp, platform.ts and mcp. Effect in production:
  - tenant-provisioning and mcp-server have no handler, so Node's default exits the process.
  - The gateway runs in `survive` mode (index.ts:1187-1201), so the request hangs instead.
  - Reachability: pg, fetch and fs throw only Error objects, so I found no way for a request to cause it.
  - platform.ts's own KS-1771 / KS-1524a "describe the value in its own try" pattern was not applied to the lines this PR rewrote.

---
# A) #1848 tenant-provisioning - VERDICT: GO WITH NOTES
**(1) Behaviour.** Probe `probes/g46-tp-behaviour.test.ts`, which runs the real module with pg replaced by a thrower (the ks1544 harness). Output: `tp_behaviour_head.json`.
- Kinds tested: Error, string, number, object with toString, object with toPrimitive, AggregateError, a 2 MB message, undefined.
- Head: all 6 routes x 8 kinds answer 500 with exactly `{success:false,error:{code:'INTERNAL_ERROR',message:'An unexpected error occurred'}}`. The SECRET marker is in no body. /health is still 200 after every kind.
- Positive control: the same probe on base index.ts gives 8 FAIL with SECRET in the body (`tp_behaviour_base.log`). Exotic kinds: see F3.

**(3) Every 500 site in index.ts.** There are 7 `.status(500)` sites:
- The 6 changed ones are now constant.
- POST /api/tenants (:361) still answers `message: message`. This is deliberate and pinned by R's C2 (Kam's card ks1240).
- The other catches (:117, :126, :295, :325, :357, :556, :567, :613) only log or continue; none of them sends a response.
- Final fallback: shared `errorHandler` (packages/shared/src/errors/index.ts:230). It sends a constant 'An unexpected error occurred' for anything that is not an AppError.

**(4) Consumers.** In the gateway, GET /:id, PATCH /:id, PATCH /:id/status and DELETE /:id forward with `res.status(r.status).json(data)`. GET /api/platform/tenants (platform.ts:301-306) uses `res.json(data)`, which turns an upstream 500 into a gateway **200** (F5).
- Admin UI (`frontend/admin/src/services/api.ts:1016-1082`): fetchTenants, fetchTenant, updateTenant, updateTenantStatus, deleteTenant and fetchPlatformAuditLog read only `res.ok`. Only createTenant (POST, unchanged) reads `res.error`. **Nothing breaks.** This closes R's "admin UI render not checked".
- Spec: `ErrorResponse.error.message` is a required string and `details` is optional (packages/shared/src/openapi/responses.ts:44-60). The gateway spec declares a 500 response with that schema for all six forwarded routes (`probes/secuura-api.yaml`, parsed with node `yaml`). The new body conforms.

**(5) R's claims.**
- Red-first confirmed: Spark's deterministic run gives BASE 3 pass / 3 fail and HEAD 6/6. Note that the 3 that pass on base are R's controls, not handlers.
- Suite 8 files / 54 tests pass (`tp_suite_head.log`). The base figure 7/48 matches arithmetically (one new file of 6 tests).
- tsc -p tsconfig.json: rc 0 with 0 errors. Positive control: an injected TS2322 is reported. R's "2 pre-existing TS2835" do not reproduce under this tsconfig, which excludes `__tests__`.
- Mutants (`probes/mut1848/summary.txt`, file restored by sha256 6a0ef68d...): 6 of 6 killed.
  - T1 (back to `message: message`), T2 (adds `hint: message`), T4 (adds `String(err)`), T5 (drops console.error), T6 (`.send(message)`): R's tests kill them.
  - T3 (leak on the next line): R's tests PASS it; my probe kills it (F2).
- **F4 Info. Fix before merge: no.** The thrown text is logged verbatim and unbounded. The 2 MB message went to stderr in full.
- **F5 Info. Fix before merge: no. Pre-existing, outside this PR.** The gateway's GET /api/platform/tenants answers 200 when the upstream answers 500.

# B) #1849 api-gateway platform.ts - VERDICT: GO WITH NOTES
**(1) Behaviour.** Probe `probes/g46-gw-behaviour.test.ts`: the real createPlatformRoutes over HTTP, with pg.Pool.prototype.query rejecting, and the clone route's tenant lookup answered by a local stub.
- Head: document-types, workflows (bare-catch control) and clone-to-tenant answer exactly `{success:false,error:{code:'INTERNAL_ERROR',message:'Failed to fetch templates'|'Clone failed'}}` for Error, string, toString object, AggregateError, the 2 MB message and undefined. There is no `details` and no SECRET.
- Positive control: base platform.ts gives 6 FAIL (`gw_behaviour_base.log`).
- Exotic kinds give no answer on document-types and clone (F3). Under `survive` mode the gateway does not exit.

**(3) Every catch in platform.ts.**
- 500 sites: there are 4 (:996, :1020, :1094, :1173) and all are constant.
- sendUpstreamError (:236-251) sends constant 502/504 bodies. The proxied tenant routes use it.
- The audit-log catch (:505) only logs and degrades.
- 502s at :688, :874 and :891 are constant, apart from the upstream status code.
- No other catch answers with thrown text.

**(4) Consumers.** `details.detail` / `details?.detail` readers in Blockchain/: 0 hits. Positive control: the same grep for `details?.` finds 5 frontend files. The templates routes have 0 consumers outside platform.ts and developer-portal.html.
- **F6 Info. Fix before merge: no.** The three templates routes are not in `docs/openapi/secuura-api.yaml`. Control: the /api/platform/tenants* entries are found in the same parse.

**(5) R's claims.**
- Red-first confirmed: Spark BASE 3 pass / 2 fail, HEAD 5/5.
- api-gateway whole suite: **131 files / 1326 tests pass** (`gw_suite_head.log`).
- Leg 16 (`scripts/preflight/test-types-ratchet.sh services/api-gateway`): "27 errors: 27 in the baseline, 0 new". Positive control: an injected test-file error gives "1 new" and FAIL (`leg16_gw.txt`).
- Mutants (`probes/mut1849/summary.txt`, restored by sha256 7f0af9d2...): 5 of 5 killed.
  - P1 (details back), P2 (console.error dropped), P4 (`err?.message ?? constant`), P5 (`.status(500)` / `.json` split across lines): R kills.
  - P3 (leak on the next line): R passes it; the probe kills it.
- Scope note: platform.ts is not one of KS-1410's six named files. The change is correct, but it falls outside the ticket's stated list.

# C) #1850 mcp-server http-server.ts - VERDICT: GO WITH NOTES
**(1) Behaviour.** Probe `probes/g46-mcp-behaviour.test.ts`: real module, with api-client and package-generator replaced by throwers and hashing left REAL.
- Head: the 8 directly reachable changed routes answer 500 with the constant body for all 8 safe kinds. /verify answers `{verified:false,error:'An unexpected error occurred'}`.
- The outer 500 of /verify-batch cannot be reached through any value that `String()` can describe. With `[null]` it returns 200 with a per-item TypeError text. Its outer catch is shown constant by the exotic-kind path.
- Positive control: base gives 8 FAIL with SECRET in POST /register (`mcp_behaviour_base.log`).
- Exotic kinds give no answer plus 7 unhandled rejections; this service has no handler, so the process would exit (F3).

**(2) Batch per-item text in a 200.**
- **F7 Minor. Fix before merge: no (R disclosed it). Same leak class (thrown text reaches the caller), in a 200.** http-server.ts:104-106 and :165-167.
  - Measured: an upstream Error ('SECRET-E gateway 10.0.0.7:6882') appears verbatim in `results[i].error` for /register-batch and /verify-batch.
  - The 2 MB message is echoed in full (an amplification of up to 50 items per call).
  - fs errno text appears verbatim: `ENOENT ... open '/nonexistent...'` and `EISDIR ... read '/etc'`.
  - /verify-batch is `security: []` in the spec. Suggest a follow-up card: give a constant per-item error and log the cause.
- **F8 Major, pre-existing, out of scope for KS-1410. Fix before merge: no. Needs its own card.** POST /hash (:41-63, untouched by design) and the `filePath` field of /verify, /register-batch and /verify-batch read ANY server path with no auth on this server.
  - /hash `/etc/hosts` returned 200 with its sha256.
  - /hash `/etc` returned 500 `EISDIR`; a missing path returned 500 `ENOENT ... '<path>'`.
  - That gives a server filesystem existence/type oracle plus a hash of any readable file.
  - Exposure: compose comments out the host port (docker-compose.yml:2148). The gateway proxies only /generate-package (proxy.ts:1289-1314). The deployment docs, however, tell users to expose :7890 through a tunnel for ChatGPT Actions.
- **F9 Info. Fix before merge: no. Pre-existing.** mcp-server has no `errorHandler`. Malformed JSON gets Express's finalhandler: an HTML 400 with the parser message, which quotes the body, plus a stack under NODE_ENV=test. The container sets `NODE_ENV=production` (Dockerfile:48), which hides the stack; I did not run production mode (see NOT TESTED).

**(3) Every catch in http-server.ts.** There are 10 `.status(500)` sites:
- 9 are constant.
- /hash still leaks (F8).
- The 2 per-item catches leak into a 200 (F7).
- There are no other catches.

**(4) Consumers.**
- The gateway's /api/mcp/generate-package forwards a non-ok body verbatim (proxy.ts:1300-1303). It now forwards the constant, which is an improvement.
- The generated CI script reads `.verified // false` only (package-generator.ts:688).
- The MCP Deployment docs have no `.error` readers.
- **F10 Info.** Both openapi.yaml copies (same blob 3726a940) declare NO 500 response and no `error` property anywhere: 0 hits for `error`, against 9 hits for `"200":` as a control. So the spec does NOT say error is an optional string; it says nothing. The PR changes nothing in the spec. ChatGPT Actions clients themselves were not run.

**(5) R's claims.**
- Red-first confirmed: Spark BASE 8 pass / 6 fail, HEAD 14/14.
- Suite 8 files / 44 tests pass (`mcp_suite_head.log`); base 6/30 matches arithmetically.
- tsc: rc 0, 0 errors.
- Mutants (`probes/mut1850/summary.txt`, restored by sha256 65987db2...): 5 of 5 killed.
  - K1 (/verify back to `error: message`), K3 (generate-package back to message), K4 (console.error dropped), K5 (`detail: String(err)`): R kills.
  - K2 (/policy leak on the next line): R passes it; the probe kills it.

---
**NOT TESTED:** real Postgres; a running stack or gateway in front of the services; ChatGPT Actions or any external client; the mcp-server finalhandler under NODE_ENV=production; the base suites as runs (base counts are arithmetic, plus Spark's targeted base runs); the full suites of other services (no other product files changed); the stdio MCP tools (tools/verify.ts carries its own `error: message`, outside this PR); deploy.

**HOW:**
- Clone and setup: `git clone --shared --no-checkout` from gate 36's clone into the non-existent `repo/`; toplevel asserted; remote set with the Blockchain deploy key as core.sshCommand; push URL no_push_qa_gate (the gate 45 method). Fetched refs/pull/{1848,1849,1850}/head and develop. `npm ci` (1806 packages); built `packages/shared` and the services, then stopped my own build before the frontends.
- Checkout and tools: one tree, checked out at each PR head in turn (the PRs touch disjoint files). Repo vitest via `npx --prefix <svc> vitest run --root <svc> --maxWorkers=2`.
- Probes were copied into `src/__tests__` only for their runs and then moved to `probes/_quarantine_2026-10-31/` (not deleted). Mutants: `probes/mut.py` (unique anchor, restore and sha256 assert after each mutant). Base controls swapped the one product file and restored it by sha256.
- Instrument faults:
  - The first tp probe timed out on a 10 s hookTimeout (cold transform); fixed by raising it to 60 s.
  - The T4 "unicode identifier" mutant collapsed to a plain `String(err)` mutant in the heredoc, and is reported as such.
  - The first mcp verify-batch cell was mis-designed (inner catch); corrected.
  - The `NODE_ENV=production` malformed-JSON cell is invalid, because Express fixes the env at import.

**Spark shadow** (`spark_gate.sh` per PR, work dirs in the session scratchpad, `--node-modules` set; `spark_review.py` saved in `probes/spark/`).
- Deterministic facts match mine exactly: 3/6 -> 6/6, 3/5 -> 5/5, 8/14 -> 14/14.
- spark_review gave GO WITH NOTES for all three, with Notes only (6, 8 and 5).
- It correctly flagged that the tests are source-text only (my F2) and the /hash and per-item leaks (F7, F8 in part). It did not measure the next-line blind spot, F3, F5, F8's file-read oracle or the consumer analysis.
- It said "the gateway forwards are only grepped" (closed here) and gave #1849's ticket title as "fetch failed: IndexError", which looks like a wrong ticket text fetch. There were no false Majors.
