---
date: 2026-09-01
type: preference
source: "Kam, 2026-09-01 17:55 (dashboard chat, verbatim in Discovery/00_prompt-log.md): 'please create a new process where an agent hands over to you confirming what was done, you hand over to the testing agent to double check the changes. All changes made be checked visually and through code. If browser related, then through a browser. Once the testing agent check, you double check' — minutes after his two live screenshots showed a Settings icon that never rendered and a dashboard tab whose KPIs fail to load, on a build that had been scored 1.0 on unit tests and a code read."
status: live
supersedes: "the two-hop verification in delegation-protocol (agent wrap → Wednesday verify → score) — now three hops"
---

# Every change goes agent → me → testing agent → me before it is scored or shipped

**The rule (Kam's order, exactly):**
1. **The agent hands over to me confirming what was done** — the wrap/STATUS mail: sets not
   counts, branch + SHA, the surfaces changed, how it authenticates, what it did NOT do.
2. **I hand over to the testing agent** — a per-invocation brief from the fleet QA template
   (`2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md`, charter beside it): what changed,
   where to drive it, the credentials path, the flows. **Every change is checked visually
   AND through code; anything browser-related is driven in a real browser** (the QA
   project's default driver is Claude-in-Chrome). The QA agent is findings-only — it never
   fixes.
3. **Once the testing agent has checked, I double-check COMPLETION** — Kam's clarification
   one minute later (17:55:45, verbatim): *"completion. you do not have to do the same test
   as the testing agent."* My pass is delivered-vs-commissioned, item by item against the
   brief and Kam's own asks ([[2026-08-10_own-the-spec-not-just-the-escalation]]), plus the
   source facts only I hold (the ruling, the ticket, `ls-remote`, the deploy target) — NOT a
   re-run of the QA agent's tests. Then SCORE, then any deploy GO. Three different questions,
   three different instruments: the agent proves it built it; the QA agent proves it works
   for a user; I prove it is what was asked for.

**What it changes:** the delegation protocol's verifier-first loop had two hops (agent →
me). Today's evidence for why two is not enough: NexusAI s11 scored 1.0 on 377/482 green
tests, six mutation-proven guarantees and a deploy proved by content probe — and Kam's first
click found a Settings icon that renders as a blank (the class name `bi-leaf` was in the
source; the glyph was never rendered by anyone) and a Sustainability tab that says "Could not
load sustainability KPIs" on demo. Both were invisible to unit tests, to a code read, and to
my verification, which checked the deploy, not the user's screen. **A code read proves the
code; only a render proves the artefact** ([[2026-08-07_a-check-that-cannot-fail]] — prefer
checking the artefact over the intent — applied to the UI, where I had never applied it).

**How to apply (from today):**
- A wrap or READY-FOR-QA mail is not a score trigger; it is a QA trigger. The scoring step
  moves to AFTER the QA report and my double-check. Deploys likewise.
- Briefs say so in the QUEUE ("this round ends at READY FOR QA") and in HOLDS ("no deploy
  until the QA pass and Wednesday's GO"). The NexusAI s12 brief (2026-09-01 17:34) is the
  first with the gate; the Secuura merges of the same evening get a code-level QA pass
  before their score.
- Code-only changes get the "through code" half (diff review against the ticket's claim,
  tests read not just run); anything with a rendered surface gets the browser half too.
- The QA surface must be one an agent can actually drive: where SSO blocks the demo (RD-76),
  a local run of the SAME commit in open mode, stated as such — "same commit, not the demo
  image" — never a claim that demo was tested when localhost was.
- Go-slow applies to the mechanism: pilot on s12 and tonight's Secuura wrap, measure the
  cost (an extra session per wrap) and the catch rate at the next weekly consolidation; the
  rule stands regardless — it is Kam's — but its tooling is scored like any adopted
  mechanism (DGM guard: adoption ≠ improvement).

**Mechanism (a promise is not a mechanism):** the QA project exists (`Testing Agent MAIN`,
charter + template in this tree) but has no launcher entry, no inbox and no wrap hook.
WED ticket filed the same session for: a cockpit launcher entry, a per-invocation brief
path that keeps R0 (client-neutral charter; one client's content only in the brief), a
report path I read, and the scoring ritual amended so SCORE cannot be sent without a QA
report id. Until it ships, I run the hop by hand on every wrap and say so in the SCORE.

**Related:** [[2026-08-10_own-the-spec-not-just-the-escalation]] (testing is mine to demand
and sample), [[2026-08-11_coordinator-not-carrier]] (the QA agent is the org design this
activates), [[2026-08-06_local-proof-is-not-target-evidence]], [[2026-08-07_a-check-that-cannot-fail]],
[[../skills/delegation-protocol]], [[../people/kam]]
