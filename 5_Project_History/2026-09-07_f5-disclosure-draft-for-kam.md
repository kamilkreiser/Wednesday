# F5 disclosure — draft message for Kam to send
**Prepared 2026-09-07 06:5x AEST on Kam's ruling `secuura-f5-disclosure-timing` => withfix
("Tell them WITH the fix, later today") and his note on `secuura-f5-login-limiter-bypass`
("and when ready, prepare the message to them").**

## STATUS — this is a DRAFT and it is NOT sendable yet
The fix exists: **PR #884 @ `f3a037978`**, built this morning, at READY. **It has not been gated
and it has not merged.** The message below deliberately says "fix is up and under test" rather
than "fixed", and that wording is only honest until the gate reports. **Two things must land
before Kam sends anything:**
1. the tier-1 QA gate on #884 reports (running now), and
2. Kam's word on the merge.
If the gate comes back NO GO the message changes, so **holding it is the right state, not a delay.**
Kam asked for it prepared; it is prepared, and this note says plainly what it waits on.

## WHAT PETER AND STUART ARE ACTUALLY BEING TOLD
- An extra slash in the URL (`/api/auth//login`) skipped the rate limiter entirely.
- It affected **all eight protected auth mounts**, and **six of those need no login at all**.
- Confirmed on a real running gateway, locally booted — **never on the demo**.
- **Whether the demo is affected is still UNMEASURED.** Kam authorised one read-only probe at 06:43;
  it has not run yet. **The message must not claim either way until it has.**
- The fix normalises the path once at the gateway edge, above every guard, so the same trick is
  closed for the scope gates and the GDPR routes too — not just the limiters.

---

## DRAFT 1 — WhatsApp to Peter (Kam sends; short by design, the detail is on the ticket)

> Morning Peter. One security item worth your eyes today, and the fix is already up.
>
> We found that adding an extra slash to an auth URL — `/api/auth//login` — skipped the rate
> limiter completely. It affects all eight protected auth routes and six of them are
> unauthenticated. Confirmed on a real running gateway, not the demo, and the demo was never
> touched.
>
> The fix is PR #884: it normalises the path once at the gateway edge, above every guard, so it
> closes the scope gates and the GDPR routes at the same time. It's under test now.
>
> Full detail, the reproduction and the eight affected routes are on **KS-946**. Nothing needs
> doing from you before your normal review — I wanted you to have it before you test.

**Length: ~110 words. Kam's 2026-08-19 rule — the detail is in the ticket so the message can be
short.**

## THE TEST BLOCK — for when #884 goes to Peter for review
Per Kam's 2026-09-05 instruction (handovers are test blocks as large as one pass proves, never a
list of PRs). **The Secuura seat builds this and Wednesday ratifies it; it is NOT part of the
WhatsApp above** — it goes on the review-stream parent when #884 is gated:
- **Stream parent:** the auth/gateway review stream.
- **PRs in the block:** #884 (KS-858/F5) — and, if they gate clean in time, #876 (KS-930) and #882
  (KS-698), which are the other two guards on the same auth surface. **Grouping them is the point:
  one pass over the gateway auth surface proves all three.**
- **The one pass that proves it:** the repo's own DEV-PROCESS gateway/auth pass.
- **The one thing Peter does:** run that pass and review #884's routing sweep.
**Not yet assembled — #876 and #882 are both at NO GO round 1, so the block's membership is not
final. Assembling it before they gate would produce a list, which is the thing Kam has corrected
three times.**

## DRAFT 2 — Stuart: RECOMMENDATION, NOT A DRAFT
**Wednesday has NOT established whether Stuart's Platform S work touches this gateway's auth
mounts, and will not guess.** The eight affected mounts are Platform K's `/api/auth` and
`/api/users/me/mfa`.

**Recommendation: no separate message to Stuart now.** If Platform S calls Platform K's auth
endpoints, he needs one; if it does not, a security note about someone else's surface costs him a
context switch for nothing. **The cheap way to settle it:** the Secuura seat can answer "does
Platform S call any of the eight?" from the code in minutes, and Wednesday will put the answer in
front of Kam before the message goes. **Kam can of course overrule and tell him anyway** — it is
his relationship and his call.

## WHAT WEDNESDAY WILL DO WITHOUT FURTHER INSTRUCTION
1. Hold this draft until the #884 gate reports.
2. Put the demo-probe result in front of Kam the moment it lands, and amend the draft if the demo
   turns out to be affected — that would change the urgency and possibly the wording.
3. Ask the Secuura seat the Platform S question and bring the answer back.
4. **Send nothing.** External communication is Kam's signature class; Wednesday drafts, Kam sends,
   and nobody else messages Peter or Stuart.

## PROVENANCE
- The eight mounts, six unauthenticated, and the confirmation on a locally booted gateway | seat B's (s142) mail 2026-09-06T14:43:04Z, quoted not paraphrased | read 2026-09-07
- The fix's shape and that it closes the scope gates and the GDPR routes | the s143 seat's mail 2026-09-06T20:42:49Z (`//api/gdpr//erasures` 404 -> 401 measured) | read 2026-09-07
- #884 head `f3a0379787123b45e4ffdb48d9d3db78e9661726` | `git ls-remote origin` from Wednesday's own seat | measured 2026-09-07 06:4x
- Kam's rulings | `kam_rulings_today.sh`, cards `secuura-f5-disclosure-timing` => withfix and `secuura-f5-login-limiter-bypass` => wait + the "prepare the message" note | read 2026-09-07
- Whether the DEMO is affected | **UNMEASURED** — the authorised probe has not run | not read
- Whether Platform S calls any of the eight mounts | **UNMEASURED** | not read
- KS-946's current content and whether it already carries the reproduction | NOT read by Wednesday in this action | not read
