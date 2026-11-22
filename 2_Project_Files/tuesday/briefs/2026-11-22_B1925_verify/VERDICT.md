GATE B1925: NO GO @ 081f422 on main 8858e5d

Independent review, tier 1 with a rendered leg in light and dark. Lane N-L: RD-349 and RD-175. Branch
`b1911/nexusai-lane-nl-brand-contrast`, head `081f4221f442bbd7ee68be6475f5f64280d558d5`, BASE = main
`8858e5d11ec101de0a49a819c2d29f4eadf95c40`. Round 1.

Clocks (AEDT, 2026-11-22, from `date`): first read 22:09:51; jest lock acquired 22:15:44 (one acquisition, tag
`b1925-gate`, 0 s wait, queue empty, no NexusAI pane live), released 22:39:11.

Trees: my own clone of the builder's clone (push URL `invalid://no-push`; the branch sha and its tree
`d9dd23ae516364f6109b0db68ed3a51c036a95b4` equal GitHub's by `gh api`) under
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/g1925/`. Worktrees there, all on jest slot 10 (band
26400-27039), printed by the project's own `worktreeSlot()`: `h5` the head, `b4` the BASE, `v0` the verify.
`node_modules` is a symlink to the builder clone's (`.tools/b1911/clone`; lockfile blob = BASE's). Jest and the verify
ran on Node v24.22.2 (first on PATH), `NODE_OPTIONS` unset. The ratio program ran on Node v26.13.0 (pure arithmetic).

Blocker 0 | Major 1 | Minor 3 | Info 7

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| **Major** | **F-1. The toner chip's light text colour `#212529` is off-guide.** It is not a token: 0 hits in `docs/BRAND.md`, in `static/css/tokens.css` and in `scripts/derive-brand-tokens.js` (case-insensitive counts; the same reads find `#333333` and `#00719f`). It is Bootstrap's body colour. At BASE, `index-styles.css` carried it only in two comments, and both comments reject it by name: `:1459` "#333333 at 7.75:1 rather than Bootstrap's #212529 at 9.06 ... the token is the point" and `:1472` "The value is --nx-text-strong (#333333 ...), not Bootstrap's #212529". So the lane adds the first `#212529` declaration to that sheet. BRAND.md section 8 rule 1: "Use a token. If none fits, the gap is a brand decision". Tokens fit here. The guards cannot see it: the light sheets are checked by pinned counts only (BRAND.md 8.3), and cell C1 accepts any six-digit hex. Not in the kit's Q-list and not in Tuesday's stamp; no Q-answer covers it. The commission: off-guide is a Major. | One literal, the coordinator's choice. (a) **`#333333` `--nx-text-strong`, 12.635:1 on white**: the token the RD-194 rule chose over `#212529` by name. Its light count is pinned (`derive-brand-tokens.js` `text-strong` 22), so the pin goes to 23 with a call-site comment (the RD-194 / RD-283 shape) and `tokens.css` is regenerated (`x22 measured` sits in it). That is 2 more paths. (b) **No pin moves**: `#636c73` `--nx-text-secondary`, 5.353:1 on white; BRAND.md 9.4 says it clears 4.5:1 on card, page and raised; it carries no pinned count. (c) `#00719f`, 5.437 on white, the same colour as the three texts. Either way: the ratio comment, the plant P5 anchor and the pr-body figure 15.43 change; the test file does not. |
| Minor | F-2 (rendered leg, new in dark). **The dark toner track `#313131` swallows the black fill.** The black fill gradient `#2c3e50` to `#34495e` reads 1.184 to 1.400 against `#313131`; on the light track it read 9.262 to 7.834. Magenta drops to 2.992. Cyan and yellow gain (1.94 to 5.66, 1.38 to 7.98). Visible in `rendered-head-dark.png`: the black bars look empty. The chip still states the value, so no information is lost and no text pair fails. | Not a landing blocker on its own. For the records: a dark track that separates from all four fills, or a dark black-fill counterpart. Raise it when F-1 is re-cut if the coordinator wants it in this lane. |
| Minor | F-3 (docs, pre-existing since RD-251). **`docs/BRAND.md` R5 still says `#00719f` is "on text-bearing chrome only" and "it is never text".** RD-251 put it as text on the light page ground (the `.tab-button` comment records that). This lane adds three more light text uses. BRAND.md never mentions RD-251. The R5 numbers (3.45, 3.13, 2.78) are dark grounds, where the lane covers every use with a dark rule (D3, D4). | Records: a BRAND.md line saying `#00719f` is legal as LIGHT text on white (5.44), page (5.16) and raised `#e9ecef` (4.585, measured by the repo helper), and never as dark text. Out of this lane's paths. |
| Minor | F-4 (cells). **The drag-over and file-chosen states of the drop zone are pinned by no cell.** In the engine: light drop text 4.900 on the drag-over composite `241,243,249` and 4.979 on the file-chosen composite `238,247,243` (BASE 3.135 and 3.185). They clear by 0.40 and 0.48. The new file reads `.file-drop-zone` white only. | A cell that composites `.file-drop-zone.drag-over` and `.has-file` over `.import-section` (a follow-up, or the re-cut). |
| Info | I-1. The KPI label is now `#00719f` under the `#0096d6` value: blue on blue (`rendered-head-light.png`). The drafter's Q-1 named the alternative `#495057` (8.18). Tuesday answered Q-1 with `#00719f`; recorded, not reopened. | None. |
| Info | I-2. The chip ground is written `white`, not `#ffffff`, so the pinned `surface-card` count (51) does not see it. That is Tuesday's Q-5 answer. The keyword resolves to the `--nx-surface-card` value. | None. |
| Info | I-3. Dark KPI label `#8c8c8c` on the tile gradient reads 5.068 on the first stop and 4.500 on the last. Unchanged by this lane; D1 holds it at 4.5. | None. |
| Info | I-4. Every other dark colour the lane writes is a token: `#313131` (`--nx-border` dark / surface-3), `#dedede` (`--nx-text-strong` dark), `#1c1c1c` (dark card), `#8c8c8c` (`--nx-text-muted` dark). `#00719f` is `--nx-brand-chrome`, the RD-251 literal C-258 points at. | None. |
| Info | I-5. The e2e contrast suite: its `.consumable-text` allow-list entry is now dead and `tests/e2e/light-baselines.json` is stale. The kit leaves both to a later lane (outside `npm run verify`). | Records: one ticket. |
| Info | I-6 (builder's process, Corrections 1 to 14). Two typed `cd`, one `git reset` in a throwaway scratch tree, an uncaptured push rc, renamed slot-17 trees and two kit-tool files that did not exist. None has a product effect. The remote head is `081f4221` by my own `gh api` read. The builder's heads census named two stale heads (`rd-334-...`, `rd-427-...`); neither is live work (head commits 2026-09-06 and 2026-09-14, behind main by 1221 and 1126, no open PR). | None. |
| Info | I-7 (gate's own process). The browser harness was dry-run once at the head outside the jest lock (one headless Chromium, about 3 s; output in scratch `out/dry/`) to prove it, before the one lock acquisition. One `cd /dev/null` that failed sat inside a subshell of a loop line and changed nothing. The BASE copy of the new test file was moved to `_quarantine/`, never deleted. | None. |

## WHAT WAS MEASURED

### Scope (item 3)
- `gh api compare main...head`: status `ahead`, ahead 4, behind 0, merge base `8858e5d1` = main; 0 open pull requests.
- `git diff --name-only 8858e5d1 081f4221`: exactly the five paths: `__tests__/fixtures/index-light-failure-baseline.json`
  (+3 -5), `__tests__/rd349-rd175-readable-text-on-its-ground.test.js` (+235), `scripts/verify-expected-counts.json`
  (+3 -3), `static/css/dark-mode.css` (+13), `static/css/index-styles.css` (+18 -7). 272 insertions, 15 deletions.
- Commits A `8b21d537`, F `493ad19e`, T `8f4b7166`, K `081f4221`. Author and committer equal on all four. Every message
  ends with the Co-Authored-By line. No message attributes a choice to the product owner. A's message: "The colours
  are the coordinator's defaults".
- Braces balanced: `index-styles.css` 249/249 at BASE and head; `dark-mode.css` 193/193 to 195/195.

### Colours against BRAND.md and the ruling (item 1)
| written | where | token | verdict |
|---|---|---|---|
| `#00719f` x3 | light text of the three greys | `--nx-brand-chrome`, the RD-251 literal C-258 applies | ruling's literal (F-3 for the docs) |
| `#212529` | light chip text | none | **off-guide: F-1** |
| `white` | light chip ground | `--nx-surface-card` value | token value, keyword (I-2) |
| `#8c8c8c` | dark `.drop-text` (list join) | `--nx-text-muted` dark | token |
| `#313131` | dark track | `--nx-border` dark / `--nx-surface-3` | token |
| `#dedede` on `#1c1c1c` | dark chip | `--nx-text-strong` dark on dark card | tokens |

### Ratios, by the repo's own `contrastRatio` (`__tests__/helpers/dom.js`; my program `progs/ratios.js`, output identical from the BASE and head helper; control `#000` on `#fff` = 21.000)
| pair | ratio |
|---|---|
| `#7f8c8d` on `#ffffff` (BASE KPI label, drop text) | 3.478 |
| `#00719f` on `#ffffff` (head) | 5.437 |
| `#7f8c8d` on `#f8f9fa` (BASE description) | 3.299 |
| `#00719f` on `#f8f9fa` (head) | 5.158 |
| `#ffffff` on `#e9ecef` (BASE toner label, both modes) | 1.186 |
| `#212529` on `#ffffff` (head chip) | 15.426 |
| `#dedede` on `#1c1c1c` (head dark chip) | 12.667 |
| `#7f8c8d` on `#1c1c1c` (BASE dark drop text) | 4.900 |
| `#8c8c8c` on `#1c1c1c` (head dark drop text) | 5.068 |
| `#00719f` on `#1c1c1c` (the trap, if no dark rule) | 3.135 |
| `#8c8c8c` on `#262626` (dark description, KPI last stop; unchanged) | 4.500 |
| `#333333` / `#636c73` / `#495057` on `#ffffff` (F-1 options) | 12.635 / 5.353 / 8.176 |
Every ratio comment the lane writes (5.437, 5.158, 5.437, 15.426, 12.667) equals these.

### The new test file (item 1): red at BASE, green at head (Node 24, jest 29.7.0, JSON judged by title prefix)
- BASE (`b4`, the head's file copied in untracked, `cmp` equal): 15 cells, **8 red: L1 L2 L3 L4 D3 C1 C2 C4**; 7 green:
  I1 R1 D1 D2 D4 C3 M1. Each red for the property's reason (L1 to L3: Expected `#00719f`, Received `#7f8c8d`; L4: the
  grey still on a rule; D3, C2, C4: the rule or declaration is absent; C1: no opaque ground). Equal to the kit's table.
- Head (`h5`), twice: 15 of 15 green each run.
- What the file cannot see: C1 checks that the chip colour is a six-digit hex, not that it is a token (F-1). No cell
  covers the drop-zone states (F-4).

### Outside the frame (item 1)
- **Who shares the changed selectors.** `index-styles.css` is linked by `static/index.html` only (the other hits are
  comments in other sheets). In shipped markup: `.file-description` x3 and `.drop-text` x3 in `index.html`;
  `metric-label` x7 and the toner pill (`consumable-bar`, `consumable-text`) x1 template in `static/js/index.js`. No
  other stylesheet defines these selectors. The `.metric-card` block at `index-styles.css:815` is a media-query
  padding override only.
- **Hover.** `.metric-card:hover` moves the tile only. The engine reads the same label colour and ratio while hovered,
  in both modes.
- **Focus.** Focusing the first `label.file-select-btn` (tabindex 0) leaves the drop text at 5.437 light and 5.068 dark.
  The button's own white on `#667eea` is pre-existing (`label.file-select-btn x3` stays in the baseline).
- **Drop-zone states.** Drag-over and file-chosen: see F-4. In dark, `body.dark-mode .file-drop-zone` (0,2,1) outranks
  both state rules (0,2,0), so the ground stays `#1c1c1c` and the text reads 5.068 in all three states.
- **Dark gradient.** The dark KPI tile is `linear-gradient(135deg, #1c1c1c, #262626)`. Label 5.068 to 4.500 (I-3).
- **Specificity.** `body.dark-mode .metric-label` and `.file-description` (0,2,1) beat the light (0,2,0)/(0,1,0)
  rules, so no dark pixel moves for them. The new `body.dark-mode .consumable-text` and `.consumable-bar` (0,2,1) beat
  `.consumable-text` (0,1,0) and `.consumable-cell .consumable-bar` (0,2,0, which sets flex only).

## THE RENDERED LEG (item 2)
Harness `progs/g1925-browser.js` (mine, in scratch), headless Chromium 151.0.7922.34 from the project's
`playwright-core`, `file://` only, no network, no port, run inside the jest lock. **What it fakes:** Bootstrap is the
repo's own vendor excerpt `__tests__/helpers/vendor-surface.css` (5.3.0 surface rules), not the CDN file, so the grid
is absent and the tiles stack. No page script runs: the KPI tiles and toner pills are written from the `index.js`
templates with sample values (6 rows: 0, 5, 25, 50, 75 and 100 percent, x 4 fills, one EST tag). The import modal is
`index.html`'s own markup (lines 195-246 found by program), shown in place, not as an overlay. All seven local
stylesheets `index.html` links, in its cascade order. Drag-over and file-chosen classes are set on the second and
third drop zone. A translucent ground is composited up the tree onto the first opaque one.

Screenshots (full page, 1100 px wide), in this folder:
- `B1925_base_light.png`, `B1925_base_dark.png`, `B1925_head_light.png`, `B1925_head_dark.png`;
- the same four bytes as `rendered-base-light.png`, `rendered-base-dark.png`, `rendered-head-light.png`,
  `rendered-head-dark.png` (`cmp` equal; names carry no gate id, for the pull request).
Data: `browser_base.json`, `browser_head.json`; harness pages `harness_<base|head>_<light|dark>.html`.

| element | mode | BASE fg on ground, ratio | head fg on ground, ratio |
|---|---|---|---|
| KPI label x4 | light | `127,140,141` on `255,255,255`, 3.478 | `0,113,159` on `255,255,255`, 5.437 |
| KPI label x4 | dark | `140,140,140` on the gradient (5.068 / 4.500 by stop) | same |
| import description x3 | light | on `248,249,250`, 3.299 | 5.158 |
| import description x3 | dark | `140,140,140` on `38,38,38`, 4.500 | same |
| drop text span: rest / drag-over / file-chosen | light | 3.478 / 3.135 / 3.185 | 5.437 / 4.900 / 4.979 |
| drop text span, all three states | dark | `127,140,141` on `28,28,28`, 4.900 | `140,140,140` on `28,28,28`, 5.068 |
| toner label x24 | light | white on the track `233,236,239`, 1.186, shadow `rgba(0, 0, 0, 0.85) ...` | `33,37,41` on its chip `255,255,255`, 15.426, shadow none, 16 px, inside its bar x24 |
| toner label x24 | dark | white on the same light track, 1.186, shadow | `222,222,222` on `28,28,28`, 12.667, shadow none, inside x24 |
| toner track | dark | `rgb(233, 236, 239)` | `rgb(49, 49, 49)` |
At the head, no text ratio in either mode is below 4.5, and no chip sits outside its bar or carries a shadow (by
program). The live page with real Bootstrap, other viewports and the hosted CSP were not rendered.

## VERIFY (item 3)
- Command: `npm --prefix v0 run verify -- --maxWorkers=2`, Node v24.22.2 and its npm first on PATH, under
  `env -u NODE_OPTIONS -u MIN_TESTS -u MIN_SUITES -u VERIFY_EXPECTED_FILE`, inside the one lock acquisition
  (`nexusai-lock.sh jest b1925-gate`, base `session-tools/locks-laptop-1017`, the builder's base).
- 22:15:51 to 22:39:11, rc 0: `VERDICT: PASS — 6231/6231 tests passed across 394 suites (jest exit 0)`.
  Jest summary: Test Suites 394 passed of 394; Tests 6231 passed of 6231. The pair equals the committed
  `scripts/verify-expected-counts.json` at the head (6231 / 394 = BASE 6216 / 393 plus the new file's 15 cells and 1 suite).
- `EADDRINUSE` 0 in the log; porcelain of `v0` empty after; `lsof` of band 26400-27039: 0 listeners before, after
  the jest steps and after the verify. Load1 6.61 at the chain start and 5.75 at the verify start.
- `git diff --name-only 8858e5d1 081f4221` = exactly the five paths (above).

## CODEQL (item 3)
`pr_codeql_check.sh --repo datasecau/Reporting_Dashboard_Au --checkout <my scratch clone> --base 8858e5d11ec101de0a49a819c2d29f4eadf95c40 --head 081f4221f442bbd7ee68be6475f5f64280d558d5 --lang javascript --work <scratch>/cq/run1 --threads 4`,
run after the lock was released, one CodeQL process, load1 4.90: **rc=0**.
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
```
Equal to the builder's CQ-1 and CQ-2. The lane adds no product JavaScript; the only added JavaScript is the test
file. This is a local approximation, and the hosted CodeQL check on the pull request is the authority.

## GITLEAKS (item 3)
gitleaks 8.30.1. Control first: a planted AKIA-shaped pair in a scratch folder reports 1 finding (rc 1). Then the 252
added lines of `git diff 8858e5d1 081f4221` plus the four commit messages (56 lines): **0 findings** (rc 0). Then
`gitleaks git` over `8858e5d1..081f4221` (4 commits): **0 findings**.

## TEXT
Over the added lines and the four messages (my program, every pattern with a control that fires): B-numbers and seat
ids 0; person names introduced 0 (3 added and 3 removed: the old words of the fixture's one replaced `history` line);
product-owner attribution 0; timer, skip, `new RegExp(`, `new Function(`, `eval(` 0; bidi and zero-width 0 (control
1); non-ASCII 1 added and 1 removed, net 0 (the em dash of the re-flowed consumable comment). The word "card" is
introduced 6 times, all the KPI tile or "card ground", no decision-card id; 0 in messages. Ticket keys introduced:
RD-175, RD-349 only. Landing texts: scanned (below).

## LANDING TEXTS
`pr-title.txt`, `pr-body.md`, `merge-subject.txt`, `merge-body.txt`, `landing.txt` are written for this head and
**held**: `landing.txt` opens with the NO GO hold. After a re-cut of F-1 they need the chip colour, its ratio and the
head sha replaced and a re-gate.
Landing-text scan (my program, controls fire): `pr-title.txt`, `pr-body.md`, `merge-subject.txt`, `merge-body.txt`
have 0 B-numbers or seat ids, 0 person names, 0 decision-card ids, 0 addresses, 0 token shapes. The only non-ASCII
is the robot mark of the pr-body's last line. `landing.txt` is internal and carries the gate id and the branch name
(5 hits) by design.

## FOUND / TESTED / NOT TESTED
**FOUND:** F-1 (Major), F-2 to F-4 (Minor), I-1 to I-7.
**TESTED:** scope and commits; each colour against BRAND.md, tokens.css and the generator; every ratio by the repo's
helper; the new file red-first at BASE and green twice at head; the selectors' other matches; hover, focus, drop-zone
states and the dark gradient in a real engine; screenshots at BASE and head in both modes; the full verify on Node 24;
CodeQL; gitleaks with a control; the text scans.
**NOT TESTED:** the live page (real Bootstrap from the CDN, page scripts, CSP); other viewports; Linux; the e2e
contrast suite; the builder's 72-file run list and 12 plants (the full verify backstops the run list; I re-ran no
plant); Jira (not read); the hosted Build and CodeQL on a merge commit; the Deploy demo run a landing starts.
**HOW:** read the kit (636 lines), the drafter report, the seat's STATUS (156 lines, Corrections 1 to 14), C-258,
C-190 and C-224 at source by line, `docs/BRAND.md` at the head; measured everything above in my own scratch trees.
