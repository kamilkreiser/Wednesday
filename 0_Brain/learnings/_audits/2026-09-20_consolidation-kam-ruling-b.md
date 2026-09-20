---
date: 2026-09-20
type: audit
source: Kam's ruling (b) on card `tuesday-boot-digest-outgrew-the-window`, panel 2026-09-20 16:41:18
status: live
---

# Consolidation audit — Kam's ruling (b): "keep the whole read, shrink the corpus to fit"

**His words, verbatim:** *"Decision tuesday-boot-digest-outgrew-the-window: b — Keep the whole read,
shrink the corpus to fit"* (panel, 2026-09-20 16:41:18, tagged `view: wednesday` but naming
Tuesday's card by id, so it is unambiguously this seat's). He ruled AGAINST this seat's
recommendation (a). **This audit is his review point — per `weekly-consolidation.md` step 7, no
consolidation takes silent effect.**

## What was done this session

**One file, as a worked example, chosen because it was 8% of the whole corpus on its own.**

`2026-08-07_a-check-that-cannot-fail.md` — **77,770 B → 10,197 B** (86% off the lesson file).
Its **27 accumulated case sections** moved VERBATIM to
`_cases_2026-08-07_a-check-that-cannot-fail.md` (72,395 B). Nothing deleted, nothing summarised.
The lesson keeps the rule, the concrete remedy, and **an index of all 27 case headings** — because
a heading IS the retrieval handle (`weekly-consolidation.md` step 4: *a merged lesson that cannot
be grepped is a destroyed memory*).

**Conservation asserted:** 77,770 B in → 82,592 B out. It GREW by 4,822 B (the index plus the
companion's header). Nothing was removed; this is a move.

**Precedent, not invention:** this is the pattern Kam himself ruled for `_ledger.md` on 2026-09-04
(card `wed-ledger-boot-cost`) — a file that grows by accretion is split, the rule stays hot, the
evidence is read on demand. The `_` prefix keeps the companion out of `boot_digest.py`'s
`2026-*.md` glob, which is the mechanism.

## 🔴 FINDING 1 — a mechanical split is UNSAFE, and it would have demoted LIVE RULES

The obvious automation — "move every dated section to the cases file" — **would bury current
rules.** Measured on two files:

- `2026-09-02_rotate-in-the-70-80-band-conditionally.md` contains
  `## SUPERSEDED AGAIN 2026-09-07 10:49 — Kam: "the Wednesday window is between 80 and 90% context."`
  **That dated section IS the live rotation band.** Moving it leaves the superseded 70–80 band in
  the headline and the live rule in a file nobody opens at boot.
- `2026-09-01_qa-gate-before-my-verification.md` contains
  `## REFINED 2026-09-05 20:19 — Kam: "Let's go ahead with your recommendation." — the gate is TIERED and CAPPED`.
  Same shape.

These accreted sections are a **MIX of cases and rule-amendments**, and only reading tells them
apart. This system has already been bitten by exactly this: the boot prompt's rotation line stood
TWO rulings stale for days. **So every file is split by hand, or not at all.** The 77 KB file was
safe because its sections are explicitly dated INSTANCES (`### A failure-only log going quiet is
not recovery (2026-08-22, Secuura s61)`).

## 🔴 FINDING 2 — the digest is NOT a linear function of corpus size, and this changes what (b) requires

**Measured, not assumed:**

| | before | after | delta |
|---|---|---|---|
| lesson corpus (source) | 960,266 B | 887,534 B | **−72,732 B** |
| `_boot_digest_by_tier.md` | 511,178 B | 500,655 B | **−10,523 B** |

**Cutting 72.7 KB of source bought 10.5 KB of digest — a 14% return.** The by-tier digest already
reduces W files (operative paragraph, section index, rules sections verbatim), so it was never
carrying most of that case text. Source → digest is 56% overall, but for *case* bytes it is far
lower.

**The consequence for (b), stated plainly and without re-arguing the ruling:** archiving cases is
cheap, safe and nearly free in digest terms. **The digest is dominated by RULES rendered verbatim
— which is exactly what must survive.** So "shrink the corpus to fit" cannot be achieved by
archiving evidence. It requires genuinely MERGING lessons whose rules overlap, so that N rules
become one rule with N sub-clauses.

## 🔴 FINDING 3 (added 17:4x) — THE SAFE MECHANICAL WORK IS EXHAUSTED AFTER ONE FILE. Measured, so nobody re-explores it.

Blocked on CI and looking for more work inside (b), I checked whether the other accreted giants
share the safe shape of the 77 KB file — dated INSTANCE sections that can be moved without touching
a rule. **They do not. Not one of them.**

| file | size | its `##` sections are |
|---|---|---|
| `2026-08-14_i-read-representations-they-read-sources` | 28,808 B | *"Sharpened 2026-08-15: the variable is not WHOSE claim it is"*, *"Sharpened again 2026-08-16: the third switch is EXPECTATION"* — **rule changes** |
| `2026-09-08_a-false-absence-is-usually-my-own-instrument` | 21,888 B | *"EXTENSION … a SEMANTIC control is what catches it"*, *"SHARPENED … A CONTROL DRAWN FROM THE SAME FAMILY … AGREES WITH THE WRONG ANSWER"* — **rule changes** |
| `2026-08-06_ghost-suggestions-in-panes` | 17,636 B | *"THE ESCALATION LADDER (consolidated 2026-08-23 — **read this first when triaging any prompt line**)"* — an explicitly load-bearing operative rule |

**`2026-08-07_a-check-that-cannot-fail` was the exception, not the pattern.** Its sections were
genuinely dated instances (`### A failure-only log going quiet is not recovery (2026-08-22,
Secuura s61)`); these are the lesson's own evolution. Splitting any of them would do precisely what
Finding 1 warns about, at three times the scale.

**So: the cheap, safe, mechanical half of (b) is DONE and it bought 10.5 KB of digest.** Everything
remaining is the merge work in the clusters above — which is what Finding 2 predicted, and which is
held for Kam's look. **A future seat should not re-explore case-splitting; this table is the answer.**

## The merge clusters this seat can already see (proposal, not executed)

From the 322-handle index, these say overlapping things and are the real candidates:

1. **False zeros / controls** — `a-false-absence-is-usually-my-own-instrument` ·
   `a-census-complete-over-a-frame-that-is-not` · `a-two-answer-question-hides-a-third-state` ·
   `surprising-measurements-are-selector-errors` · `a-cap-is-never-neutral` ·
   `2026-09-20_an-absence-goes-stale-while-you-compose-the-complaint`
2. **Representation vs source** — `i-read-representations-they-read-sources` ·
   `i-endorse-things-i-have-not-read` · `artifact-presence-is-not-execution` ·
   `git-topology-is-a-measurement-not-a-model` · `a-classification-list-is-a-representation-not-an-instruction`
3. **Mechanism vs intention** — `a-promise-is-not-a-mechanism` ·
   `an-enforcement-you-must-arm-is-not-one` · `a-ritual-nothing-triggers-is-not-a-ritual` ·
   `a-refusal-nobody-reads-is-indistinguishable-from-working`
4. **Superseded-in-place rotation/context rules** — several files carry two or three dead numbers
   above the live one. The dead ones are retrievable history and belong in a `_cases_` companion;
   **the live number must stay in the lesson file.** This cluster is the highest-risk and should be
   done last, by hand, with the live rule quoted in the audit.

**Guards that bind the rest of this work** (`weekly-consolidation.md`): merge and supersede, never
delete; newer wins with the old marked `status: superseded` and linked; protect retrieval handles;
**never regenerate a memory file wholesale** (anti-collapse, ACE); and no consolidation takes
effect without an entry in this audit.

## State at the end of this session

- 193 lesson files, 887,534 B source; by-tier digest 500,655 B; default digest 505,227 B.
- 1 file split (the 77 KB one). 27 case sections preserved in its companion.
- Both digests regenerated per session-end rule 3b.
- **Nothing merged and nothing retired yet** — the clusters above are a proposal for Kam, not a
  completed action, and finding 2 means they are the work that actually delivers his ruling.
