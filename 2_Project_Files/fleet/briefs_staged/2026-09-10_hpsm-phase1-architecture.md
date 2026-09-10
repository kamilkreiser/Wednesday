# Brief — HPSM Phase 1: architect the Datasec-branded Policy Composer, ready to build

**Commissioned by Kam, 2026-09-10. He has answered the scoping questions himself; his words are
below and they OVERRIDE any earlier reading, including Tuesday's.** Produce an ARCHITECTURE this
round. Do not start the product build — Tuesday commissions that separately once the architecture
is reviewed.

## KAM'S ANSWERS, VERBATIM — these are the scope

> **1)** internal means used as a commercial product but sold by Datasec (and delivered to Datasec
> clients), not sold by HP and not branded HP.
> **2)** all. everything to generate the output I attached is in this phase
> **3)** every output provided is included. Branding needs to be flexible
> **4)** full authority to build, spin up resources (local first until I approve). We will be
> running this against HP printers. The main difference is that this version will be sold by datasec

> *"sorry. the discovery questionnaire was included by accident"*

**What each one settles:**
- **"Internal" does NOT mean internal-use.** It is a **commercial, Datasec-branded product sold and
  delivered to Datasec's clients**. Tuesday initially read it as an internal tool and was wrong.
  **It stays a real multi-tenant product; it simply is not HP's.**
- **Scope is ALL**, bounded by a test: *everything needed to generate the attached outputs*. Any
  earlier proposal to drop multi-tenancy, approval workflow or versioning is **withdrawn** — do not
  resurrect it.
- **Every attached output is in scope, and BRANDING MUST BE FLEXIBLE** — the sample is an HP-branded
  report and this product is not HP-branded. Branding is a configuration concern, not a template edit.
- **Local first.** Full authority to build; **NO cloud resources and nothing billable until Kam
  approves.** This is a hard line, not a preference.

## SOURCES — read all of them; they are the specification

`/Users/kamil/Downloads/Archive/`
- `Datasec_HPSM_Cloud_Policy_Composer_Detailed_Scoping_Design_Specification_v1_1.docx` — **the
  primary input.** 54 headings: object model + DB constraints, 10 screens, universal questionnaire
  logic, deterministic rules engine and precedence, validation/release gating, exceptions, output
  generation and Policy Bridge, API design, NFRs, testing, and **Appendix A (22 categories),
  Appendix B (26 universal discovery questions), Appendix C (123-control registry), Appendix D
  (dictionaries)**.
- `Policy Preview.pdf` — **the target output**, in HP Security Manager's own report format:
  hierarchical policy items (`Authentication > Credentials`, `Device Control > Stored Data`,
  `Network Services > Web` …) with **Policy Value · Severity · Remediation · UnSupported**.
- `HPSM Policy Composer - Screens.pptx` — the screen designs. **Measure the layout into the
  architecture; a picture does not survive into a build unless someone writes it down.**
- `HP_Solutions_Centre_HPSM_Essential_Eight_SOW.docx` — the engagement this serves; 100 policy
  settings, Essential Eight maturity targets, and the scope qualification that HPSM covers the
  printer/MFP boundary only.
- `image.png`.
- ⛔ **`Datasec_Consolidated_Discovery_Questions_and_Responses.docx` — EXCLUDED. Kam confirmed it was
  attached by accident.** It is Datasec's own CRM/finance/warehouse discovery and has nothing to do
  with this product. Do not read it into the design.

**First action: copy the five in-scope files into `1_Project_Definition/Source_Documents/` in this
project**, so the architecture cites a stable path and not someone's Downloads folder.

## WHAT TO PRODUCE

An architecture a builder can start from tomorrow, in `1_Project_Definition/Architecture/`:

1. **The canonical object model**, honouring the spec's non-negotiable cardinality —
   `Tenant 1:N Engagement`, `Engagement 1:1 Policy`, `Policy 1:N PolicyVersion` — enforced by
   **database constraint AND API logic**, because the spec says a second policy per engagement is a
   data-integrity error.
2. **The rules engine**: how the 26 discovery answers and the 123 controls combine deterministically
   into a policy, how dependencies resolve, how conflicts are decided, and what precedence applies.
   **This is the hard part and the part everything else exists to serve — architect it first and in
   the most detail.**
3. **The output pipeline.** Recommend and justify the internal representation. Tuesday's view, to
   accept or overturn with reasons: **generate a canonical JSON manifest first and render every
   document from it** — the HP-style preview, the Datasec DOCX/PDF, the evidence matrix, the
   implementation worksheet. That makes branding a render-time concern, which is what "branding
   needs to be flexible" requires.
4. **The screens**, mapped to the spec's ten, with what each needs from the model.
5. **The local-first deployment shape**, and — stated separately — what would need cloud resources
   later and roughly what it would cost, **as information for Kam's approval, not as a request.**
6. **The build plan**: what an agent builds first, what can run in parallel, what the definition of
   done is per piece. Tuesday commissions the build from this.

## HOLDS

- **Architecture only this round. Do not build the product.**
- 🔴 **NO cloud resources, no Azure, nothing billable.** Local only until Kam approves.
- **Nothing HP-facing.** Only Kam talks to HP.
- Read-only on Jira; report what should be filed.
- Never put a secret in any artefact.
- Do not email Kam. Mail **`tuesday-agent@agentmail.to`**.

## RAISE RATHER THAN GUESS

Kam has said plainly he would rather be asked than have someone guess. **Anything the spec leaves
genuinely ambiguous goes in your wrap as a question with your recommendation and your reasoning** —
Tuesday files it to his decision panel in that shape, which is his standing instruction. **Do not
bury an assumption in the architecture.** List every assumption you did make at the top, so he can
overturn any one of them in a line.
