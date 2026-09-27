#1305 KS-1090 R2-3: type-check the api-gateway wiring test the tsc program never saw
head 7aab743e13f45d10a43650e07f25abffccb6441e

Refs KS-1090

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run; the harness's figures are quoted as the harness's at the end.

## What changes

**One NEW api-gateway test file. No product change.**

The merged mint-scope test pins **two** of the eighteen service keys that must never receive the gateway vouch header — it checks analytics and auth only — so an allow-list widening that spares those two keys stays green. The new cells drive the **real** `createProxyRoutes` with every service pointed at one local recorder and pin, for each non-originate key, that no vouch arrives. A control cell proves originate **does** receive it, and that the factory reads exactly the eighteen service keys the file lists.

**Renamed at raise**, per the READY's own note: the builder's filename described the ticket's *other* half (the tsc-excludes-tests shape), which this change does not address. The rename is a rename — content byte-identical, sha256 `d67ae63b95d27b13…` before and after.

**Not covered, stated rather than implied.** This is R2-3 only, so it is `Refs`, not a close: the tsconfig half (R2-2) and the record (R2-4) stay open on the ticket. The cells pin *that* no vouch arrives for the sixteen non-originate keys; they do not pin the header's value for originate beyond the control's equality check.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**A defect in the READY, found and measured before applying.** Its closing code fence is **glued onto the diff's last `+` line** (`+});` immediately followed by three backticks) with no fence line after it. Taken as-is the committed file ends in stray backticks and vitest fails to **transform** it — a load failure, not a red. Stripped, and proven to be the only change: a full `diff` of the READY's raw block against what I applied is **exactly two lines** — `< +});```` / `> +});`. Nothing else differs.

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**: 1 file, **+96**. Paired with a control that must fail — a **new file cannot be controlled by a path tamper** (a new file applies at any path, so that control passes and proves nothing), so the hunk line count is corrupted instead (`@@ -0,0 +1,96` -> `+1,999`): **refused, rc 128, "corrupt patch at line 100"**. So the rc 0 on the real section is a measurement.

**RED — a product tamper, since this change is test-only.** Tampered `services/api-gateway/src/routes/proxy.ts:275` in my worktree only, the anchor asserted to occur **exactly once in that file** first (and exactly once repo-wide at this tip), sha256 before/after proving it landed — the vouch condition widened to every key the old cells do not name:

- **2 failed / 2 passed of 4**, and the two failures are **both declared cells**, each on its **assertion**, not a crash: `AssertionError: expected [ [ '/api/anchoring/p1', true ], …(7) ] to deeply equal [ Array(8) ]` and the same shape for the second cell's seven keys.
- **Restored by content and verified against the tip blob** — on-disk sha256 `0968c155431e6f3b…` equals `git show <tip>:<path>`; 0 `TAMPER` markers remain.

**GREEN at my head.** The new file alone: **4 of 4 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**, which these tests need):

| | files | tests |
|---|---|---|
| bare (file moved aside, not deleted) | 82 | **754** |
| patched (my head) | 83 | **758** |

**0 new reds**; +1 file and +4 tests are exactly this file. The bare run was taken with the file **absent, asserted absent** before the run, then moved back and its sha256 re-checked.

**`packages/shared`** (its guard suites read service sources by text, and this adds one): **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** This package's own `tsc --noEmit` says nothing about it: `tsconfig.json` excludes `src/__tests__`, so its program is 491 files with **zero** test files. Measured instead on a config extending it with `exclude: []`, whose program is **619 files including 83 test files, this one present exactly once**: **29 errors, the SET byte-identical to the tip's 29**, and **0 naming this file**.

**Lint, the package's own script.** `npm run lint` (`eslint src`) is **rc 0, 36 problems, 0 errors, 36 warnings** — unchanged from the tip, measured in the same worktree family. eslint is proven to cover `src/__tests__` by a planted-`debugger` control run on this package earlier in this session (it reported `no-debugger` as an **error** inside a test file, rc 1).

**Gate lines: only what THIS push printed.** This push touches a `Blockchain/Dev/` path, so the platform preflight ran. Parsed per suite block by exact basename (the three names are prefixes of one another, so one combined count loses a figure):

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

**Environment, because a figure carries it:** worktree `s-b34-ks1090`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. The machine carried a load average of ~40 on 28 cores throughout from an unrelated volume copy and Spotlight reindexing; timings are inflated, no verdict changed.

## Wednesday's figures, as hers
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0 **after stripping the glued fence**, and **4/4 green** in her scratch clone. Not my proof; mine is above.

