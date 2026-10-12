# GATE PR #1484 (KS-695 ask 3 part i) — verdict: NO GO (one Major, fix is one line)

Head `59158be205a663fb83e7b487d8bae27d10ce5b8b` (bundle sha256/16 a2f25547a6645826 verified; 1 commit on 524db0ce6).
Predicted merge: develop tip `6fa9bf7bd7863c6e0830f1a48d513cde8169d034` (newest origin/develop found, worktree s-f17-ks1317; 9 commits past base), merges clean (yaml + gateway index.ts auto-merged).
Scope: 9 files, +1002/-1, all KS-695 (gateway door + proxyPaths, originate router/service/spec, yaml, 2 tests).

## Defects
1. **Major — `packages/shared` suite RED on head AND merged tree** (1 failed / 948). `ks764-key-revoke-call-site-guard.test.ts` ("no file mentions svc_api_keys + is_active except the call sites and a NAMED allowlist") now finds `services/originate/src/originate.openapi.ts`: the PR adds the literal `svc_api_keys` at originate.openapi.ts:3673 (keyId description) to a file that already says `is_active` 4x. Controls: base and develop tip have 0 mentions; rewording that one word → 15/15 green; restored. Seat's "full suites twice" is wrong for shared. Fix: reword, or add a NON_REVOKE_MENTIONS entry with a reason.
2. **Minor — the door comment's claim is false** (proxy.ts:849-851 "nothing else forwards /api/platform to originate"). `router.use('/originate/', proxy('originate', {'^/originate': ''}))` (proxy.ts ~1219, no auth) forwards `POST /originate/api/platform/organizations/erase-connector` (also `/ORIGINATE/...`, and the GET) to originate with the scope gate skipped, flag ENFORCING, role-only principal: 200, upstream saw `/api/platform/organizations/erase-connector`. Same holds for `/originate/api/gdpr/erasures` already, so this is an old problem the PR inherits, not one it introduces. Mitigated: nginx.conf:224 and nginx-demo.conf:457 answer `/originate/` 404 (KS-1041); originate still requires a connector JWT plus the organisation and key checks; with grace ON the door admits a role-only connector anyway. Correct the comment and ticket the passthrough before KS-843 enforcement.
3. **Minor — refusal shape differs from the design note and the brief.** externalRef or key crossings answer **403 FORBIDDEN** (platformOrganizations.ts:63-68), not a 200 `unresolvable`/`denied` (design note line 23, "Any disagreement is `unresolvable`"). This matches ask 1 (gdpr.ts) and the spec, and it is not a 5xx. But "S takes 403 as terminal" is asserted, not verified (no S client in reach). Either reconcile the design note or confirm with S.
4. **Minor — test gap.** No mixed-case `svc_api_keys.organization_id` cell: mutant M11 (drop normalise on the key org) survives. The surviving behaviour fails closed.

## Notes
- Answering a valid request with 501 is a 5xx, so S retries without bound, the same as today's 404. Do not deploy before part (ii) and Q1.
- The door's spelling cell also passes with NO door (a miss reaches nothing), so it is not a red test on its own.
- My RED counts: always-501 stub 25 failed / 1 passed (seat says 24/2); door removed 4 failed / 2 passed (seat says 5/1, probably because the seat also removed the proxyPaths entry). The difference comes from the stub. Every failure is red as expected.

## Attack results (originate auth rule) — holds
- Target = caller's org from claims. Org-less key → 200 unresolvable/org_less_key. NULL-org key row, other org's key, same org but another connector's key, unknown key → identical 403 body (sendRefusal ignores which check failed). Mixed case is normalised. Blank or oversize values → 400 before the db. Organisation with no stored externalRef → only the K id matches. Nothing in either file writes (the fake db recorded 0 executes).
- My door probes (16 spellings, identical on head and merged): absolute-form `http://evil/api/platform/...` / `HTTP://h/API/...` / GET → 403 with nothing sent upstream (express's mount matches the parsed path). `;x=1`, `%2D`, `%2F`, `./`, `x/../`, `%00` → 404. `/api/gdpr/../platform` and `%2e%2e` → 400. `#frag` → 403. The positive control (scope holder) reaches upstream through both the plain and the absolute-form path.

## Mutations (each applied, run, restored byte-identical by sha)
Seat-class and mine. RED: M1 key-org check dropped (2 failed), M2 key-connector check (1), M3 key tenant bind (1), M4 K-id arm (1), M5b externalRef accepts anything (4), M7c org-less key trusts externalRef (2), M8 org-less answered as 503 (2), M9b POST swallows the key refusal (3), M10 GET role dropped (1), M13 crossing answered 200 (7), M14 valid answered 200 (2), M6c unknown vs foreign key disclosed in body (1). Survived: M11 (gap, defect 4), M12 (drop claimed-null guard: equivalent, because zod trims and requires min 1), M6/M6b (equivalent: both key cases raise the same error). M5/M7/M9 first spellings failed to compile and were re-run as b/c.

## Suites (my runs; head | merged)
originate jest 1133/1133 | 1140/1140; gateway vitest 973/973 | 1025/1025; shared 948/949 RED | 948/949 RED (defect 1); tsc originate+gateway 0 | 0; eslint originate+gateway 0 | 0; check:openapi exit 0 | 0. PR cells: 26/26 and 6/6 on both trees.
Caveat: node_modules were symlinked from worktree s-f17-ks1317, so `@secuura/shared` resolves to that worktree's build. The PR does not touch shared.
Evidence in this folder: suites_*.txt, shared_ks764_red_head.txt, door_probe_head.txt, gate-door-probe.test.ts.txt.
