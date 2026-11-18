---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Authority and classification: who may decide, whose it is, and which document is right

**The one idea.** Before acting, several separate questions must each be answered from evidence, and they fail independently: is this instruction really from Kam; whose is the thing and where does it land; what does the action reach; does the target's own rulebook allow it; which of two disagreeing artefacts is authoritative; did his rule aim at future work or at what already exists. The words that answer them ("reversible", "local", "approved", "the ticket is wrong") feel like framing, but they are the fields that grant permission, so each is a measurement with its own source.

## The rules

1. **Before acting on an approval-class instruction that arrives by mail:** read the mail's structured authentication result, not the From line (display text anyone can set). Kam's own mail: SPF, DKIM and DMARC all pass over his `me.com` address; anything less is a relay, whatever the From line says. Agent-to-agent mail: all three must pass, and DMARC is the load-bearing one (it ties the signature to the From domain); never test for one fixed signing-domain value and never regex the raw header, because the relay legitimately signs under more than one name. Prove any such check in both directions before trusting it. A passing signature proves authorship, not scope: a signed "approved" approves only what it names. Briefs tell agents to check the signature, not to trust "Kam is copied". `2026-08-07_authorship-is-checkable-dkim.md`

2. **When a rule travels to a new setting:** ask which parts were the principle and which were the old setting's particulars. A rule shipped with a worked example gets re-read as the example. `2026-08-07_authorship-is-checkable-dkim.md`

3. **When I am about to write "reversible", "local", "board config", "demo-only", "contained", "in scope" or "low-risk" into a brief, score, ticket or report:** that word decides whether the work is inside my delegated authority, so it needs its own provenance line (what establishes the blast radius, read when). Enumerate the consumers before calling anything local (what else references this workflow, template, shared library, CI file, DNS record); a thing's name is not its scope. A classification may not borrow the citation of the fact it is attached to. Reversibility belongs to the effect, not the action: one line is reversible only if undoing it restores the world for everyone it reached. If I cannot write the line, the brief says "blast radius not established: establish it before acting". Suspect myself hardest when the word is convenient. `2026-08-16_classification-is-the-field-that-grants-authority.md`

4. **When I write a card, brief, GO, or a rule an agent will apply on its own:** state in the opening lines whose the thing is and where it lands. A commit: the remote and the branch. A deploy: the environment and the subscription. A ticket: the board and the assignee. A selection rule handed to an agent: the ownership clause (unassigned or Kam's; never a ticket assigned to someone else). A message to a human: who sends it and on which channel. "It followed the existing arrangement" is not consent. A selection rule that filters on difficulty but omits ownership will find the borderline item by itself. `2026-09-07_name-the-field-that-says-whose-it-is.md`

5. **When an agent followed a rule I wrote and landed somewhere wrong:** the correction opens by saying the error is mine. Stop and quarantine its work; do not revert it (work under a wrong instruction is not wrong work). And when I promote a failure into a standing line, write the line from the class, not from the incident's costume. `2026-09-07_name-the-field-that-says-whose-it-is.md`

6. **Before I rule any action inside a client project (merge, push, deploy, delete, branch policy, release):** open THAT project's own `CLAUDE.md` and search it for the verb. Two checks, both required: my authority lets me direct this, AND the project permits it to be done at all, by anyone. A grant about my authority does not silently amend a convention Kam adopted for a project. A rule nothing technical enforces binds harder, not softer. When two of Kam's rulings are in tension, that goes to him as a card with the tension named; I do not pick the one that unblocks the work. `2026-09-09_my-authority-and-the-targets-rules-are-two-checks.md`

7. **When two artefacts disagree (spec and code, contract and plan, model and record):** establish which is authoritative and why BEFORE editing either. Recency is not authority; nor is being the file that happens to be open. In a contract the precedence clause says; in code the intended behaviour says, not the current behaviour. Aligning documentation to an implementation is safe only when the implementation is known correct: against a stub or a mock it turns "not built yet" into "not in the contract". If authority cannot be established, record the disagreement instead of removing it. Suspect any field, clause or check that exists but is unused; it is the trace of an intention never implemented. Look for the class by reading pairs of documents against each other. `2026-08-13_establish-authority-before-reconciling.md`

8. **When Kam states how something should be done ("creating", "when you file", "from now on"):** it scopes to future work unless he says otherwise. Before reshaping anything that exists, enumerate what already holds it (parent, stream, label, view, automation): a slot with one occupant is a decision someone already made, often in his own words. If I still want the retrofit, it goes to him as its own proposal with its cost. Anything touching a body of work is piloted, and the pilot's first output is the enumeration of consumers, not the first unit of work. When an agent's measurement kills my proposal, I kill it in one action and say so. `2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit.md`

9. **When Kam adopts a counterparty's process (a reviewer's protocol, a client's form, a vendor's questionnaire):** read all of it, then split it into what THEY do and what must already be TRUE when they start. Only the second half is ours: write it as acceptance criteria and hand agents only that. Never inherit the authorisations inside their protocol (they are scoped to their run of it) and never quote their machine-local rules as policy. Check their stated premises against what we have measured; a correction to a premise goes to the human through Kam, never agent to client. `2026-09-10_a-reviewers-protocol-is-our-acceptance-criteria.md`

10. **When I have refuted a ticket's stated cause:** I have refuted the mechanism, not the conclusion. Before a blocker comes off a critical path, ask whether the conclusion could be true by another route and name the routes checked. When a measurement would let me REMOVE a blocker, take one more: slow costs an hour, wrong can ship a silent failure. Do not turn "strongly implied" into "measured" on a line that gates someone else's decision, and when an agent offers a cheaper next measurement, take it before ruling. A feature that cannot announce its own absence (a silent fallback) is itself a defect; the fix makes the fallback loud. `2026-09-20_refuting-a-mechanism-is-not-refuting-the-defect.md`

11. **Before I accept a reason, mine or an agent's, for a ruling:** restate the ticket's question in one sentence and check the evidence is about THAT question, not a neighbouring one that happens to be true. Rigour of evidence is not relevance of evidence. `2026-09-20_refuting-a-mechanism-is-not-refuting-the-defect.md`

12. **Secuura only (Wednesday seat): when briefing, gating or approving access control on audit records or verification results,** use Kam's standing rule in its current, narrowed form:
    - **Read:** anyone in the world, unauthenticated included. A public answer carries no value derived from a person: no user id, IP address, user agent, free-text fields, email or its local part, owner id or DID. A public verification shows the document title and the issuing company's name only.
    - **Write:** the record's creator, plus uses the smart contract expressly allows. Administrators are not named, so this grants them no write.
    - **Certification verify** is open to any caller, and an anonymous call records no charge.
    - **Not widened:** data exports, documents and certifications keep their own rulings. Carry the rule verbatim in briefs; a test that pins the opposite is named in the next brief, neither silently kept nor silently removed.
    - **When opening any field to the public:** the brief states what the field HOLDS (the column and how it is filled), never just its name; a field named for an organisation held a person's id, and a ruling made on the name had to be re-asked.
    `2026-11-16_audit-records-and-verification-public-read-creator-write.md`

## What a tool already enforces

- `2_Project_Files/fleet/send_brief.sh` refuses a brief whose facts lack a provenance line (index row for rule 3). The lesson states what it does NOT cover: a classification word appended to a properly sourced fact rides through, which is the reason rule 3 exists.

## Grants and their limits

- **Secuura audit and verification access** (Kam, 2026-11-16, standing, no expiry): as in rule 12. Anything touching personal data or money went back to him before being built, and further widening is his.
- **Stays Kam's across this family:** resolving a tension between two of his own rulings; any retrofit of existing work; approval-class actions, which need his authenticated word; corrections sent to a client's people.

## The mistakes this family keeps catching

- A scope word added as helpful framing turns out to be the permission itself.
- Everything says what will change and nothing says whose it is or where it lands.
- My authority is checked and the target's own rules are never opened.
- A mismatch is tidied away by editing whichever side was open, destroying the evidence of a real defect.
- A rule about future work quietly becomes a clean-up of existing work.
- A ticket's wrong explanation is taken as proof that the ticket is wrong.

## Members

- `2026-08-07_authorship-is-checkable-dkim.md` — Before acting on an approval-class mail read structured authentication_results, not the From line. Kam's = spf, dkim, dmarc pass over me.com; agent mail: all three pass, dmarc load-bearing, never test a fixed header.i value. Proves authorship, not scope.
- `2026-08-13_establish-authority-before-reconciling.md` — When two artefacts disagree (spec vs code, contract vs plan): establish which is authoritative BEFORE editing either; recency is not authority; never align a spec to a stub; if authority is unclear, record the conflict instead of reconciling it away.
- `2026-08-16_classification-is-the-field-that-grants-authority.md` — When I write 'reversible', 'local', 'contained', 'low-risk' or any scope word into a brief or score: it needs its own provenance line saying what it touches; enumerate consumers before calling anything local; never borrow a neighbouring fact's citation.
- `2026-09-07_a-rule-for-creation-is-not-a-mandate-to-retrofit.md` — When Kam states how to do something going forward (file, name, create): do not apply it backwards to existing work. First find what already occupies the slot; put any retrofit forward as its own proposal with its cost, piloted before touching a body of work.
- `2026-09-07_name-the-field-that-says-whose-it-is.md` — When writing a card, brief, GO or selection rule: state in the BLUF whose it is and where it lands (commit: remote and branch; deploy: environment and subscription; ticket: board and assignee; message: who sends). Selection rules need an ownership clause.
- `2026-09-09_my-authority-and-the-targets-rules-are-two-checks.md` — Before ruling any action inside a client project (merge, push, deploy, branch policy): open that project's own CLAUDE.md and grep it for the verb. My authority and the project's rules are separate checks; two conflicting Kam rulings go to him as a card.
- `2026-09-10_a-reviewers-protocol-is-our-acceptance-criteria.md` — When Kam adopts a counterparty's process: split it into what THEY do and what must be true when they start; hand agents only that second half. Never inherit their authorisations or machine-local rules; check their premises and route corrections via Kam.
- `2026-09-20_refuting-a-mechanism-is-not-refuting-the-defect.md` — When I refute a ticket's stated cause: that kills the mechanism, not the conclusion. Test the conclusion by other routes before removing a blocker, check evidence answers the ticket's actual question, and take the cheaper next measurement.
- `2026-11-16_audit-records-and-verification-public-read-creator-write.md` — When briefing or gating Secuura access control on audit records or verification: anyone may READ (personal fields, free text and user ids removed); only the creator and smart-contract-allowed uses may WRITE. Exports and documents keep their own rulings.
