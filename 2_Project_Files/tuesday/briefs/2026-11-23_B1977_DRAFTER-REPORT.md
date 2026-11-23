STARTABLE: YES

# B1977 drafter report (NexusAI RD-1032 light toner fills build kit)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1977_SEAT-N167_nexusai-rd1032-build.md` (573 lines), sidecar `.measured` (112 claims, `stamp_check.py` prints 112 measured, 0 not measured; the `____` count over the kit reads 5: four slots and the last line). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1977/` (trees `base`, `proto`, `redfirst`, `mut`, `applytest`, `b1977-nodot/mut21`; renders under `render/o2`, `o3`, `o4`). Read at BASE `3c3be156e8ea36ad297fdadd3055c6e00252ba38` (main re-read 11:30, unchanged).

## BLUF
- The kit builds option a: light `.consumable-fill.cyan/.magenta/.yellow` = `#0a8793`, `#b44752`, `#b57a13` flat; dark byte-identical; `surface-raised` added to the three tokens' grounds; tokens.css regenerated; one BRAND.md bullet; a new 8-cell test file; K = the counts file (PREDICTED 6243 / 395). Two commits, render leg, CQ, one push.
- **Two departures from the commission's wording, both forced by the project's own gates (Q-1, Q-4):** (1) the light rules use literal hex with the token named beside it, not `var(--nx-*)`: tokens.css is linked by no page, so a `var()` paints no fill (project rule RD-234, `index-styles.css` 704-706 and 1197-1204; guard in `brand-shell-tokens.test.js`). (2) Neither "an explicit dark rule" nor "a light-only selector" survives: a selector naming the dark state in `index-styles.css` fails `dark-mode-link-order` and `sustainability-dark-mode` (measured, 2 red); hex in `dark-mode.css` fails the RD-182 zero-debt guard (measured, 2 red). The kit's shape: light rules flat; the six old stops live as `--toner-*` custom properties in the light `:root`; `dark-mode.css` gets three rules reading them. A real Chromium shows the dark computed styles and PNG bytes identical before/after (sha256 `c94549bbea10...` both) and the light fills changed.
- **A shared path with pull request 242: `scripts/verify-expected-counts.json`** (242's head reads 6237/394; mine will read 6243/395). The commission said no shared path; that holds for the other paths only. Whoever lands second needs K rebuilt (Q-2).

## Facts re-measured with instruments
- Frozen program `apply1977.py` (10 anchors over 6 files, ASCII only) applied to a fresh BASE copy gives six blobs equal to the prototype's; `revert` gives the six BASE blobs back. BASE blobs equal GitHub's tree blobs (tarball control). Table is in the kit.
- New test (8 cells, 8850 bytes, 0 non-ASCII, indented-pattern count 8, column-1 count 0): at BASE stylesheets 4 red (L1, L2, D1, D3) / 4 green; patched 8/8 green.
- Plants MA-MG (frozen `plants1977.py`, round trip checked on a tree named `b1977-nodot/mut21`, wrong-tree control refused): each caught by name; D2 is red under none (said so in the kit).
- Gate-reading runs at the patched tree: 42 BASE-list files = 735 tests, 0 red (41 suites / 705 in one run incl. the new file, 2 suites / 30 in a second). 7-file mutation set at M0: 160/160. `runlist1977.py` at BASE prints FRAME 394 (= `suites` in the counts file: control) and COUNT 42.
- Render proof (`render1977.js`, `cmp1977.py`): 11 OK lines; control: with an unscoped plant the same compare prints FAIL on dark.
- Scans over all added lines (214) and both messages: owner-attribution 0, B-number 0, card/decision 0, existsSync / new RegExp / eval / setTimeout / .only 0; non-ASCII added 36 = removed 36 (existing em dashes in tokens.css comment lines, replaced in place); keys `RD-1032, RD-158, RD-175, RD-182, RD-234` only (drafter's list, not the project's scanner).
- Code-scanning open alerts 22, none under `__tests__/`, `scripts/`, `static/`. Deploy-demo `paths-ignore` is `**.md`, `docs/**`, `tests/**`: a landing starts a run, gated on `vars.CI_DEPLOY_ENABLED`.
- Slot-17 names: `b1977-nodot/{work4, mut21, vupd21, chk4, rnd19}` (controls 17). Band 30880-31519: 0 listeners (8 other listeners exist: control); only OXPd2 records kit B1887 mentions `31481`, as a number.

## D-decisions
- D-1 literal hex + token comment. D-2 dark rule shape via `--toner-*`. D-3 one extra edit: cell C5 of the RD-175 test resolves the `--toner-*` stops (3 added, 1 removed; no cell added). D-4 BRAND.md bullet (docs only, not forced by the gate). D-5 A then K, form of B1958. D-6 render leg owed to the G2 gate.

## Q-questions (each with a default)
- Q-1 literal hex instead of `var(--nx-*)`: default yes (the alternative paints nothing).
- Q-2 landing order and the shared counts file with 242: default land 243, then 242, then this lane (K rebuilt only if this lane lands before 242's counts move; HOLD 20 stops the seat on a move of the counts file).
- Q-3 the BRAND.md bullet: default yes (drop it and the commit loses one path only).
- Q-4 the dark rule shape through `--toner-*` properties: default yes; the alternative is amending the RD-158 and RD-182 guards, which is the product owner's guard design.
- Q-5 G2 Sonnet gate with the render leg, not G1: default yes (no security surface).
- Q-6 window: default 2 h 30 as for B1966 (two verifies of about 23-60 minutes each).

## UNMEASURED
The full `npm run verify` and `--update-counts` (counts 6243/395 are PREDICTED), CodeQL, the lock steps, the seat's tools, hosted CI, other viewports, forced-colours, print, Linux. The sidecar's 112 lines are counts of where each literal is found in 16 source files (program `fill1977.py`, control fired); those that are seat commands or tool outputs are marked UNMEASURED as outputs in their own lines. Not measured: the two e2e suites (`tests/e2e/dark-mode-contrast.spec.js`, RD-1031). A `grep` for a precedent of `:not(.dark-mode)` in stylesheets was refused by a hook and not retried (the guards' own text was read instead).

## Outside-the-fences disclosure
Read-only toward the project, Jira (not touched) and GitHub (`gh api -X GET` only: refs, pulls and their files, contents, tarball, code-scanning, trees). Wrote only the kit, its sidecar, this report and scratch under `fleet/state/s315/d1977/` (one first sidecar moved there as `first.measured.quarantined`). Ran jest 29.7.0 and Chromium in scratch trees through `NODE_PATH` from `.tools/b1958/clone/node_modules` (read), no lock taken (queue empty, no NexusAI pane, band empty); a hook refused `ln -s` into that clone and an unscoped `grep -r`: not retried. `tmux list-panes` and `ps` read.
