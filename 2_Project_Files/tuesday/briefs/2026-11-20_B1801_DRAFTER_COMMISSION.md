# B1801 drafter commission -- Security Composer lane CW-1: the sample crosswalk (PCOMP-29, L0-1), a records-only build (SEAT-C104)
Commissioned by Tuesday (s301), 2026-11-20 evening. Drafter model: Sonnet (routing row C8). You DRAFT a kit; you build nothing and
write no Jira, no GitHub and no record.

Draft ONE builder kit `2_Project_Files/tuesday/briefs/2026-11-20_B1801_SEAT-C104_composer-cw1-sample-crosswalk.md` (+ `.measured`;
ALSO save your drafter report as `2026-11-20_B1801_DRAFTER-REPORT.md` beside it and return its head as TEXT). The lane is defined by
the read-only plan `2_Project_Files/tuesday/briefs/2026-11-20_B1797_COMPOSER-LANE-PLAN.md` (158 lines; Tuesday of this session read it
whole): its section 4, "Lane CW-1", is the lane's scope, fences, sources, prior-work check and STOP list, and binds the kit; its
sections 2 (row PCOMP-29), 3 and 8 are context. The plan is an analyst's CLAIM: re-measure every fact of it that the kit freezes.
FORM: the last stamped Composer builder kit `2026-11-15_B1581_SEAT-C103_composer-lane-a-pcomp82-cover-date-sydney.md` for the kit's
skeleton (Step 0 copy, the STATUS protocol, final markers, the Stamp slots), and the last Composer records kit
`2026-11-18_B1688_SEAT-R265_composer-records-pcomp-74-80-81.md` for how a seat writes inside `1_Project_Definition/` and commits the
root records repository; read both in pages. Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole. All paths are under
/Volumes/Datasec_DEV/TUESDAY or /Volumes/Datasec_DEV/!CODING/Datasec. The paths named here were listed by Tuesday in commands dated
19:41:22 and 19:41:31 AEDT.

THE LANE, in one paragraph (from the ticket; read PCOMP-29 whole by Jira GET and quote its scope sentence in the kit): a crosswalk
from the client sample's 132 rows (the approved template's `analysis_row` M001 to M132) to the vendor product's 143 items and their
sub-settings, and to the Composer's registry controls and policy items, with flags for the rows the registry lacks and for M106.
It is a RECORDS document: one new dated folder under `!CODING/Datasec/Datasec Security Composer/1_Project_Definition/Content/`, plus
the seat's own STATUS and evidence under `.../1_Project_Definition/Briefs/`. NOTHING in the code repository, no pull request, no
content release, no deploy, nothing on any hosted site.

What the kit must settle or hand to a Stamp slot (each choice below is the coordinator's, never the product owner's):
1. SOURCES, each listed and sized by you: the approved template folder `.../Content/2026-10-20_hpsm-baseline-template-DRAFT` (read-only
   for the seat), `.../Briefs/2026-10-20_B314_evidence/extract/map132.txt` and `map132_sm316.txt`, and the two files of held pull
   request 85 the plan names (`content/sources/sm_316_catalogue.json`, `packages/content/src/sm-map.ts`) read by `gh api -X GET` at
   the head `851057291ffb019baee6c3c51a50d7b8833f5b3a` (Tuesday read that head, open and draft, at 19:40:28 AEDT) under the
   Composer's own `GH_CONFIG_DIR`, account read first. Say in the kit what the seat does if the head has moved (STOP and report).
2. THE OUTPUT SHAPE: propose it (one machine-readable file plus a short README, or as the ticket says); every row carries its
   M-id, the vendor item id(s), the registry control(s) and policy item(s), and a flag column; **no sentence of the client sample and
   no sentence of the vendor's text is copied into the new folder** (ids, enumerations and Datasec's own short labels only): the
   kit carries a by-program check for that (no line of 40 characters or more equal to a line of the template's source-wording fields
   or of the catalogue's description fields), with a planted positive control.
3. THE CHECKS, by program, each with a control that can fail: 132 rows, each M-id once; the absent rows flagged (the plan says 11:
   re-derive the number from the sources, do not freeze 11); M106 flagged; every vendor id present in the 143-item catalogue; a
   planted bad id reported; an M-id with two registry controls and no stated rule is a STOP, not a guess.
4. THE REQUIRED QUESTION (stamp checklist item 11, carried from round 1): the crosswalk claims to cover EVERY sample row and EVERY
   catalogue item. Name three things the sources hold that are NOT a clean one-to-one row (for example: duplicate vendor names, the
   13 duplicates the plan mentions; catalogue items no sample row maps to; sub-settings the sample names as items) and say for each
   whether the kit covers it or states it as a limit.
5. FENCES, frozen: the seat does not open anything of HPSM-POC (a hold stands to 2026-12-10); does not edit `CLARIFICATIONS.md`,
   `BACKLOG.md`, `JIRA.md`, `5_Project_History/history.md` or the template folder; writes no Jira (the records pass after the review
   does); no build, test, docker or install; no port. Review tier after READY: G2 (the plan's reasoning; say if you disagree).
6. PRIOR-WORK CHECK section (required in every Datasec kit): what exists and why (the plan lists B314, B330, B532: re-read each
   pointer), and a search of the repository's branches and pull requests for anything already naming PCOMP-29 (the plan read only the
   first 100 of the branch list: read them all, paged, and print the total).
7. THE KIT'S LOAD: print by program the byte sum of the kit plus every file its READ list names; the seat is Sonnet; keep it under
   about 400 kB or name sections and line ranges instead of whole files.
Slots for Tuesday's stamp: base facts (the pull request head, the source file sizes), RECORDS WRITE or DRY, hard stop.
Every count by program; every prose list recounted; no predicted number; no clock typed.

HOW: read-only everywhere except your three files and scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s301/d1801/`.
Jira GET only (credentials by name, in-process, from the Composer project's `4_Credentials/.env`, never printed). `gh api -X GET`
only. Git read verbs only in the project. No `cd` (a hook refuses it); zsh; absolute single-quoted paths; no unquoted word starting
with `=`. Clocks from `date` in the same command. Never delete. Write the kit to disk as you go; temp file then os.replace; ASCII;
`stamp_check.py` exits 0 with the slots unfilled. NO HPSM-POC anything; nothing of any other project; no request to any hosted site.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, the byte sum of the READ list, recommended slots, your answer to
item 4, corrections to this commission and to the plan, UNMEASURED.
