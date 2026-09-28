# KS-1124 F4: Spark brief + golden (a certification whose anchoring failed outside production is saved with status 'failed')

Written 00:01 AEST 2026-09-29 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and PR #1324's state were only READ, by `build_input.sh`), mailed nobody and wrote nothing under `!CODING/`. Every git write verb ran under `scratchpad/bw0929/`. The read-only sources were only read: `carve_base` HEAD `d9ce1403` porcelain 0 before and after; `verify_clone` was only fetched FROM.

- **Ruling:** Kam ruled card `secuura-ks1124-f4-failed-anchor-shows-pending` option **b** (2026-09-28 20:22): "Save a 'failed' status the gateway already reads as off-chain-only".
- **Base:** develop `0d156d12cc0fc45fc323397c6999898565c44c54` (tree `c0497437f34c`), built as `bw0929/base` = `cp -a carve_base` + fetch from `verify_clone` + detached checkout; porcelain 0; `packages/shared` rebuilt (rc 0). `build_input.sh`'s own `ls-remote` confirmed origin develop = `0d156d12`.
- **Shape:** both routes (`/issue` `:471`, `/:id/recertify` `:1206`) add `...(anchoringStatus === 'failed' ? { status: 'failed' } : {}),` to the saved `blockchain` blob. The success leg stays statusless. The `confidence: 'pending-onchain'` label is left alone (that would be option a).
- **Edit points (3):** `certifications.ts` after `:471`, after `:1206`; one hunk appending a `describe` to `ks543-certify-boundary-strip.test.ts` (modified in place).
  - **Why not a new test file:** measured, a new file that sets `ANCHORING_SERVICE_URL` reddens `ks1293-originate-suite-is-hermetic.test.ts` (MANIFEST-DRIFT: the new file is not in its SUBJECTS list), which would be a 4th edit point. `ks543` is already a subject and already has the harness.
  - The two product hunks have byte-identical context (the routes build the same blob); the header line numbers place them. The A2a anchor check passed on both.

## Files
- `KS-1124.md` is the brief (19,253 chars).
- `KS-1124.golden.diff` is the golden, sha256 `36addc419195…`: 2 files, 35 `+` lines (32 non-blank), 0 `-` lines.
- **Fence rebuild:** a diff rebuilt from the brief's two fences is IDENTICAL to the golden (`cmp`). The comparator control (one token mutated in the brief) printed DIFFER.
- **Char lint of `+` lines:** 0 contain a backslash, a backtick, a double quote or a non-ASCII character (control: a planted backtick counted 1). 0 blank context lines; 0 non-ASCII context lines.

## Measured (scratch copy at 0d156d12; jest 29.7.0 / ts-jest, node 24.7.0)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0; applied result `cmp`-identical to the measured files |
| test hunk ALONE at the tip (RED) | **2 failed / 3 passed / 5**: exactly F4-1 and F4-2, by ASSERTION (`"saved": "failed"` expected, `undefined` received). 0 Unhandled. |
| golden applied (GREEN) | **5 / 5** |
| originate suite | tip **89 suites / 1055 / 0 failed**; golden **89 / 1058 / 0** |
| `tsc --noEmit -p services/originate` | rc 0 at the tip and with the golden (excludes tests) |
| tsc incl. tests (temp tsconfig, jest types) | rc 0 at the tip and with the golden. Control: planted `const x: number = 'x'` in the test file gave rc 2 (TS2322). |
| eslint (run from `Blockchain/Dev`) on both files | rc 0 at the tip and with the golden. Controls: planted `var` + `debugger` file rc 1; same planted in the test file rc 1. |
| **the real Spark checker on the golden as model output** (`spark_checker.sh`, clone made + `prepare_clone.sh` as the round does) | **SPARK RESULT: PASS**, A1-A7 all PASS, A2a anchor 3/3 hunks ok. A4: 2 failed / 5, assertion reds, controls green. |

**Arms** (the golden test against a variant `certifications.ts`; golden restored and `cmp`-checked after):

| arm | result |
|---|---|
| issue-route line (`:474` in the fixed file) emptied | 1 failed / 5: F4-1 only |
| recertify-route line (`:1212`) emptied | 1 failed / 5: F4-2 only |
| `:474` unconditional `...({ status: 'failed' })` | 1 failed / 5: the control F4-3 (the success leg must stay statusless) |
| `:474` saving `'anchor_failed'` | 1 failed / 5: F4-1 (pins the ruled literal) |

Happy path: F4-3 (anchoring accepted: statusless, `pending-onchain`, anchor id kept) is green at the tip and with the golden.

**The served answer, through the REAL gateway route** (scratch vitest file on the `ks1123-f2` harness; not part of the golden; moved to `bw0929/_quarantine_2026-09-28/` after): the tip's blob -> `pending-onchain`; the golden's blob (`status: 'failed'`) -> `off-chain-only`, `verified: false`; `'anchor_failed'` -> `off-chain-only`; a submitted blob -> `pending-onchain`. 4 / 4.

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw0929/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1124-F4 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1124 <out>/input.json product=Blockchain/Dev/services/originate/src/routes/certifications.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks445-certifications-issue-unstorable-payload.test.ts test_file=Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts line=471 ctx=65536 started_ok=O1-merged-1324_F4-carved-by-card-ruling-b-2026-09-28-2022
```
Output, verbatim:
```
ticket KS-1124 · In Progress (started) · Medium · assignee=kamil.kreiser@secuura.ai · updated 2026-09-28T09:32:16.222Z
attached PR #1324 (Secuura/Distributed_Secuura): merged
WARN state is In Progress (started) — ADMITTED by started_ok: O1-merged-1324_F4-carved-by-card-ruling-b-2026-09-28-2022
product file PINNED: services/originate/src/routes/certifications.ts (ticket names 1: ['services/originate/src/routes/certifications.ts'])
fix shape: WEDNESDAY BRIEF (KS-1124.md) — the ticket's fix-shape/decision gates are bypassed; the brief states the change and any decision → 'The exact change'
product services/originate/src/routes/certifications.ts (60650 B, 1427 lines) defect line 471 [pinned (line=)]: 'anchoringStatus,'
reference test PINNED: Blockchain/Dev/services/originate/src/__tests__/ks445-certifications-issue-unstorable-payload.test.ts
test_file PINNED (modify in place): Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts (5970 B) — suggested_test_file = it
  named sites: no '## Where' section — checklist empty (A3b passes vacuously)
  expected '+' lines from the brief's edit blocks: 32 (A3c)
  red cells declared by the brief: 2 ['RED KS-1124 F4-1', 'RED KS-1124 F4-2']
  prompt source: WEDNESDAY BRIEF /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1124-F4/KS-1124.md (19253 chars) — the ticket description is NOT the prompt
  suggested_test_file = the brief's `## The test` File: line Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts (== the title slug)
contract: key set == KS-871 input (top-level, ticket, repo)
wrote /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw0929/bi_f4/input.json (101230 B; ~25308 prompt tokens at 4 B/token — num_ctx 65536 leaves ~40228 for the answer)
```
The first run (without `started_ok=`) was REFUSED by the state gate: **KS-1124 is In Progress**, PR #1324 (O1) merged. See doubt 1.

## The round command (NOT run)
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/bw0929/round_0d156d12.sh KS-1124-F4 KS-1124 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1124-F4 - product=Blockchain/Dev/services/originate/src/routes/certifications.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks445-certifications-issue-unstorable-payload.test.ts test_file=Blockchain/Dev/services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts line=471 ctx=65536 started_ok=O1-merged-1324_F4-carved-by-card-ruling-b-2026-09-28-2022
```
**Round counter:** first brief for F4. One rebrief is allowed, then it goes to the cloud.

## UNMEASURED / doubts for Wednesday
1. **`started_ok=` is my assertion, not a measured fact.** KS-1124 is In Progress (O1 merged as #1324). I could not see the live lanes. Confirm nobody holds F4, or drop the round.
2. **Originate's own vocabulary is `'anchor_failed'`, not `'failed'`.** `documents.ts:1098` and `:1532` serve `anchored: status !== 'anchor_failed'`, and the anchor-retry route (`:1338`) refuses "already anchored" unless `status === 'anchor_failed'`. With the ruled literal `'failed'`, a derived document (the blob is copied at `certifications.ts:526`) still reads `anchored: true` on those originate reads and is not retryable. That is the same as at the tip (no status), so nothing gets worse. `'anchor_failed'` would ALSO reach off-chain-only through the gateway (measured) AND fix those originate reads. The brief follows Kam's literal wording. Whether he meant the literal is worth one line to him.
3. **Records already saved** with the statusless blob are not migrated (the card said so: only option c reached them).
4. Production is unaffected (503 before the blob exists). Whether any client-reachable environment runs originate with a non-production `NODE_ENV` was not measured.
5. No real Postgres: the save is the mocked `saveCertification`. The gateway read was driven with the blob as JSON; no row was written and read back.
6. The open-PR file list I could see (`prfiles.txt`) is from 06:10 on 09-28 and did not name either file. Nothing newer was checked.
7. The round script's run folder name carries the date `2026-09-28` (inherited unchanged from `round_d9ce1403.sh`; only SP/SRC/TIP were changed, as instructed).
