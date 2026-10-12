From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B60 · SEAT-B: carry B47's feedback pill onto today's main as a NEW branch (no force-push), re-prove it, READY FOR GATE
**Fired: 2026-10-13 03:30 AEDT.** Pane `Datasec/MPS-B`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B60_SEAT-B_b47-feedback-onto-main.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. QA tier 1 follows your READY (a separate gate seat). Round 1.

## Why
B47 (`Briefs/2026-10-12_B47_SEAT-B_feedback-pill.md`, its STATUS `Briefs/2026-10-12_B47_STATUS.md`) ended `READY FOR GATE: b47/feedback-pill 81b0135d13a20b770df0669857d3043cf03653ec` on base b28c95eb. Main has since moved (B46/B49 home dashboard #28, B53 #29) and is now **d711b42cfcb53da3a2043a2d672511f8ea6ea296** (GitHub refs API, Friday 03:3x AEDT). B47's pane was closed, so this is a fresh seat. The B47 brief and STATUS are your SPEC: the feature, its holds and its tests do not change; only the base does.
Friday measured (GitHub compare API, 03:3x): B47's own changes = 31 files (merge base b28c95eb); the open fix round B58 (`b58/gate-b57-overlay-fix-round`, 4 files under `Inventory/` + three overlay test files) shares NONE of them, so B58 merging later will not touch your files. Expected conflict surfaces are the shared additive files B47's STATUS names (:47): `web/src/App.tsx`, `src/MpsCalc.Api/Program.cs`, `docs/api/openapi.json`, `docs/API.md`, `tests/…/EntraAuthTests.cs`, `src/MpsCalc.Api/appsettings.Development.json`, plus B47's one line in `tests/…/Infrastructure/ApiProcess.cs`.

## Do
0. `git fetch origin`; `ls-remote origin refs/heads/main refs/heads/b47/feedback-pill` must read d711b42c… and 81b0135d…; else STOP: NEEDS FRIDAY. `ls -a` your worktrees area: no `b60` worktree yet.
1. New branch **`b60/feedback-pill-on-d711b42`** from origin main d711b42c, in its own worktree. Bring B47's commits across (cherry-pick the range `b28c95eb..81b0135d` in order, or one squashed re-application — say which and why). **Never rewrite or force-push `b47/feedback-pill`**; it stays as the record.
2. Conflicts: resolve so BOTH sides survive (main's home dashboard + B53, and B47's additive hunks). Record every conflicted file and the resolution in the STATUS (a hunk-level line each). If a conflict needs a product decision (two behaviours that cannot both hold), STOP: NEEDS FRIDAY with the two options.
3. Re-prove on the new branch everything B47's STATUS proved (its "Suites" section :12 onward and the brief's §7): API xUnit (full, counts base d711b42c vs head), web lint + typecheck + Vitest (full, counts), production build, and the Playwright `web/e2e/b47-feedback.spec.ts` in STUB mode with synthetic data only. Plus: the existing home-dashboard and overlay tests still green (they are main's; any red is reported with base-vs-head runs, never fixed by editing main's tests).
4. NEW WORDS: list every user-visible string the branch adds (B47's `words.ts` and any server detail text), same as B47 did, so Friday can card them.
5. Push the NEW branch only (`git push -u origin b60/feedback-pill-on-d711b42`), read back with ls-remote. Write `Briefs/2026-10-13_B60_STATUS.md`: method, conflicts, counts, ports used, NEW WORDS, ls-remote line. Last line `READY FOR GATE: b60/feedback-pill-on-d711b42 <sha>` or `STOPPED: NEEDS FRIDAY`.

## HOLDS
- **Datasec only.** No other client's names, tickets or paths.
- **The Jira credential is not yours** (B47 brief §6): never read `4_Credentials/.env`, never put a token in code, tests, settings, CI or a commit; tests use the fake handler and `test-token-not-real`. Hosted store-path settings unchanged (records `BACKLOG.md:16-24`). Price-book data never goes into Jira.
- Ports **6630–6639** only (B47's range; `lsof` first, 0 listeners after you stop); stop your own processes by port + cwd, never by name.
- No PR, no merge, no deploy, no Jira writes, no history.md, never delete, never force-push, never dismiss a CodeQL alert.
