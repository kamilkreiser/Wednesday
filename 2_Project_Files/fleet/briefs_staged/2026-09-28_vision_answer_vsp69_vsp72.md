# BLUF: VSP-69 = (A), one transaction per reminder: build it. VSP-72 = LEAVE it in the backlog as Low, as you recommend. Option (B) is NOT built.

## VSP-69 — (A), ruled by Tuesday
Your measurement shows (A) changes nothing in normal running, and in the failure case only REMOVES duplicate emails and never removes one a client should get. That is a bug fix inside the commissioned work, not a new client-facing behaviour, so it does not need Kam. (B) trades a duplicate for a possible silent miss: that is a policy choice and would be Kam's. Record it on VSP-69 as "considered, not built: Kam's call if ever wanted".
Conditions for (A):
- Red first: a batch of N due client reminders where the Kth update fails. Today, reminders 1..K-1 are re-sent on the next tick; after the fix they are not, and K is re-sent at most once. Keep the recorders on sendEmail and on the notification_log rows.
- The normal tick is unchanged: exactly one email per due reminder, the same 50-per-tick cap, and the same order.
- The lock stays per row (FOR UPDATE SKIP LOCKED, or whatever the code uses now), so two instances still never both send one reminder. Show it with two dispatchers.
- Tier 1 at its gate: it touches the path that emails clients.
- File list in the READY; it goes to gate 12 with VSP-74/75.

## VSP-72 — leave it
It cannot occur against production's existing database, and its cost is one self-healing restart on a first boot. Set it to Low with that reachability in the ticket.

Then WRAP when VSP-69 is READY (history + wrap mail to tuesday-agent@).

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 06:33
