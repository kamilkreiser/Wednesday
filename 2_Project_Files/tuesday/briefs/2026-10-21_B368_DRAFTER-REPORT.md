# B368 DRAFTER REPORT (MPS records seat after PR #92), 2026-10-21 04:53-04:58 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B368_SEAT-R13_mps-records-pr92.md` (106 lines; pane `Datasec/MPS-R13`; routing rows C7 `model-routing.md:97` and C8 `:98`). Two stamp slots, count 2 by `/usr/bin/grep -o -E '@[A-Z_]+@' | wc -l`; last line `READ-WHOLE-BY-TUESDAY: PENDING`. The `.pre-stamp` copy is Tuesday's to make at stamping.

## Facts (MEASURED, read verbs only, times from `date`)
- PR #92 (`gh api -X GET …/pulls/92` under the project's `.gh-config`, 04:53): merged true, `merge_commit_sha` 1eccbc8baf6f930f15ae7931b4be79fe5dfc6e08, `merged_at` 2026-10-20T17:52:04Z (04:52:04 AEDT), head 3f1ebd139db815cf25849d3104ee9fc33a6bc44b, commits 2, files 2, +153/-0. The brief's stated parent/tree match: `git/commits/1eccbc8b…` one parent f78c64089ecff8e55984e10c278cf4615fccf91a, tree 495a007147500a454cc18b0c8f941f8a201f35fb, equal to `git/commits/3f1ebd13…` tree. `ls-remote` main = 1eccbc8b…; the builder branch still on origin at 3f1ebd13.
- The squash subject differs from the PR title (`(test-only) (#92)` vs `(test-only, B305-3/-4)`); both name MPSCALC-304 and -305, so no landing-text finding.
- Root repo: HEAD d422c8e31babcae374700c7aa9134c58952e6cfb (B360's records commit), CLARIFICATIONS.md clean at 782 lines, B360's section at `:748-782`; no `#92` and no `1eccbc8b` in CLARIFICATIONS (`log -S` 0, control `C-44` -> faf2695). `history.md` holds 0 lines for `B361|B365`. BACKLOG.md 2336 lines (B360 rows `:2270-2336`), JIRA.md 177 lines (B360 section `:168-177`).
- The two drafted lines are `B365_STATUS.md:153` (MPSCALC-304) and `:154` (MPSCALC-305). Each holds `(not merged)` once. The scan regex over both (digit-dot-digit, `%`, `$`, `Tuesday`, `Friday` plus name tokens) gives 0 hits; the planted control fires.
- Transition rule: the only written rule is the sentence in `JIRA.md` B351/B360 sections (`:163`, `:174`, also `:72`, `:89`, `:105`, `:122`): "no project rule moves a ticket on merge or deploy". Done transitions in `JIRA.md:28`, `:39` are answered question tickets. Nothing says a merged test-only change closes a ticket, so the brief transitions nothing and puts it in FOR TUESDAY with the gate's wording.
- B360 recorded Minors as individual rows, owner-question/words Notes as individual rows, and the remaining Notes as ONE grouped row (`[B360-B354-N]`, `BACKLOG.md:2312`), plus a pointer row and an open-decision row; no tickets. B368 copies that: `[B368-B365-1]`, `[B368-B365-N]` (B365-2..-6), `[B368-LANDED]`.
- Stray untracked root paths, not mine and not touched: `=` (0 bytes), `head-B104CarePackApiTests.cs`, `seller` (`git status --short`, 04:54).

## UNMEASURED (instrument in brackets)
- Any Jira state: the fences forbid Jira calls. Current comment counts on -304/-305 and the highest key are RELAYED from `B365_STATUS.md:49` (0 comments, 04:45:56) and `B360_STATUS.md:39` (MPSCALC-315, about 03:37). [the seat's `j360.py` GETs]
- Whether `.tools/b360/` helpers still exist. [`ls` by the seat]
- CI and CodeQL on the post-merge push of 1eccbc8b. [`gh api …/commits/<sha>/check-runs`]
- `AGENTMAIL_API_KEY` presence. [in-process test by name]
- Whether any seat filed to Jira or wrote BACKLOG/JIRA/history since 04:54. [the seat's before-snapshots]

## Questions, numbered, with recommended answers
1. Append the landing sentence and CodeQL fact to the two lines, beyond your replacement of "(not merged)" with "(merged as main 1eccbc8b)"? Recommend YES (B360 precedent; the replacement alone omits time, tree and not-deployed). To strike it, edit Part 1 item 2 to "replacement only".
2. B365-1 as BACKLOG row only, or a ticket? Recommend row only (R-B368-3, B360's R-R13-3); ticket it if you commission the optional tests-only fix round.
3. Transition MPSCALC-304 (GO) and -305 (GO WITH FINDINGS)? Recommend NO (no written rule; nothing deployed). If you overrule, name the keys at stamping (R-B368-2 gives the verb handling).
4. B365-2..-6 as one grouped Notes row? Recommend YES: none is an owner question or a words-gate item (B365 NEW WORDS 0).
5. Quote the stamps in CLARIFICATIONS without the launch-authority clause (it names a person), as B360 did (`B360_STATUS.md:140`)? Recommend YES.
6. A C-number for the section? Recommend NO (B360 precedent).
7. The stray root paths (`=`, `head-B104CarePackApiTests.cs`, `seller`): leave to a later cleanup card? Recommend YES, listed in the seat's FOR TUESDAY.
8. Launch gate: load1 under 7 via your waiter. Recommend YES; the seat does Python and Jira calls only.
