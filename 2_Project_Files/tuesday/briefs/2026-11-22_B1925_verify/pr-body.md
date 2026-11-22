## What this changes

Four pieces of dashboard text failed the readable-contrast check (WCAG AA, 4.5:1) against the ground they actually sit
on. Each is now measured against that ground, in light and dark mode.

| text | mode | before | after |
|---|---|---|---|
| KPI labels (`.metric-card .metric-label`, written by `static/js/index.js`) | light | `#7f8c8d` on white, 3.48 | `#00719f` on white, 5.44 |
| | dark | `#8c8c8c` on the dark tile gradient, 5.07 to 4.50 | unchanged |
| Import description (`.file-description`) | light | `#7f8c8d` on `#f8f9fa`, 3.30 | `#00719f` on `#f8f9fa`, 5.16 |
| | dark | `#8c8c8c` on `#262626`, 4.50 | unchanged |
| Import drop text (`.drop-text`) | light | `#7f8c8d` on white, 3.48 (3.14 and 3.19 in the drag-over and file-chosen states) | `#00719f` on white, 5.44 (4.90 and 4.98 in those states) |
| | dark | `#7f8c8d` on `#1c1c1c`, 4.90 (it had no dark rule) | `#8c8c8c` on `#1c1c1c`, 5.07 |
| Toner percentage (`.consumable-text`) | light | white on the `#e9ecef` track, 1.19, with a text-shadow | `#212529` on its own white chip, 15.43, no text-shadow |
| | dark | white on the same light track, 1.19 | `#dedede` on its own `#1c1c1c` chip, 12.67; the track is `#313131` |

- `static/css/index-styles.css`: three colour lines, and the toner label becomes a small opaque chip (16px tall
  inside the 20px bar, centred, never clipped). The text-shadow is removed: no single text colour clears the track and
  all four toner fills, and a shadow is not credited as contrast.
- `static/css/dark-mode.css`: the drop text joins the existing dark muted-text rule, and the toner track and chip get
  dark rules. Without the first, the new light colour would have reached dark mode at 3.13.
- `__tests__/fixtures/index-light-failure-baseline.json`: two signatures leave the recorded light failure set
  (`p.file-description x3` and `span x3`, the drop-text spans); none appears.
- `__tests__/rd349-rd175-readable-text-on-its-ground.test.js`: 15 cells that read the two stylesheets and measure each
  colour with the repository's own contrast helper against the ground its own rule paints. 8 of them fail without the
  change.
- `scripts/verify-expected-counts.json`: 6231 tests in 394 suites.

No script changes and no text a user reads changes.

## Who decided

The product owner's recorded outcome: the earlier grey-text decision applies to these three places, and the white
toner text is fixed. It names the result, not the colours. The colours are the coordinator's defaults: `#00719f` for the three texts (the colour the
tab strip already uses), the opaque chip with the text-shadow removed, the dark track `#313131`, and the drop text in
the dark muted-text rule.

## Rendered check

An independent check rendered the real stylesheets in headless Chromium, in light and dark, before and after the
change: `rendered-base-light.png`, `rendered-base-dark.png`, `rendered-head-light.png`, `rendered-head-dark.png`.
Every measured text ratio after the change is at least 4.5:1 in both modes, and the chip sits inside its bar for every
fill from 0 to 100 percent. The page was a local harness (the repository's Bootstrap excerpt, no page scripts, sample
values), not the live page.

## Not changed, listed

- The e2e contrast suite's allow-list entry for the toner label and its light baselines are now out of date; that suite
  is not part of the verify.
- Other grey text on the KPI tiles (`.metric-card .text-muted`, `#95a5a6`, about 2.6:1) and the KPI value colour.
- In dark mode the black toner fill is close to the new `#313131` track (1.18:1); the percentage chip still states the
  value.

## Not tested

- The live page, hover and focus on the hosted page, other viewports, Linux.
- The e2e contrast suite.
- The hosted Build and CodeQL on the merge commit.
- The Deploy demo run a merge starts, which must read skipped.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
