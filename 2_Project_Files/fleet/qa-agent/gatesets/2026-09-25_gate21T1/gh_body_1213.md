#1213 KS-530 PATCHLINE: mcp-server + originate take @hono/node-server 1.19.17
head f2751859c01565df066a3cdbe008e7360de4205a

## BLUF

The baseline row's premise is stale. `GHSA-frvp-7c67-39w9` carries **two** vulnerable ranges, and the 1.x one is patched: `< 1.19.15 -> patched 1.19.15`, alongside `>= 2.0.0, < 2.0.5 -> patched 2.0.5`. So no semver-MAJOR v1->v2 bump is needed for the two standalone locks that report it. Read from the GitHub advisory API, read-only, 2026-09-25.

This moves the pin in the two locks `audit-locks` reads, and nothing else.

| lock | before | after | flag | how |
|---|---|---|---|---|
| `services/mcp-server/package-lock.json` | 1.19.14 | **1.19.17** | PROD | `npm update` alone; transitive via `modelcontextprotocol/sdk`, which requires `^1.19.9`, so no manifest change |
| `services/originate/package-lock.json` | 1.19.11 | **1.19.17** | devOptional | one `overrides` line, because `prisma/dev` requires **exactly** `1.19.11` and `npm update` cannot move it |

*(npm scope sigils are omitted so the symbols stay searchable.)*

**Why this one mattered:** the `mcp-server` entry is **PROD**, and that image's final stage runs `npm ci --ignore-scripts --omit=dev`, which keeps a PROD dependency. The vulnerable copy was reaching a runtime image.

**Scope, per lock: added 0 / removed 0 / version-changed 1.** Platform discriminators unchanged — `mcp-server` `libc 10->10, os 53->53, cpu 52->52`; `originate` `os 27->27, cpu 26->26`. That check exists because an earlier attempt at this change silently deleted ten `libc` blocks including the `musl` markers every `node:24-alpine` image needs; that finding has its own Backlog ticket, named in the round record rather than keyed here so this PR does not attach to it.

## Test Evidence

**Touched**
- `Blockchain/Dev/services/mcp-server/package-lock.json` (+3/-3)
- `Blockchain/Dev/services/originate/package-lock.json` (+3/-3)
- `Blockchain/Dev/services/originate/package.json` (+2/-1)

No source file, no test file, no spec, no migration.

**Ran, by me, at this PR's head `f2751859c01565df066a3cdbe008e7360de4205a`**
- **`audit-locks` with the clock frozen at 2026-09-30T00:00Z: `GHSA-frvp-7c67-39w9` no longer lapses.** Advisory matches **24 -> 22**. The freeze is a `Date` preload outside the repo, with three controls: with the preload the repo's own `utcToday()` reads `2026-09-30`, without it `2026-09-25`, and an argument-bearing `new Date(...)` is unaffected.
- `audit-locks` bare (real clock): **rc 0**.
- A second, independent instrument: the repo's own `isLapsed()` called with an explicit date — 0 rows lapsed at 2026-09-29, exactly 3 at 2026-09-30, 5 at 2026-10-02; with boundary, never-expiring and malformed-value controls.
- **The in-hook push preflight, 12 of 15 legs:** leg 2 lockfile clean-room — **all 35 standalone locks pass `npm ci --dry-run`**, with `services/mcp-server` and `services/originate` both in the covered list; leg 5 audit-contract **59 cases pass**; leg 6 npm-audit gate **26 reported / 26 baselined, OK**; leg 7 standalone-lock advisories **22 match, 22 baselined, OK**; legs 1, 9, 10, 11, 12, 13, 14, 15 all OK. **Zero FAIL-shaped lines in the run.**
- Each lock proved self-consistent: an isolated resolution pass over it moves 0 versions.

**NOT run — say it plainly**
- The preflight's own verdict is **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`**, and it prints `This is NOT a pass. Do not quote it as one — say which legs ran.` The three are **leg 3** (spec-auth conformance), **leg 4** (path resolvability) and **leg 8** (served-spec consistency), each `SKIP — local stack not up on http://localhost:6882`. All three are stack-dependent and none touches a lockfile.
- **No runtime was exercised.** Nothing here was proved by booting `mcp-server` or `originate` on the new pin; the evidence is the lock, the advisory range and the clean-room install. A behaviour change in `hono/node-server` between 1.19.11/1.19.14 and 1.19.17 would not be caught by this PR.
- No image was built, so "the pin reaches the image" is measured from the lock's PROD flag plus the Dockerfile's `--omit=dev`, not from an image inspect.
- The four platform suites (Schemathesis, Akto, Playwright, k6) were not run: no service source, spec or route changed.

**Migrations + config**
None. No `.sql`, no env template, no compose file. One `overrides` key added to `services/originate/package.json`.

## What this does NOT clear

- **The workspace-root lock still reports the advisory**, through `prisma/dev`'s nested `1.19.11` (devOptional). No lock-only route moves it — measured: a plain refresh, `npm update`, a root `overrides` entry, and a full regeneration all leave it. That residue is Kam's card **`secuura-audit-root-lock-0930-remeasured`**.
- Whether `originate`'s devOptional copy survives into its runtime image is **not measured** — that needs an image build and inspect.
- The baseline row is **not** removed, because the root leg still reports it.

## Merge exposure

Merging this makes dependabot **#575** and **#949** dirty — both touch `Blockchain/Dev/services/originate/package.json`.

Refs KS-530

🤖 Generated with [Claude Code](https://claude.com/claude-code)

