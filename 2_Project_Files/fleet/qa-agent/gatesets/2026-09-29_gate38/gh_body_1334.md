#1334 KS-888: pin that validate logs a failed usage write and never refuses
head 9b41a5fcc8fa20070aeff975a07a6f7aa13f7d99

## BLUF — TEST-ONLY. No product change.
Kam ruled card `secuura-ks888-validate-usage-write-failure` option **a** (2026-09-28 20:22:15):
*"Validate still answers from the key itself; a failed usage write is logged, never refused."*

**Measured at `0d156d12`: validate ALREADY behaves that way.** It calls `await dbSaveApiKey(apiKey);`
(`index.ts:1369`) with **no opt-in**; `dbSaveApiKey` logs one line (`:332`) and re-throws **only** for a
caller that opts in (`:336`). Only the mint (`:1141`) and the revoke (`:1293`, #1327) opt in. So there
is nothing to fix — only a behaviour to **pin** before someone changes it.

`Refs KS-888`, no closing keyword. **Not deployed.** Base `develop` `0d156d12cc0f`.
This is KS-888's **third** part: mint shipped in #1322, revoke in #1327.

## Why "the cells pass" proves nothing here, and what does
Because the product is already correct, **these cells are green at the untouched tip by design.** A
test-only pin whose only evidence is "it passes" is indistinguishable from a test that asserts
nothing. All of the discriminating power is therefore in the arms below, and each one is a real edit
to the real product file.

## Provenance
A Spark pass (`spark-dsv4flash`, briefed, first round, PASS 7/7). Verified **three ways myself**: the
READY's single fenced block, the brief-writer's golden and the checker's `patch.diff` are
**byte-identical**, sha256 `7c1ba3e062263c4b…`.
⚠ `hold_ready.py` **REFUSED** it (`checker.out has no 'mode: code_patch' line`) and it was held **by
hand** — the known code_patch-mode assumption for a test-only round, not a patch defect. One section,
one file, **+38/−1** per the checker; `git diff --stat` reads **+37** net, which is the same thing.

## Test Evidence

**Touched:** `services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts` **only**.
`git diff --name-only` proves the product file is untouched (0 matches for `src/index.ts`).

**RAN — all mine, on this worktree at base `0d156d12`** (security is **vitest**, not jest):
| run | result |
|---|---|
| `git apply --check` at the tip | rc 0 |
| security **baseline** at the untouched tip | **26 files / 270 tests, 0 failed, 0 Unhandled** |
| the pinned file with the pin | **19 passed / 19** |
| security **full, with the pin** | **26 files / 275 tests, 0 failed, 0 Unhandled** (+5 = exactly the new cells) |
| `tsc --noEmit` build program | rc 0, **0 errors** |
| `tsc` **including `src/__tests__`** | **2 errors — identical to the pristine tip's 2**, both in pre-existing `ks952-rate-limit-scope*.test.ts` (TS2339 and TS1343); restore sha256-verified. **Delta zero.** |
| `eslint src` — **run by hand** | rc 0, **0 errors, 0 warnings**; a planted `no-control-regex` **error** in the pinned test file → rc 1 with 1 error, restored by sha256 |

### Four tamper arms, each a real edit to `src/index.ts`
| arm | tamper | predicted | **measured** |
|---|---|---|---|
| A | the log line also carries `k.keyHash` | V2 only | **18 passed / 1 failed — RED V2** |
| B | `:332` deleted, no log line at all | V2 only | **18 / 1 — RED V2** |
| C | a **second** `logger.error` after `:332` | V2 only | **18 / 1 — RED V2** |
| D | **the REFUSE shape Kam ruled OUT** — validate opts in and answers 503 | 5 red | **14 / 5 — RED V1 ×3, V2 and the existing C3**, by assertion |

Arm D is written here from the ruled-out shape directly; the retired `briefs/KS-888-validate/`
material was not used. Restored after each arm with sha256 proved equal; 19/19 green afterwards.

**Push gate, from the raw hook log via `gatelines36`:** 28/0 · 6/0 · 49/0 · shell **60 passed, 0
failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` 0 · **13 code guards** · **VERDICT MATCHES** ·
**PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED**. **12/15 is not a pass.**

**NOT RUN:** no live stack and no Postgres — the cells drive the route with a stubbed `query`, so the
**real** failed INSERT is not exercised. Test-only, so **no §5f sweep is owed for this PR**; the
runtime behaviour it pins was already live. The four platform suites: **not run**.
**Migrations + config:** none.

## ⚠ Two doubts I did NOT close, and one I did — reported rather than buried
- **The ruling conflict.** Kam's 20:22:15 tap (log-only) and a 20:22:48 tap on an older card (refuse
  503) disagree. This PR builds **a**, per Wednesday's stated default, and a check-back is posted. **If
  Kam confirms "refuse", this pin is wrong** — and arm D shows exactly what it would cost: 5 cells.
- **A hung usage write is not covered.** Validate awaits the write before answering (`:1369`); the pool
  bounds only connection acquisition (`db.ts:33`, `connectionTimeoutMillis: 5000`) and the gateway's
  fetch has no timeout. A hung INSERT delays every validate — a latency path to the very lockout the
  ruling avoids. Not measured; a design change Kam did not rule on.
- **The `is_active` write-back doubt: I measured it, and it is REAL.** Filed separately — see the
  comment on this PR. It is not fixed here and this PR does not touch it.

Refs KS-888

