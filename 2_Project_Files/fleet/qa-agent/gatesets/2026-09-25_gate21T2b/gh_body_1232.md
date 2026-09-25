#1232 KS-1128 SEEDWARN: a failed platform tenant seed logs WARN FAILED, 200 chars
head ec0d7efcf682112639505cf45baec71b899b665f

## BLUF

The platform tenant seed's catch logged at DEBUG as `Platform tenant seed skipped`, with the error truncated to 80 characters, so a seed that cannot seed reported into a level the demo does not read. It now logs at warn, names itself a failure - `Platform tenant seed FAILED (platform DB)` - and keeps 200 characters of the error, in the same shape as the main-DB arm.

## This PR NARROWS the ticket

The code ask is met. The ticket's proof instrument is a **real PostgreSQL** whose `tenants` table cannot take the insert, driven through the ks949 boot driver. This proves the arm with an in-process fake pg instead, so that bullet remains owed. The `:1142` inner catch, where a failing `tenant_config` row is swallowed silently, is the same class, is not in the ticket's ask, and is untouched.

## Test Evidence

**Touched** - `services/api-gateway/src/startup-migrations.ts` (+3/-1) and a new cell `services/api-gateway/src/__tests__/ks1128-platform-tenant-seed-failure-warns.test.ts` (+80).

**Ran, by me, at this head**
- api-gateway lane **bare 750/750** over 81 files at develop, **patched 754/754** over 82 files. `tsc --noEmit` rc 0 both sides.
- Red-first at the tip: 2 of 4 fail before the product hunk, 4 of 4 pass after.
- The cell boots the real `runStartupMigrations()` with `pg` redirected, for the product file only, to a fake Pool that throws on the seed INSERT. Its first control asserts the redirect took effect (`Module.createRequire(PRODUCT).resolve('pg')`) and that a clean run logs the INFO line, so the redirect is proven before any verdict is believed; a second control proves a refused seed does not escape.
- **Cross-package readers run, because three files read this product file BY TEXT** (the LEG D lesson: a text-pinned reader in another package reds a lane your own run never touches): `packages/shared` **918/918 bare -> 918/918 patched**, `services/auth` **828/828 -> 828/828**, and the shell suites **57/57 -> 57/57**. None moved.
- Applied blobs asserted: product `cd2583963f04` / 1229 lines, new cell `39e6b0a87e8c` / 80.

**NOT run**
- Push preflight verdict, verbatim: `PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 NOT run (local stack not up on :6882); no route, spec, served-spec or runtime-config surface here.
- **No real PostgreSQL.** That is the ticket's own instrument and it is not used here, as stated above.
- No image was built and nothing was deployed, so the WARN has not been observed in a real boot log.
- One `packages/shared` run reddened 4 cells, all `Test timed out` in repo-walk guard files this PR does not touch; re-run once, 920/920 with 0 timeouts, import phase 56.37s then 15.45s.

**Migrations + config** - none.

Refs KS-1128


🤖 Generated with [Claude Code](https://claude.com/claude-code)

