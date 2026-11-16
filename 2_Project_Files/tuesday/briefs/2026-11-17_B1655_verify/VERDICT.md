GATE B1655: GO WITH FINDINGS @ 7eed6f0 on main c74e2ec

Subject: datasecau/MPS-Commercial-Calculator, branch b1653/mps-lane-md2-test-comment, head 7eed6f0077d29254efefc00161cd4a4af1fdd2c4, base c74e2ecf24898220d9d2ab3c1262fcc63ecfcd55 (main tip read by gh api at review time: c74e2ecf, the compare to head reports behind_by 0).

| # | Check | Result | Evidence / control |
|---|---|---|---|
| 1 | compare base...head | PASS | status ahead, ahead_by 1, behind_by 0, total_commits 1; one file, tests/MpsCalc.Engine.Tests/PurchasePageEstimate.cs, +1 -1; patch hunk starts @@ -7,7 +7,7, changed line is line 10 (differing line numbers over both raw files: [10] only, 222 lines each); base line 10 with the old phrase replaced by the new phrase equals head line 10 (True; old phrase present in base line 10: True) |
| 2 | equal after removing // lines | PASS | base and head equal once lines whose first non-blank chars are // are dropped: True. Control: a planted identifier change (first "int " to "long ") on a copy of base compares False |
| 3 | pointer is TRUE | PASS | docs/ENGINE.md at head: exactly 1 line starts "\| X-33 \|" (count 1; line 160; control row X-34 also counts 1, so the pattern works). Row text: "page estimates are checked on **every** purchase quote, with or without deal usage, and a refusal stops the calculation before any figure is formed ..." which agrees with the comment's description (checks on every purchase quote; refusal stops before any figure) |
| 4 | added line and message | PASS WITH FINDING | added line is ASCII (isascii True; control with U+200B prepended: False); regex for B-numbers, ticket-style ids, Kam, Kreiser over the added line: no match. Commit message: subject "Test comment: point X-33 at its row in docs/ENGINE.md, not at a status record (MPSCALC-390)"; body "Comment only: one phrase on one summary line of PurchasePageEstimate.cs. No code, identifier or test row changes."; trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Clean of person names and B-numbers; it does carry the Jira key MPSCALC-390 in the subject (repo convention shows keys in subjects, e.g. 459db8b8 "MPSCALC-215/..."), not a card id. See finding F1 |
| 5 | other branch / open PR touching the file | PASS WITH FINDING | open PRs: 0 (pulls state=open length 0; control: state=all returns #208 closed). Of 231 branches, per-branch latest commit touching the path: 101 sit on main's last touching commit 459db8b8 (no own edit), 128 return no commit (the file does not exist on them), 1 is this branch (7eed6f00), 1 is b518/mps-api-input-hardening (9732ce5a, diverged 15 ahead / 108 behind main, an old pre-squash branch, no open PR). See F2 |
| 6 | STATUS claims, graded | RELAYED | STATUS reads: build `dotnet build MpsCalc.slnx -c Release` 0 Warning(s), 0 Error(s) at base and head; Engine tests Passed 743 / Failed 0 at both. Not re-run by me. A comment cannot change compilation unless it feeds an XML doc file: GenerateDocumentationFile count 0 in Directory.Build.props, Engine.Tests csproj and Engine csproj (control: Directory.Build.props TreatWarningsAsErrors count 1, so the grep reads the files). Note `///` summary text is only consumed if doc generation is on, and it is not. Equal counts are therefore expected, not proven by me |

## Findings

- F1 (low): the branch commit trailer is `Co-Authored-By: Claude Sonnet 5.5`, while the repo's squashes usually carry `Claude Opus 5.5`. The squash body supplied here ends with the Opus trailer, so the squash commit is unaffected. The commit subject names MPSCALC-390; the PR title omits it as asked.
- F2 (info): b518/mps-api-input-hardening holds an older, diverged version of this file. It has no open PR and is 108 behind main (it reads as a squash-merged leftover); a revival of it would conflict with line 10 only if it also edited that line, which was not checked.
- F3 (info): the new comment says "the row of that id in docs/ENGINE.md". The pointer is true at head (one X-33 row). If ENGINE.md ever carries a second X-33 row the pointer becomes ambiguous.

## NOT RUN

- No build and no test run by this gate (STATUS claims are RELAYED).
- Did not diff the full tree of head against base beyond the compare API's file list (one file reported).
- Did not read the branch b518 diff or confirm its relation to main beyond the compare counts.
- Did not read the builder's kit file or the Jira ticket MPSCALC-390; item 3's wording was taken from the brief text in the task.
- No check of the later-stage CI result on the branch (no PR exists, so no checks).
- Commit signature/verification not examined.
