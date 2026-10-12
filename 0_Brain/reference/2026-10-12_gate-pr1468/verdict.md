# Gate verdict: PR #1468 (KS-1210 contract half, the closed OAuth scope enum)

**VERDICT: GO WITH NOTE** for head `01b2b0209aed6d74f4a8cd0576071d93b16f906f`
Gate: an independent Opus QA gate, 2026-10-12, finished 07:26Z. Read-only. All runs are in my own clone (`git clone --no-hardlinks`) in the session scratchpad. Logs are in `logs/` beside this file.

## Refs (ls-remote at 07:26Z)
- `refs/pull/1468/head` = `01b2b0209aed6d74f4a8cd0576071d93b16f906f`. It matches the brief.
- `develop` = `f9c7880f91dba5e74d5148af2a99bb411b4d4410` (the #1464 / KS-839 merge). **The brief said develop had moved past the seat's base. It has not.** `00d27598` is the parent of `f9c7880`, so the seat's base IS the current tip.
- Merge-base of the head and develop: `f5a24026`. Two commits: `6559a9a` and `01b2b02`. Between them, `01b2b02` changes exactly one line, a header comment in the test file. I verified this.
- **The predicted merge is clean, tree `aabab8d6ffda3e271cf1a70cde86fbf953022f33`.** This is my own `git merge-tree` run, and it equals the seat's tree. I built a local merge commit `a3cf3c12` in my clone only.

## Q1 first: is auth.openapi.ts used for runtime validation? **No. It only generates the spec.**
- No runtime module imports `auth.openapi.ts`. I searched the whole Dev tree, case-insensitive. The only importers are tests (for example `s130-f6`) and comments in `routes/auth.ts`, `routes/mfa.ts` and `api-gateway/src/index.ts`.
- Runtime validation lives in `services/auth/src/routes/oauth.ts`:
  - `CreateOAuthAppSchema` at :1182-1189
  - `UpdateOAuthAppSchema` at :1301-1304
  - Both already use `z.array(z.enum(AVAILABLE_SCOPES))` on develop.
  - This PR does not touch that file.
- **The PR therefore changes no request outcome.** Any value outside the nine was already a 400 at runtime. The spec now says what the service already does.
- Stored or legacy values: response schemas (`OAuthApp.allowedScopes` and the others) stay `string[]`, which is correct. The DB default (`038a:55`, four scopes) is inside the enum.
- The new import of `services/oauth` brings `db.ts` into the generator's import graph. That adds nothing new: `db.ts` creates its pool lazily, and `passwordLoginGate` already imports `userRepo` and through it `db`. The generator runs with `DATABASE_URL` unset (rc 0).

## (1) The diff
- Exactly three files:
  - `auth.openapi.ts`: one import, plus the two `scopes` lines at :2273 and :2902
  - `secuura-api.yaml`
  - the new test file
- Nothing else changes.
- The yaml hunks are the intended ones only:
  - the enum anchor `&a23` at OAuthAppCreateRequest
  - `enum: *a23` at the PATCH body
  - an anchor renumber of an unrelated example, `&a23` to `&a24`, together with its alias
- The merged tree against develop has the same three files and the same four hunks.
- `generate-openapi` reproduces the yaml byte for byte: sha256 `fb73ebf5…` on both sides.
- `check:openapi` passes on the head, the merged tree and the base. That includes `check:spec-examples`: 406 example blocks, all resolve.
- Control: I deleted one enum line, and `--check` then gave CHECK FAIL rc 1.

## (2) The new cells (5: 2 RED, 3 CONTROL)
- On the base (develop's yaml and auth.openapi.ts, with the head's test): **2 failed**, both RED cells with `expected null`. The 3 controls stayed green.
- On the head: 5 out of 5 green.
- Planted mutations, each red only where expected:

| Plant | Cells that went red |
|---|---|
| P1: create-only enum loses `admin:write` (PATCH given an inline full list) | create RED only |
| P2: PATCH enum removed | PATCH RED only |
| P3: create reordered | both |
| P4: PATCH alias pointed at the wrong anchor `*a24` | PATCH RED only |
| P5: extra `"*"` value | both |
| P6: `AVAILABLE_SCOPES` gains `subjects:erase` | both REDs plus the count control |

P3 and P5 turning both cells red is correct, because the PATCH body aliases the create anchor.

## (3) Suites, tsc, eslint (services/auth)

| Tree | Files | Tests | tsc (src) | tsc incl. tests | eslint |
|---|---|---|---|---|---|
| head | 85/85 | 899/899 | 0 | 42 errors, 0 in the new file | 0 errors, 15 warnings |
| base f9c7880 | 86/86 | 908/908 | 0 | 42 | 0 errors, 15 warnings |
| merged aabab8d | 87/87 | 913/913 | 0 | 42 | 0 errors, 15 warnings |

- Merged against the base: +1 file and +5 tests, which are this PR's.
- The head count matches the seat's own logs: 85/899 twice.
- The 42 tsc errors in test files exist before this PR. Control: other test files do report errors, for example `ks431` has 2.
- tsc control: a planted type error in `auth.openapi.ts` made tsc report TS2322.
- None of the 15 lint warnings is in a touched file.

## (4) Enum against the authoritative set, examples and consumers
- The enum is imported, not retyped. It equals `services/oauth.ts:57-67 AVAILABLE_SCOPES` in order: nine values, no drift, nothing missing, nothing extra. Parsed with the real `yaml` lib, both sites resolve to the same nine.
- No other OAuth-app request body carries scopes. I enumerated every `scopes` property in the spec. `rotate-secret` has no scopes in its body.
- Examples:
  - OAuthAppCreateRequest's example has no `scopes` key: `{name, redirectUris}`.
  - The PATCH body has no example.
  - So nothing can violate the enum. `check:spec-examples` is OK.
  - The developer portal curl example (`developer-portal.html:443`) uses `verify:read`, `documents:read` and `certifications:write`, all inside the enum.
- Consumers:
  - The gateway's `buildSpecMethodMap` is identical on the base and the merged tree (310 entries). The gateway uses the yaml only for docs and the method map, never for body validation.
  - No SDK generator is declared in any package.json.
  - No frontend, mobile, connectors, packages, Extranet or platform-s-main file calls `/api/oauth/apps`.
  - Controls: the frontend has 5 files hitting `/api/auth/`. Extranet has 15 files and platform-s-main 32 that match `api/`.

## (5) Deploy note
- `docker-compose.yml:553` bind-mounts the single file `secuura-api.yaml` read-only into api-gateway.
- In production there is no hot-reload. A delivery by replacement (rsync or image) leaves the mount on a dead inode until `docker compose restart api-gateway` runs. Until then, `/api/docs` serves the old, wider type. That is stale docs only: the method map does not change and there is no runtime effect.
- There is no migration and no auth service code-path change.

## Defects
None Major.

1. **Minor (nit), `services/auth/src/__tests__/ks1210-contract-publishes-the-closed-oauth-scope-enum.test.ts:13`.** The header says the scan's control checks a sibling field "(`redirectUris`, `name`)". `SITES` (:86-87) checks only `redirectUris`. The prose overstates the control. It does not affect correctness.

## Note (not this PR's defect)
- **Pre-existing:** `packages/shared/src/security/scopes.ts` calls `SCOPES` the "single source of truth … used by OAuth apps". But the OAuth app vocabulary is `AVAILABLE_SCOPES`, which includes `verify:read`, `webhooks:manage` and `admin:read/write`, none of which are in `SCOPES`. The published enum correctly follows the list the runtime enforces. The two-vocabulary wording is worth a follow-up ticket.

## Not checked
- The live or deployed gateway (no deploys).
- Schemathesis against a running stack.
- Prod or demo DB contents of `oauth_apps.allowed_scopes`. This is irrelevant to this PR, because the PR changes no runtime path.
- `npm ci` ran with `--ignore-scripts`, then `npm rebuild argon2 bcrypt`. The same install was used for all three trees.
