---
date: 2026-09-09
type: grant
source: Kam, panel 2026-09-09 08:12:01 (decision tap) + 08:12:27 (confirmed in words)
status: live
tier: W
---

# A BOUNDED authority to accept newly-published advisories — four clauses, and the exception is the clause that matters

**The operative case, so the headline matches it:** a newly-published security advisory has appeared
against a pin this fleet already holds, the pre-push gate now refuses **every author's** push, and
Wednesday is deciding whether to clear it. **Check the four clauses AND the exception below. If all
five hold, clear it and flag it. If any one does not, it stops for Kam — and "it is probably fine" is
not a clause.**

**His words, verbatim:** ruled `both` on card `secuura-advisory-gate-moving-set` at 08:12:01, then
*"Okay, go ahead with your recommendation."* at 08:12:27.

## What the grant covers

Wednesday may add a baseline entry for a newly-published advisory **without a card** when **ALL FOUR**
hold:

1. **Severity is MODERATE or below.**
2. **MEASURED — by the project's own agent, with a control — not to reach a runtime image.** Not
   reasoned, not inferred from a manifest. *"It is a devDependency" is a claim about the manifest,
   not about the image* (the Secuura seat's own sentence, 2026-09-09).
3. **The expiry is the SHARED re-triage date**, never a fresh one. One re-triage covering all of them
   is the entire point; a per-advisory date rebuilds the treadmill the grant exists to remove.
4. **Flagged to Kam in the same action.** The grant removes the pause, not the receipt.

## THE EXCEPTION, and it is written first because it is the one that will be met

**A package appearing in BOTH a test lock and a shipped tree stops for Kam, regardless of severity.**
In that case clause 2 is carrying the whole decision, and one wrong read accepts a live exposure.
**Check it explicitly and say you checked it** — an exception nobody checks is not an exception.

## What it does NOT cover

- **HIGH or CRITICAL, ever.**
- **Anything reaching a shipped tree.**
- **Any measurement without a clean control** — a zero whose instrument was never shown to fire is not
  a measurement ([[2026-09-08_a-false-absence-is-usually-my-own-instrument]]).
- **Baselining ONLY.** No pin bumped, no existing expiry moved, no preflight or gate change, no
  `--no-verify`. The gate reshape Kam ruled in the same breath is a TICKET, not a licence to edit the
  gate now — and **its window LENGTH is unruled and remains his.**
- **The grant is WEDNESDAY'S, not the seat's.** A project agent measures and reports; it does not
  clear its own blocker. Keeping the measurement and the decision in different hands is the point,
  and it is why the Secuura seat refusing `--no-verify` twice on 2026-09-09 was correct both times.

## Why he granted it, in one line the successor needs

**The advisory set MOVES without us.** Measured by the Secuura seat across its own two runs: match
count 31 → 32 with nothing in the dependencies changed, one JSON file edited. Its framing, adopted:
**the gate converts a third party's publishing schedule into a repo-wide outage.** Three advisories
inside one hour on 2026-09-09, none of them ours, each blocking Kam, Wednesday, Peter and Stuart.

## How to apply

1. **Check the five, in writing, in the mail that clears it.** A grant applied silently is
   indistinguishable from a grant exceeded.
2. **Name the measurement's OWNER.** Wednesday holds no client identity, so clause 2 is always
   someone else's read — say whose ([[2026-08-14_i-read-representations-they-read-sources]]).
3. **Flag it to Kam with what was accepted and until when**, in the same action, not at the wrap.
4. **This grant has no stated expiry** — he attached no window, unlike the three week-scoped grants of
   2026-09-07. That is stated rather than assumed; it does **not** get a `doctor.sh` expiry check, and
   if he meant one he can say so ([[2026-09-06_a-scoped-override-carries-its-own-expiry]]).
5. **A rule is most dangerous just after adoption** ([[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]]).
   Its exception is written above rather than waited for. **The first time a case argues its way past
   a clause, that is the clause working — stop and card it.**

**Family:** [[2026-08-07_protocol-v1.3-signed-delegation]] (the baseline this narrows one line of) ·
[[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded, so the boundary is written down
and never vibes) · [[2026-08-16_classification-is-the-field-that-grants-authority]] (severity and
"does not reach runtime" are the fields that decide authority here, so each needs its provenance) ·
[[2026-09-07_production-ban-lifted-for-the-week]] (a grant read narrowly, every use flagged) ·
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the gate reshape is the mechanism; this grant
is the interim rule).
