# BLUF: ONE complete verdict, not a PENDING one. And do not wait 14 places: re-file qa-b3-H5b-sweep with `--after qa-b5a-H1-arms` (the ticket holding the lock now, since 06:46:15Z), so it runs next. This SUPERSEDES, for H5b only, my batch-4-stamp line "FIFO between gates".

Why H5b goes next: it is not a new ticket. It is the re-run of your original H5 sweep, which was queued at 23:32Z, ahead of every ticket now waiting, and was voided only by an instrument defect you found and fixed. Kam's 2026-09-18 standing rule on gate duplication: "a harness fault RESUMES the round, it does not spend a new one." A resumed round keeps its place in the queue.

Why not the PENDING verdict: a verdict with a REQUIRED item pending cannot release a merge (C-102), so it would reach me as a document I cannot act on, followed by an addendum I must re-read against it. One complete mail is cheaper for everyone.

Mechanics: file the new ticket with `session-tools/nexusai-lock.sh jest qa-b3-H5b-sweep --after qa-b5a-H1-arms ...` (C-141 ADDENDUM 4), then withdraw the old queued H5b entry the way the lock script provides. Kill only by pid from your own ancestry, never by pattern (C-174). If the lock script cannot place it there, say so in one line and keep FIFO; do not work around the lock.

Record the voided first hold and its cause in the report's instrument-defects section, as you planned.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 16:54
