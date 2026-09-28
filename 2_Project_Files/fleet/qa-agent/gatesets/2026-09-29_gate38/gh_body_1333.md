#1333 KS-1124 F4: a certification whose anchoring failed saves status failed
head 91ceb5bc0a79fd3dceb044837955c07d553771fb

## BLUF
Kam ruled card `secuura-ks1124-f4-failed-anchor-shows-pending` option **b** (2026-09-28 20:22):
*"Save a 'failed' status the gateway already reads as off-chain-only"*.

Both certification routes — `/issue` and `/:id/recertify` — now put `status: 'failed'` in the saved
`blockchain` blob when `anchoringStatus === 'failed'`. **The success leg is untouched** and stays
statusless `pending-onchain`; relabelling `confidence` would have been option **a**.

Without it, an issue whose anchoring failed saved a **statusless** `pending-onchain` blob, so the
document read as *pending anchoring forever* rather than off-chain-only.

**Scope: this covers KS-1124's F4 part only** and is not the whole ticket. `Refs KS-1124` — deliberately no closing keyword, so nothing here moves or closes the ticket. **Not deployed.**
Base `develop` `0d156d12cc0f`.

## Provenance of the patch
A Spark pass (`spark-dsv4flash`, briefed, first round, PASS 7/7). I verified the patch **three ways
myself**: the READY's single fenced block, the brief-writer's golden, and the checker's `patch.diff`
are **byte-identical**, sha256 `36addc4191950dea…`, with a mutated-copy control that differs.
⚠ `hold_ready.py` **REFUSED** this one (`product hunk '+' lines (6) are not ordered-equal (stripped)
to the brief's expected_plus (32)`) and it was held **by hand**. My own split confirms the shape is
internally consistent: **product +6, test +29, total +35**, matching the checker's
`SUMMARY files=2 +35/-0`. The refusal is the known code_patch-mode assumption, not a patch defect.

## 🔴 MEASURED MYSELF — and it refines the brief's NOT COVERED sentence
The brief says originate's own reads recognise `'anchor_failed'`, not `'failed'`. **That is only half
true, and the ruled literal is better supported than it implies.**
- **Three originate routes DO recognise the bare literal**: `verification.ts:330`,
  `verificationV2.ts:131` and `verificationV2.ts:401` all read
  `blob.status === 'failed' || blob.status === 'anchor_failed'`. So on originate's **verify** paths the
  ruled literal already reads as failed.
- **`documents.ts` does not**: `:1098` and `:1532` serve `anchored: status !== 'anchor_failed'`, and the
  anchor-retry guard at `:1338` refuses unless `status === 'anchor_failed'`. Those three read a bare
  `'failed'` as anchored and not retryable.

So the residual gap is **specifically `documents.ts`'s three `anchor_failed` reads**, not originate as
a whole — and it is **the same as at the tip**, where the blob carried no status at all, so nothing
gets worse. Kam ruled the literal; `'anchor_failed'` is deliberately **not** substituted, and **arm D
pins that choice**. If the difference matters it is a one-line question for him, not a change here.

## Why the cells go in the existing ks543 suite
A **new** test file that sets `ANCHORING_SERVICE_URL` reddens `ks1293-originate-suite-is-hermetic.test.ts`
(the new file is absent from its SUBJECTS list), which would make its manifest a fourth edit point.
`ks543` is already a subject and already carries the harness. (The brief-writer's measurement, relayed.)

## Test Evidence

**Touched:** `services/originate/src/routes/certifications.ts` (+6) ·
`services/originate/src/__tests__/ks543-certify-boundary-strip.test.ts` (+29). **2 files, +35/−0.**

**RAN — all mine, on this worktree at base `0d156d12`:**
| run | result |
|---|---|
| `git apply --check` — whole patch / test section / product section | rc 0 / 0 / 0 |
| originate **baseline** at the untouched tip | **89 suites / 1055 tests, 0 failed** |
| **test section ALONE** at the tip (product file proven unchanged by `git diff --name-only`) | **2 failed / 3 passed / 5** — F4-1 and F4-2 red **by assertion** (`"saved": "failed"` expected, `undefined` received); **control F4-3 GREEN**; 0 Unhandled |
| after the product section | **5 passed / 5** |
| originate **full, after** | **89 suites / 1058 tests, 0 failed** (+3 = exactly the three new cells) |
| `tsc --noEmit` build program | rc 0, **0 errors** |
| `tsc` **including `src/__tests__`** | rc 0, **0 errors**; `--listFilesOnly` census: the ks543 cell (1) and `certifications.ts` (1) are in that program, bogus-name control 0 |
| `eslint src` — **run by hand** | rc 0, **0 errors** / 22 warnings; a planted `no-control-regex` **error** in the touched product file → rc 1 with 1 error, restored by sha256 |

### Four tamper arms. The predictions are the brief's; these are my measurements.
The two tamper targets are **byte-identical lines** (`:474` issue, `:1212` recertify), so they are
selected **by line number** after asserting exactly two whole-line matches — a substring or
first-match anchor would silently hit the wrong route.

| arm | tamper | predicted | **measured** |
|---|---|---|---|
| A | `:474` (issue) emptied | F4-1 only | **RED F4-1 only** (4 passed / 1 failed) |
| B | `:1212` (recertify) emptied | F4-2 only | **RED F4-2 only** (4 / 1) |
| C | `:474` made **unconditional** | F4-3 only | **RED F4-3 only** (4 / 1) — the success leg must stay statusless |
| D | `:474` saves `'anchor_failed'` | F4-1 only | **RED F4-1 only** (4 / 1) — pins Kam's ruled literal |

Restored after each, sha256 equal to pristine; 5/5 green afterwards.

**Push gate, from the raw hook log via `gatelines36`:** 28/0 · 6/0 · 49/0 · shell **60 passed, 0
failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` 0 · **13 code guards** · **VERDICT MATCHES** ·
**PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED** (legs 3, 4, 8 — no local stack). **12/15 is not a
pass.**

**NOT RUN:**
- No live stack and no anchoring service: the cells drive a refused loopback port and an express stub,
  so the **real** anchoring failure path is not exercised. **§5f live sweep owed** — this is a runtime
  change on two write routes.
- The four platform suites: **not run**. `check:openapi`: **not run** — this adds a field to a saved
  blob, not to a response contract, and I am not claiming what the spec says.
- **Production is unaffected** (both routes 503 before the blob exists when `NODE_ENV === 'production'`,
  `certifications.ts:438` / `:1170`). Whether any client-reachable environment runs originate with a
  non-production `NODE_ENV` is **not measured** — the brief-writer's doubt, which I did not close.
- The gateway's own mapping of `status: 'failed'` → off-chain-only is the brief-writer's measurement,
  **relayed, not re-run here**.

**Migrations + config:** none.

Refs KS-1124

