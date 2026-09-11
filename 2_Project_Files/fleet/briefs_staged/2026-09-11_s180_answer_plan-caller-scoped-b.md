# ANSWER — plan confirmation s180 — YES: build B as your caller-scoped rule

## BLUF
- **YES. The caller-scoped rule is inside Kam's ruling B — build it now. This SUPERSEDES the stop-trigger in brief §6, by name, for this rule only.** Your STOP was exactly right. That trigger existed because a GLOBAL resolve over non-unique refs picks an Organisation by chance. Your rule resolves only the caller's own Organisation — the only resolution that could ever pass the compare — so that failure cannot happen (your row 6). Any OTHER departure from option B still stops.
- **Your table is ratified as a SHAPE:** rows 1-10, 403 and not 404 on row 5, no unique index this round. **Whether the code does what the table says is the tier-1 gate's question, not Wednesday's.**
- **The card's error is Wednesday's, not yours:** "B keeps issuer_organization_id recording the issuer" was wrong — under the bind, A and B both record the signing key's Organisation. Kam is being told on his panel, with the default that you build B. If he changes the ruling, Wednesday mails you with SUPERSEDES.
- **Your recommendation is accepted:** in the same PR, amend `S-K-OWNERSHIP-CONTRACT.md:176`, the `organizationUuid` wording in `originate.openapi.ts` plus the regenerated yaml, and the KS-978 cells. The PR body says in terms that issuer ≠ signing-key org stays 403.

## Recommendation — what to do
1. **Item 1 now.** Branch, push and HOLDS exactly as the brief says (MAIN checkout, no `-u`, push protocol, STOP and mail on any DIFF, never restore).
2. **Cells Wednesday adds — every one is about the REAL read, not the rule:**
   - **(a) Row 3 → 201 and row 4 → 403 with the caller-Organisation read running as the database role originate really uses, under the request's real tenant context.** Your DB measurements ran as a superuser with BYPASSRLS, which sees through row-level security. UNMEASURED by anyone: whether the `organizations` read is subject to RLS for originate's role. If it is and the read comes back blind, row 3 refuses every S claim in the real stack while every superuser test stays green — the shape the #930 tier-1 gate found (a read blind under fail-closed RLS). **If the read is blind, STOP and mail; do not reach for a bypass.**
   - **(b) Row 9 as a cell:** the caller-Organisation read throws → no 201 and nothing written.
   - **(c)** In the row-3 cell, assert `metadata.sIdentity.organizationUuid` still carries S's GUID and the column carries the caller's K id.
   - **(d)** A case-variant claim in both directions (upper-case GUID against a lower-case stored ref, and the reverse).
3. **Red-proof:** remove the new arm → row 3 goes red while rows 2 and 4 stay green; the rewritten KS-978 cells redden on the same removal; restore sha256-identical; cells RUN quoted on every run.
4. **Test Evidence:** the published spec changes, so Schemathesis is in scope; record the local gateway restart.
5. **Item 2 — the Stuart draft — can be written now.** Draft only; Kam sends. It says plainly:
   - Kam ruled B. K accepts S's Organisation GUID when it is the calling Organisation's own externalRef. S changes nothing.
   - #810 is Stuart's to revert once B is deployed, or to keep as a stopgap until then.
   - Contract line `:176` is amended in the PR — quote the old and the new wording.
   - **Issuer ≠ signing-key Organisation stays refused under A and under B.** His cost #1 is solved by neither, and the draft says so.
   - What is measured and what is inferred about kintsugi and demo-pk.
6. **Your path 2** (the gateway `/originate/` mount with no gateway auth): not this round. One line in your handover, as an untraced question.

## Detail — for the record
- **Authority:** v1.3 — scope and sequencing inside work Kam commissioned, and an agent's deviation accepted on technical grounds. Not a signature class: nothing merges or deploys this round.
- **SUPERSEDES:** brief §6, *"if item 0 shows option B is not what the card assumed — externalRef is not unique … STOP and mail before building. That goes back to Kam as a card"* — superseded for the caller-scoped rule only.
- Your line-number re-derivations (Stuart's `:487-490` holds, the 2026-09-07 `:450` is stale, the card's `platform.ts:598` is exact) are noted. The stale one was in Wednesday's brief as someone else's reading, which is why it said "re-derive".

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 15:57
