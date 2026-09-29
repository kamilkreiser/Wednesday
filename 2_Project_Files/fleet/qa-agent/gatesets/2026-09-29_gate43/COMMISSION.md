# gate43 COMMISSION — five Secuura PRs from Seat B 44th (T1: #1341, #1342; T2: #1343, #1344, #1345), round 43

Filled by fill_gate43.py at 2026-09-29T07:43:51Z from pins_gate43.json (measured 2026-09-29T07:33:54Z). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the 29 keywords.

## The PRs (merge order = this table's order: T1 first)
| PR | tickets | tier | head | parent | behind develop | files | declared subject -> lands |
|---|---|---|---|---|---|---|---|
| #1341 | KS-1375 + KS-1368 | T1 | `bf0dfa64a424a3979d8efcb683ce18972a386b1c` | `2cb858335472` | 1 | 3 | 72 -> 80 |
| #1342 | KS-1369 | T1 | `add62ea8114627ef386d5399c4011e33e097e784` | `2cb858335472` | 1 | 2 | 80 -> 88 |
| #1343 | KS-1371 | T2 | `6600514d61efd90387cdeb9316635c3ae83a241b` | `2cb858335472` | 1 | 2 | 61 -> 69 |
| #1344 | KS-1359 | T2 | `ca4aab7f3b33eaafc7ef9dae8891e11c0e46816b` | `0aa9b52c691b` | 0 | 2 | 61 -> 69 |
| #1345 | KS-1360 | T2 | `052f4a3b9c56f78a5fa907a2db8e320105410a54` | `0aa9b52c691b` | 0 | 2 | 62 -> 70 |

- develop `0aa9b52c691bb852e3fd1b796514fe9122ebc054` (tree `09c593f29fd4ecf1691d99e961bfa060812932c8`). #1341-#1343 have parent `2cb858335472fafcce535ca4ad328c897ed87bfb` (one behind: the #1340 squash touched only `Blockchain/Dev/scripts/audit/audit-baseline.json`); #1344-#1345 sit on develop.
- Author: Seat B 44th (wrapping). MERGER: Seat B 45th. Pane `QA/Secuura-batch1341`. Report dir `2026-09-29-batch1341-g43`.

## Kam's rulings, as the commit messages quote them (the gate checks each diff against its ruling)
- #1341 KS-1375 — option (b), card `secuura-ks1352-unknown-id-policy-after-gate38`: verification FAILS CLOSED when no issuer record exists, reason `no issuer record`. Refs KS-1368 too (Wednesday's ANSWER 2026-09-29T00:41:59Z: KS-1368 IS the unknown-id policy question).
- #1342 KS-1369 — option (a), card `secuura-ks1369-gateway-proxy-crash-guard-shape`: one guard at the top of the hook; if the outgoing request's headers are already sent, skip the header writes.
- #1343 KS-1371 — the ticket's first direction: validate against the declared bound (`nonnegative()`); revoke's -1 tolerance (KS 662) unchanged.
- #1344 KS-1359 — option (a), card `secuura-ks1359-platform-audit-log-bounds`: 400 for wrong-type and below-minimum; the KS 5 cap for too-large kept.
- #1345 KS-1360 — option (a), card `secuura-ks1360-wallet-session-delete-reply-shape`: add `success: true` to the reply (additive).

## What the gate must check
1. **Red at base, green at head, a tamper that reds for the RIGHT reason** — per PR; unique anchor, sha256-asserted restore. (RED-AT-BASE, GREEN-AT-HEAD, TAMPER-RIGHT-REASON, TAMPER-UNIQUE-ANCHOR, RESTORE-SHA256)
2. **The changed services' whole suites before / after, and tsc** — packages/shared, vc-issuer, api-gateway, wallet-connector (+ prism, a verifier.ts consumer): develop, each head, END; no new red; tsc error count per tree. (WHOLE-SUITE-BEFORE-AFTER, NO-NEW-RED, TSC-BEFORE-AFTER, SUITES-AT-END)
3. **Every test anywhere in the monorepo that references a changed file's PATH** — `git grep -l '<path>'` over test files, LISTED and RUN. The drafter's census: 23 files. (CENSUS-TESTS-RUN, CENSUS-LISTED)
4. **Key-scan every squash subject** (own key only, no `(#n)`, landed <= 92) and **bodies** `Refs <own key>`, no closing keyword. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, REFS-OWN-KEY, NO-CLOSING-KEYWORD)
5. **#1345: grep the run for hang / timeout / open-handle** and report (a mocked `../db` whose initDb never settles). (HANG-GREP-1345, OPEN-HANDLE-1345)
6. **Merge order and END** — T1 first: 1341, 1342, then 1343, 1344, 1345, each squash on the previous tip; END_TREE `dd70cc631be4f2f9d8ac6c8744acf109931e4ee1`; the path overlap MEASURED (the author claims zero; see the 15-vs-11 note); whether any PR needs a rebase. (END-TREE, MERGE-ORDER-T1-FIRST, OVERLAP-MEASURED, NO-REBASE-NEEDED, PATH-COUNT-15-VS-11)
7. **T1 full weight** — #1341: ID-SWAP-TO-LIVE-1341, NO-RESOLVER-UNCHANGED-1341, STALE-DOC-RESOLVERS-1341; #1342: HEADERSSENT-REAL-SOCKET-1342, UPSTREAM-NOT-HUNG-1342. Plus DISK-ENOSPC and TIERING.

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 45th): merge 1341 1342 1343 1344 1345 on gate43` — Seat B 45th merges. Verdict mail subject: `[QA -> Wednesday] GATE43 batch #1341-#1345 (Seat B44 -> B45, round 43; T1: KS-1375 fail closed + KS-1369 proxy crash guard; T2: KS-1371, KS-1359, KS-1360)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate43.py -> pin_1.out: OVERLAP: 0 of 10 pairs overlap; 11 paths in total, 11 distinct (measured at develop 0aa9b52c691b). END_TREE `dd70cc631be4f2f9d8ac6c8744acf109931e4ee1`; reverse order `dd70cc631be4f2f9d8ac6c8744acf109931e4ee1`.
- testrefs_gate43.py -> testrefs_1.out: 23 test files — packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts; packages/shared/src/__tests__/scopes.test.ts; services/api-gateway/src/__tests__/ks1041-vouch-mint-scope.test.ts; services/api-gateway/src/__tests__/ks1090-vouch-reaches-only-originate.test.ts; services/api-gateway/src/__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts; services/api-gateway/src/__tests__/ks1212-erasure-door-reads-its-own-router-case-option.test.ts; services/api-gateway/src/__tests__/ks1359-platform-audit-log-refuses-a-bad-limit-or-offset.test.ts; services/api-gateway/src/__tests__/ks1369-onproxyreq-skips-header-writes-once-sent.test.ts; services/api-gateway/src/__tests__/ks453-proxy-body-restream.test.ts; services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts; services/api-gateway/src/__tests__/ks570-proxy-mount-auth.test.ts; services/api-gateway/src/__tests__/ks843-erasure-path-bypass.test.ts; services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts; services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts; services/vc-issuer/src/__tests__/credentialsVerify.fuzz.test.ts; services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts; services/vc-issuer/src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts; services/vc-issuer/src/__tests__/ks1352-revoked-credential-fails-verify.test.ts; services/vc-issuer/src/__tests__/ks1375-verify-fails-closed-on-no-issuer-record.test.ts; services/vc-issuer/src/__tests__/ks444.requestSchema.test.ts; services/vc-issuer/src/__tests__/ks586-status-write-authorization.test.ts; services/vc-issuer/src/__tests__/ks692-status-write-platform-only.test.ts; services/wallet-connector/src/__tests__/ks1360-session-delete-carries-success.test.ts
- keyscan_gate43.py -> keyscan_1.out: KEYSCAN PASS: 31 checks over 5 PRs, 0 FAIL, 0 FLAG line(s) (live surfaces; the gate rules them)
