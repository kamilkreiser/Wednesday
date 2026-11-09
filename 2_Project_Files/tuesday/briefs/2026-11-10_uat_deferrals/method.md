# Method: how the deferral register was built

## FOUND
- The pack has 367 cases: 285 functional, 38 non-functional, 32 production gates, 12 end-to-end journeys. Counts re-read from the tracker workbook by program: 285 / 38 / 32 / 12 (control: the four sheets add to 367).
- The register lists **185 cases**: 174 functional (126 Missing, 48 Partial) and 11 end-to-end (8 Missing, 3 Partial).
- By priority: P0 14, P1 99, P2 72. By proposed disposition: Deferred to phase 2 143, Partial (passes with a stated difference) 37, Out of scope for the POC 5. Cross-table (priority by disposition) is at the top of both register files.
- Functional P0 and P1 cases that cannot pass as written: **102** (P0 4 + P1 98: 22 partial + 76 missing). **The earlier analysis summary says 98. That is an addition slip: its own parts, 4 + 22 + 76, sum to 102.** Correct before quoting 98 to anyone. The cover note says 102.
- 111 functional cases and 1 journey (E2E-08) were judged already supported and are not listed.

## TESTED (what the counts are checked against)
- Every figure is computed by `build.py`/`write.py` in the session scratchpad (python3 -I -B, no spreadsheet library; the xlsx is written as plain XML).
- Controls, all asserted in the program: tracker IDs found per sheet (285/38/32/12); every non-supported functional case maps to exactly one group (no unmapped, no duplicate, no supported case swept in); priority in the analysis equals priority in the tracker for all 285 cases; total by priority = total by disposition = rows listed = 185; the 102 P0/P1 figure equals 4+22+76; every Deferred row carries a ticket key and every key used is in the ticket sheet; a planted wrong figure (98) is rejected by the assertion (control fired).
- Output re-read after writing: the xlsx parsed back (Register 197 rows = 9 summary rows + header + 185 cases + 2 spacers, 185 unique IDs) and the csv has 185 case rows.

## HOW each case was classified
1. **Status on the hosted site** (Missing / Partial / supported) comes from the Nov 9 read-only cross-reference of every functional case against the HPSM-POC main branch at commit 2075486 (digest Appendix A, plus its journey table). I did not re-run the site. The status is a code reading, not a test on the deployed site.
2. **Disposition** is my proposal by feature group, not an HP or product-owner ruling:
   - Missing feature that is in the phase 2 layout catalogue (HPSMPOC-448 epic, tasks 449 to 460): Deferred to phase 2, with the ticket for that feature's page or entity. The mapping of catalogue items to tickets was taken from the filing brief (twelve tickets in order, item counts 13/7/2/17/9/9/5/7/13/6/7/1 match). Ticket-to-case matching is by feature, case by case in groups.
   - Missing because the pack tests a browser-only prototype behaviour (JSON import/export, hash routes) or a review aid (white/blue toggle): Out of scope for the POC.
   - Present but different (storage location, by-design differences, role model): Partial, with the difference stated in the "why" column.
3. The "Review note" column holds Datasec-only cautions. Delete it before sending.

## NOT CHECKED
- **No live check against the hosted UAT site.** If the deployed build differs from commit 2075486, statuses may differ. Tonight's builds (Playbook Partner Readiness, Demo Walkthrough) are not in these statuses; readiness cases UAT-087, 089, 090 should be re-read after they land.
- **17 Partial rows** are marked "verify" or carry no stated behaviour in the analysis (UAT-100, 105, 109, 111, 128, 130, 135, 211, 212, 213, 215, 222, 250, 254, 258, 265 and 276). Their gap is unconfirmed. Flagged in the review note column. Confirm before sending, or move them to "supported".
- Good / Better / Best cases (UAT-027, 028, 181 to 184) are proposed as deferred or partial, but the product owner removed it from the menu on purpose and the catalogue lists its return as an open question. The review note says so.
- **38 non-functional cases:** not classified against the hosted site; listed on the second sheet as "Not assessed". **32 production gates:** listed on the second sheet with the proposal "Out of scope for the POC (production gate)", as the pack itself records. Five gates (PRD-001, 005, 007, 010, 014) are marked as partly built already, per the analysis; none has been evidenced against the gate wording.
- The deferral record the pack requires also needs an owner, a date and a risk acceptance (pack section 5.1); only signatory, date and signature columns are provided.
- Ticket numbers 451, 453 and 458 follow the filing order and are not read back from Jira in this pass.
