#1301 KS-1349: clear the logger per environment in the ks730c cell and assert the call list
head 3b7e71f461ef4dd789f019cbf07e06be258a31fd

## What this changes

The ks730c C1 loop asserted `mockLoggerError.mock.calls.at(-1)` **with no per-iteration clear**, so calls
accumulated across the `NODE_ENV` rows. An iteration that logged nothing still saw the *previous*
iteration's call at `.at(-1)` — and since every row expects the same route context, the assertion passed
on a stale entry. The loop now clears the mock per environment and asserts the **whole call list**, so
each row has to reach `fail500` for itself.

**One file, +3 / -1, test-only.** The product file is untouched. This is the blindness KS1344 fixed in
the ks1341a cell next door, on the admin-config security guard. `Refs KS-1349`.

**Stacked on KS1334 part B (#1300).** Both PRs edit this file, so this PR's **base is that branch** and
the diff above shows only its own hunk. Its base is retargeted to `develop` once #1300 merges.

## Provenance

Produced by the local model (Spark) under a Wednesday brief, **re-verified by this seat**. The brief's
golden is byte-identical to the run's canonical `patch.diff` (`cmp` rc 0, with a one-token control
proving the comparison discriminates). It applied **strictly** (`git apply --check -p1`, rc 0) at
#1300's head **with no re-anchor**, paired with a hunk-line-count tamper (`+N,999`) that git refused
(rc 128, "corrupt patch"), so the rc 0 is not a check that could not fail. **Wednesday's harness figures
are hers**; every number below is from my own runs. Her figures were taken at develop, where this file
has 19 cells; at my stacked head it has **23**, because #1300 added four.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`

**Ran** — worktree detached at `5bd58f0ebd14` (#1300's head), which CONTAINS develop `94c9c7aa9be7`
(`merge-base --is-ancestor`); `npm ci` 1936 packages; `packages/shared` BUILT.

**The RED is a product TAMPER, and it is a 2×2 — executed, not reasoned.** The tamper makes `fail500`
log only under development (`adminConfig.ts:104`, the only `logger.error(` in the helper, literal count
asserted 1):

| arm | tamper | test | result | the four C1 rows |
|---|---|---|---|---|
| **R0** | no | old | 23 passed / 23 | 4 green |
| **R1** | **yes** | **old** | 4 failed / 19 passed / 23 | **4 GREEN — the blindness, reproduced** |
| **R2** | no | **fixed** | 23 passed / 23 | 4 green |
| **R3** | **yes** | **fixed** | 8 failed / 15 passed / 23 | **4 RED — the fix catches it** |

That C1 is **green in R1 and red in R3** is the whole claim: the old assertion cannot see this tamper and
the new one can. Zero loadfail markers in all four arms. The two part A rows and the two part B rows were
already per-environment, so they red under the tamper in both R1 and R3 — they are not what this change
buys. The tamper was applied to a guarded copy and **restored by content with sha256 asserted identical**
after every arm; the literal-count assertion (`==1`) guards the plant itself.

**Why the ticket's own tamper is not used:** it names "log only under production", but C1's `NODE_ENVS`
has no production row, so under it C1 logs nothing at all and reds at the *old* test too — it does not
discriminate. The development-only tamper is the one that separates the two. (Measured by Wednesday's
brief; I used the tamper it specifies.)

| check | result |
|---|---|
| originate suite **BARE** (stack base) | 84 suites, **983 passed / 983**, rc 0 |
| originate suite **PATCHED** | 84 suites, **983 passed / 983**, rc 0 |
| **NEW reds** (patched failing set minus bare) | **none** — both sets empty. No cells added; an assertion strengthened |
| `tsc` — widened program **proven to contain the test file** | `exclude: []`; test file **1 hit**, control **0** in the package program. **0 errors** |
| `tsc` **positive control** — unused const appended | **exactly 1 error, 1 × TS6133** → the widened program really type-checks this file |
| `eslint src` at **HEAD** / at **BARE** | rc 0 both, 0 errors both |
| lint **control** — planted `debugger;` | rc **1**, 1 × `no-debugger` → lint runs and can fail |
| restore after every control | **sha256 identical** each time |

**Gate lines THIS push printed** (`s-b33-ks1349-3b7e71f461ef-push.out`, parsed per suite block by
exact basename): `pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh`
**6/0** · `run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`^FIXTURE BUILD FAILED` **0** · `OK — 13 code guards passed.` ·
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 need a local stack).
Push rc 0; `ls-remote` confirms the head; 0 orphaned `login_stub` pids.

**Migrations + config:** none. No migration, no `package.json`, no lockfile; the widened tsconfig was
temporary and removed before staging. **Exactly 1 file staged**, and the guard asserted `adminConfig.ts`
is NOT staged — the product file must stay untouched for a test-only change.

**NOT run / NOT covered:**
- **Nothing deployed.** No live or deployed exercise of these routes; unit-level only, through mocks.
- The integration suite was not run (needs a live stack); preflight legs 3, 4 and 8 do not run without one.
- This change strengthens an existing assertion. It does not add coverage for any new route or behaviour,
  and it does not test `fail500` itself — only that each `NODE_ENV` row independently reaches it.
- The `.at(-1)` pattern was checked in this file only; other files may carry the same shape. Not surveyed.

Refs KS-1349

