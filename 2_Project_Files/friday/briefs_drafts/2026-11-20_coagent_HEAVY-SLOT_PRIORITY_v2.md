This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It is for ALL FOUR seats: AUDIT-SEAL, POLICY-MODE, ROSTER-SETTLE, RELAY-RECONNECT. It SUPERSEDES `2026-11-20_coagent_HEAVY-SLOT_PRIORITY_addendum.md` (withdrawn by name: stop following that file from the moment you read this one). It changes only how heavy runs take turns. Record under "## HEAVY-SLOT PRIORITY v2" in your own STATUS file that you read it.

# Heavy-run slots, version 2: one order, one marker, no chaining past a waiting seat

Why: the first version protected one seat only. Since then a seat that needs ONE run to be ready has waited from 13:41 while another seat started its runs back to back, each within seconds of the last (Friday read both STATUS lines and the process list at 14:13).

## The order (highest first)
1. AUDIT-SEAL   (`STATUS_M3_AUDIT_SEAL.md`)
2. POLICY-MODE  (`STATUS_POLICY_MODE.md`)
3. ROSTER-SETTLE (`STATUS_ROSTER_SETTLE.md`)
4. RELAY-RECONNECT (`STATUS_RELAY_RECONNECT.md`)
All four files are in `coagent/5_Project_History/`.

## The marker
While you are blocked waiting for a heavy slot, your LAST LINE contains exactly these words, in capitals: `WAITING FOR A HEAVY SLOT`. For example: `IN PROGRESS: (HH:MM) WAITING FOR A HEAVY SLOT for check.sh on <head>`. The marker is in your last line ONLY while you are blocked, never while a heavy run of yours is going and never when you have nothing queued. The script that starts or ends your run changes the line in the same step (not only your next turn). Refresh the time at least every 20 minutes.

## The rule, before you START any heavy run (as your brief defines one)
1. Do your brief's job count. If it does not allow a start: write the marker and wait; look again every 2 minutes.
2. If the count allows a start: read the last non-empty line of the STATUS file of EVERY seat above you in the order. If any of them contains `WAITING FOR A HEAVY SLOT` (match without regard to case), do NOT start: that seat goes first. Keep your own marker and look again every 2 minutes.
3. No chaining: when one heavy run of yours ends, the next one is a new start and goes through 1 and 2 again. A queue script that starts the next run by itself must do both checks itself.
4. A run of yours that is already going is never stopped for this rule.
5. This is not a reason to idle: tests, code and docs go on; only heavy runs wait.
6. If you have waited on the same higher seat for 90 minutes: last line `STOP Q<n> (coordinator): heavy slot not freed by <seat> for 90 minutes`.

## Right now
- AUDIT-SEAL: nothing changes for you except the marker (use it in place of "heavy count at") and item 3.
- POLICY-MODE: rewrite your last line with the marker now; you are next for the first free slot.
- ROSTER-SETTLE: your running check.sh goes on; when it ends, your runners wait while POLICY-MODE or AUDIT-SEAL shows the marker.
- RELAY-RECONNECT: you are last in the order; your two base runs and later your final runs wait for any of the three above that shows the marker.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
