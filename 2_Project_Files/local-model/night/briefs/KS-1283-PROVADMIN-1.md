# KS-1283 PROVADMIN-1 PIN THAT requireOrgProvisioner REFUSES A TENANT ADMIN ROLE (ADMIN and admin) WITH 403 AND MARKS NO provisionerKind — the guard register-connector mounts, the row that MINTS A KEY — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 01:xx on 2026-09-21, widened sweep round 22)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts`
Tip: `778e6cfe2b6061d60ffcf3a57a951c84dc152b67`
Runner: `vitest`

Written from develop `778e6cfe2b6061d60ffcf3a57a951c84dc152b67` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 01:0x on 2026-09-21, read verbs only; the #1104 merge, KS-1272 UUID-DEDUP-1). The test file at that tip is **83 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` (**990 lines**, read whole): `SUPER_ROLES` at `:64`, `requireSuperAdmin` at `:66-73` (not exported), `requireOrgProvisioner` at `:91-114` (exported, `:18` of the test file imports it), its `SUPER_ROLES.includes` branch at `:97`, and the `POST /api/platform/organizations/register-connector` mount at `:486-489` whose guard is `requireOrgProvisioner`. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `platform.ts`, `auth.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1283 is a COVERAGE gap, not a live defect: today `SUPER_ROLES` (`platform.ts:64`) is exactly `['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN']`, so a tenant-level `ADMIN` / `admin` role is refused 403 by `requireOrgProvisioner` and by the six `requireSuperAdmin` surfaces — but the #1100/#1101 gate measured that widening `SUPER_ROLES` to admit `'ADMIN'` / `'admin'` reds only **1 of 674** api-gateway cells (the #1101 cell for `GET /api/platform/tenants`); every other guarded route, the lead item `POST /api/platform/organizations/register-connector` included, goes past its guard unpinned, and on that route a widened list turns 403 into **201 and a minted connector key**. The suite that drives the REAL `requireOrgProvisioner` in process is this file: its refusal cells (`:68`) use `HOLDER`, `ISSUER`, `VERIFIER`, `ORG_ADMIN` — none of which a widened list admits — so nothing here reds either. This change adds ONE cell to the `refusals` describe that calls the file's own `harness(...)` (the real guard with a fake req/res, `:20-36`) for `{ role: 'ADMIN' }` and `{ role: 'admin' }` and asserts, per role, `[role, passed, status, message-is-the-guard's-own, provisionerKind]` equals `[role, false, 403, true, undefined]`. `passed === false` and `kind === undefined` are the pinned facts (the guard did not call `next`, did not mark the request `admin`); the `/platform-admin role/` match on the 403 message is the liveness element (the refusal is `requireOrgProvisioner`'s own `:107-113` body, not some other 403). Every existing cell is unchanged. **It pins TODAY's behaviour and decides nothing about KS-1283's ticket text** — the ticket asks for route-level cells in the ks1215 real-app suite; this brief pins the GUARD the lead row mounts (`:489` -> `:91` -> `:97`), so a widened `SUPER_ROLES` now arrives as a deliberate red in the guard's own suite instead of passing 673/674 silently.

## The exact change — ONE hunk in the test file

The new cell goes at the end of the `describe('requireOrgProvisioner — refusals', ...)` block opened at `:60`, directly above that block's closing line `});` (`:83`, the file's LAST line and the ONE trailing context line). There is NO leading context: the line above (`:82`, `  });`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts`.**

```
@@ -83,1 +83,5 @@
+  it('RED KS-1283: refuses a tenant ADMIN role (ADMIN and admin) with 403 and marks no provisionerKind - the widened SUPER_ROLES shape that would let register-connector mint a key', () => {
+    const outcomes = ['ADMIN', 'admin'].map((role) => { const r = harness({ role }); return [role, r.passed, r.status, /platform-admin role/.test(r.body?.error?.message ?? ''), r.kind]; });
+    expect(outcomes).toEqual([['ADMIN', false, 403, true, undefined], ['admin', false, 403, true, undefined]]);
+  });
 });
```

`describe`, `it`, `expect` and `vi` are already imported by the file at `:16`, `requireOrgProvisioner` at `:18`, and `harness` is the file's own helper at `:20-36` (it builds the fake req/res, calls the REAL guard once, and returns `status`, `body`, `passed` and `kind`) — you add NO import and NO helper. The cell needs no mock, no app boot, no port, no fetch and no database: the guard is called as a function with the file's fake req/res, exactly as `:39-82` already call it.

## Cells

- `provadmin` = `RED KS-1283: refuses a tenant ADMIN role (ADMIN and admin) with 403 and marks no provisionerKind - the widened SUPER_ROLES shape that would let register-connector mint a key`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1283: refuses a tenant ADMIN role (ADMIN and admin) with 403 and marks no provisionerKind - the widened SUPER_ROLES shape that would let register-connector mint a key

## Tampers

Two single-line tampers on two DIFFERENT lines of `platform.ts` (`:64` and `:97`; each occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1 each; positive control `SUPER_ROLES.includes` matches 2 lines, `:68` and `:97`). They are the two shapes a widening can take: the ticket's own (the list grows two entries, which also widens `requireSuperAdmin` at `:68`), or the guard's own branch admitting an ADMIN spelling beside the list. Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (`user.role` is a string on the `req.user` principal), so nothing fails to load and no cell reds for the wrong reason.

### WIDENROLES — the ticket's tamper: SUPER_ROLES admits 'ADMIN' and 'admin'
File: `Blockchain/Dev/services/api-gateway/src/routes/platform.ts`
Line: 64
From:
```
const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];
```
To:
```
const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN', 'ADMIN', 'admin'];
```
Reds: `provadmin`

### ADMINBRANCH — the provisioner guard's own branch admits any ADMIN spelling beside the list
File: `Blockchain/Dev/services/api-gateway/src/routes/platform.ts`
Line: 97
From:
```
  if (SUPER_ROLES.includes(user.role)) {
```
To:
```
  if (SUPER_ROLES.includes(user.role) || String(user.role).toUpperCase() === 'ADMIN') {
```
Reds: `provadmin`

## Controls

- `401s an unauthenticated request rather than 403`
- `admits a connector carrying organizations:register, marked as connector`
- `does not mark provisionerKind on a refusal`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:74`, `:47` and `:80` — each occurs exactly once in the file and none is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; the prefix rule in `build_test_only_input.sh`'s header is for BASH suites only. The file's `it.each` cells (`:39`, `:68` — reported as `admits super_admin as admin`, `refuses the non-platform role ORG_ADMIN`, etc.) are also green under both tampers but are left undeclared. The `:80` control is the liveness proof for the `kind` half of the new cell: it reads the same `provisionerKind` slot through the same harness after the same refusal branch.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: for `'ADMIN'` and for `'admin'`, `harness` builds `{ user: { role } }`, the guard finds a user (`:93`), `SUPER_ROLES.includes(role)` is false (`:97`, the list holds neither spelling), `role === 'connector'` is false (`:102`), so `:107-113` answers `403` with `code: 'FORBIDDEN'` and the message `Organisation provisioning requires a platform-admin role or the organizations:register scope`; `next` is never called and `provisionerKind` is never set. `outcomes` is `[['ADMIN', false, 403, true, undefined], ['admin', false, 403, true, undefined]]`, exactly what the cell asserts.

Under **WIDENROLES** `SUPER_ROLES.includes('ADMIN')` and `SUPER_ROLES.includes('admin')` are both true: the guard marks `provisionerKind = 'admin'` and calls `next` (`:98-99`), the harness never sees a status or a body, so each entry reads `[role, true, 0, false, 'admin']` — assertion red. Under **ADMINBRANCH** `String(role).toUpperCase() === 'ADMIN'` is true for both spellings, with the same `[role, true, 0, false, 'admin']` — assertion red. Under BOTH, every existing cell stays green: the four `admits %s` roles are still in the list, the connector cells never reach `:97`'s truthy side (`'connector'` is not in the widened list and `'CONNECTOR' !== 'ADMIN'`), `HOLDER` / `ISSUER` / `VERIFIER` / `ORG_ADMIN` are in neither widened list and none upper-cases to `ADMIN`, the unauthenticated request 401s at `:93` before either tamper line, and `harness({ role: 'HOLDER' }).kind` stays undefined.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` lines.** `platform.ts` at `778e6cfe2`, line 64 is `const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];` and line 97 is `  if (SUPER_ROLES.includes(user.role)) {`, byte for byte; each occurs **exactly once** in the file (`grep -c -F -x`, 1 and 1; `:68` is `  if (!user || !SUPER_ROLES.includes(user.role)) {` — different bytes, the `requireSuperAdmin` guard). The checker plants and restores them one at a time (T8 by sha256 after each).
- **Premise: the ticket's claim, re-derived.** The ticket's tamper is `platform.ts:64` widened to admit `'ADMIN'` / `'admin'`; its gate measurement is 1 red of 674 across the api-gateway suite. In THIS file the refusal roles at `:68` are `HOLDER`, `ISSUER`, `VERIFIER`, `ORG_ADMIN` and at `:81` `HOLDER` — `git grep` for `'ADMIN'` / `'admin'` over `src/__tests__` at the tip finds no cell that drives `requireOrgProvisioner` or `platform.ts` with a bare ADMIN role (the hits are auth/verify fixtures). `KS-1283` occurs **0** times in `src/__tests__`.
- **Premise: the anchor.** The test file is **83** lines; `:83` is `});` (column 0, the file's last line, one of exactly THREE column-0 `});` lines — the others close the describes at `:44` and `:58` — so the hunk header's line number, not the bytes alone, places the insertion) and `:82` is `  });`. The trailing context line is non-blank and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: the in-process guard call.** `harness` (`:20-36`) calls `requireOrgProvisioner(req, res, next)` synchronously with `{ user }` as the request, a two-method `res` (`status`, `json`) and a `vi.fn()` `next`; the guard reads only `req.user`, `res.status(...).json(...)` and `next()`. `r.body` is typed `{ error?: { message?: string } } | null` at `:32`, so `r.body?.error?.message ?? ''` type-checks; `r.kind` reads `req.provisionerKind` (`:34`).
- **Premise: no `+` line re-adds a tip line.** The only `+` line that also occurs at the tip is the closing `  });` (unavoidable for a new cell).
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). The title uses `-`, not an em dash; the describe titles' em dashes are context the diff never writes.
- **Premise: the runner.** `api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: no live-lane collision.** `platform.ts` is not `index.ts`, `enforcement.ts`, `startup-migrations.ts` or `trustHeaders.ts`, and is not under `services/anchoring/**`; the test file is not `ks480-connector-auth`, `ks740-bounded-fanout`, `row-converters`, `ks1041-vouch-header-strip` or `ks501-enforcement-non-string-doctype`. **No held `READY_*` and no brief in `night/briefs/` names `ks480-org-provisioner-gate`** (0 by `grep -il`). `git log` on the test file at the tip: last change `44fb6f388` (KS-480 §4 amendment); on `platform.ts`: `a105cd32b` (#1034, KS-1215) — `:64` and `:97` have not moved since the amendment.
- **Premise: the surface.** The cell constructs a bare `{ role }` principal and drives one exported guard function twice. No user store, no session, no MFA state, no JWT, no product bytes. AUTH surface, test-only pin (allowed).

## Collision

**Shared tamper line, different test file.** The held `READY_KS-1282-N99-1` (ks1215 real-app suite, `GET /api/platform/tenants` for a tenant ADMIN JWT) names the SAME `platform.ts:64` tamper; its cell lives in `ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts`, which this brief never touches. When N99-1 merges first, the SUPER_ROLES tamper will red that file's cell too — in a DIFFERENT file, so this brief's T6 (per-file red set) is unaffected. The held `READY_KS-1282-N96-1a/1b` pin the CONNECTOR-KEY dimension of the same six routes (block tampers on the guard mounts), not the role dimension. No held READY touches `ks480-org-provisioner-gate.test.ts`. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 01:xx, `--shared` scratch clone at `778e6cfe2`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after)

- REAL `tasks/test_only/checker.sh` on this brief's own diff: **RESULT: PASS (8/8)**, `apply=strict` (header counts right: 4 `+` and 1 context = 5). T5 green at the tip 14/14 cells in the file (13 at the bare tip — vitest counts each `it.each` row: 4 + 2 + 1 + 4 + 1 + 1 — plus the new one); T6 WIDENROLES reds exactly `provadmin`, T6 ADMINBRANCH reds exactly `provadmin`, every red an assertion failure — both read `AssertionError: expected [ …(2) ] to deeply equal [ [ 'ADMIN', false, 403, …(2) ], …(1) ]`, received `['ADMIN', true, 0, false, 'admin']` and `['admin', true, 0, false, 'admin']` (direct run with the default reporter, `direct_widenroles.out` / `direct_adminbranch.out`); T7 all three controls green under both; T8 `platform.ts` restored by bytes (sha256 7d04a92ca724 == tip blob) after each.
- Three WRONG variants refused at the named gates: a control declared as the PREFIX `401s an unauthenticated request` -> **FAIL T5** `DECLARED CELL NOT IN THE RUN` (`var1/`); the WIDENROLES tamper at `Line: 63` (off by one) -> **builder REFUSED rc 2** naming the tip's `:63` (an empty line) against the brief's From (`var2/`); a weakened cell asserting only `status !== 401` -> **FAIL T6** `reds NOTHING (0 of 14 cells failed)` under both tampers (`var3/`). Each checker variant ran in its own fresh `--shared` clone (the checker resets its clone at START, not END — measured: a direct `git apply` on the golden clone after the checker run landed the cell TWICE, 15 tests / 2 failed, until the clone was restored).
- Whole api-gateway vitest suite with the cell applied: **69 files, 679/679 green** (`full_suite.out`); the bare tip **69 files, 678/678** (`full_suite_tip.out`; +1 = this cell). `tsc` not run: `tsconfig.json` excludes `src/__tests__`.
- Input key set identical to `night/inputs/test_only_1232INFOEMPTY-1.json` (both directions empty). Source checkout tracked-modified count 0 before prepare, after prepare, after every checker run.
- Artefacts: `local-model/runs/2026-09-21_search-widen-drafter-precheck/` (build.log, prepare.log, checker.log, out.md, golden.patch.md, out.md.checker/, direct_widenroles.out, direct_adminbranch.out, direct_tip.out, full_suite.out, full_suite_tip.out, var1/, var2/, var3/, sweep/).
- NOT measured: the `register-connector` route itself (mount + handler + key mint) and the five `requireSuperAdmin` routes — the cell drives the guard function, not the app; no live stack was booted and no port was touched (the guard is called as a function with the file's fake req/res).

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts`, then the hunk above exactly as shown (`@@ -83,1 +83,5 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2. Refs KS-1283** (and KS-1282, whose #1101 cell is the one existing red under the same widening; KS-480 §4, the guard's amendment). **NEVER Closes** — KS-1283's six rows ask for route-level cells in the ks1215 real-app suite (guard + mount, "403 -> 201 and a key is minted"); this brief pins the GUARD the lead row mounts, not the mount, and none of the five `requireSuperAdmin` rows (`requireSuperAdmin` is not exported; `platformRbac.test.ts` restates it locally, so it cannot red on a product tamper).
- **Not from a gate cell.** Found by the 2026-09-21 widened test-only sweep (round 22, the 270 Backlog/Todo tickets outside the 88 file-named ones); the ticket's load-bearing premise (1 of 674 reds under the widening) was re-derived against this file's own refusal roles.
- **Not pinned here, said plainly:** the `register-connector` MOUNT (`:486-489`) and the five `requireSuperAdmin` routes; the 201-and-minted-key outcome under a widened list (needs the real app + a key-mint double, the ks1215 shape, a Claude seat or a later brief once the 13 held ks1215 READYs have merged).
- **Collision: shared tamper line with held N99-1, different file** (measured above).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1283 night/inputs/test_only_1283PROVADMIN-1.json night/briefs/KS-1283-PROVADMIN-1.md ctx=65536
```
