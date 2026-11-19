# B1738 drafter commission — NexusAI records pass for PR 231 (RD-793 + RD-990) (SEAT-R279)
Draft ONE records kit `2_Project_Files/tuesday/briefs/2026-11-19_B1738_SEAT-R279_nexusai-records-231.md` (+ `.measured`;
return the drafter report as TEXT, Tuesday saves it) in the FORM of `2026-11-19_B1730_SEAT-R277_nexusai-records-229.md`
(read it whole and its STATUS `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-19_B1730_STATUS.md`, Deviations first).
Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole.
Facts to re-measure at source (Tuesday read them at landing, 15:30): PR 231 merged as merge commit 9373976efc7d93f522f97648beb608b4d3e16fb2
(parents 295f989e + f06b080e; tree 7d4516cf = head's); 7 of 7 checks green; CodeQL check 'No new alerts in code changed by
this pull request'; Deploy demo run 44458821234 skipped (not deployed); Build of the merge was in progress at landing (the kit
waits for it). Gate verdict `2_Project_Files/tuesday/briefs/2026-11-19_B1736_verify/VERDICT.md` (GO WITH FINDINGS F1-F5);
builder STATUS `.../Briefs/2026-11-19_B1733_STATUS.md`. Also record PR 230 (history of 228/229, merge 295f989e).
Scope: RD-793 and RD-990: ONE comment each + move to Testing (project rule: code change -> Testing); C-entry (next free,
expected C-306, section 104); follow-up tickets, each searched first (state the searches): (a) ONE Medium security ticket for
the four viewer-reachable routes that make the server dial with the stored credential (POST /api/data-sources/:id/test,
POST /api/setup/data-sources/:id/test, GET /api/data-sources/:id/discover-tables, GET /api/data-sources/:id/describe-table;
gate F2, measured by the gate); (b) ONE Minor ticket: requestPath records an absolute-form target's scheme and host and the
text after a raw '#' (gate F1, introduced by RD-990; fix: record only the pathname); (c) the Entra router's own audit row
(routes/entraProvisioning.js:167, relative path) — fold into (b) if the same fix shape, else its own Low; (d) the stale
header comment rd988 test :25 ('30', now 34) — a note in the entry, no ticket unless the source gives a reason. History PR
(records/b1738-history). Who decided: no product-owner ruling; RD-793's split from RD-761 was Tuesday's 2026-10-05 decision
(the ticket's own words); the land-now-and-ticket-F1 call is Tuesday's; write every choice as the coordinator's.
Read-only everywhere; NexusAI GH_CONFIG_DIR verified kamilDatasec; Jira GET only, credentials in-process by name. Scratch
`2_Project_Files/fleet/state/s292/d1738/`. No cd; zsh. First line of your reply: STARTABLE: YES|NO - why.
