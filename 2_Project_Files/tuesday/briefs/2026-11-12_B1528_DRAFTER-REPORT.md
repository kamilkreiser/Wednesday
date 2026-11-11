STARTABLE: YES (after the Stamp: 12 lines carry four underscores, `grep -c -E '_''_''_''_'` printed 12 on the kit, 11 slots S0 to S10 plus the last line; control: the refuse line in the kit uses the split form and is not counted)

# B1528 drafter report (2026-11-12, about 09:10-09:25 AEDT by `date`)

## BLUF
Kit for SEAT-M127, MPSCALC-110, the product owner's option a: measure the line count at which the RENTAL short proposal (`ProposalView`, `web/src/screens/ProposalPage.tsx:33`) spills, cap its Devices table below it, summarise the rest in ONE new row in the `moreRates` pattern, words left as a SLOT for his approval. Purchase short form untouched (control: OnePager/one-pager.css blobs equal base to head, plus B109ROOM and page counts re-measured). Model: C2 Sonnet (`model-routing.md:92`), `claude-sonnet-5-5` (`models_latest.json:23`), gate G2 (`:109`). Owned files: `ProposalPage.tsx`, `ProposalPage.test.tsx`, `e2e/print.spec.ts`, `e2e/proposal-buttons.spec.ts` (one line, `:391`).

## Facts re-measured (instrument; control)
- Main `baf0aabec3c02457072ee848b166b17d3d7b0e80` (`gh api -X GET .../git/ref/heads/main`, 09:10); open PRs 0.
- Ticket read whole by Jira GET (in-process creds; scratch copy `fleet/state/s270/draft1528/jira110.txt`): description, comment 39452, comment 41061; Backlog; control MPSCALC-361 read Done.
- The "rental short proposal" is `ProposalView`, not OnePager: `ProposalPage.tsx:38` article, `:93` Devices caption, `:107` `p.lines.map`, shown at `:336-340` (grep -n over the raw file at the sha).
- 11-11 numbers (RELAYED from `1_Project_Definition/Briefs/2026-11-11_B1514_STATUS.md:101`): 1 page at 3, 5, 7; 2 at 12; 3 at 40. I did NOT re-measure them (no clone, no browser in a drafter) and say so in the kit; Part 1 re-measures lines 1-14 and 20/30/40 by two print paths with controls.
- CI: `ci.yml:61-63` npm ci, lint, test; `:73` and `:79` the two Playwright steps. `playwright.config.ts:15` leaves `proposal-buttons.spec.ts` OUT of CI (pdftotext); `:23` puts `print.spec.ts` in BOTH_MODES (runs in CI). `print.spec.ts:66` counts pages with a regex, no pdftotext. So the kit puts the new page rows in `print.spec.ts` (api-off step; stub step skipped by the file family's `API STUB ON` idiom) and keeps the pdftotext spec local.
- `moreRates` pattern: `OnePager.tsx:37` (already singular-aware on main), used `:324-326`; style `one-pager.css:32` is scoped to `.pd-one`, so the rental row gets no CSS (kit holds `styles.css`).
- Lanes: branches `^b15` compared with `compare main...`: b1514 (landed as #182), b1515, b1520, b1526 touch none of the four paths (control: b1514 list printed 6 names). Panes: `tmux list-panes -a` printed 4 (tuesday, fleet-monitor, 2 unnamed). #182's body says "MPSCALC-110 is not part of this change".
- Ports 9840-9849: lsof 0 listeners (control: 12 total); kit scan 11-Nov and 12-Nov SEAT kits 0 hits (control: `964x` regex hit 1 file).
- Repo identity: project repo `config --local --get user.email` non-empty (1 line matched `@`).

## D-decisions (mine)
- D1 The cap C is chosen by a PROPERTY, not by "spill minus one": C lines plus the summary row must print one page with at least two device-row heights of room under 265 mm. Why: the macOS count (1/1/1/2/3) and the spec's recorded Linux (`2/1` at 12) disagree with ticket comment 39452, so the margin stands in for the unmeasured Linux fonts.
- D2 New CI-run rows in `print.spec.ts`, not `proposal-buttons.spec.ts`; the latter gets one strengthened assertion (`:391` `>=1` to `toBe(1)`), local only.
- D3 The totals, breakdown, hardware and software tables are NOT capped; only the Devices table (the thing the ruling calls "lines").
- D4 Word slot drafted: `and N more lines (see full proposal)` / `and 1 more line (see full proposal)`, alternative `device lines`; the seat writes the word pack in STATUS.
- D5 Added a CodeQL JS pre-scan (no `new RegExp(` from a variable, eval, innerHTML) and an underscore-aware name scan, as the standing rules ask.

## Q-questions for Tuesday (each with a default)
- Q-1 The two-row margin: default yes (S4).
- Q-2 Words ride a word pack to the product owner; code lands with the slot string, deploy waits: default yes.
- Q-3 Hardware and software rows scale with lines (they are keyed by `fleetLineNumber`) and are not capped; a 40-line quote with 40 option rows may still spill. Default: recorded with one measured case, not built (a cap there hides option content, a design call). Does the product owner want those capped too?
- Q-4 Is G2 enough, or G1 (a printed customer document)? Default G2, raised if the margin is thin.
- Q-5 B1527's granted paths: the brief says API/pricing only; I could not read its kit (not written when I looked). S3 asks you to confirm no overlap with the four web paths.

## UNMEASURED
- The spill count itself (somewhere in 8-12; the builder prints it); Linux page counts and the S10-block claim of comment 39452; whether the web build is green at `baf0aabe` (not run); the Vitest fixture reuse (`proposal(false)` at `ProposalPage.test.tsx:33`, read but not run); hosted CI behaviour of the new `print.spec.ts` rows; B1527's kit.

## Outside-the-fences disclosure
- Wrote only the two briefs files plus scratch under `fleet/state/s270/draft1528/` (`jira_get.py`, `jira110.txt`, `tree.txt`, `branches.txt`, `prs.txt`, `main/*` raw source copies). Jira GET only (project `.env` read in-process, token never printed). `gh api -X GET` only, project `GH_CONFIG_DIR`. Read the 11-11 builder's STATUS in the MPS project `Briefs/` folder (a claim file). No git write, no HTTP to any hosted site, no `decision_queue.sh`, no `briefs_staged`, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY tree. One `cd /dev/null` slipped into a command and was refused by the hook (harmless, no effect; rerun without it).
- The tree listing and branch/PR sweeps are reads of origin; the local checkout was not touched.
