# Gate 249 commission, TIER 2 batch, round 1 of 2: PRs 2062, 2082

Model: Sonnet, routing tier-2 gate row. Same rules, questions and output as /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate243-tier2-batch/commission.md: read it whole, ignore its PR list, use clone /private/tmp/g249, and keep its per-PR NEEDS TIER 1 stop line. Both are test-only by the seat's statement, unread by Wednesday. Root H as in that file.

- PR 2062, KS-864, head 71566cce6101 [H/2026-11-06_seatT-14th/mail/out_12_ready_ks864_body.txt]
- PR 2082, KS-1534, head 75c1282a64dc [H/2026-11-06_seatT-14th/mail/out_15_ready_ks1534_body.txt], one file, +21/-1. A test edit that removes a line: what did the removed line assert?
- PR 2083, KS-1505, head 72182689bace [H/2026-11-06_seatT-14th/mail/out_16_ready_ks1505_body.txt]. This one touches product code, index.ts: the seat says the only non-comment change is one comparison and a log call, non-production only, parse and assign order unchanged. Confirm that first by your own diff. If it does more, or can run in production, mark it NEEDS TIER 1.
- PR 2084, KS-1858, head 223499281cb9 [H/2026-11-06_seatT-14th/mail/out_17_ready_ks1858_body.txt], test-only, one new auth test file. It lists one tamper that stays green by construction, not counted: does that leave a real hole?
- PR 2086, KS-736, head c70f8182f43d [H/2026-11-06_seatV-26th/mail/out_05_ready_ks736.txt], tests only, 1 file +169/-6, but they are a security check's assertions, gateway mount auth. Card secuura-ks736-made-up-token-result-1106 = b, read it. Test Evidence was run by V 25th, not by V 26th: reproduce it yourself. If it weakens any assertion or needs security judgement beyond a test read, mark it NEEDS TIER 1. An overlap with PR 2060 on one line is granted; check the merge.
