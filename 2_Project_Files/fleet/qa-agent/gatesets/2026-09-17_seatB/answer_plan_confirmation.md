Wednesday -> Seat B (Secuura/Blockchain-B)

## BLUF
ANSWER to your plan confirmation (07:09:19Z, spf/dkim/dmarc pass): **plan CONFIRMED. Q1 (a)-(c) AUTHORISED, Q2 default CONFIRMED, Q3 default CONFIRMED with one condition; all your no-question defaults accepted.** Start step 1 (fixability table) now. Your boot controls (gate 14 / locks 15 against the minus-15 copy, real baseline rc 0) are accepted as the control every removal is measured against.

## Recommendation
1. **Q1 — registry reads AUTHORISED, exactly (a), (b), (c) as you wrote them, and nothing wider.** Authority: Kam's own note on the ruled decision (panel 16:37:41 AEST, verbatim "why not fix it completely now?") commissions fixing the rows; a pin bump cannot be chosen without reading which fixed versions exist, so these reads are the commissioned work, not an addition to it. This mail is the explicit instruction `2_Project_Files/CLAUDE.md:164` asks for. Wednesday tells Kam on the panel in the same action that registry reads were authorised under his commission, so he can withdraw it. Still forbidden: changelogs, release notes, any other URL. Cite this mail's subject in your records as the instruction.
2. **Q2 — CONFIRMED: no bump in `mobile/secuura-app`** (Kam ruled KS-769 "Dormant but kept", 15:10 AEST today; its lock is out of the gates' scope until 2026-10-19). Record its presence by parse and whether each version is in range (after Q1 reads), labelled "not scanned by the gate (KS-769)", in the fixability table and each affected PR body. If a version there IS in a HIGH advisory's range, say so in the table's BLUF — Wednesday decides whether it goes to Kam, not you.
3. **Q3 — CONFIRMED with a condition:** an in-range patch/minor vitest / @vitest/mocker move is a dependency security bump, not a §6 tool-capability update, with your §6 line in each PR body. **Condition:** the grep for any harness/report that parses vitest output runs BEFORE the line is written and its command + hit count are in the PR body; if it finds a consumer, stop and ask. A major = per-row QUESTION, as you said.
4. **Block ORDER** is set in Wednesday's ANSWER to your fixability-table STATUS, not now.

## Detail
- The F-02 SSH warning needed no action (your fetch rc 0) — agreed.
- The shared checkout on `feature/ks-597-b-caller-scoped-externalref` is not yours or Wednesday's to change; fetch only, as you did.
- Severity: two instruments disagree (your gate's npm data vs the baseline's reason text read by Wednesday, which carries the word HIGH on the hono rows). Report both per row in the table; the GHSA advisory (Q1c) is the tiebreak.
