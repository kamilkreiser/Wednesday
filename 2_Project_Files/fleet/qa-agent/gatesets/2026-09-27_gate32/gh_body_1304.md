#1304 KS-1227: pin a hit-only witness in the ks1072 anchor-store cells and clear its listener
head c8233156f0912ec63773e6261cd6926dbce9de7f

Refs KS-1227

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** The harness's own figures are Wednesday's and are quoted as hers below; every number under "My measurements" I measured in this run.

## What changes

Two edits in one api-gateway test file, **in place, no product change**:

1. **`postTier2`'s anchor-store listener is detached in a `finally`.** Previously the `off('request', …)` sat after `await res.json()`, so an early `expect(res.status).toBe(200)` red left the listener attached for the rest of the file. The status read moves inside the `try`, so a red still reaches the detach.
2. **Two new cells.**
   - **R1** pins the counting rule **as merged**: the witness counts *every* request the stub anchor store receives, so a hit-only URL filter in the helper's own listener reds here. It drives the product's live chain scan (which reads `ANCHORING_SERVICE_URL` per request) to make a real second, non-hit request reach the stub, scoped to the one cell by `vi.stubEnv` / `vi.unstubAllEnvs` in a `finally`.
   - **R2** pins that a status red inside `postTier2` still detaches, leaving exactly one listener.

**R1 pins the counting rule AS MERGED; the keep-vs-filter decision stays open on the ticket.** The ticket offers a choice ("either keep and say so in the comment, or filter by this document's path"); that is decision-shaped and is not taken here. If the owner later rules "filter by path", R1's expectation flips and must be rewritten in that change.

**Not covered, stated rather than implied:** the optional reword of the `:128` witness message is left for the tier-1 half, as the ticket allows. The cells pin the helper's own listener accounting; they do not pin the tier-1 selector path.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**. Paired with a control that must fail: the same section with a corrupted hunk line count (`@@ -115,14` -> `@@ -115,999`) is **refused, rc 128, "corrupt patch at line 26"** — so the rc 0 on the real section is a measurement and not a check that cannot fail. Result: 1 file, **+24 / -8**.

**RED — a product tamper, since this change is test-only.** Tampered `services/api-gateway/src/routes/verification.ts:585` in my worktree only, the anchor asserted to occur **exactly once in that file** first, sha256 before and after proving the tamper landed:

```
-    const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
+    const anchoringBase = 'http://anchoring:4005';   // no second request reaches the stub
```

- **1 failed / 7 passed of 8**, and the single failure is **R1, on its assertion**, not on a crash: vitest reports `AssertionError: expected 'no red' to contain …` where the expected string is the helper's tier-2 witness message. **That message, and the cells' titles, carry a ticket key as file content**, so they are described here rather than pasted: a hyphenated key in a PR body attaches that ticket.
- R2 and the six pre-existing cells stayed green under the tamper, which is what the design predicts: the tamper changes only *where* the scan goes, never the verify's status for a tier-2 answer.
- **Restored by content and verified against the tip blob**, not against a remembered string: on-disk sha256 `7d2d71f055766c21…` equals `git show <tip>:<path>` sha256, and 0 `TAMPER` markers remain.

**GREEN at my head.** The file alone: **8 of 8 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` built, which this package's tests need — without it every cell in this file is *skipped* on a `vite:import-analysis` failure, which is a load failure and not a red):

| | files | tests |
|---|---|---|
| bare (the tip) | 82 | **754** |
| patched (my head) | 82 | **756** |

**0 new reds**; +2 is exactly the two new cells. The revert for the bare run was **confirmed by blob id** (`a4cd8434b355` -> `238f9ded899b`) and asserted to differ from the patched file, so this is not a tree compared against itself; the cell count read 6 bare and 8 patched.

**`packages/shared`** (its guards read service sources by text): **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the test file.** This package's own `tsc --noEmit` is rc 0 and says nothing about this cell: `tsconfig.json` excludes `src/__tests__`, and `--listFilesOnly` shows its program is **491 files with ZERO test files**. Measured instead on a config extending it with `exclude: []`, whose program is **618 files including 82 test files, this one present exactly once**:

- **29 errors at my head, 29 at the tip, and the SETS are byte-for-byte identical** (`file(line,col): error TSxxxx`, sorted) — compared as a set, not as a count. **0 errors name this file.** Control: removing one row from the set makes the comparison fire.

**Lint, the package's own script, at BOTH trees.** `npm run lint` (`eslint src`) is **rc 0, 36 problems, 0 errors, 36 warnings at the tip AND at my head**, and **0 problems in this file** at either tree. Both zeros carry controls: planting a `debugger` and an unused `const` in this file makes eslint report **`no-debugger` error at 205:5 in this exact file** and rc 1, so lint does cover `src/__tests__`; and the same extractor pulls those 2 problems back out of the control run, so the "0 in this file" is a measurement rather than a blind grep.

**Gate lines: only what THIS push printed.** This push touches a `Blockchain/Dev/` path, so the platform preflight ran. Parsed per suite block by exact basename (the three names are prefixes of one another, so a single combined count loses a figure):

```
pre_push_hook_base.test.sh                 28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh    6 passed, 0 failed
run_shell_suites.test.sh                   49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
OK - 13 code guards passed.
PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
lines starting FIXTURE BUILD FAILED: 0
```

Legs 3, 4 and 8 did not run: no local stack is up. Push rc 0, and `ls-remote` after the push confirms the branch at this head.

**Environment, because a figure carries it:** figures measured in worktree `s-b34-ks1227`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev` (1936 packages) and `packages/shared` **built**. The machine carried a load average of ~40 on 28 cores throughout, from an unrelated volume copy and Spotlight reindexing; no suite figure above was affected (every run was rc 0 with the expected counts), but the timings are inflated.

## Wednesday's figures, as hers
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0, and the file **8/8 green** in her scratch clone. Not my proof; mine is above.

