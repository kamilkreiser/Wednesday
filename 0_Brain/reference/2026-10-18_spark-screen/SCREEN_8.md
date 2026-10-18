# Spark screen, part 8 (2026-10-19 ~07:1x-07:5x AEDT): two briefs, two rounds, two PASS (KS-1526, KS-1595 item 1); two of the four slots not filled, WHY below

By a Spark screen-and-brief sub-agent for Wednesday. Secuura only. Briefs pinned to develop `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (the cache already held it; `cat-file -t` = commit; `ls-remote` agreed at the start and again after the rounds: develop did not move). Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write; no Docker; no `hold_ready`. Linear read-only: SCREEN_4 did not name a key, so `LINEAR_API_KEY` from `Blockchain/4_Credentials/.env` was sourced inside a script file, never printed or copied. Ticket text WAS read for both briefed tickets (whole, through the API).

## Enumeration

Linear GraphQL, team KS, state type backlog + unstarted, `first:50`, paginated until hasNextPage=false: **8 pages, 357 tickets = Backlog 331 + Todo 26** (control: both states counted; SCREEN_4 read 361 about 5 hours earlier).

## Filter funnel (script `filt.py`, counts measured)

| step | removed | left |
|---|---|---|
| open KS Backlog + Todo | | 357 |
| the commission's named exclusions (1612 1385 1384 1603 1628 1622 1621 1620 1627 1626 1625 1623 1624) | 6 present in the pool | 351 |
| assigned to Peter or Stuart | 19 | 332 |
| prior-art by ticket number (a `night/briefs` / `night` name, `spark/done.md`, `night/done.md`, `spark/queue.md` mention) | 19 | 313 |
| Linear attachment that is a GitHub pull-request URL (open-PR proxy; GitHub itself NOT queried) | 12 | 301 |
| title keyword for auth/token/credential/security/session/policy/permission/login/oauth/mfa/jwt/password/secret/rls/key, or decision/design/investigate/audit/whether/spike/rfc/plan | 135 | 166 survive; all 301 titles read, the 135 keyword-held titles skim-read, a dozen re-admitted by hand (KS-1595 and KS-1524, KS-1493, KS-1481, KS-1475, KS-1531, KS-1537, KS-1208, KS-1191, KS-870 read; the auth/key/OAuth/MFA ones left held) |

Descriptions read (whole or first 600-4500 characters): about 90, including 1526 1595 1515 1516 1530 1539 1419 1505 1112 807 954 1466 1340 1494 1468 1500 1548 1463 1424 1178 1559 1529 1329 1491 1338 1259 1177 1327 1377 1507 1531 1322 1475 1537 1524 1493 1481 1602 1607 1184 1208 1191 870 1051 1579 1567 1501 1593 1578 1600 and about 35 of the 40 tooling/facts-only survivors (1590 1576 1575 1573 1571 1565 1495 1454 1398 1391 1379 1343 1332 1308 1307 1247 1224 1200 1048 1044 1022 956 955 846 837 783 765 761 757 748 735 658 648 625 624 607 598 595 579 491). Source read at the tip for both briefed tickets (`logger.ts` whole; `routes/gdpr.ts` :1-60 and :440-640; the ks730b and ks1346b gdpr tests; the ks753 timestamping test).

## Result

| # | ticket / item | brief dir (`local-model/night/briefs/`) | mode / rung | edit points | control | round verdict | golden | model s / tokens | run dir (`local-model/runs/`) | FAIL class |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | KS-1526 api-gateway production File transports write `undefined`: `format: combine(json())` on both (`utils/logger.ts` :32-33) | `ks_1526_p1` | code_patch, rung 2 | 3 (1 product hunk with 2 changed lines, 1 NEW vitest file) | CONTROL-PASS 7/7 BYTE-IDENTICAL (`..._ks_1526_p1-control`) | PASS | BYTE-IDENTICAL | 34.1 / 11061+1482 | `spark_secuura_2026-10-19_ks_1526_p1` | none |
| 2 | KS-1595 item 1: originate `routes/gdpr.ts` `connectorContext` hands connector id, tenantId, organizationId to the erasure service (POST and GET `/erasures`) | `ks_1595_p1` | test_only (jest), rung 1 | 1 (NEW jest file: 3 RED, 4 CONTROL; tamper `gdpr.ts:473`) | CONTROL-PASS 7/7 BYTE-IDENTICAL (`..._ks_1595_p1-control`) | PASS | BYTE-IDENTICAL | 53.3 / 21440+1978 | `spark_secuura_2026-10-19_ks_1595_p1` | none |

brief_lint rc 0 and dry-run rc 0 for both before any control or round. No rebrief used (counter: original only, for each). Both new test files were also run BY HAND in a scratch clone before the brief was written (KS-1526: 2 failed / 2 passed at the tip, 4 passed with the edit; KS-1595: 7 passed at the tip, 3 failed / 4 passed under the tamper), so the golden was proved before the checker saw it.

## Checker lines (both rounds)
- KS-1526: `RESULT: PASS (7/7)`; A3b 2 sites; A3c 2 lines, A3i byte-exact; A4 "fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)"; A5 "4 passed / 4 run"; A6 whole api-gateway suite no new red; A7 tsc rc 0 (baseline rc 0); `PASS A2a ... hunks=1 ok=1 bad=0 skipped_newfile=1`; `SPARK RESULT: PASS`.
- KS-1595: `RESULT: PASS (7/7)`; A3 (test-only) the one new test only, gdpr.ts untouched; A4 tamper planted at `gdpr.ts:473` and reverted, "3 failed / 7 run; controls green; assertion reds"; A5 "7 passed / 7 run"; A6 whole originate suite no new red; A7 tsc rc 0 (baseline rc 0); `PASS A2a ... hunks=0 ok=0 bad=0 skipped_newfile=1`; `SPARK RESULT: PASS`.

## Red cells and controls (exact titles, in each brief's `## Red cells`)
- KS-1526 RED: `RED KS-1526 L1: logs/error.log holds one JSON line carrying level, message and service`; `RED KS-1526 L2: logs/combined.log holds both calls as JSON lines, in order`. CONTROL L3 (production logger still has Console + 2 File transports), L4 (outside production only Console, no `logs` dir made). The cells build the production logger in a `mkdtemp` scratch cwd (`process.chdir`, restored in `afterEach`), after `vi.resetModules()`.
- KS-1595 RED: `R1` POST /erasures passes `['ref-1','c-1','t-1','o-1']`; `R2` GET passes `['ref-2','t-1','o-1']`; `R3` no organization reaches the service as `undefined`. CONTROL `C1` POST tenant-less 403, `C2` GET tenant-less 403, `C3` no principal 403, `C4` empty externalRef 400. Tamper: `gdpr.ts:473` `  if (!user || !tenantId) return null;` becomes `  if (!user || !tenantId || user.userId) return null;` (always-null mutant). Harness copied from the ks730b file (jest.mock of gdprService, auth, logger; real router; real fetch) plus a `req.user` injector.

## Things Wednesday should read before holding
- **KS-1526 carries an open decision in the ticket.** Its last Detail bullet says to decide FIRST whether the gateway should create these files at all (the shared logger made file transports opt-in because Container Apps mount the cwd read-only, so `mkdir('logs')` can throw EACCES at import; "if nothing reads the files, the better fix may be to make them opt-in"). The brief takes the ticket's own Recommendation (format both) and leaves the transports unconditional; the formatting is correct under either outcome, but this is a judgement for Wednesday to confirm before holding. **Refs KS-1526, does NOT close it.** The test uses `process.chdir` inside a vitest worker (works under vitest 4.1.10's default forks pool; the whole api-gateway suite was green, A6).
- **KS-1595** is item 1 only; item 2 (27 `(req as any)` claim reads, 7 re-casts) is facts-only and not briefed, ticket stays open. `requireRole` is a pass-through double here (as in ks730b), so the role gate on `/erasures` is NOT exercised and the service is a double: this pins the helper and the two handlers' use of it, not the SQL. Tenant-isolation surface on an erasure path: route to a tier-1 gate. Only the always-null mutant is planted; swap and organizationId-undefined mutants are reasoned (R1/R2/R3 use distinct values), not run.
- Neither touches an excluded file; `routes/gdpr.ts` and `utils/logger.ts` are not on the exclusion list. Open-PR overlap on both files: NOT checked (no GitHub query).

## Not briefed, and WHY (the measured rejections for the two empty slots)

- **KS-1515 (timestamping `eidasQualified` for a mock reply) - REJECTED ON THE ENVIRONMENT, and it was the cleanest ticket in the pool** (a one-line change the ticket spells out, plus a prescribed cell). A test was written and run in a scratch clone: all 5 cells fail at load, `Cannot find package 'asn1js' imported from services/timestamping/src/tsa/rfc3161-client.ts`; `tsc --noEmit` for timestamping has a BASELINE rc 2 (TS2307 `asn1js` and `pkijs`, plus knock-on TS18046/TS2339 in `rfc3161-client.ts`) because the Secuura checkout's `services/timestamping/node_modules` (ioredis and a few others) does not hold the KS-1404 dependencies (`ls .../timestamping/node_modules/asn1js` and `.../Dev/node_modules/asn1js` both absent). So the checker's A4 (assertion red), A6 and A7 (tsc rc 0) cannot pass for ANY timestamping brief, existing `ks753` and `ks1404-*` suites included. Unblocking: a Secuura seat runs `npm install` in `Blockchain/Dev/services/timestamping` (I am read-only there). Draft test and golden idea are in the scratch folder; no brief dir was written.
- Decisions first / no fix shape: KS-1530 (mcp-server `|| []`: "decide what the endpoint should do"), KS-1112 (align or document), KS-807 (scan or declare out), KS-1516 (policy first), KS-1419 and KS-1424 (change every `updateDocument` caller), KS-1481 (measure first), KS-1537 (spec prose plus regenerated yaml, `npm run generate-openapi`), KS-1322 (keep or strip), KS-1184 and KS-1177 (design calls), KS-1467 (needs a ruling), KS-1493 N2.
- Excluded by file: KS-1539 and KS-1534 (verification.ts, info.ts), KS-1548 and KS-1524 (platform.ts), KS-1184 (verification.ts), KS-1475 and KS-1590 (documents.ts / verification surface), KS-1466 (enforcement; "authorization-shaped", measure first).
- Auth / keys / credentials surface (held by the title keywords and left held): KS-1377, 1525, 1568, 1569, 1572, 1574, 1581, 1498, 1486, 1500, 1468 (auth wallet ordering guard), 1602 (security keys route test timeout), 1208, 1191 (audit), 870.
- Needs a real Postgres or a stack: KS-1600, 1578, 1495, 1475 item 3, 1499, 1567, 1589.
- Test-only on a guard that lives IN the test file: KS-1491, 1501, 1529, 1338, 1340/1494 (integration guards). The test_only tier plants its tamper at a fixed line in the product file and applies the patch to a different test file (checker line 543: `TEST_FILE != REF_TEST`; the tamper line would also shift under an in-place patch), so a tamper target that is the test file itself is not expressible.
- No tier fits: KS-1579 items 3/4 (a cell title reword, a header sentence), KS-1505 (a comment plus a dev-only boot block), KS-1289 (`.dockerignore`), KS-1331, KS-1088 and the other bash-suite fixes (bash test_only unwired), KS-1551/1523/1527 (scripts outside `services/*`).
- Facts only, no fix, or cross-system: KS-1593 (a tsc-level guard; originate is not in the ratchet's default list), KS-1565, 1576, 1599, 1571, 1573, 1247, 1022.
- KS-1471 ("nearly qualified" in SCREEN_4) was not re-read.

## NOT measured
- No open-PR census against GitHub (Linear attachments only); no check of live seats' unpushed work; no open-PR overlap on `logger.ts` or `gdpr.ts`.
- I did not read the two model patches line by line (both BYTE-IDENTICAL to my golden by `cmp`, which is stronger than a read). No jest/vitest/tsc by hand beyond the new test files; every other red/green figure is the checker's.
- 135 keyword-held titles were skim-read, not all descriptions; about 90 of 301 descriptions were read.
- KS-1526: whether the deployed gateway writes these files, whether anything collects them, and the opt-in question are not established.

## Files written
Briefs: `local-model/night/briefs/ks_1526_p1/` and `ks_1595_p1/` (each `KS-<n>.md`, `golden.diff`, `spark.pins`). Run dirs (`local-model/runs/spark_secuura_2026-10-19_ks_1526_p1`, `..._ks_1595_p1`, and the two `-control` dirs) and `spark/state/dry/` are round.sh's own; `spark/cache/work/` accumulated 2 control + 2 round clones (about 335 MB each, not pruned). `spark/queue.md` NOT touched. Scratch (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/spark_screen8/` (`fetch.sh`, `filt.py`, `filt.out`, `all.json` the 357 tickets, `clone/` a shared clone at the tip, `g/` the two test files and `mkbriefs.py`, `gold.sh`, `prove.sh`, `rounds.sh`, `t1515.sh`, `t1526.sh`, `t1595.sh`, `tsc_ts.sh`, `logs/`).

WHY not four: of 357, 301 survived the mechanical filters, 166 the title keywords, about 12 a description read plus a source read, 3 got a hand-run test (KS-1515, KS-1526, KS-1595), 2 became briefs; KS-1515 was killed by the missing `asn1js`/`pkijs` install in the Secuura checkout (above), the rest by the clauses listed.
