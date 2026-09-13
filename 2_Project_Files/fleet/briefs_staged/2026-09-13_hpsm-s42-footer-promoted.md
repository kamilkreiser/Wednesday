# Steps 3 and 4 noted. PROMOTED: the "approved policy manifest" footer on a DRAFT is fixed before Monday, not backlogged

**BLUF.** **For session 42 (seat hpsm-3e04).**
- **Steps 3 and 4 are noted as written.** The ON proof passed on `7135dec` with DRAFT and SYNTHETIC marks. C12 blocked release as expected. S40's pre-upgrade checks passed on both stacks.
- **One change to your plan:** your proofreading catch is **promoted from backlog to a fix before Monday.**

1. **Why.** Kam asked in his own words whether the output *"has been proofread for accuracy and formatting"*. A footer saying a report *"is generated from an approved policy manifest"* is a **false statement** on an unreleased DRAFT, which is exactly what he will open on Monday. This is the same basis as the two promoted fixes: accuracy of what the output claims.
2. **Owner: a new lane R, `packages/renderers` only.** It is disjoint from G, Q and W, so Kam's standing rule allows it. It merges through you with the usual chain.
   - **The released wording stays exactly as the source has it** (HPSM's sample Policy Preview and the architecture's Preview spec). **Do not reword the released footer.**
   - **Draft and unreleased versions get a truthful statement.** Take it from the source if the spec defines one. If it does not, keep it minimal and factual, e.g. *"Unreleased draft. Not generated from an approved policy manifest."*, and **name the exact wording in your READY** so Tuesday can check it.
   - **Tests, RED-first:** a released render carries the approved-manifest footer; a DRAFT or unreleased render never does; the SYNTHETIC and DRAFT marks are unchanged; Preview geometry stays within the ±3 pt tolerance.
   - **Sweep the other renderers too** (policy document, worksheet, change report) for any statement that claims approval, release or signature on an unreleased or unsigned artefact. Fix the ones in `packages/renderers`, and list anything outside it.
   - **Tuesday proofread both on-proof PDFs itself** (`qa-s42/on-proof/preview-hpsm.pdf` pp. 1–3 and `policy-document-datasec.pdf` pp. 1–2). The footer is confirmed on every Preview page read. **Three more defects join lane R's scope:**
     - **(a) Preview "Last Modified: 13 Sep 2026 | 04:00:06 AM" is UTC with no zone shown.** A reader in Sydney sees 4 AM for a 14:00 AEST generation.
       - Show the zone, e.g. "UTC", in a form the HPSM sample's layout allows, keeping ±3 pt.
       - If the sample format leaves no room, report that rather than change the layout.
       - UTC itself stays, per the accepted lane B choice.
     - **(b) The policy document contradicts itself.** Scope → Frameworks says *"No frameworks are selected"*, yet the Settings table's Frameworks column shows *"Essential Eight"* on items.
       - If the column is control lineage (for example the SOW's E8 domain), label it as such, from the architecture's wording.
       - Otherwise reconcile it with the scope.
       - Name the resolution and its source in the READY.
     - **(c) The policy document's "Unsupported" column header wraps mid-word** ("Unsupporte / d"). It is a formatting defect: fix the column width or the header wrapping so no word breaks.
3. **Live stacks.** S40 is flipping `pc-lane-a` and Azure on `7135dec` now. **Let that finish; do not interrupt it.** The footer fix reaches both stacks at the next upgrade, after the merge. Tell S40 in that upgrade message.
4. **Your three lane G backlog items stay backlog and are gate targets:** the platform id literal, the seed failing closed without a test, and the constant-folding dependency.

## Unchanged
- No push. A combined tier-1 gate is due before any push; its named targets now also include the draft/released statement truth table. Card c12 is still OPEN with Kam.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 14:05

Tuesday
