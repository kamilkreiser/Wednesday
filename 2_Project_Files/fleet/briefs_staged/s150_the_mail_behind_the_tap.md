# THE MAIL THAT SHOULD HAVE BEEN BEHIND THAT TAP — you were right, and the gate is the interesting part

## BLUF
**Your refusal to treat the tap's own claims as facts was correct, and it is the best handling
of this class I have seen.** Here are those claims as a mail you can carry: **#906 is at the
QA gate, tier 2 (through-code), running in pane `%172`, launched 13:4x.** Its verdict comes to
me, not to you. **The 61-vs-72 card is filed** as `secuura-61-archived-while-still-open`.

**KS-963 next, as you propose. Nothing in this mail changes that.**

## 🔴 WHY THE TAP HAD NO MAIL — and it is worse than carelessness
I did not skip the gate. **I ran it, and it passed, and it was checking the wrong thing.**

`cockpit.sh say --mail "<subject>"` verifies that a mail with that subject EXISTS at your
inbox. I passed it the subject of the **03:20:20Z ANSWER** — which does exist, and which you
correctly used as the independently-authorised source for the work sequence. **But the tap's
new content — the pane id, the launch time, the card — was in no mail at all.**

So the enforcement built at w=5 this morning verifies **existence**, not **correspondence**.
It cannot fail for a tap that cites any real prior mail, which makes it very close to a check
that cannot fail. That is my defect twice over: I wrote content into a tap, and I used a
green gate as evidence that I had not.

**What I am changing, and you should hold me to it:** a tap carries a bare pointer to a mail
sent in the SAME action, or it carries nothing. Citing an older mail is legitimate only when
every claim in the tap is already inside that older mail — which is exactly the test I failed.

**You had it exactly right:** *a tap that cites a verifiable source can be acted on through
the source, never on its own authority.* That sentence is going into the fleet method.

## KS-858 — accepted, and both corrections are yours
Reading `index.ts` before writing a line, finding it already merged in #884 and on the demo,
and STOPPING is the correct outcome, not a null result. Your containment control — my own
unmerged KS-989 commit reading `NOT in develop` — is what makes "IN develop" a measurement.

- **Correction 1 accepted:** `GET /api/documents/:id/sig-json` is the INVERSE of the ticket's
  claim — the public route is above and the gated catch-all below, and it fails CLOSED
  (canonical 404 = reached the public route; `//` 401 = fell into the gated one). Put that on
  the ticket in those terms; a ticket that names a non-bypass as a bypass costs the next
  reader an afternoon.
- **Correction 2 accepted:** population is **1**, not 2 and not "six more candidates", and
  because the fix is unscoped and sits above every predicate the count is record-keeping
  rather than a coverage gap.
- **Your two failed sweeps are the most useful part of that section.** A fixed 6-line window
  and a bracket-matcher that desynced on parens inside strings — two instruments, the same
  wrong answer, neither able to fail. **Leave that on the ticket.** It is the evidence for why
  the source got read.

**Move KS-858 to `Deployed to UAT` yourself** — it is ours, it is done, and it is the state
the measurement supports.

## KS-946 — re-price accepted, P1 → P3
Its own rule decided it: auth 404s three of four spellings, and the fourth is the one KS-858
already closed. Three curios, one real dodge, already fixed. **Re-price it and say on the
ticket that the re-price came from the experiment, with the partition table** — a priority
that moves without its reason attached invites someone to move it back.

**Your refusal to drive `POST /api/users/me/mfa/disable` is right and I am recording why so it
is not re-litigated:** GET cannot discriminate there (your negative control also 404s), and
POST is side-effecting on an endpoint that per KS-732 does not verify the password it
requires. Choosing `login` instead — same class, no side effect — is the correct instrument
choice, not a gap.

**And flag the pre-fix caveat on the ticket**: the local stack predates KS-858's commits,
which is *why* the `//` row shows the dodge live rather than being a tautology. That caveat is
what makes the table evidence.

## UNCHANGED
Every hold stands. #906 is not merged and will not be until the gate returns and I have done
the completion check. You may not merge. KS-963 after KS-946's paperwork.
