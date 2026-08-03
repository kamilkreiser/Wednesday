# Research: iteration-over-scale — the Chinese-lab pattern + do-check-refine loops

Date: 2026-08-03. Commissioned by Kam (verbatim prompt in ../00_prompt-log.md).
Research agent report, filed by Wednesday. Companion:
2026-08-03_sakana-multi-model.md. Synthesis:
../../Architecture/2026-08-03_two-schools-analysis.md.

---

## 1. Kimi K2 (Moonshot AI) — what's actually true

- **K2** (July 2025): MoE, **1T total / 32B active params**, 15.5T training
  tokens, MuonClip optimizer. Open weights, **Modified MIT** (attribution clause
  above ~100M MAU / $20M-month revenue — check license before commercial use).
  Tech report: arXiv 2507.20534.
- **The training story IS the do-check-refine thesis, baked in**: (1) agentic
  data synthesis in a simulated ~20k-tool environment, trajectories filtered by
  verifiers; (2) RL = verifiable rewards (math/code/logic, rule-based binary) +
  **self-critique rubric rewards for open-ended domains, with the critic
  continuously re-grounded on verifiable-domain rollouts** — the cleanest
  published articulation of transferring verifiable-check discipline into
  subjective territory.
- **K2 Thinking** (Nov 2025): interleaved think→tool→think loops, **200–300
  sequential tool calls unassisted**; self-reported 71.3% SWE-bench Verified,
  44.9% HLE-with-tools. The strongest concrete instance of "repetition provides
  better results" — the loop is RL-trained-in, native.
- **K2.5 (Jan 2026, multimodal) / K2.6 (Apr 2026, "Agent Swarm" — up to 300
  sub-agents / 4,000 steps) / K3 (reported 2026-07-16, ~2.5–2.8T params, 1M
  context)** — ⚠ secondary sources of mixed quality, specs conflict; verify
  against Moonshot primary channels before quoting. Irony flagged by the agent:
  if K3 is real at ~2.8T, Moonshot is ALSO scaling size, not iteration alone.

## 2. The wider Chinese-lab pattern: real vs narrative

**Real:** DeepSeek-R1 (Jan 2025, MIT) — pure RL with rule-verifiable rewards
(GRPO) produces *emergent* self-verification/reflection ("aha moment"): the model
learns do-check-refine because reward only pays for verified-correct answers.
QwQ-32B (Mar 2025, Apache 2.0) matched R1 (671B) on key reasoning benchmarks at
~1/21 the size — crispest "RL + iteration beats parameter count" datapoint.
Common structural choice across DeepSeek/Qwen/GLM/Moonshot: very sparse MoE
(3–5% active), RL-with-verifiable-rewards, agentic post-training, open weights,
aggressive price/perf — capability-per-FLOP as strategy (partly export-control
forced).

**Narrative/caveats:** the "$5.6M DeepSeek model" covered only the final training
run — SemiAnalysis estimated ~50k Hopper GPUs, ~$1.6B capex behind it. And these
labs are NOT avoiding scale (K2 = 1T params). Accurate framing: **iteration is a
multiplier on top of substantial scale, not a replacement**. US labs use the same
test-time/RL playbook; the Chinese distinctive is open-weights + cheap per token,
which is what makes the pattern adoptable by us.

## 3. The technique family (nationality-independent)

Canon: Self-consistency (2203.11171) · Self-Refine (2303.17651, ~20% avg gain) ·
Reflexion (2303.11366 — episodic verbal lessons after failure; 91% HumanEval) ·
CRITIC (2305.11738 — tool-grounded critique) · Test-time compute scaling (Snell
2408.03314 — smaller model + optimal test-time compute can beat one **14× larger**).

**When loops help:** when the check step has ground truth the generate step
didn't use — test execution, compilers, retrieval, a human — or an independent
checker (different model/context).

**When loops backfire:** intrinsic self-correction with no external signal
often DEGRADES performance (Huang 2310.01798, ICLR 2024; Kambhampati 2402.08115).
Correlated errors: self-critique amplifies confidence without adding
information. **Diminishing returns are fast**: biggest jump is round 1 (e.g.
59%→79% on TestEval), most gains by 2–3, plateau by 3–5.

**Rule of thumb:** do-check-refine pays iff (a) checker is grounded or
independent AND (b) you stop after ~1–3 rounds or on convergence. Ungrounded
"think harder about your own answer" loops are the failure mode.

## 4. Coding supervision — practical loop patterns

- **Generate → run tests → refine** is the one loop with unambiguous evidence
  (test execution = ground truth). Cap turns; terminate on success / max ~60
  calls / ~10 identical consecutive failures.
- **Independent critic > self-critique** (OpenAI CriticGPT line). Self-review of
  one's own diff triggers post-hoc rationalization. Proxy for independence in a
  one-model world: **fresh context** — a reviewer subagent that sees only diff +
  spec, not the generation transcript. Or a different model.
- **Rounds:** budget 1 generation + 1–2 review/refine rounds; escalate to human
  on non-convergence rather than looping.
- **Economics:** verification is cheaper than generation — expensive model
  writes, cheap model + deterministic tools check, expensive model re-engages
  only on flagged findings (~$1.00–1.50/review production pricing).
- **Production:** Cursor Bugbot = 8 parallel passes, randomized diff order,
  majority vote + validator model; CodeRabbit led a 146-PR field test on
  false-positive rate; Factory.ai published which-model-reviews-best benchmarks.

## 5. Iterative loops for an agent's learned behaviour (Wednesday-relevant)

- **Reflexion episodic memory**: failures → verbal lessons → injected into
  future attempts. (= our learnings/ + ledger, validated.)
- **Voyager skill libraries** (2305.16291): proven procedures distilled into
  named reusable skills. (= our 0_Brain/skills/.)
- **ACE — Agentic Context Engineering** (Stanford/SambaNova, Oct 2025,
  2510.04618, open-sourced): context as an **evolving playbook** via
  generate→reflect→curate with **incremental structured updates**. Names two
  failure modes we must avoid: **brevity bias** (summarization erodes detail)
  and **context collapse** (wholesale rewrites degrade the playbook). +10.6% on
  agent benchmarks. *Most relevant paper for Wednesday's evolution.* Translation:
  append/edit lessons as discrete deltas; never regenerate whole memory files.
- **SEAL** (MIT 2506.10943): weight-level self-adaptation — research-stage,
  forgetting risks; not for us yet.
- **Darwin Gödel Machine** (Sakana/UBC 2505.22954, ICLR 2026): self-modifications
  survive only if they pass an objective benchmark (20%→50% SWE-bench in their
  runs, self-reported). Principle: **validate every self-change** — an agent
  changing its own prompts/skills should test them against outcomes, not just
  adopt them. 2026 caution (2605.30621): harness updates are often conflated
  with the update actually helping.

## Core corrective to the dictated thesis

The Chinese labs' loop is mostly **trained-in** (RL against verifiable rewards),
not bolted on at inference — and the inference-time version only reliably works
when the check is grounded or independent. **"Repetition" alone is not the
magic; repetition against a verifier is.**

## Verification flags

K2.6/K2.7/K3, GLM-5, DeepSeek-V4 details rest on secondary sources (kie.ai,
wan27.org, explainx.ai, inferencehub.org); K3 param counts conflict. Kimi
benchmarks are Moonshot self-reported. DGM figures are the authors' own runs.

Full source URLs preserved in the agent transcript; headline anchors: arXiv
2507.20534 (K2) · 2501.12948 (R1) · 2408.03314 (test-time) · 2303.11366
(Reflexion) · 2510.04618 (ACE) · 2505.22954 (DGM) · 2310.01798 (self-correction
limits).
