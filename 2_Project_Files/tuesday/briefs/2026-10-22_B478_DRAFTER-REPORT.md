# B478 drafter report (read-only, 2026-10-22 20:04-20:25 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B478_SEAT-G44_hpsmpoc-b466-177-178-gate-tier1.md` (unstamped, about 56 KB; shape cloned from the B477 kit: every section, `## Stamp` with five blank slots, Step 0, REFUSE, Launch, Report, HOLD incl. the two-locks and Api-suite rules, 9 checks, SEVERITY/VERDICT, NOT TESTED, last line). It is over the 40 KB aim (B477 kit is 69 KB): the HOLD (binding, copied) is about 9 KB of it and the nine checks carry the named items; no check was dropped.

## Slot count with a control
- `/usr/bin/grep -c -E '_''_''_''_'` on the kit = **6 lines** (Stamp time, Launch authority, Heads at stamp, Model receipt, Hard stop, plus the last line `READ-WHOLE-BY-TUESDAY: ____`). Control: a scratch file `a____b` reads 1. The REFUSE line states 6.
- `@[A-Z_]+@` count 0 (control: `x @AB_C@ y` reads 1). Owner name (first name, surname) in the kit: 0.
- Tuesday still owes: the stamp, the `.pre-stamp` copy beside the kit, the READ-WHOLE line.

## Measured (command -> outcome)
- `ls-remote origin` 20:04:17: main `d70f9dc1…`; `b466/hpsmpoc-177-178-hidden-chars` `3eded112…` (= READY); `b467` `d6eba5f6`, `b472` `e353322e`, `b429` `4c02e8b9`, `b460` `b9fd28ed`, `b461` `52bd6e7c`, `b462` `e8ecb8ae`, `b465` `c65a5ab6`, `b459` `26460869`, `b438` `c1a245f8`; no `b478*`.
- Shape: merge-base `4695d7f2`; main..head 2, head..main 1; main-only commit `d70f9dc1` touches only `Hpsmpoc290Tests.cs`; legacy `merge-tree` 0 markers; `gh compare` diverged 2/1, 10 files. numstat per file as in the kit; `-` lines in the whole diff 8 (Assessment README 1, Feedback README 1, FeedbackEndpoints 4, Hpsmpoc99 1, api.ts 1). Commit trailers: `Claude Sonnet 5.5`.
- Overlap of the 10 paths with 9 live branches by `gh compare` + `grep -c -x -F -f`: all 0 (b429 43 files with control `web/src/instrumentation.ts` = 1; b460 1; b461 14; b462 6; b465 19; b467 9; b472 1; b438 2; b459 2). Open PRs 0 (control: closed list length 1). Required contexts: five. Check-runs on head 0; actions runs 0.
- Prior work (`git log -S` against the main sha): `HasControl` `7d073ca cfb16ec b9af5ad a8c165a`; `comment-invalid` `042db0c a6ae0b4`; `name-invalid` 0; zero control 0. (Note: `git log -S` without a ref printed nothing in the shared clone because local HEAD is not main; the kit says "against the sha".)
- Ruled messages: each occurs once in the word pack; at the head once in `FeedbackEndpoints.cs` (177) and in `Requests.cs`, `customer-detail.ts`, `customer-name.test.ts` (178); the old comment sentence has 0 hits at the head.
- Table `invisible-characters.json` at the head: 9 refused range rows (0000-0008, 000B-000C, 000E-001F, 007F-009F, 202A-202E, 2066-2069, E0000-E007F, 2028-2029, FEFF, FFF9-FFFC, 206A-206F as 11 pairs in 9 rows) equal the code's `Refused` by reading; `cases.kept` holds the emoji-with-ZWJ row. Not run: the equality is for the gate to prove over every scalar.
- Callers: `Shape.Customer(` two production callers; `Validate(` one production caller (`FeedbackEndpoints.cs:108`); `new Customer` sites `:83`, `:134` (constant self name), `ShowcaseSeeder.cs:496`: no second user-typed name write path found.
- Ports 8290-8299: 0 listeners (control: unfiltered `lsof` listed 22); `.tools/b478` absent (control: `.tools/b198` exists). `levels.opus.model_id` = `claude-opus-5-5`.

## Answers to the named items (what the kit makes the gate attack)
1. **Scotland-flag row.** The removed `Hpsmpoc99Tests.cs` line is NOT lost: the same code points (U+1F3F4 + E0067 E0062 E0073 E0063 E0074 E007F) are in `SubdivisionFlags` in `Hpsmpoc177InvisibleCommentTests.cs` (England, Scotland, Wales), with a refusal theory (alone and in a sentence, 422 + ruled sentence, nothing saved) and a parity theory. Drafter read, not run. **One weakness found by reading:** the parity row calls `FollowUpShape.HasControl` on both sides, so it pins the FUNCTION, not the follow-up note SURFACE; the kit has the gate route the flag through the real note guard (`Requests.cs:204-215`) and rates a gap Minor. The kit adds mutants F1 (put the row back in `RealText`: must go red), F2 (tag-sequence exemption), F3 (drop only the TAG range).
2. **Set equality / one source.** Both surfaces call `FollowUpShape.HasControl`; the branch touches neither it nor the table nor `answer-text.ts`. The kit demands an every-scalar run of both surfaces against an oracle parsed from the table (not `Refused`), start/middle/end positions, and 9 one-range-dropped mutants x 3 surfaces (M9). Two other invisible-character lists exist in `FeedbackEndpoints.IsInvisible` and `FeedbackFiles.cs` (they decide EMPTY, not REFUSED, unchanged); the kit tells the gate to read both and say why they are a different job.
3. **178 and the web.** Create and rename both go through `Shape.Customer` (400, list). The mock's `nameRefusal` is wired into create and rename. **Web shows the 400 message: NO for a customer name.** `describeFailure` (`client.ts:317`) shows the API message only for 422; a 400 gives "The service answered with an error (400). Try again." The feedback form does show it for 400 and 422. The builder stated this (FOR TUESDAY 5). The kit has the gate prove it with a scratch vitest.
4. **Contract fold.** `openapi.yaml:1922` still says "control or text-direction characters"; a grep of that file for `customer.name|name-invalid|name-length` prints 0 (the contract holds no `customer.name-*` code, even the existing length code). Reported as FOR TUESDAY in the kit.
5. **Suites/merge/overlap/gitleaks.** All in check 8 with controls; the Api-suite rule is in HOLD.
6. **PRIOR WORK.** Check 9.

## Findings the drafter adds beyond the brief (the kit asks the gate to measure each)
- **Held-name hazard (builder FOR TUESDAY 4, confirmed by reading):** `ApiSteps.tsx:74` sends the stored `shown.name` back on every profile save and `CustomerEndpoints.cs:194` has `heldIndustry` for the industry but no held-name allowance, so a customer already stored with a hidden character cannot save its facts. Kit: Major, FOR TUESDAY.
- Check-before-trim newly refuses edge U+000B/000C/001C-001F/0085 in a comment (silently trimmed before). Kit: Note.
- The mock returns the first 400 (the existing length cap) where the API lists all shape errors. Kit: Minor Note.
- Hazard in my own tooling: macOS `grep` has no `-P`; the kit's non-ASCII count uses `grep -c '[^ -~]'`.

## Corrections to the commission
- The brief says "10 files ... Hpsmpoc99Tests.cs +0 -1": confirmed. The brief's "mock/customer-detail.ts +12": confirmed (+12 -0). `api.ts` is +3 -1 (the import line).
- The kit says 8 `-` lines, which is the measured figure; the B477 kit's 16 does not apply.

## UNMEASURED by the drafter
Anything that needs a build or a test run (no `dotnet`, `vitest` or probe was run), the Jira GETs (not made; the kit gives the gate the comment ids 39894 and 39895 from the STATUS), gitleaks, the line numbers marked `~` in the kit (`Requests.cs:~139-143`, `Hpsmpoc177…:156-180`, `ApiSteps.tsx:~74`, `ClientFollowUpScreen.tsx:~151`), and whether any stored customer name at a hosted environment holds a hidden character (no hosted reads).
