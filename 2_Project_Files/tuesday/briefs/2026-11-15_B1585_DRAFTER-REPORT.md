STARTABLE: YES, but only once the MIGRATION slot reads ALLOWED with the product owner's word quoted. Under HOLD (the default) the kit is not launched. Q-1 is the gate; read it first.

# B1585 drafter report: HPSM-POC lane N, F10 (re-edit an approved narrative), seat H168

Drafted 2026-11-15 17:31 to 17:46 AEDT (`date` printed 17:31:01, 17:31:36, 17:37:51, 17:40:40, 17:45:59).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1585_SEAT-H168_hpsmpoc-lane-n-f10-narrative-reedit.md` (88 lines).
- Sidecar: `...narrative-reedit.md.measured` (70 claims plus S01-S11, S17, S21, S24, S30-S32).
- Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1585/`.

## BLUF
- **What blocks the reviewer today.** The review rule refuses every status except `generated` (`NarrativeReview.cs:28`). An accepted review also overwrites the row's text and review fields (`ReportingEndpoints.cs:306-311`). So once a summary is approved it cannot be edited again, and a second edit would lose the first one.
- **The design follows the plan and D-016.**
  - `Edit` is now also accepted on `approved` and `edited`. Approve and Reject stay for new drafts only.
  - Each re-edit first copies the review it replaces into a new append-only table, `narrative_revision`. That copy keeps the text, the reviewer, the time, the note and the role.
  - The `narrative` row stays the current version. So the report selector, the metrics, the PDF approver line and the web list are all unchanged.
  - The screen shows the existing `Edit` button on an approved, current card. It reuses the existing `Save edit and approve`, so there is no new word anywhere.
- **It needs one migration per provider, and migrations are frozen.**
  - The 2026-11-10 precedent: the product owner opened the one migration since then in his own words, "Allow the one migration (gated, not deployed)" (RELAYED: B1442 stamp, B1461 kit).
  - Today's ruling, "please action the reviewers feedback", does not name a migration. So the kit carries a MIGRATION slot, default HOLD (**Q-1**).
- **Two findings the plan did not list. Both are now in the kit's scope.**
  1. **Erasure.** `StoredReportsAsync` (`PersonalDataEndpoints.cs:215-222`) finds the reports that may print an approver's name. It reads only the narrative row's current `review_by`. After someone else re-edits, the first approver would no longer be found by an erasure, and the PDF that names them would stay downloadable. The kit makes the lookup also read `narrative_revision`, and pins this with a test.
  2. **The Demo copy of an issued report** is re-rendered from what is recorded now, and must match the issued file byte for byte (`ReportingEndpoints.cs:436-437`, `:457-462`). After a re-edit it answers 409 `report.changed-since-issue`. That is existing behaviour for any later change. It is measured and written as a deploy note, not changed.
- **Partition.**
  - None of the kit's 14 files is among b1577's 41 paths (measured by set intersection: 0; control: adding `infra/README.md` gives 1).
  - `infra/README.md` IS a b1577 path, so its two DENY sentences (`:105`, `:219`) are left alone (Q-5).
  - Lanes P and R had no kit on disk at drafting. The kit makes the seat read their OWNS lines at Step 0 and STOP on any shared path.
- **Routing and resources.**
  - Base `f32b209bfa6f33c3c0268c1daa76753c816b316e`, 0 open PRs.
  - Seat H168 (B1577's seat was H166 and B1584's is H167 in the commission), pane `Datasec/HPSM-POC-H168`, branch `b1585/hpsmpoc-narrative-reedit`.
  - Ports 10010-10019: SQL Server 10010, Azurite 10011, WEB 10012, hosted 10013, stub 10014, chooser 10015, live-API APIs 10016 and 10017.
  - Model Sonnet (`model-routing.md:92`, row C2), gate G1 (`:108`), model id `claude-sonnet-5-5` (`models_latest.json:23`).

## Facts re-measured with instruments
- **Main.**
  - `gh api branches/main` gave `f32b209b...` (2026-11-15T05:04:28Z) at 17:31.
  - Open PRs: 0. Control `state=all&per_page=3` gave 319, 318, 317, all closed. `pulls/99999` gave 404.
  - `matching-refs/heads/b1585`, `b1584` and `b1586` each gave 0. Control `b1541` gave 1. `b1577` gave 1 (`fda88777...`).
- **b1577.** `compare f32b209...fda8877` gives ahead 1, behind 0, files 41. The commission's "41 paths" is right; the plan's "43 files" is stale.
- **Census.** `scripts/census.py` over the tarball, frame as in the kit, found 218 rows in 84 files: STATE 10, REVIEW 138, ERASE 7, TABLES 11, WEB 31, MIGR 14, DENY 7, NEW 0. Rows are in `census_rows.tsv`. REVIEW is broad on purpose: `/review` also matches the review door and the follow-up review. Its extra rows are UNAFFECTED by property.
- **Prior work.** `narrative_revision|NarrativeRevision` matches 0 files at base (control `NarrativeRow`: 44 files). 335 branches; the pattern `narrat|revis|re-?edit|reapprov|1585|h168|f10` hits 5, all earlier narrative work. Newest commits: `ApiNarrative.tsx` `a026cb30` (10-30), `NarrativeReview.cs` `32b74ba3` (09-24). JQL `project = HPSMPOC AND ( text ~ "narrative" AND text ~ "approved" )` gives COUNT 33, with no re-edit ticket. A second JQL with OR'd text terms returned 43 broad hits and is not used as evidence. 3 tickets were created today (482-484), all unrelated.
- **Nothing ever deletes a narrative.** No `Narratives.Remove`, `ExecuteDelete` or `DELETE ... narrative` in `api/src` outside the migrations. The 12 `ExecuteDelete` sites are imports, follow-up sessions and feedback attachments. So the Restrict FK from `narrative_revision` to `narrative` blocks nothing.
- **The export follows the new table by program** (`PersonalDataEndpoints.cs:80-87`, every FK to `app_user`). The erasure's report lookup does not (`:215-222`).
- **Migration house rules.**
  - `Migrations/.editorconfig`: "GENERATED by `dotnet ef migrations add`" and "never edited by hand".
  - Guards: `PersistenceTests.cs:43-44` (no pending model change) and `:49-51` (providers name for name), plus the two SQLite rebuild guards.
  - Newest migration: `LedgerAuditAndFollowUpRetention` (commit `eb2e49c7`). Sqlite has 39 files, SqlServer 37.
  - The EF tool at `.tools/b1442/ef/dotnet-ef` printed 10.0.12 with `DOTNET_ROOT` set, equal to the EF Core pin at csproj `:21`.
- **Toolchains.** `.tools/dotnet-10.0.404/dotnet --version` gave 10.0.404. `.tools/node24/bin/node` gave v24.21.0, npm 11.19.0. `.nvmrc` reads 24. `global.json` pins 10.0.404 with rollForward disable. The CodeQL suites are `javascript-queries/2.5.0` and `csharp-queries/1.11.0` (`ls`).
- **e2e.**
  - The Playbook e2e shards run the web in mock mode (`playwright.config.ts:74`). The mock has no narrative routes (grep of `web/src/server/mock`: 0 narrative handlers).
  - So the only browser path to `ApiNarrative` is the live-API set (`e2e.mjs:103-108`, ten specs, not in any CI shard).
  - The kit adds test 3 to the existing `playbook-narrative-attention-live-api.spec.ts`, so that `web/scripts/e2e.mjs` is not touched, and runs both live-API passes.
- **Ports and load.**
  - `lsof` 10010-10019: 0 listening (control 18).
  - Kit scan for `1001[0-9]`: 31 kits, 0 hits (control `992[0-9]` in B1577: 2).
  - Panes at 17:37: `%0 tuesday`, `%63 Datasec/MPS-M141`, `%54 Datasec/MPS-M140`, `%1 fleet-monitor`. No HPSM-POC pane.
  - Load 14.69. `df` 1198 GiB free.
- **CI pointers at f32b209.** 71, 87, 184, 252, 255, 277-310, 303, 314, 396, 409, 413, 426, 478, 494, 518, 630 (the same numbers as at 8766b253).
- **Contract.** Both `openapi.yaml` copies are `cmp` IDENTICAL. Their 409 text at `:1597` reads "The narrative is not a generated draft".

## Census verdicts (the drafter's reading of each line, not a run; the seat's Step 4 decides)
**Property.**
- REWRITE when the line enforces or asserts that only a generated narrative may be EDITED, lists the user-id or append-only tables, or finds the reports an approver's erasure must withhold.
- UNAFFECTED when the line is about Approve or Reject, a fresh draft, the scripted sample, the review door or follow-up review, a migration guard that must stay green, or contract text.

| file | verdict | why |
|---|---|---|
| `NarrativeReview.cs:16-20,28` | REWRITE (product) | the rule and its summary |
| `ReportingEndpoints.cs:262-318` | REWRITE (product) | writes the revision before the overwrite |
| `Entities.cs`, `AssessmentDbContext.cs` | REWRITE (product) | new entity, its mapping, append-only guard beside `:64-65` |
| 2 migrations + 2 Designer files + 2 snapshots | NEW (generated) | `NarrativeRevisions`, CreateTable only |
| `PersonalDataEndpoints.cs:215-222` | REWRITE (product) | the erasure finding above |
| `infra/sql/api-identity.sql:19-25,48-50` | REWRITE (infra) | DENY on the new append-only table; its own rule `:23-25` allows it |
| `ApiNarrative.tsx:108-114,190-195` | REWRITE (product) | Edit on an approved, current card |
| `PersonalDataTests.cs:149-152` | REWRITE | the user-id table list gains `narrative_revision` |
| `ReviewAndTemplateTests.cs` | REWRITE (add rows) | Edit on approved/edited; `:21-24` (Approve refused) stays true |
| `ReportingApiTests.cs:63-64`, `B45StaleReviewTests.cs` | UNAFFECTED | Approve on edited is still 409; a stale edit is still 409 |
| `ApiNarrative.review409/previous.test.tsx`; e2e `Approve narrative` rows (`journey.ts:104`, `playbook.ts:53`, `keyboard.spec.ts:81`, `playbook-event-states.spec.ts:142`, `step-previous.spec.ts:31`, the live-API specs); `NarrativeScreen.previous.test.tsx` | UNAFFECTED | fresh drafts, or the scripted sample |
| `LedgerAuditTests.cs:151-152` | UNAFFECTED | `Assert.Contains` of two DENY lines; a third line keeps it true |
| `DeleteGrantCensusTests.cs`, `FirstVisitWarmupTests.cs:276`, `ImportCheckTwinTests.cs:176` | UNAFFECTED | no delete site added; tables derived from the model |
| `PersistenceTests.cs:34,43-44,49-51,58,204`, both SQLite migration guards | UNAFFECTED, must stay GREEN | they are the migration's proof |
| contract copies, `schema.gen.ts` | UNAFFECTED (Q-4) | description text only |
| `infra/README.md:105,219` | UNAFFECTED here (Q-5) | b1577's path |

## Chain table (rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 | kit (stamped, MIGRATION=ALLOWED), project identity, the three toolchains, docker, pinned MSSQL image | exist at BASE or on the machine (measured by the drafter, except docker and the identity) |
| 1 | `mut`, gh | step 0 |
| 2 | `mut` with npm ci and dotnet restore; writes `base-unit.json`, `base.trx`, `census.tsv` | step 0 |
| 3 | `head`; the EF tool; Q-answers | steps 0 and stamp |
| 4 | `head` product files and the build (Step 3 builds) | step 3 |
| 5 | REWRITE list (steps 2, 4); `mut` for red-at-BASE runs | steps 2 and 4 |
| 6 | `head` complete; `base-unit.json`; containers and live-API APIs (started inside 6d and 6f) | steps 2 and 5 |
| 6e | CodeQL CLI and suites; the diff | step 5 |
| 7 | all green | steps 4 to 6e |
| 8 | pushed sha; census files | steps 2, 4 and 7 |

## D-decisions (made in the kit; Tuesday can reverse each at the stamp)
- D-1 **A revision table, not a new narrative row per re-edit.**
  - I weighed the no-migration alternative: each re-edit becomes a new `N-xxx` row. It fits every CHECK and needs no schema change.
  - It was rejected for three reasons. It changes the M-metrics: `NarrativesAttempted` counts rows (`MetricsCalculator.cs:29`). It makes the report selector depend on row order. And it duplicates the input digest and audit history of one narrative.
  - It is the fallback if the product owner keeps migrations frozen (see Q-1 (b)).
- D-2 **Only superseded reviews are copied.** A first review writes no revision row, because `GeneratedText` already keeps the model's draft. So nothing needs back-filling for existing rows.
- D-3 **Edit only.** Re-approval is the existing "Save edit and approve" (the edit is the approval, dated by `review_at`). Approve and Reject stay for generated drafts.
- D-4 **No new words.** The WrongState message ("Only a generated narrative can be reviewed.") and the 422 message stay as they are. Both remain true for Approve and Reject. No audit text or usage kind changes.
- D-5 **Append-only in code plus a SQL DENY. Not a SQL Server LEDGER table.** A ledger would be a bigger, separately ruled change (the HPSMPOC-117 precedent). The `narrative.reviewed` audit row of each re-edit already sits in the ledger table.
- D-6 **The browser proof.** It is a new test 3 in an existing live-API spec, so `web/scripts/e2e.mjs` and `LIVE_API_ORDER` are not touched. Both live-API passes run at BASE and at head.
- D-7 Added code comments may cite the decision document's `D-016`. The commit message carries no ticket key (the F10 ticket is B1583's and its key was unknown at drafting).

## QUESTIONS FOR TUESDAY (each with a default)
- **Q-1 Migration authority (the gate).** Migrations are frozen unless the product owner opens one. His 17:16 words do not name a migration.
  - Default: **HOLD**. Do not launch. Ask him with a card in the 2026-11-10 form:
    - (a) "Allow the one migration (gated, not deployed)": this kit runs as written.
    - (b) "Keep migrations frozen; build only what needs none": a different, smaller kit instead (D-1's alternative). It costs a change in what "narratives attempted" counts, and needs its own words check.
  - If Tuesday reads the 17:16 ruling plus the plan's "a migration pair" as enough, the slot can read ALLOWED with that reading quoted as Tuesday's. The drafter does not recommend it: the freeze was set by the product owner's own words.
- **Q-2 Builder model.** Row C2 says Sonnet. This adds a table and touches the human review gate before customer reports and the erasure lookup. B1442's migration was built on Opus.
  - Default: Sonnet with the G1 Opus gate.
  - Raise to Opus if Tuesday weighs the erasure path as row C3/C4-adjacent.
- **Q-3 Show earlier revisions?** Default: no. They are stored and exported, not shown. A list on screen needs new words (a heading, labels) for the product owner.
- **Q-4 Contract text.** The 409 description ("The narrative is not a generated draft", both `openapi.yaml` copies `:1597`, `openapi.merged.json`, `schema.gen.ts`) becomes narrower for Edit. Shapes, codes and fields do not change.
  - Default: unchanged now. The PR body names the sentence, and it is folded at the next contract version.
  - Alternative: the seat edits all four with a version bump. That widens the diff into `web/contract/**` and the drift test.
- **Q-5 `infra/README.md:105,219`** list the DENY tables (`audit_event`, `finding_disposition`). It is a b1577 path.
  - Default: unchanged by this kit. One line follows after b1577 lands, in Tuesday's next HPSM records or doc pass.
- **Q-6 The live-API set** (two passes, each on a fresh API and database, at BASE and head). It is the only browser path to this screen. It adds about four heavy runs.
  - Default: run it, as the kit says.
  - Alternative: component tests only, with the browser proof named NOT RUN in the PR body.
- **Q-7 Window and hard stop.** READY target 360 minutes after Step 0: eight e2e shards, two SQL Server parts, two live-API passes at two refs, and two CodeQL databases. Load was 14.69 with two MPS seats live.
  - Default: one window with the context band and handover form.

## UNMEASURED
- Everything the seat runs. The drafter ran no build, test, browser, container, EF command or CodeQL. In particular:
  - the Step 4 red set;
  - whether both migration guards stay green;
  - the exact `Up` and `Down` calls the EF tool generates;
  - whether a racing re-edit gives 412 and not 500 (DERIVED from the If-Match precondition and the assessment stamp);
  - the SQL Server catalog rows;
  - the live-API run times.
- The census verdicts are readings of each line's context.
- RELAYED, not re-read by the drafter:
  - the landing rule (CLARIFICATIONS.md line 3617) and the hosted CodeQL languages, from the B1577 kit;
  - the freeze precedent, from the B1394, B1442, B1444 and B1461 kits.
- The B1584 and B1586 OWNS lines did not exist at drafting.

## Outside-the-fences disclosure
Reads:
- `DRAFTER_RULES.md`, the commission file, the plan folder (ACTION-PLAN.md, FEEDBACK.md, RESULT.md, COMMISSION-ACTION-PLAN.md), the B1577 kit, its drafter report and ANSWER-1, the D-016 and D-017 blocks of the decision document, and the migration-freeze lines of the B1394, B1442, B1444 and B1461 kits (by python search).
- The B1442 STATUS in the project's `1_Project_Definition/Briefs/` (by grep, read-only).
- `model-routing.md`, `models_latest.json`, `brief_seat.sh` (grep of its level lines).
- `gh api -X GET` under the project's `GH_CONFIG_DIR`: main, pulls, matching-refs, the paginated branch list, the b1577 compare, commits for three paths, and the f32b209 tarball.
- Jira: three JQL searches through my own GET-only copy of the B1577 drafter's `jsearch.py`. Credentials were read in-process from the project `.env` and never printed. No ticket was read whole.
- Toolchain `--version` prints (dotnet, node, npm, dotnet-ef), an `ls` of the CodeQL qlpacks and of the project's `.tools` folder, `lsof`, `tmux list-panes`, `uptime`, `df`.

No card was read: none was needed, and no `decision_queue.sh` call of any form was made.

Local runs, in my work folder only: tarball extraction, the census program, and measurement scripts.

Writes: only the kit, its sidecar (by `stamp_check.py --init`, then filled by my `scripts/fill.py`), this report, and scratch files in `s278/d1585/`.

Nothing else was touched: no Jira write, no git or GitHub write, no file under `/Volumes/Datasec_DEV/!CODING/`, no message, no tmux send-keys, no az, no docker, nothing deployed, no `_ledger.md`, no WEDNESDAY, FRIDAY or non-Datasec tree.

DRAFTED B1585: kit 88 lines, sidecar rc 0, questions 7
