# Weekly consolidation ("dreaming") — ritual

Approved by Kam 2026-08-03. Cadence: weekly, in the 06:00 slot (Sunday proposed,
pending Kam's confirmation). Until the WED-16 scheduler ships, run it in the
first session after each Sunday. ~30–45 min of focused work, before Kam's day.

## Steps

1. **Re-read the week:** all `daily/` notes since the last consolidation, the
   correction ledger (`learnings/_ledger.md`), and every lesson touched this week.
2. **Distil patterns:** recurring themes across sessions become candidate lessons;
   candidate lessons that recurred become promotion candidates (weight ≥3 rule).
3. **Merge & supersede:** overlapping lessons merged; contradictions resolved
   (newer wins, old file marked `status: superseded` with link). Never leave old
   and new as peers.
4. **Protect retrieval handles:** consolidation must keep stable names, dates,
   IDs — a merged lesson that can't be grepped is a destroyed memory.
5. **Ledger review:** retire weights only here, with reasoning; check the repeat-
   correction trend — this number is the health metric of the whole system.
6. **Promotions:** execute any earned promotions (lesson → `identity/`, or →
   enforcement in launcher/CLAUDE.md/hooks).
7. **Write the audit note:** `learnings/_audits/YYYY-MM-DD_consolidation.md` —
   every change made, every weight retired, the trend line, anything needing
   Kam's decision. **Kam skims this at the next briefing — no consolidation
   takes silent effect.**

## Guards

- Over-personalization: promotion needs recurrence (w≥3) or Kam's explicit
  "always" — never a single occurrence.
- Drift: the audit note is mandatory even for a quiet week ("nothing to
  consolidate" is a valid, recorded outcome).
- **Anti-collapse (ACE, arXiv 2510.04618, adopted 2026-08-03):** consolidate by
  *incremental deltas* — edit/merge specific lessons; NEVER regenerate a memory
  file wholesale, and never let summarization erode concrete detail (brevity
  bias). The audit note records what changed as diffs, not rewrites.
- **Validate self-changes (DGM principle, adopted 2026-08-03):** a change to my
  own rituals/skills counts as validated only when subsequent ledger/retro
  evidence shows it working in real sessions — adoption alone is not improvement.
  Unvalidated changes get flagged in the next audit note.

## STANDING KPI — is the process working, or looping? (Kam's ruling, 2026-09-07 13:27)

**His words, verbatim:** *"Whether the process is working or looping is hard to decide. It can only
be decided by the outcome. So let's keep watching and be mindful of it as we go forward."*

**He declined to rule on the 30% self-referential board finding and named the CRITERION instead:
the OUTCOME.** "Keep watching" is an intention, so this section is the mechanism that makes it fire
([[../learnings/2026-08-07_a-promise-is-not-a-mechanism]]). **Every consolidation reports these four
lines, with the measurement in the same breath as the characterisation:**

1. **The split.** Open tickets whose SUBJECT is one of our own instruments (guard/gate/harness/
   preflight/hook) vs the product, with the predicate stated and its boundary named — the 2026-09-07
   pass published **88 with its definition attached and said the class is 88–94 depending on the
   boundary**. Quote a number that way or not at all.
2. **The trend.** That split against the previous consolidation. **A ratio rising with no
   corresponding fall in product defects is the LOOPING signal.**
3. **The outcome test, which is the one that actually answers Kam:** of the instrument tickets
   CLOSED this week, **how many later caught a real product defect?** A guard that has never caught
   anything is decoration; a guard that caught something is the process working, and this is the
   only number that distinguishes them.
4. **Duplication rate.** Findings carried by more than one ticket
   ([[../learnings/2026-09-07_a-control-proving-it-is-not-yours-does-not-say-who-filed-it]]).
   **Duplication is the cheapest looping signal available** — it needs no judgement at all.

**Report all four to Kam even when they look good**, and never as a verdict — the ruling on what
they mean is his. **Baseline set 2026-09-07: 293 open · 88 instrument-subject (69 ours / 4 product /
7 both / 8 unclassified) · 79 actionable · 5 findings across 14 tickets · 7 legacy.**
