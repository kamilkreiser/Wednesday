# B2037 COMMISSION (Opus author, in-session agent; a Fable review after) - OXPd 2: drop OneDrive "Shared with me" from 02_architecture and 03_plan-of-attack, per the product owner's ruling

Written by Tuesday (s322). Tracked so a successor can RE-COMMISSION if the output files are absent. One agent, model **opus** (the 2026-11-21 standing rule; Fable is for the REVIEW only, under Kam's 2026-11-24 ~08:12 word "Use fable to review once you are ready"). Prompt: "read this commission whole; you are lane D".
Form: the B2019/B2020 lanes of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2018-B2020_OXPD-MEETING-PACK-AND-DESIGN-UPDATE_COMMISSION.md` (read its LANE A / LANE P and "For every agent" sections whole: they bind here too).

## THE RULING (the authority; decision store print read by Tuesday 2026-11-24 after 12:36)
Card "OneDrive 'Shared with me' is in our rebuild but HP removed it from the shipped 4.4 app; drop it?" (Datasec/OXPd), ruled **a "Drop it"** at 2026-11-24 11:31:08, option detail verbatim: **"Match the shipped 4.4 app; the design notes the removal and its source."** Recorded in the project as C-82 (`<P>/1_Project_Definition/CLARIFICATIONS.md`, heading `## C-82` at line 980) and owed item 113 of `<P>/BACKLOG.md` (lines 816-822; read whole). The card's BLUF also says Kam's full-match ruling C-16 was read as matching the product in the market and did not decide this feature: keep that reading, never write it as his ruling on C-16.
`<P>` = `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2`.

## THE SOURCES OF THE REMOVAL (cite these in the documents; read them, do not paraphrase from here)
- The 4.4 release notes line, as captured by Tuesday's help-site reader: `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-24_hpauthsuite-help/MAP.md` lines 66-68 (the quote and its URL).
- The OneDrive guide, page 26 (limitation, workaround "Use SharePoint", resolution "TBA"): `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-24_hpauthsuite-help/docs/DOCS-MAP.md` line 13.
In the documents, cite them as HP's documents (the 4.4 release notes article and the OneDrive user guide p26), never by a local path of Tuesday's.

## THE JOB (lane D)
1. `cp -n` a before-copy of each of `02_architecture.{md,docx,pdf}` and `03_plan-of-attack-and-build.{md,docx,pdf}` in `<P>/1_Project_Definition/Design/` named `<name>.pre-1124b.<ext>` (the `.pre-1124` copies already exist from this morning: never overwrite them), read back with `cmp`.
2. At measuring (Tuesday, between the 12:36 note line and this commission; that count printed no clock): "shared with me" occurs 11 times in 02 and 3 times in 03 (case-blind, `grep -o -i -c`; control "onedrive" 62 and 44). Re-count yourself; list every occurrence with its line and section.
3. For each: remove "Shared with me" from what the rebuild BUILDS (features, screens, menu entries, Graph calls and permissions, tests, work packages, estimates, acceptance criteria), and where the design must still MENTION it, say it is NOT built, why (the 4.4 app removed it; Microsoft deprecated the Graph call; the guide's workaround is SharePoint), and the ruling (C-82). If a Graph permission or consent scope exists ONLY for Shared with me, say so and remove it from the permission list; if it serves other features too, keep it and say so in your reply. Any question in either document that only Shared with me raised (e.g. OP-20, T14) is marked closed by C-82, not deleted.
4. One CHANGE-LOG entry in each document, in its own form, naming C-82 and the two sources.
5. Re-render each .docx and .pdf by the method this morning's lanes used (find it in their outputs or scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s320/`; say which).
6. Prove by program: the .md before/after diff touches only the places of step 2-4 (a diff summary by section); "shared with me" left only in NOT-built / removed / change-log sentences (list each remaining line).

## RULES (as the B2018-B2020 "For every agent" section, plus)
No other change to 02 or 03. No Jira, GitHub, Linear or mail write; nothing to any person; the code repository is not touched; never delete; no `cd`; `python3 -I`; clocks from `date`; every count by program with a positive control. HPSM-POC is under a hold: nothing of it is opened. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/D/`.
Reply in at most 12 lines: anything that contradicts the ruling or the sources FIRST (e.g. the build already contains code for it: name the file); output paths with byte counts; occurrences before/after per document; permissions removed or kept; render method; what you did not verify.

## NEXT (Tuesday)
Fable review of both outputs (grant: OXPd document reviews through tonight's kick-off meeting); corrections applied; then a records + Jira kit for an OXPd seat: attach the new 02 and 03 Word+PDF to OXPD2-55 with one comment (Kam's standing rule, lesson 2026-11-24_oxpd-jira-holds-the-latest-design-docs-and-kams-actions), tick owed 113, and the owed-114 CLAUDE.md:58-62 edit, with history.
