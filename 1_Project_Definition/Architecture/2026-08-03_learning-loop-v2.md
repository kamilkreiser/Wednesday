# Learning loop v2 — proposal (WED-17)

Date: 2026-08-03 · Status: DRAFT — awaiting Kam's review
Commissioned by Kam (verbatim in `../Discovery/00_prompt-log.md`, 2026-08-03).
Research base: `../Discovery/research/2026-07-31_second-brain-best-practices.md`.

## What we already have (v1)

| Mechanism | State |
|---|---|
| Same-session capture of corrections/preferences → `0_Brain/learnings/` with provenance + supersede links | live |
| Full-brain read at every boot (token cost accepted) | live |
| Episodic/semantic/procedural split: `daily/` / `learnings/`+`people/` / `identity/` | live |
| Verbatim prompt log during discovery | live |
| Linear as task truth; projects_index feed for cross-project awareness | live |

v1 is a **capture** system. What it lacks is everything after capture: nothing
verifies a lesson changed behaviour, nothing consolidates as the brain grows, and
Kam can only teach when a session happens to be open. Six additions, ranked.

## 1. Correction ledger — make "improving" measurable (start today)

The success metric Kam set is "interactions measurably improve." Make it a number:
every time Kam corrects me, one line in `0_Brain/learnings/_ledger.md` —
date · what · **new or repeat** · linked lesson.

- **Repeat correction = regression** — treated like a failing test (no-skip rule):
  diagnose *why* the stored lesson didn't fire, fix the lesson or its placement.
- The trend line (repeat-rate falling toward zero) is the health measure of the
  whole learning system. Reviewed at each weekly consolidation (§3).

## 2. Wrap-up self-retro — the cheap, high-leverage ritual (start today)

Research verdict: session-end reflection is the highest-leverage cheap mechanism.
Add to the wrap-up ritual, 3–5 lines in the daily note:

- What went well / what I'd do differently
- Which stored lessons I *applied* (proof the brain is load-bearing)
- Which I *missed or nearly violated* → feeds the ledger
- Candidate new lesson? (only if it would change future behaviour — write-time
  importance filter)

Occasionally (not every session) ask Kam for a one-word grade. Implicit signals —
what he re-asks, overrides, rephrases — count as training data too and belong in
the retro even when he never says "remember this."

## 3. Weekly consolidation ("dreaming") — keep the brain sharp as it grows

Once the 06:00 rhythm ships (WED-16), one early-morning slot a week (suggest
Sunday) before Kam is up:

1. Re-read the week's daily notes + ledger; distil patterns.
2. Merge overlapping lessons, mark superseded ones, fix contradictions (never
   leave old + new as peers).
3. Preserve retrieval handles (names, dates, IDs) — consolidation must not
   destroy grep-ability.
4. Write an **audit note** of every change for Kam to skim at the next briefing —
   human review guards against silent drift in my own memory.

This is also what keeps "read ALL learnings at boot" viable: the file count grows
slower than the lesson count.

## 4. Recurrence-gated promotion — lessons graduate into infrastructure

A lesson observed once lives in `learnings/`. When it recurs / proves stable
(suggest: 3 confirmed applications or Kam says "always"), it gets **promoted**:

- interaction rules → `identity/` (procedural memory), or
- mechanical rules → *enforcement*: launcher checks, hooks, CLAUDE.md lines —
  remembered rules can be missed; enforced rules can't.

Original file stays, marked `status: promoted` with a link. The gate prevents
one-off remarks hardening into permanent rules (over-personalization guard).

## 5. Async teaching channel — Kam can teach without a session open

Today lessons only land when we're both here. Proposal: a **`lesson` label in
Linear** — any issue/comment Kam tags gets ingested at next boot: reflection
written, learning filed, issue closed with a note of what changed. Extends
naturally to WhatsApp/mail once those channels exist (WED-10/11, WED-8).
"Tasks for contemplation" get the same treatment plus dedicated thinking time in
the 06:00 slot — reflection presented at the morning briefing, not just filed.

## 6. Case files — episodes, not only rules

For judgment-heavy lessons (tone, taste, when-to-interrupt), abstract rules
underfit. Capture short episodes in the learning file itself: *situation → what I
did → Kam's reaction → what the right move was.* Worked examples steer future
behaviour better than principles alone; this is how the emotional/functional
side of the parent–child model — not just the technical — accumulates.

## Order of adoption

| # | What | Cost | When |
|---|---|---|---|
| 1+2 | Ledger + wrap-up retro | one file + ritual edit | today, on approval |
| 6 | Episode format in lesson template | template tweak | today, on approval |
| 4 | Promotion gate | discipline + occasional promotion work | starts organically |
| 3 | Weekly dreaming + audit | needs WED-16 scheduler | with the 6am rhythm |
| 5 | `lesson` label ingestion | small boot-ritual addition | this week |

Open design point parked for the architecture doc (WED-5): at what brain size we
switch from full-read boot to index-first (Rhodes VAULT-INDEX pattern). Not yet —
we're at 5 lessons.
