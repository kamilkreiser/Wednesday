# B1782 drafter commission -- NexusAI records pass for PR 236 (RD-1011, RD-1012, RD-1013: the data-source role checks and the audit pathname rule) (SEAT-R285)
Commissioned by Tuesday (s298), 2026-11-20. Drafter model: Sonnet (routing row C8). You DRAFT a kit; you write no Jira and no record.

Draft ONE records kit `2_Project_Files/tuesday/briefs/2026-11-20_B1782_SEAT-R285_nexusai-records-236.md` (+ `.measured`; ALSO save
your drafter report as `2026-11-20_B1782_DRAFTER-REPORT.md` beside it and return its head as TEXT) in the FORM of today's stamped
NexusAI records kit `2026-11-20_B1759_SEAT-R282_nexusai-records-233-234.md` (read it whole, as STAMPED) with the lessons of its
STATUS folded in by name: `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-20_B1759_STATUS.md` (Deviations and
Corrections first). The commission that produced that kit, `2026-11-20_B1759_DRAFTER_COMMISSION.md`, shows the shape (the evidence
wait, ONE C-entry per pull request, ONE history pull request on a `records/` branch touching HISTORY.md only). Follow
`2_Project_Files/tuesday/DRAFTER_RULES.md` whole. All paths are under /Volumes/Datasec_DEV/TUESDAY or
/Volumes/Datasec_DEV/!CODING/Datasec. Every path named in this commission was listed by Tuesday (`ls -d`) at 16:19:00 AEDT.

Facts to re-measure at source (repo datasecau/Reporting_Dashboard_Au, NexusAI GH_CONFIG_DIR, GET only; Tuesday's reads are dated
2026-11-20 16:16 to 16:19 AEDT and are pointers, not facts):
- PR 236 merged 2026-11-20T05:16:46Z as a MERGE commit 98e6a4d72f5745a17438bdd2788cff5872f6fcaf, parents
  b169b8a0eee8eaac594e98918c2ccaff91164dcf and 8af88ee80b47a5f57c8f176690111047a8678e4e (the reviewed head), tree
  f5f7094e9981516890032a9e74785f7b3f4b3366 (equal to the head's tree); before the merge the checks table named 7 jobs, each
  completed success (Analyze (actions), Analyze (javascript-typescript), Analyze (python), CodeQL, audit-production-deps, build,
  scan); Deploy demo run 44679971602 on the merge: build skipped, deploy skipped (NOT deployed).
  UNMEASURED by Tuesday and owed by this kit: the runs on the merge commit on main (Build, audit, scan, CodeQL push), that CodeQL
  on main shows no new alert, and the hosted CodeQL check run's title on the pull request (alerts 67 and 68 were the watch item of
  the landing file): the kit WAITS for and reads them (the evidence wait of the form).
- The builder kit and STATUS: `tuesday/briefs/2026-11-20_B1762_SEAT-N160_nexusai-lane-nk-datasource-role-checks.md` (as stamped)
  and `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-20_B1762_STATUS.md` (READY, Deviations, Corrections).
- The independent review `tuesday/briefs/2026-11-20_B1776_verify/` (VERDICT.md first line "GATE B1776: GO WITH FINDINGS @ 8af88ee
  on main b169b8a", Blocker 0, Major 0, Minor 4, Info 7; read VERDICT.md and FOR-RECORDS.md WHOLE, with pr-body.md, merge-body.txt
  and landing.txt). Tuesday read FOR-RECORDS.md, landing.txt and merge-body.txt whole, and only the head of the verdict. Every
  sentence in a frozen Jira or records text that says what the review found is matched against the VERDICT row it rests on.

What the kit records (each decision below is Tuesday's as coordinator, never the product owner's; write it that way):
1. RD-1011, RD-1012, RD-1013: ONE comment each with the sentence FOR-RECORDS gives for it (checked against the verdict), and the
   transition FOR-RECORDS names (Testing), by the board's own transition id read at the seat's run, never predicted.
2. RD-1011's open question STAYS OPEN on the ticket: must the two read routes (describe-table, discover-tables) stay open to a
   viewer? The landed behaviour (refused) is the coordinator's default. The comment carries the reversal as FOR-RECORDS words it,
   and that the permission table still gives both reads `config.read`. A card to the product owner is Tuesday's to post, not the
   seat's: a Stamp slot carries its state; the kit quotes no approval.
3. New tickets on RD (search each first by route, symbol and phrase, with a control; a true duplicate is commented, not created):
   (a) the two sibling routes MEASURED by the review, `GET /api/setup/data-sources` and `GET /api/debug/data-sources` (a signed-in
   viewer makes the server use stored sign-in details): ONE security ticket with both, the review's measured figures quoted, marked
   as the next NexusAI security lane; (b) the five routes the review did NOT measure with a primary workspace configured: a
   REVIEW ticket worded as a question, not a defect claim; (c) the two audit sinks in `backend/services/scimProvisioning.js` that
   still record the router-relative path; (d) the follow-up cells (a count of the stored-source read for a refused caller; a
   non-viewer non-administrator role value) and the stale comment above `pathnameOf`: one ticket or lines in (a), your call, said
   plainly; (e) the design note on the setup window (after an administrator resets first run, every signed-in viewer passes every
   administrator check until first run is completed again): a ticket worded with the review's own measurement, marked as needing
   the product owner's word before any build. The four stale remote heads are a records sentence, not a ticket.
4. ONE C-entry for 236 (next free number and section, by program) and ONE history pull request (branch `records/b1782-history`,
   HISTORY.md only), as B1759 did.
5. A section FOR TUESDAY in the STATUS: the facts a card to the product owner on RD-1011's question needs, each with the file and
   line that proves it (what a viewer could do before, what is refused now, what reversing costs, the two sibling routes).
Who decided: refusing all four routes (the two reads included), recording percent-encoded text as sent with no dot segment
resolved, keeping `config.read` for the two reads in the permission table, the RD-793 key leaving the pending list and the four
rewritten old-answer tests are the coordinator's defaults: NONE is the product owner's. Record that Tuesday landed the pull request
as her own decision on the review's GO.
Slots for Tuesday's stamp: JIRA WRITE or DRY; which creates run; RECORDS WRITE; the card's state; base facts; hard stop.
Every count by program; every prose list recounted; selectors checked against the names they must match; no predicted number.

HOW: read-only everywhere while drafting except your three files and scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s298/d1782/`. Jira GET only (credentials by name, in-process, from the
NexusAI project's `4_Credentials/.env`, never printed). Git read verbs only in the project. NO jest, no server (another seat may
hold the jest lock later). Nothing of any other project; NO HPSM-POC anything. No `cd` (a hook refuses it); zsh; absolute
single-quoted paths; no unquoted word starting with `=`. Clocks from `date` in the same command. Never delete. Write the kit to
disk as you go; temp file then os.replace; ASCII; `stamp_check.py` exits 0 with the slots unfilled.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, recommended slots, the searches for each create, corrections to
this commission, D/Q defaults, UNMEASURED.
