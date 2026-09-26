#1296 KS-1346 part A: log a non-Error throw from systemErrors fail500 with inspect
head eff979b3d493b973aaa4f91defe2c58f960c3f11

## BLUF
`fail500` in `routes/systemErrors.ts` rendered a caught value with `String(err)` when it was not an `Error`, so a thrown **plain object** reached the log as `[object Object]` and its content was lost. It now uses `inspect(err)`. The 500 **body** was already constant, so this changes only what is **logged**.

Refs KS-1346

## ⚠ READ THIS BEFORE MERGING — what this change widens
The gate asked whether inspecting a thrown object can put a secret or PII field into the log. **It can, and nothing on this path redacts it.** I measured both halves:

1. **The rendering.** For a thrown object `{ code, password, apiKey, email }`: the tip logs `"[object Object]"`; this head logs `"{ code: 'P0001', password: 'hunter2', apiKey: 'sk_live_DEADBEEF', email: 'subject@example.test' }"`. A nested `{ outer: { inner: { ssn: … } } }` likewise logs the SSN. The `Error`, `string` and `null` paths are byte-for-byte unchanged.
2. **The sink.** `systemErrors.ts` imports `logger` from `../utils/logger` (line 18) — the service's own winston logger. I read that module in full (77 lines): **it performs no redaction of any kind, in any environment.** The redacting logger (`packages/shared/src/logger/index.ts`, with `SENSITIVE_KEYS` and `redactValue`) is **not on this path**.

And a nuance that matters if anyone proposes routing this through the shared logger as a mitigation: **that redactor keys off the field NAME**, and after `inspect()` the secret is inside a *string value* under the key `error`. Modelling its rules, a thrown object carrying an SSN and no email **survives redaction**; the flat example above is caught only incidentally, by the unrelated "value contains `@` and `.`" email rule, which then redacts the whole string. So the shared logger would not be a reliable fix either. (That second part is a *reimplementation* of its rules for a hypothetical, not a run of the real module — the load-bearing fact is #2 above, which I measured by reading the actual logger this route uses.)

**This is inherent to the ticket, not a defect in the patch** — the whole point is to stop losing the thrown content, and `[object Object]` has no diagnostic value. But it is a real widening of what reaches log storage on an admin surface, and whether that is acceptable depends on who can read those logs. **That call is not mine, and I have filed no ticket for it.** Part B (`gdpr.ts`) makes the same change on a subject-data surface, where it matters more.

## What changed
Two files, +99/−1.
- `services/originate/src/routes/systemErrors.ts` (+2/−1) — the `inspect` import and the one rendering expression.
- `services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-a-non-error-throw.test.ts` (+97, new).

## Provenance
**Raised from the brief's golden**, which the hold record names as the canonical patch: 111 lines, 6,053 B, sha256 `7002806683950f9c325318954ba6901f540ed780e586b1b414aee72a875fc8f6`.
**The model's own block is NOT byte-identical to it, and I measured the difference rather than repeating the claim:** the model's diff is 112 lines / 6,056 B and differs by exactly **one extra trailing context line** (` }` at line 12) and nothing else. That matches the hold record. My tooling refused the raise until I pointed it at the golden — it will not silently accept a near-match.
Strict `git apply --check -p1` per section at `3f70224a069b`: rc 0, no `--recount`, no fuzz. **Both tamper controls fire:** `String(err)`→`String(errZZ)` rc 1; and for the new-file section a corrupted hunk count `+1,97`→`+1,999` rc 128.

## Test Evidence
Author-run, locally, in this worktree at head `eff979b3d493b973aaa4f91defe2c58f960c3f11` (base `3f70224a069b`). `packages/shared` built.

- **RED (cell alone, product reverted — confirmed by blob id):** `Tests: 4 failed, 7 passed, 11 total`. The four are the A1 rows, one per admin route — `GET /stats`, `GET /`, `PATCH /:errorId/resolve`, `POST /resolve-by-service` — each driven by making that route's own service call reject on a real loopback listener. Zero crash signatures; 11 ran, so not a load failure.
- **Control A5 makes A1 non-vacuous:** it asserts that `String()` of the thrown object really is the lossy text. Controls A3 and A4 pin that the `Error` and `string` paths log exactly what they logged before.
- **GREEN:** `Tests: 11 passed, 11 total` after a sha256-verified restore.
- **originate suite, serial:** **bare 962 passed / 0 failed (82 suites)**, **patched 973 passed / 0 failed (83 suites)**. 0 new reds; +11 is this cell.
- **`tsc --noEmit` over a program PROVEN to contain both touched files** (`exclude: []`, **715 files**, each present once by `--listFilesOnly`) → **rc 0, 0 errors**.
- **`packages/shared`:** 48 files, **945 passed**.
- **ESLint (`npm run lint`) at BOTH trees:** **22 problems (0 errors, 22 warnings)** each; **0 lines name either touched file** at either tree. Control: a planted `debugger` gives a `no-debugger` error and rc 1.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 of 60** · `OK — 13 code guards passed` · zero `FIXTURE BUILD FAILED`.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`

**NOT run / NOT covered:**
- **No assessment of who can read originate's logs**, which is what decides whether the widening above is acceptable. Flagged, not resolved.
- No redaction is added by this change, and none exists on this path.
- No local stack (legs 3, 4, 8), no live sweep, no deploy, no integration/e2e against a real database.
- Part B (`gdpr.ts`) is a separate PR; the same widening applies there on a subject-data surface.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in. Foreign keys un-hyphenated throughout.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

