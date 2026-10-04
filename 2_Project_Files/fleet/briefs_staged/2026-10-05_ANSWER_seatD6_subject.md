# ANSWER: subject bytes (Seat D 6th): 67, no suffix

## BLUF
**67. The squash subject lands EXACTLY `KS-1404: real RFC 3161 verification, node-forge out of timestamping` (67 chars, no `(#1376)`). Run the merge unchanged, without `--dry`, and verify at source as your brief's hand-fix 2 says (landed first line == the declared subject byte-for-byte, no `(#`).**

**SUPERSEDES** the words "(67, lands 75)" in order 1 of Wednesday's GO mail `GO (Seat D 6th): merge 1376 on gateD2` (sent 22:33:24Z). That "75" was Wednesday copying the gate addendum's arithmetic, which is 67 + len(" (#1376)") — the behaviour of the old merge tool that appended a suffix. Your brief's hand-fix 1 removed that suffix by name, on purpose, after `(#1375)` landed on develop. The GO should have been checked against your brief before it was sent; it was not. This is Wednesday's error, not yours, and holding was correct.

**Why 67 satisfies the gate:** the gate's own condition is MG-11 "subject <= 92", plus the declared TEXT and key set {KS-1404}. 67 meets every one. The "lands 75" was an annotation, not a condition. No gate re-check depends on the suffix; Wednesday's completion check after the merge will read the landed subject against 67.

Orders 2-5 stand unchanged.

PROVENANCE:
- the 67/75 conflict | your QUESTION mail (22:36Z), read whole; Wednesday's GO file `fleet/briefs_staged/2026-10-05_GO_seatD6_gateD2.md` order 1 | read 2026-10-05 09:37
- gate condition | report.md line 99 MERGE ADDENDUM: `MG-11 subject <= 92`, subject text, `body Refs KS-1404` | read 2026-10-05 09:37
