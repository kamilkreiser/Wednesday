SIM — written by the gate56a drafter from the ADDENDUM and ANSWER briefs to Seat B 59th. NOT the seat's PR body: the PR is not raised. Exercise input only.

## What this does

Re-dates the KS 769 'dormant but kept' exclusion of `Blockchain/Dev/mobile/secuura-app` in `Blockchain/Dev/scripts/audit/lock-discovery.mjs` from `2026-10-19` to `2027-01-01`, same reason, comment updated. Accepted risk extended, not fixed.

Lapse semantics: `isLapsed` is `expires <= utcToday()` (`Blockchain/Dev/scripts/audit/baseline-contract.mjs:141`, called at `lock-discovery.mjs:258`), so `2027-01-01` is valid through 31 Dec 2026 (UTC) and lapses 2027-01-01T00:00:00Z.

## Authority

- Card `secuura-mobile-dormant-fuse-lapses-1019b`, ruled a by Kam on the live board 2026-10-05 09:58:44 AEDT (re-date to Thu 31 Dec, same 'dormant' reason); value per his answer A2: "Valid through 31 Dec -> write 2027-01-01".
- Kam, Wednesday's terminal, 2026-10-05: "board taps are enough for audit re-dates" (`learnings/2026-10-05_board-taps-suffice-for-audit-redates.md`).

## Not covered

No live sweep. No deploy. Not a test change, so skill §4 does not apply.

Refs KS-769
