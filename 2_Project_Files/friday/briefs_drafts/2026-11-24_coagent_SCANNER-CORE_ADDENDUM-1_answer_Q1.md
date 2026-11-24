This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-24_coagent_SCANNER-CORE_brief.md`. Seat SCANNER-CORE only.

# SCANNER-CORE ADDENDUM 1: the answer to Q1

You are right, and thank you for stopping on it: with the bound at 64 KiB, property 4's third clause cannot be tested as written and its red control would be correct code. The fault is in the brief, which carried a clause written for a larger bound. That clause and that red control, AS WORDED in the brief, are WITHDRAWN by name: "a secret placed after 64 KiB and before the bound is flagged" and "Red `prefix_window` (only the first 64 KiB scanned)".

**RULED BY FRIDAY: your option (i).**
- `MAX_SCAN_BYTES` stays 64 KiB (FR-3 = (a) governs).
- Property 4's third clause is now: a secret that ENDS exactly at the bound (the last bytes of a text of `MAX_SCAN_BYTES`), and a secret that begins just after the first half of such a text, are both flagged.
- Red `prefix_window` is now: only a prefix SHORTER than the bound is scanned (the first 32 KiB, cut back to a character boundary); it must turn that test red on its own evidence text.
- Add one more position to the same test, since the point is "no part of the text is skipped": a secret that STRADDLES the half-way point (it begins before 32 KiB and ends after it) is flagged. The red above must miss at least the two later positions; say in STATUS which positions it misses.

Your count of 10 for `share_flagged` (the brief said 11) is noted; the conclusion stands. Nothing else changes. Carry on; the last line of STATUS returns to `IN PROGRESS`.
