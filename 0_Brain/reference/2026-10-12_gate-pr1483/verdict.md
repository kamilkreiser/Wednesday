# Gate verdict: PR #1483 (KS-1479), Secuura Platform K api-gateway verification limiter

**Verdict: GO WITH NOTE** for head `efb9b5d83fe5e5542911f43bf68b23e451962722`
(No Major. No Minor defect in the PR. The notes are test-gap and pre-existing items, not regressions.)

- **Gate:** independent Opus QA gate, 2026-10-12, read-only. My own `--no-hardlinks` clone in the scratchpad; refs fetched from GitHub. Nothing written to the shared repo, GitHub, the board or any deploy.
- **Refs:** PR head efb9b5d83 = branch tip (GitHub). Tests-first 95b75d533. Base named by the seat 5bfa5a804f63.
- **develop MOVED during the gate:** at 19:26 it was `a28ed5d81d1d` (+2 commits: KS-1000 auth tsconfig; KS-1457 `middleware/audit.ts` auditPath). GitHub's `pull/1483/merge` was still built on 5bfa5a80. I built the predicted merge myself: `merge --no-ff` clean, tree `63be8590d463`. All suites below were re-run on it.
- **Seat K's worktree:** none for KS-1479 on disk under `worktrees/`; everything taken from GitHub shas.

## 1. Diff
- 5bfa5a80..efb9b5d83 touches exactly `services/api-gateway/src/index.ts` (+24/-22) and the new test `src/__tests__/ks1479-v1-v2-verification-spelling-is-counted.test.ts` (129 lines).
- The fix commit touches index.ts only.
- The block moves from after `versioningMiddleware()` (old index.ts:506-524) to after the `/api/v1/` rewrite (head index.ts:544-564). The mounts go from 3 to 2 (`/api/verification`, `/api/v2/verification`), on one instance. The comment at index.ts:494-495 is updated.
- **Between the old and new positions there are only two middlewares:** the version check (400 for unsupported versions, index.ts:511-534) and the rewrite (536-541). Body parsing, CSRF, the JSON guard, sanitisers and the global limiter all sit above both positions. Audit (570) and the handlers sit below both. Nothing else was re-ordered.

## 2. Tests first, then green (my runs)
| Tree | KS-1479 file (7 cells) | KS-1469 file (31 cells) |
|---|---|---|
| tests-first 95b75d533 | 3 red: A1, A2, B1 | 31 green |
| head | 7 green | 31 green, production cell included |
| predicted merge (on a28ed5d8) | 7 green | 31 green |

## 3. Tampers (each landed, then restored; run against both files)
**The seat's four, reproduced exactly:**

| Tamper | Seat claim | Mine |
|---|---|---|
| T9: 3 mounts back above the rewrite (= develop) | 3 red | 3 red (A1, A2, B1) |
| T2: only the unversioned mount | 4 red | 4 red |
| T11: naive, 3 mounts above the 307 | 5 red, incl. KS-1469's production cell | 5 red, incl. KS-1469's production cell |
| T4: one instance per path | 1 red | 1 red (A2) |

**Mine:**

| Tamper | Cells red |
|---|---|
| 2 mounts in KS-1469's slot | 7 |
| 2 mounts above the 307 | 7 |
| only the v2 mount | 7 |
| limiter removed | 10 |
| `/api/v1/v2/verification` mount added above the 307 | 2 (double count) |
| the v1 mount re-added after the rewrite | 1 (A3) |
| limiter moved below the audit middleware | **0** (see N1) |

The A3 result matters: re-adding the v1 mount after the rewrite counts `/api/v1/v1/...` 404s. So dropping that mount is not just redundant, it is the correct choice.

## 4. Suites
| Tree | gateway | shared | tsc (gw / shared) | eslint | check:openapi |
|---|---|---|---|---|---|
| head | 107 files / 1017 tests, 0 failed | 49 / 949 | 0 / 0 | 0 errors, 36 warnings | rc 0 |
| merged (a28ed5d8 + PR) | 108 files / 1026 tests, 0 failed | 49 / 949 | 0 / 0 | 0 errors, 36 warnings | rc 0 |
| base 5bfa5a80 | 106 / 1010 | 49 / 949 | 0 / 0 | 0 errors, 36 warnings (identical set) | rc 0 |

- **Touched files:** index.ts has 2 warnings, both pre-existing (lines 117 and 919). The new test file has none.
- **Counts reconcile:** +7 tests from the PR, +9 from KS-1457.

## 5. Adversarial probes (real app, recording stub)
Probes were run on head, on develop's index.ts and on the merge; merge = head exactly. Each spelling got 6 POSTs on a fresh boot at cap 3 (`evidence/probe_*.jsonl`).

**These 25 spellings are bounded on head (200x3 then 429, 3 upstream hits), test and production:**
- `/api/v1/v2/...`
- every case mix
- trailing `/` and `//`
- `?q`
- repeated slashes anywhere, including a leading `//`
- `verify-batch` and `verify-file`
- `/./` and `/../` inside the tail
- the bare `/api/v1/v2/verification`
- absolute-form `http://h/API/V1/v2/...`
- `#frag`

**Control:** on develop the same spellings reach the upstream 6 of 6.

**Zero bypass:** no spelling reaches the upstream more than 3 times on head. The spellings that do not count all reach no handler (0 upstream hits, identical on develop):
- `%2F`, `%76`, `;/`
- `/./` before `verification`
- `/api/v1/v1`, `/api/v2/v1`, `/api/v2/v2`
- backslash
- `/api/v9` (400 in test)

**The seat's /api/v9 question:** it is not new. The old mounts never matched `/api/v9/...` either. It gets 400 (test) or a 307 to `/api/v1/v9/...` (production) on both trees, with 0 upstream hits. Cell A4 pins it, and A4 is green on develop.

**Nothing counted before is uncounted now.**
- Every old-mount match (pre-rewrite `/api/{,v1/,v2/}verification`) maps to a new-mount match after the rewrite.
- The 400 branch only fires for versions other than v1 and v2, which no old mount matched.

**Production allowance, real default (no override):**

| Request | head | develop |
|---|---|---|
| direct v1 | 60 x 200, 429 from #61 | 60 x 200, 429 from #61 |
| direct v2 | 60 x 200, 429 from #61 | 60 x 200, 429 from #61 |
| `/api/v1/v2` | 60 x 200, 429 from #61 | 65 of 65 through |
| 65 followed 307s | 65 x 307 + 60 ok, 429 at call 61: counted once | the same |

**Global limiter (production, verification cap raised):** v1/v2 and v2 both give 300 then 429 from #301, identical on both trees. The skip list is unchanged.

**XFF (trust proxy 1):**
- The key is still the last hop.
- One shared bucket across spellings: v1/v2 x3, then v2 with a different first hop → 429.
- Rotating the last hop bypasses the limit, as on develop.

## Notes (no defect blocks)
- **N1, Minor test gap.** No cell pins the limiter **above** the audit middleware. Moving it below `createAuditMiddleware` (head index.ts:570) turns 0 cells red, and would start auditing 429s. That is a harmless position today, but it is unguarded.
- **N2, pre-existing, carried over from the KS-1469 trade-off.** Unversioned production 307s are counted by no limiter. They reach no handler. B2 pins this.
- **N3, pre-existing.** Rotating the last XFF hop evades every per-IP limiter (trust proxy 1). Edge config is not checked here.
- **N4, pre-existing.** `/api/v1/v2/verification/../verification/verify` is forwarded upstream with the literal `..`. It is now counted. Upstream normalisation is unchecked.

**Not checked:**
- Real edge or ingress behaviour.
- Redis-backed limiter stores (the app uses the in-memory default in these boots).
- Multi-replica counting.
