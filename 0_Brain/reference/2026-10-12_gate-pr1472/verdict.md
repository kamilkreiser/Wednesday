# Gate verdict: PR #1472 (KS-1469), Secuura Platform K api-gateway front door

**Verdict: GO WITH NOTE** for head `3929dbe5e9c658ce91db011d95721ff4dfab3846`

- **Gate:** an independent Opus QA gate, run 2026-10-12. It was read-only. I made my own `--no-hardlinks` clone in the scratchpad and fetched develop, `refs/pull/1472/head` and `refs/pull/1472/merge` from GitHub. Nothing was written to the shared repo or to GitHub.
- **Refs (from GitHub):**
  - develop is **f9c7880f91db**. That is still the tip: 00d27598 is its parent, not a newer commit.
  - The branch was merged up to date at 6d66951d1, so a local `merge --no-ff` gives tree `c1cd32ac57f1`. That tree is identical to the head tree and to GitHub's `pull/1472/merge`.
  - The predicted merge is therefore the head tree, and every "head" run below is also the merged run.
- **Seat K's worktree:** I did not find one for KS-1469 on disk. I took every sha from GitHub.

## 1. Is the diff as described?
- Against develop, the PR changes exactly four files:
  - `src/index.ts` (+20/−11)
  - `src/specRouteMap.ts` (one regex line)
  - `src/middleware/csrf.ts` (one strip line)
  - the new test file (272 lines, 31 cells)
- Nothing else changed. The merge commit 6d66951d1 brings in only develop.

## 2. Red first, then green (my runs)
**Tests-first commit and head:**

| Tree | PR test file |
|---|---|
| Tests-first commit 8372637a8 | 18 of 31 red, the same cells the commit names |
| Head | 31 of 31 green |

**Ten tampers of my own.** The seat's commit does not enumerate its ten, so I wrote mine. Each one was checked to have landed and was restored clean. Each reddened its own cells:

| Tamper | Cells red |
|---|---|
| Regex without the `/?` | 5 O1 cells |
| `/*` in place of `/?` | the cell "the regex does not take `abc//`" |
| Regex without the `i` flag | 4 O1 cells |
| Limiter without the v1 mount | 3 O3 cells |
| Two limiter instances | the shared-allowance cell |
| Limiter without the unversioned mount | 2 O3 cells |
| CSRF without the strip | 10 O2 cells |
| CSRF strip repeated | the `/api/v1/v1/auth/login` cell |
| `/api/v2/verification/verify-batch` entry deleted | the m1 cell |
| CSRF strip on the unfolded path | 10 O2 cells |

**The naive O3 fix** (the alias added, the limiter left above the 307) turns exactly **1 of 998** cells red in the full suite: the production cell.

## 3. Suites (head, which is also the merged tree)
- **api-gateway:** 105 files / 998 tests, 0 failed. Base: 104 files / 967 tests.
- **packages/shared:** 49 files / 949 tests, 0 failed.
- **tsc:** api-gateway and shared both rc 0.
- **eslint:** 0 errors. There are 36 warnings, the same count as on base.
- **`check:openapi`:** rc 0.

## 4. Adversarial probes (real app, recording stub)
Evidence: `evidence/probe_head.out` and `evidence/probe_base.out`.

**O1, trailing-slash variants.** All of these are 401 with 0 upstream hits on head, where base gave 200 with 1 hit:
- single, double and triple slash
- slash plus a query string
- `;/`
- upper case with a slash
- the v1 alias with a slash
- `//api/...`

**Methods:**
- DELETE, PATCH and HEAD on `login/` give 405.
- OPTIONS gives 204, from cors, the same as canonical.
- `X-HTTP-Method-Override` is not honoured by the gateway, the same as base.

**Controls:**
- A credentialled request still passes to the later checks.
- A public POST to `login/` still reaches the upstream.
- Paths outside the spec stay 404 with 0 hits.

**Spec:** 310 paths, none ending in `/`.

**Global limiter, measured in a production boot.** The limiter turns out measurable after all: I raised the verification cap out of the way and left the global default alone. 305 POSTs to `/api/v1/verification/verify` gave 300 × 200, then 429 from #301. This confirms K's 300/min claim.

**Limiter key (`trust proxy 1`):**
- The key is the last X-Forwarded-For hop. Rotating that hop bypasses the per-IP limit, identically on base and head.
- Rotating the first hop with the last one fixed does not bypass it.
- This behaviour is unchanged by the PR.

**CSRF breadth:**
- `/api/v1/X` is excluded only when `/api/X` is excluded.
- These stay 403: `loginx`, `/api/v1/v1/`, `/api/v11/`, `%2F` spellings, `/api/v1/health`, `/api/v1/./`, and `/api/v2/v1/`.
- No entry was widened beyond the routes the rewrite actually makes equal.

## Defects
1. **Minor (the O3 fix is incomplete; pre-existing, not a regression). index.ts:515-516.**
   - **The gap:** `/api/v1/v2/verification/*` goes through the rewrite to the v2 verify route but matches none of the three mounts. I measured, with the cap at 3:
     - NODE_ENV=test: 5 × 200, all reaching the upstream.
     - production: 6 × 200.
     - It is counted only by the global limiter, at 300/min.
   - **The inconsistency:** the PR's own CSRF strip treats this spelling as an alias; the limiter does not.
   - **The demonstrating cell:** my cell G1 is red on head, while G2 and G3 are green.
   - **A fix that measures clean:** one limiter instance placed **after** the rewrite, on `['/api/verification','/api/v2/verification']`. It passed all 31 PR cells, including the production 307 cell, and also G1–G3.
2. **Minor/note (a trade-off of the new ordering). index.ts:504-515 with rateLimitSkip.ts:23.**
   - In production, the unversioned `/api/verification*` 307s are now counted by no limiter: 305 out of 305 went through, where base counted them.
   - No request reaches the upstream this way.

## Not changed, and not checked
**Unchanged from base, outside this PR:**
- Dot-segment and extra-segment spellings still reach the upstream without auth, identically to base. These are `/abc/.`, `/abc/./`, `/./abc`, `/abc/..`, `/abc/%2e`, `/abc/%20` and `/abc/%2F`.

**Not checked:**
- Real edge and ingress behaviour.
- Whether originate actually serves `/api/v1/...`. Reading the code, HPM 2.0.10 forwards `originalUrl`, and originate mounts only the unversioned and v2 paths. That is unmeasured.
- Whether express-rate-limit printed validation warnings. Console output appears filtered in these runs.
