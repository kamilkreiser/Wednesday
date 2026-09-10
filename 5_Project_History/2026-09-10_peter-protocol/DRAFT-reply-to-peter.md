# DRAFT — reply to Peter. **KAM SENDS THIS. Not sent by any agent.**

Prepared 2026-09-10 20:3x on Kam's instruction (*"prepare a response to anything that needs to be
responded"*). Written in BLUR per Peter's own §4 — brief, diplomatic, kind. Nothing in it quotes
anyone's machine-local rules as policy.

---

Peter — thanks for this, it's genuinely useful and we're adopting it as our process on our side.
Two things we measured today that touch your document directly, and one question.

**1. GitHub Actions is running again.** Your §3.7 has it retired with no CI to read. It came back
some time on 9 September and nobody on our side recorded it either — we only caught it today. It
matters because its security gates currently fail on essentially every PR, so you'll see red checks
that aren't telling you anything about the change under review. Six of the seven PRs currently
waiting on you read `mergeable_state: unstable`, which is what a live-but-failing checks run
produces. We haven't touched a workflow or re-run a job — we're measuring first — but you should
know the checks you see are not yet trustworthy either way.

**2. The approval gate isn't armed.** Your protocol treats the reviewer's approval as the gate. On
the `require-pr-gates` ruleset for `develop`, required approving reviews is currently **0**, and
required status checks isn't on the ruleset at all. So nothing technical is enforcing the thing your
process depends on — it's held by convention alone right now. We're raising it to 1. Flagging it
because it's your gate, and you'd want to know it was open rather than assume it was closed.

**3. The one we'd like your steer on.** Your protocol is thorough and it's per-PR — up to six suites
in series with a full teardown and rebuild between. Run properly that's most of a day for one PR.
Kam's steer to us has been that you'd rather review three substantial things with sub-issues than
thirty separate ones. We think both hold together only if we batch PRs into review streams before
they reach you, rather than sending them one at a time. Before we reshape how we hand things over,
we'd rather ask: is that how you'd want it, or would you rather keep them separate and we simply
send you fewer, better-prepared ones?

On our side, effective immediately: every PR we open will lead with the risk map, carry unit tests
we've actually reverted to confirm they go red, include the Test Evidence block from local runs, and
keep the env-template, compose, ENVIRONMENT-VARIABLES and bicep entries in step for any new
variable. We'll also hold to the series rule for our own runs — the 2026-08-20 measurement you
included is a good argument and we'd rather not learn it again ourselves.

One honest note: several PRs currently in your queue predate all of this and won't meet it. We'd
rather tell you that than have you find it. We're working through them.

---

## Notes for Kam — NOT part of the message

- **Every factual claim above is measured, with provenance:**
  - Actions alive + gates red: card `secuura-actions-alive-but-security-gates-red`, your
    `measure-then-decide` ruling 2026-09-10 11:00.
  - `required_approving_review_count = 0` and `required_status_checks` absent: read by the Secuura
    seat from `GET /repos/Secuura/Distributed_Secuura/rules/branches/develop` **and** a second
    independent endpoint, with a discriminating control on a nonexistent branch, 2026-09-10 ~20:1x.
  - `mergeable_state: unstable` on 6 of 7: same seat, same window.
  - Peter-prefers-batched: your panel instruction 2026-09-03 10:53.
- **What I deliberately did NOT put in it:** the `akto-autoheal` root+docker.sock finding. It is
  ours, it is bounded, it is not yet ticketed, and a security finding about his own test stack is not
  something to raise in the same breath as adopting his process. **It goes to him separately, on the
  ticket, once we've written it up — your call on timing.**
- **The "several PRs won't meet it" line is deliberate.** Five of the seven waiting on him have never
  been through a gate at all. He will discover that on his first verification; better it comes from
  us. **Cut it if you'd rather I fix the queue before telling him it's untidy** — but I'd keep it.
- **Question 3 is the only thing that asks him for anything.** Cut it if you'd rather steer that
  yourself.
