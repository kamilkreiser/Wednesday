GATE B1942: GO WITH FINDINGS @ 6a8bdc0 on main 8858e5d

Independent review, tier 1, with a rendered leg in light and dark. Lane N-L round 2 of 2: RD-349 and RD-175. Branch
`b1911/nexusai-lane-nl-brand-contrast`, head `6a8bdc0d78903b24f406a456dedab8ddaad78e7d` (R), PREV (round 1's head)
`081f4221f442bbd7ee68be6475f5f64280d558d5`, BASE = main `8858e5d11ec101de0a49a819c2d29f4eadf95c40`.

Clocks (AEDT, 2026-11-23, from `date`): first read 01:41:47. Jest lock: acquisition 1 (`b1942-gate`) 01:46:20 to
02:08:48, 0 s wait; acquisition 2 (`b1942-gate-2`) 02:08:52 to 02:28:03 (it queued behind the first). Two
acquisitions, not one: see I-8.

Trees: my own clone of the builder's clone (`.tools/b1931/clone`; push URL `invalid://no-push`), under
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s312/g1942/`. The head's tree `000957e3...` and parent
`081f4221` equal GitHub's by `gh api` GET. Worktrees (slot printed by the project's own `worktreeSlot()`): `h6` head
(slot 2), `p0` PREV (7), `v1` the verify at head (7), `r0` PREV plus the head's test file (6), `b2` BASE plus the
head's test file (0), `m3` head for plants (17). `node_modules` is a symlink to the builder clone's (lockfile blob
`2d7dbece2ecd` = PREV's = head's = BASE's). Node v24.22.2 first on PATH for everything, `NODE_OPTIONS` unset. Never the
seat's worktree; nothing written in the project but the lock queue's own files.

Blocker 0 | Major 0 | Minor 0 | Info 8

## ROUND 1'S FINDINGS, ONE BY ONE, MEASURED AT THE HEAD

| round 1 | at the head | closed? |
|---|---|---|
| **F-1 (Major)** the light chip text `#212529` is on no token | `.consumable-text` `color: #333333; /* 12.635:1 on #ffffff */`. `#333333` is `tokens.css:33` `--nx-text-strong` (light block, `:root` at :19), re-read at the head. `#212529` declarations in `index-styles.css`: 0 (its 3 hits are comments: the new one at :297 and the two RD-194 ones at :1472, :1485). Pin `derive-brand-tokens.js:166` `count: 23` with a 4-line call-site comment; the generator's `--stdout` is byte-equal to the committed `tokens.css` at PREV AND at the head (control: one appended byte reads DIFFERENT), and `diff` PREV->head of `tokens.css` is exactly `33c33` `x22 measured` -> `x23 measured`. Ratio 12.635 by the repo helper. C1 is tightened: it reads RED at PREV (received `#212529`, not in the light token values) and GREEN at head; my plant G1 (`#212529` back) reds C1 and the pin cell of `brand-token-conformance`; G2 (`#6c757d`, a token but not `--nx-text-strong`) reds C1 and the pin cell. | **Closed** |
| **F-2 (Minor)** the dark track `#313131` swallows the black fill | Dark track `#262626` = `tokens.css:121` `--nx-surface-raised` (dark block at :117); dark black fill `#8c8c8c` = `tokens.css:129` `--nx-text-muted` (dark), by the new rule `body.dark-mode .consumable-fill.black` (0,3,1 over the light 0,2,0; the `background` shorthand also drops the gradient: the engine reads one stop `140,140,140`). Lowest stop on the dark track, repo helper and engine agree: black 1.184 -> 4.500, cyan 5.664 -> 6.590, magenta 2.992 -> 3.481, yellow 7.981 -> 9.284: every stop of every fill clears BRAND.md R8's 3:1 for a graphic (`docs/BRAND.md:768-769`). C5 RED at PREV, GREEN at head; plants G3 (`#313131` back) and G5 (fill `#555555`) red C5. The comment's "1.38:1" is `#2c3e50` on `#262626` 1.378 (correct). | **Closed** |
| **F-3 (Minor)** BRAND.md R5 "it is never text" untrue in light | R5 now reads "never text on a DARK ground" with "dark page / dark card / dark raised"; the figures are right: `#00719f` on `#121212` 3.4458, `#1c1c1c` 3.1347, `#262626` 2.7836. The new paragraph's light figures: on white 5.4366 (5.44), `#f8f9fa` 5.1575 (5.16), `#e9ecef` 4.5847 (4.58). Its quotes are verbatim at source: `index-styles.css:671-672` (RD-251's words, across a line break), `HISTORY.md:7226-7227` ("Shipped, and explicitly not ratified / as his meaning"), `CLARIFICATIONS.md:2752` (the C-258 question) and `:2753` (the recommendation), read by `awk`. It states no new rule, and its one owner attribution is the C-258 citation (HOLD 51: exactly 1, below). | **Closed** |
| **F-4 (Minor)** drag-over and file-chosen states uncelled | Cells S1 (drag-over), S2 (file-chosen) composite the state's translucent ground over `.import-section` `#f8f9fa` with the repo's `composite`; S3 proves `body.dark-mode .file-drop-zone` (0,2,1) outranks both state rules (0,2,0) and that no dark state rule exists. S1, S2 RED at BASE (3.130 / 3.180 unrounded), GREEN at PREV and head (4.894 / 4.971; the engine, which rounds the composite, reads 4.900 / 4.979). Plant G6 (file-chosen alpha 0.05 -> 0.4) reds S2 alone. Dark: 5.068 in all three states in the engine. | **Closed** |

Round 1's I-1 to I-7 stand as recorded (I-5, the e2e allow-list entry and stale light baselines, is still owed).

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| Info | **I-1. In dark, the track is the striped row's own ground.** `body.dark-mode .table tbody tr:nth-of-type(odd) > *` paints `#262626` (`dark-mode.css:344`), the same value as the new track, so on odd rows the empty part of the bar does not show (track on ground 1.000; on even rows 1.126; hovered 1.163). Visible in `rendered-head-dark-toner.png` (rows 5, 50, 100). The fill and the chip show on every row, and BRAND.md section 5 (`:438-441`) records a separator of this kind as not a 1.4.11 boundary; light's track on white is 1.186. The drafter disclosed the 1.000 and Tuesday's Q-2 answer took it. | None for landing. If the product owner wants the full-scale visible on striped rows, that is a palette question, not a defect. |
| Info | **I-2. The black toner reads as mid-grey in dark.** `#8c8c8c` is the `--nx-text-muted` token, whose role column says "secondary text", used here as a graphic fill. It resolves to a token (BRAND.md section 8 rule 2 is met; `brand-token-conformance` passes) and the column header says "Black Toner". The coordinator's Q-2 default. | None. |
| Info | **I-3. C5 does not itself require the dark fill to be a token; the repo's guard does.** My plant G4 (dark black fill `#999999`, off-token but 5.0:1 on the track) leaves C5 GREEN and reds `brand-token-conformance` ("every hex in dark-mode.css resolves to a token" and "the debt is ZERO"), `brand-shell-tokens` CONTROL and `css-ratio-comments`. Covered, by the guard BRAND.md section 8 rule 2 names. | None. |
| Info | **I-4. The LIGHT toner fills on the light track stay below 3:1** (cyan 1.741, yellow 1.290, magenta 2.579; black 7.834), unchanged from BASE by both rounds (engine: every light fill row identical at BASE, PREV and head). The dark fills now meet a rule the light ones do not. Pre-existing; the kit's LEFT FOR OTHERS 2 and Tuesday's Q-6. | Records: the candidate ticket. Named in the pr-body. |
| Info | **I-5. One BRAND.md line was not re-wrapped**: line 309 ("ground, 3.13 on the dark card ... would have left the") is about 110 characters where its neighbours are about 80. Cosmetic; the frozen text, byte-equal to the kit. | None. |
| Info | **I-6. BRAND.md's count table and the generator now move together by one** (15 -> 16 and 22 -> 23); they still count different populations (RD-235), as the new note says. | None. |
| Info | **I-7 (builder's process, STATUS Corrections 1 to 9).** Two typed `cd`, one `rm` of the seat's own 0-byte temp file outside the project, three lock acquisitions (two resumable-step bugs in its own tools; R0 and R each made once), a stale scratch worktree record. None has a product effect: R's parent is PREV, R's tree equals GitHub's, author = committer on all five lane commits. Correction 3 (the kit called the copied test file "untracked" when PREV already tracks it) is a kit fault, as Tuesday said. | None. |
| Info | **I-8 (gate's own process).** Chain 1's six jest runs in `r0`, `b2` and `m3` exited 127: I had linked `node_modules` into `h6`, `p0` and `v1` only. Nothing ran in those trees; the plant loop still planted and reverted each file (blobs proved equal to the head's after every plant). I linked the three trees and re-ran those steps as chain 2, a second lock acquisition queued FIFO behind the first. The browser leg, the head runs and the verify were chain 1's and unaffected. The head's test file copied into `r0` (over PREV's tracked file) and `b2` (untracked) stays there, in scratch. | None. |

## WHAT WAS MEASURED

### Scope (item 3)
- `gh api compare main...head` (GET, 01:42): `ahead`, ahead 5, behind 0, merge base `8858e5d1` = main; 0 open pull
  requests; `matching-refs`: the branch at `6a8bdc0d`, main at `8858e5d1`, no other `b19*` head.
- `git diff --name-only 8858e5d1 6a8bdc0d`: **exactly the eight paths**: `__tests__/fixtures/index-light-failure-baseline.json`,
  `__tests__/rd349-rd175-readable-text-on-its-ground.test.js`, `docs/BRAND.md`, `scripts/derive-brand-tokens.js`,
  `scripts/verify-expected-counts.json`, `static/css/dark-mode.css`, `static/css/index-styles.css`, `static/css/tokens.css`.
- `081f4221..6a8bdc0d`: one fast-forward commit, seven files, 169 insertions, 13 deletions: `index-styles.css` +4 -2,
  `dark-mode.css` +9 -2, `derive-brand-tokens.js` +5 -1, `tokens.css` +1 -1, `BRAND.md` +26 -3, the test file +122 -2,
  counts +2 -2 (GitHub's compare and `git diff --stat` agree; equal to the kit's diff line classes).
- The head's test file is byte-equal (`cmp`) to the kit's frozen text (kit lines 159-513): 19 cells.
- Braces balanced: `index-styles.css` 250/250 at PREV and head; `dark-mode.css` 205/205 -> 206/206. No CR in either.
- Five lane commits (A `8b21d53`, F `493ad19`, T `8f4b716`, K `081f422`, R `6a8bdc0`), author = committer on each,
  each message ends with the Co-Authored-By line. R's message: "The colours are the coordinator's defaults."

### Colours against BRAND.md and the tokens (item 1), re-read at the head
| written | where | token (line at head) |
|---|---|---|
| `#333333` | light chip text | `--nx-text-strong`, `tokens.css:33` |
| `white` | light chip ground | the `--nx-surface-card` value (round 1 I-2) |
| `#262626` | dark track | `--nx-surface-raised` dark, `tokens.css:121` |
| `#8c8c8c` | dark black fill; dark `.drop-text` | `--nx-text-muted` dark, `tokens.css:129` |
| `#dedede` on `#1c1c1c` | dark chip | `--nx-text-strong` dark on dark card (round 1 I-4) |
| `#00719f` x3 | light KPI label, description, drop text | `--nx-brand-chrome` (the RD-251 literal C-258 points at) |
No colour the lane writes is off-guide. `#313131` and `#212529` are gone from the lane's rules.

### Ratios by the repo's own `contrastRatio` / `composite` (`__tests__/helpers/dom.js` at the head; `progs/ratios.js`; control `#000` on `#fff` = 21.000)
| pair | ratio |
|---|---|
| `#212529` on `#ffffff` (PREV chip) / `#333333` on `#ffffff` (head chip) | 15.426 / 12.635 |
| `#dedede` on `#1c1c1c` (dark chip) | 12.667 |
| black on dark track, PREV `#2c3e50`..`#34495e` on `#313131` / head `#8c8c8c` on `#262626` | 1.184..1.400 / 4.500 |
| cyan, magenta, yellow on `#262626` (lowest..highest stop) | 6.590..7.331, 3.481..4.949, 9.284..9.895 |
| same on `#313131` (PREV) | 5.664..6.302, 2.992..4.254, 7.981..8.506 |
| light fills on `#e9ecef` (unchanged) | black 7.834, cyan 1.741, magenta 2.579, yellow 1.290 (lowest stops) |
| dark track on its cell: even / odd (striped) / hovered, PREV `#313131` vs head `#262626` | 1.310 / 1.163 / 1.000 vs 1.126 / 1.000 / 1.163 |
| drop text on drag-over / file-chosen, `#00719f` (unrounded; rounded composite) | 4.8936 (4.900) / 4.9711 (4.979) |
| same, BASE grey `#7f8c8d` | 3.1304 (3.135) / 3.1800 (3.185) |
Every ratio comment the round writes (12.635, 4.500, 1.38) equals these.

### The test file (item 1): red at PREV and BASE, green at head (Node 24, jest 29.7.0; colours from the JSON by title prefix)
- PREV (`r0`, head's file copied over PREV's, `cmp` equal): 19 cells, **2 RED: C1, C5** (C1: `toContain` on the light
  token values; C5: the deep-equality fill check); 17 GREEN. Equal to the kit's table.
- BASE (`b2`, the file untracked): **11 RED: L1 L2 L3 L4 D3 C1 C2 C4 C5 S1 S2**; 8 GREEN: I1 R1 D1 D2 D4 C3 S3 M1.
  Equal to the kit's table.
- Head (`h6`), twice: 19 of 19 GREEN each run.
- S1, S2, S3 cannot be red at PREV (the states pass since round 1); their red is at BASE and by plant.

### Plants (mine, at the head in `m3`; plant set = the lane file, `brand-token-conformance`, `brand-shell-tokens`, `dark-ground-luminance`, `index-dark-surfaces`, `css-ratio-comments`, `brand-md-accent-count`, `muted-4-16-attribution`: 155 cells; reverted by copying back, both stylesheet blobs proved equal to the head's after each)
| plant | change | RED |
|---|---|---|
| G0 | none | 0 of 155 |
| G1 | chip `#212529` (round 1) | C1, BTC pinned light counts |
| G2 | chip `#6c757d` (a token, not text-strong) | C1, BTC pinned light counts |
| G3 | dark track `#313131` (round 1) | C5 |
| G4 | dark black fill `#999999` (off-token, clears 3:1) | BTC every dark hex resolves, BTC debt zero, brand-shell-tokens CONTROL, css-ratio-comments (C5 green: I-3) |
| G5 | dark black fill `#555555` (off-token, fails 3:1) | C5 and the four of G4 |
| G6 | file-chosen alpha 0.4 | S2 |
`m3` porcelain empty after the six.

### Outside the frame (item 1)
- **Who shares the changed selectors.** `.consumable-bar`, `.consumable-fill`, `.consumable-text` are defined in
  `index-styles.css` and `dark-mode.css` only; their one producer is `static/js/index.js:7957` (`_renderTonerCell`,
  colours `black|cyan|magenta|yellow`); `index.js:6017`, `:6177` only read `.consumable-text`'s text for CSV export.
  `.consumable-fill.black` has no other rule. `dark-mode.css` is global, but no other page writes these classes.
- **The dark table's striped and hover rows**, in the engine with the real `table table-hover` classes: odd rows
  `38,38,38`, hovered `49,49,49`, even `28,28,28` under the track. Every dark fill's lowest stop on its track is the
  same on every row, hovered (an even and an odd row hovered) or not: black 4.500, cyan 6.590, magenta 3.481, yellow
  9.284. The track on its row: I-1.
- **Hover and focus.** Focusing `label.file-select-btn` leaves the drop span `0,113,159` light and `140,140,140` dark.
  Hovering a light row changes nothing (vendor excerpt; light row ground stays white).
- **tokens.css** differs in exactly the one line the kit says (above).
- **BRAND.md readers**: `brand-md-accent-count` and `muted-4-16-attribution` green at the head (G0) and in the verify.

## THE RENDERED LEG (item 2)
Harness `progs/g1942-browser.js`: the kit's `browser1931.js` (extracted by `awk`, kit lines 623-714) with four
asserted edits (gate names, an odd row hovered as well as an even one, a focus read, a close-up of the toner table).
Headless Chromium 151.0.7922.34 from the project's `playwright-core` 1.62.1 (`assert-browser.js` OK), `file://` only,
no network, no port, run inside the jest lock. **What it fakes:** Bootstrap is the repo's vendor excerpt
`__tests__/helpers/vendor-surface.css`, not the CDN file (no grid); no page script runs; the toner pills are written
from the `index.js` template with sample values (rows at 5, 25, 50, 75, 100, 60 percent x 4 fills) inside
`index.html`'s own `table table-hover` classes; the import modal is `index.html`'s own markup (lines 195-246, found by
program) shown in place, drag-over and file-chosen classes set on the second and third zone. The seven stylesheets
`index.html` links, in its order (8 sheets with the excerpt). Translucent grounds composited up the tree.

Screenshots in this folder (full page, 1100 px; and `_toner` close-ups of the table):
`B1942_<base|prev|head>_<light|dark>.png`, `B1942_<base|prev|head>_<light|dark>_toner.png`; for the pull request the
same bytes (`cmp` equal) as `rendered-<base|head>-<light|dark>.png` and `rendered-<base|head>-<light|dark>-toner.png`.
Data `browser_<base|prev|head>.json`; pages `harness_<base|prev|head>_<light|dark>.html`.

| element | mode | PREV | head |
|---|---|---|---|
| chip x24 | light | `33,37,41` on `255,255,255`, 15.426, shadow none | `51,51,51` on `255,255,255`, **12.635**, shadow none, inside 24/24 |
| chip x24 | dark | `222,222,222` on `28,28,28`, 12.667 | same, inside 24/24 |
| track | light | `233,236,239` | same (every light fill row identical to PREV and to BASE) |
| track | dark | `49,49,49` | **`38,38,38`** |
| black fill on track | dark | `44,62,80`..`52,73,94`, min 1.184 | **`140,140,140`, 4.500** |
| cyan / magenta / yellow | dark | min 5.664 / 2.992 / 7.981 | min 6.590 / **3.481** / 9.284 |
| drop span rest / drag-over / file-chosen | light | 5.437 / 4.900 / 4.979 | same |
| drop span, all three states | dark | `140,140,140` on `28,28,28`, 5.068 | same |
By program (`progs/brcmp.py`): at the head every chip ratio >= 4.5 and inside its bar in both modes, no shadow; every
dark fill (24) >= 3:1 on its track; every drop span >= 4.5 in both modes and all three states; the light fills
identical to PREV. BASE (main) read in the same harness: light chip white on the track 1.186 with the shadow, dark
the same (the light track in dark), drop text 3.478 / 3.135 / 3.185 light and 4.900 dark. Not rendered: the live page
(CDN Bootstrap, page scripts, CSP), other viewports. Nothing deployed; the demo untouched (C-224).

## VERIFY (item 3)
- `npm --prefix v1 run verify -- --maxWorkers=2`, Node v24.22.2, under `env -u NODE_OPTIONS -u MIN_TESTS -u MIN_SUITES
  -u VERIFY_EXPECTED_FILE`, inside lock acquisition 1 (`nexusai-lock.sh jest b1942-gate`, base
  `session-tools/locks-laptop-1017`, queue empty, 0 s wait).
- 01:46:30 to 02:08:48, rc 0: `VERDICT: PASS — 6235/6235 tests passed across 394 suites (jest exit 0)`; Test Suites 394
  of 394, Tests 6235 of 6235. Equal to the committed `scripts/verify-expected-counts.json` at the head (6235 / 394 =
  PREV 6231 / 394 plus the lane file's 4 new cells).
- `EADDRINUSE` 0; `v1` porcelain empty after; listeners in the slot bands 0 before and after both chains
  (machine-wide control 11 to 12). Load1 1.93 at the verify start.

## CODEQL (item 3)
`pr_codeql_check.sh --repo datasecau/Reporting_Dashboard_Au --checkout <my scratch clone> --base 8858e5d11ec101de0a49a819c2d29f4eadf95c40 --head 6a8bdc0d78903b24f406a456dedab8ddaad78e7d --lang javascript --work <scratch>/cq/run1 --threads 4`,
run after both lock acquisitions were released, one CodeQL process: **rc=0**.
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
```
Equal to the seat's CQ-1 and CQ-2. The lane adds no product JavaScript (the generator gains comments and one number;
the only other JavaScript is the test file). Open code-scanning alerts on main: 22, all in `backend/**` and
`tests/uat-run.js`, none in a lane path (GET at 01:43). A local approximation: the hosted CodeQL check on the pull
request is the authority.

## GITLEAKS (item 3)
gitleaks 8.30.1. Control first: a planted AKIA-shaped pair in a scratch folder reports 1 finding (rc 1). Then the 433
added lines of `git diff 8858e5d1 6a8bdc0d` plus every lane commit message: **0 findings** (rc 0); the 169 added lines
of round 2 plus the messages: **0** (rc 0); `gitleaks git` over `8858e5d1..6a8bdc0d` (5 commits scanned): **0**.

## TEXT (HOLD 51 and the scans; `progs/textscan.py`, every pattern with a control that fires)
- **Owner attribution** (`product owner|owner's ruling|ruled by|decided by`, case-insensitive): **exactly 1** over the
  round-2 added lines and exactly 1 over the whole lane's, the `docs/BRAND.md` line beginning `the product owner's
  2026-11-11 ruling (C-258), option (a), on the question` (HOLD 51's one citation); **0** in every commit message.
- B-numbers and seat ids 0; decision-queue ids 0; timer, skip, `new RegExp(`, `new Function(`, `eval(` 0; bidi and
  zero-width 0. Person names: round 2 0; the lane 1 added and 1 removed, the same pre-existing words of the fixture's
  one replaced `history` line (net 0, round 1's reading). Non-ASCII: round 2 1 added and 1 removed (the em dash of the
  regenerated `tokens.css` line), net 0. The word "card" in round 2's added lines: 4 (`--nx-surface-card` x3, "the dark
  card" in BRAND.md); 0 in messages. Addresses: only the Co-Authored-By line. Ticket keys introduced by round 2:
  RD-175, RD-251, RD-349.

## LANDING TEXTS (item 4)
`pr-title.txt`, `pr-body.md` (before/after in both modes, the dark fill table, the screenshot names, who decided: the
colours are the coordinator's defaults under the product owner's C-258 outcome, which names the result),
`merge-subject.txt`, `merge-body.txt`, `landing.txt` (head-pinned MERGE commit per C-190; the repo's 7 check names, 8
runs, from the last merged PR 239; the Deploy demo run that must read `skipped`, with its path-ignore lines and the
last three skipped runs, re-read 01:43). Scan (`progs/textscan.py`, controls fire): `pr-title.txt`, `pr-body.md`, `merge-subject.txt`, `merge-body.txt`
have 0 B-numbers or seat ids, 0 person names, 0 decision ids, 0 timer or dynamic-code tokens, 0 bidi characters, 0
addresses but the merge body's Co-Authored-By line. Owner attribution: 1, the pr-body's "Who decided" line ("The
product owner's recorded outcome: ... It names the result, not the colours. The colours are the coordinator's
defaults"), round 1's form; 0 in the merge texts. The only non-ASCII is the robot mark of the pr-body's last line.
`landing.txt` is internal and carries the gate id and the branch name (5 hits) by design. The texts carry this head's
sha, the chip colour `#333333` at 12.64, the dark track and fill, and the pair 6235/394.

## FOUND / TESTED / NOT TESTED
**FOUND:** round 1's F-1 to F-4 all closed at the head; I-1 to I-8 (no Blocker, Major or Minor).
**TESTED:** scope, commits and tree; every colour against BRAND.md and `tokens.css` at the head; the generator byte-check
at PREV and head and the one-line `tokens.css` diff; every ratio by the repo helper; the BRAND.md quotes at source; C-258,
C-190 and C-224 at source by `awk` lines 2751-2757, 2062-2068, 2412-2418; the test file red at PREV and BASE as the kit
says and green twice at head; six plants of my own; the selectors' other users, the striped and hovered dark rows,
focus; the engine in light and dark at BASE, PREV and head with screenshots; the full verify on Node 24; CodeQL;
gitleaks with a control; the text scans.
**NOT TESTED:** the live page (CDN Bootstrap, page scripts, CSP); other viewports; Linux; the e2e contrast suite; the
seat's 78-file run list and 19 plants (the full verify backstops the run list; my six plants cover F-1, F-2, F-4);
Jira (not read); the hosted Build and CodeQL on the PR and merge commit; the Deploy demo run a landing starts.
**HOW:** read this commission, round 1's VERDICT, the round-2 kit (813 lines, in pages), the drafter report (101 lines)
and the seat's STATUS (207 lines, Corrections 1 to 9) whole; C-258, C-190 and C-224 by line; `docs/BRAND.md` at the
head by section; measured everything above in my own scratch trees. GitHub GET only; nothing pushed, opened, merged or
deployed; nothing sent to any human.
