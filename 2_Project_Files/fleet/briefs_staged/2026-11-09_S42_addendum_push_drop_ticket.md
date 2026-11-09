Seat S 42nd

ADDENDUM: one filing, after its search (search the board first: 'rc 141', 'Broken pipe', 'closed by remote host', 'pre-push', 'push driver'; if a ticket holds it, a facts-only comment instead, as you did for KS-1847).

What: a push holds its SSH session to GitHub through the whole 17-20 minute pre-push hook (git opens the connection before the hook runs), and the remote has closed it three times: 2026-11-06 (one seat), 2026-11-09 Seat T 19th's D5 (rc 141, 1224 s, a local socket error inside leg 14), 2026-11-09 Seat T 20th's E1 (rc 141 after 1205 s, 'Connection to github.com closed by remote host' / 'client_loop: send disconnect: Broken pipe', after the hook's verdict). The seats' push driver already sends SSH keep-alives every 15 s (tools/pushlock_*_v3.sh line 55, by Seat T 20th's read), so keep-alives do not prevent it; GitHub's reason is UNMEASURED. Cost per drop: a full hook run and a queue turn. NOT options (state them as ruled out): --no-verify; running the hook first and pushing after (both move the hook out of its place in the push).

Board account, Backlog, Low (tooling, no product effect), facts only, no exploit-shaped content. Evidence pointers by seat record path: Seat T 20th evidence/e1/push/real/push.out lines 2860-2861; Seat T 19th evidence/d5/push/real. New key back in your STATUS.

Wednesday
