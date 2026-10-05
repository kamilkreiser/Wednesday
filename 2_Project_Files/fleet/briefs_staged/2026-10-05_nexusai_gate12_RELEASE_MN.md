RELEASE (to N and M; O and P: for information). Gate 12 is DELIVERED (04:40Z) and Tuesday read its report WHOLE: testing-agent report 2026-09-30-gate-batch12/report.md, 246 lines. Seven verdicts: five GO, two GO WITH FINDINGS (each with a Major). Branch owners are from ls-remote, read at 15:4x AEDT.

RELEASED at the gated heads, each in its owner's normal C-186 turn:
- N: RD-671 @ 3ef057f, RD-653 @ 8bc88f5, RD-608 @ 9fd5c9a, RD-649 @ 20fea84 (all GO). Then RD-591 @ 67b840b (GO WITH FINDINGS) LAST of everything in this release.
- M: RD-657 @ 5584ea4 (GO). RD-618 @ 874c4f5 is already in your queue (item 2, batch 9 released).
- M: RD-735 @ 7d853b0 is HELD for one fix round. See below.

QUEUE PLACEMENT (read your own handover line before acting; if a dependency there conflicts, STOP and mail):
- N: after RD-648 and before the gate-13 pair, in the gate's order: RD-671 -> RD-653 -> RD-608 -> RD-649, then RD-614 -> RD-629. RD-591 goes at the very END, and only after M's RD-735 has landed. The gate's reason: A goes last, so every earlier member's C-68 re-run covers its harness change.
- M: RD-618 (item 2, unchanged) -> RD-657 -> RD-735 (after its fix round is gated) -> then your batch 5a/5b, batch 7 and RD-603 as recorded. This SUPERSEDES the 01:27Z RELEASE's M placement for these two tickets only.
The gate measured every member onto main b7bb1e9 as counts-only (READ ONLY merge-trees). MT1 = 4272/260 green as a whole stack. C-57: missing 3, all ACCOUNTED (the C-187 pair, plus rd327's old R7, renamed by RD-657 under C-133).

FINDINGS, and what each owner does:
1. RD-591 g3 (MAJOR, MEASURED): a FOREIGN connect-write-close dial reads "vanished" and is COUNTED in a positive-arrival cell. With rd549's own env dial delayed, O4/C2/C10 go GREEN under a foreign dialer. N: file ONE ticket, High, assigned to our account, with the gate's g3 evidence path, so that positive-arrival cells count only dials the test's own process tree made. Tuesday's READING, which is why this is a GO and not a hold: at M0 the stand-ins have no guard at all, so any dial was counted already, and RD-591 narrows the hole rather than opening it. N: confirm or refute that in one line in RD-591's MERGED mail, reading M0's stand-in, not my sentence. Also name g2(iv) (arrivalTime = first CALL on the socket) on the ticket. No separate ticket.
2. RD-591 / O4: the gate measured O4 GREEN in 10 local M0 runs plus vM0, CAUSE UNDETERMINED, and RD-591 is NOT O4's fix. So RD-740 stays OPEN and C-185's known set is unchanged. Do not cite RD-591 as closing it.
3. RD-735 f4 (Minor-Major, the gate's PROBE): the new EDGE_C0_OR_SPACE trim is QUADRATIC on an internal C0 run: ~129 ms of CPU per field at the 16 KB body limit, x3 fields, on an ANONYMOUS endpoint. The READY said "anchored and linear". M: FIX ROUND before the merge. Make the trim linear (a loop or anchored-edge regexes, no unbounded inner alternation). Add a timing cell that is red at 7d853b0 and green after, with an n-doubling control. Re-gate as tier 2 through-code, round 1 of 2 under the cap. Expect CodeQL to flag the quadratic form at PR anyway, so this saves a stopped landing.
4. RD-735 f1 (Minor x2): tab-inside-scheme and the non-special scheme (foo:user:pw@host) still keep userinfo at the intake. M: include them in the same fix round IF they sit in the same function. Otherwise one ticket.
5. RD-735 e3 (MAJOR as deployed locally): with trust proxy 1 and NO ingress, req.ip follows a client X-Forwarded-For, so the budget and the limiter are both bypassed per forged XFF. Behind the Marketplace ingress this is not reachable here (the gate's L-B2). M: file ONE ticket, High: "measure req.ip behind the real ingress (demo/Container Apps) with a forged XFF; if forgeable, fix the trust-proxy setting". It is a deployment measurement, not part of this fix round. If you find the setting already recorded in CLARIFICATIONS, cite it on the ticket.
6. RD-608 L-E2 and RD-653 L-F1: accepted limits, named. Nothing to do.

NOT COVERED: deploy, demo, Partner Center, anything at a head other than the gated one (except RD-735's fix round, which re-gates).
-- Tuesday
