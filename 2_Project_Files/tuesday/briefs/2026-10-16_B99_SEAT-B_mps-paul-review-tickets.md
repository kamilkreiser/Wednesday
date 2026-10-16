From Tuesday (Kam's Datasec coordinator seat; Friday handed this project to Tuesday on 2026-10-15). Datasec / MPS Commercial Calculator. Questions to tuesday-agent@agentmail.to; your STATUS file is the wrap.
# BRIEF B99 · SEAT-B (records): turn today's MPS Calculator review with Paul into Jira tickets, plus every open feedback item, and propose the build lanes

**BLUF.** Kam held a review of the calculator with Paul Waite today and sent five files. Read them, extract EVERYTHING mentioned in the meeting (actions, defects, asks, "it should…", numbers that disagree), check each against what already exists, and file the tickets on MPSCALC. Then sweep EVERY feedback item this project holds and ticket the open ones the same way. Finally propose lanes (file-disjoint) for build seats. Report `1_Project_Definition/Briefs/2026-10-16_B99_STATUS.md`. Last line exactly `DONE: B99 <n> tickets filed, lanes proposed` or `STOPPED: NEEDS TUESDAY` + ONE question.
**Step 0:** copy this file unchanged into your `1_Project_Definition/Briefs/` (sha256 both equal; this copy is in Tuesday's tree, read-only to you).

## Kam's words, verbatim (Tuesday's terminal, 2026-10-16 ~12:0x AEDT)
> *"please find attached notes from todays MPS calculator review with Paul.  The MPS Calculator Walkthrough.docx has a transcript and all actions from the meeting.  The files and documents discussed in the meeting are also attached.  Some will be repeats but check.  Please create tickets from everything mentioned in the meeting then get agents to action these as well as all feedback items in this project"*

## The five files (Kam's Downloads folder; read-only there; byte sizes read by Tuesday 12:0x)
- `/Users/kamil/Downloads/MPS Calculator Walkthrough.docx` (2,692,665 B): the transcript + actions. **The primary source.**
- `/Users/kamil/Downloads/Fleet_BOM_Final_PG_26.10.08 1.xlsx` (35,598 B)
- `/Users/kamil/Downloads/Synnex - HP Managed Print Price Book - CSG - Q4 26 v1a 2.xlsx` (5,727,458 B)
- `/Users/kamil/Downloads/Woods_Bagot_MPS_Concise_Proposal_Standard_Pricing_Oct_2026 1.docx` (590,476 B)
- `/Users/kamil/Downloads/Woods_Bagot_Integrated_Managed_Print_Proposal_Standard_Pricing_Oct_2026 2.docx` (604,854 B)

## DO
1. Copy all five, byte for byte, into `1_Project_Definition/Source_Documents/2026-10-16_paul-review/` (sha256 each, source = copy). "Some will be repeats": for each, find whether an earlier version already sits in `Source_Documents/` (by name family and by content); record new vs repeat vs NEWER VERSION OF, and for a newer version list what changed (sheets/rows/prices/sections). A newer price book or BOM is itself a ticket if the calculator's data must follow it.
2. Read the transcript WHOLE (parse the docx properly; it may hold images; describe any screenshots that carry an action). Build `1_Project_Definition/Registers/2026-10-16_paul-review-items.md`: one row per item: id (PR-nn) · who said it · verbatim quote · what it asks · type (defect / change / new feature / data / words / question for Kam) · the screen or workbook cell it concerns · already ticketed? (search MPSCALC by symbol/screen/words, say what you searched) · disposition.
3. Feedback sweep: find EVERY place this project's feedback lives (the hosted app's feedback store, BACKLOG.md, CLARIFICATIONS open items, earlier review registers, Paul's emails recorded in the project) and list each open item in the same register with source and status.
4. File the tickets on MPSCALC (board 608) for every item that is not already ticketed or done: **one ticket when one test pass proves it; split only for separate workloads or separate fixes**. Every ticket: BLUF description, the verbatim source line(s), acceptance check, and the register id. Assign to the project's board account (ours). Items that are Kam's to decide (pricing policy, customer-facing WORDS, anything needing Paul's or HP's input) are filed AND listed in STATUS under "FOR KAM" as one-line card candidates with a recommendation and default. **Pricing rules stay workbook-driven: any number change needs a workbook-register row and a red-first test, so say which tickets touch the calculation register.**
5. Propose LANES: group the build tickets by the files/areas they touch so seats never share files (web proposal templates · pricing engine/API · data import/price book · UI flows · docs). For each lane: tickets in order, the files it owns, tier (1 = pricing/security/data; 2 = words/UI tweak), and whether it can go to a local model per the Spark predicate (one file, fix spelled out, test nearby). Tuesday launches the lanes.
6. history.md entry + a records commit in the project-root records repo (LOCAL ONLY, no remote: never push it).

## HOLDS
- Nothing to Paul, HP, Woods Bagot or any human: Kam sends. Customer names in these documents (Woods Bagot) stay inside this project: never in a commit message on GitHub, never in a public artefact.
- No code changes in this brief (B98 owns the code repo). Never delete (quarantine). Secrets stay in 4_Credentials/.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 12:0x
