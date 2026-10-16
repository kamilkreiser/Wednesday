# B157 drafter report · MPS QA gate, seat Q, on lane F (7 branches) and lane H (MPSCALC-174)
Drafted 2026-10-16 ~16:00-16:15 AEDT. Brief: `2026-10-16_B157_SEAT-Q_mps-gate-lanes-F-H.md` (this folder). Nothing was launched or sent, and nothing was written outside these two files.
How the drafter read: `git --no-optional-locks` read verbs only in the project checkout, with no fetch. Conflict prediction used the legacy `git merge-tree <base> <a> <b>`, which prints to stdout and writes no objects. GitHub was read with `gh api` GETs under the project's `GH_CONFIG_DIR`. No az, no HTTP to the hosted site, no Jira.

## Measured
- **Pins:** `ls-remote` at 15:59:56. All nine shas equal the READY lines and Tuesday's list. Main = `621e3300…` (#44 B106-177 on #43 B102-175 on 0f8ad97). Every pinned commit is present in the local clone (`cat-file -t` = commit ×9).
- **Bases and lag behind main:**
  - 168, 162 and 174 sit on `7af91de`: 3 behind, 1 ahead.
  - 164 and 165 are stacked on 162: 3 behind, 2 and 3 ahead.
  - 166, 167 and 163 sit on `0f8ad97`: 2 behind, 1 ahead.
- **CI:** none of the 8 heads has any check-run (0 each), and no PR is open. Every CI number in the READY lines is a local run. Main `621e3300` shows 8/8 success.
- **Overlaps:**
  - 174 and main's #44 both change `FeedbackPill.tsx`.
  - 168 × 166 (and 162) all change `SourceDocumentChecks.cs`.
  - 166 and the stack both change `SourceLifecycle.cs`.
  - The legacy merge-tree gives 0 conflict markers for each branch vs main and for the pairs above. That is a reading; the gate measures it with `--write-tree`.
- **No figure or price path is touched.** For 7 branches, `diff --name-only` over Engine, Quotes, Import, docs and the web api/screens/proposal paths is empty. 166 adds only the new `Import/Validation/ReferenceDocumentValidator.cs`, which is called only from `SourceDocumentChecks.Run` at validate (`7dfa241:…SourceDocumentChecks.cs:96`, `SourceLifecycle.cs:401`).
- **164's refusal code:** activate and rollback of a document with a repeated key return `Unreadable`, which is 409 `SOURCE_DOCUMENT_INVALID` (`9a863fa:SourceLifecycle.cs:492-497`, `:825-826`). This matches B105's claim.
- **Hosted context:**
  - Hosted runs `0f8ad97` (B156 last line DEPLOYED).
  - It has no `overlay.json` and 4 feedback items (2 in `/1`, 2 in `/2`) (`B156_STATUS.md:54,71`).
  - None of the 17 setting names contains `SourceVersions`, so the version store is off on hosted.
- **Machine:** 0 heavy slots held; load 1.45 at 16:01; 0 listeners on ports 6750-6759. All ten lanes' STATUS files end in DONE.

## Choices made (deliberate; say if you want them otherwise)
1. **Verdict token = the template's `GO WITH NOTES`, not "GO WITH FINDINGS".** B91 and B95 use `GO | GO WITH NOTES | NO GO`, and their last line was `READY FOR REVIEW: …`. I kept their per-branch token and replaced the last line with your `VERDICT:` form: `VERDICT: B157 <a> GO / <b> GO WITH NOTES / <c> NO GO (of 8) on main <sha7>`, or `STOPPED: NEEDS TUESDAY` + one question.
2. **Jira GET is allowed, with `JIRA_*` exported by name from `.env`.** The template seats had "no Jira" and "never open .env". You asked for the ticket acceptance, and it is not in the register, which holds only row titles. If Jira is unreachable, the gate falls back to the BACKLOG rows.
3. **The gate takes heavy slots like a lane, at most one at a time.** Removing its own slot is the one removal the brief allows. With 8 branches, the minimum .NET runs are `m-stack` + `m-all` + each head's own new tests, and the brief says so.
4. **No records commit.** STATUS and evidence are working-tree files only. This differs from B95's `records/b95` branch and matches the B105, B106 and B156 practice under Tuesday.
5. **The brief adds an all-eight merged tree** (order 168, 166, 167, 163, 162, 164, 165, 174) beside the stack's merged result. Three of the branches edit the same two source files, so the merged tree is what actually ships.

## Traps for Tuesday
- **The branches are behind main, so a fast-forward is impossible.** 174 is based on `7af91de`, but main's #44 already rewrote `FeedbackPill.tsx`. 174's tests have never run on main's pill, so treat the gate's merged-tree result as the one that counts, not the branch head's.
- **Main may move during the gate** if you merge other lanes' PRs meanwhile. The brief makes the seat re-read main and re-run the merged line once. Merging lane-F/H-adjacent PRs (lane D contract, lane E inventory) before the verdict gives it more to redo.
- **Your two rulings are still open.** The brief treats "Expired does not count" (168) and the 164 repeated-key rule as Tuesday's and checks only the implementation. If you have not confirmed them, do it before reading the verdict, or say so on the board.
- **166 cannot be proved safe on the real price books.** That would need `.local/pricebooks/`, which the brief forbids. The CPP_INCONSISTENT and SOURCE_EXPIRED checks are only exercised on synthetic books. Hosted's version store is off, so nothing changes there today. It matters when `[B40-R3]` switches it on. If you want it measured, grant a counts-only validator run in a follow-up.
- **174 ships only part of its ticket.** The rate-limit half `[B47-D8]` is a local, unpushed branch (`150441b`), so MPSCALC-174 stays open after this merge. The brief also flags a contradiction for grading: on a feedback-only 401, the dialog says "Your session has ended" while the app session stays alive (B106's own test at `51102a4`).
- **165 reshapes `Program.cs` by wrapping it in try/catch** (+118 −86). The brief makes the gate prove with `diff -w` that no start or pipeline step moved. This is the one tier-2 change with hosted-start blast radius.
- **The real hosted backups sit in the project's `.tools/backup-B92` and `backup-B156`.** The brief forbids opening them; "hosted-shaped" means gate B59's H0 synthetic layout from `showcase.bicep:81-83`.
- **Port range 6750-6759 is the gate's.** If you launch a second gate for other lanes in parallel, give it another range and container prefix.

## UNMEASURED by the drafter
- Jira acceptance text.
- Whether the textual merges compile and pass.
- Base test counts at `621e3300`. The lanes measured 1,822 at `7af91de`; main has since added #43's tests.
- 163 under load.
- Hosted link counts.
- Whether 166's checks pass on the real price books.
