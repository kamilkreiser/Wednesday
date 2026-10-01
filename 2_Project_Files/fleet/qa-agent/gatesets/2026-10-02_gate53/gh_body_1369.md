## What this does

`GHSA-frvp-7c67-39w9` (moderate, path traversal in `serve-static` on Windows via an encoded
backslash) is baselined with the reason *"fix is >=2.0.5 only, a semver-MAJOR v1->v2 bump"*.
**That reason is wrong.** The advisory has a **v1 patched range, 1.19.15**, so it is fixable
without the v2 migration. This PR fixes it with one scoped npm override and removes the
baseline row. **It narrows KS-530 and does not close it** — the v2 bump named in the ticket
title is still outstanding.

## The one vulnerable copy

All **45** tracked `package-lock.json` files parsed (not just the suspected ones):

| lock | `@hono/node-server` |
|---|---|
| `Blockchain/Dev/package-lock.json` | `node_modules/@hono/node-server` **1.19.17** (hoisted, patched) and `node_modules/@prisma/dev/node_modules/@hono/node-server` **1.19.11** |
| `Blockchain/Dev/services/mcp-server/package-lock.json` | **1.19.17** only |
| the other 43 | no entry |

**Vulnerable copies (< 1.19.15) across all 45 locks: exactly 1.** Its parent
`node_modules/@prisma/dev` 0.24.3 (`devOptional`) declares `"@hono/node-server": "1.19.11"`
**exactly**, so no caret admits the patch. The sole parent pulling `@prisma/dev` is
`services/originate/node_modules/prisma` 7.8.0, the CLI that `services/originate/package.json`
declares in devDependencies.

**Correction to the record:** `services/originate/package.json:60` does **not** declare
`@hono/node-server`. That line is inside originate's own `overrides` block, and npm honours
`overrides` only in the ROOT manifest of an install — so it governs originate's standalone
lock and is ignored by the workspace-root install. That is why the root lock still carried
1.19.11. **No `package.json` anywhere declares `@hono/node-server` as a dependency.**

## The override

```json
"@prisma/dev": { "@hono/node-server": "^1.19.15" }
```

in the `overrides` of `Blockchain/Dev/package.json` only, mirroring the existing scoped
`"jsdom": { "undici": ... }` entry. Scoped rather than top-level because it names exactly the
one parent that pins the vulnerable copy; a top-level pin would also constrain mcp-server's
path through the MCP SDK for no measured benefit (that path already resolves 1.19.17) and
would be a wider net to remember to remove when the v2 migration lands.

**Why `^1.19.15` and not `>=1.19.15`:** measured, not reasoned — `npm view` shows **2.x is
published** (2.0.0 … newest **2.1.3**). A bare `>=` would resolve the semver-major move this
ticket exists to do properly.

## It moves the EXECUTED code, not just the lockfile

The valibot entry in `// overrides KS 493` records an override that was **inert** because
`@prisma/dev` bundles valibot. That is a real risk, so it was tested rather than assumed:

- `bundledDependencies`: **None**.
- `@prisma/dev` loads the module as a **bare external specifier** — `await import("@hono/node-server")` — in three shipped dist files (`chunk-2O6J3K3T.js`, `index.cjs`, `daemon.cjs`).
- Hono's own internals (`createAdaptorServer`, `getRequestListener`, `serveStatic`): **0 files**. No inlined copy.
- The 31 shipped `.tar.gz` runtime assets: 0 contain the specifier (they are PostgreSQL extension tarballs; the decode instrument was checked by decompressing one).

**Resolution, by action:**

| | resolves `@hono/node-server` | path |
|---|---|---|
| from `@prisma/dev`, BEFORE | **1.19.11** | `node_modules/@prisma/dev/node_modules/...` |
| from `@prisma/dev`, AFTER | **1.19.17** | `node_modules/@hono/node-server` (hoisted) |

Controls: a nonexistent module gives `MODULE_NOT_FOUND`; the two resolved directories differ.
Note that `require.resolve('@hono/node-server/package.json', …)` throws
`ERR_PACKAGE_PATH_NOT_EXPORTED` — this package's `exports` map does not expose
`./package.json` — so the main entry was resolved and the owning package directory walked.

## How the lock was regenerated

Container `node:24-alpine`, **node v24.21.0 / npm 11.19.0**, both printed in the same run.
`Blockchain/Dev` mounted **whole**: the root lock carries `file:` link entries for the
workspaces, so a per-directory mount is the `EMISSINGTARGET` case recorded in KS 1394 — and
that was confirmed the hard way, when a two-file control directory rewrote the lock for
exactly that reason.

**The ruled command alone was inert, and that is stated plainly rather than papered over.**
Both `npm update @hono/node-server --package-lock-only --ignore-scripts` and then
`npm install --package-lock-only --ignore-scripts` printed `up to date` and left the lock
**byte-identical** (sha256 `79a1c682199c9327bc475c00…`, 674706 bytes, blob `c8cf17aa62a5`).
npm applies `overrides` when it BUILDS a tree; against an already-complete lock with no
version drift it never re-evaluates a newly added override against an exactly-pinned nested
dependency.

So the one stale entry `node_modules/@prisma/dev/node_modules/@hono/node-server` was
**removed by hand**, and the ruled command re-run; npm then validated the pruned tree
(`npm install --package-lock-only` rc 0). **npm did not produce this edit unaided.**

Two things corroborate that the result is a real re-resolution rather than a hand-authored
lock:

1. **An independent from-scratch resolve gives the same shape.** A throwaway project with
   `prisma@7.8.0` and this override, no lock, resolves `@hono/node-server` **1.19.17** with
   **no nested entry at all** — it dedupes. The same project **without** the override resolves
   **1.19.11**.
2. **The result is idempotent.** Re-running `npm install --package-lock-only --ignore-scripts`
   in the container returns rc 0 and leaves the lock byte-identical, and `npm ci
   --ignore-scripts` from it succeeds.

`npm`'s `up to date` banner is not evidence either way; the byte comparison is the instrument.

## The delta, per lock — NO COLLATERAL

Both lock blobs parsed as JSON and their `packages` maps diffed key by key, not eyeballed:

| | |
|---|---|
| entries | 1968 → **1967** |
| added | **0** |
| removed | **1** — `node_modules/@prisma/dev/node_modules/@hono/node-server` (was 1.19.11) |
| changed | **0** |
| `dev` / `devOptional` flag flips | **0** |

- `node_modules/@prisma/dev` is **byte-identical**: its `dependencies` map records the
  package's own manifest (`"1.19.11"`), not the override.
- The hoisted `node_modules/@hono/node-server` is **unchanged at 1.19.17**, so no `integrity`
  or `resolved` value is newly introduced.
- The other **44** locks are untouched — `git diff --numstat` lists none of them.
- Control: with a version change planted, the comparator reports 1 changed, so it can see a
  difference.

For contrast, the comparable undici override in KS 1378 carried **12** dev-flag bookkeeping
flips (eleven `lightningcss-*` binaries and `magicast`). None recurs here.

**A pristine control:** a full tree at this PR's base, with **no** override, given the
identical container command, leaves the root lock **byte-identical** (sha256 unchanged,
`cmp` rc 0). So the override supplies the direction and the command the re-resolution, and
neither alone moves the lock.

## The baseline row

`GHSA-frvp-7c67-39w9` removed from `scripts/audit/audit-baseline.json` (it was at `:88`).
Excised as a **text range**, not re-serialised: the diff is **0 added / 7 removed**, one JSON
object, trailing newline preserved.

> A first attempt re-serialised the file with `json.dumps` and escaped every em-dash and
> arrow to `\uXXXX` across 7 unrelated rows. The JSON-level comparison passed — the decoded
> values were equal — while the bytes had changed. It was reverted and redone surgically.
> **Both the value-level and the byte-level comparison are reported below.**

Proved by parsing both blobs:

- rows **25 → 24**; removed exactly `{GHSA-frvp-7c67-39w9}`; added none.
- surviving rows: **0** changed by value and **0** changed by raw bytes.
- `$comment` byte-identical; top-level keys unchanged.
- **no `expires` changed anywhere.** Dated rows 7 → 6, and the 2026-10-09 cohort is now
  exactly `GHSA-wrjc-x8rr-h8h6` and `GHSA-337j-9hxr-rhxg` (the react-router pair, KS 528).
- `GRANDFATHERED_NO_EXPIRY` untouched; `baseline-contract.mjs` and
  `baseline-contract.test.mjs` byte-identical by blob (`ef82d7c5211d`, `2379c0aeee6e`).
  The contract floor at `baseline-contract.test.mjs:217` asserts more than 20 entries; 24
  still passes and the floor is **not** lowered.
- Control: a planted byte edit makes the comparator report 1 differing row.

**The id still appears twice in the file after the removal** — inside the *reason* text of the
two react-router rows, which quote the instruction mail that named it. So the removal was
verified on the **row key**, never a substring search, which would have read as a failure
after a correct removal.

## Red-first control

With the row removed and **no** override, leg 6 goes **rc 1**:
`FAIL — 1 NEW advisory not in the baseline:` naming `GHSA-frvp-7c67-39w9`, baselined count
25 → 24. So the row is load-bearing today, and the **override**, not the deletion, is what
makes this head green. The baseline was then restored byte-exact (blob back to
`4e5f5daba207…`, `git status --porcelain` empty, rows 25) before the real change was made.

## The three audit legs

| leg | at the base | at this head |
|---|---|---|
| `audit:contract` | rc 0 — pass 59, fail 0 | rc 0 — pass 59, fail 0 |
| leg 6 `audit:gate` | rc 0 — `11 distinct advisories reported, 25 baselined.` | rc 0 — `9 distinct advisories reported, 24 baselined.` |
| leg 7 `audit:locks` | rc 0 — 43 standalone locks, 1611 packages, 6 match, 6 baselined | rc 0 — identical |

**The denominators moved**: reported 11 → 9, baselined 25 → 24, and `frvp` appears in
**neither** set at this head (0 mentions in leg 6's output).

**leg 6's CLEANUP line at this head, verbatim:**

```
CLEANUP (advisory): 15 baseline entries are no longer reported — remove:
```

🔴 **It now names `GHSA-92pp-h63x-v22m` (@hono/node-server, KS 470)** — the second hono row,
which was matching through the same 1.19.11 copy and no longer matches once it is lifted.
**Nothing is removed for it here.** That row is in `GRANDFATHERED_NO_EXPIRY`
(`baseline-contract.mjs:65`), and removing it would edit that set, which is not this PR.
Reported and left alone, following the KS 1378 precedent, which quoted its CLEANUP line and
left the cleanup to a separate change.

Leg 7's CLEANUP block cannot see these rows at all: it filters on
`e?.scope === 'standalone-locks'` (`audit-locks.mjs:299`) and no row carries a `scope`, so
it is not evidence either way.

## Prisma still runs

| | base | this head |
|---|---|---|
| `prisma --version` | rc 0 — prisma 7.8.0, @prisma/client 7.8.0 | rc 0 — identical |
| `prisma generate` | rc 0 — Generated Prisma Client (v7.8.0) | rc 0 — identical |
| `prisma dev --help` | rc 0 — prisma dev v0.16.28 | rc 0 — identical |
| `import("@prisma/dev")` | OK, 11 exports | OK, 11 exports |

`prisma generate` is the command `services/originate/Dockerfile:38` runs. It needs the schema
that `Dockerfile:36` copies from the **project root** (`COPY prisma/ ./prisma/`) — originate
has none of its own — so that copy was reproduced, the command run, and the copy deleted;
`git status` is clean. The `@prisma/dev` entrypoint was identified from the importer, not
guessed: `prisma/build/index.js` holds
`[{startPrismaDevServer},{ServerState}] = await Promise.all([import("@prisma/dev"), import("@prisma/dev/internal/state")])`.

## Images

**No image reads a lock this PR changes, so nothing was built.** Over all **35** tracked
Dockerfiles, every manifest `COPY` is per-service or per-package
(`services/<x>/package*.json`, `packages/shared/package*.json`, `frontend/<x>/package*.json`);
**0** copy the workspace-root lock. Control that must hit:
`services/originate/Dockerfile:28:COPY services/originate/package*.json ./`. Only originate
uses Prisma, and its builder installs from its **own** standalone lock, which has no
`@hono/node-server` entry at all — it resolves `prisma` 7.10.0 → `@prisma/dev` 0.24.17, a
version that no longer depends on the package.

## Alternatives not taken

Bumping `prisma` in the root tree would pull `@prisma/dev` 0.24.17 and remove the vulnerable
copy with no override at all. It moves the Prisma CLI and many lock entries, which is
collateral outside this PR's shape, so it is recorded here and not built.

No `// overrides` note was added beside the entry, following KS 1378, which added none; this
body carries the reason.

## Test Evidence

**Touched:** `Blockchain/Dev/package.json` (+3/−0), `Blockchain/Dev/package-lock.json`
(0/−11), `Blockchain/Dev/scripts/audit/audit-baseline.json` (0/−7). Three paths, all
`100644`, exec bits unchanged.

**Ran, at this head:**
- `audit:contract` rc 0 — pass 59, fail 0
- `audit:gate` (leg 6) rc 0 — 9 reported, 24 baselined
- `audit:locks` (leg 7) rc 0
- `services/originate` unit suite (**jest**) rc 0 — **90 suites, 1062 tests, 0 failed**
- `services/mcp-server` unit suite (**vitest**) rc 0 — **3 files, 5 tests, 0 failed**
- `tsc --noEmit` for both services — rc 0, 0 errors each
- `npm ci --ignore-scripts` from the new lock rc 0, then `npm run build --workspace=packages/shared` rc 0, with `@secuura/shared` proved to **resolve and require** (253 exports) from inside both services
- in-hook preflight on the push: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` All three skips carry one named reason, `SKIP — local stack not up on http://localhost:6882`. **Legs 6 and 7 ran inside the hook** and reproduced the figures above. Shell suites 67 passed / 0 failed / 0 skipped of 67; 13 code guards passed. 0 orphaned `login_stub` listeners.

**NOT run:**
- no service was started; no Schemathesis, Akto, k6 or Playwright
- no `prisma dev` **server** was started — only `--help` and the module import, so the running Prisma Dev server on 1.19.17 is unverified
- no image was built (nothing reads a changed lock)
- the three preflight legs needing the local stack
- `Blockchain/Dev/mobile/secuura-app` is outside the audit corpus (KS 769) and unmeasured
- the two react-router rows (KS 528) are untouched and still expire 2026-10-09
- the `GHSA-92pp-h63x-v22m` cleanup leg 6 now reports is deliberately left for a separate change

**Migrations + config:** none. No schema, no environment variable, no compose file.

Refs KS-530
