# Drafter notes, test-stack brief, 2026-11-15

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatT_test_stack.md

## What Wednesday must decide or check before launching
1. Floor is red right now: load1 7.03 (guard is under 7), swap 1.77 of 3.0 GB already used, about 84 MB free pages. The seat is told not to `up` until green; launching it now just spends tokens waiting.
2. Docker Desktop VM is 7.748 GiB. Compose limits sum 20.2 GB (all profiles), reservations 9.2 GB. The stack may not fit. Raising the VM memory is Kam's machine setting; the brief makes it a QUESTION. Consider asking Kam first.
3. No secuura-* image exists: first bring-up is a full build of all services (time and disk unknown).
4. Commission names TEST_ADMIN_EMAIL/PASSWORD; the compose stack seeds admin@secuura.com from ADMIN_USER_PASSWORD and harnesses read BOOTSTRAP_ADMIN_PASSWORD. TEST_ADMIN_* are only Schemathesis's .env names. Brief explains this.
5. Peter's CI also runs run.py integration, spec-auth, auth-rate-limited, test:migrations and Playwright static+unit; commission did not list them. Added as legs 8-11. `integration` may touch a chain: brief makes that a QUESTION if it would leave localhost/Yaci.
6. Slot choice left to the seat (highest free of 1-4; max is 4).
7. Lane T chosen: routed in inbox_routing.conf:46, not live; ordinal T 25th (0 hits), control T 24th (1 hit).

## Not measured by me (read-only, no docker start)
Develop SHA, durations on this Mac, docker system df (hung 120 s), which compose services are in the default profile, Akto's own container count.

## Slips
Two Bash calls were refused by the zsh hook for `=====` separators; re-run with `----`.
