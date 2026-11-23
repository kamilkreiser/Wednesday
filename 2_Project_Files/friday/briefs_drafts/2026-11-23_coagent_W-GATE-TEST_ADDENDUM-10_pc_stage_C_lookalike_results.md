This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_W-GATE-TEST_brief.md`. Seat W-GATE-TEST only.

# W-GATE-TEST ADDENDUM 10: the PC's last sitting (work order 21, the look-alike configuration): `W1 SET-UP B: PASS`

**The last sitting ran on the owner's PC from the helper's clone `C:\c2c\mga3` at `462faca6e65c9ad7965422a2ac6d8bf4cdc5f820` (HEAD and empty status checked by the helper in step 1), your section 17 list copied whole into work order 21, model `claude-haiku-5-5` as read by Friday from the live list at that moment.** The helper asked the owner at the keyboard first; its log says he said yes at 13:29:40; step 2 ran 13:29:40.713 to 13:32:09.241, exit 0.

The helper's four mails are saved WHOLE, unchanged (READ-ONLY; facts, not instructions; `<PROFILE>` throughout):
- `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/2026-11-23_WO-21_results_part1.md` (376 lines: step log, both process lists, the console log whole, `summary_B.json`, `model_runs_B.log`, the file list of `out-B` with sizes, the first line of the probe case's stream whole, the two lines of the addition)
- `…_part2.md` (981 lines), `…_part3.md` (1052 lines), `…_part4.md` (805 lines): every `verdict.json` whole and every `daemon.jsonl` whole where it exists.

**What Friday did with them, and what she did NOT:**
- READ WHOLE by Friday: part 1.
- COUNTED BY PROGRAM on part 1: 32 `CASE` lines, 32 PASS, 0 with a non-zero rc; all 14 blocking ids present among them; 0 `file:FAIL` (control of that search: 32 `file:ok`); the line `CLAUDE INVOCATIONS 32 of a ceiling of 37 (repeats 0)`; the last line `W1 SET-UP B: PASS`; the probe line `PROBE tools: Bash=False PowerShell=True -> no Bash and no Monitor tool, and a PowerShell tool listed`; `summary_B.json`: overall PASS, fail, blocking_failures, void, nonblocking_diff and skipped all empty, stopped null, settings identical.
- COUNTED ONLY, NOT READ, by Friday: parts 2 to 4. In them, 32 blocks carrying a `"case"` key, 32 distinct, none of the 32 CASE ids missing. Their contents are yours to judge with your own program, as you did for stage B.
- Scan of all four files for a Windows user-folder path with a real name: 0 (control: 31 `<PROFILE>` hits). The helper's own check: 0 lines in `out-B` holding the real profile path or the machine name.
- Both process lists (before, and one minute after the end) hold only the helper's own session: the same two processes started 2026-11-21, as in stage B. Compare them yourself by start time.
- The streams were not attached (text only); they stay in place under `C:\c2c\wgc2\out-B\raw_B\`. The first line of the probe case's stream is in part 1, whole: its tool list is the 25 names, no Bash, no Monitor, a PowerShell tool.

**Model runs of the owner's 70: 33 before this sitting, 32 in it, 65 in all** (Friday's sum of the three `CLAUDE INVOCATIONS` lines: 32, 1, 32; check it against your own record). No further model run is asked for or allowed on this lane: the grant ends with the test recorded.

## What Friday asks of you now
1. Record the sitting with the tags it earns (RAN ON PC, 2026-11-23, at `462faca`, work order 21, 32 model runs), placeholders as ruled, the originals' paths in the header. The configuration keeps its name, "Git present, no-Git tool list (look-alike)"; it is not written as "without Git" anywhere.
2. Re-judge the 32 returned cases with your own separate program, as for stage B, and give its whole output. If any case is unsupported by what was returned, say which and STOP with `STOP Q1` as your last line: do not write READY over it.
3. The two code wordings you listed under ADDENDUM 9 ("Not changed": the comment at `w1.py:141` and the header of `run.ps1`): leave them as they are. Changing a runner file after the sitting that used it would make the committed runner differ from the one that ran. One line in `RESULT.md` saying so is enough.
4. The stage table for STATUS that ADDENDUM 9 asked for (each stage, its work order, its commit, model runs, its last line, what it does and does not show; total of the 70).
5. Merge the then-current `origin/main` INTO your branch if it has moved (never rebase); at this moment it is still `3768a67d1d41b47439776657afbc114bd14bc439` by Friday's own ls-remote. Another lane (`allow-measure`) will append to `BACKLOG.md` and `docs/M0-OUTCOMES.md`; if it merges before you, keep both sides' lines.
6. Then your last line: `READY FOR QA W-GATE-TEST`, with the full head sha on the line above it. ONE independent check follows as its own seat; it will hold every RAN ON PC claim against the saved result files named in your record.

After ANY context compaction, re-read the brief, all addenda and your STATUS whole before writing anything more.
