---
course: Tactical Agentic Coding (agenticengineer.com)
lessons: 02, 03, 04
captured: 2026-08-03
transcripts: transcripts/lesson-02…, lesson-03… (verbatim on disk); lesson-04 harvested + read, re-harvest in ~2 min via the documented pipeline
codebases: /Volumes/DevMASTER/!CODING/Agentic Coding/Resources and Lesson Material/tac-2, tac-3, tac-4
---

# Lessons 02–04 — the substance of the course so far

## Lesson 02 — The 12 Leverage Points (47 min)

**Framework:** the software development lifecycle, compressed to five steps, is
the stable frame ("bet on what doesn't change").

**Tactic 2: adopt your agent's perspective.** *"Your agent is brilliant, but
blind."* Every session starts blank — no memory, no awareness beyond what you
give it. So engineering shifts from what you can do to what you can teach an
agent to do.

**The 12 leverage points**, split in two:
- **In-agent (the core four, always present):** context · model · prompt · tools.
- **Through-agent (external, flow into the context window):** **standard out ·
  types · documentation · tests · architecture · plans · templates · ADWs.**

Worked examples: give the agent the *running* start script so it reads stderr
itself (he fixes a real SQL-escaping bug this way — "stop looking at error
messages"); types as "information-dense keywords" that trace data flow through
a codebase; architecture/file layout as something that "stacks up for or
against" the agent; a `/prime` slash-command to ramp a fresh agent quickly.

**The four KPIs — the genuinely useful bit:**
| KPI | Direction | Meaning |
|---|---|---|
| **Presence** | ↓ to zero | how much you must be at the keyboard |
| **Size** | ↑ | how much work one prompt can carry |
| **Streak** | ↑ | consecutive successes without intervention |
| **Attempts** | ↓ to one | tries needed per prompt |

*"Not guess, not vibe — this is how we know we're improving."* Each KPI is
improved by pulling one or more leverage points.

## Lesson 03 — Success is Planned: template your engineering (47 min)

**Tactic 3: template your engineering.** Plans are prompts scaled; great
planning is great prompting. Encode engineering practice into *reusable prompt
templates* stored in the codebase (`.claude/commands/`), one per **class of
work — chore / bug / feature** (his point: these are different classes and
deserve different templates; you can go further — a chore template for DB
migrations, a bug template for a specific subsystem).

Mechanics shown: **meta-prompting / higher-order prompts** — a prompt whose
output is another prompt. `/feature` is a template that *writes the plan*; the
plan then becomes the prompt for `/implement`. Plans get saved into the
codebase as artifacts ("staging environments for code") that team and agents
can reference and improve.

Also introduced: **self-validation steps inside the plan** (validation commands
the agent runs itself) — the seed of lesson 5's closed loops. And running the
planner via `claude -p` in programmable mode, streaming output to a JSONL file.

## Lesson 04 — AFK Agents / ADWs (46 min) — **the most important lesson so far**

**Tactic 4: stay out the loop.** Distinguishes *in-loop* agentic coding
(prompting back and forth at the keyboard) from **out-loop** (fire a prompt at
a pipeline, walk away — "or maybe you were never there in the first place;
maybe you sent the prompt from your phone").

**The ADW — AI Developer Workflow:** *"a reusable agentic workflow that
combines code, agentic prompts, and agents to deliver results autonomously."*
It is the **agentic layer around a codebase** — the synthesis of deterministic
code and non-deterministic agents. Lives in its own directory (`adws/`) beside
the prompt templates; the application code is untouched.

**PETER — the four elements of AFK agents:**
| | Element | His example |
|---|---|---|
| **P** | Prompt input | GitHub issue (title + body = the prompt) |
| **T** | Trigger | GitHub webhook (or a local script; cron) |
| **E** | Environment | a dedicated Mac mini the agent fully controls |
| **R** | Review | GitHub pull request |

**The demo, end to end:** create an issue → webhook fires → agent on its own
machine classifies the issue (chore/bug/feature) → creates a branch → planner
agent writes a spec → committer commits → implementer agent (bigger model)
builds from the plan → PR opened, with live progress posted as issue comments.
Chore: ~5 min. Feature (JSONL upload support): ~17 min, one shot, tests included.

**Engineering details worth stealing:**
- **Health-check command** run before any workflow (env vars, repo, agent
  reachable) — fail fast on misconfiguration.
- **No ad-hoc prompt strings in code** — every prompt is an isolated file so it
  can be improved and versioned.
- **Model tiering per step** — cheap model for classify/branch, strongest model
  for plan and implement.
- **Observability is mandatory**: per-session logs (via hooks), per-agent logs,
  live issue comments. *"It doesn't matter if our agent can solve every problem
  if we don't know that it's solved."*
- **Fix the system, not the issue:** *"every time you miss something, you don't
  fix the issue — you fix the system that caused the issue"* (fix the template
  or the ADW).
- Start small: chores first, then bugs, then features, as trust builds.
- Explicit argument for owning your pipeline rather than using Devin/Jules/
  Codex-style cloud agents: they can't encode *your* practices for *your*
  codebase.

---

# Verdict against Kam's filter — what to take, what to leave

**TAKE — genuinely valuable, not already ours:**
1. **The ADW as a named unit** with its own directory beside (not inside) the
   app — a clean way to structure the agentic layer we're building ad hoc.
2. **PETER** — the checklist for any AFK setup. Directly maps onto what we
   already half-have (see below).
3. **The four KPIs** — the best thing in the course. We have a correction
   ledger measuring *my* learning; we have no measure of *delegation quality*.
   Presence/size/streak/attempts is exactly that, and it is measurable from our
   existing Linear + wrap-email data.
4. **Work-class templates** (chore/bug/feature, and domain-specific variants) —
   stronger than our single delegation-brief format.
5. **Health-check before a workflow runs** — belongs in our delegation protocol.
6. **Prompts as versioned files, never inline strings.**
7. **"Fix the system, not the issue"** — the same principle as our ledger's
   weight-2 rule ("diagnose why the lesson didn't fire"), stated for workflows.

**LEAVE — would take us backwards:**
1. **"Stop coding" as absolute** (see lesson-01 notes) — keep verification.
2. **Yolo/`--dangerously-skip-permissions` everywhere.** He runs it constantly
   and waves it off ("it's in its own environment"). Our projects touch live
   Azure tenants, real Cardano wallets, client data. Keep permissions.
3. **Auto-merge culture.** His flow ends at a PR — good — but the pace assumes
   light review. Secuura's KS-535-class bugs (a failed anchor still reporting
   success) are exactly what a skim-review misses.
4. **Presence → zero as a universal goal.** For *chores*, yes. For decisions,
   security-sensitive changes, and anything touching prod, Kam's presence is
   the control, not a KPI to minimise. Adopt the KPI per work-class, not
   globally.
5. **"If you are not wrong now, you will be."** Rhetoric, not evidence. Our
   day-3 experiments showed the opposite of blanket claims: measure first.

**ALREADY OURS (validating, not new):** programmable `claude -p` (coordination
harness), delegation with verifier + round cap, prompts-as-files (skills),
observability via Linear receipts + wrap emails, "build the system that builds
the system" (learning loop v2).
