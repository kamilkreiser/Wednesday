# Gate 260 F1 drive results (my own builds, my own instrument)

Builds (tools/build.sh, Dockerfile layout, `npm ci --offline`, Node v26.8.1, npm 11.19.0), served by `vite preview` on 127.0.0.1:
- dev  = develop abd044f63a9d issuer, on-disk react-router 6.30.6 + react-router-dom 6.30.6, port 4323
- r1   = 258e049aaf75 issuer (round-1 head), react-router 7.18.5, no opt-out, port 4321
- head = e5742b73748b issuer, react-router 7.18.5 + `useTransitions={false}`, port 4322

Chromium via the Playwright MCP. All /api calls stood in (refresh 200, users/me 200 ISSUER_ADMIN, everything else 404). Chunk held 2500 ms. 8 samples at 200 ms after a real click on the visible sidebar button.

## v1 (tools/drive_f1.js): INVALID, kept
Waited for `getByRole('heading', {level:1, name})`, which matched the Layout HEADER h1 (it shows the current route's name before the lazy page itself has rendered), so it clicked while the start page was still in its own fallback. Result: all three builds, r1 included, showed "Loading..." 8 of 8, and the "old page" count was 0 everywhere. The control could not tell r1 from dev, so the run says nothing. Diagnosed with a marked-node probe: r1 then held the old page (marked node visible, 0 "Loading..." nodes), and dev showed the fallback.

## v2 (tools/drive_f1_v2.js): VALID
The predicate is visibility: `checkVisibility({checkOpacity, checkVisibilityCSS})` plus a non-zero box, applied to the `<p>Loading...</p>` and to the OLD page's own `<h1>` inside `<main>`. DOM presence is recorded separately.

Held samples, as fbVisible / oldVisible / oldInDomButHidden out of 8:

| scenario | settle | dev (v6) | r1 (v7, no opt-out) | head (v7 + opt-out) |
|---|---|---|---|---|
| settings -> documents, rep1 | 1000 ms | 8 / 0 / 8 | 0 / 8 / 0 | 8 / 0 / 8 |
| settings -> documents, rep2 | 1000 ms | 8 / 0 / 8 | 0 / 8 / 0 | 8 / 0 / 8 |
| documents -> settings, rep1 | 1000 ms | 8 / 0 / 8 | 0 / 8 / 0 | 8 / 0 / 8 |
| documents -> settings, rep2 | 1000 ms | 8 / 0 / 8 | 0 / 8 / 0 | 8 / 0 / 8 |
| settings -> documents | 0 | 8 / 0 / 8 | 0 / 8 / 0 | 8 / 0 / 8 |
| documents -> settings | 0 | 8 / 0 / 8 | 0 / 8 / 0 | 8 / 0 / 8 |

- Layout header during the hold: dev and head show the NEW name, r1 keeps the OLD name. Path is the new path in 8 of 8 samples for every build.
- Unheld: dev and head show the fallback in their first sample (1 of 8) and r1 in none.
- After the chunk arrives, every run shows the new page's h1 visible, no fallback, and no old h1.
- Chunk requested 0 times before the click and once after it, in every run. 0 pageerrors in every run.
- Planted visibility control (head, unheld): a `display:none` `<p>Loading...</p>` was appended to `<main>` before the click. The predicate reported it hidden in 7 of 8 samples (the 8th sample is the real fallback, visible). It was still in the DOM at the end (plant=1, fbInDom=1, fb=false). The predicate therefore does not read DOM presence as "shown".
- Natural control: in dev and head the old h1 is in the DOM but hidden in 8 of 8 held samples. React keeps the old children mounted and hides them, and the visibility predicate tells this apart from r1's visible old page.
