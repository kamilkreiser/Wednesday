#1293 KS-1344: clear the logger per environment in the ks1341a cell and assert the call list
head 0ddffb6a52dbfa89ab71d7297c737c8b4d8722fd

## BLUF
The `ks1341a` A1 rows loop over four `NODE_ENV` values but never cleared the logger mock between iterations, and asserted only `calls.at(-1)`. A `fail500` that logged in one environment and not the others therefore left the last call in place and the assertion passed for **every** iteration. This closes that blindness.

Refs KS-1344

## What changed
**Test-only. One file, one hunk, +3/−1. No product bytes change.**

`services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts`, at `@@ -112,7 +112,9 @@`: `mockLoggerError.mockClear()` at the top of the per-environment loop, and `expect(mockLoggerError.mock.calls.at(-1)).toEqual([...])` becomes `expect(mockLoggerError.mock.calls).toEqual([[...]])`.

## Provenance
The patch raised here is **the brief's golden** — 13 lines, 944 B, sha256 `59e1bf3bde8cbbdb7a82be57ea2de1c656a57d938fd1631ad6e14202324c8803`. The local model's own output differs from it in exactly two ways and no others: a function-name suffix on the hunk header, and one extra trailing context line `  });`. **Both produce a byte-identical file** — I measured the applied result at sha256 `d999b07834ad163f…`, from an original at `fe5e989ff9c19d04…`, which are the two values the hold record states.

The pre-image blob is `3318cccbca3f7438…` at **both** `179a4f32ec06` (the hold base) and `3f70224a069b` (this base), so the base move did not touch it. Strict `git apply --check -p1` at `3f70224a069b`: rc 0, no `--recount`, no fuzz. Control: `.at(-1)` → `.at(-2)` is refused, rc 1, "patch failed … :112".

## Test Evidence
Run by the author, locally, in this worktree at head `0ddffb6a52dbfa89ab71d7297c737c8b4d8722fd` (base `3f70224a069b`). `packages/shared` built.

**Touched:** `services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts`

**Ran:**
- **GREEN:** the whole `ks1341a` file at this head — `Tests: 8 passed, 8 total`.
- **RED — the discriminating 2×2, the point of the ticket.** The change is test-only, so the red comes from a **product tamper**: make the `fail500` helper (`routes/webhooks.ts:563`, exactly 1 occurrence, re-counted) log only under `NODE_ENV === 'production'`.

  | tree | assertion | result |
  |---|---|---|
  | **this head** (whole call list) | `expect(mockLoggerError.mock.calls).toEqual([[…]])` | **2 failed, 6 passed of 8** — the two A1 rows, `A1 GET /` and `A1 POST /` |
  | **the tip** (`.at(-1)`), *same tamper* | `expect(mockLoggerError.mock.calls.at(-1)).toEqual([…])` | **8 passed, 0 failed — completely blind** |

  The difference is **exactly the two A1 rows**. A2 and all four controls stay green at both trees, so A2 does not discriminate this defect either — A1 is the row that carries it. The tip revert was confirmed by blob id before the second run, and the tamper was verified still in place. Restored by content, verified by sha256.
- **originate suite, serial (`jest --runInBand`):** **bare 962 passed / 0 failed (82 suites)**, **patched 962 passed / 0 failed (82 suites)**. Equal counts are correct here: the change adds no cell. 0 new reds.
- **`tsc --noEmit` over a program PROVEN to contain the file:** the service tsconfig excludes `src/__tests__`, so a config extending it with `exclude: []` was used — **714 files, the file present (1 occurrence, `--listFilesOnly`)** → **rc 0, 0 errors**.
- **`packages/shared` (vitest):** 48 files, **945 passed**, rc 0, 0 startup errors.
- **ESLint, the package's own `npm run lint`, at BOTH trees:** tip **22 problems (0 errors, 22 warnings)**, head **22 problems (0 errors, 22 warnings)**; **0 lines name the touched file at either tree**. Control: a planted `debugger` in that file gives `no-debugger` **error** at `:177` and rc 1, so lint does see it.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `OK — 13 code guards passed` · zero lines starting `FIXTURE BUILD FAILED`.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack not up).

**NOT run / NOT covered:**
- No local stack, so preflight legs 3, 4 and 8 did not run; no live sweep. This change is **test-only**, so it carries no runtime behaviour of its own.
- No deploy of any kind.
- No integration/e2e against a real database.
- The A2 rows are left as they are: this ticket is about A1's per-iteration blindness, and the same tamper leaves A2 green at both trees — whether A2 should also assert a whole call list is a separate question, not decided here.

## Review notes
- Base is `develop` at `3f70224a069b`; a fast-forward on it. No merge-in.
- Foreign keys are un-hyphenated in the title, body and commit message (`KS1341`). The cell titles in the
  touched file carry the part-A ticket key hyphenated as a prefix; that is **file content** and is unchanged.
  This body therefore names the rows short (`A1 GET /`, `A1 POST /`) instead of quoting the full titles, so no
  hyphenated foreign key appears here — the alternative was to misquote a test name, which is worse.
- Closes note N-1288-2 from the part A gate.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

