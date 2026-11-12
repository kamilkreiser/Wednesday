STARTABLE: YES (as a measure-first kit; but read Q-1 before stamping: the kit is predicted to end in its STOP branch unless Tuesday settles the device cap or the margin first)

# B1536 drafter report (SEAT-M130, MPSCALC-110 option-table cap), drafted 2026-11-12 11:08-11:30 AEDT

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1536_SEAT-M130_mps-110-options-cap.md` (87 lines, 12 stamp slots as four underscores, ASCII only, no person name, no decision-card id). This report is the second file. Paths are written with `/Volumes/Datasec_DEV`.

## BLUF
The kit is written in the shape of the B1528 kit, with the merged #186 as the house pattern: `RENTAL_SHORT_OPTION_CAP` (or two constants if the measurement says so) and `moreRentalOptions(n)` in `ProposalPage.tsx`, a summary row in the hardware table (`colSpan={4}`) and in the software table (`colSpan={6}`), words as a slot with a WORD PACK. **The main finding: on the relayed numbers, the ruled property cannot be met.** With the devices capped at 5 (article 231.2 mm at 703 px with one row in each option table), each extra option row in both tables costs about 13.3 mm, so K=1 is about 244.5 mm (margin 20.5 mm = 1.89 device rows, 1.2 mm short of the two-row property at 243.3 mm), K=2 about 257.8 mm (7 mm left), K=3 two pages. This is DERIVED (arithmetic over the B1528 STATUS and gate numbers), not measured by me. The kit therefore measures the whole grid first (including device caps 4 and 3 as recorded columns), builds only if a K of 2 or more meets the property, and otherwise stops with the grid and ranked options.

## Facts re-measured (instrument, control)
- Main `5239020234b416c6c2c07f8a7912d88830de6f7f`, as expected (`gh api -X GET .../git/ref/heads/main`, 11:08:34). Open PRs 0 (`pulls?state=open` printed no row; the project's own prior reads of the same call printed rows when PRs existed).
- #186 content is on main: `ProposalPage.tsx:37` and `:39` are the cap and `moreRentalLines`; device cap at `:115`, summary row `:127-131`; hardware `:135-157`, software `:159-185` (`grep -n` over the raw file at the sha, saved in my scratch folder).
- Jira (GET-only helper written in the scratch folder, `jira_get.py`, JQL with the parentheses): MPSCALC-110 Backlog, updated 2026-11-11T15:04:57.995+1100, comments 39452 and 41061 only; control MPSCALC-361 read Done.
- `^b15` branches (`matching-refs/heads/b15`, 12 rows) compared `main...<branch>` for `ProposalPage|print.spec|proposal-buttons`: 0 files on each of b1502, b1508, b1510, b1511, b1512, b1514, b1515, b1520, b1526, b1527, b1530; 4 on b1528 (control fires: it is the landed #186 branch, squashed, so ahead 1 behind 2). No `b1533`, `b1534`, `b1536` ref yet.
- Live kits B1527, B1530, B1533: `grep -c -i -E 'ProposalPage|print\.spec|proposal-buttons'` printed 1, 6, 4; each hit read as "not yours" or "runs beside you"; none grants my four paths. B1533 owns `web/src/styles.css` (not touched by this kit, no CSS needed).
- Panes (11:1x): tuesday, fleet-monitor, Security-Composer-C94, MPS-M129, NexusAI-N125, MPS-M128, MPS-M126, unnamed; no `Datasec/MPS-M130`.
- Ports 9910-9919: `lsof ... | wc -l` 0, control 12 machine-wide listeners; kit scan for `991x` with the boundary regex: 0 files, control (`9[0-9][0-9][0-9]` scan) fires on 20 kits (note: my first control attempt, `984x`, printed nothing because the B1528 kit writes the block as `9840-9849`, which the regex rightly excludes; replaced by the broad control).
- Heavy locks: `.tools` listing had no `.heavy-lock-*` at 11:10 (control: the listing printed b1526, b1527, b1528, b1530, b1533). Load `LC_ALL=C uptime` 11:10: load1 4.90. `.tools/b1536` absent.
- Model: row C2 at `model-routing.md:92`, G2 at `:109`, `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh` and `launch_when_cool.sh` exist at the paths the launch line names.
- CI predicates read from `ci.yml` at the sha (`web` job `:45`, steps `:61`, `:62`, `:63`, `:69`, `:73`, `:76`, `:79`) and `playwright.config.ts` (`LEFT_OUT` `:10`, `proposal-buttons.spec.ts` at `:15`, `BOTH_MODES` `:23` with `print.spec.ts`).
- The full proposal lists every option: `RentalDocument.tsx:231-250` maps `p.hardware` and `p.software` uncapped (source reading, DERIVED), so "see full proposal" is truthful.

## D-decisions
- D-1 Property is the ruling's: devices capped at 5 plus summary, both option tables capped, at least two Devices-row heights (21.7 mm at 703 px) of margin under 265 mm on both print paths. 703 px governs (default viewport is far shorter).
- D-2 Floor K >= 2 (K=1 shows one option and a pointer for the second; a judgement, Q-1).
- D-3 One K and one function `moreRentalOptions` for both tables (the ruling's wording is one line "and N more options"); two constants only if hardware and software row heights measure more than 1.0 mm apart and a pair works.
- D-4 The cap is emulated in Part 1 as K+1 plain rows per table (summary counted as a full row, #186's conservative method), then re-measured on the real code in Part 2's POST-BUILD step; a margin below the property after the change is a STOP.
- D-5 STOP branch instead of silently lowering the device cap: lowering `RENTAL_SHORT_LINE_CAP` changes what the product owner ruled and approved in #186. The kit lets Stamp S4 carry a verbatim ruling that does it, with the only existing-line edits listed.
- D-6 `proposal-buttons.spec.ts` gets new lines only (a `rentalWithOptions` helper and a loop); the stale `R1_RENTAL_PAGES` label (gate F4) is left alone (Q-4).
- D-7 Word pack: slot `and 1 more option (see full proposal)` / `and N more options (see full proposal)`; alternative table-specific `hardware options` / `software products` (two functions). I chose "software products" for the alternative because the software table is captioned "Software" and its column is "Product".

## Q-questions for Tuesday (each with a default)
- **Q-1 (the one that matters).** The derived arithmetic says no K >= 2 meets the two-row margin at device cap 5 (K=1 misses by about 1.2 mm; device cap 3 with K=2 would pass at about 29 mm). Settle before stamping, or let the seat measure first? **Default: let the seat measure first**; the figures are derived, the grid it returns is the evidence for a card, and the kit's STOP branch hands you the ranked options. If you would rather ask the product owner now, the options are: (i) K=1 and accept 1.89 rows (or call it close enough), (ii) lower the device cap to 3 and use K=2, (iii) relax the margin to one Devices row and accept K=1 only (K=2 leaves about 7 mm, no). Put his words into S4 if he answers before launch. Also confirm the floor K >= 2 (default yes).
- Q-2 Slot words go to the product owner as a word pack; landing allowed before his word, deploy not. Default: yes.
- Q-3 Long option descriptions (the gate's F3 analogue) recorded only with one probe at the chosen K. Default: yes.
- Q-4 Leave the stale `R1_RENTAL_PAGES` label (`proposal-buttons.spec.ts:372`, gate F4) unedited. Default: yes (the ruling does not ask; the kit allows only new lines in that file).
- Q-5 Linux print UNMEASURED; hosted CI api-off is the first Linux read. Default: yes.
- Q-6 Launch window and hard stop (S5, S9) are yours; the kit says READY = Step 0 + 150 min.

## UNMEASURED
Everything in FACT 6 (the K grid) is arithmetic, not a run. Linux print. The device-row height at 703 px for rows with long option descriptions. Whether the hardware and software rows differ in height (the seat measures). Project `CLAUDE.md:50` landing rule was not re-read (the sha has no root `CLAUDE.md` at that path: HTTP 404); it is RELAYED from the B1528 kit.

## Outside-the-fences disclosure
- My first Bash call contained the text `cd` inside a variable name and the hook refused it before it ran; re-issued without it. No project repo was touched except by read-only `gh api -X GET` (contents, trees, compare, matching-refs, pulls) under the project `GH_CONFIG_DIR`, plus the Jira GET helper (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1536/jira_get.py`, GET only, token read in-process and never printed). Scratch files (raw main copies, `tree.txt`, `branches.txt`, `kits.txt`) are in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1536/`.
- I read the project `.env` only by name-match for the three `JIRA_` keys (inside the helper), the other kits only by `grep` for the four path names and by the port scan, and the B1528 kit, STATUS and gate VERDICT whole as instructed. No `decision_queue.sh`, no briefs_staged, no ledger, no WEDNESDAY/FRIDAY tree, no hosted host.
