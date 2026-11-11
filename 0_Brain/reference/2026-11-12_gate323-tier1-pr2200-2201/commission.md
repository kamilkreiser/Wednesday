# Gate 323, TIER 1 (Opus; routing v1.0 tier-1 row: auth route log content + six tokenisation route catches = security-surface error handling). Seat R 104th's batched READY: PR 2201 (KS-1873) and PR 2200 (KS-1868 rows 32+34). Commissioned 2026-11-12 ~10:4x AEDT by the 10:0x Wednesday seat.

Method: copy-and-change of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate321-tier1-pr2197-2198/commission.md (a tier-1 two-PR KS-1868 gate: read it WHOLE; its Constraints, output shape, controls and Spark-shadow step all apply). Calibration: gate 321's verdict.md.

Pins (R 104th's ls-remote 23:41:56Z; RE-READ at start and end): develop d35f75875275158ce3b20b636b4198a4c8834968; refs/pull/2201/head 50c32501e60c4400a37fa2f3bb2be58815666806; refs/pull/2200/head 911af60042753b957dce171d92f14e11c3a21514; PR 2075 head 32aa0d06bc0aceccb790443bbf16384ff0c8e930. Both branches were cut on c78c80bd5370; merge-tree onto d35f75875275.

READY (read whole; reproduce, do not trust): ready_r104_2200_2201_mail.txt in THIS folder.

Questions:
1. PR 2201 (users.ts:678 logs userId instead of email): does the admin create-user log line now carry no email (and no other PII) on every path through that handler? Are the four new cells red on develop by assertion and green on the head? Is user.id always defined at that line (a create that fails before the id exists)?
2. PR 2201 x PR 2075 (open, same file, hunk @@ -835): reproduce git merge-file both orders, 0 conflicts, byte-identical, planted overlap conflicts; and say whether the merged result still compiles and the two changes interact (same handler or not).
3. PR 2200 (six tokenisation route catches): for each of tokenise, detokenise, hash-key, generate-key, rotate-key, detect-pii: does a thrown value whose message cannot be read now produce the guarded log/response instead of hanging or throwing, and does any response or log now carry a token, a key, PII or the thrown object? The READY says the 400 body still echoes the caught message: is that a leak on any route (what can the message contain)?
4. The 18 cells: red on develop by assertion, green on the head; one deliberate mutant per route must turn its cell red.
5. Tier check: does either PR change behaviour a client can see (status, body)? Name it as a GO sentence if so.
6. Census on the touched paths (GraphQL, with a control).

Note for the gate: the services/auth whole-suite rc is NOT a pass signal (G321-PRE-1: the seedDemoUsers timer can make it exit rc 1 with all green); read counts.

Spark shadow after your verdict: run spark_gate.sh / spark_review.py with --pr-body-file, in the session scratchpad.

OUTPUT: verdict.md in THIS folder. Line 1: 'PR 2201: GO / GO WITH NOTES / NO GO (at head ...; tier 1)'; line 2 the same for PR 2200. Findings G323-<PR>-N, graded. NOT TESTED. The Spark shadow result. If your Write is refused, return the text in full.

Constraints: exactly gate 321's. DevMASTER has dropped four times today (enclosure power). If it drops, wait, re-read what you wrote, then resume.
