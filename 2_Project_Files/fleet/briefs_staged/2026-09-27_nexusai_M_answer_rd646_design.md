# BLUF: RD-646/647 design ACCEPTED as within Kam's C-179 "fail closed". "Closed" means REQUESTS are refused. Booting while refusing them keeps that, and removes a crash loop. One condition is load-bearing, because the design changes what a boot with Redis down SERVES.

At main, a boot with Redis down serves NOTHING: the process exits before /api/live answers (your red log). With your design the process stays up, so every route NOT behind a limiter is now served while Redis is down. That is the part "fail closed" has to cover, and it is unmeasured.

Conditions for the READY:
1. **CENSUS CELL (required):** with Redis configured and down at boot, drive every /api route (enumerated from the source, not listed by hand, with a positive control that a known route is found). Each one must answer 503 (refused) or appear in an explicit, named ALLOW LIST: /api/live, plus anything else you can justify, one line each. A route that serves data while Redis is down and is not on the list is a STOP: mail me. Do the same for the mid-run shape.
2. **The READY states the behaviour change in plain words, first:** "at main a boot with Redis down exits; with this change it stays up and refuses rate-limited requests with 503". I will tell Kam, because C-179 is his ruling.
3. Keep your control for no Redis configured (Marketplace), and the recovery cell (Redis returns and requests are served with no restart).
4. Tier 1 (security posture on an outage). It goes into a gate batch with the next lane-1 READYs.

Queue order as you have it is fine: RD-618 F-A2..F-A5 cells, RD-650, RD-657 while the hold waits. RD-705 and RD-594 are in gates 5a and 5b; 5a is running now.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 10:31
