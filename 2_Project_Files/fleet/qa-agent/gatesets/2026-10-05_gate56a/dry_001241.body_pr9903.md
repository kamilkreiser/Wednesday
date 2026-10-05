SIM — written by the gate56a drafter from the ADDENDUM and ANSWER briefs to Seat B 59th. NOT the seat's PR body: the PR is not raised. Exercise input only.

## What this does

Re-dates the two react-router rows of `Blockchain/Dev/scripts/audit/audit-baseline.json` (GHSA-wrjc-x8rr-h8h6, GHSA-337j-9hxr-rhxg) from `2026-10-09` to `2026-10-31`. Nothing else in the file changes. Accepted risk extended, not fixed: the v7 migration (KS 528's real fix) is separate work.

Lapse semantics: `isLapsed` is `expires <= today` (`Blockchain/Dev/scripts/audit/baseline-contract.mjs:141`), so `2026-10-31` is valid through 30 Oct (UTC) and lapses 2026-10-31T00:00:00Z.

## Authority

- Card `secuura-fuse-1009-measured-1001`, ruled a by Kam 2026-10-02 10:02:04 (re-date wrjc + 337j to 2026-10-31).
- Kam, Wednesday's terminal, 2026-10-05: "board taps are enough for audit re-dates" (`learnings/2026-10-05_board-taps-suffice-for-audit-redates.md`).

## Not covered

No live sweep (§5f is not engaged by a date change). No deploy. Not a test change, so skill §4 does not apply.

Refs KS-528
