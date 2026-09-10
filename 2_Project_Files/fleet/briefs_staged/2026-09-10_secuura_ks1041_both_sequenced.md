# KS-1041 — Kam ruled the FIX SHAPE: both, in sequence. Route first, header trust second.

## THE RULING, VERBATIM AND IN ORDER

Kam, dashboard panel, 2026-09-10 10:32:49 (+10:00), card
`secuura-ks1041-fix-shape-demo-exposed`, option `both-sequenced`:

> "Both, in order: drop the /originate/ nginx route FIRST, then fix the header
> trust behind the QA gate"

This discharges the second half of his 09:18 `probe-then-rule` ruling on
`secuura-originate-unauthenticated-cross-tenant-billing`. The probe ran; this is
the fix he kept for himself, and he has now given it.

**The sequence is the ruling, not a suggestion.** Step 1 ships on its own and
closes the exposure. Step 2 does not begin until Step 1 is verified closed on the
demo box. Do not combine them into one PR.

## STEP 1 — DROP THE /originate/ ROUTE FROM NGINX (do this first, alone)

Remove the `location /originate/` block so the route is not reachable from
outside. It exists in all three configs; Kam's ruling is about closing the
exposure, so the demo config is the one that closes it today, and the other two
are changed in the same PR for consistency of the shape.

Verification required before you call Step 1 done, and it is a pair:
- The credential-free GET that returned HTTP 200 must return 404 (or connection
  refused at that path) on the demo host after the change.
- A positive reachability control on the same host in the same run — an
  unrelated path that still answers 200 — so a total outage cannot be mistaken
  for a closed route. A false absence reads exactly like a true fix.

## STEP 2 — HEADER TRUST, BEHIND THE QA GATE (only after Step 1 is verified)

Stop `originate` treating a client-supplied `x-user-role` / `x-tenant-id` as an
identity. The route's own comment states the premise this breaks — that
originate is internal-only ingress — so make the premise true rather than
assumed: the gateway stamps what it vouches for, and originate trusts only that.

**The named risk, carried from the card so you do not rediscover it:** the
gateway LEGITIMATELY sets those headers and originate reads them in three
places. A blanket strip broke `x-tenant-override` silently for two weeks once
before. This is tier-1 QA under the gate.

## KS-741 IS STILL HELD

It shares the root cause. It unblocks when Step 2 lands, not when Step 1 does —
fixing it alone would leave the larger hole open while reading as closed.

## SCOPE THAT IS NOT YOURS

Disclosure to Peter or Stuart is Kam's signature class. Nobody outside Kam,
Wednesday and this seat is told anything about this exposure. Do not put the
mechanism in a public PR title or a ticket comment that Stuart's board renders.

## RULED BY KAM, NOT YET IN AN ARTEFACT

These are Kam rulings on this project that carry no delivered mark. They ride
here because a ruling that lives only in a card is a ruling the next reader never
meets. The one that bears on today's work is the first:

- `secuura-agent-github-identity` — ruled `identity` 2026-08-26 17:12: the agent
  gets its OWN GitHub identity, because GitHub refuses to let `kksecura` approve
  `kksecura`'s own PRs. **Never actioned.** It blocked PR #914 on 2026-09-09
  (`secuura-merge-914-without-reviewer-approval` => `you-approve`) and it blocked
  PR #934 again this morning. Third occurrence of one unactioned ruling.
- `secuura-merge-914-without-reviewer-approval` — ruled `you-approve` 2026-09-09.
- `secuura-originate-unauthenticated-cross-tenant-billing` — ruled
  `probe-then-rule` 2026-09-10 09:18; discharged by this brief.
- A further 27 ruled Secuura cards carry no delivered mark. Wednesday holds that
  list and is working it; it is named here so this seat knows the backlog is
  real and not a clean slate.

## QUEUE

- KS-1041 — the two steps above, in order.
- KS-741 — HELD behind Step 2.

PROVENANCE:
- KS-1041 fix shape ruled `both-sequenced` by Kam | /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/decisions.json card secuura-ks1041-fix-shape-demo-exposed, and his panel message 10:32:49 | read 2026-09-10
- Demo box returns HTTP 200 with no credential on GET /originate/api/metering/usage, control with no headers returns 401 | Secuura seat s166's probe, recorded in the BLUF of card secuura-ks1041-fix-shape-demo-exposed | read 2026-09-10
- Production is not exposed — hostname does not resolve, az vm list under Founders Hub shows only demo + kintsugi dev | same card BLUF, measured by seat s166 | read 2026-09-10
- location /originate/ exists in nginx-demo.conf:441, nginx.conf:208, nginx-production.conf:369 | card secuura-originate-unauthenticated-cross-tenant-billing BLUF, verified read-only by Wednesday | read 2026-09-10
- Gateway legitimately sets those headers, originate reads them in three places, a blanket strip broke x-tenant-override for two weeks once | card secuura-originate-unauthenticated-cross-tenant-billing, option fix-both-shapes detail | read 2026-09-10
- KS-741 is held behind KS-1041 sharing the root cause | card secuura-ks1041-fix-shape-demo-exposed default_action | read 2026-09-10
- secuura-agent-github-identity ruled `identity` 2026-08-26, still undelivered | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura | read 2026-09-10
- PR #934 approval refused by GitHub with "Can not approve your own pull request", author kksecura | Wednesday ran gh pr review 934 --approve against Secuura/Distributed_Secuura | read 2026-09-10
- 30 ruled Secuura cards carry no delivered mark | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura, counted from its output | read 2026-09-10

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-10 10:47
