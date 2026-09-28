#1317 KS-1346 D: log a thrown object's type and field names in the webhooks routes
head 2a688b24054929a66c85f7b9a9852a46f2edb8f6

## What this changes

`fail500` in `services/originate/src/routes/webhooks.ts` logged a non-Error throw through
`String(err)`, so a thrown plain object reached the log as `[object Object]` and its content was lost.
The 500 **body** was already constant; this changes only the **log**. One line, in the one helper that
covers **7** call sites.

**Kam's ruling, verbatim** — card `secuura-ks1346-logging-thrown-objects-leaks-secrets`, option **a**
(2026-09-27 16:32): *"Type and field names only"*. A non-Error, non-string throw is logged as its
TYPE and FIELD NAMES only, never its values, so no secret reaches the log. Error throws and string
throws log exactly what they logged before.

This is the second half of the KS-1346 residue gate33 named as **F-3**. Part C covers
`routes/adminConfig.ts` in **#1316**; the two touch different files and do not conflict in either
merge order. `Refs KS-1346` — deliberately not a closing keyword. The gate decides the ticket move.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+1/−1)
- `Blockchain/Dev/services/originate/src/__tests__/ks1346d-webhooks-fail500-logs-type-and-field-names.test.ts` (new, +134)

**Ran — all by me, in this branch's own worktree at base `ec32c40e2b1e`, `npm ci` and `packages/shared` built**
- **RED-FIRST**, product reversed to the tip blob (verified equal to
  `ec32c40e…:…/webhooks.ts`), test applied alone: **3 failed / 10 passed / 13**. The three reds are the
  `D1` cells — `PATCH /:id`, `DELETE /:id`, `POST /:id/rotate-secret`.
- **GREEN**, product hunk applied: **13 passed / 13**.
- **Whole `services/originate` suite: 87 suites / 1026 tests / 0 failed** (`rc 0`). The "no NEW red"
  claim rests on **0 failed**, not on a count delta.
- **Tamper arm — `util.inspect(err)` substituted for the field-names rendering: 7 failed / 13.**
  All three `D1` rows red **and** all three `D6` controls (*"no VALUE of a thrown object reaches the
  log"*) red, plus `D4` (a string throw gets quoted by `inspect`). So the `D6` controls are
  falsifiable rather than green-by-construction. Tamper placed by an anchor asserted to occur
  **exactly once**; restored from a pre-tamper copy with the blob verified equal
  (`a3cba92d1db49c23e9171f1acfb7afdd18f9fdd8`), `util.inspect` residue 0, and the cell re-run green
  afterwards so no figure rests on the tamper run.
- **`tsc --noEmit`: rc 0, 0 errors** — over a program **proven to contain the new cell**. The package
  tsconfig excludes `src/__tests__`, so a bare `tsc` rc 0 proves nothing; an `exclude: []` config was
  used (655 files) with `typeRoots` pointing at the hoisted `@types`, and `--listFilesOnly` shows the
  new test once and `routes/webhooks.ts` once, with a bogus-filename control at 0. That config lives
  in `5_Project_History/.../quarantine/` and is not committed.
- **Lint (the package's own `eslint src`): rc 0** — 22 warnings, 0 errors, all pre-existing.
  `webhooks.ts`: **0 messages**, and **0 at base as well**, measured by putting the base blob in place
  and re-linting. My test file: **0 messages**. No new lint finding.

**NOT run**
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) — no local stack.
- The `services/originate` **integration** suite — needs a database.
- No baseline full-suite run: unnecessary, because the after-suite is **0 failed**.

**Migrations + config**
- **None.** One expression inside one logging call, plus a new test file.

## NOT COVERED (carried from the brief's own OPEN DOUBTS)

- **D7 is a pin, not a red.** It is green at the tip and after, because the behaviour is already safe
  (gate29 S1). **Its fail-ability is shown only by the planted-log arm** — I did not independently
  red it.
- **D7 does not cover everything the probe did.** Its UPDATE rejects with an `Error`, so it proves the
  secret is kept out of the log. It does **not** cover a Prisma error object whose own fields might
  carry the bound ciphertext. Under the ruling such an object would log only field NAMES.
- **The real key sits in the process keyring for this file's lifetime** and is not reset in
  `afterAll`. jest isolates module registries per file, so no other suite is affected — and the whole
  suite stayed green, which I measured.
- The behavioural cells drive **3 of the 7** sites. The other 4 share the one helper line.
- **F-2 is not hardened.** The ruled residue (field NAMES are themselves data) applies here exactly as
  it does to parts A, B and C.

⚠ One line of that OPEN DOUBTS list is **stale and I am not carrying it**: it says *"No Spark round was
run."* The run exists — `checker.out` records **9 PASS / 0 FAIL**, its A4/A5 figures (3/13 red,
13/13 green) are exactly what I reproduced, and the run's `patch.diff` is byte-identical to the
brief-writer's golden. Same stale note as part C's README, which was written minutes before its run.
Reported rather than silently dropped.

## Provenance

Patch produced by the local model (Spark) under a Wednesday brief, then **re-verified here**: the
READY's fenced diff block is **byte-identical** to the checker's canonical `patch.diff` (8336 bytes
both; a one-character mutation control differs), both `section_*.opts` name the plain `.diff`, and
both sections strict-apply clean (`git apply -p1 --check`) at `ec32c40e2b1e`. Every figure above is
one I measured; none is copied from the harness.

## Push gate (in-hook preflight, from this push's own raw log)

`pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** ·
`run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`OK — 13 code guards passed.` · `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`^FIXTURE BUILD FAILED` **0**. `gatelines32` verdict: **MATCHES the declared fleet STOP condition**.
Legs 3, 4 and 8 are the SKIPPED three — they need a running local stack. Push rc 0, and the branch
head at origin was re-read afterwards and equals the commit (`2a688b240549…`).

