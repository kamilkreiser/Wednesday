#1267 KS-1295: store() no longer keeps a credential in memory silently
head 71f6f4d73cbde5b32f1564c9171eb1b705f77880

## What and why

`credentialRepo.store()` wrote the in-memory map and then returned on `if (!isDbAvailable()) return;` **with no log at all**. The caller is told the credential was stored, nothing reached PostgreSQL, and on restart it is gone — leaving no line to grep, no counter and no artefact, so the event cannot be investigated after the fact.

`#1231` made the **sibling** table-absent path loud (two WARNs per store). This is the path it did not touch, raised as **P-1** by that PR's gate.

**Shape (1) of the ticket only: LOG it**, naming the credential id and the reason. Shape (2) — refusing the write — is a behaviour change with its own decision and is deliberately **not** built here. (1) does not foreclose (2).

`loadFromDb()`'s identical early return at `:207` is a **startup read, not a store**, and is untouched. The file's bare silent returns go **2 → 1**.

## Why a new test file

`credentialRepo.test.ts` mocks `isDbAvailable` as a module-scope `vi.fn(() => false)`, so it **cannot produce the database-AVAILABLE arm** — and without that arm, "the WARN does not fire" would be untested. That file also carries 3 pre-existing `TS2339` (a KS-1090 residue) that are not this ticket's to disturb.

## Cells

| cell | asserts |
|---|---|
| **W1** database unavailable | exactly one WARN carrying `credentialId` and a non-empty reason; **no SQL issued at all** (so the WARN came from the fallback branch and not another); and the credential is still retrievable from memory |
| **W2** database available | **no such WARN** — *and* the INSERT is proven to have been issued with the expected parameters |
| **W3** two stores | two WARNs, in credential order — once per store, not once per process |

**W2's second half is the point.** Every cell asserting an absence needs a control proving the thing could have been present. Without it, W2 would also pass if `store()` had done nothing at all, or if the WARN text had simply been misspelled out of existence.

## Red proof

With the product reverted to develop:

| cell | reverted | with the fix |
|---|---|---|
| W1 | **RED** | pass |
| W3 | **RED** | pass |
| W2 | **green** | pass |

W2 staying green on both sides is correct, not a gap: it asserts an absence that holds before and after. It is the control, not a result.

## Test Evidence

**Touched**
- `services/vc-issuer/src/repositories/credentialRepo.ts` — the `store()` early return only.
- `services/vc-issuer/src/__tests__/ks1295-store-db-unavailable-warn.test.ts` — new.

**Ran**
- vc-issuer **129/129 at develop `4db87c3e4b98` → 132/132 here**, 14 files, `npx vitest run --no-file-parallelism`, **`packages/shared` BUILT**. The develop figure came from a separate worktree detached at develop.
- The red proof above.
- `npx tsc --noEmit`: **rc 0**. The new test file was additionally type-checked under a config with `exclude: []` (vc-issuer's program excludes `src/__tests__`): **0 errors in it**.
- Push preflight: **PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (legs 3, 4, 8 — local stack not up). Nothing failed.** Not a pass, and not quoted as one.
- Fleet STOP counts, read from each suite's own header: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60/0 of 60**. Zero `FIXTURE BUILD FAILED`.

- **`packages/shared` 941/941** (48 files, `npx vitest run`) in this worktree, identical to develop `4db87c3e4b98`'s 941/941. That package's guards read this lane's service sources by TEXT (the ks860 listen-call guard, the ks879 control-byte guard and the entrypoint corpus), so they are a cross-lane reader of this change and are run on every head raised.

**NOT run**
- No run against a real PostgreSQL; `isDbAvailable`/`query` are mocked.
- **The ticket's severity rests on an UNMEASURED reach, and this PR does not measure it.** Whether `isDbAvailable()` is ever false in the deployed Azure environment, and whether the least-privilege role can perform the existence check at all, were not read — both need a deployed read. The kintsugi log observation owed against KS-1281 has not been made. A WARN is an improvement regardless; it is not evidence the path fires anywhere.
- Preflight legs 3, 4, 8. Nothing deployed.

**Migrations + config**
- None. No migration, no config, no `package.json`, no lockfile, no `*.openapi.ts`.

Refs KS-1295

🤖 Generated with [Claude Code](https://claude.com/claude-code)
