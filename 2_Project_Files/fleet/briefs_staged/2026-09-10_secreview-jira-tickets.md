# Brief — 13B: raise Jira tickets so the Datasec product findings can be worked

**Commissioned by Kam, 2026-09-10: *"take the Datasec product consolidated findings document and
create tickets under each project in JIRA in order to resolve each of the findings"*, then ruled
*"Go with your defaults, and create the two missing projects."***

**This round WRITES to Kam's live Jira. Everything below that is not explicitly authorised is not
authorised. Read the HOLDS before the work.**

## WHAT KAM RULED, EXACTLY

1. **AGGREGATE, do not file one ticket per finding.** His 2026-09-06 rule: one larger ticket per
   logical path, its items as a checklist or sub-issues, never three or five separate tickets for
   one line of work. *"Within a logical path"* is the limit — two unrelated defects do not share a
   ticket because they arrived together.
2. **Create the two missing projects.** `CWP` — CryptixWebPortal. `TDP` — Task-Dispatcher. Both keys
   confirmed FREE by Tuesday at 12:04 with a control (a taken key returns 200, these return 404).
   **Re-check before creating; a key is permanent in every ticket id.**
3. **Do NOT file the parked pair** — Vision Sales Portal and QuickQuote, 17 findings, parked
   2026-09-07. They stay out.

## THE MAPPING, MEASURED — re-derive it, do not trust it

    CryptixWebPortal   30 findings  ->  CWP  (create)
    OneTimePad/CypherKey 36         ->  CPKEY   (28 open today)
    Reporting Dashboard AU 17       ->  RD      (296 open)
    myPKI              13           ->  MYP     (30 open)
    SecurePDF           9           ->  SEC     (exists, ZERO issues ever)
    Task-Dispatcher     6           ->  TDP  (create)
    HPSM                1           ->  scaffold only, nothing to assess — file nothing, say so
    Vision + QuickQuote 17          ->  EXCLUDED by ruling

**Component names are PRODUCT names and do not always match repository folders.** The register's own
Appendix D says so. Use the appendix's project line, not the component heading.

## USE THE APPENDIX THAT SHIPPED THIS MORNING — this is the point

`13B_Datasec_Products_Consolidated_Findings_Register_2026-09.md` now carries **Appendix D — Evidence
locations**: 14 entries, each naming project, file and line, keyed `EV-B-nnn`, cross-referenced from
every finding. **Every ticket you raise cites the finding ids AND their `EV-B-` entries**, so an
engineer opening the ticket gets the file and line without opening the document.

Where a ticket aggregates several findings, list each finding id with its evidence entry.

## 🔴 SEARCH BEFORE YOU CREATE — the duplicate rule

`RD` alone holds **296 open issues** and some of these findings may already be filed.

**Before creating any ticket, search that project for it** — by the SYMBOL, the FILE PATH or the
error string, **never by your own phrasing of the problem**, which is exactly what differs between
two people describing one defect. In the ticket, state what you searched and found:
*"searched `<symbol>` and `<path>`, 0 open hits"*. That line is cheap and it makes the absence
checkable.

**If it IS already filed: do not raise a duplicate.** Add the finding id, the evidence entry and
your search to the existing ticket as a comment, and count it separately in your report.

## 🔴 THE SECRET RULE, UNCHANGED

Several findings concern committed credentials. **A ticket gives project, file, line, variable name
and credential class — never a value, never a prefix, never a length.** Jira is a wider audience
than the register. If a ticket cannot be written usefully without the value, it cannot be written:
say so and leave it for Kam.

## TICKET SHAPE

BLUF first ([[2026-08-06_bluf-write-for-the-reader]]): what is wrong, what to do, then the detail.
Summary line names the component and the fix, not the finding number. Body carries: the findings
covered (ids + `EV-B-` entries + severity), the evidence locations, the remediation from the
register — **do not invent new remediation and do not contradict the register** — and your duplicate
search. Severity/priority from the register's band; do not re-score anything.

## HOLDS

- **Jira writes are limited to: creating `CWP` and `TDP`, creating tickets, and commenting on an
  existing ticket you found by search.** Nothing else. **No transitions, no reassignment, no edits
  to anyone else's tickets, no bulk operations, no deletions.**
- **The credentials act as KAM'S OWN ACCOUNT and carry admin rights.** Behave accordingly: an
  accident here is an accident on his board under his name.
- **Read-only on the registers.** Do not edit `13A`, `13B` or `03_Findings_Register`.
- **Nothing to Peter, Stuart, HP or any client human.** Do not email Kam.
- **STOP and mail Tuesday** if: a project key is taken, a component maps to no project, the
  register and the appendix disagree, or you are about to do anything not in the list above.

## REPORT

Mail **`tuesday-agent@agentmail.to`**:

- the two project keys created, with their ids;
- per project: tickets created (with keys), findings covered, and **findings NOT filed with the reason**;
- duplicates found and commented on rather than re-raised;
- the arithmetic: findings in 13B = filed + commented + deliberately excluded + nothing-to-assess.
  **If that does not balance, say so rather than making it balance.**
- every control you ran, and anything you could not verify.
