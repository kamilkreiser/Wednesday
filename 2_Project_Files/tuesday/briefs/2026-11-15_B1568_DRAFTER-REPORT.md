STARTABLE: YES (the slice choice Q1, the reading of the RD-858 ruling Q2, the slot Q6 and the gate level Q5 need your eye at the stamp; the kit holds a default for each and STOPs on any other reading)

# B1568 DRAFTER REPORT (SEAT-N130, NexusAI lane F2, slice 1), drafted Sun 15 Nov 2026 10:55 to 11:1x AEDT (`date` at start 10:55:06, last `date` read 11:08:54 before this file was written)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1568_SEAT-N130_nexusai-lane-f2-banner-and-testing-page.md` (165 lines, 5 lines with the four-underscore slot pattern: four slots and the last line; 0 non-ASCII characters; ban-list name scan 0 with the `_by_kam_` control firing 1). Sidecar `.md.measured` (169 lines): `stamp_check.py` prints `137 claims, 137 measured, 0 not measured`, rc 0 (run alone, not through a pipe). The sidecar also carries S01 to S31 (plus S20b), each a real read at main `4ba2e03c`. Many claim lines are "a NEW literal the seat writes or runs (an instruction), 0 in the repository"; those are instructions, not claims about a file, and the sidecar says so line by line.

## BLUF
- **Slice (one Sonnet seat, about 45 min setup and edit plus about 100 to 120 min of lock hold):** **RD-532, RD-538, RD-858.** (1) RD-532: the open-site banner's z-index rises from 1100 to 10000, above both 9999 loading overlays and below the 20000 session-expired overlay (one declaration in `static/css/open-access-banner.css`), proved by a NEW real-browser measurement of the dashboard WHILE its loading overlay is up (a never-answered `/api/auth/check` holds the overlay). (2) RD-538: the 10-minute edge cell G15 in the banner guard, as Tuesday's own 2026-09-18 comment on the ticket asks. (3) RD-858: the test page's custom-SQL control (textarea, Run Edited Query, Reset to Original, their functions and CSS rule) removed, with its dependent cells rewritten into a new jsdom file. **No new words anywhere** (a hard property with a program scan in the kit).
- **Rulings quoted with comment ids:** RD-532 comment 41049 ("the open-site warning banner is put above the loading overlay, so it is never hidden while the page loads."; accepted recommendation "Yes. A security warning should never be hidden."); RD-858 comment 41041 ("the page's custom-SQL control is removed, with any cells that depend on it rewritten, not deleted."; "Remove. The page is unlinked, and its only job ended with your earlier ruling."); RD-538 comment 37764 (Tuesday's 2026-09-18 comment: the bound-edge cell at `HOLD_VIRTUAL_MS + 1`, "The first is preferable"). Card tags in the ticket text are not copied into the kit.
- **PREDICTED cells 11 (rd490 file +6: L0, L1, L2, L3, H1, G15; new rd858 file 5: T1 to T5), one new suite, pair about 5647 / 350.** Red-first PREDICTED 4 red (T1, T2, T5, L1) and 7 green (the pins). Mutations P1 to P7 in the kit.
- **How CI runs the browser guard (predicate written into the kit):** `.github/workflows/build.yml:64` `node scripts/assert-browser.js`, then `:93` `npm run verify -- --maxWorkers=2`; `scripts/verify-suite.sh:366-367` prints `VERDICT: PASS` only after every fail check and the count equality. There is NO other Playwright run in any workflow (`grep -c -i playwright` over `.github/workflows` -> no file; control `browser` in build.yml 5). The rd490 jest file is the only browser file in verify.

## Slice choice, ticket by ticket (all 21 lane keys read whole by my own GET-only reader; LEFT reasons)
IN: RD-532, RD-538, RD-858 (above). LEFT, each with its reason:
- RD-512, RD-513, RD-515: the same guard files, test-only, no ruling needed, but each can expose a REAL red on a page that then needs a design choice (dark banner colours; 375 px layout; the first-run inline note lives on a lane F1 page). They are the natural slice 2 (Q7). RD-538's cell is the only one of the family with a written fix recipe, so it is in.
- RD-175 and RD-349: the ruling comments (41048, 41047) say "fixed" / "take the same contrast ruling, measured against the ground each sits on" and give NO replacement value; the only ruled colour in the family is the tab chrome pair `#00719f` + white (RD-251), whose use on KPI labels or the toner label is a design choice nobody ruled. RD-175's dark half (a dark track for `.consumable-bar`) IS buildable by the lane note's rule, but the ticket gives `#2a2a4a` as an option, not a ruling, and the light half is open; held (Q7).
- RD-164 (dark card border 1.47:1, "one border-color value", value not ruled), RD-222 (ticket: "neither should be guessed at ... once someone rules which look to keep").
- RD-144 (tab semantics on every dashboard tab; the ticket asks for its own QA pass).
- RD-220, RD-259 (console errors on load: three of the four families are 503s and an empty query that need server answers; the TypeError and CSP families are unmeasured here), RD-832 (URLs not captured; needs a run).
- RD-261 (first step is to decide and record the intended behaviour), RD-483 (the 24 px / 32 px offsets include `legal.html`, outside lane F2's paths), RD-613 (adds the alarm banner to Settings, admin and first-run pages: lane F1 pages and a new surface).
- RD-835 (CSV formula neutralisation: the ticket itself asks for a decision on negative numbers; exported data changes).
- RD-771, RD-861 (after lane F1), RD-145 (needs the `Dockerfile`, lane T's): excluded as instructed. The front-end write-callers ticket: not kitted, as instructed.

## Facts re-measured (instrument; control)
1. Main `4ba2e03cc88e928c2c6fdf6694ebed0e7cadf2e5`, tree `b52c8378...` (`gh api -X GET .../commits/main`, 10:55 and 10:58:52); counts file at that sha 5636 / 349 (`git show`); open PRs 0; open CodeQL alerts on main 64, 6 in `static/` or `tests/` (settings.js x2, index.js x2, first-run-setup.js x1, `tests/uat-run.js` x1), none in any file the seat edits.
2. Tickets: RD-532, RD-538, RD-858 To Do, read whole with comments by `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1568/jira_ro.py` (my own helper: credentials read in-process by name from the project `.env`, never printed; every JQL it accepts starts `project = RD AND (`; this drafter ran issue GETs only) plus RD-144, 164, 175, 222, 349, 220, 259, 261, 483, 613, 832, 835, 512, 513, 515 and RD-251 (for the contrast ruling's colour).
3. Source at main, by `awk NR==n` / `git show` in my own clone (detached at 4ba2e03c, push URL `invalid://no-push-drafter`): every `file:line` in the kit is printed in S10 to S19 and the claim lines.
4. **The dashboard holds the overlay on `await checkAuthStatus()`:** `static/js/index.js:958` handler, `:925` `apiFetch('/api/auth/check')`, `hideLoadingOverlay()` at `:895` only after the data calls; no timer hides it before. The banner reads `/api/auth/status` (`open-access-banner.js:25`). So routing `/api/auth/check` to a handler that never answers holds the overlay deterministically. PREDICTED, not run (UNMEASURED); the kit makes the proof step 1's required property (L0) and a STOP.
5. **The existing guard cannot see the loading page by design** (`open-access-banner-guard.js:77-80` comment; it waits for network quiet before measuring); the new `guardLoadingPage` is the missing measurement; G14 is the nearest existing cell (a cover that never clears).
6. Slot: control `b1430-nodot/b1` -> 6 and `b1563-nodot/old12` -> 1 by my `slot.js`; slot-4 names `old52 new4 mut6 chk12 v5 chk25` each printed 4 (S20b). Live kits read at 11:07: N128 slot 1, **N129 (kit B1567, now exists) slot 7**, so slot 4 is free of both.
7. Ports: block 9850-9859 `lsof` 0 rows (11:08), control machine-wide listeners 18; word-boundary scan `985[0-9]` over the 16 other non-`.pre` SEAT kits of 11-14 and 11-15: 0 hits, control `979[0-9]` 2. Live panes at 11:0x: wednesday, N128, H164, M135, R231, fleet-monitor (no N129 or N130 pane). The rd490 file's own band 38900-38939 and the slot band 22560-23199 both read 0 listeners.
8. Landing rule quoted from `CLARIFICATIONS.md:2067` (S27); demo hold C-224 `:2412` (S25); deploy-demo `on:` `:26`, `paths-ignore` `:29`, `workflow_dispatch` `:33`, the two job conditions `:53` and `:91`.
9. **CodeQL CLI path correction:** the lane message gave `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/codeql/codeql`; that is a DIRECTORY (`ls -ld` drwxr-xr-x, an invocation read "permission denied"). The binary is `.../tools/codeql/codeql/codeql` (`-r-xr-xr-x`); the JS suite is `.../qlpacks/codeql/javascript-queries/2.5.0/codeql-suites/javascript-code-scanning.qls` (found by `find`). I did NOT run the CLI (fences: read a tool's usage, never invoke it); the kit uses the corrected paths, one timed run before the lock, a 20-minute cap, NOT RUN is allowed with a reason.
10. Prior work: 0 commits name RD-532, RD-538, RD-858, "loading overlay", "custom SQL" or `editableSqlQuery` on main (control RD-774 11); the 2 unmerged `b1480/*` branches carry 0 such messages and 0 files in the seat's paths (control: 10 and 11 files in all; 38 `b1*` refs, only those 2 ahead). The earlier front-end queue kit B1432 lists RD-532 and RD-538 in its queue table; its last line is `HANDOVER B1432: next RD-144` and its STATUS names none of the three keys as built.

## Census of existing tests pinning behaviour the slice changes (by program; frame: tracked files at 4ba2e03c; instrument `git grep -c -E` over the paths named; S26 and the claim lines)
| pattern | paths | result | status |
|---|---|---|---|
| `editableSqlQuery`, `runEditableQuery`, `resetQueryToOriginal`, `resetQueryBtn`, `runEditableQueryBtn` | `__tests__ tests scripts docs` | 0 files | nothing pins the removed control; only `static/css/testing-styles.css:47` (1 line, goes with it) |
| `Edited Query`, `Editable Query`, `Edit the SQL`, `Reset to Original` | whole repo minus testing.html and testing.js | 0 files | nothing pins the removed text |
| `testing.js`, `testing.html` | `__tests__ tests` | 2 files: `dark-mode-page-scope.test.js` 1, `rd892-testing-dropdown-null-level.test.js` 4 | rd892 pins `conditionSelect`, `statusMessage`, `originalSqlQueryBox`, `runQueryBtn` and at `:253-255` the SQL display with `runQueryBtn` and `copyQueryBtn` enabled: must stay green UNCHANGED (the kit keeps those) |
| `test-custom-query` | `__tests__ tests` | 1 file: `rd774-risk-sql-templates.test.js` 2 | server route untouched; run in step 3 |
| `1100` | `__tests__ tests` | 5 files (widths, heights, layout JSON, a hex string) | none pins a banner z-index |
| `loading-overlay`, `loadingOverlay` | `__tests__ tests` | 6 files (`dark-ground-luminance` 1, `loading-overlay-contrast` 8, `dark-mode-contrast.spec` 1, the guard 1, `overlay-cta-legibility.spec` 3, `settle.js` 1) | CSS colour pins, no z-index pin; the two jest ones run in step 3; the specs are outside verify |
| guard consumers | `scripts/assert-browser.js` (calls `launchBrowser`), `tests/e2e/rd286-ground-and-geometry.spec.js` | named in the kit | the seat only ADDS exports |
Control for the instrument: `git grep -c -F describe` over `__tests__` printed 341 files. A zero for a removed identifier was cross-checked against the nonzero count in `testing.js` (6 lines), `testing.html` (2) and the css (1).

## Chain-step inputs (each produced by an earlier step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| Commit A | BASE clone, `npm ci`, line pointers re-read | Step 1 |
| 0 browser (`new4`) | tree at A | commit A |
| 1 red-first (`old52`) | BASE tree; the guard, concealments, rd490 test and rd858 test | Step 1; commit A (copied in, `cmp`) |
| 2 new-cells (`new4`) | tree at A | commit A |
| 3 related (`new4`) | tree at A | commit A |
| 4 mut (`mut6`) | tree at A; step 2 green | commit A; step 2 |
| 5 mainmove | steps 0 to 4 green | steps 0 to 4 |
| 6 plain verify (`chk12`) | head of step 5 | step 5 |
| 7 update-counts (`v5`) | step 6's counts refusal | step 6 |
| 8 K (`wt`) | step 7's counts file | step 7 |
| 9 plain verify (`chk25`) | K | step 8 |
No step reads a file a later step makes. There is no inventory step: no route, status or handler gate changes; the kit says so and prints it in READY.

## D-decisions (drafter, at source)
- D1 The fix is the banner's z-index, not a DOM move: the banner is already first child of the body, the overlay is `position: fixed`, so a higher z-index on a `position: relative` banner is the one-declaration change the ticket itself names; the `--inline` variant's later `z-index: auto` is untouched.
- D2 10000 as the default: above 9999 (both overlays, `index-styles.css:442,1057`, `settings-styles.css:159`), below 20000 (session-expired overlay, `:1398`), and still above the 1080 widgets and 1055 modals the banner already beat at 1100.
- D3 The measurement is a sibling function `guardLoadingPage` (additions and one export only) so no existing guard check changes; the overlay state is READ into the result and its absence is a failure code, so the cell cannot pass by measuring the finished page.
- D4 G15 uses the literal 600001 on purpose; H1 pins the bound it stands on; mutation P4 (HOLD_VIRTUAL_MS lowered) makes both go red, which is the ticket's stated purpose.
- D5 RD-858 keeps the read-only SQL display, the Run Query and Copy Query buttons: the ticket text names the "hand-typed" box and rd892 pins the rest. No new string; messages that remain are the page's existing ones.
- D6 No inventory drive and no `docs/**` write: nothing in the slice changes a route answer.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q1 Slice choice.** RD-532 + RD-538 + RD-858 as the first F2 slice? **Default: yes.**
- **Q2 RD-858 reading.** "The custom-SQL control" = the editable textarea and its run, reset and CSS, keeping the read-only display, Run Query and Copy Query. **Default: this reading** (rd892 pins the rest; the seat STOPs if it thinks the ruling also removes the display).
- **Q3 Ownership.** The lane note's owns list omits `static/testing.html` and `static/js/testing.js` (RD-858 names them) and the new `__tests__/rd858-*` plus the edit of `__tests__/rd490-open-access-banner-browser.test.js` sit in lane T's tree. **Default: accept; no other live kit writes them** (N128, N129, R231 read in the kit's PARTITION).
- **Q4 Side effect.** The banner file serves every page, so the banner now also stacks above `settings.html`'s own 9999 overlay (a lane F1 page). **Default: accept** (it is the same ruling's intent; READY lists it under OWED). The alternative, scoping the rule to `index.html`, needs a DOM or body-class change.
- **Q5 Gate.** G2 by default (CSS plus tests). **Default: G2; raise to G1 if you treat the banner as a security surface** (it is the whole mitigation for the open first-run window).
- **Q6 Slot.** Slot 4, chosen to avoid N128 (1) and N129 (7, read from the B1567 kit at 11:07). **Default: keep 4; re-run `slot.js` if the lane B kit's trees change.**
- **Q7 Slice 2.** Next F2 kit: RD-512, RD-513, RD-515 (same guard files; STOP on any real red they expose) plus RD-175's dark half if you rule that half can ship alone. **Default: draft 512/513/515 next, 175 only on your word.**

## UNMEASURED
- That an unanswered `/api/auth/check` holds `#loadingOverlay` for the whole measurement (read from source only; step 1 and L0 are the proof); that z-index 10000 leaves no other fixed element above the banner on the loading page; Playwright route handlers that never answer closing cleanly on page close; the rd490 file's wall time with three extra measurements; the CodeQL pack's result on the edits (CLI not run); every cell's received value (PREDICTED 4 red / 7 green in red-first; 11 cells; pair about 5647 / 350); a hosted Build and the Deploy demo run a landing starts (must read `skipped`).
- The counts file race: N128, N129 and this kit all end on `scripts/verify-expected-counts.json`; whoever lands second is rebuilt (HOLD 20).

## Outside-the-fences disclosure
- Writes: the kit, its sidecar, this report; scratch only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1568/` (my Jira helper, ticket texts, alert list, slot program, generators, my clone). The first sidecar skeleton briefly sat in the briefs folder as `.measured.pre-fill`; I moved it to the scratch folder (three earlier skeletons are there as `measured.*-init`). One stray file `/tmp/x_sc.txt` (a stamp_check print) was written outside the scratch folder; harmless. Nothing under `/Volumes/Datasec_DEV/!CODING/`; no Jira write; no GitHub write; no git write verb in any project repo; no message; no az, ssh, docker or tmux send-keys (one `tmux list-panes` read).
- My clone: `git clone --no-hardlinks` of the PREVIOUS drafter's scratch clone (`.../fleet/state/s276/d1563/clone`, detached at the same sha) because the project's own checkout lacks `4ba2e03c`; push URL set to `invalid://no-push-drafter`; checked out detached at `4ba2e03c`; never pushed. I did not copy any helper from another seat's `.tools/`; my Jira helper is my own file.
- Reads in the project folder (read-only): `CLARIFICATIONS.md` (lines 2067, 2410-2413), `CLAUDE.md:286-293`, the Briefs folder (grep and one table read of B1432), `session-tools/nexusai-lock.sh` header, `scanlib1114.py:20` (existence and pattern shape only), the `.tools/b1555/` listing (to name the tools the kit copies), `.env` variable NAMES by my helper in-process only (values never printed). Read of other briefs: B1563 kit and report (template), B1567 kit (slot, ports, owned files), the sweep lanes file section 4, the gate standard.
- Hook events: a `cd` refused once (nothing ran); an unquoted `=====` refused once (nothing ran); one `git -C $VAR checkout` refused because the hook did not expand the variable (re-issued with the literal path inside the TUESDAY tree); several advisories on case-sensitive greps, `grep | cut` and `$?` after a pipe (none relied on). No fence was bypassed.
- `DRAFTER_RULES.md` names `/Volumes/Laptop-DEV/...`; I used `/Volumes/Datasec_DEV` everywhere. The CodeQL path in the lane message was one folder short (item 9 above).
- Weakest parts: the overlay-holding premise (item 4), the exact `guardLoadingPage` shape (properties given, code left to the seat), and the PREDICTED red-first split.

DRAFTED B1568: kit 165 lines, sidecar rc 0, questions 7
