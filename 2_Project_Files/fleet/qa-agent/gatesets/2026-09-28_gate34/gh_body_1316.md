#1316 KS-1346 C: log a thrown object's type and field names in the adminConfig routes
head 14fc80fb144c2b95f016cc325885c2684105c7cc

## What this changes

`fail500` in `services/originate/src/routes/adminConfig.ts` logged a non-Error throw through
`String(err)`, so a thrown plain object reached the log as `[object Object]` and its content was
lost. The 500 **body** was already constant (KS 730 — de-hyphenated on purpose: a hyphenated key in a PR body ATTACHES that ticket); this changes only the **log**. One line, in the
one helper that covers **50** admin-config call sites.

**Kam's ruling, verbatim** — card `secuura-ks1346-logging-thrown-objects-leaks-secrets`, option **a**
(2026-09-27 16:32): *"Type and field names only"*. A non-Error, non-string throw is logged as its
TYPE and FIELD NAMES only, never its values, so no secret reaches the log. Error throws and string
throws log exactly what they logged before.

This is part of the KS-1346 residue gate33 named as **F-3** (`adminConfig.ts` and `webhooks.ts` still
logged a thrown non-Error through `String(err)`). Part D covers `webhooks.ts` separately; the two
touch different files and do not conflict in either merge order.

`Refs KS-1346` — deliberately not a closing keyword. The gate decides the ticket move.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (+1/−1)
- `Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts` (new, +117)

**Ran — all by me, in this branch's own worktree, at base `ec32c40e2b1e`, `npm ci` (1936 packages) and `packages/shared` built**
- **RED-FIRST**, product untouched, test applied alone: **4 failed / 11 passed / 15**. The four reds
  are the four `C1` cells (`GET /settings`, `/document-types`, `/workflows`, `/organizations`).
- **GREEN**, product hunk applied: **15 passed / 15**.
- **Whole `services/originate` suite: 87 suites / 1028 tests / 0 failed** (`rc 0`). The
  "no NEW red" claim rests on **0 failed**, not on a count delta.
- **Tamper arm — `util.inspect(err)` substituted for the field-names rendering: 9 failed / 15.**
  All four `C1` rows red **and** all four `C6` controls (*"no VALUE of a thrown object reaches the
  log"*) red, plus `C4` (a string throw gets quoted by `inspect`). So the `C6` controls are
  falsifiable rather than green-by-construction. The tamper was placed by an anchor string asserted
  to occur **exactly once**; the file was restored from a pre-tamper copy and the blob verified equal
  (`ccd978ba3f4499dd28b4ec481c2f0c8b661a5065`), `util.inspect` residue 0, and the cell re-run green
  afterwards so no figure here rests on the tamper run.
- **`tsc --noEmit`: rc 0, 0 errors** — over a program **proven to contain the new cell**. The package
  tsconfig excludes `src/__tests__`, so a bare `tsc` rc 0 would prove nothing; an `exclude: []`
  config was used (655 files) and `--listFilesOnly` confirms the new test appears **once** and
  `routes/adminConfig.ts` **once**, with a bogus filename control at **0**. That config lives in
  `5_Project_History/.../quarantine/` and is not committed.
- **Lint (the package's own `eslint src`): rc 0** — 22 warnings, **0 errors**, all pre-existing.
  My test file: **0 messages**. `adminConfig.ts`: 2 messages, and they are **identical at base and
  at this head** (lines 2089 `prefer-const`, 2129 `no-unused-vars`), measured by putting the base
  blob in place and re-linting, so this change introduces **no new lint finding**.
  Coverage measured directly, not assumed: the JSON formatter lists **143** linted files and both of
  my files are among them. A planted violation in my test file produced 2 messages and disappeared on
  restore, so the lint can fail on it.

**NOT run**
- No local stack, so nothing that needs one: the four platform suites (Schemathesis · Akto ·
  Playwright · Performance/k6) were **not** run for this PR. The in-hook preflight's own legs are in
  the push log.
- The `services/originate` **integration** suite (`jest --config jest.integration.config.js`) was not
  run — it needs a database.
- No baseline full-suite run: unnecessary here, because the after-suite is **0 failed**.

**Migrations + config**
- **None.** No migration, no schema change, no environment variable, no config file. One expression
  inside one logging call, plus a new test file.

## NOT COVERED (carried from the brief's own OPEN DOUBTS)

- The behavioural cells drive **4 of the 50** sites. The other 46 share the one helper line, and
  ks730c's source cell C3 (50 helper calls, 50 distinct contexts) still passes.
- `$queryRaw` rejecting with a plain object is **synthetic**. As gate33 recorded, nothing in
  originate is known to throw a non-Error today.
- The ruled residue **F-2** (field NAMES are themselves data — e.g. an email-shaped key) applies here
  exactly as it does to parts A and B. **It is not hardened by this PR.**
- Merge order with part D is free: the two briefs touch different files.

⚠ One line of that OPEN DOUBTS list is **stale and I am not carrying it**: it says *"No Spark round
was run. This is a brief and a golden only."* The README was written **05:01:37Z** and the Spark
run's `patch.diff` **05:03:38Z**, so the round happened two minutes after the note. `checker.out`
records **9 PASS / 0 FAIL**, and the run's patch is byte-identical to the brief-writer's
`KS-1346.golden.diff`. Reported rather than silently dropped.

## Provenance

Patch produced by the local model (Spark) under a Wednesday brief, then **re-verified here**: the
READY's fenced diff block is **byte-identical** to the checker's canonical `patch.diff` (7031 bytes
both; a one-character mutation control differs), `cat(section_1, section_2)` reproduces that
canonical patch, and `section_2.opts` names `section_2.diff` as the applied file. Both sections apply
**strict** (`git apply -p1 --check` clean) at `ec32c40e2b1e`. Every figure above is one I measured;
none is copied from the harness.

## Push gate (in-hook preflight, measured in this push's own raw log)

`pre_push_hook_base.test.sh` **28/0** · `pre_push_hook_base_fixture_guard.test.sh` **6/0** ·
`run_shell_suites.test.sh` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** ·
`OK — 13 code guards passed.` · `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`^FIXTURE BUILD FAILED` **0**. `gatelines32` verdict: **MATCHES the declared fleet STOP condition**.
Legs 3, 4 and 8 are the three SKIPPED — they need a running local stack. Push rc 0; the branch head
at origin was re-read afterwards and equals the commit (`14fc80fb144c…`).

