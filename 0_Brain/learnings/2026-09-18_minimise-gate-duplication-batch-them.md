---
date: 2026-09-18
type: grant
source: Kam, panel 2026-09-18 09:22:42 AEST (view=wednesday), verbatim — asked for after Wednesday's measured answer at 09:2x
status: live
tier: W
expires: none — Kam called it a STANDING RULE
---

# STANDING RULE: minimise gate DUPLICATION — batch gates, and never spend a second session on a round the first one should have carried

**His words, verbatim (09:22:42):**
> *"Thank you very much. The clarification is great. In that case, can you please create a standing rule to minimize the duplication of the gates? If we don't need to, let's run it less frequently or on batches. Please keep going with the pulls, the merges, and the commits, as well as all the work with the agents and the local LLM."*

**The measurement that produced it** (Wednesday, 09:2x, from the report directories): **186 QA gate sessions since 2026-09-11 — 54 tier-1, 68 tier-2 — and 80 of them were round 2 or later. 43% of our most expensive activity was a repeat.** Over the same window the local model ran 256 times at zero Claude cost. Kam's reading of that number is this rule.

## The distinction the rule turns on — not every second round is duplication

**A round 2 that follows a REAL FINDING is the gate earning its keep.** The seat fixed something the gate caught; that is the process working and it is not what Kam is asking me to cut.

**Duplication is a second session that establishes nothing the first could not have:**
- the pin went STALE (develop or the head moved between staging and launch), so the gate refuses or measures the wrong tree;
- a HARNESS fault (a launcher refusal, a broken tool) killed a session that never reached a verdict — *2026-09-18: a bug in `decl_splice.py` would have sent a Claude seat to investigate a fault in our own toolkit*;
- the SAME unchanged diff is gated twice because nobody recorded that a verdict already covered it;
- a full-weight gate ran on a change whose tier did not call for one.

## How to apply

1. **BATCH BY DEFAULT.** One gate session covers every change that is **disjoint by file** and shares a tier. **The batching key already exists:** `local-model/night/SUNDAY_MERGE_AUDIT.md` is a generated collision table — 19 files carry more than one READY, 54 of 147 files need sequencing. Changes that touch no common file can be gated together; changes that collide must be sequenced anyway, so gate them in that order. **Normalise the path prefix first** (`services/…` vs `Blockchain/Dev/services/…`) or the collision check under-reports.
2. **RE-PIN IMMEDIATELY BEFORE LAUNCH, never after a refusal.** Read `git ls-remote origin develop` and the head SHA in the same action as the launch. A stale pin costs a whole session and is the cheapest duplication to remove.
3. **NEVER RE-GATE AN UNCHANGED DIFF.** If head and develop are unmoved and the diff is byte-identical, the previous verdict STANDS — record it rather than re-running. A verdict is evidence about a tree, and the tree has not moved.
4. **A harness fault RESUMES the round, it does not spend a new one.** Fix the tool, re-run the same round, and record the fault in `IMPROVEMENTS.md` so it cannot repeat.
5. **Tier honestly** — the tiered gate ([[2026-09-05_qa-gate-tiers-and-the-two-nogo-cap]]) already caps rounds at two per class and reserves full weight for security, data destruction, deploys and human handovers. **This rule is that one applied harder**, not a new scheme.
6. **What must NOT be cut:** the gate itself on anything in a signature class. Kam asked to stop paying twice, not to stop checking. **A gate that misses things is worse than no gate — it comes with a receipt saying everything is fine** (the line that prompted him to ask for this).

## Owed, and offered to Kam

A proper cause breakdown of the 80 repeats — real-finding versus stale-pin versus harness versus re-gate — so the rule is tuned against evidence rather than my four plausible categories. **It has not been run.** The report directories carry round numbers and verdicts, so it is a measurable question, not a guess; the four categories above are named as *candidates*, not as findings.

**Family:** [[2026-09-05_qa-gate-tiers-and-the-two-nogo-cap]] (the tiering this sharpens) · [[2026-09-01_qa-gate-before-my-verification]] (the gate that stays) · [[2026-09-18_ornith-works-constantly-standing-rule]] (the free half of QA: the local checker's seven assertions cost nothing) · [[2026-09-14_do-not-guess-a-comparison-a-citation-you-did-not-open-is-a-guess]] (why the 186/80 figures were counted before being quoted).
