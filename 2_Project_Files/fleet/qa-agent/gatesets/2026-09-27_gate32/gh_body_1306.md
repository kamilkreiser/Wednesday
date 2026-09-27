#1306 KS-1205 F3: pin that a JWT claim cannot name another key's rate-limit bucket
head 00180ad72bffdcf917d618b54557a4df90f510c8

Refs KS-1205

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

**One NEW api-gateway test file. No product change.**

The per-key rate limiter counts an API key under `api_key:` plus a **domained** sha256 of the key. **Nothing pinned the domain**, so a bucket built from the *bare* sha256 of the key — the same value the security service stores as `key_hash` — left the whole suite green. The cells read the bucket the **real** `authenticateToken` puts on `req.user` for two distinct keys, and assert it is not the bare hash.

**Not covered, stated rather than implied.** This is F-3 (`G-BUCKET-HASH`) only, so it is `Refs`, not a close. The cells read `req.user.rateLimitBucket`, **not Redis keys**: a tamper inside `rateLimitEnforce.ts` would not red them, which the brief states and this PR repeats. The file keeps the builder's name — unlike two of its siblings, this READY asks for no rename.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's glued closing fence**, the same defect as its siblings: the fence sits on the diff's last `+` line with no fence line after it, so taken as-is the file ends in stray backticks and vitest fails to **transform** it — a load failure, not a red. Stripped, and the only difference between the READY's raw block and what I applied is those three backticks.

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**: 1 file, **+77**. **Control:** a new file cannot be controlled by a path tamper (it applies at any path), so the hunk line count is corrupted instead — **refused, rc 128**.

**The tamper line MOVED, and I re-located it rather than trusting either figure.** The READY names `middleware/auth.ts:300`; its own note predicted `:304` *if* the optional-API-key follow-up merged first — **and that did merge**. Measured at this tip, the `rateLimitBucket` assignment is at **`:313`**, and `rateLimitBucket` occurs in that file exactly twice: the optional type field at `:54` and this one. The anchor was asserted to occur **exactly once** before planting, with sha256 before and after proving the tamper landed.

**RED under that tamper** — the bucket rebuilt from the bare sha256:

- **1 failed / 2 passed of 3**, and the single failure is the **declared cell, on its assertion**: `AssertionError: expected '200 api_key:b28a76e0bb3f5dc02857f7188…' not to be '200 api_key:b28a76e0bb3f5dc02857f7188…' // Object.is equality` — i.e. the bucket became exactly the bare hash the cell forbids.
- **Restored by content and verified against the base blob** — on-disk sha256 `9abef1c21164bbbc…` equals `git show <base>:<path>`; 0 `TAMPER` markers remain.

**GREEN at my head.** The new file alone: **3 of 3 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**, which these tests need):

| | files | tests |
|---|---|---|
| bare (file moved aside, asserted absent) | 82 | **754** |
| patched (my head) | 83 | **757** |

**0 new reds**; +1 file and +3 tests are exactly this file. The file was moved aside, not deleted, and moved back with its sha256 re-checked.

**`packages/shared`**: **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** The package's own `tsc --noEmit` covers **491 files with zero test files** (`tsconfig.json` excludes `src/__tests__`), so its rc 0 says nothing about this cell. On a config extending it with `exclude: []` the program is **619 files including 83 test files, this one present exactly once**: **29 errors, the SET byte-identical to the base's 29**, and **0 naming this file**.

**Lint.** `npm run lint` (`eslint src`): **rc 0, 36 problems, 0 errors** — unchanged from the base. eslint is proven to cover `src/__tests__` by a planted-`debugger` control run on this package earlier in this session (reported as an **error** inside a test file, rc 1).

**Environment, because a figure carries it:** worktree `s-b34-ks1205`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. This PR's base is `94c9c7aa`; develop has since moved, and develop has **not** been merged into this branch.

**Gate lines: only what THIS push printed.** This push touches a `Blockchain/Dev/` path, so the platform preflight ran. Parsed per suite block by exact basename:

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

## Wednesday's figures, as hers
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0 after the fence strip, and **3/3 green** in her scratch clone. Not my proof; mine is above.

