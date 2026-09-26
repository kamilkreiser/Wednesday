KS-1318 ks781 J2: the combined default-shapes control asserts the COUNT of shapes, not which shapes
state In Progress

## BLUF

Non-blocking finding from the tier-2 gate on PR #1249 (KS-1144, merged `8b666a33a2b4`). J2's **combined** control cell asserts the **number** of default-export shapes found, not **which** shapes they are, so it would pass if two shapes were detected under one another's name.

## Detail

`defaultShapesOf()` returns tagged strings — `'export default function'`, `'export default <Kind>'`, `'export { x as default }'`. The per-shape rows each assert the exact tag, and they are the strong cells. The combined fixture, which carries all three at once, asserts only `toHaveLength(3)`.

So a change that made the `export default function` branch emit the `export { x as default }` tag (or made one branch fire twice and another not at all) would leave the combined cell green. The per-shape rows would catch *that* particular swap — but they are fed one shape each, so they cannot see an interaction between branches, which is the only thing the combined fixture is there to test.

## Why it is Polish and not a defect

The walk is correct at the merged tree and the per-shape rows do pin the labels. What is missing is that the **combined** cell, the one cell whose job is the interaction, checks the weakest property available.

## Done when

- [ ] the combined cell asserts the **set of tags**, not the count — e.g. `toEqual([...])` against the three expected strings in source order

## Board search before filing

Literal match over **1,307 issues (includeArchived) and 3,684 comments**: `LENGTH-ONLY` -> 1 (KS-1144, this finding's own record) · `defaultShapesOf` -> 1 (same). **Searched those two terms, 0 open hits outside KS-1144 itself.** Controls: `readYaml` -> 10 hits, fires; `qqx7-fresh-control-never-written-anywhere` -> 0.

⚠ Control note: the nonsense token used earlier today stopped being a control once it was written into two ticket bodies — it then returned 2 hits, itself. A control token has to be one that has never been recorded. This search uses a fresh one.

## Provenance

Tier-2 gate `QA/Secuura-batch1249`, non-blocking (N-1249-a), recorded at the merge of #1249.

Refs KS-1144
