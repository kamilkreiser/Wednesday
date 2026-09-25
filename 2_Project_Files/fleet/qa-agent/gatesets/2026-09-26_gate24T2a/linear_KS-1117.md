KS-1117 k6 YAML loader: a BOM immediately followed by a comment is a marked syntax error in js-yaml 5.2.3, so a comments-only config prints "at line 1, column 2" — strip a leading U+FEFF in readYaml() (QA-963-2)
state In Progress

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
