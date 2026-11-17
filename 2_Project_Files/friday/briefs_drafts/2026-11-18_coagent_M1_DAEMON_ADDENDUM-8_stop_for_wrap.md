This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It stops your work for today at a safe point. It changes no rule of your brief or earlier addenda.

# M1_DAEMON — ADDENDUM-8: stop for the wrap

Kam, live board, 2026-11-18 09:53, verbatim: "lets wrap up now and we can do the test during the next session". So the final test runs wait for the next session. Do this now, in order:

1. Stop your own running test processes (only your own; name them in STATUS). Keep every log where it is.
2. Commit anything uncommitted that belongs to your work (if a file is half-edited, finish or revert that one edit first; say which). Push the branch `m1-daemon`: never force, never rebase. Record `git status` (clean), the head SHA and the output of `git ls-remote origin m1-daemon`: local and remote must be equal.
3. In `coagent/5_Project_History/STATUS_M1_DAEMON.md` write a short section "STOPPED FOR WRAP" that says exactly: what is done and pushed; which runs were in flight and how far each had got (a run that did not finish counts as NOT run); what remains before your READY line: addendum 5 section 3 (the runner end to end, then item 3 from the beginning); anything you know that the next seat would otherwise have to rediscover.
4. The last line of that file, exactly: `STOPPED FOR WRAP M1_DAEMON at <head SHA>`. Do NOT write `READY FOR QA M1-DAEMON r4`: the remaining runs are not done.
5. Then stop. Start nothing else.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
