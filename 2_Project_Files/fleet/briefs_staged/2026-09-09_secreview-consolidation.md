# BRIEF — CONSOLIDATION: apply five seats' verdicts to the register, in ONE action

**From:** Tuesday (s2). **You are a fresh seat with no stake in any partition — that is deliberate.**
The five verdicts were produced by five agents; **you produced none of them**, so you are the first
reader who can weigh all five without defending any.

## BLUF

**Read all FIVE verdict files. Apply their proposed changes to the register together, in one action.
Re-add the reconciliation both ways. Verify the rendered `.docx` by reading it, not by trusting an exit
code. Conserve the estate total unless a verdict explicitly adds or removes a finding.**

    _Working/verification-2026-09/round2-a.md      · HPAuthenticationManager · infra_hpam   (19 rows)
    _Working/verification-2026-09/round2-b.md      · License-Services · LicenseServer       (25 rows)
    _Working/verification-2026-09/round2-c.md      · HPK · UniversalPrint · MailFlow · CypherSharePoint · QuickAccessLibrary (28)
    _Working/verification-2026-09/round2-d.md      · Task-Dispatcher · marketplace · admin-portal · WorkPath · cc-api · hpam-api · SPDF-D1 (25)
    _Working/verification-2026-09/round2-june.md   · the JUNE baseline, 03_Findings_Register.md (31 rows)

**FIVE, not four.** Seats B, C and D were briefed when there were four and their headers say so; the
June seat was added on Kam's later ruling. **If a verdict file tells you to read "all four", it is
stale in that one respect and in no other.**

## 🔴 THE THINGS THAT MAKE THIS DANGEROUS, NAMED SO YOU CAN AVOID THEM

1. **This is the ONLY moment in the whole round when the register is written.** Five seats deliberately
   did not touch it so that this one action could be atomic and checkable. **Do not make it two actions.**
2. **CONSERVE THE TOTAL.** The estate stands at **339**. A band move changes the split, never the total.
   **Re-add the reconciliation table by ROW and by COLUMN and state both sums.** If they disagree, stop
   and report — do not reconcile by adjusting a cell to make it balance
   ([[2026-08-13_establish-authority-before-reconciling]]: reconciliation destroys evidence).
3. **The `.docx` is what ships.** Regenerate it with `_Working/build-doc13.sh` and **verify by extracting
   the changed rows back out of `word/document.xml`**, as round 1 did (11/11). A `.md` fixed and a
   `.docx` stale is the same defect in a worse place.
4. **Quarantine before you write** — `.pre-consolidation-2026-09-09_*` beside the deliverable, both
   formats. Never delete.
5. **June is a SEPARATE DOCUMENT.** `round2-june.md` applies to `03_Findings_Register.md`, not to the
   2026-09 register — **except** where the June register's rows feed the estate tally, which they do
   (June contributes 31 of the 339). **Say explicitly how you handled that, because it is the one place
   the two documents interact and it is easy to double-count.**

## WHAT A VERDICT ENTITLES YOU TO DO

**Apply what a seat PROPOSED for its own partition.** That is what they were commissioned for and their
reasoning is in the file.

**Do NOT apply, and instead list for Tuesday:**
- Anything a seat marked **out-of-partition**, or "not my verdict, do not apply on my say-so" — seat A's
  file has such a section by name.
- Anything where **two seats disagree** about the same row or the same shared fact.
- Anything that would **create or delete a finding** rather than re-score one.
- Anything a seat flagged as needing a **second reader**, a **live datum**, or **Kam**.

**Where a verdict's own arithmetic does not reproduce, say so and do not apply that row.** You are
entitled — expected — to recompute any CVSS vector yourself. **Validate your implementation against
published reference vectors before you trust it**; every seat this round did, and one of them caught
its own recalled reference vector being wrong rather than its calculator.

## HOLDS

No live pass; the tenant question is unresolved and Kam's. `Source_Code/` read-only. No secret value,
prefix or redacted head. No client-facing comms. No Jira writes. Never delete — quarantine.
**No ticket creation.** **Round 2 of 2 under the cap — this is the closing action, not a new round.**

## THE OUTPUT

`_Working/2026-09-09_CONSOLIDATION_REPORT.md`: what you applied, what you refused and why, the before
and after estate table with both sums, the `.docx` verification, and **the honest headline number**.

**Say where you disagree with Tuesday, and say what you did not verify.** If the five verdicts are
individually sound and collectively incoherent, that is the most valuable thing you can report and it
is exactly what a fresh reader is for.
