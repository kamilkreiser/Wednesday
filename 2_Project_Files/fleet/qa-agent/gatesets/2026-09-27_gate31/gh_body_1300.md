#1300 KS-1334 part B: route the remaining adminConfig 500s through the fail500 helper
head 5bd58f0ebd14bcf89fcde1fbb37434edee008eb5

## What this changes

`POST /api/admin/seed-demo-users` and `POST /api/admin/migrate-tenant-data` answered a 500 carrying the
thrown error's own text, with **no NODE_ENV guard**, so it reached the client in every environment
including production. Both now call the `fail500` helper: the thrown text is logged server-side with the
route named, and the client receives the constant `INTERNAL_ERROR` body.

**These are sites 4 of 4.** Part A (`cdba29ad711f`, #1294) converted the first two. `Refs KS-1334`.

Two files, **+53 / -6**:
- `services/originate/src/routes/adminConfig.ts` (+2 / -2) — the two `res.status(500).json({… message: err.message })` calls become `fail500(res, '<context>', err)` at `:2031` and `:2158`.
- `services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts` (+51 / -4).

The existing ks730c cell's SOURCE assertions move with the fix **by design**: `helperCalls` and
`distinctContexts` go 48 → 50, and the C4 list of UNCONDITIONAL sites becomes empty, because this change
converts the last two that were on it.

**Why the new cells drive the routes indirectly.** Neither handler reaches its outer `catch` through the
prisma mock the existing cells use, so each is driven through the first call its `try` block makes
outside any inner `catch`: seed-demo-users through the refusal warning of its closed demo-seed gate, and
migrate-tenant-data through the platform pool of its tenant manager.

## Provenance

The patch was **produced by the local model (Spark) under a Wednesday brief, and re-verified by this
seat.** It is byte-identical to the run's canonical patch (`patch.diff`, sha256 `30253f93…`, itself
`cmp` rc 0 against the concatenation of `section_1.diff` + `section_2.diff`), and the READY's fenced
block is byte-identical to that canonical patch including context lines, with a one-token control
confirming the comparison can see a difference. Applied **strictly, per section** (`git apply --check
-p1`, rc 0 each) at develop `94c9c7aa9be7`, **no recount and no fuzz**. Each section's strict check was
paired with a hunk-line-count tamper (`+N,999`) that git refused (rc 128, "corrupt patch") — so the
rc 0 is not a check that could not fail. **Wednesday's own harness figures are hers, not mine**; every
number below is from my own runs in this worktree.

## Test Evidence

**Touched:** `services/originate/src/routes/adminConfig.ts`, `services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts`

**Ran** — worktree detached at `94c9c7aa9be7` (`merge-base --is-ancestor` YES, against a control: #1296's
open head reads NOT an ancestor), `packages/shared` **BUILT** (`tsc`, 28 dist entries), `npm ci` 1936 packages:

| check | result |
|---|---|
| **RED** — test section applied, **product hunk withheld** | **4 failed / 19 passed / 23 total**, rc 1, **0 loadfail markers**; all four fail on assertions |
| **GREEN** — product hunk applied | **23 passed / 23 total**, rc 0, 0 loadfail markers |
| originate suite **BARE** (jest `--runInBand`) | 84 suites, **979 passed / 979 total**, rc 0 |
| originate suite **PATCHED** | 84 suites, **983 passed / 983 total**, rc 0 |
| **NEW reds** (patched failing set minus bare failing set) | **none** — both sets are empty |
| `packages/shared` (its guard suites read originate sources by TEXT) | 48 files, **945 passed**, rc 0, 0 `Startup Error` |
| `tsc --noEmit` — package program | rc 0. **But that program does NOT contain the test file** (`--listFilesOnly`: 0 hits) |
| `tsc` — **widened program proven to contain the test file** | `exclude: []` (an `extends` inherits `src/__tests__`); `--listFilesOnly` shows the test file **1 hit** and `adminConfig.ts` 1 hit of 716 files, control = 0 hits in the package program. **0 errors** |
| `eslint src` at **HEAD** | rc 0 — 22 problems (**0 errors**, 22 warnings) |
| `eslint src` at **TIP** | rc 0 — 22 problems (**0 errors**, 22 warnings) |
| HEAD-vs-TIP lint compared as **SETS**, not counts | **no row present at HEAD that is absent at TIP** |
| lint **control** — planted `debugger;` | lint rc **1**, `no-debugger` error at `:2031` → lint really runs and can fail. Restored by content, **sha256 identical** |

**The four RED rows, named descriptively.** Two of them are pre-existing cells whose titles embed a
foreign ticket key as file content, so they are named by position rather than pasted verbatim (a
hyphenated foreign key in a PR body attaches that ticket):
1. **C3 SOURCE** — all converted sites routed through the helper, each with a distinct context (`helperCalls`/`distinctContexts` 48 vs 50).
2. **C4 SOURCE** — the UNCONDITIONAL `err.message` sites are named, not silently left (the list is now empty).
3. **B1 `POST /seed-demo-users`** — the thrown message is not in the 500 body under production or any other NODE_ENV, and `fail500` logged it.
4. **B1 `POST /migrate-tenant-data`** — same, for that route.
Each reds on its assertion with the product hunk withheld, and each is green with it applied.

**Gate lines THIS push actually printed** (`s-b33-ks1334b-5bd58f0ebd14-push.out`, parsed per suite
block by exact basename — `pre_push_hook_base` is a prefix of two sibling suites, so a prefix match
misreads them). The fleet STOP count was **DECLARED** at `94c9c7aa`; this push is the **measurement**,
from a worktree that CONTAINS `94c9c7aa` with `packages/shared` built:

| suite | measured |
|---|---|
| `pre_push_hook_base.test.sh` | **28 passed, 0 failed** |
| `pre_push_hook_base_fixture_guard.test.sh` | **6 passed, 0 failed** |
| `run_shell_suites.test.sh` | **49 passed, 0 failed** |
| shell suites | **60 passed, 0 failed, 0 skipped (of 60)** |
| `^FIXTURE BUILD FAILED` | **0** |
| code guards | `OK — 13 code guards passed.` |
| preflight verdict | `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 need a local stack) |

Push rc 0; `ls-remote` after the push confirms `refs/heads/feature/ks-1334-adminconfig-500-part-b-b33-1`
at `5bd58f0ebd14bcf89fcde1fbb37434edee008eb5`; 0 orphaned `login_stub` pids left behind.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no `tsconfig` change (the
widened tsconfig used for the type-check was a temporary file, removed before staging and never
committed). Exactly **2 files staged**, asserted against a forbidden-path guard (`.env`, lockfile, keys).

**NOT run / NOT covered:**
- **No live or deployed exercise of either route.** This is unit-level only; the two handlers are driven
  through mocks, not against a running stack. **Nothing was deployed.**
- The integration suite (`test:integration`) was not run — it needs a live stack.
- Legs 3, 4 and 8 of the platform preflight do not run without a local stack.
- `revoke`-style side effects and the actual demo-seed path are not exercised; the B0 controls assert only
  that each route still answers its **own** refusal (403 / 400) and logs no error when nothing throws.
- The two pre-existing C3/C4 SOURCE cells are **source-text** assertions: they prove the call sites were
  converted, not that the routes behave correctly at runtime. The B1 cells are what cover behaviour.

Refs KS-1334

