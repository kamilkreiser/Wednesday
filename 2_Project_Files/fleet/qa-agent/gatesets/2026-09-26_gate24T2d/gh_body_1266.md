#1266 KS-1120: pin the memory PREFIX class and the DB-miss to memory-get fallback
head 952f4329de97cd7f94ab6363e670248c456d0a54

## What and why

The KS-1020 fix (#966) is correct at head on every row the gate measured. What it lacks is **cover**: two classes of the exact-or-404 contract are unpinned, so a regression re-introducing either runs the vc-issuer suite **129/129 green**.

That is not repeated from the report — it is measured here. Both of the gate's tampers were applied to `develop` and the suite run:

| tamper | at develop (without these cells) | with these cells |
|---|---|---|
| **T4** — `startsWith` scan after the exact memory get | **129/129 green — invisible** | 130 pass / **1 red: X1 only** |
| **T5** — `return undefined` after the DB miss, skipping the memory get | **129/129 green — invisible** | 130 pass / **1 red: X2 only** |
| neither | 129/129 | **131/131** |

Each tamper reds exactly its own cell and nothing else.

### X1 — the PREFIX class (gate F-1)
Every partial-id cell in this file is a SUFFIX (`F4` bare uuid) or a MIDDLE (`M1`–`M6`, `F1`–`F3`) of the stored id. **None is a PREFIX.** So a `startsWith` scan is invisible to all of them, while `GET /https%3A%2F%2Fabc0.issuer1.example` answers 200 with someone's presentation.

X1 sends the VC base URL, which *is* a prefix, and asserts `storedId.startsWith(id)` — without that assertion the cell could pass on an id that is not a prefix at all and would pin nothing.

### X2 — memory-present, DB-absent (gate F-2)
No cell built a row that exists in memory and not in the DB, so `return undefined` after the DB miss — which skips the memory get — is invisible.

X2 makes the row memory-only by **rejecting the INSERT**, which is `storePresentation`'s real `catch` at `routes/presentations.ts:104-106`, not a contrived state. It then asserts:
- the INSERT really was attempted and rejected (exactly 1 matching call);
- the DB model really answers `{rows: []}` for that id;

so a 200 can only have come from the memory get. Without those two the cell could pass while measuring nothing.

**F-3 is not in scope** — #1145 (`497f69b96`) closed it.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts` — 54 insertions, 0 deletions. **Test-only. No product file is touched.**

**Ran**
- vc-issuer **129/129 at develop `4db87c3e4b98` → 131/131 at this head**, `npx vitest run --no-file-parallelism` in `services/vc-issuer`, **`packages/shared` BUILT**. The develop figure came from a separate worktree detached at develop, not from reverting this one.
- The four tamper arms tabled above. Red cells were read from `vitest --reporter=json` **`fullName`**, not from the summary line — the `✕` line carries no `describe` prefix, so two same-named cells in different describes are indistinguishable there.
- Each tamper asserts it **applied** and is **present in the file afterwards**, so a tamper that does not apply, or applies and is inert, cannot be scored as a pass. `presentations.ts` was verified byte-identical to its pre-tamper copy after every arm.
- `npx tsc --noEmit`: **rc 0**. vc-issuer's tsc program **excludes `src/__tests__`** (measured: 0 files from that directory in the program), so the touched file was additionally type-checked under a config with `exclude: []` — **0 errors in it**.
- Push preflight, this worktree's own hook: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.** Legs **3, 4, 8** did not run (local stack not up). Its own output says this is not a pass.
- Fleet STOP counts, read from each suite's own `=== <path> ===` header: `pre_push_hook_base` **28/0** · `pre_push_hook_base_fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Zero lines starting `FIXTURE BUILD FAILED`.

**NOT run**
- Preflight legs 3, 4, 8 — local stack not up.
- No run against a real PostgreSQL. The DB describe uses the file's existing `pgModel`, whose limits its own header states (`_`, interior `%` and escapes are not modelled). X2 does not widen that model; it only adds a row the model answers `{rows: []}` for.
- **X1 pins the memory path only.** The DB path's prefix class is already pinned by S1 (every SQL issued is `WHERE id = $1`, never a LIKE), so a DB-side prefix cell would be redundant; the ticket calls it optional for that reason.
- Nothing deployed. No environment touched.

**Migrations + config**
- None. No migration, no config, no `package.json`, no lockfile, no `*.openapi.ts`, no product source.

Refs KS-1120

🤖 Generated with [Claude Code](https://claude.com/claude-code)
