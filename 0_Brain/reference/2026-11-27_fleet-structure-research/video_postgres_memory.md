---
date: 2026-11-27
type: reference
source: https://youtu.be/eNhiHP7t5bo + linked repos/docs (read 2026-11-27)
status: research report, no design recommendation
---

# Video research: "Why We Built Agent Memory on Postgres, Not Markdown"

Provenance tags used on every statement:
**[T]** from the transcript (timestamps are mm:ss, 30-second resolution) ·
**[D]** from the video description ·
**[L]** from a linked or primary source I read (URL given) ·
**[I]** my inference.

---

## SOURCE

| Field | Value |
|---|---|
| Title | Why We Built Agent Memory on Postgres, Not Markdown [D] |
| URL | https://youtu.be/eNhiHP7t5bo |
| Channel | The Multimodal Society (`@multimodalsociety`, 327 subscribers at fetch) [D] |
| Published | 2026-11-03 [D] |
| Length | 14:48 (888 s) [D] |
| Views / likes at fetch | 48,198 / 492 [D] |
| Speaker | Vasilije Markovic, founder of Cognee [D] |
| Setting | Lightning talk at "Agent Memory Night", SF Tech Week, AWS Builder Loft; hosted by The Multimodal Society, FalkorDB and GMI Cloud [D] |

**How the transcript was obtained.** `yt-dlp 2026.11.23` in a throwaway venv,
`--skip-download --write-auto-sub --write-sub --sub-lang en --sub-format vtt --write-info-json`.
The video has **no human-written subtitles**; what came back is YouTube's
**auto-generated English captions**.

**Complete or partial.** Complete in coverage: captions run 00:00 to 14:46 of
14:48, 2,753 words. **Not verbatim-reliable**: auto-captions mis-hear names
and some numbers. Known mis-hearings (corrected below by cross-checking the
description and repo): "Cogni" = Cognee; "Gary Tran's G Brain" = Garry Tan's
GBrain; "Glider 2.5" = GLiNER (Fastino); "PlotCode" = Claude Code;
"on Tropic" = Anthropic; "Falcor" = FalkorDB; "beam" = BEAM. One number is
unrecoverable: "Now we are **to** people between Berlin and San Francisco" (01:10)
— team size is lost.

**Important limit.** The talk is slide-driven and the slides are not in the
captions. I did not watch the video frames. The description quotes two slides
(reproduced below); anything else on slides is not captured here. The speaker
also says his live demo failed ("I would have shown you my personal brain, but
since I can't connect ... I'll leave it on theory here", 06:20) — so the talk
contains **no demonstration and no schema**.

Files kept beside this report, in `transcript/`:
- `eNhiHP7t5bo.en.vtt` — raw auto-captions
- `eNhiHP7t5bo.transcript.txt` — de-duplicated, 30-second timestamped text
- `eNhiHP7t5bo.info.json` — yt-dlp metadata (description, chapters)

---

## WHAT THE VIDEO CLAIMS

### Nature of the video (read this first)

- It is a **vendor talk for Cognee**, an open-source "AI memory platform", not a
  how-to for building your own Postgres memory. [T][D]
- It gives **no table names, no SQL, no schema, no MCP tool list**. The title's
  "Postgres" occupies roughly 50 seconds of a 15-minute talk (03:34–04:25). [T]
- Every structural detail below the level of "layers" comes from the linked
  repo, not from the talk — see LINKED ARTEFACTS. [I]

### The argument against markdown files (01:21–02:27)

- "people tried solving this with MD files. MD files ... don't work really that
  well at scale. So you cannot, you know, use a file instead of a database."
  [T 01:20]
- Stated reason: "you need concurrency, you need many processes to read and
  write and lock and index and retrieve at scale where there is a lot of data in
  one place." [T 01:30]
- Example given: "Gary Tran's G Brain is a good [example] of that where you end
  up with 16,000 MD files that you are parsing through ... and you're going to
  end up in trouble." [T 01:55]
- Further claimed failures of files: scattered knowledge across the business,
  "agents repeat themselves", and "the model itself doesn't know really your
  domain". [T 02:00]
- Slide quote: "We can't move forward with MD files. We need compliance,
  predictability and control." [D]
- Description's framing: "Markdown memory files work for one agent. They break
  when many agents, users and teams share them." [D]
- **No measurement is offered** for where files break — no file count, size,
  latency or failure rate beyond the "16,000 MD files" anecdote. [I]

### Ontology (02:27–03:34)

- "an ontology, this representation of knowledge that needs to sit in between
  your agent and your system." [T 02:30]
- Not an opinionated memory model: "we need an engine that can construct memory
  as any type of a data pipeline" with "modules of memory transformations",
  building "graph vector representations in pure Python". [T 02:55–03:15]
- Background: first version was a WhatsApp chatbot with 20,000 users; "It failed
  miserably." [T 02:40]

### Postgres and the "memory box" (03:34–04:25)

- FalkorDB is "one great option because you can do thousand of agents with
  thousands of databases as a key value store. The problem with it is then you
  still need another database. So we managed to dump everything into Postgres."
  [T 03:35–03:45]
- "for every agent you can have a small Postgres instance ... We call it memory
  box." [T 03:48]
- Isolation unit: "isolated per agent, per team, per user, per org." [T 04:05]
- A "self-improvement loop so you can continuously change and update the schema
  that the agent is dealing with without actually having to do that manually."
  [T 04:15]
- The closing line lists what they offer: "Python runtime, auto ontology
  generation for businesses, Postgres and a small model runtime." [T 14:40]

### The layers (04:25–06:21)

1. **Ingestion** — "multimodal ingestion ... It's not real multimodal ingestion.
   I'm kind of faking it a bit. We turn everything to text in this layer."
   [T 04:30]
2. **Knowledge structuring** — "We extend PyDantic objects and create a PyDantic
   representation of the graph and then store that in any type of a graph and
   vector store." [T 04:45]
3. **Access control and isolation** — "the full ACL table where you define read
   write permissions per agent, per tenant." Purpose: "make sure that nothing is
   polluting context for different agents". [T 05:00–05:30]
4. **Retrieval strategies** — "everything from temporal [to] code. You can pull in
   whole GitHub repos and understand them", plus "complex questions that require
   multi-hop reasoning". [T 05:35]
5. **Feedback loops** — "You can run improvements on embeddings, improvements on
   the graphs. We weight and we scale certain subgraphs." Layers can be switched
   on and off; extensions are "a simple Python function that transforms [the]
   data model that is passing through the pipe". [T 05:50–06:15]

### How agents write and read it (06:21–08:19)

- **Write path is hooks, not tool calls**: "Session memory is fed by intercepting
  hooks ... if you do user prompt submit, we take the context from here, put it
  into session memory, apply distillation and get the information we need, facts
  and whatever is relevant, and then we store that into the permanent memory."
  [T 06:35–06:55]
- **Only two memory concepts**: "session memory where agents store their data as
  a temporary data store, a cache of sorts, and a permanent memory which is a
  graph vector representation that can also live in object storage." [T 07:15]
- Explicit rejection of the episodic/semantic/procedural split: "I don't like
  long-term, short-term procedural memory ... you only then have N groups of
  memory ... but we need thousands of groups of memories ... that you can
  dynamically define." [T 06:57–07:10]
- Permanent memory also ingests from external sources (Google Drive etc.,
  "100 plus" connectors) but **stores structure, not copies**: "just to get
  actually the base structure of that data so we can effectively let agents
  navigate back to the original system ... more as a mind map of the system than
  effectively a full data storage layer." [T 07:30–08:05]
- Read path: not described in the talk beyond "retrieval strategies". [I]

### Scopes and promotion (08:19–09:13)

- Four scopes: "agent memory, user memory, team memory, organization memory". [T 08:20]
- Memory is **promoted** between scopes on instruction: "promote the memory to
  my personal knowledge ... send this to my team". [T 08:30–08:40]
- Organisation scope holds slow-changing material: "contracts ... mission vision
  ... things that shouldn't be changed too often". [T 09:00]

### Self-improvement and deletion (12:14–13:17)

- "we weigh the embedding space and then populate that back into the graph." [T 12:15]
- "We do some type of a soft delete on the graph representation because doing
  delete on memory is relatively dangerous since if you delete the data you
  cannot get it back." [T 12:20]
- "we reposition the embeddings and get them closer or further apart based on
  the type of interaction patterns we see from the users or the agents ... that
  happens at any type of query or ingestion." [T 12:30–12:45]
- A "meta representation layer" over facts: "habits, patterns, temporal ...
  that sits on top of your facts that kind of reasons about the system." [T 12:55]
- "We're publishing a couple of papers on this" — not yet published per the talk. [T 12:10]

### Small-model runtime and cost (09:41–12:14)

- Entity extraction can run on Fastino's GLiNER on CPU: "you're not calling
  OpenAI [or Anthropic] to get your ... structure of the graph anymore". [T 10:10]
- Cost anecdote: agents "would spend let's say 300k ... on 100 gigs of data";
  "if we use [Cognee] we would halve that price. But that's still ... 150k";
  with small models, cost is CPU only, "80 bucks for 16 gigs of RAM". [T 10:30–11:00]
  These are spoken illustrations with no method given. [I]
- Runs local, managed cloud, and on a phone in airplane mode. [T 11:45–12:00]

### Numbers claimed

| Claim | Where | Tag |
|---|---|---|
| 79% accuracy on BEAM "on 10 million and 100k chunks" | 09:15 | [T] |
| "79% accuracy on SOTA AI memory benchmark" | slide | [D] |
| "86% cheaper than context stuffing" | slide | [D] |
| LoCoMo result "coming out this week" (not given) | 09:25 | [T] |
| ~12 million memories generated (said once as total, once as "each month") | 01:15, 05:10, 14:05 | [T] |
| ~60 companies in production, of 500 production runs seen in anonymised telemetry | 05:15 | [T] |
| One deployment with 300 tenants (named as AstraZeneca in China) | 05:05 | [T] |
| 100+ connectors, built on `dlt` | 07:35, 13:20 | [T] |
| Customers named: Bayer, University of Wyoming | 13:50 | [T] |
| Plugins for Claude Code, Codex, OpenClaw; "listed in [Anthropic] store the other day" | 14:15–14:25 | [T] |

**The 79% claim does not match the linked report as spoken.** The talk attaches
79% to both scales. The repo's own report gives 0.79 at 100K tokens and 0.67 at
10M tokens. [L — see below]

---

## LINKED ARTEFACTS

Links in the description: cognee.ai, github.com/topoteretes/cognee,
docs.cognee.ai, github.com/dlt-hub/dlt, fastino.ai, a sister talk
(youtu.be/IfkDHlEipvk), multimodalsociety.com, a Luma events page. I read the
Cognee repo and docs. I did **not** read dlt, Fastino, cognee.ai marketing
pages, or the sister talk.

### 1. Cognee repo — https://github.com/topoteretes/cognee [L]

- Apache-2.0, created 2023-08-16, last push 2026-11-26, 33,654 stars,
  1,118 open issues. Latest release named in README: v1.6.1 (2026-09-24).
- Python 3.10–3.14. Four operations: `remember`, `recall`, `improve`, `forget`.
- **Default stores are not Postgres**: SQLite (relational), LanceDB (vector),
  Kuzu/"Ladybug" (graph) — all file-based (`.env.template` header).
- README section "Run the Whole Memory Layer on Postgres" carries this warning,
  verbatim: "**Using Postgres as a graph store is currently released as a demo
  feature. The production-ready version is available as a licensed product.**"
- The graph adapter lives in a directory literally named
  `cognee/infrastructure/databases/graph/postgres_demo/`, and its module
  docstring says: "not production-ready ... rely on a graph-native backend such
  as Kuzu or Neo4j for production workloads."
- **So the open-source "everything in Postgres" configuration the talk
  headlines is a demo; the production version is paid.** [L for the facts,
  I for the juxtaposition with the talk]

### 2. Postgres schema actually in the repo [L]

Graph store — `.../graph/postgres_demo/tables.py`:

| Table | Columns |
|---|---|
| `graph_node` | `id` PK, `name`, `type`, `properties` JSONB, `created_at`, `updated_at` |
| `graph_edge` | PK (`source_id`, `target_id`, `relationship_name`), FKs to `graph_node` ON DELETE CASCADE, `properties` JSONB, timestamps |
| `graph_node_source_ref` | (`node_id`, `source_ref_key`) + `dataset_id`, `pipeline_run_id`, `position` identity, `source_pipeline`, `source_task`, `source_node_set`, `source_user`, `source_content_hash`, `description` |
| `graph_edge_source_ref` | edge key + `source_ref_key`, `dataset_id`, `pipeline_run_id`, `position` |
| `graph_metadata` | `key`, `value` |

Indexes on edge source/target (plus covering indexes for neighbour lookups),
node type, and source-ref key/dataset/run. Provenance is one row per
(node-or-edge, source document), which is what makes per-document delete and
failed-run rollback possible.

Vector store — `.../vector/pgvector/PGVectorAdapter.py`: pgvector >= 0.7.0
required; embeddings stored as `halfvec`; HNSW index (`m=8`,
`ef_construction=64`, default `ef_search=100`).

Session cache — `.../cache/sql/tables.py` (`CACHE_BACKEND=postgres`):
`cache_qa_entries`, `cache_trace_entries`, `cache_session_context`,
`cache_capture_receipts`, `cache_usage_logs`, `cache_kv` — each a
`(user_id, session_id, payload, created_at, expires_at)` shape. Plus relational
`session_records` / `session_model_usage` (status, start/last-activity/end,
tokens in/out, cost, error count, last model).

Isolation — `.env.template`: per-dataset handlers. `postgres_graph` / `pgvector`
= **one Postgres database per dataset** (needs `CREATE DATABASE`);
`postgres_graph_shared` / `pgvector_shared` = **one schema `ds_<dataset_id>` per
dataset** in a shared database (needs only `CREATE SCHEMA`). This is the
concrete form of the talk's "memory box". [L; the mapping to "memory box" is I]

Schema is created automatically by the library ("tables, entities, and schemas
are created automatically, so you never define them yourself" —
docs architecture page); relational side is Alembic-migrated (about 50
migrations in `cognee/alembic/versions/`).

### 3. Session vs permanent memory — https://docs.cognee.ai/core-concepts/sessions-and-caching [L]

- Session = short-term memory keyed by `(user_id, session_id)`.
  `remember(data, session_id=...)` writes raw text to the cache plus one Q&A
  vector per turn — "no chunking, no entity extraction", "no LLM calls".
- `remember(data)` with no session id runs the full pipeline: chunking,
  entity/relationship extraction, embeddings, then an improve pass.
- Session cache **expires**: `SESSION_TTL_SECONDS`, default 7 days after last write.
- `recall(query, session_id=...)` searches the session cache first **by keyword
  matching**, then falls through to the permanent graph; results carry a
  `_source` of `"session"` or `"graph"`.
- Cache backends: sqlite (default), turso, postgres, redis, tapes. The
  filesystem cache backend was **removed**.

### 4. Improve — https://docs.cognee.ai/core-concepts/main-operations/improve [L]

- Nine fixed stages: `feedback_weights`, `persist_session_qa`,
  `persist_agent_traces`, `extract_agent_context`, `distill_sessions`,
  `update_user_preferences`, `build_truth_subspace`, `review_conflicts`,
  `global_context_index`.
- `feedback_weight` is a stored number on graph nodes and edges, default 0.5,
  raised or lowered from feedback on session answers that used them. This is
  the documented form of the talk's "re-weighting". The talk's "reposition the
  embeddings" wording is **not** what the docs page describes; the docs describe
  a weight on graph elements. [L for the docs; I for the mismatch]
- Distillation filters out guidance "with harmful feedback or low confidence",
  then a curator/writer pass keeps "only durable lessons that are supported by
  the session and not already known".
- Without an LLM key, the weight/persist stages still run; the LLM-drafting
  stages (extract context, distill) skip.

### 5. Claude Code plugin — https://github.com/topoteretes/cognee-integrations/tree/main/integrations/claude-code [L]

Install: `claude plugin marketplace add topoteretes/cognee-integrations` then
`claude plugin install cognee-memory@cognee`.

| Hook | Behaviour |
|---|---|
| `SessionStart` | mode select, identity setup, dataset readiness, watcher bootstrap |
| `UserPromptSubmit` | dataset-scoped context lookup + async prompt staging |
| `PreToolUse` (Read) | injects code-graph facts about the file about to be read |
| `PostToolUse` | async trace write |
| `Stop` | assistant answer write |
| `PreCompact` | builds a memory anchor before compaction |
| `SessionEnd` | triggers detached final sync into graph memory |

- Captures prompts, tool calls (name, arguments, output) and answers.
  Credentials, private keys and DB URLs are redacted; `.env`/key files never
  captured; `<private>…</private>` spans never leave the hooks.
- Two tools for the model: `mcp__cognee-memory__search` and
  `mcp__cognee-memory__remember`.
- Local mode starts a Cognee server on `localhost:8011` and pip-installs
  `cognee==1.6.6` into `~/.cognee-plugin/venv`. State lives under `~/.cognee/`
  and `~/.cognee-plugin/` — **in the home directory, not the project folder**.
- In local mode with no `LLM_API_KEY` and `claude` on PATH, graph-building LLM
  calls run as `claude -p --safe-mode` and count against the Claude subscription.
- In cloud mode the plugin **disables Claude Code's native auto-memory** unless
  explicitly enabled.
- "Shared agent memory" (default on): each plugin identity is its own Cognee
  user; a tenant plus a `cognee-agent` role is created so Claude Code and Codex
  agents of one user share datasets. Grants flow child to parent only.
- A separate MCP server exists (`cognee-mcp/`, port 8001) for Cursor, Cline and
  other MCP clients.

### 6. BEAM report — `cognee/eval_framework/beam/REPORT.md` in the repo [L]

- Marked "*Preliminary version*".
- **0.79 at 100K tokens**: fixed hybrid retrieval, four rounds over 20 questions
  from **one held-out conversation**.
- **0.67 at 10M tokens**: "exploratory"; retrieval settings were selected on the
  same questions that were scored; one conversation.
- Retrieval settings and answer prompts "were tuned for BEAM"; routing used
  BEAM's own question-type labels; no ablations were run; LLM judge.
- The 10M run used distributed mode on Modal and "the public code does not
  include the BEAM-specific distributed orchestration from that run".

### 7. Token cost — https://docs.cognee.ai/core-concepts/evaluation-and-efficiency/token-efficiency-and-context-compression [L]

- Recall carried ~1,118 tokens over a 16,075-token corpus and ~1,864 tokens over
  a ~202K-token corpus. Graph build is a one-time token cost that "paid for
  itself after about 23–26 repeated queries" on their test corpus. "For a single
  question over a small document, sending the document directly is cheaper."
- The slide's "86% cheaper" figure does not appear on this page. [L]

---

## COMPARABLE APPROACHES

Stars and dates are from the GitHub API on 2026-11-27. "Add / cost" lines are
descriptive of what each mechanism brings, not a recommendation.

### A. GBrain — https://github.com/garrytan/gbrain [L]

- **Mechanism.** Markdown repos stay canonical; a sync-and-parse step indexes
  them into **PGLite** (Postgres 17 via WASM, zero-config, default, "up to ~50K
  pages") or **Postgres + pgvector** for shared or multi-machine use. README:
  "Your brain repo holds the Markdown; the database is an index rebuildable from
  it, and git deletes become soft-deletes." Retrieval: "vector + keyword + RRF +
  source-tier boost + reranker", plus typed graph traversal. Surface: CLI and
  MCP share one op registry; `gbrain setup claude-code` wires MCP, hooks and an
  instruction block. Keyless mode = keyword search only.
- **Maturity.** MIT, created 2026-04-05, 33,631 stars, pushed 2026-11-26.
  Author reports 155,795 pages in his own brain.
- **Relevance to the video.** This is the project the speaker cites as the
  markdown failure case. Its README describes markdown **plus a Postgres
  index**, not bare file parsing. The talk's characterisation is at least
  out of date. [I]
- **Adds.** Hybrid search and a graph over existing markdown without changing
  the source of truth. **Costs.** A sync step and a second copy to keep
  consistent; README warns "Markdown export is not a full database backup"
  (DB-only pages, history and operational state live only in the database).

### B. Basic Memory — https://github.com/basicmachines-co/basic-memory [L]

- **Mechanism.** Knowledge "lives as Markdown files that both you and your AI
  can read, write, and search"; two-way sync; observations and wikilinks form a
  graph; "Hybrid full-text + vector ranking with FastEmbed embeddings, on SQLite
  or Postgres". MCP-native. Obsidian reads and writes the same files.
- **Maturity.** AGPL-3.0, created 2024-12-02, 4,719 stars, pushed 2026-11-26.
  Hosted version runs on Neon Postgres.
- **Adds.** Same shape as A, with an Obsidian-compatible file format.
  **Costs.** AGPL licence; README notes the current release needs
  `--prerelease=allow` for a dependency.

### C. Graphiti (Zep) — https://github.com/getzep/graphiti [L]

- **Mechanism.** Temporal knowledge graph. Facts are edges with validity
  windows: "When information changes, old facts are invalidated — not deleted."
  "Explicit bi-temporal tracking." Hybrid retrieval: embeddings + BM25 + graph
  traversal. Paper: arXiv 2501.13956.
- **Backends.** Neo4j, FalkorDB, Amazon Neptune, or Relate (embedded).
  **No Postgres backend listed.**
- **Maturity.** Apache-2.0, created 2024-08-08, 33,120 stars, pushed 2026-11-26.
- **Adds.** The most explicit treatment of superseded facts — the same problem
  the video answers with "soft delete and re-weighting". **Costs.** A graph
  database to operate, and LLM calls on ingest.

### D. Mem0 — https://github.com/mem0ai/mem0 [L]

- **Mechanism.** LLM extracts discrete memories from conversation; retrieval is
  "semantic, BM25 keyword, and entity matching scored in parallel and fused".
  pgvector is a supported vector store
  (https://docs.mem0.ai/components/vectordbs/dbs/pgvector).
- **Maturity.** Apache-2.0, created 2023-06-20, 69,513 stars, pushed 2026-11-25.
  Claims 92.5 on LoCoMo, with the stated caveat that scores are from the
  managed platform with "proprietary optimizations not available in the
  open-source SDK".
- **Adds.** Smallest schema of the set; Postgres-only is possible.
  **Costs.** Extraction is LLM-driven on every write; published scores are not
  the open-source numbers.

### E. claude-mem — https://github.com/thedotmack/claude-mem [L]

- **Mechanism.** Same hook-capture pattern as Cognee's plugin (SessionStart,
  UserPromptSubmit, PreToolUse, PostToolUse, Stop, SessionEnd) feeding a local
  worker; storage is **SQLite with FTS5** at `~/.claude-mem/claude-mem.db`
  (sessions, observations, summaries) with Chroma for vectors; three MCP search
  tools in a progressive-disclosure flow.
- **Maturity.** Apache-2.0, created 2025-08-31, 119,979 stars, pushed 2026-11-26.
- **Adds.** Evidence that the hook-capture write path is the common pattern for
  coding agents regardless of store. **Costs.** Not Postgres; state in the home
  directory.

### What the set has in common [I]

- Hybrid retrieval (keyword/BM25 + vector, often + graph) is universal;
  nobody ships vector-only.
- Two families: **database is the source of truth** (Cognee, Mem0, Graphiti,
  claude-mem) versus **markdown is the source of truth and the database is a
  rebuildable index** (GBrain, Basic Memory).
- Writes come from lifecycle hooks; reads come from hook-injected context plus
  one or two search tools.
- None of the sources read describes a boot-time "load everything" digest;
  all assume retrieval per prompt.

---

## OPEN QUESTIONS / NOT VERIFIED

1. **Slides not seen.** No video frames were examined. Only the two slide
   excerpts quoted in the description are captured.
2. **Auto-captions only.** No human transcript exists. Names and numbers were
   cross-checked where a second source existed; team size at 01:10 is lost.
3. **"79% on BEAM at 10M and 100K"** as spoken conflicts with the repo report
   (0.79 at 100K, 0.67 at 10M, both on a single conversation, preliminary).
4. **"86% cheaper than context stuffing"** — source not found in the docs page
   read; `cognee.ai/token-cost-of-persistent-ai-memory` was not read.
5. **Customer and usage claims** (AstraZeneca 300 tenants, Bayer, University of
   Wyoming, 60 production companies, 12M memories) are the speaker's word only.
   "12 million" is stated both as a total and as monthly.
6. **"Soft delete / reposition embeddings"** — the papers are described as
   forthcoming. The docs show a `feedback_weight` on graph elements; I found no
   documented mechanism that moves embedding vectors. Not searched in source code.
7. **Promotion agent → user → team → org** — described in the talk; I read the
   permissions/tenant/role docs index and the plugin's shared-memory section but
   did not find or read a documented "promote" operation.
8. **What the licensed production Postgres graph store differs in**, and its
   price — not public in anything read.
9. **The file-scale claim** ("16,000 MD files ... end up in trouble") has no
   measurement behind it in the talk, and its cited example (GBrain) documents
   itself as markdown indexed into Postgres.
10. **Not read:** dlt repo, fastino.ai, the cognee-mcp tool list in detail, the
    LoCoMo result promised in the talk, the sister FalkorDB talk, the Cognee
    arXiv paper (2505.24478), Letta and Memori (repo stats fetched only).
11. **Nothing was installed or run.** No claim here about Cognee's behaviour is
    from execution; all are from its documentation and source files.
