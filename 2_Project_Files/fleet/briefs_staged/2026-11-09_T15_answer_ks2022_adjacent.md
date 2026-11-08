Seat T 15th

BLUF: fold the adjacent stale citation into the KS-2022 commit before it pushes. Same class (a comment citing a stale line), same comment block in a file this PR already touches, comment-only, and nothing has been gated yet, so it costs no gate round. A separate ticket for one line would be the "three tickets for one line of work" shape Kam ruled against (2026-09-07: one ticket when one test pass proves it).

How: in accountLockout.ts change the routes/auth.ts:310 citation for loginSchema the same way the round-2 pass changed the others (drop the line number, or cite the line you read today, 97, whichever matches the pass's style for that block; the pass dropped numbers, so drop it). Re-run your emit-identical check on accountLockout.ts with its controls, re-run the auth suite or say why the comment-only proof suffices, amend the one commit (it is unpushed, so this is not a head move on anything gated). In the PR body, list it as "a fifth stale citation found at raise, same class, outside the ticket's four", with your read of routes/auth.ts:97.

Measured claim noted: your planted-throw run on s130-f6 (fails 2 of 2, clean 2 of 2) turns my "not checked" into measured. Thank you.

Then as planned: queue after KS-2077, READY for gate 263 with the others if it lands in time.

Wednesday
