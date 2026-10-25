From Tuesday (the product owner's Datasec coordinator seat), Datasec / NexusAI. ADDENDUM-1 to B650 (SEAT-M9), written by Tuesday s170 on 2026-10-25. Answers your STOPPED question (B650-1).

ANSWER: your option (i). Push the four commits ending `8993b233` UNCHANGED as the plain fast-forward from `412c784b` to `refs/heads/b642/nexusai-validators-777-776`, exactly as your FOR TUESDAY section scripts it (re-read ls-remote and the intersection first, push under /bin/bash, no force, no rebase, no amend, read the ref back), then finish Steps 7(d) and 8 and write your READY FOR QA last line.

Why (Tuesday's technical ruling, inside the coordinator's delegated scope; no word on any screen changes):
1. The defect this round exists for is SUPERLINEAR (B647-1: 18 s at 200 KB on the round-1 head). Your bounded strip makes it linear (3-4 ms at 200 KB). That is the fix.
2. B650-1 is a LINEAR, bounded cost at the 50 MB body limit on hostile nested input (S1 1.07-1.28 s, S3b 1.85-2.32 s, S3c 1.02-1.03 s), the same order as main's own linear `< ` / `<LF` shapes (1.2-1.9 s, per your measurement and the B647 follow-up list), and the round-1 head pays the same or more. The "under 1 s" figure in your brief was an UNMEASURED drafter prediction, not a requirement from the ticket or the product owner; you measured it false, which is the correct outcome of a prediction.
3. A different bound (P = 2) changes the gate's expected outputs, and option C carries an unmeasured CodeQL risk: both are new design in round 2 of 2 with no measured gain. The length cap (iii) is new customer-visible behaviour and is the product owner's, so it is NOT brought into this round.
4. B650-1 joins the existing length-cap follow-up (the B647 linear-shapes ticket). Tuesday owns filing it with your three figures; you do not write Jira in this round.

Record in STATUS under Corrections: this addendum, the ruling (i), and that B650-1 is accepted as a bounded linear cost carried to the length-cap follow-up. Your last line stays as the brief specifies (READY FOR QA). The round-2 tier-1 gate will be told this ruling, so it judges the strip against the linear property, not against the 1 s prediction.
