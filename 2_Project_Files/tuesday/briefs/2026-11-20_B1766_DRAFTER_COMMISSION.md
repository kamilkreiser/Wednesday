# B1766 drafter commission -- MPS records pass for PR 221 (MPSCALC-278, the priced or unpriced option) (SEAT-R283)
Commissioned by Tuesday (s296), 2026-11-20. Drafter model: Sonnet (routing row C8). You DRAFT a kit; you write no Jira and no record.

Draft ONE records kit `2_Project_Files/tuesday/briefs/2026-11-20_B1766_SEAT-R283_mps-records-221.md` (+ `.measured`; ALSO save your
drafter report as `2026-11-20_B1766_DRAFTER-REPORT.md` beside it and return its head as TEXT) in the FORM of today's stamped MPS
records kit `2026-11-20_B1758_SEAT-R281_mps-records-218-220-deploy.md` (read it whole, as STAMPED) with the lessons of its STATUS
folded in by name: `!CODING/Datasec/Datasec MPS Commercial Calculator/1_Project_Definition/Briefs/2026-11-20_B1758_STATUS.md`
(Deviations and Corrections first; in particular: no text is filled with PREDICTED ticket keys before the tickets exist; the seat
reads its sources whole BEFORE the Jira writes; a count the kit states is re-measured with the generated copies counted or
excluded by name). Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole. All paths are under /Volumes/Datasec_DEV/TUESDAY or
/Volumes/Datasec_DEV/!CODING/Datasec.

Facts to re-measure at source (repo datasecau/MPS-Commercial-Calculator, MPS GH_CONFIG_DIR, GET only; Tuesday's reads are dated
2026-11-20 about 12:10 AEDT and are pointers, not facts):
- PR 221 squash -> MPS main 565ba142d4d07b183099eee42c1b73f94242489b, one parent 50d2a47195957a8b0c914ab2972d0dc703f9bee3,
  mergedAt 2026-11-20T01:10:05Z; four paths (web/src/screens/ProposalPage.tsx, web/src/proposal/ProposalDocument.tsx,
  web/src/proposal/OnePager.tsx, web/src/proposal/unpriced.test.tsx), each blob equal to head
  42a08f9a9fa1ab81c023561ae88a93d34cc76e41; nine hosted checks on the head, all success; the hosted CodeQL check run title
  "No new alerts in code changed by this pull request". NOT deployed: read the runs on the merge commit and say what ran.
- The builder kit and STATUS: `tuesday/briefs/2026-11-19_B1747_SEAT-M165_mps-v13-lane2-priced-unpriced.md` (as stamped) and
  `.../Briefs/2026-11-19_B1747_STATUS.md`; the WORD-PACK `.../Briefs/2026-11-19_B1747_WORD-PACK.md`.
- The independent review: `tuesday/briefs/2026-11-20_B1761_verify/` (VERDICT.md first line "GATE B1761: GO WITH FINDINGS @ 42a08f9
  on main 50d2a47"; FOR-RECORDS.md lists what to file). Read VERDICT.md and FOR-RECORDS.md WHOLE; every sentence in a frozen Jira
  or records text that says what the review found is matched against the VERDICT row it rests on.

What the kit records (each decision below is Tuesday's as coordinator, never the product owner's; write it that way):
1. MPSCALC-278: ONE comment (what landed, the three clauses of its acceptance check judged one by one as FOR-RECORDS.md does,
   what is not built) and it STAYS OPEN (Backlog; no transition), because "the choice is recorded" is not met in the lasting sense.
2. New tickets on MPSCALC (search each first by symbol, path and phrase, with a control; a true duplicate is commented, not
   created), from FOR-RECORDS.md "Follow-ups to file": (1) harden the committed check to read attribute values and whole-dollar
   forms; (2) narrow the no-new-word cell and commit a priced-markup check; (3) the durable record of the choice; (4) a rental
   unpriced option, marked as needing the product owner's word before any build; (5) part codes in the unpriced documents,
   marked as waiting on the card below; and the builder's off-by-one skip breakdown is a records sentence, not a ticket.
   The Dependabot notice the remote printed at the builder's push ("1 high" on the default branch, alert 11): read the alert by
   `gh api -X GET`, search the board (today's records pass filed a Dependabot ticket among MPSCALC-416 to 421: read it), and
   either add evidence to that ticket or say why a new one is needed.
3. The words: a card is OPEN with the product owner, `mps-278-unpriced-option-three-words-1120` (posted 2026-11-20; options: add
   part codes so the third label is true / change the third label / approve as written; default: the option stays on main only
   and is not deployed). The records say the three words are PENDING and quote no approval. Do not read the card store; the
   kit's Stamp slot carries its state at the stamp.
4. Root records: one CLARIFICATIONS entry (the next C-number, computed by the seat from the file) for the landing and the review,
   BACKLOG and JIRA records as B1758 did, the history line; fast-forward of the root records repository as B1758 did.
Slots for Tuesday's stamp: JIRA WRITE or DRY; which creates run; RECORDS WRITE; the card's state; base facts; hard stop.
Every count by program; every prose list recounted; selectors checked against the names they must match; no predicted number.

HOW: read-only everywhere except your three files and scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s296/d1766/`.
Jira GET only (credentials by name, in-process, from the MPS project's `4_Credentials/.env`, never printed). Git read verbs only in
the project. No `cd` (a hook refuses it); zsh; absolute single-quoted paths; no unquoted word starting with `=`. Clocks from
`date` in the same command. Never delete. Write the kit to disk as you go.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, recommended slots, corrections to this commission, UNMEASURED.
