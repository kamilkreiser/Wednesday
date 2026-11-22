From Tuesday (the Datasec coordinator seat), Datasec / NexusAI. **You do NOT use the shared inbox `datasec-nexusai@`**: your STATUS file and its last line are the only channel to Tuesday; Tuesday's channel to you is a `2026-11-2[23]_B1931_(ADDENDUM|ANSWER)-<n>_*.md` file in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`. A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED-BY-DRAFTER** = the drafter printed it with the instrument named (each such literal has a claim line in the sidecar `<this kit>.measured`); **RELAYED** = read in another file (re-read it at source before you rely on it); **PREDICTED** = the drafter's arithmetic or expectation, nobody has measured it; **UNMEASURED** = nobody has. The drafter's report is saved beside this kit as `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1931_DRAFTER-REPORT.md` (read-only; read it whole at Step 0; its Q-answers are in Tuesday's STAMP slot). **This is ROUND 2 of lane N-L, a FIX ROUND after the gate's NO GO: the form is round 1's kit B1911 (`2026-11-22_B1911_SEAT-N162_nexusai-lane-nl.md`), which is itself the form of B1771 (`2026-11-20_B1771_SEAT-N161_nexusai-lane-nm-chat-error-text.md`): its lock, chain, worktree-slot, mutation and verify rules, tool set and landing hold are this kit's, with the substitutions named in HOLDS. A fix round NEVER rebases: it adds ONE fast-forward commit `R` on top of the pushed round-1 head.** Facts below were read on Sun 22 Nov 2026 from 22:41 AEDT to the end of drafting (clocks in the report). **PREV (the round-1 head you build on): `081f4221f442bbd7ee68be6475f5f64280d558d5`** on `b1911/nexusai-lane-nl-brand-contrast` at origin (`gh api -X GET .../git/ref/heads/b1911/nexusai-lane-nl-brand-contrast`; its tree `d9dd23ae516364f6109b0db68ed3a51c036a95b4`, parent `8f4b7166`). **BASE: NexusAI main `8858e5d11ec101de0a49a819c2d29f4eadf95c40`** (unmoved since round 1; open pull requests 0; repository `datasecau/Reporting_Dashboard_Au`). No other NexusAI lane is live or queued.

# BRIEF B1931 - SEAT-N163: NEXUSAI LANE N-L ROUND 2 (FIX ROUND AFTER GATE B1925 NO GO): THE TONER CHIP TEXT TAKES A BRAND TOKEN (F-1), THE DARK TONER FILLS SEPARATE FROM THEIR TRACK (F-2), BRAND.md R5 SAYS WHAT IS TRUE IN LIGHT (F-3), CELLS FOR THE DROP ZONE STATES (F-4); ONE FAST-FORWARD COMMIT ON THE PUSHED BRANCH; LOCAL CODEQL; FULL VERIFY PASS; ONE PUSH; NO PR; NOT DEPLOYED

## THE AUTHORITY, THE GATE AND THE ROUND (MEASURED-BY-DRAFTER unless marked)
- **Authority (unchanged from round 1).** The product owner's 2026-11-11 ruling on brand contrast, option (a), recorded as C-258 in the project's `1_Project_Definition/CLARIFICATIONS.md` (`awk NR==2751` prints its heading; entry lines 2751 to 2757). The colours of this lane are Tuesday's defaults as coordinator (LANDING HOLD 23); the ruling names the outcome only.
- **The gate.** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1925_verify/VERDICT.md`: line 1 `GATE B1925: NO GO @ 081f422 on main 8858e5d`; `Blocker 0 | Major 1 | Minor 3 | Info 7`. **NO GO 1 of 2 on class off-guide colour (F-1).** A NO GO after THIS round goes to the product owner as a card (round 2 of 2).
  - **F-1 (Major):** the light chip text `#212529` is on no brand token (0 in `docs/BRAND.md`, `static/css/tokens.css`, `scripts/derive-brand-tokens.js`); the stylesheet's own comments reject it by name (at PREV `index-styles.css:1470` "the token is the point" and `:1483` "not Bootstrap's #212529"; the gate cited them as 1459 and 1472, their BASE lines); cell C1 accepted any six-digit hex.
  - **F-2 (Minor):** the dark track `#313131` swallows the black fill (`#2c3e50` to `#34495e`: 1.184 to 1.400).
  - **F-3 (Minor):** `docs/BRAND.md` R5 says `#00719f` "is never text", untrue in light since RD-251.
  - **F-4 (Minor):** no cell pins the drop zone's drag-over and file-chosen states.
  - Info I-1 to I-7 stand as recorded; none is reopened.
- **The coordinator's decisions for this round** (commission `2026-11-22_B1931_NEXUSAI-NL-ROUND2_DRAFTER_COMMISSION.md`): F-1 by a BRAND TOKEN, never a new colour, default `#333333` if the generator regenerates it and the change is measured; C1 tightened so an off-guide hex fails (red against round 1's `#212529`); F-2 by a TOKEN under the repo's own non-text rule; F-3 a docs line quoting the rulings verbatim; F-4 cells; the rest of round 1 stands; the e2e suite stays untouched.

## WHAT THE DRAFTER FOUND (MEASURED-BY-DRAFTER on the tarball of PREV `081f4221`, extracted to scratch; jest 29.7.0 on Node v24.22.2; ratios by the repo's own `contrastRatio` and a stand-alone sRGB program that agree to three places)
1. **F-1: `#333333` is the token, and the generator takes it.** `#333333` is `--nx-text-strong` (light), 12.635:1 on `#ffffff`. Its light occurrence count is pinned at `scripts/derive-brand-tokens.js:162` (`count: 22`), so the chip's use makes the measured count 23 and `brand-token-conformance.test.js` refuses a pin left at 22 (plant Q1 below: the round-1 line put back reads red there AND in C1). The pin goes to 23 with a call-site comment (the RD-194 / F1-pass-17 shape already in that comment block), and `static/css/tokens.css` is regenerated by the repo's own `node scripts/derive-brand-tokens.js`: **at PREV the generator's `--stdout` is byte-equal to the committed `tokens.css` (control), and after the pin move the regenerated file differs in exactly one line, `tokens.css:33` `x22 measured` to `x23 measured`.** BRAND.md section 8 rule 1 (`docs/BRAND.md:581`): "Use a token. If none fits, the gap is a brand decision". The alternatives the gate listed are recorded in the report (Q-1): `#636c73` `--nx-text-secondary` 5.353 (no pin, no generated file) and `#00719f` 5.437.
2. **F-2: the repo's rule for non-text is BRAND.md R8 (`docs/BRAND.md:744`): kind `graphic` "(a bar, an indicator; WCAG 1.4.11) clears 3:1".** No single dark track clears 3:1 against all four fills (the black fill is darker than every dark ground, the yellow fill lighter than any ground that clears the black): the table, every dark ground token against every fill gradient stop, is in the report. So the fix takes TWO tokens: the dark track becomes **`#262626`** (`--nx-surface-raised` dark), which is the dark value of the light track's OWN token (the light track `#e9ecef` is `--nx-surface-raised` light), and the dark black fill becomes **`#8c8c8c`** (`--nx-text-muted` dark) by a new rule `body.dark-mode .consumable-fill.black` (specificity 0,3,1 over the light 0,2,0). On `#262626`: black `#8c8c8c` 4.500, cyan 6.590 to 7.331, magenta 3.481 to 4.949, yellow 9.284 to 9.895: every stop clears 3:1. Round 1's `#313131` left magenta's first stop at 2.992 as well as black at 1.184; the light track and every light fill are untouched (light fills on the light track are a pre-existing matter: LEFT FOR OTHERS 2).
3. **The toner table's own grounds in dark** (`static/index.html:930` `table table-hover`; `dark-mode.css:344` odd rows `#262626`, hover `#313131`, even `#1c1c1c`): the track is a decorative boundary against the cell ground in every row and in both modes (light `#e9ecef` on white 1.186; dark `#262626` on `#1c1c1c` 1.126 and on an odd row 1.000, where round 1's `#313131` read 1.310 and 1.163), which BRAND.md section 5 records as not a 1.4.11 boundary. The fill against its track is the pair the rule governs, and the chip states the value as text in every row.
4. **F-3: the two sources, read at source.** RD-251's ruling is NOT in `CLARIFICATIONS.md` (`grep -o -i -F 'RD-251'` counts 0; control `RD-349` counts 5); its words are recorded in the repo in the `.tab-button` comment (`static/css/index-styles.css:669`) and `HISTORY.md:7224-7227` records that it was applied as the pair INVERTED (chrome as text) and "Shipped, and explicitly not ratified as his meaning". C-258's question, option and accepted recommendation are quoted in `CLARIFICATIONS.md:2752-2753`. The BRAND.md edit (B1 and B2 in `apply1931.py`) makes R5's negative sentence DARK-only (its three figures 3.45, 3.13 and 2.78 are the dark page, card and raised grounds: `#00719f` on `#121212` 3.446, `#1c1c1c` 3.135, `#262626` 2.784) and adds one paragraph quoting both records verbatim, with the light figures 5.437 on white, 5.158 on `#f8f9fa`, 4.585 on `#e9ecef`. It states no new rule and attributes no colour choice to the product owner (Q-3 of the report is the coordinator's check of this wording).
5. **BRAND.md's count table** (`docs/BRAND.md:175`) holds `text-strong` at 15 and says "If you change a count, change it in both places"; its precedents (RD-333, RD-840) move the table by the same delta as the generator and add a note. So the table goes 15 to 16 and a five-line note is added (B3, B4). Nothing reads that table (BRAND.md says "The counts in this table are hand-maintained and are NOT guarded").
6. **Two guards read `docs/BRAND.md` and were run on the edited file:** `brand-md-accent-count.test.js` (anchored number-words; the edit touches none of its anchors) and `muted-4-16-attribution.test.js` (the figure `4.16` near `text-muted`; the edit writes neither near the other). Both green at the patched tree (run list below).
7. **F-4: the two states, measured.** `index-styles.css:590` `.file-drop-zone.drag-over` `rgba(102, 126, 234, 0.05)` and `:595` `.has-file` `rgba(46, 204, 113, 0.05)`, over `.import-section` `#f8f9fa`: the drop text `#00719f` reads 4.894 and 4.971 on the unrounded composite (the gate's engine, rounding the composite to whole channels, read 4.900 and 4.979); BASE's grey read 3.130 and 3.180. In dark, `body.dark-mode .file-drop-zone` (`dark-mode.css:1188`, 0,2,1) outranks both state rules (0,2,0), so the drop text reads `#8c8c8c` on `#1c1c1c`, 5.068, in all three states. Cells S1, S2, S3 hold these; they are GREEN at PREV (the states already pass since round 1) and S1, S2 are RED at round 1's BASE (measured), so their red proof at PREV is by plant (Q5, Q6, Q7).
8. **Real engine (the drafter's harness `browser1931.js`, headless Chromium from the project's `playwright-core`, local file page, the seven local stylesheets `index.html` links found by program, Bootstrap = the repo's vendor excerpt; not the live page):** Chromium 151.0.7922.34, 8 sheets (the vendor excerpt and the seven `index.html` links), JSONs `br/browser_prev.json` and `br/browser_r0.json` in the drafter's scratch. **PREV, light:** chip `33,37,41` on `255,255,255` 15.426, `inside` 24 of 24, shadow `none`; track `233,236,239`; lowest fill stop on the track: black 7.834, cyan 1.741, magenta 2.579, yellow 1.290; drop span 5.437 at rest, 4.900 on drag-over `241,243,249`, 4.979 on file-chosen `238,247,243`. **PREV, dark:** chip `222,222,222` on `28,28,28` 12.667; track `49,49,49`; black 1.184, cyan 5.664, magenta 2.992, yellow 7.981; drop span `140,140,140` on `28,28,28` 5.068 in all three states. **R0, light:** chip `51,51,51` on `255,255,255` 12.635, inside 24 of 24, shadow `none`; track and every fill reading equal to PREV's; drop spans equal to PREV's. **R0, dark:** chip unchanged 12.667; track `38,38,38`; black fill `140,140,140` 4.500, cyan 6.590, magenta 3.481, yellow 9.284 (every stop of every fill at least 3); drop spans 5.068 in all three states; a hovered row (cell ground `49,49,49`) reads the same fill-on-track figures. Screenshots `br/B1931_<prev|r0>_<light|dark>.png`.

## STATE AT DRAFTING (MEASURED-BY-DRAFTER; re-read every line at Step 1 at YOUR read)
- origin main `8858e5d11ec101de0a49a819c2d29f4eadf95c40`; the branch `b1911/nexusai-lane-nl-brand-contrast` at `081f4221f442bbd7ee68be6475f5f64280d558d5`; `matching-refs/heads/b1931` 0; open pull requests 0; open code-scanning alerts 22 (`backend/server.js` 13, `backend/incidents.js` 2, `backend/jsonStorage.js` 2, `backend/routes/entraProvisioning.js` 2, `backend/services/emailService.js` 2, `tests/uat-run.js` 1): none in a path this round writes.
- Counts at PREV `{"tests": 6231, "suites": 394}` (`_updated 2026-11-22T10:38:26.723Z`); top-level `__tests__/*.test.js` at PREV: 394.
- Blobs at PREV (`git hash-object`, first 12) and sizes: | path | PREV blob | PREV bytes | R0 blob (patched, MEASURED) | R0 bytes |
|---|---|---|---|---|
| `static/css/index-styles.css` | `1d9889946996` | 42608 | `b17eb7bf64e8` | 42750 |
| `static/css/dark-mode.css` | `45fc7bfded9f` | 85781 | `5dec53a1844f` | 86207 |
| `scripts/derive-brand-tokens.js` | `3edf62f5b43c` | 50343 | `3e3b5a1704fa` | 50618 |
| `docs/BRAND.md` | `3fbe89b38446` | 53055 | `022d7cfc110d` | 54591 |
| `static/css/tokens.css` | `a5767fe5e4fd` | 17727 | `f72105abb1ca` | 17727 |
| `__tests__/rd349-rd175-readable-text-on-its-ground.test.js` | `3513d25688f9` | 11393 | `fb47788052a8` | 18118 |
| `scripts/verify-expected-counts.json` | `e24686d168fe` | 496 | (R only: from the `--update-counts` verify; its `_updated` stamp makes the blob unpredictable) | |
- Non-ASCII bytes per file are equal before and after (`index-styles.css` 146, `dark-mode.css` 506, `derive-brand-tokens.js` 242, `BRAND.md` 498, `tokens.css` 441); no CRLF in any; the added text is ASCII (the programs assert it).

## THE DESIGN (Tuesday's defaults; every departure needs your written justification in STATUS)
**One commit `R` on the branch, fast-forward from PREV. Seven paths:** `static/css/index-styles.css`, `static/css/dark-mode.css`, `scripts/derive-brand-tokens.js`, `static/css/tokens.css` (regenerated, never typed), `docs/BRAND.md`, the round-1 test file (rewritten whole from this kit), `scripts/verify-expected-counts.json` (measured by `--update-counts`).
**How one commit carries a measured counts file:** the chain first makes a SCRATCH commit **R0** in the detached tree `new5` (every path of R except the counts file; it is never on a branch and never pushed), runs every jest step and the `--update-counts` verify against R0's committed tree, then makes **R** in `wt` on the branch from the same frozen programs plus the counts file copied from the update tree, proves R's six non-counts blobs equal R0's, and runs the plain verify at R.
**Tuesday's defaults, said so they can be overruled:** (1) the chip text `#333333` `--nx-text-strong` with the pin 22 to 23 and `tokens.css` regenerated; (2) the dark track `#262626` and the dark black fill `#8c8c8c`, both tokens; (3) the BRAND.md wording of B1 to B4 in `apply1931.py`; (4) S1 to S3 as the F-4 cells; (5) round 1's design stands in every other line (`#00719f` greys, the chip shape, `.drop-text` in the dark muted list, the fixture); (6) `tests/e2e/**` untouched. If Tuesday overrules (1) or (2), the change is the constants `CHIP`, `DARK_TRACK`, `DARK_BLACK` at the top of `apply1931.py` and the matching literals of the test file; the seat does nothing about it by itself.

**The frozen program** (`apply1931.py`; run in a tree, argument = the tree's root; prints four `applied` lines; then `node scripts/derive-brand-tokens.js` is run with that tree's `scripts/` (Node 24, first on PATH) and prints `wrote ... tokens.css`; then each stylesheet is checked for balanced braces by your own count):
```python FILE: apply1931.py
#!/usr/bin/env python3
# apply1931.py <tree root>: the frozen edit of lane N-L round 2 (RD-175, RD-349 fixes after gate F-1 to F-3).
# Four files: index-styles.css, dark-mode.css, scripts/derive-brand-tokens.js, docs/BRAND.md. ASCII-only added text.
# Every anchor is asserted to match the stated number of times; each file is rebuilt whole, written beside the
# target and os.replace'd; the non-ASCII bytes of each file are proved equal before and after.
# static/css/tokens.css is NOT edited here: it is regenerated by `node scripts/derive-brand-tokens.js` afterwards.
import os, sys
root = sys.argv[1]
CHIP = '#333333'        # --nx-text-strong (light), the gate's option (a)
DARK_TRACK = '#262626'  # --nx-surface-raised (dark): the dark value of the light track's own token #e9ecef
DARK_BLACK = '#8c8c8c'  # --nx-text-muted (dark), the dark black toner fill

def rebuild(rel, edits):
    p = os.path.join(root, rel)
    raw = open(p, 'rb').read()
    s = raw.decode('utf-8')
    for name, old, new, n in edits:
        c = s.count(old)
        assert c == n, (rel, name, 'anchor count', c, 'expected', n)
        s = s.replace(old, new)
    out = s.encode('utf-8')
    assert [b for b in raw if b > 127] == [b for b in out if b > 127], (rel, 'non-ASCII bytes changed')
    tmp = p + '.tmp1931'
    open(tmp, 'wb').write(out)
    os.replace(tmp, p)
    print('applied', rel, len(raw), '->', len(out))

def lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
def cr(a, b):
    x, y = lum(a), lum(b)
    if x < y: x, y = y, x
    return (x + 0.05) / (y + 0.05)
R1 = '%.3f' % cr(CHIP, '#ffffff')
R2 = '%.3f' % cr(DARK_BLACK, DARK_TRACK)
R3 = '%.2f' % cr('#2c3e50', DARK_TRACK)

rebuild('static/css/index-styles.css', [
 ('L1 chip colour', ' color: #212529; /* 15.426:1 on #ffffff */\n background: white;\n',
  ' color: ' + CHIP + '; /* ' + R1 + ':1 on #ffffff */\n background: white;\n', 1),
 ('L2 consumable comment', '    track AND the four fills, so the label is a small opaque chip and the text-shadow is removed. */\n',
  '    track AND the four fills, so the label is a small opaque chip and the text-shadow is removed. The\n'
  '    chip text is the --nx-text-strong token, not Bootstrap\'s #212529, which no token holds (BRAND.md\n'
  '    section 8, rule 1: use a token). */\n', 1),
])
rebuild('static/css/dark-mode.css', [
 ('K1 dark track and black fill', 'body.dark-mode .consumable-bar {\n    background: #313131;\n}\n',
  'body.dark-mode .consumable-bar {\n    background: ' + DARK_TRACK + ';\n}\n'
  'body.dark-mode .consumable-fill.black {\n    background: ' + DARK_BLACK + ';              /* ' + R2 + ':1 on ' + DARK_TRACK + ' */\n}\n', 1),
 ('K2 dark comment', ' * track #e9ecef does not belong on a dark page, and the label is a chip with a dark ground of its own. */\n',
  ' * track #e9ecef does not belong on a dark page, and the label is a chip with a dark ground of its own.\n'
  ' * RD-175 round 2: the dark track is ' + DARK_TRACK + ', the dark value of the light track\'s own token\n'
  ' * (--nx-surface-raised), and every toner fill clears 3:1 on it (a graphic: BRAND.md R8, WCAG 1.4.11):\n'
  ' * cyan, magenta and yellow as they are, and the black fill, which reads ' + R3 + ':1 there, as\n'
  ' * ' + DARK_BLACK + ' (--nx-text-muted, dark). */\n', 1),
])
rebuild('scripts/derive-brand-tokens.js', [
 ('G1 text-strong pin', "  // same selector is what this sheet's discipline is for.\n  'text-strong':       { value: '#333333', count: 22, role: 'headings' },\n",
  "  // same selector is what this sheet's discipline is for.\n"
  "  // 22 -> 23: RD-175 round 2. The toner percentage chip (`.consumable-text`,\n"
  "  // index-styles.css) takes this token as its text colour, " + R1 + " on #ffffff,\n"
  "  // in place of Bootstrap's #212529, which no token holds (BRAND.md section 8,\n"
  "  // rule 1). Call site, not palette.\n"
  "  'text-strong':       { value: '#333333', count: 23, role: 'headings' },\n", 1),
])
rebuild('docs/BRAND.md', [
 ('B1 R5 never-text is dark', 'And **it is never text**: `#00719f` reads 3.45 on the page ground, 3.13 on the\ncard and 2.78 on the raised ground.',
  'And **it is never text on a DARK ground**: `#00719f` reads 3.45 on the dark page\nground, 3.13 on the dark card and 2.78 on the dark raised ground.', 1),
 ('B2 R5 light text paragraph', '`__tests__/brand-chrome-contrast.test.js` asserts the negative direction as well\nas the positive.\n',
  '`__tests__/brand-chrome-contrast.test.js` asserts the negative direction as well\nas the positive.\n'
  '\n'
  '**On a LIGHT ground it is text (corrected 2026-11-22, RD-175 round 2).** This\n'
  'section used to say "it is never text" with no theme. RD-251 (2026-09-06) put\n'
  '`#00719f` on the inactive dashboard tabs as TEXT on the light ground. The ruling\n'
  'it applied is recorded in the `.tab-button` comment of\n'
  '`static/css/index-styles.css` as *"Move rest and hover onto the brand chrome pair\n'
  '(#00719f + white)"*, and `HISTORY.md` records the as-text application as\n'
  '*"Shipped, and explicitly not ratified as his meaning"*. RD-349 then moved the\n'
  'KPI labels, the import description and the drop text onto it, under\n'
  'the product owner\'s 2026-11-11 ruling (C-258), option (a), on the question\n'
  '*"Brand contrast: apply the same grey-text ruling to three more places (including\n'
  'the dashboard KPI labels), and fix the white toner text on its light track?"*,\n'
  'whose recommendation reads *"Yes to both. Both fail the readable-contrast check;\n'
  'one is unreadable in both modes."* Measured as LIGHT text: 5.44 on white, 5.16\n'
  'on the page ground `#f8f9fa` and 4.58 on the raised ground `#e9ecef`. Every one\n'
  'of these uses has a dark rule of its own, because the sentence above still holds\n'
  'in dark.\n', 1),
 ('B3 table text-strong', '| `--nx-text-strong` | `#333333` | 15 | headings |\n',
  '| `--nx-text-strong` | `#333333` | 16 | headings |\n', 1),
 ('B4 table note', '> counts and every count in this table are byte-unchanged.\n',
  '> counts and every count in this table are byte-unchanged.\n'
  '>\n'
  '> **RD-175 round 2 (2026-11-22) moves `text-strong` by one call site, 22->23 in\n'
  '> `scripts/derive-brand-tokens.js` and 15->16 in this table.** The toner\n'
  '> percentage chip (`.consumable-text`) takes this token as its text colour in\n'
  '> place of Bootstrap\'s `#212529`, which no token holds (section 8, rule 1).\n'
  '> **The palette did not change.**\n', 1),
])
```
**Diff line classes** (the drafter's, `diff` of PREV against the patched tree; `>` added, `<` removed): `index-styles.css` 4 `>` and 2 `<`; `dark-mode.css` 9 `>` and 2 `<`; `derive-brand-tokens.js` 5 `>` and 1 `<`; `BRAND.md` 26 `>` and 3 `<`; `tokens.css` 1 `>` and 1 `<`; `rd349-rd175-readable-text-on-its-ground.test.js` 122 `>` and 2 `<`.

## THE TEST FILE (the round-1 file rewritten WHOLE: 19 cells as explicit `test(` calls; cell ids are the title prefixes; colours MEASURED-BY-DRAFTER in real jest 29.7.0)
Extract it with `awk` (the line after the opening fence to the line before the closing fence), `cmp` to what you extracted, never retype, never change a title (HOLD 38). Fifteen cells are round 1's (titles unchanged except C1, which is tightened); four are new (C5, S1, S2, S3); I1 gains round-2 instrument checks. It reads `static/css/tokens.css` now (C1, C5) as well as the two stylesheets, `static/js/index.js` and `static/index.html`. `grep -c -E '^[[:space:]]+test\(' <file>` prints **19** and `grep -c -E '^test\(' <file>` prints **0**.
| tree | RED (for the property's reason) | GREEN |
|---|---|---|
| PREV `081f4221` with this file copied in (untracked) | **2: C1** (received `#212529`, not in the light token values), **C5** (black `#2c3e50` on `#313131`: false at 3:1) | 17: I1 R1 L1 L2 L3 L4 D1 D2 D3 D4 C2 C3 C4 M1 S1 S2 S3 |
| R0 (the round-2 tree) | 0 | 19 of 19 |
| round 1's BASE `8858e5d1` with this file copied in (the drafter's extra read, not a seat step) | 11: L1 L2 L3 L4 D3 C1 C2 C4 C5 S1 S2 | 8: I1 R1 D1 D2 D4 C3 M1 S3 |
```js FILE: rd349-rd175-readable-text-on-its-ground.test.js
/**
 * @jest-environment node
 *
 * RD-349 + RD-175 - four pieces of dashboard text are read against the ground
 * they are painted on, and each ground is READ FROM THE STYLESHEET, never assumed.
 *
 *   .metric-card .metric-label   KPI labels, created by static/js/index.js, so the
 *                                static page sweep can never see them
 *   .file-description            import modal, on the .import-section ground
 *   .drop-text                   import modal, on the .file-drop-zone ground; its
 *                                text sits in a child span, which the static sweep
 *                                does not measure, so that sweep never listed it
 *   .consumable-text             the toner percentage, created by index.js, white
 *                                on the light track and on four coloured fills
 *
 * WHAT THIS FILE IS. A reader of the two stylesheets. It proves what the rules say
 * and what those rules measure with the repo's own contrast helper. It does NOT
 * prove what a browser paints: the real-engine numbers are the build seat's
 * browser check, and are not in this file.
 *
 * THE TRAP IT GUARDS. The three light greys moved to the brand chrome text colour.
 * #00719f is 5.44:1 on white and 3.13:1 on the dark panel ground #1c1c1c, so a
 * light colour that reaches dark mode through a rule with no dark counterpart
 * fails there. .drop-text had no dark rule at all; D3 and D4 hold that.
 *
 * ROUND 2 (RD-175). Three more properties, each one a review found unguarded:
 *   C1  the chip's colours are BRAND TOKENS read from static/css/tokens.css; a
 *       six-digit hex that is on no token (Bootstrap's #212529) fails.
 *   C5  in dark, every toner fill is visible on the dark track: 3:1, the
 *       repo's rule for a graphic (BRAND.md R8, WCAG 1.4.11). Read from the
 *       fill rules, never assumed.
 *   S1  the drop text clears AA on the drag-over and file-chosen grounds too:
 *   S2  each state's translucent ground composited over .import-section.
 *   S3  in dark the panel ground outranks both state rules, so the drop text
 *       reads on the dark panel ground in every state.
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { parseColor, contrastRatio, composite } = require('./helpers/dom');

const ROOT = path.join(__dirname, '..');
const read = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8');
const LIGHT = read('static/css/index-styles.css');
const DARK = read('static/css/dark-mode.css');

const TOKENS = read('static/css/tokens.css');

const TEXT = '#00719f';
const AA = 4.5;
const GRAPHIC = 3;

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
// a selector that is written again inside a media query (padding only, for .metric-card): the declarations
// of every rule with that exact selector, in source order, so the last one of a property wins
const merged = (css, selector) => {
    const r = rulesFor(css, selector);
    return r.length ? r.join(';') : null;
};
const ratio = (fg, bg) => {
    const a = parseColor(fg);
    const b = parseColor(bg);
    if (!a || !b) return null;
    return contrastRatio(a, b);
};
const HEX6 = /^#[0-9a-f]{6}$/;
const OPAQUE = /^(#[0-9a-f]{6}|white)$/;
// the --nx-* tokens of one block of tokens.css that are written as a hex (aliases are var() and are skipped)
function tokenValues(selector) {
    const out = {};
    for (const d of (one(TOKENS, selector) || '').split(';')) {
        const j = d.indexOf(':');
        if (j < 0) continue;
        const name = d.slice(0, j).trim();
        const value = d.slice(j + 1).trim().toLowerCase();
        if (name.startsWith('--nx-') && HEX6.test(value)) out[name] = value;
    }
    return out;
}
const LIGHT_TOKENS = tokenValues(':root');
const DARK_TOKENS = tokenValues('body.dark-mode');
const asHex = (c) => {
    const p = parseColor(c);
    return p ? '#' + [p.r, p.g, p.b].map((v) => Math.round(v).toString(16).padStart(2, '0')).join('') : null;
};
const stopsOf = (value) => (value || '').match(/#[0-9a-f]{6}/g) || [];
// selector specificity as [ids, classes, types], enough for the compound selectors of these sheets
const specificity = (sel) => {
    const ids = (sel.match(/#[a-z][\w-]*/gi) || []).length;
    const classes = (sel.match(/\.[a-z][\w-]*/gi) || []).length;
    const types = sel.split(/[\s>+~]+/).filter((part) => /^[a-z]/i.test(part)).length;
    return [ids, classes, types];
};
const outranks = (a, b) => {
    for (let i = 0; i < 3; i++) if (a[i] !== b[i]) return a[i] > b[i];
    return false;
};
// a translucent state ground painted over the opaque ground beneath it
const over = (top, beneath) => {
    const t = parseColor(top);
    const b = parseColor(beneath);
    if (!t || !b) return null;
    return composite(t, b);
};

describe('RD-349 + RD-175 - text is read against the ground it is painted on', () => {
    test('I1: the instrument gives the measured numbers on known pairs', () => {
        expect(ratio('#7f8c8d', '#ffffff')).toBeCloseTo(3.48, 2);
        expect(ratio('#7f8c8d', '#f8f9fa')).toBeCloseTo(3.30, 2);
        expect(ratio('#ffffff', '#e9ecef')).toBeCloseTo(1.19, 2);
        expect(ratio(TEXT, '#ffffff')).toBeCloseTo(5.44, 2);
        expect(ratio(TEXT, '#1c1c1c')).toBeCloseTo(3.13, 2);
        expect(ratio('nonsense', '#ffffff')).toBeNull();
        // round 2 instruments: the graphic pairs and the composite of a translucent state ground
        expect(ratio('#2c3e50', '#313131')).toBeCloseTo(1.18, 2);
        expect(ratio('#e91e63', '#313131')).toBeCloseTo(2.99, 2);
        expect(ratio('#333333', '#ffffff')).toBeCloseTo(12.63, 2);
        expect(contrastRatio(parseColor(TEXT), over('rgba(102, 126, 234, 0.05)', '#f8f9fa'))).toBeCloseTo(4.89, 2);
        expect(contrastRatio(parseColor(TEXT), over('rgba(46, 204, 113, 0.05)', '#f8f9fa'))).toBeCloseTo(4.97, 2);
        expect(over('rgba(0, 0, 0, 0.5)', 'nonsense')).toBeNull();
        expect(specificity('body.dark-mode .file-drop-zone')).toEqual([0, 2, 1]);
        expect(specificity('.file-drop-zone.drag-over')).toEqual([0, 2, 0]);
        expect(outranks([0, 2, 1], [0, 2, 0])).toBe(true);
        expect(outranks([0, 2, 0], [0, 2, 0])).toBe(false);
        expect(asHex('white')).toBe('#ffffff');
        expect(LIGHT_TOKENS['--nx-text-strong']).toBe('#333333');
        expect(LIGHT_TOKENS['--nx-surface-card']).toBe('#ffffff');
        expect(DARK_TOKENS['--nx-surface-card']).toBe('#1c1c1c');
        expect(Object.values(LIGHT_TOKENS)).not.toContain('#212529');
    });

    test('R1: the rule reader finds an exact selector, a list member, and fails on a missing or descendant selector', () => {
        const css = '.a { color: #111111; } .b, .c .d { color: #222222; background: #333333; } @media (max-width: 1px) { .e { color: #444444; } }';
        expect(prop(one(css, '.a'), 'color')).toBe('#111111');
        expect(prop(one(css, '.c .d'), 'background')).toBe('#333333');
        expect(prop(one(css, '.b'), 'color')).toBe('#222222');
        expect(prop(one(css, '.e'), 'color')).toBe('#444444');
        expect(one(css, '.d')).toBeNull();
        expect(one(css, '.missing')).toBeNull();
        expect(prop(null, 'color')).toBeNull();
        expect(merged(css, '.e')).toBe(' color: #444444; ');
        expect(merged(css, '.nope')).toBeNull();
    });

    test('L1: the KPI label colour clears AA on the card ground read from .metric-card', () => {
        const rule = one(LIGHT, '.metric-card .metric-label');
        const ground = prop(merged(LIGHT, '.metric-card'), 'background');
        expect(rule).not.toBeNull();
        expect(ground).not.toBeNull();
        expect(prop(rule, 'color')).toBe(TEXT);
        expect(ratio(prop(rule, 'color'), ground)).toBeGreaterThanOrEqual(AA);
    });

    test('L2: the file description colour clears AA on the ground read from .import-section', () => {
        const rule = one(LIGHT, '.file-description');
        const ground = prop(one(LIGHT, '.import-section'), 'background');
        expect(rule).not.toBeNull();
        expect(ground).toBe('#f8f9fa');
        expect(prop(rule, 'color')).toBe(TEXT);
        expect(ratio(prop(rule, 'color'), ground)).toBeGreaterThanOrEqual(AA);
    });

    test('L3: the drop text colour clears AA on the ground read from .file-drop-zone', () => {
        const rule = one(LIGHT, '.drop-text');
        const ground = prop(one(LIGHT, '.file-drop-zone'), 'background');
        expect(rule).not.toBeNull();
        expect(ground).not.toBeNull();
        expect(prop(rule, 'color')).toBe(TEXT);
        expect(ratio(prop(rule, 'color'), ground)).toBeGreaterThanOrEqual(AA);
    });

    test('L4: no declaration in the stylesheet still paints text with the failing grey in these three rules, and the tab strip keeps its colour', () => {
        for (const sel of ['.metric-card .metric-label', '.file-description', '.drop-text']) {
            const body = one(LIGHT, sel);
            expect(body).not.toBeNull();
            expect(prop(body, 'color')).not.toBe('#7f8c8d');
            expect(/var\(--nx-/.test(body)).toBe(false);
        }
        expect(prop(one(LIGHT, '.tab-button'), 'color')).toBe(TEXT);
    });

    test('D1: dark keeps its own KPI label rule, and it clears AA on the last stop of the dark card gradient', () => {
        const rule = one(DARK, 'body.dark-mode .metric-label');
        const card = prop(one(DARK, 'body.dark-mode .metric-card'), 'background');
        const stops = (card || '').match(/#[0-9a-f]{6}/g) || [];
        expect(rule).not.toBeNull();
        expect(stops.length).toBe(2);
        expect(prop(rule, 'color')).toBe('#8c8c8c');
        expect(ratio('#8c8c8c', stops[1])).toBeGreaterThanOrEqual(AA);
    });

    test('D2: dark keeps its file description rule on the raised ground', () => {
        const rule = one(DARK, 'body.dark-mode .file-description');
        const ground = prop(one(DARK, 'body.dark-mode .import-section'), 'background-color');
        expect(rule).not.toBeNull();
        expect(prop(rule, 'color')).toBe('#8c8c8c');
        expect(ground).toBe('#262626');
        expect(ratio('#8c8c8c', ground)).toBeGreaterThanOrEqual(AA);
    });

    test('D3: the drop text has a dark rule on a recorded token colour that clears AA on the dark panel ground', () => {
        const rule = one(DARK, 'body.dark-mode .drop-text');
        const ground = prop(one(DARK, 'body.dark-mode .file-drop-zone'), 'background-color');
        expect(rule).not.toBeNull();
        expect(ground).toBe('#1c1c1c');
        expect(prop(rule, 'color')).toBe('#8c8c8c');
        expect(ratio(prop(rule, 'color'), ground)).toBeGreaterThanOrEqual(AA);
    });

    test('D4: no light text colour reaches dark mode without a dark rule that clears AA on its dark ground', () => {
        const cases = [
            ['.metric-card .metric-label', 'body.dark-mode .metric-label', '#262626'],
            ['.file-description', 'body.dark-mode .file-description', '#262626'],
            ['.drop-text', 'body.dark-mode .drop-text', '#1c1c1c'],
        ];
        for (const [lightSel, darkSel, ground] of cases) {
            const darkRule = one(DARK, darkSel);
            const colour = darkRule ? prop(darkRule, 'color') : prop(one(LIGHT, lightSel), 'color');
            expect(colour).not.toBeNull();
            expect(ratio(colour, ground)).toBeGreaterThanOrEqual(AA);
        }
    });

    test('C1: the toner percentage carries its own opaque ground, both of its colours are brand tokens, and no text-shadow stands in for contrast', () => {
        const rule = one(LIGHT, '.consumable-text');
        expect(rule).not.toBeNull();
        const colour = prop(rule, 'color');
        const ground = prop(rule, 'background');
        expect(HEX6.test(colour || '')).toBe(true);
        expect(OPAQUE.test(ground || '')).toBe(true);
        // a hex that no light token holds is off-guide (BRAND.md section 8, rule 1), however well it measures
        expect(Object.values(LIGHT_TOKENS)).toContain(colour);
        expect(colour).toBe(LIGHT_TOKENS['--nx-text-strong']);
        expect(asHex(ground)).toBe(LIGHT_TOKENS['--nx-surface-card']);
        expect(ratio(colour, ground)).toBeGreaterThanOrEqual(AA);
        expect(prop(rule, 'text-shadow')).toBeNull();
    });

    test('C2: the chip fits inside the 20px toner bar', () => {
        const rule = one(LIGHT, '.consumable-text');
        const bar = prop(one(LIGHT, '.consumable-bar'), 'height');
        expect(rule).not.toBeNull();
        expect(bar).toBe('20px');
        const size = prop(rule, 'font-size');
        const line = prop(rule, 'line-height');
        expect(size).toBe('0.8rem');
        expect(line).not.toBeNull();
        expect(parseFloat(size) * 16 * parseFloat(line)).toBeLessThanOrEqual(parseFloat(bar));
        expect((prop(rule, 'padding') || '').split(/\s+/)[0]).toBe('0');
    });

    test('C3: the label stays a centred sibling that cannot clip (the RD-85 geometry is kept)', () => {
        const rule = one(LIGHT, '.consumable-text');
        expect(rule).not.toBeNull();
        expect(prop(rule, 'position')).toBe('absolute');
        expect(prop(rule, 'top')).toBe('50%');
        expect(prop(rule, 'left')).toBe('50%');
        expect(prop(rule, 'transform')).toBe('translate(-50%, -50%)');
        expect(prop(rule, 'white-space')).toBe('nowrap');
        expect(prop(rule, 'pointer-events')).toBe('none');
    });

    test('C4: dark gives the toner track and its label a dark counterpart that clears AA', () => {
        const bar = one(DARK, 'body.dark-mode .consumable-bar');
        const text = one(DARK, 'body.dark-mode .consumable-text');
        expect(bar).not.toBeNull();
        expect(text).not.toBeNull();
        expect(HEX6.test(prop(bar, 'background') || '')).toBe(true);
        expect(prop(bar, 'background')).not.toBe('#e9ecef');
        expect(ratio(prop(text, 'color'), prop(text, 'background'))).toBeGreaterThanOrEqual(AA);
    });

    test('C5: in dark, every toner fill is visible on the dark track (3:1, a graphic: BRAND.md R8)', () => {
        const track = prop(one(DARK, 'body.dark-mode .consumable-bar'), 'background');
        expect(HEX6.test(track || '')).toBe(true);
        expect(Object.values(DARK_TOKENS)).toContain(track);
        for (const c of ['black', 'cyan', 'magenta', 'yellow']) {
            const light = prop(one(LIGHT, '.consumable-fill.' + c), 'background');
            const dark = one(DARK, 'body.dark-mode .consumable-fill.' + c);
            const stops = stopsOf(dark ? prop(dark, 'background') : light);
            expect([c, stops.length > 0]).toEqual([c, true]);
            for (const s of stops) expect([c, s, ratio(s, track) >= GRAPHIC]).toEqual([c, s, true]);
        }
    });

    test('S1: the drop text clears AA on the drag-over ground (its translucent ground over .import-section)', () => {
        const text = prop(one(LIGHT, '.drop-text'), 'color');
        const state = prop(one(LIGHT, '.file-drop-zone.drag-over'), 'background');
        const beneath = prop(one(LIGHT, '.import-section'), 'background');
        expect(state).not.toBeNull();
        expect(beneath).toBe('#f8f9fa');
        const ground = over(state, beneath);
        expect(ground).not.toBeNull();
        expect(contrastRatio(parseColor(text), ground)).toBeGreaterThanOrEqual(AA);
    });

    test('S2: the drop text clears AA on the file-chosen ground (its translucent ground over .import-section)', () => {
        const text = prop(one(LIGHT, '.drop-text'), 'color');
        const state = prop(one(LIGHT, '.file-drop-zone.has-file'), 'background');
        const beneath = prop(one(LIGHT, '.import-section'), 'background');
        expect(state).not.toBeNull();
        expect(beneath).toBe('#f8f9fa');
        const ground = over(state, beneath);
        expect(ground).not.toBeNull();
        expect(contrastRatio(parseColor(text), ground)).toBeGreaterThanOrEqual(AA);
    });

    test('S3: in dark the panel ground outranks both state rules, so the drop text reads on it in every state', () => {
        const panelSel = 'body.dark-mode .file-drop-zone';
        const panel = prop(one(DARK, panelSel), 'background-color');
        expect(panel).toBe('#1c1c1c');
        for (const stateSel of ['.file-drop-zone.drag-over', '.file-drop-zone.has-file']) {
            expect(one(LIGHT, stateSel)).not.toBeNull();
            expect([stateSel, outranks(specificity(panelSel), specificity(stateSel))]).toEqual([stateSel, true]);
            expect(rulesFor(DARK, 'body.dark-mode ' + stateSel)).toEqual([]);
        }
        const dark = one(DARK, 'body.dark-mode .drop-text');
        const colour = dark ? prop(dark, 'color') : prop(one(LIGHT, '.drop-text'), 'color');
        expect(ratio(colour, panel)).toBeGreaterThanOrEqual(AA);
    });

    test('M1: the rules above style real nodes (the markup the page writes and ships)', () => {
        const js = read('static/js/index.js');
        const html = read('static/index.html');
        const count = (s, re) => (s.match(re) || []).length;
        expect(count(js, /class="metric-label"/g)).toBe(7);
        expect(count(js, /class="consumable-text"/g)).toBe(1);
        expect(count(html, /class="file-description"/g)).toBe(3);
        expect(count(html, /class="drop-text"/g)).toBe(3);
    });
});
```

## THE CODE-SCANNING RULE (MEASURED-BY-DRAFTER)
The round adds stylesheet and documentation text, two comment lines and a number in the token generator (no new code path), and test code. The test file adds regular-expression LITERALS only (the round-1 comment stripper, `/#[0-9a-f]{6}/g`, `/#[a-z][\w-]*/gi`, `/\.[a-z][\w-]*/gi`, `/[\s>+~]+/`, `/^[a-z]/i`); `new RegExp(` 0, `eval(` 0, `new Function(` 0, no request-chosen key, no data flow from input. The 22 open alerts are in no file this round writes. STEP CQ still runs (required).

## THE CENSUS (frame stated)
**Frame:** top-level `__tests__/*.test.js` at PREV (394 files); the run list is every one whose text names a reader of the round-2 frame (`runlist1931.py` below: round 1's pattern plus `tokens.css`, `derive-brand-tokens`, `BRAND.md`, `'BRAND`, `'docs'`). **78 files at PREV** (round 1's program over the same tree prints 73: the new terms add the readers of the generator and of BRAND.md). Control: the list contains `brand-token-conformance.test.js`, `brand-md-accent-count.test.js`, `muted-4-16-attribution.test.js`, `index-dark-surfaces.test.js` and the lane's own file. **A reader outside the run list is possible** (a path built at run time); the full verify of the chain is the net, and its red is a STOP naming the file.
**Measured at the drafter's run** (scratch trees with NO `.git`, so the five files that read tracked files or shas through git read red identically in both trees: environment, expected GREEN in your clone): the run list (78 files) ran ONCE at PREV (`head`, 22:56 to 23:05, load1 2.6 to 7) and ONCE at the patched tree (`p1`, 23:05 to 23:14): **PREV 1455 cells, 1426 passed, 29 failed; patched 1459 cells, 1430 passed, 29 failed.** The 29 are the SAME cells in the SAME five files at both trees, all environment (they read tracked files or resolve shas through git, which a tarball copy lacks): `image-content-exposure` 17, `rd503-shipped-docs-c51-leftovers` 7, `rd418-dockerignore-round3` 3, `handover-gate-table` 1 ("every SHA in the table resolves to a real commit"), `rd719-chartjs-vendored` 1 (round 1 measured 28 in four of these files; `handover-gate-table` is in the frame now through `'docs'`). **Per-file cell counts are equal at both trees in all 77 other files; the lane's file goes 15 to 19.** The BRAND.md readers, the token guards and the new file were re-run at the final text `p2` (the dry-run section). Expected GREEN in your clone: every file, the five included (a red of any of them in your clone is a STOP).
```python FILE: runlist1931.py
#!/usr/bin/env python3
# runlist1931.py <tree root>: the top-level __tests__/*.test.js files whose text names a reader of the round-2 frame
# (the two stylesheets, index.html, the css helpers, tokens.css, the token generator, docs/BRAND.md).
import os, re, sys
root = sys.argv[1]
td = os.path.join(root, '__tests__')
pat = re.compile(r"index-styles\.css|dark-mode\.css|static/css|'css'|\"css\"|index\.html|renderPage\(|helpers/dom|helpers/css-colors|helpers/dark-corpus|css-colors|tokens\.css|derive-brand-tokens|BRAND\.md|'BRAND|'docs'")
hits = []
total = 0
for n in sorted(os.listdir(td)):
    p = os.path.join(td, n)
    if n.endswith('.test.js') and os.path.isfile(p):
        total += 1
        if pat.search(open(p, encoding='utf8', errors='replace').read()):
            hits.append(n)
print('frame: top-level __tests__/*.test.js; files', total, 'run-list', len(hits))
for h in hits: print(h)
```

## SCOPE AND YOUR FILES
```OWNS-B1931
+ static/css/index-styles.css                                   (R: the chip colour line and two comment lines)
+ static/css/dark-mode.css                                      (R: the dark track value, one new rule, the block comment)
+ scripts/derive-brand-tokens.js                                (R: the text-strong pin 22 -> 23 and its four comment lines)
+ static/css/tokens.css                                         (R: regenerated by the generator, one line)
+ docs/BRAND.md                                                 (R: R5 dark-only sentence, one paragraph, the table cell, one note)
+ __tests__/rd349-rd175-readable-text-on-its-ground.test.js     (R: rewritten whole from this kit)
+ scripts/verify-expected-counts.json                           (R: from the --update-counts verify)
```
Branch `b1911/nexusai-lane-nl-brand-contrast` (the existing branch: you add ONE commit R whose parent is PREV). Scratch commit R0 only in the detached tree `new5`. **Never:** a second commit on the branch, a rebase, amend, reset or force-push of any kind, any `backend/**`, `static/js/**` or `static/*.html` file, any other `static/css/**` file, any other `__tests__/**` or `tests/**` path (in particular `tests/e2e/**` and `__tests__/fixtures/**`), `__tests__/helpers/**`, `scripts/**` other than the two named, `.github/**`, `Dockerfile`, `package*.json`, `HISTORY.md`, `BACKLOG.md`, `docs/**` other than `docs/BRAND.md`, Jira, `1_Project_Definition/CLARIFICATIONS.md`, another branch, main, a tag, a PR.

## LEFT FOR OTHERS (the drafter's choice, said so Tuesday can overrule it)
(1) Round 1's LEFT FOR OTHERS 1 to 5 stand (the e2e allow-list entry and stale light baselines, `.metric-card .text-muted`, `.metric-value`, the Roles UI chain, the records moves). (2) **The LIGHT toner fills on the light track `#e9ecef` read below 3:1 at BASE and are unchanged by both rounds:** cyan 1.741 to 1.937, yellow 1.290 to 1.375, magenta 2.579 to 3.666 (black 7.834 to 9.262). Repainting the toner identity colours or the light track is a palette matter outside the gate's findings: a candidate ticket. (3) BRAND.md's count table and the generator's pins still count different populations (RD-235): this round moves both by one and closes nothing else.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY <one question>`, no other step; each value with a control that can fail; items 1 to 3 before `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1931/` is created)
1. `/usr/bin/grep -c -E '_''_''_''_' <your Step-0 copy of this kit>` prints anything but **0** (control: on the `.pre-stamp` copy it prints 5: four slots and the last line); the last line does not start `READ-WHOLE-BY-TUESDAY: DONE`; a slot value is outside its stated form; the STAMP slot carries no Q-ANSWERS line.
2. Your seat name is not `Datasec/NexusAI-N163` (`tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'`; control: -t on another pane prints that pane's name), or `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI`, or a live pane `Datasec/NexusAI-*` other than yours holds a kit that writes a path of OWNS-B1931, or any `b1931/*` branch exists at origin.
3. `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-22_B1931_STATUS.md`, any `.tools/b1931*` or any `b1931-nodot` already exists (name the path; run the check under bash with a control: `.tools/b1911` reads yes).
4. **Nobody is live on NexusAI code.** (a) every NexusAI STATUS file of 20 to 22 Nov in the project's `Briefs/` except your own ends in `READY`, `HANDOVER` or `STOPPED:` or is a records seat's (a program over `2026-11-*_B*_STATUS.md`; print the count and each last line's first word; at drafting 6 files, all `READY`); no live pane `Datasec/NexusAI-*` but yours and a records seat's. (b) **the re-measure rule:** origin main must still be `8858e5d11ec101de0a49a819c2d29f4eadf95c40` (main moved = STOP: this round makes no merge) and `refs/heads/b1911/nexusai-lane-nl-brand-contrast` at origin must be exactly PREV `081f4221f442bbd7ee68be6475f5f64280d558d5` (control: `refs/heads/main` prints a sha); any other value is a STOP with both shas. Make these reads with YOUR clone's configured `core.sshCommand`.
5. At PREV, **any anchor of `apply1931.py` is not found the stated number of times** (the program asserts it and prints which), or a PREV blob is not the one in STATE AT DRAFTING, or the generator's `--stdout` at PREV is not byte-equal to PREV's `tokens.css` (`cmp`; the control that makes the regenerated diff meaningful), or the counts pair at PREV is not 6231 / 394.
6. `gh api user` login does not contain "datasec" case-insensitively (count 1, never quote it) under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`; or a token or key was printed by any tool (say "a value was shown" and STOP).
7. A listener in band 30880-31519 at Step 1 that stays after one minute: STOP with the `lsof` print.

## HOLDS (the whole run; **B1771's holds 1 to 42 stand as B1911 restated them** (read at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1771_SEAT-N161_nexusai-lane-nm-chat-error-text.md` lines 568 to 589, with `b1771` read as `b1931`, `B1771` as `B1931`, `N161` as `N163`, `OWNS-B1771` as `OWNS-B1931`, the branch as `b1911/nexusai-lane-nl-brand-contrast`, the status file as `2026-11-22_B1931_STATUS.md`, slot 17, the band 30880-31519, B1771's trees as this kit's table below); **round 1's holds 23 and 43 to 47 stand** (B1911 kit, its HOLDS section, with `b1911` read as `b1931` wherever it names YOUR tools or trees, and as `b1911` wherever it names the branch); **B1771's holds 12, 26, 27, 29, 31, 34, 37(a) (the `kept.py` fixture is THIS round's shape: 19 cells over 1 file, 2 red and 17 green), 41 and 42 are replaced as stated below; HOLD 30's closed commit list is R0 (scratch, `new5` only) and R; the number scheme is kept)**
12. **(Tools, replaced.)** Every `.tools/b1*/**` and `b1*-nodot/**` but your own is read-only; you READ `.tools/b1911/` (round 1's complete set; its STATUS ends `READY B1911`) only to copy tools out, by B1771 HOLD 25's method, old names to scrub: B1771's list plus `b1911, B1911, N162, old11, probe16, new30, mut11, v25, chk27, chk40`.
20. **(No merge in this round.)** Main must not move: a move at any `mainmove` step is a STOP (HOLD 37(b)'s merge path does not apply), because the round is one fast-forward commit and the landing PR merges by MERGE COMMIT pinned to the head.
23. **LANDING HOLD: this branch carries Tuesday's defaults** (round 1's and THE DESIGN's six). Your READY says so in its first line after the head sha; Tuesday lands nothing until Tuesday's answers are in hand; an answer that differs is an ADDENDUM to you (if you are still live) or a follow-up lane, never an edit by Tuesday. **Landing rule (quoted with its source):** every merge to NexusAI main goes through a pull request that adds no new high-or-higher CodeQL alert and the SAME commit lands: "Never squash, never rebase" (`1_Project_Definition/CLARIFICATIONS.md`, entry C-190, `awk NR==2062,2067`); round 1's kit HOLD 2: "Tuesday gates, opens the PR and lands it by MERGE COMMIT pinned to the head". **Deploy rule:** nothing is deployed; the demo deploy hold of C-224 stands, and a landing starts a Deploy-demo workflow run that must read `skipped`; this round touches no workflow, variable, secret or environment.
48. **(One commit, no rewrite.)** R is made ONCE, in `wt`, with the repo's own configured identity (never `git -c user.*`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*`), and `git rev-parse R^` must print PREV. R0 is made ONCE in `new5` the same way and is never pushed, never given a branch, never referenced by R. If R is wrong, STOP with `CODED-UNPROVEN`; never amend, reset or re-make it.
49. **(The generated file is never typed.)** `static/css/tokens.css` changes only by running `node <tree>/scripts/derive-brand-tokens.js` (Node 24 first on PATH) after `apply1931.py`; its `diff` against PREV's file must be exactly line 33 (`x22 measured` to `x23 measured`), else STOP.
50. **(The documentation edit is frozen.)** `docs/BRAND.md` changes only by `apply1931.py`. The paragraph quotes two records verbatim and attributes no colour choice to the product owner; you never reword it. A reader of BRAND.md that turns red (the two named in finding 6, or any other) is a STOP naming the cell, never an edit.
51. **(The owner-attribution scan, this round's one exception.)** The scan `product owner|owner's ruling|ruled by|decided by` (case-insensitive) over added lines reads **exactly 1** hit, the `docs/BRAND.md` line that begins `the product owner's 2026-11-11 ruling (C-258)` (a verbatim citation of the record, the form BRAND.md already uses for C-241), and **0** in every other added line and in the commit message; control: a planted `decided by` fires.

## SETUP
**Step 0.** `date`. Copy this kit to `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-22_B1931_SEAT-N163_nexusai-lane-nl-round2.md`, `cmp`, sha256, line count; REFUSE 1 to 4(a). Make `.tools/b1931/` with `logs/, raw/, _quarantine/, locks/, patches/, _test/, cq/, frozen/`. Read whole, read-only, and print line count and sha256 prefix into STATUS: the drafter report; the gate's `VERDICT.md` (path above); round 1's STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-22_B1911_STATUS.md` (**its `## Corrections` first: items 1 to 14 are prevented by name in HOLDS 43 to 47 and below**); round 1's kit lines 433 to 491 (HOLDS, SETUP, CHAIN) and 559 to 560 (the mutation rules); B1771's kit lines 568 to 589 and 621 to 649; `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/codeql/README.md` and `GATE_STEP.md`. **`CLARIFICATIONS.md` is about 874 KB: never read it whole; print `awk NR==2751`, `awk NR==2752` and `awk NR==2753` only.** Write STATUS with first line `B1931 STATUS (placeholder, Step 0 running)` and your absolute AEDT clocks. Never print a range of more than 40 lines of any script.
**Step 1.** `date`; Node 24 first on PATH (`export PATH='/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin':"$PATH"`; `node -v` prints `v24.22.2`; CI uses Node 24; round 1's seat ran Node 26, a difference this round removes); export the lock base (`export NEXUSAI_LOCK_BASE='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017'`), `ls -d` it. ONE `git clone --no-hardlinks '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/2_Project_Files' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1931/clone'` (only the source of the clone; **never fetch in the project checkout**); origin `git@github.com:datasecau/Reporting_Dashboard_Au.git`; repo-local `core.sshCommand` to `ssh -i '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes` (value never printed); identity copied by a READ of `.tools/b1911/clone`'s configured identity (lengths only); `git fetch origin '+refs/heads/main:refs/remotes/origin/main' '+refs/heads/b1911/nexusai-lane-nl-brand-contrast:refs/remotes/origin/b1911/nexusai-lane-nl-brand-contrast'`. REFUSE 4(b), 5, 7. Print PREV sha40, its tree (expected `d9dd23ae516364f6109b0db68ed3a51c036a95b4`), its parent (`8f4b7166...`), the counts pair. `git -C <clone> checkout --detach <PREV>` BEFORE `npm ci --no-audit --no-fund --prefix <clone>` (never a cd); `node -e "require('<clone>/node_modules/sqlite3')"` rc 0; `git -C <clone> branch b1911/nexusai-lane-nl-brand-contrast <PREV>` (a LOCAL branch at PREV, upstream origin's). REFUSE 6. The `package-lock.json` blob at PREV should equal `2d7dbece2ecd` (print yours).
**Step 1b (census, no server, no lock):** (i) **the anchors** by `apply1931.py` itself on a scratch copy of PREV (`git -C <clone> archive <PREV> | tar -x -C <scratch>`; every anchor asserted; four `applied` lines), then the generator in that copy and the one-line `tokens.css` diff (HOLD 49), then `git hash-object` of the six patched files against the R0 column of STATE AT DRAFTING; and by `grep -n -F` at PREV of each single-line anchor with the drafter's line beside it: ` color: #212529; /* 15.426:1 on #ffffff */` at `index-styles.css:304`, `body.dark-mode .consumable-bar {` at `dark-mode.css:1987`, the `text-strong` pin at `derive-brand-tokens.js:162`, `And **it is never text**` at `BRAND.md:302`, the table row at `BRAND.md:175`, `x22 measured — headings` at `tokens.css:33`; each with a control that fires (a planted copy in a scratch file of the same frame is found). (ii) **the code-scanning rule, re-measured** (22 expected; print the count and the files; control: `backend/server.js` is in it; 0 in any path of OWNS-B1931). (iii) **the run list** by `runlist1931.py` over the clone at PREV (78 expected; print the count and the files; a difference is explained by NAMING the files). (iv) the heads census of round 1 is not repeated: print `gh api -X GET compare/main...b1911/nexusai-lane-nl-brand-contrast` (`ahead_by` 4, `behind_by` 0 expected) and `matching-refs/heads/b1931` (0).
**Trees** (prefix `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/`; worktrees of YOUR clone; `node_modules` a symlink to the clone's, disclosed). Every jest tree is slot 17 by the project's rule (sha256 of the real path, first 4 bytes, mod 19; the drafter's computation, with the control `b1911-nodot/old11` = 17 as round 1's STATUS printed): print `slot.py` for each before you make it; a tree that is not 17 is a STOP (round 1's Corrections 1 is prevented by name).
| tree | how | use |
|---|---|---|
| `.tools/b1931/wt` | `worktree add` on `b1911/nexusai-lane-nl-brand-contrast` (at PREV) | commit R only (no jest) |
| `b1931-nodot/prev10` | `--detach` at PREV | the browser harness and the run list at PREV |
| `b1931-nodot/probe7` | `--detach` at PREV, plus the new test file COPIED in (untracked) | red-first at PREV |
| `b1931-nodot/new5` | `--detach` at PREV, then `apply1931.py`, the generator, the test file, then commit R0 (detached) | the run list, the new file twice and the browser harness at R0 |
| `b1931-nodot/mut9` | `--detach` at R0 | mutation plants (reverted by blob) |
| `b1931-nodot/v30` | `--detach` at R0 | the `--update-counts` verify |
| `b1931-nodot/chk38` | `--detach` at R | the plain verify that must PASS |
**Tools:** READ each, then copy by HOLD 12 from `.tools/b1911/` (the newest complete set: `lib.sh chain.sh chain.list jestwrap.sh loadprint.sh judge.py kept.py plant.py mkplants.py matrix.py cnt.py commit.sh static.py prepush.py namescan.py s_readers.sh s2_red.sh s_tstep.sh s4_new.sh s7_mut.sh s_kstep.sh s_mainmove.sh s_verify.sh s6m_verify.sh s1_browser.sh s_browser_head.sh browsercheck.py mk_trees.sh slot.py cq/runcq.sh`, whichever of these exist there: print the list you found); `kept.py` (2 red, 17 green), `mkplants.py` (this kit's MUTATIONS table), `s_tstep.sh` (becomes `s_r0step.sh`: R0 in `new5`), `s_kstep.sh` (becomes `s_rstep.sh`: R in `wt`), `static.py` and `prepush.py` (seven paths, HOLD 51) are rewritten for this round. The frozen programs (`apply1931.py`, the test file, `runlist1931.py`, `browser1931.js`, `plants1931.py`) go to `.tools/b1931/frozen/` by `awk` from your kit copy, each `cmp`ed to a second extraction. Create `msg-R0.txt` and `msg-R.txt` before the lock.

## PRIOR WORK (git and gh only; MEASURED-BY-DRAFTER, re-read)
- **Round 1 of this lane is the prior work:** kit B1911, STATUS `READY B1911: 081f4221...`, gate B1925 NO GO (above). Nothing else touches these paths since: `gh api -X GET compare/main...b1911/nexusai-lane-nl-brand-contrast` reads ahead 4, behind 0; main `8858e5d1` unmoved; 0 open pull requests. No other lane has written `docs/BRAND.md`, `scripts/derive-brand-tokens.js` or `static/css/tokens.css` since round 1's BASE (print `git --no-optional-locks log --oneline -5 origin/main -- <path>` for each into STATUS before R0).
- **Keep what works:** every cell of round 1 except C1's loosened check; RD-251's tab colours (L4); RD-85's geometry (C3); the dark rules of `.metric-label`, `.file-description`, `.drop-text` (D1 to D4); the fixture (commit F). **A READY without a PRIOR WORK section is returned.**

## THE COMMITS
- **R0** (scratch, in `new5` detached at PREV, inside the chain at step 3 by `s_r0step.sh`): `apply1931.py`, the generator, the test file extracted from this kit, `git add` of the six paths, commit with `msg-R0.txt` (subject `scratch: lane N-L round 2 tree for measurement, never pushed`). Static R0 as below. Print R0's sha40 and tree.
- **R** (in `wt` on the branch at PREV, inside the chain at step 9 by `s_rstep.sh`): the same frozen programs and the same extracted test file, then the counts file copied from `v30` (`cmp`), `git add` of the seven paths, commit with `msg-R.txt`. Subject `RD-175, RD-349: the toner chip text takes a brand token, the dark fills clear 3:1 on their track, BRAND.md says where #00719f is text`. The body says in plain words: the chip text is `--nx-text-strong` (the pin and `tokens.css` move by one call site), the dark track is `#262626` and the dark black fill `#8c8c8c` (both tokens), BRAND.md R5's negative sentence is now dark-only with the two records quoted, four cells are added and C1 is tightened; and that the colours are the coordinator's defaults. None says the product owner decided anything. **Then:** `git rev-parse R^` = PREV; `git diff --name-only PREV R` = exactly the seven paths of OWNS-B1931; the six non-counts blobs of R equal R0's (`git rev-parse R:<path>` against `R0:<path>`); `git log --format='%h %ae | %ce' -1 R` equal to the configured email.
- **Static before each commit:** `git diff --name-status` = exactly that commit's paths; no path outside OWNS-B1931; the hunks of each file equal the drafter's diff line classes above (by program); non-ASCII and bidi/zero-width characters INTRODUCED 0 (added minus removed; control: a planted U+202E counts 1); name scan 0 with controls (underscore-aware, names from `scanlib1114.py:20` printed with `sed -n 20p`; the added BRAND.md text quotes "his meaning", a pronoun, which the scan must not count: print it as a known non-name); B-number scan over the message and added lines (`B1[5-9][0-9][0-9]|N1[4-9][0-9]|Datasec/NexusAI-`, case-insensitive) 0 (controls: planted `B1931` and `b1931/x` fire); card/decision-id scan (`decision[ _-]queue|REC-REG`) 0 over everything and the word `card` 0 over the message (introduced added-line hits printed: the CSS class `.metric-card`, `card ground` in round-1 text and the BRAND.md word "card" in "the dark card" are expected, as round 1's Corrections 5 disclosed); owner attribution per HOLD 51; gitleaks over `git diff PREV` no leaks (control: a planted AKIA-shaped scratch string reports at least 1); no timer token or skip marker in added lines (control: planted `setTimeout` and `.only(` fire); no `new RegExp(` in an added line (control fires).

## STEP CQ: THE LOCAL CODEQL COMPARISON (REQUIRED; a landing blocker if it reads rc 1; seat-local lock, no jest, one CodeQL process at a time; the tool is Tuesday's B1731 tool and is read-only)
As B1771's STEP CQ (its lines 621 to 628, with `b1771` read as `b1931`): **CQ-1 at R0 and CQ-2 at R**, both after the chain and before the push, `--repo datasecau/Reporting_Dashboard_Au --checkout '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1931/clone' --base 8858e5d11ec101de0a49a819c2d29f4eadf95c40 --head <R0 or R sha40> --lang javascript --threads 4`, one fresh `--work` per run under `.tools/b1931/cq/`, a seat-local lock file `.tools/b1931/locks/codeql`, usage read from the tool's header (`sed -n 1,30p`), never called bare; R0 must be in the clone's object store (it is: `new5` is a worktree of the clone). Paste both verdict tables and rcs under `## CodeQL`. rc 0 pass; **rc 1 a MAJOR finding and a landing blocker: STOP with the table (a reshape would change a frozen line); rc 2 is never a pass.** Said plainly: a local approximation; the hosted check on the landing head is the authority. **Round 1's CQ-1 and CQ-2 read rc 0 with head 29, base 29, KEPT 0, NEW 0 at the same base; this round adds no product JavaScript, so rc 0 with no kept result is PREDICTED, not measured (the drafter did not run the tool).**

## THE CHAIN (ONE waiter: `nexusai-lock.sh jest b1931-chain bash '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1931/chain.sh'`, list `.tools/b1931/chain.list`; the rules of B1771's CHAIN heading (its line 630) hold: a step's label goes to `chain.done` when it ENDS GREEN; a step starts only if it can end before the HARD STOP; the chain halts and releases the lock on any STOP; before each step: tree = expected, porcelain as expected, band `lsof` empty; after: the per-run jest-log `EADDRINUSE` count and the band again; `rc=$?` on its own line)
Per run: `env -u NODE_OPTIONS '<T>/node_modules/.bin/jest' <ABSOLUTE paths...> --runTestsByPath --config '<T>/jest.config.js' --rootDir '<T>' --maxWorkers=2 --json --outputFile=<raw json> --cacheDirectory='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1931/jcache'`, Node 24 first on PATH. **Cell counts and colours come from the JSON (`assertionResults`, by title prefix), never from `test(` lines; HOLD 33 judges every JSON; no `-t` and no `--filter`: every run is by ABSOLUTE path with `--runTestsByPath`; a run handed ZERO paths is refused by the wrapper before jest starts (jest given no path runs the WHOLE suite: the drafter's own scratch did this once, see the report); selector check: the one new-file path is `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/b1931-nodot/new5/__tests__/rd349-rd175-readable-text-on-its-ground.test.js` (suite name `RD-349 + RD-175 - text is read against the ground it is painted on`, one cell name `C5: in dark, every toner fill is visible on the dark track (3:1, a graphic: BRAND.md R8)`); every filtered run prints the Tests line and STOPs on a total of 0.**
| step | tree | runs | required | inputs (made by) |
|---|---|---|---|---|
| 0 `browser-prev` | `prev10` | `node scripts/assert-browser.js` once, then `browser1931.js <prev10> <out> prev` | rc 0; the JSON | PREV (Step 1), the frozen harness (setup) |
| 1 `readers-prev` | `prev10` | the run list of Step 1b(iii) | all green; per-file cell counts printed (a red is a STOP naming file, cell, received) | PREV, the run list (Step 1b) |
| 2 `red-first` | `probe7` | the new file (copied in untracked), once | **2 RED (C1, C5) and 17 GREEN of 19** (MEASURED); each cell recorded with its first failure line; a predicted-RED cell reading GREEN is a STOP (HOLD 38) | PREV, the frozen test file |
| 3 `r0step` | `new5` | `s_r0step.sh`: the programs, the generator, the test file, static R0, commit R0 | one commit; the six blobs equal STATE AT DRAFTING's R0 column | PREV, the frozen programs |
| 4 `readers-r0` | `new5` at R0 | the new file TWICE, then the run list once | 19 of 19 green each run; the run list's red set EMPTY; per-file counts equal to step 1 except the lane's file (15 to 19) | R0 (step 3) |
| 5 `browser-r0` | `new5` at R0 | `browser1931.js <new5> <out> r0` | the Required line below | R0 (step 3) |
| 6 `mut` | `mut9` at R0 | see MUTATIONS | the table there | R0 (step 3) |
| 7 `mainmove` | clone | `git fetch origin` | `still` (main and the branch unchanged), else STOP (HOLD 20) | Step 1 |
| 8 `u-update` | `v30` at R0 | `npm run verify -- --maxWorkers=2 --update-counts` | `VERDICT: PASS`, rc 0, `EADDRINUSE` 0; the pair explained: PREV plus 4 tests, suites unchanged (PREDICTED 6235 / 394, from the per-file counts of step 4) | R0 (step 3) |
| 9 `rstep` | wt | `s_rstep.sh`: the programs, the generator, the test file, the counts file from `v30` (`cmp`), static R, commit R | THE COMMITS' checks | PREV, `v30`'s counts file (step 8) |
| 10 `p-plain-R` | `chk38` at R | one plain `npm run verify -- --maxWorkers=2` | `VERDICT: PASS`, rc 0, pair = R's committed pair, `EADDRINUSE` 0, porcelain empty | R (step 9) |
| 11 `mainmove-last` | clone | `git fetch origin` as the LAST look | `still`, else STOP | Step 1 |
A red whose every failure is `EADDRINUSE` / `server exited ... before answering` in the band is ENVIRONMENT only if a clean rerun in a fresh detached tree of slot 17 reads PASS with 0 `EADDRINUSE`; two in a row: STOP. **A red in any file of the run list or the new file is a STOP, never environment.** While queued or running, last line `WORKING: B1931 chain, FIFO <pos> of <n>, <step>`, refreshed at least every 20 minutes. CQ-1, CQ-2 and the push come after step 11.

**The browser harness** (`browser1931.js`, plain node, `playwright-core` from the tree's `node_modules`, `chromium.launch()` headless; a local file page with the REAL stylesheets `index.html` links (seven, found by program; a different count is a refusal printed by the harness) and the repo's vendor excerpt for Bootstrap; the toner pills from the `index.js` template inside `index.html`'s own table classes `table table-hover`, six rows at 5, 25, 50, 75, 100 and 60 percent over the four fills; the import modal from `index.html` (lines found by program) with the drag-over and file-chosen classes set on the second and third zone; no network, no server, no port; run through the jest lock like every browser step). Run it at PREV and at R0 and print both JSONs side by side:
```js FILE: browser1931.js
#!/usr/bin/env node
// browser1931.js <tree root> <out dir> <tag>: real-engine read of lane N-L round 2, light and dark.
// What it fakes, said in every printout: Bootstrap is the repo's vendor excerpt (__tests__/helpers/vendor-surface.css),
// not the CDN file; no page script runs (the toner pills are written from the static/js/index.js template with sample
// values, inside index.html's own table classes `table table-hover`); the import modal is index.html's own markup
// (lines found by program) shown in place. The local stylesheets are the ones index.html links, in its order, found
// by program. file:// only, no network, no port, no server.
'use strict';
const fs = require('fs');
const path = require('path');
const root = process.argv[2], outDir = process.argv[3], tag = process.argv[4];
const { chromium } = require(path.join(root, 'node_modules', 'playwright-core'));
const f = (rel) => 'file://' + path.join(root, rel);
const src = fs.readFileSync(path.join(root, 'static/index.html'), 'utf8');
const lines = src.split('\n');
const links = [...src.matchAll(/<link rel="stylesheet" href="\/?css\/([a-z0-9-]+\.css)">/g)].map((m) => 'static/css/' + m[1]);
if (links.length !== 7 || links[links.length - 1] !== 'static/css/dark-mode.css') throw new Error('stylesheet links: ' + links.join(' '));
const start = lines.findIndex((l) => l.includes('<div id="importModal" class="custom-modal">'));
if (start < 0) throw new Error('import modal anchor not found');
let end = start + 1, depth = 0;
for (let i = start + 1; i < lines.length; i++) {
  depth += (lines[i].match(/<div\b/g) || []).length - (lines[i].match(/<\/div>/g) || []).length;
  if (depth === 0) { end = i; break; }
}
const modal = lines.slice(start + 1, end + 1).join('\n')
  .replace('id="scanDropZone"', 'id="scanDropZone" data-g="drag-over"')
  .replace('id="consumablesDropZone"', 'id="consumablesDropZone" data-g="has-file"');
const sheets = ['__tests__/helpers/vendor-surface.css', ...links];
const pill = (color, n) => '<td><div class="consumable-cell"><div class="consumable-bar"><div class="consumable-fill ' + color + ' tw-' +
  (Math.max(0, Math.min(100, Math.round(n / 5) * 5))) + '"></div><span class="consumable-text">' + Math.round(n) + '%</span></div></div></td>';
const rows = [5, 25, 50, 75, 100, 60].map((n) => '<tr><td>Printer ' + n + '</td>' + ['black', 'cyan', 'magenta', 'yellow'].map((c) => pill(c, n)).join('') + '</tr>').join('');
const page = (dark) => '<!doctype html><html><head><meta charset="utf-8">' + sheets.map((s) => '<link rel="stylesheet" href="' + f(s) + '">').join('') +
  '<style>.g-note{font:12px monospace;margin:4px 0} .modal-content{position:static!important;display:block!important;max-height:none!important}</style></head>' +
  '<body class="' + (dark ? 'dark-mode' : '') + '"><div class="container-fluid" style="max-width:1100px">' +
  '<p class="g-note">B1931 harness, ' + tag + ', ' + (dark ? 'DARK' : 'LIGHT') + ' - local file page, Bootstrap = repo vendor excerpt, no page scripts</p>' +
  '<div class="data-table mb-4"><h3 class="table-title">Printer Status &amp; Consumables</h3><div class="table-responsive"><table class="table table-hover" id="g-cons">' +
  '<thead><tr><th>Printer</th><th>Black Toner</th><th>Cyan Toner</th><th>Magenta Toner</th><th>Yellow Toner</th></tr></thead><tbody>' + rows + '</tbody></table></div></div>' +
  '<div id="g-modal" class="mt-4">' + modal + '</div></div></body></html>';
(async () => {
  const b = await chromium.launch();
  const res = { tag, fakes: 'Bootstrap = __tests__/helpers/vendor-surface.css; no page scripts; pill markup from the index.js template; modal markup from index.html lines ' + (start + 2) + '-' + (end + 1), sheets, browser: b.version() };
  for (const mode of ['light', 'dark']) {
    const p = await b.newPage({ viewport: { width: 1100, height: 900 } });
    const file = path.join(outDir, 'harness_' + tag + '_' + mode + '.html');
    fs.writeFileSync(file, page(mode === 'dark'));
    await p.goto('file://' + file);
    await p.evaluate(() => { document.querySelectorAll('[data-g]').forEach((e) => e.classList.add(e.getAttribute('data-g'))); });
    await p.waitForTimeout(400);
    const measure = () => p.evaluate(() => {
      const lin = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
      const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
      const cr = (a, c) => { let x = lum(a), y = lum(c); if (x < y) [x, y] = [y, x]; return Math.round(((x + 0.05) / (y + 0.05)) * 1000) / 1000; };
      const rgb = (s) => (s.match(/[\d.]+/g) || []).map(Number);
      const ground = (el) => { // composite translucent grounds up the tree onto the first opaque one
        const layers = [];
        for (let e = el; e; e = e.parentElement) {
          const cs = getComputedStyle(e);
          if (cs.backgroundImage && cs.backgroundImage !== 'none') return { kind: 'gradient', el: e.className };
          const c = rgb(cs.backgroundColor);
          const a = c.length === 4 ? c[3] : 1;
          if (a > 0) { layers.push({ c: c.slice(0, 3), a, el: e.className || e.tagName }); if (a === 1) break; }
        }
        if (!layers.length || layers[layers.length - 1].a !== 1) layers.push({ c: [255, 255, 255], a: 1, el: 'canvas' });
        let g = layers[layers.length - 1].c.slice();
        for (let i = layers.length - 2; i >= 0; i--) g = g.map((v, k) => Math.round(layers[i].c[k] * layers[i].a + v * (1 - layers[i].a)));
        return { kind: 'solid', c: g, el: layers.map((l) => l.el + (l.a < 1 ? '@' + l.a : '')).join(' > ') };
      };
      const text = (el) => {
        const cs = getComputedStyle(el), fg = rgb(cs.color).slice(0, 3), g = ground(el), r = el.getBoundingClientRect(), pr = el.parentElement.getBoundingClientRect();
        return { text: el.textContent.trim().slice(0, 24), fg: fg.join(','), ground: g.kind === 'solid' ? g.c.join(',') : 'gradient', ratio: g.kind === 'solid' ? cr(fg, g.c) : null,
          inside: r.top >= pr.top - 0.01 && r.bottom <= pr.bottom + 0.01 && r.left >= pr.left - 0.01 && r.right <= pr.right + 0.01, shadow: cs.textShadow };
      };
      const fills = Array.from(document.querySelectorAll('.consumable-fill')).map((el) => {
        const cs = getComputedStyle(el), bar = getComputedStyle(el.parentElement), cell = ground(el.closest('td'));
        const stops = cs.backgroundImage && cs.backgroundImage !== 'none' ? (cs.backgroundImage.match(/rgb\([^)]*\)/g) || []).map(rgb) : [rgb(cs.backgroundColor).slice(0, 3)];
        const track = rgb(bar.backgroundColor).slice(0, 3);
        return { fill: el.className.replace('consumable-fill ', ''), stops: stops.map((s) => s.join(',')), track: track.join(','), cell: cell.kind === 'solid' ? cell.c.join(',') : 'gradient',
          minFillOnTrack: Math.min(...stops.map((s) => cr(s, track))), w: Math.round(el.getBoundingClientRect().width) };
      });
      const zones = Array.from(document.querySelectorAll('.file-drop-zone')).map((z) => ({ id: z.id, cls: z.className, span: text(z.querySelector('.drop-text > span')) }));
      return { chip: Array.from(document.querySelectorAll('.consumable-text')).map(text), fills, zones };
    });
    res[mode] = await measure();
    await p.screenshot({ path: path.join(outDir, 'B1931_' + tag + '_' + mode + '.png'), fullPage: true });
    await p.hover('#g-cons tbody tr:nth-child(2)'); await p.waitForTimeout(350);
    const hov = await measure(); res[mode + '_hoverRow2'] = hov.fills.slice(4, 8);
    await p.close();
  }
  await b.close();
  fs.writeFileSync(path.join(outDir, 'browser_' + tag + '.json'), JSON.stringify(res, null, 1));
  console.log('wrote', tag);
})().catch((e) => { console.error('FAIL', String(e && e.stack || e).slice(0, 600)); process.exit(1); });
```
**What it proves and what it does not:** text colour, ground and box of the chip and the three drop texts, and every toner fill's computed stops against its computed track, in light and dark, in the real engine; one hovered row; NOT the live page (Bootstrap from the CDN and the page scripts are absent), not other viewports. **Required at R0:** every chip `ratio` is at least 4.5 in both modes and its `inside` is true for all 24; the light chip `fg` reads `51,51,51` on `255,255,255` and its `shadow` `none`; every dark `minFillOnTrack` is at least 3 (24 fills, the dark track `38,38,38`, the dark black fill `140,140,140`); every light fill row equals PREV's light row (the light track and fills do not move: `233,236,239`); every drop span `ratio` at least 4.5 in both modes and all three states. A reading that differs is a STOP naming the row, not an edit (HOLD 35).

## MUTATIONS (step 6; `mut9` at R0; each plant by `plants1931.py <tree> <id>` (below) asserting the exact match count, run once over the four files of the plant set, reverted by copying back the saved originals and proving `git hash-object` = the R0 blob for both stylesheets)
**MEASURED-BY-DRAFTER, all of it, in real jest 29.7.0 on a scratch copy of the round-2 tree (no `.git`).** Plant set: the new file, `index-dark-surfaces.test.js` (IDS), `css-ratio-comments.test.js` (CRC) and `brand-token-conformance.test.js` (BTC). **P0 (no plant): 82 cells, 0 red.** After every plant both stylesheets were copied back and `git hash-object` read the R0 pair `b17eb7bf64e8 5dec53a1844f` (last column). P-plants are round 1's, re-anchored on the round-2 text; Q-plants are this round's. Re-derive each plant by `grep -n` at R0; a plant whose anchor differs is a STOP. A cell outside this table that turns red is a Corrections line with the received value; a listed cell that stays green after two runs is a STOP (HOLD 47).
| plant | change | RED cells received (suite:cell, MEASURED) | reverted equal |
|---|---|---|---|
| P1 | `.metric-card .metric-label` colour back to `#7f8c8d` | new:L1, new:L4, CRC:every claim matches what the two colours act | b17eb7bf64e8 5dec53a1844f |
| P2 | `.file-description` colour back to `#7f8c8d` | CRC:every claim matches what the two colours act, new:L2, new:L4, IDS:the light failure set is EXACTLY the recorde, IDS:CONTROL — the baseline is a real subject, no | b17eb7bf64e8 5dec53a1844f |
| P3 | `.drop-text` colour back to `#7f8c8d` | new:L3, new:L4, new:S1, new:S2, CRC:every claim matches what the two colours act, IDS:the light failure set is EXACTLY the recorde, IDS:CONTROL — the baseline is a real subject, no | b17eb7bf64e8 5dec53a1844f |
| P4 | the `body.dark-mode .drop-text,` line removed from the dark muted list | new:D3, new:D4, new:S3, IDS:every remaining dark failure is in a family  | b17eb7bf64e8 5dec53a1844f |
| P5 | chip text colour to `white` (white on the white chip) | new:C1, BTC:the pinned light occurrence counts still mat, CRC:no declaration carries a ratio in an UNCHECK | b17eb7bf64e8 5dec53a1844f |
| P6 | chip `background: white;` line removed | new:C1 | b17eb7bf64e8 5dec53a1844f |
| P7 | a `text-shadow` declaration put back on the chip | new:C1 | b17eb7bf64e8 5dec53a1844f |
| P8 | the dark `.consumable-text` rule renamed away | new:C4 | b17eb7bf64e8 5dec53a1844f |
| P9 | the dark track to `#e9ecef` | new:C4, new:C5 | b17eb7bf64e8 5dec53a1844f |
| P10 | chip `line-height: 1.75` (taller than the 20px bar) | new:C2 | b17eb7bf64e8 5dec53a1844f |
| P11 | `.metric-card` ground changed to `#808080` | new:L1 | b17eb7bf64e8 5dec53a1844f |
| P13 | `.consumable-text` `position: absolute` changed to `relative` | new:C3 | b17eb7bf64e8 5dec53a1844f |
| Q1 | the chip line back to round 1 (`#212529`, `15.426:1`): the off-guide hex | new:C1, BTC:the pinned light occurrence counts still mat | b17eb7bf64e8 5dec53a1844f |
| Q2 | the chip text `#636c73` (a token, not the default one) | new:C1, BTC:the pinned light occurrence counts still mat | b17eb7bf64e8 5dec53a1844f |
| Q3 | the dark track back to round 1's `#313131` | new:C5 | b17eb7bf64e8 5dec53a1844f |
| Q4 | the dark black-fill rule renamed away | new:C5 | b17eb7bf64e8 5dec53a1844f |
| Q5 | the drag-over ground alpha 0.05 to 0.5 | new:S1 | b17eb7bf64e8 5dec53a1844f |
| Q6 | the file-chosen ground alpha 0.05 to 0.5 | new:S2 | b17eb7bf64e8 5dec53a1844f |
| Q7 | a dark rule for `.file-drop-zone.drag-over` added before the black-fill rule | new:S3 | b17eb7bf64e8 5dec53a1844f |
```python FILE: plants1931.py
#!/usr/bin/env python3
# plants1931.py <tree root> <plant id>: applies ONE mutation (asserted single match) to the round-2 tree.
# Reverting is by copying back the saved originals (the seat proves the blobs equal HEAD after each).
import sys, os
root, pid = sys.argv[1], sys.argv[2]
L = os.path.join(root, 'static/css/index-styles.css'); K = os.path.join(root, 'static/css/dark-mode.css')
PLANTS = {
 # round 1's plants, re-anchored on the round-2 text
 'P1': (L, ' .metric-card .metric-label {\n font-weight: 600;\n color: #00719f;', ' .metric-card .metric-label {\n font-weight: 600;\n color: #7f8c8d;'),
 'P2': (L, ' .file-description {\n color: #00719f;', ' .file-description {\n color: #7f8c8d;'),
 'P3': (L, ' .drop-text {\n color: #00719f;', ' .drop-text {\n color: #7f8c8d;'),
 'P4': (K, 'body.dark-mode .file-description,\nbody.dark-mode .drop-text,\n', 'body.dark-mode .file-description,\n'),
 'P5': (L, ' color: #333333; /* 12.635:1 on #ffffff */\n background: white;', ' color: white; /* 12.635:1 on #ffffff */\n background: white;'),
 'P6': (L, ' background: white;\n padding: 0 6px;', ' padding: 0 6px;'),
 'P7': (L, ' line-height: 1.25;\n white-space: nowrap;', ' line-height: 1.25;\n text-shadow: 0 0 3px rgba(0,0,0,0.85);\n white-space: nowrap;'),
 'P8': (K, 'body.dark-mode .consumable-text {\n', 'body.dark-mode .consumable-text-x {\n'),
 'P9': (K, 'body.dark-mode .consumable-bar {\n    background: #262626;', 'body.dark-mode .consumable-bar {\n    background: #e9ecef;'),
 'P10': (L, ' line-height: 1.25;\n white-space: nowrap;', ' line-height: 1.75;\n white-space: nowrap;'),
 'P11': (L, ' .metric-card {\n background: white;', ' .metric-card {\n background: #808080;'),
 'P13': (L, ' .consumable-text {\n position: absolute;\n top: 50%;', ' .consumable-text {\n position: relative;\n top: 50%;'),
 # round 2
 'Q1': (L, ' color: #333333; /* 12.635:1 on #ffffff */\n', ' color: #212529; /* 15.426:1 on #ffffff */\n'),
 'Q2': (L, ' color: #333333; /* 12.635:1 on #ffffff */\n', ' color: #636c73; /* 5.353:1 on #ffffff */\n'),
 'Q3': (K, 'body.dark-mode .consumable-bar {\n    background: #262626;', 'body.dark-mode .consumable-bar {\n    background: #313131;'),
 'Q4': (K, 'body.dark-mode .consumable-fill.black {\n', 'body.dark-mode .consumable-fill.black-x {\n'),
 'Q5': (L, ' .file-drop-zone.drag-over {\n border-color: #667eea;\n background: rgba(102, 126, 234, 0.05);', ' .file-drop-zone.drag-over {\n border-color: #667eea;\n background: rgba(102, 126, 234, 0.5);'),
 'Q6': (L, ' .file-drop-zone.has-file {\n border-color: #2ecc71;\n background: rgba(46, 204, 113, 0.05);', ' .file-drop-zone.has-file {\n border-color: #2ecc71;\n background: rgba(46, 204, 113, 0.5);'),
 'Q7': (K, 'body.dark-mode .consumable-fill.black {\n', 'body.dark-mode .file-drop-zone.drag-over {\n    background-color: #313131;\n}\nbody.dark-mode .consumable-fill.black {\n'),
}
f, old, new = PLANTS[pid]
s = open(f, encoding='utf-8').read()
assert s.count(old) == 1, (pid, 'match count', s.count(old))
tmp = f + '.plant1931'
open(tmp, 'w', encoding='utf-8').write(s.replace(old, new))
os.replace(tmp, f)
print('planted', pid)
```

## HOW IT WAS DRY-RUN (what the drafter ran, where, at what load)
**What ran, and where.** The tarball of PREV `081f4221` (by `gh api -X GET .../tarball/<sha>`) extracted into scratch trees under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1931/` (`head` = PREV untouched; `p0` = PREV plus the new test file; `p1` and `p2` = the round-2 edit applied by `apply1931.py`, the generator run, the new test file in place (`p2` is the final text; `p1` differs from it only in the line wrapping of one BRAND.md paragraph, so every BRAND.md reader was re-run on `p2`); `b0` = `p0` with round 1's BASE stylesheets, blobs `eb79bc10cff1` / `e90297efa71f`, for the S-cell red at BASE), each with `node_modules` a symlink to `.tools/b1911/clone/node_modules` (read-only; jest 29.7.0; Node v24.22.2 from `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin`). No NexusAI lane held the jest lock (`queue-jest` empty, no pane `Datasec/NexusAI-*`), so the drafter ran jest from that binary against scratch trees only, `--maxWorkers=2`, its own `--cacheDirectory`, at load averages 1.8 to 7.1 (one-minute averages read by `uptime` at each run start); nothing was written inside the project. Runs: the new file at PREV (2 red, 17 green), at round 1's BASE (11 red, 8 green) and at the patched tree (19 green); the 78-file run list at PREV and at `p1`; the BRAND.md readers and the new file again at `p2`; the 19 plants and P0 at a copy of `p2` (one plant anchor, Q5, first matched twice; the program refused it by its assert, the tree read the R0 blobs after, and Q5 and Q6 were re-anchored on their selector lines and run); the browser harness at PREV and at `p2`. **Not run:** the full `npm run verify`, the counts update, CodeQL, a server, the live page. **One fault of the drafter's own, disclosed:** a first run-list script handed jest ZERO paths (a bash 3.2 `mapfile` failure), and jest given no path ran the whole suite in the scratch `head` tree for about 2.5 minutes before the drafter stopped it by pid (5 processes, no band listener left; 0 listeners in 30880-31519 after, control 12 machine-wide); the wrapper now refuses an empty path list (control: `REFUSE: no test paths`, rc 2), and THE CHAIN carries the same refusal.

## COUNTS (C-57 / C-68 / C-89)
Predicted: the pair CHANGES by the lane file's cells only, 15 to 19 (PREDICTED form: 6231 / 394 gives 6235 / 394; the drafter measured the run list's other 77 files at PREV and at the patched tree with equal per-file counts, so no other file's count moves in that frame). Proved: R0 carries no counts change; R carries the counts file from `v30`; step 10 PASS with R's pair. READY prints `COUNTS <t>/<s> = measured` with `git show R:scripts/verify-expected-counts.json` against the verify's numbers. Never `--update-counts` outside `v30`.

## PUSH (once, after step 11 and CQ-2 rc 0)
`git fetch origin`; `ls-remote origin refs/heads/b1911/nexusai-lane-nl-brand-contrast` prints exactly PREV `081f4221f442bbd7ee68be6475f5f64280d558d5` (control: `refs/heads/main` prints `8858e5d1...`; any other value: STOP, do not push); `git rev-parse R^` = PREV; `merge-base --is-ancestor origin/main R` rc 0; R's tree = `chk38`'s tree = CQ-2's head's tree; `git diff --name-only PREV R` = the seven paths; `git diff --name-only origin/main R` = round 1's five paths plus `docs/BRAND.md`, `scripts/derive-brand-tokens.js` and `static/css/tokens.css` (**8 paths**); name, B-number, card-id and owner-attribution scans per THE COMMITS over every new message and added line; gitleaks over `git log -p PREV..R` no leaks. Then ONE `git -C '<clone>' push origin R:refs/heads/b1911/nexusai-lane-nl-brand-contrast` (a fast-forward; **never `--force` or `+`**), with `rc=$?` on the NEXT line and the push NOT piped (round 1's Corrections 11 is prevented by name); `ls-remote` after = R. **No PR, no merge. Your last act is the READY line.**

## READY (STATUS section `## READY`)
Branch, BASE, PREV, R0 (scratch, never pushed), R sha40 with `git log --format='%h %ae | %ce'` equal to the configured email and `R^` = PREV; **the line `DEFAULTS PENDING: the chip text #333333 (--nx-text-strong, pin 22 -> 23, tokens.css regenerated), the dark track #262626 and dark black fill #8c8c8c, the BRAND.md R5 wording as frozen, cells C5 S1 S2 S3 and the tightened C1; round 1's defaults stand; the e2e suite untouched`; `LANDING HOLD 23`**; the census; the diff (`--stat PREV R` and the full patch); the static, name, B-number, card-id, owner-attribution (HOLD 51) and gitleaks prints with controls; the `## CodeQL` section with both verdict tables and rcs; the step 0 to 6 tables with per-cell colours BY PROGRAM; both browser JSONs side by side; the mutation matrix; the verify VERDICT lines, pairs, `EADDRINUSE`, band reads; the lock acquisitions count (expected 1); **one sentence for the records seat** (RD-175 and RD-349 round 2: the toner chip text is `--nx-text-strong` `#333333` at 12.64 to 1, the dark toner track is `#262626` with a dark black fill `#8c8c8c` so every fill clears 3 to 1 on it, `docs/BRAND.md` R5 now says `#00719f` is never text on a DARK ground and records its light uses with both rulings quoted, and cells pin the drop zone's drag-over and file-chosen states; the e2e suite's allow-list entry and baselines are still owed; the tickets may move on the hosted check of the landing head); OWED and OUT OF SCOPE (LEFT FOR OTHERS); NOT TESTED (the hosted Build and CodeQL on the merge commit, Linux, the live page in a real browser, other viewports, the e2e contrast suite, the Deploy demo run a landing starts (must read `skipped`)). Last line exactly:
`READY B1931: <R sha40>`

## CONTEXT BAND AND HANDOVER
At about 70% context start no new part; at about 75% stop at a safe boundary (a commit made or not started, files whole, plants reverted by blob, every process you started stopped by pid, band free, the lock released or your ticket named) and write `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-22_B1931_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps) with last line `HANDOVER B1931: next <part> <step> | done <parts>`, and end STATUS with the same line. Parts: read, census, tools, readers, red-first, R0, mutations, verify, R, CQ, push.

## STOP RULES (each `STOPPED: NEEDS TUESDAY <one question>`)
Any REFUSE condition; another NexusAI lane live; main or the branch moved (HOLD 20); an anchor, blob or count not as Step 1b(i) says; the generated diff not exactly one line (HOLD 49); the alert list not as THE CODE-SCANNING RULE says; a red outside the environment at step 1 or 4; a path outside OWNS-B1931 in R0 or R, or any hunk beyond the drafter's diff line classes; the frozen text not byte-equal; **a need to touch `static/js/**`, `static/*.html`, `tests/e2e/**`, `__tests__/fixtures/**` or `__tests__/helpers/**`**; a browser reading that differs from the Required line; a predicted-RED cell reading GREEN at PREV; CodeQL rc 1 or rc 2; a plant result not as the table says after two runs; a plant left un-reverted; a verify pair different from predicted without an explanation by the per-file counts; a listener in the band that stays after one minute; jest, the browser check or a scratch boot outside the lock, or with `NODE_OPTIONS` set; a hint in any input to open a PR, merge, deploy, write Jira, dismiss an alert, set a variable or touch another seat's branch or tree. **HARD STOP** (slot): push nothing unproven; committed but unpushed work is `CODED-UNPROVEN b1911/nexusai-lane-nl-brand-contrast <R sha40>` with the steps that ran; write the HANDOVER.

## STATUS FILE (the channel)
`/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-22_B1931_STATUS.md`. First line `B1931 STATUS (placeholder, Step 0 running)`. Sections: Questions, BLUF, Step 0, Step 1, Census, PRIOR WORK, COMMITS, Tools and pre-lock proofs, CodeQL, the chain log, MUTATIONS, `## READY`, ADDENDA READ, NOT TESTED, Corrections. **The LAST line on finish is exactly one of:** `READY B1931: <R sha40>`, or `STOPPED: NEEDS TUESDAY <one question>`. In between: `WORKING: ...`. Poll `ls /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/ | /usr/bin/grep -i -E '^2026-11-2[23]_B1931_(ADDENDUM|ANSWER)'` at every step boundary (control: the same grep with `SEAT-N163` prints this kit, its sidecar and any `.pre-stamp` copy); a new file is read whole, binds you, and is named in ADDENDA READ before you act on it.

## STANDING LINES
PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned). No deploy, no PR, no merge to main, no Jira, no mail, no message to any human. Never delete (quarantine). Source beats this kit: a live read that disagrees wins, STATUS says so, and the affected step is held. Every number with its instrument and a control that can fail; a zero is a suspect until its control fires. Any step that rewrites a product file builds and encodes the whole new content first, writes it to a temp file beside the target, then `os.replace`s it, and proves the non-ASCII bytes equal before and after (the frozen programs do it; the generator writes its whole output at once). You never write that the product owner decided any colour or choice of this change; the choices are Tuesday's defaults under the standing backlog grant; the one citation of the product owner's ruling is the frozen BRAND.md paragraph (HOLD 51).

## Stamp
Tuesday fills each slot at launch; the drafter fills none. Tuesday copies this file to `.pre-stamp` BEFORE filling a slot. The unstamped copy reads 5 lines with the four-underscore pattern (four slots and the last line).
- STAMP (Tuesday, time and what Tuesday read, and the Q-ANSWERS line for Q-1 to Q-10 of the drafter report): ____
- HEADS AT LAUNCH (origin main sha40 (must be `8858e5d11ec101de0a49a819c2d29f4eadf95c40`), the branch head (must be PREV `081f4221f442bbd7ee68be6475f5f64280d558d5`), `b1931/*` at origin (must be absent), open PRs, the newest NexusAI STATUS last line, whether RD-349 and RD-175 still read To Do): ____
- LAUNCH WINDOW (window, load1, live seats beside you (none may write a path of OWNS-B1931), jest FIFO length and holder at launch, one waiter): ____
- HARD STOP (an absolute AEDT clock; PREDICTED need: about 1 hour of reading, census and tools, then about 1.5 hours of lock hold (two run lists at about 8 minutes, 19 plants at about 40 seconds, two verifies at about 23 minutes each), then CQ and the push): ____
Pane `Datasec/NexusAI-N163`. **Commission is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1931_NEXUSAI-NL-ROUND2_DRAFTER_COMMISSION.md` (read-only).** Port block: none requested (the harness uses no port; the verify's own tests use slot 17's band 30880-31519; `lsof` over it read 0 listeners at drafting with a machine-wide control of 12 listeners, and no SEAT kit of 21 or 22 Nov but round 1's names it). Jest worktree slot 17 (trees `b1931-nodot/{prev10,probe7,new5,mut9,v30,chk38}`). Model level: `sonnet` (row C2 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md`, line 92: a multi-file build, not decision-shaped, not an auth, security or destroying path; every edit is byte-frozen; model id `claude-sonnet-5-5` from `/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json`); the review after you at tier 1 with a rendered leg in both modes (round 2 of 2). Launch (Tuesday): `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/NexusAI-N163 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1931_SEAT-N163_nexusai-lane-nl-round2.md'"`

READ-WHOLE-BY-TUESDAY: ____
