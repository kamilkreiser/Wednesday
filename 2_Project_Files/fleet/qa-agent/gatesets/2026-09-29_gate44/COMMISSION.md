# gate44 COMMISSION — two Secuura PRs from Seat B 45th (T1: #1346 KS-1054; T2: #1347 KS-1374), round 44

Filled by fill_gate44.py at 2026-09-29T09:29:11Z from pins_gate44.json (measured 2026-09-29T09:22:56Z). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 40 keywords.

## The PRs (merge order = this table's order: T1 first)
| PR | tickets | tier | head | parent | behind develop | files | declared subject -> lands |
|---|---|---|---|---|---|---|---|
| #1346 | KS-1054 | T1 | `2075c3ec70789d9a87a6359fccf1a58d97db3255` | `0aa9b52c691b` | 5 | 4 | 79 -> 87 |
| #1347 | KS-1374 | T2 | `2c4b98253b1fa820c4fe08585dad5da57947ffb4` | `bd740147c3d8` | 0 | 5 | 84 -> 92 |

- develop `bd740147c3d88fbf45af109fd68fd35f602c2914` (tree `dd70cc631be4f2f9d8ac6c8744acf109931e4ee1`). #1346's parent is `0aa9b52c691bb852e3fd1b796514fe9122ebc054`, **5 commits behind** (gate43's five squashes; none touches its four paths — the commission said two, the drafter measured 5). #1347 sits on develop.
- RECORDED MODES (pin (H), `git ls-tree`, at head / alone / chain step / END): check-startup-migrations.sh 100755; deploy-all.sh 100755; deploy.sh 100755; ks1054_deploy_scripts_read_startup_migrations.test.sh 100644 — all 4 OK.
- Author AND merger: Seat B 45th. Pane `QA/Secuura-batch1346`. Report dir `2026-09-29-batch1346-g44`.

## The rulings (the gate checks each diff against its ruling)
- #1346 KS-1054 (N-1332-5) — Kam option (a), card `secuura-ks1054-f9282-migration-failure-visibility`: "Keep serving, flag it on /health — The migration run returns its failed count. /health reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it and the deploy reads as failed. The running service is not stopped." A DEPLOY-PATH change: TIER 1.
- #1347 KS-1374 A+B+C — Kam 16:17:55 / 16:18:57 (Tuesday ROUTED): Peter's reply was for us to implement the change = option 2 plus one guard: LOCAL stacks raised to 10000, docker-compose's `:-2000` fallback unchanged, demo and production unchanged, one limiter test at the demo's limit; the Akto harness reads the platform limit (junk -> 2000 + warn; a lower limit honoured). TIER 2.

## What the gate must check
1. **Red at base, green at head, a tamper that reds for the RIGHT reason** — per PR; unique anchor, sha256-asserted restore. For #1346 the tampers include a RECORDED-100644 helper (core.filemode is false: the recorded mode is the evidence, not the disk bit) and a predicate keyed on `error`; the seat's 0/11 test-half-alone -> 11/0 is re-measured. For #1347 the api-gateway file is a PIN (7/7 green at base; W1 is titled RED) and the akto file needs a develop-compatible probe. (RED-AT-BASE, GREEN-AT-HEAD, TAMPER-RIGHT-REASON, TAMPER-UNIQUE-ANCHOR, RESTORE-SHA256, TEST-HALF-0-11-1346, TAMPER-MODE-100644-1346, TAMPER-KEY-ON-ERROR-1346, W1-GREEN-AT-BASE-1347)
2. **Whole suites before / after, with tsc where present** — the shell suite (`run-shell-suites.sh`), api-gateway, the akto unit suite (its OWN `npm ci`): develop, each head, END; no new red. (WHOLE-SUITE-BEFORE-AFTER, NO-NEW-RED, TSC-BEFORE-AFTER, SUITES-AT-END, AKTO-OWN-NPM-CI-1347)
3. **Every test anywhere referencing a changed path** — `git grep` over Blockchain/** and systemTest/** test files, LISTED and RUN. The drafter's census: 18 files. (CENSUS-TESTS-RUN, CENSUS-LISTED)
4. **Key-scan subjects** (own key only, no `(#n)`, landed <= 92 — #1347 lands at exactly 92) and **bodies** `Refs <own key>`, no closing keyword. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, REFS-OWN-KEY, NO-CLOSING-KEYWORD)
5. **#1346 on the deploy path, with stubs only** — both deploy scripts driven; deploy.sh's exit code; `ran:false`; the pass line printed for a skipped check; the ABSENT-passes-and-warns design claim verified (the rollback it protects). (ABSENT-FIELD-PASSES-WARNS-1346, DEPLOY-PATH-DRIVEN-1346, DEPLOY-SH-EXIT-CODE-1346, RAN-FALSE-1346, PASS-LINE-ON-SKIP-1346, MODE-100755-RECORDED-1346)
6. **Merge order and END** — 1346 then 1347, each squash on the previous tip; END_TREE `0c16f76bd6ccffb38130966e428f47ba2e8da82d`; overlap measured; #1346 merges AS-IS. (END-TREE, MERGE-ORDER-T1-FIRST, OVERLAP-MEASURED, NO-REBASE-NEEDED, BEHIND-5-NOT-2)
7. **#1347 through-code** — the dotenv order the author left NOT COVERED, measured if possible; RATE_LIMIT_MAX_REQUESTS=1 -> unthrottled; the production-compose and CI templates; every factual line of the author's KS-1374 CORRECTION checked against the tree; Peter's 09:14 comment. (DOTENV-ORDER-1347, LOWER-LIMIT-1-UNPACED-1347, PROD-COMPOSE-TEMPLATE-1347, CI-TEMPLATE-1347, CORRECTION-LINES-1347, PETER-0914-1347)
8. **The report's `## MERGE ADDENDUM` is the LAST thing written; nothing goes into report.md after the verdict mail**, whose body carries the report's sha256. (REPORT-HASH-LAST) Plus DISK-ENOSPC and TIERING.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 45th): merge 1346 1347 on gate44` — Seat B 45th merges. Verdict mail subject: `[QA -> Wednesday] GATE44 batch #1346 #1347 (Seat B45, round 44; T1: KS-1054 deploy scripts read startupMigrations; T2: KS-1374 local limit + Akto reads it)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate44.py -> pin_1.out: OVERLAP: 0 of 1 pair overlap; 9 paths in total, 9 distinct (measured at develop bd740147c3d8). END_TREE `0c16f76bd6ccffb38130966e428f47ba2e8da82d`; reverse order `0c16f76bd6ccffb38130966e428f47ba2e8da82d`.
- testrefs_gate44.py -> testrefs_1.out: 18 test files — scripts/__tests__/bootstrap_env_canonical_template.test.sh; scripts/__tests__/bootstrap_env_slot_ports.test.sh; scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh; services/api-gateway/src/__tests__/ks1054-startup-migration-failure-on-health.test.ts; services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts; services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts; systemTest/__tests__/slot_target.test.sh; systemTest/akto/tests/unit/bootstrap/slotKeysDocumented.test.ts; systemTest/akto/tests/unit/config/aktoContainer.test.ts; systemTest/akto/tests/unit/config/envPrecedence.test.ts; systemTest/akto/tests/unit/config/slot.test.ts; systemTest/akto/tests/unit/scan/scanOptions.test.ts; systemTest/akto/tests/unit/setup/aktoRateLimit.test.ts; systemTest/akto/tests/unit/setup/ks1374-platform-limit-from-env.test.ts; systemTest/akto/tests/unit/setup/tierPacing.test.ts; systemTest/playwright/tests-unit/env-example.test.ts; systemTest/playwright/tests-unit/environment.test.ts; systemTest/schemathesis/tests/conftest.py
- keyscan_gate44.py -> keyscan_1.out: KEYSCAN PASS: 12 checks over 2 PRs, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
- linear_read_gate44.py -> linear_read_1.out: LINEAR READ OK: 1 CORRECTION comment(s) on KS-1374 -> linear_gate44.md
