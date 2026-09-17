=====MSG 2026-09-17T01:45:54.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
MERGED #1017 KS-1195 as `d7e95cd9f153e9036ed77935a73c93504fa6e3dc`, verified at origin against every GO target. KS-1195 stays In Progress (§5f). The facts comment and all three tickets are filed: (i) KS-1205, (ii) KS-1206, (iii) KS-1207. **KS-1207 is High, and heavier than the gate's R-4 reading.** Measured in-process: a revoked-session JWT plus any junk `sk_` header skips the gateway's session-revocation check on five optional-auth mounts, and the shared `authenticate()` the upstreams mount accepts it. I build #1019 round 2 next.

## Recommendation
1. **KS-1207 is an escalation candidate for Kam.** Only the gateway and originate check session revocation, so on credentials, referrals, governance, nft and billing, logout, the session cap and a suspension do not stop a token whose holder adds any `x-api-key: sk_…` header, until expiry (1h default). This was measured in-process only, not on demo. I have not built it and will not start it without your word; it is outside this brief.
2. No other action needed. #1019 round 2 starts now; READY follows.

## Detail

### The merge
- `gh pr merge 1017 --squash --match-head-commit a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66` at 01:33:51Z; subject "KS-1195: the per-key rate limiter runs after authentication, so a key's ceiling is enforced (#1017)", author kksecura, body ends `Refs KS-1195` + Co-Authored-By.
- **Pre-step:** linkKind KS-1195 `contributes` (In Progress). Closing phrases: 0 in title, body, 1 comment, 3 commits and my squash body (regex control 2). No leading STOP/HOLD mail since your ANSWER (control: `HOLD:` matches, "holds" does not).
- **At origin (01:33:5xZ):** develop tip (ls-remote) = M; parents of M = `fa887f382b212b8da4a0a4a556bacb05ea34daaa` only; tree `35974a2ffce620fe37c956daf5fde1a2e4e7a738` = the prediction; files base..M = the PR's 5.
- **The five blob equalities:** `auth.ts` `7c985bdce` · `rateLimitEnforce.ts` `90bd29378` · `index.ts` `db127dbfa` · ks1195 test `4b1fc017d` · ks781 test `bc4815c4e`. All equal the GO targets and the gated head.
- **After:** `attachmentsForURL(pull/1017)` = [KS-1195 contributes, In Progress]. KS-1195 In Progress, 3 comments.

### (a) KS-1195 facts comment
`21522e2b-998f-4ab7-a499-665ddd945d2a` (01:35:31Z), anchors 8/8. It carries: the §5f line (`Merged d7e95cd9f…; offline gates green; NOT Done per secuura-test-discipline §5f — live sweep owed …`); the deploy precondition (measure real keys' allowances and real connector traffic first, both UNMEASURED); F-1 CLOSED with the gate's re-run numbers; F-2 CLOSED; Rec-A, Rec-B, Rec-D; KS-164's per-key wording as the product note. One Linear 503 on the first attempt; I re-read the ticket (still 2 comments) before re-posting, so there is no duplicate.

### (b) KS-1205, the limiter follow-up
Medium, Backlog, related KS-1195 / KS-1156 / KS-1198, not linked to #1017, anchors 8/8. Covers N-2 (with the gate's fix shape: a request-level tag, not a `req.user` field, plus a namespaced fallback), the fallback literal, F-5 (+61 s validate 1; +481 s validate + exchange; audit row per refusal), F-4, F-3 + N-1 (G-OAUTH / G-UNKOPT / G-JWTCATCH / G-BUCKET-HASH / G-BUCKET-RAW-2, with the N-1 cell to add) and R-2. Search: `rateLimitBucket` 2/1, `enforceClientRateLimit` 6/6, `has no rateLimit` 124/1, `per-key rate limit` 107/5, `rateLimitEnforce` 9/9, `limiter` 96/50. KS-1156 is related, not duplicated: it records the machine set never meeting the `oauth` label; F-3 is that no cell pins the exemption.

### (c) KS-1206, R-1 originate
Low, Backlog, related KS-1195 / KS-869, anchors 5/5. `adminConfig.ts:946` writes `d.rateLimit || 1000` unclamped with window 3600 and no `connector_id`; the security service clamps at `index.ts:569-570`. The gate's a4 rows are on it (-1 → 429 forever; `'abc'` → never limited). The ticket says only -1 is shown storable by READ. Low because the input needs an admin, and after #1017 a connector-less key no longer shares a bucket. Search: `rateLimit || 1000` 64/0, `adminConfig` 33/33, `rate_limit` 92/27, `connector_id` 101/14 (KS-869 / KS-908 / KS-889 are the security service's own create path; none names originate, checked by text), `api-keys` 86/11.

### (d) KS-1207, R-4 security, measured before the priority
High, Backlog, related KS-1195 / KS-736 / KS-588, anchors 7/7.
- **Mechanism (READ at `d7e95cd9f`):**
  - The spec auth gate `index.ts:1073-1074` admits on the presence of an `sk_…` header.
  - `authenticateToken(false)` runs the API-key block first and, on a failed validation, calls `next()` without ever reaching the Bearer block, where `isSessionActive` runs (`auth.ts:376`).
  - Every non-test `isSessionActive(` caller: api-gateway `auth.ts:376` and originate `auth.ts:105` only (control: both hits present). vc-issuer, referral, governance, nft-certificate and billing use shared `authenticate()`, which checks the signature only.
- **Measurement (01:41Z, in-process):**
  - **Substrate:** the real assembled gateway app in my worktree at `a067d4e3e`, whose `auth.ts` / `index.ts` / `proxy.ts` / `admin.ts` / `config/services.ts` / shared `middleware/index.ts` blobs equal `d7e95cd9f` (the only tree difference is #1014's three files). Upstreams went to one stub; the session store was stubbed (`r4-revoked` revoked, `r4-active` live); forwarded requests were replayed against the real shared `authenticate()` on a bare app. 84 rows = 12 paths × 7 credentials.
  - **Result on 7 paths** (credentials GET / GET :id / POST :id/revoke, referrals GET :code / POST apply, governance GET, nft GET): revoked JWT alone → 401 `SESSION_INVALIDATED`, session check ran (7/7). Revoked JWT + unknown key → 200 forwarded, 0 session checks, the revoked JWT forwarded as sent, upstream 200 with principal session `r4-revoked` (7/7). Unknown key alone → forwarded, upstream 401 (7/7). Bad-signature JWT + unknown key → forwarded, upstream 401 (7/7).
  - **Billing:** gateway rows the same; upstream replay not applicable (`/billing` mount), so upstream acceptance there is READ.
  - **Controls:** required `/api/documents` → 401 for both; `/api/certifications` → 401 (its `requireScope`).
- **Not measured:** running services, the edge, demo.
- **Instrument notes:** my first `git grep` for callers used a `services/*/src` pathspec and read 0. The control (the gateway's own caller) exposed it; re-run with a plain path. The probe file was run once and moved to `5_Project_History/2026-09-17_seatA-4th/tickets/r4/` (worktree porcelain 0).
- **Search:** `SESSION_INVALIDATED` 109/8, `isSessionActive` 7/7, `authenticateToken(false)` 80/8, `optional auth` 94/1, `session revocation` 106/11, `unknown sk_` 104/0. Nearest: KS-736 (the mount-auth guard scoring `(false)` green on the same six mounts; no key or revocation angle), KS-570 / KS-257 (archived, same class elsewhere; named in the text, relations refused on archived), KS-588.

### Next
#1019 round 2: switch my worktree to `feature/ks-1187-…` @ `8b8996f8b` (porcelain 0 first), re-read develop and confirm the three #1019 files are byte-identical between `fa887f382` and `d7e95cd9f`, then build to the NO GO items 1-4. Login stubs: 0 now; none are expected, since I run no push until the READY push.
