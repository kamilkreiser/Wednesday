#1284 KS-730: stop returning the thrown message from adminConfig 500s
head dfc2468a547f0bb3d4995404942736312384539b

## BLUF
The third and last of KS-730's three files. `routes/adminConfig.ts`'s **46** inline handlers returned
`err.message` verbatim unless `NODE_ENV === 'production'`; all 46 now go through one small local
`fail500` helper that logs the message server-side under a distinct per-route context and answers the
constant body. No product behaviour changes beyond those 46 sites.

**Authorship:** the source change was built by the previous build seat, which has since wrapped. This
seat adopted the branch and worktree unchanged, diagnosed and fixed the failing cell, and raised the
PR — so the PR is this seat's, and the history before this commit is its author's.

## The cell was failing 9 of 12, and the cause was the cell's own fixture
This was re-measured here rather than inherited: `9 failed / 3 passed / 12 total`, reproduced exactly.

All four GET routes the cell drives open their catch with a **pre-existing benign branch**:

```ts
if (err?.message?.includes('does not exist') || err?.code === '42P01') {
  return res.json({ success: true, documentTypes: [] });   // 200
}
fail500(res, 'Admin config request failed (GET /api/admin/document-types)', err);
```

The cell threw `'relation admin_settings does not exist ks730c-private-detail'`, which **contains that
substring**. Every route took the benign branch, answered **200**, and **never reached `fail500`** —
the code this ticket is about never ran. Changing **only** that string, and nothing else, took the
cell from 9/12 to **12/12**. One variable, one outcome.

Worth stating because three cells were *passing* at 9/12 while the fix was never exercised: a fixture
that routes the subject down a different branch yields green cells asserting a property of a code
path that did not run.

Four things now stop that returning silently:
- the trap is written into the file at the `LEAK` definition, naming the branch and why the string
  must not match it;
- **C1 asserts the catch was REACHED** — `mockLoggerError`'s last call must be
  `[route.context, { error: LEAK }]`. A clean body is also what the benign branch and a mock-shaped
  crash produce; only `fail500` logs that pair. **This is the load-bearing assertion in the file.**
- **new `control KS-730 C0`** pins the benign branch: a `does not exist` error still answers 200 and
  never calls `fail500`. Same routes, same mechanism, different message, different answer;
- the `describe` was narrowed from *"the admin-config routes never..."* to *"the 46 converted
  admin-config sites never..."*, which is what is actually proved — see NOT COVERED.

## Test Evidence
Base this worktree **CONTAINS**: `d7cdecf1d2ee` (`merge-base --is-ancestor` YES). `node_modules` and
`packages/shared/dist` present. originate is jest, run **BARE and SERIAL** (`--runInBand`).

**Touched**
- `services/originate/src/routes/adminConfig.ts` (+69 / −46)
- `services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (new)

**Ran**
| suite | command / cwd | result |
|---|---|---|
| the cell | `npx jest <cell> --runInBand`, `services/originate` | **14 passed / 14** |
| originate, full, BARE | `npx jest --runInBand`, at base, cell absent | **74 suites / 878 tests / 0 failed** |
| originate, full, PATCHED | `npx jest --runInBand` | **75 suites / 892 tests / 0 failed** |
| `packages/shared` | `npx vitest run` | **48 files / 941 tests / 0 failed** |
| `tsc --noEmit` | `-p tsconfig.json`, `services/originate` | **rc 0, 0 output lines** |

Delta is exactly **+1 suite / +14 tests** — this cell and nothing else.

**Red proofs — 4 arms, `arms730c.py`.** Each asserts the tamper APPLIED (byte diff), reads the verdict
from `jest --json`, restores, and asserts the restore is **byte-identical**. **LOADFAIL is graded
separately from PASS**: 0 passed AND 0 failed is never read as "inert".

| arm | tamper | result | named reds |
|---|---|---|---|
| arm0 | none | 14/0 GREEN | — |
| **base** | `adminConfig.ts` restored to `d7cdecf1` | **5/9 RED** | C1 ×4, C2 ×4, C3 |
| **nobenign** | delete `/document-types`' benign branch | **13/1 RED** | **C0 only** |
| **fifthsite** | add a 5th unconditional `err.message` site | **13/1 RED** | **C4 only** |
| **wrongcontext** | `fail500` logs `context + ' TAMPER'` | **6/8 RED** | C1 ×4 **and** C2 ×4 |
| armfinal | none | 14/0 GREEN, source byte-identical to arm0 | — |

Zero LOADFAIL. `fifthsite` only adds, and `wrongcontext` keeps `logger` and `context` referenced, so
no arm could orphan an identifier.

**`packages/shared`'s 941/941 is a statement about this file, not silence about it.** Proved rather
than assumed: binding the cell's listener to `0.0.0.0` makes the ks860 loopback guard go
**1 failed / 24 passed, naming this file at `:78`**; restored byte-identical, **25/25** on both sides.

**NOT run**
- No local stack, so preflight legs 3, 4 and 8 are **NOT run**.
- No database. No integration cell here, and the merged ks1263 integration file was not run — it
  refuses any DSN outside `127.0.0.1:55410-55419`, which is not this seat's range.
- No deploy of any kind. No demo, no UAT.
- The other **42** of the 46 converted sites are covered by the **source** cell (C3), not driven end
  to end. Four are driven. That trade is stated in the file's own header.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no config file.
**No `withTenant(` call is touched** — `git diff` contains zero such lines (control: 9 exist in the
file), per the KS1304 ruling.

## NOT COVERED — and it is a real gap, now owned
Four handlers in **this same file** return `err.message` in a 500 body with **no `NODE_ENV` guard at
all**, so they leak in **production** too: `:113` `POST /refresh-tenants`, `:1859`
`POST /backfill-certification-metadata`, `:2031` `POST /seed-demo-users`, `:2158`
`POST /migrate-tenant-data`.

They are **pre-existing — 4 at the base `d7cdecf1d2ee`, 4 at this head** — and are a different, worse
class than this ticket's off-production ternary, which is why they are **not fixed here**: KS-730
enumerated 46 ternary sites and this PR converts exactly those.

Filed as **KS1334** (High). `KS-730 C4 SOURCE` pins all four **by enclosing route name** so a fifth
reds — and so that **fixing one also reds**, forcing the list to be updated as part of the fix rather
than drifting. KS1334's Done-when says so explicitly.

## For the gate
The fixture trap above is worth checking in any cell that asserts a catch body: an error string that
happens to match a benign early-return routes the request away from the code under test, and the cell
then passes or fails for reasons unrelated to the change. **C1's REACHED assertion is the load-bearing
one here**; a body-shape assertion alone would not have caught it.

Refs KS-730

