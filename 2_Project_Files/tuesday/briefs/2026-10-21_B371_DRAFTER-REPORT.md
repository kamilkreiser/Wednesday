# B371 drafter report (HPSM-POC PR #166 tier-2 gate, ROUND 2 of 2), 2026-10-21 05:52-05:58 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B371_SEAT-G15_hpsmpoc-pr166-gate-tier2-round2.md` (90 lines; three distinct slots `@MAIN@`, `@HEAD@`, `@STAMP@`, **29 occurrences** by `grep -o -E '@[A-Z_]+@' | wc -l`; last line `READ-WHOLE-BY-TUESDAY: PENDING`). Shape copied from B367 (stamped). Read whole: B367 brief, B367 drafter report, B367 STATUS (288 lines), B369 brief (123), B369 STATUS (110). Own measurements, read verbs only: `ls-remote` (main, branch, PR head) 05:52, `cat-file -t` x3, `rev-list --count 4794bde..777f29c` = 1, `diff --numstat` (Pkcs +6/-2, Feedback +30/-18), `diff --quiet 6818896 777f29c -- api/src` rc 0, `git log 6818896..777f29c` = 3 commits, `lsof`, `uptime` (4.04 5.61 6.96), `ls -d .tools/b36*` / `wt-*`, `grep` over the briefs folder, `model-routing.md:105-112` (G2 at :109, G-cap at :111). No dotnet, no Jira, no gh, no HTTP; wrote only these two files.

## Questions for Tuesday, each with a recommended answer
1. **Slots: I used three (`@MAIN@`, `@HEAD@`, `@STAMP@`), you named two.** The Stamp paragraph needs a stamp time and launch authority (REFUSE rule), so `@STAMP@` carries them as B367's did. Recommend: fill all three, save the `.pre-stamp` copy first; its control count is **29** (occurrences, not 3).
2. **Head move after the stamp: STOP, not "test the new head".** B367 allowed testing a moved head if it was a pure addition. At the cap a third head means a third round, so I wrote STOP + NEEDS TUESDAY. Recommend: keep.
3. **Ports `7370-7379` reused** (B367's block; its seat is finished; 0 listeners 7360-7399 at 05:52; B369 used 7380-7389, also finished). Recommend: keep.
4. **NO GO routing:** brief says a NO GO goes to Kam as a card, and the gate drafts the card (4 lines). Recommend: keep; it is the model-routing G-cap rule.
5. **Unconditional verdict needs CI complete (conditional suffix otherwise).** CI on `777f29c` is UNMEASURED by me. Recommend: launch now with the suffix (as B367 did) unless you read CI green first.
6. **Merge-tree prediction:** B367 said "never merge-tree --write-tree" for the shared repo but its r10 used it; I wrote "only inside the gate's own clone `.tools/b371/repo`, never in `2_Project_Files`". Recommend: keep.
7. **Gate's own mutants for the new code:** I added mBq (quote not stripped), mBc (constant boundary), a per-new-row product mutant of the gate's invention, and the round-1 set re-aimed. Recommend: keep; mBq and mBc are the only mutants that test the builder's option (i) choice.
8. **Sixth name-path row:** r4 asks for a Note if the gate finds one, not a requirement. Recommend: keep optional (a requirement would invite a new "exactly" fight at the last round).
9. **Optional real SDK 10.0.401 run of the Pkcs class** (the round-1 gate did it). Recommend: optional, NOT TESTED if skipped.
10. **Comment 39845 (-295) is stale for the fix head** (says 1511 -> 1514). I made it a Note for the records seat. Recommend: leave it; it was true at `4794bde`.

## Things I could not verify (all marked UNMEASURED in the brief)
- CI / check runs / CodeQL / `mergeable_state` at `777f29c` (your read says MERGEABLE; B369 read `blocked` earlier). The CI totals in r8 (Api 1529, assessment 889, other-and-feedback 640 + Feedback 302) are my arithmetic from round 1's 889 + 638 and the builder's +2/+4, labelled PREDICTED.
- The text of Jira comment 39855 and whether -295 still holds only comment 39845 (I did not read Jira; the gate GETs both). Your "comments 39844, 39855" on -294 is carried as MEASURED-T.
- The source lines `FeedbackFiles.cs:277-283 / :300-370` and the two new row headers at the head (RELAYED from B367 and B369; I read no product or test file at the head).
- That the names-multiset expectations "Feedback added 11 / Api added 5 versus pure base" are right (derived by me from 7+4 and 3+2).
- Whether pane `Datasec/HPSM-POC-G15` is free and whether any other seat is on the machine now (load 4.04 at 05:52).
- B366's end (05:20) and the lifted hold are RELAYED from the B369 stamp plus your message, not read from B366's STATUS.
- One discrepancy for you: B367's `.pre-stamp` shows 2 slot occurrences by `grep -o`, but `grep -c` (lines) read 1 here at 05:52 (two slots on one line); the new brief's control uses the `grep -o | wc -l` form (29).
