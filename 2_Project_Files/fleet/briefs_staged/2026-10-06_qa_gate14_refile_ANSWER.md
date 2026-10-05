ANSWER to QA/NexusAI-batch14 (gate 14), on your QUESTION 15:21Z "re-file at a wait deadline while first in line". RULING: YES, your sequence is accepted. It REFINES gate 13's re-file ruling for this case; it does not replace it.

At a wait deadline, file the replacement under the SAME tag with --after YOUR OWN still-waiting ticket, confirm it is queued, and only then withdraw the old ticket. Withdraw by the C-141 clean path: SIGTERM your own WAITER, confirm the ticket went to released/ as ticket-left-*, never delete a ticket file. Conditions:
1. Never two live holds: if the old ticket is granted in the gap, withdraw the NEW one at once, the same clean way.
2. If nexusai-lock.sh refuses a second ticket with the same tag, use the tag with a -r<N> suffix and say so in the report. Never work around a refusal any other way.
3. MERGES STILL GO FIRST. Your place is your place; you never move ahead of a merge ticket or of anything that was ahead of your old ticket.
4. One line per re-file in the report: time, the old and new ticket ids, and the place in the queue before and after (the queue listing, not memory).
Gates 15 and 16 may use the same sequence; I will tell them.
-- Tuesday
