--- comment 5826293848 by linear[bot] at 2026-09-25T03:41:28Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1181/ks-727-error-handler-guard-corpus-1-canary-cells-cannot-witness-a-hit">KS-1181 KS-727 error-handler guard: corpus-1 canary cells cannot witness a hit, and the header's 'a wrong count is a red test' sentence is false (KS-844 gate F2/F3)</a></summary>
<p>

## BLUF

The KS-727 error-handler class guard (`packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts`) has two test-quality gaps, found by the tier-1 QA gate on PR #1006 (KS-844):

* **F2 (Minor):** the corpus-1 canary cells cannot witness that the handler was hit. If a handler throws first, the constant backstop answers and all 8 canary cells stay green; only the authored CONTROL reddens.
* **F3 (Polish):** the header sentence "if a count below is wrong, a test is red" is false (reverting the counts to 8/9 leaves 851/851 green). "The 10th handler" also means the surplus handler, not the 10th in the sorted set.

## Recommendation

* Assert a hit or answered count (or `forwarded === false`) in the canary cells for non-forwarding handlers, with a 0-hit control. The gate's G5 (the handler throws) must then redden the 6 NODE_ENV cells.
* Either parse the header counts in a cell and compare them with the sets, or reword the sentence.

## Detail

Source: tier-1 QA gate on PR #1006 at `86fe59e6bf07108142fb3dbd06bef8747d2a4687`, 2026-09-17. Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks844-1006-86fe59e6b-tier1-r1/report.md`. The findings, verbatim from its table:

| \# | finding | evidence class | severity | target | SHIPS-WITH / TICKET | oracle |
| -- | -- | -- | -- | -- | -- | -- |
| **F2** | The KS-727 corpus-1 canary cells cannot witness a hit. With the handler throwing (G5), the 6 NODE_ENV + payload-size + `details` cells stay GREEN because the constant backstop answers; only the authored CONTROL reds. The gate's counting cells show the handler IS hit today (hits 1 / answered 1 × 6 envs, 0-hit control 0) and red 12/12 under G5. | MEASURED AT RUNTIME (§5) | Minor (test-quality, pre-existing harness) | KS-727 guard owner (`packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts` `driveThroughRoute`) | TICKET. Fix-shape: assert `forwarded === false` (or a hit/answered count) in the canary cells for non-forwarding handlers. Regression test: G5's throw must red the 6 NODE_ENV cells. | *Purpose* |
| **F3** | ks727 header `:18-21` "if a count below is wrong, a test is red" is false: the counts are comments, and G7 (8/9) gives 851/851. Also "The 10th handler is … `payloadTooLargeErrorHandler`": it is the 4th in the sorted set; the sentence means "the surplus handler". The #1006 header commit is correct at head (header == sets by AST) but relies on that sentence. | MEASURED (G7) + READ (AST) | Polish | KS-727 guard owner | TICKET (or Record). Fix-shape: parse the header counts in a cell and compare with the sets, or reword the sentence. | *Product* (comment vs behaviour) |

Dedupe before filing (seat A, 2026-09-17): literal matches over Linear `searchIssues` (archived and comments included), title + description + comments.
TERM 'ks727-errorhandler-class-guard': scanned 91 over 2 page(s); literal hits 12
    KS-1141 \[Backlog\] QUESTION: are `crypto-agility.guard.test.ts:44` SCAN_DIRS and `ks727-errorhandler-cla     KS-1155 [Backlog] packages/shared tree-walking guards exceed vitest's 5 s default under fleet load — 5      KS-573 [Done] systemTest (Schemathesis): assert the shared control-byte boundary is mounted in ever     KS-727 [Deployed to UAT] Security: errorHandler returns err.message verbatim on any non-production NODE_ENV -      KS-764 [Done] Security: decideKeyRevoke has no organisation arm — an ORG_ADMIN can revoke a sibling     KS-818 [Done] KS-800 follow-up: four small scanner and harness items from the re-gate (G-05…G-08)     KS-830 [Canceled] KS-727 guard suite: three CONTROL cells are red on develop — referral, staking and vc     KS-832 [Done] KS-800 scanner residues from the KS-817/831 gate: a silent guard-side false clean, an     KS-833 [Done] KS-818 residues from the #834 gate: a live entry-point list left behind, and three co     KS-845 [Done] Close the NINE bare `app.listen(0)\` sites in auth and referral — the intermittent-red
    KS-876 \[Done\] KS-860 guard walks services/ only — test listeners under packages/ are unguarded, inc
    KS-953 \[Backlog\] CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and nothing
TERM 'driveThroughRoute': scanned 0 over 1 page(s); literal hits 0
TERM 'EXPECTED_HANDLERS': scanned 127 over 3 page(s); literal hits 1
    KS-830 \[Canceled\] KS-727 guard suite: three CONTROL cells are red on develop — referral, staking and vc
TERM 'demo-service/src/middleware/errorHandler': scanned 90 over 2 page(s); literal hits 0
TERM 'headersSent': scanned 1 over 1 page(s); literal hits 1
    KS-815 \[Deployed to UAT\] Security: two live api-gateway verify routes parse a body no control-byte guard inspe
TERM 'finalhandler': scanned 0 over 1 page(s); literal hits 0
None of the hits is about the canary cells' inability to witness a hit, or the header-count sentence. KS-830 (canceled) was red CONTROL cells; KS-1141 is the SCAN_DIRS question; KS-1155 is timeouts; KS-953 is api-gateway index edits reddening shared. Filed new. The status-sanitisation findings (F4/F7) are a separate ticket with a separate owner.

Related: KS-844 (the PR that surfaced these), and KS-727 (the guard's origin ticket). KS-727 is archived, so Linear refuses a relation to it; it is named here instead.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1181-canaryhit-the-ks727-canary-cells-witness-that-the-handler-999aead136e6">Review in Linear</a></p>

