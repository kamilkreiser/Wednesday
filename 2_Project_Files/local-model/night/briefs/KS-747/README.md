# KS-747: Spark rebrief + golden (GET /api/security/keys declares organizationId)

Written 06:29 AEST 2026-09-28 by a screening/brief-writer sub-agent for Wednesday. It ran no model, raised no PR, and changed no GitHub or Linear state (Linear, `ls-remote` and PR head refs were READ). It wrote nothing under `!CODING/`. Every git write verb ran in its own `--shared` scratch clone of `ks1346cd/base`, at `ec32c40e`.

- **Base:** develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45`, confirmed by `ls-remote` at 06:08 AEST. The base clone's HEAD was verified equal before any copy.
- **Why a rebrief:** the 09-15 Ornith READY is stale. It used service-relative paths, and the census on 09-27 found it would not apply until re-pathed. It also omitted the generated YAML, which `check:openapi` needs.
- **Edit points:** 1 (a pure insertion after `security.openapi.ts:809`).
- **Round counter:** 1 used (`done.md:77`, retracted as a brief defect and re-checked PASS). This rebrief is the one allowed round.

## Files
- `KS-747.md` is the brief: one product line and one new vitest file of 50 lines.
- `KS-747.golden.diff` is the Spark-scope golden, sha256 `6b8f07b11862…`: 2 files, **51 + / 0 -**.
- `KS-747.openapi-yaml.companion.diff`, sha256 `9d47d59a5859…`, is the 7-line regenerated `docs/openapi/secuura-api.yaml` hunk. **It is NOT the model's.** The raising seat adds it; see "For the raise".
- **Fence rebuild:** the diff rebuilt from the brief's own `File:`/`Test file:` lines and its two fences is **IDENTICAL** to the golden (`cmp`). Comparator control: a one-token mutation printed **DIFFER**.
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote. There are 0 non-ASCII lines and 0 blank context lines.

## Measured (scratch clone at `ec32c40e`, node_modules farmed by `prepare_clone.sh`, shared built in the clone)

| step | instrument | result |
|---|---|---|
| strict apply | `git apply --check` / `patch -p1 -F0 --dry-run` | rc 0 / rc 0 |
| test file alone (RED) | `vitest run <file> --reporter=json` | **2 failed / 3 passed / 5**: exactly A1 and A2, by ASSERTION (`declared:false`, `type/format undefined`) |
| golden applied (GREEN) | same | **5 / 5** |
| whole security suite | `vitest run --reporter=json` | tip **23 files / 247 passed / 0 failed**; golden **24 / 252 / 0** (+5 = this file) |
| tsc | `tsc --noEmit -p services/security` | rc 0 at the tip and with the golden |
| tsc with tests | temp tsconfig including `src/**/*.ts` | rc 2 at both, the SAME 2 pre-existing ks952 errors, 0 naming the new file |
| eslint | both changed files | rc 0. Control: a planted `debugger`/`var` file gave rc 1 |
| openapi drift | `npm run generate-openapi -- --check` | tip PASS; **golden alone FAIL**; golden + companion: `npm run check:openapi` **PASS** (drift + 405 examples) |

**Arms** (the golden test against variant product lines; the clone was reset to the tip after):

| arm | failed / total | which |
|---|---|---|
| tip (no line) | 2 / 5 | A1, A2 |
| `.uuid().optional()` | 1 / 5 | A1 only |
| `z.string()` (no uuid) | 1 / 5 | A2 only |
| golden | 0 / 5 | none |

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/ks1346cd/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-747 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-747 <out>/input.json product=Blockchain/Dev/services/security/src/security.openapi.ts ref=Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts line=810 ctx=65536
```
Output (the run was on a byte-identical scratch copy of this brief):
- `prompt source: WEDNESDAY BRIEF … (12654 chars)`
- red cells `['RED KS-747 A1', 'RED KS-747 A2']`, 1 expected `+` line (A3c)
- `suggested_test_file` = the brief's `File:` line
- the contract key set is OK
- input.json 51,679 B, about **12.9K prompt tokens**, whole file (32.8 KB, no excerpt needed)
- the base's porcelain was 0 before and after

## The round command (NOT run)
Use the round script already pinned to this tip: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/sparkrun/round.sh`. It pins `SRC=ks1346cd/base` and `TIP=ec32c40e…`, and it refuses if the source is not clean at the tip.
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/sparkrun/round.sh KS-747-R2 KS-747 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-747 - product=Blockchain/Dev/services/security/src/security.openapi.ts ref=Blockchain/Dev/services/security/src/__tests__/ks974-published-bound-vs-runtime-bound-on.test.ts line=810 ctx=65536
```

## For the raise (after a PASS)
Add the companion hunk: `git apply KS-747.openapi-yaml.companion.diff`, or run `npm run generate-openapi` in `Blockchain/Dev` and confirm it produces the same 7 lines. Then run `npm run check:openapi`. Without the companion, the Dev preflight's openapi drift check fails (measured).

## OPEN DOUBTS
- **No Spark round was run.** This is a brief and a golden only.
- The served spec (`/api/docs/openapi.json`) and the Schemathesis `pr` tier were not run. The ticket itself calls the Schemathesis outcome a prediction.
- API keys sit next to a credential surface. This change is spec-only (no handler, no auth code). The screen still classed it Spark, because the ticket's fix is a declaration and Wednesday named it in the pool.
