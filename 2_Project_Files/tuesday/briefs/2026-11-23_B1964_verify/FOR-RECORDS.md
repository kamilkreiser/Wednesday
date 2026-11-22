# For the records seat: RD-1030 (gate B1964, after the landing of branch b1958/nexusai-nx-p-permission-table)

## RD-1030's state
- At the stamp of the build kit (Tuesday, 06:39 AEDT 2026-11-23, Jira GET): **To Do**, labels `records-pass-1123`,
  `security`, 0 comments. The gate did not read Jira (relayed, not re-measured).
- After the landing: RD-1030 may move to **Testing** on the hosted checks of the landing head (7 check names green,
  the hosted build at 6237 / 394, no new CodeQL alert against main's open 22, the Deploy demo run's build and deploy
  jobs both skipped). Not before; the gate's local CodeQL and jest runs are not the hosted authority.
- One sentence for the ticket and HISTORY.md (the seat's, checked by the gate against the head): RD-1030: the
  permission table now lists `GET /api/data-sources/:id/describe-table` and `GET /api/data-sources/:id/discover-tables`
  under `admin.read`, as the 2026-11-20 ruling on RD-1011 (C-311) keeps both reads administrator-only; cell P2 expects
  it and two census cells hold the opposite case; the inventory and its page are unchanged.
- Who decided: the 2026-11-20 ruling (C-311) settles that the table is brought into line with the administrator-only
  wire. The destination `admin.read` (the existing capability, no new one), the placement at the end of the
  `admin.read` block, the test shape and the two commits are the coordinator's defaults (Q-1 to Q-8 of the kit STAMP).
  C-311's point (1) of "What it does not settle" (CLARIFICATIONS.md line 3151) is answered by this landing.

## The two LEFT FOR OTHERS items (unedited by the lane; candidate records or follow-up items)
1. **The `about` text of `admin.read`** (`backend/services/capabilities.js` line 96 at the head: "administrator-only
   reads: audit, incidents, retention, state, users, provisioning") does not name the two data-source reads it now
   holds. Words for the Roles UI work (RD-929); no test reads it.
2. **The RD-1011 test's header comment** (`__tests__/rd1011-four-routes-administrator-only.test.js` lines 9 and 10 at
   the head: "Choice of refusing all four: a default of the coordinator, not the product owner's; one line per route
   reverses it.") is now true only of the two TEST routes (`POST /api/data-sources/:id/test`,
   `POST /api/setup/data-sources/:id/test`); the two reads are ruled (C-311). A comment-only edit, owed to a later
   change of that file.

## The RD-1011 header comment, quoted (lines 3 to 10 at head 27d49f70)
> RD-1011: four routes make the server connect with a data source's stored sign-in details and had no role check:
> POST /api/data-sources/:id/test, GET /api/data-sources/:id/describe-table, GET /api/data-sources/:id/discover-tables
> and POST /api/setup/data-sources/:id/test. Each handler now runs the setup-mode-aware administrator check first. [...]
> Choice of refusing all four: a default of the coordinator, not the product owner's; one line per route reverses it.

## Also for the records (from the gate's findings, none blocking)
- Only the viewer role is pinned not to hold `admin.read` (cell P2 and the census). A proposed role given `admin.read`
  in the table turns no cell red (the gate's probe Q2, 42 of 42 green). Proposed roles are not accepted by the user
  store today, so the wire is unaffected; RD-929's wiring matrix is where it belongs (VERDICT.md I-1).
- The move also takes the two reads away from the five proposed roles that hold the viewer's reads (print operations,
  finance, security, executive, department manager), which is what "administrator-only" means for them; a note for the
  Roles UI design (VERDICT.md I-2).
- RD-1021 and RD-1022 rows stay `config.read` until their tickets decide; this landing moves every table line from 180
  down by 3, so lane NX-S re-reads the table after it lands.
- Not touched by the lane or the gate: HISTORY.md, BACKLOG.md, CLARIFICATIONS.md, Jira.
