# Drafter notes, Seat C 43rd billing catches, 2026-11-16 09:0x AEDT
Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatC43_billing_unclassified_catches.md (STAMP blank).
Develop dee28f4be27b (unmoved 08:55-08:59). Scratch: _work/ (copies of billing.ts, stripeService.ts, 25 tests, open_prs.tsv, pr_files.tsv, lin_*.txt).
Findings: (1) no existing ticket owns the 7 routes (KS-2219 = by-email only, PR 2246 merged; KS-1888 F4 "recorded, no ticket" = the five lookup routes' 404-on-outage; KS-593/KS-445/KS-431 do not name them). Seat files ONE ticket. lin.py has no create; S 84th's file_ticket_s84.py does.
(2) Reachability reading: getCustomer/getInvoice swallow all errors, so five routes reach their catch only via keyless getStripeService throw (and listPurchases/listInvoices for 4,5); bundle and admin reach it on any provider throw. Cells split K/D/L; class L (F4) measured with the real service, not fixed.
(3) Admin 403 returns before provider work: catch cannot hide authz by reading; cell A-G1 proves it. Tier 2, flagged.
(4) 61 open PRs, 0 touch billing/src (only package.json in 575, 649); B188/K36 queues clear.
Brief ~35 KB. Nothing was run.
UNMEASURED: every suite/red label (readings), OpenAPI declared responses for the 7 ops, CreditLockUnavailableError message vs classifier regex, limit-cast behaviour, whether file_ticket_s84.py runs unchanged, docs-fragment requirement at the seat's pin.
