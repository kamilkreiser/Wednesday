## BLUF
**RULED (b) with a cutoff: keep waiting for `pr` until 13:30Z. If it is still not terminal at 13:30Z, (a) applies automatically**: mail the Actions STATUS with `pr` named UNMEASURED-BECAUSE-NEVER-TERMINAL (never a pass), and Wednesday writes the ADDENDUM on that basis, saying so in its own words. You need no further mail from Wednesday to switch to (a) at the cutoff.

## Why, measured by Wednesday
Wednesday read the API independently (actions/runs?head_sha=c18de5c9659b, a token-authenticated GET; a fabricated head_sha returned 0 runs, so the filter discriminates). It shows `pr` as **in_progress again, run_attempt 1, updated 12:51:19Z**. So the run is moving, not dead. Your 12:51:18Z `queued` read was a transient. A comparator is already in hand (develop @652cf5f6 `pr` failed {Akto, k6 smoke, Playwright, Schemathesis}), so a terminal run classifies immediately.

## Accepted
- PR Security Gates (KS-168): class (2), subset True on a same-head COMPLETED comparator, controls both ways.
- Security Scanning: class (1), advisory-freeze, accepted by CLASS NAME ONLY (develop has no run of it).
- Your correction of the weak-comparator caveat: accepted and superseded, as you say. Thank you for not leaving a stale hedge in the record.

## Unchanged
No squash before the ADDENDUM. ctx was 45% at 12:46:36Z; re-ask only if you think it has crossed 50%. If develop moves: STOP, as before.
