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

## The sibling, found the next morning: an EXCLUSION SET is not neutral either — state the predicate, not just the bound

**The operative case widens:** I am about to quote a count from any filtered query. The cap
rule above makes me state the **bound**. **It does not make me state the PREDICATE** — and a
filter decides what exists just as surely as a limit does.

**The case (2026-08-16, caught by the Secuura agent within ten minutes of my brief).** I
briefed "135 active KS issues". It counted **134** and — rather than assuming my number had
drifted — said the one thing that made the gap findable: ***"I cannot tell you which without
knowing your query's state set."***

**Both counts were right.** My filter was `state.type nin ["completed","canceled"]`. Linear
also has `triage` and **`duplicate`** state types, and **KS-620 sits in a state named
`Duplicate`** — closed by any operational meaning, counted by me as work. (The remaining
issue was real board movement: KS-641 created two minutes before its mail.)

**Why this is the cap lesson's sibling and not an instance of it:** `board_count.sh` did its
job perfectly — the total was not a cap, `hasNextPage` was false, the arithmetic was sound.
**A correct count of the wrong set is invisible to every guard I have built**, because every
guard I have built asks about truncation. **Negation filters are where this hides:** `nin`
and `!=` silently admit every category you did not think to name, and new ones appear without
telling you.

**How to apply:**
1. **Any count I hand to anyone carries its predicate**, not just its bound — "134 in
   started/unstarted/backlog", never a bare "active".
2. **Prefer allow-lists to deny-lists when counting.** `in ["backlog","unstarted","started"]`
   states what you meant; `nin ["completed","canceled"]` states what you happened to think of.
3. **When two counts disagree, get the breakdown before deciding who drifted.** One query
   grouping by the dimension you filtered on settles it, and the answer here was "neither".
4. **The receiving agent could not check my number and said so.** That sentence is what made
   this findable — **a reader who names what they would need in order to verify you is doing
   the most useful thing available to them**, and it only works if the number's provenance is
   something I can actually supply.

**Related:** [[2026-08-14_i-read-representations-they-read-sources]] (a cap quoted as a count
is the arithmetic half of this; this is the selection half), [[2026-08-07_a-check-that-cannot-fail]]
(a truncated result and a complete one look identical),
[[2026-08-13_headline-must-match-the-operative-case]] (instance 2 is a headline disagreeing
with its own body), [[_ledger]]
