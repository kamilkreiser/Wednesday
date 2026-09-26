#1297 KS-1346 part B: log a non-Error throw from gdpr fail500 with inspect
head f6565fa66532fa0a60e968ae22f664c71e22da08

## BLUF
`fail500` in `routes/gdpr.ts` rendered a caught value with `String(err)` when it was not an `Error`, so a thrown **plain object** reached the log as `[object Object]` and its content was lost. It now uses `inspect(err)`. The 500 **body** was already constant, so this changes only what is **logged**. Companion to part A (`systemErrors.ts`).

Refs KS-1346

## ⚠ READ THIS BEFORE MERGING — and it matters more here than on part A
This is the same rendering change as part A, on a **subject-data surface**. I measured both halves again for this file:

1. **The rendering.** A thrown object logs its contents where it previously logged `[object Object]` — including fields such as `password`, `apiKey`, `email`, and a nested `ssn`. The `Error`, `string` and `null` paths are byte-for-byte unchanged.
2. **The sink.** `gdpr.ts:22` imports `logger` from `../utils/logger` — the service's own winston logger, which performs **no redaction of any kind, in any environment**. The redacting logger (`packages/shared/src/logger/index.ts`) is not on this path; and because it keys off the **field name**, it would not reliably help even if it were, since after `inspect()` the content sits inside a string value under the key `error`.

On these routes the object a repository or service throws can plausibly carry **the data subject's own identifiers**. The change is still correct for the ticket — `[object Object]` has no diagnostic value and losing the content is the defect being fixed — but it widens what reaches log storage on the one surface where that is most sensitive. **Whether that is acceptable depends on who can read originate's logs; that is not this seat's call, and no ticket has been filed for it.** It is raised here and mailed so the gate can decide with the measurement in hand.

## What changed
Two files, +97/−1: `services/originate/src/routes/gdpr.ts` (+2/−1) and the new cell `ks1346b-gdpr-fail500-logs-a-non-error-throw.test.ts` (+95).

## Provenance
Raised from the brief's golden: 5,869 B, sha256 `6530f63a6e8814fdcef4be02211ff5dc350b1f7991e309da37cb96f8820da08e`, **`cmp` rc 0 against BOTH the golden and the run's canonical patch** (unlike part A, where the model's block carried one extra context line). Strict `git apply --check -p1` per section at `3f70224a069b`: rc 0, no `--recount`, no fuzz. **Both tamper controls fire:** `String(err)`→`String(errZZ)` rc 1; new-file hunk count `+1,95`→`+1,999` rc 128.

## Test Evidence
Author-run, locally, at head `f6565fa66532fa0a60e968ae22f664c71e22da08` (base `3f70224a069b`). `packages/shared` built.

- **RED (cell alone, product reverted — confirmed by blob id):** `Tests: 4 failed, 7 passed, 11 total` — the four B1 rows, one per route: `GET /dsr/pending`, `GET /retention`, `GET /deletion-log`, `GET /consent/check`, each driven by making that route's own service call reject on a real loopback listener. Zero crash signatures; 11 ran.
- **Control B5 makes B1 non-vacuous** (`String()` of the thrown object really is the lossy text); B3 and B4 pin the `Error` and `string` paths as unchanged.
- **GREEN:** `Tests: 11 passed, 11 total` after a sha256-verified restore.
- **originate suite, serial:** **bare 962 / 0 failed (82 suites)**, **patched 973 / 0 failed (83 suites)**, 0 new reds.
- **`tsc --noEmit` over a program PROVEN to contain both touched files** (715 files, each once by `--listFilesOnly`) → rc 0, 0 errors.
- **`packages/shared`:** 945 passed.
- **ESLint at BOTH trees:** 22 problems (0 errors, 22 warnings) each; 0 lines name either touched file. Control: planted `debugger` → `no-debugger` error, rc 1.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `..._fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 of 60** · `OK — 13 code guards passed` · zero `FIXTURE BUILD FAILED`.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`

**NOT run / NOT covered:**
- **No assessment of who can read originate's logs** — the question above, unresolved by design.
- No redaction added; none exists on this path.
- No stack (legs 3, 4, 8), no live sweep, no deploy, no integration/e2e against a real database.
- No cell asserts that a *real* GDPR repository error carries subject identifiers — the cells throw a synthetic object. The widening is demonstrated at the rendering level, not by capturing a production throw.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in. Foreign keys un-hyphenated throughout.
- Part A is a separate PR on `systemErrors.ts`; the two touch different files and do not overlap.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

