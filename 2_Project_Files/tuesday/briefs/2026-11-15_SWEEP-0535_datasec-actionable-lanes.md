# SWEEP-0535: Datasec tickets agents can work now, in lanes (read-only sweep, 2026-11-15)

Written by a read-only sweeper at 2026-11-15 05:35 to 05:45 AEDT (clock: `date` at the end of the sweep read 05:40:58 AEDT). Method and shape copied from SWEEP-1326 (2026-11-11). Every number below was re-measured today; nothing is carried over from SWEEP-1326 except its method and its exclusion classes, each re-checked against the live board (a carried key that is no longer open is dropped and counted).

## BLUF

- Board census (instrument: own GET-only helper `jqdump.py`, Jira REST `search/jql`, paginated by `nextPageToken` to `isLast`; JQL `project = <KEY> AND ( statusCategory != Done )`, parentheses present; 2026-11-15 about 05:30). Control that can fail: open + Done must equal the project's full count by `created >= "2000-01-01"`, and it did in all four (134 + 347 = 481; 81 + 47 = 128; 186 + 213 = 399; 856 + 126 = 982):

| project | open now | open at SWEEP-1326 | actionable tickets now | lanes |
|---|---|---|---|---|
| HPSM-POC (HPSMPOC) | 134 (3 In Progress, 131 Backlog) | 140 | 10 (plus 1 conditional) | 4 |
| Security Composer (PCOMP) | 81 (all Backlog) | 89 | 6 | 3 |
| MPS Commercial Calculator (MPSCALC) | 186 (all Backlog) | 214 | 51 | 5 |
| NexusAI (RD) | 856 (To Do 384, Testing 256, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2) | 853 | 124 To Do tickets in 5 lanes, plus 1 serial-last ticket and 2 on an unfinished branch | 5 |

- Lanes: HPSM 4 + PCOMP 3 + MPSCALC 5 + NexusAI 5 = 17 lanes, file-disjoint inside each project by the ownership rule named per lane (exceptions are named).
- What changed since 2026-11-11 and drives this sweep: on 2026-11-11 about 14:15 to 14:34 AEDT the product owner accepted the day's "quick recommendations" on all four boards (HPSM-POC 18, MPSCALC 29, PCOMP 7, NexusAI 17; counted from the ticket comments themselves by `text ~ "quick recommendations"`, 16 + 25 + 7 + 38 tickets carry the note). Many tickets SWEEP-1326 excluded as "needs ruling" are now ruled and buildable; many it listed as actionable were built by the 2026-11-11/12 landings. That is why MPSCALC rises from 43 to 51 even though 28 fewer tickets are open.
- Top 3 lanes to launch first:
  1. **MPSCALC lane M-O (deploy-script and package rulings: 202, 222, 103, 226, 224, 223, 349).** All five rulings are accepted, no open PR, no seat in flight, files confined to `scripts/` and `src/MpsCalc.Api/Api.csproj`; 202 carries a deadline in its own ruling ("must land before the first hosted price overlay exists"). Nothing deploys.
  2. **NexusAI lane S (server.js).** The B1484 landing chain is DONE (origin main `ab5a16e9`, PRs 192 to 199 all merged), which was the stated reason lane S had to wait. The 11-11 rulings approve the viewer write-gates (RD-958, 964, 965, 966, 968), the permission core (RD-930 to 932), the erasure/wipe-alarm design (RD-610, 612, 622) and others; the CodeQL set is open (64 alerts on main per SWEEP-1326, UNMEASURED today). Highest security value on the board. One seat at a time owns `backend/server.js`.
  3. **HPSM-POC lane H-1 (Demo alias on six surfaces + one count wording + Industry choice list: 467, 420, 168).** Rulings accepted 2026-11-11 14:15, "queued as its own change", no open PR (`gh api -X GET repos/datasecau/HPSM-POC/pulls` state open: 0), main `576231b7`. Demo-facing; reviewer-visible.
  Next after those: NexusAI F1/F2/B/T (independent of S), MPSCALC M-W1/M-A/M-E, PCOMP B and C, HPSM H-4 (drafts for Kam).
- Standing context re-verified, not assumed (details in "Standing context" below): the HPSM-POC HTML-phase decision still has no recorded answer on the board (all 21 HTML-phase tickets show no Jira update after 2026-11-10 11:40 AEDT); PCOMP PR #85 is still an open draft "HOLD K6" (last updated 2026-10-21) and still touches `document-pdf.ts`, `pdf-fit.ts`, `policy-document.ts`; Composer deploy remains Kam's word per the project CLAUDE.md line 30; HPSM-POC next-phase items are being gathered, not built (tickets 471 to 479 filed 2026-11-12 labelled `next-phase`/`gather`, "held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT", quoted from HPSMPOC-392 comment).

Frame notes: every file list comes from ticket text, ticket comments or origin tree reads (`gh api -X GET repos/<repo>/git/trees/main?recursive=1`, positive control: 1528 / 709 / 1005 / 973 blobs returned, and each named path below was found by `/usr/bin/grep` on that tree unless marked). Local `2_Project_Files` checkouts were not used (stale). Origin mains at sweep time (`gh api -X GET repos/<repo>/commits/main`): HPSM-POC `576231b7` (2026-11-12 17:17 AEDT), PCOMP `68975c10` (2026-11-13), MPSCALC `0bb3ed12` (2026-11-12), NexusAI `ab5a16e9` (2026-11-12). Every builder's PRIOR WORK check and a `git grep` on origin main must re-confirm before building: a ticket whose BLUF I read is dated, and a ticket I did not re-read (marked "unchanged since 2026-11-11 12:00" by Jira `updated`) is judged from SWEEP-1326's reading.

---

## 0. Open pull requests (per repo, `gh api -X GET repos/<repo>/pulls state=open`, each under that project's own `GH_CONFIG_DIR`; auth read `Logged in ... account kamilDatasec`)

| repo | open PRs | note |
|---|---|---|
| datasecau/HPSM-POC | 0 | control: the same call with `state=closed` returned PRs 295 to 316 |
| datasecau/Datasec-Security-Composer | 1: #85 draft "HOLD K6: L1 SM 3.16 content catalogue (release built, not cut)", branch `b330/sm316-content-catalogue`, updated 2026-10-21, base `308b7aa6`, 57 files incl. `packages/renderers/src/document-pdf.ts`, `pdf-fit.ts`, `document.ts`, `policy-document.ts` | #86 and #91 (Dependabot) are gone: PR #126 (b1534) replaced them, #127 and #128 cleared alerts 28 and the undici set |
| datasecau/MPS-Commercial-Calculator | 0 | last merge #191 (2026-11-12) |
| datasecau/Reporting_Dashboard_Au (NexusAI) | 0 | last merge #199 (RD-691, 2026-11-12) |

Branches that look built or unfinished (`gh api -X GET .../git/matching-refs/heads/b14|b15` plus `compare/main...<branch>`):
- NexusAI, NOT merged and not PR'd: `b1480/nexusai-s-viewer-write-gates` (diverged, 7 ahead, 52 behind) and `b1480/nexusai-s-setup-column-mapping` (12 ahead, 52 behind). These are the unfinished work for RD-958/793 and RD-967. Every other NexusAI `b14*`/`b15*` branch compares "behind, 0 ahead" (squash-merged leftovers). A records or lane-S seat must decide: rebase and finish, or restart from the rulings (see question 4).
- HPSM-POC, PCOMP, MPSCALC: every `b15*` branch reads "diverged" with 1 to 9 commits ahead and many behind, the signature of squash-merged leftovers (their PRs are in the merged lists above). Not proven merged branch by branch: UNMEASURED. Old `b150` to `b158` scratch branches on HPSM-POC are 199 to 202 behind.
- Built-looking tickets still open on the board (a records seat should check; a ticket whose newest comment says the PR landed and whose Done-when may be met):
  - NexusAI, 32 keys still open with merged PRs: RD-969 and RD-563 (PR #198, still To Do), RD-691 (PR #199, Testing), RD-970/971 (#192), RD-720 (#193), RD-731 (#194), RD-972/976 (#195), RD-929/977/978 (#197), RD-962/963/979, RD-605, RD-544, RD-796, RD-798 to 800, RD-759 (shapes 1 and 2), RD-892, RD-893 part 1, RD-498, RD-312, RD-959 to 961, RD-973, RD-928, RD-936, RD-407, RD-982. (SWEEP-1326 listed the same families as records-only; the three newest are RD-969, 563, 691.)
  - PCOMP: PCOMP-74, 80, 81 (PR #125 merged 2026-11-11: "the white is one named style value, and the withdrawn list's setting key takes the code-style font"; the rulings' leftovers are exactly that), PCOMP-77, 15, 21, 26, 27 (closed since 11-11), PCOMP-23 (change-report half merged in #120; policy-PDF half open).
  - MPSCALC: 14 tickets SWEEP-1326 listed actionable are now Done (96, 198, 377, 122, 98, 217, 339, 160, 147, 196, 126, 203, 119, 201); 173 (clause 2 met by #181; clause 1 seed identity open).
  - HPSM-POC: 439, 432, 409, 461, 465, 399, 405, 436 and NEW-1 (HPSMPOC-468) are Done. Open but built in part with the remainder ruling-bound: 228, 356, 357, 406, 408, 462 (see Excluded).
  - HPSM-POC eight "no build left" tickets from SWEEP-1326 (99, 178, 431, 323, 343, 117, 100, 315) are still all open: a records pass is still owed (UNMEASURED whether each Done-when is met).

---

## 1. HPSM-POC (Jira HPSMPOC)

Open 134: 3 In Progress (HPSMPOC-87, 90, 91; 87 and 91 are drafting tickets in my actionable set: confirm no seat holds them), 131 Backlog; 10 Epic, 123 Task, 1 Sub-task by type (awk over the dump). New since 2026-11-11: HPSMPOC-467 to 481 (15 created, of which 468 is Done). Main `576231b7`; PRs 309 to 316 landed 2026-11-11/12 (customer look and accessibility, shell/buttons, SDK pin, messaging alignment #314, three reworded lines #316, minimatch override #315).

Phase rule applied: this phase only. A ticket is excluded if it matches an item of the 2026-11-10 decision document (HTML phase, 21 tickets) or any HP-tool integration, or is a `next-phase`/`gather`/`messaging` held ticket.

### Actionable (10 tickets, plus 1 conditional)

| key | title (short) | why actionable now | size | files (origin tree; confirm) | lane |
|---|---|---|---|---|---|
| HPSMPOC-467 | Demo view: stored customer name still shown on 7 surfaces | The product owner's 2026-11-11 ruling (comment 41018): "Alias on all seven", as on the two pages already built. BUILD SIX SURFACES (customer lists, engagements, document preview, profile context row, firmware-risk task, snapshot launcher). The seventh, the Home pipeline table, overlaps the planned Home rebuild (HPSMPOC-457, HTML phase): leave it out and say so. Demo real-name reader read 5 on Home before and after the 2026-11-12 deploy (RELAYED from the ticket; not re-measured: no hosted read) | M | `web/src/components/customer/CustomerManagement.tsx`, `EngagementOverview.tsx`, `web/src/components/playbook/SnapshotLauncher*`, document preview and profile components under `web/src/components/` | H-1 |
| HPSMPOC-420 | "N of M scored questions answered" used everywhere | Ruled 2026-11-11 ("Yes, everywhere"); the four lines that print another count are named in comment 40670: `engagement.ts`, `EngagementOverview.tsx`, `SnapshotLauncher.tsx`, `SnapshotResult.tsx` (all four paths exist on the origin tree; `/usr/bin/grep` hit for `engagement.ts`, `EngagementOverview.tsx`, `SnapshotLauncher.b56.test.tsx`) | S | those four | H-1 |
| HPSMPOC-168 | Customer profile: Industry becomes a choice list (healthcare, financial services, public sector, other) | Ruled 2026-11-11. BUILD THE CHOICE LIST ONLY: the neutral fleet-size note's own words are not written and "come to the product owner before they ship", so the note is out. No scoring effect, no refusal. May touch the API enum: check before building | M | profile form under `web/src/components/customer/`, maybe `api/src/HpsmPoc.Modules.Assessment/` | H-1 |
| HPSMPOC-470 | Five open points after the latest merges | Done-when "each point built or declined". Buildable without any word: (1) `web/e2e/a11y.spec.ts` journey test at 26 to 28 s of a 30 s limit; (3) `startingOwner` in `web/src/components/customer/remediation-store.ts:56` cuts inside an emoji sequence (cosmetic); (4) one SQL Server migration timeout seen once on the squash of PR 310 (diagnose, add a test or record not reproducible). NOT (2) (two blocks keep a 768 px cap: an edge not measured, a layout call) and NOT (5) (pin the runtime or accept the float: "Not decided") | S to M | `web/e2e/a11y.spec.ts`, `remediation-store.ts`, `api/tests/` | H-1 (point 3), H-3 (points 1, 4) |
| HPSMPOC-193 | Outbound addresses believed as a proxy from anywhere | Ruled 2026-11-11: option (b), a shared header value only the web front end sends, held on both apps; the API believes a forwarded address only when it is present. Regression row named in the ticket. The stored value and its rotation are configuration: build code and test, set nothing on a host | M | `api/src/` forwarded-headers setup, `web/src/server/` | H-2 |
| HPSMPOC-87 | Customer questions: use the 16 as the base, aligned to the Composer's policy principles (DRAFT for Kam) | Product owner chose 2026-11-10 that an agent drafts the content; drafts stay in the analysis repository, marked draft, never loaded into the product. STATE In Progress: check whether a seat holds it before launch | M | `1_Project_Definition/Content/` (documents only) | H-4 |
| HPSMPOC-162, 163 | AI at the printer phase-one position; meaning of green/amber/red | Ruled 2026-11-11 "Yes, draft both": an agent drafts both for the product owner's review; nothing is shared with the vendor | S each | documents only | H-4 |
| HPSMPOC-91 | Client collateral: three packs (before, during, after engagement); STATE In Progress, check for a seat | Ruled 2026-11-11 "Yes, agent drafts"; each draft marked draft; nothing loaded or sent until approved | M | documents only | H-4 |
| HPSMPOC-241 | HP lab and integration questions | Ruled 2026-11-11: one batch, an agent drafts the e-mail for the product owner; nothing goes to the vendor except from the product owner. A DRAFT is not an HP-tool integration | S | document only | H-4 |

Conditional (1): **HPSMPOC-480** (one failed Kudu upload leaves a mixed UAT site; `scripts/deploy-from-ci.sh` lines 68/69). The ticket "asks for a remedy to be chosen" and names its own default, "(a) if the product owner does not answer": read the app's latest deployment status once before concluding, test in the script's existing stub test. A choice is pending, so it is not counted as actionable: Tuesday to say "default (a)" (question 2). Lane H-3 if released.

### Lanes (HPSM-POC)

- **H-1 web components (Demo alias, count wording, Industry list, emoji cut).** Owns `web/src/components/customer/**` and `web/src/components/playbook/**` and the profile form. Order 420 (four files), 467 (six surfaces), 168 (choice list), 470.3. Sonnet. Drafter rule 8 applies: the `infra` job's repo-wide scans (hidden characters etc.) run in every gate.
- **H-2 server and API.** Owns `web/src/server/**` and the API forwarded-headers setup under `api/src/`. 193 only. Sonnet; API tests must run on SQL Server as CI does.
- **H-3 tests and scripts.** Owns `web/e2e/a11y.spec.ts`, `api/tests/` for point 4, `scripts/deploy-from-ci.sh` and its stub test (480 if released). Sonnet. Shares no file with H-1 or H-2.
- **H-4 documents (drafts for Kam).** Owns `1_Project_Definition/Content/` drafts only: 87, 162, 163, 91, 241. Sonnet. No product file, no Jira transition by the seat.

Standing line for every kit: this phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only; nothing deploys.

### Excluded (HPSM-POC, 123 of 134)

Class assignment by a program that put every one of the 134 open keys in exactly one class; union equals the dump (134 assigned, 0 residual after the manual add of 87).
- Epics (10): 1, 10, 18, 23, 30, 38, 45, 50, 56, 448.
- HTML-phase items (21; no Jira update on any of them after 2026-11-10 11:40 AEDT, so no recorded phase answer): 368, 370, 390, 392, 393, 394, 396, 449 to 460, 463, 464.
- Messaging held for later (8, filed 2026-11-12, `next-phase`/`gather`/`awaiting-hp`): 471 to 477, 479.
- HP-tool integration or awaiting HP (22): 46, 47, 48, 82, 83, 84, 85, 86, 92, 94, 96, 97, 164, 165, 166, 167, 173, 181, 191, 220, 240, 259. (164 and 90 below were ruled "prove once then close": the proof needs a feedback item sent through a hosted site with the route on, a hosted step.)
- Ruling or a person still needed (10): 31, 35, 37, 44, 51, 52, 55, 90 (hosted proof), 237 (ruled "wait": the timing measurement is a hosted measurement, no spend), 246.
- Built or partly built, remainder is ruling-, word-, or hosted-bound (9): 228 (N-7 second half, the Retry saving button, is a visible word), 356 (unread step bodies "neither commissioned nor recorded as not wanted": a decision), 357 (mock half met, UAT half is a hosted measurement), 406 (items 2 and 3 are layout calls; item 5 declined), 408 (three limits as sentences held for the product owner), 462 (fill defect fixed except sidebar rows, an HTML-phase surface; "UX/UI review" half unscoped), 469 (fifth customer record without "(sample)": keep, mark or remove is undecided and the cause may be UAT data), 478 (waits on an upstream release), 481 (decide whether the walkthrough panel shows eight presenter lines: gather).
- Deploy, hosted measurement, VM or Azure (15): 57, 60, 62, 63, 64, 126, 196, 207, 234, 235, 303, 304 (ruled: a cleanup of the HPSM test machine, its own approved step, Azure), 309, 362, 428.
- Records-check closings, no build left (8; UNMEASURED whether each Done-when is met): 99, 100, 117, 178, 315, 323, 343, 431.
- Human-owned or SOW paperwork (20): 5, 6, 11, 12, 19, 20, 21, 24, 29, 58, 61, 169, 170, 171, 172, 174, 175, 176, 389, 395.
- Conditional (1): 480 (above).

---

## 2. Security Composer (Jira PCOMP)

Open 81, all Backlog (3 Bug, 4 Epic, 74 Task). New since 2026-11-11: PCOMP-128. Ticket count by program class below sums to 81. Main `68975c10`; no seat is known in flight (STATUS files not read: UNMEASURED). Composer deploys only on Kam's word (project `CLAUDE.md` line 30: "never deploy to it without Kam's word"); nothing below deploys.

### Actionable (6)

| key | title (short) | why actionable now | size | files (origin tree) | lane |
|---|---|---|---|---|---|
| PCOMP-52 | Table of contents for the policy PDF (L6-a, "depends: none") | Ruled 2026-11-11 14:39: the word "Contents" is approved as the heading ("the only new word the feature needs"). Build unblocked. Ticket text names `policy-document.ts`, `policy-summary.ts`, `document-pdf.ts`, `document-docx.ts`; template bump `policy-document-pdf/3` | L | `packages/renderers/src/policy-document.ts`, `policy-summary.ts`, `document-pdf.ts`, `document-docx.ts` and tests | A |
| PCOMP-82 | Policy PDF cover date in Sydney time, set on the brand profile | Ruled earlier (C-71 COMP-15 (a)); STILL UNBUILT on main: `packages/renderers/src/policy-summary.ts:260` `${dateWords(releasedAt)} (released, UTC)` and `:283` "(UTC)" (grep on origin file, positive control: `document-pdf.ts` has 4 `UTC` hits elsewhere). Note the string lives in `policy-summary.ts`, which PR #85 does NOT touch | L | `packages/renderers/src/policy-summary.ts`, brand profile in `apps/api`, `packages/db` (migration plus rollback), `packages/api-contract/src` | A |
| PCOMP-123 | Size the footer by the real page count | Open, "not built" (comment 2026-11-10); needs the page count in `document-pdf.ts` | M | `packages/renderers/src/change-report.ts` (`FOOTER_LABELS`), `document-pdf.ts`, `pdf-fit.ts` | A (waits on PR #85) |
| PCOMP-23 | Policy PDF drops the manifest hash line with long names | Change-report half merged (#120); policy-PDF half open: `document-pdf.ts` | M | `document-pdf.ts`, `pdf-fit.ts`, renderer test | A (waits on PR #85) |
| PCOMP-75 | End page "Still to answer" heading touches the tiles (item b) | CSS spacing; the string is at `apps/web/src/screens/GuidedWizard.tsx:724` (`<h3>... "Still to answer"`). The old path SWEEP-1326 named, `apps/web/src/guided/GuidedWizard.tsx`, returned 404: the file moved | S | `apps/web/src/screens/GuidedWizard.tsx`, its css | B |
| PCOMP-128 | DEPLOY.md: lines outside the 0020/0024/0025 sections that still say Route B is "as above" or UNMEASURED, plus one grammar line | New 2026-11-11, docs only | S | `DEPLOY.md` | C |

### Lanes (PCOMP)

- **Lane A, PDF renderers.** Owns `packages/renderers/src/**`, `packages/db` (migration for 82), `packages/api-contract`. PR #85 touches `document-pdf.ts`, `pdf-fit.ts`, `document.ts`, `policy-document.ts`. So: start with PCOMP-82 (in `policy-summary.ts`, not in #85, but the brand-profile migration is deploy-bearing: Opus), then 52 (touches `policy-document.ts` and `document-pdf.ts`, both in #85: accept a rebase or wait), then 123 and 23 only after #85 moves. Default per question 5. Opus (PDF layout and a migration).
- **Lane B, web polish.** Owns `apps/web/src/screens/GuidedWizard.tsx` and css. 75 only. Sonnet. Held Guided tickets (73, 85, 90) edit the same screen: they are `held`, not built.
- **Lane C, deploy guide.** Owns `DEPLOY.md`. 128 only. Sonnet.

### Excluded (PCOMP, 75 of 81)

- Epics (4): 1, 2, 3, 4.
- `held` label (19): 19, 20, 68, 69, 70, 71, 72, 73, 76, 79, 84, 85, 86, 87, 88, 89, 90, 91, 92.
- Waits on Kam (2): 46 (ruled 2026-11-11 "warn, never block"; build waits on L1 to L3, held PR #85), 94 (ruled "send now"; the send is the project owner's own act).
- Ruling or words still needed, or built (9): 9, 13, 29, 38 and 65 (words or optional ruling), 11 (ruled 2026-11-11 "show where it was asked", but needs a contract change and two new words to the approval list first), 74, 80, 81 (their ruling's leftovers were built by PR #125 merged 2026-11-11: records-only).
- Blocked by another ticket or held PR #85 (24): 31 to 37, 39, 44, 45, 47 to 51, 53 to 58, 60, 66, 67.
- Not agent work, human, other project, or nothing to write (15): 5, 6, 7, 8, 10, 12, 16, 18, 25, 28, 59, 61, 64, 78, 93.
- Stale or unclear (2): 41, 42 (42 likely built in migration 0025; UNMEASURED).
- Closed since SWEEP-1326 (dropped from its lists): 15, 21, 26, 27, 77, 83, 98, 116, 127.

---

## 3. MPS Commercial Calculator (Jira MPSCALC)

Open 186, all Backlog (170 Task, 15 Epic, 1 Bug). Class assignment by program: union 186, 0 residual. Main `0bb3ed12`; no open PR; origin branches are squash-merge leftovers. Pricebook values are confidential: no price value is to enter any ticket text, lane brief or this file. Nothing below deploys. 13 new tickets since 2026-11-11 (MPSCALC-387 to 399; 387, 388, 389, 391, 392, 393 already Done).

Reading rule used (the product owner's 2026-11-11 ruling, MPSCALC-371 and 364): "Leave developer-only docs out of your word review": corrected developer-only sentences are written from what the code does; a sentence a customer sees goes to the product owner first. Also his earlier rule, restated in MPSCALC-169: every contract change waits for the exact name to be approved.

### Actionable (51)

SWEEP-1326's actionable tickets still open (judged from its reading unless the ticket was updated since; the 2026-11-11 22:24 records notes were read for 135, 297, 251, 57, 334, 130, 121, 123, 99, 369, 173):

| key | what remains (today's reading) | lane |
|---|---|---|
| 135 | smoke journey loads, presses Short-form, but is not green in all four legs (red on the dev stub and the no-API leg; green only against an API on invented data) | M-W1 |
| 297 | same red legs; release is 135's change plus a run at both widths | M-W1 |
| 251 | stub step runs in CI (clause 3 met); sign-in leg not built | M-W1 |
| 57 | four PDF-text specs (itemised-summaries, proposal-buttons, proposal-purchase, rental-book) are left out of CI because `pdftotext` is not on the runner: put them in CI | M-W1 |
| 111, 185, 139, 369 | 390 px proposal e2e; 390 px home check; missing axe check on the (i) hint button (words approval NOT in scope); whole-suite timeouts (19 of 20 counted runs clean: needs more runs) | M-W1 |
| 334 | stub does not answer an update of a held-created rental quote | M-W1 |
| 130 | style half built (#178); printed words per page still differ from the approved mock's | M-W1 |
| 121 | unreadable-file refusal built (#178); browser step with a folder drop not built (one words question open: build the e2e step only) | M-W1 |
| 123 | streaming built (#176); bound on concurrent uploads not built | M-A |
| 99 | clause 3 built (#176); clause 5 and the review findings open | M-A |
| 163 | overlay Busy bound under 20 group runs under load | M-A |
| 324, 325, 338, 333, 331, 340, 341 | validation-row tests and independent re-runs of mutants (test files only) | M-A |
| 207, 302 | importer prove step blind to mis-bounding / says AGREE for a tamper | M-A |
| 170 | stable fleet line id and price audit (contract change: needs the exact field name approved first; ticket does not say a ruling is needed. Treat as a PROPOSAL step until Tuesday confirms) | M-A |
| 158 | two follow-up tests never re-run by a gate | M-E |
| 200 | importer coverage table (counts only, no values) | M-E |
| 223 | runbooks look in the wrong log (runbook path unlocated: UNMEASURED) | M-O |
| 349 | `Api.csproj` comment example (needs an SDK that carries the tie: UNMEASURED) | M-O |

Newly ruled by the product owner on 2026-11-11 14:34 AEDT ("29 quick recommendations accepted"; each ticket's own comment read today):

| key | ruling in one line | lane |
|---|---|---|
| 233 | Clone whose typed reference already exists is refused ("two quotes with one reference break the audit trail") | M-A |
| 91 | A price-book store that lost its registry refuses to start instead of starting fresh (its refusal wording goes with the change; use a plain operator line) | M-A |
| 229 | Deal-usage proposal prints a colour rate only for device classes with estimated colour pages | M-W2 |
| 128 | Rental price screen keeps "Software / month" in the breakdown row only | M-W2 |
| 150 | Deal-level usage tile sits at the top of the usage section | M-W2 |
| 202 | Pre-deploy overlay check refuses every overlay form the app refuses at start-up; a malformed shape stops with one plain line; "must land before the first hosted price overlay exists" | M-O |
| 222, 103, 226 | Roll forward only is the standing rule; the deploy refuses an older package once care-pack or staging rows exist (222 needs the row count described in comment 39648) | M-O |
| 224 | Patched Xml assembly ships inside the app package, as the Pkcs one did (a package change; it reaches a host only with a deploy on its own approval) | M-O |
| 195 | Put the accepted engine-target sentence into the engine docs (other clauses of 195 are not settled) | M-E |
| 316 | The agreed sentence ("at most 100 characters, an emoji counts as two") in the remaining places comment 40472 lists | M-E |
| 364, 371 | Developer-only docs sentences (four staff list columns; three template-store sentences) written from what the code does, no word review | M-E |
| 189, 394 | Source version id rule (case and accent forms are one id) in the validate paragraph of `docs/API.md`: clause 5 of 189, owed by 394 (one sentence, one change) | M-E |
| 120 | Contract version practice (a minor bump at each feature change) gets its own short section in the API docs | M-E |
| 78 | Escalation and rounding confirmed: remove the provisional marking in the places comment 39419 names | M-E |
| 390 | Register wording: X-33 omits the margin refusal's order of precedence; X-46 omits that panel pairs the map already holds are skipped (developer register, no word review) | M-E |
| 396 | Comments that state the old rental short-proposal rule (`ProposalPage.tsx:35-38`, `:44`, `print.spec.ts:75`, `proposal-buttons.s...`) | M-W1 |
| 397, 398 | SDK pin guard: a row that plants a defect through `all_problems`; routes still outside the guard (GITHUB_PATH, PowerShell steps, MSBuild SDK variables, local actions, allowPrerelease) | M-O |
| 399 | Web dev stub drift: `purchaseQuotes.ts:91`, `:109` do not model the 7 per cent default or copied hidden inputs | M-W1 |

### Lanes (MPSCALC)

- **M-W1, web e2e, CI, stub, print, feedback form (13 keys: 135, 297, 251, 57, 111, 185, 139, 369, 334, 130, 121, 396, 399).** Owns `web/e2e/**`, `web/playwright.config.ts`, `.github/workflows/ci.yml`, `web/src/api/stub/**`, `web/src/feedback/**`, `web/src/proposal/**` (111 and 130 share `proposal.css`), `web/src/screens/ProposalPage.tsx` comments. Order 135, 297, 251, 57, then 111/130, 185, 139, 369, 334/399, 121, 396. Sonnet.
- **M-W2, ruled web screens (229, 128, 150).** Owns the rental price screen and the purchase usage section under `web/src/screens/**` EXCEPT `ProposalPage.tsx`. Any e2e row they need goes into NEW spec files, never edits to M-W1's. 229 may live in the proposal print (M-W1's `web/src/proposal/`): read first and, if it does, sequence it after M-W1. Sonnet.
- **M-A, Api stores, validation, importer (123, 99, 163, 324, 325, 338, 333, 331, 340, 341, 207, 302, 233, 91, 170).** Owns `src/MpsCalc.Api/Feedback`, `Sources`, `Quotes`, `Inventory`, `src/MpsCalc.Import/**`, and `tests/MpsCalc.Api.Tests/**`, `tests/MpsCalc.Import.Tests/**`. 170 also touches `web/src/screens/bom/PriceAudit.tsx` and `docs/api/openapi.json`: build only after the contract name is approved. Sonnet; Opus for the independent mutant re-runs (324 to 341, 207, 302).
- **M-E, engine and docs (158, 200, 195, 316, 364, 371, 189, 394, 120, 78, 390).** Owns `docs/ENGINE.md`, `docs/API.md`, `docs/IMPORTER.md`, engine tests, `src/MpsCalc.Engine/**` for 158. 316's "remaining places" may reach `docs/api/openapi.json` (generated: regenerate, do not hand-edit). Sonnet; Opus for 158.
- **M-O, ops scripts and package (202, 222, 103, 226, 224, 223, 349, 397, 398).** Owns `scripts/**`, `scripts/tests/**`, `infra/scripts/**`, `src/MpsCalc.Api/Api.csproj` (224 and 349 share it). Nothing deploys; no `az`. Sonnet.

### Excluded (MPSCALC, 135)

- Ruled, but a contract name or customer-visible words must go to the product owner first (7): 161 (archive a quote: contract change), 156 (rental credit field), 169 (field naming the price-book versions), 368 (hide six figures; "agent proposes the name for your approval"), 194 (the session-ended sentence goes to him before it ships), 110 (one-pager design rule still owed), 277 (Enterprise proposal book, no ruling comment). 156, 161, 169, 368 become actionable as a NAME PROPOSAL step (a document), then a build after approval: question 6.
- Records only or Kam's own act or a secret (4): 173 (clause 1 seed identity), 188 (ruled "record only, no code"), 85 (Kam re-sends the specification file), 395 (hosted showcase seed identity's client secret expired: Entra and hosted).
- Still needs ruling or product words (10): 129, 153, 157, 159, 177, 261, 288, 306, 310, 314.
- Held or waits on a person, deploy or hosted data (9): 118, 124, 133, 140, 144, 155, 162, 187, 372.
- Blocked by another ticket (2): 212, 236.
- Later phase (5): 149, 152, 154, 181, 260.
- HTML-phase `lane-v*` tickets (33, unchanged): 237, 243 to 246, 248, 258, 264, 265, 267 to 276, 278 to 287, 315, 358 to 360 (277 is in the ruled-pending class above). Reading caveat kept from SWEEP-1326: "HTML phase" is defined for HPSM-POC in the order; the nine server-side keys (237, 284, 285, 286, 287, 258, 358, 359, 360) are the first to release if the hold does not cover MPSCALC (question 3).
- Epics (15): 1 to 15. Spec-seed umbrellas (42): 16 to 20, 23 to 36, 40 to 54, 55, 58, 59, 60, 62 to 65. Questions for Kam (8): 69, 74, 75, 76, 79, 80, 82, 83.
- Closed since SWEEP-1326 (14 carried keys, dropped): 109, 112, 113, 114, 115, 117, 131, 132 (the "leave all four" rulings closed 114, 115, 117, 132), 295, 342, 380 to 383.

---

## 4. NexusAI (Jira RD)

Open 856: To Do 384, Testing 256, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2 (sum 856; types by program: Bug 407, Task 374, Story 72, Epic 3). Testing and Release Ready (455) are not work (JIRA.md flow To Do, In Progress, Testing, Release Ready, Done). All 384 To Do keys were assigned to a class by program (below); 101 of them were not individually judged by SWEEP-1326 or today: they are listed, with a suggested lane, as second-tier. 5 new tickets since 2026-11-11: RD-982 (Testing), 983, 984, 985, 986.

Landing chain: DONE. PRs 190 to 199 merged 2026-11-11/12 (main `ab5a16e9`); the only unmerged feature branches are `viewer-write-gates` and `setup-column-mapping` (section 0). `scripts/verify-expected-counts.json` is touched by every branch and regenerated by Tuesday at landing (not repeated). Never make "the alert reads fixed on `refs/pull/N/head`" a landing condition (drafter rule); the check is main's analysis after landing.

### Actionable (124 To Do keys in 5 lanes + 1 serial)

The 2026-11-11 14:34 AEDT rulings (17 accepted, per the ticket comments) that unlock work, read today:
- Write and setup routes: administrators only; no admin routes in open (no sign-in) mode; the managed-identity check runs only inside Azure; no fixed password in the source for the model switch: RD-958, 964, 965, 966, 968.
- Server-side permission model approved as proposed (row scope, sensitive-field masking, audited reads and denials): RD-930, 931, 932 (large build).
- Erasure and wipe alarm: sign-in settings kept outside what a data erasure deletes; the volume-wipe alarm stays until acknowledged; the health page shows a plain status line: RD-610, 612, 622.
- RD-888 (same 1,000-row limit and a defined answer to a malformed limit on the Log Analytics path), RD-858 (remove the test page's SQL box), RD-810 (fix, not dismiss, the test-code alert), RD-644 (per-deployment also-notify address, empty by default), RD-433 (demo data loads only with a second demo-only marker, plus a banner), RD-532 (banner above the loading overlay), RD-522 (scrub names of people and seats from shipped code comments), RD-349 and RD-175 (grey-text contrast ruling), RD-578 and RD-577 (key-vault setting read under the wrong name: "may be fixed now", the sign-in one reviewed on its own), RD-947 (write the reconciliation of the mock's eight fixed risk rules with the free-text conditions first).
- NOT unlocked: RD-702 and RD-636 (truthful "encrypted at rest" wording is drafted for the product owner first).

Lane S, `backend/server.js` and friends (33 keys). One seat at a time owns `server.js`, `jsonStorage.js`, `simpleDb.js`, `intentRouter.js`, `queryPreprocessor.js`, `ticketStore.js`, `costCentreMap.js`, `dataErasure.js` start-up paths, `docs/role-capabilities.json`:
RD-958, 964, 965, 966, 968 (write and setup gates; continue or restart from `b1480/nexusai-s-viewer-write-gates`: question 4) then 930, 931, 932 (permission core), then 974, 975, 926, 772, 773, 770, 765, 766, 762, 767, 768, 769, 763, 764 (CodeQL set; never dismiss; 763 and 764 are judgement tickets: read first), 711 (SIGTERM tears `audit-buffer.json`, High), 830, 893 part 2, 896, 820, 888, 610, 612, 622, 644, 433. Lane S is long: split across successive seats, never parallel, because every item edits `server.js`. Any new handler gate needs the route inventory regenerated from a non-dot tree (carried from SWEEP-1326: UNMEASURED today). Opus for the permission core, the CodeQL set and RD-711; Sonnet for the rest.

Lane B, backend periphery without `server.js` (13): RD-804, 455 + 805 together (805: local branch `942204d1` red, needs the carrier-gate review-list entry: UNMEASURED today), 744 (Opus), 745, 750, 824, 728, the locally-built 576, 590, 826 items 1 and 2 (no full-suite run), and 577 + 578 (`backend/azureADManager`-family key-vault setting name; the sign-in one reviewed alone). Sonnet.

Lane F1, first-run, login, settings pages (17): RD-475 + 560, 189, 456, 492, 117 + 188 + 176, 481, 808, 371 + 373, 151, 416, 540, 687, 396. Owns `static/{login,first-run-setup,settings}.html` and `static/js/{first-run-setup,settings,entra-provisioning-ui}.js`; do NOT touch `scripts/refactor-inline-styles.js` if the csp branch (now merged as #192) changed it: re-read first. Sonnet.

Lane F2, dashboard, css, front-end tests (21): RD-144, 164, 175 + 222 + 349 (dark/grey contrast; build the dark half of 175 only if the light half still needs a design choice), 220, 259, 261, 483, 532, 613, 832, 835, 858 (remove SQL box from `testing.html`), 771, 861 (after F1), 512, 513, 515, 538, then 145 last (vendor the CDN assets; needs `Dockerfile`, lane T's). Owns `static/index.html`, `static/js/{index,admin,chart-details}.js`, `static/css/**`, `tests/e2e/**`. Sonnet.

Lane T, tooling and tests (40): finish the built local branches RD-730, 749, 729 (unpushed worktrees in `.tools/b1431/wt-*` per SWEEP-1326: UNMEASURED today), 757, 734, 345, 352, 355, 378, 379, 384, 134, 249, 353, 394, 397, 580, 586, 348, 668, 829, 918, 320, 387, 426, 539, 566, 572, 595, 597, 599, 600, 623, 726, 980, and today's new test items 983, 985, 986, RD-810 (`tests/uat-run.js`), RD-947 (docs: the risk-rule reconciliation, documents first). Owns `scripts/**`, `.github/**`, `docs/**` (not the role-capability files), `__tests__/**`, `Dockerfile`, `package.json`. Sonnet.

Serial, last, alone: RD-522 (scrub names from shipped code comments) touches every lane's files. Run it when no other lane is open.

Cross-lane exceptions: RD-771 and RD-861 touch F1's `settings.js` (sequence after F1); RD-145, 745, 397, 918 need the `Dockerfile` (lane T owns it).

### Second-tier To Do, not individually judged (101 keys; title read only today)

Suggested lane in brackets, to be settled by each builder's PRIOR WORK check: RD-132 [T], 152 [F2], 154 [T], 156 [F1], 162 [F1], 178 [F2], 221 [F2], 231 [S], 234 [F2], 235 [T], 252 [F2], 262 [F2], 268 [F2], 276 [F2], 280 [T], 285 [T], 289 [F2], 317 [T], 326 [B], 328 [T], 344 [T], 346 [T], 350 [F2], 351 [F2], 356 [T], 357 [B], 359 [B], 360 [F2], 364 [S], 368 [S, Azure ARM: check], 370 [T], 375 [T], 380 [B], 386 [T], 389 [F2], 390 [B], 392 [T], 405 [B], 420 [B], 422 [B], 434 [T], 439 [S], 440 [S], 445 [S], 458 [not agent], 478 [B], 482 [F1], 484 [S], 485 [F1], 488 [F1], 489 [B], 493 [T], 496 [S], 500 [F1], 502 [S], 504 [T], 509 [F1], 511 [S], 517 [S], 519 [F1], 537 [B], 550 [S], 551 [T], 553 [docs, T], 556 [F1], 557 [B], 565 [T], 569 [B], 581 [S], 588 [B], 596 [F1], 598 [T], 620 [T], 621 [B], 632 [B], 633 [B], 634 [B], 635 [B], 637 [B], 650 [S], 654 [S], 676 to 680 [F2 and F1: brand palette], 689 [serial with 522], 701 [F2], 704 [T], 712 [B], 714 [B], 715 [F1], 717 [T], 746 [T], 748 [T], 752 [F2], 753 [F1], 754 [F2], 758 [S, measurement], 901 [F2], 984 (dev-only dependency with no patched release: record, no build). These are plausible work for second-wave seats; none is counted in the 125 above.

### Excluded (NexusAI, other than the second tier)

- Built and merged, awaiting records (32 keys, Jira still open): 312, 407, 498, 544, 563, 605, 691, 720, 731, 759 (shapes 1 and 2; the third shape, a `data:` payload, is still open and unruled), 796, 798, 799, 800, 892, 928, 929, 936, 959 to 963, 969, 970 to 973, 976 to 979. A records seat closes these.
- Unfinished branches, not new lanes: RD-793 and RD-967 (`viewer-write-gates`, `setup-column-mapping`; see lane S, question 4).
- Wording drafted for the product owner first (2): 636, 702.
- Held or needs ruling (17): 146, 193, 305, 313, 400, 401, 546, 583, 584 (deferred by ruling, blocked on RD-574), 674, 722, 740 (cause undetermined), 842, 854, 884, 908, 911.
- Roles UI chain (23, held on word rows or design-first): 933 to 935, 937 to 957 (947 is lifted for its document step only).
- Not agent work (57): 6, 7, 8, 13, 20, 21, 22, 28, 29, 30, 31, 34, 50, 54, 55, 69, 76, 83, 233, 287, 393, 414, 415, 449, 467, 468, 469, 473, 479, 480, 507, 520, 530, 534, 536, 542, 543, 552, 562, 570, 587, 642, 659 to 661, 663, 664, 666, 667, 672, 673, 724, 738, 739, 742, 827, 886 (epics, business, Partner Center, customer-test, other projects, Azure, fleet tooling).
- In Progress and owned by another seat or human (8): 49, 81, 427, 431, 432, 450, 643, 662 (427, 431, 432 are stale 2026-09-14 plans: whether they merged is UNMEASURED).
- Put on Hold or Declined (9): 18, 32, 33, 41, 93, 104, 743 (held); 300, 564 (declined).
- Not examined by any sweep, listed in SWEEP-1326 as title-only (41): 133, 236, 316, 319, 325, 331, 358, 366, 383, 398, 406, 421, 446, 457, 487, 547, 548, 582, 589, 611, 655, 688, 713, 716, 718, 725, 727, 792, 797, 806, 834, 845, 855, 859, 872, 876, 909, 914, 925, 927, 981.
- Testing (241 of the 256, not in any class above) and Release Ready (198 of the 199): not work; not read.

Class union check: 316 keys in the classes above plus 540 residual (439 Testing/Release Ready, 101 second-tier To Do) = 856.

---

## Standing context re-verified

- **HPSM-POC builds only this phase.** Re-verified from the board only: tickets 471 to 479 were filed 2026-11-12 with labels `messaging-2026-11-12`, `next-phase`, `gather`, `awaiting-hp`, text "held, not built, filed for later". The HPSM project `CLAUDE.md` does not carry the phrase (`grep -i -c phase` read 0, with control `Datasec` reading 6): the rule is the order's, not the file's.
- **HTML decision awaited.** No recorded answer found on the board: HPSMPOC-449 to 456, 458 to 460 last updated 2026-11-09 22:26; 463, 464 on 2026-11-10 11:40; 368, 370 on 2026-11-10 04:12; 390, 393, 394 on 2026-11-10 11:19 (Jira `updated`, read per ticket). The decision cards themselves were NOT read (fence): Tuesday attests the card state.
- **Composer deploys only on Kam's card.** Project CLAUDE.md line 30 reads "never deploy to it without Kam's word" (grep); no PCOMP ticket in the actionable set deploys.
- **PCOMP lane A waited on held PR #85.** Still true: #85 open draft, last updated 2026-10-21, 57 files, 14 of them under `packages/renderers` or `apps/web` (grep over `pulls/85/files`), including `document-pdf.ts`, `pdf-fit.ts`, `policy-document.ts`. `policy-summary.ts` and `change-report.ts` are NOT among them.

## Questions for Tuesday (each with a default)

1. **MPSCALC and NexusAI, 2026-11-11 rulings read as the product owner's:** the ticket comments say "the product owner accepted all N quick recommendations of that day's decision register". Default: treat them as rulings and build; the card state is not read by this sweep.
2. **HPSMPOC-480 remedy.** Default: option (a), read the app's latest deployment status once, test in the existing stub test; lane H-3.
3. **MPSCALC `lane-v*` (33) and the HTML hold.** Default: held as before; the nine server-side keys release first if the answer is no.
4. **NexusAI `viewer-write-gates` (7 ahead, 52 behind main) and `setup-column-mapping` (12 ahead).** Default: lane S restarts RD-958/964/965/966/968 from the rulings on a fresh branch off `ab5a16e9` and reads the old branch for its tests; do not rebase 52 commits.
5. **PCOMP lane A against held PR #85.** Default: PCOMP-82 first (`policy-summary.ts`, not in #85), then 52; 123 and 23 wait for #85.
6. **MPSCALC contract-name tickets (156, 161, 169, 368, 170).** Default: one lane M-A seat writes the name proposals as a document for approval; no contract change before.
7. **Records seats.** Default: one records seat per project: NexusAI (32 built-awaiting-records keys), HPSM-POC (8 "no build left"), PCOMP (74, 80, 81 built by #125), MPSCALC (173, 188).
8. **HPSMPOC-87 and HPSMPOC-91 are In Progress:** is a seat on either? Default: no seat found in this sweep (panes not read); H-4 starts only after Tuesday confirms.

## Method and disclosures

- Instruments: `jqdump.py` (board dumps, `updated >=` and `created >=` filters, `text ~ "quick recommendations"` filters; every JQL `project = <KEY> AND ( ... )` with parentheses) and `jqget.py` (issue summary, status, labels and the NEWEST comment, truncated) in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s275/sweep/`: GET-only, credentials read in-process from each project's own `4_Credentials/.env`, never printed, 0.2 to 0.25 s apart. `classify.py` there is the class-union program. `board_count.sh` was read by header only (its Jira mode takes the token as an argument); not invoked, since the helper paginates to `isLast` and the done-plus-open control above can fail. `gh api -X GET` under each project's own `GH_CONFIG_DIR`; `/usr/bin/grep` and `base64 -d` on fetched origin files.
- Limits of reading depth: for tickets whose Jira `updated` is before 2026-11-11 12:00 AEDT I carried SWEEP-1326's reading; the newest comment was read for about 100 tickets (all HPSM, PCOMP and MPSCALC candidates changed since, and all NexusAI tickets carrying the ruling note). 101 NexusAI To Do tickets and 439 NexusAI Testing/Release Ready tickets were not read.
- Outside the one-output-file rule: scratch files in the sweep folder above (helpers, TSV dumps, `cls`/`classify` outputs), and three scratch files in the session scratchpad (`dpdf.ts`, `p85.txt`, tree listings and `cls.txt`) under `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/93cac939-ff46-41b2-accf-0dacdb4f4284/scratchpad/`. No Jira write, no GitHub write, no git write verb, no hosted HTTP, no `decision_queue.sh` call, no WEDNESDAY, FRIDAY, Secuura or non-Datasec tree read. `DRAFTER_RULES.md` was read whole; its `/Volumes/Laptop-DEV` paths mean `/Volumes/Datasec_DEV` on this machine.
- READ-WHOLE-BY-TUESDAY: DONE 2026-11-15 05:5x by Tuesday s275 (BLUF, standing context, questions and method read whole; lane sections read per lane at commissioning). Q1 premise verified at source: kam_rulings_today 2026-11-11 shows 14:15 a (Composer 7, HPSM-POC 18) and 14:34 a (NexusAI 17, MPS 29). All eight defaults taken; Q8: no pane holds HPSMPOC-87 or -91 (pane list 05:43:20).
