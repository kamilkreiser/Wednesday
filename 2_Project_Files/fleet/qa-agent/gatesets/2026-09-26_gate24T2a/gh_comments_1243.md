--- comment 5833173569 by linear[bot] at 2026-09-25T13:26:24Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1117/k6-yaml-loader-a-bom-immediately-followed-by-a-comment-is-a-marked">KS-1117 k6 YAML loader: a BOM immediately followed by a comment is a marked syntax error in js-yaml 5.2.3, so a comments-only config prints "at line 1, column 2" — strip a leading U+FEFF in readYaml() (QA-963-2)</a></summary>
<p>

## BLUF

js-yaml 5.2.3 rejects a file whose first bytes are a byte-order mark followed directly by `#` as a marked syntax error ("end of the stream or a document separator is expected" at raw mark 0:1). `readYaml()` in `systemTest/performance/utils/yaml.ts` prints that mark faithfully, so a comments-only `secrets.yml` or `scenarios.yml` written by a BOM-emitting editor answers `Could not parse YAML in <file> at line 1, column 2 (the file's content is not shown).` — a verdict true of what the parser did and false of the file, which holds no document. Pre-existing and identical at base (`34be9c18a`); outside PR #963's promise; content-free on every path. Measured by the tier-2 gate on #963 (QA-963-2).

## Recommendation

One line in `readYaml()`: strip a leading U+FEFF from `source` before `loadYaml(source)`. That makes `<BOM># comment` read `: it contains no YAML document` (the KS-1109 wording) and, as a side effect, makes the K4 row print the editor's column rather than the BOM-shifted one. The alternative is to leave js-yaml's behaviour and document it in the loader's why-comment. Either way, add the two regression cells below.

## Detail

* **Where:** `systemTest/performance/utils/yaml.ts` (`readYaml()`, the `loadYaml(source)` call; the mark is printed at the lines the gate cites as `:68-70` at `90d7d0c75`). The parser behaviour is js-yaml 5.2.3 `dist/js-yaml.mjs` (READ ONLY by the gate: the BOM is not skipped before a `#` at position 1; `BOM + space + #` and `BOM + LF + #` parse; `BOM` alone and `BOM + LF` raise the "input is empty" constant).
* **Measured (gate evidence** `evidence/instruments/bom.mjs`**,** `evidence/probe963/`**,** `evidence/drives/`**):** `<BOM># c\n` → `YAMLException` at raw mark 0:1; probe rows E08 (BOM + comments holding a sentinel) and E21 (BOM + comment + `---`) print `at line 1, column 2` at head and base, 0 content in every rendering and in the uncaught print; drive D09 (`runner/cli.ts`, `secrets.yml` = BOM + a comment holding a sentinel) prints `[run] ERROR: … at line 1, column 2 (…)`, rc 1, 0 sentinels, at head and base alike. Rows E06 (BOM alone) and E07 (BOM + LF) already print `: it contains no YAML document`.
* **Blast radius:** `config/secrets.example.yml` begins with `#` (22 of 58 lines are comments), so `cp` + an editor that writes a BOM (Windows Notepad, some IDE encodings) lands a first-run operator on "line 1, column 2" of a file whose line 1 looks like a comment. The bootstrap hint is not involved.
* **Regression cells to add with the fix:** `'﻿# only a comment\n'` reads `: it contains no YAML document`; `'﻿admin:\n  a: 1\n'` still parses to `{admin:{a:1}}`.
* **Source:** `Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks1109-963-90d7d0c75-tier2-r1/report.md`, FINDINGS QA-963-2 (severity Polish there; filed Low here as a one-line fix with a first-run operator in its blast radius).
* **Related:** KS-1109 (PR #963, the loader's wrapped-parse-failure round this was found in); KS-1110 (the two unit tests that bypass `readYaml()`), KS-1099 (the sanitiser this loader carries).
* **Dedupe, before filing (s200, 2026-09-13):** a literal census over 1,106 KS issues (685 archived, titles + descriptions) and 899 comments on non-archived issues — `readYaml` → KS-1099 (archived), KS-1109, KS-1110; `utils/yaml.ts` → the same plus KS-429 (archived); `BOM` → KS-975 only (a rateLimitScope input-shape table; unrelated). None describes the BOM-plus-comment mark. Controls: `LIKE` → KS-1020; a nonsense token → 0.
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1300/k6-readyaml-adoption-the-unit-suite-that-proves-it-is-run-by-no-gate">KS-1300 k6 readYaml adoption: the unit suite that proves it is run by no gate, and three coverage gaps the new self-read cells leave</a></summary>
<p>

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
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1117-ks-1300-bomstrip-strip-a-leading-ufeff-in-readyaml-and-make-f98c3650c4c1">Review in Linear</a></p>

