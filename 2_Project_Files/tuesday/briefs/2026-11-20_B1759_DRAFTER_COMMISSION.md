# B1759 drafter commission -- NexusAI records pass RE-CUT: PR 232, PR 233 and PR 234 (SEAT-R282)
Commissioned by Tuesday (s295), 2026-11-20. Drafter model: Sonnet (routing row C8).
The kit `2026-11-19_B1751_SEAT-R280_nexusai-records-233.md` was drafted on 19 November against NexusAI main b0499db0 and was
never read by Tuesday, never stamped, never launched. Since then PR 234 landed. RE-CUT it as ONE new kit
`2_Project_Files/tuesday/briefs/2026-11-20_B1759_SEAT-R282_nexusai-records-233-234.md` (+ `.measured`; drafter report as
TEXT). Read WHOLE first: the B1751 commission `2026-11-19_B1751_DRAFTER_COMMISSION.md` (it still binds: every scope item,
the four follow-up creates (a) to (d), the who-decided rule), the B1751 kit and `2026-11-19_B1751_DRAFTER-REPORT.md` (its
corrections: the merge tree of 233 does not equal the head tree; RD-861's description has 2 alert lines), the form
`2026-11-19_B1738_SEAT-R279_nexusai-records-231.md` as STAMPED with its STATUS, and `2_Project_Files/tuesday/DRAFTER_RULES.md`
whole. Keep what B1751 measured only after RE-MEASURING it at today's main; do not copy a number unread.

NEW since B1751 (re-measure each at source; repo datasecau/Reporting_Dashboard_Au, NexusAI GH_CONFIG_DIR, GET only):
- PR 234 (RD-445 item 2: the Marketplace webhook token check refuses the skip flag in production) merged
  2026-11-19T21:35:39Z as MERGE commit c05522407a81bf8575c9f713b49072b16effe650, parents b0499db08dafc08313e855faf7c2ce4f7f9f0bcc
  and 18c490c653fee13346d98779ba63222a77c83f00 (the reviewed head), tree b94d4fdac9a6892622832fa1ef233478206d51f6; before
  the merge gh pr checks listed 7 distinct job names all pass; the CodeQL check run title read 'No new alerts in code
  changed by this pull request'; Deploy demo run 44620339933 on the merge: build skipped, deploy skipped (NOT deployed).
  UNMEASURED by Tuesday and owed by this kit: the runs on the merge commit on main (Build, audit, scan, CodeQL push) and
  that CodeQL on main shows no new alert: the kit WAITS for and reads them (the evidence wait of the form).
- The independent review `2026-11-19_B1756_verify/VERDICT.md` (GO WITH FINDINGS, 0 Blocker, 0 Major, Minor M-1 to M-4, Info
  I-1 to I-3; read WHOLE) with pr-body.md, merge-body.txt, landing.txt; the builder STATUS
  `!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-19_B1739_STATUS.md` (READY, Corrections).
- Records for 234: RD-445 gets ONE comment for item 2 and STAYS OPEN for items 1, 3 and 4 (quote the ticket's own items);
  follow-up tickets, each SEARCHED FIRST: M-1 a cell that loads the real token library against a loopback key set (the
  mocked cells cannot see a weakened verification); I-3 whether the global sign-in gate lets Microsoft's webhook through
  on an auth-enforced instance (unmeasured at run time: a question ticket, not a defect claim); I-1 a boot-time refusal
  when the flag is on outside production is 'left for others' (ticket only if none holds it). M-2 and M-3 go in the entry.
- Who decided, for 234: the branch carries the coordinator's defaults (refuse in production and keep the flag; the
  case-insensitive trimmed NODE_ENV test; the log lines and their wording; mocked token library; RD-445 left open): NONE is
  the product owner's; write each as the coordinator's default. The landing file's LANDING HOLD says so: record that
  Tuesday landed it as her own decision and told the product owner on the morning card of 2026-11-20.
ONE C-entry for 233 and ONE for 234 (next free numbers and section, by program), ONE history PR (branch
`records/b1759-history`, HISTORY.md only) covering 232, 233 and 234.
Read-only everywhere while drafting; Jira GET only, credentials in-process by name; NO jest, no server; nothing of any
other project; NO HPSM-POC anything. Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s295/d1759/`. No
`cd`; no unquoted word starting with `=`; zsh; absolute quoted paths; never delete; clocks from `date`. stamp_check exits 0;
slots unfilled; ASCII; temp file then os.replace.
First line of your reply: STARTABLE: YES|NO - why. Then: files, recommended slots, the searches for each create,
corrections to this commission, D/Q defaults, UNMEASURED.
