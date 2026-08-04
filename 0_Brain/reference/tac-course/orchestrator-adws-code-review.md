# Code review: `orchestrator-agent-with-adws` (TAC companion repo)

**Date:** 2026-08-04 · **Commissioned by Kam** ("review this as part of yesterday's
learnings") · folds into WED-39. Repo (read-only):
`/Volumes/DevMASTER/!CODING/Agentic Coding/Resources and Lesson Material/orchestrator-agent-with-adws`
Method: subagent survey (very thorough, 59 tool calls) → I validated the
load-bearing claims against source myself (orchestrator system prompt,
self-improve.md, review.md, meta_prompt.md, verdict-parse code) per
[[../../learnings/2026-08-03_mental-model-not-source-of-truth]].

## What it is

The lessons 12/13/4 patterns as one shipped system: a FastAPI+Vue **orchestrator**
(single chat interface, 10 CRUD/ADW management tools via in-process MCP, WebSocket
event stream, Postgres event log), **ADW workflows** (deterministic Python chaining
plan→build→review→fix agents), and **agent experts** (expertise.yaml as mental
model + self-improve command). Notable: the repo DIVERGES from lessons 4/8 —
no ADWState JSON, no worktrees, no KPI tracking; state is all Postgres.

## ADOPT for Wednesday (passes the "good, not backwards" filter)

1. **Two-tier summarization as a context firewall.** Every agent event gets an
   async Haiku summary in a `summary` column; the orchestrator reads summaries
   by default, raw payload only on request (`check_agent_status(verbose_logs)`,
   pagination as first-class params). This is "protects its own context" made
   concrete — cheap model pays the attention tax. → Apply to my wrap-email
   digests, boards digest, and the WED-46 dashboard feed.
2. **Capability-by-filesystem-convention.** Dropping a file in
   `adw_workflows/adw_<type>.py` / `.claude/agents/*.md` adds a capability;
   live inventories are injected into the system prompt at boot via
   `{{PLACEHOLDER}}`s. No registry, no drift. → My skills/, brief templates,
   and the WED-16 scheduler should self-discover the same way.
3. **The self-improve recipe** (`experts/adw/self-improve.md`): optional git-diff
   → read expertise → **validate against codebase** → fix discrepancies →
   `MAX_LINES: 1000` trim LOOP (repeat until under) → YAML-compile gate →
   "there may be nothing to be done — this is perfectly acceptable."
   Two verbatim-worthy guards: don't store work summaries as expertise; nothing-
   to-do is a valid outcome. → Upgrade weekly-consolidation with the trim loop +
   compile gate; this is THE template for WED-43/44 gatekeeper expertise files.
4. **Structural manage-don't-do.** The orchestrator's `allowed_tools` has **no
   Write/Edit** — my rule 0a enforced by construction, not instruction. Same for
   scout agents (`tools: Read, Glob, Grep`). → Monitoring/reviewing agents I
   spawn get read-only toolsets; enforcement beats exhortation.
5. **Prompt-as-API verdict gating.** review.md mandates a terminal PASS/FAIL
   line; deterministic code branches on it (fix step only on FAIL). The risk-tier
   taxonomy (BLOCKER/HIGH/MEDIUM/LOW with explicit membership criteria + report
   skeleton + 1-3 ranked solutions per issue) is the best review format I've
   seen. → Feeds WED-21 (do-check-refine) and WED-44. **But fix their bug:**
   parsing is `"PASS" in text and "FAIL" not in text` on free text — a review
   saying "no FAIL conditions" scores FAIL (verified at
   adw_plan_build_review_fix.py:871-877). Use an explicit structured last line
   (e.g. `VERDICT: PASS`) — cheap determinism.
6. **The house prompt format** (meta_prompt.md enforces it): frontmatter →
   Purpose → Variables (dynamic $1/$2 first, then static) → Instructions →
   Workflow → Report (literal output template). A prompt that writes prompts in
   its own format. → Adopt for my briefs and skills; candidate: port
   meta_prompt.md into `0_Brain/skills/`.
7. **Run-state shape** from `ai_developer_workflows`: status / current_step /
   total_steps / completed_steps / error_step / error_count / input_data /
   output_data / duration. → Steal the FIELDS, store as JSON-per-run file
   (Kam already ruled files-not-DB on WED-39). Gives delegations resumability
   the repo itself lacks.
8. **Async-agent monitoring patterns** (for WED-42): completion oracle = Stop
   event after a response event in the log tail; sleep+check loop with explicit
   "return to the loop after interruptions"; interrupt-on-new-message with a
   broadcast warning; "don't delete agents after completion — we might have
   additional work"; anti-eager-polling instructions. → The reference
   architecture for agents-ask-Wednesday-not-Kam.

## REJECT / adapt (would take us backwards)

- **Postgres as delegation state.** Kam ruled files; repo's own gaps agree
  (no resume, agents share one working_dir → concurrent collisions).
- **Fire-and-forget with stdout to /dev/null.** All observability via DB+WS.
  Ours: wrap emails + files + history — mount-independent, greppable. Keep.
- **80% self-reported context rule.** Their % = cumulative DB tokens ÷ 200k —
  drifts from the real window. Our close-before-full discipline is honest about
  this; don't import the fake precision.
- **LLM-extracted artifact paths** between steps (with mtime-glob fallback).
  Fragile. Convention beats extraction: write outputs to a KNOWN path per run.
- **No-resume, copy-pasted workflows** (3 files ~85% duplicated). Teaching
  artifact, not engineering to copy.

## Noted for later (not now)

- Guard hook `pre_tool_use.py`: blocks 6 `rm -rf` variants; `.env`-access block
  present but **commented out** — re-enable if we adopt. Hooks→external
  observability server (`send_event.py` → localhost:4000) pairs with WED-46.
- 11 output-styles + TTS backends — a presentation layer relevant to WED-13.
- Autocomplete expert (`autocomplete_agent.py` + typed pydantic expertise,
  session persistence, identity-change reset, accepted/rejected learning) — the
  best miniature of the whole expert pattern; re-read before building WED-43/44.
- `scripts/copy_claude.py` (whitelist merge of shared .claude/ into apps) —
  answer to sharing prompt libraries across projects without symlinks.
- KPI tracking is ABSENT here despite lesson 8 — the lesson's
  `track_agentic_kpis.md` remains the reference for WED-30.

## Direct feeds

WED-42 (adopt #1/#8 — this is the blueprint) · WED-38 (benchmark my three
pillars against this implementation) · WED-43/44 (adopt #3, autocomplete-expert
miniature) · WED-21/44 (adopt #5 with the verdict fix) · WED-16 (adopt #2) ·
WED-30 (KPI gap note) · delegation protocol (adopt #4, #7).
