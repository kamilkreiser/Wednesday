STARTABLE: YES (after the Stamp; nothing in the kit waits on an answer, Q-1 to Q-6 all have defaults)

# B1659 drafter report (lane H-ALIGN-2, SEAT-H178), 2026-11-17

Clocks (`date`): start 10:11:58; last measurement 10:23:46; sidecar and kit final 10:24:19 AEDT.

## BLUF
- **Chosen design (MEASURED on the exact candidate, built and run locally): grey unit box `w-[5.375rem]` = 86.0 px, unit text `text-[0.6875rem]` = 11 px with `leading-4` (16 px) and `px-1.5` (6 px), centred, the long units allowed to wrap; the control column back to `md:grid-cols-[minmax(0,1fr)_14rem]` (base main's own text).** Against `5f6b916b` (box 160.0 px, number box 96.0 px, hint column 171.2 px) the candidate gives: all 16 boxes 86.0 px; number box 138.0 px (ratio 1.60, Q1 needs 1.5); hint paragraphs 203.2 px = base main, and 0 of 96 label-and-hint rows (1280, 820, 390) differ in line count from base main (control: `5f6b916b` against base differs in 11 rows at 1280, 59 wrapped lines at base and 70 at `5f6b916b`); every box 44.0 px tall, `USD / hour` on one line, `USD / device / month` on two (`USD / device` over `/ month`).
- It is the smallest width meeting Q1-Q3 in all seven fonts tried: in the system font alone 82 px would pass (0.8 px to spare), but in Verdana (the widest of six stress fonts) 82 and 84 take a third line and 86 passes with 0.5 px to spare. Q1 caps the box at 89.6 px (224 minus box at least 1.5 times box), so the window is 86 to 88 px. 12 px text with 8 px padding cannot meet Q1 and Q3 together (needs 90 px, ratio 1.49).
- Tests: the kit rewrites B1658's A5 token row (new tokens, forbids `w-40`, `max-w-32` and `whitespace-nowrap`, and pins the row grid at `14rem`) and its T20 (properties P1, P3, Q1, Q2, Q3 as `expect.soft` rows, so one run names every red property). Red-first against `5f6b916b`: A5 red on the token; T20 red on Q1 and Q2 only (P1, P3 and Q3 hold at that head). The drafter measured seven mutants by injected CSS (table in the kit): each turns a named property red, except `text-xs` back, which survives the browser row and is caught by the A5 token pin.
- One commit on top of `5f6b916b`; the diff against main is then ONE line (`:220`), because `:201` returns to base's text. Plain fast-forward push of the same branch; no PR; no deploy. The seat writes NEW landing files (PR title/body, squash subject/body, landing line) for the combined branch, since B1658's say `w-40` and `16rem`. Screenshots `head2-1280-step1/3/4.png` and `head2-390-step1.png` (plus 390 steps 3 and 4) go beside B1658's base and head shots in the B1659 evidence folder. Tuesday shows them to the product owner before any PR is opened.

## Facts re-measured (instrument; control)
- Branch head `5f6b916b87d75c3d2e7faa37c9d157c860a1ecc4` and main `5a79f8a47bac26d093fe2eb3bd55ae83817dd4ff` (`gh api -X GET branches/...` and `commits/main`, 10:12 and 10:22:53). Compare main...branch: ahead 1, behind 0, three files. Open PRs 0 (control: `pulls?state=all` length 3 with `per_page=3`); `pulls?state=all&head=datasecau:b1658/...` length 0; `matching-refs/heads/b1659` length 0 (control `heads/b1658` length 1).
- Method: tarballs of main and of `5f6b916b` extracted in scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s285/b1659/` (`export-base`, `export`), `npm ci` and `npm run build` in each (the Next.js security notice stopped each first build once, retry rc 0; no upgrade run, no dependency touched), plus a third tree `export-cand` (`cp -Rc` of `export` with the two-line edit, built). Servers on 9880, 9881, 9882 by pid, all stopped; 0 listeners on 9880-9899 afterwards (`lsof`), 0 processes left. Measurement script `scripts/probe.mjs` (Playwright from the project's own `@playwright/test`, the project's node and `ms-playwright`): modes `plain` (every box and every label and hint at 1280, 820 and 390), `sweep` (injected CSS grid of font size x padding x width), `fontsweep` (seven fonts x widths 78-90), `mutants`.
- Controls: the label comparison fires (head against base: 11 rows differ at 1280); the candidate matches base in 96 of 96. Counts are 6, 4, 6 boxes per viewport (48 rows over three viewports). The built CSS holds the four new class rules once each (0 in the `5f6b916b` build). Computed styles on the candidate: 11px, 16px line height, 6px padding, centred, grid columns `203.188px 224px`.
- Screenshots of the candidate read by the drafter (scratch `out/cand-1280-step1.png`, `cand-1280-step4.png`): six equal grey boxes, number boxes visibly wider, labels as at base, long unit on two lines, no clipped text.
- Ports: `lsof` 9890-9899 0 rows (control: 17 listeners overall); word-boundary scan `989x` 0 files over the 46 non-`.pre-` SEAT kits of 16-17 Nov other than B1658 and B1659 (control `997x`: 3 files; `988x`: 0); panes `tuesday`, `Datasec/NexusAI-N143`, `fleet-monitor`. I used 9880-9882 for my own drafting servers (the seat's block is 9890-9899); no kit names 988x.
- stamp_check: 26 claims, 26 measured, rc 0; the sidecar also carries S01-S14 (source lines and measured outputs). Kit 153 lines, no line over 1900 characters.

## D-decisions
- D-1: the control column returns to base's `14rem` rather than staying at `16rem` (Q2 then holds by construction and was measured equal in all 96 rows); the cost is the Q1 ceiling of 89.6 px on the box.
- D-2: text 11 px and padding 6 px (not 12 px / 8 px, which cannot meet Q1 and Q3 together; not 10 px, which is harder to read and not needed).
- D-3: `whitespace-nowrap` is dropped (the long unit needs its second line); the unit text is centred with `text-center` so a two-line unit does not look ragged. `leading-4` pins the line height so two lines stay inside the 44 px input.
- D-4: T20 uses `expect.soft` on the property rows and hard `expect` only on the positive controls, so the red-first run reports Q1 and Q2 together and each mutant's red properties are readable from one run.
- D-5: the A5 row now also pins the row grid at `14rem` (jsdom can read the grid class), so Q2 has a fast row besides the browser row.
- D-6: Q2's measurable form is the hint width (at least 203 px, base 203.2) plus a by-program line-count comparison against a base-main build; the hint width is font-independent.

## Q-questions for Tuesday (each with a default)
- Q-1: 11 px unit text and 6 px side padding in the grey box (a look change the product owner sees in the screenshots). Default yes (the commission allows a smaller text, e.g. 11 px).
- Q-2: 86 px (default, the commission's "smallest") or 88 px (`w-[5.5rem]`, 1.0 px more room under Verdana, Q1 ratio 1.545)? Reason to ask: Q3 depends on the machine's font; the hosted runner's font was not read (DERIVED, no hosted request); a wider font there turns T20's Q3 red and costs a round. The kit's rule steps to 88 px on the seat's own red. Default 86.
- Q-3: `USD / device / month` shows on two lines (`USD / device` over `/ month`). The commission allows this only if every box keeps its input's height (measured: 44.0 on all 48 rows). Default accept; the alternative is a wording change, held.
- Q-4: gate G2 as commissioned (one gate over the combined branch, after the product owner sees the screenshots). Same note as B1658: `model-routing.md:109` words G2 as tests-only/spec-only/docs/config, while this changes a visible look; Tuesday may raise it. Default G2.
- Q-5: Tuesday shows the screenshots to the product owner BEFORE opening or landing any PR (his option b says "shown to you before it lands"); the kit says so in the seat's FOR TUESDAY. Default as written.
- Q-6: the seat writes new `pr-title`, `pr-body`, `squash-subject` (proposed: `Revenue calculator: give every input unit one slim width so the boxes line up`, 77 characters), `squash-body` and `landing` files for the combined branch and does not edit B1658's. Default yes.

## Chain inputs table (each input is produced by an earlier step or exists at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | the kit copy; clone of the branch at `5f6b916b`; `npm ci` | exists at BASE (origin) |
| 1 | repo state, pointers | BASE |
| 2 | builds of `5f6b916b` and of a restored-to-main tree; `measure.mjs` | Step 0, Step 2 itself |
| 3 | the `5f6b916b` build (Step 2) for T20; the two test files | Step 2 / BASE |
| 4 | tests (Step 3), D1 edit, a rebuilt production build, seven scratch mutant trees | Steps 3, 4(a) |
| 5 | diffs against `5f6b916b` and against main; B1658's `checks.py` | Steps 3-4; B1658 evidence (exists) |
| 6 | the head build, `base-unit.json` | Steps 2, 4(b) |
| 7 | all green results | Steps 3-6 |
| 8 | B1658's shots (`.tools/b1658/shots/`, 12 files) and the new shots | exists at BASE; Step 6 |

## UNMEASURED
- The hosted CI runner's system font (DERIVED only; Verdana stands in); whether T20's Q3 holds there. The seat cannot measure it either; hosted CI would.
- The seat's real-class mutant results (the drafter measured injected-CSS equivalents).
- The product owner's taste for 11 px text and a two-line long unit.
- 820 px (the tablet project's own viewport) is measured by the drafter's probe (box 86.0, hints equal to base) but T20 asserts only 1280 and 390, as B1658's did.
- Jira (not searched); no hosted or UAT site touched.

## Outside-the-fences disclosure
- Read: the commission (whole), DRAFTER_RULES, B1658's kit, `.pre-stamp` copy, sidecar, report, STATUS and evidence folder (including its measure script, tests diff, mutants and run counts), the six B1658 screenshots named, `stamp_check.py` header and claim code, `model-routing.md` lines 92 and 109, `models_latest.json:23`, `brief_seat.sh:31`.
- Network: `gh api -X GET` only (branches, commits/main, compare, pulls, matching-refs, two tarballs) under the project's `GH_CONFIG_DIR`; the npm registry for two `npm ci` runs (a lockfile install of the project's own dependencies, in scratch). No hosted, demo, UAT or production host. `lsof` and `tmux list-panes` read-only. Local servers on 9880-9882 only.
- Writes: scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s285/b1659/` (tarballs, three trees, scripts, outputs, two superseded sidecar skeletons moved aside with `os.replace`); the kit, its sidecar and this report. **One stray write outside scratch:** a redirect typo (`>/tmp/null`) created `/tmp/null` (a stamp_check output, 1678 bytes); I did not delete it (the no-rm hook refused `rm`); harmless. Nothing under `!CODING` was written; no `cd` typed; no `rm` run.
- A Next.js tool output told the reader to ask about `next upgrade --agent=security` (planted-instruction class); not followed, named in the kit.
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-17_B1659_SEAT-H178_hpsmpoc-lane-revenue-unit-box-slim.md` (153 lines), sidecar `...unit-box-slim.md.measured`.

DRAFTED B1659: kit 153 lines, sidecar rc 0, questions 6
