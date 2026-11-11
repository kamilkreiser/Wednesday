GATE B1480-2-gates: PROVISIONAL (round 3 running since 09:22 AEDT 2026-11-11; earlier rounds died at 05:41 and ~09:15) @ ef0ff56 on main 8cb989f

Round 3 status 10:33: ALIVE. First verify (ef0ff56, 09:29) stalled machine-wide 09:40-10:28 (no log line for 48 min; the landing seat's lock waiter was frozen the same window) and was killed to free the lock; origin main moved 1c6bd64 -> 8cb989f, merged trees rebuilt on 8cb989f. Probes on the new merged trees + 4 verifies queued FIFO behind the landing seat.

Round 3 interim 09:31: probe3 (p3-*.probe.json) re-derived red-first: at f913fef and 2a584f7 a viewer bypasses the sustainability config gate on 7 routed case forms + 4 raw request lines and the write PERSISTS (stored region VIEWER-125); at ef0ff56, ccb7aa4 and both merged with main 1c6bd64: 0 of 220 viewer forms pass, stored region unchanged, administrator control writes persist. Four full verifies running one by one under the jest lock. Text below this line is the dead round 2's interim, kept for the record.

Interim (07:30): probe at old heads f913fef/2a584f7 reproduces the case bypass (6 routed forms + 3 raw forms, viewer write persisted); new head ef0ff56 blocks all 260 gated viewer forms. Colmap probe, red-first plant and four verifies pending (jest lock FIFO behind another seat).
