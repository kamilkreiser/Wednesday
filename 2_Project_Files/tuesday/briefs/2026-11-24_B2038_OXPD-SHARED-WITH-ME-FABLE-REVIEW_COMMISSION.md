# B2038 COMMISSION (Fable reviewer, in-session, READ-ONLY) - OXPd 2: review lane D's (B2037) removal of OneDrive "Shared with me" from 02 and 03

Written by Tuesday (s322). Fable under Kam's word of 2026-11-24 ~08:12 (Tuesday terminal, verbatim: "Use fable to review once you are ready."), recorded in EXPIRING-GRANTS as OXPd document reviews through tonight's kick-off meeting. RE-COMMISSION if `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2038_review/REVIEW.md` is absent.

Read whole: the lane's commission `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2037_OXPD-DROP-SHARED-WITH-ME-02-03_COMMISSION.md` (the ruling, the sources, the job). Then review, in `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Design/`, the changes of `02_architecture.md` and `03_plan-of-attack-and-build.md` against their `.pre-1124b.md` before-copies (`diff` them: 02 old lines 3, 98, 212, 216, 226, 231, 371, 543, 743, 1259, 1279 plus an appended change-log entry; 03 old lines 3, 105, 229, 268, 312, 539, 544 plus an appended entry). The lane's own checks: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/D/` (apply_b2037.py, verify_b2037.py, verify_installed.txt).

Find, each with doc:line and severity (Blocker / Major / Minor / Info):
1. Any place that still has the rebuild BUILD, test, estimate or accept Shared with me (search both documents for every spelling: "shared with me", SharedWithMe, Shared-with-me, sharedWithMe, the Graph call names for it if the documents name them).
2. Any sentence that overstates the ruling (calls C-82 a ruling on C-16, or says something Kam did not rule) or understates it.
3. Any sentence that is now inconsistent with another part of the same document or the other document (counts of "four places", work-package scope, estimates, acceptance lists, OP-20/N-10/W30 state).
4. Any quote of HP's sources that does not match `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-24_hpauthsuite-help/MAP.md` lines 66-68 or `docs/DOCS-MAP.md` line 13 byte for byte.
5. Whether the .docx and .pdf carry the same text as the .md for the changed lines (extract text by program: python-docx or unzip of word/document.xml; pdftotext), sampled on at least three changed lines per document.
Every "absent" with a positive control. READ-ONLY: write only `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2038_review/` (REVIEW.md, first line `REVIEW B2038: <GO | GO WITH FINDINGS | NO GO>`). No `cd`; `python3 -I`; no write in the OXPd project, Jira, GitHub or mail; nothing to any person; HPSM-POC not opened.
Reply in at most 10 lines: verdict, Blockers and Majors first with doc:line, then counts.
