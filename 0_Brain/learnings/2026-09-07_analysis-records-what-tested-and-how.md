---
date: 2026-09-07
type: preference
source: Kam, dashboard panel 18:56:36
status: live
tier: W
---

# Where there is analysis, the record carries THREE fields — what was found, what was TESTED, and HOW

**His words, verbatim (2026-09-07 18:56:36):**
> *"Fantastic. Keep with the work, and there is analysis, make notes of what was found, what was
> tested, and how."*

(Dictation: *"and where there is analysis"*. The instruction is unambiguous.)

**The operative case, so the headline matches it:** a gate has returned, a verification pass has been
read, a probe has run, a register has been re-derived — **anything where someone measured something.**
Wednesday is about to write it into a handover, a ticket, a panel line or a report. **A record of
WHAT WAS FOUND is one field of three. The other two are what was tested and how it was tested, and
they are the ones that get dropped**, because the finding is the interesting part and the method feels
like scaffolding.

## Why he asked for it, and why it is not bookkeeping

**A finding without its method cannot be re-checked, re-used, or trusted at a distance.** Three things
today turn on precisely this:
- The **`checkout@v7`** claim was a finding with no named instrument. It stood for a day and was wrong.
  *"104 pushes landed on that pin"* — a method — killed it in one line.
- The **RD-329** verdict is only worth anything because it says **how**: 16 tamper classes, each
  `node --check` clean, each read **off the wire from a booted server**, with both controls held. Take
  the method out and "6 caught, 10 missed" is an assertion.
- The **verification pass** across ten components reports **zero refuted**. That number is only
  credible because each file states what it re-derived and with which command — including the greps
  that were *mis-run* and re-run.

**The method is also the part that transfers.** A finding is about one file; *"tamper five ways and
assert each tamper landed before concluding"* is reusable by every agent on every repo. Most of what
this fleet has learned this week came from method sections, not from findings.

## How to apply

1. **Every analysis record carries the three fields explicitly** — not implied, not woven into prose:
   **FOUND** (the claim), **TESTED** (the scope: what was and was not exercised), **HOW** (the
   instrument, the command, the controls).
2. **"HOW" includes the controls.** A positive control proving the instrument fires, and — since the
   09-07 RD-368 precedent — a **negative control** so a zero is one the reader can vouch for. A method
   without its controls is a story about what someone did.
3. **State what was NOT tested, in the same breath.** The QA charter already requires it; this makes
   it a property of every analysis record, not only gate reports. *"Unit-proven; the click path could
   not be exercised"* is a complete record. A bare green tick is not.
4. **Where the analysis produced an artefact, name its PATH** — the report directory, the matrix
   files, the evidence folder ([[2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id]]).
   A finding whose evidence cannot be reached is a finding on trust.
5. **Record the instrument errors too.** Both gates today reported their own bad probes (a 403 that
   was CSRF; a tamper matrix that never ran). **Those belong in the record** — they are what tells the
   next reader which greens to re-check.
6. **This binds Wednesday's OWN analysis, not only the agents'.** Handovers, ledger rows and panel
   summaries that carry a finding carry its method, or say plainly that the method was someone else's
   and name whose ([[2026-08-14_i-read-representations-they-read-sources]]).

**Related:** [[2026-08-07_a-check-that-cannot-fail]] (the method IS the discriminator) ·
[[2026-08-06_bluf-write-for-the-reader]] (found goes first; tested and how follow — never the reverse) ·
[[2026-09-01_qa-gate-before-my-verification]] · [[2026-08-16_an-overstated-record-gets-discounted-wholesale]]
(a register survives on its method) · [[2026-09-07_hand-kam-the-link-not-the-instruction]] (same day,
same principle: hand the reader the thing, not the promise of it).
