# Spark briefs, batch 2, 2026-10-28 12:55-13:45 AEDT (drafter for Wednesday)

Develop at start = 8894c7486f82f6eb682fecb879791f53312537b1 (ls-remote). It moved to 65bc28234507 at ~13:29 (#1756 and #1772 merged); round.sh accepted every brief at the new tip (none of the briefs' files changed).
Independence: `gh pr list --state open` read twice (12:57 17 PRs/74 files; 13:4x 15 PRs/57 files); a script compared every golden.diff file header to the open-PR file sets: 0 overlaps both times. No two of these 7 briefs touch the same file. (Batch 1's ks_1779_p1 also edits adminConfig.ts, at :2181/:2221; this batch's ks_1780_p2_admin edits :128-:1725; different hunks, the raise seat merges them separately.)
Backlog screened: 377 KS Backlog/Todo titles read (paginated to the end), then KS-1780, 1776, 1777, 1467, 1530, 1761, 1593, 1712, 1681, 1755, 1250, 1197, 1208, 1113, 1105 read whole. Generator: scratchpad/gen/mk.py (specs specA..F beside it); briefs are generated, goldens made by difflib, never typed.

## Queued (7). All Secuura. Verdicts are from done.md (13:03-13:4x).
| brief dir | ticket | tier / rung | dry-run | control | Spark round | harder? |
|---|---|---|---|---|---|---|
| night/briefs/ks_1780_p2_admin | KS-1780 (15 adminConfig.ts catches) | code_patch, 16 hunks in one file (2 helpers + 15 replaced conditions) + NEW 21-cell loopback jest | rc 0 | CONTROL-PASS BYTE-IDENTICAL; A4 9 failed/21, A6 1690->1711, A7 ok | PASS BYTE-IDENTICAL 13:03 (113 s model) | YES: multi-site (15 near-identical lines) |
| night/briefs/ks_1780_p3_webhooks | KS-1780 (webhooks.ts:320) | code_patch rung 2: wrapper in utils/pgErrors.ts + NEW 8-cell route+unit jest | rc 0 | r1 CONTROL-FAIL (A4: the unit cells were red by a thrown error, not an assertion; fixed with a THREW wrapper), r2 CONTROL-PASS BYTE-IDENTICAL | PASS BYTE-IDENTICAL 13:13 | no |
| night/briefs/ks_1250_p1 | KS-1250 (smoke-test.sh ignores SMOKE_BASE_URL) | bash_patch rung 2: 1 hunk + NEW 5-cell stub-curl bash suite | rc 0 | CONTROL-PASS BYTE-IDENTICAL | PASS TREE-IDENTICAL 13:21 | YES: first bash tier of the batch |
| night/briefs/ks_1467_p2_shared | KS-1467 (packages/shared AppError prototype) | code_patch rung 2: 1 line + NEW vitest | rc 0 | CONTROL-PASS BYTE-IDENTICAL | PASS BYTE-IDENTICAL 13:23 | no |
| night/briefs/ks_1776_p1 | KS-1776 (auth routes/auth.ts seedDemoUsers timer) | code_patch rung 2-3: 5 lines -> 12 + NEW 4-cell FAKE-TIMER vitest with a 9-module mock set | rc 0 | CONTROL-PASS BYTE-IDENTICAL | PASS BYTE-IDENTICAL 13:27 | YES: the ticket is facts-only, the fix shape is the drafter's (stated); fake timers |
| night/briefs/ks_1197_p1 | KS-1197 (POST /api/documents half) | code_patch rung 2: enforcement.ts 2 hunks + NEW 16-row vitest | rc 0 | CONTROL-PASS BYTE-IDENTICAL | PASS BYTE-IDENTICAL 13:29 | YES: loose-ish (ticket recommends a different place; consumer-side fix chosen) and security-adjacent (fails toward LESS access) |
| night/briefs/ks_1467_p1 | KS-1467 (services/auth half) | code_patch2 RUNG 3: 2 products (errorHandler.ts 1 line, passwordLoginGate.ts comment) + NEW 34-row vitest incl. a source-text cell | rc 0 | r1 REFUSED (two packages: 'not under the ONE service'), r2 REFUSED (a move diff has a '+' line equal to a '-' line), r3 CONTROL-FAIL (A6: top-level await TS1378 against the ks1000 type-check baseline), r4 CONTROL-PASS BYTE-IDENTICAL | PASS BYTE-IDENTICAL 13:36 | YES: rung 3 |

Harder = 5 of 7 (p2_admin, 1250, 1776, 1197, 1467_p1). Spark results: 7 of 7 PASS (6 byte-identical, 1 tree-identical; model time 31-113 s, rounds 77-201 s), so none of the harder ones failed; the capability data is "no failure yet on multi-site, bash, fake-timer or two-product work when the golden is spelled out byte for byte". A genuinely loose brief (fix described, not spelled) is still blocked by the builder, not tried.

## Capability / tooling data from drafting (dead ends worth keeping)
- The tier refuses a brief that spans two packages (code_patch2: 'not under the ONE service'): split per package.
- The builder refuses a diff whose '+' line equals a '-' line in the same edit block (a pure MOVE of a line). KS-1467 gate note 1 (move a const below imports) was dropped for that reason.
- Blank context lines are refused by the builder: the generator trims leading/trailing blank context from each hunk.
- A test red by a THROWN error inside a cell (not an assertion) fails A4 ('CONTROL cell red at the tip'): wrap the call and return a sentinel string.
- A new vitest file with a top-level `await` fails A6 (the ks1000 type-check ratchet, TS1378); use static imports.
- Builders still refuse products outside services/* and packages/shared (KS-1105 Login.tsx, KS-1775 check.cjs).

## Candidates dropped
- KS-1777 (flat 403 body: relied on by 3 systemTest files, a decision), KS-1778 (question), KS-1782 (box config), KS-1530 (decision first, flips a pinned test), KS-1208 (shape decision: 401 vs guard), KS-1113 (e2e spec, cannot be run by the checker), KS-1105 (frontend/admin product path refused by the builder), KS-1761 (guard hardening, no fix shape, test file is the product), KS-1593 (tsc-level cell, originate not in the type-check ratchet), KS-1712 (needs Postgres), KS-1681 (maintainer call), KS-1755/1764 (preflight design), KS-1322 (spec prose, openapi file in #1773 at the time), I4 anchorExistsInDb (routes/anchors.ts was in #1772; #1772 has since MERGED, so it is now a candidate for a later batch).
- KS-1467's ticket also says 'decide deliberately that 422 responses now carry details': NOT decided here. In services/auth the handler's existing branch starts to run (cell H1). The raise seat must put that visible change to the owner. Gate notes 1 and 2 of KS-1467 are not in the brief.
- KS-1776 is facts-only ('no fix proposed'); KS-1197's ticket recommends a different place for the fix. Both briefs say so and name the chosen shape; the raise seat confirms with the owner.

## Drainer
pid 23016 (started 13:00, first drain), pid 40030 (13:15), pid 80190 (13:4x, the one running at the end); log local-model/spark/state/queue.log. The queue emptied between drafts twice (13:13 and 13:30) because the controls had not finished: the Spark was idle for ~2 min at 13:13-13:15 and ~1 min at 13:30.

## Final state
All 7 rounds PASSed by 13:36; queue empty, no drainer, Spark IDLE at 13:37 (spark_status.py prints IDLE). Nothing is held, raised or pushed: Wednesday reads the diffs against the briefs and hands them to a raise seat.
