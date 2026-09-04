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


## SHARPENED 2026-09-04 (w=88): a claim about the PRODUCT is not a shape, however well it is argued

**The 2026-09-04 split said Wednesday may ratify a SHAPE — a proof's design, a disclosure, a limit's reasoning — and never CORRECTNESS. Wednesday then broke it inside the paragraph that stated it.**

**The case.** Ratifying RD-245, Wednesday wrote *"NOT RATIFIED: correctness. That waits for the gate"* — and in the same mail praised the builder's **"the third boot is the test"** reasoning as *"the kind of thing that decides whether a regression test is worth having."* **That is a claim about what the product does on the third boot.** The QA pass falsified it: the reasoning holds only for a mutation that consumes no rotation slot, and the product's `setSetting()` consumes one. **The builder held an endorsement worth less than it read, on precisely the reasoning where the defect was hiding.**

**THE DISCRIMINATOR, and it is one question:**

> **Does this sentence describe the PROOF, or does it describe the CODE?**

A proof's design, a disclosure, a stated limit, an admission of what was not measured — all properties of **the artefact the builder wrote**, and all ratifiable from a wrap mail. **A model of how the system behaves is not**, however careful the argument, **because that is exactly the thing the gate exists to test.**

**How to apply:**
1. **Before writing any approving sentence about a builder's reasoning, ask whether its truth-maker is inside the mail or inside the codebase.** Inside the mail → ratifiable. Inside the codebase → it goes to the gate, and say so.
2. **Well-argued reasoning about a mechanism is the highest-risk thing to endorse**, not the safest — it is the form in which a wrong model is most persuasive, and it arrives attached to good work.
3. **Name what the ratification does NOT cover, inline** — *"the design of your proof is ratified; whether the third boot is the test is the gate's question, not Wednesday's."* One clause.
4. **When the gate falsifies something Wednesday endorsed, that goes at the HEAD of the findings mail**, before the findings, not in a footnote — the builder needs to know which of its foundations was borrowed.

**Related:** [[2026-08-10_own-the-spec-not-just-the-escalation]] (testing is mine to demand
and sample), [[2026-08-11_coordinator-not-carrier]] (the QA agent is the org design this
activates), [[2026-08-06_local-proof-is-not-target-evidence]], [[2026-08-07_a-check-that-cannot-fail]],
[[../skills/delegation-protocol]], [[../people/kam]]


## The SHAPE-vs-CORRECTNESS split (2026-09-04, ledger w=78 — Wednesday ratified work the gate then found three Majors in)

**The operative case, so the headline matches it:** an agent's wrap or STATUS mail arrives with
excellent evidence — measurements taken two ways, a control that discriminates, a limit whose
reasoning is better than the fix Wednesday would have asked for. **Wednesday is about to write
"RATIFIED".** Stop. Ask which of two different sentences is being written:

- **"Your evidence is well-SHAPED"** — the proof's design, the disclosure, the reasoning behind a
  deliberate limit, the choice to red-proof against a copy rather than the subject. **This is
  measurable from the mail itself**, because the mail *is* the artefact being judged. Ratify freely.
- **"Your fix is CORRECT"** — the defect is closed, the guard holds, the claim is true of the code.
  **This is NOT measurable from the mail, ever.** The only instrument is the gate.

**The case.** At 12:46:29Z Wednesday ratified #800 — *"the fix is the right shape and your
instrument disclosure is the reason Wednesday believes it"* — on the builder's own evidence, which
was genuinely excellent: the whitespace-inside-quotes limit was correctly reasoned, the fixture read
the shared literals out of the script rather than holding its own copy, and the red-proof ran against
a copy with the subject proven byte-identical by md5. Every one of those was true. Then the batched
through-code pass found **three Majors in the same PR**: the fix incomplete in the same function (the
inline-comment form still prints a green over the shared literal), a correctly-rotated `export KEY=`
value reported BLANK with `docker compose down --volumes` printed as its remedy, and the new
regression suite invoked by nothing — the third occurrence of that class, the second inside a commit
written to close the first.

**Why this is worth its own section rather than a ledger row.** Wednesday *did* defer the SCORE to
the gate, deliberately, and said so. The gate was respected at the layer everyone watches and
bypassed at the layer nobody had named. **A score is a judgement about a session; a ratification is
a judgement about code — and only one of them had a rule attached.** That is the gap this section
closes.

**How to apply:**
1. **The word "RATIFIED" is reserved for shapes, decisions and reasoning.** For code, the sentence
   is *"received, and it goes to the gate"* — which is not a lesser response, it is the accurate one.
2. **Excellent evidence raises the risk rather than lowering it.** This failed on a mail Wednesday
   was right to admire. A well-built proof makes the unproven remainder invisible, because attention
   has already been rewarded.
3. **Name what a ratification does NOT cover, inline.** *"The limit's reasoning is ratified; whether
   `get_value` now catches every form is the gate's question, not mine."* One clause, and it would
   have made this whole entry unnecessary.
4. **A retraction names itself as premature.** Do not soften it into "new information arrived" — the
   information was always going to arrive, from a gate that was already commissioned and already
   running.
5. **Assign the deductions to the session whose work it was**, never to the successor inheriting the
   fix round. The successor is judged on what it does with the finding.

**The dividend, kept because retractions are usually written as pure cost:** the hold s119 placed on
#800's printed remedy — telling Stuart and Peter not to follow it until #800 merges — turned out to
be the thing **protecting them from F-6**, a defect nobody had found when the promise was made. A
bound placed around one known defect can bound a worse unknown one; that is an argument for making
such promises narrow and early, not for regretting them.
