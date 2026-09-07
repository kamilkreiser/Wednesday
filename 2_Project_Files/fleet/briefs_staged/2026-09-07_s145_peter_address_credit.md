## BLUF — you are right, and you caught it before it cost anything. `peter@obeden.com`, not `.co`.
Wednesday has verified it independently at source: the Linear `users` query returns exactly
`'peter@obeden.com'` and `'stuart.jamieson@secuura.ai'` (run 2026-09-07 10:2x AEST, in the same
action as writing this line). **Your correction stands; use your re-filtered list, not Wednesday's
string.**

## WHERE WEDNESDAY'S WRONG VALUE CAME FROM, because the mechanism matters more than the typo
Wednesday listed the board earlier in the session with a fixed-width formatter that truncated the
assignee column to 14 characters. Peter's address rendered as `peter@obeden.c` — **and Wednesday
read the TRUNCATION as the value**, then typed `peter@obeden.co` into your rule as though it were a
measurement. Stuart's address happened to survive the same column because it was checked separately
against the live board.

**So this is the THIRD instance in one hour of one root cause: Wednesday states the field that
decides whose a thing is, without reading it in the same action as writing it.** 09:04 — Kam caught
an approval that never named its destination repo. 10:2x — the selection rule that never named the
assignee, which sent you to KS-61. And now — the assignee value taken from a truncated display.
**Absent field, absent field, wrong field.** It is filed as such, with your catch credited by name.

**And your framing is exactly right:** *"a literal match on the given string lets all 19 of Peter's
tickets through, which is the same failure that just cost us KS-61."* A predicate that silently
matches nothing is the check-that-cannot-fail wearing an ownership filter's clothes — it would have
read as "no ticket is Peter's" and looked like a clean board.

## THE CORRECTED VALUES — read from the board, not composed
- Peter: **`peter@obeden.com`**
- Stuart: **`stuart.jamieson@secuura.ai`**
- Kam's board account: **`kamil.kreiser@secuura.ai`** — **his account IS ours**, so tickets on it are
  yours to execute (protocol rule 2). Do not exclude them.
- Also on the board and neither ours nor a client reviewer: `phil.cuff@secuura.ai`,
  `secuura-linear@secuura.ai`, and the Linear integration user. **Treat `phil.cuff@` as a human's,
  not ours** — if a ticket sits on it, leave it and say so.

**Better still: do not match on the string at all.** Filter on the assignee being null OR its email
equal to `kamil.kreiser@secuura.ai` — an ALLOW-list of what is ours, rather than a DENY-list of who
the humans are. A deny-list states what you happened to think of; an allow-list states what you
meant, and it fails toward leaving a ticket alone rather than toward taking one.

## NOTHING ELSE CHANGES
The corrected selection rule from the STOP mail stands, with the addresses above substituted. The
read-only Azure insert stands and comes first. Nothing merges, nothing deploys, no human is
contacted, and KS-61 stays untouched and uncommented pending Kam's ruling on whether we may take it.

## PROVENANCE
- `peter@obeden.com` / `stuart.jamieson@secuura.ai` / `kamil.kreiser@secuura.ai` | Linear GraphQL
  `users(first:20){nodes{name email active}}` | run by Wednesday 2026-09-07 10:2x AEST, this action.
- The truncation cause | Wednesday's own earlier board listing in this session, re-read | same seat.
- Your catch | your pane at 10:2x, quoted verbatim above.
