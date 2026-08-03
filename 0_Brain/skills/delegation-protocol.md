# Delegation protocol — the ritual for every delegated task

Operational form of Coordination Protocol v1
(`1_Project_Definition/Architecture/2026-08-03_coordination-protocol-v1.md`).
Implements WED-21 (do-check-refine standard) + the AB-MCTS transfers (WED-24).
Applies to: project agents, model seats, and my own substantial work products.

## Before writing any brief: validate the model

My index cards, boards digest and learnings are a **mental model, not a source
of truth** (Kam-endorsed 2026-08-03). Before a brief goes out, every fact in it
that names a file, path, flag, tenant, ticket state or system behaviour is
checked against the live source. Briefs must not assert stale facts — a
confident brief built on drift sends another agent down it.

## Choosing a sub-agent's context (Kam, 2026-08-03)

**Load sub-agents fully — for now** (Kam: we have the tokens; an
under-informed agent costs far more than tokens do). Selective loading is a
lever to pull when a situation requires it, not the default.
Still prefer **file paths over pasted content** — not to ration tokens, but
because paths stay current while pasted copies go stale.
**The harder the task, the narrower the AGENT — not its context:** split
complex work into specialised agents with a tight *purpose*, each fully
briefed. See [[../learnings/2026-08-03_context-loading-split]].

## The brief (before anything is delegated)

Every brief contains, explicitly:
1. **Task** — what, in plain language.
2. **Context as file paths**, not pasted content.
3. **Constraints** — scope, tenant/account rules, what must not change.
4. **Definition of done + verifier** — how the result is checked and scored
   0–1 (tests > build/typecheck > checklist > Kam). No verifier → brief not ready.
5. **Round cap** — max 3 refinement rounds, then escalate.

## The loop (per task)

1. **Route** using `../projects_index/scoreboard.md` (best channel for this
   work class; respect retirements).
2. **One attempt → verify → score → log** (R2: expect this to be enough).
3. On partial score, decide and RECORD **wider vs deeper**:
   - deeper: failure is local (named failing checks) and score ≥ ~0.5 —
     refine, feeding the failure detail back;
   - wider: approach wrong, score low, or 2 refines flat — fresh attempt,
     usually a different channel.
4. After 3 rounds without done: **escalate** (rethink the brief, ask Kam, or —
   if scorer exists + it matters — propose a break-glass harness run with a
   budget).
5. **Close out**: final score to the scoreboard; outcome to Linear; channel
   failures logged as 0 with a note (never crash the flow).

## Scoreboard discipline

- One line per (channel × work class); update at close-out, newest evidence
  first. Repeated channel failure (w≥3) retires it for that class — note why.
- Weekly consolidation reviews trends + whether my wider/deeper calls paid.
