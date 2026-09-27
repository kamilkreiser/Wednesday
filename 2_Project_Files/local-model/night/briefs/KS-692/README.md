# KS-692: Spark rebrief + golden (status-list writes narrowed to platform roles, as Kam ruled)

Written 06:30 AEST 2026-09-28 by a screening/brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state, and wrote nothing under `!CODING/`. Every git write verb ran in its own `--shared` scratch clone of `ks1346cd/base`, at `ec32c40e`.

- **Ruling:** Kam, 2026-09-16 15:04 AEST, card `secuura-ks692-status-revoke-interim-posture`, option a: "Narrow now, bind-creator later". Source: `0_Brain/dashboard/data/decisions.json`, where the card reads `ruled_choice: a`.
- **Base:** develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45`. `status.ts` changed after the 09-16 brief (KS-1269, #1071, 2026-09-19), so the old READY is stale.
- **Edit points:** 2 in `vc-issuer/src/routes/status.ts`:
  - Edit 1 replaces 3 comment lines `:34`-`:36` with 7 lines.
  - Edit 2 replaces the constant at `:40` with 1 line.
- **Round counter:** ONE. At `done.md:181` the round FAILed at A4 and Wednesday retracted it as a brief defect. The SAME output was then re-checked PASS at `done.md:182`, with no second model round. This rebrief is the one allowed round.
- **Scope:** refs KS-692 and does NOT close it. The owner-column / bind-creator fix stays open.

## ⚠ The harness caveat, measured
`build_input.sh` **REFUSES** this brief as written: rc 2, "edit block 2 has a BLANK CONTEXT line". It builds rc 0 only with **`ALLOW_BLANK_CONTEXT=1`**. The blank line cannot be designed away:
- `:40` is the last changed line, and `:41` is empty.
- A hunk with no trailing context fails strict `git apply`. Measured on a probe hunk: rc 1, "patch does not apply".

The builder's gate exists because a model once dropped a blank context line (KS-1229 r1). The brief tells the model explicitly to emit the one-space line. If the Spark drops it anyway, classify the result as a **harness/brief** FAIL, not a model one. **Wednesday decides whether to spend the round under the override.** The alternative is a cloud seat raising the golden after review.

## Files
- `KS-692.md` is the brief: 2 hunks and one new vitest file of 81 lines.
- `KS-692.golden.diff`, sha256 `e14fcf43e1be…`: **89 + / 4 -**.
- **Fence rebuild:** the diff rebuilt from the brief's `File:`/`Test file:` lines and its three fences is **IDENTICAL** to the golden (`cmp`).
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote, and 0 `+` lines are non-ASCII. The diff as a whole has:
  - ONE non-ASCII line: Edit 1's third `-` line, which carries an em dash that must be copied;
  - ONE blank context line (`:41`).

## Measured (scratch clone at `ec32c40e`, node_modules farmed by `prepare_clone.sh`)

| step | instrument | result |
|---|---|---|
| strict apply | `git apply --check` / `patch -p1 -F0 --dry-run` | rc 0 / rc 0 |
| test file alone (RED) | `vitest run <file> --reporter=json` | **2 failed / 3 passed / 5**: A1 and A2, by ASSERTION (the array holds ISSUER_ADMIN; revoke/unrevoke answer 400, past the gate) |
| golden applied (GREEN) | same | **5 / 5** |
| whole vc-issuer suite | `vitest run --reporter=json` | tip **14 files / 136 / 0 failed**; golden **15 / 140 / 0**. The count is +5 for the new file and -1 for ks586: its `it.each(STATUS_WRITE_ROLES)` goes from 14 cells to 13, all green |
| tsc | `tsc --noEmit -p services/vc-issuer` | rc 0 at both |
| tsc with tests | temp tsconfig including `src/**/*.ts` | rc 2 at both, with byte-identical lists (4 pre-existing errors) and 0 naming the new file |
| eslint | both changed files | rc 0 |

**Arms:**

| arm | failed / total | which |
|---|---|---|
| tip | 2 / 5 | A1, A2 |
| golden + `, 'ISSUER_ADMIN'` | 2 / 5 | A1, A2 |
| golden + `, 'ORG_ADMIN'` | 1 / 5 | A1 only |
| golden | 0 / 5 | none |

## build_input
**Without the override: rc 2 (REFUSED, blank context).** With the override: rc 0.
```
ALLOW_BLANK_CONTEXT=1 NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/ks1346cd/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-692 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-692 <out>/input.json product=Blockchain/Dev/services/vc-issuer/src/routes/status.ts ref=Blockchain/Dev/services/vc-issuer/src/__tests__/ks586-status-write-authorization.test.ts line=40 ctx=65536
```
The builder output with the override:
- prompt source: WEDNESDAY BRIEF;
- red cells `['RED KS-692 A1', 'RED KS-692 A2']`;
- 8 expected `+` lines (A3c);
- input.json 38,438 B, about **9.6K prompt tokens** for the whole file.

## The round command (NOT run; needs Wednesday's go on the override)
```
ALLOW_BLANK_CONTEXT=1 bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/sparkrun/round.sh KS-692-R2 KS-692 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-692 - product=Blockchain/Dev/services/vc-issuer/src/routes/status.ts ref=Blockchain/Dev/services/vc-issuer/src/__tests__/ks586-status-write-authorization.test.ts line=40 ctx=65536
```
`round.sh` passes its environment through to `build_input.sh`, and `build_input.sh` reads `ALLOW_BLANK_CONTEXT`. Whether the CHECKER also has a blank-context rule was not measured.

## OPEN DOUBTS
- **No Spark round was run.**
- **This is an authorization change (a role gate), and it was ruled by Kam.** The screen put it in the Spark tier only because Wednesday named it in the pool and Kam's ruling fixes its shape. It is not in the excluded auth list (623/938/1009/1219/1186/1250/884/888).
- **Tenant admins lose status writes until the owner column lands.** That is the ruled cost. No live-tenant usage census was run beyond the card's caller scan.
- **The ks586 file's own header comment still says "tracked on KS-586".** This brief does not edit that file.
