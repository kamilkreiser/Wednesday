--- comment 5833976988 by linear[bot] at 2026-09-25T14:21:39Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1144/ks781-j2-ks-900-half-the-default-only-factory-pin-has-no-in-suite">KS-1144 ks781 J2 (KS-900 half): the default-only factory pin has no in-suite positive control (three `shapes.push` inert → 231/231), and `:4650` "recorded once" cannot fail (`Map&lt;string, Set&lt;string&gt;&gt;`)</a></summary>
<p>

## BLUF

PR #981 (KS-828 + KS-900, merged 2026-09-13) added J2 — a structural pin that a default-only parser factory (`export default jsonParser` and its two sibling shapes) is loud under its local name. The tier-2 gate found the pin's walk unguarded by any in-suite control (GF-3) and one assertion that vouches for a data structure rather than the change (GF-4). Both Polish; one file, one test pass; the KS-885 class one step milder (a missing control, not a weakened one).

Report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks828-900-981-04807ea0e-tier2-r1/report.md` — §6 GF-3, GF-4, Records R-2; §4 Tg-J2 (a)/(b), Tg-ONCE. Line numbers at `04807ea0e` = develop after the squash.

## Items (one test pass)

1. **GF-3 — J2's structural pin has no positive control.** With `:4688`, `:4691`, `:4699` (`shapes.push(…)`) each made `void 0;`, the file reads `Tests 231 passed (231)` — J2 green with its walk disabled. The control the cell lacks was proven to work when present: `requestLimitsSource() + '\nexport { jsonParser as default };\n'` → `1 failed | 230 passed (231)`, exactly J2 (`expected [ 'export { x as default }' ] to deeply equal []`). **Proposal:** factor the walk into a describe-local `defaultShapesOf(source)` and add a sibling control cell feeding the three shapes, expecting three entries.
2. **GF-4 —** `:4650` **"recorded once, not once per export site" cannot fail.** `exported` is `Map<string, Set<string>>` (`:4486`); `addExport` writes one Set per local (`:4497-4499`); `exportsSorted` (`:4586-4588`) flatMaps `exported.get(n)` over the unique `isFactory` locals — a Set cannot hold `jsonParser` twice, no second local records it, a mis-keyed `exported.set(exportedAs, names)` parks the Set under `default` (which `isFactory` never reads), and an ABSENT `jsonParser` fails `:4648` first. **Proposal:** drop it, or make it a control feeding a fixture where a second local aliases the name and expect the flatMap to report both.
3. **R-2, for context (no change asked):** `export default jsonParser` (an ExportAssignment naming an identifier) is still silent in the G-05 derivation at head; caught only by J2's `:4690-4692` branch on the real file — a known limit, not a regression.

## Dedupe (searched before filing)

By symbol over 1,131 KS issues + 908 comments (includeArchived): `defaultShapesOf` 0; `J2` → KS-900 (the ticket) and KS-682 (another subject); `shapes.push` / `positive control` fuzzy only. No home; filed new.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1144-j2control-give-j2s-walk-a-positive-control-and-record-what-the-3877b91cc5b8">Review in Linear</a></p>

