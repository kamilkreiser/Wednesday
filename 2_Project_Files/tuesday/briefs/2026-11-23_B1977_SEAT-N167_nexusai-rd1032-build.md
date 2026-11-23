From Tuesday (the Datasec coordinator seat), Datasec / NexusAI. **You do NOT use the shared inbox `datasec-nexusai@`**: your STATUS file and its last line are the only channel to Tuesday; Tuesday's channel to you is a `2026-11-2[345]_B1977_(ADDENDUM|ANSWER)-<n>_*.md` file in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`. A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED-BY-DRAFTER** = the drafter printed it with the instrument named (each such literal has a claim line in the sidecar `<this kit>.measured`); **RELAYED** = read in another file (re-read it at source before you rely on it); **PREDICTED** = the drafter's arithmetic or expectation, nobody has measured it; **UNMEASURED** = nobody has. The drafter's report is saved beside this kit as `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1977_DRAFTER-REPORT.md` (read-only; read it whole at Step 0; its Q-answers are in Tuesday's STAMP slot); the re-cut's own report `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1977R_DRAFTER-REPORT.md` is read whole too (its Q-2 is answered by the facts: both pull requests landed). **The form is lane NX-P, kit B1958 (`2026-11-23_B1958_SEAT-N164_nexusai-nx-p-permission-table.md`, status `READY B1958`, two commits A then K, `--update-counts`) with the one-commit simplifications of kit B1966 (`2026-11-23_B1966_SEAT-N165_nexusai-signal-read-race.md`, status `READY B1966`): their lock, chain, worktree-slot, mutation and verify rules and tool set are this kit's, with the substitutions named in HOLDS.** This lane is a STYLESHEET lane: three product stylesheets/scripts, one existing test cell, one new test file, a regenerated tokens file, one guide paragraph, TWO commits (A the change, K the counts file), one browser render leg, no fix round. Facts below were read on Mon 23 Nov 2026 from 11:08 to the end of the first cut (clock at the build of the first cut: 2026-11-23 11:30:44 +1100) and **RE-CUT at 2026-11-23 13:56:12 +1100 (clock printed by `date`) against the new main: every fact that changed is in the table CHANGED SINCE 3c3be156 below, and every other fact of this kit was re-read at the new main** (marks as above; a fact carried over unchanged from the first cut says so). **BASE: NexusAI main `85b39c77b84573757d26113cf094325b5b80c182`** (repository `datasecau/Reporting_Dashboard_Au`; open pull requests at the re-cut: 0; numbers 242 (branch `b1958/nexusai-nx-p-permission-table`) and 243 (branch `b1966/nexusai-signal-read-race`), which were open at the first cut, have LANDED: 243 as merge commit `df72a283d38c1261344f3dbd8c9d14b86c776833` and 242 as merge commit `85b39c77b84573757d26113cf094325b5b80c182` (parents `df72a283` and `27d49f70`); **pull request 242 wrote `scripts/verify-expected-counts.json`, which this lane's commit K also writes: the file is no longer shared with an open pull request, and at BASE it already carries 242's pair, see PARTITION and HOLD 20**).

# BRIEF B1977 - SEAT-N167: NEXUSAI LANE NX-TF: THE LIGHT-MODE TONER FILLS (CYAN, MAGENTA, YELLOW) TAKE THREE BRAND-TOKEN COLOURS THAT CLEAR 3:1 ON THEIR TRACK; DARK MODE PAINTS EXACTLY WHAT IT PAINTS TODAY; THE BRAND GATE NAMES THE RAISED GROUND; TWO COMMITS (A, K) ON A NEW BRANCH; A REAL-BROWSER RENDER LEG; LOCAL CODEQL; ONE FULL VERIFY; ONE PUSH; NO PR; NOT DEPLOYED

## CHANGED SINCE 3c3be156 (MEASURED-BY-DRAFTER at the re-cut; sources: `gh api -X GET` of the compare `3c3be156...85b39c77`, of `git/ref/heads/main`, `git/commits/85b39c77...`, `pulls?state=open` and `contents/<path>?ref=`, and `git hash-object` of the tarball of `85b39c77`; each line has its control in the report)
| item | at 3c3be156 (first cut) | at 85b39c77 (this cut) |
|---|---|---|
| origin main | `3c3be156e8ea` | `85b39c77b845` (merge commit; tree `89bc13afdf45`; parents `df72a283` and `27d49f70`); 5 commits ahead, 0 behind, 6 files changed |
| open pull requests | 2 (242 head `27d49f70`, 243 head `d37db35c`) | **0** (both landed: 243 as `df72a283`, 242 as `85b39c77`) |
| `scripts/verify-expected-counts.json` blob | `32146fe9377e` | **`e732d2608521`** (496 bytes both) |
| its `tests` / `suites` | 6235 / 394 | **6237 / 394** |
| its `_updated` | `2026-11-22T14:12:23.681Z` | `2026-11-22T20:15:23.513Z` |
| `backend/services/capabilities.js` blob | `f56e6e346d35` | `8c0da99119fe` (+5 -2; not a path or a reader of this lane) |
| `__tests__/rd1011-four-routes-administrator-only.test.js` | `dda98a9892f6` | `e2d5ab0035de` (+4 -2; not on the run list) |
| `__tests__/rd929-capability-design-census.test.js` | `f2a319c1767c` | `99d2d5faaa01` (+20 -0; not on the run list) |
| `__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js` | `438fcc38f087` | `180acd015d22` (+8 -2; not on the run list) |
| `__tests__/rd711-audit-flush-serialised.test.js` | `023b8f976867` | `931e7fa69b30` (+8 -2; not on the run list) |
| the hosted build on `85b39c77` (RELAYED by Tuesday) | (none) | `Tests: 6237 passed, 6237 total`, `Test Suites: 394 passed, 394 total` |
| PREDICTED / MEASURED pair after A | PREDICTED 6243 tests, 395 suites | **MEASURED-BY-DRAFTER (a count) 6245 tests / 395 suites** (see finding 5) |
| K's base blob and the shared path | shared with open pull request 242 (HOLD 20 stopped the seat on a move of the counts file) | not shared; 242's pair is already in BASE; HOLD 20 stops the seat on a further move of the counts file |

**Unchanged and re-read at `85b39c77` (each one a line in the report):** the six BASE blobs of the files the lane edits (equal to the table below), every anchor of `apply1977.py` found exactly once with the same sizes and the same patched blobs, the generator's own output equal to the patched `tokens.css`, `package-lock.json` sha256 prefix `37e5add354e5`, `runlist1977.py` at BASE (FRAME 394, COUNT 42, the same 42 names as the first cut's list), the open code-scanning alerts (22, none under `__tests__/`, `scripts/` or `static/`), the render (dark PNG sha256 prefix `c94549bbea10` before and after) and the seven plants. **No path of OWNS-B1977 was touched by pull request 242 or 243 other than the counts file** (the six paths they changed are the five above and the counts file; none is a reader on the run list).

## THE DEFECT AND THE AUTHORITY (MEASURED-BY-DRAFTER unless marked)
- **The defect (RD-1032, status To Do, RELAYED from `.../Briefs/2026-11-23_B1967_OPTIONS/data/rd1032.txt`).** On the light toner track `#e9ecef` (`--nx-surface-raised`) the lowest stop of the fills reads black 7.83, cyan 1.74, magenta 2.58, yellow 1.29 to 1; the brand rule for a graphic is 3:1 (`docs/BRAND.md` R8, WCAG 1.4.11). Dark already meets it (RD-175 round 2, pull request 240).
- **The ruling (RELAYED).** The product owner's live-board answer of 2026-11-23 11:06:40 read "looks great.  please build and deploy" after the options document `.../Briefs/2026-11-23_B1967_OPTIONS/RD-1032_options.md` (read whole by the drafter, 207 lines). Tuesday (the coordinator) read it as option a of the pending decision and recorded that option a in the store as the product owner's own choice (Tuesday quotes the card in the STAMP slot): option a, "Darker brand colours: Cyan --nx-role-partner-manager #0a8793, magenta --nx-role-security #b44752, yellow --nx-role-partner-tech #b57a13; light mode only, dark unchanged." **This lane builds exactly that and nothing about deploying** (a separate research seat reads the deploy route; this kit never deploys; see HOLD 23).
- **The figures (MEASURED-BY-DRAFTER, `proto` tree, the project's own contrast helper through the new test's cell I1):** on `#e9ecef` the three tokens read 3.61, 4.47 and 3.08; the old lowest stops read 1.74 (`#26c6da`), 2.58 (`#f06292`) and 1.29 (`#ffca28`).
- **Tier (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md`).** Builder: Sonnet, row C2 (line 92: a multi-file build that fails the local predicate, not decision-shaped, not auth-design, not destroying). Gate after you: **G2** (line 109: tests, docs, config, tooling; no security surface is touched), Sonnet, **with the render leg below owed to the gate**. Model id `claude-sonnet-5-5` (`/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json` line 23).
- **A landing, not yours.** "Every merge to NexusAI main goes through a PULL REQUEST ... Never squash, never rebase" (`1_Project_Definition/CLARIFICATIONS.md`, entry C-190, `awk NR==2062,2067` read at drafting): Tuesday gates, opens the PR and lands it by MERGE COMMIT pinned to the head. C-190's item 1 asks a seat to look in the files its branch changes for patterns CodeQL flags: this lane adds no `existsSync`, no file write, no `new RegExp(` and no network call (scan below). **Deploy rule:** nothing is deployed (C-224 demo hold, and the product owner's word "deploy" is a separate decision, see HOLD 23). **`static/**` and `scripts/**` are NOT in the Deploy demo workflow's path-ignore list** (`.github/workflows/deploy-demo.yml` lines 29 to 32 ignore only `**.md`, `docs/**` and `tests/**`), so a landing of this branch STARTS a Deploy demo run on main; its build and deploy jobs are gated on `vars.CI_DEPLOY_ENABLED` (lines 53 and 91). You touch no workflow, variable, secret or environment.

## WHAT THE DRAFTER FOUND (MEASURED-BY-DRAFTER on the tarball of BASE; jest 29.7.0 on Node v24.22.2; a real Chromium 151.0.7922.34 from the Playwright package of a project clone, file:// only)
1. **A `var(--nx-...)` in the light sheet paints NOTHING; the lane writes literal hex with the token named beside it (a departure from the commission's wording, said first).** `static/css/tokens.css` is linked by NO shipped page: the test `__tests__/brand-shell-tokens.test.js` ("no HTML page under static/ links tokens.css", and "no stylesheet other than tokens.css ... contains var(--nx-") asserts it, and `index-styles.css` lines 704 to 706 and 1197 to 1204 record the project's own rule (RD-234): "a var(--nx-*) here would be a dead reference" (a declaration invalid at computed-value time, which for `background` paints no fill). So each light rule carries the token's hex and the token's name in a comment, and a new cell reads the hex against `tokens.css`.
2. **Neither shape the commission offered for "dark stays" survives the project's own gates; the lane uses a third.** (i) A light-only selector (`body:not(.dark-mode) ...`, or any selector naming the dark state) in `index-styles.css` turns two guards red: `__tests__/dark-mode-link-order.test.js` ("static/css/index-styles.css defines no .dark-mode selector", RD-158) and `__tests__/sustainability-dark-mode.test.js` ("no page defines dark mode privately any more", R3-1): measured, 2 failed of 705 on the first prototype, the received list naming the three new selectors. (ii) An explicit dark rule that WRITES the old hexes into `dark-mode.css` turns the RD-182 zero-debt guard red (`__tests__/brand-token-conformance.test.js`, "every hex in dark-mode.css resolves to a token", "the debt is ZERO"); planted at the dry run (plant ME below) it reads 2 red there. (iii) **The shape that passes:** the light rules are the flat tokens; the six old gradient stops live as `--toner-*` custom properties in the light sheet's `:root` block (non-`nx` names; hex is allowed in the light sheet); `dark-mode.css` gets one rule per fill, `body.dark-mode .consumable-fill.<colour>`, painting `linear-gradient(90deg, var(--toner-<c>-from), var(--toner-<c>-to))`, with no hex of its own. Rendered in a real browser the dark computed styles, geometry and PNG bytes are IDENTICAL before and after (step 5 below; the drafter's run printed the same sha256 `c94549bbea10...` for both dark pages), and the light fills change.
3. **One existing cell must learn the new dark shape.** Cell C5 of `__tests__/rd349-rd175-readable-text-on-its-ground.test.js` read a dark rule's stops with `stopsOf(prop(dark,'background'))`; a `var()` gives no hex and the cell would read `stops.length > 0` false. The frozen program changes ONE statement of C5 (a `named()` helper resolving the `--toner-*` properties from the light sheet's `:root`: 3 lines added and 1 removed). No cell is added or removed there.
4. **The brand gate.** `scripts/derive-brand-tokens.js` gives every role accent `grounds = ['surface-card','surface-page']` (the loop at lines 375 to 380 at BASE). The lane adds `surface-raised` to the grounds of `role-security`, `role-partner-manager` and `role-partner-tech` (graphic kind, so the floor is 3:1, which the gate asserts in both themes through `shellPairs()`); `static/css/tokens.css` is regenerated by the script (comment text only: the six "at worst" figures move to the raised ground, no value moves, the dark hexes are unchanged); the negative pairings of these tokens AS TEXT on the raised ground (`SHELL_NEGATIVE`) stay and still fail. None of the three has a pinned count (R7), so no pinned-count line and no `docs/BRAND.md` table line is forced by the gate (measured: `brand-md-accent-count.test.js` and the pinned-count cell of `brand-token-conformance.test.js` stay green); one explanatory bullet is added to BRAND.md section 9.4 (a default, Q-3 of the report).
5. **Cells: red-first, then green, by program.** The new file has 8 cells (indented-pattern count 8, column-1 count 0, by `/usr/bin/grep -c`). Placed in a tree at BASE with BASE's stylesheets, the drafter's run read **4 red (L1, L2, D1, D3) and 4 green (I1, T1, D2, M1)**; in the patched tree **8 of 8 green**. Seven plants, each caught by name (MUTATIONS below). **Counts after A: 6245 tests, 395 suites, MEASURED-BY-DRAFTER as a count** (BASE 6237 / 394, plus the new file's 8 cells and one suite): `jest` over the whole suite at a patched scratch tree printed `Tests: 6245` in `Test Suites: 395` (the JSON's `numTotalTests` and `numTotalTestSuites`). That run's own verdict was `VERDICT: FAIL` because 39 suites failed on the scratch tree's environment (no `.git`, no `lsof` on its PATH, a borrowed `node_modules`, a docker-context test), none of them a file of this lane (the 43 files of the run list were all green in their own run); so a plain PASS has been seen by nobody: the seat's own verifies at A and K prove it.
6. **What the cells cannot say, said plainly.** They read stylesheets; they do not prove what a browser paints. The render leg (step 5) is the browser proof. Cell D2 (the dark rule outranks the light rule) is not alone red under any of the seven plants (plant MG, which lowers the selector, is caught by D1, D3 and by the RD-158 guard instead): D2 is a stated guard with a control in its own body, not a separately mutation-proved one.
7. **The run list: the project files that read these sheets.** `runlist1977.py` (frozen below) over BASE prints **FRAME 394 and COUNT 42** (the frame equals the `suites` of the counts file: the control). The drafter's run of all 42 at BASE `85b39c77` read 42 suites, 727 tests, 0 red; at the patched tree the 43 files (the 42 and the new one) read 43 suites, 735 tests, 0 red (727 + the new file's 8), of which the new file is 8 (jest JSON by program, both runs by absolute path with `--runTestsByPath`). The first cut's figures (735 at the patched tree) are the same.
8. **Nothing else paints the fills.** The cartridge table's colour dots (`SUPPLY_COLOURS` at `static/js/index.js` line 7416: `#2c3e50`, `#00bcd4`, `#e91e63`, `#ffc107`) are NOT changed: **a limit, named**: a recoloured light bar no longer equals its own dot (the options document, section 7). The end-to-end suite `tests/e2e/dark-mode-contrast.spec.js` names `consumable` and its light baselines are stale by RD-1031's own text; it is not part of `npm run verify` and is not touched. The one page that writes the class is `static/js/index.js` line 7957 (`class="consumable-fill ' + color + ' tw-'`).

## STATE AT DRAFTING (MEASURED-BY-DRAFTER; re-read every line at Step 1 at YOUR read)
- origin main `85b39c77b84573757d26113cf094325b5b80c182` (re-cut: read by `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/git/ref/heads/main` at 13:17:21 and again at 13:20 (the sha printed by `--jq .object.sha`); the first cut read `3c3be156e8ea36ad297fdadd3055c6e00252ba38`); no open pull request (`pulls?state=open` returned nothing); `matching-refs/heads/b1977` reads 0 by `--jq length` (control: `matching-refs/heads/b1966` reads 1); open code-scanning alerts 22 (by `--jq length`; none under `__tests__/`, `scripts/` or `static/`; `backend/server.js` is among them: the control).
- Blobs at BASE (`git hash-object` of the extracted tarball; each equal to the GitHub tree's blob sha, the tarball control), sizes, and the patched blobs (MEASURED, in scratch trees by `apply1977.py`):
| path | BASE blob | BASE bytes | patched blob (MEASURED) | patched bytes | added / removed |
|---|---|---|---|---|---|
| `static/css/index-styles.css` | `b17eb7bf64e8` | 42750 | `8e98826ba901` | 43579 | 15 / 3 |
| `static/css/dark-mode.css` | `5dec53a1844f` | 86207 | `11a129c1f668` | 86891 | 12 / 0 |
| `scripts/derive-brand-tokens.js` | `3e3b5a1704fa` | 50618 | `36c924697567` | 50966 | 3 / 0 |
| `static/css/tokens.css` | `f72105abb1ca` | 17727 | `3c840004cb66` | 17739 | 6 / 6 |
| `docs/BRAND.md` | `022d7cfc110d` | 54591 | `86262042a478` | 55075 | 6 / 0 |
| `__tests__/rd349-rd175-readable-text-on-its-ground.test.js` | `fb47788052a8` | 18118 | `d74a5c14f20c` | 18363 | 3 / 1 |
| `__tests__/rd1032-light-toner-fills-clear-their-track.test.js` (NEW) | (absent) | 0 | `b4cb91e899f0` | 8850 | 214 total added lines across the seven paths / 8 cells here |
| `scripts/verify-expected-counts.json` (K only) | `e732d2608521` | 496 | (written by the project command) | | |
- The counts file `scripts/verify-expected-counts.json` at BASE: blob `e732d2608521`, `tests` 6237, `suites` 394, `_updated 2026-11-22T20:15:23.513Z` (read from the tarball of BASE by `cat`; at the first cut's BASE it read 6235 / 394; pull request 242 moved it).
- Slot-17 tree names (the project rule: sha256 of the real path, first four bytes big-endian, mod 19; the drafter's computation, controls: `b1958-nodot/work4` = 17, `b1931-nodot/new5` = 17, `b1966-nodot/work4` = 17): `b1977-nodot/work4`, `b1977-nodot/mut21`, `b1977-nodot/vupd21`, `b1977-nodot/chk4` and `b1977-nodot/rnd19` all read 17 (printed by the drafter's program). Band 30880-31519.

## THE DESIGN (Tuesday's defaults; every departure needs your written justification in STATUS)
**TWO commits on a NEW branch `b1977/rd1032-light-toner-fills` at BASE: A (the change: seven paths, the new test file included) then K (the counts file only, written by the project's own command).** Defaults (the coordinator's, never the product owner's): (1) literal hex with the token named beside it, not `var(--nx-...)` (finding 1); (2) the dark rule shape of finding 2(iii); (3) flat colours (one token per fill, the gradient goes in light); (4) the BRAND.md bullet (Q-3); (5) black is untouched; (6) `SUPPLY_COLOURS` is untouched (a named limit). The product owner's ruling fixes the three tokens and "light only, dark unchanged"; everything else is how.
**The frozen program** `apply1977.py` (run in a tree: first argument the root, second `apply` (default) or `revert`; every anchor of every file is asserted to match exactly once BEFORE any file is written, so a half-state is refused; each file is rebuilt whole, written beside the target and `os.replace`d; non-ASCII bytes proved unchanged beyond the anchors; ASCII-only program text). It edits SIX existing files; **the new test file `rd1032-light-toner-fills-clear-their-track.test.js` is copied from the frozen `test1977.js`** (a seventh path, new).
```python FILE: apply1977.py
#!/usr/bin/env python3
# apply1977.py <tree root> [apply|revert]: the frozen edit of lane NX-TF (light toner fills). apply = the edit; revert = the exact inverse.
# Four existing files only (the new test file is copied from test1977.js by the seat). Every anchor is asserted to match exactly once
# BEFORE any file is written; each file is rebuilt whole, written beside the target and os.replace d; non-ASCII bytes proved equal.
import os, sys
root = sys.argv[1]
what = sys.argv[2] if len(sys.argv) > 2 else 'apply'
assert what in ('apply', 'revert'), what
ANCHORS = [
    ('static/css/index-styles.css',
     ' --card-shadow: 0 2px 8px rgba(0,0,0,0.1);\n',
     ' --card-shadow: 0 2px 8px rgba(0,0,0,0.1);\n /* RD-1032: the toner gradients main painted in both themes, kept for DARK (see .consumable-fill.cyan below) */\n --toner-cyan-from: #00bcd4;\n --toner-cyan-to: #26c6da;\n --toner-magenta-from: #e91e63;\n --toner-magenta-to: #f06292;\n --toner-yellow-from: #ffc107;\n --toner-yellow-to: #ffca28;\n'),
    ('static/css/index-styles.css',
     ' .consumable-fill.cyan { background: linear-gradient(90deg, #00bcd4, #26c6da); }\n .consumable-fill.magenta { background: linear-gradient(90deg, #e91e63, #f06292); }\n .consumable-fill.yellow { background: linear-gradient(90deg, #ffc107, #ffca28); }\n',
     ' /* RD-1032: in LIGHT the three coloured fills are flat brand-token colours that clear 3:1 on the track\n    #e9ecef (--nx-surface-raised): a graphic, BRAND.md R8 / WCAG 1.4.11. Literal hex with the token NAMED\n    beside it (RD-234): tokens.css is linked by no page, so a var(--nx-*) here would be a dead reference\n    and the fill would paint nothing. DARK keeps the gradients it has always had: dark-mode.css reads them\n    from the --toner-* properties in :root above (that sheet may hold no hex of its own: RD-182). */\n .consumable-fill.cyan { background: #0a8793; }    /* --nx-role-partner-manager, 3.61:1 */\n .consumable-fill.magenta { background: #b44752; } /* --nx-role-security, 4.47:1 */\n .consumable-fill.yellow { background: #b57a13; }  /* --nx-role-partner-tech, 3.08:1 */\n'),
    ('scripts/derive-brand-tokens.js',
     '  s.prov = `role accent ${name.slice(5)}, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text`;\n}\n',
     "  s.prov = `role accent ${name.slice(5)}, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text`;\n}\n// RD-1032: three role accents are ALSO the light toner fills (cyan, magenta, yellow), which are painted on the\n// toner track, --nx-surface-raised (R8: a token is correct only on the grounds it names). Graphic use only.\nfor (const n of ['role-security', 'role-partner-manager', 'role-partner-tech']) SHELL_ROLES[n].grounds.push('surface-raised');\n"),
    ('static/css/tokens.css',
     '    --nx-role-security:                 #b44752;  /* NEW graphic \u2014 role accent security, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text \u2014 5.03:1 at worst (on --nx-surface-page), needs 3 */\n',
     '    --nx-role-security:                 #b44752;  /* NEW graphic \u2014 role accent security, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text \u2014 4.47:1 at worst (on --nx-surface-raised), needs 3 */\n'),
    ('static/css/tokens.css',
     '    --nx-role-partner-manager:          #0a8793;  /* NEW graphic \u2014 role accent partner-manager, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text \u2014 4.07:1 at worst (on --nx-surface-page), needs 3 */\n    --nx-role-partner-tech:             #b57a13;  /* NEW graphic \u2014 role accent partner-tech, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text \u2014 3.46:1 at worst (on --nx-surface-page), needs 3 */\n',
     '    --nx-role-partner-manager:          #0a8793;  /* NEW graphic \u2014 role accent partner-manager, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text \u2014 3.61:1 at worst (on --nx-surface-raised), needs 3 */\n    --nx-role-partner-tech:             #b57a13;  /* NEW graphic \u2014 role accent partner-tech, mock V271_ROLE_ACCENT; graphic only (the KPI bar), never text \u2014 3.08:1 at worst (on --nx-surface-raised), needs 3 */\n'),
    ('static/css/tokens.css',
     '    --nx-role-security:                 #b64d57;  /* R10 lift 3% \u2014 dark \u2014 3.40:1 at worst (on --nx-surface-card), needs 3 */\n',
     '    --nx-role-security:                 #b64d57;  /* R10 lift 3% \u2014 dark \u2014 3.02:1 at worst (on --nx-surface-raised), needs 3 */\n'),
    ('static/css/tokens.css',
     '    --nx-role-partner-manager:          #0a8793;  /* R10 lift 0% \u2014 dark \u2014 3.98:1 at worst (on --nx-surface-card), needs 3 */\n    --nx-role-partner-tech:             #b57a13;  /* R10 lift 0% \u2014 dark \u2014 4.67:1 at worst (on --nx-surface-card), needs 3 */\n',
     '    --nx-role-partner-manager:          #0a8793;  /* R10 lift 0% \u2014 dark \u2014 3.53:1 at worst (on --nx-surface-raised), needs 3 */\n    --nx-role-partner-tech:             #b57a13;  /* R10 lift 0% \u2014 dark \u2014 4.15:1 at worst (on --nx-surface-raised), needs 3 */\n'),
    ('docs/BRAND.md',
     '  ratios.\n',
     '  ratios.\n- Three role accents are also the LIGHT toner fills (RD-1032): `--nx-role-partner-manager`\n  (cyan), `--nx-role-security` (magenta) and `--nx-role-partner-tech` (yellow) name\n  `--nx-surface-raised`, the toner track, as a third ground, for graphic use only. They\n  read 3.61, 4.47 and 3.08 there (floor 3:1; dark values 3.53, 3.02 and 4.15 on the dark\n  raised ground). Dark mode does not use them: its fills keep their gradients. The text\n  pairings on raised stay asserted to FAIL.\n'),
    ('static/css/dark-mode.css',
     '    background: #8c8c8c;              /* 4.500:1 on #262626 */\n}\n',
     '    background: #8c8c8c;              /* 4.500:1 on #262626 */\n}\n/* RD-1032: cyan, magenta and yellow keep the gradients they had before the light fills became flat tokens\n * (each stop clears 3:1 on #262626; cell C5). The stops are the --toner-* properties of index-styles.css :root,\n * because this sheet holds no hex that is not a token (RD-182). */\nbody.dark-mode .consumable-fill.cyan {\n    background: linear-gradient(90deg, var(--toner-cyan-from), var(--toner-cyan-to));\n}\nbody.dark-mode .consumable-fill.magenta {\n    background: linear-gradient(90deg, var(--toner-magenta-from), var(--toner-magenta-to));\n}\nbody.dark-mode .consumable-fill.yellow {\n    background: linear-gradient(90deg, var(--toner-yellow-from), var(--toner-yellow-to));\n}\n'),
    ('__tests__/rd349-rd175-readable-text-on-its-ground.test.js',
     "            const stops = stopsOf(dark ? prop(dark, 'background') : light);\n",
     "            // RD-1032: a dark rule may read its stops from the --toner-* properties of the light sheet's :root\n            const named = (v) => (v || '').replace(/var\\((--toner-[a-z-]+)\\)/g, (m, n) => prop(one(LIGHT, ':root'), n) || m);\n            const stops = stopsOf(dark ? named(prop(dark, 'background')) : light);\n"),
]
PLAN = {}
for rel, old, new in ANCHORS:
    p = os.path.join(root, rel)
    s = PLAN[rel][1] if rel in PLAN else open(p, "rb").read().decode("utf-8")
    o, n = (old, new) if what == "apply" else (new, old)
    assert s.count(o) == 1, (rel, "anchor count", s.count(o), "expected 1")
    PLAN[rel] = (p, s.replace(o, n))
for rel, (p, s) in PLAN.items():
    raw = open(p, "rb").read()
    out = s.encode("utf-8")
    na = lambda b: len([c for c in b if c > 127])
    want = sum(na((n if what == "apply" else o).encode("utf-8")) - na((o if what == "apply" else n).encode("utf-8")) for r, o, n in ANCHORS if r == rel)
    assert na(out) - na(raw) == want, (rel, "non-ASCII bytes changed beyond the anchors", na(out) - na(raw), want)
for rel, (p, s) in PLAN.items():
    raw = open(p, "rb").read()
    out = s.encode("utf-8")
    tmp = p + ".tmp1977"
    open(tmp, "wb").write(out)
    os.replace(tmp, p)
    print(what, rel, len(raw), "->", len(out))
```
**The new test file, frozen** (copied to `__tests__/rd1032-light-toner-fills-clear-their-track.test.js` byte for byte; 8 cells):
```js FILE: test1977.js
/**
 * @jest-environment node
 *
 * RD-1032 - in LIGHT mode the cyan, magenta and yellow toner fills are flat brand-token colours that clear 3:1 on the
 * toner track, and DARK mode keeps the fills it has today.
 *
 * WHAT THIS FILE IS. A reader of the stylesheets, in the manner of rd349-rd175-readable-text-on-its-ground.test.js
 * (RD-175 round 2 did the same for dark). It proves what the rules say and what they measure with the repo's own
 * contrast helper. It does NOT prove what a browser paints: the real-engine numbers are the build seat's render.
 *
 *   TRACK   .consumable-bar is #e9ecef, the light value of --nx-surface-raised.
 *   LIGHT   the old fills (#00bcd4 1.74:1, #e91e63 / #f06292 2.58:1, #ffc107 / #ffca28 1.29:1 at the lowest stop) fail
 *           3:1 (BRAND.md R8, WCAG 1.4.11). Each coloured fill is now ONE token colour, read from tokens.css:
 *           cyan --nx-role-partner-manager, magenta --nx-role-security, yellow --nx-role-partner-tech.
 *   DARK    before this change dark inherited the light gradients. Now the light rules are the flat tokens, so dark has
 *           a rule of its own for each of the three that paints the SAME gradient. Its stops are the --toner-*
 *           properties of the light sheet's :root, because dark-mode.css may hold no hex that is not a token (RD-182)
 *           and a selector that names the dark state may not appear in the light sheet (RD-158).
 *   GATE    each token is a graphic painted on the raised track, so the generator names --nx-surface-raised in its
 *           grounds (BRAND.md R8: a token is correct only on the grounds it names).
 */
'use strict';

const fs = require('fs');
const path = require('path');
const G = require('../scripts/derive-brand-tokens');
const { parseColor, contrastRatio } = require('./helpers/dom');

const ROOT = path.join(__dirname, '..');
const read = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8');
const LIGHT = read('static/css/index-styles.css');
const DARK = read('static/css/dark-mode.css');
const TOKENS = read('static/css/tokens.css');

const GRAPHIC = 3;
const HEX6 = /^#[0-9a-f]{6}$/;
const TOKEN_OF = {
    cyan: '--nx-role-partner-manager',
    magenta: '--nx-role-security',
    yellow: '--nx-role-partner-tech',
};
// the gradients main paints today, written out here so that a change to them is named, not followed
const TODAY = {
    cyan: 'linear-gradient(90deg, #00bcd4, #26c6da)',
    magenta: 'linear-gradient(90deg, #e91e63, #f06292)',
    yellow: 'linear-gradient(90deg, #ffc107, #ffca28)',
};
const BLACK_LIGHT = 'linear-gradient(90deg, #2c3e50, #34495e)';

const stripComments = (s) => s.replace(/\/\*[\s\S]*?\*\//g, '');
function rulesFor(css, selector) {
    const out = [];
    for (const chunk of stripComments(css).split('}')) {
        const i = chunk.lastIndexOf('{');
        if (i < 0) continue;
        const sel = chunk.slice(0, i).split('{').pop();
        const names = sel.split(',').map((x) => x.replace(/\s+/g, ' ').trim());
        if (names.includes(selector)) out.push(chunk.slice(i + 1));
    }
    return out;
}
function prop(body, name) {
    let val = null;
    for (const d of (body || '').split(';')) {
        const j = d.indexOf(':');
        if (j > 0 && d.slice(0, j).trim().toLowerCase() === name) val = d.slice(j + 1).trim().toLowerCase();
    }
    return val;
}
const one = (css, selector) => {
    const r = rulesFor(css, selector);
    return r.length === 1 ? r[0] : null;
};
const ratio = (fg, bg) => {
    const a = parseColor(fg);
    const b = parseColor(bg);
    return a && b ? contrastRatio(a, b) : null;
};
// the light value of a token: its declaration in the :root block of tokens.css
const lightToken = (name) => prop(one(TOKENS, ':root'), name);
// a dark gradient with its --toner-* stops read from the light sheet's :root
const resolved = (value) => (value || '').replace(/var\((--toner-[a-z-]+)\)/g, (m, n) => prop(one(LIGHT, ':root'), n) || m);
// selector specificity as [ids, classes, types], enough for the compound selectors of these sheets
const specificity = (sel) => [
    (sel.match(/#[a-z][\w-]*/gi) || []).length,
    (sel.match(/\.[a-z][\w-]*/gi) || []).length,
    sel.split(/[\s>+~]+/).filter((part) => /^[a-z]/i.test(part)).length,
];
const outranks = (a, b) => {
    for (let i = 0; i < 3; i++) if (a[i] !== b[i]) return a[i] > b[i];
    return false;
};
const DARK_SEL = (c) => 'body.dark-mode .consumable-fill.' + c;

describe('RD-1032 - light toner fills clear 3:1 on their track; dark keeps today\'s fills', () => {
    test('I1: the instrument gives the measured numbers, and the old stops fail it', () => {
        expect(ratio('#0a8793', '#e9ecef')).toBeCloseTo(3.61, 2);
        expect(ratio('#b44752', '#e9ecef')).toBeCloseTo(4.47, 2);
        expect(ratio('#b57a13', '#e9ecef')).toBeCloseTo(3.08, 2);
        // control: the stops of main fail it, so a green below is not a ratio that cannot fail
        expect(ratio('#26c6da', '#e9ecef')).toBeLessThan(GRAPHIC);
        expect(ratio('#f06292', '#e9ecef')).toBeLessThan(GRAPHIC);
        expect(ratio('#ffca28', '#e9ecef')).toBeLessThan(GRAPHIC);
    });

    test('T1: the track is the light value of --nx-surface-raised, read from the stylesheets', () => {
        const track = prop(one(LIGHT, '.consumable-bar'), 'background');
        expect(HEX6.test(track || '')).toBe(true);
        expect(track).toBe(lightToken('--nx-surface-raised'));
        expect(track).toBe('#e9ecef');
    });

    test('L1: each light fill is ONE flat token colour read from tokens.css, and clears 3:1 on the track', () => {
        const track = prop(one(LIGHT, '.consumable-bar'), 'background');
        for (const c of ['cyan', 'magenta', 'yellow']) {
            const rule = one(LIGHT, '.consumable-fill.' + c);
            expect([c, rule !== null]).toEqual([c, true]);
            const bg = prop(rule, 'background');
            expect([c, HEX6.test(bg || '')]).toEqual([c, true]);      // flat: no gradient, no var()
            expect([c, bg]).toEqual([c, lightToken(TOKEN_OF[c])]);    // the token's own value
            expect([c, ratio(bg, track) >= GRAPHIC]).toEqual([c, true]);
        }
    });

    test('L2: the black fill is untouched in light, and the three tokens are graphic and name the raised track', () => {
        expect(prop(one(LIGHT, '.consumable-fill.black'), 'background')).toBe(BLACK_LIGHT);
        for (const c of ['cyan', 'magenta', 'yellow']) {
            const name = TOKEN_OF[c].slice('--nx-'.length);
            const s = (G.SHELL_LIST || []).find((x) => x.name === name);
            expect([c, !!s]).toEqual([c, true]);
            expect([c, s.kind]).toEqual([c, 'graphic']);
            expect([c, s.grounds.includes('surface-raised')]).toEqual([c, true]);
        }
    });

    test('D1: dark paints today\'s gradients - its own rule for each of the three, whose stops resolve to the old values, and the black rule is as it was', () => {
        for (const c of ['cyan', 'magenta', 'yellow']) {
            const rule = one(DARK, DARK_SEL(c));
            expect([c, rule !== null]).toEqual([c, true]);
            expect([c, resolved(prop(rule, 'background'))]).toEqual([c, TODAY[c]]);
            // no hex of its own in dark-mode.css for this rule (RD-182), only the properties
            expect([c, /#[0-9a-f]{3,8}\b/.test(rule)]).toEqual([c, false]);
        }
        expect(prop(one(DARK, DARK_SEL('black')), 'background')).toBe('#8c8c8c');
        expect(prop(one(DARK, 'body.dark-mode .consumable-bar'), 'background')).toBe('#262626');
    });

    test('D2: the dark rule outranks the light one it replaces, so a dark body never paints the flat token', () => {
        for (const c of ['cyan', 'magenta', 'yellow']) {
            expect([c, outranks(specificity(DARK_SEL(c)), specificity('.consumable-fill.' + c))]).toEqual([c, true]);
        }
        // control: the comparison can say no
        expect(outranks(specificity('.consumable-fill.cyan'), specificity(DARK_SEL('cyan')))).toBe(false);
    });

    test('D3: every dark stop clears 3:1 on the dark track (the RD-175 floor holds for what dark keeps)', () => {
        const track = prop(one(DARK, 'body.dark-mode .consumable-bar'), 'background');
        for (const c of ['cyan', 'magenta', 'yellow']) {
            const stops = resolved(prop(one(DARK, DARK_SEL(c)), 'background')).match(/#[0-9a-f]{6}/g) || [];
            expect([c, stops.length]).toEqual([c, 2]);
            for (const s of stops) expect([c, s, ratio(s, track) >= GRAPHIC]).toEqual([c, s, true]);
        }
    });

    test('M1: the rules above style real nodes (index.js writes the fill class from the toner colour name)', () => {
        const js = read('static/js/index.js');
        expect((js.match(/class="consumable-fill ' \+ color \+ ' tw-'/g) || []).length).toBe(1);
    });
});
```

## THE FROZEN HELPERS (scratch use; never committed)
```python FILE: runlist1977.py
#!/usr/bin/env python3
# runlist1977.py <tree root>: the run list of lane NX-TF = every file directly under __tests__ named *.test.js whose text names a stylesheet,
# the tokens, the generator or the brand guide (the pattern below, the same one `grep -l -E` ran at drafting), one absolute path per line,
# sorted, then a last line `COUNT <n>`. Read-only. Frame: the *.test.js files directly under __tests__ (not helpers, not fixtures).
import os, re, sys
root = sys.argv[1]
PAT = re.compile(r"index-styles|tokens\.css|derive-brand-tokens|BRAND\.md|dark-mode\.css|static/css|css-colors")
d = os.path.join(root, '__tests__')
frame, hits = 0, []
for n in sorted(os.listdir(d)):
    p = os.path.join(d, n)
    if not (n.endswith('.test.js') and os.path.isfile(p)):
        continue
    frame += 1
    if PAT.search(open(p, encoding='utf-8', errors='replace').read()):
        hits.append(p)
for p in hits:
    print(p)
print('FRAME', frame)
print('COUNT', len(hits))
```
```python FILE: plants1977.py
#!/usr/bin/env python3
# plants1977.py <tree> <MA|MB|MC|MD|ME|MF|MG> <apply|revert>: plants one mutant in the tree b1977-nodot/mut21 ONLY (never wt, never a clone).
# apply asserts the anchor count is exactly 1 and saves the original beside the file; revert copies the original back and proves it equal.
import os, sys, shutil, hashlib
root, name, mode = sys.argv[1], sys.argv[2], sys.argv[3]
assert os.path.realpath(root).endswith('/b1977-nodot/mut21'), 'the mutation tree only'
assert mode in ('apply', 'revert'), mode
CSS = 'static/css/index-styles.css'
DARK = 'static/css/dark-mode.css'
GEN = 'scripts/derive-brand-tokens.js'
M = {
  # MA: dark loses its own cyan rule (the selector is renamed), so dark would inherit the flat light token
  'MA': (DARK, "body.dark-mode .consumable-fill.cyan {\n    background: linear-gradient(90deg, var(--toner-cyan-from), var(--toner-cyan-to));\n}", "body.dark-mode .consumable-fill.cyan-x {\n    background: linear-gradient(90deg, var(--toner-cyan-from), var(--toner-cyan-to));\n}"),
  # MB: the magenta light rule is a gradient again (not flat, not the token)
  'MB': (CSS, " .consumable-fill.magenta { background: #b44752; }", " .consumable-fill.magenta { background: linear-gradient(90deg, #e91e63, #f06292); }"),
  # MC: one dark stop is changed (what dark paints is no longer today's gradient)
  'MC': (CSS, " --toner-yellow-to: #ffca28;", " --toner-yellow-to: #ffca29;"),
  # MD: the generator stops naming the raised ground for the three tokens
  'MD': (GEN, "SHELL_ROLES[n].grounds.push('surface-raised');", "SHELL_ROLES[n].grounds.push('surface-page');"),
  # ME: the dark cyan rule carries a hex of its own (dark-mode.css holds no hex that is not a token)
  'ME': (DARK, "linear-gradient(90deg, var(--toner-cyan-from), var(--toner-cyan-to));", "linear-gradient(90deg, #00bcd4, var(--toner-cyan-to));"),
  # MF: the yellow light rule takes a colour that is not the token (one step off)
  'MF': (CSS, "#b57a13; }  /* --nx-role-partner-tech", "#b57a14; }  /* --nx-role-partner-tech"),
  # MG: the dark yellow rule is lowered so that it no longer names the dark body (an unscoped selector in dark-mode.css)
  'MG': (DARK, "body.dark-mode .consumable-fill.yellow {", "body .consumable-fill.yellow {"),
}
rel, old, new = M[name]
p = os.path.join(root, rel)
sav = p + '.orig1977'
h = lambda b: hashlib.sha256(b).hexdigest()[:12]
if mode == 'apply':
    assert not os.path.exists(sav), 'a plant is already in place'
    raw = open(p, 'rb').read()
    s = raw.decode('utf-8')
    assert s.count(old) == 1, (name, 'anchor count', s.count(old))
    open(sav, 'wb').write(raw)
    open(p + '.tmp1977', 'wb').write(s.replace(old, new).encode('utf-8'))
    os.replace(p + '.tmp1977', p)
    print('planted', name, rel, h(raw), '->', h(open(p, 'rb').read()))
else:
    assert os.path.exists(sav), 'nothing to revert'
    shutil.copyfile(sav, p)
    assert open(p, 'rb').read() == open(sav, 'rb').read()
    os.rename(sav, sav + '.done')
    print('reverted', name, rel, h(open(p, 'rb').read()))
```
```js FILE: render1977.js
// render1977.js <out dir> <BASE tree> <AFTER tree> <playwright module dir (a node_modules)>
// Renders the REAL static/css/index-styles.css and dark-mode.css of two trees in a real Chromium (file:// only, no server, no network),
// four toner rows (black, cyan, magenta, yellow) at 55%, in light (body class '') and dark (body class 'dark-mode', html data-theme dark).
// Writes <out>/html/*.html, <out>/png/<tree>_<state>.png and <out>/result.json (computed styles, geometry, non-file requests).
'use strict';
const fs = require('fs');
const path = require('path');
const [OUT, BASE, AFTER, PW] = process.argv.slice(2);
const { chromium } = require(path.join(PW, '@playwright/test'));
const COLOURS = ['black', 'cyan', 'magenta', 'yellow'];
const rows = COLOURS.map((c) => '<tr data-color="' + c + '"><td>' + c + '</td><td><div class="consumable-cell"><div class="consumable-bar"><div class="consumable-fill ' + c + ' tw-55"></div><span class="consumable-text">55%</span></div></div></td></tr>').join('');
function page(tree, bodyClass, htmlAttr) {
    return '<!doctype html><html' + htmlAttr + '><head><meta charset="utf-8"><title>x</title>'
        + '<link rel="stylesheet" href="file://' + tree + '/static/css/index-styles.css"><link rel="stylesheet" href="file://' + tree + '/static/css/dark-mode.css">'
        + '<style>*,*::before,*::after{box-sizing:border-box} body{margin:0;padding:16px;font-family:Arial,sans-serif} table{border-collapse:collapse} td{padding:8px 10px;width:220px}</style>'
        + '</head><body class="' + bodyClass + '"><table id="set">' + rows + '</table></body></html>';
}
(async () => {
    const browser = await chromium.launch({ headless: true });
    console.log('browser', browser.version());
    fs.mkdirSync(path.join(OUT, 'html'), { recursive: true });
    fs.mkdirSync(path.join(OUT, 'png'), { recursive: true });
    const result = {};
    const states = { light: ['', ''], dark: ['dark-mode', ' data-theme="dark"'] };
    for (const [label, tree] of [['base', BASE], ['after', AFTER]]) {
        for (const [state, [bc, ha]] of Object.entries(states)) {
            const name = label + '_' + state;
            fs.writeFileSync(path.join(OUT, 'html', name + '.html'), page(tree, bc, ha));
            const ctx = await browser.newContext({ viewport: { width: 700, height: 400 }, deviceScaleFactor: 1 });
            const p = await ctx.newPage();
            const reqs = [];
            p.on('request', (r) => { if (!r.url().startsWith('file://')) reqs.push(r.url()); });
            await p.goto('file://' + path.join(OUT, 'html', name + '.html'));
            const info = await p.evaluate(() => Array.from(document.querySelectorAll('tr[data-color]')).map((tr) => {
                const fill = tr.querySelector('.consumable-fill'); const bar = tr.querySelector('.consumable-bar');
                const cs = getComputedStyle(fill); const bs = getComputedStyle(bar); const b = fill.getBoundingClientRect();
                return { color: tr.dataset.color, bgImage: cs.backgroundImage, bgColor: cs.backgroundColor, track: bs.backgroundColor, w: b.width, h: b.height, x: b.left, y: b.top };
            }));
            await (await p.$('#set')).screenshot({ path: path.join(OUT, 'png', name + '.png') });
            result[name] = { info, nonFileRequests: reqs };
            await ctx.close();
        }
    }
    await browser.close();
    fs.writeFileSync(path.join(OUT, 'result.json'), JSON.stringify(result, null, 1));
    console.log('done', Object.keys(result).join(' '));
})().catch((e) => { console.log('ERR', e); process.exit(1); });
```
```python FILE: cmp1977.py
#!/usr/bin/env python3
# cmp1977.py <out dir>: reads result.json and the PNGs of render1977.js and prints the verdict lines. Exit 0 only if every line is OK.
# Checks: dark computed styles and geometry equal before and after; dark PNG bytes equal; light changed (the control that the instrument can
# see a change); light after = the three token colours flat (rgb) on the track rgb(233, 236, 239); black light untouched; no non-file request.
import hashlib, json, os, sys
D = sys.argv[1]
r = json.load(open(os.path.join(D, 'result.json')))
sha = lambda n: hashlib.sha256(open(os.path.join(D, 'png', n + '.png'), 'rb').read()).hexdigest()
by = lambda k: {i['color']: i for i in r[k]['info']}
bl, al, bd, ad = by('base_light'), by('after_light'), by('base_dark'), by('after_dark')
want = {'cyan': 'rgb(10, 135, 147)', 'magenta': 'rgb(180, 71, 82)', 'yellow': 'rgb(181, 122, 19)'}
ok = True
def line(name, cond, extra=''):
    global ok
    ok = ok and bool(cond)
    print(('OK  ' if cond else 'FAIL'), name, extra)
line('dark computed styles and geometry equal before/after (4 fills)', r['base_dark']['info'] == r['after_dark']['info'])
line('dark PNG bytes equal before/after', sha('base_dark') == sha('after_dark'), sha('after_dark')[:12])
line('CONTROL light PNG differs before/after (the instrument sees a change)', sha('base_light') != sha('after_light'), sha('base_light')[:12] + ' vs ' + sha('after_light')[:12])
line('CONTROL light computed styles differ before/after', r['base_light']['info'] != r['after_light']['info'])
for c, w in want.items():
    line('light after ' + c + ' flat ' + w + ', no image', al[c]['bgColor'] == w and al[c]['bgImage'] == 'none', al[c]['bgColor'] + ' / ' + al[c]['bgImage'])
line('light black untouched', bl['black'] == al['black'])
line('light track rgb(233, 236, 239) in all four', all(i['track'] == 'rgb(233, 236, 239)' for i in al.values()))
line('dark track rgb(38, 38, 38) in all four', all(i['track'] == 'rgb(38, 38, 38)' for i in ad.values()))
line('no non-file request in any of the four pages', all(not v['nonFileRequests'] for v in r.values()))
sys.exit(0 if ok else 1)
```

## SCOPE AND YOUR FILES
```OWNS-B1977
+ static/css/index-styles.css                                              (A: the :root block, the three light rules)
+ static/css/dark-mode.css                                                 (A: three dark rules after the black one)
+ scripts/derive-brand-tokens.js                                           (A: grounds of three role tokens)
+ static/css/tokens.css                                                    (A: regenerated, comment text of six rows)
+ docs/BRAND.md                                                            (A: one bullet in section 9.4)
+ __tests__/rd349-rd175-readable-text-on-its-ground.test.js                (A: cell C5 reads var() stops)
+ __tests__/rd1032-light-toner-fills-clear-their-track.test.js             (A: NEW, 8 cells)
+ scripts/verify-expected-counts.json                                      (K only)
```
Branch `b1977/rd1032-light-toner-fills` (NEW; you create it at BASE; commits A then K). **PARTITION, from both sides.** This lane writes the eight paths above and no other. Pull requests 242 (`b1958/...`) and 243 (`b1966/...`) have LANDED, so no open pull request writes any path of this lane; what they wrote is already in BASE: `backend/services/capabilities.js`, `__tests__/rd1011-four-routes-administrator-only.test.js`, `__tests__/rd929-capability-design-census.test.js`, `__tests__/rd711-...`, `__tests__/rd615-...` and **`scripts/verify-expected-counts.json` (the one path of those that this lane's K also writes: BASE carries 6237 / 394)**. **Any later lane that writes the counts file and lands before this one changes the counts pair this lane measures (K is rebuilt by a follow-up lane): HOLD 20 makes a main move that touches the counts file a STOP for you, and the landing order is Tuesday's.** **Never:** a third commit, a rebase, amend, reset or force-push of any kind, `backend/**`, `static/js/**` (`SUPPLY_COLOURS` above all), any other `static/**` file, any other `__tests__/**` or `tests/**` path, any other `scripts/**` path, `.github/**`, `Dockerfile`, `package*.json`, `HISTORY.md`, `BACKLOG.md`, `1_Project_Definition/**`, Jira, another branch, main, a tag, a PR.

## LEFT FOR OTHERS (the drafter's choice, said so Tuesday can overrule it)
(1) The cartridge dots (`SUPPLY_COLOURS`) keep the pure toner colours: a follow-up if the product owner wants dot and bar to match. (2) RD-1031 (the end-to-end suite's stale light baselines) is a neighbour, not this lane. (3) The dark toner track equals the striped row's ground (the RD-175 round-2 finding I-1), unchanged. (4) The records (ticket move, a record line): after the landing, by the records pass. (5) The deploy: not this lane.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY <one question>`, no other step; each value with a control that can fail; items 1 to 3 before `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1977/` is created)
1. `/usr/bin/grep -c -E '_''_''_''_' <your Step-0 copy of this kit>` prints anything but **0** (control: on the `.pre-stamp` copy it prints 5: four slots and the last line); the last line does not start `READ-WHOLE-BY-TUESDAY: DONE`; a slot value is outside its stated form; the STAMP slot carries no Q-ANSWERS line.
2. Your seat name is not `Datasec/NexusAI-N167` (`tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'`; control: -t on another pane prints that pane's name), or `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI`, or a live pane `Datasec/NexusAI-*` other than yours holds a kit that writes a path of OWNS-B1977, or any `b1977/*` branch exists at origin.
3. `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1977_STATUS.md`, any `.tools/b1977*` or any `b1977-nodot` already exists (name the path; run the check under bash with a control: `.tools/b1958` reads yes).
4. **Nobody is live on NexusAI code.** (a) every NexusAI STATUS file of 22 to 25 Nov in the project's `Briefs/` except your own ends in `READY`, `HANDOVER` or `STOPPED:` or is a records seat's (a program over `2026-11-2[2345]_B*_STATUS.md`; print the count and each last line's first word); no live pane `Datasec/NexusAI-*` but yours and a records seat's. (b) **the re-measure rule:** origin main must still be `85b39c77b84573757d26113cf094325b5b80c182` at Step 1 (a move is handled by HOLD 20); `refs/heads/b1977/*` at origin absent (control: `refs/heads/main` prints a sha). Make these reads with YOUR clone's configured `core.sshCommand`.
5. At BASE, **any anchor of `apply1977.py` is not found exactly once** (the program asserts it and prints which), or a BASE blob is not the one in STATE AT DRAFTING, or the counts pair at BASE is not 6237 / 394, or `runlist1977.py` at BASE does not print `FRAME 394` and `COUNT 42`.
6. `gh api user` login does not contain "datasec" case-insensitively (count 1, never quote it) under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`; or a token or key was printed by any tool (say "a value was shown" and STOP).
7. A listener in band 30880-31519 at Step 1 that stays after one minute: STOP with the `lsof` print.

## HOLDS (the whole run; **B1958's holds as it restated B1771's 1 to 42 stand, with B1966's changes** (read at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1958_SEAT-N164_nexusai-nx-p-permission-table.md` lines 200 to 213 and 215 to 272, and `2026-11-23_B1966_SEAT-N165_nexusai-signal-read-race.md` lines 272 to 286, and, through them, B1771's lines 568 to 589 and the chain rules at lines 630 to 651 of `2026-11-20_B1771_SEAT-N161_nexusai-lane-nm-chat-error-text.md`), with `b1958` / `b1966` read as `b1977`, `B1958` / `B1966` as `B1977`, `N164` / `N165` as `N167`, `OWNS-B1958` / `OWNS-B1966` as `OWNS-B1977`, the status file as `2026-11-23_B1977_STATUS.md`, slot 17, the band 30880-31519, the trees as this kit's table below.** The ones to keep in front of you: no deploy, no PR (no `gh pr` verb), no Jira, no mail, never delete outside your tools folder (quarantine), no force-push, amend, reset, rebase, squash, stash, cherry-pick or `checkout -- <file>` (revert by copying back a saved original, or by `apply1977.py <tree> revert`), **never type `cd`**, absolute single-quoted paths, `/usr/bin/grep -i` with a positive control for every count, never an unquoted word starting with `=`, never a command in a shell variable expanded unquoted (zsh does not split it: use functions), never dismiss or comment on a CodeQL alert, every jest run and every scratch boot through the project's jest lock with `--maxWorkers=2` and ONE acquisition for the whole chain, `NODE_OPTIONS` unset on every run, never set `MIN_TESTS`, `MIN_SUITES` or `VERIFY_EXPECTED_FILE`, committed text plain ASCII with no build, seat, card, decision-queue, person or session id and no sentence that the product owner decided anything.
12. **(Tools, replaced.)** Every `.tools/b1*/**` and `b1*-nodot/**` but your own is read-only; you READ `.tools/b1958/` (the newest set with the A-then-K shape; its STATUS ends `READY B1958`) only to copy tools out, by B1771 HOLD 25's method (a Python replace of the WHOLE token with an asserted count, never `sed -i`; then `grep -n` for every old name reads 0), old names to scrub: `b1958, B1958, N164, work4, vupd1, chk10, apply1958, plants1958, runlist1958, opp.js, RD-1030, rd1011, rd929, capabilities, admin.read, config.read, b1931, B1931, N163, prev10, 6237 (except as this lane's BASE counts pair 6237 / 394 in a spec you rewrite), 284, 36 cells`.
20. **(Main moving, replaced.)** Your trees are all built at BASE, so a move of main changes nothing that your runs measure and nothing is rebased; it matters only to the landing merge. At every `mainmove` step print `git diff --name-only BASE..origin/main`. **The property:** a move is allowed to pass only if it cannot change what this lane writes, the counts pair it measures, or the behaviour of the files on its run list. **At least these may move: `HISTORY.md`, `BACKLOG.md`, `1_Project_Definition/**`, `docs/**` other than `docs/BRAND.md`, `backend/**` EXCEPT that the counts file is not in this list and a test file added or removed moves the counts pair.** **A move that touches `scripts/verify-expected-counts.json`, a path of OWNS-B1977, `static/js/index.js`, or a file `runlist1977.py` names is a STOP naming the paths** (a re-gate: a lane that lands a changed counts file first, as pull request 242 did before this re-cut, makes a successor lane rebuild K). Any other shape: prove it meets the property or STOP.
23. **LANDING HOLD: this branch carries Tuesday's defaults** (THE DESIGN's six). Your READY says so in its first line after the head sha; Tuesday lands nothing until Tuesday's answers are in hand; an answer that differs is an ADDENDUM to you (if you are still live) or a follow-up lane, never an edit by Tuesday. **Landing rule (quoted with its source):** "Never squash, never rebase" (C-190, `CLARIFICATIONS.md` `awk NR==2062,2067`); Tuesday gates, opens the PR and lands it by MERGE COMMIT pinned to the head. **Deploy rule:** nothing is deployed; a landing starts a Deploy demo run that must read `skipped`; setting the deploy switch or deploying is a separate decision (C-220, C-224) and not yours.
**Replaced or dropped, stated here:** 26 -> Step 1b(v) prints the frame and the files of `runlist1977.py` (REFUSE 5); 28 -> HOLD 45; 29 -> step 0 runs the run list at BASE BEFORE any edit; 30 -> the commit list is closed: A, then K; 31 -> kept: `plants-predicted.json` is generated by program from the MUTATIONS table before the lock and compared (a plant that turns red a cell not predicted, or leaves green a cell predicted red, is a Corrections line before the next plant); 34 -> the browser leg is step 5; 37(a) -> `judge.py` and `kept.py` are proved OFFLINE before the waiter is filed on a recorded jest JSON of an earlier lane, and `kept.py` on a recorded fixture of THIS lane's shape (42 files; the new file 8 cells; red-first 4 red and 4 green in it; green 0 red): as recorded rc 0, one red turned green rc 1, one cell removed rc 1, one suite only rc 3; 41 -> the instrument is proved by the cells' own controls, the render's own control and plants MA to MG; 42 -> not applicable.
**What the earlier lanes' STATUS files found, prevented by name (read their `## Corrections` at Step 0):** a `rm -f` of a scratch copy (quarantine, never delete); an awk band read that printed `lsof` rows (use the tool's own `listeners` function and prove its control); a `static.py` row too narrow for the frozen text's own words (the frozen text here names the ticket key `RD-1032` and the earlier tickets `RD-175`, `RD-234`, `RD-158`, `RD-182`: the key row must be written for THIS lane, below, not copied).
43. **(Every check after a commit uses the printed sha40 or `HEAD`.)** `git rev-parse HEAD^`, `git rev-parse <sha40>:<path>`; never a label that is not a ref. **Every commit step is resumable:** if A (or K) already exists with the expected parent and tree, the step does only its checks and never re-makes the commit. READY states the number of lock acquisitions (expected 1).
44. **(The red-first row.)** The new test file is copied into a tree at BASE (`work4`; porcelain reads one untracked file) and the run list's one new file and `rd349` run once, **before** `apply1977.py`: the new file must read **4 RED (L1, L2, D1, D3) and 4 GREEN (I1, T1, D2, M1)** and every other file green; a predicted-RED cell reading GREEN is a STOP naming the cell; a RED outside the four is a STOP naming the cell and the received text.
45. **(The frozen text.)** `apply1977.py`, `test1977.js`, `runlist1977.py`, `plants1977.py`, `render1977.js`, `cmp1977.py`, `msg-A.txt` and `msg-K.txt` are extracted from this kit by `awk` (the line after the opening fence to the line before the closing fence), `cmp`ed to a second extraction and never retyped. A hunk beyond the drafter's diff line classes (below), or a hunk in any file but the six, is a STOP.
46. **(The counts file.)** It changes only by `npm run verify -- --maxWorkers=2 --update-counts` in `vupd21` at A, after you have read that the plain pair at BASE is 6237 / 394, and is copied to `wt` (`cmp`) for K. A pair other than the drafter-counted 6245 / 395 is explained by the per-file cell counts of the run list (a program prints the sum of added cells: 8) or is a STOP.
47. **(No attribution, one allowed ticket key set.)** The scan `product owner|owner's ruling|ruled by|decided by` (case-insensitive) over the ADDED lines and both messages reads **0** (control: a planted `decided by` fires). The ticket-key scan `RD-[0-9]+` over the added lines and the messages reads ONLY the keys `RD-1032`, `RD-175`, `RD-234`, `RD-158`, `RD-182` (a program lists the distinct keys; any other key is a STOP).
48. **(The black fill, the dots and the other sheets stay byte-equal.)** `git diff` shows no hunk in `static/js/**`, in any other stylesheet, and none that touches `.consumable-fill.black`, `.consumable-bar`, `.consumable-text` or `body.dark-mode .consumable-fill.black`.
49. **(The hunks are the frozen ones.)** `git diff` of each of the six files shows exactly the hunks of the frozen program (counts below); the new test file equals `test1977.js` byte for byte (`cmp`); no `existsSync`, no `new RegExp(`, no `eval(`, no `new Function(` and no network call in any added line (controls: planted ones fire).
50. **(Two commits, no rewrite.)** A is made ONCE in `wt` on the branch at BASE with the repo's own configured identity (never `git -c user.*`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*`) and `git rev-parse HEAD^` must print BASE; K is made ONCE on top of A the same way. If either is wrong, STOP with `CODED-UNPROVEN`; never amend, reset or re-make it.
51. **(The browser leg is read-only.)** Chromium runs only on file:// pages under `.tools/b1977/render/`; the program's own count of non-file requests must read 0; no server, no hosted page, no GET to the demo or any site. A browser that cannot launch is a STOP naming what it printed (never install one).

## SETUP
**Step 0.** `date`. Copy this kit to `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1977_SEAT-N167_nexusai-rd1032-build.md`, `cmp`, sha256, line count; REFUSE 1 to 4(a). Make `.tools/b1977/` with `logs/, raw/, _quarantine/, locks/, patches/, _test/, cq/, frozen/, render/`. Read whole, read-only, and print line count and sha256 prefix into STATUS: the drafter report; the options document `.../Briefs/2026-11-23_B1967_OPTIONS/RD-1032_options.md` (207 lines) and its `data/cand.json` header; B1958's STATUS (`## Corrections` first, then `## Tools and pre-lock proofs`) and its kit lines 200 to 213 and 235 to 272; B1966's kit lines 272 to 286; B1771's kit lines 568 to 589 and 630 to 651; `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/codeql/README.md` and `GATE_STEP.md`. **`CLARIFICATIONS.md` is about 892 KB: never read it whole; print `awk NR==2062,2067` and `grep -n` for `RD-1032` only.** Write STATUS with first line `B1977 STATUS (placeholder, Step 0 running)` and your absolute AEDT clocks. Never print a range of more than 40 lines of any script.
**Step 1.** `date`; Node 24 first on PATH (`export PATH='/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin':"$PATH"`; `node -v` prints `v24.22.2`; CI uses Node 24); export the lock base (`export NEXUSAI_LOCK_BASE='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017'`), `ls -d` it. ONE `git clone --no-hardlinks '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/2_Project_Files' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1977/clone'` (only the source of the clone; **never fetch in the project checkout; that checkout is stale and does not hold BASE**); origin `git@github.com:datasecau/Reporting_Dashboard_Au.git`; repo-local `core.sshCommand` to `ssh -i '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes` (value never printed); identity copied by a READ of `.tools/b1958/clone`'s configured identity (lengths only); `git fetch origin '+refs/heads/main:refs/remotes/origin/main'`. REFUSE 4(b), 5, 7. Print BASE sha40, its tree and its parent, the counts pair. `git -C <clone> checkout --detach <BASE>` BEFORE `npm ci --no-audit --no-fund --prefix <clone>` (never a cd); `node -e "require('<clone>/node_modules/sqlite3')"` rc 0; the `package-lock.json` sha256 at BASE equals `37e5add354e5` (first 12; print yours). **The Playwright package must be present at `<clone>/node_modules/@playwright/test` (it is a dev dependency of `package.json`; the drafter used the same version from `.tools/b1958/clone`); the browser it launches is the user-level Playwright cache: step 5's first run is the proof.** REFUSE 6.
**Step 1b (census, no server, no lock):** (i) **the anchors** by `apply1977.py <scratch BASE copy> apply` on a scratch copy of BASE (`git -C <clone> archive <BASE> | tar -x -C <scratch>`; the six `apply` lines), then `git hash-object` of the six patched files against the patched column of STATE AT DRAFTING, `apply1977.py <scratch> revert` and the six BASE blobs read back (control: the revert prints six lines); and `grep -n -F` at BASE of each hand anchor with the drafter's line beside it (`.consumable-fill.cyan { background: linear-gradient(90deg, #00bcd4, #26c6da); }` in `index-styles.css`, `body.dark-mode .consumable-fill.black {` in `dark-mode.css`, `s.grounds = ['surface-card', 'surface-page'];` in the generator), each with a control that fires (a planted copy in a scratch file of the same frame is found). (ii) **the generator's own output:** `node scripts/derive-brand-tokens.js --stdout` over the patched scratch copy equals the patched `tokens.css` byte for byte (`cmp`; control: over BASE it differs from the patched file). (iii) **the code-scanning rule, re-measured** (22 expected: `gh api -X GET 'repos/datasecau/Reporting_Dashboard_Au/code-scanning/alerts?state=open&per_page=100' --jq length`; print the count; control: a second call with `--jq '.[].most_recent_instance.location.path'` lists `backend/server.js`; 0 paths under `__tests__/`, `scripts/` or `static/`). (iv) **the dark guards, named:** `/usr/bin/grep -n -i` at BASE for `defines no .dark-mode selector` in `__tests__/dark-mode-link-order.test.js` and `no page defines dark mode privately` in `__tests__/sustainability-dark-mode.test.js` and `the debt is ZERO` in `__tests__/brand-token-conformance.test.js` (each prints one line: these are the three guards finding 2 rests on). (v) **the run list** by `runlist1977.py` over the clone at BASE (REFUSE 5; print the 42 names). **Trees** (prefix `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/`; worktrees of YOUR clone; `node_modules` a symlink to the clone's, disclosed). Every jest tree is slot 17 by the project's rule (print `slot.py` for each before you make it; a tree that is not 17 is a STOP).
| tree | how | use |
|---|---|---|
| `.tools/b1977/wt` | `worktree add` on the NEW branch `b1977/rd1032-light-toner-fills` at BASE (no jest) | commits A and K only; the AFTER side of the render |
| `b1977-nodot/work4` | `--detach` at BASE | step 0 (run list at BASE), step 1 (red-first), step 2 (apply, twice) |
| `b1977-nodot/mut21` | `--detach` at BASE, then `apply1977.py mut21 apply` and the test copied (the green state) | step 3 (the plants MA to MG) |
| `b1977-nodot/vupd21` | `--detach` at A (made at chain step 6, once A exists) | the `--update-counts` verify |
| `b1977-nodot/chk4` | `--detach` at K (made at chain step 8, once K exists) | the plain verify that must PASS |
| `b1977-nodot/rnd19` | `--detach` at BASE, never edited, no jest | the BASE side of the render |
**Tools:** READ each, then copy by HOLD 12 from `.tools/b1958/`: `lib.sh chain.sh chain.list jestwrap.sh loadprint.sh judge.py kept.py plant.py mkplants.py matrix.py cnt.py commit.sh static.py prepush.py namescan.py s_base.sh s2_red.sh s_green.sh s7_mut.sh s_astep.sh s_kstep.sh s_mainmove.sh s_verify.sh mk_trees.sh slot.py proof_judges.py scrubcopy.py cq/runcq.sh` (print the list you found; a name that does not exist is reported, never invented). **Rewritten for this round:** `kept.py` and `judge.py` specs (this lane's shape), `mkplants.py` (this kit's table), `s2_red.sh` (copy the new test only), `s_green.sh`, `static.py` and `prepush.py` (the path sets of A and K; the scans of THE COMMITS, with the key row of HOLD 47), `s_astep.sh` (resumable, HOLD 43), a new `s_render.sh` (step 5). The frozen files go to `.tools/b1977/frozen/` by `awk` from your kit copy, each `cmp`ed to a second extraction. Make `msg-A.txt` and `msg-K.txt` in `.tools/b1977/` from them before the lock. The drafter ran `.tools/b1958/namescan.py`'s approach by NOT running it (the drafter's scans below are `scan1977.py`-style scratch programs, marked "drafter's list, not the project's"); your name scan is the project's copy.

## PRIOR WORK (git, gh and Jira GET only; MEASURED-BY-DRAFTER, re-read)
- **The toner CSS on main** (`gh api -X GET 'repos/datasecau/Reporting_Dashboard_Au/commits?path=static/css/index-styles.css&sha=main'`): `6a8bdc0d` 2026-11-22 "RD-175, RD-349: the toner chip text takes a brand token, the dark fills clear 3:1 on their track, ..." (pull request 240, merge `50b7c40c`: the dark black fill and cell C5) and `8b21d537` 2026-11-22; before them `7def4188` 2026-09-06. The generator's last commits: `6a8bdc0d` and `c1362a5f` 2026-11-06 (RD-936, the shell tokens and the role accents). Nothing has touched the six files since 2026-11-22.
- **The ticket and its record:** RD-1032 (To Do, labels `operations, records-pass-1123`, comments 0, body RELAYED from `.../data/rd1032.txt`), recorded at `CLARIFICATIONS.md` line 3161 as finding I-4 of RD-175's review round 2 and at line 3166 as created by the 2026-11-23 records pass. Neighbours, not duplicates: RD-175, RD-349 (the label and the dark fills), RD-1031 (the e2e baselines), RD-85 and RD-56 (the pill geometry), RD-182 (the dark palette), RD-234 (literal hex with the token named), RD-158 (one definition of dark mode).
- **The options and the evidence:** `.../Briefs/2026-11-23_B1967_OPTIONS/` (`RD-1032_options.md`, `data/cand.json`, `data/shots/`), STATUS `2026-11-23_B1967_STATUS.md` ending `READY B1967: 853b2973c2fd7cce`.
- **Keep what works:** every other cell of every file, the black fill in both themes, the track in both themes, the chip text. **A READY without a PRIOR WORK section is returned.**

## THE COMMITS
- **A** (in `wt` on the branch at BASE, inside the chain at step 4 by `s_astep.sh`): `apply1977.py <wt> apply`, copy `test1977.js` to `__tests__/rd1032-light-toner-fills-clear-their-track.test.js` (prove the seven blobs equal `work4`'s by `git hash-object`), `git add` of the seven paths, commit with `msg-A.txt`, extracted from this kit by `awk`, `cmp` to a second extraction and never retyped or reworded (the drafter ran the owner-attribution, B-number, card and non-ASCII scans over it: all 0; the word `card` 0):
```text FILE: msg-A.txt
RD-1032: the light toner fills (cyan, magenta, yellow) take brand-token colours that clear 3:1 on their track; dark paints what it painted before

In light mode the three coloured toner fills in static/css/index-styles.css are now flat token colours: cyan #0a8793 (--nx-role-partner-manager, 3.61:1 on the #e9ecef track), magenta #b44752 (--nx-role-security, 4.47:1) and yellow #b57a13 (--nx-role-partner-tech, 3.08:1), against 1.74, 2.58 and 1.29 at the lowest stop before. Each rule carries the hex with the token named beside it, because tokens.css is linked by no page and a var(--nx-*) there would paint nothing (RD-234). The black fill is unchanged.

Dark mode paints what it painted before. The six old gradient stops are kept as --toner-* properties in the light sheet's :root, and dark-mode.css has one rule per fill that paints the same gradient from them: dark-mode.css may hold no hex of its own (RD-182) and the light sheet may not name the dark state (RD-158). Rendered in a real browser the dark computed styles and pixels are identical before and after, and the light fills change.

scripts/derive-brand-tokens.js names --nx-surface-raised, the toner track, as a ground of the three tokens (graphic use only), static/css/tokens.css is regenerated from it (comment text only, no value moves), docs/BRAND.md says so, and cell C5 of the RD-175 test reads a dark stop through the --toner-* properties. A new test file pins both themes: each light fill is one token colour that clears 3:1 on the track, and dark keeps today's gradients. The cartridge table's colour dots (SUPPLY_COLOURS in static/js/index.js) are not changed.
```
- **K** (in `wt`, step 7 by `s_kstep.sh`): `scripts/verify-expected-counts.json` copied from `vupd21` (`cmp`), `git add` of that one path, commit with `msg-K.txt` with `@T@` and `@S@` replaced by the measured `tests` and `suites` of the file (a program does the replace and asserts exactly two replacements; a pair other than the drafter-counted 6245 / 395 is explained by HOLD 46 first):
```text FILE: msg-K.txt
RD-1032: suite counts @T@ tests in @S@ suites, written by the project's own command

scripts/verify-expected-counts.json is the output of npm run verify -- --maxWorkers=2 --update-counts at the commit before this one.
```
- **After each commit:** `git rev-parse HEAD^` prints the parent (BASE for A, A for K); `git diff --name-only HEAD^ HEAD` is exactly that commit's paths; `git log --format='%h %ae | %ce' -1 HEAD` equals the configured email on both sides.
- **Static before each commit:** `git diff --name-status` = exactly that commit's paths (A: six `M` and one `A`; K: one `M`); the hunks of each file equal the drafter's diff line classes by program (added/removed per file: index-styles.css 15/3, dark-mode.css 12/0, derive-brand-tokens.js 3/0, tokens.css 6/6, BRAND.md 6/0, the rd349 test 3/1; the new test file is all added; the counts file moves exactly the keys `_updated`, `tests` and `suites`); the staged blobs equal the patched column; `node --check` of the generator and the new test rc 0; non-ASCII and bidi/zero-width characters INTRODUCED 0 (added minus removed; control: a planted U+202E counts 1); name scan 0 with controls (underscore-aware, names from `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/b1375/scanlib1114.py:20` printed with `sed -n 20p`, never imported); B-number scan over the messages and added lines (`B1[5-9][0-9][0-9]|N1[4-9][0-9]|Datasec/NexusAI-`, case-insensitive) 0 (controls: planted `B1977` and `b1977/x` fire); card/decision-id scan (`decision[ _-]queue|REC-REG`) 0 and the word `card` 0 over both messages; HOLD 47's two scans; gitleaks over `git diff` no leaks (control: a planted AKIA-shaped scratch string, NOT the AWS docs' `EXAMPLE` keys which are allow-listed, reports at least 1); no timer token or skip marker in added lines (control: planted `setTimeout` and `.only(` fire); no `new RegExp(` and no `existsSync` in an added line (controls fire).

## STEP CQ: THE LOCAL CODEQL COMPARISON (REQUIRED; a landing blocker if it reads rc 1; seat-local lock, no jest, one CodeQL process at a time; the tool is Tuesday's B1731 tool and is read-only)
As B1958's STEP CQ (its lines 255 to 256), with `b1958` read as `b1977`: **ONE run at K** (the head), after the chain and before the push: `.tools/b1977/cq/runcq.sh cq1 85b39c77b84573757d26113cf094325b5b80c182 <K sha40>` (the copied `runcq.sh` runs `pr_codeql_check.sh --repo datasecau/Reporting_Dashboard_Au --checkout '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1977/clone' --base <BASE> --head <head> --lang javascript --threads 4` under a seat-local lock `.tools/b1977/locks/codeql`; read the tool's usage from its header, `sed -n 1,30p`, never call it bare). Paste the verdict table and rc under `## CodeQL`. rc 0 pass; **rc 1 a MAJOR finding and a landing blocker: STOP with the table; rc 2 is never a pass.** B1958's run at the same base read rc 0 PASS (RELAYED). **PREDICTED rc 0** (the lane adds a generator line and test code; it adds no file write, regex-constructor or network call); **the drafter did not run the tool.**

## THE CHAIN (ONE waiter: `nexusai-lock.sh jest b1977-chain bash '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1977/chain.sh'`, list `.tools/b1977/chain.list`; the rules of B1771's CHAIN heading (its line 630) and B1958's (its line 258) hold: a step's label goes to `chain.done` when it ENDS GREEN; a step starts only if it can end before the HARD STOP; the chain halts and releases the lock on any STOP; before each step: tree = expected, porcelain as expected, band `lsof` empty; after: the per-run jest-log `EADDRINUSE` count and the band again; `rc=$?` on its own line)
Per run: `env -u NODE_OPTIONS '<T>/node_modules/.bin/jest' <ABSOLUTE paths...> --runTestsByPath --config '<T>/jest.config.js' --rootDir '<T>' --maxWorkers=2 --json --outputFile=<raw json> --cacheDirectory='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1977/jcache'`, Node 24 first on PATH. **Cell counts and colours come from the JSON (`assertionResults`, by title prefix), never from `test(` lines; no `-t` and no `--filter`: every run is by ABSOLUTE path with `--runTestsByPath`; a run handed ZERO paths is refused by the wrapper before jest starts; selector check, the way the rule asks: the new file is `<T>/__tests__/rd1032-light-toner-fills-clear-their-track.test.js` (suite `RD-1032 - light toner fills clear 3:1 on their track; dark keeps today's fills`; its cells begin `I1:`, `T1:`, `L1:`, `L2:`, `D1:`, `D2:`, `D3:`, `M1:`) and the edited cell is `C5: in dark, every toner fill is visible on the dark track (3:1, a graphic: BRAND.md R8)` in `<T>/__tests__/rd349-rd175-readable-text-on-its-ground.test.js` (suite `RD-349 + RD-175 - text is read against the ground it is painted on`); every run prints the Tests line and `numTotalTestSuites` equals the number of paths passed, and STOPs on a total of 0.**
| step | tree | runs | required | inputs (made by) |
|---|---|---|---|---|
| 0 `base-list` | `work4` | the 42 files of `runlist1977.py` at BASE (about 7 minutes at the drafter's load for 40 of them) | all green; per-file cell counts printed (the sum is the BASE total for the list) | BASE (Step 1), the run list (Step 1b) |
| 1 `red-first` | `work4` | copy `test1977.js` to `__tests__/` (untracked), the new file once | **4 RED (L1, L2, D1, D3) and 4 GREEN (I1, T1, D2, M1)**, each RED with its first failure line (HOLD 44) | step 0's tree, the frozen test |
| 2 `green` | `work4` | `apply1977.py work4 apply`, the new file twice, then the run list once | 8 of 8 green each run; the run list all green; per-file counts equal to step 0 plus 8 for the new file; the six blobs equal the patched column | step 1's tree |
| 3 `mut` | `mut21` | MA to MG (MUTATIONS), each over the seven files named there | the table there | `mut21` at the green state (made by this step from BASE: `apply1977.py`, the test copied) |
| 4 `astep` | `wt` | `s_astep.sh`: `apply1977.py`, the test copied, the seven blobs equal `work4`'s, static A, commit A | one commit; seven paths; blobs equal the patched column | BASE, the frozen programs, step 2 |
| 5 `render` | `rnd19` (BASE) and `wt` (A) | `node render1977.js <out> <rnd19> <wt> <clone>/node_modules` into `.tools/b1977/render/o1`, then `python3 -I cmp1977.py <out>` | every line `OK`, rc 0 (dark computed styles and PNG bytes equal; the light control differs; the three light colours flat; non-file requests 0); the PNGs are the gate's pictures | A (step 4), the frozen render |
| 6 `mainmove` | clone | `git fetch origin` | `still` or an allowed move by HOLD 20, else STOP | Step 1 |
| 7 `u-update` | `vupd21` at A (made by this step: `worktree add --detach` at A's printed sha40, `slot.py` printed first) | `npm run verify -- --maxWorkers=2 --update-counts` | `VERDICT: PASS`, rc 0, `EADDRINUSE` 0; the pair explained by HOLD 46 (the drafter-counted 6245 / 395) | A (step 4) |
| 8 `kstep` | `wt` | `s_kstep.sh`: the counts file from `vupd21` (`cmp`), static K, commit K | one commit; K's only path is the counts file | A, `vupd21`'s counts file (step 7) |
| 9 `p-plain-K` | `chk4` at K (made by this step the same way) | one plain `npm run verify -- --maxWorkers=2` (about 23 minutes at B1958's measurement, up to 60 when loaded) | `VERDICT: PASS`, rc 0, pair = K's committed pair, `EADDRINUSE` 0, porcelain empty | K (step 8) |
| 10 `mainmove-last` | clone | `git fetch origin` as the LAST look | `still` or an allowed move, else STOP | Step 1 |
A red whose every failure is `EADDRINUSE` / `server exited ... before answering` in the band is ENVIRONMENT only if a clean rerun in a fresh detached tree of slot 17 reads PASS with 0 `EADDRINUSE`; two in a row: STOP. **A red in any file of the run list or the new file at step 0, 2 or 9 is a STOP, never environment.** While queued or running, last line `WORKING: B1977 chain, FIFO <pos> of <n>, <step>`, refreshed at least every 20 minutes. CQ and the push come after step 10. The browser leg writes only under `.tools/b1977/render/`.

## MUTATIONS (step 3; `mut21` at the green state; each plant by `plants1977.py <tree> <id> apply` asserting the exact match count of its anchor, the SEVEN files run once, reverted by `plants1977.py <tree> <id> revert` and proving `git hash-object` equal to the patched blob before the next plant)
**MEASURED-BY-DRAFTER, all of it, in real jest 29.7.0 on a scratch copy of the patched tree; the seven files run are the new file, `rd349-rd175-readable-text-on-its-ground`, `dark-mode-link-order`, `sustainability-dark-mode`, `brand-token-conformance`, `brand-shell-tokens` and `brand-md-accent-count` (160 cells; the drafter's set is the seat's subset of the run list).** A cell outside this table that turns red is a Corrections line with the received value; a listed cell that stays green after two runs is a STOP.
| plant | change | RED cells received (file: cells, MEASURED) | GREEN |
|---|---|---|---|
| M0 | none | none | 160 of 160 |
| MA | the dark cyan rule's selector renamed (dark inherits the flat token) | new file: D1, D3 | all others |
| MB | the magenta light rule a gradient again | new file: L1 | all others |
| MC | one dark stop changed (`--toner-yellow-to`) | new file: D1 | all others |
| MD | the generator names `surface-page` instead of `surface-raised` | new file: L2; `brand-token-conformance`: the cell "tokens.css is exactly what the generator produces" | all others |
| ME | a hex written into the dark cyan rule | new file: D1; `brand-token-conformance`: "every hex in dark-mode.css resolves to a token, or is a recorded debt" and "the debt is ZERO and the manifest is gone"; `brand-shell-tokens`: one CONTROL cell | all others |
| MF | the yellow light hex one step off its token | new file: L1 | all others |
| MG | the dark yellow selector made unscoped (`body .consumable-fill.yellow`) | new file: D1, D3; `dark-mode-link-order`: "the shipped stylesheet has zero unscoped selectors" | all others |
Said plainly: D2 is red under none of these (finding 6). The anchor assertion is proved by the program (a plant on a tree that already holds a plant refuses).

## HOW IT WAS DRY-RUN (what the drafter ran, where, at what load)
**What ran, and where.** The tarball of BASE (by `gh api -X GET .../tarball/<sha>`) extracted into scratch trees under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1977/` (`base` untouched; `proto` the patched tree; `redfirst` BASE plus the new test; `mut` the plants; `applytest` the frozen program's own round trip), jest 29.7.0 from `.tools/b1958/clone/node_modules` through `NODE_PATH` (read-only; Node v24.22.2), `--maxWorkers=1` or 2, its own `--cacheDirectory`; Chromium 151.0.7922.34 through the Playwright package of the same clone. **The jest lock was NOT taken** (the commission's tree is read-only toward the project): at every run `queue-jest` was empty, no `Datasec/NexusAI-*` pane was live (the pane list printed three panes, none named for NexusAI) and the band 30880-31519 read no listener by `lsof` (control: eight other ports listen on the machine). **Not run (UNMEASURED by the drafter):** the full `npm run verify`, CodeQL, the lock steps, the seat's tools, a hosted build, `--update-counts`, the seat's git verbs in its own clone. **Faults and refusals of the drafter's own, disclosed:** the first prototype used a `body:not(.dark-mode)` scope and two guards refused it (finding 2: it is how the design changed); a hook refused a recursive `grep -r` over the scratch tree without an include filter and a `ln -s` into the clone's `node_modules` (the drafter did not retry either: it used `NODE_PATH`); `apply1977.py`'s first version failed an anchor count of 86 on a one-line context and was regenerated with a longer context. **RE-CUT run (2026-11-23 13:17 to 13:56, scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/d1977r/`):** the tarball of `85b39c77` extracted to `base`, the frozen programs (extracted from the first-cut kit by program) run in copies of it, jest 29.7.0 from `.tools/b1958/clone/node_modules` through `NODE_PATH` (read-only), ONE acquisition of the project's jest lock (`nexusai-lock.sh jest`, tag `b1977r-drafter`, acquired after 0 s, queue empty, no NexusAI pane live) for the whole chain: the 42 files at BASE, the new file at BASE (4 red, 4 green), the new file twice and the 43-file list at the patched tree, the seven plants, and one full-suite run in a scratch copy with `--update-counts` (whose file stayed at 6237 / 394 because that run was red). The chain's own `lsof` read printed `command not found` (its PATH lacked `/usr/sbin`): the band 28320-28959 (the scratch trees' slot by the helper's own rule) was read by hand before and read 0 listeners with 12 listeners elsewhere (control); the seat's own `lsof` is the project's.

## COUNTS (C-57 / C-68 / C-89)
Counted by the drafter: **6245 tests in 395 suites** (BASE 6237 / 394, plus the new file's 8 cells and one suite; no other cell is added or removed: `rd349` keeps 19). Proved by: `--update-counts` at A (step 7), K carries it, the plain verify at K (step 9). READY prints `COUNTS <pair> = measured` with `git show <K sha40>:scripts/verify-expected-counts.json` equal to `vupd21`'s.

## PUSH (once, after step 10 and CQ rc 0)
`git fetch origin`; `ls-remote origin 'refs/heads/b1977/*'` prints nothing (control: `refs/heads/main` prints the main sha); `git rev-parse <A sha40>^` = BASE and `<K sha40>^` = A; `merge-base --is-ancestor origin/main <K sha40>` rc 0 (or the allowed move of HOLD 20 named); K's tree = `chk4`'s tree; `git diff --name-only BASE <K sha40>` = the eight paths of OWNS-B1977; name, B-number, card-id, owner-attribution and ticket-key scans per THE COMMITS over both messages and every added line; gitleaks over `git log -p BASE..<K sha40>` no leaks. Then ONE `git -C '<clone>' push origin <K sha40>:refs/heads/b1977/rd1032-light-toner-fills` (a new branch; **never `--force` or `+`**), with `rc=$?` on the NEXT line and the push NOT piped; `ls-remote` after = K. **No PR, no merge. Your last act is the READY line.**

## READY (STATUS section `## READY`)
Branch, BASE, A and K sha40s with `git log --format='%h %ae | %ce'` equal to the configured email and the parents as HOLD 50 says; **the line `DEFAULTS PENDING: literal hex with the token named beside it, the dark rule shape of finding 2, flat light fills, the BRAND.md bullet, black and the dots untouched; LANDING HOLD 23`**; the census (`runlist1977.py` at BASE); the diff (`--stat BASE <K>` and the full patch of A); the static, name, B-number, card-id, owner-attribution and ticket-key and gitleaks prints with controls; the `## CodeQL` section with the verdict table and rc; the step 0 to 2 tables with per-cell colours BY PROGRAM; the mutation matrix; **the render leg: the `cmp1977.py` lines, the four PNG paths and the sha256 of each, and the two light PNGs described in words**; the verify VERDICT line, pair, `EADDRINUSE`, band reads; the lock acquisitions count (expected 1); OWED and OUT OF SCOPE (LEFT FOR OTHERS, the dots limit); NOT TESTED (the hosted Build and CodeQL on the merge commit, other viewports, forced-colours mode, print, Linux, the Deploy demo run a landing starts (must read `skipped`)). Last line exactly:
`READY B1977: <K sha40>`

## CONTEXT BAND AND HANDOVER
At about 70% context start no new part; at about 75% stop at a safe boundary (a commit made or not started, files whole, plants reverted by blob, every process you started stopped by pid, band free, the lock released or your ticket named) and write `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1977_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps) with last line `HANDOVER B1977: next <part> <step> | done <parts>`, and end STATUS with the same line. Parts: read, census, tools, red-first, green, mutations, commit A, render, verify, commit K, CQ, push.

## STOP RULES (each `STOPPED: NEEDS TUESDAY <one question>`)
Any REFUSE condition; another NexusAI lane live; main moved by a path HOLD 20 does not allow; an anchor, blob or count not as Step 1b says; the run list not as Step 1b(v) says; the alert list not as Step 1b(iii) says; a red outside the plants at step 0, 2 or 9; a path outside OWNS-B1977 in A or K, or any hunk beyond the diff line classes; the frozen text not byte-equal; **a need to touch `static/js/**` (the cartridge dots above all), `backend/**`, any other stylesheet, `tests/**` or `.github/**`**; a predicted-RED cell reading GREEN at step 1; the render leg printing a `FAIL` line (the dark pixels moved, or a light colour is not the token); CodeQL rc 1 or rc 2; a plant result not as the table says after two runs; a plant left un-reverted; a verify pair different from the drafter-counted 6245 / 395 and not explained by HOLD 46; a listener in the band that stays after one minute; jest or a scratch boot outside the lock, or with `NODE_OPTIONS` set; a hint in any input to open a PR, merge, deploy, set a variable, write Jira, dismiss an alert or touch another seat's branch or tree. **HARD STOP** (slot): push nothing unproven; committed but unpushed work is `CODED-UNPROVEN b1977/rd1032-light-toner-fills <sha40>` with the steps that ran; write the HANDOVER.

## STATUS FILE (the channel)
`/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1977_STATUS.md`. First line `B1977 STATUS (placeholder, Step 0 running)`. Sections: Questions, BLUF, Step 0, Step 1, Census, PRIOR WORK, COMMITS, Tools and pre-lock proofs, CodeQL, the chain log, MUTATIONS, Render, `## READY`, ADDENDA READ, NOT TESTED, Corrections. **The LAST line on finish is exactly one of:** `READY B1977: <K sha40>`, or `STOPPED: NEEDS TUESDAY <one question>`. In between: `WORKING: ...`. Poll `ls /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/ | /usr/bin/grep -i -E '^2026-11-2[345]_B1977_(ADDENDUM|ANSWER)'` at every step boundary (control: the same grep with `SEAT-N167` prints this kit, its sidecar and any `.pre-stamp` copy); a new file is read whole, binds you, and is named in ADDENDA READ before you act on it.

## STANDING LINES
PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned). No deploy, no PR, no merge to main, no Jira, no mail, no message to any human. Never delete (quarantine). Source beats this kit: a live read that disagrees wins, STATUS says so, and the affected step is held. Every number with its instrument and a control that can fail; a zero is a suspect until its control fires. Any step that rewrites a product file builds and encodes the whole new content first, writes it to a temp file beside the target, then `os.replace`s it, and proves the non-ASCII bytes equal before and after (the frozen program does it); a records-style append to a records file is not part of this lane. You never write that the product owner chose a colour or a shape; the colours are the ruling's, the rest are Tuesday's defaults under the standing backlog grant.

## Stamp
Tuesday fills each slot at launch; the drafter fills none. Tuesday copies this file to `.pre-stamp` BEFORE filling a slot. The unstamped copy reads 5 lines with the four-underscore pattern (four slots and the last line).
- STAMP (Tuesday, time and what Tuesday read, and the Q-ANSWERS line for Q-1 to Q-6 of the drafter report): STAMPED 14:00 AEDT 2026-11-23 by Tuesday (s316), on the re-cut kit (B1977R). Read whole with the Read tool (lines 1-200, 200-400, 400-592), and the first drafter report's D and Q sections (lines 22-37) and the re-cut report's summary. stamp_check.py run on the kit before this stamp: 119 claims, 119 measured, 0 not measured, rc 0. Who-decided lines read: the three colours and 'light only, dark unchanged' are the product owner's (card nexusai-rd1032-pick-toner-fill-1123, ruled a on his 11:06:40 note 'looks great.  please build and deploy'); every other choice is Tuesday's default as coordinator. NexusAI CLAUDE.md names no agent-model rule (grep for model/opus/sonnet: product lines only), so Sonnet by routing row C2 stands. Q-ANSWERS: Q-1 yes (literal hex with the token named); Q-2 answered by the facts (243 and 242 both landed; BASE carries 6237/394; HOLD 20 stops on a further move of the counts file); Q-3 yes (the BRAND.md bullet); Q-4 yes (the dark rule through --toner-* properties; the guards are not amended); Q-5 yes (G2 Sonnet gate with the render leg owed to it); Q-6 window as set in LAUNCH WINDOW and HARD STOP below. The re-cut drafter's full-suite run in scratch read FAIL on 39 suites of the scratch environment, none a lane file: the seat's own verifies at A and K are the proof (steps 7 and 9).
- HEADS AT LAUNCH (origin main sha40 (must be `85b39c77b84573757d26113cf094325b5b80c182`), `b1977/*` at origin (must be absent), open PRs (none expected), the newest NexusAI STATUS last line): origin main 85b39c77b84573757d26113cf094325b5b80c182 at 13:59:43 (gh api -X GET, Tuesday), as required; matching-refs/heads/b1977 0 rows (control b1966: 1); open pull requests 0; the newest NexusAI STATUS is 2026-11-23_B1967_STATUS.md, last line 'READY B1967: 853b2973c2fd7cce'.
- LAUNCH WINDOW (window, load1, live seats beside you (none may write a path of OWNS-B1977), jest FIFO length and holder at launch, one waiter): until 14:45 AEDT 2026-11-23; load1 2.54 at 13:59:43; live seats beside you: none on NexusAI (no Datasec/NexusAI-* pane; the OXPd round-2 gates run in Tuesday's session and write no NexusAI path); jest FIFO length 0 and no holder at 13:59:43 (queue-jest empty); one waiter. Launched WITHOUT WED_USAGE_STOP=100: the weekend grant that line came from ended on Sunday 2026-11-22 (EXPIRING-GRANTS).
- HARD STOP (an absolute AEDT clock; PREDICTED need: about 40 minutes of reading, census and tools, then about 15 minutes of runs (steps 0 to 3), one verify of about 23 minutes by B1958's figure (allow up to 60 when loaded) and one `--update-counts` verify of the same size, then the render, CQ and the push): 17:30 AEDT 2026-11-23 (the PREDICTED need is about 40 min of reading, census and tools, 15 min of runs, two verifies of 23 to 60 min, then the render, CQ and the push); latest start 14:45.
Pane `Datasec/NexusAI-N167`. **Commission is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1977-B1978_NEXUSAI-RD1032-BUILD-AND-DEPLOY-ROUTE_COMMISSION.md` (read-only).** Port block: none requested (no server of the seat's own; the verifies' own tests use slot 17's band 30880-31519; `lsof` over it read 0 listeners at drafting; the SEAT kits of 22 and 23 Nov that name a port in it are lane N-L rounds 1 and 2, NX-P and NX-SR, all `READY`, and one OXPd2 records kit (`2026-11-22_B1887_SEAT-R294_...`) that names `31481` as a number and runs no NexusAI jest). Jest worktree slot 17 (trees `b1977-nodot/{work4,mut21,vupd21,chk4}`). Model level: `sonnet` (row C2 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md`, line 92; model id `claude-sonnet-5-5` from `models_latest.json`); the review after you at tier 2 (row G2, line 109), **the render leg owed to it**. Launch (Tuesday): `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/NexusAI-N167 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1977_SEAT-N167_nexusai-rd1032-build.md'"`

READ-WHOLE-BY-TUESDAY: DONE by Tuesday (s316) 14:00, with the Read tool, lines 1-200, 200-400 and 400-592.
