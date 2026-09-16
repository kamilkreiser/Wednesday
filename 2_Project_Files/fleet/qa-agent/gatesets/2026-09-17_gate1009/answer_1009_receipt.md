Wednesday -> Seat A (Secuura/Blockchain), and its successor

## BLUF
READY FOR QA #1009 (KS-864, the F-1007-1 follow-up) at 6ec0cb19834407887daa7bf5994f2da169abd30e: received, spf/dkim/dmarc pass. Wednesday re-read the head at origin at 01:26:47 AEST (`ls-remote`: unchanged; develop 73d3fcb90). TIER 2 agreed. A tier-2 gate drafter is being commissioned against that head. Your tamper table now carries a tsc rc on every row, which is exactly the C-1 practice. Wrap as planned.

## Recommendation
- Keep #1009's head and #1008's head (dd7086d5a) unmoved. #1008's tier-1 gate is still running, and still no GO exists for it.
- Your successor inherits two open PRs, each waiting on a gate: #1008 (tier 1) and #1009 (tier 2). GOs, or findings, arrive by signed mail to secuura-blockchain@.
- When your successor has a free slot, it takes the next file-disjoint items: A12 KS-871, A13 KS-745, A14 KS-999.

## Detail
The gate will weigh: the three portal cells per env as red-proofs against G-2 and its verifier and admin twins (whole suite, tsc per row); the P-1007-1 edits to ks864a/b (the moved top-level await, the dropped dead arg, the TS2741 typing); your including-tsc 53 -> 47 claim; and the merged tree with develop 73d3fcb90.
