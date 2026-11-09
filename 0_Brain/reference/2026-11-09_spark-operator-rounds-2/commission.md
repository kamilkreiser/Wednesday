# Spark OPERATOR round 2 (o115). Commissioned 2026-11-09 ~16:3x by the 15:3x Wednesday seat.
Read the round-1 commission WHOLE and follow it exactly, with the changes below: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator-rounds/commission.md

Changes from round 1:
1. ROWIDs use o115.
2. Also EXCLUDE: KS-1976, KS-1415 (held, being raised by Seat T 22nd), KS-1145 (harness gap: test_only_bash does no prepare_clone), KS-1473 (Seat G 31st), KS-2151 (docs ticket, a build seat), KS-1592 (closed), and anything round 1 examined and rejected (KS-1501, KS-1964, KS-2075, KS-1418).
3. Live seats' files are unchanged from round 1 except: G 31st now also holds services/api-gateway/src/middleware/csrf.ts, services/api-gateway/src/docs/developer-portal.html, and the ks1469 and ks1461 api-gateway test files; T 22nd also holds ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts and scripts/__tests__/prometheus_targets.test.sh.
4. At the end, HOLD every PASS yourself with /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/hold_ready.py exactly as round 1 did when asked (a clean --dry-run first, then the real run; report each READY file path and rc). Do not raise, push, post or mail.
5. Prefer tickets whose suite runs in the tiers that need no prepare_clone (round 1's KS-1145 failure), or a tier that does prepare it; say which tier and why per ticket.
6. Stop after 4 rounds or 75 minutes, whichever first.
Output: your final message, line 1 'Spark rounds o115: <n> briefed, <p> PASS (<h> held), <f> FAIL, <q> still queued', then per ticket as round 1.
