# Spark screen, part 4 (2026-10-19 ~02:3x-03:0x AEDT): 4 briefs, 4 rounds, 4 PASS

By a Spark screen-and-brief sub-agent for Wednesday. Secuura only. Briefs pinned to develop `6184eaa0af75c1e27eb69bbff67a7790ef494b5f` (Wednesday's 02:3x read; the cache lacked it, so I ran the round script's own fetch once). Develop moved twice while I worked (b5742c3e1 KS-1624 F1, 385fc288f KS-1623 N3); round.sh's stale-brief check passed each time (no brief file touched) and the real rounds ran at `385fc288fae8`. Nothing held, raised, pushed, merged, committed, deleted or written to Linear. Linear read-only (key sourced transiently inside a script file, never printed).

## Enumeration

Linear GraphQL, team KS, state type backlog + unstarted, `first:50`, paginated until hasNextPage=false: **8 pages, 361 tickets = Backlog 335 + Todo 26** (control: both states counted; the 10-18 count was 367, so six tickets left the pool since, plausible given the day's merges; not otherwise verified).

## Filter funnel (script `filt.py`, counts measured)

| step | removed | left |
|---|---|---|
| open KS Backlog + Todo | | 361 |
| the commission's named exclusions (1482 1497 1114 1490 1619-1625 1612 1385 1384 1545) | 5 present in the pool | 356 |
| assigned to Peter (12) or Stuart (7) | 19 | 337 |
| prior-art by ticket number (a `night/briefs` / `night` name, `spark/done.md`, `night/done.md`, `spark/queue.md` mention) | 19 | 318 |
| Linear attachment that is a GitHub pull-request URL (open-PR proxy; GitHub itself NOT queried, unmeasured) | 12 | 306 |
| title keyword for auth/token/credential/security/session/policy/permission/login/decision/design/audit/key... | 139 | 167 survive; all 306 titles read, 139 keyword-held titles skim-read, a few re-admitted by hand (KS-1504, 1485, 1471, 1540 are security-adjacent words) |

Descriptions read (whole or first 1-3 KB): about 70, including 1593 1578 1566 1500 1588 1589 1491 1468 1527 1513 1563 1560 1483 1419 1409 1331 1251 1249 1243 1601 1600 1599 1597 1596 1587 1585 1583 1567 1558 1501 1507 1551 1523 1505 1573 1571 1540 1459 1484 1377 1340 1329 1259 1197 1115 1113 1112 954 1030 1088 1082 1010 1039 1473 1494 1463 1465 1424 1327 1304 1420 1444 1546 1412 1415 1387 1104 1611 758 1106 1467 1471 1504 1357 805 1485. Source read at the tip for the four briefed plus 1471.

## Briefed (all four: dry-run rc 0, brief_lint rc 0, CONTROL PASS 7/7 golden BYTE-IDENTICAL, ONE real round, PASS, golden TREE-IDENTICAL; no FAIL, no rebrief used)

| ticket | brief dir (`local-model/night/briefs/`) | mode / rung | edit points | control run | round verdict | model s / tokens | run dir (`local-model/runs/`) | auth/security |
|---|---|---|---|---|---|---|---|---|
| KS-1485 item 2: `authoritativeTxHash` also rejects `mock_batch_tx_` (anchorStateSync.ts:81) | `ks_1485_p1` | code_patch, rung 1 | 2 (1 product line, 1 NEW jest file: 3 RED, 4 CONTROL) | `..._ks_1485_p1-control` (A4 3 failed/7, A5 7/7) | PASS 7/7 + A2a, TREE-IDENTICAL | 33.7 / 16409+1175 | `spark_secuura_2026-10-19_ks_1485_p1` | no |
| KS-1504 product change: no-allowance warning's authMethod through `logField` (applied at the call site rateLimitEnforce.ts:181, ASCII line) | `ks_1504_p1` | code_patch, rung 1 | 2 (1 product line at -U1, 1 NEW vitest file: 3 RED, 3 CONTROL, getter harness) | `..._ks_1504_p1-control` (A4 3 failed/6) | PASS 7/7 + A2a, TREE-IDENTICAL | 49.0 / 20134+1791 | `spark_secuura_2026-10-19_ks_1504_p1` | **yes, mild**: api-gateway rate limiter, a log-field escape only; route to a tier-1 gate |
| KS-1540: `/api/connector/info` 503 when Redis unavailable (health.ts, 2 insertion hunks) | `ks_1540_p1` | code_patch, rung 2 | 3 (2 product hunks, 1 NEW vitest file: 2 RED, 3 CONTROL) | `..._ks_1540_p1-control-r2` (A4 2 failed/5) | PASS 7/7 + A2a, TREE-IDENTICAL | 48.8 / 17721+1882 | `spark_secuura_2026-10-19_ks_1540_p1` | **yes**: connector allow-list gate (fail closed); fully spelled out; route to a tier-1 gate |
| KS-1387: governance router `const router: Router = Router();` | `ks_1387_p1` | code_patch, rung 1 | 2 (1 product hunk, 1 NEW jest source-text file: 1 RED, 2 CONTROL) | `..._ks_1387_p1-control-r2` (A4 1 failed/3) | PASS 7/7 + A2a, TREE-IDENTICAL | 23.0 / 15058+633 | `spark_secuura_2026-10-19_ks_1387_p1` | no |

Pins files are in each brief dir. Wednesday must read each patch at source.

## Things Wednesday should read before holding

- **KS-1540 deviates from the ticket on purpose**: `isRedisAvailable?` is OPTIONAL and only an explicit `false` refuses, so six existing test files whose doubles lack the method (ks1054, ks1231, ks1232, ks1246, ks1532, ks480) are untouched; the ticket's AGREEMENT cell against the real create route is NOT written (literal text compare instead); ks1532's "resolved null still answers []" control stays green and its title is now partly stale. Production passes the whole redis module, which has the method.
- **KS-1504** applies `logField` at the call site (:181) rather than inside the template (:123, which holds a non-ASCII em dash: the harness is known to mishandle non-ASCII `-` lines). Same output. The RED cells use a getter that answers `api_key` to the gate's first read and a hostile value afterwards; they rely on exactly two reads of `user.authMethod`.
- **KS-1387**: the declaration sits between two blank lines and the builder refuses blank context; the hunk therefore removes and re-adds both blank lines as `-`/`+` (net no change). Worked (control and round). The test is a source-text pin of the annotation; TS2742 itself was not reproduced and whether the clean image build still fails at the tip is unmeasured.
- **KS-1485** edits the code line only; the doc comment above still lists two prefixes (it holds non-ASCII). Item 1 of the ticket (carry pin) is not covered; KS-1485 stays open.
- None touches the excluded gate files (verification.ts, whatsapp-bot verify/index, ks812*).

## Nearly qualified, and why not

- KS-1471 (log `req.baseUrl + req.path`): the log moved into `refuseConnectorBearer` (auth.ts:26) and the inner call is unreachable behind the KS-1470 front door; the pin cell needs an authenticateToken-under-router harness. Not briefed.
- KS-1551 (a), KS-1523 (a): product is `scripts/typecheck-tests/check.cjs`, outside `services/*`; the code_patch builder refuses such a product (SCREEN.md finding); the test is a 919-line spawn-tsc suite. KS-1551 (a)'s fix also flips every fixture that omits a baseline.
- KS-1459 item 2 (auth users.ts LEVEL_ORDER): changes comparison semantics of an auth route (unknown level index); not a pure comment-and-import. KS-1484 item 1: auth userRepo comment only, thin. Held back.
- KS-1566 (cap value pin): tamper target is originate `routes/verification.ts` (gate file, excluded). KS-1600 / KS-1588 / KS-1578 / KS-1587: test_only but the cells need a real Postgres or are auth/security test gaps with several mutants.
- KS-1573 ("whether to delete" = decision), KS-1593/1571/1599/1597 (facts only), KS-1596 (cross-system vocabulary), KS-1467 (needs a ruling on 422 `details`), KS-1473 (owner decision), KS-1409/1243/1249 (decisions), KS-1197 (hang plus two sites, auth middleware), KS-1540's sibling KS-1534 (not read), KS-1585 m2 (script with no suite), KS-1560 / KS-1527 / KS-1563 / KS-1465 (the fix is in a bash suite itself; no product, bash test_only unwired).

## NOT measured

- No open-PR census against GitHub (Linear attachments only); no check of live seats' unpushed work; no open-PR overlap for the four files beyond the attachments filter.
- No jest/vitest run by hand; red/green figures are the checker's. I did not read the four model patches line by line (TREE-IDENTICAL to my golden).
- 139 keyword-held titles were skim-read, not all descriptions.
- The claim that KS-1485 item 2 cannot reject a real hash rests on the ticket (hex has no `_`).

## Files written

Briefs: `night/briefs/ks_1485_p1`, `ks_1504_p1`, `ks_1540_p1`, `ks_1387_p1` (each `KS-<n>.md`, `golden.diff`, `spark.pins`). `spark/queue.md` (one provenance comment). Run dirs and `spark/state/dry/` are round.sh's own; `spark/cache/work/` clones accumulated (about 335 MB each, not pruned). Scratch (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/db9b2375-e430-4d46-b18c-db37397c2500/scratchpad/spark_screen4/` (clone, `g/` golden and brief generators, `prove.sh`, `rounds.sh`, logs, `all.json` the 361 tickets).

WHY not fewer than four: n/a (four reached). WHY the pool was thin: of 361, 306 survived the mechanical filters, about 25 survived a description read, 5 a source read, 4 became briefs; the rest are decisions, facts-only notes, security/RLS/Postgres-bound cells, bash-suite-only fixes, or tooling outside `services/*`.
