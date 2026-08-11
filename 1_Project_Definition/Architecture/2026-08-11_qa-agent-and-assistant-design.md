# QA Agent + Wednesday-Assistant — design & rulings needed

Date: 2026-08-11 · Tickets: WED-41 (QA agent), WED-91 (Wednesday assistant) ·
Status: **RULED — Kam, 2026-08-11 morning: "approve all six as recommended."**
Q1(a) shared-core+envelope · **Q2 SUPERSEDED same day → findings-only,
absolute: the QA agent NEVER makes changes (Kam: "the QA agent should never
make changes. only findings, reports and reccomendaitons"). The opt-in
regression-test grant is retired; charter §1/§8, brief §6, CLAUDE.md all
updated.** · Q3 per-brief safest-default cleanup · Q4(c) hybrid, project owns
artefacts · Q5(a) advisory-only, deterministic-probe constraint if teeth ever
wanted · Q6(a) hard rule (charter §6). WED-91 assistant pattern GRANTED. QA is
its OWN project at `/Volumes/KK_T9_External_HDD/QA_AGENT/` (scaffolded).
**Still open: pilot target — Kam picked QuickQuote Stage 3 (in flight).**
Commission: Kam, 2026-08-11 morning (verbatim in
`1_Project_Definition/Discovery/00_prompt-log.md`). Built from two research
reports: `1_Project_Definition/Research/2026-08-11_peter-testing-corpus.md`
and `.../2026-08-11_qa-agent-industry-practices.md`.

---

## BLUF

Two things were built and one pattern was sketched:

1. **A cross-project QA/testing agent** — a client-neutral charter
   (`2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`) plus a fill-in
   invocation brief (`.../BRIEF_TEMPLATE.md`). It bottles Peter's methodology
   and the industry testing canon into an **advisory-only, falsification-first,
   user-perspective** tester that any project can call through Wednesday. It is
   R0-safe by construction: the charter carries zero client content; each
   invocation brief carries only the calling client's context.
2. **A Wednesday-assistant pattern (WED-91)** — sketched below, not built: a
   standing pattern where Wednesday spawns a background execution agent per
   task-batch so her own context stays on coordination, not carrying.

**What needs your ruling:** six open design questions (§Detail), the most
load-bearing being **the write boundary** (may the QA agent commit regression
tests back into a project, or is it findings-only?) and **verdict authority**
(can a QA fail block a ship?). Everything ships behind those rulings; the
charter is written to the conservative default (findings-only, advisory-only,
no gate authority) until you say otherwise.

---

## Recommendation

- **Adopt the charter + brief template as the QA agent's v1**, on the
  conservative defaults already written in: advisory-only, findings-only,
  no ship-block authority, non-prod only, disposable-or-teardown state policy.
- **Pilot it on one target you choose** before generalising (§Honest limits).
- **Rule on the six open questions** so the defaults can be relaxed where you
  want them relaxed. My recommendation is marked on each.
- **Approve the Wednesday-assistant pattern (WED-91)** as a standing
  default-delegate posture, piloted and scored like any adopted mechanism.

---

## Detail

### The QA agent — design summary

- **What it is:** an advisory-only tester that a calling project points at a
  running target + spec. It tests from a demanding user's perspective, tries to
  **break** the build (falsification-first, not confirmation), reproduces every
  finding at wire level, classifies coverage honestly (executed / skipped-why /
  N-A-why), and reports one defect per finding with the oracle named — never a
  bare PASS.
- **Where it lives:** `2_Project_Files/fleet/qa-agent/` —
  `QA_AGENT_CHARTER.md` (the method; client-neutral) and `BRIEF_TEMPLATE.md`
  (the per-invocation fill-in). It sits alongside the existing fleet tooling
  (`send_brief.sh`, etc.).
- **How projects call it — through Wednesday, R0-safe:** Wednesday fills the
  brief template with the calling client's specifics and sends it into that
  project's own session via `send_brief.sh` (PROVENANCE gate applies). The
  **charter is the shared methodology core** (no client content, safe in any
  session); the **brief is the per-client evidence/context envelope** (one
  client only, never referencing another). This is the same shape as the
  08-10 org design: bottle the METHODOLOGY client-neutrally, never carry one
  client's content into another's session.
- **What it is based on:** Peter's corpus (distrust-green, hunt-the-class,
  evidence-over-claims, honesty/blast-radius/silence reasoning, audit-your-own-
  tooling, coverage honesty, stay-in-lane) + the industry canon (SBTM charters,
  SFDIPOT coverage, FEW HICCUPPS oracles, Hendrickson attack tables, Whittaker
  tours, Nielsen/WCAG user pass, RIMGEA reporting, and the measured LLM-tester
  failure modes with their mitigations).

### Consolidated open design questions

Format: **Client/Project · problem · options · recommendation (marked).**
The corpus report raised six; the industry report's contribution folds into #2,
#4, and #6.

**Q1 — Cross-client isolation model.**
`WED / QA agent` · Peter's methodology is client-neutral but his *artefacts*
are client-specific; how does the agent carry transferable heuristics between
clients while keeping each client's findings/creds/spec strictly siloed?
Options: (a) shared methodology core + per-client evidence store; (b) a fully
separate agent instance per client with no shared anything; (c) one agent, load
everything, trust instructions to silo.
→ **Recommendation: (a).** Already implemented — the charter is the shared core
(no client content), the brief is the per-client envelope. R0 holds by
construction because the charter physically contains nothing to leak, and
briefs are single-client. (c) is unsafe; (b) discards the whole point of a
reusable methodology.

**Q2 — The write boundary (findings vs regression tests).**
`WED / QA agent` · Peter never writes fixes, but he *does* write regression
tests into the repo (report-only skip/xfail that auto-flip when the fix lands).
May the QA agent write *tests* into a calling project's test tree, or is it
purely read-and-report with the project agent applying any test PRs? This is
the "manage, don't do" tension, and it is the one place the two reports pull
against each other (see §Honest limits). Options: (a) findings-only, the
project agent authors all tests; (b) findings + regression tests into a named
test tree, opt-in per brief; (c) full write to the project's test suite by
default.
→ **Recommendation: (b), opt-in per brief.** Default is findings-only (charter
§8); the brief has a write-scope field that, when granted, lets the agent write
**report-only regression tests** (never the fix, never product code) into a
named tree. This captures Peter's highest-value habit — the test that flips
green when someone else fixes it — without breaking advisory-only, because a
skip/xfail regression test changes no product behaviour and no gate.

**Q3 — State-mutation & cleanup policy.**
`WED / QA agent` · Fuzzing inherently mutates state; Peter's own harness got
this wrong repeatedly (self-inflicted state that filled a cap; self-lockout by
fuzzing its own auth account). What is the sanctioned pattern? Options: (a)
disposable accounts the agent provisions and tears down; (b) scoped teardown —
record exact keys touched, restore by key; (c) exclude-and-report-only for any
irreversible/destructive op.
→ **Recommendation: all three, chosen per brief, defaulting to the safest
available.** Charter §8 already forbids mutating state it cannot clean up and
forbids fuzzing credential-mutating ops against its own identity. The brief's
state-cleanup field names which pattern this project sanctions. Where none is
safe, exclude-and-report-only (c) is the floor.

**Q4 — Tool ownership (who maintains harnesses it builds).**
`WED / QA agent` · Does the agent run its own tool stack drive-locally (per the
portability rule) or invoke the calling project's existing suites? Peter mostly
*hardened the project's own suites* rather than running a parallel stack; the
industry pattern is hybrid (agent takes exploratory + regression, deterministic
scripts keep compliance/perf). Options: (a) agent brings its own portable stack;
(b) agent drives the project's existing suites and hardens them; (c) hybrid —
project suites for deep tool runs, agent-owned lightweight probes for coverage
honesty and deterministic gates.
→ **Recommendation: (c) hybrid, and whatever the agent builds is OWNED by the
project, handed over in the report — not maintained by Wednesday.** The QA agent
is advisory; a harness it leaves behind is a deliverable to the project team,
not a standing Wednesday-run system. This keeps "manage, don't do" intact and
avoids Wednesday accreting per-client tooling debt.

**Q5 — Verdict authority (can a QA fail block a ship?).**
`WED / QA agent` · Peter proved scanner verdicts are non-deterministic (identical
input, opposite answers) and that a run which loaded nothing can pass with "0
vulnerable." Should the agent be *barred* from gating on any single tool verdict,
and can a QA fail block a ship at all? Options: (a) advisory-only — QA never
blocks; humans decide on the report; (b) QA fail blocks, but only on a
deterministic probe it authored, never on a raw scanner verdict; (c) QA fail
blocks on any finding ≥ threshold.
→ **Recommendation: (a) for now, with the (b) mechanism available when you want
teeth.** Default: the agent assigns **severity**; **priority and
ship/no-ship stay with the humans** (charter §8). If you later want a blocking
gate, it must gate on a **deterministic probe**, never a flaky scanner verdict —
that constraint is non-negotiable given the evidence, and it is already baked
into the charter's distrust-green rule.

**Q6 — Encoding the public-self-correction norm.**
`WED / QA agent` · Peter's culture — retract your own wrong findings with
evidence, name the reasoning error, record corrections in the open rather than
quietly fixing them — is a behaviour worth encoding. How strongly should
Wednesday bake it in vs leave it to each project's conventions? Options: (a)
hard charter rule (mandatory retract-in-public + name-the-error); (b) charter
norm, project may override; (c) leave to project conventions.
→ **Recommendation: (a) hard rule.** It is cheap, it is client-neutral, and it
directly counters the measured LLM failure "can't catch its own mistakes." The
charter already carries "separate proved from assumed / record corrections in
the open"; promoting it to a named mandatory behaviour costs nothing and buys
trust in the agent's findings.

### Wednesday-assistant (WED-91) — design sketch

**A standing pattern, not a persistent process.** Wednesday does not run a
long-lived junior; she **spawns a background execution agent per task-batch**,
briefs it with full context per the loading rules (full context, not the
builder's conclusions — [[2026-08-03_context-loading-split]]), and lets it
execute while she stays conversational with Kam.

- **What goes to the assistant:** anything with implementation surface — builds,
  refactors, multi-file edits, research fan-out, artefact production. The R&D
  "Delegate" lever applied to Wednesday's own work, so her context is spent on
  the board, not on carrying one task.
- **What stays in Wednesday's hands (glue only):** Kam-prompt captures; relaying
  rulings; verification probes (the final browser/wire E2E as verifier);
  brain writes (learnings, daily notes, ledger); scoring the delegated run on
  the scoreboard. These are the coordinator's irreducible work.
- **How it interacts with the threshold-delegation rule
  ([[2026-08-05_wed-work-threshold-delegation]]):** it **tightens** it. The old
  rule was "small rounds direct, chunky builds delegated." The
  coordinator-not-carrier ruling ([[2026-08-11_coordinator-not-carrier]]) moves
  the default to **default-delegate**: Wednesday's direct hands are for glue
  only; anything with implementation surface delegates, even when she could do
  it faster inline. Small-round direct build survives only for genuine glue
  (single-file, instantly verifiable, no meaningful implementation surface).
- **Review asks the breadth questions, not just correctness:** all
  possibilities considered? aligned to the commission's *objective*, not just
  its letter? what would the adversarial user do? — own-the-spec
  ([[2026-08-10_own-the-spec-not-just-the-escalation]]) operating as the job.

### Honest limits

- **The corpus snapshot has drifted.** The Testing Harness folder that seeds
  much of the Peter methodology is a **May–June 2026 snapshot** and has drifted
  behind the live repo — several wrappers that read as "stub / not deployed"
  there are now implemented in-repo. The *methodology* distilled into the
  charter is stable; any *artefact-specific* claim should be date-stamped and
  re-checked before it is relied on.
- **The charter is untested until its first pilot.** It is synthesised from two
  research reports, not yet run against a live target. Treat v1 as a hypothesis.
- **The one place the two reports pull against each other:** the corpus frames
  the QA function as *embedded and write-capable* (Peter hardens the project's
  own suites and writes regression tests into the repo), while the industry
  report frames the tester as *cold, structurally separate, no shared context
  with the builder* and reporting-only in shape. **Resolution:** I split
  "context" into two kinds. Cold acceptance means the tester must not inherit
  the *builder's belief that it works* (the metadata-sway failure — charter §6),
  NOT that it must be ignorant of the platform. Peter's rich agent-brief is
  legitimate **domain/platform knowledge** (how to reach the target, the
  gotchas) and is exactly what makes an LLM productive in one turn. So: load
  platform context fully; never load the builder's "it works" narrative. The
  write tension is resolved separately by Q2's opt-in, report-only regression
  tests — Peter's habit preserved without breaching advisory-only.
- **Pick the pilot target yourself.** I recommend you choose the first project
  the QA agent runs against, rather than me picking — it is your call which
  live surface is worth the first real test and which env is safe to point it
  at.
