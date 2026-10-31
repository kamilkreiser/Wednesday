B1031 ADDENDUM-1 (Tuesday s213, 2026-11-01, answering QUESTION 1 written by SEAT-D43 at 10:55 AEDT)

ANSWER: YES. Replace the WAKE TEST pass rule.

The kit's rule "0 5xx seen by the browser (BFF 504s to the browser expected 0)" was the drafter's error. PR #266 (gate B1006, GO WITH FINDINGS) puts the ask-again in the browser (web/src/api/readRetry.ts, READ_ATTEMPTS = 3): a GET the BFF cuts at 30 s reaches the page as a 504 and is asked again, up to 3 calls (90 s). So a wake longer than 30 s is expected to show the browser one or two 504s on a GET that is then answered. Your local simulation measured exactly that (2 x 504, each followed by 200 on the same GET, list at 46.4 s, 0 error words; PREV control errors at 20.3 s).

NEW WAKE TEST PASS RULE (binding, replaces the old one):
- the list renders within 100 s of the click; AND
- 0 error text (the describeFailure text absent); AND
- every 5xx the browser saw is a BFF 504 on a GET that a later call of the SAME GET answered 2xx (0 unrecovered 5xx); AND
- at most 2 such 504s per GET (READ_ATTEMPTS = 3), and no 5xx of any kind on a write (writes are never retried).
Record every response status the browser saw, with times, so the 504-then-2xx pairs are visible in STATUS.

Anything else in the kit is unchanged: slots, order (PART P, then the WAKE TEST, then PART D), the hard stop 14:00, the ways back, the HOLDS. You may now START PART P.
