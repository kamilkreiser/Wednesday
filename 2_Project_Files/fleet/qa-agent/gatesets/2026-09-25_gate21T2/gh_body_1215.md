#1215 KS-1288 LEGDBYTEXT: LEG D pins its three api-gateway sites by text, not line
head 5e3419a46db5a1a4e7e640aee2e60dd89db3912a

## BLUF

LEG D of the ks781 body-parser-order suite named its three post-guard parser sites by **line number**. Six edits that touched none of those routes moved the list and reddened `packages/shared`: KS-818 (+14), KS-833 (+10), KS-858 (+14), KS-1126 (-8), KS-1195 (-1), KS-1239 (-18). Every one of them was an edit **above** the sites. This pins them by **text** instead.

`ParserSite` gains an `anchor`: the call the parser is an argument to, carrying that call's first string literal when it has one — `app.post('/api/auth/wallet/challenge')` for a route, `createVerificationRoutes(…)` for a factory handed an object. `line` is unchanged and still carries every diagnostic.

**One file. Test-only. No product code, no config, no dependency, no lockfile.**

## Why the anchor is derived the way it is

The walk in `siteAnchor` is **the same walk `classify` uses to decide `kind`** — the first enclosing `CallExpression` that has this node inside one of its ARGUMENTS. So the anchor names the very call that decided the classification, by construction rather than by coincidence. A node with no such call reads `(top level)`, never an empty string: an anchor that cannot be derived must not compare equal to another one.

## The red-proof — the edit that broke it six times

Eighteen lines of pure comment inserted above the routes in `services/api-gateway/src/index.ts` (KS-1239's exact shape; the challenge route moves 827 → 845):

| test file | index.ts | result |
|---|---|---|
| **develop's** (`6ab9d5021e96`) | tampered | **2 failed** — `expected [ 845, 858, 891 ] to include 873`, and the three-site list |
| **this PR's** | tampered | **8 passed** |

Both files restored byte-exactly afterwards (`sha256` equal to the pre-tamper reading; `git diff --name-only HEAD -- index.ts` = 0 lines).

## Tamper matrix — every new cell is live

| # | tamper | expected | measured |
|---|---|---|---|
| T-A | `siteAnchor` always returns `(top level)` | red | **5 failed / 3 passed** |
| T-B | `siteAnchor` drops the string literal (always `…`) | red | **4 failed / 4 passed** |
| T-C | the no-call fallback returns `''` instead of `(top level)` | red | **1 failed** (the emptiness control — the only cell that guards it) |
| T-D | LEG D pinned back on `x.line` | red | **1 failed** (the names-WHERE cell) |
| T-E | the `+18` shift assertion weakened to `+0` | red | **1 failed** (the shift cell) |

Baseline between every tamper: **8 passed**. File restored byte-exactly at the end (`sha256` match).

T-A is worth reading: the "anchors are unchanged" cell alone **passes** when every anchor collapses to one constant — which is exactly why cells 2–4 exist. The vacuity is closed by measurement, not by assertion.

## Test Evidence

**Touched**
- `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` — the only file in this PR.

**Ran** (worktree `s-l3-ks1288` at `6ab9d5021e96` + this commit, clean `npm ci` at `Blockchain/Dev`, rc 0, 1936 packages)
- `npx vitest run --no-file-parallelism` in `packages/shared` → **46 files, 922 passed (922), rc 0**, 42.5 s.
  **bare 918 / patched 922** (+4 = the four new cells).
- `npx tsc -p packages/shared --noEmit` → **rc 0**, zero output. Live: a planted `const x: number = 'not a number'` gives rc 2 / TS2322, and the bare re-run after removal is rc 0 again.
- `npm run lint -w packages/shared` → **36 problems (1 error, 35 warnings), rc 1 — byte-identical to bare on the clean tip.** The 1 error is the pre-existing `no-control-regex` at `src/middleware/index.ts:521`, recorded in `BACKLOG.md`. Control: `npx eslint` on the touched file alone resolves a config and reports clean, so "36 == 36" is a comparison and not a blind spot.
- the red-proof and the five tampers above.

**Bare baseline, disclosed**
The bare number moved once across two runs of the same tree: **run 1 (cold) 917/918 rc 1**, `threadToken.test.ts > returns different policy IDs for different seeds` — `Test timed out in 30000ms`, the test's own per-test argument, at 34.2 s under five concurrent seats; the file alone is **15/15 in 2.35 s**; **run 2 (warm) 918/918 rc 0**. Bare is taken as **918**. A `threadToken` timeout is a load flake, not a finding against this change.

**NOT run**
- **Push-preflight legs 3, 4 and 8.** The hook ran **12/15 legs; 3 SKIPPED (3, 4, 8 — local stack not up); nothing failed.** Its own closing words are *"This is NOT a pass. Do not quote it as one — say which legs ran."* So it is not quoted as one. This PR has **no route, spec, served-spec or runtime-config surface**, so those three legs have nothing to say about it. Per the fleet ruling of 2026-09-25, no seat starts the local stack mid-round; a PR that *does* have a surface carries "legs 3/4/8 owed at the gate" instead, and this one does not.
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6). Same reason: one test file inside `packages/shared`, no deployable surface. Named rather than implied.
- Any service unit suite other than `packages/shared`. `services/api-gateway/src/index.ts` is **read** by this suite and is **not modified** by this PR — it was tampered and restored byte-exactly during the red-proof.

**Migrations + config**
- None. No migration, no `package.json`, no `tsconfig`, no lockfile, no env var, no `.githooks` change.

Refs KS-1288


---
*Gate note, verbatim from the push hook:* `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed. legs 3 4 8 — local stack not up … This is NOT a pass. Do not quote it as one — say which legs ran.` Head `5e3419a46db5a1a4e7e640aee2e60dd89db3912a`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
