# B261 DRAFTER REPORT (HPSM-POC records seat R4, 2026-10-18)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-18_B261_SEAT-R4_hpsmpoc-records-1018.md`. Drafted 11:29–12:0x AEDT.
- Nothing was launched, mailed or written outside these two files.
- The project was read only: Jira GETs (plus JQL search POSTs, which are reads), gh GETs and git read verbs.
- Scratch copies of the records files are in the session scratchpad only.
- B261 was free in both Briefs folders (`ls | grep -i B261`: 0 and 0).

## What I read
- The template, WHOLE: the B257 brief (128 lines), its DRAFTER-REPORT (42), ANSWER-1 (13) and B257 STATUS (172).
- Today's sources, WHOLE: B258 STATUS (313), B259 STATUS (188), B260 STATUS (384), B260 ANSWER-1 (8) and ANSWER-2 (16).
- Each brief's stamp, by diff against its `.pre-stamp`: B258 `:99-102`, B259 `:156-157`, B260 `:107-112`.
- Records `origin/main` `2e284455` through the GitHub API: `CLARIFICATIONS.md` (1,342 lines; C-108…C-111 in full, and the `:1137` precedent) and `history.md:1-40`.
- Tuesday's `decisions.json`: the HPSM cards.

## Verified pointers
1. **PR #158:** merged 2026-10-17T22:59:28Z. Merge `d1fca809e28b283b29a54d02816efcc6409b5b67`, head `7fa59c5…`. Code main = `d1fca80` (API), present locally (`cat-file -t` = commit).
2. **Records:** main `2e284455` = PR #118 (B257), squash-merged by the coordinator account.
   - #118's head `69b6104` has CodeQL, Analyze (csharp) and Analyze (python) all success.
   - **No branch protection** on records main (404).
   - Highest heading C-111 (111 headings), so the next free is C-112.
   - 0 open PRs; no `records/b25*` or `records/b26*` branch is left.
   - `core.sshCommand` still names the other machine's key.
3. **Jira before:**
   - -260/-265/-262/-261/-264/-266: Backlog, 0 comments, assignee `616503d4…`.
   - Text searches `d1fca80`/`d1fca809`/`B258`/`B259`/`B260` all 0.
   - Highest key 273; transitions 11/21/31/41.
   - **B257's negative control `zzqxvbw` now hits 14** (B257's own tickets quote it). The brief swaps it for `qzxwvkj` (0). `ce40ce07` = 23.
4. **The Done rule** is B257's (its brief `:37`, its STATUS FOUND 7). B259 says all six Done-whens are met (`:13`, table `:84-98`), so all six go to Done, with findings filed as new tickets (B257's -256 precedent).
5. **Code cites, read at `d1fca80` by `git show`:** `ImportEndpoints.cs:135`/`:137` (StoredAt save and catch), `:191-195`, `:245-265`; `formGate.ts:93`, `:130`; `guard.ts:41-42`; `ShapeAnchorTests.cs:177-184`, `:243`; `deploy-package.py:463`. All hold.
6. **Catch-up:** records main has nothing for 18 Oct. The 8 project files are sha256-equal to Tuesday's copies wherever both exist.
7. **Decision store:** `hpsmpoc-hosted-runtime-10013-1017` is still open. No HPSM card was ruled on 17–18 Oct, so there is no Kam C-entry today.

## Doubts (for Tuesday, before stamping)
1. **FOUND-2 is EXISTING on HPSMPOC-207, not new.**
   - -207 (open, `b132-found`) is exactly the 3211 seed-lock wait + 3213 RCSI-read pair. It carries 6 sighting comments, including B191's same pair.
   - HPSMPOC-248/-249, which ANSWER-2 names, are Done timing-test tickets (`HostedDemoSlowFirstLoginTests`), related only.
   - So the brief makes FOUND-2 a comment on -207 (MC-7) that names -248/-249. A strike note turns it into a create (H01) if you meant a new ticket. Counts with the note struck: 8 tickets, 7 comments.
2. **"Tuesday's rulings → CLARIFICATIONS, not C-entries".**
   - The file has no un-numbered section, and C-111 is the precedent: it quotes Tuesday's answers verbatim inside the deploy C-entry. `:1137` says coordinator rulings are "not C-entries".
   - So the B258/B259/B260 stamps and both answers are quoted verbatim inside **C-112** (the B260 deploy entry), marked as the coordinator's, not Kam's, and not numbered. Only one new C-entry is written.
   - If you want a C-108-style numbered coordinator entry for ANSWER-2 (it narrows your own rollback rule), say so: that adds C-113.
3. **G05–G07 (B259-4/-5/-6 test gaps)** are filed because B259 `:13` says "Notes become tickets" and each has its own fix-shape. They are not on the gate's 4-item candidate list. Strike them → 4 tickets.
4. **G01/G02 Done-whens are mine.** The gate drove F-4/F-3 but wrote no regression test. Each ticket says so.
5. **G01 vs HPSMPOC-263.** Same phase-2 region but a different Done-when (shape 2f vs retry exhaustion), so I classed it RELATED and it is a create. You may prefer a comment on -263.
6. **MC-8 (a runtime reading on -268)** goes beyond the six tickets. It is there because B260 Open 5 re-measured 10.0.12 on three new containers. Strike it → 7 comments.
7. **Names:** B260 STATUS `:47` names a sample customer. The brief forbids copying it (the PDF is named by sha256 only). The catch-up copies carry it byte-for-byte, as earlier catch-ups carried such text. The HP-mail window scan stays yours (B257 ANSWER-1).
8. **B260 STATUS was written at 11:28 AEDT.** The brief tells the seat to use the current file if its sha256 changes.

## Summary
- **7 tickets:**
  - G01 F-4 (StoredAt retry exhaustion);
  - G02 F-3 (FailAsync unguarded);
  - G03 B259-1 (BFF over-refusal);
  - G04 B259-2+3 (census blind spots);
  - G05 B259-4, G06 B259-5, G07 B259-6 (test gaps).
- **8 comments, 6 Done:** six built/gated/merged/deployed comments, then Done; -207 (FOUND-2) and -268 (runtime reading), comment only.
- **C-112:** the B260 deploy (3 rounds, rollback, FOUND-2), with ANSWER-1, ANSWER-2 and the three stamps quoted verbatim.
- **History:** 4 entries (B258, B259 + merge, B260, the seat).
- **Records:** an 8-file catch-up on one branch `records/b261` from `2e284455`. Tuesday runs hpwin, opens the PR and lands it through checks.
