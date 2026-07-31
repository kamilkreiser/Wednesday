# Research: agent second-brain + self-improvement best practices (2025–2026)

Date: 2026-07-31. Synthesized from ~20 sources: Anthropic engineering posts,
OpenClaw memory docs, arXiv memory surveys, practitioner systems (obsidian-mind,
obsidian-llm-memory, memsearch). Full source list at the bottom.

## 1. Vault structure (converged practitioner pattern)

- **Three tiers:** (1) auto-loaded *index* layer, ≤~3K tokens — routing CLAUDE.md,
  a MEMORY-as-index, a USER/persona file; (2) curated *semantic* layer — atomic,
  dated, frontmattered fact/lesson notes + per-project state files; (3) *episodic*
  layer — append-only daily notes/session logs, auto-load today + yesterday only.
- **Indexes point, never store.** The most-repeated rule: the auto-loaded file is
  a map to vault locations, not the content ("memory on demand").
- Atomic, "retrieval-sized" notes (one read = one complete idea); MOC hub notes as
  entry points; wikilinks so the agent traverses a graph instead of guessing greps.
- **Write down the implicit conventions** (note types, where links live, folder
  rules) — agents can't infer them the way humans do. YAML frontmatter (date,
  status, type, project) makes markdown queryable; enforce schema via hooks
  (obsidian-mind validates frontmatter/wikilinks on every write with a PostToolUse
  hook).

## 2. Memory mechanics

- **Episodic / semantic / procedural separation** is standard: daily notes /
  distilled facts / skills+identity files — each with its own retention rules.
- **Consolidation is the load-bearing mechanism**, not retrieval: "an agent that
  remembers everything remembers nothing useful." Levers: write-time importance
  filter ("would this change how the agent acts next time?"), write-time
  merge/dedupe of contradictions, time-decay ranking, eviction rarely.
- **OpenClaw "dreaming"**: memory-flush before every compaction (PreCompact hook)
  + a scheduled background job that distills daily notes → promotes qualifying
  facts → explicitly invalidates superseded ones → writes an audit summary a
  human reviews before it takes effect (guards silent drift).
- **Grep-first retrieval beats vector DBs** for this use case (Anthropic replaced
  vector search with grep in Claude Code; ~94.5% of RAG faithfulness with zero
  vector store). Works only if consolidation preserves *retrieval handles*: stable
  entity names, dates, IDs, predictable file names.
- Claude Code specifics: CLAUDE.md under ~300 lines (instruction compliance
  degrades beyond ~150–200 directives); rationale must hit disk at decision time
  (compaction loses rationale first); compact proactively ~60% context.

## 3. Learning the user (the parent–child loop, formalized)

- **Dedicated living persona/preferences file** (imperative directives, dated
  revisions) separate from the facts file.
- **Correction-capture loop:** clarify before acting → ground actions in stored
  preferences → write every correction immediately with provenance (the failure
  that produced it + date).
- **Recurrence-gated promotion pipeline:** correction → feedback log (episodic)
  → recurs? → promoted into persona/skill (procedural) → original archived.
  Prevents one-off remarks hardening into permanent rules (over-personalization
  guard).
- **Session-end reflection ritual** is the highest-leverage cheap mechanism:
  review memory at start, write what changed at end. Structure as Preferences /
  Decisions / Workarounds / Recurring Mistakes.
- **Implicit signals** (what the user re-asks, re-edits, overrides) are training
  data even when he never says "remember this."

## 4. Multi-agent coordination via shared files

- Shared task list on disk = coordination substrate; state survives crashed
  agents; one-writer-per-file conventions to avoid races.
- One **status/progress file per project** as the orchestrator's read surface
  (exactly the `projects_index/` design). Structured handoffs: task, context as
  *file paths* (not pasted content), constraints, definition of done.
- Caution from the field: one well-structured session beats several poorly
  coordinated agents.

## 5. Pitfalls checklist

1. Memory bloat / attention dilution — hard token budgets per auto-loaded file;
   but **silent truncation is worse than bloat** — always say what was dropped.
2. Stale facts — date everything; recency-wins with explicit supersede links.
3. Contradictions — resolve at write time, never leave old + new as peers.
4. Consolidation that destroys retrieval handles (names/dates/IDs).
5. Over-personalization — recurrence threshold before promotion; human review of
   consolidation output.
6. Schema drift — enforce frontmatter via hooks; add SQLite only if aggregate
   queries are genuinely needed.
7. Compaction amnesia — decision rationale to disk at decision time.

## Implications for Wednesday's brain (already partly applied)

- `0_Brain/` maps to the three-tier model: `daily/` (episodic), `learnings/` +
  `people/` (semantic), `identity/` (procedural). Kam has accepted full-read
  startup cost for `learnings/`; when it outgrows that, move to index-first
  (Rhodes' VAULT-INDEX pattern) — decision point noted in discovery questions.
- Adopt: dated frontmatter on every note (done), supersede-links not deletions
  (done), correction-capture with provenance (template done), session-end ritual
  (in CLAUDE.md).
- To decide in discovery/architecture: recurrence gate before a learning changes
  `identity/`; a scheduled "dreaming" consolidation job + audit file Kam reviews;
  frontmatter-validation hooks; PreCompact flush hook.

## Sources

obsidian-mind (github.com/breferrari/obsidian-mind) · obsidian-llm-memory
(github.com/CodyLiska/obsidian-llm-memory) · OpenClaw memory docs
(docs.openclaw.ai/concepts/memory) · memsearch (Milvus blog) · Anthropic:
Effective context engineering for AI agents · Anthropic: Context management ·
orchestrator.dev Claude Code agent memory 2026 · Hindsight: the consolidation
problem · MindStudio: self-improving agent feedback loop + agent teams shared
task list · PAHF (arxiv 2602.16173) · dynamic personas (arxiv 2607.26473) ·
memory survey (arxiv 2512.13564) · rate-distortion compaction (arxiv 2607.08032)
· MemGuard (arxiv 2605.28009) · "Stop calling it memory" critique · AI-powered
Zettelkasten (codewithseb.com).
