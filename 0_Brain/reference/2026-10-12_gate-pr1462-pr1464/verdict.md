# QA gate verdicts, 2026-10-12 (tier 3, test/spec-text only). READ-ONLY; own clones in scratchpad.

Base for both: f5a2402. Vitest 4.1.11, tsc 5.9.3. Heads were absent from the l05 clone / l05b clone respectively; each fetched from the worktree that holds it (git archive into scratchpad; no ref writes anywhere in the shared repo).

## #1462 (KS-1193 F3) head f58dd9d1f6c68e9f2fc32a0b1e050e928515ed21 : GO WITH NOTE
1. Diff: exactly 1 file, +143 / -0 (new test, services/auth/src/__tests__/ks1193-f3-...test.ts). No runtime code.
2. Suite (services/auth): base f5a2402 = 84 files / 894 pass; head = 85 files / 898 pass, 0 fail (+4 = the four cells).
3. Plants (users.ts fallbacks -> null / null / []), full suite each, vs. own cell:
   - pending -> only RED PENDING red (1 failed). list -> only RED LIST red (1 failed). Control green in both.
   - by-id -> RED REVIEW red, PLUS ks467-user-admin-isolation.test.ts:400 and :408 (2 existing KS-467 cells) red, PLUS ks949 "real person is gone..." red once in the full run; ks949 passes alone under the same plant (2/2) and unplanted (3 full runs) = load flake, not caused by the plant (it also failed once in an unrelated first run).
   - Control cell green under all three plants.
4. "13 of 13 existing cells green": holds. 13 = ks1018 (6) + ks1193-review-read (3) + ks1193-codeless (4); none red under any plant.
5. tsc: project rc 0 (0 lines); new test file type-checked separately (tsconfig.json excludes src/__tests__, KS-1000) rc 0, control (planted `const zz: number = 'x'`) is caught.
Defects:
- Minor 1: "each removal reds only its own cell" is true inside the new file and the 13 cells, but suite-wide the by-id removal also reds ks467-user-admin-isolation.test.ts:400 and :408. The by-id fallback was already pinned by KS-467. Wording, not a hole.
- Minor 2: RED REVIEW (test file, the review cell) pins the stale-memory-approval behaviour; flagged in the cell title and header as KS-1018 item 3 (Kam's ruling). Acceptable; keep open for Kam.
- Note: ks949 flake under full-suite load (Error: STACK_TRACE_ERROR in the enumeration cell); pre-existing, not this PR.

## #1464 (KS-839 contract sentence) head 937c447f19b1445fff90bd976ab0afdb287bd7ae : NO GO (one Major, sentence over-promises)
1. Diff: 3 files, +65/-4 as described. yaml diff line by line = exactly two description hunks (secuura-api.yaml:18776 GET, :18919 POST, +9/-2); auth.openapi.ts +4/-2 (lines 2553, 2673); new test +52.
2. generate-openapi on head regenerates the yaml byte-identical to the committed one (cmp, md5 fdec5b8e...). check:openapi rc 0 (406 spec examples OK). Control: base yaml + head source -> rc 1 "generated YAML differs".
3. New test: 4 cells, base 2 failed / 2 passed (the two CONTROL cells green, two RED cells red), head 4 pass. Suite: base 894 / head 898 pass, 0 fail. tsc project rc 0; new test file separately rc 0.
4. Truth vs code: TRUE: allow-list holding `*` incl. padded entries (` *`, `openid,*`) -> services/oauth.ts:353 returns []; named scopes + empty grant -> routes/oauth.ts:422 refuses 400 invalid_scope; omitted scope -> default = allow-list -> [] -> ok:true with empty grant, code stores '' and the token carries scopes [] with authMethod oauth (jwt.ts:203). Same resolver for GET and POST. Ticket text: KS-839 Done-when "the wildcard's meaning is stated in the published contract"; Kam's ruling text ("'*' grants no scopes") is cited by the test header but is not in raw_ks_issues.json (comments are ids only) - unverified by me.
Defects:
- **Major 1** auth.openapi.ts:2554 and :2674 (yaml 18780, 18926): "the gateway answers 403 on it" is unconditional and false. The 403 applies only to scope-gated gateway routes (requireScope: proxy.ts:445,464,638,645,855,861; requireScopeOrRole :807, which admits by ROLE during the KS-843 grace). Counter-example: proxy.ts:450 `/api/users/me` has no scope gate, so the empty-scope token passes. ks835-oauth-mint-carries-granted-scope.test.ts:203 itself says "refuses every scope-gated route". No cell drives a gateway 403 for this token; the new test only string-matches the phrase (ks839-contract-...test.ts:37,49), so it locks the overstatement in. Fix: "...and every scope-gated gateway route answers 403 on it" (or drop the clause: the ruling is "grants no scopes").
- Minor 2 ks839-contract-...test.ts header ("this service's build compiles __tests__"): false, tsconfig.json excludes src/__tests__ (KS-1000). Comment only.
- Minor 3 sentence says an app "whose registered allow-list contains `*`"; the create/update schemas are z.enum(AVAILABLE_SCOPES) so such apps exist only as legacy rows. Not wrong, but an integrator cannot register one; consider "a legacy app".

Not checked: Kam's ruling comment body (not in the raw export); CI/lint (eslint not run); whole-repo suites other than services/auth.
