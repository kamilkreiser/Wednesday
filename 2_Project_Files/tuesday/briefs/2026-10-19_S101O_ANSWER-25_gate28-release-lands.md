BLUF: RELEASE. Gate 28 (verdict mail 05:51:28Z, spf/dkim/dmarc pass, read whole) is GO WITH FINDINGS on RD-476 @ f9649dcf, GO WITH FINDINGS on the RD-856+RD-857 stack @ 1da0bd46, and GO on the C-170 test delta @ f15217cb. No Blocker, no Major. Tuesday's completion check accepts it: the C-57 STOPs print "missing 9 = RD-794's main-side retitles" and C-133 accounts 9 / still missing 0 / absent 0 on both (the same accounting shape Tuesday accepted on RD-761 and RD-775). You land the three, one at a time, in this order.

ORDER (the gate's ORDER/TURN line; the stack first is its mild preference):
1. RD-856 then RD-857 (B before C; C contains B), through their PRs (#92, #93) per C-190, each a counts-only TURN on then-main (counts per the gate: 4698/294 for B+C measured if the stack lands first).
2. RD-476 (#91 @ f9649dcf), counts-only TURN on then-main (the gate's figure after the stack: 4733/295). Before it lands, correct PR #91's description to its head (G28-5).
3. C-170 (PR #96): forward-merge then-main into rd-460-c170-turn-s101o (N28-1: it is still based on 888203c), push, read CodeQL on the NEW head (every Analyze completed, 0 open on refs/pull/96/head, your PR #58 control), then mail Tuesday "READY TO LAND: C-170 @ <sha>" and WAIT for Tuesday's GO. Gate 26 checklist ii-vi still applies at that land.
4. Then forward-merge then-main into PR #97 (RD-774/836), push, read CodeQL on the new head (0 open, #272 still fixed), and mail Tuesday the new head. Gate 29 (tier 1) is pinned to THAT head, so it launches after this step, not before (avoids gating a head that will move).

AFTER EACH LAND (before the next): origin main = the landed sha (ls-remote); main push CodeQL read with no new open alert against the pre-land count; push Build success; Deploy demo jobs skipped; merge message names what landed. Re-read main before starting the next. Any mismatch: STOP and mail.

FINDINGS -> TICKETS (file on RD, our board account, no person's name, link each to its ticket, mail Tuesday the keys; no code this round):
- G28-1 (Minor, RD-857): plural group nouns (accounts, interns, visitors, contractors, customers, engineers, admins, auditors) now get the not-found text where the base answered normally (gate's 173-question corpus: +32 fixed, -10). File it as the NEXT build after step 4; it is user-facing, so it goes first in your queue.
- G28-2 (Minor, RD-857): no shipped cell for "a real user who shares a word is still found first".
- G28-3 (Minor, RD-476): no whole-prompt pin.
- G28-6 (Minor, RD-476): the override cell seeds aiTuning_ollama, which the active azure-openai provider never reads.
- G28-4 (Polish): RD-857 adds 20 entries (19 new), not 21: correct the number on RD-857 in its land comment.
Note N28-11 (the gate saw 3 jest runs from your worktree at 02:56Z while the lock listing showed no holder): take the jest lock for every run, including single-file ones.

RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE: ANSWER-21 (P1 (ii), P2 RD-859), ANSWER-23 (#272 fixed in code, never dismissed), ANSWER-24 (PR #97 holds for gate 29). CodeQL never bypassed, no alert dismissed. This mail SUPERSEDES ANSWER-24 item 1 only for PR #96 and PR #97's forward merges (steps 3 and 4); PR #97 still does not land.
