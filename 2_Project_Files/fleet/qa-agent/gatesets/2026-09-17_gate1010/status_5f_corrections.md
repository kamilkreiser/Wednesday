hits: 1
SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: #1010 no longer closes KS-1183; four runtime tickets moved back from Done
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-16T17:53:16.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
Seat A

## BLUF
- Item 2 done: #1010's body now reads "Refs KS-1183". attachmentsForURL(pull/1010) re-read at 17:52:22Z = KS-1183 contributes, KS-1087 contributes. Head unchanged c3213b04e3ad96068c367f7e0ba426822d32cda9; body read back == sent; 0 closing phrases (control fires).
- Item 3 done. Each ticket got the facts comment first; each state write was refused unless the ticket still read Done:
- KS-1165: Done -> In Progress, comment 49ee639b-8df1-4a4c-98cd-d6426f2b88ae
- KS-932: Done -> In Progress, comment 00c142ab-1911-458a-88dd-a5d22fe9b56d
- KS-1073: Done -> In Progress, comment 23461917-3a45-45de-8415-205aff63a96e
- KS-844: Done -> In Progress, comment c3b9f334-5a58-47f7-84bd-97c6814e638b
- KS-1130 left Done: #999 was tests + comments only.
- KS-1183 carries a correction comment (4628db7c-1b7f-47f6-8db7-efeed3f17ba0): my earlier "close it when #1010 merges" line is withdrawn.

## Recommendation
Nothing needed. The state for a merged runtime ticket is In Progress. No board state means "merged, not verified live":
- In Review is described "Pull request is being reviewed", i.e. the review queue.
- In Test has no description and has held 0 tickets, archived included, so its meaning is not established.
- Tested Not Deployed is a completed-type state, so Linear counts it closed; its 4 current tickets use it for "deploy owed".
So by your fallback, In Progress. The same state goes in every MERGED receipt from here.

## Detail
A12 KS-871 is built and committed locally at 0a1f8900c (base d067725ff), tamper-graded 8 rows, all as predicted, tsc rc 0. It pushes next, with "Part of KS-871" (no closing phrase), as a runtime-behaviour PR under 5f. #1010 unchanged otherwise. Holds unchanged, nothing deployed.

Seat A

