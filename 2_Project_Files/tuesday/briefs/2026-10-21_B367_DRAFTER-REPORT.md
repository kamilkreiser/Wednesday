# B367 drafter report (HPSM-POC PR #166 tier-2 gate), 2026-10-21 04:34-04:45 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B367_SEAT-G14_hpsmpoc-pr166-gate-tier2.md` (slots `@MAIN_SHA@` and `@STAMP_TIME@` unfilled, count 2; last line `READ-WHOLE-BY-TUESDAY: PENDING`). Shape copied from B357. Read verbs only (`gh api` GET under the project's `.gh-config`, `git --no-optional-locks ls-remote` / `cat-file`, `lsof`, `uptime`, `date`); no dotnet, no Jira read, no write outside the two drafter files.

## What I read
B357 brief (whole, 85 lines), B357 drafter report (whole), `B357...md.pre-stamp` (slot lines only), B364 STATUS (whole, 125 lines), B364 builder brief (whole, 105 lines), the PR #166 patch for both files (whole, `gh api pulls/166/files`), `FeedbackFiles.cs:296-402` and `FeedbackEndpoints.cs:88-102` at the head (`gh api contents?ref=4794bde`), `model-routing.md:105-112`, `models_latest.json` (`levels.sonnet.model_id`), B366's brief (grep for ports, trees, merge, main pin; not read whole).

## Facts (MEASURED unless marked)
- Clock: first read `date` 04:34:30, last 04:36:34 AEDT. Load `3.62 4.98 6.56` (04:34), `3.52 4.49 6.15` (04:36).
- `ls-remote`: main `6818896b68090777c8edbf0e694741928c96ca3f`; branch and `refs/pull/166/head` both `4794bde3ac1fc7e0025146e37c11dfa6bd63db90` (04:34 and 04:36). `b364*` 1 ref, `b367*` 0, control `b300*` 1.
- PR #166 (`gh api pulls/166`): open, draft false, `mergeable_state` blocked, 2 commits (`560ef654…`, `4794bde3…`), 2 files, +174/-13, base `6818896`; compare 6818896...4794bde = ahead 2, behind 0, merge base 6818896. Open PRs: only #166; control `--state merged --limit 2` = #165, #164.
- Files: `PkcsInPackageTests.cs` +28/-9, `Hpsmpoc290Tests.cs` +146/-4. Objects for head, base and commit 1 present in `2_Project_Files` (`cat-file -t` = commit x3).
- Check runs at the head: 18 (7 success, 1 neutral `CodeQL`, 10 in progress incl. all four `Analyze`, `api`, both SQL Server shards, vitest). A read 2 minutes earlier listed 13 (e2e legs added meanwhile). `ci` workflow run on the PR: `39467193765`. Code scanning on the PR ref: 1 analysis (`/language:actions` at 4794bde, 2026-10-20T17:34:43Z); open alerts 0. Control on main: 4 analyses at 6818896 (csharp, javascript-typescript, python, actions), 0 open alerts. Required contexts of main (5) as in B357; `web (Next.js)` not yet on the head.
- Main's last green run at 6818896 (check-run times): `api on SQL Server (api-assessment)` 118743110132 16:17:04Z-16:30:35Z (13m31s); `api-other-and-feedback` 118743109922 -16:33:09Z (16m05s); `api (ASP.NET Core)` 118743109431 -16:26:48Z (9m44s); an aggregate `api on SQL Server` 118751291789 exists on main (3 s).
- Ports: `7370-7379` 0 listeners; `7360-7369` 0 listeners at 04:3x (B366's block, not yet bound); unfiltered listeners 11 (control). Brief census: `\b737[0-9]\b` 0 files; control `\b730[0-9]\b` 3 files; `\b736[0-9]\b` 2 files (B366's brief and its drafter report).
- Trees: `.tools/wt-B366` exists, `.tools/b366` did not yet; builder's `.tools/b364`, `.tools/wt-b364-base`, `.tools/wt-b364-fix` present; no `b367*` anywhere. `.tools/b198/lock.sh` present.
- Model: routing row G2 at `model-routing.md:109`; `levels.sonnet.model_id` = `claude-sonnet-5-5`.
- B366 brief facts (RELAYED by grep, `B366_...md:32,43,89`): deploys main `6818896` and STOPS if main differs; block 7360-7369; worktree `.tools/wt-B366`; says Tuesday holds B364's merge until the deploy ends.
- Slot count of the unstamped brief: 2 (the `.pre-stamp` equivalent). Tuesday must save a `.pre-stamp` copy before filling the slots so the gate's control (reads 2) can fire; I wrote only the two permitted files.

## Things I found that change what the gate must do (read before stamping)
1. **The commission's "-9/-4 are comment-only" is not true line by line.** From the patch: `Hpsmpoc290Tests.cs` -4 = 2 comment lines + 2 CODE lines (`private sealed class FailingBody : Stream` becomes a primary-constructor declaration; the `throw new NotSupportedException("planted: …")` line becomes `throw fault?.Invoke() ?? new NotSupportedException(Planted)`). `PkcsInPackageTests.cs` -9 = 8 comment lines + 1 `[InlineData]` line changed only in its trailing comment. The builder discloses the 4 changed Feedback lines itself (STATUS `:62`). The brief (T-f, r5) tells the gate to measure by program, with a control, and to byte-compare the new `Planted` constant to the removed literal, rather than assert comment-only.
2. **The Done-when's "mN red in 5" is unreachable by the code as I read it** (mN affects `:348`, the name path; the two file-name rows reach `:370`). Builder measured 3. The brief makes this a Note for the records seat, not a NO GO, unless the gate finds a reachable unbent row (T-e, r4).
3. **Product path correction:** the builder brief says `FeedbackFiles.cs`; it lives in `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackFiles.cs` (tree listing). The gate brief uses the right folder.
4. **`dotnet build-server shutdown` is machine-wide.** B357's release line required it. With B366 live, that could hit its build servers, so the gate brief forbids it, requires `DOTNET_CLI_USE_MSBUILD_SERVER=0`, `MSBUILDDISABLENODEREUSE=1`, `UseSharedCompilation=false` on its runs, and release by ancestry.
5. **Merge/main coupling:** B366 pins main at `6818896`; PR #166's merge moves main. The brief says the verdict does not trigger a merge and writes `MERGE: HOLD (B366 live)` into FOR TUESDAY; the VERDICT last line keeps B357's exact shape (no merge word).
6. **Added attack points beyond the commission:** derived-host disposal (could close the shared SQLite keep-alive; order test, T-a), duplicated seeding on second startup, SQL Server per-instance database naming (the control row could be red on SQL Server, T-a(iii), r8), log capture shared across tests in the class, whether the filter header is inert on the shared host (T-b probe with a control), vacuity of "count unchanged" (T-c), the 400 theory's reliance on `Rows` labels, and gate-own mutants mR (swallow inside the reader: old guard AND new 500 row must both go red), mW, mH, mC, mD, mM, mU.
7. **Jira GET:** the gate may not copy the builder's/B300's `jira.py`; the brief tells it to write its own short GET reading `JIRA_*` in-process.

## UNMEASURED (with the instrument that would measure it)
- Whether B366 has since bound a port or created `.tools/b366` (re-run `lsof -nP -iTCP:7360-7369 -sTCP:LISTEN` and `ls -d .tools/b366` at stamp; Tuesday).
- Which CI shard runs the Feedback project and which runs the Pkcs class, and any shard totals (job logs by GET after completion; the gate does it).
- Whether the xunit config serialises tests within the class (read the Feedback test project's xunit settings; gate r2(f)).
- Whether `FeedbackApiFactory` ConfigureWebHost shares the database on SQL Server for a derived host (`FeedbackApiFactory.cs:40-49` read by the gate, and the SQL Server leg).
- Live Jira state and comment ids 39844/39845 (not read by me; no Jira GET was in my fence scope; gate r9).
- Whether main moves before launch (re-run `ls-remote origin refs/heads/main` at stamp).
- Load at launch time (B366 may run heavy jobs).
- Whether the model line `brief_seat: model=…` prints for the gate (launch-time).

## Questions for Tuesday, with recommended answers
1. **Gate tier: G2 Sonnet, with `api/src` in the diff as Blocker and tier-1 re-gate?** Recommend yes (tests and comments only; mechanisms measured by B286 and B283).
2. **Round count: 1 of 2?** Recommend yes (new PR; B357's GO WITH FINDINGS means no NO GO has been spent).
3. **Launch with CI pending (conditional verdict suffix)?** Recommend yes; CI completes in about 10-16 minutes and the verdict carries `(CI pending: …)` otherwise.
4. **Launch while B366 is live?** Recommend yes only with the HOLD as written, and only when load1 is below 8 at launch (the launcher's waiter pattern from B357). If you prefer zero risk to B366, delay the launch until B366's STATUS exists; the cost is the gate runs after the deploy and the merge waits longer.
5. **Port block `7370-7379` (none expected)?** Recommend yes.
6. **Is a NO GO justified if the Done-when's "mN red in 5" cannot be reached?** Recommend no: GO WITH FINDINGS (Note) plus a records amendment ("mG 5, mN 3"), because the clause contradicts the code and the builder reported honestly. Say otherwise at stamp if you want the ticket text treated as binding.
7. **Should the gate's own mutants include the product-file mutants (mR, mW, mH) that live under `api/src` in the scratch worktree only?** Recommend yes (scratch, never committed), as B357 did for its mutants; it is the only way to show the old guard and new row differ.
8. **Jira comment byte-equality (39844/39845)** is NOT TESTED by design (another seat's tree). Recommend the records seat compares them, as for B357.
9. **Stamp:** after filling the slots, save the pre-stamp copy first (`.pre-stamp`) so the REFUSE slot-count control has something to read, and re-run `ls-remote` for main and PR head just before.
