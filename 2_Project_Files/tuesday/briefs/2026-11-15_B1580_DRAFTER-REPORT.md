STARTABLE: NO with the drafter's default. It becomes YES once Tuesday stamps the PART-75 slot BUILD (Q-1). The kit is complete and `stamp_check.py` exits 0 (130 claims, 130 measured, 0 not measured). Every other precondition is clear. Under the default (DROP) the seat runs Steps 0 to 1 and pushes nothing.

# B1580 drafter report (SEAT-C102, Datasec / Security Composer, lane B: PCOMP-75 item (b))
Drafted 2026-11-15 from 15:52 to 16:01 AEDT (`date` printed 15:52:24 first and 16:01:11 last). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1580_SEAT-C102_composer-lane-b-end-heading-gap.md` (104 lines), plus its `.measured` sidecar (130 lines). Scratch folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1580/`. It holds `jget.py` (a GET-only Jira helper), `fill.py`, the raw files at main under `raw/`, `pcomp75.txt`, `pr85_files.txt`, `pulls_all.txt`, `tree_sha.txt`, `census.txt` and `claims.txt`.

## BLUF
- **This exact part was drafted this morning as B1559 (SEAT-C100, 08:12, at main `68975c10`) and Tuesday DROPPED it under the Guided hold.** The evidence: `NEXT-PICKUP-TUESDAY.md:140`, "Composer lane B DROPPED (Guided hold)", and `:146`, a held note on PCOMP-75 still owed to a records pass. B1559 was never stamped (no `.pre-stamp` copy), never copied into the project's `Briefs/` (0 files), and never built (`matching-refs/heads/b1559` returns 0). B1580 replaces it. I moved it to the current main, gave it the new seat, branch and ports, and re-measured every fact.
- **Nothing that mattered has changed since 08:12.** Main is now `27adb709` (PR #129). `compare/68975c10...27adb709` returns `ahead=1 behind=0 files=1`, and that one file is DEPLOY.md. The defect is unchanged by CSS reading: the nav at `GuidedWizard.tsx:527` is followed by the `<h3>` at `:724`, `.gw-sections` has `margin: 0` (`guided.css:153`), `.gw-card h3` has `margin: 0 0 6px` (`:45`), and `gw-sections-nav` is in no stylesheet (0 hits, control 1). On Jira, PCOMP-75 still has 0 comments (control: PCOMP-127 has 2), no `held` label, and has not been updated since 2026-10-23. `CLARIFICATIONS.md` names PCOMP-75 0 times (control: PCOMP-128 appears 17 times), and nothing written after `:2600` lifts the hold.
- **The fix is small:** one CSS rule, `.gw-end .gw-sections-nav + h3 { margin-top: 16px }`, placed above `@media print` because b58's print-slice test reads everything from `@media print` to the end of the file. It comes with two new test files. No word changes, no migration, no contract change, and no DB suite. The census of the 421 web files (all 421 proven equal to main by blob sha) finds 0 tests to rewrite.
- **What blocks it is the hold, not the code.** COMP-2 (a) at `CLARIFICATIONS.md:1298` says "No Guided work until you turn it back on." Its row list does not include #76 (PCOMP-75), so how far the hold reaches can be argued. But Tuesday has read it as covering 75 twice: B1495 on 11-11 and s275 this morning. The commission's "keep going with the tickets" is a standing word, not a ruling on Guided. None of the five rulings of 2026-11-15 names Composer. So I kept the default at DROP and left the call to Tuesday.

## Facts re-measured with instruments (each with its control; every line is in `.measured`)
| Fact | Instrument | Result |
|---|---|---|
| origin main | `gh api -X GET commits/main` | `27adb70991ff3d7ec13f0732de6ecdcb1aab8043`, 2026-11-15T02:16:26Z, author `kamilDatasec` / `88359143+kamilDatasec@users.noreply.github.com`, parent `68975c10` |
| change since B1559 | `compare/68975c10...27adb709` | ahead 1, behind 0, 1 file (`DEPLOY.md` +9 -3) |
| open PRs | `pulls?state=open` | 1: #85, a draft on hold; its 57 files include 0 `apps/web` paths, 0 `guided.css`, 0 `GuidedWizard` (control: `document-pdf.ts` 1) |
| prior work | `pulls?state=all`, every page (129 PRs), case-insensitive scan | hits #13 and #31 only, both old End-page work, neither this gap (control phrase 1); refs b1580 0 and b1559 0 (control: b1569 1); newest commits: `guided.css` `3a4d1668` (10-06), `GuidedWizard.tsx` `6e458e7d` (10-09) |
| ticket | Jira GET (my own helper, run with `-I -B`, token never printed) | Backlog; labels `composer-seed-1023`, `plan-comp-76`; 0 comments (control: 127 has 2); (b) "Still OPEN" |
| pointers | `awk NR` / `grep -c -F` over raw files at main | `GuidedWizard.tsx:705/:717-:721/:724/:517/:527/:528`; `guided.css:42/:45/:151/:153/:223/:784`; candidate gaps `:134-:135`, `:340-:341`, `:113/:117`, `:546-:547` |
| census | 272 test or spec files among the 421 web files at main (blob sha 421/421 equal; a mutant control compares unequal) | `gw-card h3` in 0 test files (control: the CSS has it on 1 line); `gw-sections` in 2 files (one wizard markup row, one e2e print row); b58 `:404`/`:408` print slice. Rows to rewrite: 0 |
| CI | `scripts/ci.sh` (144 lines), `package.json`, `vitest.config.ts`, `docker/Dockerfile` | `:118` image, `:119` ci:node, `:120` db; 0 `playwright` lines (control: `docker` 13); the workspace project includes `apps/*/src/**/*.test.{ts,tsx}`; node is `node:22-bookworm-slim@sha256:83f487e0...` inside the image; the Composer `.tools/` has no node* or dotnet* entry |
| ports 9950-9959 | `lsof` (no output, rc 1; control: 23 listeners); word-boundary scan of the 28 non-`.pre-`, non-`.measured` SEAT kits of 11-14 and 11-15 | 0 hits (control `99xx`: 7 files) |
| panes (15:55) | `tmux list-panes -a` | no Composer pane; live: N131, M140, H166, M138, M139, N130, tuesday, fleet-monitor, plus unnamed panes |
| seat id | `ls briefs \| grep -o SEAT-C[0-9]+ \| sort -V` | highest C101, so this is C102; B1581 is commissioned as C103 (RELAYED from the commission) |
| model | `model-routing.md:92` (C2), `:109` (G2); `models_latest.json:23` | claude-sonnet-5-5; the launch line puts `BRIEF_SEAT_LEVEL=sonnet` inside the quotes (`brief_seat.sh:31` defaults to opus) |
| lock | `ls -d` | `.tools/composer-heavy.lock` absent; `.tools/b1580` absent; `.tools/b1551/scripts/heavy.sh` 1724 bytes, with 3 lines naming b1551 or c99 |
| load at 15:57 | `LC_ALL=C uptime` | 22.27 20.68 18.58: just under the gate of 24, so expect lock and load waits |
| landing rule | `grep -n -o -F` over `CLARIFICATIONS.md` | C-101 (1) is quoted at `:1799`; the latest landing, C-149, is at `:2806` |

### Inputs of the chain (each comes from an earlier step or exists at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | the kit, the project repo, the deploy key, B1551's `heavy.sh` | kit file; repo; `.tools/b1551/scripts/heavy.sh` (exists) |
| 0b | origin refs, PRs, Jira | read-only GETs |
| 1 | `guided.css`, `GuidedWizard.tsx`, the b104 and b58 tests in the clone | BASE (the Step 0 clone) |
| 2 | clone at BASE, Docker, heavy lock | Step 0; DOCKER slot |
| 3 | base counts, b104's `rule()` helper, b58's harness | Step 2; BASE files read in Step 1 |
| 4 | `runs/base.json` (Step 2), `runs/head.json` (made in this step) | Steps 2 and 3 |
| 5 | the Step 3 commit, the Step 4 results | earlier steps |

## D-decisions
- D-1: I rebuilt B1559 rather than writing something new. Its method was sound and its facts still hold at the new main (proven by compare). What changed: seat C102, `b1580` paths, ports 9950-9959, BASE `27adb709`, a toolchain-by-PATH line (DRAFTER_RULES, added today), a partition and lock-sharing line for the sibling B1581, an extra GAP slot, and a moved-main note because B1581 may land first.
- D-2: The rule goes above `@media print`, because of the b58 print slice (`:408`).
- D-3: The PART-75 slot defaults to DROP, following the two DROPs Tuesday already made.
- D-4: The DB suites stay out of the seat's predicate (CSS and web tests only). The gate may add them.
- D-5: I removed the deploy-rule quote's personal name from the kit text (fence 7). The kit cites `CLAUDE.md:30` instead.

## Questions for Tuesday (each with a default)
- **Q-1. Does the Guided hold (COMP-2 (a)) cover PCOMP-75 (b), and does today's "keep going with the tickets" lift it?** Default: the hold covers it and the word does not lift it, so stamp DROP and do not launch. This is the same call s275 made at 09:2x. One word unlocks the build: BUILD in the PART-75 slot, decided by you or by a product-owner card. Suggested card text: "Build a CSS-only gap above the Guided End page's 'Still to answer' heading while Guided stays switched off? No word changes."
- Q-2. The gap value. Default `16px`, the same as `.gw-handoff` at `guided.css:547`. The alternatives are printed in FACT 3. Stamp it in the GAP slot.
- Q-3. The gate. Default: G2 (tier 2), with the DB suites left out of the seat's predicate. Name them if you want the gate to run them.
- Q-4. B1559. Default: treat it as superseded and do not launch it (it is your file, so I did not touch it). If DROP stands, the owed records item still applies: a records seat should give PCOMP-75 a `held` label or comment, so the next sweep stops listing it as actionable (it was listed in SWEEP-0535 and in this commission).

## UNMEASURED
- Docker, build, lint, tests and base counts at this main. The 315 files / 3177 tests and the 2 SOW reds are RELAYED from the B1551 and B1495 STATUS files at earlier mains.
- Any render of the End page, including whether `</nav><h3>` really sit next to each other in markup. The kit makes row (d) a guard and tells the seat to STOP if it is red at base.
- The `apps/api` and `packages/db` test trees. The seat's Step 1 git grep covers them.
- `git ls-remote` through the deploy key (I used `matching-refs`), hosted CodeQL, and the Docker daemon state (fence: no docker).
- Whether Guided is switched on today. The records only ever say OFF.
- Whether any decision card about the Guided hold is pending: I listed no cards (fence 1) and knew no exact id to `show`.
- B1581's actual paths: its kit did not exist when I drafted (`ls briefs | grep B1581` printed nothing). The partition rests on the commission's lane-A scope.

## Disclosure (outside my files)
I wrote only the kit, its `.measured` sidecar, this report and the files under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1580/`. Network access: `gh api -X GET` under the Composer `GH_CONFIG_DIR`, and Jira `GET rest/api/3/issue` for PCOMP-75 and PCOMP-127 through my own helper, with credentials read in-process and never printed. I read the following read-only: the Composer folder (`CLARIFICATIONS.md`, `CLAUDE.md:30`, the B1495 and B1551 STATUS files, the `.tools/` listing, `heavy.sh`, the B41 evidence file listing); s275's drafter scratch (`d_complb/web`, used only after checking each file's blob sha); and the Tuesday kits, sweep, `NEXT-PICKUP-TUESDAY.md` and `brief_seat.sh`. I ran no docker, git writes, ssh, az, mail, hosted-site request or decision-card command, and touched no WEDNESDAY, FRIDAY or non-Datasec tree. Slips: three Bash calls were refused by hooks (an unquoted `======`, a zsh `for $K` word-split, and a `mapfile` under macOS bash 3). Each was rewritten, not retried unchanged. One `fill.py` f-string syntax error was fixed before it ran.

DRAFTED B1580: kit 104 lines, sidecar rc 0, questions 4
