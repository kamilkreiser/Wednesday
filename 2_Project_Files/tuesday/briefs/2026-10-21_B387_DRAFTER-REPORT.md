# B387 drafter report (2026-10-21 ~08:25 AEDT)

Brief: `2026-10-21_B387_SEAT-G17_hpsmpoc-pr168-gate-tier2.md`. Shape copied from B375 (brief and report read whole). Builder STATUS B382 read whole (119 lines); builder brief only grepped (key lines :15-25, :77-90), so the gate is told to read it whole.

## Stamp slots
Two: `@STAMP_TIME@` and `@LAUNCH_AUTH@`, both in the Stamp paragraph (last sentence). Count by `grep -o -E '@[A-Z_]+@' | wc -l` = 2 (verified after removing a second mention from the SELF-CHECK). `READ-WHOLE-BY-TUESDAY: PENDING` is the last line; Tuesday replaces it.

## Measured by me (08:16 AEDT, read verbs only)
- main `54fbceac`, branch and `refs/pull/168/head` both `0f46875c`; `cat-file -t` = commit; log shows 2 commits (`0f46875`, `c9dd2fe`).
- PR #168: open, not draft, 2 commits, 3 files, +117/-2. Open PRs: `[168]` only.
- `diff -U0 -- api/src`: FeedbackModule.cs `@@ -174 +174,3 @@` (doc comment) and README.md `@@ -13 +13 @@` (table row clause); quoted in the brief.
- `.tools/b38*`: only b380 and b382 trees; no b387. No `b387*` remote ref.
- Row G2 text re-read at model-routing.md:109. Load 7.39 / 9.85 / 10.04.

## Deliberate departures from B375
- `api/src` escalation clause rewritten: the two allowed paths (comment-only .cs, text-only README), anything else is Blocker/tier 1.
- Added traps the builder left open: byte-hunt walker alone (T-a, builder admits it survives), vacuity of the empty export, the walker control can-fail (T-d), cref resolution, truth of "per person / 5 x N" (T-h), README table cell count.
- Known main-CI timing flake written in (question 7, T-j, r8) per your note.
- Api tests' Feedback rows: filtered run plus one whole-project run.

## Not verified (UNMEASURED)
- The new test file content, FeedbackPersonalData lines, FeedbackSubmitLimiter lines: RELAYED from the builder only.
- Which SQL Server shard runs the Feedback tests (brief says "probably api-other-and-feedback"); CI state at the head; the `ci` run id.
- Whether HPSMPOC-226 has exactly 6 comments now (derived 5 + 39860).
- Port block 7470-7479 listeners not checked; sibling branch name `b380/hosted-first-impression-235-234-232` is from the builder STATUS.
- No dotnet run.

## Questions (each with a recommended answer)
1. Launch with CI pending (conditional suffix)? Recommend yes, as B375.
2. Stamp authority: reuse Kam's 2026-10-16 merge-once-tested grant plus the board item 3 line as B375 did? Recommend yes.
3. Keep the extra mutants (m-name-leak, m-type-hex, m-sha-b64, m-sixth-key, m-drop-*, m-n-off, m-extra-file, m-lower-hex)? Recommend keep; the priority line lets the gate drop them after the builder's three plus T-a.
4. Launch now at load 7-10 with B380 live? Recommend yes with the HOLD as written.
