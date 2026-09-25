#1243 KS-1117 + KS-1300 BOMSTRIP: strip a leading U+FEFF in readYaml, and make the routing cell able to fail
head 0c89e2b503d9333829c277c50ad3b1a33f03cb96

## What this changes

**KS-1117** — `readYaml()` strips exactly one **leading** U+FEFF before `loadYaml()`. Node keeps the byte-order
mark when it decodes as `utf-8`, and js-yaml 5.2.3 raises a *marked* failure at 0:1 for a mark followed directly
by `#`, so a file holding no document answered `at line 1, column 2`.

**KS-1300 items 2–4** — the two k6 unit suites #1236 routed through `readYaml()` get the three things its gate
found missing: a retained canary, a routing check that can fail, and shape assertions.

## Measured against the real parser, not the ticket's example line

Captured from js-yaml 5.2.3 through the real `readYaml()` at develop `6e2a00bfe`:

| fixture | js-yaml | `readYaml` before | after |
|---|---|---|---|
| `<BOM># comment` | `YAMLException` MARK 0:1 | `at line 1, column 2` | `: it contains no YAML document` |
| `<BOM># comment` + a real document | `YAMLException` MARK 0:1 | **unreadable** | parses |
| `<BOM>admin: …` | parses | parses | parses (control) |
| `"<BOM>value"` inside a scalar | parses | parses | parses, mark intact (control) |

**Two corrections to KS-1117, both measured.** (1) The ticket frames this as a *comments-only* file problem. It is
not: `<BOM>` + a leading comment + real content fails identically, so a valid config whose first line is a comment
— which `config/secrets.example.yml` is — was rejected outright. That is the larger half of the blast radius and
the ticket does not state it. (2) The ticket's second regression cell (`<BOM>admin:` still parses) reads as an
outcome of the fix; it **already passed at base**, so it ships as a control, not as a result.

## Test Evidence

**Touched:** `systemTest/performance/utils/yaml.ts`, `tests/unit/utils/yamlRedaction.test.ts`,
`tests/unit/config/sheddingCeiling.test.ts`, `tests/unit/package_scripts.test.ts`, and a new
`tests/unit/support/readYamlRouting.ts`. No `package.json`, no lockfile, nothing outside
`systemTest/performance/`.

**Ran** (all by the author, on this head, macOS, node v24.7.0, vitest 4.1.11):

- `npm run test:unit` — **63 files / 1097 passed / 0 failed**, rc 0. Base at develop `6e2a00bfe` was
  **63 / 1089 / 0**, so +8 cells and no pre-existing red on either side. Load 6.30–8.51 throughout; taken bare
  and serial.
- `npm run lint` — rc 0. This runs **both** tsconfigs (`tsconfig.json` *and* `tsconfig.node.json`) plus eslint;
  the second one is the check a recent PR in this package missed, so it is named explicitly.
- `npm run format:check` — rc 0.
- **Red-proof, KS-1117** (`tamper1117.sh`, one arm per conjunct of "strip / leading-only / exactly one"):
  no strip → **B1 + B2 red**; blanket `replace(/﻿/g,'')` → **only B4 red**; unconditional `slice(1)` →
  **B4 + E2 red**. Baseline 19/19 between arms, file restored byte-exactly (sha256 asserted, not `git checkout`).
- **Red-proof, KS-1300** (`tamper1300.sh`): routing narrowed back to the old `startsWith('import')` predicate →
  **the positive control reds**; detector blinded to `[]` → **the positive control reds**; `readYaml` rethrowing
  the parser's own error → **the canary reds**; parsed arrays flattened to strings → **READYAML-SHAPES reds**
  (plus the pre-existing "keeps the ceiling loose" cell). Baseline 21/21 between arms, restores sha256-asserted.

**Which gate ran, exactly:** this is a repo-root `systemTest/` change, and `.githooks/pre-push` gates its 15-leg
preflight on `^Blockchain/Dev/`. **The preflight did not run** — the push took 12 s and printed only
`[format-gate] 1 package(s) checked, 0 skipped, 0 failed`. The fleet STOP count (`pre_push_hook_base` 28/0,
`fixture_guard` 6/0, shell suites 60/60) was therefore **not executed on this branch**, and nothing here quotes
it. Everything above was run by hand.

**NOT run / NOT covered:**

- No k6 run, no docker, no environment of any kind. Nothing deployed.
- `npm run knip` and `npm audit` (the other halves of `npm run quality`) were not run; neither is affected by a
  parser call or a test cell, and `audit` reaches the network.
- **KS-1300 item 1 (READYAML-UNGATED) is not delivered and stays open.** Wiring this suite into a gate edits the
  pre-push hook or the preflight, and neither is in this lane's scope. It is the item the ticket calls "the one
  that undoes the rest", so it is stated rather than quietly dropped.
- The routing check recognises static, indented, re-exported, `require`d and dynamic imports. A parser reached
  through a **computed specifier** (`import(base + '-yaml')`) would still evade it; that is a disclosed limit,
  in the under-reporting direction.
- The canary spawns one `tsx` child (~2.5 s), which is most of this suite's added wall-clock.
- `tamper1117.sh` T-3 reds only 2 cells. A file whose first byte is removed often still parses as valid YAML,
  so the corpus does not strongly pin "the first byte of a non-BOM file survives"; B4 is what catches it.

**Migrations + config:** none. No migration, no schema change, no environment variable, no config file.

Refs KS-1117
Refs KS-1300

