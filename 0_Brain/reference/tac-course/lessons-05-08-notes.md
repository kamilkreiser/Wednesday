---
course: Tactical Agentic Coding
lessons: 05, 06, 07, 08 (+ codebase review tac-4…tac-8)
captured: 2026-08-03
method: full transcript for L8 (Kam's priority); framing + recap for L5–L7, with mechanics read from the actual code (Kam's steer: "code builds, spend most time on lesson 8")
---

# Lessons 05–08 — the advanced half

## Lesson 05 — Close The Loops (54 min) · Tactic: **always add feedback loops**

**The question that unlocks it:** *"Given a unit of valuable work that's
production-ready, how would you, the engineer, test and validate this work?"*
Answer it for every class of work in your codebase, **encode each answer as a
command or tool call**, and the agent can self-validate.

He enumerates the feedback loops engineers already run by hand — linter, unit
tests, UI tests, CI, build/compile, log checks (Datadog), error checks (Sentry),
custom evals, LLM-as-judge, and "you probably opened the browser and clicked
through your feature." All of these are handoff candidates.

Claim worth keeping: **the value of a test is multiplied by the number of agent
executions in your codebase** — which is a genuinely good argument for tests
that doesn't depend on any AI hype.

Closing the loop = agent executes → calls a validation command → takes the
feedback → keeps building until the feedback is positive.

## Lesson 06 — Let Your Agents Focus (57 min) · Tactic: **one agent, one prompt, one purpose**

**Review ≠ test.** He frames each SDLC step as a question:
plan *"what are we building?"* · build *"did we make it real?"* · test *"does it
work?"* · **review *"is what we built what we asked for — now prove it"*** ·
document *"how does it work?"* Grouping test and review together is, in his
words, a mistake in the age of agents. (This is the strongest idea in the
lesson and maps exactly onto our verifier-vs-acceptance distinction.)

**Against giant context windows:** context pollution/overloading degrades
agents; specialised single-purpose agents free the window, let the agent focus,
and — the important side effect — **make every prompt individually reproducible
and improvable, i.e. an eval surface.** `/compact` is called "a band-aid;
if your agent is compacting, it is losing information."

**Document step exists for future agents**, not for humans — documentation is
context for the next agent run.

Also demonstrated (in code, `tac-6`): review via **Playwright MCP screenshots**
compared against the spec, with issue severity `skippable | tech_debt | blocker`
returned as strict JSON.

## Lesson 07 — ZTE: The Secret (53 min) · Tactic: **target zero-touch engineering**

**The velocity scale — three levels:** in-loop → out-loop → **ZTE (zero-touch
engineering)**. The "secret" is really two claims: (1) it's the *primitives and
their composition* that matter, not the SDLC or any tool; (2) at some point
**human review becomes the bottleneck, not the safety net**, and you drop it.

**Parallelism via git worktrees** (`trees/<adw_id>/`), each with its own
allocated ports and a `/install_worktree` step — five issues fired at once, each
handled by an isolated pipeline on one machine. He is explicit that worktrees
are incidental: containers/VMs work equally well; what matters is isolation.

Also introduced: **model sets** (`base` vs `heavy`) chosen per workflow, and
workflow variants — `adw_sdlc_iso`, `adw_patch_iso`, `adw_ship_iso`,
`adw_sdlc_zte_iso`. He ends by shipping a change **to production with no human
review**, from a single prompt.

## Lesson 08 — The Agentic Layer (63 min) · Tactic: **prioritize agentics**

The culmination, and the most useful lesson for us.

**The agentic layer defined:** the combination of *deterministic code* (the
`adws/` scripting layer) and *non-deterministic agentic prompts* — a ring
around your application layer that operates the codebase on your behalf. He
recommends **more than half your engineering time be spent on the agentic layer**.

**Minimum viable agentic layer** — three directories, nothing more:
```
specs/              plans the agents follow
.claude/commands/   the reusable/meta prompts
adws/               the workflow scripts (uv/bun/shell — language irrelevant)
```
**Scaled version** adds: `.claude/hooks/`, `adw_modules/` (agent, state, git_ops,
github, workflow_ops), `adw_triggers/` (webhook, cron, custom), `adw_tests/`,
`agents/<adw_id>/` (per-run state + artifacts + logs), `trees/` (worktrees),
`ai_docs/`, `app_docs/`, `.mcp.json`.

**The five example applications** (all in `tac-8-2/`) — this is the part worth
mining:
1. **agent_layer_primitives** — the empty starter: prime, start, implement, one
   template meta-prompt, one ADW that just calls an agent.
2. **multi_agent_todone** — a **shared `tasks.md` task board** with status
   markers (`[]` pending, `[🟡, adw_id]` running, `[✅ hash, adw_id]` done,
   `[❌] // reason`, `[⏰]` blocked-by-dependency); a **cron trigger polls every
   ~5 s**, spawns parallel agents across worktrees, respects blocking, and
   writes status back. Per-task tags choose model and workflow
   (`{opus, adw_plan_implement_update_task}`).
3. **out_loop_multi_agent_task_board** — **observability**: Claude Code hooks →
   HTTP POST → Bun server → SQLite → WebSocket → Vue dashboard, live view of
   many concurrent agents.
4. **agentic_prototyping** — **Notion board as prompt input**: cron polls Notion
   every 15 s, claims a task by flipping status (prevents duplicate work),
   creates a worktree, runs a framework-specific `/plan_*` meta-prompt, builds,
   writes results + commit hashes back to Notion. Columns: Not started → In
   progress → **HIL Review** → Failed → Done.
5. **nlq_to_sql_aea** — **agents embedded inside the running application**
   (`/aea` spins up an agent you converse with in-app, multiple at once).

**PETER → PETE.** Once ZTE is reached he drops the **R**eview: prompt input,
trigger, environment — no review.

**The single guiding question** (the whole course compressed):
> **"Am I working on the agentic layer, or the application layer?"**

Closing framing: "the commoditization of implementation"; value moves to system
design, architecture, encoding domain expertise, quality control/validation
systems, and creative problem decomposition.

---

# Code review — the nuggets (tac-4 → tac-8)

Reading the code was higher-yield than the videos. Concrete things worth taking:

1. **`track_agentic_kpis.md`** (tac-7) — a working KPI implementation. Attempts
   = count of plan/patch workflows re-run for one issue; **streak = consecutive
   runs with attempts ≤ 2**; size = plan lines + `git diff --shortstat`;
   presence = average attempts. Writes `app_docs/agentic_kpis.md` with a summary
   table and a per-run table. *We can adapt this almost directly for P1.*
2. **`ADWState`** (`adw_modules/state.py`) — one JSON per run at
   `agents/<adw_id>/adw_state.json`, whitelisted fields, passed between
   composable scripts via stdin/stdout, `all_adws` list recording every workflow
   that touched the issue. This is what makes workflows chainable *and*
   resumable — and it's exactly the shape of our delegation tickets.
3. **`worktree_ops.py`** (tac-7) — worktree per run under `trees/<adw_id>` +
   **unique port allocation per instance** so parallel agents can each run the
   full app. The port allocation is the non-obvious bit most people miss.
4. **`resolve_failed_test.md`** — a beautifully scoped self-healing prompt:
   reproduce with the *provided* execution command, fix minimally, re-run **only
   that test**, don't touch anything else. Narrow blast radius by construction.
5. **`review.md`** (tac-7) — spec-vs-implementation review with Playwright
   screenshots (1–5, numbered, saved to a per-agent dir), severity taxonomy
   (`skippable`/`tech_debt`/`blocker`), strict JSON output for machine parsing.
6. **`health_check.py` / `health_check.md`** — verify env, repo, agent
   reachability *before* a workflow starts.
7. **Slash-command library as the unit of reuse** — ~25 commands per project
   (`chore`, `bug`, `feature`, `implement`, `test`, `test_e2e`, `review`,
   `document`, `patch`, `commit`, `pull_request`, `classify_issue`,
   `generate_branch_name`, `prime`, `install`, `cleanup_worktrees`…). Everything
   the workflow does is a named, versioned prompt file.
8. **Model tiering per step** — cheap model to classify/branch, strong model to
   plan/implement; `model_set` carried in state.

---

# Verdict: what we take, what we refuse

**TAKE (high value, low risk):**
- The KPI implementation (P1) — now with a concrete reference implementation.
- **Review as a distinct step from test** — "is this what we asked for, prove
  it" with evidence attached. Fits our verifier culture perfectly.
- **One agent, one prompt, one purpose** — validates our subagent pattern and
  argues against giant shared contexts. Also the eval argument: single-purpose
  prompts are individually improvable.
- **The three-directory minimum viable agentic layer** — a clean, cheap starting
  shape for any project we pilot in.
- **State-file-per-run + worktree isolation + per-instance ports** — the
  mechanics for running several delegated jobs at once without collisions.
- **Task-board-as-prompt-input with atomic claiming** (app2/app4) — this is
  precisely the mechanism for Kam's phone co-working: Linear replaces Notion,
  claiming prevents double-work, HIL Review column is the escalation gate.
- **Hooks → event stream → dashboard** (app3) — the fleet feed we independently
  wanted after the CoAgent review, with a proven architecture.
- `resolve_failed_test`-style narrow repair prompts; health checks; severity
  taxonomy for review findings.

**REFUSE (would take us backwards):**
1. **ZTE as a goal for client work.** Shipping to production from one prompt
   with no human review is the opposite of our hard rules. Our recent evidence:
   Secuura's failed-anchor bug (a workflow reporting success while the chain
   failed) and cosmetically-anonymised GDPR data — both would have sailed
   through an unreviewed pipeline. ZTE is *conceivable* for low-risk chores in
   our own repo; it is not a target for Datasec/Secuura.
2. **`--dangerously-skip-permissions` as default**, and especially his lesson-6
   suggestion of running *entire workflows* in yolo mode to production. No.
3. **Dropping the R from PETER.** We keep Review permanently. What we adopt is
   *cheaper* review (automated evidence, screenshots, severity triage) so Kam's
   attention goes to what matters — not review's removal.
4. **"Presence to zero" as a universal target.** Per work-class only; presence
   on decisions and security is a control, not waste.
5. **Compact-is-always-bad.** Ours is a managed handoff to disk, not information
   loss (see our context-discipline lesson) — his critique doesn't apply to a
   system that writes durable state.
