# gate43 COMMISSION — five Secuura PRs from Seat B 44th (T1: #1341, #1342; T2: #1343, #1344, #1345), round 43

Filled by fill_gate43.py at {{FILLED_AT}} from pins_gate43.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords.

## The PRs (merge order = this table's order: T1 first)
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`). #1341-#1343 have parent `{{OLD_BASE}}` (one behind: the #1340 squash touched only `Blockchain/Dev/scripts/audit/audit-baseline.json`); #1344-#1345 sit on develop.
- Author: Seat B 44th (wrapping). MERGER: {{MERGE_SEAT}}. Pane `QA/Secuura-batch1341`. Report dir `{{REPORT}}`.

## Kam's rulings, as the commit messages quote them (the gate checks each diff against its ruling)
- #1341 KS-1375 — option (b), card `secuura-ks1352-unknown-id-policy-after-gate38`: verification FAILS CLOSED when no issuer record exists, reason `no issuer record`. Refs KS-1368 too (Wednesday's ANSWER 2026-09-29T00:41:59Z: KS-1368 IS the unknown-id policy question).
- #1342 KS-1369 — option (a), card `secuura-ks1369-gateway-proxy-crash-guard-shape`: one guard at the top of the hook; if the outgoing request's headers are already sent, skip the header writes.
- #1343 KS-1371 — the ticket's first direction: validate against the declared bound (`nonnegative()`); revoke's -1 tolerance (KS 662) unchanged.
- #1344 KS-1359 — option (a), card `secuura-ks1359-platform-audit-log-bounds`: 400 for wrong-type and below-minimum; the KS 5 cap for too-large kept.
- #1345 KS-1360 — option (a), card `secuura-ks1360-wallet-session-delete-reply-shape`: add `success: true` to the reply (additive).

## What the gate must check
1. **Red at base, green at head, a tamper that reds for the RIGHT reason** — per PR; unique anchor, sha256-asserted restore. (RED-AT-BASE, GREEN-AT-HEAD, TAMPER-RIGHT-REASON, TAMPER-UNIQUE-ANCHOR, RESTORE-SHA256)
2. **The changed services' whole suites before / after, and tsc** — packages/shared, vc-issuer, api-gateway, wallet-connector (+ prism, a verifier.ts consumer): develop, each head, END; no new red; tsc error count per tree. (WHOLE-SUITE-BEFORE-AFTER, NO-NEW-RED, TSC-BEFORE-AFTER, SUITES-AT-END)
3. **Every test anywhere in the monorepo that references a changed file's PATH** — `git grep -l '<path>'` over test files, LISTED and RUN. The drafter's census: {{CENSUS_N}} files. (CENSUS-TESTS-RUN, CENSUS-LISTED)
4. **Key-scan every squash subject** (own key only, no `(#n)`, landed <= 92) and **bodies** `Refs <own key>`, no closing keyword. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, REFS-OWN-KEY, NO-CLOSING-KEYWORD)
5. **#1345: grep the run for hang / timeout / open-handle** and report (a mocked `../db` whose initDb never settles). (HANG-GREP-1345, OPEN-HANDLE-1345)
6. **Merge order and END** — T1 first: 1341, 1342, then 1343, 1344, 1345, each squash on the previous tip; END_TREE `{{END_TREE}}`; the path overlap MEASURED (the author claims zero; see the 15-vs-11 note); whether any PR needs a rebase. (END-TREE, MERGE-ORDER-T1-FIRST, OVERLAP-MEASURED, NO-REBASE-NEEDED, PATH-COUNT-15-VS-11)
7. **T1 full weight** — #1341: ID-SWAP-TO-LIVE-1341, NO-RESOLVER-UNCHANGED-1341, STALE-DOC-RESOLVERS-1341; #1342: HEADERSSENT-REAL-SOCKET-1342, UPSTREAM-NOT-HUNG-1342. Plus DISK-ENOSPC and TIERING.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate43.py -> pin_1.out: {{OVERLAP_LINE}} END_TREE `{{END_TREE}}`; reverse order `{{REVERSE_END}}`.
- testrefs_gate43.py -> testrefs_1.out: {{CENSUS_N}} test files — {{CENSUS_LIST}}
- keyscan_gate43.py -> keyscan_1.out: {{KEYSCAN}}
