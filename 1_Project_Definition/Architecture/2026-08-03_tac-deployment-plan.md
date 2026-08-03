# TAC deployment plan — what we adopt, in what order

Date: 2026-08-03 · Status: proposal for Kam (Linear: WED-29…33)
**UPDATED 2026-08-03 (evening): all 8 lessons + all codebases now reviewed.**
Notes in `0_Brain/reference/tac-course/` (lesson-01, lessons-02-04,
lessons-05-08 incl. the code review). Filter applied throughout: Kam's *"use
what is good, not what will take us backwards"*.

## The honest headline

The course's core idea — **build an agentic layer around each codebase: prompt
templates per work-class, composed into AI Developer Workflows, triggered
externally, reviewed via PRs** — is genuinely good, and it is the missing piece
between what we have (a delegation protocol and a coordination harness) and
what Kam wants (phone-driven work, agents talking to agents, escalate-only).

Two things we should NOT import: his permission posture (`yolo` everywhere) and
his framing of human presence as pure waste. Our verification culture is the
reason Secuura's failed-anchor and cosmetic-erasure bugs got caught; presence
is a control for risky work, not a KPI to zero out.

## P1 — Agentic KPIs on delegation (adopt now, cheapest, highest signal)

Add the four KPIs to the delegation scoreboard, measured per delegated task
from data we already produce (Linear + wrap emails):
- **Presence** — number of Kam interventions required (target ↓, *per work
  class*: chores → 0; decisions/security → unchanged, presence is correct).
- **Size** — scope one brief carried end-to-end (↑).
- **Streak** — consecutive delegations completed without intervention (↑).
- **Attempts** — refine rounds used, cap 3 (↓ toward 1).

Why first: zero build cost, and it gives the delegation protocol the numeric
health metric it currently lacks (the correction ledger measures *my* learning;
this measures the *system's*). Feeds the weekly consolidation review.

## P2 — Work-class templates for briefs (adopt now)

Replace the single delegation-brief format with **chore / bug / feature**
variants, plus room for project-specific ones. Each carries its own definition
of done and verifier expectations. Ours already mandate a verifier and a round
cap — the course adds the *classification* idea, which is what lets an agent
route work automatically later (P4).

Deliverable: `0_Brain/skills/brief-templates/{chore,bug,feature}.md`.

## P3 — Health check + prompts-as-files (adopt now, small)

- Every workflow/delegation starts with a **health check** (env, credentials,
  target reachable, correct tenant) that fails fast — this is a natural home
  for the tenant-verification rule that already bit us today (stale tenant in
  Secuura's launcher).
- **No ad-hoc prompt strings**: every reusable prompt lives in a versioned file.
  We mostly do this (skills); make it explicit in the protocol.

## P4 — First ADW pilot (build, after 5–8 are reviewed)

One project, one workflow, smallest useful scope: **chore-class only**.
- **P**rompt input: a Linear issue labelled `adw` (we already have Linear
  everywhere and the `lesson`/`proposal` label convention working).
- **T**rigger: manual script first (`uv run adws/plan_build.py <issue>`), webhook
  later.
- **E**nvironment: the project's own launcher-scoped session — **not** yolo
  mode; permissions stay on for anything touching Azure/wallets/prod.
- **R**eview: PR + our existing cross-model review pilot (WED-20) as the
  automated first pass, Kam approving the merge.

Candidate project: the **Secuura extranet** (already the WED-20 pilot; low blast
radius, auto-deploys only from main which we gate) or **Wednesday's own repo**
(zero client risk — arguably the right first target).

## P4b — Parallel isolation (new, from lesson 7 code)

Once P4's single ADW works, add the mechanics that let several delegated jobs
run at once without collisions: a **state file per run**
(`agents/<run_id>/state.json`, the fields carried between steps), a **git
worktree per run** (`trees/<run_id>/`), and **per-instance port allocation** so
each isolated copy can actually run the app. Reference implementations:
`tac-7/adws/adw_modules/{state,worktree_ops}.py`.

## P4c — Fleet observability feed (new, from lesson 8 app3)

The read-only "watch both sides" view we wanted after the CoAgent review, now
with a proven architecture: **Claude Code hooks → HTTP → SQLite → WebSocket →
web dashboard**. Renders live agent activity across the fleet without adding any
attention tax to the agents themselves. Pairs with the mail/Linear receipts we
already produce.

## P5 — Phone-driven co-work (Kam's point 3) — **mechanism now identified**

Lesson 8's app2/app4 are exactly this pattern, and we can build it before
lessons 9–14: a **task board as prompt input**, polled by a cron trigger that
**atomically claims** a task (flip status first, so no double-work), runs the
workflow in an isolated environment, and writes status/results back — with an
explicit **"HIL Review" column as the escalation gate**.

Our version: **Linear replaces Notion** (already the source of truth, already on
Kam's phone), the `adw` label is the trigger, Wednesday polls and dispatches,
project agents execute, and anything ambiguous/decision-shaped moves to a
`needs-Kam` state instead of proceeding. That is precisely Kam's brief:
*work back and forth with the agents, escalate only for approval, ambiguity, or
a decision.*

Sequencing note: build it AFTER P4/P4b prove out, and still review lessons 9–14
(Multi-Agent Orchestration, Agent Experts) before scaling it — but the design no
longer waits on them.

## Sequencing

| # | Item | Cost | When |
|---|---|---|---|
| P1 | KPIs on the scoreboard (ref impl: `tac-7/.claude/commands/track_agentic_kpis.md`) | ~1 h | now |
| P2 | Work-class brief templates | ~2 h | now |
| P3 | Health check + prompts-as-files rule | ~1 h | now |
| ✅ | Lessons 1–8 + all codebases reviewed | done | 2026-08-03 |
| P4 | First ADW pilot (chore-class, own repo) | ~1 session | next |
| P4b | State file + worktree + port isolation | ~1 session | after P4 |
| P4c | Fleet observability feed (hooks → dashboard) | ~1 session | opportunistic |
| P5 | Phone co-work: Linear board → claim → dispatch → HIL gate | ~1–2 sessions | after P4/P4b |
| — | Lessons 9–14 (orchestration, agent experts) | ~1–2 sessions | before scaling P5 |

Nothing here changes another project's files without Kam's per-change approval
(hard rule 1); P4's implementation is executed by the target project's own
agent from a brief I write.
