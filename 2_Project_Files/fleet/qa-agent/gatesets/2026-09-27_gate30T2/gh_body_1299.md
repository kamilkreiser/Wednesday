#1299 KS-1339: name the offending file before the count in the ks1293 CONFIGPINNED cell
head e23557f777a2bafd0b5d8b1d2bdc197eae9a3fcd

## BLUF
The `CONFIGPINNED` cell in the ks1293 hermeticity suite asserted the **count floor before the offender list**. A run that was both one base short *and* carried a real offender therefore failed on the count, and the output named a **number** instead of the offending file. The two assertions are reordered so the offender list fails first and names the file.

Refs KS-1339

## What changed
**Test files only, +65/−1. No product change.**
- `services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts` (+1/−1) — one line **moved**: `expect(offenders).toEqual([])` now runs before `expect(pinned).toBeGreaterThanOrEqual(SUBJECTS.length)`.
- `services/originate/src/__tests__/ks1339-configpinned-names-the-offender-before-the-count.test.ts` (+64, new).

**The count floor is not weakened, and that is asserted rather than claimed:** control A2 drives a scan that is one base short with **no** offender and shows it still fails. Reordering two assertions can silently drop one; A2 is what proves this one did not.

## Provenance
The diff block is **`cmp` rc 0 against BOTH the brief's golden and the run's canonical patch**. Strict `git apply --check -p1` per section at `3f70224a069b`: rc 0, no `--recount`, no fuzz. **Both tamper controls fire:** `offender`→`offenderZZ` rc 1 on the edit; and for the new-file section a corrupted hunk count `+1,64`→`+1,999` rc 128 (a path tamper would not fire — a new file applies at any path).

## Test Evidence
Author-run, locally, at head `e23557f777a2bafd0b5d8b1d2bdc197eae9a3fcd` (base `3f70224a069b`). `packages/shared` built.

- **RED (new cell alone, the ks1293 edit reverted — revert confirmed by blob id):** `Tests: 1 failed, 3 passed, 4 total`. The failure is the discriminating case: `RED KS-1339 A3: a scan with one offender and one base short fails FIRST on the offender list, naming the file`. The three controls stayed green — A0 pins the shape of the CONFIGPINNED cell's own assertions, A1 a clean scan, **A2 the count floor**. Not a load failure: 4 ran, 0 crash signatures.
- **GREEN (both files):** `Tests: 14 passed, 14 total` after a sha256-verified restore.
- **originate suite, serial (`jest --runInBand`):** **bare 962 passed / 0 failed**, **patched 966 passed / 0 failed**. 0 new reds; the +4 is this cell.
- **`tsc --noEmit` over a program PROVEN to contain both touched files** (`exclude: []`, **715 files**, each once by `--listFilesOnly`): **rc 0, 0 errors**, and **0 errors name either touched file**.
- **`packages/shared`:** 48 files, **945 passed**.
- **ESLint (`npm run lint`) at BOTH trees:** **22 problems (0 errors, 22 warnings)** each, identical. Control: a planted `debugger` in the new cell gives `no-debugger` and rc 1.
- **Push gate — only what THIS push printed:** `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 of 60** · `OK — 13 code guards passed` · zero `FIXTURE BUILD FAILED`.
- **Preflight:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`

**NOT run / NOT covered:**
- This changes **only the order in which two existing assertions fail**. It does not widen what CONFIGPINNED detects, and no cell here asserts that the scanner itself finds any *new* class of offender.
- The `MANIFEST-DRIFT` cell in the same file is untouched.
- No local stack (legs 3, 4, 8), no live sweep, no deploy, no integration/e2e.
- The new cell exercises the scan through fixtures; it does not run the real hermeticity scan over the whole suite directory to confirm ordering there.

## Review notes
- Base `develop` `3f70224a069b`, fast-forward. No merge-in.
- Foreign keys un-hyphenated in title, body and commit message (`ks1293`).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

