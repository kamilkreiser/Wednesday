# Research: Sakana AI multi-model collective intelligence (AB-MCTS / TreeQuest)

Date: 2026-08-03. Commissioned by Kam (verbatim prompt in ../00_prompt-log.md).
Research agent report, filed by Wednesday. Companion report:
2026-08-03_iterative-refinement.md. Synthesis + proposals: see
../../Architecture/2026-08-03_two-schools-analysis.md and Linear `proposal` issues.

---

## 1. What Kam means

"Japanese stock model" = **Sakana AI** (Tokyo, founded 2023 by ex-Google
researchers David Ha and Llion Jones; sakana = fish — schooling/collective
metaphor). Their July 1, 2025 release **AB-MCTS (Adaptive Branching Monte Carlo
Tree Search)**, open-sourced as **TreeQuest**, matches the description exactly:
no big training run — an *inference-time* algorithm that pools several frontier
LLMs (o4-mini, Gemini 2.5 Pro, DeepSeek-R1-0528 in the flagship experiment) and
dynamically delegates each search step to whichever model is proving best.

- Announcement: https://sakana.ai/ab-mcts/ (2025-07-01)
- Paper: "Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive
  Branching Tree Search" — https://arxiv.org/pdf/2503.04412

Related Sakana lines (context only): Evolutionary Model Merge (2024), AI
Scientist (version published in *Nature*, 2026-03), ShinkaEvolve (2025,
open-source LLM-driven program evolution, ~150-sample efficiency), Darwin Gödel
Machine, Recursive Self-Improvement Lab (2026).

## 2. How AB-MCTS works + results + open source

Mechanism: builds an answer tree; at every node **Thompson sampling** decides:
1. **Go wider** — fresh candidate;
2. **Go deeper** — refine a promising candidate using feedback (e.g. failing tests);
3. **(Multi-LLM variant) which model** — a second bandit layer treats each LLM as
   an arm, learning *during the search on that specific problem* which model
   produces the best-scoring nodes. Cross-model repair observed: one model's
   near-miss gets fixed by another.

Results (ARC-AGI-2, 120 public eval tasks, Pass@250):
- o4-mini repeated sampling: ~23% · single-model AB-MCTS: 27.5%
- **Multi-LLM AB-MCTS: >30%** — beats every member; solves problems none solved
  alone. BUT with a realistic rule-based selector, Pass@2 falls to **19.2%** —
  the collective *finds* good answers far better than it can *identify* them.
  Verification is the bottleneck (best-case domain: code, where tests verify).

Open source: `SakanaAI/treequest` (Apache 2.0, pip-installable, you supply the
generate_fn + scorer) and `SakanaAI/ab-mcts-arc2`. **Research-grade** (~560
stars) — a library to build around, not a service.

## 3. Landscape: two families, don't conflate

**(a) Routers** (RouteLLM/ICLR-2025, Not Diamond → OpenRouter "Auto", LLMRouter
UIUC v0.2.0 Jan-2026): pick ONE model per request for cost/quality. Save money;
add **no validation** — mostly irrelevant to Kam's goal.

**(b) Ensembles / councils / judges** — multiple models on the SAME task:
- Mixture-of-Agents (Together AI 2024) — strong academically, latency-heavy.
- **Karpathy's `llm-council`** (late 2025): N models answer independently → each
  anonymously ranks the others → chairman synthesizes. Models often rank a
  rival's answer above their own.
- **Cross-model PR review is a shipped 2026 product category** (Git AutoReview:
  Claude + Gemini + GPT in parallel behind one human gate; CodeRabbit/Greptile
  class). Benchmark leadership is genuinely split in 2026: Claude Opus leads
  SWE-bench Verified, Gemini leads LiveCodeBench Pro, GPT-Codex leads
  Terminal-Bench — each model has a real miss-rate the others partially cover.
- Production surveys (Zylos 2026-04): dominant patterns are (1) LLM-as-judge on
  code/tests, (2) one-writer/different-reviewer at PR time, (3) small distilled
  judges inline (~97% cost cut at 0.88–0.95 agreement) + big judge at gates.
  AB-MCTS-style search remains research/competition territory.

## 4. Assessment for a Claude-Code-primary workflow (validation + testing)

Structural fact: **the strongest validator of LLM code is a deterministic test
suite, not another LLM** — use other models only where determinism can't reach
(design review, spec compliance, adversarial reading, test-gap finding).

Ranked by value-per-effort:
1. **Second-model diff review via hook/slash-command** — pipe `git diff` to a
   different model (Kimi K2's API is Anthropic-compatible — base-URL swap;
   or GPT/Gemini) and return findings for Claude to triage. Cents per review;
   catches author-blind-spot bugs (decorrelated errors). Buildable in an afternoon.
2. **Zen MCP Server** (BeehiveInnovations, Apache 2.0) — ready-made #1: plugs
   into Claude Code, exposes `codereview`, `consensus`, `precommit`, `debug`
   backed by Gemini/O3/Grok/OpenRouter/Ollama. Most popular practitioner
   implementation of "Claude authors, other models validate."
3. **Cross-model test generation** — second model writes tests *from the spec
   only, without seeing the implementation*; breaks the "tests that pass their
   own bugs" correlation. Cheapest genuinely adversarial signal.
4. **Council at decision checkpoints only** — 3 models + chairman for
   architecture/security decisions; 3–5× cost, a few times a week not per commit.
5. **TreeQuest itself — low priority**: legitimate heavy weapon for a rare,
   genuinely stuck problem WITH an automatic scorer (failing tests), at tens-to-
   hundreds of calls per problem. Not a daily driver.

NOT recommended: routers (they substitute the author) and backend-swap tricks
(ANTHROPIC_BASE_URL) — both change who writes the code, which Kam doesn't want.

## 5. Failure modes (field-reported)

- **Cost blowup**: Pass@250 economics; councils multiply every query by N+2.
  "Cost-driven performance collapse" is a named production failure mode.
- **Selection is the hard part**: >30% with oracle-ish selector vs 19.2% Pass@2.
  Solvable in code (run the tests) — why code is the best-case domain.
- **Correlated errors**: shared training distributions → confident convergence on
  the same wrong answer; polished chairman syntheses invite overtrust.
- **Latency**: search/councils kill interactive flow — restrict to async
  checkpoints (PR review, nightly).
- **Judge noise**: false positives scale with model count; keep one human gate.
- **Operational drift**: provider/version churn (e.g. Google cut individual
  Gemini CLI access mid-2026); cross-model context is a prompt-injection surface.

## Sources

sakana.ai/ab-mcts · arXiv 2503.04412 · github.com/SakanaAI/treequest ·
VentureBeat TreeQuest · The Decoder · sakana.ai/shinka-evolve · sakana.ai/rsi-lab ·
openrouter.ai/blog/insights/model-routing · github.com/ulab-uiuc/LLMRouter ·
github.com/Not-Diamond/awesome-ai-model-routing · llmcouncil.ai/karpathy-llm-council ·
VentureBeat Karpathy council · github.com/BeehiveInnovations/zen-mcp-server ·
gitautoreview.com blog · deployhq.com CLI comparison · zylos.ai LLM-as-judge
production survey 2026-04 · arXiv 2511.19933 (failure taxonomy) ·
kimi.com/resources/claude-code-api
