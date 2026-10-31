STARTABLE: YES after the stamp (a records seat; Sonnet; no builder, no deploy, no new ticket; 6 lines carry the four-underscore pattern until Tuesday fills them)

BLUF: Eleven Composer tickets have merged work and sit in Backlog: PCOMP-14, -17 (PR #89), -22 (#96), -62, -63 (#90), -95 (#92), -96 (#93), -97 (#94) and, from the B975 finding, PCOMP-40, -41, -43 (PR #87, migrations 0025, 0024, 0023; their text still says NOT started and names 0022_*). Nothing is deployed. The project's Done rule does not make Done wait for a deploy ("Done here means merged to main, not deployed"), so the kit defaults MOVE where the seat's own Done-when table reads MET and COMMENT-ONLY (HELD) for PCOMP-62 and -97, where the landing comment itself says the ticket's regression or per-item closure was not proved. The sweep's "12 done-pending-record" is 8 of these plus PCOMP-5, -7, -64, -65, which have no merged PR (stale or information); they are left out and put as Q-3.

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B976_SEAT-R95_composer-records-merged-not-closed.md (unstamped, 87 lines, 0 non-ASCII by program). Seat R95 (0 briefs name it; R89 control 5; R94 is a live HPSM pane). Template shape copied from the B921 kit (REFUSE, Stamp, helpers copied from .tools/b921, 22-write fence, records branch records/b976 folded by merge --no-ff, launch via launch_when_cool).

Per-ticket table (MEASURED 2026-10-31 12:0x AEDT; Jira GET + gh api -X GET; deployed is RELAYED from the sweep and C-102, hosted not probed):
| key | PR / squash | gate line | deployed | Done-when met | default |
|---|---|---|---|---|---|
| PCOMP-14 | #89 d64efb8f | B648 :1109 GO WITH FINDINGS | n | y (migration 0027 index) | MOVE |
| PCOMP-17 | #89 d64efb8f | B648 :1109 | n | y (migration 0026 CHECK) | MOVE |
| PCOMP-22 | #96 422ecf37 | B787 :301 NO GO round 2 of 2, landed on the owner's ruling C-105 | n | y on fix-shape; optional ledger comparison not built; residue PCOMP-99..102 | MOVE (Q-2) |
| PCOMP-40 | #87 e019ac3a | B593 :649 GO WITH FINDINGS round 1 of 2 | n | probable y (0025 + contract); seat must confirm the 422 refusal is gone in apps/api | MOVE (Q-1) |
| PCOMP-41 | #87 | B593 :649 | n | probable y (0024) | MOVE (Q-1) |
| PCOMP-43 | #87 | B593 :649 | n | probable y (0023) | MOVE (Q-1) |
| PCOMP-62 | #90 667830ed | B659 :358 GO WITH FOLLOW-UPS round 2 of 2 | n | partial: fix built, its own regression not run | COMMENT-ONLY |
| PCOMP-63 | #90 | B659 :358 | n | y (comment-only fix; one Note open) | MOVE |
| PCOMP-95 | #92 8347f91b | B682 :518 NO GO round 2 of 2, landed on ruling C-106 | n | y per the gate's cells; 13 survivors ticketed (row #388) | MOVE |
| PCOMP-96 | #93 0b52848c | B698 :114 GO WITH FOLLOW-UPS round 1 of 2 | n | y (6 of 6 lines) | MOVE |
| PCOMP-97 | #94 4a2911f1 | B755 :97 GO WITH FOLLOW-UPS (short check) | n | not backed: the five were not re-closed one by one | COMMENT-ONLY |
All seven PRs: merged true; both Analyze runs success on each squash; Composer main d70edf70; pulls/9999 404.

The Done rule, with its line: CLARIFICATIONS.md:2029 (C-111 (3)): "The project still records no standing rule for when a merged, not deployed ticket moves (C-105 (3)); these moves rest on the coordinator's instruction and on those checks. Done here means merged to main, not deployed." The earlier batches (C-100, B818, B842, B852, B872, B882, B902, B921) all commented, then moved with transition 41 once the Done-when was met per the gate. CLAUDE.md:30 keeps the deploy on the product owner's card. The kit therefore needs three things for a move: slot MOVE, the seat's table MET, no gate line contradicting. Searched with /usr/bin/grep -i over CLAUDE.md, JIRA.md and CLARIFICATIONS.md; CLAUDE.md and JIRA.md hold no Done rule, CLARIFICATIONS.md holds the line above (positive control: the C-111 line prints).

Q-questions:
- Q-1: Move PCOMP-40, -41, -43 to Done? They have no Done-when clause and no landing comment; the merge was on a words-ruled PR (C-102). Default: MOVE only if the seat reads the 422 refusal gone and the table MET, else COMMENT-ONLY. Safer alternative: set all three to COMMENT-ONLY.
- Q-2: Move PCOMP-22 and PCOMP-95, whose last gates were NO GO (round cap) and which landed on the product owner's rulings? Default: MOVE, since the fix-shape and Done-when are met and the residue is ticketed; set COMMENT-ONLY if you read a NO GO as not closable.
- Q-3: PCOMP-5, -7, -64, -65 (stale/superseded/info)? Default: leave out of this brief; they need a stale-close ruling, not a merge record.
- Q-4: Adopt the sweep's suggestion to write a standing rule (Done = merged, not deployed) into the project's records? Default: NO in this brief; the kit's C-112 only applies and counts the rule (the ninth batch if the chain holds).

Stamp values: seat Datasec/Security-Composer-R95; model claude-sonnet-5-5 (models_latest.json line 23) with BRIEF_SEAT_LEVEL=sonnet; ports none; main heads at launch: Composer code d70edf70fc43bb69737b2a242ba56480ce79f0d8, root records ce82875c899819c5486d00b6507077759badbf4b (B921's fold; BACKLOG highest #417, C-111 highest); load1 2.21 at 12:0x (below 7); live panes: tuesday, fleet-monitor, HPSM-POC-R94, HPSM-POC-H79, no Composer pane, 0 Composer processes. Slots to set: DONE-14, -17, -22, -40, -41, -43, -62, -63, -95, -96, -97 and C-ENTRY (defaults above, FILE). Launch: WED_USAGE_STOP=100 bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh' Datasec/Security-Composer-R95 "WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer' '<stamped kit path>'" (as in the B921 kit; no cockpit.sh add inside the string).

Not measured: hosted demo state, gate findings beyond the VERDICT lines and landing comments, the overrides round trip in #87, PCOMP-5/-7/-64/-65 beyond summaries. No SOW, Source_Documents or inbound opened; nothing written to any project, Jira or git.
