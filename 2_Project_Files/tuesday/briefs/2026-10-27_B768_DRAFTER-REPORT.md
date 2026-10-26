STARTABLE: YES

# B768 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H40: HPSMPOC-356 docstring half, then HPSMPOC-228 gate-N-8 half, one branch, two commits)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B768_SEAT-H40_hpsmpoc-356-228-infra-test-rows.md` (127 lines, shape of the B708 kit). Drafted Tue 27 Oct 2026, `date` reads 00:41:15 AEDT at the first read; the writing came after the last read. Drafter: Sonnet 5.5, read-only. Nothing built in a project tree, nothing fetched, no ref written; scratch runs on copies in the session scratchpad only.

## BLUF
- Startable now. Pins hold: main `4c067e4f600d814f8b80672369a687f1702b43ed`, no `b768*` ref, open PRs = #222 only (one Api test file, no overlap), ports 8610-8619 free (lsof empty, control fired), no pane or kit names H40 or B768, local clone holds the base commit.
- **Finding that changes the design:** a comment strip alone fixes only ONE of the three N-8 rows. Measured on main (regex stage, copies of the product file): commented-out call (line and block form) = still 1 match (green, the leak); `return;` and `break;` after the pass = 1 (green); renaming the `timer` local = 0 (RED, the unwanted red). So the kit adds a second check (loop cannot be cut short: return/break/goto/throw as whole words in the loop body; the real body holds none) and makes the regex follow the timer's name. The ticket's "fix-shape: strip comments" under-describes its own regression rows.
- Two more guard holes measured and deliberately left out of the lane (reported, not fixed): `if (false)` before the call and an added `await Task.Delay(...)` after it both still match (green).
- Docstring half: the three sentences are at the cited lines on main (385-387, 409, 428). The same imprecision appears a fourth time near lines 432-433 ("the values of the env entries (for instance ..." across a line break); the kit's property covers it and the seat lists it.
- Reader on main: 34 tests OK under 3.14.7 and 3.9.6; timeout 30->20 control FAILED (failures=1).
- Gate round: assumed NO GO 0 of 2 on two NEW classes; Tuesday states it at stamp (Q-1). Load was 7.81 at 00:44: the seat's heavy runs will wait.

## Facts re-measured (instrument, time, control)
- main: `ls-remote origin refs/heads/main` and `gh api -X GET commits/main` both `4c067e4f...` (2026-10-26T12:39:23Z). `ls-remote 'refs/heads/b7*'` listed 14 refs, none `b768*` (control: lists `b709`, `b753`, `b759`).
- Blobs at main, `git hash-object` of the raw API bytes = API `sha` = local `rev-parse 4c067e4f:<path>`: `test_ci_workflow.py` `a183d2ac...` (813 lines, 48277 B); `test_security_baseline.py` `ecfedeeb...` (1623 lines, 97191 B); `ci.yml` `0176b491...` (679 lines, unchanged since `b069274c`); `FeedbackDispatcher.cs` `962cdb63...` (21704 B).
- Open PRs: `[222]`; `pulls/222/files` = `api/tests/HpsmPoc.Api.Tests/Hosting/RequestTimingLogTests.cs`. Stale branch `b71/f006-title` (2 ahead, 161 behind) lists `infra/tests/test_security_baseline.py` (`compare/main...`); `b71/comment-followup` lists neither path (so the filter fires on one and not the other).
- Compare control used in the REFUSE rule: `compare/b069274c...4c067e4f` lists 18 `web/` paths and `infra/tests/test_ci_workflow.py` once (`grep -c -x -F` = 1).
- Reader: `python3 -I` on a scratch layout from the main blobs: 34 tests OK (3.14.7) and 34 OK (3.9.6); timeout edit (2 diff lines) = `FAILED (failures=1)`.
- Guard regex (`DISPATCH_LOOP.findall` from the main module on single-edit copies, each edit `count == 1`): real file 1; `//` call + no-op 1; `/* */` call + no-op 1; `return;` after 1; `break;` after 1; `if (false)` 1; `Task.Delay` after 1; `"//x"` before call 1; comment holding `return;` 1; **controls:** timer x1000 = 0, `timer` rename = 0. (A column my script printed as "violations" was a stub and is not cited.)
- Product loop (lines 287-310): `\b(return|break|goto|throw)\b` finds 5 lines in the whole file (control, count 5, last at 213 and 264), none in the loop; 28 `///` lines, 0 `/*` lines, 10 lines with `@"`, `$"` or `"""`.
- CI predicate: required job `infra`, step `validate ...` runs `bash infra/scripts/validate.sh` (`set -euo pipefail`), whose line 21 runs `python3 tests/test_security_baseline.py` with `BICEP`; its `main()` runs its own tests and every `infra/tests/test_*.py` and fails on a failed test, a `ResourceWarning` or an open file. `BICEP_VERSION: v0.47.16` in CI. Importers of `test_security_baseline`: `test_hosted_demo_pin.py:19`, `test_outbound_address_spelling.py:15`, `validate.sh:21`.
- Callers of `test_ci_workflow`: none outside the file (a zero that rests on one fact; control: `test_security_baseline` hits `validate.sh:21`).
- Local Bicep: `.tools/bicep/bicep` exists, no `bicep` on PATH. I did NOT run it (it is an executable; the kit allows the seat to run it and to read nothing in that folder).
- Ports 8610-8619: lsof empty (rc 1); control: python socket on 8611 listed (2 lines with the header), 0 after it ended. Word scan over 62 non-`.pre-` SEAT kits of 10-26 and 10-27: no hit (control: `x 8611 y` 1, `x 18611 y` 0); no kit names H40 or B768. Panes: `tuesday`, `Datasec/MPS-G158`, `Datasec/HPSM-POC-D33`, `Datasec/MPS-G157`, `fleet-monitor`.
- Ruleset on main: `deletion, non_fast_forward, code_scanning, required_status_checks`. Squash precedent: `CLARIFICATIONS.md` line 138.
- Model: `models_latest.json` line 23 `claude-sonnet-5-5`. Routing line 85 is row L6; its S55 cell reads "1st fallback" (the O15 and Spark cells ahead of it are not routable to a Datasec seat; the Studio-only local model ruling), line 92 (C2) reads "1st"; line 109 is G2 tier 2. `brief_seat.sh` line 24 defaults to Opus; the launch line carries `BRIEF_SEAT_LEVEL=sonnet`.
- Jira (HPSMPOC-356, HPSMPOC-228, read whole): 356 is Backlog with 0 comments and names B734-2/3/6/9; 228 is Backlog with 1 comment (the N-8 note) and its old line numbers (638-640, 671) are now 727/760. Gate sources read: B734 STATUS lines 440-460 and 485-495; B243 STATUS N-8 note and line 5.

## D-decisions (taken by the drafter; Tuesday accepts or changes at stamp)
- D-1 Series order: commit 1 = docstring (`test_ci_workflow.py`), commit 2 = guard (`test_security_baseline.py`); two disjoint paths, one per commit, one PR, one squash.
- D-2 Docstring half is docstring-only: the kit forbids any code change in `test_ci_workflow.py` and proves it by AST equality (module minus class docstring) with a planted-edit control.
- D-3 The (c) word list is derived from the code by program, not copied from the gate; a table of plants proves each reworded claim true (F3 flip green, `PART` value red, each listed word red, benign echo green).
- D-4 N-8 is built as three properties: comment strip (string-literal aware), loop-cannot-exit-early check, rename-following regex. Applied to the dispatcher text only; `FeedbackModule` text is left alone and the seat reports one plant for it.
- D-5 Red-first against the OLD guard (a scratch main file plus only the new tests): the wrong-on-old rows must fail there.
- D-6 No Jira write by the seat. B734-3, -6, -9 stay open on the ticket (its text already says so); the seat lists them under FOR TUESDAY.
- D-7 Hard-stop suggestion: target READY 100 min, hard stop 160 min after launch.
- D-8 `.tools/bicep/bicep` is made an execute-only exception to the `.tools/b*` read-forbidden rule, since `bicep` matches `b*` and the CI predicate cannot be run without it.

## Q-questions for Tuesday (each with a default)
- Q-1 Gate round: the kit assumes NO GO 0 of 2 on two new classes ("docstring wording of a reader", "the R11 guard reads comments as code"), one gate for the one PR. Default: that.
- Q-2 Jira: the commission said the seat records B734-3/6/9 "as left open" on the ticket, ticket comment only if the kit's scope says the seat writes Jira. Default: NO Jira write (the ticket body already records all three as open; the records seat comments after landing). Say if you want one seat comment instead.
- Q-3 Is the extra check "loop cannot exit early" (return/break/goto/throw) in scope? The ticket row "early `return;` after the first pass RED" cannot be met by a comment strip. Default: YES, as written.
- Q-4 Routing cell: line 85 S55 reads "1st fallback", not "1st". Default: the receipt cites L6 line 85 as commissioned plus C2 line 92; Sonnet either way.
- Q-5 Pane: `Datasec/HPSM-POC-H40` is free now; the sibling Pkcs seat (H39, B767) was not visible in the pane list at the read, so its branch name and exact paths are as you stated, not measured. Default: the kit lists its paths as given and tells the seat to stop on any live branch sharing either of ours.

## UNMEASURED
Whole `test_security_baseline.py` run and its test count at main; `.tools/bicep/bicep` version; runner Python version; whether the rule (not only the regex) goes red on each plant; whether `DISPATCHER_ON_WHEN_ROUTE_ON` / `POLL_DEFAULT` read comments as code in `FeedbackModule.cs` (never planted); the 10 literal-bearing lines of the product file (not read); GitHub's parser; the H39 seat's actual state.

## Outside-the-fences disclosure
- Read-only everywhere except the two files written here. `gh api -X GET` only, under the project's `GH_CONFIG_DIR`; `git --no-optional-locks` read verbs (`ls-remote`, `rev-parse`, `log`-via-API, `grep`, `cat-file`) in `2_Project_Files`; Jira GETs through `.tools/b649/jira.py` (its first 80 lines read; output saved to the scratchpad). The Jira comment on HPSMPOC-228 carries a person's display name in the helper's output; it appears in no file written.
- Scratch under the session scratchpad: the fetched main copies of four files, a two-folder reader layout, and `r11.py` (loads the main `test_security_baseline.py` as a module via `importlib`, which executes its module-level code; it opens no hosted host and wrote nothing outside the scratchpad). Python runs used `-I`.
- One socket bound to 127.0.0.1:8611 for 4 s as the port control, then freed (a background python in the same command, no `pgrep`). No az, ssh, docker, HTTP to a hosted host, mail, chat, Artifact, Docs, decision-queue, scoreboard, `_ledger*`, `fleet/briefs_staged/`, WEDNESDAY or FRIDAY tree, or non-Datasec project. I did not open the decision-card store. Two hook advisories (case-sensitive grep) were seen; every count that matters was paired with a control above or is marked as resting on one fact. One shell command was refused by a hook for an unquoted `======` word and was re-run without it.
- No person's name and no decision-card id appears in the kit (`grep -c -i` of two surnames over the kit = 0; stamp-slot lines 8, at-sign tokens 0).
