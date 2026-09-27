#1307 KS-1212: pin that the erasure door reads its own router's caseSensitive option
head 64d8e398599687b53520bc3710cae6869bdc6b8f

Refs KS-1212

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

**One NEW api-gateway test file. No product change.**

The gdpr erasure door compares the canonical path using the case rule of **its own** router, `erasureDoor`. The merged cell from the earlier round makes **every** Router the factory builds case sensitive at once, so it cannot tell the door router from the factory router — and a product that reads the *factory* router's option stays green under it. The new cells build the **real** `createProxyRoutes` twice through a Router seam that makes exactly **one** of the two routers case sensitive: first the door router, then the factory router. The door must follow its own either way. A control cell pins that the factory makes exactly two `Router()` calls, so the seam cannot silently target the wrong one.

**Renamed at raise** per the READY's note — the builder's filename named the parent ticket rather than this behaviour. The rename is a rename: content sha256 `15d5dc0ee6f32ccd…` before and after.

**Not covered, stated rather than implied.** `Refs`, not a close: the cells pin the door's *source* of the case rule, not the full canonicalisation behaviour, and not the other doors in the same factory. The Router seam is a test seam; nothing about the product's own Router construction is changed.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's glued closing fence**, as with its siblings: the fence sits on the diff's last `+` line with no fence line after it, so taken as-is the committed file ends in stray backticks and vitest fails to **transform** it — a load failure, not a red. Stripped, and the only difference between the READY's raw block and what I applied is those three backticks.

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**: 1 file, **+134**. **Control:** a new file cannot be controlled by a path tamper (it applies at any path), so the hunk line count is corrupted instead — **refused, rc 128**.

**The tamper line had MOVED, and I re-located it rather than trusting the brief.** The brief names `routes/proxy.ts:808`, read at an older tip; at this base the declaration is at **`:814`**, and `erasureDoorCaseSensitive` appears in that file exactly twice — the declaration and its single read at `:817`. The anchor was asserted to occur **exactly once** before planting, with sha256 before and after proving it landed.

**RED under that tamper** — the door reads the *factory* router's option instead of its own:

- **2 failed / 2 passed of 4**, and both failures are the **two declared cells, each on its assertion**, not a crash:
  - `AssertionError: expected [ 400, 'NON_CANONICAL_PATH', [] ] to deeply equal [ 200, null, …(1) ]`
  - `AssertionError: expected [ 200, null, …(1) ] to deeply equal [ 400, 'NON_CANONICAL_PATH', [] ]`
- **The two assertions are mirror images of each other, and that is the point:** with the door case sensitive and the factory default the request must be forwarded; with the factory case sensitive and the door default it must be refused. A product reading the wrong router gets exactly one of those backwards in each direction, so a single cell could not have caught it.
- **Restored by content and verified against the base blob** — on-disk sha256 `0968c155431e6f3b…` equals `git show <base>:<path>`; 0 `TAMPER` markers remain.

**GREEN at my head.** The new file alone: **4 of 4 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**, which these tests need):

| | files | tests |
|---|---|---|
| bare (file moved aside, asserted absent) | 82 | **754** |
| patched (my head) | 83 | **758** |

**0 new reds**; +1 file and +4 tests are exactly this file. Moved aside rather than deleted, moved back with its sha256 re-checked.

**`packages/shared`**: **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** This package's own `tsc --noEmit` covers 491 files with **zero** test files (`tsconfig.json` excludes `src/__tests__`), so its rc 0 says nothing about this cell. On a config extending it with `exclude: []` the program is **619 files including 83 test files, this one present exactly once**: **29 errors, the SET byte-identical to the base's 29**, and **0 naming this file**.

**Lint.** `npm run lint` (`eslint src`): **rc 0, 36 problems, 0 errors** — unchanged from the base. eslint is proven to cover `src/__tests__` by a planted-`debugger` control run on this package earlier in this session (reported as an **error** inside a test file, rc 1).

**Environment, because a figure carries it:** worktree `s-b34-ks1212`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. This PR's base is `94c9c7aa`; develop has since moved and has **not** been merged into this branch.

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
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0 after the fence strip, and **4/4 green** in her scratch clone. Not my proof; mine is above.

