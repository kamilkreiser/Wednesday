STARTABLE: YES (P0 closures and P1 and P3 run without a ruling; P2 (432) and P4 (468) wait for the RELEASED slot, see D-2 and D-3)

# B1497 DRAFTER REPORT: SEAT-H157, HPSM-POC lane H-A (customer workspace look and accessibility: HPSMPOC-439, 357, 432, 409 item 2, 461; plus 399's two open clauses and, conditionally, HPSMPOC-468)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1497_SEAT-H157_hpsmpoc-lane-ha-customer-look-a11y.md` (135 lines) and its identical `.pre-stamp` (`cmp` silent). Written 2026-11-11 14:13-14:2x AEDT.

## BLUF
- **H-A is valid at source, but half of it is already built.** SWEEP-1326 read the tickets from records comments that predate the landings:
  - **439 is BUILT AT MAIN** by PR 300 (b1392, squash 0820efe9, merged 2026-11-10 07:02 AEDT; its message: "Recent activity: the detail line sits 3 px under its title in 120 of 120 rows (was 23 px in 36 linked rows)"). Jira 439 was last updated 2026-11-03.
  - **357 is BUILT AT MAIN** by PR 244 (7365165d). Only its UAT half is open, and that half is a hosted measurement no seat can make while UAT is held.
  - **399 is fully built at main, and the ticket does not know it.** Its 2026-11-04 comment calls B908-7 (390 px plus letter spacing) and B908-4 (last row's menu clipped at 1024) NOT MET. But PR 244's squash message states "At 390 with 1 px body letter spacing: 400 -> 390", and PR 255 (41922a36, 2026-10-30) made the row menu `fixed`, opening above when there is no room, at 1024x768 among other sizes. The sweep sent 399 to H-B. I moved both clauses into H-A as closures, because both live in H-A files. H-B keeps nothing of 399.
- **What is left to build:** 461 (drop `max-w-3xl` from the snapshot run list, `ApiSteps.tsx:161`), 409 item 2 (diagnose the one `region` node; build only inside PlaybookShell or the snapshot components, with no word), and conditionally 432 and 468.
- **468 shares no file with any live lane.** No HPSM build seat is live: the panes show C93 (Composer), M113 (MPS) and the coordinator. B1493 (records) is the only HPSM seat with a STATUS today, and it writes to Jira and the analysis repository only. B1496 (H156, not launched; no STATUS file) owns four register files, disjoint from mine. 468 fits a Sonnet web seat. **C-270 does not name the walkthrough** (see D-3), so the kit holds 468 behind the RELEASED slot.
- Sonnet row C2 (line 92), ports 9650-9659, branch `b1497/hpsmpoc-customer-look-a11y`, no PR, nothing deploys.

## Facts re-measured (instrument; control)
- **Jira** (Python REST GET `/rest/api/3/search/jql` and `/issue/<key>`; credentials read in-process from the project `.env`, never printed). JQL `project = HPSMPOC AND ( key in (HPSMPOC-439, HPSMPOC-357, HPSMPOC-432, HPSMPOC-409, HPSMPOC-461, HPSMPOC-468, HPSMPOC-399) )` returned 7 rows, all Backlog, at 14:13:49 AEDT. Control: `key in (HPSMPOC-99999)` returned 0 rows. Last updated, with comment counts:
  - 468: 11-11 13:59, 0 comments
  - 461: 11-10, 0
  - 439: 11-03, 0
  - 432: 11-02, 0
  - 409: 11-02, 1
  - 399: 11-04, 5
  - 357: 11-01, 3
- **Code main:** `009421a28616c8b31dde86b59d4c4ca674c288fa`, unchanged from the morning (`gh api -X GET .../branches/main`, 14:14:24 AEDT). Check-runs: success 21, skipped 1. Open PRs: 0 (control: `pulls/99999` 404). `git/matching-refs/heads/b1497` length 0 (control: `heads/b1463` length 1). Tree: 1525 blobs, truncated false.
- **Origin branches b1440, b1441, b1442, b1463 and b1464 are all merged** (PRs 304, 305, 307, 308, 306, closed with merged_at set). SWEEP-1326 left this UNMEASURED. b1464 touched `steps.test.ts` and is in main.
- **Landings, each checked by `commits/<sha>/pulls`, then `compare <sha>...009421a2` status "ahead" with behind 0:**
  - 439: 0820efe9 = PR 300 (ahead 6). Files: EngagementOverview.tsx, `residualLinks.targets.test.tsx`, mock files.
  - 357 and 399 B908-7: 7365165d = PR 244 (ahead 64). Its parts.tsx patch is `whitespace-nowrap` -> `md:whitespace-nowrap`.
  - 399 B908-4: 41922a36 = PR 255 (ahead 56).
  - At 94274a75 (the B908 read), `CustomerManagement.tsx:67` read `absolute right-0 ... mt-1`. At 41922a36 and at main the list is `fixed`, with the flip at `:95` and the list at `:114` at main.
- **Pointers in the kit:** every `file:line` comes from `/usr/bin/grep -n` over raw files fetched by `gh api -X GET contents/<path>?ref=009421a2`, printed at 14:20:31 AEDT. Pointers that moved since the tickets were written:
  - 439: the ticket says `:241` and `:221`; the comment is now at `:242` and the link at `:247`.
  - 432: `FindingDetail.tsx:171` and `:173`, unchanged since 55e6063c.
- **461 reading:**
  - `ApiSteps.tsx:161` is `<ol className="flex max-w-3xl flex-col gap-2">`. `max-w-3xl` occurs 2 times in ApiSteps (`:97` and `:161`) and once in `FollowUpPanel.tsx:99`.
  - `CustomerShell.tsx:189` is `<section aria-label="Customer engagement" ...>` and `NextStep.tsx:19` is the full-width row.
  - `AssessmentScreen.tsx` renders `ApiAssessments` when the customer has no held assessment.
- **409 item 2 (DERIVED only):**
  - `PlaybookShell.tsx:19` is the outer div, `:20-25` the top line (link and `modules-viewed`), `:26` `<main id="main">`.
  - `(app)/playbook/layout.tsx` wraps every `/playbook` page in PlaybookShell, the snapshot runner and result included.
  - `PlaybookShell.test.tsx:21` pins "no navigation landmark" and one `main#main`, so a `<nav>` fix is excluded by an existing row.
  - `AppShell.tsx:203` also has an sr-only `role="status"` outside any landmark on every page. Whether axe counts it is UNMEASURED.
- **432:** `TableScroll` lives at `ui/Table.tsx:13` (`role="region"`, `tabIndex={0}`, `aria-label={label}`). The precedent is `OneCustomerEstimate.tsx:19` (`TABLE_CAPTION`) and `:72`.
- **468:**
  - `steps.ts:143` is the title, `:212` the screen link "Delivery phases", `:1-2` the header ("verbatim except where noted on the step"). `steps.test.ts:29` pins the old title. `GlobalNav.tsx:50` is the menu label. `WalkthroughPanel.tsx:134` prints `{step.title}` in an h2.
  - The e2e specs read titles from `STEPS` (`playbook-walkthrough.spec.ts:7/56`, `walkthrough-uat.spec.ts:6/26`).
  - `/usr/bin/grep -rn -i -F 'service offers'` over all 66 fetched e2e files finds 1 hit, a comment at `playbook-partner.spec.ts:1`. Control: 'delivery phases' is found in 2 specs.
  - `WalkthroughPanel.test.tsx`: 'service offers' 0 hits (control: `STEPS` 12).
- **C-270 at source:** CLARIFICATIONS.md at analysis main `830dae78` (6041 lines; `gh api -X GET` raw). Line 5278: "### C-270 - The product owner's 2026-11-02 06:09:19 AEDT ruling on the name of the old Service offers page in the new left menu: option (a), keep 'Delivery phases' and match the Home tile and sentence". The card's BLUF recommends "one name everywhere".
  - Line 6028 (C-339) records 468 as "against the ruling of entry C-270".
  - Line 3617 is the landing rule ("The landing form is a head-pinned squash").
- **HTML/v2.1 check:** `/usr/bin/grep -n -i` over DECISION-DOCUMENT.md (1872 lines) for walkthrough, service offers, delivery phases, recent activity, engagement overview, snapshot, stage, finding, landmark, scroll, 360, tile. Items that touch these pages:
  - D-056 (Delivery phases page; the HTML's heading is "Service offers"; NEXT PHASE; product owner content)
  - D-062 (customer workspace overview, "recent activity ... decide what stays"; NEXT PHASE)
  - D-065 (question screen; NEXT PHASE)
  - D-067 (finding detail "Not written yet"; THIS PHASE, words)
  - D-046 (snapshot launcher off readiness)

  None of them is the build in this kit. The kit builds no item of the document and adds no word to it. SWEEP-1326's 21 excluded HTML keys do not include 439, 357, 432, 409, 461, 399 or 468.
- **HP-tool check:** no path in the kit touches the Security Manager API, Fleet Threat Assessment, firmware tools or SIEM.
- **CI:** ci.yml at 009421a2 (682 lines). web-build steps at lines 387-426. web-unit `npm test` at :478. web-e2e matrix at :494 (8 shards), run at :518. infra job at :578-630 (shellcheck over `git ls-files '*.sh'`, `bash infra/scripts/validate.sh`). `playwright.config.ts:4` reads `WEB_PORT ?? 3100`, so the kit sets WEB_PORT in the block.
- **Ports 9650-9659:** `lsof` showed 0 listeners at 14:19:00 (control: 9 distinct listening addresses). Python range-overlap scan of the 66 non-`.pre-` SEAT kits of 10-11 Nov: only wide lists hit, and no bare number. Control: 9630-9639 hits the live B1495.
- **status_watch.sh line 56 arm** (copied into `bash -c`): `READY B1497: <40>`, `HANDOVER B1497: ...` and `STOPPED: NEEDS TUESDAY ...` fire. `WORKING:` and `PROGRESS B1497:` do not.
- **Kit self-checks (python):**
  - four-underscore count 7 (six Stamp slots plus the last line)
  - `@TOKEN@` 0
  - non-ASCII lines 0
  - decision-card ids `C-nnn` 0 (control 'x C-270 y' = 1)
  - underscore-aware name scan 0 for the owner's names and the deputy's first name (control `_by_<name>_` fired)
- **Model:** model-routing.md line 92, row C2. Id `claude-sonnet-5-5` from models_latest.json (checked 2026-11-11 13:59). Disk: 1335 GiB free.

## D-decisions (drafter's; Tuesday may overturn)
- **D-1: closures run in a build seat, with mutation controls, instead of going to a records kit.** Without a failing control, a closure is just "the code is there". The measurements need a local mock build and Playwright, which a records seat does not run. If Tuesday prefers, P0 alone is a valid smaller kit.
- **D-2: 432 is held behind the RELEASED slot.** The fix gives a region a name. The product owner ruled that pattern for the one-customer table only (C-269, line 5270). The name reuses the existing caption string, so it adds no new word, and `OneCustomerEstimate.tsx:18` says so of its own case. **Recommended default: release 432.** It is the same pattern, the same kind of string, and the ruling's reason (clears a serious axe finding) applies here too.
- **D-3: 468 is held behind the RELEASED slot.** C-270 rules the page's name and "match the Home tile and sentence". It does not name the walkthrough. The steps file states its titles are the demo presentation's own words, and the ticket's done-when allows "recorded as kept as the demo's own words". The new string is the ruled name verbatim, plus the step's existing ": Assess / Implement / Optimize". **Recommended default: release 468.** C-270's card argued for "one name everywhere", and C-339 itself records 468 as against C-270. Caveat: D-056 (NEXT PHASE) shows the v2.1 HTML calling this page "Service offers". If the product owner and the deputy later adopt the HTML's naming, the page, the menu and this title would all move back together.
- **D-4: 399's two clauses go to H-A as closures,** against the sweep's lane split, because both are H-A files and both are already built.
- **D-5: 461's "snapshot tile" = the run list, and only it.** The feedback attachment is unread (UAT store; not ours). The follow-up panel and the profile card stay at 768 px and are written under HELD. The seat measures first and STOPs P1 if the edges already line up.
- **D-6: 409 item 2's fix is allowed only in PlaybookShell or the snapshot components,** with no new landmark and no name. A node in the app shell is a NEEDS-SHARED (lane H-B's files).

## Q-questions for Tuesday (each with a default)
- **Q-1:** the RELEASED slot: `432`, `468`, both, or `none`? Default: **both** (D-2, D-3).
- **Q-2:** after this seat, 439 and 399 can be moved under C-263 ("Done means merged to main, each ticket's done-when checked first"). 357's done-when names the UAT site. Default: the next HPSM records pass comments on 439 and 399 with the seat's closure lines and moves them; 357 stays open on its UAT half.
- **Q-3: port clash between two of today's kits.** B1496 (H156, HPSM, not launched) and B1494 (M113, MPS, live in pane %25) both name block 9620-9629. M113's kit says a listener is not expected. Default: re-block H156 at its stamp (for example 9660-9669, which I found free under the same scan) before it launches.

## UNMEASURED
- Every number the seat will produce: closure widths, gaps, hit tests, axe counts, and whether each mutation fires. I ran nothing.
- Which element the 409 item 2 `region` node is, and whether it still exists at main. It was measured at feb3da65 (10-31); PR 286 (shell) landed after that.
- Whether the snapshot run list appears for an API-backed sample customer on the mock build (P1's precondition).
- Which element the feedback's author meant by "snapshot tile". The attachment is unread.
- Whether `residualLinks.targets.test.tsx` goes red under the 439 mutation.
- Whether `customer-text.test.ts` scans `steps.ts` literals (vitest whole covers it).
- The 432 axe count at 360 at main. It was measured at 55e6063c; FindingDetail.tsx has not changed since 10-30 (edf36342).

## Outside the fences (disclosure)
- Scratch files went to `/tmp/b1497d/`: helper scripts `jq.py` and `ports.py`, ticket texts, raw source files fetched by `gh api -X GET`, the tree listing, and CLARIFICATIONS.md. Nothing went in any project folder. I will remove the folder at the end.
- I wrote three files (kit, `.pre-stamp`, this report), as the brief asked. The rules file says two.
- No Jira write, no GitHub write, no git verb in a project repo except one `--no-optional-locks remote -v` on the local analysis checkout. `decision_queue.sh`, `briefs_staged/`, the scoreboard, `_ledger.md` and the WEDNESDAY/FRIDAY trees were not read.
- Two shell calls were refused by hooks: one contained `cd`, and one had a bare `======` separator. Both were re-issued without them, and nothing ran from the refused calls.
- The rules file names `/Volumes/Laptop-DEV`; this drive is `/Volumes/Datasec_DEV`.

READ-WHOLE-BY-TUESDAY: ____
