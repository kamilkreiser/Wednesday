TASK: code_patch

The INPUT is a JSON object describing ONE defect ticket and the repository
state it must be fixed in:

- `ticket` — identifier, title, description (verbatim; it names the fix shape).
- `repo` — pinned `tip` SHA, `repo_subdir`, `service_dir`, the test runner and
  the TypeScript settings that apply.
- `product_file` — the ONE product source file you may change (path from the
  repo root). Its FULL current content is in `files[product_file]`.
- `defect_line` — the line (number + text) the ticket is about.
- `test_dir` — the ONLY directory in which your test file may live.
- `suggested_test_file` — the path to use for a NEW test file.
- `reference_test_file` + `reference_test_note` — an EXISTING test file (full
  content in `files[...]`) that shows how this repo drives the same route
  in-process with `vi.mock` stubs. It is a template to copy the mock shape
  from. You must NOT modify it.

Produce a fix for the ticket as ONE unified diff, and nothing else.

HARD CONSTRAINTS (a mechanical checker enforces every one; a violation is a
failed task, not a style point):

1. Output exactly ONE fenced code block, opened with ```diff and closed with
   ```. No prose before it, no prose after it, no second block.
2. The diff is `git apply -p1` applicable from the repo root at the pinned
   tip: `--- a/<path>` / `+++ b/<path>` headers, `@@` hunks, context lines
   copied EXACTLY (byte for byte, including indentation) from the file
   content in the input. A new file uses `--- /dev/null` and
   `+++ b/<path>` with a single `@@ -0,0 +1,N @@` hunk where every line is
   prefixed `+`.
   DIFF MECHANICS (attempt 1 failed here — both errors below were made):
   2a. A context line is ONE space followed by the source line UNCHANGED.
       If the source line is `  const user: User = {` (2-space indent) the
       context line is ` ` + `  const user: User = {` — three leading
       spaces in total, never more. Do not re-indent context lines.
       Take the `-` line's text from `defect_line.text` verbatim.
   2b. In `@@ -a,b +c,d @@`, b MUST equal the number of lines in the hunk
       that start with ' ' or '-', and d the number that start with ' ' or
       '+'. Count them. A wrong count makes git read the NEXT file's
       `--- /dev/null` header as a deletion line and the whole patch is
       rejected. Prefer a small hunk: 3 context lines above, the one `-`
       line, the one `+` line, 3 context lines below → `@@ -N,7 +N,7 @@`
       where N is the line number of the first context line.
   2c. For the new test file, N in `@@ -0,0 +1,N @@` is the exact number
       of `+` lines. Count them.
3. The diff touches EXACTLY two files: `product_file`, and ONE test file
   under `test_dir` (new at `suggested_test_file`, or an extension of an
   existing file in `test_dir` other than the reference file). No third
   file. Never touch package.json, lockfiles, configs, or the reference
   test file.
4. The test file must be RED at the current tip (its KS-named cell fails
   because the defect is present) and GREEN once the product hunk is
   applied. State in the test's `it(...)` title which cell is the red-first
   one, e.g. `it('🔴 KS-806 — ...')`. Include at least one CONTROL cell that
   passes both before and after (proves the harness reaches the code).
   The checker applies the test hunk ALONE first (must fail with at least
   one failed assertion — a file that fails to load counts as a load error,
   not a red), then the product hunk (must pass).
5. The product change is MINIMAL and DETERMINISTIC: only the lines the
   ticket's fix shape requires, using imports the file ALREADY has. No new
   dependencies, no refactors, no renamed symbols, no changed behaviour
   outside the defect. Keep existing comments; a short `// KS-<n>:` comment
   on the changed line is welcome.
6. TypeScript must compile under the repo's stated settings (strict,
   noUnusedLocals, noUnusedParameters). Do not leave unused imports,
   variables or parameters in either file. vitest globals are available but
   importing `{ describe, it, expect, beforeAll, afterAll, beforeEach, vi }`
   from 'vitest' is the repo's precedent — follow it.
   6a. Every identifier the test uses must be imported or declared IN the
       test file. `vi.mocked(userRepo.createUser)` without an
       `import * as userRepo from '../repositories/userRepo'` is a
       ReferenceError at runtime (attempt 1 did this). Simpler and
       preferred: capture inside the `vi.mock` factory itself — declare a
       `vi.hoisted(() => ({ created: [] as Array<{ email: string }> }))`
       state and have the mocked `createUser` push into it.
   6b. Follow `reference_test_note` literally: for the KS-named cell the
       `auth_find_user_by_wallet` query mock must return `{ rows: [] }` (so
       the CREATE branch runs — an existing row means `createUser` is never
       called and there is nothing to compare), and the challenge row's
       `wallet_address` must equal the address of the CURRENT request (the
       handler rejects a mismatch with 400), so keep the current address in
       the hoisted state and set it before each request.
7. Where the input lacks a fact you need, write `UNKNOWN` in a comment
   rather than inventing an API, a path, or a value.
8. The whole test suite of the service must stay green: do not change any
   exported symbol, route, status code, or response shape the existing
   tests assert.

Fix shape for a synthetic-identifier collision (the KS-806 class): derive the
synthetic local-part from a stable hash of the WHOLE input value, e.g.
`crypto.createHash('sha256').update(walletAddress).digest('hex').slice(0, 24)`,
so that two distinct inputs can no longer map to one identifier. Keep the
`@wallet.local` domain so nothing that keys on the suffix changes.

Output the ```diff block now.
