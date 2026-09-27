#1309 KS-1196: make admin document-type ids collision-proof with randomUUID
head f615d12d58d95b01b98816644334cfd06832252d

Refs KS-1196

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

`POST /api/admin/document-types` built the new id as `` `dt-${Date.now()}` `` — **from the clock alone**. Two creates in the same millisecond therefore got the **same id**, both answered 201, and the second **silently overwrote the first** in the catalogue. The id now comes from `crypto.randomUUID()`.

**One product line**, plus a new api-gateway test that drives the real admin router with the clock pinned, creates two types in the same millisecond, and pins both that the ids differ and that both types survive in the catalogue.

**Not covered, stated rather than implied.** `Refs`, not a close. Whether any caller **sorts by id** is unmeasured — a time-ordered id is no longer monotonic, and nothing here establishes that no consumer relied on that. A side finding read from the handler but not addressed: it stores `{ id, ...body }`, so a body-supplied `id` would diverge from its catalogue key.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's own diff does not apply strict at this tip**, so the brief's regenerated diff was used. **Both of its claims were proven before applying, not taken on trust:**

1. **The `+`/`-` line sequences are identical, in order** — 119 lines on each side. Compared with `l and l[0] in '+-'`, never `l[:1] in '+-'`: the empty string is "in" every string, so the short form counts a trailing blank line as a change. Controls: an identical pair reads IDENTICAL, and a one-token mutation reads DIFFER.
2. **The regenerated diff applies strict** `git apply --check` **rc 0, where the READY block FAILS** — `error: patch failed: …/routes/admin.ts:679`. Its sha256 matches the brief's declared prefix `2c17773c8f2f03e1`.

⚠ **One stated figure disagreed with my measurement and the brief's author confirmed mine.** The brief declared the regenerated diff as **+109 / −1**; I measure **+118 / −1** excluding the `+++`/`---` headers (`admin.ts` +1/−1, the new test +117/−0). Cause, confirmed: the brief's count used `grep '^+[^+]'`, which cannot match an added **empty** line, so it missed the 9 blank lines in the new test. The diff itself was always right.

**Apply.** Strict `git apply`, no `--recount`, no fuzz: **both sections rc 0**. The tool also asserts that the bytes it split are the bytes it verified — `split-source CONFIRMED == KS-1196.regenerated-at-94c9c7aa.diff (5070 B, sha256 2c17773c8f2f03e1)`.

**RED — the product line WITHHELD** (this item changes product, so no tamper is needed):

- **2 failed / 2 passed of 4**, and both failures are the **two declared cells, each on its assertion**:
  - `AssertionError: expected 'dt-1758000000000' not to be 'dt-1758000000000' // Object.is equality` — the two creates returned the identical id.
  - `AssertionError: expected [ 'Beta Type' ] to deeply equal [ 'Alpha Type', 'Beta Type' ]` — the catalogue kept only the second.
- **Those two assertions are the ticket**: the collision and the silent loss, each pinned separately.
- Restored and verified byte-identical to my head.

**GREEN at my head.** The new file alone: **4 of 4 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**):

| | files | tests |
|---|---|---|
| bare (both hunks withheld) | 82 | **754** |
| patched (my head) | 83 | **758** |

**0 new reds**; +1 file and +4 tests are exactly this change.

**`packages/shared`**: **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** The package's own program is 491 files with **zero** test files, so its rc 0 says nothing here. On a config extending it with `exclude: []`: **619 files, 83 test files, this one present exactly once** — **29 errors, the SET byte-identical to the base's 29**, **0 naming this file**.

**Lint, with a control that fires.** `npm run lint` **rc 0, 36 problems, 0 errors** — unchanged from the base. Control: a planted `debugger` gives **rc 1, `no-debugger` error at 117:3 in this file**, so eslint does cover it.

⚠ **Disclosed, because it cost me a restore:** after that lint control I reverted with a copy I could not vouch for and the file came back at the **wrong** sha. I caught it by comparing blob ids, moved the untrusted copy to quarantine rather than deleting it, and **re-created the file from the section diff**, which is the authoritative source. The tree was then verified line-for-line against the regenerated diff — product `+`/`-` identical, new file 117 lines identical, zero `debugger` occurrences — and **the cell and lint were both re-run on the restored tree**, so no figure in this PR rests on the control run.

**Gate lines: only what THIS push printed.** This push touches `Blockchain/Dev/` paths, so the platform preflight ran:

```
pre_push_hook_base.test.sh                 28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh    6 passed, 0 failed
run_shell_suites.test.sh                   49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
OK - 13 code guards passed.
PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
lines starting FIXTURE BUILD FAILED: 0
```

Legs 3, 4 and 8 did not run: no local stack. Push rc 0; `ls-remote` after the push confirms the branch at this head.

**Environment:** worktree `s-b34-ks1196`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. This PR's base is `94c9c7aa`; develop has since moved and has **not** been merged into this branch.

## Wednesday's figures, as hers
In her scratch clone at this tip: the test file alone **2 failed / 2 passed**, with the product line **4 passed**, api-gateway **83 files / 758 tests**. Not my proof; mine is above and agrees.

