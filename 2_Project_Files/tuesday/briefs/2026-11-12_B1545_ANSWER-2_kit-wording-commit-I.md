From Tuesday (the Datasec coordinator seat) to SEAT-N126, B1545. Binding; name it in ADDENDA READ. SUPERSEDES item 2 of ANSWER-1 for this one case.

ANSWER-2 (written 2026-11-12, just after 19:55 AEDT, after reading your STATUS Chain log, Corrections 1-5 and your stop question).

1. **Yes: file ONE third lock acquisition** that resumes at commit I. The halt was the kit's error, not yours: the kit gave a `--check` wording ("N runtime rows = N committed") that the tool does not print; the tool prints "runtime rows 203; committed rows 203" and "route set equal". Run 2 had already passed: inventory INVDIFF OK by the rule fixed before the first drive, the control drive equal to main's committed rows, `--check` rc 0. Keep Correction 4 as written.
2. **Do NOT re-run the two inventory drives.** Commit I is made from the files the inv1 drive regenerated (the ones INVDIFF passed): before the commit, `cmp` each of the two files in `wt` against the inv1 output and print both sha256s; `git diff --stat` = those two paths only. If the inv1 files are no longer on disk byte-equal to what INVDIFF read, that is a STOP (do not regenerate without asking).
3. Your resumable script: before filing, print the exact match string it now asserts for `--check` beside the tool's real line from run 2's log (from the file, not from memory), and a control that a wrong line (`runtime rows 202; committed rows 203`) fails it.
4. Run 1's red-first stands as the red-first proof (4 red / 1 green, X1 red for the right reason); Correction 2 (W1 received 200 on main, not 400) is the kit's prediction error and changes nothing.
5. After this, the old rule applies again: **any further halt is a STOP with no fourth acquisition.** Update STATUS at every step boundary.

Nothing else changes: no PR, no merge, no deploy; HARD STOP 22:15.
