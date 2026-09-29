# gate44 COMMISSION — two Secuura PRs from Seat B 45th (T1: #1346 KS-1054; T2: #1347 KS-1374), round 44

Filled by fill_gate44.py at {{FILLED_AT}} from pins_gate44.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords.

## The PRs (merge order = this table's order: T1 first)
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`). #1346's parent is `{{OLD_BASE}}`, **{{BEHIND_1346}} commits behind** (gate43's five squashes; none touches its four paths — the commission said two, the drafter measured {{BEHIND_1346}}). #1347 sits on develop.
- {{MODE_LINE}}
- Author AND merger: {{MERGE_SEAT}}. Pane `QA/Secuura-batch1346`. Report dir `{{REPORT}}`.

## The rulings (the gate checks each diff against its ruling)
- #1346 KS-1054 (N-1332-5) — Kam option (a), card `secuura-ks1054-f9282-migration-failure-visibility`: "Keep serving, flag it on /health — The migration run returns its failed count. /health reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it and the deploy reads as failed. The running service is not stopped." A DEPLOY-PATH change: TIER 1.
- #1347 KS-1374 A+B+C — Kam 16:17:55 / 16:18:57 (Tuesday ROUTED): Peter's reply was for us to implement the change = option 2 plus one guard: LOCAL stacks raised to 10000, docker-compose's `:-2000` fallback unchanged, demo and production unchanged, one limiter test at the demo's limit; the Akto harness reads the platform limit (junk -> 2000 + warn; a lower limit honoured). TIER 2.

## What the gate must check
1. **Red at base, green at head, a tamper that reds for the RIGHT reason** — per PR; unique anchor, sha256-asserted restore. For #1346 the tampers include a RECORDED-100644 helper (core.filemode is false: the recorded mode is the evidence, not the disk bit) and a predicate keyed on `error`; the seat's 0/11 test-half-alone -> 11/0 is re-measured. For #1347 the api-gateway file is a PIN (7/7 green at base; W1 is titled RED) and the akto file needs a develop-compatible probe. (RED-AT-BASE, GREEN-AT-HEAD, TAMPER-RIGHT-REASON, TAMPER-UNIQUE-ANCHOR, RESTORE-SHA256, TEST-HALF-0-11-1346, TAMPER-MODE-100644-1346, TAMPER-KEY-ON-ERROR-1346, W1-GREEN-AT-BASE-1347)
2. **Whole suites before / after, with tsc where present** — the shell suite (`run-shell-suites.sh`), api-gateway, the akto unit suite (its OWN `npm ci`): develop, each head, END; no new red. (WHOLE-SUITE-BEFORE-AFTER, NO-NEW-RED, TSC-BEFORE-AFTER, SUITES-AT-END, AKTO-OWN-NPM-CI-1347)
3. **Every test anywhere referencing a changed path** — `git grep` over Blockchain/** and systemTest/** test files, LISTED and RUN. The drafter's census: {{CENSUS_N}} files. (CENSUS-TESTS-RUN, CENSUS-LISTED)
4. **Key-scan subjects** (own key only, no `(#n)`, landed <= 92 — #1347 lands at exactly 92) and **bodies** `Refs <own key>`, no closing keyword. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, REFS-OWN-KEY, NO-CLOSING-KEYWORD)
5. **#1346 on the deploy path, with stubs only** — both deploy scripts driven; deploy.sh's exit code; `ran:false`; the pass line printed for a skipped check; the ABSENT-passes-and-warns design claim verified (the rollback it protects). (ABSENT-FIELD-PASSES-WARNS-1346, DEPLOY-PATH-DRIVEN-1346, DEPLOY-SH-EXIT-CODE-1346, RAN-FALSE-1346, PASS-LINE-ON-SKIP-1346, MODE-100755-RECORDED-1346)
6. **Merge order and END** — 1346 then 1347, each squash on the previous tip; END_TREE `{{END_TREE}}`; overlap measured; #1346 merges AS-IS. (END-TREE, MERGE-ORDER-T1-FIRST, OVERLAP-MEASURED, NO-REBASE-NEEDED, BEHIND-5-NOT-2)
7. **#1347 through-code** — the dotenv order the author left NOT COVERED, measured if possible; RATE_LIMIT_MAX_REQUESTS=1 -> unthrottled; the production-compose and CI templates; every factual line of the author's KS-1374 CORRECTION checked against the tree; Peter's 09:14 comment. (DOTENV-ORDER-1347, LOWER-LIMIT-1-UNPACED-1347, PROD-COMPOSE-TEMPLATE-1347, CI-TEMPLATE-1347, CORRECTION-LINES-1347, PETER-0914-1347)
8. **The report's `## MERGE ADDENDUM` is the LAST thing written; nothing goes into report.md after the verdict mail**, whose body carries the report's sha256. (REPORT-HASH-LAST) Plus DISK-ENOSPC and TIERING.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate44.py -> pin_1.out: {{OVERLAP_LINE}} END_TREE `{{END_TREE}}`; reverse order `{{REVERSE_END}}`.
- testrefs_gate44.py -> testrefs_1.out: {{CENSUS_N}} test files — {{CENSUS_LIST}}
- keyscan_gate44.py -> keyscan_1.out: {{KEYSCAN}}
- linear_read_gate44.py -> linear_read_1.out: {{LINEAR_LINE}}
