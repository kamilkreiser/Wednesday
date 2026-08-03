---
course: Agentic Horizon (extended lessons 9–14, same author/platform as TAC 1–8)
captured: 2026-08-03
method: full framing + recap per lesson; 12 & 13 read most deeply (Kam's stated interest: multi-agent management + agents that learn)
---

# Lessons 09–14 — Agentic Horizon

## 09 — Elite Context Engineering (73 min) · **the R&D framework**

**Only two ways to manage a context window: Reduce and Delegate.** Everything
else is a technique inside those two buckets.

- **Measure first:** `/context` in Claude Code, plus a token counter in the IDE.
  "What gets measured gets managed."
- **Don't preload MCP servers.** His example: 24K tokens (12% of a 200K window)
  consumed at boot by MCP definitions he wasn't using. Delete the default
  `.mcp.json`; launch with `--mcp-config <file> --strict-mcp-config` when a
  specific server is actually needed.
- **Context priming over always-loaded memory files.** His sharpest argument,
  and it is aimed squarely at `CLAUDE.md`: *"It's incredible for one reason —
  it's a reusable memory file always loaded into your context window. It's
  terrible for exactly the same reason."* Memory files only grow, eventually
  carry irrelevant context, and in the worst case **contradictory** context.
  Replace with a `/prime` slash command that loads what *this* task needs.
- **Sub-agents = partially forked context.** A sub-agent's system prompt is not
  added to the primary agent's window, and its work (e.g. web scraping 10 docs
  at 3K tokens each) stays out of the primary. That's the **D** in R&D.

**⚠ This lesson directly challenges our own design** — see "Honest challenge to
us" below.

## 10 — Agentic Prompt Engineering (57 min) · **seven prompt formats, composable sections**

Framing: *"The prompt is the fundamental unit of engineering"*, written for a
**stakeholder trifecta — you, your team, your agents.**

Prompts are built from **composable, swappable sections**, ranked by usefulness
and skill required: `title` · `metadata` (tool/model restrictions, argument
hints) · `purpose` · `variables` · **`workflow`** · `report` (output format —
JSON/YAML/structure) · `relevant files` · `codebase structure`.

His ranking: **`workflow` is the single most useful section** (S-tier
usefulness, moderate skill) — a sequential list of steps for the agent to
execute. `report` controls output format and is what makes prompts
machine-composable. `metadata` is the least valuable.

Progression: level 1 high-level ad-hoc prompt → level 2 **workflow prompt** →
up through variables, templates, meta-prompts. Practical rule offered:
**"three times marks a pattern"** — the third time you do something by hand,
write it as a prompt file.

## 11 — Building Domain-Specific Agents (67 min) · **custom agents on the Claude Agent SDK**

Progression every engineer follows: *base agents → better agents → more agents
→ custom agents*. The argument for custom: off-the-shelf tools "are built for
everyone's codebase, not yours."

- **The system prompt is the most important element of a custom agent, with
  zero exceptions** — his "Pong agent" demo replaces Claude Code's system prompt
  with three lines and the agent will only ever reply "Pong", no matter the
  input. Point made: *replacing the system prompt throws away everything the
  Claude Code team built.* Be careful.
- SDK shape: set options → query → handle response blocks (message blocks, tool
  blocks, result message) → log.
- **In-memory MCP servers** via `create_sdk_mcp_server` — custom tools defined
  with a decorator; the *tool description* is what teaches the agent when to use
  it.
- Model downgrading per agent (Haiku for simple agents) — same tiering idea as
  the ADW `model_set`.
- Custom agents also **protect** — restricting which tools an agent can call.

## 12 — Multi-Agent Orchestration: the O-Agent (56 min) · **most relevant to Wednesday**

**The orchestrator agent = the single-interface pattern applied to a fleet of
agents.** Three pillars, and he insists all three are required:
1. **Orchestrator agent** — one unified interface to all your agents.
2. **CRUD for agents** — create/command/inspect/delete agents at will = agents
   at scale.
3. **Observability** — real-time monitoring of status, context, cost, results.
   *"If you can't measure it, you can't improve it. If you have 10 agents doing
   the wrong thing, does it matter that you have 10?"*

Architecture: Vue/Pinia front end · HTTP + WebSocket · **Claude Agent SDK** for
the agents · **Postgres** for all state. Explicitly an **out-loop PETER system**
(Cmd+K prompt input → HTTP trigger → local environment → observability as
review), deployed so he can reach it from any device.

Key design points worth stealing:
- **The orchestrator is itself a custom agent, specialised at managing agents** —
  and crucially it **does not continuously read the logs**; its own context
  window is protected. It queries state when asked.
- **Result-oriented reporting:** every agent reports **consumed assets and
  produced assets**, with one-click-into-the-editor from any result.
- Per-agent view of the **core four** (context %, model, prompt, tools) — you
  always know each agent's state.
- Honest admission: **ADWs are not yet plugged into the orchestrator** — the
  deterministic-code layer is the missing piece he says he's building.

## 13 — Agent Experts (63 min) · **agents that actually learn** — most relevant to my brain

**The problem:** *"Traditional software improves as it's used. Agents don't.
Your agents forget, and that means your agents don't learn."*

**Agent expert = a self-improving template meta-prompt**, running an
**act → learn → reuse** loop, updating its own knowledge *at runtime with no
human in the loop*.

**The single best idea in the whole course:** the expertise file is a
**mental model, NOT a source of truth**.
> *"You don't have a source of truth in your mind. You have a mental model — a
> data structure you constantly update."* The code is always the source of
> truth. So the expert prompt's workflow is: **read the expertise file first →
> validate its assumptions against the actual code → only then report.**
He deliberately repeats the validation instruction twice in the prompt.

**Meta-agentics** — the building blocks: **meta prompts** (prompts that write
prompts), **meta agents** (agents that build agents), **meta skills** (skills
that build skills). *"There is no codebase I create that does not have
meta-agentics."*

**When to build an agent expert:** the area is complex and evolving; agents keep
getting it wrong in that specific area (high error rate); the codebase has grown
unique.
**When NOT to:** the problem doesn't change over time; it's a fresh generic
codebase; **or you yourself don't have a mental model** — *"if you don't
understand the problem, do not build an agentic expert. You will build an expert
that can't solve the problem, because you can't."*

He again rejects memory files (always loaded, "can't detach when the time is
right") in favour of an explicit, dedicated expertise file the agent is told to
consult.

## 14 — The Codebase Singularity (67 min) · the finale

**Three classes of agentic layer**, each with grades within it, so you can place
yourself and see the next step:
- **Class 1** — thinnest possible: a `prime` prompt and/or memory files, small
  amount of code. If you have that, you technically have an agentic layer.
- **Class 2** — workflows/ADWs composed over prompt templates.
- **Class 3** — orchestrator-driven, out-loop, with the orchestrator able to
  **kick off ADWs directly** (which closes the gap he admitted in lesson 12).

Structural advice: **bundle the agentic layer around ALL of a product's
repositories/applications**, not one — so agents can see everything related to
the product, with the application layer (front end, back end, DB, DevOps,
scripts) sitting inside.

**The "codebase singularity"** is his name for the moment you conclude: *"My
agents can now run my codebase better than I can. Nothing ships to production
without my teams of agents."*

---

# Honest challenge to us — where lesson 9 argues we're wrong

Lesson 9 is a direct critique of **my own boot design**. I read **all** of
`learnings/` at every session start, and Kam explicitly accepted the token cost
on 2026-07-31. His argument: always-loaded memory grows without bound, carries
irrelevant context, and eventually contradicts itself.

**My assessment — he's half right, and the half that's right matters:**
- Right: unbounded growth is a real failure mode, and we already predicted it.
  Our own research note (2026-07-31) flagged the switch to index-first retrieval
  as a future decision point, and the weekly consolidation exists precisely to
  stop contradiction accumulating (newer wins, supersede links, audit note).
- Right: **context priming per task** is better than one giant always-on load.
  A `/prime` per work type (delegation vs. research vs. wrap-up) would be
  strictly better than reading everything every time.
- Wrong for us *today*: at 8 learnings the full read costs almost nothing, and
  it's what makes a cold session able to *be* Wednesday. The cost only bites at
  scale — and the ledger + consolidation are the mechanisms that keep the count
  low.

**Recommendation:** keep the full read for now, but add the trigger condition —
when `learnings/` exceeds roughly 25 files or the boot read exceeds ~10K tokens,
switch to **index-first + `/prime`-style task-specific loading**, and measure it
with `/context` rather than guessing. That belongs in the weekly consolidation
review. (Deferring this is now a *dated decision*, not an oversight.)

The lesson-13 rule I should adopt immediately, though, is the **mental-model
discipline**: my brain files are a mental model, not a source of truth. The
repo, the boards, and the live systems are the truth. Any learning that names a
file, flag or system must be **validated against reality before I act on it** —
which is exactly what my own tooling already warns about, now with a principle
behind it.

---

# What we take from 9–14

| Idea | Verdict |
|---|---|
| **R&D framework (reduce/delegate)** | **Adopt as vocabulary** — it names what we already do with sub-agents and gives a discipline for what to load |
| **Measure context with `/context`** | **Adopt now** — cheap, and it turns the boot-cost question into data |
| **MCP servers loaded per-need, not by default** | **Adopt** — check what our sessions preload |
| **Prompt sections, `workflow` as the key one** | **Adopt** — improves our brief templates (P2) |
| **"Three times marks a pattern"** | **Adopt** — a concrete trigger for the workflow-systemisation duty Kam set |
| **Orchestrator = single interface + CRUD + observability** | **Adopt the three-pillar test** — it's a good spec for what I should become; pillar 3 is P4c |
| **Orchestrator must protect its own context** | **Adopt** — I should query state, not stream every agent's logs |
| **Consumed/produced assets in every report** | **Adopt** — cheap addition to the wrap-email format |
| **Agent expert: act/learn/reuse** | **Already ours** (learning loop v2) — but adopt the *mental model ≠ source of truth* rule and the validate-against-code step |
| **Meta-agentics (prompts/agents/skills that build their own kind)** | **Adopt selectively** — a meta-prompt for writing briefs is genuinely useful |
| **Don't build an expert where you have no mental model** | **Adopt as a guard** — applies to me delegating into domains I haven't read |
| **Class 1/2/3 agentic layer ladder** | **Useful as a self-assessment** — we're Class 1 heading to Class 2 |
| **Bundle the agentic layer across a product's repos** | **Note for Secuura** (Blockchain + Extranet are already a declared coupled pair) |
| **Codebase singularity / "nothing ships without agents"** | **Reject as a goal** for client work — same reasoning as ZTE. Keep as a description of *his* end state, not ours |
| **Replacing the system prompt wholesale** | **Caution** — his own Pong demo shows how much you throw away |
