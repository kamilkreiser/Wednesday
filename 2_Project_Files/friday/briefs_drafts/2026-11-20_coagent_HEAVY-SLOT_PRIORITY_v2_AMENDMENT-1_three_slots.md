This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is for every seat that still has heavy runs to do (today: RELAY-RECONNECT; any seat given a notes round later). It AMENDS `2026-11-20_coagent_HEAVY-SLOT_PRIORITY_v2.md` in ONE number and changes nothing else in it. Note under "## HEAVY-SLOT v2 AMENDMENT 1" in your STATUS file that you read it.

# Heavy-run slots: THREE at once, from now

What Friday measured today: three heavy jobs ran together for about a quarter of an hour (15:47 to 16:05) at load 8.4 on 12 cores with 78 percent of memory free, and both hour-long checks in that window passed with no failed test. At 16:49, with two checks running, the load was 2.9.

The amendment: wherever your brief, an addendum or version 2 says "at 2 or more, wait", read **"at 3 or more, wait"**. You may start a heavy run when the job count is 0, 1 or 2 and no seat above you in version 2's order shows `WAITING FOR A HEAVY SLOT`. Everything else in version 2 stands: the order, the marker, no chaining (each next run goes through both checks again), one heavy run of your OWN at a time.

If a test fails in a run that overlapped two other heavy jobs, say so beside the failure (which jobs, from the process list) and re-run that one target alone before you treat it as a real failure; record both results.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
