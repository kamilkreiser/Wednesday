---
date: 2026-09-14
type: correction
source: Kam, panel 2026-09-14 16:19:29 +10:00 (view=wednesday), verbatim in the prompt log
status: live
tier: W
---

# Do not guess — a comparison recited from memory and labelled "from the model cards" is a guess wearing a citation; a comparison to Kam rests on a measurement taken or a document read in the same action, or says "unmeasured"

**His words, verbatim (2026-09-14 16:19:29):**
> *"I just realized that when you gave me the original comparison between the two models, you were
> guessing. Please don't do this. Whether it was because of expedience or anything else, do not
> guess. Analyze and check."*

**The operative case, so the headline matches it:** Kam asks a comparison question — two models, two
tools, two vendors, two approaches — and Wednesday has an answer in memory that *sounds* like the
documentation. **Stop. Either open the document and quote it, or run the thing and report the number,
or write "unmeasured" — in the same action as the sentence.** A fluent answer with a source-shaped
label ("from the published model cards", "per the docs", "by the benchmarks") that no read in this
session produced is a guess, and labelling it as sourced is worse than a bare guess because it
removes his reason to check.

## The case
At 15:5x Kam asked how gpt-oss 120B compares to the 20B. Wednesday answered within a minute with
sizes, speeds and an eval placement ("about 14 gigabytes", "likely around double the speed",
"roughly o3-mini level vs o4-mini level"), prefaced *"from the published model cards, not from a run
on this machine"*. **No card had been opened in the session; nothing on the 20B had been run.** Two
of the recited figures happened to be right when the card was read twenty minutes later (14 GB,
128K context); the speed and the eval placement were memory. Kam noticed the shape, not the error —
*"you were guessing"* — and named the cause candidly: expedience.

## Why the existing rules did not fire
- [[2026-08-14_i-read-representations-they-read-sources]] binds counts, states and mechanisms; a
  *model card recited from training memory* did not register as a representation, because it arrived
  as knowledge rather than as a document.
- [[2026-09-04_decisions-held-narration-drifted]] rule 3 ("no characterisation reaches Kam unless the
  measurement is in the same breath") was applied to *this machine* ("unmeasured here") and skipped
  for the *published* figures — as if a number from memory were a measurement someone else had made.
- [[2026-09-10_i-endorse-things-i-have-not-read]] covers endorsing an AGENT's claim unread; this is
  the same act pointed at a DOCUMENT: citing what was not opened.

## How to apply
1. **Every comparison or factual characterisation to Kam names its instrument inline** — *"read at
   ollama.com/library/gpt-oss, 16:2x"*, *"measured on this machine: 164 s, 50 tok/s"* — or carries
   the word **unmeasured**. "From the model cards" is a claim that the cards were read *now*.
2. **When the answer is in memory, that is the trigger to read, not the licence to skip reading.**
   The cost is one `curl` and a minute; Kam priced the alternative as trust.
3. **Speed and quality claims about a model come from a run on THIS machine on OUR tasks**, never from
   memory of benchmarks — his own ruling the same hour: *"metrics don't always tell the truth"*, and
   the KS-871 pass-with-a-partial-fix is the case. The head-to-head design (same tasks, same
   checker, an agent's source read, diffs attached) is the mechanism.
4. **Expedience is the named cause, so the countermeasure is structural:** an ask that needs a read
   or a run gets a receipt first (*"received — measuring, answer in N minutes"*) and the answer
   second; a fast full answer to a comparison question is the smell.
5. **Own it in the ledger the same session** with the specific sentences that were guessed, not a
   general apology; the retraction is scoped to what was recited (the speed multiple, the eval
   placement), and the figures that a later read confirmed are marked confirmed, not retracted.

**Family:** [[2026-08-14_i-read-representations-they-read-sources]] · [[2026-09-04_decisions-held-narration-drifted]]
(rule 3) · [[2026-09-10_i-endorse-things-i-have-not-read]] · [[2026-09-09_acknowledge-panel-instructions-on-receipt]]
(the receipt-first shape that makes "measuring, N minutes" the default) · [[2026-08-07_a-check-that-cannot-fail]].
