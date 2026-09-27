# KS-888 rev 2: NOT BRIEFED. The ticket's fix shape crashes two other routes. A ruling is needed first.

Written 23:48 AEST 2026-09-27 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state, mailed nobody and wrote nothing under `!CODING/`. Every git write verb (clone, fetch, checkout, stash) ran in the scratch clone `a0b3d8ae-.../scratchpad/ks888brief/base`. That clone is `--shared` from the 09-26 `sparkfeed`, which was only read. The tip was fetched by SSH. node_modules were farmed by `tasks/code_patch/prepare_clone.sh`, which exited rc 0 and left the source checkout with 0 tracked-dirty lines before and after.

**Verdict: STOP, per the brief-writer rule "if the fix needs a design decision, write only README.md".** There is no `KS-888.md` and no `KS-888.golden.diff` in this directory, on purpose.

- **Base:** develop `958df2465368c3c7c68acacd68b1833f13a3b752`, confirmed by `git ls-remote` at 23:4x.
- **Product file:** `Blockchain/Dev/services/security/src/index.ts`, blob `84b39f638ffc`. It is byte-identical (`cmp`) to Wednesday's `k888/w/.../index.ts`.
- **Express:** `express@4.22.2`, as installed in the farmed node_modules.

## Why it is not briefable as a one-file local-model round

The ticket's fix shape puts the re-throw inside `dbSaveApiKey`: structural SQLSTATE classes 42, 23 and 22 re-raise, and 08 and 57 stay log-only. That changes ALL THREE callers, and two of them cannot handle the throw:

| call site (tip) | handler | what catches a throw |
|---|---|---|
| `:1132` POST `/api/keys` (mint) | `:1043`, `async (req, res, next)` | `try` … `:1162 catch` → `:1166 next(error)` → `errorHandler` → **500**. This is the intended fix. |
| `:1267` DELETE `/api/keys/:id` (revoke) | `:1229`, `async (req, res)`: **no `next`, no try/catch** | nothing. Express 4 does not forward a rejected async-handler promise. |
| `:1335` POST `/api/keys/validate` (the gateway's pre-session check for every `sk_*` key, unauthenticated, `:679`-`:684`) | `:1281`, `async (req, res)`: **no `next`, no try/catch** | nothing. |

Security's boot block (`:1577`-`:1607`) installs no `unhandledRejection` listener. A case-insensitive grep of `unhandledrejection` over security `src` found 0 hits. As a positive control, the same grep over `packages/shared/src` did hit `gracefulShutdown.ts`, but security never wires it, and its default mode is `'exit'` anyway (`gracefulShutdown.ts:35`). The Dockerfile runs `node:24-alpine` with `CMD ["node", "dist/index.js"]`. Node 24's default for an unhandled rejection is to throw. Measured: `node -e "Promise.reject(new Error('x')); setTimeout(()=>console.log('alive'),200)"` gave rc 1, and `alive` was never printed.

### Measured: the probe

The probe was a vitest file in the scratch clone. It mocks `../db` with `isDbAvailable` true, and the INSERT into `svc_api_keys` rejects with the given `code`. It drives the real app over HTTP with the ks742 RS256 platform token. The same probe ran against the tip and against the candidate fix. The candidate is the ticket shape: log `code`, plus `if (typeof err?.code === 'string' && /^(42|23|22)/.test(err.code)) throw err;` after `:332`.

| cell | tip `958df246` | candidate fix |
|---|---|---|
| mint, INSERT 42703 | **201** + `sk_…` key material (the bug) | **500** `INTERNAL_ERROR`, no key (fixed) |
| mint, INSERT 08006 (transient) | 201 | 201 (control holds) |
| mint, INSERT ok | 201, INSERT issued | 201, INSERT issued |
| **validate an ACTIVE key, INSERT 42703** | 200 `valid: true` | **no response: client timeout after 3 s, plus vitest "Unhandled Rejection" (`dbSaveApiKey` ← `index.ts:1336`)** |
| **revoke, INSERT 42703** | 200 "API key revoked" (in-memory only, the swallow) | **no response: client abort after 3 s, plus "Unhandled Rejection" (← `index.ts:1268`)** |
| (stack lines are in the candidate file, +1 vs the tip) | | |
| vitest totals | 3 passed, 0 errors | 3 passed, **2 errors (Unhandled Rejection)** |

Under production node the candidate turns two cases into a process exit:
- any structural error on the usage-count save in `/api/keys/validate`;
- any structural error on a revoke.

Take the case the 09-15 READY's own test simulates: a missing column (42703) after a migration drift. Under the candidate, **every `sk_*` API-key validation would crash-loop the security service**. Today those same calls answer `valid: true`.

**The existing suite is blind to this.** The whole security suite (`npx vitest run` in the scratch clone) gave:
- tip: 23 files / 247 passed;
- candidate: 23 / 247 passed, 0 unhandled errors.

No existing test runs a key route with the DB "available".

This also explains why the 2026-09-15 Ornith READY scored PASS 7/7: its test drives mint only. Its note names `:1261` / `:1329` as blast radius, but nothing exercised them.

### The decision a brief cannot make (for Kam, via Wednesday)

Pick one. Each option then becomes briefable with at most 3 edit points in `index.ts` plus one new test file.

1. **Mint-only strictness.** The re-throw is opt-in from the mint call alone, e.g. `dbSaveApiKey(k, { strict: true })` at `:1132`. Revoke and validate keep today's swallow, byte for byte.
   - Closes the ticket's title case (a 201 for a key that never persisted).
   - Does NOT close "ALL key persistence": a revoke that does not persist still answers 200, and the key comes back live after a restart.
2. **All sites, each with a ruled outcome.** Revoke on a structural error answers what? A 500? With what body? The in-memory `isActive = false` is already applied at `:1266`: keep it or roll it back? Validate's usage-count save: fail-open (log-only, today's behaviour) or fail-closed (refuse the key)?
   - This is 3 or more edit points, the DELETE handler signature change included, and it carries two product semantics.
   - It probably belongs to a cloud round, not Spark.
3. **Route-level async error forwarding for Express 4** across the service. That is a different ticket.

Option 1 is the one a Spark round can carry. It still narrows the ticket, so it needs the ruling "refs KS-888, does not close it" or a ticket split.

## Why the 09-15 READY no longer applies (measured, not assumed)
- **Product hunk:** content drift. The catch is now at `:331`-`:333`, and the context above it was re-indented and extended by the KS-869 and KS-458 comments. Wednesday's `patch -F0` gave rc 2.
- **Test hunk, "unexpected end of file in patch":** this is NOT a glued fence. The READY's closing fence sits on its own line (`READY…diff.md` line 136). The cause is a **header/body count mismatch**: the header says `@@ -0,0 +1,120 @@`, but the body has **110** `+` lines (counted with `l and l[0]=='+'`). `patch` runs off the end looking for 10 more lines.
- The product hunk's header is also inconsistent: `-327,7 +327,10`, while the body carries 9 context, 1 `-` and 5 `+` lines (old 10, new 14). The stub-merge splitter kept the model's headers, not recomputed ones.

## Artefacts (scratch, ephemeral)
All under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/ks888brief/`:
- `zz-probe.test.ts` is the probe. It was moved out of the clone after the run.
- `probe_tip.log` / `probe_tip.out` and `probe_fix.log` / `probe_fix.out` are the per-cell results and the vitest output.
- `candidate_fix.diff` is the ticket-shaped product change used for the probe.
- `suite_before.out` / `suite_candidate.out` are the two whole-suite runs.
- `index_tip.ts` is the tip blob.

## NOT MEASURED
- **The probe is not an actual production process exit.** The exit is inferred from:
  - node 24's default, measured with the one-liner above;
  - no listener in security, measured by grep with a positive control;
  - vitest's Unhandled Rejection report plus the hung requests, measured.
- Whether any deployment sets `NODE_OPTIONS=--unhandled-rejections=warn` was not checked (Container Apps env).
- The Linear ticket text was not re-read by this agent. The fix shape is as Wednesday relayed it.
- No brief, no golden and no `build_input.sh` run. `build_input.sh` was not invoked, because there is no brief for it to find.
- No Spark round.
