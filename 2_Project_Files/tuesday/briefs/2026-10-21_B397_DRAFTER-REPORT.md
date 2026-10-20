# B397 drafter report (2026-10-21 10:25-10:32 AEDT, clock from `date`)

Brief: `2026-10-21_B397_SEAT-D19_hpsmpoc-232-fix-round2.md` (55 lines, long paragraphs; slots `@STAMP_HEADS@`, `@STAMP_AUTHORITY@` 1 each; last line `READ-WHOLE-BY-TUESDAY: PENDING`). Read whole: B390 brief, B391 STATUS, B395 brief, B380 brief lines 93-110 and -232 mentions, B380 STATUS -232 sections (grep), `model-routing.md:92,109`, B389 HOLD dotnet text.

## Measurements
- Branch `b380/hosted-first-impression-235-234-232` = `refs/pull/170/head` = `b5ea627e7cd30511c48917f6e567a5c4eba64a48`; main `3aeeacc5` (PR #170 not updated); no `b397*`; `.tools/b397` absent; ports 7550-7559 free.
- `gh api --allow-escape-sequences .../actions/jobs/118918697027/logs` WORKED (94 KB; plain `gh api` refuses escape sequences). Results: `Failed 3, Passed 645, Total 648`; Feedback 302/302. The three failing names and the exact SQL Server texts are quoted in the brief: INSERT app_user batch `SET NOCOUNT ON;\nINSERT INTO [poc].[app_user] …;\nINSERT INTO [poc].[audit_event] … OUTPUT INSERTED.[audit_id] …;`, and `SET IMPLICIT_TRANSACTIONS OFF;\nSET NOCOUNT ON;\nUPDATE [poc].[app_user] SET … OUTPUT 1 WHERE …;`. Row 4's line in the log read `warmCallerWrite rolled back in 3 ms` (plant never fired).
- Read `Support/ApiFactory.cs:176-179` (`SqliteQuoted` maps `[poc].[x]` and `[x]` to `"x"`, so the schema prefix is already handled) and both test files at `b5ea627e` (assertions at `FirstVisitWarmupTests.cs:252-254`, Rollback `:224-227`, `:242`, recorder `See` at `:47`).

## FINDING the B391 fix shape missed (put into the brief as a TRAP)
On SQL Server the app_user INSERT and the audit_event INSERT go in ONE batch (log item [3]); SQLite sends them as two commands. Stripping `SET …;` fixes the `INSERT INTO "app_user"` and `UPDATE "app_user"` anchors, but the Rollback test's `StartsWith("INSERT INTO \"audit_event\"")` (about `:226`) would still fail on SQL Server because no command starts with it. The brief therefore asks for a statement-splitting normaliser with any-statement semantics (also for `FailWhen`) and mutant n2 for the split. This is my reading of the log text, not a SQL Server run (UNMEASURED); the seat must confirm from the log. I did not read line 226 itself beyond the grep/sed output (`:225-227` area from the raw file: lines for INSERT app_user, INSERT audit_event, UPDATE app_user are consecutive).

## What changed versus your instruction
- Normaliser = strip `SET … ON|OFF;` + SqliteQuoted + statement split (above), not just strip + quote.
- Partition: ApiFactory.cs is read-only to the seat (normaliser goes in a new `Support/SqlBatchText.cs`); if it must live in ApiFactory the seat STOPs and asks.
- Brief says #170 now carries only -232's value (-235/-234 land via #175); Step 7 forward-merge waits for your ADDENDUM and expects a clean merge (identical content on both sides); any conflict = STOP.
- No Jira write; the correcting comment is drafted in the brief (Step 8a) and the seat fills the sha/CI state.

## Questions (recommended answers)
1. Should the fix seat push to #170's branch while B396 gates #175 from the same history? Recommend yes: separate branches; #175's head is unaffected.
2. Is a merge commit for the forward-merge acceptable on #170 (squash lands it anyway)? Recommend yes.
3. Stamp slots: `@STAMP_HEADS@` (stamped heads: branch `b5ea627e…`, main `3aeeacc5…`, #175 `89bdb18e…`, with `ls-remote` time) and `@STAMP_AUTHORITY@` (Kam's 2026-10-16 grant + terminal words 2026-10-21 ~07:2x + the 2026-09-01 three-hop QA gate rule; the fix-round-2 ruling, Tuesday 2026-10-21 ~10:2x).
4. The brief's Step 4 re-runs m232a in a scratch worktree only; if you prefer none, delete that sentence.
