KS-1300 k6 readYaml adoption: the unit suite that proves it is run by no gate, and three coverage gaps the new self-read cells leave
state In Progress

## BLUF

PR **#1236** (KS-1110, merged `2208acc0638a`) routed both k6 unit tests through `readYaml()`, so a malformed scenarios file fails them **without printing its content** — measured: the old path printed the whole file. The gate recorded **four** non-blocking findings alongside it. They are one file and one fix pass, so they are items of one ticket rather than four, per Kam's 2026-09-07 rule.

## The four items

1. **READYAML-UNGATED — the one that undoes the rest.** **No pre-push leg and no PR workflow runs this unit suite.** The cells that prove the property exist, and nothing executes them. A regression here is caught only if someone runs the suite by hand.
2. **READYAML-CANARY.** The canary that proves the old path leaked file content was measured for items A and B; it is not retained as a standing cell, so the property "a malformed file does not print its content" has no permanent witness.
3. **READYAML-ROUTING.** An **indented or dynamic** parser import would pass the new self-read cells — they read the file's own source for a top-level import, so a `js-yaml` import that is indented, conditional or dynamic is invisible to them.
4. **READYAML-SHAPES.** The shapes covered are those the two tests use; other config shapes are unasserted.

## Why item 1 leads

The other three are ordinary coverage limits. Item 1 is different in kind: it means the suite's verdict is **never produced** in the normal flow. That is the "a verdict nobody runs" shape the repo already tracks elsewhere — and it makes items 2-4 moot in practice, because even a perfect cell that nothing runs protects nothing.

## NOT claimed

Not a live failure. `systemTest/performance` reads 1088/1089 at the merged tree, and the single red is the pre-existing path-dependent `PRESUITE-URLPATH`, identical at base, head and end — not this PR.

## Board search before filing (team Secuura-PK, 1,286 issues incl. archived, 3,631 comments, literal match on titles, descriptions and comments)

* `readYaml` -> 5 total / 3 open (**KS-1117**, KS-1110, KS-485). **KS-1117 read in full and is NOT a duplicate** — it is js-yaml 5.2.3 rejecting a BOM followed by `#`, a parsing defect in the loader itself.
* `scenarios.yml` -> 18 total / 5 open; `sheddingCeiling` -> 2 total / 1 open (**KS-1110**, the merged ticket this comes from).
* Controls that fire: `KS-1229` -> 5; `consumeResetToken` -> 3; nonsense control -> 0.

`Refs KS-1110`; does not close it (item C is separately open there).

## Provenance

Tier-2c QA gate `2026-09-25-batch1218-t2c` (report sha256 `70dc4c987f04…`), raised as a **non-blocking** finding and recorded at the merge. Filed on the coordinator's instruction after the batch landed; it did not hold the merge.
