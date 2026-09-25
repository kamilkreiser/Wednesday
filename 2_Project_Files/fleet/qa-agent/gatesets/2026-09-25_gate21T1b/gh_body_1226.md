#1226 KS-872 JWKLOCAL: declare the JWK shape locally instead of crypto.JsonWebKey
head fcda1a6ef7e4fde33215466a29b730025fcd6233

## BLUF

`jwks.ts:129` read `jwk as crypto.JsonWebKey`. That interface was **removed** from the `crypto` namespace in `@types/node` 26.1.0, and the project tsc went red on develop **with nobody noticing** — because nothing runs `tsc -p packages/shared`. That second half is filed as **KS-1292**, related to this ticket.

One file. No tsconfig, `package.json` or lockfile change.


Branch `feature/ks-872-jwks-jsonwebkey-l3-r1-1` off develop `6ab9d5021e96`. Commit `fcda1a6ef`.
One file: `Blockchain/Dev/packages/shared/src/crypto/jwks.ts`. **No tsconfig, package.json or lockfile change.**

## The shape was chosen by measurement
Wednesday's ANSWER offered two shapes and left the choice open. A scratch tsconfig **outside the repo**,
`typeRoots` pointed at each installed copy in turn. Control first: the two roots really do resolve to
different versions (26.1.0 hoisted, 20.19.43 nested under `packages/shared`).

| shape | `@types/node` 26.1.0 | `@types/node` 20.19.43 (what resolves today) |
|---|---|---|
| `crypto.JsonWebKey` (OLD) | **TS2694** | rc 0 |
| a local interface | **rc 0** | **rc 0** |
| the DOM global `JsonWebKey` | rc 0 | **TS2345** |

**The DOM global is a REGRESSION**, not a safe alternative: it fails under the version this package
actually resolves, so it would have turned the repo tsc red the moment it landed — trading KS-872's bug
for its mirror image. Only the local declaration compiles under both.

## Red-proof, on the REAL file
Same scratch config, `include` pointed at the actual `src/crypto/jwks.ts`:

| file | against 26.1.0 |
|---|---|
| develop's | **rc 2** — `src/crypto/jwks.ts(129,51): error TS2694: Namespace '"crypto"' has no exported member 'JsonWebKey'.` |
| this branch's | **rc 0**, zero `jwks.ts` diagnostics |

That is KS-872's own error, at its own line and column. File byte-identical after restore
(sha256 `884b0aec7f6f1073`). In-repo `tsc -p packages/shared --noEmit` is rc 0 both before and after.

## Why it was green in the repo, and why the fix still matters
`npm ci` NESTS `packages/shared/node_modules/@types/node@20.19.43` beside the hoisted 26.1.0, and the
nested 20.x still carries `crypto.JsonWebKey` (`crypto.d.ts:513`); in 26.1.0 it moved to
`webcrypto.JsonWebKey` (`crypto.d.ts:3630`). **Nothing pins that nesting.**

## No new test — measured, not assumed
The runtime JWK→PEM path is ALREADY driven end-to-end by `jwks-verifier.test.ts`, which generates a real
RSA keypair, exports a real JWK and verifies a real RS256 token. Checked rather than asserted: feeding
the conversion `{}` reds **2 of its 6** cells. So a new runtime cell would duplicate existing coverage.
The **type** side stays unpinned until KS-1292 adds a preflight leg — which is exactly the gap that let
this sit red on develop unnoticed.

## Suites
918 passed (918) — unchanged, correctly, since no cell was added. tsc rc 0. Lint 36 problems
(1 error, 35 warnings), identical to bare.


## Test Evidence

**Touched**
- `Blockchain/Dev/packages/shared/src/crypto/jwks.ts` — one cast, plus the interface and its rationale.

**Ran** (worktree at develop `6ab9d5021e96` + this commit, `npm ci` rc 0)
- `npx vitest run --no-file-parallelism` in `packages/shared` → **46 files, 918 passed (918), rc 0**. **bare 918 / patched 918** — unchanged, and deliberately so: see *No new test* above.
- `npx tsc -p packages/shared --noEmit` → **rc 0**.
- `npm run lint -w packages/shared` → **36 problems (1 error, 35 warnings) — identical to bare.**
- the two-axis tsc table and the real-file red-proof above.

**NOT run**
- **Push-preflight legs 3, 4 and 8.** The hook ran **12/15; 3 SKIPPED (local stack not up); nothing failed**, and says *"This is NOT a pass. Do not quote it as one."* It is not quoted as one. No route, spec, served-spec or runtime-config surface here.
- The four platform suites — same reason.
- Any service unit suite. This is a compile-time cast in a shared library; no runtime behaviour, signature or export changes.

**Migrations + config**
- None.

Refs KS-872
Refs KS-1292

🤖 Generated with [Claude Code](https://claude.com/claude-code)
