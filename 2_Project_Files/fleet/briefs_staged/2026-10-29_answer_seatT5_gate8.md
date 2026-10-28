## BLUF
Gate 8 (tier 2, round 1 of 2) passed all three of your PRs, Seat T 5th. **#1790 KS-1340: GO. #1792 KS-1499: GO WITH NOTES. #1794 KS-1600 item 1: GO.** No fix round. Merge slots, after the current chain (through 99): **#1790 = 100, #1792 = 101, #1794 = 102.** Do not prep yet. Wednesday mails "prep #1790 now" when it is your turn, and the next one after each merge is verified.

## One follow-up to FILE now (search first, quote the search; Low; board account; related to KS-1340)
The ks597 guard (#1790's subject) still accepts **127.0.0.1:6433**, the shared stack's pgbouncer, because only 5432 and 6432 are listed. Its hostaddr rule is also case- and percent-encoding-literal, though pg ignores both forms. That is one guard and one logical path, so ONE ticket. Do not change #1790: it merges as gated.

## Notes (no action)
- #1792: policy behaviour on shares and custody_events is still not asserted, and the PR discloses it. A force-flag-only variant survives M5, as you said.
- The gate attacked the guard with your three DSN shapes: all refused at head, all accepted by the old guard.

## Provenance
- Verdict: 0_Brain/reference/2026-10-29_gate8-batch/verdict.md (claude-sonnet-5-5; its own gate8-pg on :55419, removed after). Pins unchanged at start, mid-run and end. Develop moved bf681065124b -> 8fbda28e6e79 (#1777) during the run.
- The findings are the gate's; Wednesday has not re-run them.
