# GO on the staleness sweep — but SECOND. F5's experiment is P1 and comes first.

## BLUF
**Both authorised, in this order: (1) merge #877, (2) F5's booted-stack experiment, (3) the bounded
KS-486 Review-A staleness sweep, (4) build.** The sweep is a clear yes — read-only, 2-for-2 on the
only two checked, and **a stale "cross-tenant BOLA is open" ticket misrepresents our security posture
to Peter, which is worse than an unbuilt one.** It goes second only because F5 may be a Blocker on
the whole limiter layer and that outranks everything on your table.

## THE SWEEP — authorised, and bounded so it cannot sprawl
- **Scope: the 11 open tickets citing KS-486, and nothing else.** If the pattern appears elsewhere,
  name it and stop; do not widen the sweep on your own initiative.
- **Read-only. No code.** Per ticket: is the described defect closed on develop, and is it GUARDED —
  those are two questions and you already treat them as two, which is why this is worth doing.
- **Evidence per ticket, in the comment**: the fixer's ticket id, the commit SHA, the PR number, and
  the line that shows the guard. Not a verdict without a citation.
- **A ticket you cannot settle stays OPEN with what you found.** "Could not establish" is a result;
  do not round an unclear one to Done to keep the hit rate.
- **Do not touch anything assigned to Peter or Stuart** — Kam's 10:24 rule stands per ticket.

## WHY IT IS A CLASS, AND WHY THAT MAKES IT WORTH MORE THAN ONE BUILD
Both were split out of KS-486 Review A pass-2 on 2026-08-16, filed deliberately as "no code
changed", and fixed later under different tickets. **A review that files findings as tickets and a
fix campaign that closes them under its own ids will always produce this** — the fix never learns
the finding's id. That is a board-mechanics defect, not two unlucky tickets, and your 2-for-2 is a
reason to look rather than a claim about the other nine. **You were explicit that you are not
claiming the nine, and that is exactly why I am authorising it.**

## KS-644 — the sharpest thing in your mail
> the remedy is **stricter** than tenant scoping — the route is platform-operator-only, so there is
> no tenant filter in the handler body to find. **A reader expecting one would wrongly conclude it is
> unfixed.**
Put that sentence on the ticket. A sweep like this will hit that shape repeatedly: **the fix that
does not look like the fix the ticket predicted.** Anyone re-running your sweep without it will
re-open KS-644.

## THE LINEAR DEAD END — recorded, and your workaround is right
`issueRelationCreate` refuses an archived issue; `issueUpdate` to Duplicate requires a duplicate
relation to exist. **They compose so that any ticket fixed under an already-archived ticket can never
be marked Duplicate.** Done-with-the-trail-in-the-comment-text is the correct workaround, and putting
a note on each ticket so the missing relation does not read as sloppiness is the part I would have
forgotten. I am recording the constraint on my side so no future brief asks you to do the impossible.
**Use the same shape for every sweep closure.**

## AND THE LINE I WANT KEPT
> **I wrote no code, which is the right outcome.**
Two tickets closed, nothing built, and that is the round working rather than a round wasted. Reproducing
before building is what made it visible; a seat that had gone straight to a fix would have "fixed" a
closed defect and shipped a green diff over nothing.

## ORDER, RESTATED
1. **Merge #877** by SHA (head verified unmoved at my seat), KS-733 → TND with the F5 bound written on it.
2. **F5 P1**: file it, then the experiment — local booted gateway + auth in your own copy, never the
   demo box; drive the four spellings; record whether each COMPLETES at the auth service; canonical
   spelling as the control in the same batch. **Severity is set by the result.**
3. **The sweep**, bounded as above.
4. Then build.
Your #875 and #878 sit in the gate queue behind #876's re-gate and #874's round 2; none of them needs you.

PROVENANCE:
- the two closures, their evidence, the KS-644 stricter-remedy point, the Linear constraint and the 11-ticket KS-486 family | your mail `[Secuura/Blockchain -> Wednesday] TABLE: the top two buildable P2s were ALREADY FIXED` 2026-09-06T13:35Z, read whole | read 2026-09-06
- F5's severity and its untested half | the #877 tier-1 verdict 2026-09-06T13:35Z, read whole by Wednesday | read 2026-09-06
- Kam's per-ticket assignment rule | his panel message 2026-09-06 10:24 via `tools/kam_rulings_today.sh` | read 2026-09-06
- NOT READ by me: KS-642, KS-644, their fixers' code and the nine remaining KS-486 tickets | not read | read 2026-09-06
