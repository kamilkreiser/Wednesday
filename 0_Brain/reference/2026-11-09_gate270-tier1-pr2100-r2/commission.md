# Gate 270, tier 1, ROUND 2 OF 2 (the cap): PR 2100, KS-1868 (originate email.ts catches). Launched 2026-11-09 ~04:4x AEDT by the 03:5x Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. ONE PR.
Round 1: gate 268, 'PR 2100: NO GO' — read its verdict WHOLE: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate268-tier1-pr2100-ks1868/verdict.md (G268-1 Major test isolation: the new test's ACS mock marked virtual on an installed module; G268-2 Medium false words 'every caller treats false as not sent'; G268-3/4 Low words; G268-5 the seat's tsc controls fired on a config error).
Pins (Wednesday's ls-remote 04:40:36): PR 2100 head eb4a08362cfb6ce90ffa094078bd8620caebe5e7; develop 15dca468b86f878b27fe1c567e1d39e523d114b1 (MOVED since the seat's READY: PR 2074's merge, shell/tooling only by its PR). Re-read both at start and end; a moved head voids the verdict.
READY (claims, untested by Wednesday): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-17th/mail/ready_ks1868_round1_body.txt, whole. The fix round is ONE commit on 60e2bf4e6d25: 3 files, +9/-7 (the test, the cheat and flow fragments), no product byte by the seat's read. HELD drafts to read (posted only after this verdict): .../2026-11-09_seatT-17th/mail/pr_body_ks1868_round1_HELD.md and .../mail/ticket_comment_ks1868_round1_HELD.md.

Questions, deepest first:
1. Each of G268-1..5: closed, closed in part, or not? Run, do not reason. G268-1: the pair ks1868 + ks1937 in both orders under --runInBand, and plant the virtual flag back (must fail), restore byte-equal.
2. Scope: is the round delta exactly the 3 files with no product byte (git diff --stat 60e2bf4e6d25 eb4a08362cfb with a control)? Did the round-1 product hunks in email.ts stay unchanged?
3. Product re-check at this head (round-1 findings did not hold the product, but a fix round can disturb it): one hostile-throw cell of your own on each of the three catches; ordinary errors' logged text unchanged.
4. G268-5: the tsc control fires on a real type error (TS2322), not a config error.
5. Words: every sentence in the cheat + flow fragments at the head AND in the two HELD drafts true at this head.
6. Merge tree onto develop 15dca468b86f; open PRs sharing a path (planted control).
This is round 2 of 2 under the cap: a NO GO means the closed instances ship and the residue is ticketed (Wednesday decides), so mark each finding as BLOCKING THE MERGE or TICKETABLE.

Clone on the boot volume /private/tmp/g270 (QA no-rm; name its size); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; stop if DevMASTER under 10 GiB.
Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate270-tier1-pr2100-r2/verdict.md, line 1 exactly 'PR 2100: <GO|GO WITH NOTES|NO GO>', then per the common rules (BLUF; findings with severity, file:line, FOUND / TESTED / HOW; NOT tested; own conduct). Findings only; post nothing.
