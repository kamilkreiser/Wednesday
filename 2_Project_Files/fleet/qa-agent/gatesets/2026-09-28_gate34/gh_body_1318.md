#1318 KS-747: declare organizationId as a required query parameter on the keys list
head 62f9a288cf6032263ff183dfdc00ac1b60811f9d

## What this changes

`GET /api/security/keys` requires `organizationId` at runtime, but the **published contract never
declared it**. A generated client had no way to know, and the spec-driven suites could not exercise the
parameter. This declares it — required, `uuid`-format — in the Zod source of truth.

`Refs KS-747` — deliberately not a closing keyword. The gate decides the ticket move.

## Three files, because the contract is GENERATED

| file | change |
|---|---|
| `services/security/src/security.openapi.ts` | **+1** — `request: { query: z.object({ organizationId: z.string().uuid() }) }` |
| `services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts` | **new, +50** |
| `docs/openapi/secuura-api.yaml` | **+7/−0**, **regenerated** |

**The yaml was produced by `npm run generate-openapi` — the repo's own generator — and never
hand-edited.** Without it, `check:openapi` fails, because that script regenerates and diffs.

**Proof it is the generator's output and not a hand edit:** the generated diff's **added-line set is
byte-equal to the brief-writer's companion diff** (7 lines against 7, `equal: True`), at the same hunk
header (`@@ -33995,6 +33995,13 @@`). The two diff *files* differ only in framing — mine carries a
`diff --git` header and git's `paths:` function-context suffix — not in content. A one-character
mutation of the generated added-set does **not** match the companion, so that comparison discriminates.
The regeneration is **+7/−0**: it added the parameter block and reordered or dropped nothing else.

## Test Evidence

**Ran — all by me, in this branch's own worktree at base `ec32c40e2b1e`, `npm ci` and `packages/shared` built**
- **RED-FIRST**, test applied alone with the spec source untouched: **2 failed / 3 passed / 5**. The two
  reds are `A1` (organizationId declared as a REQUIRED query parameter) and `A2` (it is a uuid-format
  string).
- **GREEN**, spec hunk applied: **5 passed / 5**.
- **Whole `services/security` suite: 24 files / 252 tests / 0 failed** (`rc 0`). "No NEW red" rests on
  **0 failed**, not a delta.
- **`npm run check:openapi`: rc 0** — the generator's `--check` mode plus `check:spec-examples`
  (405 example blocks, every published example resolves to the fixture set). This is the gate the third
  file exists for, so it is the one that matters most here.
- **`tsc`, both ways, because one of them proves nothing on its own:**
  - the package's own `tsc --noEmit`: **rc 0, 0 errors** (its tsconfig excludes `src/__tests__`);
  - an **including** program (`exclude: []`, 441 files, `--listFilesOnly` confirms the new cell appears
    once and `security.openapi.ts` once, bogus-filename control 0): **2 errors, neither in my files.**
    I measured them at base with my test held aside, and the error set is **identical at base and at
    this head** — `ks952-rate-limit-scope-route.test.ts:249` (TS2339) and
    `ks952-rate-limit-scope.test.ts:313` (TS1343 `import.meta`, itself an artefact of the `exclude: []`
    module setting). **Both pre-existing; this PR adds none.**

**NOT run**
- ⚠ **`services/security` has no `lint` script.** So there is no package lint to report, and I am not
  implying one passed.
- The **served** spec (`/api/docs/openapi.json`) and the **Schemathesis `pr` tier** were not run — no
  local stack. The ticket itself calls the Schemathesis outcome a prediction.
- The `services/security` integration path and the other three platform suites (Akto · Playwright ·
  Performance/k6): not run, no stack.

**Migrations + config**
- **None.** One declaration in the Zod source, its regenerated spec output, and a new test file.

## NOT COVERED (from the brief's own OPEN DOUBTS)

- The served spec and the Schemathesis `pr` tier are unverified here (above).
- **API keys sit next to a credential surface.** This change is **spec-only** — no handler, no auth
  code — which is why it was routed as it was. It changes what the contract *declares*, not what the
  endpoint *enforces*; the runtime requirement already existed.

⚠ One line of that list is **stale and I am not carrying it**: *"No Spark round was run. This is a brief
and a golden only."* The run exists — `checker.out` records **9 PASS / 0 FAIL**, its A4/A5 figures
(2/5 red, 5/5 green) are exactly what I reproduced, and the run's `patch.diff` is byte-identical to the
golden. The README was written before the round, as with parts C and D. Reported, not dropped.

## Provenance

Patch produced by the local model (Spark) under a Wednesday brief, then re-verified here: the READY's
fenced diff block is **byte-identical** to the checker's canonical `patch.diff` (3325 bytes both; a
one-character mutation control differs), both `section_*.opts` name the plain `.diff`, and both sections
strict-apply clean at `ec32c40e2b1e`. Every figure above is one I measured.

## Push gate (in-hook preflight, from this push's own raw log)

`pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** ·
`run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`OK — 13 code guards passed.` · `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`^FIXTURE BUILD FAILED` **0**. `gatelines32`: **MATCHES the declared fleet STOP condition**. Push rc 0;
the branch head at origin was re-read afterwards and equals the commit (`62f9a288cf60…`).

