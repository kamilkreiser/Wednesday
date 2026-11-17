STARTABLE: YES (after the Stamp; Q-1 is the one answer that could void it)

# B1658 drafter report (lane H-ALIGN, SEAT-H177), 2026-11-17

## BLUF
- The grey boxes Kam circled are the UNIT SUFFIXES. One component renders them: `NumberFields` in `web/src/components/partner/RevenueCalculator.tsx` (main `5a79f8a47bac26d093fe2eb3bd55ae83817dd4ff`, unchanged at 09:15:38). The suffix box (`:220`) has `max-w-32` and no width, no `shrink-0`, no `whitespace-nowrap`; its input is `w-full min-w-0` inside a 14rem control column (`:201`). DERIVED from CSS flex (not run): the two shrink in proportion, so each suffix lands on its own width and a multi-word one (`USD / hour`) is shrunk below its text and wraps, which is the shape of the screenshot.
- Census by program (`census.py`): 16 suffixes, 8 distinct strings. Step 1 Business inputs 6 (`reps`, `customers`, `devices` x2, `%`, `USD / hour`); step 2 Engagement model 0 (radio group + checkbox); step 3 Conversion assumptions 4 (`%` x4); step 4 Pricing and attach 6 (`hours` x3, `%`, `USD`, `USD / device / month`). Longest string: `USD / device / month`, 20 characters. No other file renders a suffix box.
- Design (kit D1-D3): two class edits in the component (suffix box `max-w-32` becomes `w-36 shrink-0 justify-center whitespace-nowrap`; control column `14rem` becomes `15rem` so the input keeps 96 px); one new `describe` in `Revenue.restyle.test.tsx` (class-token pin plus unit-text equality plus a 16-box positive control); one new measured row T20 in `web/e2e/html-layout.spec.ts` (widths equal, one line, inputs and boxes line up, text fits with 12 px slack, input at least 88 px; at 1280 and 390). Property-first: any shape meeting P1-P6 is allowed; if 9rem fails P4 on the seat's measurement the rule is the next width up with the column at suffix + 6rem.
- Verification of the commission's reading: the PNG shows the loop round the right-hand column of step 1 only (suffix boxes and the right ends of the inputs); the helper sentences sit at the left, outside the loop, and are already left-aligned. Both are `text-fg-muted`, so Q-1 is asked with the suffix reading as the default.
- Seat gate burden beyond the commission: the revenue rows of `playbook-partner.spec.ts` (axe and no-side-scroll walk) in `playbook-desktop` and `playbook-mobile` with `--no-deps`, because a fixed-width suffix is what could push the control past a phone's width; plus the infra scans (DRAFTER_RULES fence 8) and the CI audit steps.

## Facts re-measured (instrument; control)
- Main: `gh api -X GET commits/main --jq .sha` -> `5a79f8a4...` at 09:06:56 and again 09:15:38 (sidecar line S28 and this report).
- Open PRs 0 (control: closed list #330 #329 #328, S28). `matching-refs/heads/b1658` 0 (control: `heads/b1639` 2). Branch pattern list printed three names (b916 binding-rule, b945 revenue, b1535 messaging alignment); none opened for this work (the kit makes a hit that touches the suffix box a STOP).
- Ports: 9890-9899 0 listeners (control: unfiltered list 22 rows); word-boundary scan `989x` 0 files over the 46 non-`.pre-` SEAT kits of 16-17 Nov (control: `997x` 3 files). Pane list: tuesday, Datasec/NexusAI-N143, fleet-monitor.
- Toolchain: project node `v24.21.0` (`.tools/node24/bin/node --version`), `web/.nvmrc` 24, Playwright `chromium-1243` in `.tools/ms-playwright`, `.tools/bicep/bicep` present. `.tools/b1658` does not exist; `.tools/b1650` does (an earlier seat; not this work).
- No test reads the suffix box (0 over both unit files and 0 files over `web/e2e`; control 2 lines in the component); no screenshot-baseline test exists (0 files; control `toBeVisible` 57 files), so a layout change cannot turn a baseline red.
- Template: the nearest HPSM web e2e/UI kit is B1571 (a11y journey margin: ports, e2e shard and CI-predicate form); B1639 for lock, toolchain, REFUSE/HOLD form and the landing artefacts; its STATUS ends `READY B1639` (both branches pushed, #329 and #330 are the closed PRs). Measured-layout form copied from `html-layout.spec.ts` (T01-T19).
- stamp_check: 23 claims, 23 measured, rc 0. 36 S-lines in the sidecar carry the source text of every frozen pointer.

## D-decisions
- D-1: a new unit row appended to `Revenue.restyle.test.tsx` rather than a new test file (reuses its mocks and the `tokens` helper; smaller diff).
- D-2: a measured e2e row T20 in the existing `html-layout.spec.ts` (the project's home for measured layout rows; no new file, so no shard-list change beyond what `--check-shards` verifies).
- D-3: centred text in the box (`justify-center`) so equal boxes do not look ragged; styling only.
- D-4: the draft design refuses to change any unit string, label or hint (P6 by program in Step 5).

## Q-questions for Tuesday (each with a default)
- Q-1: Does "grey descriptions" mean the unit suffix boxes (default) or the grey helper sentences under each label? Evidence for the suffix reading is above; if helper sentences, the kit is void (REFUSE 6) and a new kit is needed.
- Q-2: Accept D1 as written (9rem fixed box, 15rem control column, with the next-width-up rule if P4 fails)? Default yes. Trade-off to know: the label column loses 1rem.
- Q-3: Include the measured e2e row T20 (touches the shared `html-layout.spec.ts`, which only this lane owns today)? Default yes (the commission asks for a measured layout check if the project has one; it does).
- Q-4: No ticket exists (not searched). Default: no key in the commit; a records seat may open one after landing.
- Q-5: Seat does not deploy; UAT update only on Kam's word, asked by Tuesday after the merge. Default as written.
- Q-6: Gate G2 as commissioned, but `model-routing.md:109` defines G2 as "tests-only, spec-only, docs, config/CI ..." and this changes a visible look going to a client-facing UAT site; G1 is "anything handed to a client tester". Default G2 (the commission); Tuesday may raise it.

## Chain inputs table (each input is produced by an earlier step or exists at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | the kit copy, clone, `npm ci` | BASE / Step 0 |
| 1 | repo state, pointers | BASE |
| 2 | `npm run build` output, `measure-suffixes.mjs`, dev server on 9892 | Step 0 (clone, deps) then Step 2 itself |
| 3 | base build (Step 2) for T20; owned test files | Step 2 / BASE |
| 4 | tests (Step 3), D1 edit, a rebuilt build (the e2e reads the production build) | Steps 3, 4(a) |
| 5 | the three diffs | Steps 3, 4 |
| 6 | the head build, `base-unit.json` | Steps 2, 4(b) |
| 7 | all green results | Steps 3-6 |

## UNMEASURED
- Rendered widths at base and head (no browser run; the drafter made no build). The 9rem choice rests on a glyph-count estimate (about 110 px of text plus 17 px padding and border for the longest string), marked DERIVED in the kit; the seat's Step 2 and P4 slack decide it.
- That `USD / hour` wraps at the seat's viewports (RELAYED from the screenshot at the product owner's browser; the kit's Step 2 STOP covers the case that nothing differs).
- The product owner's UAT site text (no hosted request made).
- Whether `w-36 shrink-0` reproduces correctly under Tailwind 4's generated classes in the build (the seat's green runs measure it).

## Outside-the-fences disclosure
- Read: the commission, DRAFTER_RULES, the B1639 and B1571 kits and B1639's STATUS tail, `model-routing.md`, `models_latest.json`, `brief_seat.sh` line 31, `stamp_check.py` header, the screenshot PNG.
- Network: `gh api -X GET` only (commits/main, pulls, matching-refs, branches, commits?path, the tarball of main, under the project's `GH_CONFIG_DIR`). No hosted site contacted. `lsof` and `tmux list-panes` read-only.
- Writes: the tarball and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s285/b1658/` (`src/`, `census.py`, `measure.py`, backups of earlier sidecar skeletons, a `.bak` from one `sed -i` I ran on my own scratch `census.py` before re-reading the no-`sed -i` rule; it touched no project file); the kit, its sidecar and this report. Earlier sidecar skeletons were moved aside by `os.replace`, never deleted. Nothing in `!CODING` was written.
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-17_B1658_SEAT-H177_hpsmpoc-lane-revenue-unit-suffix-alignment.md` (148 lines), sidecar `...alignment.md.measured`.

DRAFTED B1658: kit 148 lines, sidecar rc 0, questions 6
