---
date: 2026-08-13
type: principle
source: "Secuura/Blockchain agent, session 28, diagnosing its own slip after I corrected it for CC'ing Kam on a plan confirmation. Their formulation: 'A rule whose first line contradicts its own operative case will be misapplied under load.' The memory already carried the correct carve-out; the headline still read 'CC Kam on every email' and the exception sat in the body."
status: live
supersedes: ""
---

# A rule whose headline contradicts its operative case will be misapplied — the first line IS the retrieval handle

**The case.** The Secuura agent CC'd Kam's client address on a fleet
plan-confirmation, against his 2026-08-12 instruction. I corrected it. The
correction was right — but the interesting part is what the agent found when it
checked: **it already held the rule.** Its memory carried both the older
2026-06-26 "CC Kam on every email" instruction and the newer carve-out that
narrowed it to human-facing mail only. The carve-out was accurate, complete, and
sat in the body. The headline still said the old thing. Under load, the headline
is what fired.

It rewrote the memory so the exception leads, and named the failure precisely:
*a rule whose first line contradicts its own operative case will be misapplied
under load.*

**Why this is a distinct lesson and not just "keep notes current".** The note
WAS current. Nothing in it was false. The defect was purely **structural**: the
part that gets retrieved disagreed with the part that governs. That is invisible
to every check I run on my own brain, because I verify lessons for *truth* and
never for *whether the first line matches the case they actually govern*.

**This brain has already failed this way twice, and I diagnosed both without
naming the class.**
- [[2026-08-04_never-blanket-markseen-mid-monitoring]] failed to fire on
  2026-08-10 because its retrieval handle was the SCRIPT (`mark-seen`) and the
  recurrence wore a different costume (a watcher baseline). Diagnosis at the
  time: "wrong retrieval handle."
- [[2026-08-06_artifact-presence-is-not-execution]] failed to fire because
  occurrence 1 was written as a CI rule, and occurrence 2 was a scheduler log.
- And on 2026-08-13 my own absence-claim rule, filed at w=3 three hours earlier,
  failed at w=4 because I had filed it as a **wording** rule when the failure
  happened upstream of wording.

All four are the same shape: **the title indexed something narrower, older, or
differently-shaped than the situation the rule was supposed to govern.**

**How to apply — to my own learnings, memories, briefs and specs:**
1. **Write the headline last, from the operative case**, not from the incident
   that produced the rule. The question is not "what happened?" but "what will I
   be doing when I need this?"
2. **If a rule has an exception that is load-bearing, the exception goes in the
   first line.** A qualifier that lives only in the body is a qualifier that does
   not exist when someone is busy.
3. **Never leave a superseded headline above a corrected body.** When newer
   guidance narrows an older rule, the title changes too — otherwise the file
   answers the old question and the new one contradicts it three paragraphs down.
4. **Test a rule by its handle:** read only the title and ask what you would do.
   If that differs from what the body requires, the file is a trap regardless of
   how correct the body is.
5. Applies equally to brief section headings, ticket titles (my own ticket title
   is what caused the w=3 provenance regression on 08-06), and spec BLUFs. The
   BLUF rule and this one are the same discipline pointed at different readers:
   the reader who stops early must not be misled.

## The tooling costume (2026-08-17, Secuura s43): a check whose MESSAGE rots while its measurement stays correct

KS-78's launcher drift warning printed *"N commit(s) on main"* while its `git log` (no
revision argument) counted HEAD — and it was RIGHT the day it shipped: main was the
integration line then. Git Flow moved integration to develop ten days later; the
measurement silently followed HEAD and stayed correct, **the hardcoded label did not** —
and two sessions discounted a TRUE warning because its label named a branch that had not
moved. Same law, pointed at tool output: **the message a check prints is its headline, and
a headline nobody re-reads after the world changes becomes a lie wrapped around a truth.**
When writing any checker: print the MEASURED thing (the actual revision, the actual set),
never a prose assumption about what was measured.

**The meta-note, and it is now a pattern rather than an anecdote.** This is the
**fourth** protocol improvement handed to me by a delegated agent — after the
local-proof rule (Secuura, 08-06), the DKIM authorship check (NexusAI, 08-07),
and the containment-control rule (HPSM, 08-13). All four arrived unprompted from
an agent examining its own work, and all four were better than what I would have
written. Two of them, including this one, came from an agent diagnosing a mistake
I had just corrected it for — which is the strongest argument for correcting
plainly and then listening to what comes back.

**Related:** [[2026-08-04_never-blanket-markseen-mid-monitoring]] (the class,
first costume), [[2026-08-06_artifact-presence-is-not-execution]],
[[2026-08-06_bluf-write-for-the-reader]] (same discipline, different reader),
[[2026-08-12_no-cc-kam-on-agent-mail]] (the rule in question),
[[2026-08-11_coordinator-not-carrier]] (noticing and propagating is the job),
[[_ledger]]
