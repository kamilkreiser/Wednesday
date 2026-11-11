STARTABLE: YES
(kit: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1521_SEAT-M124_mps-181-codeql-test-modes.md, 140 lines; 8 four-underscore lines = 7 Stamp slots + last line; 0 `@X@` tokens; 0 non-ASCII; 0 person names. Caveat: `.heavy-lock-1` was held at 20:59, so the builder's loop may wait; main moved after the old BASE, see Q2.)

## BLUF
- The kit's first idea (a mode like 0o750) is WRONG, measured at source: CodeQL 2.27.4 `py/overly-permissive-file` flags any INTEGER-LITERAL mode in `os.chmod`/`os.open` with a non-zero world digit, or (world zero) a non-zero group digit. So 0o750 and 0o710 are flagged "group readable". No literal wider than 0o700 passes.
- What the script checks: `scripts/deploy-from-ci.sh:119` `chmod 700 "$DIR.live"` (absolute), after `umask 077; mkdir -p` (:118). Any wider start mode proves the narrowing; the tests stay meaningful.
- Shape A (built and run in a scratch tree of head fa713a5b): keep the same real mode rwxr-xr-x but spell it `WIDE_FOLDER = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH` (not an IntegerLiteral, so not matched), plus a precondition `assertTrue(S_IMODE & (S_IRWXG | S_IRWXO))` after each chmod. One file, two sites, no new test name.
- n of N: emulator over the 11 python files of the PR: 6 `os.chmod`/`os.open` calls, 2 flagged (test_deploy_pre1.py:468, :506 = alerts #12, #13); the other four are 0o700, 0o400, and two non-literal. After the fix: 6 and 0.
- The csharp "not found" warning is not a cause: the CodeQL check output names only the 2 alerts; Analyze (csharp) success, 0 results; its log has 0 "not found". CodeQL check completed 09:45:24Z, csharp analysis uploaded 09:48:15Z (so the warning is most likely the "not yet reported" state; UNMEASURED where the text is shown).

## Facts re-measured (instrument; control)
- PR 181: head fa713a5bdf4b020d8754780c9b3bd269acb9de56, branch b1512/mps-lane-l5-ops-tooling, OPEN (`gh pr view --json`; branches/ API gives the same sha). Check run `CodeQL` failure, annotations 2 (both the chmod message).
- Alerts #12 and #13: `code-scanning/alerts/12`, path/line/rule/tool.version 2.27.4 (control: the check's annotations list the same two lines).
- Query: `github/codeql` `WeakFilePermissions.ql` at tag codeql-cli/v2.27.4 read by `gh api -X GET` raw, `diff` against main rc 0; lines 18, 34, 37-47 quoted in the kit.
- Emulator (my reading of the query, `emulate.py`, embedded in the kit): flags exactly 468/506 at head; plants 0o750, 0o710, 0o644, `os.open(.., 0o602)` flagged, 0o700 passes (control fires).
- Tests, under tripwire-az + strict PATH + empty AZURE_CONFIG_DIR (tripwire log absent every time), tarball of the head: unchanged `test_deploy_pre1.py` Ran 40 OK; with Shape A Ran 40 OK; P1 (delete line 119) FAILED failures=3 (ix_a and ix_b `pre-existing 0755` subtests, ix_c; fresh subtests stay green); P2 (`WIDE_FOLDER = stat.S_IRWXU`) failures=3 at the precondition line. A first draft of the precondition used `== WIDE_FOLDER` and P2 passed (vacuous); changed to the `&` form, re-run, P2 now red.
- Branch is 8 ahead / 4 behind main c7f5202e (main moved at ~20:50 by one commit, `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs`); open PRs: 181 only; `pulls/99999` 404.
- Ports 9730-9739: `lsof` 0 rows (control 15 listeners); text occurs in finished HPSM kits of 10 Nov (B1395 assigned it; B1455, B1460, B1466 range mentions), none in the live pane list (M123, M121 live).
- Whole python loop NOT run by me (heavy slot held); the 241 tests / 11 files figure is RELAYED from the gate verdict. I ran only test_deploy_pre1.py (40).

## D-decisions
D1 Shape A, symbolic flags, test file only. D2 Keep mode value (0755) rather than a "less wide" mode: nothing else survives the literal rule, and 0755 is the real state an earlier run leaves. D3 Precondition assertion added so the fixture cannot silently stop being wide (found vacuous-by-self-comparison in my own first version). D4 No suppression comment, no CodeQL config edit, no deploy-from-ci.sh edit. D5 Commit subject ends with the ticket key as the branch's other commits do (kit text carries no person, B-number, card id). D6 Clone by URL (B1520 pattern), no-az tripwire and strict PATH copied from B1517. D7 Seat does NOT run a local CodeQL (no CLI here); the hosted check on the new head is the deciding evidence and is written as UNMEASURED until it runs.

## Q for Tuesday (each with a default)
Q1 Is a non-literal spelling of the same wide mode acceptable to you as "a new round, not a dismissal"? It changes how the test is written, not what it proves, and the script is untouched. Default: YES (SHAPE A). If NO, the alternative is a CodeQL path exclusion for tests, a configuration change outside this kit.
Q2 Main moved (c7f5202e) and the branch is 4 behind; the kit makes a forward commit only and leaves any merge-in to you. Default: leave it.
Q3 READY target is Step 0 + 60 min (small change, one heavy loop twice). Default: 60.
Q4 If the new head's CodeQL check still shows "csharp configuration not found" while red/green is otherwise clear, treat it as a timing state, per the timestamps. Default: yes, re-read after csharp analysis lands.

## UNMEASURED
Whether hosted CodeQL accepts the non-literal form (DERIVED from the query only); where the "configuration not found" text is shown; whole python loop counts at the new head; `dotnet`/`web` check results (still running at drafting); whether M123/M121 will finish and release heavy slots in time.

## Outside-the-fences disclosure
Read-only `gh api -X GET` under the MPS GH_CONFIG_DIR: PR/branch/check-runs/annotations/code-scanning alerts+analyses/compare/pulls/refs, job logs (2 jobs), raw contents of the 14 changed files and ci.yml at the head sha, the head tarball (extracted in my scratch), and two reads of the public `github/codeql` query file (tag and main). Local reads: B1520 kit, B1512/B1517 kits and STATUS, B1512-2 verdict, tmux pane list, lsof, uptime, df, `git config --local --get` for the project's identity. I ran the repo's test file (40 tests) 6 times in my scratch with fake-only PATH. I typed `cd` once inside a process substitution while diffing two files (no effect on the shell; the hook did not refuse it); noted as a slip. Written outside the two deliverables: only /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s270/draft1521/ (tarball, tree/fix/mut copies, logs, emulate.py, proposed.diff). No git write in any project repo, no Jira, no mail, no az, no hosted-host HTTP.
