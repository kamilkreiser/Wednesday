# Gate 249 commission, TIER 2 batch, round 1 of 2: PRs 2062, 2082

Model: Sonnet, routing tier-2 gate row. Same rules, questions and output as /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate243-tier2-batch/commission.md: read it whole, ignore its PR list, use clone /private/tmp/g249, and keep its per-PR NEEDS TIER 1 stop line. Both are test-only by the seat's statement, unread by Wednesday. Root H as in that file.

- PR 2062, KS-864, head 71566cce6101 [H/2026-11-06_seatT-14th/mail/out_12_ready_ks864_body.txt]
- PR 2082, KS-1534, head 75c1282a64dc [H/2026-11-06_seatT-14th/mail/out_15_ready_ks1534_body.txt], one file, +21/-1. A test edit that removes a line: what did the removed line assert?
- PR 2083, KS-1505, head 72182689bace [H/2026-11-06_seatT-14th/mail/out_16_ready_ks1505_body.txt]. This one touches product code, index.ts: the seat says the only non-comment change is one comparison and a log call, non-production only, parse and assign order unchanged. Confirm that first by your own diff. If it does more, or can run in production, mark it NEEDS TIER 1.

More tier 2 READYs from T 14th may join this batch before launch; the launching seat adds them here.
