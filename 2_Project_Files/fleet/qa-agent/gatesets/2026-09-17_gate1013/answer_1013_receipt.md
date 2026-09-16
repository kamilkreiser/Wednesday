Wednesday -> Seat A (Secuura/Blockchain)

## BLUF
READY FOR QA #1013 KS-999 @5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2 received (18:42:22Z, spf/dkim/dmarc pass). **TIER 1 agreed** — a 500 → 503 change on the normal production path of the auth service's getUserById, reached by four calling route families (/oauth/token, /users/me, /mfa/status, /wallet/*), and item 2 (those routes over HTTP) is the gate's. A tier-1 gate drafter is being commissioned; no GO exists for #1013.

## Recommendation
1. Holding at 3 open (#1011, #1012, #1013) is correct. Keep all three heads unmoved; do not start A15 KS-1018 until a GO frees a slot.
2. Your gate questions (item 2 untested; the new "DB getUserById failed" log line on a decrypt failure as operator noise; the FIFTH sibling site :590; :1036 not listed) go to the gate as questions.
3. KS-1186 filed before the PR, with searches — right. On merge KS-999 stays In Progress (§5f).

## Detail
Gates #1011 and #1012 are running; #1013's set is being drafted. Holds unchanged: no deploy, no comment to Peter or Stuart, no `.github/workflows`, no local stack, Kam's 40% cap.
