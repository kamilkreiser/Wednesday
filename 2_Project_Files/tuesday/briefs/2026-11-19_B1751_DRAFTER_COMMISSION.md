# B1751 drafter commission — NexusAI records pass for PR 232 and PR 233 (RD-835 + RD-861) (SEAT-R280)
Commissioned by Tuesday (s293), 2026-11-19. Drafter model: Sonnet (routing row C8).
Draft ONE records kit `2_Project_Files/tuesday/briefs/2026-11-19_B1751_SEAT-R280_nexusai-records-233.md` (+ `.measured`;
return the drafter report as TEXT, Tuesday saves it) in the FORM of `2026-11-19_B1738_SEAT-R279_nexusai-records-231.md`
(read it whole, as STAMPED, and its STATUS `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-19_B1738_STATUS.md`,
Deviations and Corrections first: fold each in by name; its Corrections 1 and 2 were kit errors of Tuesday's stamp: a
predicted line shift and a key count: compute, never estimate). Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole,
its 2026-11-19 section included.

Facts to re-measure at source (Tuesday read them at each landing):
- PR 232 (records: history of 230 and 231) merged as merge commit 64b9840f254c9510cbbf7f2da4306438e5e85852 (parents
  9373976e + 6c3c28d5; HISTORY.md only; no Deploy demo run).
- PR 233 (RD-835 + RD-861) merged 2026-11-19T07:47:09Z as merge commit b0499db08dafc08313e855faf7c2ce4f7f9f0bcc (parents
  64b9840f + ca11062972e3cab9d713b1d1fdcb6cfd874db854, the reviewed head); 7 of 7 check names green on the head; the
  CodeQL check run title 'No new alerts in code changed by this pull request'; 0 open alerts on the PR merge ref;
  Deploy demo run 44482289102 completed/skipped with both jobs skipped (not deployed); the Build, npm-audit, Gitleaks
  and Push on main runs of the merge were IN PROGRESS at landing: the kit WAITS for them (the evidence wait of the form).
- Six paths: static/js/index.js (blob 676a78625c63), settings.js (f82ca22d8b27), first-run-setup.js (6e1992d07958), two
  new test files (22 and 20 cells by the review), the counts file (6086/384 -> 6128/386).
- The independent review: `2_Project_Files/tuesday/briefs/2026-11-19_B1745_verify/VERDICT.md` (GO WITH FINDINGS, no
  Blocker, no Major; read it WHOLE; its `still-open-census.tsv` lists the remaining unescaped write sites) with
  pr-body.md and merge-body.txt; the builder STATUS `.../Briefs/2026-11-19_B1737_STATUS.md` (398 lines; READY, Corrections).

Scope: RD-835 and RD-861: ONE comment each + move to Testing (the project rule: a code change goes to Testing; quote it
from the project CLAUDE.md as the form does); each comment says exactly what its ticket's acceptance asked and what the
review measured, and what is NOT claimed. ONE C-entry (next free, C-307 and section 105 expected: by program). History PR
branch `records/b1751-history` (HISTORY.md only). Follow-up tickets, EACH SEARCHED FIRST (state the searches and their
controls; a found ticket on the same subject = no create, name it):
 (a) ONE ticket for the remaining unescaped HTML write sites a value from outside can reach (the review's finding 2:
     scan file names, print-log user names, printer-host data-arg values; the census file is the list; the chat region
     belongs to RD-1008 and is named, not included). Type, priority and labels by the review's severity and the sibling
     tickets' practice (propose; Tuesday's default at the stamp).
 (b) ONE ticket for the CSV residue: numeric columns still written raw inside the ten writers (sheets, pages, size, cost),
     a leading space or new line before an equals sign and Unicode look-alikes not neutralised, a negative amount with a
     currency sign now shown as text (findings 3, 4, 5); say plainly which parts are measured and which were not
     reproduced in a spreadsheet.
 (c) ONE ticket: `static/js/settings.js` defines `escapeHtml` twice (lines 93 and 2440 at the builder's read); the page
     uses the second, which passes an array or object through unescaped (finding 1; no attacker path found today).
 (d) ONE ticket from Tuesday's read-only audit census (`2026-11-19_B1740_RD-1006_audit-write-census.md`, same folder):
     `AUDIT_ACTIONS.SETTINGS_CHANGE` is used at backend/server.js 17353 and 17600 and defined nowhere, so those audit
     rows carry an undefined action (Tuesday verified: the name is on exactly 2 lines of server.js at 9373976e, both
     uses; RE-MEASURE at b0499db0; RD-1006 names it but says it does not scope it: read RD-1006 and say so).
 If two of these are one fix in one place, propose folding them and say why; otherwise four creates at most.
Also to record in the entry (no ticket): the builder's Corrections of the kit Tuesday stamped (the P2/P3 plant table
was wrong in the kit; the gross-against-net non-ASCII count); RD-300 and RD-564 read Declined while Jira counts them
open (a note for the product owner's housekeeping, from SWEEP-1630).
Who decided: no product-owner ruling is cited; every choice of the change is the change's default and every decision of
this pass (land as reviewed, ticket the residue, priorities) is the coordinator's, written as such.
Read-only everywhere; NexusAI GH_CONFIG_DIR verified kamilDatasec; Jira GET only, credentials in-process by name. NO
jest, no server (nothing holds the lock now, but a build lane will be launched beside the records seat: the records kit
shares no code path with it; say so in its launch window and partition). Nothing of any other project. Scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1751/`. No `cd`; no unquoted word starting with `=`; zsh;
absolute paths; never delete; clocks from `date`. stamp_check exits 0; slots unfilled; ASCII; temp file then os.replace.
First line of your reply: STARTABLE: YES|NO - why. Then: files, recommended slots, the searches for each create, corrections
to this commission, D/Q defaults, UNMEASURED.
