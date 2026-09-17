SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1023 KS-1207 @2f74491ebd6211e722f778838339c55e8add008d (TIER 1)
TS: 2026-09-17T08:02:01.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
READY FOR QA: **#1023 KS-1207 @ `2f74491ebd6211e722f778838339c55e8add008d`** (tier 1), shape (B) as ratified 02:06:01Z. The fix commit is `0f8b699b4`; develop was merged in twice (`f8c7aaa39`, then `581c9db0d` after #1019), with no file overlap. Kam's ruling `build-after-1019` is on the ticket (comment `1c90d0fc`) and in the PR body; #1019 merged at 07:52:46Z. A key that fails validation on an optional-auth mount now falls through to the Bearer path instead of `next()`. So a revoked-session JWT plus a junk `sk_` header is refused 401 `SESSION_INVALIDATED` on all five mounts, and a live JWT plus a junk key is forwarded with the JWT's principal. With no Bearer the request stays anonymous, as before. Red-proof at develop: 10/26 red, as predicted. Tamper table: 6 rows, all as predicted.

## Recommendation
Gate this head (tier 1). Merge on your GO; KS-1207 stays In Progress on merge (§5f). The residual is KS-736's and is not widened into here: a junk key ALONE is still forwarded without a principal on a bearerAuth operation, because the spec gate at `index.ts:1073-1074` counts the header's presence; the upstreams refuse it 401 (measured on KS-1207).

## Detail

### Head
- PR https://github.com/Secuura/Distributed_Secuura/pull/1023, base develop `581c9db0d`. Branch `feature/ks-1207-security-an-unknown-sk_-key-on-an-optional-auth-mount-skips` (Linear's branchName, one id, its own). Commits: fix `0f8b699b4` (parent `d7e95cd9f`); merge `9bd0fd333` (develop `f8c7aaa39`, tree = prediction); merge `2f74491eb` (develop `581c9db0d`, tree `4bdf1b8c7ea3a679e6b20a21c5970d375ba8776f` = prediction). PR files vs develop: exactly the two below, byte-identical to the fix commit.
- Files: `services/api-gateway/src/middleware/auth.ts` (+14 −10) and the new test (+185). #1019's three files come from develop byte-identical; no overlap.

### The change (`authenticateToken`)
`presentedKey` = an `x-api-key` starting `sk_`; `meta` = its validation (or null). A presented key that fails validation on a REQUIRED mount → 401 `Invalid API key`, unchanged. On an optional mount → no return: the Bearer path runs, and with no Bearer it calls `next()` anonymously, as before. A valid key → the connector branch, byte-identical to before (same indentation; only its `if` changed from `apiKey && apiKey.startsWith('sk_')` to `apiKey && meta`).

### Cells (26, real app: index.ts default, `../db` mocked, session store stubbed, one recording upstream that also answers validate and the connector-token exchange)
Per mount — credentials `/api/credentials/:id`, referrals `/api/referrals/:code`, governance `/api/governance/proposals`, nft `/api/nft/tiers`, billing `/api/billing/config`:
- 🔴 revoked-session JWT + junk key → `[401, SESSION_INVALIDATED, []]`, and the session check ran for `ks1207-revoked`;
- 🔴 live JWT + junk key → 200, forwarded with `x-user-id` = the JWT's user;
- control: revoked JWT alone → `[401, SESSION_INVALIDATED, []]` (the stub is live);
- control: a real key → 200, forwarded with `connector:ks1207-conn`;
- 🟢 control: a junk key, no Bearer → 200, forwarded with no `x-user-id` (anonymous, as before).
Plus: on REQUIRED `/api/documents`, live JWT + junk key → `[401, UNAUTHORIZED, []]`.

### Red-proof at develop `auth.ts` (blob `7c985bdce`; prediction written first: 10 red / 16 green)
26 run: **16 green, 10 red, every red an `AssertionError`**, as predicted. The revoked+junk cells read `[200, null, one hit]` at develop, which is the bypass reproduced. The live+junk cells read `[null]`, meaning no principal was forwarded. Restored sha256-equal.

### Tamper table (at `0f8b699b4`; each row: anchor 1, `tsc --noEmit -p .`, WHOLE api-gateway suite 55 files / 480, pending 0, restore by bytes + sha256 + `git diff --quiet HEAD`; every red an AssertionError)
| Row | Tamper (`middleware/auth.ts`) | Reds (pred) | tsc |
|---|---|---|---|
| T0 | none | 0 (0) | 0 |
| TBYPASS | the old immediate `next()` on an optional failed key | 10 (10): 5 revoked+junk, 5 live+junk | 0 |
| TSKIPSESSION | the session check skipped whenever a key header is present | 5 (5): the revoked+junk cells | 0 |
| TNOBEARER | a failed key with no Bearer refused 401 (shape A's behaviour) | 5 (5): the 🟢 anonymous controls | 0 |
| TREQ | a required mount no longer refuses a failed key | 1 (1): the required-mount control (ks480's and ks1195's invalid-key cells stay 401 through the Bearer path, as predicted) | 0 |
| TI | inert comment | 0 (0) | 0 |

### Suites
- **At the head `2f74491eb`:** api-gateway **56 files / 550, 0 failed, 0 pending** (develop `581c9db0d` 524 + 26); packages/shared **44 / 851, 0 failed**; `tsc --noEmit -p .` rc 0. Porcelain 0.
- **At `9bd0fd333`:** 55 / 480, 44 / 851, tsc 0.
- **At the fix commit `0f8b699b4` (predecessor):** api-gateway 55 / 480, shared 44 / 851, tsc 0. Test-including program (`exclude: []`): 591 files, ks1207 in the program, 31 error lines / 11 files, 0 in either touched file. eslint: `auth.ts` 1 `no-unused-vars` (`'error'`), identical at develop; the new test 0.

### Push and post-push
- 07:54:54Z → 08:00:49Z, rc 0; first push; push protocol **CLEAN** (tracking ref added at origin's head); ls-remote = head. Guards: branch absent on origin, origin develop = `581c9db0d`, HEAD = `2f74491eb`, porcelain 0, `8a6b0d9c2` an ancestor.
- In-hook preflight: **12/15 legs ran, 3 SKIPPED (3, 4, 8: no local stack), nothing failed** — not a full pass. Legs 1, 2, 5 (59 / 59), 6 and 7 OK.
- 4 login stubs stopped by verified pid (CONTROL: ps rows parsed 1090; 0 alive; non-node controls 17 before and after).
- `attachmentsForURL(pull/1023)` = [KS-1207 **contributes**]; control pull/99999 = []. KS-1207 walked Backlog → In Progress at 08:01:36Z (botActor GitHub, same second as the attachment). Left.
- Closing-phrase scan of the title and body: 0. The body names only KS-1207 (the residual is described without its id).

### NOT run
The edge, running upstream services, demo; Schemathesis / Akto / Playwright / k6 (no stack); preflight legs 3/4/8. Not re-run at the merge commits: the red-proof, the tamper table, the test-including program and eslint (this PR's files are unchanged by the merges).

### Open PRs of this lineage
#1018, #1023 = 2.
