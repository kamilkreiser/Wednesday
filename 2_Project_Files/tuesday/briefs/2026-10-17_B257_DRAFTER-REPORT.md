# B257 DRAFTER REPORT (HPSM-POC records seat R3, 2026-10-17)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B257_SEAT-R3_hpsmpoc-records-1017.md` (127 lines). Drafted 16:0x-16:2x AEDT. Model claude-opus-5-5 (Kam 2026-10-09 override). Nothing launched, mailed or written outside `tuesday/briefs/`; the project was read only (Jira GETs, gh GETs, git read verbs). Scratch reads in the session scratchpad only.

## What I read
- Templates, WHOLE: B169 (129 lines) and B164 (271), Tuesday's MPS records briefs.
- HPSM-POC: `CLAUDE.md` (51), `JIRA.md` (17), `BACKLOG.md` (53). The newest HPSM-POC records brief + STATUS: **B250** (`Briefs/2026-10-16_B250_SEAT-G_…`, 106; `B250_STATUS.md`, 115), WHOLE. This is the HPSM shape I used, not the MPS one: records branch on `HPSM-POC-analysis` + PR by Tuesday; Jira Done-on-merge when the Done-when is met; C-entries for deploys (C-104 shape); HP-mail window scan.
- Records `origin/main` `6f5f0dc` via the GitHub API: `CLARIFICATIONS.md` (1,254 lines; C-103…C-106 read in full) and `history.md:1-24`. Not the root working copy (stale).
- Sources: B252 STATUS (verdict, acceptance, findings, fix-shapes, candidates, comment lines, Check 5), B255 STATUS (whole tail from Findings), B249/B253/B256 STATUS (BLUF, Open, Records, last lines), B249 ADDENDUM-1, B256 ANSWER-1, B256 evidence `ci-failure-excerpt.txt`, B174 STATUS R2-3 lines.
- Tuesday's `decisions.json` (both HPSM cards), `kam_msgs.sh` (live), daily note 2026-10-16 lines 48-53.

## Verified pointers (file:line, quoted at source)
1. **#156:** pulls API: merged 2026-10-16T22:14:14Z, `72073dace1635899e1262548e561781073b4c7b4`, head `9195408…`; the title names -251/-252/-253/-258/-256/-255. **#157:** 2026-10-17T04:03:43Z, `787d159089d8a774801b03e959f269c8a12e4ce1`, head `7a2c7ae…`, -254. Code main = `787d159` (local log).
2. **Jira before:** all seven in `Backlog`. -251/-252/-253/-256/-258 have 0 comments; -254 has 1 (39430), -255 has 1 (39431). `text ~ "72073da"` 0, `"787d159"` 0 (control `ce40ce07` 9). Transitions on -251: 11/21/31/41 (Done = 41).
3. **B252:** comment lines `:449-465` (task said ~:438-465; candidates are `:438-447`, 8 candidates + B251's line). All six tickets CLOSED (`:2-7`). B252-1 is a Minor regression (`:384`).
4. **B255:** `:2` (-254 Done-when OPEN), `:10` (B254-1…-4 dispositions). The **ticket candidates are `:258-268`, not :250-262** (the Findings table is `:233-243`, fix-shapes `:245-256`). The -254 comment line is `:270-271`.
5. **Kam 12:11:53:** `kam_msgs.sh`: `2026-10-16T12:11:53.920000+11:00 | [live] view=tuesday`, text `Decision hpsmpoc-hosted-words-9-b241-1016: a — Approve all 9 as written; deploy main to hosted`. Equal to `B249_ADDENDUM-1:4` and `B249_STATUS.md:3`. Store `ruled_ts` 2026-10-16T12:12:25.556119+11:00 (differs by 32 s; the brief quotes both, as C-103 does).
6. **-229 words:** `ImportPendingSweep.cs:98` @787d159 = the sentence, verbatim. B249 Open 3 = `:203`; B253 Open 2 = `:244-245`. **In B256 it is Open 5 (`:271`), not Open 2** (B256 Open 2 is FOUND-1, `:266`).
7. **`__EFMigrationsLock`:** B256 `:140-146` (2/886, job 117304131543, 36 s each), Open 1 `:262-265`, ANSWER-1 `:7`, `:13`; B174 `:347`, `:359`. Jira: 0 hits for the symbol, both test classes, `AcquireDatabaseLock`, `"Execution Timeout Expired"` and `R2-3`; related only: `"application lock"` → -140 (Done, the seed lock), `flake` → 7, all Done.
8. **Card `hpsmpoc-hosted-runtime-10013-1017`:** open, posted 16:04:09 AEDT, default b ("Nothing changes … re-raises this on Monday 19 October").
9. **Records:** main `6f5f0dc`, highest `### C-106` `:1245`. Next free is C-107. The only `records/b25*` branch is b250 (#117 merged); 0 open PRs. `core.sshCommand` still points at the other machine's key path.
10. **Code cites,** read at `787d159`: `formGate.ts:93` and `:122-131`, `ImportEndpoints.cs:187-191`, `PkcsInPackageTests.cs:43/45/71/76`, `guard.ts:18`, `ReportingEndpoints.cs:940`, `NarrativeOutputValidator.cs:217/307`, `ImportPendingSweep.cs:98`, `AssessmentModule.cs:183`, `HostedDemoRobustnessTests.cs:79`. All hold. `72073da..787d159` touches no source file in those paths (only the csproj and the test).
11. **Assignee:** "assignee" has 0 hits in `CLAUDE.md`, `JIRA.md` and `BACKLOG.md`. Assigned tickets (-226, -229, -248, -249, -237) hold the project lead's id (= the API account). B250's -251…-259 and -91 are unassigned.
12. **Catch-up:** 15 project-folder Briefs files from 16-17 Oct are missing from records main (the API listing has only B250's five).
13. **Pane** `Datasec/HPSM-POC-R3` is free (`cockpit.sh status` 16:11; control: 7 panes listed).

## Doubts (for Tuesday, before stamping)
1. **"-229 words → C-entries".** No ruling exists. The store has 0 hits for "Upload the files again", and the card Kam ruled at 12:11:53 did not include the sentence (ADDENDUM-1 `:13`). I did not invent an approval. The brief instead records **C-108 as Tuesday's coordinator rule** (it doesn't block while imports are off; Kam's word is owed before imports go on), says in the entry that it is not Kam's ruling, and files ticket **W01** (`needs-kam`), which aggregates it with B252-2's 500 text. Strike C-108 if you want only Kam rulings in the file. The C count then falls to 4.
2. **P01/P02 vs HPSMPOC-254.** -254's own Done-when already covers the hosted and local runtimes, which makes it EXISTING under the dedupe rule. The brief files them anyway as separate fixes, keeps -254 open as the umbrella, and adds a strike note. Striking it gives 12 tickets.
3. **Done transitions.** This is the B250 precedent: Done when merged code meets the ticket's Done-when. Tuesday's brief set that rule; no project file states it. The seat STOPs if it finds a contrary rule. -256 goes to Done even though B252-1 is a regression on its path; the gate itself proposes a new ticket for it (G01).
4. **Assignee:** no CLAUDE.md rule exists. I chose HPSMPOC-229's assignee (the majority precedent). B250 left its tickets unassigned. Strike the rule if you prefer B250's way.
5. **B252 candidate 8 (B252-14)** is filed as G07, although the gate says Tuesday may close it as no action. B252 candidate 2 is folded into W01 rather than filed alone.
6. **Deploy records:** I read the project's convention as a C-entry per deploy plus a history entry (C-104/B238). The three deploys get C-109…C-111. There is no separate Jira deploy comment for B249 (its tickets were closed by B250 before the deploy). For #156/#157 the deploy line goes inside the merge comment.
7. **Last-line token:** `RECORDS DONE: B257 @ <sha> · …`, following B250 (your daily note fixed the HPSM token to RECORDS DONE). It is not MPS's `DONE: B169`.
8. **Not measured:** the -251…-258 descriptions' Done-when texts (the seat reads them; B252 `:67-79` quotes them as of 08:28), -226's Done-when (it decides whether G06 is a comment), and B252-6's exact line.

## Summary
- **14 tickets:** G01-G07 from B252, W01 (words owed before imports go on), P01-P05 from B255 (P01 names the open card), F01 (`__EFMigrationsLock`).
- **7 comments and 6 Done:** one merge + gate + deploy comment each on -251/-252/-253/-255/-256/-258 (all then Done) and -254 (comment only; runtime Done-when OPEN).
- **C-107…C-111:** Kam's 12:11:53 ruling (verbatim, both times), Tuesday's -229 rule (marked as not Kam's), and the deploys B249/B253/B256.
- **Records:** 4 history entries, a 15-file catch-up, one branch `records/b257` from `6f5f0dc`, and Tuesday opens the PR.
- **Main doubts:** C-108 (no Kam ruling exists for -229) and P01/P02 overlapping -254. Both carry strike notes.
