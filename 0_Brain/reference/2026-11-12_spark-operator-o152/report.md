# o152 report (saved by Wednesday; the operator's Write was refused, text returned in its result)

ROUND NOT RUN: STOP at pre-check 2 (the ticket leaves the fix a choice). No PASS/FAIL, no held READY.

1. Tunnel + pin PASS: tunnel UP (127.0.0.1:47788/v1/models 200); ls-remote develop d0e58f55c861f12b31e072ea39332324da8dcb23; load1 ~5.0.
2. Linear FAIL = a DECISION: KS-1573 Backlog, 0 comments; body says "Facts only, no fix" and ends "Not decided here: Whether to delete the forward (one line, plus the pin test flipped) or leave it." Facts agree with S 61st (originate 0 reads of x-wallet-address; control x-user-id in metering.ts). The ticket ALSO names services/referral/src/routes/referrals.ts:55 as a non-test reader of the header (KS-1223 changes it), and ks1041-vouch-header-strip.test.ts:113 pins the header as NOT stripped at the gateway edge. Ticket line 1383 is an older develop; 986 not re-measured by the operator (S 61st's number). KS-1223's comments UNREAD (team-scoped query returned only KS-1573; an unscoped number filter matched PS-1223, another team: Done-ness unconfirmed by the operator).
3. Re-measure: NOT RUN. 4. Exclusions: NOT RUN.

To proceed: a ruling that KS-1573 = delete the forward (a tier-1 gateway header path). Pre-check 3 must then settle the referral reader at referrals.ts:55 (the commission treats any reader other than originate as a STOP).

No push, PR, comment, mail or Linear write; no cd; nothing deleted; Secuura checkout saw only ls-remote. Scratch: scratch/lin.py (+ .bak), linear.txt (mixed teams), linear_ks.txt.
