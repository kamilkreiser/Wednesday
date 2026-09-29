# gate47 DRAFTED TICKET TEXTS — VERBATIM from Seat B 46th's READY (13:58:06Z), HELD, NOT POSTED

Extracted 2026-09-29T14:14:25Z by drafts_gate47.py from mail_gate47_ready.md (the CLAIM block). The READY as captured == the seat's record /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-29_seatB-46th/mail/READY-gate47.txt: True.

Each text is the `> `-quoted block with the `> ` prefix removed; markdown emphasis is kept as the seat wrote it. The gate returns each as POST AS-IS / POST AMENDED (with the amended text) / DO NOT POST, after checking every factual claim as a ROW with evidence. Nothing is posted by anyone until the gate has read it (STANDING_LINES :352).

## KS-1374 — KS-1374 checklist tick (#1349)
- TEXT_SHA256: fe7ba98c45550129a63201f5ae1be32fa0dad9f1032ac4eda0bd403d26e482b9
- 555 chars, 6 lines

```
- [x] **N-1347-11 — the residue of the target-keyed pacing.** Closed by PR #1349
(`daab8ff3bff5`): `isLocalScanTarget()` now keys on `OVERRIDE_APP_URL || SECUURA_API_URL`, the
same precedence `scanOptions.ts:98` uses for the host the scan attacks. A scan aimed at a remote
stack through `OVERRIDE_APP_URL` alone paced at 7500/min and now paces at 1500; a local override
still paces at 7500. Unit-proven (9 cells, 4 red-first, 5 controls, one tamper arm); no Akto scan
was run against any stack, and the demo's own `RATE_LIMIT_MAX_REQUESTS` remains unread.
```

## KS-1054 — KS-1054 facts comment (N-1348-9 + #1350)
- TEXT_SHA256: 3a5227e14526fad89b5ac0241d81cc181ada6e61ac785a7411ccacda0cfeeade
- 595 chars, 7 lines

```
Merged `a72149a1a803d802430568254e7fa9afa7029321` (PR #1348, round-2 head
`94e31db501cd01aaec7437418d7efbb592b1b59a`): `deploy.sh` now exits non-zero when post-deploy
verification counts issues. Comment `b82bebb3` named the round-1 head `1bb58b4ebb97`, whose red
proof was blind to the return value and red on GNU; its claims hold of the round-2 head.
Follow-up PR #1350 (`8f4f0ef14963`) gives the predicate a third exit code so a check that did not
run stops printing a pass line, and folds in the two gate findings against #1348's test file.
Offline gates green; **live sweep owed**; not Done.
```

