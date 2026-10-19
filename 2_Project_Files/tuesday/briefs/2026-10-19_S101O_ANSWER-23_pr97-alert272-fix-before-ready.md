BLUF: PR #97 (RD-774 + RD-836) has ONE open CodeQL alert at its head 360cd82: #272 js/log-injection, rule severity ERROR (security medium), backend/server.js:20945, "Log entry depends on a user-provided value", created 2026-10-19T01:42:52Z (Tuesday's gh read, 14:5x AEDT). Under C-190's ADDENDUM ("alerts_threshold = errors, so ANY new alert whose RULE severity is error blocks") it blocks the land. Fix it IN CODE before you send READY FOR QA. Never dismiss it.

Why now: Kam forwarded GitHub's code-scanning comments on PR #96 and PR #97 to Tuesday (DKIM pass, "FYI"). PR #96 is clean at f15217c (0 open; the comment was about fd8ff2a's six alerts, already fixed). PR #97 is not.

What Tuesday asks (your design; this is the shape, not the code):
1. Read the line and its data path first: what user-provided value reaches the log at :20945, and whether it is one RD-774/836 added or moved.
2. Route it through the repo's existing log sanitiser (the logSafe helper that RD-801 changed to remove control characters on main), not a new hand-rolled escape. If logSafe does not fit this call, say why in the READY.
3. Red-first: a cell that fails with the raw value logged (a CR/LF or ANSI sequence in the request field reaches the log line) and passes with the fix; restore byte-equal.
4. Push, then read CodeQL on the NEW head: every Analyze completed, 0 open alerts on refs/pull/97/head, with your PR #58 control, and #272's instance on the PR ref = fixed.
5. Only then send READY FOR QA with the alert section (numbers, before/after).

Nothing else changes: ANSWER-21's rulings stand (P1 (ii), P2 ticket), tier-1 gate before any merge, no land without Tuesday's GO, nothing else lands on main.

-- Tuesday
