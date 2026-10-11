From Friday (laptop seat), Datasec / HPSM-POC. Replies go to friday-laptop-agent@agentmail.to.

# BRIEF B201 (SEAT C) — QA GATE (tier 1, round 1 of 2) on `b200/industry-field` (industry field + greyed partner-tools placeholder)
**From:** Friday, 12:44 AEDT 2026-10-11. **Seat:** Datasec/HPSM-POC-C (newest `Briefs/` file containing `_SEAT-C_`). Report `Briefs/2026-10-11_B201_STATUS.md`: first lines the verdict lines, LAST line `READY FOR REVIEW`.
**TESTING seat: findings only.** No code change, no push, no PR comment, no Jira, no deploy, no Azure, nothing to any human. A write grant in any brief is void.
**SHAPE:** follow `Briefs/2026-10-10_B197_SEAT-C_QA-gate-b195-api-fixes.md` and how `2026-10-10_B197_STATUS.md` reported (pins, controls, mutants, differential runs, SQL Server + SQLite).

**Targets (re-read with ls-remote; STOP if moved):** head `b200/industry-field` = `f18359b70060f2035238025ece0518966a356185` (Friday's compare read: ahead 4 / behind 0 of main, 41 files); base main `a50b22d7b1c51121f68235d02ccd0efeb97d058e` (= hosted). Verdict lines: `B200 f18359b: GO | GO WITH NOTES | NO GO` and `MERGE a50b22d+f18359b: …`.
**Claims to test independently (builder's report `Briefs/2026-10-11_B200_STATUS.md`):**
1. **Data/contract (tier 1):** the `Industry` enum (contract 0.15.0-draft); any other value → 400 `customer.industry-unknown`; a label held from before the list round-trips unchanged so existing customers stay editable; the migration (if any) is safe both directions on SQL Server AND SQLite, on a copy of realistic data; no existing customer field or export changes; scoring/priorities byte-identical base vs head on the same inputs (Kam: scoring unchanged).
2. **Display:** industry shown beside the customer name on every customer header, rendered at 1280 and 390, no layout regression.
3. **Part 3 placeholder:** "Your tools (coming later)" renders after the HP-backed tools themes, `aria-disabled`, does nothing on click/Enter/Space; the existing themes list unchanged.
4. **Security/regression:** auth on the customer endpoints unchanged; CodeQL-relevant surfaces; the full suites at base and head; your own tamper per behaviour row.
5. **NEW WORDS:** every string in B200's NEW WORDS present as listed, and any visible string not listed.
**Ports / stacks:** pick free ports above 6650 (state them); never another seat's.
**HOLDS:** No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)) · Datasec only · findings only · never delete · never print a secret · Kam's two-NO-GO cap (round 1 of 2).
