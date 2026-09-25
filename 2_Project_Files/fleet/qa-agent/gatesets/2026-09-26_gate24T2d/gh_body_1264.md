#1264 KS-1281: credentialRepo header no longer claims the table is auto-created
head 2e95121dfc475a09c81d61d61f9a81148b6bb0b9

## What and why

`#1231` (KS-1281) removed the runtime `CREATE TABLE` from `credentialRepo.ensureTable()`; what remains is an existence check (`SELECT 1 … LIMIT 0`), because the runtime role has no `CREATE` on schema `public`. Two comment blocks still described the **old** behaviour and were named as still-open on the ticket at the merge:

- the file header, `credentialRepo.ts:8` — "a dedicated `vc_credentials_store` table **(auto-created)**";
- the section heading, `credentialRepo.ts:24` — "**Table auto-creation**".

Both now say what the code does and name the migration path that owns the table (`migrations/001_initial-schema.sql`, `docker/init/03-service-tables.sql`).

**Comment-only.** No executable construct changed.

## AST-equivalence, with a control

Both revisions transpiled with `removeComments: true` and the emitted JavaScript compared:

| comparison | verdict | emit bytes | diagnostics |
|---|---|---|---|
| develop `4db87c3e4b98` vs this head | **EQUIVALENT** | 6490 vs 6490 | 0 / 0 |
| develop vs a tampered copy (one executable change: negated guard in `store()`) | **DIFFERENT** | 6490 vs 6489 | 0 / 0 |

The control matters: without it, "EQUIVALENT" is a verdict the instrument might return for anything. It reported the tamper's first divergent emit line (`if (!(0, db_1.isDbAvailable)())` → `if ((0, db_1.isDbAvailable)())`), so it discriminates.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts` — comments only (9 insertions, 4 deletions).

**Ran**
- vc-issuer: **bare 129/129 → patched 129/129**, 13 files, `npx vitest run --no-file-parallelism` in `services/vc-issuer`, **with `packages/shared` BUILT**. The bare figure was taken in a separate worktree detached at develop `4db87c3e4b98`, not by reverting this one.
- `npx tsc --noEmit` in `services/vc-issuer`: **rc 0**.
- AST-equivalence as tabled above, with its control.
- Push preflight, in this worktree's own hook: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.** Legs **3, 4 and 8** did NOT run (local stack not up). The preflight's own output says this is not a pass and must not be quoted as one.
- Fleet STOP counts, each read from its own `=== <path> ===` suite header rather than from a neighbouring summary line: `pre_push_hook_base` **28/0** · `pre_push_hook_base_fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**. No line starting `FIXTURE BUILD FAILED` (count 0).

**NOT run**
- Preflight legs **3, 4, 8** — the local stack was not up.
- No integration or end-to-end run against a live database. The touched file's DB paths are unexercised by this change because it changes no code.
- `credentialRepo.test.ts` carries **3 pre-existing `TS2339`** (`revoked`, `revocationReason`, `revokedAt` on `VCCredentialStatus`). They are a KS-1090 residue, not mine, and are unchanged. vc-issuer's tsc program excludes `src/__tests__`, so they do not appear in the rc-0 run above; they surface only under a config with `exclude: []`.
- Nothing deployed. No environment touched.

**Migrations + config**
- None. No migration, no config, no `package.json`, no lockfile, no `*.openapi.ts`.

## Scope

The ticket's other two open items — **Azure reach** and whether the least-privilege role can perform the existence check — are **UNMEASURED** and are not addressed here. Both need a deployed read, which this change does not have and did not attempt.

Refs KS-1281

🤖 Generated with [Claude Code](https://claude.com/claude-code)
