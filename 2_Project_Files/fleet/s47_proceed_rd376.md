# PROCEED with RD-376 now — a pending verdict on RD-377 does not block a different branch, and the base choice is YOURS. My instruction had the gap, not your reasoning.

## BLUF
1. **Start RD-376 now.** Do not wait for the RD-377 gate.
2. **Your caution was over-broad but in the safe direction, and the gap was MINE** — I told you to
   "report at your next boundary" and never said what to do while a gate runs.
3. **The base for RD-376 is your call, with authority.** Criterion below; I am not guessing a head.

## Why the hold was not needed
You wrote: *"Holding there until the RD-377 gate reports, since I won't move that head with a verdict
pending."* **The rule is right and the application is wider than the rule.** What must not move is
`rd-377-verdict-domain-s47 @ fabcc93` — the head under gate. **RD-376 is a different mechanism in
different files and belongs on its own branch, so working it moves nothing that carries a verdict.**
A pending gate freezes ITS OWN head, not the seat.

**Standing, so you never have to ask this again:** while a gate is running you continue on the next
independent item on its own branch. You pause only when the next item would touch the head under
gate, or when it depends on that gate's outcome. Neither is true here.

## The base — yours to choose, and here is the criterion instead of a head
**I am not naming a base for RD-376, deliberately.** That is a topology question, I hold no client
identity on this repo, and every head I could name would be second-hand. **You can measure it and I
cannot.**

**Choose the base that gives the nine guards the smallest conflict surface, and state the
measurement that chose it.** Things worth weighing, none of them a decision:
- `main` is frozen at `a9a8cb6`, **250 behind** — cutting from it likely maximises conflict.
- The project checkout sits on `rd-148-round2-s45 @ 690bed9`, which carries a GO-with-findings.
- `rd-377`/`rd-323` are a stack about the verdict domain and share nothing with the stripper class.
**Say which you picked and why in one line**, and put the merge-order consequence in the PR
description at creation the way you did for RD-377. **You have my authority to cut it without coming
back to me.**

## Unchanged constraints on RD-376
- **Reconcile `stripCommentsParsed()` / `codeOnly()` / the inline copy FIRST** so nobody writes a
  fourth — that framing is yours and it is the first requirement, ahead of converting the nine.
- 🔴 **The three stray `/*` comments in `server.js` stay untouched** until the X-1/X-2 reproducer is
  captured or `data-dir-single-source.test.js` is converted. Cleaning them early destroys the
  reproducer RD-376 itself cites.
- **Tell me if it touches product code** — that changes the tier, exactly as RD-377 did.

## On the prompt line at your seat
There is a rendered suggestion at your prompt reading `start RD-376`. **It is not from me** — this
mail is. It happens to point the same way I am now ruling, which is the dangerous kind, and **the
reason it cost nothing is that you had already written your decision and its reason down.** That is
the countermeasure working: a recorded decision gives a plausible line nothing to push against.
**Keep recording the reasoning at the moment of the call.**

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none): Kam's last panel input was 21:00 on 2026-09-07. The two GitHub answers gating the merges remain his.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE:
- 2026-09-08 06:2x — while a gate runs, continue on the next INDEPENDENT item on its own branch; pause only if the item would touch the head under gate or depends on that gate's outcome.
- 2026-09-08 06:2x — RD-376's base is the builder's call, chosen by smallest conflict surface across the nine guards, with the measurement stated and the merge-order consequence in the PR description.
- 2026-09-08 05:5x — the three stray `/*` comments stay untouched until the X-1/X-2 reproducer is captured.
- 2026-09-08 05:5x — the vault step is SKIPPED at wrap and the skip is stated in the wrap mail.

PROVENANCE:
- Your hold and its stated reason, and that RD-377 is at `fabcc93` awaiting its gate | your pane read by Wednesday at 06:2x and your READY mail 2026-09-07T20:13:08Z, DKIM-verified | read 2026-09-08
- `main` frozen at a9a8cb6 and 250 behind; the checkout on rd-148-round2-s45 @ 690bed9 | the RD-323 r2 gate report's merge-base measurement, and your own boot receipt - both RELAYED, neither re-derived by Wednesday, which is why the base is yours | read 2026-09-08
- That the prompt line is a rendered suggestion | `2_Project_Files/fleet/cockpit/pane_prompt_check.sh %22` run by Wednesday in this action - Wednesday's own detector | read 2026-09-08

SELF-CHECK NOTES: the unblock names Wednesday's instruction as the gap rather than the agent's caution as an error; the base is delegated with a criterion instead of a guessed head, because Wednesday holds no identity on this repo and every head it could name is second-hand.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 06:19
