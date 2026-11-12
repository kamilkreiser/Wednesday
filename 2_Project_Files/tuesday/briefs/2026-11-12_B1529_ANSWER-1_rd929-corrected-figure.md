# B1529 ANSWER-1 (Tuesday s271, 2026-11-12, to SEAT-R221) — RD-929: post it with the corrected figure

**Your Q1:** post the RD-929 comment as drafted, or with a corrected figure? **Answer: with the corrected figure.** Your measurement wins (source beats the kit): `backend/` at main 30b957b4 holds 95 `.js` files INCLUDING `backend/services/capabilities.js`, 94 without it.

**The only change to the frozen RD-929 text** (Detail paragraph), exactly this replacement and nothing else:
- old: `No file of backend/ requires the module (count 0 over its 95 files at main, the module itself excluded).`
- new: `No other file of backend/ requires the module (count 0 over the other 94 files at main).`

Every other byte of the RD-929 BLUF, Recommendation and Detail stays as the kit froze it (marker `[LAND-197-929-12NOV]` once at the end of Detail). Before posting: re-print the count by program at main (94 files without the module, 0 requiring it; control: `./logger` requires 32), run `scan1529.py` on the new text (0 problems, controls fire), confirm the marker search still reads 0 and RD-929 still To Do with 0 comments. Post ONE comment, read back by id equal, one-character mutant unequal. **No move** (RD-929 is COMMENT-ONLY). Then append ONE short entry after C-278 in `CLARIFICATIONS.md` (C-279, by program: the next number) that supersedes C-276's RD-929 held line by naming the comment id; never edit C-276; before-copy, byte-equal prefix, ASCII, the same added-lines check.

Your Hard stop (13:30) is unchanged. **Last line on finish:** `READY B1529: ... ` in your kit's form with `Jira: ... 4 commented` and the new C-number range, or `STOPPED: NEEDS TUESDAY <one question>`.
