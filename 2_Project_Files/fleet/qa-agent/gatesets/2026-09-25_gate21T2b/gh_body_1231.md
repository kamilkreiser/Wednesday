#1231 KS-1281 EXISTENCECHECK: vc-issuer credentialRepo sends no runtime DDL
head bd1d2daec2bf1b934437eae19c6239fe257305a6

## BLUF

`credentialRepo.ensureTable()` ran `CREATE TABLE IF NOT EXISTS vc_credentials_store` on every vc-issuer boot. Migration 001 already owns that table and the runtime role has no CREATE on schema public, so each boot logged a WARN. The call becomes an existence check, `SELECT 1 FROM vc_credentials_store LIMIT 0`.

The ticket offers two shapes - remove the DDL, or reduce it to an existence check. **This PR takes the second shape.**

## Test Evidence

**Touched** - `services/vc-issuer/src/repositories/credentialRepo.ts` (+3/-7) and a new cell `services/vc-issuer/src/__tests__/ks1281-vc-store-no-runtime-ddl.test.ts` (+46).

**Ran, by me, at this head**
- vc-issuer lane **bare 127/127** over 12 files at develop, **patched 129/129** over 13 files. `tsc --noEmit` rc 0 both sides.
- Red-first at the tip: the new file fails 1 of 2 before the product hunk, passes 2 of 2 after.
- The cell mocks the db module in the existing `credentialRepo.test.ts` shape with the database reported AVAILABLE and reads every statement back from the query mock: no `CREATE TABLE` is sent. Its control proves the credential row still reaches `vc_credentials_store`, so the cell cannot pass by the repository doing nothing.
- Applied blobs asserted: product `8a46bbf7f0d5` / 261 lines, new cell `125b65f81aaf` / 46.

**NOT run**
- Push preflight verdict, verbatim: `PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 NOT run (local stack not up on :6882); no route, spec, served-spec or runtime-config surface here.
- **No database was touched.** A database NOT built by migration 001 previously had the table created for it at runtime and no longer will: its first store will warn and fall back to memory. No environment's DB was inspected.
- **Whether the least-privilege role can SELECT this table on every environment is NOT measured.** `provisionAppRole` grants SELECT on ALL TABLES in schema public - read from source, not probed. If it cannot, the WARN keeps firing, as it does today.
- The ticket is a boot WARN, so the observation it waits on is a kintsugi log read after a deploy. Nothing is deployed here.

**Migrations + config** - none. No `.sql`, no env template, no compose file.

Refs KS-1281


🤖 Generated with [Claude Code](https://claude.com/claude-code)

