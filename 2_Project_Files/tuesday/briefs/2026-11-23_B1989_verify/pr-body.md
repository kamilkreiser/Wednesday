## What this changes

On the light toner track `#e9ecef` (`--nx-surface-raised`) the lowest stop of the coloured toner fills read cyan 1.74, magenta
2.58 and yellow 1.29 to 1, below the 3:1 the brand rule sets for a graphic (BRAND.md R8, WCAG 1.4.11). In light mode the three
fills are now flat brand-token colours; dark mode paints what it painted before.

| fill | light before (lowest stop) | light now | token | ratio on the track |
|---|---|---|---|---|
| cyan | `#26c6da` 1.74 | `#0a8793` | `--nx-role-partner-manager` | 3.61 |
| magenta | `#f06292` 2.58 | `#b44752` | `--nx-role-security` | 4.47 |
| yellow | `#ffca28` 1.29 | `#b57a13` | `--nx-role-partner-tech` | 3.08 |

- `static/css/index-styles.css`: the three light rules are the flat colours, each with the token named beside the hex (RD-234:
  `tokens.css` is linked by no page, so a `var(--nx-*)` would paint nothing). The six old gradient stops move to `--toner-*`
  properties in `:root`.
- `static/css/dark-mode.css`: one rule per fill, `body.dark-mode .consumable-fill.<colour>`, paints the same gradient from the
  `--toner-*` properties (no hex of its own: RD-182; the light sheet names no dark state: RD-158).
- `scripts/derive-brand-tokens.js` names `surface-raised` as a ground of the three tokens (graphic use only); `static/css/tokens.css`
  is regenerated (comment text only, no value moves); `docs/BRAND.md` gains one bullet in 9.4.
- Tests: cell C5 of the RD-175 test reads a dark stop through the `--toner-*` properties; a new file
  `__tests__/rd1032-light-toner-fills-clear-their-track.test.js` (8 cells) pins both themes.
- `scripts/verify-expected-counts.json`: 6245 tests in 395 suites, written by the project's own `--update-counts`.

The black fill, the track, the chip text and the cartridge table's colour dots (`SUPPLY_COLOURS`, `static/js/index.js`) are not changed.

## Who decided

The three colours and "light mode only, dark unchanged" are the product owner's ruling on the options for RD-1032. Everything
else (literal hex with the token named, the dark rule through the `--toner-*` properties, flat light fills, the BRAND.md bullet,
black and the dots untouched) is the coordinator's default.

## Independent check

- Red first: the new file at the base reads 4 red (L1, L2, D1, D3) and 4 green; with the change 8 of 8. The 43 files that read
  these sheets: 735 of 735 green (727 at the base plus the 8).
- Seven plants (dark rule renamed, a light rule a gradient again, a dark stop changed, the generator ground changed, a hex in
  the dark rule, a light hex one step off, the dark selector unscoped) each turn red exactly the cells predicted; each was
  reverted to the same blobs.
- Real browser (Chromium 151, file:// pages): the dark computed styles and the dark PNG bytes are identical before and after;
  the light fills read `rgb(10, 135, 147)`, `rgb(180, 71, 82)` and `rgb(181, 122, 19)` on `rgb(233, 236, 239)`.
- Full `npm run verify -- --maxWorkers=2` at the head: PASS, 6245 of 6245 tests in 395 suites.
- Local CodeQL comparison (seat): no new and no kept high-severity result.

## Not changed, listed

- The cartridge colour dots keep the pure toner colours, so a light bar no longer equals its own dot.
- In forced-colours mode no toner fill paints, before or after this change.
- The end-to-end suite's stale light baselines (RD-1031) are not part of verify and are untouched.

## Not tested

- The hosted Build and CodeQL on the merge commit; other viewports; print; Linux.
- The Deploy demo run a merge starts, which must read skipped.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
