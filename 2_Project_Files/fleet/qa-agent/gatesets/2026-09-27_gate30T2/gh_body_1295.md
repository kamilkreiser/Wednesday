#1295 KS-1337 akto site: take the pre-suite path with fileURLToPath, not URL.pathname
head 0faf41d63a75dfa348ed74ea328701646eea9c49

## BLUF
`systemTest/akto/tests/preSuiteSetup.ts` built the pre-suite step path from `URL.pathname`, which **percent-encodes**. On a checkout whose path contains a space the step resolved to a name that does not exist, and the pre-suite step failed for a reason nothing in the output explained. It now uses `fileURLToPath` — the same idiom the k6 runner site adopted.

Refs KS-1337

## What changed
Two files, +81/−1.

- `systemTest/akto/tests/preSuiteSetup.ts` (+2/−1) — the `fileURLToPath` import, and `:36` becomes `fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url))`.
- `systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts` (+79, new) — one red-first cell and two controls.

**Site 2 of 3.** The playwright site (`systemTest/playwright/global-setup.ts`) is untouched, so the ticket stays open.

## Provenance
Produced by the local model under a rung-4 brief and **re-verified by this seat**. The diff block is **byte-identical to the brief's golden AND to the run's canonical patch** — 92 lines, 4,471 B, sha256 `0714d333dccdbeddc1920b45fb755e6e46d6ec35f160b809bae7ba629dba1ecb`, `cmp` rc 0 against both.

⚠ **There are two goldens under similar names and I checked which one applies rather than assuming:** `briefs/KS-1337.golden/KS-1337.golden.diff` (4,437 B) does **not** match this block — it belongs to the k6 runner site. The matching one is `briefs/KS-1337/golden/KS-1337-akto.golden.diff` (4,471 B).

Strict `git apply --check -p1` per section at `3f70224a069b`: rc 0, no `--recount`, no fuzz. **Both tamper controls fire:** `pathname`→`pathnameZZ` on the product section rc 1; and for the new-file section, where a path tamper would *not* fire (a new file applies at any path), a corrupted hunk count `@@ -0,0 +1,79 @@`→`@@ -0,0 +1,999 @@` rc 128 "corrupt patch".

**The rung-4 caveat from the hold record, repeated rather than buried:** the brief quoted the k6 site's whole product expression and both hunk headers, so this measures *adapting* a quoted pattern, not deriving the fix. It is not a clean rung-4 result.

## Test Evidence
Run by the author, locally, in this worktree at head `0faf41d63a75dfa348ed74ea328701646eea9c49` (base `3f70224a069b`). `systemTest/akto` is a **standalone package**, not a `Blockchain/Dev` workspace member; `npm ci` was run in it.

**Touched:** `systemTest/akto/tests/preSuiteSetup.ts`, `systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts`

**Ran:**
- **RED (cell alone, product reverted — revert confirmed by blob id):** `Tests: 1 failed | 2 passed (3)`. The failure is the declared cell, `RED KS-1337 akto: from a checkout path WITH spaces the step is the real pre-suite file, not a percent-encoded one`. Both controls stayed green, including the one that drives a path **without** spaces — so the cell distinguishes the defect rather than failing everywhere. 0 startup/load errors.
- **GREEN (both files):** `Tests: 3 passed (3)`, after restoring the product **verified byte-identical by sha256**.
- **akto unit suite (`vitest run --config vitest.unit.config.ts`):** **bare 69 files / 1233 tests passed**, **patched 70 files / 1236 tests passed**. 0 new reds; the +3 is this cell.
- **`npm run lint` (the package's own: `tsc --noEmit && eslint . && stylelint`):** **rc 0 at BOTH trees.**
- **`npm run format:check` (prettier):** **rc 0 at BOTH trees** — "All matched files use Prettier code style!". This is run explicitly because it is exactly where the k6 site's raise stopped: `tsc` green is not lint green, and lint green is not format green.
- **Push gate — and this is the part to read carefully.** This branch touches **no `Blockchain/Dev` path**, so the pre-push hook's platform preflight **did not run**. What ran, in full, is: `[format-gate] systemTest/akto — format:check OK` and `[format-gate] 1 package(s) checked, 0 skipped, 0 failed`.
  **No fleet STOP count is quoted here, because none was produced.** Measured, not assumed: `pre_push_hook_base`, `run_shell_suites`, `shell suites:`, `PREFLIGHT` and `code guards` each appear **0 times** in this push's log, while the same greps find them **4 / 1 / 4** times in my `Blockchain/Dev` push earlier tonight. A missing gate is not a passing gate.
- The hook also noted that the local `develop` ref is behind `origin/develop` and that it ignored the stale ref for base selection, consulting `origin/develop` instead. That is expected: this seat never pulls the shared checkout.

**NOT run / NOT covered:**
- **No platform preflight at all** on this push (see above) — no shell suites, no code guards, no legs.
- No akto scan, no Docker, no MongoDB: only the unit config ran. The security/PR/pre-merge akto suites need the stack and were not run.
- **The playwright site is untouched**, and so is the ticket's "Done means 2" CLI-level cell.
- No deploy of any kind.
- The fix is verified by a unit cell that constructs a spaced path; it is **not** verified by running the real pre-suite step from a genuinely spaced checkout.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in.
- Foreign keys un-hyphenated in title, body and commit message.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

