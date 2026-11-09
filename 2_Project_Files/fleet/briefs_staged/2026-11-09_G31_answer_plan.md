Seat G 31st

BLUF: PLAN CONFIRMED: GO as written, ONE PR, Refs KS-1208 and KS-619, both of your asks granted with the conditions below. Your statusline by Wednesday's zoom at 15:0x AEDT: 25%.

(1) E1/E2 fixture edits in auth.test.ts: GRANTED. Giving an existing fixture what the new guard demands (E1 gets tenantId 't1'; E2 becomes SUPER_ADMIN so it pins the exemption) is the right repair: fix the fixture, never the guard. Labels and results kept. Declare both edits in the READY and say that the full gateway suite, not your static read, is what proves no other tenantless token exists.
(2) 401 on OPTIONAL mounts too: GRANTED. Kam's ruling (card secuura-backlog-31-decisions-1109 = a, row A3) is "a token with no user id or role gets 401", without a mount carve-out, and your KS-1198 reasoning holds (a pass-through forwards the verified Bearer upstream). Conditions: the PR body states it plainly as a behaviour change ("a request on a public route that presents such a token now gets 401 instead of being served as anonymous; a request with no token is unchanged"), a cell pins each half (token-without-claims on an optional mount -> 401; no token on the same mount -> served), and the READY lists it first so the gate examines it.

Your KS-619 finding (the title's x-tenant-id fall-through was never live; the default was set first since 29033ce47, and the edge strips inbound x-tenant-*) goes in the PR body and in your ticket comment on KS-619 as a facts-only correction, with the commit and line cited.
C14 not reddened by any mutant of yours: say so, as you planned. G2 uses validateHeaderValue, the proxy's own check: good choice, name it in the body.

Ends at READY FOR GATE, tier 1 (Opus gate). Census again before the push. Pace: wrap at about 70%.
