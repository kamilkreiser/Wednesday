#1256 KS-1159: close the ks1061 mock guard's three blind spots (F-931-G1)
head 5a41ed7fea96ab77ed1dc263ae0c7d25c9846440

## BLUF
Test-only. The guard that makes a partial `@secuura/shared` mock *"impossible rather than remembered"* was a text scanner with **three blind spots**, and a factory in any of them shipped a partial mock with the guard **green**. All three readers widened, with one arm per blind spot proved **two-sided** — caught by the new guard *and* missed by the old one.

## The three blind spots (L3b gate record F-931-G1)

| blind spot | why it was invisible |
|---|---|
| **quote style** | the pattern required a single-quoted module name, so a double-quoted factory matched **neither** pattern — `declared` and `viaHelper` were both 0, `declared !== viaHelper` was false, no offender reported. Nothing pins quote style: no prettier config, no `quotes` rule in `eslint.config.mjs`. |
| **`jest.doMock`** | only `jest.mock` was matched, and `doMock` registers a factory just the same |
| **non-recursive walk** | `readdirSync` alone, while jest's own `testMatch` is recursive — a factory in a `__tests__` subdirectory was never read |

The `VIA_HELPER` require path also had to accept `../helpers/…`. Once the walk is recursive, a **legitimate** nested factory requires the helper one level up, and leaving that out would have turned every compliant nested file into a false offender — a new false-positive class introduced by the fix for a false-negative one.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks1061-shared-mock-completeness.test.ts`. 1 file, +29 −8. Test-only; no runtime file.

**Ran (all on this head, base `77c6426b9`):**
- `npx jest --runInBand` (originate): **869 passed / 869, 74 suites / 74**, rc 0 — unchanged from the baseline at the same commit, as expected: this widens existing readers and adds no cell. The guard's own three cells all still pass, and it still counts **21** factories, well over its own non-vacuity floor of 10.
- **One arm per blind spot, each TWO-SIDED.** Each arm plants a fixture carrying a non-helper factory in that shape, then runs both guards:

  | arm | new guard reports it | old guard reports it |
  |---|---|---|
  | T6b a double-quoted factory | **yes (red)** | no — blind |
  | T6c a `jest.doMock` factory | **yes (red)** | no — blind |
  | T7 a factory in a subdirectory | **yes (red)** | no — blind |

  The "old" side is the **real pre-edit file**, copied in under another name and executed — not a re-implementation of its regexes, which would only have proved my reading of them. Both guards were confirmed green with no fixture planted first, so a red is attributable to the fixture. Every fixture and the subdirectory removed afterwards and their absence asserted; the new guard reads 0 failures with everything gone; the working tree carries **0 untracked files** at commit time.
- `npm run lint` (= `eslint src`): rc 0.
- `npx tsc --noEmit`: rc 0. Re-run with `exclude: []` and this file asserted present in the program (705 files, `--listFilesOnly`) because the project tsconfig excludes `src/__tests__`: rc 0.
- `npm test -w packages/shared`: 47 files / **928 tests** passed, rc 0.
- Push: rc 0. `pre_push_hook_base` 28/0, `pre_push_hook_base_fixture_guard` 6/0, shell suites 60 passed / 0 failed / 0 skipped (of 60). No `FIXTURE BUILD FAILED`.

**Worth knowing before the next edit to this file:** the guard **scans its own source**. Writing the offending shape into its doc comment makes it report *itself* — my first draft did exactly that and went red on `ks1061-shared-mock-completeness.test.ts (1 factories, 0 via helper)`. The comment now follows the convention the helper's own docstring already states: omit the scope sigil in prose. That is a live constraint on this file, not a style note.

**NOT run:**
- **Preflight INCOMPLETE — 12/15 legs ran, 3 SKIPPED, nothing failed:** legs **3**, **4** and **8**, each `SKIP — local stack not up on http://localhost:6882`. A skip is not a pass. None bears on a test-only change, but they did not run.
- The guard is not extended to the **other** services' suites. It scans this service's `__tests__` only, exactly as before; whether the same factories exist elsewhere is unmeasured here and outside this ticket.
- No behavioural change, so no integration or e2e cell.

**Migrations + config:** none.

Refs KS-1159

🤖 Generated with [Claude Code](https://claude.com/claude-code)

