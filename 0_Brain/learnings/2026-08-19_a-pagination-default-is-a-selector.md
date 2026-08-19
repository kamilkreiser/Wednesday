---
date: 2026-08-19
type: correction
source: "Two independent hits in one day: my KS-256 read (comments(last:2/6) returned June/July comments, nearly missed Peter's 08-18 one) and s48's gate verification (comments(last:3) hid Stuart's 00:54/00:58Z comments — it was one step from reporting my gate claims unverifiable and blocking a correctly-authorised spend)."
status: live
---

# A pagination argument is a SELECTOR — `last:N` on Linear comments returns the OLDEST, and "newest" is an assumption you typed

**The operative case:** I am about to read "the newest" items from any paginated
API — comments, messages, events, commits — using a `last:`, `first:`, `limit:`
or default ordering I did not verify. **The pagination argument silently selects
WHICH slice I see, and the wrong slice looks exactly like a complete answer.**
Linear's comments connection is newest-first, so `last:N` takes the tail of a
reversed list — the N OLDEST comments, presented without any marker that newer
ones exist.

**Why it is dangerous in a way a cap is not:** `board_count.sh` guards against a
cap masquerading as a total. This is the sibling failure — not truncation but
**mis-selection**: the result is well-formed, plausibly sized, and from the right
object, so nothing prompts a second look. Both hits today were on AUTHORITY
reads (a client's newest instruction; a spend gate's confirmation) — exactly
where the newest item is the one that matters.

**The rule:**
1. On Linear: `comments(first:50)` (or paginate) and sort client-side; never
   `last:N` for "newest". Same for any connection whose sort I have not read
   from the docs or proven with a probe.
2. Before trusting any "newest N" read, prove the selector: does the slice
   contain an item I independently know is recent (a timestamp I just caused,
   a message I just sent)? If the known-recent item is absent, the selector is
   wrong, not the world.
3. Carry into briefs: any agent verifying ticket state reads comments with
   `first:` + client-side sort. (Both s47's brief-answer and s48's SCORE carry
   it; this file makes it standing.)

**Family:** [[2026-08-06_selector-discipline-in-ui-verification]] (suspect my own
selector before the world) · [[2026-08-15_a-cap-is-never-neutral]] (the sibling:
there the bound, here the direction) · [[2026-08-07_a-check-that-cannot-fail]]
(a read that cannot show the newest item cannot verify a newest-item claim).
