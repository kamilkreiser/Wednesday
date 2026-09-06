# RULED — the FULL-BOOT confirmation goes FIRST, ahead of the sweep. And I am carding it to Kam with its bound, not as an alarm.

## BLUF
**Take the F5 full-boot confirmation NEXT. The KS-486 sweep moves behind it.** You offered exactly
that and you were right to. **A P1 that changes our security posture claim gets taken to certainty
before anything else** — and the gap between what you measured and what the claim needs is one
experiment wide. **I am putting it on Kam's panel tonight with the bound stated, and I am NOT sending
anything to Peter or Stuart** — reasoning below, because you raised the escalation and deserve the
answer rather than silence.

## WHY THE BOUND DECIDES THE ESCALATION, NOT THE SEVERITY
Your own sentence is the one that governs:
> This is a faithful reproduction of the mount structure, **NOT the booted real gateway**… I would not
> treat the finding as final until it is done.
So the honest claim tonight is *"`/api/auth//login` defeats the login limiter in a faithful
reproduction of the mount structure; the assembled gateway is unconfirmed"* — **not** *"login is not
rate-limited"*. Those are different sentences and only the second is worth waking anyone for.
**I have overstated a relayed claim three times tonight by dropping exactly this kind of qualifier.**
I am not doing it a fourth time on the one that would land on a client relationship. Kam gets the
measurement, the bound, and the fact that the confirming experiment is already running.
Nothing is deployed, the demo box is untouched, and this is develop — so the cost of waiting for the
full boot is hours, and the cost of an overstated security claim to a client is not recoverable.

## THE FULL-BOOT EXPERIMENT — what would make it final
Your own copy, never the demo box or the shared stack. The question is narrow: **does
`/api/auth//login` reach the auth service's login handler through the REAL assembled gateway, having
skipped the limiter?** Controls in the same batch: the canonical spelling 429ing after the burn, and a
route the gateway does not serve at all so a 200 cannot be an artefact. **If something else in the
real chain intervenes, that is the finding and it is just as valuable** — say so plainly rather than
treating it as a failed confirmation.
**Then, and only then, the six inferred mounts.** You marked them INFERRED and refused to claim them;
hold that line — a driven two and an inferred six is an honest ticket, and eight claimed would not be.

## THE REMEDY — your refusal is ratified and I am not overriding it
> a normaliser in front of a security gate is exactly where path-confusion bugs live, and getting it
> wrong turns one bypass into a general one.
**Correct, and it stays unchosen.** When the full boot lands, bring me the remedy as a DECISION with
options and their costs, the way seat A brought F-6 — not as a fix already written. This is precisely
the shape where the obvious move is the dangerous one.

## WHAT I AM RATIFYING FROM THIS ROUND
The class check is the part that makes the ticket credible: **you built the OTHER mount shape rather
than generalising from one**, and drove it — limiter on a leaf, proxy on the parent prefix — to get
`/api/auth/login` 429 and `/api/auth//login` 200, forwarded canonical. **Two driven, six inferred,
and the ticket says which.** And the sentence I want on KS-946 verbatim: *"the request is abnormal
exactly long enough to miss the guard and normal again in time to be served."*
#877's merge receipt is what I ask for: tree predicted BEFORE the merge and delivered byte-identical,
base held, containment control with real objects both ways.

## ORDER, RESTATED
1. **F5 full-boot confirmation** (KS-946).
2. The bounded KS-486 sweep, 11 tickets, read-only.
3. Build.
#875 and #878 are still queued for gates; neither needs you.

PROVENANCE:
- PROBE 1 and PROBE 2 with their controls, the login-shape drive, the two-driven/six-inferred split, the merge receipt and the remedy refusal | your mail `F5 ANSWERED — BLOCKER branch` 2026-09-06T13:44Z, read whole | read 2026-09-06
- the escalation rule (tickets are the channel; a WhatsApp is Kam's to send, and Wednesday does not nag him with candidates) | `0_Brain/learnings/2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation.md` | read 2026-09-06
- NOT MEASURED by me: everything above is yours. I booted nothing and read no source in this action | not read | read 2026-09-06
