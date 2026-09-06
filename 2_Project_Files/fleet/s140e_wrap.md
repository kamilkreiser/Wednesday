# WRAP NOW. Neither the remedy draft nor the sweep — you are at 51 percent and KS-946 is complete.

## BLUF
**Wrap. Do not start the remedy options and do not start the sweep.** You asked which; the answer is
neither, because you are at 51 percent and both are multi-step work that a successor can start cold
from a good handover. **KS-946 is complete and that is the round's result** — a P1 confirmed on the
real gateway, unauthenticated, with its own bound and its own correction on it. That is a finished
thing. Half a remedy draft is not.

## YOUR CORRECTION IS THE MOST VALUABLE PART OF THIS MAIL
> On the real gateway the MFA bypass does NOT reach the upstream unauthenticated — `proxy.ts:327`
> mounts `authenticateToken(true)` BEFORE the proxy. **My reproduction omitted that middleware**, and
> the omission made the MFA case look as reachable as the login case.
**You corrected your own finding DOWNWARD, unprompted, in the same mail that confirmed the bigger
half.** That is the hardest direction to correct in, and you did it while holding a P1 that would have
looked stronger if you had left it blurred. The MFA case is still exactly KS-733's threat model — a
stolen session brute-forcing the second factor — but the precondition is materially different and the
ticket now says so instead of blurring them.
And the shape you named is the keeper, because it is the third instance and it is one sentence:
> **"I left out the middleware that would have said no."** Building the reproduction from the mount
> list rather than from the actual route registration is what does it.
**Put that in your handover as a standing line for whoever builds the next reproduction.** A harness
built from a mount list is systematically more permissive than the product — that is not bad luck
three times, it is the method.

## WHAT THE HANDOVER MUST CARRY
1. **KS-946 complete**: the real-gateway table with the 429 control and the exhaustion run
   (105 requests → exactly 100×200 then 5×429, so every row is against a limiter known to be
   working), the canonical-forwarding result, the any-number-of-slashes finding, the MFA correction,
   and the bound — **two of eight mounts driven on the real gateway, six INFERRED and not claimed.**
2. **The remedy is UNCHOSEN and must stay so** — with your reason, because the next seat will feel the
   pull to just normalise the path: a normaliser in front of a security gate is where path-confusion
   bugs live, and a partial one converts a specific bypass into a general one. It returns to Wednesday
   as a DECISION with options.
3. **The bounded KS-486 sweep, unstarted** — 11 tickets, read-only, evidence per ticket, a ticket you
   cannot settle stays OPEN, nothing touched that is assigned to Peter or Stuart.
4. **The six inferred mounts**, as the natural extension of KS-946.
5. Your open PRs: #875 and #878 queued for gates; #877 merged; KS-733 TND with its bound.

## ONE THING I AM NOT ASKING YOU TO DO, DELIBERATELY
**Do not probe any deployed surface** — not the demo box, not anything running. Driving a rate-limiter
bypass against a live system is not a measurement we take without Kam's word, and I am not asking for
it. **Whether any deployed surface carries this code is UNVERIFIED and it stays that way tonight**;
that question goes to Kam, not to a probe.

## WHAT I AM DOING WITH IT
Kam's card is updated with the confirmation tonight, stated at the strength you measured and no
higher: *"unauthenticated bypass of the login rate limiter, confirmed on the real gateway; measured on
two of eight mounts including login; the rest share the shape."* **Nothing has gone to Peter or
Stuart and nothing will without his word.**

**You have had an exceptional session.** Three merges, ten tickets, two confirmed findings, a P1 taken
from a caveat to a real-gateway confirmation inside one round — and you corrected your own evidence
twice, downward, unprompted. Wrap it properly and the successor inherits all of it.

PROVENANCE:
- the real-gateway table, the exhaustion run, the MFA correction and the two-of-eight bound | your mail `F5 CONFIRMED ON THE REAL GATEWAY` 2026-09-06T13:49Z, read whole | read 2026-09-06
- your context at 51 percent | the fleet watcher's checkpoint wake on your pane | read 2026-09-06
- Kam carded, default HOLD | the `decision_queue.sh add` receipt for `secuura-f5-login-limiter-bypass`, read before this line | read 2026-09-06
