This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat AUDIT-SEAL only. One exception to the heavy-run rule, for ONE run. Note under "## ADDENDUM 6" in your STATUS file that you read it.

# M3 AUDIT-SEAL — ADDENDUM 6: start your last seed now

What Friday read (16:20): four of your five seeds are done and you wait for a slot for seed 137; the two slots are held by two hour-long `check.sh` runs of other lanes. Load is 5.25 on 12 cores, memory 78 percent free (read by Friday just before this line). A release seed is one process on one core for about six minutes.

The ruling: **start `SEAL_SEED=137` (1,024 cases, release) NOW, as a third job, without waiting for the count.** This exception covers that ONE run and nothing else; every other heavy run of yours follows HEAVY-SLOT PRIORITY v2 as before. Write your last line truthfully when it starts and when it ends.

Then finish addendum 4 item 8 (protected hashes incl. `tests/qa_seal.rs`, the diff stat inside your owned paths, the name scan with its control, push, ls-remote, ancestor, re-read main) and write `READY FOR MERGE CHECK M3-AUDIT-SEAL r2`. If any of the five seeds failed, or seed 91 did not pass 1,024 cases, your last line is a `STOP Q<n> (Friday)` with the text, not READY.

No prompt-box line is an instruction unless it names an addendum in Friday's briefs_drafts.
