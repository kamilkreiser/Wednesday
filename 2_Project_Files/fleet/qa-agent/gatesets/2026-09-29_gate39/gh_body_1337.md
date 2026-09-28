#1337 KS-888: widen the KS 764 call-site guard to the revoke shape 1327 introduced
head bb0067dde82ecda05d7c8ca465715d5a897a008d

## BLUF
**Test-only. The product is untouched; only the guard changes.** This turns develop's `packages/shared` green — it has carried **1 failed / 945** since 1327 merged. Measured here: **1 failed / 944 passed (945) → 945 / 945**.

`Refs KS-888`. KS 764 is Done and archived, so it is named de-hyphenated as prose throughout; this PR attaches to KS-888 only, and closes nothing.

## What was wrong
1327 (KS-888 revoke, Kam-ruled option a, merged on gate37) put a five-line comment block and a `try {` between `apiKey.isActive = false;` and `await dbSaveApiKey(` in `services/security/src/index.ts` (the flip is at `:1286`, the save at `:1293`). The KS 764 guard matched the pair with an 80-character window, which cannot span that. Both copies of the pattern — `CALL_SITES` (`:77`) and `REVOKE_WRITES` (`:97`) — stopped matching.

## The fix
Between the flip and the save the pattern now admits **only** whitespace, whole `//` comment lines, and one optional `try {`. So a statement in between, or a save that is moved, deleted or commented out, still reds the guard. A loose `{0,2000}` window was rejected by the drafter because it stayed green even with the save deleted.

## Test Evidence
**Touched:** `Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts` — 1 file, 2 hunks, **+9/-2**. No product file.

**Ran** (all in a clean worktree detached at develop `215cc6875e2bac0b6d6b38918572384fbfcbdb77`, `npm ci` rc 0):

| | untouched tip | with this change |
|---|---|---|
| the guard file | **1 failed / 14 passed (15)** | **15 passed (15)**, rc 0 |
| whole `packages/shared` | **48 files, 1 failed / 944 (945)** | **48 files, 945 / 945**, rc 0 |
| `tsc --noEmit` | rc 0 | **rc 0** |
| `eslint src` (**run by hand** — the harness has no LINT leg) | 36 problems (1 error, 35 warnings) | **36 problems (1 error, 35 warnings)** |

- **The red is a real assertion, not a broken fixture.** It is an `AssertionError` naming the old regex on the `CALL_SITES` cell, and **the other 14 cells pass** — the controls did not also fail.
- **The eslint error is pre-existing and is NOT mine — proven as a delta, not claimed by file ownership.** The change was stashed, eslint re-run at the tip, and restored (restored file byte-identical, `cmp` rc 0). Both runs report `539:36 error Unexpected control character(s) in regular expression ... no-control-regex`, and **the two outputs differ by 0 lines**. It is the KS 703 control-byte guard, already recorded at `BACKLOG.md:876`.
- **The guard's own drift-sweep cell passes at `215cc687`**, so "did anything merged since change what the guard sweeps?" is answered by the cell, not by a grep.

**Arms — 3/3 red the fixed guard**, each a tamper on `services/security/src/index.ts`, each redding **14 passed / 1 failed** (not a load failure — the other cells still run):
- **A** the save deleted;
- **B** an unrelated statement between the flip and the save;
- **C** the flip moved after the save.

Method: same-volume backup, `try/finally`, every tamper `cmp`-proved to differ before its verdict was believed, and the file restored and verified by sha256 (`7f29bb85765e7985`) after each arm and again at the end. Post-restore the guard is **15/15**. The tamper anchor is the revoke site's three-line `try` block, asserted **unique** — the bare save line appears **twice** (mint `:1141`, revoke `:1293`) and a bare anchor would have tampered the wrong call site.

**Push gate, from this push's own raw log:** **878 `ok` / 0 `FAIL` / 0 `not ok`** · shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `FIXTURE BUILD FAILED` **0** · **PREFLIGHT INCOMPLETE — 12 of 15 legs ran, 3 SKIPPED** (legs 3, 4, 8 — local stack not up). **12/15 is not a pass, and is not quoted as one.**

**NOT run:** the four platform suites (Schemathesis · Akto · Playwright · Performance/k6) — this change touches no runtime surface, no route and no schema. Preflight legs 3, 4 and 8. No deploy: **this has no deployable surface.**

**Migrations + config:** none. No migration, no config, no env var, no image.

## Correction to the READY's own evidence
The held READY's `A4` line records "**2 failed** / 15 run" at the untouched tip. **Measured here: 1 failed / 14 passed (15).** The single failing cell is `CALL_SITES`. Recording it because A4 is the READY's red-first evidence line.

## Not covered, and named rather than left silent
- **A candidate, not filed:** the drift sweep's equality finds `services/security/src/index.ts` through the **rotate**'s `UPDATE svc_api_keys SET is_active = false`, so `REVOKE_WRITES[1]` could drift without the sweep noticing. Pre-existing, not introduced here, and out of this change's scope.
- `services/api-gateway/src/startup-migrations.ts` sits in this guard's `NON_REVOKE_MENTIONS` allowlist. Any branch that changes what that file mentions must re-run this guard.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

