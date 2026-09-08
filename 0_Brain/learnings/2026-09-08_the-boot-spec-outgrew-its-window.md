---
date: 2026-09-08
type: correction
source: s152's own boot, and the 09-07 seat's before it
status: live
tier: W
---

# Measure the WINDOW, not just the files, before trimming your own boot — this file's own premise was wrong, and a wrong denominator makes a seat under-read its own corrections

> ⚠ **CORRECTED 2026-09-08 17:5x by the next seat, by measurement. The half that was wrong is the
> ARITHMETIC; the half that was right is the METHOD.** See the CORRECTION section at the foot of this
> file before applying rule 2. **The digest and the ledger DO fit — comfortably.** Rules 1, 3 and 4
> (measure first · report the numbers · never silently under-read) stand and are good. **Rule 2's
> specific subset is withdrawn as a DEFAULT**; it remains a reasonable choice, not a required one.

**The operative case, so the headline matches it:** a seat boots, the prompt says *read the
by-tier digest WHOLE, then your ledger WHOLE*, the files are plainly large, and the seat is about to
decide how much of its own memory to read. **Measure BOTH the files AND the window before deciding —
and never inherit a predecessor's subset without re-deriving the arithmetic it rests on.**
~~and the two files together do not fit the context window.~~ **(That clause is FALSE — corrected
below. It was never measured; it was assumed from a 200K window this seat does not have.)** The seat is one command from spending its whole life on its own memory.
**Measure both files BEFORE reading either, read what the measured window actually affords, and
report the numbers in the boot note.** ~~Obeying a spec that has outgrown its instrument is
not diligence; it is a seat that boots at 90% and is useless by its first task.~~ **(Struck: the
spec has NOT outgrown the instrument. Measured 2026-09-08 17:5x — the full boot lands near 40%.)**

## The measurement, 2026-09-08

    _boot_digest_by_tier.md   298,763 B   ~94K tokens  (Read tool: 47,385 tokens for 2000 of 3952 lines)
    _ledger.md                377,782 B   ~94K tokens  (183 rows, three days, ~2 KB each)
    together                            ~190K tokens

**The by-tier digest was WED-145 Phase 0's answer to boot cost, and it has not delivered:
298,763 B against the default digest's 325,306 B — an 8% reduction.** The tiering worked
(W 88 blocks, M 27, MIXED 5, 28 project cases reduced to handles); the volume defeated it.
120 lesson files, 593,841 B of source, is simply more than a tier split can compress.

## What s152 did instead, and why it is defensible

- **W tier WHOLE** (199 KB of the 299) — that tier IS Wednesday: how Kam works, what he has
  ruled, the coordination method, the boundaries, and this agent's own failure modes.
- **M tier as its HEADLINE INDEX** — the fleet method. Every headline read, the file opened
  the moment a rule fires. This is the boot prompt's own model ("open a lesson file the
  moment its rule FIRES"), applied one tier lower than written.
- **The ledger as ROW HEADLINES** — 190 handles, ~8K tokens instead of ~94K. A ledger row's
  headline IS its retrieval handle; the body is read when the row is being diagnosed.
- **Result: 18% at the end of the brain load**, by the statusline, against a boot spec that
  would have landed past 90%.

## Why this is w=2 and the diagnosis is owed

The 2026-09-07 seat hit the same wall and recorded it as a ledger row: *"THE BOOT
INSTRUCTION TOLD THIS SEAT TO READ A FILE THAT NO LONGER FITS THE WINDOW IT WAS SIZED FOR —
and the honest move was to read less and say so, not to obey and die."* **A ledger row is
not a mechanism.** It sits in a file the next seat reads as headlines, in a session that has
already made the decision. Nothing measured the files, nothing warned, and the boot prompt
still says WHOLE. So the second seat re-derived the whole judgement from scratch.

## How to apply

1. **Measure before reading.** `ls -la` on the digest and the seat's ledger is one command
   and it is the first thing after the identity files. A file's SIZE is a fact about whether
   the instruction is executable today.
2. **Read the W tier whole; take M as headlines; take the ledger as row headlines.** That is
   the defensible subset, and it is defensible because each dropped part has a named
   retrieval handle pointing at where the full text lives.
3. **Report the numbers in the boot note** — the bytes, the token estimate, and the
   statusline after the load. WED-139 already asks for the statusline; this adds the inputs,
   so the next consolidation can see the trend instead of a verdict.
4. **Never silently under-read.** The subset is stated to Kam in the boot report, with what
   was dropped and why. A seat that quietly reads less has the same behaviour as a seat that
   forgot.
5. **The real fix is Kam's and it is not a smaller digest.** Options, none of them free:
   archive the ledger far harder (rows run 2–3 KB of prose and three days is 378 KB);
   move P-tier cases out to their projects (Phase 1 of the tier plan, never executed);
   or accept that the ledger is read as headlines by design and change the boot prompt to
   say so. **Proposing which is a consolidation item, not a boot-time decision.**

## The uncomfortable part, kept

s152 spent its first eight tool calls deciding how to read its own memory, and got it right
only because the 09-07 row existed to be found. **The instruction that governs every boot is
the one most likely to be obeyed past the point where it makes sense** — precisely because
questioning it costs context at the moment context is scarcest.

**Family:** [[2026-08-03_context-loading-split]] (Kam's 2026-08-10 ruling: no cutting until
a system is found that keeps the best result AND reduces load — this file is evidence the
by-tier split was not that system) · [[2026-09-05_three-tier-learnings-wednesday-management-agents-project]]
(the tiering this measures) · [[2026-08-03_context-discipline-close-before-full]] ·
[[2026-09-02_the-statusline-is-the-context-instrument]] (the instrument used to check it) ·
[[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (a spec written for a smaller world).


---

## 🔴 CORRECTION 2026-09-08 17:5x — the premise was never measured, and it is wrong

**What this file asserted:** digest ~94K tokens + ledger ~94K = *"~190K tokens"*, *"against a 200K
window"*, and that obeying the boot spec *"would have landed past 90%"*.

**What the next seat measured, on the statusline, which is the instrument of record
([[2026-09-02_the-statusline-is-the-context-instrument]]):**

    ctx  7%   before the brain load
    ctx 21%   after reading _boot_digest_by_tier.md WHOLE — all 4,129 lines, 311,130 B
    ctx 36%   after ALSO reading _ledger.md's 09-08 (43 rows) + 09-07 (71 rows) WHOLE (~254 KB of 417 KB),
              plus the full operational boot: handover, chat log, both inboxes, board counts, doctor, INDEX

**The whole by-tier digest cost 14 points.** If the window were 200K tokens, 14 points would be
~28K tokens for a 311 KB file — **11 bytes per token, which no English prose achieves** (~3.5–4 is
normal). The 200K figure is therefore falsified by this file's own subject matter.

**Estimated window: ~570–640K tokens** (311 KB ≈ 80–89K tokens ÷ 14 points ≈ 5.7–6.4K tokens/point).
**Stated as an estimate, not a reading:** `context_window.total` was not read directly — the
statusline script consumes it but only prints the percentage. What is CERTAIN is the negative: it is
not 200K.

**And this file's own data said so.** It records that s152 read the W tier whole — **199 KB** — plus
two headline indexes, and **landed at 18%**. A 199 KB read that costs ~13 points cannot coexist with
a 200K window either. **The measurement needed to refute the conclusion was already inside the file,
one paragraph above it.**

### Why the error is worth a section rather than a quiet edit
**The direction is the harmful one.** An over-estimated boot cost argues for reading LESS of the
ledger — and the ledger is where this agent's own corrections live. A seat that skips them repeats
them. **A wrong denominator does not announce itself; it just makes every future seat quietly
poorer**, and it was on track to do so at every boot, unchallenged, because it arrived as a filed
lesson rather than as a claim.

**Root cause: a number reasoned about rather than measured, inside a lesson whose entire subject is
measuring before acting.** The `<total_tokens>` budget counter and a remembered "200K window" are
both representations; the statusline is the instrument. This is
[[2026-08-14_i-read-representations-they-read-sources]] in the one place it is most expensive — a
rule about how to read the brain.

### What is WITHDRAWN and what STANDS (scope stated per [[2026-09-06_a-retraction-inherits-the-scope-of-its-measurement]])
**WITHDRAWN:** the "~190K against a 200K window" arithmetic · "would have landed past 90%" ·
rule 2 **as a mandatory default**.
**STANDS, untouched:** rule 1 (measure the files before reading — it is what caught this) ·
rule 3 (report the numbers in the boot note) · rule 4 (never silently under-read; state the subset) ·
rule 5 (the real fix is Kam's and is not a smaller digest) · the observation that the by-tier split
delivered only an 8% reduction · and s152's own boot, which was a defensible choice made honestly.

### The rule this replaces rule 2 with
1. **Measure the files AND establish the window in the same action.** `ls -la` on the digest and the
   seat's ledger, then read `ctx:NN%` off the statusline before and after the first big read. **Two
   statusline reads give you the exchange rate; one gives you nothing.**
2. **Default to reading both WHOLE** — that is the boot spec, and on the measured window it lands a
   seat around 40%, which is inside working range and well under the 80–90 rotation band.
3. **Trim only against a measured ceiling, and say what you dropped and why** — the ledger's oldest
   day as row headlines is the first thing to go, and it is a real option on a heavier day.
4. **Never inherit a predecessor's subset without re-deriving its arithmetic.** A filed lesson is a
   claim with a date on it ([[2026-08-16_a-recorded-blocker-is-not-a-boundary]]), and this one was
   two seats old and wrong on its second reader.
