# QA Gate 98 verdict: Secuura/Distributed_Secuura PR 1916 (KS-1868, api-gateway routes/admin.ts, three identity-admin catches, O58-P1 from the -r2 run), TIER 2

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.** Tier 2 stands; I would not raise it. The change is log-only. I ran the real admin router (real `createAdminRoutes`, real `requireAdmin`, ADMIN_ROLES, `mockBodyParser`) on a real loopback express listener with only `verifyToken` (auth context), `query` (DB), `log` and redis replaced. At base an unreadable thrown value (revoked Proxy, or Error with a throwing `message` getter) gives **NO RESPONSE** (request hangs until my 1.5 s abort; 1 unhandled rejection; no log line) on all three routes. At head the same values give the **constant 500**, byte-identical to the body an ordinary Error gets, plus a log `{"error":"unreadable thrown value"}`. Ordinary Error and thrown string: byte-identical at base and head (status, body, queries, log). Authorisation untouched. The product file equals the -r2 held section (Q3 EQUAL, file level).
Numbers: diffstat 4 files +231/-3 as claimed; red-first 7 of 14 by assertion, green 14/14; api-gateway suite 134 files/1373 -> 135/1387; leg-16 27 errors, 27 in baseline, 0 new, before and after; eslint 0 errors/16 warnings, the same 16 as base; fragments clean and planted defects caught; mutants 24 of 24 killed; merge-tree onto develop `bd8785796118` clean, 4 paths, 0 shared.

## Heads
- START (logs/head_start.log, 2026-11-01T23:46Z, ls-remote): PR head `3840443b9a82eecc385348458f22337a45d596d0` (expected), develop `bd8785796118a20b0220924523a543baf7f73340`. Merge-base `03977e89a343`. One commit.
- END (logs/head_end.log, 23:57:43Z): both unchanged. Product sha256 restored to head `a550d518e2c9...` after every swap (checked; `git status` clean).
- Diffstat (logs/diffstat.log): 4 files +231/-3: admin.ts +21/-3, test +167, two fragments +22 / +21. Nothing outside the declared paths. Develop changed 28 files since the base; 0 are the PR's four paths (admin.ts blob on develop = base blob `ed2c2c41c0cc`).
- PR body not read (no gh login reachable); I used the author's READY, CLARIFICATION and BUILT AND PROVEN mails (evidence/). Wording in the body I could not see is not verified. Direct clone worked (no hook refusal); `git fetch`/`merge-tree` worked only with literal paths, not via `$R`.

## FINDINGS
- **G98-F1 (INFO, measured)** At base the unreadable value gave no response: the async handler rejects, Express 4 never answers, the client hangs; 1 unhandled rejection per request, no log. Head fixes all three; unhandled = 0 at head in every cell.
- **G98-F2 (INFO, ks1346, pre-existing, unchanged by this PR)** The three log lines still log `err.message` / `String(err)` as a VALUE (committed cell C1 pins `db boom 10.0.0.7` in the log). The PR adds only the constant `unreadable thrown value`; it adds no value to any log, but readable errors still do not meet "type and field names, never values". Belongs to card secuura-ks1346.
- **G98-F3 (INFO, follow-up sites, read from source, not run)** Other unguarded reads of a thrown value remain in admin.ts: `(err as Error).message` at :1238, :1455, :1475, :1514, :1608 and `err.message` at :1018, :1501. A revoked Proxy (or null/undefined) hits them. Same class, outside this PR's scope. Candidates for the next KS-1868 pass.
- **G98-F4 (INFO, author's candidate, not measured against a DB)** PATCH level is behind `requireAdmin`, whose ADMIN_ROLES include ORG_ADMIN and ISSUER_ADMIN; `adminScope` widens only platform roles. The probe confirms ORG_ADMIN and ISSUER_ADMIN reach the handler and issue the UPDATE for any id (stub DB). Whether RLS bounds them to their tenant is not run here. Pre-existing, unchanged. A card for Kam (possible privilege issue), not a merge block.
- **G98-F5 (LOW, test gap)** The committed cells bypass `requireAdmin` and call the last stack handler; they pin the handler, not the 401/403 gate or the hang. My probe covers those (scripts/probe.test.ts) but is uncommitted. Optional.
- **G98-F6 (INFO)** The PR's `git diff -U3` differs from section_1.diff only in hunk headers and the amount of context; applying section_1.diff with `patch` to base gives a file with the same sha256 as the PR head's.

## Q1. Real router, base vs head (logs/probe_table.log, probe_base.jsonl, probe_head.jsonl; scripts/probe.test.ts, probe.sh)
Real express listener, real fetch over loopback, bearer = role name, `verifyToken` returns `{role}`; DB `query` rejects with the chosen value. Positive controls: ok case 200, AUTH matrix. 31 cells per version, vitest rc 0 both.
| route | thrown | base | head |
|---|---|---|---|
| all 3 | ok | 200 | 200 |
| all 3 | Error('db boom 10.0.0.7') | 500 constant body; log `db boom 10.0.0.7` | identical |
| all 3 | string | 500; log `plain` | identical |
| all 3 | revoked Proxy | **NO_RESPONSE**, 1 unhandled, no log | **500**, body byte-equal to the Error body (3/3 routes), log `unreadable thrown value`, 0 unhandled |
| all 3 | Error with throwing `message` getter | as revoked Proxy | as revoked Proxy |
Queries issued identical to the Error case at both versions in every cell (1 each). The unreadable-value after-state equals what an ordinary Error gets. Run: real routes, middleware, express. Replaced: token verifier, DB, logger, redis.

## Q2. Authorisation and the single UPDATE
- `requireAdmin` / ADMIN_ROLES lines identical base vs head; the only product changes are the 3 hunks (-U0: 3 removed log lines, 3 guards).
- Probe auth matrix, base = head on every route: no token 401, USER 403, ORG_ADMIN / ISSUER_ADMIN / SYSTEM_ADMIN 200 with 1 query. Bad level 400 with 0 queries, unchanged.
- PATCH level: one query only, `UPDATE users SET verification_level = $1`, params `['HIGH', id]` for ok, Error and revoked Proxy, at base and head. The catch writes nothing.

## Q3. Held section equality
`patch -p1` of the -r2 `out.md.checker/section_1.diff` onto base admin.ts applies clean and gives sha256 `a550d518e2c9733e11e5f75c4af05fbb73bee244ef86d5156ded66a9c2194b4a`, equal to the PR head's admin.ts (cmp): **EQUAL** (file level; raw hunk text differs only in context, G98-F6). Operator 58's report claims (3 sites, +21/-3, tier 2, strict apply, red 7/14, green 14/14, suite 1373->1387) re-measure equal.

## Q4. ks1346
New log content is only the constant `unreadable thrown value`. Message text, level and keys unchanged. No thrown-object value is newly logged. See G98-F2 for pre-existing value logging.

## Re-measure
- Head, new file: 14/14. Base product + new file: **7 failed, 7 passed**, all AssertionError (expected 200 to be 500 x6; R3 expected undefined to equal the constant), no import error. The 7 controls pass at base.
- Suite: base (new file excluded) 134 files 1373/1373; head 135 files 1387/1387. vitest --maxWorkers=2.
- tsc tests (`tsconfig.test.json`): 27 errors base, 27 head; leg-16: "27 errors: 27 in the baseline, 0 new, 0 stale" (170 -> 171 files). Planted unused const: 28. eslint admin.ts + test: 0 errors/16 warnings; base admin.ts alone 16; planted file rc 1.
- docs-fragments check rc 0 ("64 new"); planted unclosed `<div>` in flow and cheat each rc 1; restored, rc 0 after.
- Node v26.8.1, not 24. node_modules cloned from gate 90's install (`npm ci` fails at current develop: lock file does not satisfy `@harmoniclabs/crypto` 0.3.1; pre-existing, not investigated).

## Mutants (scripts/mutants.py; ONE site per run, tests untouched, sha restored every run; logs/mutants_table.log)
24 runs (3 sites x M0 revert, M1 drop inner try, M2 constant->String(err), M3 rethrow only when unreadable, M4 constant for all, M5 rethrow after log, M6 readable non-Error branch -> 'x', M7 log removed): **24 killed, 0 survived**, all by AssertionError. M6 is killed by the committed string cell C2.

## merge-tree
`git merge-tree --write-tree origin/develop pr1916` rc 0, tree `df2142ce6349e8ea1ba76c3d0a6f7750f766ea3b`, clean; differs from develop in exactly the PR's 4 paths; 0 paths shared with the 28 files develop changed since the base.

## Notes for the PR body
1. (info) State the measured base behaviour: no response, hang, unhandled rejection, no log; head: constant 500 plus constant log, as for an Error (G98-F1).
2. (recommended) Name the follow-up unguarded reads in admin.ts (G98-F3).
3. (info) Raise the ORG_ADMIN/ISSUER_ADMIN reach of PATCH level as a separate card (G98-F4); say it was not changed.
4. (info) Optional route-level cell through requireAdmin (G98-F5).

## NOT TESTED
Real PostgreSQL / RLS; booted gateway; frontend; the real PR body; CI and pre-push hook legs (quoted from mail: 13/16 ran, 3 skipped, nothing failed); Node 24; the four platform suites; the isDbAvailable=true seed path (probe used false); whether a real unreadable throw occurs (all synthetic).
