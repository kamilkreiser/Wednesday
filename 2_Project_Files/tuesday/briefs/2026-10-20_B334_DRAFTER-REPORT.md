# B334 DRAFTER REPORT — NexusAI PR #98 fix round 2 (SEAT-W17)

Drafted 2026-10-20 15:25-15:4x AEDT (`date` 15:25:01, 15:26:42), read-only. Brief: `2026-10-20_B334_SEAT-W17_nexusai-pr98-fix-round2.md` (37,666 bytes, one stamp slot `@SLOT:LAUNCH_TIME@`, last line `READ-WHOLE-BY-TUESDAY: PENDING`).

## Measured facts (read verbs and `gh api` GETs only)
- **Refs (ls-remote 15:2x):** `refs/heads/b302/test-code-codeql` = `refs/pull/98/head` = `49ba21e101f3…`; main = `1bc9e9df5eea…`; `refs/heads/b334*` = 0 lines (control `rd-863*` = 1).
- **main since base:** `1bc9e9df` = squash of PR #100, 1 parent, HISTORY.md only. Not in the local object store (`cat-file`: bad object), so merging main would need a fetch. `49ba21e` is local (`commit`).
- **PR #98:** open, draft, 8 commits, 34 files, +245/−76, mergeable clean, author `kamilDatasec`. The body is stale ("17 files, 6 commits … 8bb6c339 … the seat continues").
- **Open PRs:** #99 (S101O RD-863, `172d321f`: rd863 test, `backend/server.js`, counts file), #97 (`278afc25`), #67 (`94b288cc`). Overlap with `rd407-…test.js` or `jsonStorage.js` = 0 each (control: `server.js` in #97 = 1).
- **G30-1 site at `49ba21e`:** the plants are at `rd407-concurrent-settings-writers.test.js:541-542` (CONTROL cell `:536-547`) and `:556` (ai-log cell `:549-561`). The `tmpDir` is `fs.mkdtempSync` (`:92-93`). The product paths are at `jsonStorage.js:1087,1089,1103`. `FALLBACK_DATA_DIR` is at `:802`, and the gate's `:1287` is now `:1204`/`:1278`. The repo precedent is the RD-155 equality guard at `auth-gate-fail-closed.test.js:89-99`.
- **The gate's mutants:** C1 (`setQuickQuestions` throws `STORE_UNREADABLE` over a torn file) and S8b (`quick_questions.json`→`quick_questions_x.json`) are in `evidence/mut/`. C2 = C1+S8b and has no file of its own.
- **RD-786's commit `017cf69` and Jira text (comment 39732)** both already say "21 of the 26".
- **Jest lock (15:25):** held by gate 31 `qa-g31-H3a`, pid 98392, since 04:21:06Z. The queue is empty. The tool sha256 is `3c33f5ae…a792`, the same as gate 30's pin. Load is 1.92. T9 is unmounted.
- **B302:** its pane is gone and no process runs in `worktrees/b302-*` (0). `b302-test-code-codeql` holds the branch (clean) and `b302-verify/node_modules` exists. The worktree list has 152 lines.
- **Ports:** 7560-7569 has 0 listeners, and no 2026-10-20 brief names it.
- **Routing:** C2 (`model-routing.md:92`), whose counter is "as C1", and C1 reads "one fix round on the same seat model" (`:91`). Result: Sonnet. G2 is at `:109`.

## Open questions (each with a recommendation)
1. **Builder edits the PR body?** Recommend **no**. The B302 brief made `gh` GET-only (`:26`), the gate assigned G30-3 to Tuesday, and no project rule grants a seat PR edits. The builder drafts the text to `Briefs/2026-10-20_B334_PR98-TEXT.md` and Tuesday runs `gh pr edit`. (Written that way.)
2. **Builder files the follow-up ticket?** Recommend **no**. The B302 brief said "No create" and no project rule grants it. The builder drafts the text and Tuesday's records step files it. (Written that way.)
3. **Merge main 1bc9e9df into the branch?** Recommend **no**. The change is HISTORY.md only, the PR is mergeable clean, and gate 30's merged-tree addendum came back 152/152. C-184's forward merge is the merge author's step and C-68 concerns product code. A merge would also need a fetch. (Ruled 6 in the brief.)
4. **Jira comment on RD-786 this round?** Recommend **none**: "nothing else changes". Comment 39732 is already accurate on "21 of 26", and Tuesday's records step can add a G30-1 note.
5. **Fix shape:** recommend an `expect` path-equality before the plants, so the red is an assertion. Keep writes rooted in `dir`. Going back to `store.<file>` would re-raise #106-#108, which makes 18 of 26. (Written that way.)
6. **Landing style (for Tuesday, not the builder):** C-190 item 2 says "Never squash, never rebase (C-68)" (`CLARIFICATIONS.md:2067`). Gate 30's checklist says squash, and PR #100 landed as a squash. Recommend Tuesday decides before landing. If the land is not a squash, the RD-788 "exact checks" subject and the c6 message stay in history, and the PR text says so.
7. **Full verify required?** Recommend **yes**, once at the head under the lock, with lock starvation handled by the ADDENDUM-1 STOP rule rather than a skip.

READ-WHOLE-BY-TUESDAY: PENDING
