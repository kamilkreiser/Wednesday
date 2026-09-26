# HPSM-POC backlog screen for Spark (batch 1)

Written 2026-09-26 10:47 AEST. Repo `datasecau/HPSM-POC`, `main` = `291a4eb29b650afdb60ffa16bcc6ff4bbcc0d1a7`. I checked it with `friday_as.sh datasec gh api …/commits/main`. Every code claim was read from a tarball of that SHA, in the scratchpad at `b1/`.

**Sources read:**
- `BACKLOG.md` (whole) and `CLARIFICATIONS.md` (C-01…C-26, whole).
- The STATUS files for B20, B21, B22, B23, B24 and B25, all dated 2026-09-26.
- The morning `CENSUS.md` and `RESULTS.md`.
- Open PRs: only #27, and its file list was read. Open GitHub issues: none.
- The pending live-board cards in the scratchpad: `hpsmpoc-showcase-labelling`, `hpsmpoc-findings-order` and `hpsmpoc-showcase-approver-line`. All three are unruled.
- **Jira HPSMPOC (the backlog of record) was NOT read.** This seat has no Jira tool. Tickets that exist only in Jira are not screened here.

**Spark predicate:**
- one product file plus its test;
- the shape of the fix is fully set by existing code or tickets;
- a runnable test sits nearby;
- not auth/security/Azure/validator, and not PR #27's files;
- at most 3 edit points.

**Result: 1 of 22 candidates passes. The list is thin because B24 and B25 already fixed every B22 row marked "ours".**

## Chosen

| # | Item | File | Edits | RED/GREEN | Brief |
|---|---|---|---|---|---|
| 1 | The firmware task's "Related engagement" status is always "New lead" for every API customer (`FirmwareTask.tsx:65`, `stageFromApi(null)`). The Customers list shows the real stage. This is a NEW finding from this screen, in the same class as B22-07. | `web/src/components/customer/FirmwareTask.tsx` + `FirmwareTask.test.tsx` | 2 (1 line → 2 lines; 1 test insertion, non-empty context on both sides) | **Measured** in a scratch tip copy: RED 1 failed/5 passed at `Assessment in progress`; GREEN 6/6; `-t` filter gives `1 passed \| 5 skipped`; customer+screens 95→96; full vitest at tip 616/616; lint rc 0 on both files; tsc no new errors | `FirmwareTaskStage.brief.md` + `.expect.json` |

## Rejected (one line each)

| Candidate (source) | Why not Spark |
|---|---|
| B24 FOUND-1 / census #10–#11: "Sample data" on the snapshot runner and result header for a user-added customer | The tag labels the content package, not the customer. Fixing it means choosing a wording or tag, which is a decision (census "Claude + decision"). |
| Census #8 / #9: "Sample data" on the customer-list and engagement-list page headers | A product decision (census), and it now overlaps the unruled card `hpsmpoc-showcase-labelling`. |
| Census #18 / #19: POC-wide "sample data" text (`ApiSteps.tsx:84`, `ReportScreen.tsx:57`) | Wording decision, for Kam. |
| B22-06 / F-38: finding order (timeframe vs severity) | Unruled card `hpsmpoc-findings-order`. |
| B22-01 / B22-02 residue: the showcase approver name | Card `hpsmpoc-showcase-approver-line`. B24 took default (b) in its own commit. |
| B22-24: amount of honesty labelling | Unruled card `hpsmpoc-showcase-labelling`. |
| B22-11, B22-12, B22-16 | Deck wording, HP content, or a new template version (Kam's; ADR-R04). |
| B22-13: pricing story | Kam's. |
| `FirmwareTask.tsx:94`: "Applies to … (N, sample figure)" ignores the RECORDED printer count (F-30 rule "recorded first") | Real residue, but it takes 4 edits (import `useApiCustomer` + hook + line + test). The wording for a recorded figure also has to be chosen. And it is the same file as the chosen brief, so it would collide. Route: a Claude seat, after #1 lands. |
| F-06: "Rule outcome", "Scored by fixed rules", "Weight" on screen | Deliberate audit terms (SOW txt:101-102). Replacing them needs wording choices. |
| F-15 / N-04: revenue jargon ("run-rate", "churn", "base case") | The new explanatory text would have to be authored. Nothing to copy. |
| F-34: "Up to 16" → 15 → 16 | Wording decision. The B14 design is deliberate. |
| N-02 residue: "Completed" with date "—" on the journey list (`EngagementOverview.tsx:72`) | No date source exists for those steps. The fix shape is open. |
| N-07: readiness cover "Partner organisation (no organisation name is recorded)" | No partner-name field exists. That would be a feature or decision. |
| N-12: the per-row "Action" label on the plan (`ActionPlanScreen.tsx:297`) | B17 added it on purpose after earlier feedback. Removing it reverses a decision. |
| B23 FOUND-3 / B24 FOUND-2: e2e flake and shared state under parallel workers | Playwright, not vitest. The root cause is unmeasured (B23 says "reasoned, not proved"). |
| BACKLOG: EF logs the lost first-sign-in insert at `fail:` | Picking a log filter could hide real DB failures, which is an observability decision. It is also API config with no nearby test. |
| BACKLOG: API "partner self" subject (duplicates) | API design, cross-module, many edits. |
| B20 "Also found": no screen can request finding-explanation / remediation-narrative | A feature, in the Narrative area next to PR #27. |
| B24 UNMEASURED: privacy notes and data inventory should mention `review_role` and showcase PDFs | Design-pack docs, with no test. |
| `SnapshotLauncher.statusText`: a report-issued run reads "Complete", not "Complete · scored" | Not a reported defect, it is a wording judgement, and no test file exists (the runner refuses a File: that is absent at the tip). |

## UNMEASURED

- Jira HPSMPOC was not read (see above).
- The brief was not put through `spark_run.py --dry-run` or `spark_check.py`, because a hook refuses write git verbs outside FRIDAY, so no checker clone was made. What was checked instead:
  - it was parsed with the runner's own `parse_brief` (File: lines and Tip: OK);
  - every `expected_added` line appears as a `+` line in the brief;
  - the brief's context lines were asserted at the stated tip line numbers.
- The Node version was 26.8.1, not the repo's `.nvmrc` 24.
- Nothing was clicked live.
