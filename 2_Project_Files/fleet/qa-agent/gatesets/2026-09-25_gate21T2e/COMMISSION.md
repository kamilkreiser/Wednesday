# COMMISSION — DRAFT the round-21 tier-2 QA gate kit "gate21T2e" over ONE PR: #1241 KS-1226 item 2, ROUND 2 OF 2. Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-25 (~21:4x AEST). Recorded here as the gate's commission; the QA agent reads it. Shape copied from
`gatesets/2026-09-25_gate21T2d/` (the round-1 kit: JSON pins, routing-file override, controls both ways with `--invert`), re-keyed to ONE row, with
BRIEF_TEMPLATE.md and QA_AGENT_CHARTER.md.

## The PR — TIER 2, round 2 of 2 (THE CAP), one seat (Seat B 27th)
- **#1241** KS-1226 item 2, head `b4427d416592b40eb5ddb8727b2d6c31f3c7d067` (READY 11:41Z), a fast-forward from the round-1 head
  `e2d0518df40228f0a183bc4223c7a6840821253e`. **Round 2 of 2: a NO GO ships nothing and tickets the residue.**
- Round-1 NO GO report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1241-t2d/report.md`.
  - LIVE-SHAPE NULL: vitest 4.1.11 prints `skipped` (and `todo`, `expected fail`) AFTER `passed`, so the round-1 regex returned NULL on every real
    summary. The ticket's example was a composed line.
  - The cells re-implemented :103's reading instead of calling it, so a change at :103 alone left them green.
- The seat's round-2 READY (read only as `inbox_digest.sh full wednesday-agent@agentmail.to '<010001a0d85ed666-…>'`) claims:
  - captured real vitest lines (5 shapes, including `expected fail`);
  - both red arms fire;
  - the 15-leg preflight did NOT run on this push, by the hook's design;
  - 4 tickets filed.

## The gate MUST (Wednesday's list, carried into the prompt)
1. **MANDATORY LIVE-SHAPE, again.** Re-capture real vitest 4.1.11 `--reporter=default` summaries from fixtures OUTSIDE the package:
   - skip+fail+pass, skip+pass, todo+pass, expected-fail+pass, pass-only, fail-only, and a multi-file summary.
   - Run the HEAD parser on each through the REAL code path (childSuiteCounts() or the exported parser), never a lifted regex.
   - Every real shape must return correct counts. NULL on any real shape = NO GO.
   - **Drafter's note:** the parser `readSuiteCounts` is NOT exported, so the prompt prescribes an in-file GATE-PROBE plant (L2) plus plants that go
     through childSuiteCounts() itself (L3).
2. Confirm the new cells go through :103: tampering :103 alone must red a cell.
   - The prompt maps round 1's :103 to its two successors: the head's :93 (R-B) and the call site :157/:161 (R-C, T-CALL).
   - The cells' strings must match captured output byte for byte (L4).
3. Red proof: the cells RED on round-1 head e2d0518df and on develop, GREEN at b4427d4165 (R-A, R-D, R-E).
4. The package suite before and after (systemTest/performance, `vitest run --config vitest.unit.config.ts --no-file-parallelism`). The one PRE-EXISTING
   PRESUITE-URLPATH red noted in round 1 is not this PR's.
5. Item 1 (the :127 budget) stays OUT of scope.
6. Base-invariant checks over the current develop, re-read at launch. It was 33ccff807eb2bb0a43c5d03ceb88d877b86950e1 at 21:4x AEST, and the drafter
   re-read the same value at 11:49:57Z and again at 11:58Z.
7. GO string `GO: merge #1241 batch`. A MERGE ADDENDUM per the precedent: subject <= 92 chars, own key only, equality targets, SHIPS-WITH.
8. Routing `QA/Secuura-batch1241r2`. PROPOSED line `QA/Secuura-batch1241r2|coagent@agentmail.to|yes`, NOT written by the drafter.
9. No Docker and no DB needed.

## Legitimate shapes (BRIEF_TEMPLATE §2a). The reader is a CHECKER of vitest's own output.
Expected verdict = what the gate must see from `readSuiteCounts` on the REAL line. Predicted-by = drafter, READ ONLY (predict_2.out (e)/(f)). The gate
MEASURES every row.

| shape (piped, `--reporter=default`) | the real line (drafter's prediction from vitest 4.1.11's dist; NOT captured by the drafter) | correct counts | head reader, predicted |
|---|---|---|---|
| S1 skip+fail+pass | `Tests  1 failed \| 1 passed \| 1 skipped (3)` | {1,1} | reads |
| S2 skip+pass | `Tests  1 passed \| 1 skipped (2)` | {1,0} | reads |
| S3 todo+pass | `Tests  1 passed \| 1 todo (2)` | {1,0} | reads |
| S4 expected-fail+pass | `Tests  1 passed \| 1 expected fail (2)` | {1,0} | reads |
| S5 pass-only | `Tests  1 passed (1)` | {1,0} | reads |
| **S6 fail-only** | **`Tests  1 failed (1)`** (utils `getStateString`: `passed ? … : null`) | {0,1} | **NULL, predicted: NO GO** |
| S7 multi-file | ` Test Files  1 failed \| 1 passed (2)` / `Tests  1 failed \| 1 passed \| 1 skipped (3)` | {1,1} | reads |
| S8 skip-only | `Tests  N skipped (N)` | {0,0} | **NULL, predicted** |
| S9 todo-only | `Tests  N todo (N)` | {0,0} | **NULL, predicted** |
| S10 orientation | `Tests  2 failed \| 3 passed (5)` | {3,2} | reads |
