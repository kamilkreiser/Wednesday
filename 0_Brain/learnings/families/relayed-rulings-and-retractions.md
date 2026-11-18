---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Relayed rulings and retractions: keeping a decision, or its withdrawal, true where the next reader lands

**The one idea.** A ruling, a clarification and a retraction are all fact-changes, and each one has to survive after the moment it was spoken. It must land verbatim in the artefact the next reader opens, it must be no wider or narrower than what was actually decided or measured, and it must still be true after the world moves under it. Correcting yourself is the highest-risk act of a session, not the safest.

## The rules

1. **When about to withdraw something I said because someone refuted it:** first write down exactly what the refuting measurement covered (file, lines, command, the claim it tested) and withdraw only that. Name the measurement and its scope inside the withdrawing sentence itself, for example "measured in suite A; withdrawn for suite A; unknown for suite B". If the retraction is broader than the measurement, it is wrong. `2026-09-06_a-retraction-inherits-the-scope-of-its-measurement.md`

2. **When the thing being withdrawn was a bundle of claims:** retract one claim at a time and check the provenance of each half separately. Claims that arrived in one paragraph may have different authors and different evidence, and only one may have been refuted. `2026-09-06_a-retraction-inherits-the-scope-of-its-measurement.md`

3. **When a retraction affects someone else's document:** never tell them to edit their text on my say-so. Say what was measured and ask them to check whether their text rests on it. `2026-09-06_a-retraction-inherits-the-scope-of-its-measurement.md`

4. **When the withdrawal is being sent as an urgent relay, to stop someone building on bad information:** that is exactly when over-withdrawal happens, so the scope clause in rule 1 is mandatory there, not optional. Prefer the precise correction ("the test must live in a harness that does not mock its own subject away") to the vague safe one ("that approach is wrong"): the vague one is what the next reader implements. If a retraction tidies more loose ends than the measurement opened, re-read it. `2026-09-06_a-retraction-inherits-the-scope-of-its-measurement.md`

5. **When a retraction has been correctly sized:** it is still not finished. Grep for the claim (the belief, not the sentence; the wording will differ) in the handover, the daily note and any brief already staged, and remove it from every artefact carrying it. The closing check is absence everywhere, not "I fixed the line I was looking at". `2026-09-06_a-retraction-inherits-the-scope-of-its-measurement.md`

6. **When recording a ruling:** in the same action record what the chosen option depends on, the condition that made it the right answer, especially when that condition is a current defect, a temporary state or someone else's unfinished work. Write the dependency at both ends: on the ruling's own ticket or card and on the ticket whose fix would remove the precondition, each naming the other. The end that matters is the one a person is holding when they merge. A defect that is doing useful work gets said out loud. `2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition.md`

7. **When about to merge any fix:** ask what currently relies on the broken behaviour (cutovers, migrations, grace periods, retry loops, manual workarounds), not only who is hurt by the bug. For any ruling with a condition attached ("once the log shows X"), ask whether this change makes the condition unobservable: a trigger that can no longer occur is a ruling that silently never completes. A precondition removed at a lower layer breaks more than the layer that used it. `2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition.md`

8. **When a fix collides with a standing ruling:** look first for a parameter or configuration path that keeps both (often one the fix already ships) before proposing to hold the merge, revert, or change a default Kam ruled. A delivered ruling and a still-true ruling are different properties; only delivery has a mechanism. `2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition.md`

9. **Tuesday seat, Datasec projects only. When Kam clarifies or rules something about a project (how it used to work, what is intended, what is in or out):** his words go verbatim, with date and channel, into that project's own `1_Project_Definition/CLARIFICATIONS.md`.
   - Live agent: relay verbatim; the relay is closed only when the agent mails back the entry's C-number.
   - No live agent: park the words verbatim in the coordinator's `0_Brain/projects_index/clarifications_register.md`; the project's next brief carries them under RULED BY KAM; the register row moves to "recorded" with the C-number.
   - No file yet: the next brief's first item creates it (numbered entries, provenance, supersede never delete) and wires it into that project's boot read.
   - The coordinator never writes the project's file itself; the register is a holding pen, not a substitute.
   `2026-09-17_every-project-keeps-kams-clarifications.md`

## What a tool already enforces

Nothing in this family is enforced by a tool according to the index. The retraction lesson says its scope clause was added to the brief standing lines so it travels in briefs, and records its own enforcement state as "rule only": a wrap step that greps for retracted claims was named as a candidate and not built.

## The mistakes this family keeps catching

- A withdrawal wider than the measurement behind it, which quietly kills a live finding nobody is guarding.
- A correctly sized withdrawal applied to one sentence while the same belief still leads the handover.
- An instruction to "correct your document" issued on the authority of a retraction instead of a measurement.
- A routine fix that never mentions a ruling yet removes the defect or temporary state the ruling relied on.
- A conditional ruling whose trigger can no longer be observed, so nothing errors and nothing ever completes.
- A clarification from Kam relayed in chat and counted as done without proof it reached the project's own record.

## Members

- `2026-09-06_a-retraction-inherits-the-scope-of-its-measurement.md` — When withdrawing something I said: name the measurement and its scope in the same sentence and withdraw only that, claim by claim. Then grep the handover, daily note and staged briefs for the claim itself. Never tell a reader to edit their text on my say-so.
- `2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition.md` — When recording a ruling or merging a fix: write what the ruling DEPENDS ON (often a defect doing useful work) at both ends. Before merging ask what relies on the broken behaviour and whether the ruling's trigger can still occur; prefer a parameter to a revert.
- `2026-09-17_every-project-keeps-kams-clarifications.md` — When Kam clarifies or rules on a Datasec project: his words go verbatim into that project's 1_Project_Definition/CLARIFICATIONS.md; a relay is done only when the agent mails back the C-number. No live agent: park in the register. Never write it myself.
