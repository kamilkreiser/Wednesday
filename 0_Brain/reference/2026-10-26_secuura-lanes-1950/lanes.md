# Secuura Platform K lane sweep - 2026-10-26 ~19:50 AEDT (drafter, read-only)

- Code read at develop **e9e32b76b0483b65eb94cffdcf09da0c9ea46ce2** (Wednesday's clone `2_Project_Files/local-model/spark/cache/src`; `git fetch origin develop` ran there, the sha is present as a commit). All file/line facts below were read with `git show`/`git grep` at that sha. Nothing was run: no test, no build.
- Linear: team KS, state type in {backlog, unstarted, started}, `issues(first:50)` paginated to hasNextPage=false: **15 pages, 705 issues read in total** (Backlog 352, In Progress 284, In Review 41, Todo 25, Blocked 3; assignee: board account 473, unassigned 211, Peter 13, Stuart 8). Comments `comments(first:50)` fetched with each issue, sorted client-side.
- Filter: Backlog/Todo only, minus the exclusion list (30 ids incl. 729/1250/1175), minus Peter/Stuart = **375 candidates**. In Progress (284) not considered: a live worker cannot be ruled out from the board. I read titles of all 375 and, by title/description keyword, the full description plus comments of **about 40**. The other ~335 (mostly ids below 1500, "Security:" titles, decisions, gate-follow-up bundles) were NOT individually read; absence from this file is not a verdict on them.
- Open-PR overlap: UNMEASURED (no gh). Where a file is known to sit in a recent PR's set it is marked.
- Result: **11 tickets qualify firmly in 5 lanes, 2 conditional, 1 contingent big one. Spark-briefable (strict): 0. Near-miss/borderline: 2.**

## LANES (no two lanes share a file; checked by path)

### Lane 1 - vc-issuer (`Blockchain/Dev/services/vc-issuer/`) - Sonnet
Order: KS-1731, then KS-1729. Both touch `ks1683-...test.ts`, so they MUST be one seat, in this order.

| id | title | state / assignee | why actionable | files | test target | size |
|---|---|---|---|---|---|---|
| KS-1731 | GET /api/credentials pages on `ORDER BY created_at DESC` alone | Backlog / board account | Gate measured 24/180 page walks wrong, 0 with an `id` tie-breaker; at develop `credentialRepo.ts:365` still `ORDER BY created_at DESC LIMIT $n OFFSET $m` (by-hash read at `:286` already has `, id DESC`; the unbound `list()` at `:423` also lacks it). | `src/repositories/credentialRepo.ts` (:365, :423); existing mock regexes that will go red and must be updated: `src/__tests__/ks1683-...bound-to-the-creator.test.ts:422` and `ks1116-...test.ts:649` | red-first: add a cell that the SQL ends `ORDER BY created_at DESC, id DESC LIMIT`; vitest in services/vc-issuer. Mocked, no DB needed. | S-M |
| KS-1729 | first run after `npm ci` skips 110 cells (cold import lapses 10 s beforeAll) | Backlog / board | Three files named with line numbers, cause measured (87.5 s cold vs 5 s warm). Fix = give the `freshModules()` beforeAll an explicit hook timeout or move import out of the hook. Ticket gives measurement, shape is a small choice, no ruling. | `src/__tests__/ks1020-...test.ts` (:137), `ks1116-...test.ts` (:259), `ks1683-...test.ts` (:208) | vitest in vc-issuer; cold-run proof needs `npm ci` into a fresh dir (state this in the brief; it is the only way to show red-first) | S-M |

Lane owns: `services/vc-issuer/src/repositories/credentialRepo.ts`, `services/vc-issuer/src/__tests__/{ks1020,ks1116,ks1683}-*.test.ts`.
Note: KS-1683 is on today's taken list; its PR (#1691) is merged per KS-1729/1731 text, but confirm no open follow-up seat still holds the vc-issuer files.

### Lane 2 - systemTest shell support (`systemTest/__tests__/`) - Sonnet
Order: KS-1735, KS-1443, KS-1438. Disjoint from KS-1714 (taken: `pre_suite.test.sh`, `quarantine_call_sites.test.sh`).

| id | title | state / assignee | why actionable | files | test target | size |
|---|---|---|---|---|---|---|
| KS-1735 | generated_guard.sh: failed restore copy unchecked, then stash deleted | Backlog / board | Confirmed at develop: `cp -R ... 2>/dev/null` with no `||`, then `rm -rf "$GENERATED_GUARD_TMP"`. Mirror what KS-1714/KS-1027 did to the two inline copies. | `systemTest/__tests__/support/generated_guard.sh` (restore fn, ~:40-42) | red-first via a failing-`cp` harness as in the inline copies' tests; run `bootstrap_login_diagnosis.test.sh` (sources it, :46) | S |
| KS-1443 | two shell tests assume macOS: `count_my_stubs` greps lsof for `node` (Linux shows `MainThrea`); migrations Cell 5 cannot hide pg_isready in /usr/bin | Backlog / board | Fix shape in ticket ("select by the stub's own PIDs/port"); confirmed `bootstrap_login_diagnosis.test.sh:82-84,163,166` and `run_migrations_failure_exit_code.test.sh:110-111`. Linux proof needs Docker (allowed, no DB). Part 2 shape is cut off in my read: builder reads the rest. | `systemTest/__tests__/bootstrap_login_diagnosis.test.sh`, `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` | both suites; a Linux container run is the red-first | M |
| KS-1438 | html_docs_check.mjs main guard compares resolved URL to unresolved argv, symlinked call exits 0 silent | Backlog / board | One line at `:120`, measured table in ticket (A rc1 / B rc0 same file via /tmp symlink; macOS reproduces on this laptop). Ticket says not firing in the hook today. | `systemTest/__tests__/support/html_docs_check.mjs` (:120) | `systemTest/__tests__/html_docs_matrix.test.sh` + a symlinked-invocation cell | S |

Lane owns: `systemTest/__tests__/support/generated_guard.sh`, `systemTest/__tests__/support/html_docs_check.mjs`, `systemTest/__tests__/bootstrap_login_diagnosis.test.sh`, `systemTest/__tests__/html_docs_matrix.test.sh`, `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh`.

### Lane 3 - shell runner (`Blockchain/Dev/scripts/run-shell-suites.sh`) - Sonnet
Order: KS-1324, then KS-1331 (same two files).

| id | title | state / assignee | why actionable | files | test target | size |
|---|---|---|---|---|---|---|
| KS-1324 | KS-1303 cell decides on a `-lt 6` wall-clock margin; load-sensitive | Backlog / board | Confirmed at develop `run_shell_suites.test.sh:573,575`. Ticket says assert from the verdict, not the clock. Shape partly open (builder picks how to assert "did not wait on the child"). | `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` | that suite | S |
| KS-1331 | untrapped background grandchild survives a signal to the runner | Backlog / board | Fix named: forward the signal to the suite's process group. At develop the trap kills by pid only (`run-shell-suites.sh:306-307`, "kill the suite by pid" :346). Evidence files named. | `Blockchain/Dev/scripts/run-shell-suites.sh` (:300-311, :355-360), same test file | `run_shell_suites.test.sh` signal cells; bash 3.2 caveat: job control is off in the script, `setsid` is absent on macOS, so the builder must choose a bash-3.2-safe way (that is a design step, not a ruling) | M |

Lane owns: `Blockchain/Dev/scripts/run-shell-suites.sh`, `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh`.
Check before launch: `run-shell-suites.sh` is the runner the preflight calls; confirm no seat on KS-1551/1513/1527 edits it (I did not measure their file lists).

### Lane 4 - comment and doc truth (api-gateway doc html + deploy/config comments) - Sonnet, S
Order: KS-1726, KS-1736. Disjoint files, one seat.

| id | title | state / assignee | why actionable | files | test target | size |
|---|---|---|---|---|---|---|
| KS-1726 | five comments call unset GATEWAY_VOUCH_SECRET fail-open/inert; since KS-1032 it fails CLOSED | Backlog / board | Sites confirmed at develop, line numbers have drifted from the ticket: `services.bicep:126` and `:705` and `:843` (ticket said 126/683/821), `docker-compose.yml:608`, `docs/ENVIRONMENT-VARIABLES.md:124` (quotes a `DISABLED` boot line that the code does not print; real line is `FAIL-CLOSED` at `gatewayProvenance.ts:195`). Comment-only. | `Blockchain/Dev/deployment/azure/services.bicep`, `Blockchain/Dev/docker-compose.yml`, `Blockchain/Dev/docs/ENVIRONMENT-VARIABLES.md` | no behaviour test; verify with `git grep -n -i "fail-open\|inert\|DISABLED"` before/after and `az bicep build` or the repo's existing bicep/compose lint legs if present | S |
| KS-1736 | developer-portal.html: "keys minted before that change" has no antecedent; :262 contradicts :564 default | Backlog / board | Wednesday already ruled item (a) Minor and ticketed; ticket quotes the gate's wording idea ("keys minted before the 3,000 default shipped keep ...") as the gate's, not chosen. Pure wording to match `routes/platform.ts:141-148`. | `Blockchain/Dev/services/api-gateway/src/docs/developer-portal.html` (:564, :262) | any existing html docs check (`html_docs_check.mjs`) and a grep cell if the repo pins portal text | S |

Lane owns: the four files above. KS-1473 (same html) is REJECTED so nothing else claims it.
Caution: api-gateway `index.ts` is held by the KS-1635 lane; this lane does not touch it.

### Lane 5 - packages/shared wallet signature - **Opus** (signature verification, crypto)
| id | title | state / assignee | why actionable | files | test target | size |
|---|---|---|---|---|---|---|
| KS-1727 | `wallet-signature.test.ts`: the only positive cell fails on develop, `verifyMessageSignature` returns false for a valid CIP-8 sig | Backlog / board | Reproduced 4x by the filer, alone in 3.4 s; both comments say Node **v26.8.1** only, never tried on Node 24. This laptop is Node 26, so the red reproduces here for free. `wallet.ts:352` read; the verifier has several early `return false` exits (extract key, decode COSESign1, payload equality, Sig_structure). It is an investigation: root cause (Node 26 crypto/CBOR behaviour, or a real verifier bug that also hits the live `/sign-wallet` route `documents.ts:3254`) is not known. | `Blockchain/Dev/packages/shared/src/cardano/wallet.ts` (suspect), `packages/shared/src/__tests__/wallet-signature.test.ts` | `npm test -- wallet-signature` in packages/shared (already red) | M, root cause unknown |

Lane owns: `packages/shared/src/cardano/wallet.ts`, `packages/shared/src/__tests__/wallet-signature.test.ts`. If the cause is a Node-26-only behaviour, the seat should say so and stop: running a second Node line is the only way to separate "verifier bug" from "runtime", and the ticket does not claim either.

## CONTINGENT / CONDITIONAL (not in the core 5)
- **KS-1531** document GET /api/connector/info in the published OpenAPI (new operation + 200 schema + 401/403). Backlog / unassigned. Confirmed absent at develop (count 0 in `docs/openapi/secuura-api.yaml` and `api-gateway.openapi.ts`). Wednesday ruled it a separate change "for whoever builds it"; schema choices are the builder's. Files `Blockchain/Dev/docs/openapi/secuura-api.yaml`, `services/api-gateway/src/api-gateway.openapi.ts`, spec-route-map test; leg 1 of preflight compares generated spec to Zod source, so M and needs a gate. Does not touch `index.ts`. Sonnet C2, **conditional**: confirm KS-1649/KS-1635 seats do not edit the spec files.
- **KS-1667** three comment fixes in originate `documents.ts` + ks1662 header. Still wrong at develop (`documents.ts:1957-1959` says "originate's only call sites are in routes/adminConfig.ts"; ticket says gdprService.ts also calls it; the `039_...:156-157` citation at :1960 is the unscoped one). Comment-only, but `documents.ts` is in the file sets of PRs #1654/#1680 per the 1550 sweep (open/merged unknown) -> **conditional on those being merged**. Sonnet S. (Also the Spark doc_patch near-miss, below.)
- **KS-1505** correct the hot-reload comment in api-gateway `index.ts:614-640` (still says replacement "fires neither watch"), optional hash-compare log. Confirmed present. **Shares `index.ts` with KS-1635** (taken): order it AFTER that seat's PR merges, or fold it into that seat. Sonnet S.

## SPARK candidates
Strict predicate (one product file under services/* or packages/shared, fix spelled out, runnable in-process test nearby, not security, <=3 edit points): **none qualify.** Honest near-misses, for Wednesday to decide whether a doc_patch rung applies:
- **KS-1667** - file `services/originate/src/routes/documents.ts` (comment lines ~1957-1960 plus one more spot) + `src/__tests__/ks1662-...integration.test.ts:20` header. Fix shape quoted from ticket: "Fix the list, keep the conclusion." / "Scope the citation to that, and cite the bypass branch separately (or not at all)." No runnable test to copy (comment-only); 3 edit points plus a third qualifier site. Fails "runnable in-process test"; passes the rest. Conditional on the PR overlap above.
- **KS-1438** - one line `html_docs_check.mjs:120` and the repro table are in the ticket, test `html_docs_matrix.test.sh` nearby. Fails "product path under services/* or packages/shared" (it is `systemTest/`) and the test is a bash matrix, not in-process.
Anything else with a one-line shape is on the Spark's side of nothing today; KS-1731's SQL fix is one line but the mock regexes in two other test files must move with it (4+ edit points).

## REJECTED (id, failing clause)
- KS-1730 Azure EMITTER_SIGNING_SECRET gap: needs a secret-provisioning/deploy decision and the estate was deleted 2026-07-31 (production/ruling).
- KS-1681 DEPLOY-BLOCKERS.md cited but not in repo: ticket says which of two options is "a maintainer call, not an agent one" (ruling).
- KS-1625 Node engines floor: title/body say "decide the floor", deliberately not a fix (ruling).
- KS-1473 portal documents verify-batch: "Owner decision, then one of" (ruling).
- KS-1530 mcp-server falsy allowedDocumentTypes: "A decision first" (400 vs pass-through) (ruling).
- KS-1467 AppError prototype reset: changes the published 422 shape, "decide deliberately" (ruling; also auth service errorHandler).
- KS-1484 userRepo FromRow follow-ups: item 3 "decide listUsersInner"; auth service (security surface).
- KS-1197 non-string verificationLevel: fix lands in the gateway auth middleware that builds the principal (auth surface); comment adds a reachable path via ISSUER_ADMIN (security design).
- KS-1493 verification limiter order: N2 is an owner decision in the same ticket; N1 alone is cell-only but api-gateway `index.ts` is the KS-1635 lane's file.
- KS-1593 connectorContext type-check guard: "facts only, no fix shape chosen", three options unweighed (ruling).
- KS-1648 gateway 60 s vs 3,600 s window: touches `middleware/auth.ts` and `rateLimitEnforce.ts` (token/rate-limit surface), ticket measures it unreachable, fix shape not chosen.
- KS-1647 registerInPlatformRegistry swallowed: "No fix shape chosen", `documents.ts` held by another lane when filed.
- KS-1720 mypy `Source file found twice`: any fix flips a leg from abort to 317 real errors; whether to make that red is a project ruling.
- KS-1721 symlinked-venv test fails on Linux: ticket measures the cause but two of three "Not established" items are open and the fix (change the test vs the guard) is unchosen; needs Docker Linux python. Hold.
- KS-1715 e2e readiness hardening: three edges, no shape chosen, API-only run semantics ("which projects need a browser") is a design call.
- KS-1606 statusline.sh arithmetic on ISO resets_at: file is at `Setup and System/statusline.sh`, OUTSIDE the project folder (hard rule 1); the ticket itself says so.
- KS-1415 gate62 minors: the `cmp-equal` wording was not found by a grep of the two docs at develop, and the prometheus cell it cites now uses `secuura-nginx-gateway:6882` (7 hits) not the ticket's string - likely stale; not confirmed within budget.
- KS-1340 ks597 DSN `?host=`/`?port=` bypass: the guard cell was not located in `services/originate/src/__tests__` by grep; builder cannot be pointed at a file. Needs a locate step first.
- KS-1010 e2e wallet check hits a route that does not exist: ticket carries an explicit "OPEN QUESTION - do not change any route until answered" (ruling).
- KS-1326 childSuiteCounts: residue of a capped no-go PR #1245, "disposition sits with the repository owner" (ruling) and later comments add a regression item.
- KS-1703/1704/1699/1696/1693/1688/1686/1690/1691/1604/1574 and the other "Security:" / auth-route titles: security surface by title (not individually read).
- KS-1712, KS-1702: need Postgres + PR #1654 overlap (carried from the 1550 sweep).
- KS-1733, KS-1732: governance read-failure semantics (200 [] vs 5xx) is a behaviour decision; not read in full.
- Still unread, not rejected on a clause: ~335 older/bundled candidates (ids < 1500 mostly). A further sweep could take: KS-1424, KS-1345-1350 range, KS-1218, KS-1088, KS-948, KS-903, KS-846 as the next read set.

## Could not establish
- Open-vs-merged for every PR (no gh); whether an In Progress ticket holds the same files; whether KS-1649/1635/1551/1513/1527 seats' file lists include Lane 3's runner or Lane 5's `packages/shared`.
- Whether KS-1727 reproduces on Node 24 (never measured by anyone, per its own comments).
- KS-1443 part 2's fix shape (my read was truncated).
