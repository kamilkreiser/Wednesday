# KS-908: Spark rebrief + golden (POST and GET /api/keys return connectorId)

Written 06:30 AEST 2026-09-28 by a screening/brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state, and wrote nothing under `!CODING/`. Every git write verb ran in its own `--shared` scratch clone of `ks1346cd/base`, at `ec32c40e`.

- **Base:** develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45`, confirmed by `ls-remote` at 06:08 AEST.
- **Edit points:** 2, both one-line pure insertions in `security/src/index.ts` (after `:1155` and after `:1216`). Each has 3 leading and 1 trailing context line. A second trailing line would be the whitespace-only `:1218`, which the builder refuses.
- **⚠ ROUND COUNTER: Wednesday's call.** `done.md` rows 32, 42 and 56 are THREE Ornith runs on 2026-09-15:
  - two on q4 (FAIL, then PASS 7/7);
  - one on q8 (FAIL).

  There is also a held, stale READY. By a strict count the ticket is already at 2 rounds, so the rule sends it to the cloud. If the q8 run counts as a separate model trial, this is round 2 on the Spark. The brief and golden serve either path; a cloud seat can raise the golden directly after review.

## Files
- `KS-908.md` is the brief: 2 product hunks and one new vitest file of 98 lines. The test is a wire test on the real app, copying ks742's harness.
- `KS-908.golden.diff`, sha256 `cb622266e29a…`: **100 + / 0 -**.
- **Fence rebuild:** the diff rebuilt from the brief's `File:`/`Test file:` lines and its three fences is **IDENTICAL** to the golden (`cmp`).
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote. There are 0 non-ASCII lines and 0 blank context lines. Edit 1's trailing context line has backticks, but it is copied context, not written.

## Measured (scratch clone at `ec32c40e`, node_modules farmed by `prepare_clone.sh`)

| step | instrument | result |
|---|---|---|
| strict apply | `git apply --check` / `patch -p1 -F0 --dry-run` | rc 0 / rc 0 |
| test file alone (RED) | `vitest run <file> --reporter=json` | **2 failed / 2 passed / 4**: A1 and A2, by ASSERTION (`{status:201, connectorId: undefined}`, `{found:true, connectorId: undefined}`) |
| golden applied (GREEN) | same | **4 / 4** |
| whole security suite | `vitest run --reporter=json` | tip **23 files / 247 / 0 failed**; golden **24 / 251 / 0** (+4; ks742 and ks869 green) |
| tsc | `tsc --noEmit -p services/security` | rc 0 at both |
| tsc with tests | temp tsconfig including `src/**/*.ts` | rc 2 at both, byte-identical error lists (2 pre-existing ks952 errors), 0 naming the new file |
| eslint | both changed files | rc 0 |

**Arms:**

| arm | failed / total | which |
|---|---|---|
| tip | 2 / 4 | A1, A2 |
| Edit 1 line fed from `apiKey.name` | 2 / 4 | A1 + control C1 |
| Edit 2 line fed from `k.organizationId` | 2 / 4 | A2 + control C1 |
| golden | 0 / 4 | none |

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/ks1346cd/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-908 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-908 <out>/input.json product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts line=1156 ctx=65536
```
The builder output:
- prompt source: WEDNESDAY BRIEF;
- red cells `['RED KS-908 A1', 'RED KS-908 A2']`;
- 2 expected `+` lines (A3c);
- `suggested_test_file` = the brief's `File:` line.

**Size:**
- **Whole file:** index.ts is 69.3 KB. That gives input.json 123,110 B, about **31K prompt tokens**.
- **Excerpted:** with `NIGHT_EXCERPT_TRIGGER_BYTES=60000`, the file becomes 5 regions `[(1,81),(267,467),(548,598),(1018,1248),(1326,1376)]` = 27.2 KB. That gives input.json 83,991 B, about **21K tokens** (rc 0).
- **Recommendation:** use the excerpt. Both edit sites and the `:1351` precedent are inside the regions.

## The round command (NOT run; only if Wednesday rules the counter allows it)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/sparkrun/round.sh KS-908-R2 KS-908 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-908 60000 product=Blockchain/Dev/services/security/src/index.ts ref=Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts line=1156 ctx=65536
```

## OPEN DOUBTS
- **No Spark round was run.**
- **The published schemas are NOT updated.** `ApiKeyCreateResponse` and `ApiKey` are `.passthrough()`, so the contract tolerates the new field and `check:openapi` needs nothing. Declaring the field is a KS-794-shaped follow-up. The list schema's `keys`-vs-`data` naming is a separate pre-existing drift.
- **No live stack.** The ticket's demo-box measurement was not re-run.
- **The test signs JWTs with node crypto, exactly as ks742 does.** The product change touches no auth code.
