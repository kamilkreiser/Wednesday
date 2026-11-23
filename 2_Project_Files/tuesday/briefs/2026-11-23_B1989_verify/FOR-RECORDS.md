# For the records seat: RD-1032 (gate B1989, after the landing of branch b1977/rd1032-light-toner-fills)

## RD-1032's state
- RD-1032 (To Do at the stamp of the build kit; labels `operations`, `records-pass-1123`) is **BUILT** on branch
  `b1977/rd1032-light-toner-fills` (head K `97a07e65d675960e937b6742981af5d338d427d7`, A `0ab1ea3948ea5543b5cdb52765b7b6f5ae5535c6`,
  base main `85b39c77b84573757d26113cf094325b5b80c182`). The gate did not read Jira (relayed, not re-measured).
- After the landing: RD-1032 may move to **Testing** on the hosted checks of the landing head (7 check names green, the hosted
  build at `Tests: 6245 passed`, `Test Suites: 395 passed`, no new CodeQL alert against main's open 22, the Deploy demo run's
  build and deploy jobs both skipped). Not before. It is NOT DEPLOYED: the demo shows the old colours until a separate deploy
  decision (C-220, C-224) is acted on.
- One sentence for the ticket and HISTORY.md (the seat's, checked by the gate against the head): RD-1032: in light mode the
  cyan, magenta and yellow toner fills are now the brand tokens #0a8793, #b44752 and #b57a13 (3.61, 4.47 and 3.08 to 1 on the
  #e9ecef track, against 1.74, 2.58 and 1.29 at the lowest stop), dark mode paints the same gradients as before (pixel-identical
  in a real browser), the generator names the raised ground for the three tokens, and a new test file pins both themes.
- Who decided: the three colours and "light mode only, dark unchanged" are the product owner's ruling (card
  `nexusai-rd1032-pick-toner-fill-1123` = option a; his note of 2026-11-23 11:06:40, "looks great.  please build and deploy").
  The six defaults (literal hex with the token named beside it, the dark rule shape through `--toner-*` properties in the light
  sheet's :root, flat light fills, the BRAND.md bullet, black untouched, the dots untouched) are the coordinator's. The word
  "deploy" in his note is a separate decision and a separate route (not this landing).

## Named limit: the cartridge dots (SUPPLY_COLOURS)
`SUPPLY_COLOURS` (`static/js/index.js` line 7416: `#2c3e50`, `#00bcd4`, `#e91e63`, `#ffc107`) is untouched. After this landing a
light bar (deep teal, rose red, amber) no longer equals its own colour dot (bright cyan, pink, yellow). A follow-up if the
product owner wants dot and bar to match (options document section 7). Not a defect of this lane.

## RD-1031 untouched
`tests/e2e/dark-mode-contrast.spec.js` (stale light baselines, RD-1031) is not part of `npm run verify` and is not touched; its
`consumable` baselines will differ further in light after this landing, which RD-1031's own text already expects.

## Also for the records (from the gate's findings, none blocking; details in VERDICT.md)
- Forced-colours: no toner fill paints at all in forced-colors mode, before or after this change (measured in the same
  Chromium: computed fills transparent before, Canvas white after, the track Canvas white in both; the page shows only the
  percentage). Not a regression, not fixed here; a possible follow-up item.
- The dark toner track equals the striped row's ground (RD-175 finding I-1), unchanged.
- Version skew: the two sheets (`index-styles.css`, which now holds the `--toner-*` properties, and `dark-mode.css`, which reads
  them) are linked without a version query and served by the default static handler; a browser holding an old `index-styles.css`
  with a new `dark-mode.css` would paint no dark fill for cyan, magenta and yellow until it revalidates. The default
  `max-age=0` revalidates on load; noted, not a blocker.
- Not touched by the lane or the gate: HISTORY.md, BACKLOG.md, CLARIFICATIONS.md, Jira.
