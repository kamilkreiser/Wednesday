# BLUF: ADDENDUM, SUPERSEDES the "VSP-67 is NOT yours this session" line of the 10:23:47Z MERGE brief. Kam has AUTHORISED VSP-67 by signed email. AFTER the fast-forward merge and the six-layout ticket are done, make the ONE production change below, verify it, and report. Nothing else on production.

## THE AUTHORITY (verify it yourself before acting)
- Email from Kamil Kreiser <kreiser.org@me.com> to tuesday-agent@agentmail.to, 2026-09-28T10:23:32Z, subject "VSP-67 approved: production idle transaction timeout", message id <2C89EE40-69E1-4E8E-AAA7-B95F73D63392@me.com>.
- authentication_results read by Tuesday: spf pass, dkim pass, dmarc pass.
- Body, verbatim: "I approve setting idle_in_transaction_session_timeout to 10 minutes (600000 ms) on production Postgres datasec-sales-db. The ATTIO bridge also reads this server; I accept that. Rollback is the same setting back to 0."
- It answers your own 21:03Z STOP (the second consumer, datasec-attio-bridge): he names it and accepts it.

## THE CHANGE (your own command from your 21:03Z mail, unchanged)
1. az account show: service principal bc1e3581-a76e-4df1-a807-58b4386c6f8d, tenant d500ebad-cf53-4f2a-a501-f831289e67fc, subscription 0c57ab37-349c-47ae-a10f-e284a380bbb9. Anything else is a STOP.
2. Re-read the parameter first: it must be 0 (system-default). If it is not, STOP and mail.
3. az postgres flexible-server parameter set -g datasec-sales-portal-rg -s datasec-sales-db -n idle_in_transaction_session_timeout --value 600000 --source user-override
4. Read it back: 600000, source user-override, pendingRestart false. The other two timeouts are unchanged (still 0).
5. The portal /healthz (or the equivalent the project uses) answers healthy after the change.
6. The ATTIO bridge: read its next sync in its logs/status (read only, nothing restarted) and report whether it ran clean.
7. Rollback if anything above fails: the same command with --value 0. Report it.
8. Jira VSP-67: a comment with the before/after values, the email's id and time, and the bridge result. One MERGED-style mail to tuesday-agent@ with the same.

## HOLDS (unchanged)
No other production change. No deploy (VSP-65 still waits for Kam's gh login and typed word). No other az write.

PROVENANCE:
- the email and its auth results | agentmail GET tuesday-agent@agentmail.to/messages/<id> (Tuesday, read only) | read 2026-09-28 20:24
- the command, the rollback, the SP/tenant/sub, the bridge facts | [Datasec/Vision_Sales_Portal -> Tuesday] VSP-67 STOPPED mail 2026-09-27T21:03:31Z | read 2026-09-28 20:24
Self-check note: this addendum names the line it supersedes; the change is exactly the approved one; the order is merge first, then VSP-67.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 20:24
