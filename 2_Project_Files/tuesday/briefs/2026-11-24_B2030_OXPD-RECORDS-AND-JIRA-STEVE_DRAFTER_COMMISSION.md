# B2030 DRAFTER COMMISSION (Opus, in-session, READ-ONLY) -- Datasec / OXPd_2: a records + Jira WRITE kit for seat R310: the product owner's answers and taps of 2026-11-24 into CLARIFICATIONS, the landing of PR 45, and 29 Jira tickets for Steve M

Commissioned by Tuesday (s320) after the command whose `date` printed 2026-11-24 10:38:29 +1100. Model OPUS (OXPd `CLAUDE.md` line 7). Return a 10-line summary with `STARTABLE: YES` or `NO` as line 1.

## FORM AND FENCES
The records kit B2022 is the model and was stamped and ran clean today: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2022_SEAT-R309_oxpd2-r-records-wave4.md` (read whole) with its drafter report, and the form commission `2026-11-23_B2010-B2012_OXPD-WAVE4-RECORDS-W2-CONTRACTS_DRAFTER_COMMISSION.md` and `tuesday/DRAFTER_RULES.md`. Every fence there applies. **NEW in this kit: Jira WRITES to project OXPD2** (create issues, set assignee, due date, label, one 'relates to' link each to OXPD2-1). Find how earlier OXPd seats wrote Jira (the project's `.tools/b1785/` helper and any earlier kit that created OXPD2 issues: grep the Briefs folder) and use that path; the kit writes nothing else to Jira. Every create is idempotent by a search for its own summary first; a hit is a skip, never a duplicate.

## AUTHORITY (verbatim; the product owner's)
- His answers file, live board 2026-11-24 09:55:19 "please review": `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-24_kam-oxpd-answers/answers.txt` (and .rtf). The ticket instruction in it, verbatim: "create a Jira ticket (with the question) and assign to Steve M - 2 week time request"; and w8: "If its a technical doc (swim lane diagrams) create a Jira ticket and assign to Steve M but for him to assign to Artur M".
- His taps on the board today (read each with `kam_msgs.sh` / `decision_queue.sh show <id>` and quote from the tool output, never from here): kd3 10:19, kd2 10:26 (with note), kd1 10:32 (with note), ka4 10:33 (with note), ka2 10:34, ka3, ka5 (b: "Steve M's: ticket them"), ka1 10:35 (with note); and his board line 10:37 "for the the meeting pack don't include questions that have already been assigned, answered or actioned"; and 08:33 / 08:34.
- **C-entries:** C-80 = the answers file whole, verbatim (copied by program, never retyped); C-81 = his board words and taps of 2026-11-24 after C-79, verbatim, each with its time; Tuesday's readings marked as Tuesday's.

## SOURCES FOR THE TICKETS
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2027_answers/JIRA-DRAFTS.md` (29 drafts T-01..T-29, Fable-reviewed in B2028 and fixed): freeze each as a TEXT with its sha256; assignee Steven Molnar (accountId read by the drafter: re-measure by a Jira GET; never guess), due 2026-12-08, label `oxpd-workpath-question`, 'relates to' OXPD2-1. T-26 (w8 swim lanes) is assigned to Steve M with the description saying it is for him to pass to Artur M.

## RECORDS (as B2022's form)
- history.md: the landing of PR 45 (main e2a20aefda7d4356af2b264576a7e3faaf0bce2c, gate B2026 GO WITH FINDINGS at 28b2533, its verdict `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2026_verify/`), the coordinator's lift of its hold (the 10:04 entry of Tuesday's note: lifted as worded, three first-run preconditions: read and show GetAuthenticationAgentRecords before any executed register; a fresh session folder per run; ASCII hosts for --agent-service/--prompt-page), the design-document updates of today (02, 03 rounds 1-4, the meeting pack), and the Jira tickets created (keys by program).
- BACKLOG.md: tick owed items 98 and 99 (FOUND 1 and 2, landed by PR 45), 100 and 101 (FOUND 3 and 4, landed) and 102 (the hold, lifted) each in place by the B2022 tick form, IF the gate's verdict shows each closed (read it); file gate B2026's three Minors (new FOUND 1-3) and three Infos as new owed items; file the three first-run preconditions as one owed item for the first-run commission.
- CLARIFICATIONS.md: C-80, C-81 appended.

## Out of scope
The printer; Azure; any message to a person (the Jira tickets are the one sanctioned channel, by his words); HP; Design/ and Meeting/ files; HPSM-POC (hold).
Write only the kit, its sidecar and the report under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/` and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s320/b2030/`. No daily-note folder of any seat is read.
