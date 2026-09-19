---
date: 2026-09-20
type: principle
source: Datasec/NexusAI S70 (its RD-525 census, 2026-09-20 22:44Z), adopted by Tuesday
status: live
tier: M
---

# A CLOSURE inherits the scope of the measurement that produced it — a census written to settle a disagreement is not a census of the world

**The operative case, so the headline matches it:** you are about to rely on a closed ticket, a completed census, a "verified complete" list or a signed-off audit — or to write one. **Ask what QUESTION it was asked, not whether it was done well.** A measurement made to settle a dispute between two lists establishes which list was right. It establishes nothing about a third thing that was in neither.

**The case (S70's, adopted verbatim in substance).** RD-310's census was written to settle a disagreement between two personal-data lists, and it answered that question correctly; its guarantee still holds. RD-525 then re-read the code and found **four jsonStorage stores in neither list**, the **largest personal-data store** (`printer_logs.db`) in neither, and — worse — a purge loop that is **file-only**, so a whole directory tree (`feedback-attachments/`) is structurally unreachable. Nothing in RD-310 was wrong. It was complete over its frame and silent about the rest, and its CLOSURE was read as completeness.

**How to apply:**
1. **Read a closed item's SCOPE SENTENCE before citing it as coverage.** "Reconciled the two lists" and "enumerated every store" are different claims that close the same ticket.
2. **When you close something, write the frame INTO the closure** — what was measured, over what set, and what was deliberately not looked at. One line, and it is the line that stops the next reader inheriting a guarantee nobody made.
3. **The dangerous inheritance is a LIST**: a store, a route, a field, a file class that was never in either candidate set is invisible to a reconciliation and to everyone who trusts it afterwards.
4. **A fix that makes the list SAY it is covered is the failure mode** — RD-575's own trap: adding the directory to the file list would fail on `EISDIR` and the per-name handler would swallow it, so the record would claim coverage while nothing was removed. **Assert the effect (the data is gone), never the bookkeeping.**
5. Same shape in reverse for us: when a gate is NOT RUN, its items are unverified CLAIMS, not results — a verdict inherits the scope of the run that produced it.

**Family:** [[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (the parent — this is its CLOSURE half: there the census was misread while fresh, here it was inherited after closing) · [[2026-08-16_a-recorded-blocker-is-not-a-boundary]] (a recorded claim with a date) · [[2026-09-06_a-retraction-inherits-the-scope-of-its-measurement]] (its mirror: a withdrawal inherits its measurement's scope too) · [[2026-08-07_a-check-that-cannot-fail]].
