# B340 DRAFTER REPORT (2026-10-20 ~19:55 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B340_SEAT-R11_mps-records-wave1-findings.md` (29,061 bytes, over the ~25 KB aim; the findings table and the Part 3 rules are load-bearing). Seat SEAT-R11, pane `Datasec/MPS-R11`, Sonnet, one stamp slot `@SLOT:STAMP_TIME@` (Step 0b counts 0 on the copy; the `.pre-stamp` copy Tuesday keeps must count 1: MEASURED 19:5x on the brief as written, `/usr/bin/grep -c -E '@SLOT:[A-Z0-9_]+@'` = 1). I wrote only the brief and this report. No git write, no Jira write, no chat, no mail, no Artifact/Docs tool.

## Sources read
Whole: B308 brief (the shape), MPS `CLAUDE.md`, `JIRA.md` B99-B308 sections, `Registers/2026-10-20_v13-ticket-map.md` rows 1-60, CLARIFICATIONS `:628-640` and the tail, history.md top 25 lines, BACKLOG tail 30 lines, the B309 ANSWER-1 file (first 30 lines), B169 brief Part 3-4 (filing rules).
By section (line numbers in the brief): B318 STATUS `:341-434`, B319 `:1-9, :147-196`, B324 `:1-22 (verdict), :480-576`, B325 `:1-6, :31-41, :142-185`, B332 `:73-84, :130-150`, B305 `:211-222, :342-394`, B309 `:163-231`, B303 `:96-112`. Not read: the B310/B312/B313 words lists themselves (only their heading lines), the evidence folders, `.local`, Source_Documents.
Daily note `0_Brain/daily_tuesday/2026-10-20.md` lines 142, 159, 165, 167, 203 (grep); B309 brief stamp lines (grep).

## Measurements (read verbs only; instrument and time)
- `git --no-optional-locks -C <2_Project_Files> ls-remote origin refs/heads/main`, 19:47:30: `67bf2004f46096255a4ea761ffc568d107c4d8b0`. Equals the daily note's #86 squash.
- `gh api -X GET …/pulls/84` under the project `GH_CONFIG_DIR`, 19:47:56: merged, `acfcf5dec5d40257c1b917ef750256b6f76d0e2e`, 2026-10-19T23:42:03Z. I did not GET #85-#88 (their shas are RELAYED from the daily note and marked so).
- Root repo: `rev-parse HEAD` = `faf2695de8b5b2b09f44e0212b4c4b773249d926`; CLARIFICATIONS clean, history/BACKLOG/JIRA ` M`; `diff --stat` +188/+364/+84 (19:4x).
- Jira GETs (python, credentials in-process, 19:48:34; script `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/ceec922c-2944-48a5-bc00-14ba876a7b55/scratchpad/jr.py`): highest key MPSCALC-287; `mpscalc-b308` 56; `mpscalc-b340` 0; `zzqxvbw` 0; `PRE-1` 9; comment counts on 13 keys; no "BLUF: QA gate" in the last three comments of each (limit stated in the brief); `B319-1` text hits -263 and -151 (comments 39760, 39761, not mine, unread), `B318-1`, `B324-1`, `B332-1`, `B305-1`, `B325-1` 0.
- Finding counts per STATUS (by reading the sections): B318 10, B319 10, B324 11, B325 12, B332 4 (1 Minor + 3 Notes), B305 10. Tuesday's commission said B318-1..4, B324-1..5, B325-1..11: the brief records all and says the counts differ.
- Drafted Jira lines: B305 3, B318 6, B324 5, B325 4, B319 4, B332 4 = 26 (B318's T-V0-8 row has no line).

## Decisions I made in the brief (flagged, all overridable)
1. **Findings to Jira by severity, Notes BACKLOG only.** The project's convention (B164 24 tickets, B169 11, B308) is a ticket for each Minor+ finding no ticket covers, a comment where an open ticket's acceptance names it, and a BACKLOG row with a `Jira:` field. Expected 18 creates (cap 24), about 26 gate comments plus 3 extras. If you wanted BACKLOG only, strike Part 1's "T" dispositions.
2. **6(b) as a coordinator section, not C-46.** The 2026-10-18 precedent (`CLARIFICATIONS.md:628`) is "Tuesday's rulings, not Kam's; not C-entries". The ruling's words are your daily-note line 142 plus the B324 recommendation it accepted. The section also carries 6(a), 6(c) (as built) and the B309 ANSWER-1.
3. **The drafted lines say "(not merged)"**, now false for the head. Instead of editing them or posting 26 separate merge comments, each gets one appended landing sentence from the seat's own PR reads (R-R11-4).
4. **Scan hit I foresaw:** the -209 line contains `3.00` (a decimal in prose), which B308's digit-dot-digit scan flags. The brief lets the seat swap only that token and list it under Corrections.
5. **Words register** is a new Registers file committed with CLARIFICATIONS (2 paths); the builders' lists are copied verbatim by program; gate additions (B318-3, B324-10, B325-4) are listed separately; nothing is approved.
6. **B319-1, -2, -4 get no open row** (FIXED by B332, `B332_STATUS.md:130-137`); B319-3 is a ticket.
7. B325-6 becomes a sentence in the -34 comment (the finding itself asks the records seat to add the three unbuilt items), not a ticket.
8. Extra records items from the STATUS "FOR TUESDAY" blocks that you did not list but that name "the records seat": the -232 correction (22 of 28), the three B305-8 cite corrections, the -236 Scope sentence, B318-7 and B318-9 rows, a V4 purchase-pair diff-test comment, the -27 stored-as-sent comment, builder candidates (iii) and (iv) from B303.

## Open questions with recommended answers
1. **Ticket for B332-1?** STATUS leaves it to Tuesday. Recommend yes (a one-click wrong figure on a staff screen, graded Minor). Brief default R-R11-1.
2. **Is C8 right?** `model-routing.md:98` row C8 is "Brief drafting, board screens, gate kits, tooling with arms". A records seat is not in that row; B308/B272 name no row. Recommend keeping Sonnet and writing "records (B308 precedent)" if you prefer not to cite C8; I cited it as you named it.
3. **B319-3 `needs-ruling`?** Depends on what R-V5-1 left open (not read). The seat reads it and decides; recommend no label unless the stamp says the multi-device question is Kam's.
4. **Should #84's drafted lines (B305) get a landing sentence for a merge a day old?** Brief says yes (same rule). Recommend yes.
5. **Concurrency:** B311 (V2 Home) may launch while this seat runs; both are root/code-separate, but a V2 seat comments on Jira keys too. Recommend launching R11 first or accepting that the seat reads every comment whole before writing.
6. **Size:** 29 KB. Recommend accepting; cutting the Part 1 table would push per-finding decisions back onto the seat.

## Not done / limits
No Jira search for any finding symbol beyond the five ids above; the seat must run the search-first step. I did not open the evidence folders or the B310/B312/B313 words lists, so the register's per-source counts are unmeasured here. #85-#88 landing values are the daily note's, not mine.
