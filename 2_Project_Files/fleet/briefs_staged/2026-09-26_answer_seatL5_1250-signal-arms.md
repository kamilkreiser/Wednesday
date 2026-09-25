# ANSWER (Seat L5): #1250 = (a) ACCEPT AS BUILT, with four conditions; (b) the PTY goes to its own ticket. SUPERSEDES the signal-cell clause of the 17:1xZ FIX ROUNDS mail.

## BLUF
**(a) RULED.** Your two shell rules are correct and they make part of my relayed must-change list impossible: bash ignores SIGINT in an asynchronous job (so INT-to-pid cannot be asserted by any harness that backgrounds the runner), and a signal ignored on entry cannot be trapped (so inside the INT-ignoring hook no INT arm can exist). **That list was the gate's text relayed by Wednesday; the error of requiring an unreachable assertion is Wednesday's to own, not yours.** This mail SUPERSEDES the clause "add one regression cell per signal (TERM to pid, INT to pid, INT to group) asserting ..." in the FIX ROUNDS mail. Re-push #1250 now.

## The four conditions on (a) — each stated in the PR's Test Evidence
1. **An UNREACHABLE is a measurement, never a skip:** each INT arm's reachability probe must be shown able to answer YES — in a normal shell the INT-to-group arm reports `installable=yes` and ASSERTS all four properties (your 58/0 normal run). Quote both runs (normal shell, INT-ignoring parent) with their counts and the rule each UNREACHABLE names.
2. **Red-proof against your round-1 head, in a normal shell:** the TERM-to-pid arm and the INT-to-group arm each go RED on c78f4093fb53's runner (rc 0 / next suite runs / verdict printed) and GREEN on the round-2 runner. That is the property the gate's NO GO was about.
3. **The PR body states the environment matrix plainly:** which arms assert where (TERM: everywhere; INT-to-group: where INT is trappable, i.e. an interactive ^C; INT-to-pid: nowhere, bash rule 2), so the next gate grades against THIS ruling, not the superseded clause. Wednesday will carry this ruling into that gate's commission.
4. **The declared fleet count:** state the NEW `run_shell_suites` count at push time (you said 58/0) and that leg 14 is 60/60 under the hook.

## (b)
File ONE ticket after the READY (search first): "a PTY harness so SIGINT can be asserted for the runner in the foreground in both environments", Refs KS-1302, tier to be proposed. Not in this round.

## Order
Commit the reachability change → re-push #1250 (fast-forward, same PR; `Refs KS-1302` / `Refs KS-1303` as their own lines in the body) → READY FOR QA for #1250 and #1253 (both round 2 of 2; #1253 with `Refs KS-1297` on its own line) → then the non-blocking findings search for both. You do not need to read the whole report for the READYs; read its #1250 and #1253 sections before filing.

## Your wake
End a turn only with a push running or a named awaited mail.
