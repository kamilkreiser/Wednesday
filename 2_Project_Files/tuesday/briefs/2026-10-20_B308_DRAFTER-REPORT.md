# B308 drafter report (MPS v13 records + tickets, 2026-10-20 ~10:1x-10:2x AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B308_SEAT-R9_mps-v13-records-tickets-and-rulings.md` (Sonnet, light, no builds, pane `Datasec/MPS-R9`, report `<project>/1_Project_Definition/Briefs/2026-10-20_B308_STATUS.md`). Read verbs only; no Jira call, no git write, nothing published.

## Read whole
B303 brief (format template); project CLAUDE.md and JIRA.md; BUILD_PLAN (298 lines); B272 records brief (the closest records shape); CLARIFICATIONS lines 1-40, 310-345, 594-639 (not the whole file: 639 lines). Read in part: GAP_ANALYSIS lines 1-80 and 249-308 (BLUF, conventions, K-1..K-14, section 4), not the 85-row table; B303 drafter report head, B305 drafter report head, B307 STATUS head.

## Measured (command)
- Which repo holds records: `git -C <root> rev-parse --show-toplevel` = the project root; `git remote -v` empty (no remote); `2_Project_Files` ls-files grep clarif|history|BACKLOG|JIRA = 0.
- Convention: `git -C <root> log --oneline -8 -- 1_Project_Definition/CLARIFICATIONS.md` = B272 `5e9a7ca`, B171, B169, B99 straight to root main, path-limited, no push. Older seats used `records/bNN` branches (about 20 listed).
- State: root HEAD `5e9a7ca69fe3...`; CLARIFICATIONS clean; last entry `611:### C-43`, C-44 absent; history/BACKLOG/JIRA carry other seats' uncommitted edits (+174/+357/+71); plan and gap analysis are untracked.
- Card: `decision_queue.sh show mpscalc-v13-gap-15-decisions-1020` = ruled, a, ruled_ts 10:09:42 (Tuesday's write; Kam's board row 10:09:20 via `kam_rulings_today.sh`, own marker). 09:44:20 text confirmed on the board and in B307's brief `:4`.
- sha256: plan `b01df310...3bf6`, gap `03ea75aa...fa08`. Code main `21c2aec7` (ls-remote, informational).
- Convention for many sub-items on one card: C-23 table form, so brief defaults to ONE entry (C-45) with a 15-row table plus C-44 for the 09:44 context.

## Slots left for Tuesday (6, all `RULED: ____` in the brief's stamp section; Step 0b refuses unfilled; count 6, `.pre-stamp` copy not yet made)
R-R9-1 to R-R9-6 below. Tuesday must also copy the brief to `.pre-stamp` before stamping.

## Questions for Tuesday (recommended default)
- R-R9-1 entry shape: C-44 context + C-45 one entry with table, not 15 entries (default as stated).
- R-R9-2 T-V4-9 finance/lease (D-02 a = later): file with `later-phase` + `calc-register` (default) vs not file.
- R-R9-3 plan and gap analysis are untracked: add them to the records commit, 4 files (default yes).
- R-R9-4 T-V4-10, T-V4-11 not filed because D-06 a / D-07 a keep existing behaviour (default yes).
- R-R9-5 new `lane-v0..v11` label family (default yes).
- R-R9-6 existing tickets (-209, -27, -28, -59, -151, -137, -212) get a comment, no link verb (default yes).

## Things Tuesday should know
- Counts: the plan holds 66 T-ids (7+8+4+5+12+8+3+6+5+2+3+3). Expectation 57 created / 7 commented / 2 not filed is the drafter's guess from the plan's own duplicate list; UNMEASURED, the seat measures.
- Plan inconsistency flagged for the seat: BUILD_PLAN `:13` says five decisions keep an earlier ruling, `:266` and the rows name more. The seat must state both and not reconcile silently.
- Figures kept out of Jira by rule (plan percentages, fixture volumes); the scan gets extra strings. "Paul" and "HP Solutions Centre" banned in Jira text.
- UNMEASURED: no Jira read (highest key, the named duplicates' status, assignee id), AGENTMAIL key, whether history.md has B303/B305/B307 entries, whether any T-id hides two workloads.
- Brief is long (about 33 KB); the stamp needs one read of the "RULED BY KAM" and Part 2 Rule 8 sections.
