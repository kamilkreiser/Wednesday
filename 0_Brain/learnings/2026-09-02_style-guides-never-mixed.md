---
date: 2026-09-02
type: correction
source: "Kam, 2026-09-02 07:3x (terminal, verbatim in Discovery/00_prompt-log.md): 'I also noticed that the nexus page (in testing) is adopting blue backgrounds (this is secuura not Datasec). Please make sure project style guides are adhered to an never mixed' — after eight QA passes and three scored rounds of NexusAI dark-mode work, none of which measured brand fidelity"
status: live
supersedes: ""
---

# Project style guides are adhered to and NEVER mixed — a palette is client identity, and contrast is not conformance

**The operative case, so the headline matches it:** I am briefing, accepting, scoring, or ruling a deploy on ANY visual change — a theme, a colour, a component, a layout — for a client project. **Ask: which document says what this project looks like, and does every colour in the change resolve to it?** If no such document exists, the change has nothing to conform to, and "it passes contrast" is a check that cannot fail on the question Kam actually cares about.

**What happened.** NexusAI's dark-mode campaign (rounds 6–8, passes 5–9) shipped a dark theme whose grounds are a navy/indigo family (`#1a1a2e` / `#1e1e3f` / `#252550` / `#16213e` at head `6b78315`). Every pass measured contrast ratios in a real browser and got better each round; three sessions were scored 0.85–0.90 for craftsmanship. **Kam looked at the page once and saw another client's aesthetic.** Measured after his message: the values are not literally copied from the other project — they are the stock "dark mode = navy" palette a model reaches for when nothing constrains it — and **NexusAI's repo contains no style guide, brand-token or palette file at all.** The product's own brand blue (`#0096d6` family) exists in the light theme; nobody was asked to derive the dark theme from it.

**Why this is the very-important-#1 family and not a design nit.** Kam's standing rule (2026-08-03, R0 in delegation v2): no bleed between clients — code, names, credentials, context. **Style is identity too.** A Datasec product that LOOKS like Secuura is contamination a customer can see without reading a line of code. And it is the costume the R0 machinery is blind to: nothing leaked through a bus or a brief; a builder with no palette to obey invented one, and an aesthetic association did the rest.

**The coordinator's gap, owned:** eight passes of "every visible text node ≥4.5:1" and zero of "every colour comes from this project's palette". I wrote the acceptance as a contrast leg because the tickets were contrast tickets; brand conformance was never a leg, never a brief line, never a completion question — **a check that could not fail on brand**, run nine times with rising confidence. Not self-caught: Kam caught it from a screen.

**How to apply (from now, every UI change, every project):**
1. **Every UI brief names the project's style guide / brand-token source as a pointer** — a file the agent reads FIRST. If none exists, **item 0 of that round is to write one from the project's existing brand tokens** (the light theme, the logo, the customer's own guide where the project is a client deliverable — HP for the HP Authentication Suite work), and NO invented colour ships until the guide exists.
2. **Brand conformance is a completion leg beside contrast:** every colour introduced by a change resolves to a token in the guide, enumerated by the QA pass as a table (value → token or **OFF-GUIDE**). An off-guide colour is a Major, at any contrast ratio; an allow-list for it does not exist.
3. **A palette is a BRAND decision = Kam's signature class** (the RD-160 precedent: brand chrome reserved for him). A dark theme derived from the guide is presented to Kam as a rendered proposal (screenshots, both modes) before it ships — the derivation is the agent's; the approval is his. **No deploy of a themed surface without that approval on the record.**
4. **Never mixed — the negative test:** before scoring any visual change I ask the one question I never asked here — *would Kam recognise this as THIS client's product at a glance?* If I cannot answer it, the QA pass gets a brand leg and I do not score until it lands.
5. **Fleet-wide standing line for every UI brief:** "Palette from THIS project's style guide only; if none exists, write it first from the project's own brand tokens; no invented colours; a colour that does not resolve to the guide is a Major regardless of contrast."

**Immediate consequences (2026-09-02):** the pass-9 brief carries a brand-conformance ADDENDUM; the NexusAI rounds 6–8 deploy is HELD on a Kam-approved palette regardless of pass 9's contrast verdict; s17's item 0 = the style guide + the derived dark palette as a proposal to Kam; the fleet brief template gains the standing line.

**Related:** [[2026-08-03_role-beyond-code-three-priorities]] (very-important #1 — no scope creep between projects, "embarrassing or worse"), [[2026-08-04_delegation-v2-observability]] (R0: no bleed between clients — this is R0's visual costume), [[2026-08-13_shared-bus-tag-filter-or-leak]] (the same family at the comms layer), [[2026-08-07_a-check-that-cannot-fail]] (nine contrast passes that could not fail on brand), [[2026-08-16_classification-is-the-field-that-grants-authority]] (a palette is a brand classification — Kam's), [[../people/kam]], [[_ledger]]
