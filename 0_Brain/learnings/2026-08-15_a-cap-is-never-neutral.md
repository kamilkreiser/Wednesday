---
date: 2026-08-15
type: correction
source: "Three instances in one day, from three different people: my own maxResults=30 (2026-08-14, recurring in memory today), Peter's PR-698 register losing its eighth item beneath its own headline count of seven, and RD-97's `--reverse` under a `head -12` cap truncating exactly the highest-priority blockers."
status: live
supersedes: ""
---

# A cap is never neutral — it removes whatever the SORT put last, and the sort is usually ordered by what you care about

**The operative case, so the headline matches it:** I am about to read, quote or act on a list
that was **limited** — a query `limit`/`maxResults`, a `head -n`, a page size, a "top N", a
UI's visible rows, or a prose summary that counts its own items. **Ask what the ORDER was**,
because the cap did not take a random sample. It took the tail of that order.

## Why this is a distinct lesson and not just "check your counts"

`board_count.sh` already refuses to print a total when the result equals its own limit. That
mechanism catches the **arithmetic** error — reporting a cap as a count. **It does not touch
the more dangerous half: that the dropped rows are systematically the ones the sort deprioritised.**

**A random 20% loss is noise you would probably survive. A sorted 20% loss is the specific
20% your ordering pushed to the bottom** — and orderings are almost always written to put
something meaningful at one end.

## The three instances, because the pattern only became visible across them

1. **Mine (2026-08-14).** `maxResults=30` with `ORDER BY priority DESC, updated DESC` on a
   46-issue board. I wrote "30 open issues" into a brief. **The 16 dropped were not a random
   16** — they were the lowest-priority and least-recently-updated, which was exactly the
   Testing and Release Ready half, **the half I then handed the agent as work while never
   having seen it.**
2. **A collaborator's register (2026-08-15).** A post-merge review headlined "seven items"
   over a list of **eight**. The eighth was the lowest-severity one. **I published "seven" too,
   having taken his count instead of counting** — so the cap propagated through a human, a
   summary and me without anyone dropping an item deliberately.
3. **A boot query (2026-08-15, Datasec/NexusAI).** `--reverse` sorted **Low first** under a
   `head -12` cap, so **the highest-priority blockers were precisely the ones truncated away.**
   The boot appeared to work perfectly and showed the session the least important twelve items
   it had.

**Three different mechanisms — an API limit, a prose headline, a shell pipeline — one shape.**

## How to apply

1. **Whenever a list is capped, state the ORDER alongside the count.** "Top 12 by priority
   ascending" is a different fact from "12 issues", and only the first lets a reader see what
   is missing.
2. **If the cap and the sort point the same way, the cap is a filter.** `head` after a
   `--reverse` is not a display convenience; it is a policy about which items exist.
3. **Prefer a total plus a sample over a capped list** — get the count unbounded, then take
   the top N deliberately and say so.
4. **Check the direction of any sort you did not write.** `--reverse`, `ORDER BY … ASC`, and
   "oldest first" defaults are where this hides, because the cap looks reasonable and the sort
   looks incidental.
5. **A prose list that counts itself is a capped list too** — the count and the items are two
   artefacts that can disagree, and the count is the one people quote. **Count the items.**

**Related:** [[2026-08-14_i-read-representations-they-read-sources]] (a cap quoted as a count
is the arithmetic half of this; this is the selection half), [[2026-08-07_a-check-that-cannot-fail]]
(a truncated result and a complete one look identical),
[[2026-08-13_headline-must-match-the-operative-case]] (instance 2 is a headline disagreeing
with its own body), [[_ledger]]
