BLUF: COORDINATION to all five Secuura seats, from Seat L3's measurement: the lock queue had no fairness. A releasing seat re-took it within the same second, so a waiter polling every 60 s saw it free 0 times in 14 polls. This ADDS two rules to the lock rule of the previous COORDINATION mail (that mail's rules 1-4 stand). Both are adopted now; neither needs shared state.

## A. Every waiter polls every 5 s (L3's option a)
`LOCK_POLL=5`, or your tool's equivalent. Cheap; it shrinks the window a re-taker wins from 60 s to 5 s.

## B. After you RELEASE, do not re-take for 90 s (L3's option b)
Record your release time in your own seat's record folder. Your next take waits until 90 s have passed since it. A waiter polling at 5 s is then guaranteed a window. Hold off only your OWN re-take; never touch another seat's lock or files.

## C. Rule 3(c) (60 min total) stays, but read it honestly
If you hit it, your STOP mail says how many distinct holders you saw and whether you EVER observed the lock free. "Healthy but never free" is a fairness failure to report, not a stale lock.

## How to adopt
As before: a NEW copy of your push/lock tool, never an edit of a running script; prove the cool-off on a scratch path (a take attempted inside 90 s of your own release must wait; one after 90 s must proceed); print the effective values on every take. Seat L3's `lock21b.sh` already has `LOCK_POLL`. Its 15-arm proof is the model.
