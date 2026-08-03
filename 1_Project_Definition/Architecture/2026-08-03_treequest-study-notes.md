# TreeQuest deep study — working notes (WED-24)

Commissioned by Kam 2026-08-03 ("go through it in detail… develop this model into
our coordination approach as much as possible"). Multi-day; newest day at top of
the log below. Clones live at `2_Project_Files/tools/treequest` and
`…/ab-mcts-arc2` (Apache 2.0, gitignored from our repo, on-drive per portability).

---

## Day 3 (2026-08-03, same day) — experiments: when does the tree actually fire?

Four runs on the working harness:

| Run | Task | Seats | Result |
|---|---|---|---|
| smoke | parse_duration (12 tests) | gpt, claude | GPT-5 one-shot 12/12, node 1, 13.7s |
| day3 | semver ranges + prerelease gate (23 tests) | gpt, claude | GPT-5 one-shot 23/23, node 1, 34s |
| day3-weak | same semver task | gpt-low, haiku | **Haiku one-shot 23/23**, node 1, 144s |
| day3-table | 10 exact-output tests, bool/int + rstrip traps | gpt-low, haiku | **Haiku one-shot 10/10**, node 1, 135s |

(The first table run crashed: `minimal` is not a valid Codex reasoning effort →
fixed to `none`; and a seat exception killed the search → now scores 0 so the
bandit routes around broken seats. The failure bought two real hardening fixes.)

### Findings

1. **Self-contained, fully-specified coding tasks are one-shot territory for
   2026 models — including small ones.** Three escalating task designs, four
   runs, zero branches. The verifier confirmed; it never needed to guide.
2. My prediction that first attempts would score 0.3–0.8 was wrong three times
   — calibration lesson: any kata I can fully specify with tests, current
   models can solve. Artificial difficulty doesn't reproduce real difficulty.
3. **Where the tree earns its keep** (consistent with Sakana needing ARC-AGI-2
   to show gains): ambiguous/underspecified problems, large real codebases with
   hidden context, genuinely hard reasoning, noisy verifiers. I.e. real
   delegated work at its worst — not benchmarks I author.
4. Practical consequence, now empirically grounded: **default = one strong
   model, one pass, grounded verification. Search = insurance for the stuck
   case** (exactly the WED-23 break-glass posture Kam approved). The bigger
   everyday transfers from AB-MCTS remain the management ones: scored attempts,
   per-seat track records, explicit wider-vs-deeper decisions (Tiers 1–2).
5. Seat economics measured: GPT-5 ~34s, Haiku ~135–144s wall on comparable
   tasks, both $0 marginal on subscriptions. gpt-low (effort "none") never got
   selected before early-stop — untested in anger.

### Day 4 (remaining)

Coordination protocol v1: Tier-1 rules + Tier-2 scoreboard format, folding in
these findings; propose where Tier 3 first runs on a *real* stuck problem.

---

## Day 2 (2026-08-03, same day — Kam accelerated) — ARC harness read + OUR harness built

### ab-mcts-arc2 read (runner, prompts, verifier, LLM layer)

- `generate_fn` pattern: **root → initial prompt (spec); non-root → feedback
  prompt = spec + parent's code + parent's failing-test detail.** Refinement is
  literally "here's what failed, fix it" — the GEN/CONT decision upstream chooses
  whether that's worth doing vs a fresh attempt.
- **NodeState carries (generation_result, eval_results, model_name)** — the eval
  detail rides in the state so the feedback prompt can use it. Score = mean
  pass-fraction over train examples; final answer = top-k by public score,
  checked privately (selection stays external to the search).
- Verifier runs candidate code **sandboxed**: resource limits (memory/stack),
  timeout, IO swallowed, `reliability_guard` disabling destructive syscalls —
  worth copying if we ever score untrusted generations beyond our own models.
- Ops: pickle checkpoint every ~10 nodes + `checkpoint_latest`, resumable;
  cost + wall-time tracked per model and dumped as JSON; models keyed off a
  pricing table (Claude via Bedrock, OpenAI, Gemini).

### Built today: `2_Project_Files/coordination/` (Tier 3 skeleton, WORKING)

- `seats.py` — subscription-backed seats, zero marginal cost: **gpt** = Codex
  CLI exec mode (ChatGPT-subscription auth, CODEX_HOME on-drive in
  4_Credentials/.codex), **claude** = `claude -p` (Max). Call counts tracked.
- `verifiers.py` — unittest-based test-suite verifier (score = pass fraction,
  failure text preserved for refinement prompts). Rubric/LLM-judge verifiers
  deliberately deferred (noisy-verifier caveat).
- `harness.py` — ABMCTSA (beta dists) ask/step loop, budget cap, early stop at
  1.0, checkpoint each step, per-seat priors parameter (track-record seeding),
  summary.json per run.
- **Smoke run passed end-to-end**: parse_duration task, 12 tests, seats
  {gpt, claude}, budget 6 → GPT-5 hit 12/12 on node 1, early-stopped, 13.7s,
  one call. Plumbing verified: seats, verifier, search, checkpoint, summary.
- Day-3 note: smoke task was too easy to exercise wider-vs-deeper — needs a
  task where first attempts score 0.3–0.8 so refinement and seat-selection
  actually get pressure. Candidates: a small real bug from a project (delegated
  brief), or a harder algorithmic kata with tricky edge cases.

---

## Day 1 (2026-08-03) — core library read (~1,500 lines: tree, trial, base, AB-MCTS-A full, AB-MCTS-M algo)

### Shape of the library

- Small and clean: ~5.5k lines src, well-tested. `Algorithm` objects are
  **stateless**; all search state lives in a returned `AlgoState` (tree +
  bandit posteriors + trial store) — checkpointable/resumable by design.
- Two interfaces: `step()` (ask+generate+tell in one) and **`ask_batch`/`tell`**
  — ask returns `Trial` objects (ULID id, parent node, chosen action), tell
  reflects a result by trial id, **order-independent and idempotent**. Between
  ask and tell, anything can happen — including a process dying. This is the
  interface that matters for us.
- `generate_fns: {action_name: fn(parent_state|None) -> (state, score)}` — an
  "action" is anything: a model, a prompt style, an approach. Multi-LLM is just
  multiple entries. Scores MUST be normalized [0,1] (validated at node creation).
- Root node is a placeholder (state None, score −1); every real node = one
  attempt with its verifier score.

### AB-MCTS-A mechanics (the transferable heart)

Per-node `NodeProbState` holds Bayesian posteriors (conjugate updates — Beta, or
Gaussian Normal-Inverse-Gamma per Murphy §3.4.3.3):
1. **GEN vs CONT** — shared posteriors over "reward if I branch NEW here" vs
   "reward if I go deeper into an existing child," decided by **Thompson
   sampling** (draw from each, take the max). No hand-tuned explore/exploit knob;
   uncertainty does the work.
2. If CONT: Thompson-sample across the node's children posteriors → descend.
3. If GEN: a **bandit over actions picks WHICH model/approach generates** —
   Thompson (posterior draw per action from its full reward history) or UCB
   (mean + √(2·ln N / n)). `all_rewards_store` = the global per-action track
   record feeding this.
4. `tell` → node added, its score **backpropagates** up the path, updating every
   ancestor's GEN/CONT/child posteriors and the action's global record.
5. **`reward_average_priors`** (global or per-action float) seeds the priors —
   i.e. the algorithm accepts *pre-existing beliefs about how good each
   model/agent is*. Track record in, better first decisions out.

### AB-MCTS-M differences

Same selection skeleton; replaces conjugate posteriors with a **PyMC Bayesian
mixed model** fit per decision (random intercept per child = "this branch's
quality", shared action effects), plus subtree **pruning** (config: min subtree
size 4, same-score proportion 0.75 — kills stagnant branches). Heavier (MCMC per
step; needs `ask_batch` + process pool, batch ≤5 recommended or the tree gets
artificially wide). Verdict for us: **A-variant first** — cheap, dependency-light
(numpy/scipy), same idea.

### Verified against the paper's claims

Matches the research report: the algorithm *finds* good nodes; identifying the
final answer is external (`top_k` by raw score / `ranker.py`). The scorer is
entirely user-supplied — **the library is only as good as the verifier you feed
it.** (Two-schools law, in code.)

---

## The mapping: AB-MCTS → Wednesday's coordination approach

The insight Kam asked for. AB-MCTS is, literally, **a formal manager**: given N
workers with unknown strengths and a budget of attempts, it decides — fresh
attempt vs refine an existing one, and who does it — using tracked evidence, not
vibes. That is my job description. The mapping:

| TreeQuest concept | Wednesday coordination equivalent |
|---|---|
| Node (state, score) | One attempt/deliverable version (a draft, a fix, a brief's result) with its verifier score |
| Tree | The full history of attempts on one task |
| Action / `generate_fn` | A delegation channel: which agent, model, or approach gets the next attempt |
| GEN vs CONT | The manager's core call: **new angle vs refine the promising draft** ("wider or deeper") |
| Thompson sampling | Decide under uncertainty by sampling beliefs — explore new agents exactly as much as their uncertainty warrants |
| `all_rewards_store` | **Per-agent/model track record, persisted across tasks** |
| `reward_average_priors` | Seeding today's delegation with the ledger/history of how each agent has performed |
| ask/tell Trials (ULID, resumable, idempotent) | Delegation tickets — brief issued (ask), result returned whenever (tell), across sessions; maps 1:1 onto Linear issues |
| Score ∈ [0,1] | A grounded verifier: test-pass fraction, rubric checklist, Kam's accept/reject |
| Pruning (M) | Kill stagnant workstreams that keep returning the same mediocre result |

### Adoption plan — three tiers

**Tier 1 — protocol (no code, adopt now):** run my delegation *decisions* on
AB-MCTS logic manually: every delegated attempt gets a recorded score; before
re-delegating I consult the track record; I explicitly choose wider (fresh
attempt/different agent) vs deeper (refine the best attempt) and record which.
Feeds and feeds-from the correction ledger. Folds into the P2 delegation
standard (WED-21).

**Tier 2 — track-record file (small build):** `0_Brain/projects_index/` gains a
per-agent/model scoreboard (rolling mean + count per channel — exactly
`all_rewards_store` serialized). Future briefs seed from it as priors.

**Tier 3 — live harness (build after study days 2–3):** a thin
`2_Project_Files/coordination/` harness wrapping `tq.ABMCTSA()` where
`generate_fns` = {Claude subagent, Kimi K2 API, GPT, …} and the scorer is a real
verifier (test suite for code; rubric-judge for text). Used at checkpoints for
hard, verifiable problems (the WED-23 break-glass case) and — the interesting
one — for **multi-agent drafting**: N attempts at a brief/design, scored,
best-of-tree returned. Budget-capped per run.

### Open questions for the coming days

- Day 2: read `ab-mcts-arc2` (the real-LLM harness: prompts, scoring, budget
  management, model configs) + `pymc_interface.py` in full; run treequest's
  tests on-drive to confirm the toolchain works here.
- Day 3: toy prototype — ABMCTSA over 2–3 real model backends on a small
  verifiable task; measure cost per quality gain.
- Day 4: coordination protocol doc v1 (Tier 1+2 formalized), proposal to Kam
  for where Tier 3 first runs.
- Watch: score normalization for non-code tasks (rubric judges are noisy
  verifiers — the two-schools caveat applies to ourselves).
