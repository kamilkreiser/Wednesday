This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-25_coagent_QA-SCANNER-NEXT_check_brief.md`. Seat QA-SCANNER-NEXT only.

# QA-SCANNER-NEXT ADDENDUM 1: do not wait for a heavy-run slot for the scanner red script

Your status line says you are waiting for a heavy-run slot (count 3) to run the red script once. The brief's heavy-run rule applies to a run of yours OVER FIVE MINUTES. The scanner red script is not one: the builder's run of it took about a minute (its STATUS section 5: 15:47 to 15:48), and the brief says so in section 2. The three heavy jobs you count are two of Friday's merge checks and another seat's long test run, and they will hold the counter at 3 for an hour or more.

So: run `bash scripts/red-controls-scanner.sh` now, once, from your clone's root, with its target, log and scratch variables pointed into your work dir, whatever the counter reads. If it has not finished after ten minutes, stop it, say so in your verdict's NOT checked table, and finish without it. Everything else in the brief stands. Then write your verdict.

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
