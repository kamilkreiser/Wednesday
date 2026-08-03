# Coordination Protocol v1 — how Wednesday delegates and coordinates

Date: 2026-08-03 · Status: v1, for Kam's review · Closes the WED-24 study
Sources: TreeQuest deep study (`2026-08-03_treequest-study-notes.md`, days 1–3),
two-schools analysis (`2026-08-03_two-schools-analysis.md`), Kam's approvals of
WED-20–23. Operational form: `0_Brain/skills/delegation-protocol.md` (the ritual)
+ `0_Brain/projects_index/scoreboard.md` (the track record).

---

## What this protocol is

AB-MCTS, read as management theory, makes three decisions from evidence instead
of instinct: **(1) is another attempt worth it, (2) fresh angle or refine the
best draft, (3) who takes the attempt.** This protocol transfers those decisions
to how I coordinate all execution channels — project agents (Claude sessions in
their own folders, per manage-don't-do), model seats (gpt, claude, haiku, later
kimi/open-source), and the break-glass search harness itself.

## The eight rules

**R1 — Verifier first.** No delegation without a checkable definition of done:
tests > build/typecheck > structured checklist > Kam's accept/reject. Every
attempt gets a score in [0,1]. If I can't say how it will be verified, the brief
isn't ready. *(Two-schools law: repetition against a verifier is the magic.)*

**R2 — One strong pass is the default.** Route to the best channel for the job
and expect one attempt + verification. Day-3 empirics: four runs, three task
designs, zero branches needed — even weak models one-shot well-specified work.
Extra attempts are bought only by evidence of failure.

**R3 — Refine at most 3 rounds.** Refinement prompts carry the verifier's
failure detail (the arc2 pattern). Literature and practice agree gains plateau
by round 2–3; after 3, escalate (to me rethinking the brief, or to Kam) — never
loop. *(WED-21, now operational.)*

**R4 — Wider-vs-deeper is an explicit, recorded decision.** On a partial score:
**deeper** (refine best attempt) when the failure is local — named failing
tests, a bounded bug — and score ≥ ~0.5; **wider** (fresh attempt, usually a
different channel) when the approach itself is wrong, score is low, or two
refines haven't moved the number. Recorded in the task log so the decision
quality itself becomes reviewable.

**R5 — Track record routes.** The scoreboard (`projects_index/scoreboard.md`)
keeps per-channel, per-work-class scores. Routing consults it; the harness's
`priors` hook consumes it. Frequency-weighting applies to channels exactly as
the ledger applies to me: repeated failure of a channel on a work class (w≥3)
retires it for that class until something changes.

**R6 — Search is break-glass.** The AB-MCTS harness
(`2_Project_Files/coordination/`) is invoked only when ALL hold: (a) an
automatic scorer exists (test suite), (b) ≥2 strong-channel attempts have
failed, (c) the problem matters enough for tens of model calls. Budget set
before launch; Kam informed at the briefing either way. *(WED-23, empirically
grounded by day 3.)*

**R7 — Council at judgment checkpoints only.** Three seats + chairman for
architecture/security/migration decisions (WED-22). Councils advise; tests or
Kam decide. Never for execution.

**R8 — Failures score zero and never crash the flow.** A broken channel (dead
API, exhausted subscription, wedged session) is recorded as a 0 with a note,
and routing carries on around it — the day-3 crash-turned-fix, as policy.

## Channel inventory (2026-08-03)

| Channel | What it is | Cost | Verified |
|---|---|---|---|
| Project agents | Claude sessions in each project folder; I brief, they execute | Max sub | standing |
| `gpt` | GPT-5 via Codex CLI (ChatGPT sub) | $0 marginal | today, 2 tasks |
| `claude` | claude -p (Sonnet) | Max sub | today |
| `haiku` | claude -p (Haiku) — cheap checker/drafter | $0 marginal | today, 2 tasks |
| `gpt-low` | Codex, effort none — cheap checker | $0 marginal | wired, untested |
| Harness | AB-MCTS over seats + verifier | seats × budget | today, 4 runs |
| (future) | Kimi K2 / open-source seat | API ¢ / local | WED-26 |

## Where each pattern applies

- **Delegated project work** → R1–R5 via the brief standard (skill file). The
  project's own agent is the channel; scores come from its verified results.
- **Quick internal work** (drafts, research, briefs) → R2 with a cheap seat +
  my own review as verifier; R4 if it misses.
- **Validation** (WED-20 pilot, once Kam picks the project) → one-writer/
  different-reviewer: `gpt` reviews Claude's diffs; `haiku`/`gpt-low` write
  spec-only adversarial tests.
- **Stuck hard problems** → R6 harness, budget agreed first.
- **Big decisions** → R7 council.

## Review cadence

The weekly consolidation reviews: scoreboard trends, wider-vs-deeper decision
quality (did deeper pay when chosen?), any channel at w≥2 failures, and whether
R2's default held (how often extra attempts were actually needed). Protocol
changes propose here, adopt after Kam's nod, and are validated by later
evidence per the DGM guard — adoption alone is not improvement.

## v2 candidates (parked)

Per-task-class priors once the scoreboard has volume · rubric verifiers for
non-code work (needs the noisy-verifier guard) · harness `ask_batch` for
parallel seats · a real-problem first outing for the harness (pairs with the
WED-20 pilot choice).
