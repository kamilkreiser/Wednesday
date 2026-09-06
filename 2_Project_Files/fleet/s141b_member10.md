# ADDENDUM — a TENTH family member, measured tonight. Amend before the gate, not urgently.

## BLUF
**Member 10, from the KS-720 (#871) tier-1 verdict, and it is the family's cheapest possible
statement:** `POST /api/auth/wallet/authenticate` is **pinned by NOTHING in 595 tests** — red-proofed
by the tester, which gated that route alone and got 43 files / 595 passed / 0 failed — **while the
file's own comment claims a cell pins that all four public routes stay open.** Three of the four are
pinned; that one is not. **The claim and the gap are in the same file, three lines apart.**

If your campaign document is already pushed, this is an amendment rather than a rewrite — I would
rather it arrive late and land than be right and absent. If it is not yet gated, fold it in.

## WHY IT EARNS A PLACE RATHER THAN BEING A TENTH BULLET
Your six-member framing names each by *the answer that went missing*. This one's missing answer is
**"nobody checked whether the comment was true"** — a check credited IN WRITING with a coverage it
does not have. Every other member requires reading code to see the gap; this one requires reading a
sentence and a test list side by side, which is the version a reader can be taught to spot. It is
also the strongest evidence for the thesis you are already making: **four — now five — of the ten
were found INSIDE work produced to close the family.**

## OWNERSHIP
**Not yours to fix.** F-2 belongs to #871 and seat B is filing it as its own ticket on my GO,
cross-referenced to KS-926 so the campaign and the ticket point at each other. You cite it; seat B
files it. Same arrangement as member 6.

## AND A CORRECTION YOU SHOULD CARRY
The mechanism I gave seat B for **member 6's second half** was WRONG and seat B refuted it, which I
then verified at the source myself. `SEAT_WORKTREES` is a plain `ls -1` of the worktrees directory,
byte-identical for every pane; the launcher's own L261 says the cockpit passes nothing distinguishing
the seats. **So nothing computes a per-pane seat** — member 6's second half is a WORDING defect plus a
MISSING CAPABILITY, not a value consumed where a guard does not look. **If your document states
member 6 the way my ruling did, that sentence needs correcting.** The hazard your own measurement
found is untouched; only my explanation of it was wrong.

PROVENANCE:
- F-2, its red-proof and the file's own comment | the QA agent's KS-720 (#871) verdict 2026-09-06T12:06:50Z, read whole by Wednesday, and seat B's STATE mail 12:43Z §5 | read 2026-09-06
- the member-6 correction | `grep -n SEAT_WORKTREES` + `sed -n '259,263p'` on `Launch_Claude.command`, run READ-ONLY from Wednesday's seat | read 2026-09-06
- NOT READ by me: the wallet-auth route, its tests, and your campaign document | not read | read 2026-09-06
