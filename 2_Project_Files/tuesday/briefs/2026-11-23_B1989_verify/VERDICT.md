GATE B1989: GO WITH FINDINGS @ 97a07e6 on main 85b39c7

Independent review, tier G2 (one Sonnet reader), round 1 of 2, WITH the render leg. Lane NX-TF (RD-1032), kit B1977, seat N167.
Branch `b1977/rd1032-light-toner-fills`, head K `97a07e65d675960e937b6742981af5d338d427d7` (tree `b47c40a6ea78`, parent A), A
`0ab1ea3948ea5543b5cdb52765b7b6f5ae5535c6` (tree `10efa664a7b2`, parent BASE), BASE = main `85b39c77b84573757d26113cf094325b5b80c182`
(unmoved; read 15:14 and again 15:20 AEDT 2026-11-23). Blocker 0 | Major 0 | Minor 0 | Info 5.

## Clocks and tools
From `date`: first read 15:13; jest lock ONE acquisition (`g1989-gate`, base `session-tools/locks-laptop-1017`, queue empty) 15:17:31
to 15:53:37; written about 16:00. Trees: `git archive` extracts of BASE, A, K (read verb on the seat clone) and, for jest, my own
`git clone --no-hardlinks --no-checkout` of the seat clone (push URL `invalid://no-push`) with worktrees `w/work` (BASE),
`b1977-nodot/mut21` (BASE) and `w/chk` (K); `node_modules` a symlink to the seat clone's. All under
`fleet/state/s316/g1989/`. Node v24.22.2, `NODE_OPTIONS` unset, `--maxWorkers=2`, every jest run by absolute path with
`--runTestsByPath`. Nothing written in the project but the lock queue's own files. Chain log: `g1989/progress.log`, `chain.json`.

## Measured (each with its instrument)
- GitHub (gh api -X GET): compare main...head ahead 2, behind 0, merge base = main, 8 files (169/0, 3/1, 6/0, 3/0, 3/3, 12/0, 15/3,
  6/6 = the kit's table); open PRs 0; branch ref = K; K's tree and parent equal the seat's; 22 open alerts, none under
  `__tests__/`, `scripts/` or `static/`.
- Frozen text: extracted from the kit by program; sha256 prefixes equal the seat's (apply `57e37f46c29e`, test `2ac8c01082f4`, runlist
  `a0b4bdd4ef46`, plants `47d10737c165`, render `5b647215c61e`, cmp `5069f4f11683`). BASE tree + `apply1977.py` + `test1977.js` equals tree A
  file for file (every file sha256 compared: no difference); A vs K differs in exactly `scripts/verify-expected-counts.json`
  (`_updated`, `tests` 6245, `suites` 395). Both commit messages = the frozen messages plus the Co-Authored-By trailer.
- RENDER (my own run, Chromium 151.0.7922.34, file:// only, 0 non-file requests): `cmp1977.py` 11 OK, 0 FAIL, rc 0. PNG sha256:
  base_light `10355119570d`, after_light `43f718736956`, base_dark = after_dark `c94549bbea10` (dark bytes equal; the light control differs).
  In words: base_light shows four 55% bars on the pale grey track: a dark slate black, then bright cyan, hot pink and golden-yellow
  gradients whose right ends fade toward the track. after_light shows the same rows with the black unchanged and cyan, magenta and
  yellow now flat deep teal, muted rose-red and amber, each clearly distinct from the track along its whole length (the white "55%" chip sits
  over the end of each fill as before). The two dark PNGs are identical: slate-grey black bar, bright cyan, pink and yellow gradients on a near-black track.
- Contrast (project helper `__tests__/helpers/dom` via node): light on `#e9ecef` 3.61, 4.47, 3.08 (old stops 1.74, 2.58, 1.29; black 9.26);
  dark tokens on dark raised `#262626` 3.53 (cyan), 3.02 (magenta), 4.15 (yellow); the six dark stops on `#262626` 6.59, 7.33, 3.48,
  4.95, 9.28, 9.90 (all >= 3). The tokens.css "at worst" comments and the BRAND.md bullet figures equal these.
- Red first (work tree at BASE, new file untracked): 27 cells (new file + rd349), RED L1, L2, D1, D3; GREEN I1, T1, D2, M1 and rd349 19 of 19.
  BASE run list 42 suites, 727 cells, 0 red (FRAME 394 / COUNT 42). Green: new file 8 of 8 twice; run list 43 suites, 735 cells, 0 red.
- PLANTS (mut21, seven files, 160 cells; M0 160 of 160): MA D1, D3; MB L1; MC D1; MD L2 + brand-token-conformance "tokens.css is exactly what the generator
  produces"; ME D1 + "every hex in dark-mode.css resolves to a token" + "the debt is ZERO" + brand-shell-tokens one CONTROL cell; MF L1;
  MG D1, D3 + dark-mode-link-order "zero unscoped selectors". Exactly the kit's matrix; after each plant the three files read back at A's content.
- FULL VERIFY at K (`npm run verify -- --maxWorkers=2`, one acquisition): `VERDICT: PASS - 6245/6245 tests passed across 395 suites (jest exit 0)`,
  `Test Suites: 395 passed`, rc 0, EADDRINUSE 0, porcelain empty, band 20000-35000 free of listeners before and after (control: 11 other listeners machine-wide).
- gitleaks 8.30.1: control (a program-built ghp-shaped token, alone) rc 1 with 1 finding; `git log -p BASE..K` no leaks.
- Scans over the 217 added lines and both messages, each with a firing control: owner attribution 0, B-number/seat/branch 0, decision-queue 0, the word card
  0, person names 0, existsSync 0, `new RegExp(` 0, eval/new Function 0, network 0, timer/skip 0, bidi 0; ticket keys only RD-1032, RD-158,
  RD-175, RD-182, RD-234; non-ASCII 12 added = 12 removed (six tokens.css em dashes replaced in place).

## ATTACK
- Other painters of `.consumable-fill`: re-grepped every non-binary file of tree A. Only `static/css/index-styles.css`, `static/css/dark-mode.css` and
  `static/js/index.js` (line 7957, the one writer; its four callers pass black/cyan/magenta/yellow). No other sheet, inline style or page. Only `static/index.html`
  links `index-styles.css` and loads `index.js`; `dark-mode.css` is linked last there (and nothing after it).
- Cascade: dark `body.dark-mode .consumable-fill.<c>` (0,3,1) outranks light `.consumable-fill.<c>` (0,2,0) regardless of link order; no `!important`
  on either; `dark-mode.js` adds `body.dark-mode` (line 78). The render proves it in a browser, with the sheets linked in that order.
- RD-182: no hex outside comments in the 12 added dark-mode.css lines (one `#262626` in a comment, like the existing comments). RD-158: no "dark" outside
  comments and no `.dark-mode` or `data-theme` in the 15 added light lines. Controls fire.
- Forced colours: in forced-colors emulation no toner fill paints before OR after (computed fills transparent before, Canvas white after, track Canvas white;
  the page shows only the percentage); not a regression. `prefers-contrast: more` has no rules in these sheets: unchanged. A stated limit.

## Findings
| Severity | Finding | Recommendation |
|---|---|---|
| Info | **I-1. Cross-sheet coupling / version skew (measured).** `dark-mode.css` reads `--toner-*` defined only in `index-styles.css`. A dark page holding the OLD `index-styles.css` with the NEW `dark-mode.css` paints NO fill for cyan, magenta and yellow (computed transparent; measured in Chromium); the reverse mix paints the flat light tokens in dark (still >= 3:1). Both sheets are linked without a version query and served by the default static handler (`Cache-Control: public, max-age=0` with ETag, no service worker), so they revalidate together. | None for landing; named in FOR-RECORDS.md. |
| Info | **I-2. Forced-colours** shows no fills before or after (above). | Possible follow-up item. |
| Info | **I-3. Bar and dot mismatch.** `SUPPLY_COLOURS` (index.js:7416) untouched, so a light bar no longer equals its dot. | The kit's named limit; a follow-up only if wanted. |
| Info | **I-4. A hosted Build on PR 242's head `27d49f70` read `failure`** at "Run tests (verify gate)" after 65 min (run 45068925824, attempt 1); a later Build on the same head was success. Unexplained here; the hosted run is the authority. | If this PR's Build reads failure, read the step log first; never re-run from a seat. |
| Info | **I-5. The seat took two lock acquisitions** (a tool's porcelain check counted a plants-program leftover file; it said so in Corrections 4). Not a product matter. | None. |

## DEFAULTS (the six, LANDING HOLD 23): none is wrong
(1) literal hex with the token named: right, tokens.css is linked by no page (a var() would paint nothing) and cell L1 reads each hex against tokens.css so drift is caught.
(2) the dark rule through `--toner-*`: the only shape that passes RD-158, RD-182 and keeps the dark pixels identical (proved in the browser); the cost is I-1.
(3) flat light fills: matches "darker brand colours". (4) the BRAND.md bullet: accurate, figures re-measured. (5) black untouched: 9.26:1, fine. (6) dots untouched: a named limit (I-3).
Who decided: the three colours and "light only, dark unchanged" are the product owner's ruling; the rest the coordinator's.

## NOT RUN / NOT TESTED
The hosted Build and CodeQL on the merge commit; CodeQL by the gate (the seat's local run rc 0 is relayed, NOT re-run here); other viewports; print; Linux; the Deploy demo run a
landing starts (must read skipped); the demo behind SSO; Jira.

Landing texts: `landing.txt`, `pr-title.txt`, `pr-body.md`, `merge-subject.txt`, `merge-body.txt`, `FOR-RECORDS.md` in this folder.
