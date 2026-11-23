# B2023-B2025 COMMISSION (FABLE reviewers, in-session, READ-ONLY on the documents) - OXPd 2: review the meeting pack (B2023), 02_architecture (B2024), 03_plan with progress (B2025)

Written by Tuesday (s320). Model **fable**: the product owner's flag, Tuesday terminal 2026-11-24 ~08:12, verbatim "Use fable to review once you are ready." (EXPIRING-GRANTS row: Fable reviews only; authors stay Opus). One reviewer per document; prompt names the lane.

Read first: the authoring commission `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2018-B2020_OXPD-MEETING-PACK-AND-DESIGN-UPDATE_COMMISSION.md` whole (Kam's words, the sources, what each document was asked to be), and the project's `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/CLAUDE.md`.

## The documents (`<P>` = `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2`)
- B2023: `<P>/1_Project_Definition/Meeting/2026-11-24_OXPd-kickoff-meeting-pack.md` (+ .docx: check the answer boxes exist and are editable).
- B2024: `<P>/1_Project_Definition/Design/02_architecture.md` against its before-copy `02_architecture.pre-1124.md` (review the CHANGES and anything they make wrong elsewhere).
- B2025: `<P>/1_Project_Definition/Design/03_plan-of-attack-and-build.md` against `03_plan-of-attack-and-build.pre-1124.md` (the new §0 PROGRESS and the B2020 change-log entry above all).

## What to check (at source, never from the document's own claims)
1. Every statement of Kam's ruling or words: verbatim in `CLARIFICATIONS.md` or his notes file? Does the document claim he decided more than his words say?
2. Every status claim (landed, PR number, sha, test count, hold, finding): against `5_Project_History/history.md`, `git -C <P>/2_Project_Files log`, the gate verdicts in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2016_verify/` and `_B2017_verify/`, and Tuesday's pickup DELTA 1384-1389.
3. Pack only: any question already answered by Kam that is still asked (grep CLARIFICATIONS for its subject, with a positive control); any question that is two questions; any "Workpath team" item that only HP can answer, or vice versa; anything important to tonight's kick-off that is missing (what a team lead would ask first). Is it usable to drive a meeting in about an hour?
4. Contradictions between the three documents (read the other two where they touch your claims).
5. Secrets: no value of any password, key or token anywhere (locations only).

## Output
One file each: `<P>/1_Project_Definition/Review/B202n_FABLE-REVIEW_<doc>_2026-11-24.md`: findings table (id, severity Blocker/Major/Minor/Nit, doc:line, the claim, the source that contradicts it with its line, the exact fix text), then what you checked and did not. Never edit the document. Reply in at most 12 lines: Blockers and Majors first, counts by severity, what you did not check.
No `cd` in Bash; absolute quoted paths; `python3 -I`; nothing to any person; no git, Jira, GitHub or Linear write. Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s320/review/`.
