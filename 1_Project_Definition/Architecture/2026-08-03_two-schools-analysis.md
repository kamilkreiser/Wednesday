# The two schools — analysis and recommendations (WED-19)

Date: 2026-08-03 · Status: Wednesday's synthesis, for Kam's review
Inputs: `../Discovery/research/2026-08-03_sakana-multi-model.md` (Japanese school)
and `2026-08-03_iterative-refinement.md` (Chinese school). Proposals filed to
Linear with label `proposal` (WED-20…23).

---

## The one insight both schools share

Kam framed these as two different challenger approaches. Having read both
literatures, they are **the same discovery arrived at from two directions**:

> **Extra model calls only buy quality when there is a trustworthy CHECK in the
> loop. Repetition against a verifier is the magic; repetition alone is noise.**

- Sakana's evidence: multi-LLM AB-MCTS beats every member model (>30% vs ~23% on
  ARC-AGI-2) — but only at Pass@250 with something oracle-like doing selection.
  With a realistic selector it drops to 19.2%. The collective *finds* good
  answers far better than it can *identify* them.
- The Chinese evidence: DeepSeek-R1's self-checking behaviour *emerged* from RL
  where reward only paid for verified-correct answers; Kimi K2's critic is
  continuously re-grounded on verifiable domains. The loop works because the
  check is anchored to ground truth.
- The negative result confirming both: ungrounded self-correction ("think harder
  about your own answer") often makes models WORSE (ICLR 2024), and gains
  plateau by round 2–3 regardless.

**Consequence for us:** every adoption below is really about engineering the
*check*, not the repetition. Coding is our best-case domain because tests,
compilers and typecheckers are free, deterministic verifiers.

Two honesty notes from the research: (1) the "iteration instead of scale"
narrative is partly myth — K2 is 1T params and the reported K3 is ~2.8T;
iteration is a *multiplier on* scale, not a substitute. (2) The famous "$5.6M
DeepSeek model" excluded ~$1.6B of infrastructure. What IS real and adoptable:
open weights, Anthropic-compatible APIs, cheap per-token pricing, and the loop
patterns themselves.

## Where each school actually fits Kam's world

| Use case | School | Verdict |
|---|---|---|
| Coding validation/testing (Claude authors) | Japanese (multi-model) | **Adopt now** — decorrelated reviewers are the cheap version of collective intelligence; 2026 benchmark leadership is genuinely split (Claude leads SWE-bench Verified, Gemini LiveCodeBench Pro, GPT-Codex Terminal-Bench), so a second model covers a real miss-rate |
| Coding supervision of delegated agents | Chinese (do-check-refine) | **Adopt now** — as a *delegation brief standard*, since Wednesday manages, never edits |
| Wednesday's own evolution | Chinese (loop + memory literature) | **Mostly already built** — learning loop v2 = Reflexion (episodic lessons) + Voyager (skills/) + weighted reinforcement; adopt ACE guards + DGM validation principle as hardening |
| Day-to-day tasks | Both, lightly | One refine round with a grounded check; independent fresh-context critic for consequential outputs only |
| Hard stuck problems | Japanese (TreeQuest proper) | **Shelf item** — legitimate heavy weapon when a test suite can score candidates; tens-to-hundreds of calls per problem, research-grade library |

What we should NOT adopt: model routers (they'd replace the author — Kam
explicitly keeps Claude as author); reflexive multi-model consensus on every
task (cost blowup is a named production failure mode); ungrounded self-critique
loops anywhere.

## The four proposals (filed to Linear, label `proposal`)

**P1 — Cross-model validation pilot for coding projects** (WED-20)
One pilot project (suggest CypherKey or Secuura — Kam picks). Two decorrelated
checks, both cheap: (a) **second-model diff review** — a hook/slash-command
pipes the diff + spec to a non-Claude model (Kimi K2 is Anthropic-API-compatible
and cheap; GPT/Gemini equally viable) and returns findings for the project's
Claude to triage; cents per review. (b) **spec-only adversarial test
generation** — the second model writes tests from the spec *without seeing the
implementation*, breaking the "tests that pass their own bugs" correlation.
Ready-made alternative: Zen MCP Server (Apache 2.0) if we prefer configured over
hand-rolled. Per manage-don't-do: Wednesday writes the implementation brief; the
project's own agent installs it.

**P2 — Do-check-refine delegation standard** (WED-21)
Every brief Wednesday writes for another agent carries: explicit success
criteria · grounded check (tests/build/typecheck) · one independent fresh-context
review (reviewer sees diff + spec only, not the generation transcript) ·
**max 3 refine rounds** then escalate to Kam/Wednesday rather than loop ·
verification cheaper than generation (cheap model + deterministic tools check;
the expensive model re-engages only on findings). This encodes the Chinese
school as management practice.

**P3 — Council-at-checkpoints for big decisions** (WED-22)
Karpathy-style council (3 models answer independently, anonymously rank each
other, chairman synthesizes) reserved for architecture choices, security-
sensitive designs, migration plans — a few times a week at most, never per-edit.
3–5× cost per invocation, worth it exactly where being wrong is expensive.
Guard: models share training data and can converge confidently on the same
wrong answer — the council advises, a human (or tests) decides.

**P4 — TreeQuest as the break-glass tool** (WED-23)
Keep `SakanaAI/treequest` (Apache 2.0, pip-installable) on the shelf. Trigger:
a genuinely stuck, well-specified problem WITH an automatic scorer (failing test
suite). Budget expectation: tens-to-hundreds of model calls. Not a daily driver;
revisit after P1 proves the multi-model plumbing.

## Hardening applied to Wednesday's own loop (done today, no approval needed —
refinements inside the already-approved mechanism)

1. **ACE anti-collapse guard** added to the weekly consolidation ritual: lessons
   are curated as *incremental deltas*; never regenerate a memory file wholesale;
   merge without destroying detail (brevity bias) — the audit note records diffs.
2. **DGM validation principle** noted in the consolidation ritual: a behaviour
   change I make to my own rituals/skills counts as *validated* only when the
   ledger/retro shows it working in real sessions — adoption is not evidence.

## Open questions for Kam (queued, one at a time)

1. Which project pilots P1?
2. Model for the second seat — Kimi K2 (cheapest, on-thesis), GPT, or Gemini?
3. Does the council (P3) need a standing budget line?
