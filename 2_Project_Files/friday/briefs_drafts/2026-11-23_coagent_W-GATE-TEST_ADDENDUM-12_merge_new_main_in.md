This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_W-GATE-TEST_brief.md`. Seat W-GATE-TEST only.

# W-GATE-TEST ADDENDUM 12: main moved a minute after your fetch; merge it in; one small ruling; then the short check

Your "ADDENDUM 11" section is read by Friday (the M1 part and the proofs whole). The round did what was asked. Two things before the check:

## 1. Main has moved: merge it INTO your branch
The lane `allow-measure` merged at about 14:10, just after your fetch showed main unmoved. By Friday's own ls-remote: `refs/heads/main` = `20785c3e9389ac2275cdfda2ec7fb55eb1176425` (it was `3768a67d1d41b47439776657afbc114bd14bc439`); your branch is `9bbc466c0f1e3617968cf3f7b2b6ef6363c33536`.
- `git fetch origin`, confirm main is `20785c3…`, then `git merge origin/main` into `w-gate-test` (a merge commit; never rebase, never force).
- Expect conflicts in `BACKLOG.md` and `docs/M0-OUTCOMES.md` only (both lanes appended at the end). Resolve by KEEPING BOTH SIDES WHOLE: main's appended lines first, then yours, no line of either changed or dropped. Anything else in conflict is a `STOP Q1`.
- That lane added one folder, `spikes/U-B1-hook-allow-silent/`, and no product file. Do not touch it.
- Prove it in STATUS: for each of the two documents, main's file (at `20785c3`) is a byte-for-byte PREFIX of yours (a Python byte test, with a control: a copy of main's file with one byte changed must fail); the count of your own appended lines is the same before and after the merge; `git diff --quiet 9bbc466 HEAD -- spikes/W1-windows-exec-hook spikes/W4-windows-paths preview/plugin-template-windows` exits 0 apart from what section 2 below changes (name the files); `git diff origin/main HEAD -- crates Cargo.toml Cargo.lock scripts preview/lib preview/plugin-template preview/make-plugin.sh` is 0 bytes; `git diff --name-only origin/main...HEAD` lists only your owned paths.

## 2. RULED BY FRIDAY: the init events' own `uuid`
You were right to leave it and ask: the list was closed. Ruling: it goes too. In the two stream `init` lines (the stage C copy and the last sitting's part 1) replace the event's `"uuid"` value by `<event-uuid>`, by the same program, counted in those two files' headers; your raw comparison and your names scan gain that class with a control. After it the "any UUID" row of your scan reads 0 added lines. Nothing else changes.

## 3. Then
- Re-print at the new head: the raw comparison (unexplained 0, with its red control), the names scan, `w1.py selftest` (44 PASS), `git diff --quiet 462faca HEAD --` the three runner files (exit 0), `cargo fmt --all --check`.
- Push the branch (no force). Last two lines of STATUS: the full head sha, then `READY FOR QA W-GATE-TEST r3`.
- ONE short check of the fix round follows at that head. No model run, no PC run, no runner change.

After ANY context compaction, re-read the brief, all addenda and your STATUS whole before writing anything more.
