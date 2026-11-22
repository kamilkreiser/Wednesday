From Tuesday (the Datasec coordinator seat), Datasec / NexusAI. **You do NOT use the shared inbox `datasec-nexusai@`**: your STATUS file and its last line are the only channel to Tuesday; Tuesday's channel to you is a `2026-11-2[34]_B1967_(ADDENDUM|ANSWER)-<n>_*.md` file in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`. A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED-BY-DRAFTER** = the drafter ran the instrument named (each such literal has a claim line in the sidecar `<this kit>.measured`); **RELAYED** = read in another file (re-read it at source before you rely on it); **PREDICTED** = the drafter's arithmetic, nobody has measured it; **UNMEASURED** = nobody has. The drafter's report is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1967_DRAFTER-REPORT.md` (read-only; read it whole at Step 0). **The form is the NexusAI kit B1958 (`2026-11-23_B1958_SEAT-N164_nexusai-nx-p-permission-table.md`: STATUS channel, REFUSE AT ONCE, frozen programs extracted by `awk`, holds) with the lock, clone, worktree and jest legs REMOVED: this seat builds nothing, commits nothing, runs no jest and no server, and writes no file of the repository. It produces ONE options document (Markdown and PDF) with screenshots.** This is a SMALL READ-ONLY lane: about 15 minutes of reading and running frozen programs, then the document. **BASE for every measurement: NexusAI main `3c3be156e8ea36ad297fdadd3055c6e00252ba38`** (repository `datasecau/Reporting_Dashboard_Au`, read through `gh api -X GET` at that sha; no clone).

# BRIEF B1967 - SEAT-N166: NEXUSAI RD-1032 OPTIONS: THE LIGHT-MODE CYAN, MAGENTA AND YELLOW TONER FILLS READ BELOW 3 TO 1 ON THE LIGHT TRACK; THE PRODUCT OWNER PICKS; THIS SEAT PROPOSES BRAND-TOKEN CANDIDATES WITH BEFORE AND AFTER SCREENSHOTS AND WRITES THE OPTIONS DOCUMENT; NOTHING IS BUILT

## THE RULING AND THE TICKET (RELAYED from Tuesday's commission, which printed the board record whole; MEASURED-BY-DRAFTER for the ticket text)
- **The ruling** (the product owner's 2026-11-23 answer, board option a, label "Show me options first", detail verbatim): "An agent proposes darker values for each fill from the brand tokens, with before and after screenshots; you pick, then it is built and gated. Nothing is built before you pick." So this seat BUILDS NOTHING for main: it writes an options document. **The colour choice is the product owner's** (the ticket's own words: "the choice of values is a brand decision (BRAND.md section 8, rule 1: use a token; if none fits, the gap is a brand decision) and is the product owner's"). **Who-decided lines for your document: the colour (or outline) choice is the product owner's; the candidate list, the hue rule, the ranking and the recommendation are the coordinator's.**
- **The ticket.** RD-1032 (Bug, To Do, labels `operations` and `records-pass-1123`, updated 2026-11-23T04:14, 0 comments; read by Jira GET at drafting, 4028 bytes of text). In light mode the cyan, yellow and magenta toner fills read below 3 to 1 on the light track `#e9ecef` (`.consumable-bar`, `static/css/index-styles.css` line 244), figures at their lowest stops: black 7.83, cyan 1.74, magenta 2.58, yellow 1.29. Rule R8 of `docs/BRAND.md` (lines 767 to 770): a graphic (a bar, an indicator; WCAG 1.4.11) clears 3 to 1 against its ground. The ticket's Recommendation: decide the light fills' colours so each clears 3 to 1, or give the bar a border or a darker track that does. The ticket is a bug the product owner has now routed to options first.
- **Tier and model.** No row of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md` names an options-document seat; the nearest measured-and-then-write row is C2 (line 92, Sonnet first), the work is spelled out in frozen programs and decides nothing, so **Sonnet** (`claude-sonnet-5-5`, `models_latest.json`, key `sonnet`). The review of the document is Tuesday's.

## WHAT THE DRAFTER FOUND (MEASURED-BY-DRAFTER; the programs below are the instruments, and each result is reproduced by you at Step 3 to 5)
1. **Control first.** The program reproduces the ticket's four lowest-stop figures exactly (black 7.83, cyan 1.74, magenta 2.58, yellow 1.29) from the stylesheet's own gradient stops on `#e9ecef`, and `#000000` against `#ffffff` reads 21.000. A negative control (the cyan stop against the yellow figure) differs, so the instrument can disagree. The project's own helper (`__tests__/helpers/dom.js` lines 151 to 167, extracted and evaluated) agrees with it on 57 pairs within 0.005.
2. **Candidates, by program.** The tokens file holds 49 light tokens and 51 dark tokens (counted by program, and a second independent `grep -c` reads 100 token lines in all). "Same hue family" is a stated rule: HSL saturation 0.20 or more and hue within 30 degrees of the fill's mean hue (cyan 187, magenta 340, yellow 45 degrees). Window sizes: cyan 22 tokens, magenta 4, yellow 6. Tokens clearing 3 to 1 on the track: cyan 15, magenta 3, yellow 3. After the stated exclusions (ground tokens, notice tokens, sidebar text tokens, aliases of the same hex) the screenshots show **cyan 7, magenta 2, yellow 2** candidates. **No hue is without a passing token**, so the "gap" path of BRAND.md section 8 rule 1 is not forced; but a colour clears 3 to 1 on this track only if its relative luminance is at most 0.245, and the current stops sit at 0.41 to 0.46 (cyan), 0.19 to 0.29 (magenta) and 0.59 to 0.64 (yellow): so every passing yellow is an amber or brown, the passing magenta a rose red, and the passing cyan a teal or blue. The document says so plainly.
3. **Non-colour options.** A darker track: no light token clears 3 to 1 for all four current fills; only `--nx-chrome-navy` clears it for cyan, magenta and yellow and it reads 1.36 for black. An outline: 27 tokens clear 3 to 1 against both the track and the card ground; the plainest is `--nx-text-muted` (`#6c757d`, 3.95 on the track, 4.69 on the card).
4. **A finding the ticket does not carry: dark mode inherits the light rule.** `static/css/dark-mode.css` has a rule for the black fill only (flat `#8c8c8c`, line 1994); cyan, magenta and yellow in dark are the light gradients. A candidate written into the light rule alone reaches dark mode, and several fall below 3 to 1 on the dark track `#262626` (for example `--nx-role-security` 2.86, `--nx-brand-chrome` 2.78). The document carries this as its own section and a screenshot.
5. **Brand-gate consequences, by program over the generator.** The role accents (`--nx-role-*`) are kind graphic with grounds card and page only, not the raised ground the track is; 20 light values carry a pinned count (e.g. `--nx-danger` 13, `--nx-brand-blue-dark` 21); `--nx-danger` is the error colour. These are listed per candidate in the document's tables, not decided.
6. **The project's own contrast harness does not render these bars from a page.** `package.json` line 34 `"test:contrast": "playwright test"` runs `tests/e2e/*.spec.js`; `playwright.config.js` has no `webServer` block and its `globalSetup` (`tests/e2e/global-setup.js`) throws "REFUSING TO RUN: BASE_URL is not set" unless `BASE_URL` is set and the app behind it answers `/api/health`. So it measures a booted app (a server, a port band, the jest-adjacent boot machinery), which this seat must not start; the render in this lane is a local-file harness over the real stylesheets, the shape pull request 240's independent check used. Read at BASE, not run.
7. **Rendered check.** A real Chromium (Playwright's bundled build, 151.0.7922.34) renders 21 scratch pages from local files only: 222 bars, 0 non-file requests; every flat candidate's pixel equals its hex and its pixel-measured ratio equals the computed one; 3 controls fired. Dark mode is rendered unchanged as the control.

## STATE AT DRAFTING (MEASURED-BY-DRAFTER; re-read every line at Step 1 at YOUR read)
- origin main `3c3be156e8ea36ad297fdadd3055c6e00252ba38` (GitHub `commits/main`, committer date 2026-11-22T17:56:29Z, read 2026-11-23 10:14 AEDT). **NexusAI lane NX-SR (seat N165, kit B1966):** its STATUS file ends `READY B1966: d37db35c9bb99cf39136448a05f1a39ef214313e` at 10:30 AEDT, its pane `Datasec/NexusAI-N165` was still listed, the jest lock directory `queue-jest` was empty and no `jest` process ran at 10:30:40. **That state is not yours to assume: you re-read it at REFUSE 4, and you never touch N165's files, worktree or lock either way.**
- Sources at BASE, each fetched by `gh api -X GET 'repos/datasecau/Reporting_Dashboard_Au/contents/<path>?ref=<BASE>' -H 'Accept: application/vnd.github.raw'` (sha256 first 16 hex, bytes; the drafter's copies; Step 1 re-hashes yours and a difference is a STOP):

| file (saved as in `work/`) | path at BASE | sha256 first 16 | bytes |
|---|---|---|---|
| `tokens.css` | `static/css/tokens.css` | 22da6d85e48d178b | 17727 |
| `BRAND.md` | `docs/BRAND.md` | 1e73795bbd646d7f | 54591 |
| `index-styles.css` | `static/css/index-styles.css` | dca036d2d0fec606 | 42750 |
| `dark-mode.css` | `static/css/dark-mode.css` | aba73a99383fbd1e | 86207 |
| `package.json` | `package.json` | 0cd0f876d2ae7015 | 4666 |
| `derive-brand-tokens.js` | `scripts/derive-brand-tokens.js` | d0f858293639d152 | 50618 |
| `dom.js` | `__tests__/helpers/dom.js` | 28d64dc2838e2fd8 | 35954 |
| `rd349test.js` | `__tests__/rd349-rd175-readable-text-on-its-ground.test.js` | 1e002043a2179840 | 18118 |
| `index.js` | `static/js/index.js` | fa12ce58102e7a57 | 476116 |
| `playwright.config.js` | `playwright.config.js` | 9a34ff09b10f5c55 | 2444 |
| `global-setup.js` | `tests/e2e/global-setup.js` | 26e7b987c1f44245 | 5520 |
| `pr240.txt` | pull request 240, GET `repos/datasecau/Reporting_Dashboard_Au/pulls/240` (state, merge sha, title, body) | f978dca17f87555a | 5838 |
| `rd1032.txt` | Jira GET RD-1032 (not a repository file; Step 1 compares size only) | fefd850678cc39ad | 4028 |
- The seat NEVER reads `docs/BRAND.md` whole or `static/js/index.js` whole (54591 and 476116 bytes): it reads the excerpts named in THE WORK by `sed -n`.
- **Tools on this machine (MEASURED-BY-DRAFTER):** Node v24.22.2 at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin` (first on PATH); Playwright 1.62.1 in `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1931/clone/node_modules` (read-only, through an argument of `render.js`; the checkout's own `2_Project_Files/node_modules` holds the same 1.62.1 and is the fallback); Playwright's Chromium builds in `~/Library/Caches/ms-playwright` (1243 among them); `pandoc` at `/opt/homebrew/bin/pandoc`; Google Chrome at `/Applications/Google Chrome.app`; `pdftoppm`; Python 3 standard library only (no Pillow: the PNG reader is in the program).

## THE LANE, ITS PARTITION AND WHAT IT MAY WRITE
```OWNS-B1967
+ /Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1967/**                                          (frozen programs, logs, kit copy)
+ /Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1967_OPTIONS/**    (the evidence folder: data, shots, the document)
+ /Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1967_STATUS.md     (the channel)
```
**PARTITION, from both sides.** You write the three paths above and nothing else: **no branch, no commit, no push, no pull request, no Jira write, no change to any tracked file of the repository, no clone, no `git fetch`, no worktree.** Every file of the repository is read only through `gh api -X GET` at BASE. **Nobody else writes these paths:** `.tools/b1967` did not exist at drafting (REFUSE 3). **Lane NX-SR (N165, kit B1966) writes `__tests__/rd711-audit-flush-serialised.test.js`, `__tests__/rd615-audit-flush-cannot-resurrect-erased-entries.test.js` and `.tools/b1966/**` and holds the jest lock for its chain: none of those is yours, and you take no lock of any kind** (a browser render is not jest). **Lane NX-P (N164, kit B1958)** owns `backend/services/capabilities.js` and two tests: not yours either. **Can N166 run beside N165 and N164?** YES: no jest, no server, no port band (the pages are opened as `file://` URLs and `render.js` counts every non-file request, expected 0, a STOP otherwise), no clone, no `npm`; the only shared resource is CPU, so run the render with `nice -n 10`.

## THE FROZEN PROGRAMS (extracted by `awk` into `.tools/b1967/frozen/`, each `cmp`ed to a second extraction, never retyped; they take the WORK DIRECTORY as first argument, which is `<EV>/data` where `<EV>` = `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1967_OPTIONS`)
Run order and what each prints: `cand.py` (controls, token table, families, the two non-colour options; writes `cand.json`), `xcheck.js` (the project helper's ratios against `cand.py`'s), `extra.py` (the luminance ceiling, a reference-only darkening, the sources' hashes), `gen_harness.py` (writes the scratch pages and `plan.json`), `render.js` (Chromium; writes `shots/`), `pixel.py` (reads the PNGs back), `mkdoc.py` (writes the document), `scans.py` (the document's scans, Step 6).
```python FILE: cand.py
#!/usr/bin/env python3
# cand.py <r2 dir>: B1967 drafter prototype of the OPTIONS seat's candidate computation (stdlib only, read-only over
# local copies of main 3c3be156 files). Prints controls first, then the token table, the per-hue families, the two
# non-colour options. Writes cand.json beside it. WCAG 2.x relative luminance with the project's own threshold 0.03928
# (__tests__/helpers/dom.js lines 151-167, which names it "WCAG 2.x relative luminance").
import re, sys, json, colorsys, os
D = sys.argv[1]
TH = 0.03928

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def lum(h):
    def ch(v):
        c = v / 255.0
        return c / 12.92 if c <= TH else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex2rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = (la, lb) if la >= lb else (lb, la)
    return (hi + 0.05) / (lo + 0.05)

def hsl(h):
    r, g, b = [v / 255.0 for v in hex2rgb(h)]
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    return hh * 360.0, ss, ll

def hdist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)

# ---------- tokens.css
css = open(os.path.join(D, 'tokens.css'), encoding='utf8').read()
i_dark = css.index('html[data-theme="dark"]')
light_txt, dark_txt = css[:i_dark], css[i_dark:]
def parse_block(txt):
    out = {}
    for m in re.finditer(r'--nx-([a-z0-9-]+):\s*(#[0-9a-fA-F]{6}|var\(--nx-([a-z0-9-]+)\))\s*;\s*/\*(.*?)\*/', txt):
        out[m.group(1)] = (m.group(2).lower() if m.group(2).startswith('#') else None, m.group(3), m.group(4).strip())
    return out
LB, DB = parse_block(light_txt), parse_block(dark_txt)
def resolve(name, blk, fallback=None, depth=0):
    v, alias, _ = blk[name]
    if v: return v
    if alias in blk: return resolve(alias, blk, fallback, depth + 1)
    return resolve(alias, fallback, None, depth + 1)
LIGHT = {n: resolve(n, LB) for n in LB}
DARK = {n: resolve(n, DB, LB) for n in DB}
TRACK = LIGHT['surface-raised']; CARD = LIGHT['surface-card']; PAGE = LIGHT['surface-page']

# ---------- the current fills (index-styles.css lines 259-262)
FILLS = {'black': ('#2c3e50', '#34495e'), 'cyan': ('#00bcd4', '#26c6da'),
         'magenta': ('#e91e63', '#f06292'), 'yellow': ('#ffc107', '#ffca28')}
REVIEW = {'black': 7.83, 'cyan': 1.74, 'magenta': 2.58, 'yellow': 1.29}   # RD-1032 / the review's figures, lowest stop

res = {'track': TRACK, 'tokens_light': len(LIGHT), 'tokens_dark': len(DARK)}
print('INSTRUMENT: WCAG 2.x relative luminance, linear threshold %s (as __tests__/helpers/dom.js lines 151-167); track %s = --nx-surface-raised (light)' % (TH, TRACK))
print('tokens parsed: light %d, dark %d' % (len(LIGHT), len(DARK)))
print('\nCONTROLS (the review\'s figures at the lowest stop, reproduced)')
ctl_ok = True
cur = {}
for f, stops in FILLS.items():
    rs = [round(ratio(s, TRACK), 2) for s in stops]
    low = min(rs)
    ok = abs(low - REVIEW[f]) < 0.006
    ctl_ok = ctl_ok and ok
    cur[f] = {'stops': list(stops), 'ratios': rs, 'lowest': low, 'review': REVIEW[f], 'match': ok}
    print('  %-8s stops %s ratios %s lowest %.2f review %.2f %s' % (f, stops, rs, low, REVIEW[f], 'MATCH' if ok else 'MISMATCH'))
print('  control fires if a figure differs: all four match = %s' % ctl_ok)
# negative control: the instrument must be able to disagree
neg = abs(round(ratio('#00bcd4', TRACK), 2) - 1.29) > 0.5
print('  negative control (cyan stop vs the yellow figure 1.29 must NOT match): %s' % neg)
res['controls'] = {'fills': cur, 'all_match': ctl_ok, 'negative_control_fires': neg}
# white on black = 21, white on white = 1 (instrument sanity)
print('  sanity: #000 vs #fff %.3f (must be 21.000); #fff vs #fff %.3f (must be 1.000)' % (ratio('#000000', '#ffffff'), ratio('#ffffff', '#ffffff')))

# ---------- dark control (unchanged by this seat): dark fills on the dark track
dtrack = DARK['surface-raised']
dk = {'black': ('#8c8c8c',), 'cyan': FILLS['cyan'], 'magenta': FILLS['magenta'], 'yellow': FILLS['yellow']}
print('\nDARK CONTROL (track %s): lowest stop' % dtrack)
res['dark'] = {}
for f, stops in dk.items():
    rs = [round(ratio(s, dtrack), 2) for s in stops]
    res['dark'][f] = {'stops': list(stops), 'ratios': rs, 'lowest': min(rs)}
    print('  %-8s %s lowest %.2f' % (f, rs, min(rs)))

# ---------- fill hues
fh = {}
for f in ('cyan', 'magenta', 'yellow'):
    hs = [hsl(s)[0] for s in FILLS[f]]
    fh[f] = sum(hs) / len(hs)
print('\nFILL HUES (mean over the two stops): ' + ', '.join('%s %.0f' % (k, v) for k, v in fh.items()))
res['fill_hue'] = fh

# ---------- generator kinds / grounds for shell tokens (derive-brand-tokens.js)
gen = open(os.path.join(D, 'derive-brand-tokens.js'), encoding='utf8').read()
kinds = {}
for m in re.finditer(r"'([a-z-]+)':\s*\{[^{}]*?kind:\s*'(text|graphic|ground)'(?:,\s*grounds:\s*\[([^\]]*)\])?", gen):
    kinds[m.group(1)] = (m.group(2), re.findall(r"'([a-z-]+)'", m.group(3) or ''))
for n in ('role-tenant-admin', 'role-finance', 'role-security', 'role-partner-manager', 'role-partner-tech'):
    kinds[n] = ('graphic', ['surface-card', 'surface-page'])   # SHELL_ROLES loop, generator lines 374-378
for n, g in (('activity-scan', ['surface-card', 'surface-page', 'activity-scan-subtle']), ('activity-fax', ['surface-card', 'surface-page', 'activity-fax-subtle'])):
    kinds[n] = ('text', g)   # generator lines 335 and 353
# pinned light counts (the 20 MEASURED light values; generator LIGHT block): a new call site of one moves its pin (R7)
PINNED = {m.group(1): int(m.group(2)) for m in re.finditer(r"^  '([a-z-]+)':\s*\{ value: '#[0-9a-fA-F]{6}', count: (\d+)", gen, re.M)}
print('pinned light tokens read from the generator: %d (control: must be 20); e.g. danger x%d, brand-blue-dark x%d' % (len(PINNED), PINNED.get('danger', -1), PINNED.get('brand-blue-dark', -1)))
res['pinned_count'] = len(PINNED)
DTRACK = DARK['surface-raised']
# ---------- all light tokens
rows = []
for n, h in sorted(LIGHT.items()):
    H, S, L = hsl(h)
    rows.append({'token': '--nx-' + n, 'hex': h, 'hue': round(H, 1), 'sat': round(S, 2), 'light': round(L, 2),
                 'vs_track': round(ratio(h, TRACK), 2), 'vs_card': round(ratio(h, CARD), 2), 'vs_page': round(ratio(h, PAGE), 2),
                 'kind': kinds.get(n, (None, []))[0], 'grounds': kinds.get(n, (None, []))[1],
                 'vs_dark_track_if_inherited': round(ratio(h, DTRACK), 2), 'pinned': PINNED.get(n)})
res['all_tokens'] = rows
print('\nALL LIGHT TOKENS (%d) with hue/sat and ratio on the track' % len(rows))
for r in rows:
    print('  %-34s %s hue %5.1f sat %.2f  track %5.2f card %5.2f  %s' % (r['token'], r['hex'], r['hue'], r['sat'], r['vs_track'], r['vs_card'], r['kind'] or ''))

# ---------- families
W, SMIN = 30.0, 0.20
print('\nFAMILY RULE: chromatic (HSL saturation >= %.2f) and circular hue distance <= %.0f degrees from the fill\'s mean hue' % (SMIN, W))
fam = {}
for f in ('cyan', 'magenta', 'yellow'):
    cs = []
    for r in rows:
        if r['sat'] >= SMIN and hdist(r['hue'], fh[f]) <= W:
            cs.append(r)
    cs.sort(key=lambda r: -r['vs_track'])
    fam[f] = cs
    print('\n  %s (hue %.0f; current lowest %.2f): %d tokens in the window' % (f.upper(), fh[f], cur[f]['lowest'], len(cs)))
    for r in cs:
        gr = ('surface-raised' in r['grounds'])
        print('     %-32s %s hue %5.1f  vs track %5.2f %s  vs own stops %s  kind=%s grounds=%s raised-named=%s' % (
            r['token'], r['hex'], r['hue'], r['vs_track'], 'PASS' if r['vs_track'] >= 3 else 'fail',
            [round(ratio(r['hex'], s), 2) for s in FILLS[f]], r['kind'], r['grounds'], gr))
res['family'] = {f: [dict(r, vs_stops=[round(ratio(r['hex'], s), 2) for s in FILLS[f]], pass3=r['vs_track'] >= 3) for r in cs] for f, cs in fam.items()}
print('\nWIDER CONTEXT (30 < hue distance <= 60, chromatic) - NOT the same family, shown so the window is not hiding a near miss')
for f in ('cyan', 'magenta', 'yellow'):
    for r in sorted(rows, key=lambda r: -r['vs_track']):
        if r['sat'] >= SMIN and W < hdist(r['hue'], fh[f]) <= 60:
            print('   %-8s %-32s %s hue %5.1f track %5.2f %s' % (f, r['token'], r['hex'], r['hue'], r['vs_track'], 'PASS' if r['vs_track'] >= 3 else 'fail'))

# ---------- option: darker track (any token as a track), against every stop of every current fill
print('\nDARKER-TRACK OPTION: any light token as the track; ratio of each CURRENT fill stop on it (3:1 needed)')
allstops = [(f, s) for f, ss in FILLS.items() for s in ss]
trk = []
for r in rows:
    rs = {f: round(min(ratio(s, r['hex']) for s in FILLS[f]), 2) for f in FILLS}
    trk.append({'token': r['token'], 'hex': r['hex'], 'per_fill_lowest': rs, 'min_all': min(rs.values()),
                'clears_all_four': min(rs.values()) >= 3, 'clears_cmy': min(rs[f] for f in ('cyan', 'magenta', 'yellow')) >= 3})
res['tracks'] = trk
print('  control: the current track %s lowest per fill %s' % (TRACK, {f: round(min(ratio(s, TRACK) for s in FILLS[f]), 2) for f in FILLS}))
for t in sorted(trk, key=lambda t: -t['min_all'])[:12]:
    print('   %-32s %s min over all 8 stops %.2f  per fill %s' % (t['token'], t['hex'], t['min_all'], t['per_fill_lowest']))
print('  tokens clearing 3:1 for ALL FOUR fills: %s' % [t['token'] for t in trk if t['clears_all_four']])
print('  tokens clearing 3:1 for cyan, magenta and yellow (black not required): %s' % [(t['token'], t['per_fill_lowest']['black']) for t in trk if t['clears_cmy']])

# ---------- option: an outline
print('\nOUTLINE OPTION: a 1px boundary token; ratio against the track and against the grounds it touches (3:1 needed)')
out = []
for r in rows:
    if r['kind'] == 'ground': continue
    ok = r['vs_track'] >= 3 and r['vs_card'] >= 3
    out.append({'token': r['token'], 'hex': r['hex'], 'vs_track': r['vs_track'], 'vs_card': r['vs_card'], 'vs_page': r['vs_page'], 'clears': ok})
res['outline'] = out
for o in sorted(out, key=lambda o: o['vs_track']):
    if o['clears']:
        print('   %-32s %s track %5.2f card %5.2f page %5.2f' % (o['token'], o['hex'], o['vs_track'], o['vs_card'], o['vs_page']))
dk_strong = '#6f6f6f'
print('  (dark-only token --nx-border-strong %s: on the dark track %s %.2f, on the dark card %.2f; not a light token)' % (dk_strong, dtrack, ratio(dk_strong, dtrack), ratio(dk_strong, DARK['surface-card'])))
json.dump(res, open(os.path.join(D, 'cand.json'), 'w'), indent=1)
print('\nwrote cand.json')
```
```javascript FILE: xcheck.js
// xcheck.js <r2 dir>: cross-checks cand.py's ratios against the PROJECT'S OWN helper (__tests__/helpers/dom.js lines 151-167,
// extracted by line range and evaluated; no jest, no server). Prints the max absolute difference over every (token, track) pair
// and over the current fill stops; control: a deliberately perturbed ratio must exceed the tolerance.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const D = process.argv[2];
const lines = fs.readFileSync(path.join(D, 'dom.js'), 'utf8').split('\n');
const src = lines.slice(150, 167).join('\n');   // lines 151-168 (1-based)
if (!/function relativeLuminance/.test(src) || !/function contrastRatio/.test(src)) { console.log('EXTRACT FAILED'); process.exit(2); }
const ctx = {}; vm.createContext(ctx); vm.runInContext(src + '\nthis.cr = contrastRatio;', ctx);
const rgb = (h) => ({ r: parseInt(h.slice(1, 3), 16), g: parseInt(h.slice(3, 5), 16), b: parseInt(h.slice(5, 7), 16) });
const c = JSON.parse(fs.readFileSync(path.join(D, 'cand.json'), 'utf8'));
let max = 0, n = 0;
for (const t of c.all_tokens) {
    const d = Math.abs(ctx.cr(rgb(t.hex), rgb(c.track)) - t.vs_track); max = Math.max(max, d); n++;
}
for (const f of Object.values(c.controls.fills)) f.stops.forEach((s, i) => { const d = Math.abs(ctx.cr(rgb(s), rgb(c.track)) - f.ratios[i]); max = Math.max(max, d); n++; });
console.log('pairs', n, 'max abs diff (python rounded to 2dp vs project helper)', max.toFixed(5));
console.log('PASS if max <= 0.005:', max <= 0.005);
const bad = Math.abs(ctx.cr(rgb('#00bcd4'), rgb(c.track)) - 1.29);
console.log('CONTROL (cyan stop against the yellow figure 1.29) differs by', bad.toFixed(3), 'must exceed 0.005:', bad > 0.005);
```
```python FILE: extra.py
#!/usr/bin/env python3
# extra.py <r2 dir>: (1) the luminance ceiling a colour must sit under to clear 3:1 on the track, and each current stop's luminance;
# (2) the R12 reference ("smallest change that clears", BRAND.md R12, 1% steps toward black) for each current stop, NOT a token and NOT
# a proposal: it shows what a NEW token would minimally be; (3) sha256 and byte size of every source copy.
import sys, os, hashlib, json
D = sys.argv[1]
sys.argv = ['x', D]
exec(open(os.path.join(D, 'cand.py')).read().split('# ---------- tokens.css')[0])   # reuse lum/ratio/hsl (no side effects before this marker)
TRACK = '#e9ecef'
Lt = lum(TRACK)
ceil = (Lt + 0.05) / 3.0 - 0.05
print('track luminance %.4f; a colour clears 3:1 on it only if its relative luminance <= %.4f (control: the track itself %.4f is above it)' % (Lt, ceil, Lt))
FILLS = {'cyan': ('#00bcd4', '#26c6da'), 'magenta': ('#e91e63', '#f06292'), 'yellow': ('#ffc107', '#ffca28')}
out = {}
for f, stops in FILLS.items():
    for s in stops:
        r, g, b = hex2rgb(s)
        step = None
        for k in range(0, 101):
            t = 1 - k / 100.0
            c = '#%02x%02x%02x' % (round(r * t), round(g * t), round(b * t))
            if ratio(c, TRACK) >= 3.0:
                step = (k, c, round(ratio(c, TRACK), 2)); break
        print('  %-8s stop %s luminance %.3f ratio %.2f -> R12-style darkening to 3:1 takes %d%% toward black = %s (%.2f:1)' % (f, s, lum(s), ratio(s, TRACK), step[0], step[1], step[2]))
        out['%s %s' % (f, s)] = step
print('\nSOURCES (sha256 first 16, bytes)')
for n in ('tokens.css', 'BRAND.md', 'index-styles.css', 'dark-mode.css', 'package.json', 'derive-brand-tokens.js', 'dom.js', 'rd349test.js', 'index.js', 'pr240.txt', 'rd1032.txt'):
    b = open(os.path.join(D, n), 'rb').read()
    print('  %-24s %s %d' % (n, hashlib.sha256(b).hexdigest()[:16], len(b)))
```
```python FILE: gen_harness.py
#!/usr/bin/env python3
# gen_harness.py <r2 dir>: writes the scratch render pages (html/*.html) and plan.json from cand.json.
# The REAL stylesheets (index-styles.css, dark-mode.css, copied from main 3c3be156) are linked UNCHANGED; every variant is a
# separate override stylesheet (html/variants.css) scoped to a wrapper class, so the "CSS swapped only in the scratch copy".
import json, os, sys, html
TH = 0.03928
def _lum(h):
    h = h.lstrip('#'); v = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    v = [c / 12.92 if c <= TH else ((c + 0.055) / 1.055) ** 2.4 for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def ratio(a, b):
    la, lb = _lum(a), _lum(b); hi, lo = (la, lb) if la >= lb else (lb, la)
    return (hi + 0.05) / (lo + 0.05)
D = sys.argv[1]
c = json.load(open(os.path.join(D, 'cand.json')))
OUT = os.path.join(D, 'html'); os.makedirs(OUT, exist_ok=True)
TRACK = c['track']

# rendered candidates: in-window, passes 3:1, and not excluded by a stated rule
EXCL_NAME = ('-emphasis', '-subtle')
def excluded(r):
    if r['kind'] == 'ground': return 'ground token'
    if any(r['token'].endswith(s) for s in EXCL_NAME): return 'notice token (BRAND.md section 8 rule 4: only on its own notice ground)'
    if r['token'] in ('--nx-chrome-navy-text', '--nx-chrome-white-text', '--nx-chrome-navy-heading'): return 'sidebar text token'
    return None
ALIAS_OF = {'--nx-role-executive': '--nx-activity-print', '--nx-role-print-ops': '--nx-activity-print', '--nx-role-end-user': '--nx-activity-scan',
            '--nx-chrome-white-accent': '--nx-brand-chrome'}
plan = {'track': TRACK, 'sets': {}}
variants_css = []
fills = c['controls']['fills']
for hue in ('cyan', 'magenta', 'yellow'):
    rend, skipped = [], []
    for r in c['family'][hue]:
        if not r['pass3']: continue
        why = excluded(r)
        if r['token'] in ALIAS_OF: why = 'alias of ' + ALIAS_OF[r['token']] + ' (same hex)'
        if why: skipped.append({'token': r['token'], 'hex': r['hex'], 'why': why}); continue
        rend.append(r)
    plan['sets'][hue] = {'rendered': rend, 'skipped': skipped}
    for r in rend:
        cls = 'v-%s-%s' % (hue, r['token'][5:])
        variants_css.append('body:not(.dark-mode) .%s .consumable-fill.%s { background: %s; }' % (cls, hue, r['hex']))
        variants_css.append('body.dark-mode .%s .consumable-fill.%s { background: %s; }' % ('vd' + cls[1:], hue, r['hex']))   # what dark mode shows if ONLY the light rule is edited (dark-mode.css has no cyan/magenta/yellow rule, so it inherits)
# non-colour options
navy = [t for t in c['tracks'] if t['token'] == '--nx-chrome-navy'][0]
variants_css.append('body:not(.dark-mode) .v-track-navy .consumable-bar { background: %s; }' % navy['hex'])
tm = [o for o in c['outline'] if o['token'] == '--nx-text-muted'][0]
variants_css.append('body:not(.dark-mode) .v-outline-bar .consumable-bar { border: 1px solid %s; }' % tm['hex'])
variants_css.append('body:not(.dark-mode) .v-outline-fill .consumable-fill { box-shadow: inset 0 0 0 1px %s; }' % tm['hex'])
plan['navy'] = navy; plan['outline_token'] = tm

HEAD = """<!doctype html><html><head><meta charset="utf-8"><title>%(t)s</title>
<link rel="stylesheet" href="../index-styles.css"><link rel="stylesheet" href="../dark-mode.css"><link rel="stylesheet" href="variants.css">
<style>
/* harness only: Bootstrap reboot box-sizing and a plain table; none of this is product CSS */
*, *::before, *::after { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Arial, sans-serif; margin: 0; padding: 16px; background: %(bg)s; color: %(fg)s; }
table.h { border-collapse: collapse; background: %(card)s; }
table.h td, table.h th { padding: 8px 10px; border-bottom: 1px solid %(bd)s; text-align: left; font-size: 13px; vertical-align: middle; }
table.h td.lab { width: 330px; } table.h td.cell { width: 190px; }
.sw { display: inline-block; width: 12px; height: 12px; vertical-align: -1px; margin-right: 6px; border: 1px solid #888; }
.small { color: %(mut)s; font-size: 11px; }
</style></head><body class="%(bc)s"><h3 style="margin:0 0 8px 0;font-size:14px">%(t)s</h3>"""
def head(t, dark=False):
    return HEAD % {'t': t, 'bc': 'dark-mode' if dark else '', 'bg': '#121212' if dark else '#f8f9fa', 'fg': '#dedede' if dark else '#333333',
                   'card': '#1c1c1c' if dark else '#ffffff', 'bd': '#313131' if dark else '#dee2e6', 'mut': '#8c8c8c' if dark else '#6c757d'}
def cell(color, pct):
    b = int(round(pct / 5.0) * 5)
    return ('<td class="cell"><div class="consumable-cell"><div class="consumable-bar"><div class="consumable-fill %s tw-%d"></div>'
            '<span class="consumable-text">%d%%</span></div></div></td>') % (color, b, pct)
PCTS = (25, 55, 85)
def row(label, wrapper, color, sub=''):
    return '<tr class="%s" data-color="%s"><td class="lab">%s<div class="small">%s</div></td>%s</tr>' % (
        wrapper, color, label, sub, ''.join(cell(color, p) for p in PCTS))
def table(rows, hdr='fill at 25%, 55%, 85%'):
    return '<table class="h" id="set"><tr><th>variant</th><th colspan="3">%s</th></tr>%s</table>' % (hdr, ''.join(rows))
def sw(hexv): return '<span class="sw" style="background:%s"></span>' % hexv
pages = {}
# 0: current, all four fills, light and dark control
rows = [row('current ' + f, 'cur', f, 'lowest stop %.2f:1 on %s' % (fills[f]['lowest'], TRACK)) for f in ('black', 'cyan', 'magenta', 'yellow')]
pages['00_current_light'] = head('Current fills, light mode (before)') + table(rows) + '</body></html>'
d = c['dark']
rows = [row('current ' + f, 'cur', f, 'lowest stop %.2f:1 on %s' % (d[f]['lowest'], '#262626')) for f in ('black', 'cyan', 'magenta', 'yellow')]
pages['01_current_dark_control'] = head('Current fills, dark mode (control, unchanged by any option)', True) + table(rows) + '</body></html>'
for hue in ('cyan', 'magenta', 'yellow'):
    rows = [row('current ' + hue, 'cur', hue, '%s lowest stop %.2f:1' % (' / '.join(fills[hue]['stops']), fills[hue]['lowest']))]
    for r in plan['sets'][hue]['rendered']:
        cls = 'v-%s-%s' % (hue, r['token'][5:])
        rows.append(row(sw(r['hex']) + '%s %s' % (r['token'], r['hex']), cls, hue, 'candidate: %.2f:1 on the track, flat fill' % r['vs_track']))
    pages['1%d_%s_candidates_light' % ('cyan magenta yellow'.split().index(hue), hue)] = head('%s fill: current and candidates, light mode' % hue) + table(rows) + '</body></html>'
    for r in plan['sets'][hue]['rendered']:
        cls = 'v-%s-%s' % (hue, r['token'][5:])
        pn = '3%d_pair_%s_%s' % ('cyan magenta yellow'.split().index(hue), hue, r['token'][5:])
        prow = [row('current ' + hue, 'cur', hue, 'lowest stop %.2f:1' % fills[hue]['lowest']),
                row(sw(r['hex']) + '%s %s' % (r['token'], r['hex']), cls, hue, 'candidate: %.2f:1 on the track, flat fill' % r['vs_track'])]
        pages[pn] = head('%s: current against %s' % (hue, r['token'])) + table(prow) + '</body></html>'
        plan.setdefault('pairs', {})[hue + '/' + r['token']] = pn
rows = [row('current ' + h, 'cur', h, 'dark track #262626; lowest stop %.2f:1' % d[h]['lowest']) for h in ('cyan', 'magenta', 'yellow')]
for hue in ('cyan', 'magenta', 'yellow'):
    for r in plan['sets'][hue]['rendered']:
        cls = 'vd-%s-%s' % (hue, r['token'][5:])
        rows.append(row(sw(r['hex']) + '%s %s' % (r['token'], r['hex']), cls, hue, 'dark mode IF only the light rule is edited: %.2f:1 on #262626' % ratio(r['hex'], '#262626')))
pages['02_dark_if_light_rule_edited'] = head('Dark mode if a candidate is written into the light rule only (it is inherited)', True) + table(rows) + '</body></html>'
# non-colour options, all four fills
rows = [row('current ' + f, 'cur', f) for f in ('black', 'cyan', 'magenta', 'yellow')]
pages['20_nc_current'] = head('Non-colour options: current (reference)') + table(rows) + '</body></html>'
rows = [row('darker track ' + navy['token'] + ' ' + navy['hex'] + ' ' + f, 'v-track-navy', f) for f in ('black', 'cyan', 'magenta', 'yellow')]
pages['21_nc_darker_track'] = head('Option: darker track (--nx-chrome-navy), current fills') + table(rows) + '</body></html>'
rows = [row('outline on the bar, 1px ' + tm['token'] + ' ' + tm['hex'] + ' ' + f, 'v-outline-bar', f) for f in ('black', 'cyan', 'magenta', 'yellow')]
pages['22_nc_outline_bar'] = head('Option: 1px outline on the bar, current fills') + table(rows) + '</body></html>'
rows = [row('outline on the fill, 1px inset ' + tm['token'] + ' ' + tm['hex'] + ' ' + f, 'v-outline-fill', f) for f in ('black', 'cyan', 'magenta', 'yellow')]
pages['23_nc_outline_fill'] = head('Option: 1px outline on the fill, current fills') + table(rows) + '</body></html>'
for k, v in pages.items():
    open(os.path.join(OUT, k + '.html'), 'w', encoding='utf8').write(v)
open(os.path.join(OUT, 'variants.css'), 'w', encoding='utf8').write('\n'.join(variants_css) + '\n')
plan['pages'] = sorted(pages)
json.dump(plan, open(os.path.join(D, 'plan.json'), 'w'), indent=1)
print('pages', len(pages)); [print(' ', k) for k in sorted(pages)]
for h in plan['sets']:
    print(h, 'rendered', [r['token'] for r in plan['sets'][h]['rendered']], 'skipped', [(s['token'], s['why']) for s in plan['sets'][h]['skipped']])
```
```javascript FILE: render.js
// render.js <r2 dir> <playwright module dir>: renders each html/*.html with a real Chromium (file:// only, no server, no network),
// writes shots/<page>.png (element #set, deviceScaleFactor 2) and shots/<page>.json (computed styles + boxes per bar).
'use strict';
const fs = require('fs');
const path = require('path');
const D = process.argv[2];
const { chromium } = require(path.join(process.argv[3], '@playwright/test'));
(async () => {
    let browser, label;
    for (const a of [{ label: "Playwright's bundled Chromium", opts: {} }, { label: 'installed Google Chrome (channel chrome)', opts: { channel: 'chrome' } }]) {
        try { browser = await chromium.launch({ headless: true, ...a.opts }); label = a.label; break; } catch (e) { console.log('launch failed:', a.label, String(e.message).split('\n')[0]); }
    }
    if (!browser) { console.log('NO BROWSER'); process.exit(2); }
    console.log('browser:', label, browser.version());
    fs.mkdirSync(path.join(D, 'shots'), { recursive: true });
    const pages = fs.readdirSync(path.join(D, 'html')).filter((f) => f.endsWith('.html')).sort();
    for (const f of pages) {
        const ctx = await browser.newContext({ viewport: { width: 1000, height: 900 }, deviceScaleFactor: 2 });
        const page = await ctx.newPage();
        const reqs = [];
        page.on('request', (r) => { if (!r.url().startsWith('file://')) reqs.push(r.url()); });
        await page.goto('file://' + path.join(D, 'html', f));
        await page.evaluate(() => document.fonts.ready);
        const info = await page.evaluate(() => {
            const out = [];
            document.querySelectorAll('tr[data-color]').forEach((tr) => {
                tr.querySelectorAll('.consumable-bar').forEach((bar) => {
                    const fill = bar.querySelector('.consumable-fill');
                    const txt = bar.querySelector('.consumable-text');
                    const cs = getComputedStyle(fill), bs = getComputedStyle(bar);
                    const r = (e) => { const b = e.getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; };
                    out.push({ wrapper: tr.className, color: tr.dataset.color, fillBg: cs.backgroundColor, fillImg: cs.backgroundImage, shadow: cs.boxShadow,
                              trackBg: bs.backgroundColor, trackBorder: bs.borderTopWidth + ' ' + bs.borderTopStyle + ' ' + bs.borderTopColor,
                              fill: r(fill), bar: r(bar), txt: r(txt), barH: bar.getBoundingClientRect().height, pct: txt.textContent });
                });
            });
            return out;
        });
        const el = await page.$('#set');
        const tableBox = await page.evaluate(() => { const b = document.getElementById('set').getBoundingClientRect(); return [b.left, b.top, b.width, b.height]; });
        await el.screenshot({ path: path.join(D, 'shots', f.replace('.html', '.png')) });
        fs.mkdirSync(path.join(D, 'shots', 'rows'), { recursive: true });
        const rowfiles = [];
        const trs = await page.$$('tr[data-color]');
        for (let i = 0; i < trs.length; i++) {
            const wr = await trs[i].getAttribute('class'); const col = await trs[i].getAttribute('data-color');
            const rf = f.replace('.html', '') + '__' + String(i).padStart(2, '0') + '__' + wr + '__' + col + '.png';
            await trs[i].screenshot({ path: path.join(D, 'shots', 'rows', rf) });
            rowfiles.push({ i, wrapper: wr, color: col, file: 'rows/' + rf });
        }
        fs.writeFileSync(path.join(D, 'shots', f.replace('.html', '.json')), JSON.stringify({ page: f, nonFileRequests: reqs, tableBox, rowfiles, bars: info }, null, 1));
        console.log(f, 'bars', info.length, 'non-file requests', reqs.length);
        await ctx.close();
    }
    await browser.close();
})().catch((e) => { console.log('ERR', e); process.exit(1); });
```
```python FILE: pixel.py
#!/usr/bin/env python3
# pixel.py <work dir>: reads each shots/*.png (stdlib PNG decoder, 8-bit non-interlaced) with its sibling .json (element boxes from the
# browser), samples the FILL and TRACK pixel of every bar and compares (1) the browser's computed fill colour with the plan's hex for flat
# candidates, (2) the sampled pixel with the expected colour, (3) the ratio measured from the pixels with the program's ratio.
# Three controls follow the table: a wrong expectation must differ, and a sample off the fill must not equal the fill colour.
import json, os, sys, struct, zlib, re
D = sys.argv[1]
TH = 0.03928
S = 2.0   # deviceScaleFactor of render.js

def lum(rgb):
    def ch(v):
        c = v / 255.0
        return c / 12.92 if c <= TH else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])

def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = (la, lb) if la >= lb else (lb, la)
    return (hi + 0.05) / (lo + 0.05)

def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def png(path):
    b = open(path, 'rb').read()
    assert b[:8] == b'\x89PNG\r\n\x1a\n'
    p, idat, w, h, ct = 8, b'', None, None, None
    while p < len(b):
        n, t = struct.unpack('>I4s', b[p:p + 8])
        d = b[p + 8:p + 8 + n]
        p += 12 + n
        if t == b'IHDR':
            w, h, bd, ct, _, _, il = struct.unpack('>IIBBBBB', d)
            assert bd == 8 and il == 0 and ct in (2, 6), (bd, ct, il)
        elif t == b'IDAT':
            idat += d
    bpp = 4 if ct == 6 else 3
    raw = zlib.decompress(idat)
    stride = w * bpp
    rows, prev, q = [], bytearray(stride), 0
    for y in range(h):
        f = raw[q]
        line = bytearray(raw[q + 1:q + 1 + stride])
        q += 1 + stride
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            up = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1: line[i] = (line[i] + a) & 255
            elif f == 2: line[i] = (line[i] + up) & 255
            elif f == 3: line[i] = (line[i] + ((a + up) >> 1)) & 255
            elif f == 4:
                pa, pb, pc = abs(up - c), abs(a - c), abs(a + up - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (up if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        rows.append(line)
        prev = line
    def px(x, y):
        r = rows[y]
        return (r[x * bpp], r[x * bpp + 1], r[x * bpp + 2])
    return w, h, px

plan = json.load(open(os.path.join(D, 'plan.json')))
cand = json.load(open(os.path.join(D, 'cand.json')))
FILLS = cand['controls']['fills']
hexof = {}
for hue, s in plan['sets'].items():
    for r in s['rendered']:
        hexof['v-%s-%s' % (hue, r['token'][5:])] = r['hex']
        hexof['vd-%s-%s' % (hue, r['token'][5:])] = r['hex']
fails, out = 0, []
for f in sorted(x for x in os.listdir(os.path.join(D, 'shots')) if x.endswith('.json')):
    j = json.load(open(os.path.join(D, 'shots', f)))
    w, h, px = png(os.path.join(D, 'shots', f.replace('.json', '.png')))
    left0, top0 = j['tableBox'][0], j['tableBox'][1]
    dark = f.startswith(('01_', '02_'))
    def at(x, y):
        return px(int(round((x - left0) * S)), int(round((y - top0) * S)))
    for b in j['bars']:
        fx, fy, fw, fh = b['fill']; bx, by, bw, bh = b['bar']; tx, ty, tw, th = b['txt']
        wr, col = b['wrapper'], b['color']
        cy = by + bh / 2.0
        exp_track = hx(plan['navy']['hex']) if wr == 'v-track-navy' else (hx('#262626') if dark else hx(plan['track']))
        trk = at(bx + bw - 14, cy)
        left = at(fx + 12, cy - 6.0)           # left of the label chip
        rx = fx + fw - 12                      # right sample only where the chip does not cover it
        right = at(rx, cy - 6.0) if (fw > 60 and not (tx - 3 <= rx <= tx + tw + 3)) else None
        flat = hexof.get(wr)
        if dark and col == 'black':
            flat = '#8c8c8c'                   # dark-mode.css: body.dark-mode .consumable-fill.black is flat
        ok, notes = True, []
        if flat:
            ok &= (left == hx(flat)); notes.append('fill px %s exp %s' % (left, hx(flat)))
            m = re.match(r'rgb\((\d+), (\d+), (\d+)\)', b['fillBg'])
            ok &= (tuple(int(v) for v in m.groups()) == hx(flat)); notes.append('computed %s' % b['fillBg'])
        ok &= (trk == exp_track); notes.append('track px %s exp %s' % (trk, exp_track))
        mr = ratio(left, trk)
        if flat:
            pr = ratio(hx(flat), exp_track)
            ok &= abs(mr - pr) < 0.01; notes.append('pixel ratio %.2f program %.2f' % (mr, pr))
        elif col in FILLS and right:
            lo, hi = sorted((ratio(hx(FILLS[col]['stops'][0]), exp_track), ratio(hx(FILLS[col]['stops'][1]), exp_track)))
            mr2 = ratio(right, exp_track)
            ok &= (lo - 0.05 <= mr <= hi + 0.05) and (lo - 0.05 <= mr2 <= hi + 0.05)
            notes.append('gradient pixel ratios %.2f left %.2f right within stops %.2f..%.2f' % (mr, mr2, lo, hi))
        out.append((f.replace('.json', ''), wr, col, b['pct'], 'PASS' if ok else 'FAIL', '; '.join(notes)))
        fails += 0 if ok else 1
for r in out:
    print(' | '.join(str(x) for x in r))
nreq = sum(len(json.load(open(os.path.join(D, 'shots', f)))['nonFileRequests']) for f in os.listdir(os.path.join(D, 'shots')) if f.endswith('.json'))
print('\nrows %d, FAIL %d, non-file requests %d' % (len(out), fails, nreq))
# controls, on the brand-chrome row of the cyan page
page = [x for x in os.listdir(os.path.join(D, 'shots')) if x.startswith('10_cyan') and x.endswith('.json')][0]
j = json.load(open(os.path.join(D, 'shots', page)))
w, h, px = png(os.path.join(D, 'shots', page.replace('.json', '.png')))
tb = j['tableBox']
b = [x for x in j['bars'] if x['wrapper'] == 'v-cyan-brand-chrome'][0]
fx = b['fill'][0]; cy = b['bar'][1] + b['bar'][3] / 2.0
good = px(int(round((fx + 12 - tb[0]) * S)), int(round((cy - 6 - tb[1]) * S)))
off = px(int(round((b['bar'][0] + b['bar'][2] - 14 - tb[0]) * S)), int(round((cy - tb[1]) * S)))
print('CONTROL 1: brand-chrome fill sample %s equals the expected hex 00719f: %s (must be True)' % (good, good == hx('#00719f')))
print('CONTROL 2: a wrong expectation 00719e must NOT match: %s (must be True)' % (good != hx('#00719e')))
print('CONTROL 3: a sample off the fill is %s and must NOT equal the fill colour: %s (must be True)' % (off, off != hx('#00719f')))
sys.exit(1 if fails else 0)
```
```python FILE: mkdoc.py
#!/usr/bin/env python3
# mkdoc.py <work dir> <out md path> <BASE sha40>: writes the RD-1032 options document (Markdown, BLUF form) from cand.json, plan.json and
# the per-row screenshots of shots/. Every figure in a table comes from those files; the prose is frozen here (the coordinator's text).
# Image paths are written ABSOLUTE (md2pdf resolves relative to its cwd, and no cd is allowed).
import json, os, sys
D, OUT, BASE = sys.argv[1], sys.argv[2], sys.argv[3]
c = json.load(open(os.path.join(D, 'cand.json'))); plan = json.load(open(os.path.join(D, 'plan.json')))
SH = os.path.join(D, 'shots')
TH = 0.03928
def lum(h):
    h = h.lstrip('#'); v = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    v = [x / 12.92 if x <= TH else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = (la, lb) if la >= lb else (lb, la)
    return (hi + 0.05) / (lo + 0.05)
TRACK = c['track']; ceil = (lum(TRACK) + 0.05) / 3.0 - 0.05
F = c['controls']['fills']; DK = c['dark']
def rowimg(page, wrapper, color=None):
    j = json.load(open(os.path.join(SH, page + '.json')))
    for r in j['rowfiles']:
        if r['wrapper'] == wrapper and (color is None or r['color'] == color):
            return '![](%s)' % os.path.join(SH, r['file'])
    raise SystemExit('no row image for %s %s' % (page, wrapper))
def img(name): return '<img src="%s" style="width:100%%; border:1px solid #c9d3e0">' % os.path.join(SH, name)
L = []; A = L.append
A('# RD-1032: options for the light-mode toner fills (cyan, magenta, yellow)')
A('')
A('Prepared for the product owner by the coordinator seat. Colour choices are yours; the candidates and the recommendation below are the coordinator\'s. Nothing has been built, committed or pushed. Measured against NexusAI main `%s`, 23 Nov 2026.' % BASE)
A('')
A('## BLUF')
A('')
A('- **The problem.** On the light track `%s` (`--nx-surface-raised`) the lowest stop of each toner fill reads black %.2f, cyan %.2f, magenta %.2f, yellow %.2f to 1. The brand rule for a bar (R8, WCAG 1.4.11) is 3 to 1. Dark mode already meets it (lowest %.2f, %.2f, %.2f, %.2f after the pull request that fixed dark). Black is fine in light.' % (
    TRACK, F['black']['lowest'], F['cyan']['lowest'], F['magenta']['lowest'], F['yellow']['lowest'], DK['black']['lowest'], DK['cyan']['lowest'], DK['magenta']['lowest'], DK['yellow']['lowest']))
A('- **Brand tokens do clear 3 to 1 in every hue, but not in the colour you see today.** A colour clears 3 to 1 on this track only if its relative luminance is at most %.3f; the current stops sit at %.2f to %.2f (cyan), %.2f to %.2f (magenta) and %.2f to %.2f (yellow). So every passing cyan is a teal or blue, the passing magenta is a rose red, and the passing yellow is an amber or brown. That is physics, not a lack of search. If you want the toner colours to stay as they are, the alternative is a non-colour fix (an outline), shown in section 5.' % (
    ceil, lum(F['cyan']['stops'][0]), lum(F['cyan']['stops'][1]), lum(F['magenta']['stops'][0]), lum(F['magenta']['stops'][1]), lum(F['yellow']['stops'][0]), lum(F['yellow']['stops'][1])))
nclear = {h: len(plan['sets'][h]['rendered']) for h in plan['sets']}
A('- **What you are choosing between:** (a) one brand token per hue from the candidate tables below (cyan %d, magenta %d, yellow %d are shown as screenshots; more passed and are listed with the reason they are not shown), (b) a 1px outline in `%s` on the fill or the bar, which keeps today\'s colours, or (c) a new brand token, which BRAND.md section 8 rule 1 says is your decision, not an agent\'s.' % (nclear['cyan'], nclear['magenta'], nclear['yellow'], plan['outline_token']['token']))
A('- **A consequence you should know about before picking:** dark mode has no cyan, magenta or yellow rule, so it inherits the light rule. Editing the light rule alone would change dark mode, and several candidates would then fall below 3 to 1 there (section 6). The build must keep the new value light-only; that is a build detail, but it is why the dark control screenshot is in this document.')
A('- **Coordinator\'s recommendation (not yours until you pick it):** see section 8. In short, the outline on the fill if you want the toner colours to keep their identity; otherwise the three graphic-kind tokens named there.')
A('')
A('## 1. What is measured today')
A('')
A('Instrument: WCAG 2.x relative luminance (the project\'s own `__tests__/helpers/dom.js` lines 151 to 167, same formula, cross-checked by program), contrast of each gradient stop against the track `%s`. The review\'s figures in the ticket are reproduced first, as a control.' % TRACK)
A('')
A('| fill | stops | ratio per stop | lowest | ticket / review figure | reproduced |')
A('|---|---|---|---|---|---|')
for f in ('black', 'cyan', 'magenta', 'yellow'):
    x = F[f]; A('| %s | `%s` and `%s` | %.2f and %.2f | **%.2f** | %.2f | %s |' % (f, x['stops'][0], x['stops'][1], x['ratios'][0], x['ratios'][1], x['lowest'], x['review'], 'yes' if x['match'] else 'NO'))
A('')
A('Current fills in light mode (before), and dark mode (control, unchanged by every option here):')
A('')
A('Light (before):')
A('')
A(img('00_current_light.png'))
A('')
A('Dark (control):')
A('')
A(img('01_current_dark_control.png'))
A('')
A('Rendered locally by a real Chromium from the real `index-styles.css` and `dark-mode.css` of main, with the real toner markup; not the live page.')
A('')
n = 2
for hue in ('cyan', 'magenta', 'yellow'):
    page = {'cyan': '10_cyan_candidates_light', 'magenta': '11_magenta_candidates_light', 'yellow': '12_yellow_candidates_light'}[hue]
    A('## %d. %s fill (hue %.0f degrees; current lowest stop %.2f)' % (n, hue.capitalize(), c['fill_hue'][hue], F[hue]['lowest'])); n += 1
    A('')
    A('Rule for "same hue family": a chromatic token (HSL saturation 0.20 or more) whose hue is within 30 degrees of the fill\'s mean hue. Every such token is listed; ratio is on the track `%s`; "own stops" is the candidate against the fill\'s two current stops (how far the colour moves); "dark if inherited" is the ratio on the dark track `#262626` if only the light rule were edited. Kind and grounds are from `scripts/derive-brand-tokens.js` (R8); "pinned" is the count the brand gate pins for that value (R7).' % TRACK)
    A('')
    A('| token, hex | hue | on track | own stops | dark if inherited | kind; raised named | pinned | status |')
    A('|---|---|---|---|---|---|---|---|')
    rend = {r['token'] for r in plan['sets'][hue]['rendered']}
    skip = {s['token']: s['why'] for s in plan['sets'][hue]['skipped']}
    for r in c['family'][hue]:
        st = 'shown below' if r['token'] in rend else (('passes, not shown: ' + skip[r['token']]) if r['token'] in skip else 'fails 3:1')
        kg = '%s; %s' % (r['kind'] or 'older token, no R8 kind', 'yes' if 'surface-raised' in r['grounds'] else 'no')
        A('| `%s` `%s` | %.0f | **%.2f** %s | %.2f / %.2f | %.2f | %s | %s | %s |' % (
            r['token'], r['hex'], r['hue'], r['vs_track'], 'pass' if r['pass3'] else 'fail', r['vs_stops'][0], r['vs_stops'][1], r['vs_dark_track_if_inherited'], kg, ('x%d' % r['pinned']) if r['pinned'] else 'no', st))
    A('')
    if hue == 'yellow':
        A('No token is a bright yellow. The brightest passing token in the window is `--nx-role-partner-tech` (`#b57a13`), an amber; `--nx-warning` (`#ff8c00`) reads 1.97 and fails.')
        A('')
    if hue == 'magenta':
        A('No token is magenta or pink. The window holds red and rose tokens only. `--nx-danger` is the error colour, so a toner bar in it would read as an alarm; that is a meaning clash, not a measurement.')
        A('')
    A('Current (top) against each candidate (a flat fill, since a token is one colour; the gradient goes):')
    A('')
    A(img(page + '.png'))
    A('')
    A('Each candidate beside the current fill (top row current, second row candidate):')
    A('')
    for r in plan['sets'][hue]['rendered']:
        A('**%s `%s`, %.2f to 1**' % (r['token'], r['hex'], r['vs_track']))
        A('')
        A(img(plan['pairs'][hue + '/' + r['token']] + '.png'))
        A('')
A('## %d. If you would rather not change the colours: the two non-colour options (the ticket names both)' % n); n += 1
A('')
tr = plan['navy']; ot = plan['outline_token']
A('**Option N1: a darker track.** Every light token tried as the track, against every stop of every current fill (a fill must clear 3 to 1 on it). Result by program: tokens that clear 3 to 1 for all four fills: **%s**. The only token that clears for cyan, magenta and yellow is `%s` (`%s`, the navy sidebar ground), and it reads %.2f for the black fill, so the black bar all but disappears. The dark fix in the earlier pull request solved this by also lightening the black fill to `#8c8c8c`; no light token pair does the equivalent here. **A darker track does not work with today\'s fills and the existing tokens.** Screenshot of the navy track for the record:' % (
    ', '.join('`%s`' % t['token'] for t in c['tracks'] if t['clears_all_four']) or 'none', tr['token'], tr['hex'], tr['per_fill_lowest']['black']))
A('')
A(img('21_nc_darker_track.png'))
A('')
A('**Option N2: an outline in a token that clears 3 to 1 against the track and against the card ground.** Tokens clearing both: %d (listed in the data file). The plainest is `%s` (`%s`: %.2f on the track, %.2f on the card, %.2f on the page), a token already used for secondary text. Two placements, both 1px, both drawn on the real markup:' % (
    sum(1 for o in c['outline'] if o['clears']), ot['token'], ot['hex'], ot['vs_track'], ot['vs_card'], ot['vs_page']))
A('')
A('N2a, outline on the whole bar:')
A('')
A(img('22_nc_outline_bar.png'))
A('')
A('N2b, outline on the fill:')
A('')
A(img('23_nc_outline_fill.png'))
A('')
A('N2b draws the edge of the fill itself, which is the boundary the 3 to 1 rule is about (the fill against the track); N2a draws the extent of the bar and does not by itself separate a pale fill from the track. Whether either satisfies WCAG 1.4.11 for you is a reading, not a measurement: the ratios above are measured, an accessibility audit verdict is not.')
A('')
A('## %d. What editing the light rule alone does to dark mode' % n); n += 1
A('')
A('`dark-mode.css` has a rule for the black fill only (flat `#8c8c8c`); cyan, magenta and yellow in dark are the light gradients, inherited. So a candidate written into `.consumable-fill.cyan` in the light sheet reaches dark mode too. The rendering below is that case, measured on the dark track `#262626`:')
A('')
A(img('02_dark_if_light_rule_edited.png'))
A('')
low = sorted((r['token'], r['vs_dark_track_if_inherited'], h) for h in plan['sets'] for r in plan['sets'][h]['rendered'] if r['vs_dark_track_if_inherited'] < 3)
A('Rendered candidates that would fall below 3 to 1 in dark if inherited: %s. The build therefore scopes the new value to light mode (or states a dark value), whichever you pick; either keeps the dark fills as they are, as the ruling says.' % (', '.join('`%s` %.2f' % (t, v) for t, v, h in low) or 'none'))
A('')
A('## %d. What each choice costs in the brand gate (for the build, not for the choosing)' % n); n += 1
A('')
A('- **Role accents** (`--nx-role-*`) are kind graphic with grounds card and page only. The toner track is `--nx-surface-raised`, which none of them names, so adopting one means adding that ground to its entry in `scripts/derive-brand-tokens.js` (R8: a token is correct only on the grounds it names).')
A('- **Tokens with a pinned count** (the 20 measured light values, e.g. `--nx-danger` x13, `--nx-brand-blue-dark` x21, `--nx-warning-emphasis` x37, `--nx-text-muted` x70): one more use moves the pin by one in the generator and in the BRAND.md table, as the earlier pull request did for `--nx-text-strong`. Tokens added by the shell ruling carry no pinned count.')
A('- **Notice tokens** (`-emphasis`, `-subtle`) are legal only on their own notice ground (BRAND.md section 8 rule 4), so they are listed but not shown or recommended.')
A('- **The cartridge table\'s colour dots** (`static/js/index.js` line with `SUPPLY_COLOURS`) keep today\'s pure toner colours (`#2c3e50`, `#00bcd4`, `#e91e63`, `#ffc107`). A recoloured bar would no longer match its own dot; the outline option does not have that problem.')
A('')
A('## %d. Coordinator\'s recommendation (the coordinator\'s, not yours and not an audit)' % n); n += 1
A('')
A('1. **First choice: N2b, a 1px outline on the fill in `%s`.** It keeps every toner colour as it is (so the bars still match their dots and the toner they stand for), changes no hue, needs no new token and no ground added, and its boundary clears 3 to 1 on the track (%.2f). It moves one pinned count. Its weakness is the reading in section 5: a pale fill with a dark edge is perceivable by its outline, but a strict auditor may still want the fill itself to clear.' % (ot['token'], ot['vs_track']))
A('2. **If you want the colour itself to clear:** cyan `--nx-role-partner-manager` (`#0a8793`, hue 185 against the fill\'s 187, %.2f on the track), magenta `--nx-role-security` (`#b44752`, a rose red, %.2f), yellow `--nx-role-partner-tech` (`#b57a13`, an amber, %.2f). They are the nearest-hue tokens that are graphic kind, have no pinned count and carry no alarm meaning. Yellow\'s margin (%.2f against 3.00) is the thinnest; `--nx-activity-fax` (`#956300`, %.2f) is the sturdier amber. Each needs `--nx-surface-raised` added to its grounds, and the light-only scoping of section 6.' % tuple(
    [r['vs_track'] for r in c['family']['cyan'] if r['token'] == '--nx-role-partner-manager'] + [r['vs_track'] for r in c['family']['magenta'] if r['token'] == '--nx-role-security'] + [r['vs_track'] for r in c['family']['yellow'] if r['token'] == '--nx-role-partner-tech'] * 2 + [r['vs_track'] for r in c['family']['yellow'] if r['token'] == '--nx-activity-fax']))
A('3. **A mix is possible** (for example the outline for all, or tokens for cyan only); the three hues are independent.')
A('4. **Not recommended:** a darker track (section 5, N1); `--nx-danger` for magenta (alarm meaning); any notice token.')
A('')
A('**Who decided what.** The choice of colour or outline is the product owner\'s. The candidate list, the hue rule, the ranking and this recommendation are the coordinator\'s.')
A('')
A('## %d. What is NOT measured' % n); n += 1
A('')
A('- The live page, the hosted site, other viewports, Linux, any real printer data; the renders use the real stylesheets of main with sample values and a minimal table, not the page, and not the real Bootstrap file.')
A('- Hover and striped-row states, forced-colours or high-contrast mode, colour-blind simulation, print output.')
A('- Whether an outline satisfies WCAG 1.4.11 in an audit (a reading, not run).')
A('- The tests that a build would add or change; the dark-mode rule shape; the brand gate\'s own reaction to an edited grounds list (not run: nothing was built).')
A('- The other places the toner colours appear beyond the bar and the cartridge dots (not searched for beyond the two named).')
A('')
A('## %d. Method and sources' % n)
A('')
A('Tokens read from `static/css/tokens.css` and kinds, grounds and pinned counts from `scripts/derive-brand-tokens.js` at main `%s`; contrast by WCAG 2.x relative luminance (linear threshold 0.03928, as the project\'s helper), computed by program and cross-checked against the helper\'s own functions; the rendered rows are read back from the PNGs and their measured ratio equals the computed one for every flat candidate (control: a wrong expectation fails). Screenshots by Playwright\'s bundled Chromium from local files only; no server, no network request, nothing hosted.' % BASE)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf8').write('\n'.join(L) + '\n')
print('wrote', OUT, len(L), 'lines')
```
```python FILE: scans.py
#!/usr/bin/env python3
# scans.py <md> <pdf text file> <scanlib file>: the kit's Step 6 checks on the options document, each with a control that must fire.
# The person-name list is READ from line 20 of the project's own scanlib file at run time (never typed here), split on '|', with word
# boundary marks stripped; the pattern is underscore-aware: (?<![A-Za-z])name(?![a-z]).
import re, sys, os
md = open(sys.argv[1], encoding='utf8').read()
txt = open(sys.argv[2], encoding='utf8', errors='replace').read()
line20 = open(sys.argv[3], encoding='utf8').read().split('\n')[19]
body = re.search(r're\.compile\(r"([^"]*)"', line20).group(1)
names = [x.replace('\\b', '') for x in body.split('|') if x.replace('\\b', '').strip()]
NAME = re.compile('(?<![A-Za-z])(' + '|'.join(re.escape(n) for n in names) + ')(?![a-z])', re.I)
BNUM = re.compile(r'B1[5-9][0-9][0-9]|N1[4-9][0-9]|Datasec/NexusAI-', re.I)
CARD = re.compile(r'decision[ _-]queue|REC-REG', re.I)
print('name list read from scanlib line 20: %d names (control: more than 0)' % len(names))
for label, text in (('md', md), ('pdf text', txt)):
    print('%s: names %d, b-numbers %d, decision-queue ids %d' % (label, len(NAME.findall(text)), len(BNUM.findall(text)), len(CARD.findall(text))))
print('control name (a planted _by_<first name>_ must fire): %d' % len(NAME.findall('x _by_' + names[0] + '_ y')))
print('control b-number (planted B1967 and b1967/x): %d %d' % (len(BNUM.findall('B1967')), len(BNUM.findall('Datasec/NexusAI-N166'))))
print('control id (planted decision-queue): %d' % len(CARD.findall('decision-queue')))
cards = [m.start() for m in re.finditer(r'\bcard\b', md, re.I)]
print('word card in md: %d occurrences, each shown with its context (a ground token name or "the card ground" is expected, anything else is a hit):' % len(cards))
for st in cards:
    print('   ...' + md[max(0, st - 30):st + 30].replace('\n', ' ') + '...')
secs = re.split(r'\n## ', md)
def section(name):
    return [x for x in secs if re.match(r'\d+\. ' + name, x)][0]
for name, n in (('Cyan', 22), ('Magenta', 4), ('Yellow', 6)):
    rows = len(re.findall(r'^\| `--nx-', section(name), re.M))
    print('%s section token rows: %d (expected %d) %s' % (name, rows, n, 'OK' if rows == n else 'MISMATCH'))
print('control: one Cyan row removed gives %d' % len(re.findall(r'^\| `--nx-', section('Cyan').replace('| `--nx-chrome-navy`', 'X', 1), re.M)))
paths = re.findall(r'<img src="([^"]+)"', md)
missing = [p for p in paths if not os.path.exists(p)]
print('images referenced %d, missing %d; control: a planted missing path reads missing %s' % (len(paths), len(missing), not os.path.exists('/nonexistent/x.png')))
```

## EXPECTED OUTPUT (copied from the drafter's real runs, never written from the tools' docs)
Lines of `cand.py` that must appear exactly (the drafter's `cand.out`, sha256 first 16 `798511d5c8315c25`, which your run must reproduce when the sources hash equal):
```text FILE: expected-cand-head.txt
INSTRUMENT: WCAG 2.x relative luminance, linear threshold 0.03928 (as __tests__/helpers/dom.js lines 151-167); track #e9ecef = --nx-surface-raised (light)
tokens parsed: light 49, dark 51

CONTROLS (the review's figures at the lowest stop, reproduced)
  black    stops ('#2c3e50', '#34495e') ratios [9.26, 7.83] lowest 7.83 review 7.83 MATCH
  cyan     stops ('#00bcd4', '#26c6da') ratios [1.94, 1.74] lowest 1.74 review 1.74 MATCH
  magenta  stops ('#e91e63', '#f06292') ratios [3.67, 2.58] lowest 2.58 review 2.58 MATCH
  yellow   stops ('#ffc107', '#ffca28') ratios [1.37, 1.29] lowest 1.29 review 1.29 MATCH
  control fires if a figure differs: all four match = True
  negative control (cyan stop vs the yellow figure 1.29 must NOT match): True
  sanity: #000 vs #fff 21.000 (must be 21.000); #fff vs #fff 1.000 (must be 1.000)
```
`xcheck.js` prints, on its last three lines:
```text FILE: expected-xcheck.txt
pairs 57 max abs diff (python rounded to 2dp vs project helper) 0.00494
PASS if max <= 0.005: true
CONTROL (cyan stop against the yellow figure 1.29) differs by 0.647 must exceed 0.005: true
```
`pixel.py` prints on its last four lines (the row count is a count of bars rendered, 222 at BASE with these programs):
```text FILE: expected-pixel-tail.txt
rows 222, FAIL 0, non-file requests 0
CONTROL 1: brand-chrome fill sample (0, 113, 159) equals the expected hex 00719f: True (must be True)
CONTROL 2: a wrong expectation 00719e must NOT match: True (must be True)
CONTROL 3: a sample off the fill is (233, 236, 239) and must NOT equal the fill colour: True (must be True)
```

`scans.py` prints, in full (the drafter's run on the prototype document; the three "card" lines are the card ground and are expected):
```text FILE: expected-scans.txt
name list read from scanlib line 20: 4 names (control: more than 0)
md: names 0, b-numbers 0, decision-queue ids 0
pdf text: names 0, b-numbers 0, decision-queue ids 0
control name (a planted _by_<first name>_ must fire): 1
control b-number (planted B1967 and b1967/x): 1 2
control id (planted decision-queue): 1
word card in md: 3 occurrences, each shown with its context (a ground token name or "the card ground" is expected, anything else is a hit):
   ...nst the track and against the card ground.** Tokens clearing...
   ....95 on the track, 4.69 on the card, 4.45 on the page), a tok...
   ...are kind graphic with grounds card and page only. The toner ...
Cyan section token rows: 22 (expected 22) OK
Magenta section token rows: 4 (expected 4) OK
Yellow section token rows: 6 (expected 6) OK
control: one Cyan row removed gives 21
images referenced 20, missing 0; control: a planted missing path reads missing True
```

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY <one question>`, no other step; each value with a control that can fail; items 1 to 3 before `.tools/b1967/` is created)
1. `/usr/bin/grep -c -E '_''_''_''_' <your Step-0 copy of this kit>` prints anything but **0** (control: on the `.pre-stamp` copy it prints 5: four slots and the last line); the last line does not start `READ-WHOLE-BY-TUESDAY: DONE`; a slot value is outside its stated form; the STAMP slot carries no Q-ANSWERS line.
2. Your seat name is not `Datasec/NexusAI-N166` (`tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'`; control: -t on another pane prints that pane's name), or `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI`.
3. `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1967_STATUS.md`, `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1967_OPTIONS` or `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1967` already exists (name the path; run the check under bash with a control: `.tools/b1931` reads yes).
4. **Nothing of yours collides.** (a) No NexusAI pane other than yours holds a kit whose OWNS block names a path under `.tools/b1967` or `2026-11-23_B1967` (a program over the `OWNS-B19` blocks of the live panes' kits; at drafting the only other pane was `Datasec/NexusAI-N165`, whose OWNS is two tests and its own tools). (b) You do not need the jest lock and you do not take it; if you find yourself about to run jest, `npm`, `node server.js` or a server of any kind, STOP: that is another kit. (c) `gh api user` login (under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`) does not contain "datasec" case-insensitively (count 1, never quote it).
5. **Main moved in a path your sources read:** at Step 1 `gh api -X GET 'repos/datasecau/Reporting_Dashboard_Au/compare/<BASE>...main'` lists, by program over `.files[].filename`, any of the eleven paths of the sources table: STOP naming them (the measurements are at BASE, but a moved source makes the document stale before it is read). A move that touches none of them is noted in STATUS and the work goes on at BASE.
6. A token or key was printed by any tool (say "a value was shown" and STOP). The Jira read uses the credentials by key name inside the program and prints none.
7. A source's sha256 at Step 1 is not the table's (name the file; the commission's re-read rule says re-read at main, so print whether main moved) .
8. A frozen program's expected output at Step 3 to 5 is not the block above, or a step's own control fails.

## HOLDS (the whole run)
1. **Never type `cd`**; absolute single-quoted paths (`!CODING` contains `!`); `/usr/bin/grep -i` with a positive control for every count; never an unquoted word starting with `=`; one simple command per Bash call; never a command in a shell variable expanded unquoted (zsh does not split it); `python3 -I`; `NODE_OPTIONS` unset on every node run (`env -u NODE_OPTIONS`).
2. **Never delete** (quarantine into `<dir>/_quarantine_<date>` and say where). **A guard or hook refusal is a STOP for that action, never a prompt to reach the same end another way** (the drafter met one: `rm` outside the scratchpad was refused and not worked around).
3. **READ-ONLY toward the project, Jira and GitHub:** `gh api -X GET` only; Jira by GET through a program that reads the project's `.env` keys `JIRA_SITE`, `JIRA_EMAIL`, `JIRA_API_TOKEN` by name and prints none; no `az`, ssh, docker; no HTTP to any hosted, demo or production host, not even GET; the browser opens `file://` pages only.
4. **Nothing to any human:** no mail, no Jira write, no message; Tuesday sends the document to the product owner.
5. **No customer-facing word is written into any product file** (none is touched). The document is for the product owner and carries no person's name, no card id and no B-number (Step 6 scans, with controls).
6. **Every number carries its instrument and a control that can fail;** a zero is a suspect until its control fires. The document says "the coordinator's" for candidates and recommendation and "the product owner's" for the choice.
7. **Records-file rule (DRAFTER_RULES):** every file you write is a NEW path inside the new folders; you never open an existing file for writing, and a second run goes to a new name (the programs write only new files: `cand.json`, `plan.json`, `html/*`, `shots/*`, the document).
8. **Context band:** at about 70% context start no new part; at about 75% stop at a safe boundary (files whole, nothing running) and write `1_Project_Definition/Briefs/2026-11-23_B1967_OPTIONS/HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps) with last line `HANDOVER B1967: next <part> <step> | done <parts>`; parts: read, fetch, programs, render, document, scans. This lane is small and is not expected to reach it.
9. **No process is left running:** Chromium is launched and closed by `render.js` itself; at the end `pgrep -fl 'chrom'` lists none of yours (print it; processes of other seats are not yours to stop).

## THE WORK (steps; each step's inputs are produced by an EARLIER step or exist at BASE: the table is in the report)
**Step 0.** `date`. Copy this kit to `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1967_SEAT-N166_nexusai-rd1032-options.md` (the Briefs folder exists; this is a plain copy), `cmp`, sha256, line count; REFUSE 1 to 4. Make `.tools/b1967/` with `frozen/, logs/, _quarantine/` and the evidence folder `<EV>` with `data/, data/shots/` (`mkdir -p`, one folder per call). Write STATUS with first line `B1967 STATUS (placeholder, Step 0 running)` and your AEDT clocks. Read the drafter report whole and the commission's ruling text above; print the report's line count and sha256 prefix into STATUS. Read `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1958_SEAT-N164_nexusai-nx-p-permission-table.md` lines 1 to 12 only (form).
**Step 1 (fetch, read-only).** `date`; Node 24 first on PATH (`export PATH='/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin':"$PATH"`; `node -v` prints `v24.22.2`). REFUSE 4(c). Origin main now: `gh api -X GET 'repos/datasecau/Reporting_Dashboard_Au/commits/main' --jq .sha`; if it is not BASE, REFUSE 5's compare. Fetch each source of the table into `<EV>/data/` under its saved name with the `gh api -X GET ... -H 'Accept: application/vnd.github.raw' > <file>` form above (one call per file; `ref=<BASE>` always), print `wc -lc` and `shasum -a 256` of each and compare with the table (REFUSE 7). The Jira ticket: save the output of a read-only GET of RD-1032 (summary, status, labels, description, comments) by a small program of your own that reads the three `.env` keys by name, into `<EV>/data/rd1032.txt`; it must read 4028 bytes or you explain the difference in STATUS (the ticket may have been commented since; a status other than To Do is a STOP).
**Step 2 (programs).** Extract the seven frozen programs and the three expected-output files by `awk` (the line after the opening fence to the line before the closing fence), twice, `cmp` the pairs; copy the programs into `<EV>/data/` for the run (they find `cand.py` beside them). Print `wc -c` of each. `awk` shape: `awk '/^```python FILE: cand.py$/{f=1;next} f&&/^```$/{exit} f' <kit copy> > .tools/b1967/frozen/cand.py` (and `javascript`, `text` for the others).
**Step 3 (candidates).** `python3 -I <EV>/data/cand.py <EV>/data > .tools/b1967/logs/cand.out`; its sha256 first 16 equals the line in EXPECTED OUTPUT and the head lines match (REFUSE 8); `env -u NODE_OPTIONS node <EV>/data/xcheck.js <EV>/data` prints the expected three lines; `python3 -I <EV>/data/extra.py <EV>/data` (a log, no expected hash). Read the printed token table and the three family blocks and note in STATUS the counts of tokens in each window and the passing ones, by `grep -c` over `cand.out` with a control each.
**Step 4 (render).** `python3 -I <EV>/data/gen_harness.py <EV>/data` must write 21 pages (print `ls <EV>/data/html | wc -l`: it prints 22, the 21 pages and `variants.css`). Then, under `nice -n 10`: `env -u NODE_OPTIONS node <EV>/data/render.js <EV>/data '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1931/clone/node_modules'` (third argument is the folder that holds `@playwright/test`; if it does not exist use the checkout's `2_Project_Files/node_modules`, read-only, and say so). It prints the browser build and, per page, `non-file requests 0`; any other value is a STOP. Then `python3 -I <EV>/data/pixel.py <EV>/data > .tools/b1967/logs/pixel.out`: its last four lines equal the expected tail and its rc is 0. **Look at the pictures**: with the Read tool open `<EV>/data/shots/10_cyan_candidates_light.png`, `11_magenta_candidates_light.png`, `12_yellow_candidates_light.png`, `02_dark_if_light_rule_edited.png`, `22_nc_outline_bar.png` and `23_nc_outline_fill.png`, and say in STATUS in one sentence each what you see (the bars are visible, the label chip is inside the bar, no clipping).
**Step 5 (document).** `python3 -I <EV>/data/mkdoc.py <EV>/data <EV>/RD-1032_options.md <BASE>` (BASE is the sha40), then `bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/md2pdf/md2pdf.sh' <EV>/RD-1032_options.md <EV>/RD-1032_options.pdf` (usage read from its header: `md2pdf.sh <input.md> [output.pdf]`; it needs `pandoc` and Google Chrome; it printed `rendered: ... (10 pages, 1692396 bytes)` at drafting and the page count may differ by a page or two). Render pages with `pdftoppm -r 55 -png <pdf> <EV>/data/pg` and Read at least pages 1, 3 and the last: the BLUF, a candidate table, a screenshot pair and the dark section must show; a picture clipped at the right edge is a STOP for this step (the images are written at 100% width by the program; the drafter's first version was clipped and fixed). The PDF is a rendering of the Markdown, not a second document.
**Step 6 (scans of the document, with controls).** `pdftotext <EV>/RD-1032_options.pdf <EV>/data/pdf.txt`, then `python3 -I <EV>/data/scans.py <EV>/RD-1032_options.md <EV>/data/pdf.txt '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/b1375/scanlib1114.py' > .tools/b1967/logs/scans.out`; its output equals the expected block (names 0, B-numbers 0, ids 0, every control reads at least 1, the Cyan, Magenta and Yellow sections list 22, 4 and 6 token rows, 0 missing images, the three "card" lines are the card ground). The name list is read from the project's own scan file at run time and is never typed into a document. A difference is a STOP naming the line.
**Step 7 (finish).** Print the two folders' file lists and sizes; `pgrep -fl 'chrom'` (HOLD 9); write the STATUS sections (below) and the last line. The deliverable paths for Tuesday: `<EV>/RD-1032_options.md`, `<EV>/RD-1032_options.pdf`, `<EV>/data/shots/`. **You send nothing to anyone.**

## PRIOR WORK (git, gh and Jira GET only; MEASURED-BY-DRAFTER, re-read)
- **Pull request 240 (RD-349 and RD-175, merge `50b7c40cf1a682baffdd3827b77166ec65e746cd`)** did the DARK fills. What it measured and how: the lowest stop of each fill on the dark track `#262626` (black 7.83 on the light track before, 4.50 after with the black fill lightened to `#8c8c8c` = `--nx-text-muted` dark; cyan 6.59, magenta 3.48, yellow 9.28), by a test (`__tests__/rd349-rd175-readable-text-on-its-ground.test.js` cell C5, read at BASE: it reads the two stylesheets and `tokens.css` and uses the project's contrast helper, 3 to 1 as GRAPHIC) and by an independent local render in headless Chromium of the repository's Bootstrap excerpt, no page scripts, sample values. **Its own text lists "In LIGHT mode the cyan, yellow and magenta toner fills read below 3:1 on the light track (1.74, 1.29, 2.58), as before this change; the percentage chip states the value" as NOT changed** and "the e2e contrast suite's allow-list entry for the toner label and its light baselines are now out of date; that suite is not part of the verify". Its chosen dark values were "the coordinator's defaults" with the product owner's recorded outcome naming the result, not the colours. **What this lane keeps:** the same instrument family (the project's own ratio formula, 3 to 1 for a bar), the same render shape (local, real stylesheets, sample values), the dark fills untouched. **What differs:** this lane does not build and does not edit a stylesheet.
- **Jira search (read-only JQL `project = RD AND (text ~ "toner fill" OR text ~ "consumable-fill" OR text ~ "toner bar")`, 11 issues at drafting):** RD-1032 (this), RD-349 and RD-175 (the pull request above, Testing), RD-160 and RD-207 (the brand chrome pair, Testing), RD-85 and RD-56 (pill clipping and width, Testing and Release Ready), RD-67 (the colour swatch dots, Release Ready), RD-332, RD-296 and RD-269 (empty-state and date matters). **None other names the light fills below 3 to 1.** RD-67 matters here: the cartridge table's colour dots are set from `static/js/index.js` (`SUPPLY_COLOURS`) in the pure toner colours, which a recoloured bar would no longer match.
- **The brand guide's rules this lane obeys:** `docs/BRAND.md` section 8 rule 1 (use a token; a gap is a brand decision), rule 4 (a token is only correct on the ground it was derived against; an `-emphasis` token belongs on its own notice ground), R7 (pinned counts) and R8 (kind and grounds) at lines 763 to 790, R12 (the smallest change that clears). **Keep what works:** the dark fills, the black light fill, the label chip, the bar geometry. **A READY without a PRIOR WORK section is returned.**

## THE DOCUMENT (what `mkdoc.py` writes, and what you must check it says)
A BLUF-first Markdown file for the product owner: the problem with the four figures; why brand tokens clear 3 to 1 but not in today's colours (the luminance ceiling 0.245); the choice (a token per hue, an outline, or a new token which is the product owner's brand decision); the dark-mode consequence; per hue the full in-window token table (name, hex, hue, ratio on the track, ratio against the fill's own two stops, ratio on the dark track if inherited, kind and whether the raised ground is named, pinned count, status), the screenshot stack and one before-and-after pair per rendered candidate; the two non-colour options with screenshots; the brand-gate consequences; the coordinator's recommendation (first the outline on the fill, then the three graphic-kind tokens, labelled as the coordinator's and not an audit); what is NOT measured; the method. **The recommendation text is frozen in `mkdoc.py` and is Tuesday's to overrule in the stamp: you copy it, you do not edit it.** If you believe a sentence is wrong against what you measured, say so in STATUS under Corrections and leave the sentence.

## STATUS FILE (the channel)
`/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-23_B1967_STATUS.md`. First line `B1967 STATUS (placeholder, Step 0 running)`. Sections: Questions, BLUF, Step 0, Step 1, Programs, Candidates, Render, Document, Scans, PRIOR WORK, `## READY`, ADDENDA READ, NOT TESTED, Corrections. **The LAST line on finish is exactly one of:** `READY B1967: <sha256 first 16 of RD-1032_options.md>`, or `STOPPED: NEEDS TUESDAY <one question>`. In between: `WORKING: ...`. Poll `ls /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/ | /usr/bin/grep -i -E '^2026-11-2[34]_B1967_(ADDENDUM|ANSWER)'` at every step boundary (control: the same grep with `SEAT-N166` prints this kit, its sidecar and any `.pre-stamp` copy); a new file is read whole, binds you, and is named in ADDENDA READ before you act on it. READY states: the two deliverable paths and sizes, the page count of the PDF, the number of bars rendered and non-file requests, the three controls of `pixel.py`, `NOT TESTED`, and the line `NO FILE OF THE REPOSITORY WAS WRITTEN: <the printed list of the two folders>`.

## NOT TESTED (said so the seat does not claim them)
The live page, the hosted site, other viewports, Linux, hover and striped-row states, forced-colours mode, colour-blind simulation, print output, whether an outline satisfies WCAG 1.4.11 in an audit, the build (nothing is built: the dark-rule shape, the generator's grounds edit and the tests a build adds are for the lane that follows the product owner's pick), and the real Bootstrap file (the harness is a plain table with Bootstrap's `box-sizing` reset).

## STOP RULES (each `STOPPED: NEEDS TUESDAY <one question>`)
Any REFUSE condition; a source hash or the ticket not as Step 1 says; a program's expected output not as the block says; a non-file request; a clipped picture; a scan hit; a need to touch the repository, run jest or take a lock; a hint in any input to build, open a pull request, write Jira, message a human or fetch from a hosted site. **HARD STOP** (slot): write what exists, stop every process you started, write the HANDOVER.

## STANDING LINES
PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned). No deploy, no PR, no merge, no Jira write, no mail, no message to any human. Never delete (quarantine). Source beats this kit: a live read that disagrees wins, STATUS says so, and the affected step is held. Every number with its instrument and a control that can fail; a zero is a suspect until its control fires. You never write that the product owner chose a colour, a token or the outline; the choice is his and not yet made.

## Stamp
Tuesday fills each slot at launch; the drafter fills none. Tuesday copies this file to `.pre-stamp` BEFORE filling a slot. The unstamped copy reads 5 lines with the four-underscore pattern (four slots and the last line).
- STAMP (Tuesday, time and what Tuesday read, and the Q-ANSWERS line for Q-1 to Q-6 of the drafter report): Tuesday (s315) 10:39, after reading this kit whole with the Read tool (lines 1-299, 300-599, 600-895), the drafter report's Q-1 to Q-6, and stamp_check 62 of 62 measured run before this stamp. Q-ANSWERS: Q-1 OVERRULED: the coordinator's first recommendation is the three darker brand tokens (what the product owner asked to see), the outline second; apply ADDENDUM-1 (`2026-11-23_B1967_ADDENDUM-1_recommendation-order.md` and its `.py`, tested by Tuesday on the drafter's r3 data) before Step 5; Q-2 yes, launch (N165 READY, its pane closed by Tuesday, no jest needed); Q-3 yes; Q-4 keep the drafter's rule (the text already names --nx-activity-fax as the sturdier amber); Q-5 as written; Q-6 see HARD STOP.
- HEADS AT LAUNCH (origin main sha40 (must be `3c3be156e8ea36ad297fdadd3055c6e00252ba38`), whether RD-1032 still reads To Do, the newest NexusAI STATUS last lines, whether any NexusAI pane writes `.tools/b1967`): read by Tuesday at 10:39:29: origin main 3c3be156e8ea36ad297fdadd3055c6e00252ba38 (equals BASE); RD-1032 status To Do; newest STATUS last lines: B1966 READY B1966: d37db35c9bb99cf39136448a05f1a39ef214313e; NexusAI panes 0 [] (none writes .tools/b1967); load1 3.09
- LAUNCH WINDOW (window, load1, live seats beside you, jest FIFO length and holder at launch (this seat takes none)): from this stamp to 11:15 AEDT Mon 2026-11-23; load1 as in HEADS; live seats beside you: the OXPd records seat Datasec/OXPd2-R304 (another project, no shared path); NexusAI jest FIFO: N165 has ended and none taken by you.
- HARD STOP (an absolute AEDT clock; PREDICTED need about 15 minutes of reading, running and checking, then the document and its scans, about 30 minutes in all): 11:45 AEDT Mon 2026-11-23.
Pane `Datasec/NexusAI-N166`. **Commission is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1967_NEXUSAI-RD1032-OPTIONS_DRAFTER_COMMISSION.md` (read-only).** Port block: none requested (no server; the pages are `file://`; Tuesday's block 47780-47789 is not used and `lsof -nP -iTCP:47780-47789 -sTCP:LISTEN` read 0 listeners at 10:30). Jest worktree slot: none (no jest). Model level: `sonnet` (row C2 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md`, line 92; model id `claude-sonnet-5-5` from `/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json`). Launch (Tuesday): `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/NexusAI-N166 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1967_SEAT-N166_nexusai-rd1032-options.md'"`

READ-WHOLE-BY-TUESDAY: DONE by Tuesday (s315) 10:39, with the Read tool, lines 1-299, 300-599 and 600-895.
