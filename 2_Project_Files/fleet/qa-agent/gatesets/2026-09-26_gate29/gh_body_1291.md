#1291 KS-1337: take the k6 pre-suite path with fileURLToPath, not URL.pathname
head 2c9022c519bd26e9b58acddeed817f4413d92449

## BLUF

`systemTest/performance/runner/cli.ts` built the pre-suite step path from **`new URL(...).pathname`**. A URL pathname is **percent-encoded**, so a checkout directory whose name contains a space handed `tsx` a path with `%20` in it and the step died `ERR_MODULE_NOT_FOUND`. **`fileURLToPath` decodes, so the step resolves to the real file either way.**

**This is live on this fleet, not hypothetical:** the QA harness runs from a directory whose name contains a space.

**Scope: one of three occurrences.** The writer measured the pattern **3×** on develop; this PR converts **one**. `Refs KS-1337`, **no closing keyword** — the other two are named under NOT COVERED and the ticket stays open.

## Provenance, stated exactly

- **`runner/cli.ts` is BYTE-IDENTICAL to the local model's (Ornith) product hunk** — sha256 `9a23668c852369b5c0ab8eea172857af9d27eccc4e7506d20fe5331f2ef2a833` after the apply, unchanged by anything I did.
- **The test file is the model's output PLUS the package's own `eslint --fix`** — formatting only, run from the package root with the lint script's own tool. **One hunk, 15 lines, 3,481 → 3,524 bytes**, re-wrapping a single `writeFileSync(probe, [...].join(NL))` call:

```diff
-    writeFileSync(probe, [
-        'import * as url from ' + SQ + 'node:url' + SQ + ';',
-        'import { fileURLToPath } from ' + SQ + 'node:url' + SQ + ';',
-        String(STATEMENT),
-        'export { preSuiteStep, url, fileURLToPath };',
-    ].join(NL));
+    writeFileSync(
+        probe,
+        [
+            'import * as url from ' + SQ + 'node:url' + SQ + ';',
+            'import { fileURLToPath } from ' + SQ + 'node:url' + SQ + ';',
+            String(STATEMENT),
+            'export { preSuiteStep, url, fileURLToPath };',
+        ].join(NL),
+    );
```

**Why that delta exists.** The model's diff was byte-identical to its reviewed golden (87 lines, 4,437 bytes, `cmp` rc 0) — but **the package's own `npm run lint` was rc 1 on it: 6 `prettier/prettier` errors, all in the new cell**, while *both* `tsc` stages passed. That was raised as a STOP rather than silently reformatted, and resolved on an explicit ruling: shipping a package whose own `lint` and `quality` scripts are red would be a regression for every later push, so the formatter's delta is applied and disclosed here instead.

## Test Evidence

**Environment:** worktree detached at develop `179a4f32ec0643689b55a8d7207e63f6ec3d3831`, which it **contains**; `npm ci` in `systemTest/performance` (standalone lockfile, 0 vulnerabilities). Runner: `vitest run --config vitest.unit.config.ts`.

**Touched:** `systemTest/performance` only — the runner plus one new unit cell. No other package.

| check | result |
|---|---|
| strict apply per section at develop | `git apply --check` rc 0 both |
| **RED**, cell alone, product hunk absent | **1 failed / 2 passed / 3** — the declared cell, on its assertion |
| **GREEN**, both files | **3 passed / 3** |
| whole performance unit suite, BARE at develop | **64 files, 1114 tests, 0 failed** |
| whole performance unit suite, PATCHED | **65 files, 1117 tests, 0 failed** — **0 new reds** |
| `npm run lint` (`tsc` ×2 + `eslint`) at this head | **rc 0** |

**The red is the defect, verbatim** — expected `…/Testing Agent MAIN/systemTest/fixtures/pre-suite.ts`, received `…/Testing%20Agent%20MAIN/systemTest/fixtures/pre-suite.ts`.

**The cell builds its own spaced directory rather than trusting the checkout**, which is the reason it can red-prove this at all: it `mkdtemp`s a path containing `Testing Agent MAIN` and resolves from there. Consequently a green run on a space-free checkout is **not** evidence the defect is absent — mine has no space in it.

⚠ **A difference from the harness worth the reviewer's eye.** The harness reported its baseline as `1114 failed=1`; I measure **1114 passed / 0 failed** at develop and **1117 / 0** here. Same totals, different failure counts. The likely mechanism is this very defect: the harness runs under a path containing a space and mine does not, so a pre-existing cell that trips on the spaced path fails there and passes here. **Stated as a hypothesis with a mechanism, not a measurement** — I cannot see that tree's run and have not identified which cell it is.

**NOT run:** no k6 scenario, no gate CLI, no stack — this is a unit-level change and the load scenarios need a running target. Nothing deployed.

**Migrations + config:** none. No migration, no lockfile change, nothing under `.github/`.

## NOT COVERED

- 🔴 **The other two occurrences of the pattern, measured on develop and NOT in this PR:** `systemTest/akto/tests/preSuiteSetup.ts:36` and `systemTest/playwright/global-setup.ts:42`. They are in different packages with their own installs and suites.
- 🔴 **The ticket's "Done means 2" is approximated, not met.** That step asks for a cell that runs **the CLI itself** from a spaced copy. This cell reconstructs the resolution in a probe module instead. It pins the defect and would catch its return, but it does not exercise `runner/cli.ts`'s own process boundary — the probe-vs-DoD gap is stated here rather than claimed closed.
- Which cell fails in the harness's spaced-path environment (see above).

Refs KS-1337

## The push gate — what ACTUALLY ran, corrected

🔴 **I first wrote the platform fleet-STOP figures here as boilerplate. They do not apply to this push and the claim was false; this is the corrected section.** The pre-push hook **filters by PATH**, and this change touches **no `Blockchain/Dev/` path** — only `systemTest/performance/` — so the platform preflight **did not run at all**. There is no `PREFLIGHT` line and no suite counts in the push log, and a missing gate is not a passing gate.

**What did run, verbatim from the push log:**

```
[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the
[pre-push]   stale ref for base selection. (git fetch origin develop:develop
[pre-push]   to refresh it.) origin/develop is still consulted below.
[format-gate] systemTest/performance — format:check OK
[format-gate] 1 package(s) checked, 0 skipped, 0 failed
```

Push rc **0**, taken under `.push-lock-27`.

Two things follow. **The `format-gate` is the gate that governs this package on a push, and it is green** — which also settles the formatting decision above empirically: the model's unformatted cell failed `prettier` under the package's own lint, so shipping it byte-identical would have put this push at odds with the very gate that guards it. And the KS-991 line is expected: this seat never moves the shared checkout's local `develop`, so the hook correctly consults `origin/develop` instead.

