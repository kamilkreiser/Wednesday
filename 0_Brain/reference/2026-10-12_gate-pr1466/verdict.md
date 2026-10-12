# Gate verdict: PR #1466 (KS-1461), Secuura Platform K api-gateway

**Verdict: GO WITH NOTE** for head `fd1e6054fa2de121bbd8a9ad7f75ff340ed60a13`

- **What was gated:** head fd1e6054fa2de121bbd8a9ad7f75ff340ed60a13, tree 5ca0bffd805f2721545959b08c5a1b2d00a1d988, parent 41ae15057 (the tests-only commit), base ba697cf3d421. GitHub `ls-remote` showed `refs/pull/1466/head` and the branch both at fd1e6054, and develop at db0df4540acf.
- **Gate:** an independent Opus QA gate, run 2026-10-12. It was read-only. I made my own `--no-hardlinks` clone in the session scratchpad and fetched the PR branch and develop from GitHub into it. The shared repo had no ref writes. The seat's worktree was not found on disk, so I took the shas from GitHub.
- **Predicted merge:** `git merge-tree --write-tree db0df4540acf fd1e6054` gives tree `86d5cde3bf08` with no conflicts. Every run below marked "merged" ran on that tree.

## 1. Is the diff as described?
- The diff touches 8 files, all under `services/api-gateway/`: index.ts, specRouteMap.ts, routes/versioning.ts, middleware/csrf.ts, middleware/security.ts and three test files. No other service and no spec file changed.
- The diff contains everything in the brief. It also contains two things the brief did not name, though the commit message discloses both:
  - the brute-force guard fold (security.ts:152);
  - the CSRF boundary rule (csrf.ts:30-34, :331). This rule narrows the exclusions; it does not just fold them.
- A test cell, "fold B2", was added in the fix commit and not in the tests-first commit. It is a GREEN fact pin, so this is harmless.

## 2. Red first, then green
These are my own runs:

| Tree | Files | Tests | Failed |
|---|---|---|---|
| Tests-only commit 41ae15057 | 101 | 922 | 16, all in the two ks1461 files (16 of 27 new cells, as claimed) |
| Head | 101 | 923 | 0 |
| Base | 99 | 895 | 0 |
| develop tip | 100 | 908 | 0 |
| **Merged** | **102** | **936** | **0** |

**Planted red, one tamper per site, on the merged tree.** I checked that each tamper landed and that the tree was clean after each restore. The cells that turned red:
- P1 version match: 1
- P2a rewrite condition: 1
- P2b rewrite without `/i`: 1
- P2c rewrite anchored with `^`: the 4 KS-1187 absolute-form cells. This reproduces the seat's claim.
- P3 spec-gate prefix: 4
- P4 regex `i` flag: 5
- P5 redirect fold: 2
- P6 redirect replace: 1
- P7 CSRF boundary: 6
- P8a and P8c, dropping the v1 verify-file and verify-batch entries: 1 each
- P9 brute-force fold: 2
- **P8b, dropping `/api/v2/verification/verify-batch`: 0 red, and the full suite stays 936/936.** This is defect m1.

## 3. Static checks on the merged tree
- gateway `tsc --noEmit`: rc 0.
- eslint: 0 errors. There are 36 warnings, the same set the develop tip has, so the PR adds none. The seat reported 3; that difference comes from the local config.
- packages/shared: 48 files, 945 tests, all pass.
- `npm run check:openapi`: rc 0. The spec needs no change.

## 4. Adversarial hunt
I ran a real app over raw sockets with a recording upstream, once on base and once on merged. The full table is in `probe_compare.txt`. The hit counts are upstream hits.

**Case variants, unauthenticated GET:**

| Request | Base | Merged |
|---|---|---|
| `/API/credentials/abc` | 200, 1 hit | 401, 0 hits |
| `/Api/Credentials/ABC` | 200, 1 hit | 401, 0 hits |
| `//API//credentials//abc` | 200, 1 hit | 401, 0 hits |
| absolute-form `http://h/API/credentials/abc` | 200, 1 hit | 401, 0 hits |
| `DELETE /API/auth/login` | 200, 1 hit | 405, 0 hits |

**/api/v1 alias:**
- `/API/V1/...`, `/api/V1/CREDENTIALS/...`, absolute-form `http://h/API/V1/...` and `POST /API/V1/anchors/BATCH` went from 404 with 0 hits to 401 with 0 hits.
- No path that was 404 or 405 before now reaches an upstream: every newly reachable case variant meets the canonical gates.

**Percent-encoding, Kelvin sign and controls:**
- `%63redentials`, `credentials%2Fabc` and the percent-encoded Kelvin sign give 404 with 0 hits on both trees.
- The raw UTF-8 Kelvin sign gives 400 on both trees.
- With the plain `i` flag, the Kelvin sign does not match `k` (control: it does match under `iu`). So the fold and Express routing agree.

**Production 307:**
- The Location header always starts with the literal `/api/v1/`, and the `Host` header and absolute-form host are ignored. There is no open redirect. I checked `//API//evil`, `/API/%2F%2Fevil`, `/API/\evil`, `Host: evil` and `http://evil/API/...`.
- `/api/V2/documents` is no longer bounced to `/api/v1/V2/...`.

**CSRF:**
- None of the 310 spec paths, as sent or under the v1 alias spelling, changes CSRF status. A control confirmed the scan does detect a change.
- The auth service has exactly 4 routes: register, login, refresh and logout. The paths newly protected are loginx, logout-all, refresh-token, login.json, verify-batchX, logsX and healthz. None of them is a real route.
- No entry got broader.

**Spec map:** none of the 310 spec paths changes match when the `i` flag is added. The spec has no case collisions.

**Remaining unfolded comparisons:** only audit.ts, which the PR declares out of scope under KS-1191.

## Defects
- **Major:** none.
- **m1 (Minor), csrf.ts:119:** nothing pins the `/api/v2/verification/verify-batch` entry. You can delete it and every test stays green. No live route exists for verify-batch, in either v1 or v2, so this has no effect today. Either add the missing control cell or drop both verify-batch entries.

## Pre-existing gaps, not caused by this PR (measured the same on base and merged)
- **O1 (worth a ticket):** a trailing slash skips the spec auth gate. An unauthenticated `GET /api/credentials/abc/` gives 200 with 1 upstream hit, in the canonical spelling. The cause is that the spec regex is anchored `^…$`, while Express routing is non-strict.
- **O2:** the CSRF exclusion list does not cover the `/api/v1/` alias spellings. CSRF runs before the rewrite, so a cookie-bearing `POST /api/v1/auth/login` gets 403 CSRF_TOKEN_MISSING. In production the 307 sends `/api/auth/refresh` to `/api/v1/auth/refresh`. I did not measure that in production.
- **O3:** the per-IP verification limiter is mounted only at `/api/verification` and `/api/v2/verification`, so `/api/v1/verification` skips it. This belongs to the KS-946 limiter-spelling work.

## Evidence (scratchpad k1466/)
Run logs, JSON results, `plant.py` and `probe.sh` are in the scratchpad's `k1466/` folder. Three files are copied here: `probe_compare.txt`, `plants_summary.json` and `gate-probe.test.ts`.
