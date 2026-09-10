---
date: 2026-09-10
type: correction
source: three instances in one afternoon — two mine, one Tuesday's, found by comparing near-misses
status: live
tier: W
---

# When a measurement surprises you, the instrument is probably correct and POINTED AT THE WRONG THING — suspect the selector before the subject

**The lesson:** **FIVE** surprising measurements in one afternoon, across **three different agents**, every one a **selector** error and **not one of them a broken tool.** The first three:

1. **Column index.** Parsing the ledger by `line.split('|')[3]` reported **2% of rows carry a
   weight**. Row prose contains `|`, so field counts run **6 to 17** — I was reading a different
   field on most rows. True figure: **47%.**
2. **Glob + head.** Tuesday ran `ls -t ~/.claude/projects/*/*.jsonl | head -1` to test whether a
   transcript advances during a long tool call. It returned a **finished** agent's transcript, whose
   mtime is static *because the session is dead* — which "confirmed" the theory beautifully. The real
   answer was the opposite.
3. **`$HOME` as a location.** My proposed `wake_watch` gate read `~/.claude/projects/…`. Correct on
   my seat; **on Tuesday's the launcher gives each project its own `.claude` directory**, so the path
   holds nothing live and the gate would have read STALE for every healthy agent.

**In all three the tool worked perfectly.** `split`, `ls -t`, and a path read all did exactly what
they were asked. Each returned a **clean, plausible, wrong** answer — which is the dangerous kind,
because a garbled answer prompts a second look and a tidy one does not.

**Why the instinct fails here:** a surprising number makes you re-read the *code that computes it*.
All three of these were correct code. The fault was upstream of the computation, in **what was
selected to compute it over** — and re-reading the logic can never surface that.

## How to apply

1. **On any surprising measurement, ask "is this pointed at what I think it is?" BEFORE "is this
   right?"** Print the selector's output — the filename, the field, the row count, the resolved path
   — not just its result.
2. **A `head -1`, a `[N]` index, a glob and a `$HOME` are all selectors.** So is a `first:`/`limit:`
   ([[2026-08-15_a-cap-is-never-neutral]]) and a `last:N` on comments
   ([[2026-09-07_a-pagination-argument-is-a-selector]]). Same family, and it is large.
3. **Two cheap discriminators, and both beat re-reading the code:** a **positive control** (something
   you KNOW must match — I used a row I had written that hour) or a **second independent
   measurement** (Tuesday re-measured against a live session). Reach for one of these on reflex.
4. **A selector that encodes a location is seat-specific.** `$HOME`, a hardcoded pane name, an inbox
   address — verify on a seat that is not your own, or derive it, never assume it.
5. **Corollary for reviewing others:** when an agent hands me a surprising figure, the useful question
   is not "how did you compute it" but **"what did you compute it over, and how do you know that was
   the whole set?"**

Related: [[2026-08-15_a-cap-is-never-neutral]] ·
[[2026-09-08_a-false-absence-is-usually-my-own-instrument]] ·
[[2026-08-14_i-read-representations-they-read-sources]] ·
[[2026-09-10_a-sync-conflict-copy-is-an-input-to-every-glob]]

## EXTENSION, same day — FOUR instances across THREE agents, and a fourth kind of selector

A fourth landed within the hour, from the Secuura seat, and it makes the family cross-fleet rather
than mine:

4. **A regex over-matching a nested path.** Deriving demo's rebuild set, `services/[a-z0-9-]+`
   matched `services/originate/src/services/**gdpr**Service.ts` and **invented a service called
   `gdpr`** — 13 services instead of 12. Fixed by **intersecting against compose's own service
   list**, and the seat then asserted the residual set ("in changed paths but not a compose service")
   was **empty**, which is the control that makes the intersection trustworthy.

**So: a column index, a glob, a `$HOME`, and a regex — four selectors, three agents, one afternoon,
zero broken tools.** The instrument worked every time.

**And a FIFTH shape the same hour, which is a selector in TIME rather than in space** — worth naming
because it does not look like this family at first: the seat measured demo's free disk **immediately
after** a build (11,097 MB), computed a 14 GB shortfall, and was one message from a correct-looking
"STOP, it will not fit". Settled free space minutes later was **13,751 MB — higher than before the
build started.** It had measured the transient peak, not the durable cost. **WHEN you sample is a
selector too**, and a measurement taken at the wrong moment is as wrong as one taken over the wrong
set.

**The seat's response is the one to copy:** it did not re-do the projection. It made the loop
**self-limiting** — check free space before each service, refuse below a 4,000 MB floor, exit and
write a stop-file, **never prune**. *"That way 'will it fit' is answered by the run rather than by my
arithmetic, and the failure mode is a clean halt rather than an exhausted disk."* **Where a
prediction keeps being wrong, replace the prediction with a mechanism that cannot overrun.**
