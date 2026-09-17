SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1028 KS-744 @e39521cfb54cb5fd47c6bdae64ce707b3c9befce (TIER 1)
TS: 2026-09-17T10:28:39.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
READY FOR QA: #1028 KS-744 at `e39521cfb54cb5fd47c6bdae64ce707b3c9befce` (tier 1, gateway auth middleware). This is the third open PR of this lineage, beside #1018 and #1026.
- **The fix** (commit `6252f06ac`, built earlier by hand to your KS-744 brief, unchanged): in `authenticateToken`'s verified-JWT branch, `x-user-email` is set only when the claim is present, and `x-verification-level` only when present and otherwise deleted. A signed token missing either claim is proxied (200, one upstream hit), not answered 500 with the internal header error.
- **The develop merge-in is the one your brief flagged.** `e39521cfb` merges develop `19f1e5475`, which brings in #1023 (KS-1207) in the same `middleware/auth.ts`. Git merged it with no conflict, and I checked it by content: the merged file's diff from develop is exactly this branch's hunk, its diff from the branch is exactly KS-1207's 24 lines, and the tree equals the prediction `b61ed1776`. The new tamper row RP-PREMERGE shows the two are behaviourally independent.
- **Red-proof and tampers at the merged head:** 7 / 7 as predicted, 0 VOID, whole api-gateway suite 57 files / 555 tests on every row. api-gateway is 57 / 555 green, including ks1207 26 / 26; tsc rc 0.
- Push PROTOCOL-CLEAN (first push). Preflight ran 12/15 legs, 3 SKIPPED (no stack), nothing failed. 4 stubs ended by pid, 0 remain. linkKinds: KS-744 `contributes`.

## Recommendation
1. **Gate the head `e39521cfb`** (tier 1). **KS-1208** (the `role` / `userId` residue, 401 shape) is named in the PR and not widened into.
2. **No KS-744 comment names #1028** (the ticket has 0 comments). Default, as you ruled for KS-839 and KS-1050: one BLUF facts comment after the verdict.
3. **KS-744 walked Backlog → In Progress at 10:27:34Z** with no actor, i.e. the GitHub branch automation on PR creation. That is expected. I left it; it does not go to Done at merge (§5f).
4. **Next:** the 3-PR cap is full (#1018, #1026, #1028), so KS-1180-P1 and KS-1194 wait for a merge. In the wait I start **KS-1213 locally**: measure `/version`, `sign-cert`, `sign-wallet` and `certifications/issue` first, and build the write-side refuse only on the writers that relabel.

## Detail

### Head and push
- Branch `feature/ks-744-gateway-500s-on-every-proxied-route-for-a-token-lacking`, first push. Commits over develop:
  - `6252f06ac`: the fix (`auth.ts` +3 −2, new test +93);
  - `fb503741a`: merge of develop `81ee4b729` (earlier seat);
  - `e39521cfb`: merge of develop `19f1e5475` (parents `fb503741a`, `19f1e5475`).
- Push 10:19:08Z → 10:26:52Z, rc 0. push_protocol verify: PROTOCOL-CLEAN, first push, one tracking ref added at origin's head, config / worktrees / 113 heads identical.
- **Origin** (ls-remote in the send action below): `refs/heads/<branch>` = `refs/pull/1028/head` = `e39521cfb54cb5fd47c6bdae64ce707b3c9befce`.
- PR created by REST 201: #1028, base develop `19f1e5475`; title and body read back byte-equal.
- Before creating it: #1018 open @ `efd677e98`, #1026 open @ `df97c0def`, 0 existing PRs for the branch.
- In-hook preflight: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 skipped (no stack), so not a pass of those. Leg 1 `spec is in sync`; leg 5 59 / 59; shell suites 35 / 35.

### Merge by content (`middleware/auth.ts`)
- Branch change (`81ee4b729..fb503741a`): `@@ -386,12 +386,13 @@`, the two guarded headers.
- Develop's change (`81ee4b729..19f1e5475`): `@@ -274,16 +274,20 @@`, KS-1207's API-key block. Its `+`/`-` lines are exactly `fb503741a..merged`, and the branch's lines are exactly `19f1e5475..merged`.
- **Semantic check on the two identity headers:**
  - `x-user-email` matches the edge strip `TRUST_HEADER_PATTERN` (`^x-(user|…)(-|$)`, `utils/trustHeaders.ts`), so a client value never reaches this code, and the conditional set is safe.
  - `x-verification-level` does NOT match, hence the `else delete`. The NOELSE tamper row shows a client-sent `enhanced` reaching the recording upstream without it.
  - READ, not measured: 0 non-test readers of `x-verification-level` anywhere under `services/` and `packages/` other than the gateway's three setters (case-insensitive git grep at `19f1e5475`; the literal matched those 3 setters, so the instrument can match). So a client value on a path that never sets the header (for example an anonymous request on an optional mount) has no consumer today. I searched `x-verification-level` (KS-744, KS-742), `verification-level` (KS-744, KS-1176) and `TRUST_HEADER_PATTERN` (KS-741, KS-492, KS-1041): none records it. With no consumer I am **not** recommending a ticket, only noting it.

### Red-proof and tamper table
Runner `5_Project_History/2026-09-17_seatA-6th/ks744/tamper.py`, output `tamper/tamper.json`, 20:17:16 → 20:18:10 AEST. Each row:
- anchor 1 or a blob swap;
- `tsc --noEmit -p .` (non-zero = VOID);
- the WHOLE api-gateway suite, denominator asserted = T0's (57 / 555 / pending 0);
- restore by bytes against the HEAD blob plus `git diff --quiet HEAD`.

Every ks744 red is an `AssertionError`.

| Row | Form | ks744 reds | Other reds |
|---|---|---|---|
| T0 | none | 0 | 0 |
| RP-DEV | `auth.ts` = `19f1e5475` bytes | R1, R2, R3 `expected [ 500, +0, null ] to deeply equal [ 200, 1, null ]` | 0 |
| RP-PREMERGE | `auth.ts` = `fb503741a` bytes (the fix without KS-1207) | 0 | 10, all ks1207's 🔴 cells (`expected [ 200, null, …(1) ] to deeply equal [ 401, 'SESSION_INVALIDATED', [] ]` ×5; `expected [ null ] to deeply equal [ 'u-ks1207' ]` ×5) |
| EDIT1ONLY | the `verificationLevel` guard reverted | R2, R3 | 0 |
| EDIT2ONLY | the `email` guard reverted | R1 | 0 |
| NOELSE | the `else delete` removed | R3 `expected [ 200, 1, 'enhanced' ] to deeply equal [ 200, 1, null ]` | 0 |
| TI | inert comment | 0 | 0 |

**Instrument slip, caught before any write:** the first run's sha guard refused row 2, because I had derived the runner from the KS-839 one and its `committed()` and blob-swap paths still read `services/auth`. The guard fired before any file was written: porcelain 0, HEAD unchanged. Kept as `tamper.run1-guard-refused-services-auth-path`. After the path fix, the re-run above.

### Suites, tsc, eslint (ratios)
- api-gateway 57 files / 555 tests, 0 failed, 0 pending (develop after #1023: 56 / 550, per the 5th successor's #1023 record). ks744 5 / 5, ks1207 26 / 26.
- `tsc --noEmit -p services/api-gateway` rc 0.
- Test-including program (scratch tsconfig extending the gateway's, `exclude: []`, ks744 in the program by `--listFilesOnly`): rc 2, 50 error lines, all pre-existing; 0 in the ks744 test, 0 in `auth.ts`.
- eslint: ks744 test 0. `auth.ts` has 1 warning, `'error' is defined but never used` at `:415`, the same warning develop's `auth.ts` carries at `:414` (fed on stdin: pre-existing, shifted by this hunk's +1).
- `packages/shared` not re-run: the PR touches only 2 api-gateway files, so the subtree is develop's.

### PR body
- **Title:** `KS-744: a verified token missing its email or verificationLevel claim is proxied, not answered 500`.
- **Body:** `Linear:` URL, BLUF, Recommendation (KS-1208 residue), the change with the merge-by-content record, cells, tamper table, Test Evidence, platform suites, PII, footer.
- `Refs KS-744`, closing phrases 0, at-signs 0.

### NOT done / NOT covered
- a real upstream service or the edge (nginx / Caddy);
- Schemathesis / Akto / Playwright / k6 (no stack);
- the test-including program's count and eslint at develop, beyond the one `auth.ts` stdin read.

