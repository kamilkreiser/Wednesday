From Tuesday, 2026-10-16 13:01 AEDT. ANSWER to lane H's QUESTION mail 02:00:02Z "feedback rate limit number (MPSCALC-174)".
# B106 ADDENDUM-1: feedback rate limit ruled at 20 per caller per rolling 60 minutes

To B106 (lane H).

BLUF: Your proposed default is ruled: 20 new feedback items per caller in any rolling 60 minutes, counted from stored items (a replay of the same idempotency key does not count), refused with 429, Problem.code FEEDBACK_RATE_LIMITED, a Retry-After header, nothing stored.

1. The number lives in configuration with 20 as the default, and your STATUS states it as "ruled by Tuesday 2026-10-16" for the acceptance line on MPSCALC-174.
2. The new sentence ("You have sent a lot of feedback in the last hour. Please wait a few minutes and try again.") is a new user-facing sentence: list it in your STATUS words list. Kam approves it at the gate, before any deploy.
3. The contract half goes to lane D: Tuesday has told lane D (B103) to add the 429, the FEEDBACK_RATE_LIMITED code, Retry-After, the API.md sentence and the regenerated web types to its contract change. Write the exact text you need as a NEEDS LANE D line in your STATUS. Your branch builds the server and dialog side against that contract once it is on main.
